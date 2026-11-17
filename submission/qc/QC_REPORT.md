# Báo cáo QC — Nhóm mã 101–104

> Trạng thái hồ sơ: **HOLD**. Báo cáo tổng hợp bằng chứng có trong repository tại thời điểm lập; không thay thế Calibration đã được nhóm chốt hoặc QC thủ công.

## 1. Mục đích QC

- Mục đích và giới hạn sử dụng: Đánh giá tính nhất quán và chuẩn bị kiểm soát chất lượng nhãn bounding box 2D trên 40 ảnh đường phố của bài lab Day 07. Đây là tập ảnh tuyển chọn để thực hành, chưa chứng minh tính đại diện cho dữ liệu vận hành.
- Nguồn và phép sử dụng dữ liệu: Nguồn/giấy phép của ảnh được ghi trong `data/ATTRIBUTION.csv`; cần giữ ghi công và tuân thủ điều kiện giấy phép khi chia sẻ.
- Manifest và checksum nhãn cuối: Chưa có `batch_manifest.json` và chưa có checksum nhãn cuối; chưa tạo bộ nhãn calibrated được phê duyệt.
- Guideline và taxonomy khi gán / khi bàn giao: Bốn lượt COCO độc lập dùng taxonomy/guideline v1.0. `guideline_v1.1_calibrated.md` hiện là dự thảo editorial; taxonomy và ngưỡng `rules` không đổi.

## 2. Quy trình gán nhãn và phân công

- Lượt hoàn thành / được giao: 80/80 lượt; 40 ảnh, 4 thành viên, 2 annotator/ảnh theo `submission/qc/assignment.csv`.
- Khối lượng COCO độc lập: `101.json` 224 annotation/20 ảnh; `102.json` 124/20; `103.json` 206/20; `104.json` 193/20. Tổng 747 annotation qua bốn file độc lập, gồm các vùng `ignore_region`; đây không phải số annotation của một bộ nhãn cuối.
- Kiểm tra cấu trúc: `validate_labels.py --all` xác nhận cả bốn file hợp lệ cấu trúc, mỗi file đủ 20 ảnh. Còn cảnh báo `img_031.jpg` #109 của 104 có bbox 16×19 px, cần reviewer xem ảnh theo ngưỡng tối thiểu 20 px. Validator không xác nhận độ chính xác nội dung.
- Công cụ/quy trình: Repository hướng dẫn gán bằng CVAT, xuất COCO, so sánh bằng `qc_compare.py` và tạo lớp phủ bằng `viz_disagreement.py`. Bằng chứng ghi nhận các đầu ra script đã có; chưa có bằng chứng vòng duyệt thủ công toàn bộ ảnh.

## 3. Phương pháp và kết quả IAA

- Phương pháp: Ghép box 1–1 theo IoU tối thiểu 0.50, không dùng lớp để ghép; tính IoU trung bình và đồng thuận lớp trên các cặp ghép. Ngưỡng IAA của taxonomy v1.0 là IoU TB ≥ 0.85 và cùng lớp ≥ 95%. IAA là phép đo đồng thuận, không phải chuẩn vàng xác định nhãn đúng.
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 295 cặp trên 40 ảnh; IoU TB 0.969 (0.969182); cùng lớp 289/295 = 97.97% (98.0%). Kết quả tổng đạt hai ngưỡng IAA về IoU và lớp.
- Đồng thuận thuộc tính trên 295 cặp: `occluded_level` 92.2%; `truncated` 92.5%. Đây là chỉ số mô tả, không phải cổng đạt/trượt bổ sung trong ngưỡng IAA được cấu hình.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: Báo cáo IAA cộng gộp 102 box chưa ghép phía A và 37 phía B; 1 trường hợp được bỏ qua do ignore; có 27 ca bất đồng `ignore_region`. Các giá trị chưa ghép là số theo phía trong tổng hợp cặp, không phải số đối tượng lỗi đã xác nhận.
- Cặp cần lưu ý: `101|102` có 38/41 cùng lớp = 92.7%, dưới ngưỡng 95%; IoU TB 0.999. Các cặp còn lại đạt ngưỡng lớp được báo cáo: `101|104` 97.1%, `102|103` 100%, `103|104` 100%.

## 4. Các vấn đề chất lượng được phát hiện

230 ca trên 32 ảnh được script gắn cờ để điều tra:

| Nhóm bất đồng | Số ca | Ý nghĩa |
|---|---:|---|
| Bỏ sót hoặc gán thừa (`bo_sot_thua`) | 125 | IAA một phía không xác định được annotation nào đúng |
| Thuộc tính (`sai_thuoc_tinh`) | 42 | Cần đối chiếu thuộc tính với phần nhìn thấy |
| Vùng ignore (`bat_dong_ignore`) | 27 | Cần kiểm tra vùng ignore và các đối tượng cá thể |
| Box/IoU (`iou_thap`) | 24 | Cần kiểm tra biên box theo R-01 |
| Lớp (`sai_lop`) | 6 | Cần áp dụng định nghĩa lớp của v1.0 |
| Cờ review (`co_can_review`) | 6 | Cần xử lý trạng thái chưa chắc chắn |

Đây là số ca bất đồng do script phát hiện, không phải 230 lỗi được xác nhận. Một số vấn đề có thể cùng phát sinh từ cách hiểu quy tắc; IAA không phát hiện trường hợp mọi annotator cùng bỏ sót hoặc cùng gán sai.

## 5. Tình trạng Calibration

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: 0/230 ca được nhóm xác nhận đã chốt. `calibration_decisions.csv` còn 230 dòng `CHỜ REVIEW THỦ CÔNG:`; chưa có người chốt, phiếu sửa hoặc kiểm lại được xác nhận.
- Hỗ trợ triage: `calibration_proposals.csv` nối 230 case với annotation nguồn, thuộc tính, IoU và rule gợi ý; crop định vị được tạo trong `work/calibration_review/cases/`. Bộ `work/calibration_review/proposed_calibrated.json` là bản xem xét riêng dựa trên consensus draft, không phải nhãn cuối. Các công cụ không sửa nhãn gốc; chưa có sửa CVAT nào được xác nhận.
- Tác động v1.1 lên nhãn và ảnh: Chưa áp dụng. Dự thảo v1.1 chỉ bổ sung cách tổ chức review; không đổi định nghĩa taxonomy, quy tắc gán nhãn hoặc ngưỡng. Chưa có nhóm phê duyệt thay đổi.
- Tham chiếu bằng chứng khi Rework: Chưa có vòng Rework/export sửa. Giữ nguyên COCO nguồn, `calibration_candidates.csv`, `calibration_decisions.csv` và ảnh gốc; sau khi nhóm chốt cần lưu COCO export và bằng chứng review gắn với từng case.

## 6. Tình trạng kiểm tra QC

- Vòng QC: Chưa mở vòng 1; chưa có số vòng QC đang nộp.
- Người review và ngày: Chưa có reviewer QC hoặc ngày review được xác nhận.
- Đã duyệt / cả lô: 0/40 ảnh có bằng chứng QC chính thức; đây không phải kết quả 0 lỗi.
- Ảnh lỗi / ảnh đã duyệt: N/A; chưa có ảnh được QC thủ công.
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: N/A; chưa có annotation nào được tính là đã QC.
- Vật bỏ sót, ảnh và vùng: Chưa có vật bỏ sót được reviewer xác nhận. 125 ca `bo_sot_thua` chỉ là các trường hợp cần phân xử.
- Ca khó / phần còn lại, lỗi lặp và ví dụ: 230 ca IAA chưa chốt; `img_031.jpg` #109 có box 16×19 px cần review ảnh. Không quy thành lỗi đã xác nhận nếu chưa xem nội dung.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Máy phát hiện được box dưới ngưỡng 20 px; chỉ reviewer đối chiếu ảnh mới xác định được box có đúng đối tượng, đúng lớp, đúng ranh giới và có bỏ sót hay không.
- Tỷ lệ lỗi QC: N/A; chưa có mẫu QC được duyệt nên không có mẫu số hợp lệ để tính tỷ lệ.

## 7. Rủi ro còn tồn tại

- Chưa phân xử bất đồng về bỏ sót/thừa, lớp, box, thuộc tính và ignore.
- IAA cao không loại trừ lỗi chung của cả hai annotator trong một ảnh.
- Một cặp annotator (`101|102`) chưa đạt ngưỡng đồng thuận lớp; cần calibration cụ thể.
- Bản consensus là bản nháp tự động; không phải nhãn đã được xác nhận bằng ảnh.
- Chưa có nhãn cuối, manifest/checksum, review QC, hay kết quả QC có thể tái lập.
- Box nhỏ cảnh báo ở `img_031.jpg` #109 chưa được con người đánh giá.

## 8. Kết luận và kiến nghị

- Quyết định: Hold
- Lý do, người nhận và phạm vi sử dụng: Không phát hành nhãn cho huấn luyện/đánh giá vì calibration, nhãn cuối và QC thủ công chưa hoàn tất. Nhóm 101–104 cần chốt các case; người được nhóm giao thực hiện sửa CVAT; reviewer độc lập kiểm export và kết quả.
- Nếu còn việc: Chốt đủ 230 dòng trong `calibration_decisions.csv`; thực hiện và lưu export sửa theo đúng quy trình `prepare_calibration.py`; chạy `build_final.py`; mở QC vòng 1, kiểm ảnh và annotation, điền phiếu thực tế, chạy `qc_report.py`; sau đó chạy lại `check_submission.py --round 1`. Không điền người chốt/reviewer thay cho người thực hiện.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: Số liệu IAA xem `iaa_summary.json`/`.md`; từng ca xem `calibration_candidates.csv`, `calibration_decisions.csv` và `calibration_proposals.csv`; ảnh gốc tại `data/images/`, lớp phủ và crop hỗ trợ trong `work/`. Chưa có nhãn calibrated chính thức để kiểm ngược.

## 9. Trạng thái hồ sơ nộp

`check_submission.py --round 1` chưa thể đạt do chưa có vòng QC số 1 và `qc_result.json`; báo cáo không khai báo một vòng chưa diễn ra. Trạng thái Hold phản ánh đúng bằng chứng hiện có.
