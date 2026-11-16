# Guideline gán nhãn — <phiên bản> — <mã hoặc nhóm>

> Copy file này (hoặc `guideline_v0_starter.md`) rồi viết. Một guideline đủ gồm **5 phần**. Câu nào của v0
> làm hai người đọc ra hai cách khác nhau thì phải viết lại cho một cách hiểu duy nhất.

- Phiên bản: v0
- Ngày: 16/11/2026
- Người viết / duyệt: Luong Hoang Bao Tran

## 1. Mục tiêu
Bộ dữ liệu này được sử dụng để huấn luyện mô hình Object Detection (nhận diện vật thể bằng bounding box) nhằm phục vụ hệ thống phân tích và giám sát giao thông đô thị.

+ Yêu cầu cốt lõi: Box phải ôm sát toàn bộ các bộ phận nhìn thấy được của phương tiện và người tham gia giao thông.

+ Rủi ro khi sai sót: Việc bỏ sót nhãn (False Negative) đối với người đi bộ hoặc xe máy, hoặc gán nhầm lớp (nhầm xe van thành xe tải) sẽ khiến hệ thống đếm sai lưu lượng, hoặc gây nguy hiểm nếu ứng dụng vào hệ thống cảnh báo va chạm (ADAS).

## 2. Lớp và thuộc tính
### Lớp
| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| truck | Ô tô tải chuyên dụng chở hàng, có cabin điều khiển tách biệt rõ ràng với thùng chở hàng phía sau. | Hai xe tải màu trắng (xe Isuzu và xe bán tải độ thùng) trong ảnh img_002.jpg | Dễ nhầm với van (khoang lái và khoang hàng liền khối). |
|car| Ô tô con thiết kế chủ yếu để chở người (thường dưới 9 chỗ), bao gồm cả sedan, hatchback, SUV, và taxi.| Xe taxi màu trắng ở góc trái ảnh img_006.jpg|Dễ nhầm với van loại nhỏ chở khách.|
|motobike| Xe 2 bánh có động cơ, dùng động cơ để di chuyển. | Chiếc xe máy màu đỏ có hai người đội mũ bảo hiểm trong ảnh img_026.jpg | Dễ nhầm với bicycle khi xe bị khuất hoặc nhìn từ xa; người ngồi trên xe là motorcyclist, không phải một phần của box xe. |
|bicycle | Xe 2 bánh không có động cơ, di chuyển bằng sức người đạp.| Chiếc xe đạp ở rìa bên phải ảnh img_006| Dễ nhầm với motorbike nhìn từ xa bị khuất chân đạp.|
|tuk-tuk | Phương tiện 3 bánh có động cơ, chuyên chở người. | Hai xe tuk-tuk màu xanh ở bên trái và bên phải ảnh img_016.jpg | Dễ nhầm với xe máy kéo theo rơ-moóc tự chế.|
|motorcyclist | Người đang ngồi và điều khiển trực tiếp trên phương tiện xe máy (motorbike). | Người lái mặc áo đen ngồi phía trước trên xe máy chở hai người trong ảnh img_026.jpg | Dễ nhầm với người đi bộ đứng cạnh xe; chỉ gán lớp này cho người đang điều khiển xe máy. |
|pedestrian| Người đang đi bộ trên phần đường giao thông (lòng đường hoặc vạch qua đường). | Hai người đang đi bộ qua đường trong ảnh img_014.jpg | Dễ nhầm với người đứng trên vỉa hè hoặc người đang ngồi/điều khiển phương tiện; người đi bộ trên vỉa hè cần chốt có thuộc lớp này không. |
|person| Người không ở trạng thái đi bộ trên đường, ví dụ người ngồi sau xe hoặc người đứng/ngồi cạnh đường. | Người ngồi sau người lái trên xe máy trong ảnh img_026.jpg | Dễ nhầm với pedestrian và motorcyclist; cần gán riêng box cho từng người và thống nhất ưu tiên lớp với motorcyclist. |
|cyclo| Phương tiện ba bánh không có động cơ, được đạp bằng sức người, có chỗ ngồi hoặc khoang chở khách. | Xe ba bánh đạp bằng sức người ở giữa ảnh img_023.jpg | Dễ nhầm với tuk-tuk (có động cơ) hoặc xe đạp kéo rơ-moóc; ảnh này minh họa xe ba bánh đạp, không thấy rõ người ngồi sau. |
|van | Ô tô có thiết kế liền khối (thân hộp vuông), khoang lái và khoang sau thông nhau, dùng chở hàng hoặc chở người (thường 10-16 chỗ). | Chiếc xe màu bạc (biển số 51LD-70.65) chạy phía sau trong ảnh img_005.jpg|Dễ nhầm với bus (lớn hơn) hoặc car SUV.|
|bus | Ô tô cỡ lớn chuyên chở khách tuyến cố định hoặc du lịch (thường trên 16 chỗ). | Xe buýt màu xanh ở phía trái ảnh img_037.jpg | Dễ nhầm với van 16 chỗ (như Ford Transit).||
|ignore_region| Vùng hình ảnh không gán từng vật riêng lẻ vì quá dày đặc hoặc không thể xác định đáng tin cậy; đây là vùng bỏ qua, không phải vật thể. | Đám đông xe máy ở xa trong ảnh img_021.jpg (chỉ dùng nếu quy tắc gán từng xe không khả thi) | Không dùng để che các vật nhìn thấy rõ và gán được; cần thống nhất ngưỡng kích thước/độ dày đặc trước khi áp dụng. |

Vật không thuộc lớp nào thì không gán nhãn vật thể; chỉ dùng `ignore_region` cho vùng đủ điều kiện bỏ qua theo quy tắc đã thống nhất, không tự tạo lớp mới trong lượt gán.

### Thuộc tính
| Thuộc tính | Các mức | Ý nghĩa và cách chọn |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Ước lượng tỷ lệ diện tích vật thể bị vật khác che khuất trên tổng diện tích toàn vật thể (bao gồm phần bị che): `0` = không bị che; `1` = bị che dưới 25%; `2` = bị che từ 25% đến dưới 50%; `3` = bị che từ 50% trở lên nhưng vẫn nhận diện được. Không tính phần bị cắt bởi mép ảnh là che khuất. |
| `truncated` | `no`, `yes` | Chọn `yes` khi vật thể bị mép ảnh cắt mất bất kỳ phần nào; chọn `no` khi vật thể nằm trọn trong khung ảnh. |
| `can_review` | `false`, `true` | Chọn `true` khi còn chưa chắc về lớp, ranh giới box hoặc quyết định có gán nhãn hay không và cần người khác xem lại; chọn `false` khi đã có thể quyết định theo guideline. |

Khi không thể ước lượng chính xác tỷ lệ bị che, chọn mức gần nhất theo phần nhìn thấy và phần bị che; nếu không chắc vật thể còn nhận diện được hay không, đánh dấu `can_review=true`.

## 3. Quy tắc vẽ **box**
1. Box phải ôm sát mép vật thể.
2. Với vật bị che khuất, box ôm sát mép phần nhìn thấy được; không ước lượng phần bị che.
3. Với vật bị cắt ở mép ảnh, box ôm sát phần vật thể còn nhìn thấy trong ảnh.
4. Không gán nhãn cho hình in, tượng hoặc đồ chơi.
5. Vật quá nhỏ để vẽ box đáng tin cậy có thể được đưa vào `ignore_region`.
6. Nếu một tình huống có nhiều đối tượng riêng (ví dụ người và xe), vẽ box riêng cho từng đối tượng khi nhìn rõ được từng phần. Phần được gán nhãn không cần nhìn thấy hoàn chỉnh; chỉ box phần nhìn thấy.
7. Các box được phép chồng lấn một phần khi các đối tượng tương ứng chồng lên nhau trong ảnh; mỗi box vẫn ôm sát đối tượng riêng.

## 4. Ca khó
| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_010.jpg, img_026.jpg | Người ngồi sau người điều khiển xe máy | R-04 (đề xuất) | Vẽ box xe riêng; vẽ box riêng cho từng người. Người điều khiển gán `motorcyclist`, người ngồi sau gán `person`. | Hai người cùng ngồi trên một xe nhưng là hai đối tượng riêng; ảnh img_026 có hai người trên xe máy, img_010 cũng có người ngồi sau người lái. |
| img_023.jpg | Xe ba bánh đạp bằng sức người; phân biệt với xe máy kéo rơ-moóc và trường hợp có người ngồi sau xe đạp/xe ba bánh | R-05 (đề xuất) | Gợi ý lớp riêng `cyclo` nếu taxonomy cho phép; không gộp với `bicycle` hai bánh. Nếu có người ngồi sau thì vẽ box người riêng và gán `person`. Ảnh img_023 minh họa xe ba bánh nhưng không thấy rõ người ngồi sau; chưa có ảnh xe đạp chở người phía sau rõ ràng trong lô. | Hình dạng ba bánh và cơ cấu đạp khác xe đạp thường; cần chốt tên lớp và cách phân biệt cyclo với xe đạp kéo rơ-moóc. |
| img_021.jpg | Đám đông xe máy ở xa, khó tách từng phương tiện | R-06 (đề xuất) | Chỉ tạo `ignore_region` khi không thể gán từng xe theo ngưỡng nhóm thống nhất; các xe rõ vẫn gán riêng. | Tránh bỏ qua các đối tượng nhìn thấy rõ chỉ vì vùng ảnh đông. |

Nếu chưa chốt, đánh dấu `can_review` trên box hoặc ghi vấn đề cấp ảnh. Dùng mã quy tắc trong nhật ký QC.

## 5. QC và phiên bản
Ngưỡng QC áp dụng, ai quyết ca mơ hồ, lịch sử thay đổi:

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Guideline đầu tiên. | Chưa có ca cụ thể; tạo bản hướng dẫn ban đầu. |
