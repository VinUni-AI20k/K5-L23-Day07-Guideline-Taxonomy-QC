#!/usr/bin/env python3
"""Script phân việc và tự động tạo Task cá nhân trên CVAT (Cloud, Local hoặc URL tùy chọn).

CÁCH SỬ DỤNG:
    python scripts/setup_cvat.py "<Họ và tên>" <MSHV>

TÙY CHỌN BỔ SUNG (NẾU MUỐN CHẠY 1 DÒNG KHÔNG CẦN CHỌN MENU):
    --server <URL>        Đường dẫn máy chủ CVAT (VD: http://localhost:8080, https://app.cvat.ai, http://192.168.1.15:8080)
    --auth <user:pass>    Tài khoản đăng nhập dạng 'username:password'
    --token <token>       Personal Access Token (dành cho app.cvat.ai đăng nhập qua Google)

Ví dụ các câu lệnh cho nhóm T005:
    python scripts/setup_cvat.py "NGUYỄN ĐỨC CƯỜNG" 2A202603040
    python scripts/setup_cvat.py "HOÀNG NHẬT ANH" 2A202603183
    python scripts/setup_cvat.py "NGUYỄN BÁ DUY" 2A202603192
    python scripts/setup_cvat.py "ĐỖ HUY KIÊN" 2A202603216
    python scripts/setup_cvat.py "PHẠM MẠNH HÙNG" 2A202603240
"""
from __future__ import annotations

import argparse
import getpass
import json
import logging
import os
import re
import sys
import unicodedata
from pathlib import Path

# Tắt cảnh báo log không cần thiết
logging.disable(logging.WARNING)

try:
    from cvat_sdk import make_client, models
    from cvat_sdk.core.proxies.tasks import ResourceType
except ImportError:
    print("\n" + "="*65, file=sys.stderr)
    print("[LỖI] Máy bạn chưa cài đặt thư viện 'cvat-sdk'!", file=sys.stderr)
    print("Vui lòng mở Terminal và chạy lệnh sau:\n", file=sys.stderr)
    print("    pip install cvat-sdk\n", file=sys.stderr)
    print("="*65 + "\n", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = ROOT / "work"
TAXONOMY_PATH = ROOT / "submission" / "taxonomy.json"
CVAT_LABELS_PATH = ROOT / "cvat" / "labels_generated.json"
QC_ASSIGNMENTS_DIR = ROOT / "submission" / "qc" / "assignments"
ASSIGNMENT_CSV = ROOT / "submission" / "qc" / "assignment.csv"

PROJECT_NAME = "Day07_T005"

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
    """Đảm bảo phân phối 40 ảnh cho 5 thành viên (24 ảnh/người)."""
    if not ASSIGNMENT_CSV.exists() or not QC_ASSIGNMENTS_DIR.exists():
        print("[*] Đang khởi tạo ma trận chia việc cho 5 thành viên...")
        import subprocess
        members_arg = ",".join(sorted(TEAM_MEMBERS.keys()))
        subprocess.run([
            sys.executable, str(ROOT / "scripts" / "split_assign.py"),
            "--members", members_arg, "--copy-images"
        ], check=True)


def get_or_create_project(client, project_name: str) -> int:
    """Tạo Project nếu chưa có trên server CVAT, dùng lại nếu đã có."""
    projects = [p for p in client.projects.list() if p.name == project_name]
    if projects:
        return projects[0].id

    print(f"[*] Project '{project_name}' chưa có trên CVAT. Đang tự động tạo mới...")
    if not CVAT_LABELS_PATH.exists():
        import subprocess
        subprocess.run([sys.executable, str(ROOT / "scripts" / "make_cvat_labels.py")], check=True)

    with CVAT_LABELS_PATH.open(encoding="utf-8") as f:
        labels_data = json.load(f)

    label_reqs = [models.PatchedLabelRequest(**l) for l in labels_data]
    proj_spec = models.ProjectWriteRequest(name=project_name, labels=label_reqs)
    proj = client.projects.create(proj_spec)
    print(f"[+] Đã tạo Project '{project_name}' thành công (ID: {proj.id})")
    return proj.id


def select_server_and_auth(cli_server: str | None, cli_auth: str | None, cli_token: str | None) -> tuple[str, any]:
    """Hỏi người dùng chọn máy chủ (Cloud, Local, Custom Link) và tài khoản."""
    server_url = cli_server

    # Nếu người dùng chưa truyền cờ --server trên CLI thì hiện menu lựa chọn
    if not server_url:
        print("\n" + "="*60)
        print("          CHỌN MÁY CHỦ CVAT BẠN MUỐN KẾT NỐI")
        print("="*60)
        print("  [1] CVAT Cloud (https://app.cvat.ai)  [Mặc định]")
        print("  [2] CVAT Local máy này (http://localhost:8080)")
        print("  [3] Tự nhập đường dẫn link CVAT (URL tùy chọn / LAN / IP máy khác)")
        print("="*60)

        try:
            choice = input("Nhập lựa chọn của bạn (1, 2 hoặc 3) [mặc định 1]: ").strip()
        except EOFError:
            choice = "1"

        if choice == "2":
            server_url = "http://localhost:8080"
        elif choice == "3":
            try:
                custom_url = input("\nNhập đường dẫn link máy chủ CVAT (VD: http://192.168.1.15:8080): ").strip()
            except EOFError:
                custom_url = ""
            if not custom_url:
                print("Đường dẫn không được để trống!", file=sys.stderr)
                sys.exit(1)
            if not (custom_url.startswith("http://") or custom_url.startswith("https://")):
                custom_url = "http://" + custom_url
            server_url = custom_url
        else:
            server_url = "https://app.cvat.ai"

    server_url = server_url.rstrip("/")

    # 1. Nếu có token truyền vào
    token = cli_token or os.getenv("CVAT_TOKEN")
    if token:
        return server_url, make_client(server_url, access_token=token)

    # 2. Nếu có auth truyền vào (username:password)
    if cli_auth:
        if ":" in cli_auth:
            u, p = cli_auth.split(":", 1)
        else:
            u = cli_auth
            p = getpass.getpass(f"Nhập mật khẩu CVAT cho tài khoản '{u}': ")
        return server_url, make_client(server_url, credentials=(u, p))

    # 3. Đăng nhập theo loại server:
    is_localhost = ("localhost" in server_url or "127.0.0.1" in server_url)

    if is_localhost:
        print("\n" + "-"*60)
        print(f"[*] Đăng nhập CVAT Local ({server_url})")
        print("Nhập tài khoản Local của bạn:")
        try:
            u = input("Username (Enter để dùng tài khoản mặc định basduy05): ").strip()
        except EOFError:
            u = ""
        u = u or "basduy05"
        try:
            p = getpass.getpass(f"Password cho tài khoản '{u}': ")
        except EOFError:
            p = ""
        return server_url, make_client(server_url, credentials=(u, p))

    elif "app.cvat.ai" in server_url:
        print("\n" + "-"*60)
        print(f"[*] Đăng nhập CVAT Cloud ({server_url})")
        print("  [1] Email/Username và Mật khẩu (nếu đăng ký trực tiếp)")
        print("  [2] Personal Access Token (nếu đăng nhập qua Google)")
        print("-"*60)
        try:
            c = input("Lựa chọn (1 hoặc 2) [mặc định 1]: ").strip()
        except EOFError:
            c = "1"
        if c == "2":
            print("\nCách lấy Token trên CVAT Cloud:")
            print("  Vào https://app.cvat.ai -> Avatar góc trên phải -> Profile -> Personal access tokens -> Create token")
            try:
                tok = input("Nhập chuỗi Token: ").strip()
            except EOFError:
                tok = ""
            return server_url, make_client(server_url, access_token=tok)
        else:
            try:
                u = input("CVAT Cloud Email / Username: ").strip()
                p = getpass.getpass(f"CVAT Cloud Password cho '{u}': ")
            except EOFError:
                u, p = "", ""
            return server_url, make_client(server_url, credentials=(u, p))

    else:
        # Đường dẫn link tùy chọn (Local LAN, IP trường, hoặc Server riêng)
        print("\n" + "-"*60)
        print(f"[*] Đăng nhập máy chủ CVAT tùy chọn ({server_url})")
        try:
            u = input("Username / Email: ").strip()
            p = getpass.getpass(f"Password cho tài khoản '{u}': ")
        except EOFError:
            u, p = "", ""
        return server_url, make_client(server_url, credentials=(u, p))


def main():
    parser = argparse.ArgumentParser(
        description="Tự động phân việc và upload task lên CVAT.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("args", nargs="*", help="Họ tên và Mã sinh viên")
    parser.add_argument("--server", help="Đường dẫn link CVAT Server (tùy chọn).")
    parser.add_argument("--auth", help="Tài khoản đăng nhập dạng 'username:password'.")
    parser.add_argument("--token", help="Personal Access Token (nếu có).")

    parsed = parser.parse_args()
    raw_args = [a.strip() for a in parsed.args if not a.startswith("-")]

    if len(raw_args) < 2:
        print("\n" + "="*65)
        print("LỖI: Bạn phải nhập đủ Họ tên và Mã sinh viên để nhận việc!")
        print("="*65)
        print("Cú pháp chuẩn:")
        print("    python scripts/setup_cvat.py \"<Họ và tên>\" <MSHV>")
        print("\nVí dụ các câu lệnh cho nhóm T005:")
        for mshv, name in TEAM_MEMBERS.items():
            print(f'    python scripts/setup_cvat.py "{name}" {mshv}')
        print("="*65 + "\n")
        sys.exit(1)

    # Phân biệt Họ tên và MSHV
    mshv_input = None
    name_input = None
    for arg in raw_args:
        if re.search(r"2A\d+|\d{5,}", arg, re.IGNORECASE):
            mshv_input = arg.upper()
        else:
            name_input = arg if not name_input else f"{name_input} {arg}"

    if not mshv_input or not name_input:
        name_input = raw_args[0]
        mshv_input = raw_args[1].upper()

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

    # 1. Đảm bảo ảnh đã được phân bổ đúng (24 ảnh)
    ensure_split_assign()
    img_dir = WORK_DIR / mshv_input / "images"
    if not img_dir.exists() or len(list(img_dir.iterdir())) < 24:
        import shutil
        txt_path = QC_ASSIGNMENTS_DIR / f"{mshv_input}.txt"
        if not txt_path.exists():
            ensure_split_assign()
        assigned_imgs = [line.strip() for line in txt_path.read_text(encoding="utf8").splitlines() if line.strip()]
        img_dir.mkdir(parents=True, exist_ok=True)
        for img in assigned_imgs:
            src = ROOT / "data" / "images" / img
            if src.exists():
                shutil.copy2(src, img_dir / img)

    images = sorted([str(p) for p in img_dir.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}])
    if not images:
        print(f"LỖI: Không tìm thấy ảnh trong {img_dir}", file=sys.stderr)
        sys.exit(1)

    slug_name = to_slug(expected_name)
    task_name = f"day07-{mshv_input}-{slug_name}"

    # 2. Chọn server và đăng nhập
    server_url, client = select_server_and_auth(parsed.server, parsed.auth, parsed.token)

    print(f"\n[*] Đang kết nối tới CVAT ({server_url})...")
    try:
        user = client.users.retrieve_current_user()
        print(f"[+] Đăng nhập thành công! Tài khoản: {user.username}")

        project_id = get_or_create_project(client, PROJECT_NAME)

        # Kiểm tra xem Task này đã tồn tại chưa
        existing_tasks = [t for t in client.tasks.list() if t.name == task_name]
        if existing_tasks:
            task_id = existing_tasks[0].id
            task_url = f"{server_url}/tasks/{task_id}"
            print("\n" + "="*60)
            print(f"[!] BẠN ĐÃ CÓ TASK TRÊN CVAT TỪ TRƯỚC:")
            print(f"  - Thành viên : {expected_name} ({mshv_input})")
            print(f"  - Tên task   : {task_name}")
            print(f"  - Task ID    : {task_id}")
            print(f"  - Link vào gán nhãn: {task_url}")
            print("="*60 + "\n")
            return

        print("\n" + "="*60)
        print(f"[*] BẮT ĐẦU TẠO TASK TRÊN CVAT CHO:")
        print(f"  - Thành viên : {expected_name}")
        print(f"  - MSSV       : {mshv_input}")
        print(f"  - Số lượng   : {len(images)} ảnh (đúng 24 ảnh được phân)")
        print(f"[*] Đang tải {len(images)} ảnh lên server...")
        print("="*60)

        spec = models.TaskWriteRequest(name=task_name, project_id=project_id)
        task = client.tasks.create_from_data(spec=spec, resources=images, resource_type=ResourceType.LOCAL)

        task_url = f"{server_url}/tasks/{task.id}"
        print("\n" + "="*60)
        print(f"🎉 TẠO TASK THÀNH CÔNG CHO: {expected_name} ({mshv_input})!")
        print(f"  - Server   : {server_url}")
        print(f"  - Task ID  : {task.id}")
        print(f"  - Tên Task : {task_name}")
        print(f"  - Số ảnh   : {len(images)} ảnh")
        print(f"  - Bấm vào link dưới đây để mở CVAT và gán nhãn ngay:")
        print(f"    👉 {task_url} 👈")
        print("="*60 + "\n")

    except Exception as e:
        print("\n" + "!"*65, file=sys.stderr)
        print(f"[LỖI THỰC HIỆN]: {e}", file=sys.stderr)
        print("!"*65, file=sys.stderr)
        print("Gợi ý khắc phục:", file=sys.stderr)
        print("1. Kiểm tra lại đường dẫn link CVAT và tài khoản/mật khẩu.", file=sys.stderr)
        print("2. Nếu dùng Local, đảm bảo máy chủ CVAT đã bật (http://localhost:8080).", file=sys.stderr)
        print("3. Nếu dùng Cloud (app.cvat.ai) và đăng nhập bằng Google, hãy dùng Token.", file=sys.stderr)
        print("!"*65 + "\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
