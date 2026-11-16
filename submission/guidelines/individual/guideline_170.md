# Guideline gán nhãn — <v0> — <170 - LAB7BROS>

- Phiên bản: v0
- Ngày: 16/11/2026
- Người viết / duyệt: Huy Anh
- Công cụ: CVAT, xuất COCO 1.0

## 1. Mục tiêu
Nhẫn dùng để huấn luyện mô hình phát hiện **người và phương tiện** trên ảnh đường phố.

Guideline cần hạn chế bỏ sót vật, chọn sai lớp, vẽ box không nhất quán và gán nhãn nhầm cho tượng, quảng cáo, hình phản chiếu hoặc đồ chơi. Áp dụng cho cả 40 ảnh ở độ phân giải gốc.

## 2. Lớp và thuộc tính
### Lớp
Mỗi vật thể chỉ có một lớp. VD: một người đang lái xe và chiếc xe là  hai vật thể tách biệt. 

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| car | Ô tô chở người có thân xe liền khối, gồm sedan, hatchback, station wagon và SUV. | Xe ô tô đang đỗ, đang chạy. | Xe bán tải, xe van và tượng xe. |
| truck | Xe chở hàng có thùng hàng hoặc kết cấu vận chuyển hàng riêng phía sau cabin. | Xe bán tải, xe chở ô tô và xe bán tải lắp nắp che thùng có thể tháo rời. | |
| van | Xe kín cỡ nhỏ có khoang chở người hoặc hàng tạo thành thân xe liên tục phía. | | Không gồm xe bán tải được lắp thêm thùng. |
| motorcycle | Phương tiện hai bánh có động cơ, gồm xe máy, mô tô và mô tô gắn thùng bên. | | Theo định nghĩa đề xuất này, không gồm xe đạp, xích lô đạp và tuk-tuk. |
| person | Người thật, gồm người đi bộ, người lái xe và hành khách có thể nhận diện từ phàn nhìn thấy. | | Khong gồm ma nơ canh, tượng, người trong hình in và hình phản chiếu |
| ignore_region | Vùng được khoanh sát, nơi không gán từng vật theo một quy tắc đã ghi rõ. | Dùng cho vật thuộc lớp mục tiêu nhưng nhỏ hơn ngưỡng hoặc vùng đám đông không thể tách từng người. | |


Vật **không thuộc lớp nào**: không ép vật vào một lớp sai. Ghi lại các trường hợp quan trọng nằm ngoài phạm vi để nhóm thảo luận. Đặc biệt, nhóm cần quyết định có bổ sung lớp cho tuk-tuk, xe đạp, xích lô và xe buýt trước khi khóa v1.0 hay không.

### Thuộc tính

| Thuộc tính | Giá trị | Ý nghĩa đề xuất |
|---|---|---|
| occluded_level | 0 | Không có dấu hiệu vật bị vật khác che khuất. |
| | 1 | Trên 0% đến 30% diện tích hình dáng dự kiến của vật trong khung ảnh bị che. |
| | 2 | Trên 30% bị che, nhưng vẫn hiện được vật. |
| | 3 | Không thể ước lượng mức che khuất một cách đáng tin cậy. |
| truncated | yes | Một phần vật nằm ngoài biên ảnh. |
| | no | Vật không bị cắt bởi biên ảnh. |
| can_review | tick | Cần reviewer giải quyết sự không chắc chắn về lớp, box, thuộc tính hoặc việc vật có phải là vật thật hay không. |
| | không tick | Nhãn được gán chắc chắn theo quy tắc rõ ràng. |


Ước lượng mức che khuất nhưng không vẽ box bao phần toàn bộ vật do tưởng tượng. Ảnh tối hoặc mờ không tự động có nghĩa là vật bị che khuất. Một vật có thể vừa bị che khuất vừa bị cắt ở biên ảnh.

Đối với ignore_region, dùng occluded_level=0 và truncated=no làm giá trị quy ước; ghi riêng lý do tạo vùng.

## 3. Quy tắc vẽ box
- R-01 — Phần nhìn thấy: Vẽ hình chữ nhật nhỏ nhất, có cạnh song song với cạnh ảnh, bao toàn bộ phần nhìn thấy của một vật. Không mở rộng box để bao phần bị che do tưởng tượng.
- R-02 — Một vật, một box: Mỗi vật có thể nhận diện được dùng một box. Các phần nhìn thấy rời nhau nhưng thuộc cùng một vật vẫn nằm trong cùng một box.
- R-03 — Người và phương tiện: Gán từng người lái hoặc hành khách là person, riêng với box motorcycle. Một xe máy chở hai người nhìn thấy được thường có ba box, nếu từng vật đáp ứng quy tắc kích thước.
- R-04 — Ranh giới vật: Box người bao quần áo và mũ bảo hiểm đang đội. Box phương tiện bao các bộ phận kết cấu, gương và thùng bên gắn với xe. Không mở rộng box để bao người hoặc hàng hóa được chở riêng. Các box có thể chồng nhau.
- R-05 — Biên ảnh: Giới hạn box trong ảnh. Đặt truncated=yes khi vật còn tiếp tục ở ngoài biên.
- R-06 — Kích thước tối thiểu: Đo chiều cao box của phần nhìn thấy bằng pixel ở độ phân giải gốc. Gán từng vật có chiều cao ≥20 px. Với vật nhỏ hơn 20 px, tạo ignore_region bao sát.
- R-07 — Vật thật: Không gán nhãn cho hình phản chiếu, hình in, tượng, ma-nơ-canh, đồ chơi và mô hình sao chép. Người thật mặc trang phục hóa trang vẫn là person; trường hợp chưa rõ cần review.
- R-08 — Xe đứng yên và xe được vận chuyển: Gán nhãn cho phương tiện thật thuộc phạm vi, dù đang chạy, đỗ hay được chở trên xe khác. Xe chở ô tô được gán truck; từng phương tiện nhận diện được trên xe được gán riêng.
- R-09 — Đám đông: Gán từng người nếu phân biệt được. Chỉ dùng ignore_region cho phần không thể tách từng người và ghi rõ lý do.

Không dùng ignore_region để bỏ qua một trường hợp khó thông thường hoặc che phủ những vật đủ điều kiện và phân biệt rõ được.

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---||---|---|
| img_026 | Hai người trên một xe máy. | R-03 | Hai box `person` và một box `motorcycle`. Bao riêng phần nhìn thấy của từng vật. ||
| img_005 | Người và xe máy chồng lên nhau. | R-01, R-02 | Gán từng vật nhận diện được; không gộp những người đứng gần nhau và không suy diễn vật bị che hoàn toàn. | |
| img_002 | Xe tải chở nhiều phương tiện | R-08 | Một box truck cho xe chở, cùng các box riêng cho phương tiện được vận chuyển. Các xe được chở vẫn là vật thật thuộc mục tiêu. | |.

## 5. QC và phiên bản

| Tiêu chí | Yêu cầu |
|---|---|
| Độ phủ lượt gắn | Đủ 100% lượt được phân công. |
| IoU trung bình của IAA | ≥0.85 |
| Đồng thuận lớp trên các cặp box ghép được | ≥95% |
| Ngưỡng so sánh box | Cao ≥50 px: IoU ≥0.85; nhỏ hơn: ≥0.70 |
| Tỷ lệ ảnh có lỗi tối đa | ≤2% |
| Phạm vi review cuối | Toàn bộ lô ảnh |

Với 40 ảnh đã review, một ảnh có lỗi tương đương 2,5%, vượt ngưỡng Release.

Trước khi nộp nhãn, kiểm tra vật bị bỏ sót, box thừa, lớp sai, ranh giới box không chính xác và thuộc tính sai. Ghi các ca chưa chắc bằng mã ảnh và mã quy tắc.

Giữ nguyên bản cá nhân đầu tiên sau khi họp nhóm. Lưu guideline thống nhất và guideline sau calibration thành các phiên bản riêng. Thay đổi làm khác cách chọn vật, phân lớp, vẽ box hoặc gán thuộc tính phải được ghi là thay đổi ngữ nghĩa (semantic) và kiểm lại phạm vi bị ảnh hưởng.


| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| | | |
