"""Tự động tạo Task trên CVAT Local và upload ảnh được phân công qua Terminal / CLI.

Mặc định kết nối tới CVAT Local: http://localhost:8080

Ví dụ sử dụng:
    # 1. Sinh nhãn CVAT từ taxonomy (nếu chưa chạy):
    python scripts/make_cvat_labels.py

    # 2. Tạo task cho 1 thành viên trên CVAT Local:
    python scripts/create_cvat_task.py --mshv 2A202603192 --auth "admin:admin"

    # 3. Tạo cả 5 Task cho 5 thành viên trong 1 lệnh duy nhất (kèm Project):
    python scripts/create_cvat_task.py --all --project-name "Day07_T005" --auth "admin:admin"

    # 4. Nếu thành viên chạy từ máy khác trong cùng mạng LAN:
    python scripts/create_cvat_task.py --server http://192.168.1.10:8080 --mshv 2A202603192 --auth "user:pass"
"""
from __future__ import annotations

import argparse
import getpass
import json
import logging
import os
import sys
from pathlib import Path

# Tắt cảnh báo lệch phiên bản giữa cvat-sdk và local cvat server
logging.getLogger("cvat_sdk").setLevel(logging.ERROR)

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
        print(f"[*] Đang sinh file nhãn {CVAT_LABELS_PATH}...")
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
        label_requests = [models.PatchedLabelRequest(**lbl) for lbl in labels_spec]
        spec = models.TaskWriteRequest(
            name=task_name,
            labels=label_requests,
        )

    print(f"[*] Đang upload {len(images)} ảnh lên CVAT Local ({server_url})...")
    try:
        task = client.tasks.create_from_data(
            spec=spec,
            resources=[str(p) for p in images],
            resource_type=ResourceType.LOCAL,
        )
        task_id = task.id
        base_url = server_url.rstrip("/")
        task_url = f"{base_url}/tasks/{task_id}"
        print(f"[THÀNH CÔNG] Đã tạo Task {task_id} cho {mshv}!")
        print(f"  - Tên task : {task_name}")
        print(f"  - Số ảnh   : {len(images)}")
        print(f"  - Link CVAT: {task_url}\n")
        return task
    except Exception as e:
        print(f"[THẤT BẠI] Lỗi khi tạo task cho {mshv}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Tự động tạo task và upload ảnh lên CVAT Local (http://localhost:8080).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--mshv", help="Mã sinh viên cần tạo task (VD: 2A202603192).")
    parser.add_argument("--all", action="store_true", help="Tạo task cho TẤT CẢ thành viên có trong submission/qc/assignments/")
    parser.add_argument("--server", default=os.getenv("CVAT_HOST", "http://localhost:8080"),
                        help="Địa chỉ máy chủ CVAT Local (mặc định: http://localhost:8080).")
    parser.add_argument("--auth", help="Thông tin đăng nhập dạng 'username:password' (VD: admin:admin).")
    parser.add_argument("--token", default=os.getenv("CVAT_TOKEN"), help="API Access Token nếu dùng.")
    parser.add_argument("--project-id", type=int, help="ID của Project đã có sẵn trên CVAT (nếu muốn gán task vào project).")
    parser.add_argument("--project-name", help="Tên Project muốn tự động tạo mới trên CVAT (VD: Day07_T005).")

    args = parser.parse_args()

    username, password = None, None
    token = args.token

    if not token:
        if args.auth:
            if ":" in args.auth:
                username, password = args.auth.split(":", 1)
            else:
                username = args.auth
                password = getpass.getpass(f"Nhập mật khẩu CVAT Local cho tài khoản '{username}': ")
        else:
            env_user = os.getenv("CVAT_USERNAME")
            env_pass = os.getenv("CVAT_PASSWORD")
            if env_user and env_pass:
                username, password = env_user, env_pass
            else:
                print(f"Kết nối tới CVAT Local ({args.server})")
                username = input("Nhập CVAT Username: ").strip()
                password = getpass.getpass("Nhập CVAT Password: ")

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

    print(f"[*] Đang kết nối tới CVAT Local: {args.server} ...")
    client_kwargs = {"host": args.server}
    if token:
        client_kwargs["access_token"] = token
    else:
        client_kwargs["credentials"] = (username, password)

    try:
        with make_client(**client_kwargs) as client:
            user = client.users.retrieve(client.users.get_self().id)
            print(f"[*] Đăng nhập CVAT Local thành công! Xin chào: {user.username}")

            project_id = args.project_id
            if args.project_name and project_id is None:
                print(f"[*] Đang tạo Project mới '{args.project_name}' trên CVAT Local...")
                label_requests = [models.PatchedLabelRequest(**lbl) for lbl in labels_data]
                proj_spec = models.ProjectWriteRequest(
                    name=args.project_name,
                    labels=label_requests,
                )
                proj = client.projects.create(spec=proj_spec)
                project_id = proj.id
                print(f"[THÀNH CÔNG] Đã tạo Project '{args.project_name}' (ID: {project_id})")

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

            print(f"\n========================================================")
            print(f"[HOÀN TẤT] Đã tạo thành công {success_count}/{len(members)} Task trên CVAT Local!")
            print(f"Mở trình duyệt truy cập: {args.server} để kiểm tra và gán nhãn.")
            print(f"========================================================")
    except Exception as e:
        print(f"\nLỖI KẾT NỐI CVAT LOCAL: {e}", file=sys.stderr)
        print("Gợi ý: Kiểm tra xem CVAT Local đã bật chưa (mặc định tại http://localhost:8080) và đúng tài khoản/mật khẩu.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
