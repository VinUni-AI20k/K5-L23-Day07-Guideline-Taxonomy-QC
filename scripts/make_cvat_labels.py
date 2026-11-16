"""Sinh JSON để dán vào CVAT (Project -> Labels -> tab Raw).

    python scripts/make_cvat_labels.py

Mặc định xuất bộ nhãn CVAT đã chốt và ghi ra cvat/labels_generated.json.
Thêm --final để sinh cấu hình trực tiếp từ taxonomy sau calibration.
"""
from __future__ import annotations

import argparse
import json

from common import ROOT, final_taxonomy_path, load_taxonomy, rel

COLORS = ["#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4", "#46c8c8", "#f032e6", "#9a6324",
          "#808000", "#008080", "#800000", "#000075"]

CVAT_LABELS = [
    ("car", 64, "#e6194b"),
    ("truck", 65, "#3cb44b"),
    ("van", 66, "#4363d8"),
    ("motorcycle", 67, "#f58231"),
    ("person", 68, "#911eb4"),
    ("ignore_region", 69, "#808080"),
    ("three_wheeler", 70, "#aaf0d1"),
    ("bus", 71, "#f59331"),
    ("bicycle", 72, "#f078f0"),
]

CVAT_ATTRIBUTES = [
    ("occluded_level", "select", ["0", "1", "2", "3"], "0"),
    ("truncated", "select", ["no", "yes"], "no"),
    ("can_review", "checkbox", ["false"], "false"),
]


def finalized_cvat_labels() -> list[dict]:
    """Tạo bộ nhãn CVAT có ID/màu cố định theo cấu hình đã chốt."""
    labels = []
    for name, label_id, color in CVAT_LABELS:
        attrs = []
        if name != "ignore_region":
            for attr_index, (attr_name, input_type, values, default) in enumerate(CVAT_ATTRIBUTES):
                attr = {
                    "name": attr_name,
                    "input_type": input_type,
                    "mutable": False,
                    "values": list(values),
                    "default_value": default,
                }
                # Các thuộc tính đã tồn tại trong CVAT mang ID 1–15; thuộc tính
                # trên ba nhãn mới được tạo sẽ để CVAT tự cấp ID.
                if 64 <= label_id <= 68:
                    attr["id"] = (label_id - 64) * len(CVAT_ATTRIBUTES) + attr_index + 1
                    attr = {"id": attr.pop("id"), **attr}
                attrs.append(attr)
        labels.append({
            "name": name,
            "id": label_id,
            "color": color,
            "type": "rectangle",
            "attributes": attrs,
        })
    return labels


def taxonomy_cvat_labels(tax) -> list[dict]:
    """Sinh cấu hình từ taxonomy, dùng cho tùy chọn --final."""
    labels = []
    for i, name in enumerate(tax.classes):
        attrs = []
        if name != tax.ignore:
            for a in tax.attrs.values():
                attrs.append({
                    "name": a["name"],
                    "mutable": False,
                    "input_type": a["type"],
                    "default_value": str(a.get("default", "")),
                    "values": [str(v) for v in a.get("values", [])] if a["type"] == "select" else [],
                })
        labels.append({"name": name, "color": "#808080" if name == tax.ignore else COLORS[i % len(COLORS)],
                       "attributes": attrs})
    return labels


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final", action="store_true", help="Sinh cấu hình cho taxonomy sau calibration.")
    args = parser.parse_args()
    if args.final:
        tax = load_taxonomy(final_taxonomy_path())
        labels = taxonomy_cvat_labels(tax)
        version = tax.version
    else:
        labels = finalized_cvat_labels()
        version = "CVAT fixed set"
    text = json.dumps(labels, ensure_ascii=False, indent=2)
    out = ROOT / "cvat" / ("labels_final.json" if args.final else "labels_generated.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(text + "\n", encoding="utf8")
    print(text)
    print(f"\n# Đã ghi {rel(out)} ({version}). Dán nội dung vào CVAT: Project -> Labels -> Raw -> Done.")


if __name__ == "__main__":
    main()
