# Guideline gán nhãn — bản cá nhân 103

- Phiên bản đề xuất: `v0.1-103`
- Phạm vi: 40 ảnh đường phố, box chữ nhật 2D, CVAT, xuất COCO 1.0.
- Bản tham khảo có AI hỗ trợ soạn. Thành viên 103 cần mở ảnh gốc, tự kiểm các ca và chốt quyết định cá nhân trước khi nộp riêng.

## 1. Mục tiêu

Huấn luyện mô hình phát hiện người và phương tiện thật trong ảnh đường phố. Kết quả cần tìm được từng cá thể nhìn thấy, kể cả người ngồi trên xe và xe đỗ. Hai lỗi cần tránh là bỏ sót cá thể bị che một phần và tạo box cho vật giả có hình dáng giống người hoặc xe.

## 2. Lớp và thuộc tính

### Lớp

Mỗi đối tượng thật có tối đa một lớp. Đề xuất đưa `bus` và `tuk_tuk` vào taxonomy ở buổi họp Pha 2. Chỉ dùng bộ lớp đã khóa khi gán độc lập.

| Lớp | Định nghĩa | Ví dụ | Phản ví dụ |
|---|---|---|---|
| `car` | Ô tô chở người kiểu sedan, hatchback, wagon hoặc SUV. | Ô tô đen bên trái `img_023.jpg`. | Bán tải có thùng hàng sau thuộc `truck`. |
| `truck` | Xe chở hàng có cabin và thùng/sàn hàng riêng, gồm xe bán tải và xe chuyên chở ô tô. | Xe chở ô tô `img_002.jpg`, xe xanh `img_036.jpg`. | Xe tải thùng liền thân kiểu van thuộc `van`. |
| `van` | Xe thân cao, có khoang kín liền thân với cabin và không có sàn hàng rời. | Xe bạc phía sau các tay lái `img_005.jpg`. | Bán tải gắn nắp cao lên thùng `img_037.jpg` vẫn thuộc `truck`. |
| `bus` | Xe buýt hoặc minibus có thân và dãy cửa sổ phục vụ khoang nhiều hành khách. | Xe buýt màu xanh bên trái `img_037.jpg`. | Van có cửa sổ nhưng thiếu dấu hiệu khoang xe buýt vẫn thuộc `van` nếu nhận ra kiểu thân. |
| `tuk_tuk` | Xe ba bánh có động cơ với khoang khách hoặc khoang hàng tích hợp kiểu tuk-tuk. | Hai xe xanh `img_004.jpg`. | Xe máy gắn sidecar `img_022.jpg` thuộc `motorcycle`. Xích lô đạp `img_023.jpg` ngoài phạm vi. |
| `motorcycle` | Xe máy hoặc mô tô nhận diện được, gồm xe có sidecar gắn cố định. | Xe đỏ ở tiền cảnh `img_026.jpg`. | Xe đạp `img_029.jpg` ngoài phạm vi. |
| `person` | Người thật xuất hiện trực tiếp trong ảnh, gồm người đi bộ và người trên xe có phần cơ thể nhận dạng được. | Người sang đường `img_034.jpg`, người ngồi trên xe `img_026.jpg`. | Tượng `img_017.jpg`, ma-nơ-canh `img_033.jpg`, chân dung in `img_018.jpg`. |
| `ignore_region` | Vùng cục bộ để đánh dấu cá thể trong phạm vi quá nhỏ hoặc cụm quá dày khó tách từng cá thể. | Phần xa của dòng xe `img_021.jpg` nếu kiểm trên ảnh gốc thấy thỏa quy tắc R-06. | Chân dung in hoặc xe đạp rõ ràng ngoài phạm vi: bỏ qua theo R-01. |

### Thuộc tính

| Thuộc tính | Giá trị và cách chọn |
|---|---|
| `occluded_level` | Gọi `p` là tỉ lệ diện tích hình chiếu của chính vật bị vật khác che, tính trên phần ước lượng nằm **trong** ảnh. `0` nếu `p = 0%`, `1` nếu `0% < p ≤ 30%`, `2` nếu `30% < p ≤ 70%`, `3` nếu `p > 70%` và vẫn nhận ra lớp. Ước lượng theo các phần cơ thể/thân xe thấy được. Khi phân vân sát ranh giới, chọn mức có căn cứ hơn và tick `can_review`. |
| `truncated` | `yes` khi mép ảnh cắt mất phần của vật, `no` khi vật chỉ chạm mép hoặc bị vật khác che. Có thể vừa `truncated=yes` vừa có `occluded_level>0`. |
| `can_review` | Tick khi vẫn vẽ được box có căn cứ nhưng còn nghi ngờ lớp, ranh giới hoặc mức che. Khi không xác định được lớp hoặc viền đủ để vẽ box, ghi vấn đề cấp ảnh với ID ảnh, mã `103`, vùng và lý do. |

Nếu cấu hình CVAT gắn thuộc tính cho `ignore_region`, đặt `occluded_level=0`, `truncated=no`, chỉ tick `can_review` khi vùng cần xem lại. Dùng trường `occluded_level` của project trên CVAT.

## 3. Quy tắc vẽ box

| Mã | Quy tắc |
|---|---|
| R-01 | Gán vật thật nhìn trực tiếp thuộc các lớp đã chốt. Bỏ tượng, mô hình, hình in, phản chiếu, bóng đổ và vật rõ ràng ngoài phạm vi. Vật thật thấy xuyên qua kính vẫn đủ điều kiện. Bỏ phần xe chủ chụp ảnh như gương hoặc mép cửa nếu nhận ra đó là xe chủ. |
| R-02 | Vẽ hình chữ nhật nhỏ nhất ôm các phần nhìn thấy của cùng một cá thể, giới hạn trong ảnh. Nếu phần nhìn thấy tách rời do bị che, dùng một box bao các phần xác định thuộc cùng cá thể. Khoảng trống giữa chúng có thể nằm trong box. Dừng tại mép ảnh và ghi `truncated=yes` nếu có phần bị cắt. |
| R-03 | Với xe và người ngồi trên xe, vẽ một box xe và một box riêng cho từng người đủ điều kiện, cho phép box chồng nhau. Box người bao phần cơ thể, quần áo và mũ bảo hộ nhìn thấy. Box xe bao phần cấu tạo nhìn thấy của xe. Với sidecar gắn cố định, bao cả xe và sidecar trong một box `motorcycle`. |
| R-04 | Với xe chở xe, vẽ một box `truck` ôm đầu kéo và sàn chở gắn với xe. Vẽ box riêng cho từng ô tô hoàn chỉnh trên sàn nếu nhận ra lớp và đủ ngưỡng chiều cao. Thân vỏ trưng bày hay mô hình trên nóc chỉ được xem như vật chở. |
| R-05 | Box xe bao bộ phận cố định như bánh, gương, nắp thùng cố định và mái. Loại hàng xếp, bao tải hoặc đồ chở nhô ra. Với bán tải, tìm ranh cabin–thùng hoặc dấu hiệu nắp lắp trên thùng trước khi phân biệt `truck` với `van`. |
| R-06 | Đo chiều cao box phần nhìn thấy theo pixel ảnh gốc. Từ **20 px** trở lên, gán riêng nếu nhận diện và tách được cá thể. Dưới **20 px**, đánh dấu `ignore_region` sát vật hoặc cụm vật nhỏ. Với cụm dày đặc, chỉ khoanh phần khó tách sau khi gán riêng các cá thể rõ. Tránh phủ các box đủ điều kiện bằng vùng ignore tùy tiện. |
| R-07 | Khi ảnh mờ hoặc bị che, dựa vào hình dáng còn nhận được để áp dụng R-02 và ghi thuộc tính. Vệt nhòe ngoài phần có thể nhận dạng không làm box dài thêm. Nếu chưa đủ căn cứ để vẽ, ghi vấn đề cấp ảnh. Giữ ảnh trong file COCO kể cả khi có 0 annotation. |

## 4. Ca khó để thành viên 103 tự kiểm trên ảnh gốc

| Ảnh | Tình huống | Mã | Quyết định đề xuất và lý do |
|---|---|---|---|
| `img_002.jpg` | Xe chở ô tô trên hai tầng | R-04 | Ôm cabin và giàn chở làm một `truck`. Xét từng ô tô trên sàn để gán `car` riêng vì mỗi xe là một cá thể nhận diện được. |
| `img_026.jpg` và `img_006.jpg` | Xe máy và người đi xe | R-02, R-03 | Với cặp đi xe ở tiền cảnh ảnh 026, kiểm hai `person` và một `motorcycle`, tức ba box nếu từng phần nhìn thấy đạt ngưỡng. Thử cùng quy tắc trên một xe có người ngồi ở ảnh 006. |
| `img_035.jpg` | Tuk-tuk chở bao tải cao | R-05 | Gán `tuk_tuk` cho thân xe và mái cố định, loại khối bao tải phía trên. Cách chất hàng không đổi ranh giới cấu tạo của xe. |
| `img_037.jpg` | Bán tải trắng gắn nắp cao | R-05 | Đề xuất `truck` vì cabin và thùng sau có ranh giới riêng. Bao nắp cố định trong box, đưa cách phân biệt với `van` ra buổi chốt Pha 2. |
| `img_017.jpg`, `img_018.jpg`, `img_038.jpg` | Tượng, chân dung trên biển, đồ chơi | R-01 | Loại tượng, người in và xe mô hình. Vẫn xét người hoặc xe thật ở phần khác trong cùng ảnh, nếu có. |
| `img_020.jpg` | Gương chiếu hậu | R-01, R-07 | Loại phần phản chiếu và gương xe chủ. Nếu ảnh gốc không có vật thật khác trong phạm vi thì giữ ảnh với 0 annotation. |
| `img_021.jpg` | Dòng xe dày, nhiều người ở xa | R-03, R-06 | Tách người và xe rõ ở tiền cảnh. Kiểm pixel trên ảnh gốc trước khi khoanh vùng xa có vật nhỏ hoặc cá thể không tách được. |
| `img_014.jpg` | Phương tiện nhòe chuyển động cạnh người đi bộ rõ | R-02, R-07 | Gán người nhận diện được. Với xe mờ, chỉ gán khi có căn cứ xác định lớp và phần thân nhìn thấy. Nếu không đủ, ghi vị trí và lý do để review. |

## 5. QC và phiên bản

- Giữ nguyên ngưỡng trong `submission/taxonomy.json`. QC vị trí dùng IoU **≥ 0,85** khi box cao **≥ 50 px**, và **≥ 0,70** khi thấp hơn. IAA dùng ghép 1–1 với IoU **≥ 0,50**, báo IoU trung bình (ngưỡng **0,85**) và tỉ lệ cùng lớp (ngưỡng **95%**) trên cặp ghép. Báo riêng box không ghép được và ghi N/A nếu không có cặp.
- Duyệt toàn bộ lô cuối. Báo tỉ lệ theo ảnh và theo đối tượng với tử số/mẫu số. Hold khi thiếu bằng chứng hoặc đặc tả/dữ liệu còn vấn đề. Rework khi quá 2% ảnh lỗi hoặc có lỗi lặp. Release khi đủ bằng chứng, đạt ngưỡng và có reviewer xác nhận. Với 40 ảnh, một ảnh lỗi tương đương 2,5%.
- Trong lượt gán độc lập, giữ nguyên v1.0 nhóm đã khóa. Đưa ca mơ hồ ra buổi calibration. Nhóm ghi người chốt theo mã, ảnh, quyết định, Rule ID, phạm vi sửa và kết quả kiểm lại. Giữ bản cá nhân Pha 1 làm mốc so sánh sau khi nộp riêng.

| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| `v0.1-103` | Đề xuất thêm `bus` và `tuk_tuk`, ngưỡng che, tách người–xe, quy tắc xe chở xe, vùng ignore và vật giả. | Xử lý các điểm v0 còn mơ hồ, ví dụ ảnh 002, 004, 021, 026, 035 và 037. |
