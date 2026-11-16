# Báo cáo QC — Nhóm Ngoc

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Thực hành đặc tả và QC bbox người/phương tiện trên 40 ảnh; chưa đánh giá tính đại diện cho vận hành. Bốn người cùng xây dựng và kiểm tra bộ nhãn xuất phát từ mô hình.
- Nguồn và phép sử dụng dữ liệu: Giữ nguyên data/ATTRIBUTION.csv và điều kiện giấy phép từng ảnh của bộ dữ liệu lớp.
- Manifest và checksum nhãn cuối: submission/qc/batch_manifest.json; labels_calibrated.json SHA-256 e2945df0863bc0f8112b75e0f4e093c1aa412073106b4eb44bf6ea27b92a41a8.
- Guideline và taxonomy khi gán / khi bàn giao: Bản nguồn dùng guideline/taxonomy v1.0; hồ sơ bàn giao guideline v1.1 editorial, taxonomy v1.0, không đổi bbox hoặc nghĩa quy tắc.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 80/80 lượt ảnh có trong 4 file, mỗi file 20 ảnh; đây là độ phủ của các phần bàn giao từ bộ nhãn cả bốn người cùng thực hiện.
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: Script so sánh được 321 cặp, IoU TB 1.000, cùng lớp 321/321 = 100%; các phần chia cùng nguồn nên số này chỉ thể hiện tính nhất quán của sản phẩm chung.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: Script không phát hiện box chưa ghép hay ca bất thường giữa các phần chia; xem iaa_summary.md và calibration_candidates.csv. Không sửa tay đầu ra script.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: Chưa có bằng chứng đối chiếu ca tham chiếu coach. Về nguyên tắc, hai bản sao đều giữ một lỗi bỏ sót từ nguồn vẫn có thể đạt IoU 1; đây là giới hạn phương pháp, không phải lỗi quan sát được trên một ảnh cụ thể.

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: Script tạo 0 ca cần calibration; calibration_decisions.csv giữ header, không ghi cuộc họp hay quyết định từng ca chưa có. 236 kiểm toàn bộ; 194 kiểm phần 202, 202 kiểm phần 231, 231 kiểm phần 236 theo xác nhận người dùng.
- Tác động v1.1 lên nhãn và ảnh: Bổ sung mã R-01…R-11 và hồ sơ nguồn, không đổi nhãn. Điểm truncated còn chưa chốt: bảng thuộc tính dùng ngưỡng 10%, R-03 nói cắt mép là yes.
- Tham chiếu bằng chứng khi Rework: Vòng 1 được giữ nguyên; mở vòng 2 sau khi đính chính mô tả cách làm chung và cập nhật checksum. Bbox không thay đổi, phiếu kiểm dùng cùng xác nhận của người dùng.

## 4. Kết quả duyệt

- Vòng QC: 2
- Người review và ngày: Nguyễn Thị Ngọc (236, 2A202603236) kiểm toàn bộ; Đào Quang Tuấn (194, 2A202603194) kiểm phần Nguyễn Thanh Thản (202, 2A202603202); Nguyễn Thanh Thản kiểm phần Đinh Tuấn Thành (231, 2A202603231); Đinh Tuấn Thành kiểm phần Nguyễn Thị Ngọc. Ngày ghi nhận xác nhận 2026-11-16; không khẳng định ngày thực hiện lượt kiểm trước đó.
- Đã duyệt / cả lô: 40/40 ảnh theo xác nhận người dùng. Nhật ký kiểm chéo bổ sung có 60 lượt ảnh, không cộng thành số ảnh duy nhất.
- Ảnh lỗi / ảnh đã duyệt: 0/40 = 0% theo xác nhận người dùng rằng bộ nhãn chính xác.
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 0/321 = 0% theo xác nhận người dùng.
- Vật bỏ sót, ảnh và vùng: Không có vật bỏ sót được người dùng báo; đây là ghi nhận từ xác nhận chung, không có biên bản nguyên thủy từng box.
- Ca khó / phần còn lại, lỗi lặp và ví dụ: Script so sánh không cờ ảnh do các file cùng nguồn; QC vẫn phủ đủ 40 ảnh. Các ca khó trong guideline là kết quả cả bốn người cùng xây dựng.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Script kiểm được box vượt kích thước ảnh, thiếu ảnh hoặc thuộc tính sai; người kiểm phải xác nhận đúng vật, đúng lớp và không bỏ sót. Không khẳng định đã quan sát một lỗi cụ thể khi chưa có biên bản.

## 5. Quyết định bàn giao

- Quyết định: Hold
- Lý do, người nhận và phạm vi sử dụng: Hồ sơ nhãn đã có kiểm chung và kiểm chéo, nhưng quy tắc truncated còn mâu thuẫn. Nhóm ghi nhận cách thực hiện là cả bốn người cùng làm. Nộp coach để đánh giá đúng phạm vi thực hành; không mô tả là đã đủ điều kiện Release.
- Nếu còn việc: Cả nhóm chốt cách hiểu truncated và đối chiếu ca tham chiếu coach. Thành viên đọc/xác nhận phần bàn giao của sản phẩm chung trước khi tự commit; chưa có commit/push tự động.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: Có thể tra img_001.jpg từ assignment.csv → file 202.json/231.json → labels_calibrated.json → R-01 và phiếu vòng 2; đây là chuỗi đường dẫn máy kiểm được, chưa có xác nhận một người ngoài nhóm đã kiểm ngược.

## 6. Nguồn xác nhận

Phiếu qc_review.csv được ghi từ xác nhận của người dùng: 236 kiểm đủ 40 ảnh/321 bbox và bộ nhãn chính xác. peer_reviews.csv ghi chuỗi kiểm chéo do người dùng cung cấp. Trợ lý tổng hợp tài liệu, chia dữ liệu và chạy script; không thực hiện kiểm trực quan mới. Xem REVIEW_ATTESTATION.md và LABEL_PROVENANCE.md.

## Đối chiếu mã thành viên

| Mã thành viên | Họ và tên | MSHV |
|---|---|---|
| 202 | Nguyễn Thanh Thản | 2A202603202 |
| 231 | Đinh Tuấn Thành | 2A202603231 |
| 194 | Đào Quang Tuấn | 2A202603194 |
| 236 | Nguyễn Thị Ngọc | 2A202603236 |

## Làm rõ tác giả sản phẩm chung

Người dùng xác nhận cả bốn thành viên cùng tạo guideline và bộ nhãn trong repo nguồn. Việc file nguồn mang tên một người không có nghĩa chỉ người đó thực hiện. Nhóm tổ chức làm chung; các file theo mã được tách để bàn giao. Toàn bộ hồ sơ mô tả sản phẩm chung của cả bốn người; mỗi người có file bàn giao riêng theo phân công.
