# Báo cáo QC — G003

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Nhãn box 2D cho mô hình phát hiện phương tiện và người trên ảnh đường phố (camera giao thông); lô 40 ảnh đô thị ngày/đêm chỉ đại diện cho các tình huống có trong lô, chưa đủ để đánh giá độ phủ thực tế.
- Nguồn và phép sử dụng dữ liệu: 40 ảnh đường phố giấy phép Creative Commons (xem data/ATTRIBUTION.csv).
- Manifest và checksum nhãn cuối: submission/qc/batch_manifest.json; SHA-256 của labels_calibrated.json là 3e17d52c92375aa8ffe36aac91b1a01e81f906fdc69873380e1d5dc86b1df7c4 (khớp round-03/qc_result.json); nguồn là bản export CVAT sau calibration labels_calibrated_d6eb727c08a830ef.json (40 ảnh, 470 box, 0 box can_review).
- Guideline và taxonomy khi gán / khi bàn giao: Khi gán dùng guideline_v1.0_agreed.md và taxonomy v1.0; khi bàn giao dùng guideline_v1.1_calibrated.md (thay đổi semantic, xem guideline_change.json) và giữ nguyên taxonomy v1.0.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 120 / 120 (40 ảnh × 3 người gán độc lập, nhóm 5 thành viên).
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 777 cặp box ghép; IoU trung bình 0.844 (ngưỡng 0.85); đồng thuận lớp 89.3% (ngưỡng 95%) trên mẫu số 777 cặp box ghép → chưa đạt IAA, 36/40 ảnh phải calibration.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: Chưa ghép A/B là 260/248; loại do ignore là 0; bất đồng ignore là 0.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: img_002.jpg (xe chở xe: hai người cùng gán sót box car con trên sàn hoặc chỉ gán 1 box truck); kiểm bằng cách rà soát theo quy tắc R-03/R-10.

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: 1261 ca trên 36 ảnh, mỗi ca một dòng trong submission/qc/calibration_decisions.csv (nhiều nhất R-10: 504, R-04: 294, R-12: 169, R-08: 102 kể cả ca ghép R-08/R-12, R-15: 90); người chốt 343; bản sửa là Task calibration v1.1 trên CVAT, export thành labels_calibrated_d6eb727c08a830ef.json; người kiểm lại 343 qua QC vòng 3 (cột kiem_lai). Người kiểm lại trùng người chốt do nhóm đổi vai, ghi nhận là hạn chế.
- Tác động v1.1 lên nhãn và ảnh: v1.1 là semantic (R-05, R-08, R-10, R-12, R-13, R-14, R-15) nên 948/1261 ca có pham_vi = lo và cả 40 ảnh được đưa vào Task calibration; nhãn cuối còn 470 box (bản đồng thuận nháp có 481 box).
- Tham chiếu bằng chứng khi Rework: Vòng 1 (reviews/round-01, HOLD vì nhãn cuối còn can_review). Vòng 2 (reviews/round-02, RELEASE) chạy trên labels_calibrated_2ea54876bc1a84fe.json là bản đồng thuận nháp do script sinh (info ghi "Đồng thuận NHÁP tự động - chưa phải nhãn cuối"), chưa phải bản export sau khi sửa trên CVAT, và phiếu vòng 2 trùng hệt phiếu vòng 1, nên nhóm không dùng vòng 2 làm căn cứ bàn giao. Vòng 3 (reviews/round-03) duyệt bản export CVAT thật, kết quả REWORK. Giữ nguyên cả ba vòng.

## 4. Kết quả duyệt

- Vòng QC: 3
- Người review và ngày: 343, 2026-11-17
- Đã duyệt / cả lô: 40 / 40 ảnh (duyệt toàn lô)
- Ảnh lỗi / ảnh đã duyệt: 24 / 40 (60.0%)
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 40 / 470 (8.5%)
- Vật bỏ sót, ảnh và vùng: 0 vật bỏ sót được ghi trên 40 ảnh đã duyệt.
- Ca khó / phần còn lại, lỗi lặp và ví dụ: Ca khó 24/36 ảnh lỗi (66.7%), phần còn lại 0/4 ảnh lỗi. Lỗi lặp là sai_thuoc_tinh truncated theo R-08 (37/40 lỗi, 34 box chạm mép nhưng ghi no, 3 box không chạm mép nhưng ghi yes; ví dụ img_001.jpg #8 person, img_021.jpg có 6 box) vì khi sửa trên CVAT chưa cập nhật truncated theo quy tắc vị trí ≤ 2 px của v1.1. Lỗi thừa 3 box: img_009.jpg #130 person cao 16.6 px và img_039.jpg #456 rider cao 19.9 px (R-09), img_004.jpg #55 bicycle (R-01). Chi tiết ở reviews/round-03/qc_review.csv.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Máy chặn được truncated sai và box cao < 20 px vì R-08/R-09 quyết định hoàn toàn bằng toạ độ (script phát hiện 39/40 lỗi, dòng ghi [script] trong phiếu, người duyệt xác nhận); cần người đọc ảnh là img_004.jpg #55: box bicycle đúng schema, đủ kích thước nhưng bao vòi phun nước góc trên phải, không có xe đạp thật.

| Mã | Lỗi | Rule | Phạm vi | Ví dụ |
|---|---|---|---|---|
| Q01 | truncated sai | R-08 | 37 box / 21 ảnh | img_001.jpg #8, img_021.jpg (6 box) |
| Q02 | box cao < 20 px | R-09 | 2 box | img_009.jpg #130, img_039.jpg #456 |
| Q03 | box trên vật không có thật | R-01 | 1 box | img_004.jpg #55 |

## 5. Quyết định bàn giao

- Quyết định: Rework
- Lý do, người nhận và phạm vi sử dụng: 24/40 ảnh lỗi (60.0%) vượt ngưỡng 2% và có lỗi lặp (truncated, Q01); chưa bàn giao cho đội phát triển mô hình, nhãn hiện tại chỉ dùng làm bằng chứng QC, không dùng để huấn luyện.
- Nếu còn việc: Sửa trong Task calibration CVAT 37 box truncated (Q01), xóa 2 box < 20 px (Q02) và box img_004.jpg #55 (Q03); người điều phối 069 phân công người sửa; export theo đường dẫn prepare_calibration.py in ra, chạy build_final.py, mở vòng QC 4 duyệt toàn lô với người kiểm khác người sửa; giữ vòng 1–3.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: Q03 → submission/qc/reviews/round-03/qc_review.csv dòng img_004.jpg (object_id 55, thua, R-01) → submission/qc/labels_calibrated.json annotation id 55 (bicycle, bbox 776,39,115,87) → guideline_v1.1_calibrated.md R-01 (chỉ gán vật thật) → kết quả: box thừa, cần xóa.
