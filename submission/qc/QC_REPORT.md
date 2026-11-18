# Báo cáo QC — KhongBietNua

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Đặc tả và QC nhãn bounding box 2D (9 lớp) cho 40 ảnh đường phố; giới hạn: mẫu nhỏ, ảnh Wikimedia chọn tay, thiên về xe máy và tuk-tuk, không đại diện cho phân bố thực tế và không dùng để huấn luyện hay quyết định an toàn.
- Nguồn và phép sử dụng dữ liệu: 40 ảnh Wikimedia Commons trong data/ATTRIBUTION.csv, giấy phép: CC BY-SA 4.0 (15), CC BY 2.0 (7), CC BY-SA 2.0 (6), CC BY 4.0 (5), CC0 (3), CC BY-SA 3.0 (3), Public domain (1); giữ ghi công, không sửa hay đổi tên ảnh, CC BY-SA yêu cầu chia sẻ tương tự khi phân phối lại.
- Manifest và checksum nhãn cuối: submission/qc/batch_manifest.json (SHA-256 cff35d03c42c05ceaddadc746562ebbb5a11c3929368d9086672e1f463401465); submission/qc/labels_calibrated.json (SHA-256 da2da74ff117ee72b2d5c0dc163dc8325c1a796be0b233ce32b3fcad50fcab10).
- Guideline và taxonomy khi gán / khi bàn giao: Gán Pha 3 theo guideline v1.0 và taxonomy v1.0 (car, truck, van, bus, bicycle, motorcycle, three_wheeler, person, ignore_region); bàn giao theo guideline v1.1 (guideline_change.json loại semantic, thêm R-13 đến R-17), taxonomy giữ v1.0 nên không đổi lớp và thuộc tính.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 120/120 (5 người, mỗi người 24 ảnh, mỗi ảnh 3 người gán).
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 689 cặp box ghép (mẫu số); IoU TB 0.846 (ngưỡng 0.85, chưa đạt); cùng lớp 98.3% (đạt); cùng occluded_level 53.4%, cùng truncated 85.9%.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: chưa ghép 167/381 (A/B), loại do ignore 0; 269 ca bất đồng ignore, nhiều nhất ở img_032 (54 ca), img_006, img_011, img_019 (23 ca mỗi ảnh) và img_025 (20 ca).
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: img_011 (xe độ làm từ phụ kiện kim loại: mục 6 của v1.0 ghi còn nhận diện là xe máy thì `motorcycle`, một bước calibration từng xóa nhầm box này và đã hoàn lại) và img_040 (xe máy của người đội mũ bảo hiểm chỉ lộ gương và tay lái ở mép dưới, chưa có box; mục 6 nhắc xe máy bị cắt mép nhưng không nói rõ có gán hay không). Cách kiểm: mở ảnh gốc, đối chiếu mục 6 và R-03; ca img_040 chưa được coach xác nhận.

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: 1389 ca trên 38/40 ảnh: bo_sot_thua 393 (R-13), sai_thuoc_tinh 372 (R-14 và R-16), bat_dong_ignore 269 (R-13), iou_thap 252 (R-15), co_can_review 91 (R-17), sai_lop 12 (mục 2.2); người chốt, bản sửa và người kiểm lại ở submission/qc/calibration_decisions.csv.
- Tác động v1.1 lên nhãn và ảnh: phạm vi cả 40 ảnh (semantic, pham_vi lo); gộp cụm vật nhỏ vào ignore_region (R-13) ở img_008, img_009, img_023, img_039; xóa box dưới 20 px ở img_031 (R-05) và box trùng ở img_007; đổi bán tải img_007 từ car sang truck; áp R-16 (truncated theo chạm mép) và R-17 (tắt can_review) cho cả lô; taxonomy không đổi nên không cần mapping.
- Tham chiếu bằng chứng khi Rework: Vòng 1 duyệt 40/40 ảnh, phiếu ghi 0 lỗi; khi đối chiếu v1.0 mục 6 phát hiện box xe độ ở img_011 bị xóa nhầm; đã hoàn lại box, cập nhật bảng quyết định và duyệt lại ở vòng 2; các ảnh còn lại nhãn không đổi nên dùng lại kết luận vòng 1.

## 4. Kết quả duyệt

- Vòng QC: 2
- Người review và ngày: 048 (img_001–img_009), 344 (img_010–img_019), 354 (img_020–img_029), 034 (img_030–img_040); ngày 2026-11-18
- Đã duyệt / cả lô: 40/40
- Ảnh lỗi / ảnh đã duyệt: 0/40
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 0/436
- Vật bỏ sót, ảnh và vùng: phiếu vòng 2 không ghi vật bỏ sót nào (0).
- Ca khó / phần còn lại, lỗi lặp và ví dụ: ca_kho đã duyệt 38/38, con_lai 2/2; phiếu không ghi lỗi nên không có lỗi lặp; dẫn submission/qc/reviews/round-02/qc_review.csv.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Máy chặn: validate_labels.py cảnh báo box cao dưới 20 px vi phạm R-05 (img_031 #158 ở nhãn 034 và img_039 #129 ở nhãn 048). Cần người đọc ảnh: box xe độ ở img_011, máy chỉ thấy hình xe máy và không phân biệt được với điêu khắc, phải đọc mục 6 của v1.0 và nhìn ảnh mới quyết được.

## 5. Quyết định bàn giao

- Quyết định: Release
- Lý do, người nhận và phạm vi sử dụng: Vòng 2 duyệt đủ 40/40 ảnh, ảnh lỗi 0/40, annotation lỗi 0/436, không còn can_review và không có ca guideline tồn đọng; người nhận là coach lớp AI20K K5-L23 (bài Day 07); chỉ dùng làm bộ nhãn minh họa cho bài thực hành, không dùng huấn luyện hay đánh giá mô hình thật.
- Nếu còn việc: img_040: hỏi coach có gán box xe máy chỉ lộ gương và tay lái không (070, đối chiếu với ca tham chiếu của coach); `occluded_level` chưa được chấm lại từng box theo R-14 sau calibration (nhóm, kiểm lại trên nhãn cuối bằng ảnh vẽ box)
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: img_011.jpg: phiếu submission/qc/reviews/round-02/qc_review.csv, mục 6 của guideline v1.0 và R-10, nhãn cuối submission/qc/labels_calibrated.json có 1 box motorcycle ở ảnh này, kết quả khớp quy tắc.
