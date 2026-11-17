# Ghi chú làm việc calibration

## Nguyên tắc đã thống nhất khi rà

- Khi hai trong ba người gán gần giống nhau, dùng phương án đó làm đề xuất mặc định để rà nhanh; kiểm tra các box chỉ cùng một vật và phù hợp guideline.
- Khi ba phương án khác nhau rõ rệt, đối chiếu ảnh gốc và guideline để lựa chọn.
- Khi chỉ một người vẽ box, dùng box đó làm phương án mặc định, sau khi kiểm tra vật thuộc phạm vi và phù hợp guideline.
- Với thuộc tính, ưu tiên giá trị được hai người chọn; nếu ba giá trị khác nhau, đối chiếu ảnh và guideline.
- Với vùng `ignore`, giữ box riêng cho vật nhìn rõ; chỉ khoanh phần quá nhỏ hoặc quá dày theo R-06, không mặc định lấy vùng rộng hơn.
- Nếu không thể xác định đáng tin cậy sau khi xem ảnh, giữ trạng thái cần xem lại; không tự đoán.

Đây là nguyên tắc rà, không thay thế quyết định cho từng ca hoặc bằng chứng đã sửa và kiểm lại.

Các đề xuất hiện có được chấp nhận làm phương án xử lý theo những nguyên tắc trên. Với 24 dòng có kết quả ghép thuộc tính theo đa số khác 101, bảng quyết định đã chuyển sang đề xuất theo đa số; việc ghép đúng vật và nhãn sau sửa vẫn cần kiểm tra. C433/C451 chưa rõ mức che khuất; C435 có dấu hiệu cắt mép trái với đa số, cần kiểm lại.

- `img_002`, R-04: Người dùng đã chốt cách xử lý chung: một box `truck` cho xe vận chuyển, box `car` riêng cho từng ô tô thật nhận diện được và cao ít nhất 20 px; không bao ô tô được chở vào box xe tải. Các box cụ thể và thuộc tính vẫn cần xem, chốt và sửa.
- `img_038`, R-01: Người dùng chốt loại 24 box xe mô hình, giữ ảnh với 0 annotation. Quyết định đã ghi cho 48 dòng so sánh; chưa sửa nhãn và chưa kiểm lại sau sửa.
