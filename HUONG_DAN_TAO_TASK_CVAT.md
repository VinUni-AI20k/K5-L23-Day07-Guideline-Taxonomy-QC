# HƯỚNG DẪN NHẬN VIỆC & TỰ ĐỘNG TẠO TASK TRÊN CVAT LOCAL (NHÓM T005)

Hệ thống được thiết kế theo đúng quy trình **phân job theo yêu cầu (on-demand)**: 
Task của thành viên nào sẽ **CHỈ ĐƯỢC TẠO khi thành viên đó chạy đúng câu lệnh Họ tên và Mã sinh viên** của mình trong Terminal.

---

## 1. Bảng Câu Lệnh Phân Việc Cho Từng Thành Viên

Mỗi bạn mở Terminal tại thư mục dự án và copy đúng câu lệnh của mình để nhận 24 ảnh và tự động tạo Task trên CVAT Local (`http://localhost:8080`):

| STT | Thành viên | Mã sinh viên | Câu lệnh chạy Terminal để nhận job & tạo Task |
|:---:|:---|:---:|:---|
| 1 | **NGUYỄN ĐỨC CƯỜNG** | `2A202603040` | `python scripts/setup_cvat.py "NGUYỄN ĐỨC CƯỜNG" 2A202603040` |
| 2 | **HOÀNG NHẬT ANH** | `2A202603183` | `python scripts/setup_cvat.py "HOÀNG NHẬT ANH" 2A202603183` |
| 3 | **NGUYỄN BÁ DUY** | `2A202603192` | `python scripts/setup_cvat.py "NGUYỄN BÁ DUY" 2A202603192` |
| 4 | **ĐỖ HUY KIÊN** | `2A202603216` | `python scripts/setup_cvat.py "ĐỖ HUY KIÊN" 2A202603216` |
| 5 | **PHẠM MẠNH HÙNG** | `2A202603240` | `python scripts/setup_cvat.py "PHẠM MẠNH HÙNG" 2A202603240` |

> **Cơ chế hoạt động:**
> - Ai chạy câu lệnh thì CVAT Local **mới tạo đúng Task của người đó** và upload đúng 24 ảnh được phân công.
> - Người nào chưa chạy câu lệnh thì trên CVAT Local hoàn toàn **chưa có Task của người đó**.
> - Nếu người dùng chạy lại câu lệnh lần 2, hệ thống sẽ tự nhận diện Task đã tạo và trả về link gán nhãn, không tạo trùng lặp.

---

## 2. Phân Bổ Ảnh Đảm Bảo Đề Bài (> 2 người gán)

* **Tổng số ảnh**: 40 ảnh.
* **Số thành viên**: 5 người.
* **Số người gán mỗi ảnh**: $K = 3$ người (thỏa mãn $> 2$).
* **Khối lượng**: Mỗi thành viên được giao đúng **24 ảnh** (không ai nhiều hơn, không ai ít hơn).
* **Ma trận phân công**: Đã lưu tại `submission/qc/assignment.csv`.

---

## 3. Quy Trình Sau Khi Chạy Câu Lệnh

1. **Nhận link Task:**
   Ngay khi chạy câu lệnh, màn hình Terminal sẽ in ra đường link Task trên CVAT Local:
   ```text
   🎉 TẠO TASK THÀNH CÔNG CHO: NGUYỄN BÁ DUY (2A202603192)!
     - Task ID  : 29
     - Tên Task : day07-2A202603192-NguyenBaDuy
     - Số ảnh   : 24 ảnh
     - Bấm vào link dưới đây để mở CVAT và gán nhãn ngay:
       👉 http://localhost:8080/tasks/29 👈
   ```

2. **Gán nhãn trên CVAT:**
   Bấm vào link task để mở giao diện CVAT và thực hiện gán 24 ảnh theo guideline nhóm.

3. **Export nhãn COCO 1.0:**
   - Tại Task CVAT: bấm **Actions** $\rightarrow$ **Export task dataset** $\rightarrow$ chọn **COCO 1.0** (tắt ô *Save images*).
   - Tải file zip về, lấy `instances_default.json` đổi tên thành `<MSHV>_<HoTen>.json` bỏ vào thư mục `submission/labels/`:
     * Nguyễn Đức Cường: `submission/labels/2A202603040_NguyenDucCuong.json`
     * Hoàng Nhật Anh: `submission/labels/2A202603183_HoangNhatAnh.json`
     * Nguyễn Bá Duy: `submission/labels/2A202603192_NguyenBaDuy.json`
     * Đỗ Huy Kiên: `submission/labels/2A202603216_DoHuyKien.json`
     * Phạm Mạnh Hùng: `submission/labels/2A202603240_PhamManhHung.json`

4. **Kiểm tra hợp lệ:**
   ```bash
   python scripts/validate_labels.py --all
   ```
