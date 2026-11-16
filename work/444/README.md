# Nhãn làm việc — member 444

- Xuất trực tiếp từ CVAT task 17, định dạng **COCO 1.0**, ngày 2026-11-16.
- **20 ảnh**, **264 box**: 254 đối tượng và 10 vùng `ignore_region`.
- Phạm vi ảnh khớp `submission/qc/assignments/444.txt`; ảnh không có vật vẫn có trong COCO.
- Giữ các thuộc tính Boolean `occluded`, `truncated`, `can_review`; hiện có 74 box bật `can_review`.
- Đã đối chiếu tên ảnh, kích thước, lớp, tọa độ và thuộc tính với bản đang lưu trên CVAT.

## Tệp

- [444.json](444.json): nhãn COCO để đọc và so sánh.
- [444_coco.zip](444_coco.zip): bản xuất gốc từ CVAT, dùng để nhập lại với định dạng COCO 1.0; không kèm ảnh.
- Ảnh tương ứng ở [images/](images/).

Đây là bản nhãn làm việc có hỗ trợ AI, theo `submission/guidelines/guideline_v1.0_agreed.md`. Các ca `can_review` còn cần người rà và calibration; bản xuất này không phải quyết định Release hay xác nhận đã hoàn tất QC của nhóm.
