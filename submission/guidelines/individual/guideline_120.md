# Guideline gán nhãn — v0 — Nguyễn Anh Tiến

- Phiên bản: v0
- Ngày: 2026-11-16
- Người viết: 120 — Nguyễn Anh Tiến
- Trạng thái: bản cá nhân v0, viết độc lập ở Pha 1; các lớp mới là đề xuất để nhóm thảo luận ở Pha 2

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình phát hiện người và phương tiện trong ảnh đường phố. Kết quả phát hiện hỗ trợ xe tự lái nhận biết các đối tượng xung quanh và chọn thao tác tiếp theo, chẳng hạn giảm tốc, dừng hoặc đổi hướng. Gán nhãn sai hoặc bỏ sót người, phương tiện có thể khiến mô hình đánh giá sai tình huống và dẫn tới thao tác không an toàn, làm tăng nguy cơ va chạm.

## 2. Lớp và thuộc tính

### Lớp

Mỗi đối tượng thật được gán một lớp phù hợp. Các lớp `bus`, `bicycle`, `tuk_tuk` và `cyclo` dưới đây là đề xuất cá nhân để nhóm xem xét bổ sung vào taxonomy; chưa phải quyết định chung. `ignore_region` là vùng ảnh, không phải một đối tượng.

| Lớp | Định nghĩa | Ví dụ | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô chủ yếu được thiết kế để chở người. | Ô tô con; xe diễu hành thực sự có thể vận hành như xe ở `img_019.jpg`. | Xe mô hình, thân vỏ rời hoặc tượng có hình dáng ô tô. |
| `truck` | Xe tải chở hàng có khoang hoặc thùng hàng rõ rệt, thường tách biệt với cabin. | Xe tải chở ô tô ở `img_002.jpg`. | Xe van cỡ nhỏ có khoang kín liền thân. |
| `van` | Xe chở hàng cỡ nhỏ có khoang kín liền với cabin. | Xe van giao hàng. | Xe tải có thùng hàng lớn, tách biệt với cabin. |
| `motorcycle` | Xe cơ giới hai bánh, gồm xe máy và mô tô. | Xe máy chở hàng ở `img_010.jpg`. | Xe đạp; xe tuk-tuk ba bánh. |
| `bus` *(đề xuất)* | Xe cơ giới lớn được thiết kế chủ yếu để chở nhiều hành khách. | Xe buýt ở `img_009.jpg`. | Xe van chở khách cỡ nhỏ; cần đưa ca biên ra reviewer nếu khó phân biệt. |
| `tuk_tuk` *(đề xuất)* | Xe cơ giới ba bánh dùng để chở khách hoặc hàng. | Tuk-tuk ở `img_004.jpg`. | Xe máy hai bánh; xích lô không động cơ. |
| `bicycle` *(đề xuất)* | Xe đạp không có động cơ, kể cả xe đạp chở hàng. | Xe đạp hoặc xe đạp chở hàng ở `img_010.jpg`. | Xe máy chở hàng; xích lô ba bánh. |
| `cyclo` *(đề xuất)* | Xe ba bánh không động cơ dùng để chở khách hoặc hàng. | Xích lô ở `img_023.jpg`. | Tuk-tuk có động cơ; xe đạp hai bánh. |
| `person` | Người thật nhìn thấy trong ảnh, gồm người đi bộ và người đang điều khiển hoặc ngồi trên phương tiện. | Người đi bộ, người lái xe, người bán hàng ở `img_003.jpg`. | Tượng, hình in, ma-nơ-canh hoặc hình phản chiếu. |
| `ignore_region` | Vùng đám đông quá dày hoặc cụm vật quá nhỏ để gán riêng từng đối tượng theo quy tắc. | Cụm người nhỏ, chồng lấp ở hậu cảnh. | Một người rõ ràng; một đối tượng bị che nhưng vẫn nhận dạng được. |

Không tạo lớp riêng như `cargo_bicycle` hoặc `cargo_motorcycle`: hàng hóa không làm thay đổi loại phương tiện. Gán phương tiện theo loại xe; hàng hóa không thuộc taxonomy hiện tại.

Người lái xe vẫn mang lớp `person`, không tạo lớp `driver` riêng vì người lái vẫn là người. Nếu mô hình cần phân biệt vai trò, đề xuất thuộc tính `person_role` với các giá trị `pedestrian`, `driver`, `passenger`, `rider`; chỉ gán khi vai trò nhìn thấy rõ và nhóm đồng ý bổ sung thuộc tính này. Không suy đoán người lái hoặc hành khách bị khuất hoàn toàn.

### Thuộc tính

| Thuộc tính | Giá trị | Quy tắc đề xuất |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | `0`: không bị che; `1`: bị che 1–30% diện tích; `2`: bị che 31–70%; `3`: bị che trên 70% nhưng vẫn nhận dạng chắc chắn. |
| `truncated` | `no`, `yes` | `yes` khi vật tiếp tục ra ngoài biên ảnh; không dùng chỉ vì vật bị một vật khác che. |
| `can_review` | bật / tắt | Bật khi chưa chắc lớp, ranh giới box hoặc quyết định có gán hay không. |
| `person_role` *(đề xuất)* | `pedestrian`, `driver`, `passenger`, `rider` | Chỉ thêm nếu nhóm cần mô hình phân biệt vai trò và CVAT/taxonomy được cập nhật tương ứng. |

## 3. Quy tắc vẽ box

Các mã dưới đây là mã tạm cho bản cá nhân; nhóm có thể đổi mã khi thống nhất guideline.

- **R-01 — Loại đối tượng:** Chỉ gán người thật và phương tiện thật thuộc phạm vi taxonomy. Không gán tượng, hình in, ma-nơ-canh, đồ chơi, phản chiếu hoặc thân vỏ xe rời không thể vận hành như phương tiện.
- **R-02 — Người và đồ vật đi kèm:** Vẽ box `person` quanh phần người nhìn thấy, không gộp hàng hóa hoặc vật đang mang vào box người. Không vẽ box riêng cho hàng hóa vì hàng hóa không thuộc lớp hiện tại. Nếu người đang đi xe, vẽ riêng box người và box phương tiện.
- **R-03 — Xe chở xe:** Gán box cho xe chở và từng xe được chở nếu từng chiếc nhìn thấy đủ để nhận dạng. Không gộp toàn bộ xe trên sàn chở thành một box. Với `img_002.jpg`, đề xuất một box `truck` và tám box `car` riêng.
- **R-04 — Bị che bởi vật khác:** Không loại xe hoặc người chỉ vì bị hàng rào che. Nếu vẫn nhận dạng được, vẽ box ôm phần nhìn thấy và đặt `occluded_level`; nếu chỉ còn mảnh nhỏ không đủ nhận dạng, bật `can_review` hoặc bỏ qua theo ngưỡng kích thước đã thống nhất.
- **R-05 — Đám đông:** Vẽ từng người còn phân biệt được rõ. Với vùng đám đông dày, chồng lấp hoặc các người quá nhỏ để vẽ tin cậy, dùng một `ignore_region` theo ranh giới vùng; không suy đoán box cho từng người trong vùng đó.
- **R-06 — Gương và tượng:** Không gán đối tượng chỉ xuất hiện dưới dạng phản chiếu trong gương (`img_020.jpg`). Không gán tượng người, tượng động vật hoặc tượng xe (`img_017.jpg`). Không dùng `ignore_region` thay cho quy tắc loại tượng/phản chiếu.
- **R-07 — Xe trưng bày:** Xe thật có thể vận hành vẫn gán theo loại xe dù đang đỗ hoặc trưng bày. Tác phẩm điêu khắc, mô hình hoặc thân vỏ rời không được gán là phương tiện. Nếu không xác định được là xe thật hay vật trưng bày, bật `can_review`.
- **R-08 — Người trên xe:** Gán `person` nếu người nhìn thấy đủ rõ để nhận dạng, kể cả người ở ghế lái. Không gán người bị khuất hoàn toàn bên trong xe; không suy ra sự hiện diện của họ chỉ từ chiếc xe.

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định cá nhân | Lý do / điểm cần hỏi nhóm |
|---|---|---|---|---|
| `img_002.jpg` | Xe tải chở nhiều ô tô | R-03 | Một box `truck` và một box `car` cho từng ô tô nhìn thấy, tổng cộng tám box `car`. | Các xe được chở vẫn là những phương tiện riêng; không gộp thành một box tải hàng. |
| `img_003.jpg` | Người gánh hàng rong | R-02 | Gán box `person` riêng quanh phần người nhìn thấy; không gán hàng hóa. | Hàng hóa không thuộc taxonomy; không gộp hàng vào box người. |
| `img_004.jpg` | Tuk-tuk ba bánh | R-01 | Đề xuất lớp `tuk_tuk`; nếu taxonomy chưa được nhóm bổ sung thì chuyển reviewer, không tự ép vào `motorcycle`. | Khác xe máy hai bánh về cấu tạo và loại phương tiện. |
| `img_009.jpg` | Xe buýt | R-01 | Đề xuất lớp `bus`. | Xe buýt là loại phương tiện riêng; lớp này cần được thêm đồng bộ vào taxonomy/CVAT nếu nhóm chấp thuận. |
| `img_010.jpg` | Xe đạp và xe máy chở hàng | R-02 | Đề xuất lớp `bicycle`; xe chở hàng vẫn giữ lớp theo loại xe, không tạo lớp “xe chở hàng”. | Tách loại xe đạp không động cơ khỏi xe máy có động cơ; hàng hóa không phải lớp. |
| `img_011.jpg` | Vật trưng bày có hình xe | R-07 | Loại các tác phẩm điêu khắc/mô hình; nếu là xe thật có thể vận hành thì gán theo loại xe. Trường hợp không rõ thì bật `can_review`. | Không thể quyết định chỉ dựa trên hình dáng giống xe. |
| `img_017.jpg` | Tượng người cưỡi ngựa | R-06 | Không gán `person` cho tượng. | Đây không phải người thật tham gia giao thông. |
| `img_019.jpg` | Xe vàng trong đoàn diễu hành và đám đông | R-01, R-05, R-08 | Xe vàng là `car` nếu là xe thật có thể vận hành; gán `person` cho người nhìn thấy rõ; người trong đám đông gán riêng nếu đủ rõ, vùng quá dày dùng `ignore_region`. | Ảnh này là cảnh diễu hành, không phải giao lộ đèn đỏ. Ở đèn đỏ, cũng chỉ gán người nhìn thấy và nhận dạng được; không suy đoán người bị khuất trong xe. |
| `img_020.jpg` | Phương tiện nhìn qua gương chiếu hậu | R-06 | Không gán xe/người chỉ xuất hiện trong ảnh phản chiếu. | Phản chiếu không phải đối tượng trực tiếp trong ảnh đường phố cần phát hiện theo quy tắc này. |
| `img_023.jpg` | Xích lô ba bánh | R-01 | Nhận diện là xích lô; đề xuất lớp `cyclo`. Nếu nhóm không thêm lớp này, chuyển reviewer, không gán thành `motorcycle`. | Xe ba bánh không động cơ khác xe máy và xe đạp hai bánh. |
| `img_024.jpg` | Thân vỏ xe đặt trên nóc xe khác | R-07 | Không gán thân vỏ rời trên nóc; gán chiếc xe bên dưới nếu nhận dạng được và thuộc phạm vi. | Thân vỏ rời không phải phương tiện có thể vận hành. |
| `img_0xx.jpg` | Người hoặc xe bị hàng rào che | R-04 | Nếu vẫn nhận dạng được thì gán phần nhìn thấy và đánh dấu bị che; nếu không đủ nhận dạng thì chuyển reviewer hoặc bỏ theo ngưỡng đã thống nhất. | Không loại tự động chỉ vì hàng rào che; đối tượng vẫn có thể liên quan đến tình huống giao thông. |

## 5. QC và phiên bản

- Đây là bản cá nhân v0; các lớp mới và quy tắc tạm cần được nhóm xem xét trước khi dùng chung.
- Khi chưa rõ lớp, box hoặc quyết định gán, bật `can_review` và ghi ảnh/vùng cụ thể để hỏi reviewer.
- Mọi thay đổi làm thay đổi lớp, box hoặc thuộc tính phải ghi lý do và tăng phiên bản guideline.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản đề xuất cá nhân ban đầu | Các ca `img_002`, `img_003`, `img_004`, `img_009`, `img_010`, `img_011`, `img_017`, `img_019`, `img_020`, `img_023`, `img_024` |
