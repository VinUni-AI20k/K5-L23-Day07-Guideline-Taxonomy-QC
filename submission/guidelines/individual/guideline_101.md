# Guideline gán nhãn — v0.1 đề xuất — 101

> Bản đề xuất cá nhân để thảo luận, chưa phải guideline v1.0 đã thống nhất. Người gán cần tự kiểm tra ảnh và chốt các ca chưa rõ với nhóm trước khi khóa quy tắc.

- Phiên bản: v0.1 đề xuất
- Ngày: 2026-11-16
- Người viết / duyệt: 101 / chờ nhóm duyệt

## 1. Mục tiêu
Nhãn bounding box dùng huấn luyện mô hình phát hiện người và phương tiện thực trong ảnh đường phố. Ưu tiên không bỏ sót đối tượng đủ điều kiện và phân biệt đúng lớp; box sai, thiếu người hoặc nhầm loại xe có thể khiến mô hình học sai. Mỗi vật đủ điều kiện có một box và đúng một lớp.

## 2. Lớp và thuộc tính
### Lớp
| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Xe cơ giới chở người cỡ nhỏ, thường có khoang hành khách và không có khoang chở hàng chuyên dụng tách biệt. | Sedan, hatchback, SUV, taxi, xe con được chở trên xe tải. | `van` thân hộp chủ yếu chở hàng/nhiều người; `truck` có khoang hàng riêng. |
| `truck` | Xe cơ giới thiết kế chủ yếu để chở hàng, có thùng hàng, sàn hàng hoặc cấu trúc chở hàng chuyên dụng. | Xe tải thùng, xe đầu kéo, xe chở ô tô. | `van` liền khối cỡ nhỏ; xe con đặt trên xe tải vẫn là `car` riêng. |
| `van` | Xe cơ giới thân kín dạng hộp, cabin liền khoang sau, dùng chở hàng hoặc chở người, nhỏ hơn xe buýt. | Xe giao hàng thân kín, xe van chở khách. | `truck` có thùng hàng riêng; `bus` thiết kế vận chuyển nhiều hành khách. |
| `motorcycle` | Xe cơ giới hai bánh gồm xe máy, xe tay ga và mô tô. | Xe tay ga có người lái, mô tô đang đỗ. | `bicycle` dùng bàn đạp; `three_wheeler` có ba bánh. |
| `person` | Người thật nhìn thấy trực tiếp trong ảnh, kể cả người đang đi bộ, đứng, ngồi hoặc lái/ngồi trên xe. | Người đi bộ, tài xế hoặc hành khách nhìn thấy. | Tượng, ma-nơ-canh, hình in và người trong phản chiếu. |
| `ignore_region` | Vùng ảnh chứa đối tượng mục tiêu không thể gán riêng đáng tin cậy hoặc đối tượng nhỏ dưới ngưỡng của bài. | Cụm người quá nhỏ hoặc chồng lấn không thể tách từng người. | Không dùng để che toàn bộ ảnh mờ hoặc bỏ qua một vật đủ rõ và đủ kích thước. |
| `three_wheeler` | Xe ba bánh có động cơ, dùng chở người hoặc hàng, bao gồm xe tuk-tuk. | Tuk-tuk, xe ba bánh chở hàng. | `motorcycle` hai bánh; xe đồ chơi hoặc xe đạp ba bánh không có động cơ. |
| `bus` | Xe cơ giới thiết kế chở nhiều hành khách, có khoang hành khách lớn với nhiều hàng ghế. | Xe buýt đô thị, xe khách đường dài. | `van` chở khách cỡ nhỏ; `truck` chở hàng. |
| `bicycle` | Phương tiện hai bánh chủ yếu vận hành bằng bàn đạp, kể cả xe có người đang đạp. | Xe đạp thông thường, xe đạp đang dựng. | `motorcycle` có động cơ; xe đạp trẻ em chỉ là đồ chơi trong ảnh. |

Vật không thuộc lớp nào thì không gán box; không tạo lớp mới trong lúc gán. Đối tượng thuộc phạm vi nhưng quá nhỏ hoặc không thể tách riêng thì xử lý `ignore_region` theo R-05, R-06. Nếu không đủ dấu hiệu để xác định có phải đối tượng mục tiêu, ghi vấn đề cấp ảnh để hỏi reviewer, không tự đoán.

**Chưa đồng bộ:** Project CVAT có `three_wheeler`, `bus`, `bicycle` nhưng `submission/taxonomy.json` hiện chưa có ba lớp này. Nhóm cần thống nhất phạm vi, cập nhật taxonomy và kiểm tra công cụ trước khi khóa v1.0; không tự coi các lớp này đã được phê duyệt.

### Thuộc tính
| Thuộc tính | Các mức cố định và quy tắc đề xuất |
|---|---|
| `occluded_level` | Ước lượng tỷ lệ diện tích đối tượng bị vật khác che so với hình dạng đầy đủ dự kiến: `0` = 0%; `1` = > 0% đến < 25%; `2` = 25% đến < 50%; `3` = từ 50% trở lên. Đây là ngưỡng đề xuất cần nhóm chốt. Che khuất khác cắt mép ảnh; không tính phần ngoài ảnh vào tỷ lệ này. Nếu khó ước lượng, chọn mức hợp lý nhất và tick `can_review`. |
| `truncated` | `yes` nếu một phần đối tượng thực sự nằm ngoài biên ảnh; `no` nếu toàn bộ đối tượng nằm trong ảnh, kể cả khi bị vật khác che. Một vật có thể vừa bị che vừa bị cắt mép. |
| `can_review` | Tick khi đã vẽ được box nhưng chưa chắc lớp, ranh giới, kích thước hoặc thuộc tính; không tick khi có đủ căn cứ. Nếu chưa vẽ được box, ghi ảnh, vùng và lý do vào danh sách vấn đề cấp ảnh, không tạo box tùy ý. |

`ignore_region` không có thuộc tính. Độ mờ không tự động đồng nghĩa với che khuất; không gán `occluded_level` theo độ mờ.

## 3. Quy tắc vẽ box
- **R-01 — Một vật, một box:** Chỉ gán vật thật nhìn thấy trực tiếp; mỗi vật đủ điều kiện có một box lớp tương ứng. Không gán tượng, ma-nơ-canh, hình in, hình trên màn hình, đồ chơi hoặc ảnh phản chiếu. Nếu không thể phân biệt vật thật với vật giả, ghi vấn đề để review.
- **R-02 — Box theo phần nhìn thấy:** Vẽ hình chữ nhật nhỏ nhất bao hết các phần nhìn thấy của cùng một vật, kể cả các phần tách nhau bởi vật che; không tưởng tượng hoặc mở rộng tới phần bị che hoàn toàn. Không kéo box của vật này sang bao cả vật khác.
- **R-03 — Che và cắt:** Phần bị vật khác che không vẽ riêng; nếu các phần nhìn thấy đủ căn cứ thuộc cùng một vật, gộp trong một box. Box không vượt biên ảnh. Cắt mép ảnh dùng `truncated=yes`; bị che bởi vật trong ảnh dùng `occluded_level`.
- **R-04 — Người và xe:** Người lái, hành khách và phương tiện là các đối tượng riêng; vẽ một box cho mỗi người nhìn thấy đủ điều kiện và một box cho xe. Box xe bao phần xe nhìn thấy, không cố ý bao người; box người bao phần người nhìn thấy, không bao xe. Các box có thể chồng nhau.
- **R-05 — Vật nhỏ:** Đo chiều cao box phần nhìn thấy trên ảnh gốc. Đối tượng cao < 20 px không gán box lớp vật thể riêng; đánh dấu vùng chứa đối tượng bằng `ignore_region`. Từ 20 px trở lên, nếu đủ căn cứ nhận diện thì gán bình thường. Nếu chưa chắc kích thước hoặc danh tính, ghi vấn đề để review.
- **R-06 — Đám đông và vùng khó:** Tách từng đối tượng khi nhận diện và vẽ riêng đáng tin cậy; vùng còn quá dày, quá mờ hoặc chồng lấn không thể tách thì bao sát vùng đó bằng `ignore_region`. Không dùng một vùng rộng để bỏ qua đối tượng đã nhìn rõ. Không tạo vùng ignore chỉ vì vật thuộc lớp ngoài phạm vi.
- **R-07 — Xe chở xe:** Xe vận chuyển và từng xe thật được chở là các đối tượng riêng nếu đủ điều kiện; phần nhìn thấy của từng xe được box theo lớp của chính nó. Không gộp tất cả vào một box.
- **R-08 — Xe chủ và hình không rõ:** Không gán bộ phận xe gắn camera (ego) nếu chỉ là phần nền/khung hình; nếu không xác định chắc đó là xe chủ hay xe khác, ghi vấn đề để review. Không suy đoán lớp dựa duy nhất vào vị trí, màu sắc hoặc hình dạng mờ; nếu nhận ra vật nhưng chưa chắc lớp và đã vẽ được box, chọn phương án có căn cứ nhất, tick `can_review`.
- **R-09 — Phân loại xe dễ nhầm:** Ưu tiên cấu tạo và công năng nhìn thấy: cabin liền khoang hộp nhỏ → `van`; khoang chở hàng riêng → `truck`; nhiều hàng ghế/khoang khách lớn → `bus`; xe chở người cỡ nhỏ thông thường → `car`. Nếu phần quyết định bị che hoặc cắt, không suy đoán chắc chắn: tick `can_review`.

## 4. Ca khó
| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| Chưa xác định — kiểm lại trên bộ ảnh | Người ngồi trên xe máy, tay/chân chồng lên xe | R-02, R-04 | Đề xuất tách box người và xe; tick review nếu không tách được phần nhìn thấy. | Người và xe là hai đối tượng khác nhau. |
| Chưa xác định — kiểm lại trên bộ ảnh | Xe chở nhiều ô tô | R-02, R-07 | Đề xuất box xe chở và từng ô tô đủ điều kiện nhìn thấy. | Mỗi xe thật là một đối tượng riêng. |
| Chưa xác định — kiểm lại trên bộ ảnh | Người hoặc xe bị cắt tại mép ảnh | R-03 | Box phần trong ảnh, `truncated=yes`; ghi mức che riêng nếu có. | Cắt ảnh và che khuất là hai thuộc tính khác nhau. |
| Chưa xác định — kiểm lại trên bộ ảnh | Người ở xa cao dưới 20 px | R-05 | Đề xuất `ignore_region` bao sát vùng người nhỏ. | Dưới ngưỡng chiều cao của lab. |
| Chưa xác định — kiểm lại trên bộ ảnh | Vùng đông người mờ và chồng lấn | R-06 | Box từng người đủ rõ; phần không thể tách dùng vùng ignore sát vùng đó. | Tránh bỏ qua những người vẫn có thể gán riêng. |
| Chưa xác định — kiểm lại trên bộ ảnh | Tượng hoặc người trong ảnh phản chiếu | R-01 | Không gán `person` cho hình không phải người thật trực tiếp. | Giảm nhãn thừa. |
| Chưa xác định — kiểm lại trên bộ ảnh | Xe mờ, không rõ là `van` hay `truck` | R-08, R-09 | Nếu vẽ được box, chọn lớp có căn cứ nhất và tick `can_review`; nếu chưa xác định được vùng, ghi vấn đề cấp ảnh. | Không đủ bằng chứng để khẳng định lớp. |

Các dòng trên là tình huống đề xuất, chưa phải kết quả kiểm chứng từng ảnh. Khi tự xem ảnh, thay bằng mã `img_0xx` thực tế và ghi nhận quyết định của người gán. Nếu chưa chốt, đánh dấu `can_review` trên box hoặc ghi vấn đề cấp ảnh. Dùng mã quy tắc trong nhật ký QC.

## 5. QC và phiên bản
- Giữ nguyên các ngưỡng trong `submission/taxonomy.json`: ghép box IoU ≥ 0.5; IAA IoU trung bình ≥ 0.85 và đồng thuận lớp ≥ 95% trên các cặp đã ghép; IoU QC ≥ 0.85 với box cao ≥ 50 px, ≥ 0.7 với box thấp hơn.
- Review toàn bộ lô để xét Release; tỷ lệ ảnh lỗi phải ≤ 2%, không có lỗi lặp và có đủ bằng chứng. Thiếu bằng chứng thì Hold; vượt ngưỡng hoặc có lỗi lặp thì Rework. Ghi tử số/mẫu số, cả tỷ lệ theo ảnh và theo đối tượng.
- Người gán đánh dấu ca chưa chắc; nhóm và người review được phân công quyết định sau khi các lượt gán độc lập đã khóa. Mọi thay đổi ảnh hưởng cách gán cần được ghi lại, thống nhất và rà lại phạm vi ảnh liên quan.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0.1 đề xuất | Bổ sung định nghĩa lớp, thuộc tính và quy tắc gán/QC cá nhân. | Làm rõ các ca che khuất, cắt mép, ảnh mờ, xe chở xe và các lớp bổ sung trong Project; chờ kiểm chứng ảnh và nhóm duyệt. |
