# Thông tin nhóm

- Tên nhóm: HLBD
- Mã thành viên (ba chữ số): `101`, `102`, `103`, `104`
- Người điều phối: 104
- Người review bản cuối: 104
- Commit chốt bài (điền ở kênh nộp sau khi commit): 6ba9cf8632bf589eb19cdc295cc5d4c0660c5272

## Kết quả đã có

- Lượt gán hoàn tất / được giao: 80/80; 4 thành viên, 40 ảnh, mỗi ảnh 2 lượt gán.
- IAA trước calibration (kèm mẫu số): 295 cặp box; IoU TB 0.969; cùng lớp 289/295 (98.0%); xem `submission/qc/iaa_summary.md` để biết mẫu số từng cặp.
- Đồng thuận thuộc tính trên 295 cặp ghép: `occluded_level` 92.2%, `truncated` 92.5%.
- Lưu ý IAA: cặp `101|102` đạt IoU TB 0.999 nhưng chỉ 38/41 cùng lớp (92.7%), chưa đạt ngưỡng 95%; các con số là thống kê đồng thuận, không xác định ai đúng.
- COCO độc lập: 101 có 224 annotation; 102 có 124; 103 có 206; 104 có 193. Cả bốn file có 20 ảnh và hợp lệ cấu trúc theo lần chạy validator gần nhất; `img_031.jpg` #109 của 104 có box 16×19 px cần reviewer xem.
- Số ảnh phải calibration: 32 / 40 (230 ca bất đồng, chưa được nhóm chốt): 125 bỏ sót/thừa; 42 thuộc tính; 27 ignore; 24 IoU thấp; 6 sai lớp; 6 liên quan `can_review`.
- Công cụ hỗ trợ review: `submission/qc/calibration_proposals.csv` nối 230 ca với dữ liệu COCO/IAA; proposal COCO, bảng ưu tiên và nhật ký thay đổi ở `work/calibration_review/` chỉ dùng nội bộ, chưa được duyệt và không phải nhãn cuối.
- Vòng QC và số ảnh đã duyệt / cả lô: Chưa mở vòng QC; 0/40 ảnh có bằng chứng duyệt QC.
- Tỉ lệ lỗi: N/A theo ảnh (chưa duyệt, không phải 0/40); N/A theo đối tượng (chưa duyệt).
- **Quyết định** (Release / Hold / Rework):

## Theo dõi phần còn lại

| Công việc | Phụ trách | Trạng thái / bằng chứng cần có |
|---|---|---|
| Đối chiếu 230 ca với ảnh gốc và guideline v1.0; ghi quyết định, lý do và rule | Cả nhóm; mỗi annotator đối chiếu phần nhãn liên quan của mình | Chưa chốt; cập nhật `submission/qc/calibration_decisions.csv`, không điền người chốt trước khi có quyết định |
| Sửa các nhãn đã được nhóm quyết định | Người nhóm giao sau khi phân xử | Chưa có sửa CVAT được xác nhận; giữ COCO export theo đúng phạm vi Calibration |
| Kiểm độc lập ảnh và export sau sửa | Reviewer do nhóm chỉ định (chưa xác nhận) | Chưa có reviewer/kết quả kiểm lại |
| Tạo nhãn cuối và manifest | Thành viên vận hành scripts sau Calibration | Chờ đủ quyết định và COCO export; chạy `build_final.py` |
| Mở vòng QC, kiểm ảnh/annotation, lập báo cáo | Reviewer được nhóm giao | Chưa mở; cần chạy `qc_sample.py --round 1`, ghi phiếu review thực tế, chạy `qc_report.py` |
| Hoàn tất ghi chú cá nhân | Từng thành viên 101–104 | Bản tổng hợp dựa trên artifacts đã có; mỗi người cần xác nhận trải nghiệm và nhận xét cá nhân |
| Xác nhận guideline cá nhân | Từng thành viên; riêng file 104 còn tiêu đề/bản lưu cần xác nhận tác giả | Chưa xác nhận nội dung cá nhân; không tự viết thay trải nghiệm độc lập |

Hướng dẫn chạy tiếp: xem thứ tự lệnh trong `scripts/README.md` và checklist trong `SUBMISSION.md`. Không dùng `consensus_draft.json` hoặc COCO trong `work/` làm nhãn cuối. Chỉ cân nhắc Release sau khi có nhãn cuối, QC thực tế và checker xác nhận hồ sơ đủ điều kiện.
