"""
Script tự động gán nhãn bằng mô hình Object Detection và xuất file .ZIP chuẩn COCO 1.0 để nạp lên CVAT.
Đã cập nhật theo Taxonomy v1.0:
    - car, truck, van, motorcycle, bicycle, other_vehicle, person, rider, ignore_region

Cách dùng:
    python scripts/auto_label_cvat.py --member 042
    python scripts/auto_label_cvat.py --member 069 --conf 0.35
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import zipfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_DIR = Path(r"C:\Users\GIA KHANG\Downloads\models")
DEFAULT_MEMBER = "042"
TAXONOMY_PATH = ROOT / "submission" / "taxonomy.json"
DEFAULT_IMAGES_DIR = ROOT / "data" / "images"
LABELS_OUTPUT_DIR = ROOT / "submission" / "labels"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--member", type=str, default=DEFAULT_MEMBER, help="Mã thành viên 3 chữ số.")
    parser.add_argument("--model-dir", type=Path, default=DEFAULT_MODEL_DIR, help="Thư mục chứa model.")
    parser.add_argument("--model-path", type=Path, default=None, help="Đường dẫn trực tiếp tới file model (.pt).")
    parser.add_argument("--images-dir", type=Path, default=DEFAULT_IMAGES_DIR, help="Thư mục chứa ảnh.")
    parser.add_argument("--conf", type=float, default=0.35, help="Ngưỡng confidence score (mặc định: 0.35).")
    parser.add_argument("--min-size", type=int, default=20, help="Ngưỡng kích thước tối thiểu px (mặc định: 20).")
    return parser.parse_args()


def find_model_path(model_path: Path | None, model_dir: Path) -> Path:
    if model_path and model_path.is_file():
        return model_path

    if not model_dir.is_dir():
        sys.exit(f"[LỖI] Không tìm thấy thư mục model: {model_dir}")

    candidates = list(model_dir.glob("*.pt")) + list(model_dir.glob("*.onnx"))
    if not candidates:
        sys.exit(f"[LỖI] Không tìm thấy file model (.pt hoặc .onnx) nào trong {model_dir}")

    chosen = candidates[0]
    print(f"[INFO] Tự động chọn file model: {chosen.name}")
    return chosen


def get_target_images(images_dir: Path, member: str) -> list[Path]:
    assignment_txt = ROOT / "submission" / "qc" / "assignments" / f"{member}.txt"
    if assignment_txt.is_file():
        assigned_names = [line.strip() for line in assignment_txt.read_text(encoding="utf-8").splitlines() if line.strip()]
        images = [images_dir / name for name in assigned_names if (images_dir / name).is_file()]
        if images:
            print(f"[INFO] Tìm thấy phân công trong {assignment_txt.name}: {len(images)} ảnh.")
            return sorted(images)

    all_imgs = sorted(list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.jpeg")) + list(images_dir.glob("*.png")))
    if not all_imgs:
        sys.exit(f"[LỖI] Không tìm thấy ảnh nào trong {images_dir}")
    print(f"[INFO] Gán nhãn cho toàn bộ {len(all_imgs)} ảnh trong {images_dir.name}.")
    return all_imgs


def load_taxonomy_categories() -> tuple[dict[str, int], list[dict]]:
    if not TAXONOMY_PATH.is_file():
        sys.exit(f"[LỖI] Không tìm thấy taxonomy tại: {TAXONOMY_PATH}")

    with TAXONOMY_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    cat_to_id = {}
    categories_coco = []
    for idx, item in enumerate(data.get("classes", []), start=1):
        name = item["name"]
        cat_to_id[name.lower()] = idx
        categories_coco.append({
            "id": idx,
            "name": name,
            "supercategory": "none",
        })
    return cat_to_id, categories_coco


def is_overlapping(box_a: tuple[float, float, float, float], box_b: tuple[float, float, float, float]) -> bool:
    xa1, ya1, xa2, ya2 = box_a
    xb1, yb1, xb2, yb2 = box_b

    inter_w = max(0.0, min(xa2, xb2) - max(xa1, xb1))
    inter_h = max(0.0, min(ya2, yb2) - max(ya1, yb1))
    inter_area = inter_w * inter_h
    if inter_area <= 0:
        return False

    area_a = (xa2 - xa1) * (ya2 - ya1)
    return (inter_area / area_a) >= 0.10


def main() -> None:
    args = parse_args()

    try:
        from ultralytics import YOLO
    except ImportError:
        sys.exit("[LỖI] Chưa cài đặt thư viện 'ultralytics'. Vui lòng chạy lệnh:\n    pip install ultralytics pillow")

    model_file = find_model_path(args.model_path, args.model_dir)
    image_paths = get_target_images(args.images_dir, args.member)
    cat_to_id, categories_coco = load_taxonomy_categories()

    print(f"[INFO] Đang nạp weights từ: {model_file.name} ...")
    model = YOLO(str(model_file))

    images_coco = []
    annotations_coco = []
    class_counter: dict[str, int] = {}
    ann_id = 1

    print(f"[INFO] Đang chạy phát hiện đối tượng trên {len(image_paths)} ảnh cho thành viên {args.member}...")

    for img_idx, img_path in enumerate(image_paths, start=1):
        with Image.open(img_path) as pil_img:
            w_img, h_img = pil_img.size

        images_coco.append({
            "id": img_idx,
            "file_name": img_path.name,
            "width": w_img,
            "height": h_img,
        })

        results = model.predict(source=str(img_path), conf=args.conf, verbose=False)
        result = results[0]

        raw_detections = []
        rideable_boxes = []

        for box in result.boxes:
            cls_id = int(box.cls[0].item())
            raw_name = model.names[cls_id].lower()
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            bw = x2 - x1
            bh = y2 - y1

            if bw < args.min_size or bh < args.min_size:
                continue

            raw_detections.append((raw_name, (x1, y1, x2, y2, bw, bh)))
            if raw_name in ("motorcycle", "motorbike", "bicycle", "bike", "other_vehicle"):
                rideable_boxes.append((x1, y1, x2, y2))

        for raw_name, (x1, y1, x2, y2, bw, bh) in raw_detections:
            target_class = None

            if raw_name in ("car",):
                target_class = "car"
            elif raw_name in ("truck",):
                target_class = "truck"
            elif raw_name in ("van",):
                target_class = "van" if "van" in cat_to_id else "truck"
            elif raw_name in ("motorcycle", "motorbike"):
                target_class = "motorcycle"
            elif raw_name in ("bicycle", "bike"):
                target_class = "bicycle"
            elif raw_name in ("bus", "other_vehicle"):
                target_class = "other_vehicle" if "other_vehicle" in cat_to_id else "truck"
            elif raw_name == "person":
                is_rider = any(is_overlapping((x1, y1, x2, y2), vb) for vb in rideable_boxes)
                if is_rider and "rider" in cat_to_id:
                    target_class = "rider"
                else:
                    target_class = "person"

            if not target_class or target_class not in cat_to_id:
                continue

            x1 = max(0.0, min(float(x1), float(w_img)))
            y1 = max(0.0, min(float(y1), float(h_img)))
            bw = min(float(bw), float(w_img) - x1)
            bh = min(float(bh), float(h_img) - y1)

            annotations_coco.append({
                "id": ann_id,
                "image_id": img_idx,
                "category_id": cat_to_id[target_class],
                "bbox": [round(x1, 2), round(y1, 2), round(bw, 2), round(bh, 2)],
                "area": round(bw * bh, 2),
                "iscrowd": 0,
                "attributes": {
                    "occluded_level": "0",
                    "truncated": "no",
                    "can_review": False,
                },
            })
            class_counter[target_class] = class_counter.get(target_class, 0) + 1
            ann_id += 1

    coco_result = {
        "images": images_coco,
        "categories": categories_coco,
        "annotations": annotations_coco,
    }

    LABELS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = LABELS_OUTPUT_DIR / f"{args.member}.json"
    zip_path = LABELS_OUTPUT_DIR / f"{args.member}_cvat_coco.zip"

    json_text = json.dumps(coco_result, indent=2, ensure_ascii=False)
    json_path.write_text(json_text, encoding="utf-8")
    print(f"\n[OK] Đã lưu nhãn JSON: {json_path}")

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("annotations/instances_default.json", json_text)
    print(f"[OK] Đã đóng gói file ZIP cho CVAT: {zip_path}")

    print("\n" + "=" * 60)
    print(f"TỔNG KẾT KẾT QUẢ THÀNH VIÊN {args.member}:")
    print(f"- Số ảnh đã xử lý: {len(images_coco)}")
    print(f"- Tổng số bounding box: {len(annotations_coco)}")
    print("- Thống kê theo lớp:")
    for cname, count in sorted(class_counter.items()):
        print(f"    + {cname}: {count} boxes")
    print("=" * 60)
    print("\nBƯỚC TIẾP THEO:")
    print(f"1. Kiểm tra cấu trúc nhãn:")
    print(f"   python scripts/validate_labels.py submission/labels/{args.member}.json")
    print(f"2. Nạp lên CVAT:")
    print(f"   Vào Task trên CVAT -> Actions -> Upload annotations -> COCO 1.0 -> Chọn file '{zip_path.name}'.")


if __name__ == "__main__":
    main()
