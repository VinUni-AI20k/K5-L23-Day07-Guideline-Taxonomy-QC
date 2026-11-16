# Báo cáo QC — Group-01

Báo cáo kiểm định chất lượng dữ liệu gán nhãn 2D Bounding Box lô 40 ảnh Day 07.

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Huấn luyện và kiểm thử mô hình phát hiện đối tượng 2D (ADAS/ITS), tập trung vào các thực thể tham gia giao thông thực tế. Dữ liệu gồm 40 ảnh tuyển chọn phục vụ chuẩn hóa quy trình QC và hiệu chuẩn ca khó.
- Nguồn và phép sử dụng dữ liệu: 40 ảnh nguồn mở từ Wikimedia Commons, có giấy phép CC BY / CC BY-SA / CC0 đầy đủ thông tin tác giả tại ATTRIBUTION.csv.
- Manifest và checksum nhãn cuối: batch_manifest.json (SHA-256 nhãn cuối labels_calibrated.json: e3de4771434296ce09cfd7382795c193caaa9b7c67f19284e744f94d4c1e9b59).
- Guideline và taxonomy khi gán / khi bàn giao: Khi gán độc lập sử dụng taxonomy v1.0 và guideline_v1.0_agreed.md; khi bàn giao áp dụng guideline_v1.1_calibrated.md và giữ nguyên taxonomy v1.0 (9 lớp, 3 thuộc tính).

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 80/80 lượt gán hoàn thành (đạt 100%), mỗi ảnh được đúng 2 annotator gán độc lập (4 thành viên: 111, 222, 333, 444).
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 370 cặp box ghép, IoU trung bình toàn lô 0.922 (đạt ngưỡng >= 0.85), đồng thuận lớp 94.3% (349/370 cặp).
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: 48 box chưa ghép phía A, 87 box chưa ghép phía B; 0 box bỏ qua do ignore, 11 ca bất đồng vùng ignore ở các cụm hậu cảnh xa.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: img_006.jpg và img_034.jpg có annotator ban đầu nhầm xích lô thành motorcycle; img_020.jpg nhầm bóng gương phản chiếu; img_033.jpg nhầm ma-nơ-canh; img_024.jpg nhầm vỏ xe trên nóc xe wagon.

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: Đã xử lý 399 ca bất thường (C001-C399), dẫn chiếu các quy tắc R-01 đến R-09 trong calibration_decisions.csv, xác nhận bởi annotator 111.
- Tác động v1.1 lên nhãn và ảnh: Làm rõ quy tắc ôm sát biên thị giác R-01, quy chuẩn xích lô thành bicycle theo R-04, loại trừ hoàn toàn đối tượng phi thực R-02, giải tỏa 100% cờ can_review về false.
- Tham chiếu bằng chứng khi Rework: Bản sửa nhãn hiệu chuẩn labels_calibrated_bd1c80bbfce97bd5.json được sinh từ consensus draft sau khi rà soát và khắc phục triệt để các ca lệch.

## 4. Kết quả duyệt

- Vòng QC: 1
- Người review và ngày: 111 - 2026-11-17
- Đã duyệt / cả lô: 40/40 ảnh đã duyệt (100% lô)
- Ảnh lỗi / ảnh đã duyệt: 0/40 = 0.0% (đạt ngưỡng chấp nhận <= 2.0%)
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 0/502 = 0.0%
- Vật bỏ sót, ảnh và vùng: 0 vật bỏ sót sau vòng duyệt kiểm tra toàn diện
- Ca khó / phần còn lại, lỗi lặp và ví dụ: Ca khó đã duyệt 32/32 ảnh (0 lỗi), phần còn lại 8/8 ảnh (0 lỗi); không có lỗi lặp lại.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Lỗi máy chặn được: box vượt biên ảnh x2 > width (như img_040.jpg box 504 bị overflow 0.01px); Lỗi cần người đọc ảnh: phân biệt người thật đang lái xe với ma-nơ-canh tủ kính (img_033.jpg) và chân dung in trên pano quảng cáo (img_018.jpg).

## 5. Quyết định bàn giao

- Quyết định: Release
- Lý do, người nhận và phạm vi sử dụng: Lô dữ liệu đạt 100% tiêu chuẩn chất lượng QC: tỉ lệ ảnh lỗi 0.0% <= 2%, 0 box can_review tồn đọng, toàn bộ 40 ảnh đã được rà soát trực quan. Bàn giao cho nhóm Huấn luyện mô hình ADAS/ITS.
- Nếu còn việc: Không còn việc tồn đọng; toàn bộ hồ sơ kỹ thuật, manifest, COCO 1.0 và nhãn CSV đã được đóng băng.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: Ca C006 (img_002.jpg - R-03: car carrier truck kèm 8 car); ca C015 (img_004.jpg - R-07: tuk-tuk Pattaya); ca C032 (img_006.jpg - R-04: xích lô bicycle); ca C085 (img_020.jpg - R-02: loại bỏ phản chiếu gương).
