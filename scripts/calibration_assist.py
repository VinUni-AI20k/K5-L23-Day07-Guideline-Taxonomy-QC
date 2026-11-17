"""Build an evidence-linked calibration triage table and crops; never edits source labels.

    python scripts/calibration_assist.py
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple

from PIL import Image, ImageDraw

from common import IMAGES_DIR, QC_DIR, WORK_DIR, Obj, Taxonomy, iou, load_all_labels, load_taxonomy, read_csv

OUTPUT_COLUMNS = [
    "case_id", "image", "issue_type", "annotators",
    "annotation_a_id", "annotation_a_match_iou", "class_a", "bbox_a_xywh", "attributes_a",
    "annotation_b_id", "annotation_b_match_iou", "class_b", "bbox_b_xywh", "attributes_b",
    "reported_iou", "recomputed_iou", "triage_evidence", "proposal",
    "guideline_reference", "triage_confidence", "visual_review_file",
]
BOX_RE = re.compile(r"^\[\s*([0-9.,\s-]+)\s*\]$")


def parse_box(value: str) -> Optional[Tuple[float, float, float, float]]:
    if not value:
        return None
    match = BOX_RE.fullmatch(value.strip())
    if not match:
        raise ValueError(f"Invalid candidate bbox: {value!r}")
    values = [float(part.strip()) for part in match.group(1).split(",")]
    if len(values) != 4:
        raise ValueError(f"Candidate bbox must have four coordinates: {value!r}")
    x, y, width, height = values
    return x, y, x + width, y + height


def find_annotation(objects: List[Obj], box: Optional[Tuple[float, float, float, float]],
                    class_name: str) -> Optional[Obj]:
    if box is None:
        return None
    choices = [obj for obj in objects if not class_name or obj.cls == class_name]
    if not choices:
        return None
    best = max(choices, key=lambda obj: iou(box, obj.box))
    return best if iou(box, best.box) >= 0.5 else None


def format_xywh(box: Optional[Tuple[float, float, float, float]]) -> str:
    if box is None:
        return ""
    x1, y1, x2, y2 = box
    return json.dumps([round(x1, 2), round(y1, 2), round(x2 - x1, 2), round(y2 - y1, 2)])


def format_attrs(obj: Optional[Obj]) -> str:
    return "" if obj is None else json.dumps(obj.attrs, ensure_ascii=False, sort_keys=True)


def rule_hint(row: dict) -> str:
    issue = row["issue_type"]
    if issue == "iou_thap":
        return "R-01: đối chiếu box với phần nhìn thấy; không lấy trung bình box thay cho kiểm ảnh."
    if issue == "sai_thuoc_tinh":
        return "Mục 2.2: kiểm occluded_level/truncated theo định nghĩa và phần nhìn thấy."
    if issue == "bat_dong_ignore":
        return "R-09: kiểm đối tượng/vùng ignore và ngưỡng kích thước tối thiểu 20 px."
    if issue == "co_can_review":
        return "Mục 2.2: xác định lý do gắn can_review và chỉ gỡ cờ sau quyết định."
    if issue == "sai_lop":
        if "tuk_tuk" in {row["class_a"], row["class_b"]}:
            return "R-04: phân biệt tuk_tuk, motorcycle và bicycle theo taxonomy."
        if "bicycle" in {row["class_a"], row["class_b"]}:
            return "R-05: xe đạp/xích lô thuộc bicycle; kiểm tách person."
        return "Mục 2.1: đối chiếu định nghĩa và phản ví dụ car/truck/van/bus."
    if "bicycle" in {row["class_a"], row["class_b"]}:
        return "R-05: kiểm xe đạp/xích lô và box person riêng."
    if "person" in {row["class_a"], row["class_b"]} or "motorcycle" in {row["class_a"], row["class_b"]}:
        return "R-02: kiểm tách riêng người và phương tiện."
    return "Đối chiếu định nghĩa lớp và quy tắc theo ảnh trong guideline v1.0."


def proposal_for(row: dict, box_a: Optional[Tuple[float, float, float, float]],
                 box_b: Optional[Tuple[float, float, float, float]], obj_a: Optional[Obj],
                 obj_b: Optional[Obj], overlap: Optional[float]) -> Tuple[str, str, str]:
    issue = row["issue_type"]
    evidence_parts = []
    if obj_a:
        evidence_parts.append(f"A=#{obj_a.id} {obj_a.cls} attrs={format_attrs(obj_a)}")
    elif box_a:
        evidence_parts.append("A: candidate bbox has no exact class-matched COCO annotation")
    if obj_b:
        evidence_parts.append(f"B=#{obj_b.id} {obj_b.cls} attrs={format_attrs(obj_b)}")
    elif box_b:
        evidence_parts.append("B: candidate bbox has no exact class-matched COCO annotation")
    if overlap is not None:
        evidence_parts.append(f"recomputed IoU={overlap:.3f}")

    if issue == "bo_sot_thua":
        available = box_a or box_b
        h = (available[3] - available[1]) if available else None
        size_note = f" reported box height={h:.0f}px." if h is not None else ""
        proposal = (
            "Compare this one-sided box with the original image, v1.0 scope and any ignore_region; "
            "if the visible in-scope object is confirmed, amend the missing/extra side by team decision; "
            "otherwise document why it is excluded."
            + size_note
        )
        confidence = "High for presence of an annotation disagreement; no confidence assigned to which side is correct."
    elif issue == "sai_lop":
        proposal = (
            "Geometry indicates a class disagreement. Inspect the original object and apply the relevant "
            "taxonomy definition; retain both source labels until the group selects the correct class."
        )
        confidence = "High for class-conflict triage; no class winner inferred."
    elif issue == "sai_thuoc_tinh":
        proposal = (
            "Compare the recorded attribute values against visible occlusion/cropping in the original; "
            "record the selected value only after image review."
        )
        confidence = "High for attribute-conflict triage; correctness requires image review."
    elif issue == "iou_thap":
        proposal = (
            "Inspect the original boundary and visible extent; apply R-01 to decide whether either source box needs correction."
        )
        confidence = "High that the script flagged a geometric disagreement; correctness requires image review."
    elif issue == "bat_dong_ignore":
        proposal = (
            "Inspect the candidate object and ignore boxes in the original; apply the 20px/ignore guidance "
            "and check whether the region actually covers the object."
        )
        confidence = "High for ignore-region disagreement triage; outcome needs visual review."
    else:
        proposal = (
            "Inspect the flagged annotation and its context; resolve the uncertainty using v1.0, "
            "then remove can_review only after the group decision and recheck."
        )
        confidence = "High that can_review was flagged; outcome needs visual review."
    return " | ".join(evidence_parts), proposal, confidence


def draw_case_crop(image_name: str, case_id: str, box_a, box_b, obj_a, obj_b,
                   member_a: str, member_b: str, output: Path) -> None:
    with Image.open(IMAGES_DIR / image_name) as source:
        image = source.convert("RGB")
    boxes = [box for box in (box_a, box_b) if box is not None]
    if not boxes:
        image.save(output, quality=88)
        return
    width, height = image.size
    left = min(box[0] for box in boxes)
    top = min(box[1] for box in boxes)
    right = max(box[2] for box in boxes)
    bottom = max(box[3] for box in boxes)
    margin = max(40, int(max(right - left, bottom - top) * 0.15))
    crop = image.crop((max(0, int(left - margin)), max(0, int(top - margin)),
                       min(width, int(right + margin)), min(height, int(bottom + margin))))
    draw = ImageDraw.Draw(crop)
    origin_x, origin_y = max(0, int(left - margin)), max(0, int(top - margin))
    for box, obj, member, color in (
        (box_a, obj_a, member_a, (230, 25, 75)),
        (box_b, obj_b, member_b, (60, 120, 255)),
    ):
        if box is None:
            continue
        local = (box[0] - origin_x, box[1] - origin_y, box[2] - origin_x, box[3] - origin_y)
        draw.rectangle(local, outline=color, width=4)
        annotation_id = f" #{obj.id}" if obj else ""
        caption = f"{case_id} {member}{annotation_id} {obj.cls if obj else ''}".strip()
        text_y = max(0, int(local[1]) - 17)
        draw.rectangle((local[0], text_y, local[0] + max(130, len(caption) * 7), text_y + 17), fill=color)
        draw.text((local[0] + 3, text_y + 2), caption, fill=(255, 255, 255))
    output.parent.mkdir(parents=True, exist_ok=True)
    crop.save(output, quality=88)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=QC_DIR / "calibration_proposals.csv")
    args = parser.parse_args()

    taxonomy: Taxonomy = load_taxonomy()
    labels = load_all_labels(taxonomy)
    candidates = read_csv(QC_DIR / "calibration_candidates.csv")
    crop_dir = WORK_DIR / "calibration_review" / "cases"
    output_rows = []
    for row in candidates:
        image_name = row["image"]
        members = [member.strip() for member in row["annotators"].split("|") if member.strip()]
        if image_name not in labels[members[0]].objects:
            raise ValueError(f"{row['case_id']}: image {image_name} absent from annotator {members[0]}")
        box_a, box_b = parse_box(row["box_a"]), parse_box(row["box_b"])
        objects_a = labels[members[0]].objects[image_name]
        obj_a = find_annotation(objects_a, box_a, row["class_a"])
        obj_b = None
        if len(members) > 1 and image_name in labels[members[1]].objects:
            obj_b = find_annotation(labels[members[1]].objects[image_name], box_b, row["class_b"])
        overlap = iou(box_a, box_b) if box_a is not None and box_b is not None else None
        evidence, proposal, confidence = proposal_for(row, box_a, box_b, obj_a, obj_b, overlap)
        visual_path = crop_dir / f"{row['case_id']}.jpg"
        draw_case_crop(image_name, row["case_id"], box_a, box_b, obj_a, obj_b,
                       members[0], members[1] if len(members) > 1 else "", visual_path)
        output_rows.append({
            "case_id": row["case_id"], "image": image_name, "issue_type": row["issue_type"],
            "annotators": row["annotators"],
            "annotation_a_id": obj_a.id if obj_a else "",
            "annotation_a_match_iou": f"{iou(box_a, obj_a.box):.4f}" if box_a and obj_a else "",
            "class_a": obj_a.cls if obj_a else row["class_a"],
            "bbox_a_xywh": format_xywh(box_a), "attributes_a": format_attrs(obj_a),
            "annotation_b_id": obj_b.id if obj_b else "",
            "annotation_b_match_iou": f"{iou(box_b, obj_b.box):.4f}" if box_b and obj_b else "",
            "class_b": obj_b.cls if obj_b else row["class_b"],
            "bbox_b_xywh": format_xywh(box_b), "attributes_b": format_attrs(obj_b),
            "reported_iou": row["iou"],
            "recomputed_iou": "" if overlap is None else f"{overlap:.4f}",
            "triage_evidence": evidence, "proposal": proposal,
            "guideline_reference": rule_hint(row),
            "triage_confidence": confidence,
            "visual_review_file": str(visual_path.relative_to(WORK_DIR.parent)),
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"Cases analyzed: {len(output_rows)}")
    print(f"Proposal table: {args.output}")
    print(f"Case crops: {crop_dir} ({len(output_rows)} images)")
    print("All entries are triage proposals only; no source annotation or calibration decision was changed.")


if __name__ == "__main__":
    main()
