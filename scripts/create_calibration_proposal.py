"""Create a review-only COCO calibration proposal and case-linked audit files."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from common import (
    QC_DIR, WORK_DIR, iou, label_errors, load_coco, load_taxonomy, read_csv,
    require_assignment, xywh_to_xyxy,
)

OUT_DIR = WORK_DIR / "calibration_review"
COCO_SOURCE = QC_DIR / "consensus_draft.json"
CANDIDATES = QC_DIR / "calibration_candidates.csv"
EVIDENCE = QC_DIR / "calibration_proposals.csv"
PROPOSED_COCO = OUT_DIR / "proposed_calibrated.json"
CASE_TABLE = OUT_DIR / "case_decisions.csv"
CHANGE_LOG = OUT_DIR / "annotation_change_log.json"
SUMMARY = OUT_DIR / "proposal_summary.md"

CASE_COLUMNS = [
    "priority", "case_id", "image", "annotators", "issue_type",
    "source_annotation_ids", "draft_annotation_ids", "proposed_action",
    "reason", "evidence", "confidence", "review_status",
]

Box = Tuple[float, float, float, float]


def parse_candidate_box(raw: str) -> Optional[Box]:
    if not raw:
        return None
    values = json.loads(raw)
    if len(values) != 4:
        raise ValueError(f"Expected xywh candidate box, got {raw!r}")
    x, y, width, height = (float(value) for value in values)
    return x, y, x + width, y + height


def read_proposal_evidence() -> List[dict]:
    with EVIDENCE.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def index_draft(coco: dict, taxonomy) -> Dict[str, List[dict]]:
    image_by_id = {image["id"]: image["file_name"] for image in coco["images"]}
    name_by_category = {category["id"]: category["name"] for category in coco["categories"]}
    result: Dict[str, List[dict]] = {}
    for source_annotation in coco["annotations"]:
        annotation = dict(source_annotation)
        image = image_by_id[annotation["image_id"]]
        annotation["_image_name"] = image
        annotation["_class_name"] = name_by_category[annotation["category_id"]]
        annotation["_xyxy"] = xywh_to_xyxy(annotation["bbox"])
        result.setdefault(image, []).append(annotation)
    if set(name_by_category.values()) != set(taxonomy.classes):
        raise ValueError("Consensus categories do not match the current taxonomy.")
    return result


def linked_draft_annotations(row: dict, draft_by_image: dict) -> List[dict]:
    candidates = [parse_candidate_box(row.get("box_a", "")), parse_candidate_box(row.get("box_b", ""))]
    candidates = [box for box in candidates if box is not None]
    available = draft_by_image.get(row["image"], [])
    links: Dict[int, dict] = {}
    for box in candidates:
        ranked = sorted(
            ((iou(box, annotation["_xyxy"]), annotation) for annotation in available),
            key=lambda item: (-item[0], item[1]["id"]),
        )
        if ranked and ranked[0][0] >= 0.3:
            links[ranked[0][1]["id"]] = ranked[0][1]
    return list(links.values())


def make_case_action(row: dict, linked: List[dict]) -> Tuple[int, str, str, str, str]:
    issue = row["issue_type"]
    linked_text = (
        "; ".join(
            f"draft #{ann['id']} {ann['_class_name']} bbox={ann['bbox']} attrs={ann['attributes']}"
            for ann in linked
        )
        if linked else "Không ánh xạ chắc chắn được candidate sang annotation trong consensus draft."
    )
    if issue == "bo_sot_thua":
        priority = 1
        action = "Giữ annotation draft; nhóm xác nhận giữ/bổ sung/bỏ đối tượng sau khi xem ảnh."
        reason = "IAA một phía không phân biệt được bỏ sót với gán thừa; không tự thêm hoặc xóa."
    elif issue == "sai_lop":
        priority = 1
        action = "Tạm giữ class trong consensus draft; nhóm chọn class đúng theo taxonomy sau khi xem ảnh."
        reason = "Bất đồng lớp không xác định bên nào đúng; không tự đổi class."
    elif issue == "iou_thap":
        priority = 2
        action = "Dùng bbox consensus làm box dự thảo; reviewer hiệu chỉnh biên theo R-01."
        reason = "Consensus draft là trung bình số học các box ghép; không chứng minh box ôm sát vật."
    elif issue == "sai_thuoc_tinh":
        priority = 2
        action = "Tạm giữ thuộc tính trong consensus draft; reviewer chốt theo phần nhìn thấy."
        reason = "Đồng thuận thuộc tính tự động không thay thế quan sát occlusion/truncation."
    elif issue == "bat_dong_ignore":
        priority = 1
        action = "Giữ nguyên draft; nhóm quyết định vùng ignore và các đối tượng cá thể liên quan."
        reason = "Bất đồng ignore có thể che giấu bỏ sót hoặc gom nhầm đối tượng."
    elif issue == "co_can_review":
        priority = 2
        action = "Giữ nguyên annotation/cờ hiện tại trong draft; chỉ gỡ cờ sau review."
        reason = "Cờ review báo tình huống chưa chắc chắn, không phải kết luận nhãn sai."
    else:
        priority = 1
        action = "Giữ draft và chuyển nhóm đối chiếu ảnh/guideline."
        reason = "Loại ca chưa có hành động tự động an toàn."
    confidence = "Thấp: ảnh chưa được review đầy đủ; trạng thái chỉ là đề xuất máy."
    evidence = (
        f"IAA candidate {row['case_id']}; annotators={row['annotators']}; "
        f"source classes={row['class_a']}|{row['class_b']}; "
        f"source boxes={row['box_a']}|{row['box_b']}; IoU={row['iou']}; "
        f"draft evidence: {linked_text}"
    )
    return priority, action, reason, evidence, confidence


def main() -> None:
    taxonomy = load_taxonomy()
    coco = json.loads(COCO_SOURCE.read_text(encoding="utf-8"))
    candidates = read_csv(CANDIDATES)
    evidence_by_id = {row["case_id"]: row for row in read_proposal_evidence()}
    if len(candidates) != 230 or len(evidence_by_id) != len(candidates):
        raise ValueError("Expected the existing 230-case IAA/evidence inputs without regenerating them.")
    if set(evidence_by_id) != {row["case_id"] for row in candidates}:
        raise ValueError("Calibration evidence case IDs do not match IAA candidates.")

    draft_by_image = index_draft(coco, taxonomy)
    decisions = []
    proposed_case_entries = []
    for row in candidates:
        evidence_row = evidence_by_id[row["case_id"]]
        linked = linked_draft_annotations(row, draft_by_image)
        priority, action, reason, evidence, confidence = make_case_action(row, linked)
        decisions.append({
            "priority": priority,
            "case_id": row["case_id"],
            "image": row["image"],
            "annotators": row["annotators"],
            "issue_type": row["issue_type"],
            "source_annotation_ids": "|".join(
                item for item in (evidence_row["annotation_a_id"], evidence_row["annotation_b_id"]) if item
            ),
            "draft_annotation_ids": "|".join(str(annotation["id"]) for annotation in linked),
            "proposed_action": action,
            "reason": reason,
            "evidence": evidence,
            "confidence": confidence,
            "review_status": "CHỜ NHÓM XÁC NHẬN",
        })
        proposed_case_entries.append({
            "case_id": row["case_id"],
            "image": row["image"],
            "issue_type": row["issue_type"],
            "draft_annotation_ids": [annotation["id"] for annotation in linked],
            "action": action,
            "review_status": "CHỜ NHÓM XÁC NHẬN",
        })

    decisions.sort(key=lambda item: (item["priority"], item["issue_type"], item["image"], item["case_id"]))
    issue_counts = Counter(row["issue_type"] for row in candidates)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    coco["info"] = {
        **coco.get("info", {}),
        "description": "Review-only calibration proposal copied from consensus_draft; not approved or final.",
        "proposal_status": "UNCONFIRMED - DO NOT USE AS FINAL LABELS",
        "source": "submission/qc/consensus_draft.json",
        "calibration_case_count": len(candidates),
    }
    PROPOSED_COCO.write_text(json.dumps(coco, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    expected_images = set(require_assignment())
    validated = load_coco(PROPOSED_COCO, taxonomy)
    if set(validated.images) != expected_images:
        raise ValueError(f"Proposal image set mismatch: {len(validated.images)} vs {len(expected_images)}.")
    category_ids = {category["id"]: category["name"] for category in coco["categories"]}
    if category_ids != {index + 1: name for index, name in enumerate(taxonomy.classes)}:
        raise ValueError("Proposal category IDs/order do not match the current taxonomy.")
    errors = label_errors(validated, taxonomy)
    if errors:
        raise ValueError("Proposed COCO failed validation:\n" + "\n".join(errors))
    small_boxes = [
        (image, obj.id, obj.cls, obj.box[3] - obj.box[1])
        for image, objects in validated.objects.items()
        for obj in objects
        if obj.cls != taxonomy.ignore and obj.box[3] - obj.box[1] < taxonomy.rules["min_box_height_px"]
    ]
    with CASE_TABLE.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CASE_COLUMNS)
        writer.writeheader()
        writer.writerows(decisions)
    CHANGE_LOG.write_text(json.dumps({
        "status": "UNCONFIRMED_PROPOSAL",
        "source_coco": "submission/qc/consensus_draft.json",
        "proposed_coco": str(PROPOSED_COCO.relative_to(WORK_DIR.parent)),
        "annotation_changes_applied": 0,
        "annotation_changes": [],
        "reason_no_changes": (
            "All 230 IAA cases are unresolved; available evidence cannot determine which label, box, "
            "attribute, omission, or ignore-region interpretation is correct. The proposal COCO preserves "
            "the existing consensus draft without changing annotation geometry, class, or taxonomy."
        ),
        "cases": proposed_case_entries,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = [
        "# Calibration proposal (chưa được nhóm xác nhận)",
        "",
        f"- Case table: `{CASE_TABLE.relative_to(WORK_DIR.parent)}` ({len(decisions)} cases; ordered by review priority).",
        f"- Proposed COCO: `{PROPOSED_COCO.relative_to(WORK_DIR.parent)}` (40-image consensus draft copy).",
        f"- Annotation edits applied: 0. The draft's categories, boxes and attributes were preserved.",
        f"- Cases awaiting group confirmation: {len(decisions)}.",
        f"- Structural validation: passed; {len(small_boxes)} object box below the {taxonomy.rules['min_box_height_px']}px minimum remains unchanged for review.",
        "- This is not `labels_calibrated.json`, a CVAT export, or an approved final dataset.",
        "- Manual visual verification: not complete for all cases; automated geometry/IAA evidence is not proof of object correctness.",
        "",
        "## Cases by issue type",
        "",
        "| Issue type | Cases |",
        "|---|---:|",
    ]
    summary.extend(f"| `{issue}` | {count} |" for issue, count in sorted(issue_counts.items()))
    summary.extend([
        "",
        "## Required next step",
        "",
        "The group should review the listed cases against original images and guideline v1.0, record confirmed decisions,",
        "then make/verify corrections in CVAT and export the exact version required by `prepare_calibration.py`.",
    ])
    SUMMARY.write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"Cases prepared: {len(decisions)}; awaiting group confirmation: {len(decisions)}.")
    print(f"Annotation edits applied: 0; preserved consensus draft as a separate review-only COCO proposal.")
    print(f"COCO structural validation passed; below-minimum object boxes: {len(small_boxes)}.")
    print(f"COCO: {PROPOSED_COCO}")
    print(f"Case decisions: {CASE_TABLE}")
    print(f"Change log: {CHANGE_LOG}")


if __name__ == "__main__":
    main()
