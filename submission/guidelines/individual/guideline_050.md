# Guideline gắn nhãn người và phương tiện 2D

**Phiên bản:** v0-050  
**Ngày:** 16/11/2026  
**Người viết / duyệt:** 050

## 1. Mục tiêu

Nhãn được dùng để huấn luyện mô hình phát hiện người và phương tiện 2D trong cảnh đường phố. Ưu tiên phát hiện đúng các đối tượng thật đang hiện diện, kể cả xe đang đỗ hoặc người bị che một phần. Sai sót nguy hiểm nhất là bỏ sót người/xe thật hoặc nhận nhầm tượng, ảnh in, đồ chơi thành người/xe.

## 2. Lớp và thuộc tính

### 2.1. Bảng lớp

| Lớp | Định nghĩa | Ví dụ | Phản ví dụ |
|---|---|---|---|
| car | Xe cơ giới đường bộ chủ yếu chở người, thân xe kín và không có thùng chở hàng hở rõ rệt. | Sedan, hatchback, SUV, taxi. | Xe buýt; xe tải có thùng hoặc sàn chở hàng; xe máy. |
| truck | Xe cơ giới chở hàng có thùng, sàn hàng hoặc kết cấu chuyên chở hàng; gồm xe tải nhỏ, bán tải và xe chở xe. | Xe tải thùng, xe bán tải, xe chở ô tô. | Van thân kín không có thùng hở; sedan; xe buýt. |
| van | Xe cơ giới thân kín dạng hộp dùng chở người hoặc hàng nhẹ, không có thùng hàng hở tách biệt. | Minivan, xe van giao hàng thân kín. | Bán tải có thùng hở; xe tải thùng; xe buýt. |
| motorcycle | Phương tiện cơ giới hai bánh, gồm xe máy, xe tay ga và xe máy điện; không gộp người lái vào box xe. | Xe máy đang chạy hoặc đỗ. | Xe đạp; tuk-tuk ba bánh; xe đồ chơi. |
| person | Một người thật có thể nhận ra là người trong ảnh, dù đang đi bộ, đứng, ngồi hoặc lái/đi cùng phương tiện. | Người đi bộ, người lái xe máy, hành khách. | Tượng, ma-nơ-canh, hình người trên biển/ảnh in. |
| ignore_region | Vùng có mục tiêu thật nhưng không thể tạo box lớp thường đáng tin cậy, như đối tượng quá nhỏ hoặc cụm chồng lấn không thể tách. Đây là vùng bỏ qua khi huấn luyện, không phải một phương tiện hay người. | Một cụm xe máy xa và chồng lấn; mục tiêu có cạnh ngắn dưới 20 px. | Nền đường trống; đối tượng rõ có thể gắn lớp thường. |
| bus | Xe cơ giới lớn được thiết kế chủ yếu để chở nhiều hành khách. Đề xuất bổ sung lớp riêng vì xe buýt xuất hiện trong dữ liệu và khác rõ với truck/van. | Xe buýt nội đô, xe khách. | Xe van; xe tải chở hàng. |
| tuk_tuk | Xe cơ giới chở khách ba bánh dạng auto-rickshaw/tuk-tuk. Đề xuất bổ sung lớp riêng vì hình dáng và cách sử dụng khác motorcycle, van và bus. | Auto-rickshaw ba bánh trong img_035.jpg. | Xe máy hai bánh; xe ba bánh đồ chơi; xe điện chở hàng không có hình dáng tuk-tuk rõ. |

**Khuyến nghị schema:** bổ sung `bus` và `tuk_tuk` thành lớp chính thức trước khi gắn nhãn đồng loạt. Nếu bộ công cụ chưa hỗ trợ các lớp mới, đánh dấu `can_review` và ghi chú chờ duyệt, không tự ý gán tuk-tuk vào motorcycle hoặc van. Xe đạp không thuộc các lớp hiện tại nên không gắn box xe đạp; người đi xe đạp vẫn gắn `person` nếu đủ kích thước.

### 2.2. Thuộc tính

| Thuộc tính | Giá trị / ngưỡng | Cách áp dụng |
|---|---|---|
| occluded_level | 0: 0% bị che; 1: 1–30%; 2: 31–70%; 3: trên 70% nhưng vẫn nhận dạng chắc. | Ước lượng phần hình dáng bị vật khác che; phần nằm ngoài khung ảnh không tính là bị che mà ghi ở truncated. |
| truncated | no / yes. | Chọn yes khi box chạm mép ảnh hoặc đối tượng bị khung ảnh cắt. Box chỉ nằm trong biên ảnh và ôm phần nhìn thấy. |
| can_review | Không tick / tick. | Tick khi còn phân vân về lớp, số lượng instance, độ nhìn thấy hoặc box sau khi phóng to kiểm tra; ghi chú ngắn lý do để người duyệt xử lý. |

## 3. Quy tắc vẽ box

- Vẽ box chữ nhật sát phần nhìn thấy của từng đối tượng, không gồm bóng đổ, nền, phản chiếu hoặc vật thể khác. Không suy đoán phần khuất: vật bị che hoặc cắt mép chỉ ôm phần nhìn thấy. Không để tọa độ box vượt ra ngoài ảnh.
- **Người đi xe máy:** tách riêng từng người thành box `person` và xe thành một box `motorcycle`. Nếu có hai người trên một xe, tạo hai box `person` và một box `motorcycle`; không gộp người vào box xe. Box người ôm phần cơ thể nhìn thấy, box xe ôm phần xe nhìn thấy.
- **Xe chở xe, ví dụ img_002.jpg:** gắn xe chuyên chở là `truck`; gắn riêng từng ô tô thật đang được chở là `car` nếu mỗi xe nhìn thấy đủ rõ và cạnh ngắn đạt ít nhất 20 px. Không gắn box cho sàn/giá chở xe. Xe chở bị che thì box chỉ ôm phần nhìn thấy; xe nhỏ hơn ngưỡng hoặc không thể tách rõ được đưa vào `ignore_region`.
- **Vật bị che / cắt mép:** vẫn gắn lớp nếu nhận dạng chắc; box chỉ ôm phần nhìn thấy. Ghi `occluded_level` theo phần bị vật khác che và `truncated=yes` khi box chạm mép ảnh.
- **Tượng, ma-nơ-canh, đồ chơi, ảnh in và phản chiếu gương/kính:** không gắn `person` hay lớp xe. Chỉ gắn đối tượng thật trong cảnh; xe thật nhìn thấy qua kính vẫn được gắn nếu không phải hình phản chiếu hoặc hình in.
- **Mục tiêu nhỏ hơn 20 px:** nếu cạnh ngắn của box dưới 20 px, không gắn lớp thường; đánh dấu `ignore_region` bao quanh mục tiêu nhỏ hoặc cụm mục tiêu nhỏ khi công cụ hỗ trợ. Không tạo ignore_region cho nền trống.
- **Đám đông/cụm xe:** gắn box riêng cho từng người/xe nếu còn phân biệt được. Nếu các đối tượng chồng lấn dày đến mức không thể tách box ổn định, tạo một `ignore_region` vừa đủ bao vùng khó; không gộp nhiều người hoặc xe thành một box person/car.
- Xe thật đang đỗ vẫn được gắn nhãn. Phân biệt xe tải và van theo kết cấu: có sàn/thùng hàng hở hoặc thùng chở hàng rõ thì `truck`; thân kín dạng hộp thì `van`. Bán tải được gắn `truck`.

## 4. Ca khó đã xem

| Ảnh | Tình huống | Quyết định | Lý do |
|---|---|---|---|
| img_026.jpg | Hai người ngồi trên cùng xe máy, thân người chồng lấn với xe. | Hai box `person` riêng và một box `motorcycle`; box chỉ theo phần nhìn thấy; gán occlusion phù hợp. | Người và xe là các instance khác nhau; không gộp người vào xe. |
| img_027.jpg | Xe tải là tượng trưng bày ngoài trời. | Không gắn lớp `truck` hoặc `car`. | Đây là mô hình/tượng, không phải phương tiện thật trong cảnh giao thông. |
| img_030.jpg | Bãi xe máy dày, nhiều xe chồng lấn và một số xe nhỏ. | Gắn từng `motorcycle` phân biệt rõ; vùng các xe không thể tách hoặc có cạnh ngắn dưới 20 px dùng `ignore_region`. | Tránh bỏ sót xe rõ ràng nhưng không ép vẽ box thiếu căn cứ cho cụm quá nhỏ/chồng lấn. |
| img_035.jpg | Nhiều tuk-tuk/auto-rickshaw cùng xe máy và xe khác trong dòng giao thông. | Gắn tuk-tuk bằng lớp `tuk_tuk` sau khi schema được duyệt; các xe máy và người nhìn rõ gắn riêng theo lớp tương ứng. | Tuk-tuk là loại phương tiện thật, có hình dáng ba bánh riêng; không nên ép vào motorcycle hoặc van. |
| img_038.jpg | Xe ô tô đồ chơi trưng bày sau cửa kính. | Không gắn `car` cho các xe đồ chơi. | Đây là đồ vật trưng bày, không phải phương tiện thật; kích thước nhỏ cũng không đạt ngưỡng. |

## 5. Lịch sử phiên bản

| Phiên bản trước → phiên bản mới | Ngày | Người viết / duyệt | Nội dung thay đổi |
|---|---|---|---|
| v0 → v0-050 | 16/11/2026 | 050 | Bổ sung định nghĩa lớp, ngưỡng thuộc tính, quy tắc box cho người đi xe máy/xe chở xe/vật che khuất, loại trừ vật giả và phản chiếu, ngưỡng 20 px, ignore_region; đề xuất lớp bus và tuk_tuk. |

