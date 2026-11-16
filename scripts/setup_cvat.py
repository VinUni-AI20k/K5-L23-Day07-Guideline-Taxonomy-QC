#!/usr/bin/env python3
"""Script phân việc và tạo Task cá nhân trên CVAT Local (http://localhost:8080).

CHỈ TẠO TASK KHI THÀNH VIÊN CHẠY ĐÚNG CÂU LỆNH VỚI HỌ TÊN VÀ MÃ SINH VIÊN:
    python scripts/setup_cvat.py "<Họ và tên>" <MSHV>

Ví dụ:
    python scripts/setup_cvat.py "NGUYỄN BÁ DUY" 2A202603192
    python scripts/setup_cvat.py "HOÀNG NHẬT ANH" 2A202603183
    python scripts/setup_cvat.py "PHẠM MẠNH HÙNG" 2A202603240
    python scripts/setup_cvat.py "ĐỖ HUY KIÊN" 2A202603216
    python scripts/setup_cvat.py "NGUYỄN ĐỨC CƯỜNG" 2A202603040
"""
from __future__ import annotations

import json
import logging
import re
import sys
import unicodedata
from getpass import getpass
from pathlib import Path

# Tắt cảnh báo log không cần thiết
logging.disable(logging.WARNING)

try:
    from cvat_sdk import make_client, models
    from cvat_sdk.core.proxies.tasks import ResourceType
except ImportError:
    print("LỖI: Chưa cài đặt thư viện 'cvat-sdk'. Chạy lệnh: pip install cvat-sdk", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = ROOT / "work"
TAXONOMY_PATH = ROOT / "submission" / "taxonomy.json"
CVAT_LABELS_PATH = ROOT / "cvat" / "labels_generated.json"
QC_ASSIGNMENTS_DIR = ROOT / "submission" / "qc" / "assignments"
ASSIGNMENT_CSV = ROOT / "submission" / "qc" / "assignment.csv"

SERVER_URL = "http://localhost:8080"
PROJECT_NAME = "Day07_T005"

# Danh sách chuẩn 5 thành viên của nhóm T005
TEAM_MEMBERS = {
    "2A202603040": "NGUYỄN ĐỨC CƯỜNG",
    "2A202603183": "HOÀNG NHẬT ANH",
    "2A202603192": "NGUYỄN BÁ DUY",
    "2A202603216": "ĐỖ HUY KIÊN",
    "2A202603240": "PHẠM MẠNH HÙNG",
}


def remove_accents(input_str: str) -> str:
    s = input_str.replace("Đ", "D").replace("đ", "d")
    nfkd_form = unicodedata.normalize('NFKD', s)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def to_slug(name: str) -> str:
    no_accent = remove_accents(name)
    words = re.findall(r"[A-Za-z0-9]+", no_accent)
    return "".join(w.capitalize() for w in words)


def normalize_compare(str1: str, str2: str) -> bool:
    s1 = re.sub(r"\s+", "", remove_accents(str1).lower())
    s2 = re.sub(r"\s+", "", remove_accents(str2).lower())
    return s1 == s2


def ensure_split_assign():
    """Đảm bảo phân phối 40 ảnh cho 5 thành viên (mỗi ảnh đúng 3 người gán, mỗi người 24 ảnh)."""
    if not ASSIGNMENT_CSV.exists() or not QC_ASSIGNMENTS_DIR.exists():
        import subprocess
        members_arg = ",".join(sorted(TEAM_MEMBERS.keys()))
        subprocess.run([
            sys.executable, str(ROOT / "scripts" / "split_assign.py"),
            "--members", members_arg, "--copy-images"
        ], check=True)


def get_or_create_project(client) -> int:
    """Tạo Project Day07_T005 nếu chưa có, dùng lại nếu đã có."""
    projects = [p for p in client.projects.list() if p.name == PROJECT_NAME]
    if projects:
        return projects[0].id

    print(f"[*] Đang khởi tạo Project '{PROJECT_NAME}' trên CVAT Local...")
    if not CVAT_LABELS_PATH.exists():
        import subprocess
        subprocess.run([sys.executable, str(ROOT / "scripts" / "make_cvat_labels.py")], check=True)

    with CVAT_LABELS_PATH.open(encoding="utf-8") as f:
        labels_data = json.load(f)

    label_reqs = [models.PatchedLabelRequest(**l) for l in labels_data]
    proj_spec = models.ProjectWriteRequest(name=PROJECT_NAME, labels=label_reqs)
    proj = client.projects.create(proj_spec)
    print(f"[+] Đã tạo Project '{PROJECT_NAME}' thành công (ID: {proj.id})")
    return proj.id


def main():
    raw_args = [a.strip() for a in sys.argv[1:] if not a.startswith("-")]

    if len(raw_args) < 2:
        print("\n" + "="*65)
        print("LỖI: Bạn phải nhập đủ Họ tên và Mã sinh viên để nhận việc!")
        print("="*65)
        print("Cú pháp:")
        print("    python scripts/setup_cvat.py \"<Họ và tên>\" <MSHV>")
        print("\nVí dụ các câu lệnh phân job cho nhóm T005:")
        for mshv, name in TEAM_MEMBERS.items():
            print(f'    python scripts/setup_cvat.py "{name}" {mshv}')
        print("="*65 + "\n")
        sys.exit(1)

    # Nhận diện tham số: cái nào là MSHV, cái nào là Họ tên
    mshv_input = None
    name_input = None

    for arg in raw_args:
        if re.search(r"2A\d+|\d{5,}", arg, re.IGNORECASE):
            mshv_input = arg.upper()
        else:
            name_input = arg if not name_input else f"{name_input} {arg}"

    if not mshv_input or not name_input:
        # Nếu không tự phân biệt được theo regex thì lấy thứ tự: arg 0 là tên, arg 1 là mshv
        name_input = raw_args[0]
        mshv_input = raw_args[1].upper()

    # Kiểm tra tính hợp lệ trong danh sách nhóm
    if mshv_input not in TEAM_MEMBERS:
        print(f"\n[LỖI] MSHV '{mshv_input}' không thuộc danh sách nhóm T005!", file=sys.stderr)
        print("Danh sách hợp lệ:", ", ".join(TEAM_MEMBERS.keys()), file=sys.stderr)
        sys.exit(1)

    expected_name = TEAM_MEMBERS[mshv_input]
    if not normalize_compare(name_input, expected_name):
        print(f"\n[CẢNH BÁO] Họ tên '{name_input}' không khớp với MSHV {mshv_input} ({expected_name}).")
        confirm = input(f"Bạn có muốn tiếp tục với tên chuẩn '{expected_name}'? (y/n): ").strip().lower()
        if confirm != "y":
            print("Đã hủy.")
            sys.exit(0)
        name_input = expected_name

    # 1. Đảm bảo ảnh đã được chia đủ
    ensure_split_assign()

    img_dir = WORK_DIR / mshv_input / "images"
    if not img_dir.exists():
        import shutil
        txt_path = QC_ASSIGNMENTS_DIR / f"{mshv_input}.txt"
        if not txt_path.exists():
            ensure_split_assign()
        assigned_imgs = [line.strip() for line in txt_path.read_text(encoding="utf8").splitlines() if line.strip()]
        img_dir.mkdir(parents=True, exist_ok=True)
        for img in assigned_imgs:
            shutil.copy2(ROOT / "data" / "images" / img, img_dir / img)

    images = sorted([str(p) for p in img_dir.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}])
    if not images:
        print(f"LỖI: Không tìm thấy ảnh trong {img_dir}", file=sys.stderr)
        sys.exit(1)

    slug_name = to_slug(expected_name)
    task_name = f"day07-{mshv_input}-{slug_name}"

    # 2. Kết nối tới CVAT Local
    print(f"\n[*] Đang kết nối tới CVAT Local ({SERVER_URL})...")
    client = make_client(
        SERVER_URL,
        credentials=(
            input("CVAT username: ").strip(),
            getpass("CVAT password: "),
        ),
    )

    project_id = get_or_create_project(client)

    # 3. Kiểm tra xem Task này đã được tạo trước đó chưa
    existing_tasks = [t for t in client.tasks.list() if t.name == task_name]
    if existing_tasks:
        task_id = existing_tasks[0].id
        task_url = f"{SERVER_URL}/tasks/{task_id}"
        print("\n" + "="*60)
        print(f"[!] BẠN ĐÃ CÓ TASK TRÊN CVAT LOCAL TỪ TRƯỚC:")
        print(f"  - Thành viên : {expected_name} ({mshv_input})")
        print(f"  - Tên task   : {task_name}")
        print(f"  - Task ID    : {task_id}")
        print(f"  - Link vào gán nhãn: {task_url}")
        print("="*60 + "\n")
        return

    # 4. Tạo duy nhất 1 Task cho người vừa chạy câu lệnh
    print("\n" + "="*60)
    print(f"[*] BẮT ĐẦU TẠO TASK CHO THÀNH VIÊN:")
    print(f"  - Họ và tên   : {expected_name}")
    print(f"  - Mã sinh viên: {mshv_input}")
    print(f"  - Số lượng ảnh: {len(images)} ảnh (đúng 24 ảnh được phân)")
    print(f"[*] Đang tải {len(images)} ảnh lên CVAT Local...")
    print("="*60)

    spec = models.TaskWriteRequest(name=task_name, project_id=project_id)
    task = client.tasks.create_from_data(spec=spec, resources=images, resource_type=ResourceType.LOCAL)

    task_url = f"{SERVER_URL}/tasks/{task.id}"
    print("\n" + "="*60)
    print(f"🎉 TẠO TASK THÀNH CÔNG CHO: {expected_name} ({mshv_input})!")
    print(f"  - Task ID  : {task.id}")
    print(f"  - Tên Task : {task_name}")
    print(f"  - Số ảnh   : {len(images)} ảnh")
    print(f"  - Bấm vào link dưới đây để mở CVAT và gán nhãn ngay:")
    print(f"    👉 {task_url} 👈")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
