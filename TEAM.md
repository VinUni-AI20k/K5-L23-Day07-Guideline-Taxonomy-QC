# Thông tin nhóm

- Tên nhóm: T012
- Mã thành viên (ba chữ số): 101(2A202603024) ,102(2A202603056), 103(2A202603073), 104(2A202603050), 105(2A202603221)
- Người điều phối: 101(2A202603024)
- Người review bản cuối: 102(2A202603056)
- Commit chốt bài (điền ở kênh nộp sau khi commit):

## Kết quả tóm tắt (điền cuối bài)

- Lượt gán hoàn tất / được giao: 120/120 (5 thành viên, 24 ảnh/người).
- IAA trước calibration (kèm mẫu số): IoU TB 0,785/914 cặp box ghép; cùng lớp 95,8%/914. Chưa đạt ngưỡng IoU 0,85.
- Số ảnh phải calibration: 38/40 ảnh bị gắn cờ trong `iaa_summary.md`.
- Vòng QC và số ảnh đã duyệt / cả lô: Vòng 2, review đủ 40/40 ảnh; 2 ảnh lỗi, 7 annotation cần sửa.
- Tỉ lệ lỗi: Ảnh 2/40 = 5,0%; annotation 7/392 = 1,8% (không tính 11 ignore_region).
- **Quyết định** (Release / Hold / Rework) và lý do một dòng: Rework — vòng 2 phát hiện lỗi ở img_003 và img_030; vượt ngưỡng ảnh lỗi 2%, cần sửa và review vòng 2.
