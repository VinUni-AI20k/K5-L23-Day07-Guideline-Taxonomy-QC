# Báo cáo QC — T012

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Hiệu chỉnh và QC nhãn bounding box 2D cho 40 ảnh đường phố trong bài thực hành; lô tuyển chọn nhỏ, không đại diện cho dữ liệu vận hành nói chung.
- Nguồn và phép sử dụng dữ liệu: Nguồn, tác giả, giấy phép và URL theo từng ảnh nằm trong `data/ATTRIBUTION.csv`; manifest khóa checksum ảnh cho cả 40 ảnh.
- Manifest và checksum nhãn cuối: `submission/qc/batch_manifest.json`; SHA-256 manifest `7fc62252fe95c1c837eaadedb99a2c3f9a2062c8b2848fa90b178208d3e989da`. `labels_calibrated.json` có SHA-256 `57934c65d9339cba9f79ecffeb0219afa02a103094090f85e599ad67fe08b849`; CSV nhãn có SHA-256 `38a536ffe93bee84f89065b82ba72e3ee3ec260bd9352c8742469113098aa355`.
- Guideline và taxonomy khi gán / khi bàn giao: Nhãn độc lập dùng taxonomy v1.0 và guideline v1.0; bàn giao dùng `guideline_v1.1_calibrated.md`, taxonomy v1.0. v1.1 thêm R-09; đã hiệu chỉnh 403 annotation trên 40 ảnh, không đổi schema lớp/thuộc tính.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 120/120 lượt, 40 ảnh, 5 thành viên, 3 người gán mỗi ảnh.
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 914 cặp ghép; IoU TB 0,785/914; đồng thuận lớp 95,8%/914. Ngưỡng lần lượt là 0,85 và 95%; IAA chưa đạt do IoU.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: 367/352 box chưa ghép ở hai phía; 15 box được bỏ qua do ignore; 377 dòng bất đồng ignore trong hồ sơ calibration. Đây là thống kê cặp so sánh, không phải số vật duy nhất.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: Không có nhãn tham chiếu độc lập để kết luận hai người cùng sai. Vì vậy reviewer đối chiếu ảnh gốc, guideline và các vật ngoài phạm vi; đã loại mô hình ở `img_038`, ma-nơ-canh ở `img_033`, và phản chiếu ở `img_020` theo R-01.

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: Đã chốt 1.919/1.919 dòng trong `calibration_decisions.csv`; reviewer 102, guideline v1.1, không còn trường quyết định/phạm vi trống. 296 dòng đánh dấu tác động ngữ nghĩa `lo`; do R-09 là thay đổi ngữ nghĩa, phạm vi kiểm lại là 40/40 ảnh. Các ca cụ thể gồm C037–C038 (`img_002`, một van), các box nhòe (`img_014`), tuk-tuk (`img_016`), pickup (`img_037`), và thuộc tính taxi `img_040`.
- Tác động v1.1 lên nhãn và ảnh: Taxonomy giữ v1.0. Áp dụng R-09 để phân biệt `truck`/`van`/`bus` theo cấu tạo và bỏ box không nhận diện chắc trong ảnh tối/nhòe; cập nhật nhãn ở `img_002`, `img_008`, `img_014`, `img_015`, `img_016`, `img_037`, `img_040`. Bản xuất được tạo từ quyết định hiệu chỉnh và kiểm hợp lệ bằng `build_final.py`.
- Tham chiếu bằng chứng khi Rework: Vòng 2 phát hiện box sai vị trí/kích thước ở `img_003` (object 19) và các box gộp nhiều xe ở `img_030` (objects 267, 268, 269, 276, 277), cùng box trùng ở `img_003` (object 33). Chi tiết vùng và rule ở `reviews/round-02/qc_review.csv`; cần sửa rồi mở vòng 2, giữ nguyên snapshot vòng 2.

## 4. Kết quả duyệt

- Vòng QC: 2
- Người review và ngày: 102 — 17/11/2026.
- Đã duyệt / cả lô: 40/40 ảnh; vòng đầy đủ, không phải vòng demo.
- Ảnh lỗi / ảnh đã duyệt: 2/40 = 5,0%, vượt ngưỡng 2%.
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 7/392 = 1,8%; mẫu số loại 11 `ignore_region`. Bộ COCO có tổng cộng 403 annotation.
- Vật bỏ sót, ảnh và vùng: 0 vật bỏ sót được ghi nhận trong phiếu vòng 2; con số này chỉ phản ánh lượt rà bằng mắt, không phải bảo đảm không còn bỏ sót.
- Ca khó / phần còn lại, lỗi lặp và ví dụ: Lỗi vị trí/kích thước lặp lại ở cụm xe máy dày `img_030`; box người quá rộng và box trùng ở `img_003`. Rà lại theo R-02/R-03; khi không thể tách riêng xe trong cụm, dùng `ignore_region` cục bộ theo R-06.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Validator chặn box ngoài biên, lớp/thuộc tính sai taxonomy và dữ liệu sai cấu trúc; người review phải nhìn ảnh để phát hiện box gộp nhiều xe như `img_030` hoặc người/box sai ranh giới như `img_003`.

## 5. Quyết định bàn giao

- Quyết định: Rework
- Lý do, người nhận và phạm vi sử dụng: 102 đã review đủ 40 ảnh. Tỷ lệ ảnh lỗi 2/40 = 5,0% vượt giới hạn 2%, và lỗi box gộp xe lặp lại; chưa phát hành như lô đã được duyệt. Kết quả dành cho nhóm T012 để sửa và QC lại.
- Nếu còn việc: Reviewer 102 sửa 7 annotation được ghi trong `reviews/round-02/qc_review.csv`, cập nhật quyết định/nhãn theo R-02/R-03/R-06, chạy `build_final.py`, sau đó mở `qc_sample.py --round 3` và review lại toàn bộ 40 ảnh trước khi quyết định bàn giao.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: C037–C038 → R-09 → `img_002` van ở nhãn cuối; C1905/C1914 → R-07 → thuộc tính taxi `img_040`; QC object 267 → R-02 → `img_030`, vùng x=55–476, y=354–720, được ghi trong phiếu vòng 2. Manifest và snapshot vòng 2 khóa đúng SHA-256 nhãn nêu trên.
