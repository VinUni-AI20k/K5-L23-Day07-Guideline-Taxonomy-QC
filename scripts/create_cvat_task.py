"""Tự động tạo Task trên CVAT và upload ảnh được phân công qua Terminal / CLI.

Sử dụng thư viện cvat-sdk (đã được cài đặt sẵn).

Ví dụ sử dụng:
    # 1. Sinh nhãn CVAT từ taxonomy (nếu chưa chạy)
    python scripts/make_cvat_labels.py

    # 2. Tạo task cho 1 cá nhân (CVAT Cloud):
    python scripts/create_cvat_task.py --mshv 2A202603192 --auth "my_username:my_password"

    # 3. Tạo task dưới một Project đã có sẵn (khuyến nghị cho nhóm):
    python scripts/create_cvat_task.py --mshv 2A202603192 --project-id 12345 --auth "user:pass"

    # 4. Tự động tạo Project nhóm và tạo luôn 5 Task cho cả 5 thành viên:
    python scripts/create_cvat_task.py --all --project-name "Day07_T005" --auth "user:pass"
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
from pathlib import Path

try:
    from cvat_sdk import make_client, models
    from cvat_sdk.core.proxies.tasks import ResourceType
except ImportError:
    print("LỖI: Chưa cài đặt thư viện 'cvat-sdk'. Chạy lệnh: pip install cvat-sdk", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = ROOT / "work"
CVAT_LABELS_PATH = ROOT / "cvat" / "labels_generated.json"
QC_ASSIGNMENTS_DIR = ROOT / "submission" / "qc" / "assignments"


def load_labels() -> list:
    if not CVAT_LABELS_PATH.exists():
        print(f"CẢNH BÁO: Không tìm thấy {CVAT_LABELS_PATH}. Đang chạy scripts/make_cvat_labels.py...")
        import subprocess
        subprocess.run([sys.executable, str(ROOT / "scripts" / "make_cvat_labels.py")], check=True)
    with CVAT_LABELS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def get_assigned_images(mshv: str) -> list[Path]:
    img_dir = WORK_DIR / mshv / "images"
    if not img_dir.exists():
        print(f"LỖI: Thư mục {img_dir} không tồn tại!", file=sys.stderr)
        print("Hãy chạy lệnh chia ảnh trước:\n  python scripts/split_assign.py --members ... --copy-images", file=sys.stderr)
        sys.exit(1)

    images = sorted([p for p in img_dir.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}])
    if not images:
        print(f"LỖI: Không tìm thấy ảnh nào trong {img_dir}!", file=sys.stderr)
        sys.exit(1)
    return images


def create_task_for_member(client, server_url: str, mshv: str, project_id: int | None, labels_spec: list | None):
    images = get_assigned_images(mshv)
    task_name = f"day07-{mshv}"
    print(f"\n========================================================")
    print(f"[*] Đang chuẩn bị tạo Task '{task_name}' cho MSHV: {mshv}")
    print(f"[*] Số lượng ảnh tải lên: {len(images)} ảnh")
    print(f"========================================================")

    if project_id is not None:
        spec = models.TaskWriteRequest(
            name=task_name,
            project_id=project_id,
        )
    else:
        # Standalone task with raw labels
        label_requests = [models.PatchedLabelRequest(**lbl) for lbl in labels_spec]
        spec = models.TaskWriteRequest(
            name=task_name,
            labels=label_requests,
        )

    print(f"[*] Đang tạo task và upload {len(images)} ảnh lên {server_url} (vui lòng chờ)...")
    try:
        task = client.tasks.create_from_data(
            spec=spec,
            resources=[str(p) for p in images],
            resource_type=ResourceType.LOCAL,
        )
        task_id = task.id
        base_url = server_url.rstrip("/")
        task_url = f"{base_url}/tasks/{task_id}"
        print(f"\n[THÀNH CÔNG] Task đã được tạo thành công!")
        print(f"  - Task ID : {task_id}")
        print(f"  - Tên task: {task_name}")
        print(f"  - Số ảnh  : {len(images)}")
        print(f"  - Link CVAT để bắt đầu gán nhãn:")
        print(f"    >>> {task_url} <<<\n")
        return task
    except Exception as e:
        print(f"[THẤT BẠI] Lỗi khi tạo task cho {mshv}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Tự động tạo task và upload ảnh lên CVAT cho từng thành viên nhóm.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--mshv", help="Mã sinh viên cần tạo task (VD: 2A202603192).")
    parser.add_argument("--all", action="store_true", help="Tạo task cho TẤT CẢ thành viên có trong submission/qc/assignments/")
    parser.add_argument("--server", default=os.getenv("CVAT_HOST", "https://app.cvat.ai"),
                        help="Địa chỉ máy chủ CVAT (mặc định: https://app.cvat.ai hoặc http://localhost:8080).")
    parser.add_argument("--auth", help="Thông tin đăng nhập dạng 'username:password'.")
    parser.add_argument("--token", default=os.getenv("CVAT_TOKEN"), help="API Access Token (nếu dùng token thay vì password).")
    parser.add_argument("--project-id", type=int, help="ID của Project đã có sẵn trên CVAT (nếu muốn gán task vào project).")
    parser.add_argument("--project-name", help="Tên Project muốn tự động tạo mới trên CVAT trước khi thêm task (VD: Day07_T005).")

    args = parser.parse_args()

    # Determine credentials
    username, password = None, None
    token = args.token

    if not token:
        if args.auth:
            if ":" in args.auth:
                username, password = args.auth.split(":", 1)
            else:
                username = args.auth
                password = getpass.getpass(f"Nhập mật khẩu CVAT cho tài khoản '{username}': ")
        else:
            env_user = os.getenv("CVAT_USERNAME")
            env_pass = os.getenv("CVAT_PASSWORD")
            if env_user and env_pass:
                username, password = env_user, env_pass
            else:
                print(f"Kết nối tới CVAT Server: {args.server}")
                username = input("Nhập CVAT Username: ").strip()
                password = getpass.getpass("Nhập CVAT Password: ")

    # Members list
    members = []
    if args.all:
        if not QC_ASSIGNMENTS_DIR.exists():
            print(f"LỖI: Chưa có thư mục {QC_ASSIGNMENTS_DIR}. Vui lòng chạy split_assign.py trước!", file=sys.stderr)
            sys.exit(1)
        for p in sorted(QC_ASSIGNMENTS_DIR.glob("*.txt")):
            members.append(p.stem)
        if not members:
            print("LỖI: Không tìm thấy file phân công nào trong submission/qc/assignments/", file=sys.stderr)
            sys.exit(1)
    elif args.mshv:
        members = [args.mshv.strip()]
    else:
        print("LỖI: Vui lòng chỉ định --mshv <MSHV> hoặc dùng cờ --all để tạo cho cả nhóm.", file=sys.stderr)
        sys.exit(1)

    labels_data = load_labels()

    # Connect client
    print(f"Đang kết nối tới CVAT ({args.server})...")
    client_kwargs = {"host": args.server}
    if token:
        client_kwargs["access_token"] = token
    else:
        client_kwargs["credentials"] = (username, password)

    with make_client(**client_kwargs) as client:
        # Check login
        user = client.users.retrieve(client.users.get_self().id)
        print(f"Đăng nhập thành công với tài khoản: {user.username} ({user.email or 'no email'})")

        project_id = args.project_id
        # Create project if requested
        if args.project_name and project_id is None:
            print(f"Đang tạo Project mới '{args.project_name}' trên CVAT...")
            label_requests = [models.PatchedLabelRequest(**lbl) for lbl in labels_data]
            proj_spec = models.ProjectWriteRequest(
                name=args.project_name,
                labels=label_requests,
            )
            proj = client.projects.create(spec=proj_spec)
            project_id = proj.id
            print(f"[THÀNH CÔNG] Đã tạo Project '{args.project_name}' (ID: {project_id})")

        # Create tasks
        success_count = 0
        for mshv in members:
            task = create_task_for_member(
                client=client,
                server_url=args.server,
                mshv=mshv,
                project_id=project_id,
                labels_spec=labels_data if project_id is None else None,
            )
            if task:
                success_count += 1

        print(f"\nHoàn tất: Đã tạo thành công {success_count}/{len(members)} Task.")


if __name__ == "__main__":
    main()
