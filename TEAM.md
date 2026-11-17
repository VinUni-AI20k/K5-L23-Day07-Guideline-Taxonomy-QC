# Thông tin nhóm

- Tên nhóm: G003
- Mã thành viên (ba chữ số): 
  - 343: Pham Duy Thanh
  - 069: Vũ Gia Khang
  - 042: Trần Hữu Thủy
  - 063: Nguyễn Bình Anh
  - 059: Lê Quang Vinh
- Người điều phối: Vũ Gia Khang
- Người review bản cuối: Phạm Duy Thanh
- Commit chốt bài (điền ở kênh nộp sau khi commit): 1aea1bb02c364607c1541765467a40ad6fc7e0a3

## Kết quả tóm tắt (điền cuối bài)

- Lượt gán hoàn tất / được giao: 120 / 120 (100% trên 40 ảnh, 5 thành viên gán độc lập)
- IAA trước calibration (kèm mẫu số): IoU TB 0.844, Đồng thuận lớp 89.3% trên mẫu số 777 cặp box ghép
- Số ảnh phải calibration: 36 / 40 ảnh
- Vòng QC và số ảnh đã duyệt / cả lô: Vòng QC 3, đã duyệt 40 / 40 ảnh
- Tỉ lệ lỗi: 60.0 % theo ảnh (24/40), 8.5 % theo đối tượng (40/470)
- **Quyết định**: Rework — 24/40 ảnh lỗi vượt ngưỡng 2%, lỗi lặp `truncated` (R-08, 37 box); còn phải sửa 37 box `truncated`, xóa 3 box thừa rồi duyệt lại ở vòng 4 (xem `submission/qc/QC_REPORT.md`).
