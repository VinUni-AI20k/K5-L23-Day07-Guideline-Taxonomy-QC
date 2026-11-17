# Báo cáo QC — T012

**Bản nháp, trạng thái Hold.** Số liệu dưới đây phản ánh lượt so sánh nhãn độc lập trước calibration; chưa phải kết quả duyệt nhãn cuối. Các ca tự động chưa được xem và chốt từng dòng.

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Đặc tả và kiểm tra nhãn bounding box 2D cho 40 ảnh; tập nhỏ không chứng minh tính đại diện cho mọi điều kiện giao thông.
- Nguồn và phép sử dụng dữ liệu: Xem `data/ATTRIBUTION.csv` cho từng ảnh; cần đối chiếu điều kiện sử dụng trước khi bàn giao.
- Manifest và checksum nhãn cuối: Chưa có `batch_manifest.json` và checksum nhãn cuối; bổ sung sau calibration.
- Guideline và taxonomy khi gán / khi bàn giao: Đầu vào IAA dùng taxonomy v1.0 và `submission/guidelines/guideline_v1.0_agreed.md`; tài liệu ghi cần nhóm xác nhận CP2. Đã chuẩn bị `guideline_v1.1_calibrated.md` làm bản làm việc giữ nguyên quy tắc v1.0, cùng `submission/guideline_change.json`; phiên bản bàn giao chưa được chốt.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 120/120 lượt, 40 ảnh, 5 người; mỗi người 24 ảnh.
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 914 cặp box ghép; IoU trung bình 0,785; cùng lớp 95,8% trên 914 cặp. Ngưỡng tương ứng 0,85 và 95%; kết quả tổng CHƯA ĐẠT do IoU. Các số chỉ tính cặp ghép IoU ≥ 0,5, không chứng minh không bỏ sót.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: 367/352 box chưa ghép ở hai phía của các phép so sánh; 15 box bị loại do ignore; 377 dòng bất đồng ignore. Đây là số theo cặp so sánh, không phải số vật duy nhất. Chi tiết `iaa_summary.md` và `calibration_candidates.csv`.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: Chưa xác nhận ca cả hai cùng sai; cần đối chiếu ảnh gốc và quy tắc, kể cả ảnh không có bất đồng.

### Tổng hợp bất đồng để ưu tiên xử lý

Có 1.919 dòng trên 38 ảnh: 530 IoU thấp, 498 khác thuộc tính, 460 bỏ sót/thừa, 377 bất đồng ignore, 38 khác lớp và 16 cờ `can_review`. Một đối tượng có thể xuất hiện nhiều lần do so sánh theo cặp; mỗi dòng là ứng viên cần xem, không tự động là lỗi đã xác nhận. Đồng thuận thuộc tính trên 914 cặp ghép: `occluded_level` 48,8%, `truncated` 92,1%.

Ưu tiên ảnh nhiều dòng: `img_003` (183), `img_021` (159), `img_006` (142), `img_008` (112), `img_032` (111). Rà R-02/R-03 cho ranh giới và tách người/xe, R-06 cho vật nhỏ/vùng ignore, R-07 cho che khuất và cắt mép. Bốn cảnh báo box nhỏ: 101 `img_003 #22`, `img_023 #174`; 103 `img_021 #164`, `img_025 #228`.

Kiểm tra bổ sung `img_003 #22` của 101: box cao 18,7 px, dưới ngưỡng 20 px của R-06. Ảnh gốc có cảnh đông người và xe; cần đối chiếu vùng tương ứng, xử lý theo R-06 và kiểm lại box/vùng ignore trong bản calibration. Chưa khẳng định đã sửa hoặc đã chốt vùng ignore.

Ảnh chồng nhãn `img_038` cho thấy các box của 103 phủ lên xe mô hình trong tủ. Theo R-01, đồ chơi và mô hình ngoài phạm vi; quyết định loại các box này đã được ghi cho các dòng liên quan, nhưng bản sửa chưa được kiểm lại. Ở `img_002`, các ca C037–C054 liên quan đến đối tượng chưa ghép, khác lớp và box lệch; một số quyết định đã được ghi theo R-02 và R-04.

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: `calibration_decisions.csv` có nội dung ở 1.919 dòng, trong đó 68 dòng ghi theo quyết định của 101 và 1.851 dòng là đề xuất AI. Sau khi rà thêm `img_033` và C1162 ở `img_025`, còn 192 dòng ghi rõ cần xem lại vì chưa đủ căn cứ chọn tự động và 1.849 dòng chưa có phạm vi hoàn chỉnh. Tại `img_038`, AI đã đối chiếu ảnh và xác nhận bản nháp còn 0 annotation sau khi loại 24 box mô hình. Tại `img_033`, AI đã đối chiếu bốn ca vùng ignore phủ vật trưng bày và xác nhận bản nháp còn 0 annotation. Bản nháp cục bộ `work/calibration_preview_img002_025_038_040.json` cũng cập nhật 7 box và một lớp ở `img_002`, chuyển một box thấp hơn 20 px ở `img_025` thành ignore và sửa thuộc tính một box ở `img_040`; bản nháp hợp lệ về cấu trúc nhưng chưa được duyệt QC chính thức, chưa phải nhãn cuối và không thuộc gói bàn giao.
- Tác động v1.1 lên nhãn và ảnh: Chưa xác định; nhóm cần chốt thay đổi guideline và phạm vi kiểm lại.
- Tham chiếu bằng chứng khi Rework: Chưa có vòng QC hoặc bản sửa để đối chiếu.

## 4. Kết quả duyệt

- Vòng QC: Chưa có vòng duyệt nhãn cuối.
- Người review và ngày: Chưa thực hiện; `TEAM.md` chỉ định 102 là người review bản cuối.
- Đã duyệt / cả lô: Chưa có kết quả duyệt chính thức / 40 ảnh.
- Ảnh lỗi / ảnh đã duyệt: Chưa xác định; chưa có phiếu QC.
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: Chưa xác định; chưa có phiếu QC.
- Vật bỏ sót, ảnh và vùng: Chưa xác định sau calibration; các box chưa ghép chỉ là ứng viên cần đối chiếu.
- Ca khó / phần còn lại, lỗi lặp và ví dụ: Xem danh sách ưu tiên ở mục 2; chưa kết luận tỷ lệ lỗi hay lỗi lặp từ phiếu QC.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Validator kiểm tra bbox vượt biên và lớp ngoài taxonomy; người xem ảnh phải phát hiện box ôm sai vật, bỏ sót chung hoặc gán mô hình làm xe thật.

## 5. Quyết định bàn giao

- Quyết định: Hold (tạm thời, chờ nhóm xác nhận).
- Lý do, người nhận và phạm vi sử dụng: IAA chưa đạt; calibration, nhãn cuối và QC độc lập chưa hoàn tất trong hồ sơ. Việc bàn giao đã được xác nhận, nhưng repo chưa có manifest nhãn cuối hay kết quả vòng QC để đối chiếu nội dung bàn giao. Người nhận và phạm vi sử dụng chưa được ghi rõ.
- Nếu còn việc: Rà và chốt ứng viên trong `calibration_candidates.csv`, xác nhận guideline và nhãn, tạo nhãn cuối và manifest; reviewer 102 duyệt toàn lô và cập nhật báo cáo cùng bằng chứng. Còn 1.849 dòng thiếu phạm vi hoàn chỉnh; các ảnh ở `work/review_draft/` chỉ để xem sơ bộ và không phải vòng QC chính thức. Nội dung ghi chú 101, 104 và 105 đã được xác nhận trong phiên làm việc; các chi tiết trải nghiệm chưa có vẫn cần bổ sung. Hồ sơ còn thiếu số vòng QC hợp lệ và `reviews/round-01/qc_result.json`.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: Ví dụ C1745 dẫn tới `img_038.jpg`, R-01, và nhãn độc lập 101/103; cần nhóm xác nhận từng box và lưu quyết định calibration trước khi coi là đã đóng ca.
