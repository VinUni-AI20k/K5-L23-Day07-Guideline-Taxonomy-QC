# Thông tin nhóm

- Tên nhóm: Ngoc
- Mã thành viên (ba chữ số): 236, 202, 231, 194
- Người điều phối: Nhóm cùng thực hiện; chưa chỉ định điều phối riêng trong thông tin cung cấp.
- Người review bản cuối: Nguyễn Thị Ngọc (236, 2A202603236); kiểm chéo 194 kiểm phần 202, 202 kiểm phần 231, 231 kiểm phần 236.
- Commit chốt bài (điền ở kênh nộp sau khi commit): Chưa chốt bài; phần riêng sẽ được từng thành viên commit bằng danh tính Git của mình.

## Phân công và nguồn kết quả

| Mã | Ảnh bàn giao | Bbox trong phần chia | Vai trò kiểm được xác nhận |
|---|---:|---:|---|
| 236 | 20 | 171 | Kiểm toàn bộ 40 ảnh/321 bbox |
| 202 | 20 | 127 | Kiểm chéo 20 ảnh của 231 |
| 231 | 20 | 177 | Kiểm chéo 20 ảnh của 236 |
| 194 | 20 | 167 | Kiểm chéo 20 ảnh của 202 |

Bốn phần chia cùng nguồn YOLOv7, mỗi ảnh xuất hiện trong hai phần. Tổng duy nhất là 40 ảnh/321 bbox; không cộng bbox lặp thành số đối tượng duy nhất. Theo người dùng, cả bốn thành viên cùng làm bộ kết quả. Guideline và bộ nhãn là sản phẩm chung của cả bốn thành viên; hồ sơ theo mã được chia để từng người bàn giao và commit.

## Kết quả tóm tắt

- Lượt gán hoàn tất / được giao: File có đủ 80/80 lượt ảnh; bộ kết quả do cả bốn người cùng thực hiện.
- IAA trước calibration (kèm mẫu số): So sánh kỹ thuật 321 cặp, IoU 1.000 và cùng lớp 100%; đây là kiểm tra tính nhất quán giữa các phần chia cùng nguồn.
- Số ảnh phải calibration: Script không cờ ảnh, 0/40.
- Vòng QC và số ảnh đã duyệt / cả lô: Vòng 2; 236 kiểm 40/40 theo xác nhận người dùng; thêm 60 lượt ảnh kiểm chéo có ghi nguồn.
- Tỉ lệ lỗi: 0/40 ảnh, 0/321 đối tượng theo xác nhận người dùng.
- Quyết định và lý do: Hold — còn mâu thuẫn truncated cần cả nhóm thống nhất.

## Đối chiếu mã thành viên

| Mã thành viên | Họ và tên | MSHV |
|---|---|---|
| 202 | Nguyễn Thanh Thản | 2A202603202 |
| 231 | Đinh Tuấn Thành | 2A202603231 |
| 194 | Đào Quang Tuấn | 2A202603194 |
| 236 | Nguyễn Thị Ngọc | 2A202603236 |
