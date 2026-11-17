# Ghi chú calibration — reviewer 102

## Nguyên tắc áp dụng

- Dùng đồng thuận 2/3 làm phương án ban đầu, nhưng kiểm box với ảnh gốc; ưu tiên box theo vật thay vì lấy trung bình cơ học khi box gộp nhiều vật.
- Với ca bất đồng lớp, đối chiếu cấu tạo xe và quy tắc phạm vi; không gán đồ chơi, tượng, hình in hoặc phản chiếu.
- Vật dưới 20 px hoặc không tách được trong cụm dày xử lý theo R-06; box người/xe riêng theo R-02/R-03.
- Ảnh nhòe/tối chỉ giữ vật khi nhận diện chắc lớp và vị trí theo R-09.

## Quyết định và đầu ra đã chốt

- Reviewer 102 đã hoàn tất 1.919/1.919 dòng trong `calibration_decisions.csv`, ghi guideline v1.1 và phạm vi cho từng case. 296 case đánh dấu `lo`; R-09 khiến phạm vi kiểm lại thành toàn bộ 40 ảnh.
- Taxonomy giữ v1.0. Guideline v1.1 thêm R-09 về xe có nắp thùng và nhận diện phương tiện trong ảnh tối/nhòe.
- `img_002`: xe sát mép phải là một van; giữ một box van, bỏ truck trùng.
- `img_008`: giữ phương tiện nền nhận diện được; không giữ box trùng/không rõ trong vùng tối.
- `img_014`: giữ hai người rõ, bỏ box theo vệt nhòe không nhận diện được.
- `img_015`: giữ các ô tô riêng, không bao bóng phản chiếu mặt đường.
- `img_016`: bỏ truck trùng tuk-tuk trái; giữ van, mô tô và hai three-wheeler riêng.
- `img_020`, `img_033`, `img_038`: giữ ảnh rỗng annotation cho phản chiếu, ma-nơ-canh/vật trưng bày, và 24 xe mô hình.
- `img_037`: pickup nắp cao là truck.
- `img_040`: xe giữa là three-wheeler; taxi tiền cảnh có `occluded_level=1`, `truncated=yes` theo xác nhận 101 và được 102 kiểm lại.
- `labels_calibrated.json`: 40 ảnh, 403 annotation (392 đối tượng + 11 ignore_region); không còn `can_review=true`.

## Kết quả QC

- Vòng 1 được giữ làm lịch sử; vòng 2 là bằng chứng hiện hành sau khi chuẩn hóa newline của bảng quyết định (nội dung quyết định không đổi). Vòng 2 đã rà 40/40 ảnh. Kết quả REWORK: 2/40 ảnh có lỗi (5,0%); 7/392 đối tượng có lỗi (1,8%); 0 vật bỏ sót được ghi riêng.
- `img_003`: object 19 box người rộng; object 33 trùng object 32.
- `img_030`: objects 267, 268, 269, 276, 277 gộp nhiều xe hoặc lệch khỏi một xe.
- Phiếu chi tiết ở `reviews/round-02/qc_review.csv`; giữ cả snapshot vòng 1 và 2. Cần sửa 7 annotation, tạo vòng 3 và duyệt lại đủ 40 ảnh trước khi phát hành.

## Ghi chú lịch sử

- Reviewer 101 đã chốt trước đó: C037/C038 (`img_002`) là van; `img_038` loại 24 xe mô hình; taxi `img_040` có `occluded_level=1`, `truncated=yes`. Reviewer 102 đã đối chiếu và giữ các quyết định này trong nhãn cuối.
- IAA gốc ghi đường dẫn với dấu phân cách Windows; 48 input hashes đã được kiểm tra khớp từng giá trị, rồi chuẩn hóa thành đường dẫn POSIX để pipeline Linux dùng được. Không tính lại hoặc thay đổi số liệu IAA.
