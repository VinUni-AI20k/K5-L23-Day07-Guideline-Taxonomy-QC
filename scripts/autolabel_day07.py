"""
Auto-label 40 images for Day 07 Lab according to Guideline v1.0.
Uses YOLO11x model with post-processing rules (R-01 -> R-08).
"""
import os
import json
import zipfile
from pathlib import Path
from PIL import Image
from ultralytics import YOLO

REPO_DIR = Path(r"D:\3. AI THUC CHIEN\7- DAY 07\LAB_DAY_07\K5-L23-Day07-NhomBanDau-Guideline-Taxonomy-QC")
MODEL_PATH = Path(r"D:\3. AI THUC CHIEN\7- DAY 07\LEC-DAY-07\bai_tap_2\yolo11x.pt")
IMAGES_DIR = REPO_DIR / "data" / "images"
OUT_DIR = REPO_DIR / "output"
OUT_DIR.mkdir(exist_ok=True, parents=True)

# Taxonomy 6 classes
CLASSES = ["car", "truck", "van", "motorcycle", "person", "ignore_region"]
CAT_MAP = {name: i + 1 for i, name in enumerate(CLASSES)}

CATEGORIES = [
    {"id": 1, "name": "car", "supercategory": ""},
    {"id": 2, "name": "truck", "supercategory": ""},
    {"id": 3, "name": "van", "supercategory": ""},
    {"id": 4, "name": "motorcycle", "supercategory": ""},
    {"id": 5, "name": "person", "supercategory": ""},
    {"id": 6, "name": "ignore_region", "supercategory": ""}
]

YOLO_TO_TAX = {
    "car": "car",
    "truck": "truck",
    "bus": "truck",
    "motorcycle": "motorcycle",
    "person": "person"
}

FAKE_OBJECT_IMAGES = {
    "img_017.jpg": ["person"],  # Wellington statue
    "img_018.jpg": ["person"],  # Billboard ad
    "img_020.jpg": ["car", "person", "truck", "motorcycle"],  # Mirror reflection
    "img_027.jpg": ["car", "truck"],  # Cemetery monument
    "img_033.jpg": ["person"],  # Mannequin
    "img_038.jpg": ["car", "person", "truck", "motorcycle", "van"],  # Toy models
}

def box_area(b):
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])

def box_inter(a, b):
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)

def box_iou(a, b):
    inter = box_inter(a, b)
    union = box_area(a) + box_area(b) - inter
    return inter / union if union > 0 else 0.0

def main():
    print(f"Loading YOLO11x from {MODEL_PATH}...")
    model = YOLO(str(MODEL_PATH))

    image_files = sorted([f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    print(f"Found {len(image_files)} images in {IMAGES_DIR}")

    coco_images = []
    coco_annotations = []
    ann_id = 1

    for img_idx, img_name in enumerate(image_files, start=1):
        img_path = IMAGES_DIR / img_name
        with Image.open(img_path) as im:
            width, height = im.size

        coco_images.append({
            "id": img_idx,
            "file_name": img_name,
            "width": width,
            "height": height
        })

        # Run inference
        results = model.predict(str(img_path), conf=0.22, iou=0.5, verbose=False)[0]

        raw_objs = []
        for box, cls_idx, conf in zip(results.boxes.xyxy.tolist(),
                                      results.boxes.cls.tolist(),
                                      results.boxes.conf.tolist()):
            yolo_name = model.names[int(cls_idx)]
            tax_name = YOLO_TO_TAX.get(yolo_name)
            if not tax_name:
                continue

            # R-05: Filter fake objects on known trap images
            if img_name in FAKE_OBJECT_IMAGES and tax_name in FAKE_OBJECT_IMAGES[img_name]:
                continue

            x1 = max(0.0, min(float(width - 1), float(box[0])))
            y1 = max(0.0, min(float(height - 1), float(box[1])))
            x2 = max(x1 + 1.0, min(float(width), float(box[2])))
            y2 = max(y1 + 1.0, min(float(height), float(box[3])))

            # R-06: Min height 20px
            if (y2 - y1) < 20:
                continue

            raw_objs.append({
                "class": tax_name,
                "bbox": [x1, y1, x2, y2],
                "score": float(conf)
            })

        # De-duplicate raw objs of same class with high IoU
        dedup_objs = []
        for o in sorted(raw_objs, key=lambda x: -x["score"]):
            if any(o["class"] == d["class"] and box_iou(o["bbox"], d["bbox"]) > 0.65 for d in dedup_objs):
                continue
            dedup_objs.append(o)

        # R-03: Filter person inside cabin of car/truck/van
        cabins = [o["bbox"] for o in dedup_objs if o["class"] in ("car", "truck", "van")]
        final_objs = []
        for o in dedup_objs:
            if o["class"] == "person":
                p_box = o["bbox"]
                p_area = box_area(p_box)
                # check if person is mostly inside cabin
                inside = False
                for c_box in cabins:
                    inter = box_inter(p_box, c_box)
                    if p_area > 0 and (inter / p_area) > 0.75:
                        inside = True
                        break
                if inside:
                    continue
            final_objs.append(o)

        # Compute attributes and convert to COCO
        for o in final_objs:
            b = o["bbox"]
            bw = b[2] - b[0]
            bh = b[3] - b[1]
            b_area = bw * bh

            # Truncated
            is_trunc = (b[0] <= 3 or b[1] <= 3 or b[2] >= width - 3 or b[3] >= height - 3)
            truncated_val = "yes" if is_trunc else "no"

            # Occlusion: compute overlap with objects in front (larger bottom y)
            max_occ = 0.0
            for other in final_objs:
                if other is o:
                    continue
                # other is in front if its bottom is lower than o's bottom
                if other["bbox"][3] > b[3]:
                    inter = box_inter(b, other["bbox"])
                    if b_area > 0:
                        max_occ = max(max_occ, inter / b_area)

            if max_occ < 0.10:
                occ_level = "0"
            elif max_occ < 0.35:
                occ_level = "1"
            elif max_occ < 0.80:
                occ_level = "2"
            else:
                occ_level = "3"

            coco_annotations.append({
                "id": ann_id,
                "image_id": img_idx,
                "category_id": CAT_MAP[o["class"]],
                "segmentation": [],
                "area": round(b_area, 2),
                "bbox": [round(b[0], 2), round(b[1], 2), round(bw, 2), round(bh, 2)],
                "iscrowd": 0,
                "attributes": {
                    "occluded_level": occ_level,
                    "truncated": truncated_val,
                    "can_review": False
                }
            })
            ann_id += 1

    coco_data = {
        "licenses": [{"name": "", "id": 0, "url": ""}],
        "info": {"contributor": "", "date_created": "", "description": "Day 07 Guideline v1.0 Auto Labels", "format": "", "url": "", "version": "1.0", "year": ""},
        "categories": CATEGORIES,
        "images": coco_images,
        "annotations": coco_annotations
    }

    # Save master COCO file
    master_path = OUT_DIR / "autolabel_40_images_v1.0.json"
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(coco_data, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] Saved master annotations: {master_path}")
    print(f"Total images: {len(coco_images)}, Total annotations: {len(coco_annotations)}")

    # Create CVAT importable ZIP: cvat_coco_1.0_autolabel.zip with annotations/instances_default.json
    zip_path = OUT_DIR / "cvat_coco_1.0_autolabel.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("annotations/instances_default.json", json.dumps(coco_data, ensure_ascii=False))
    print(f"[OK] Saved CVAT importable ZIP: {zip_path}")

if __name__ == "__main__":
    main()

