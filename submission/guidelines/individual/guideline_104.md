# Guideline gán nhãn — đề xuất cá nhân 104

- Phiên bản: `v0.1-104` (đề xuất ở Pha 1)
- Phạm vi: 40 ảnh đường phố; bounding box 2D; CVAT; COCO 1.0.
- Đây là đề xuất cá nhân để mang ra thảo luận. Các lớp bổ sung bên dưới chỉ dùng sau khi nhóm chốt taxonomy; lượt gán độc lập phải theo bản v1.0 đã khóa.

## 1. Mục tiêu và nguyên tắc

Tạo nhãn nhất quán cho người và phương tiện thật nhìn thấy trong ảnh, phục vụ mô hình phát hiện giao thông. Đếm từng cá thể có thể phân biệt; không suy đoán phần khuất chỉ để tạo box đầy đủ. Ưu tiên tránh nhầm người/vật thể thật với ảnh in, tượng, đồ chơi hoặc hình phản chiếu.

Thứ tự quyết định: (1) vật có thật và thuộc phạm vi không, (2) có đủ bằng chứng nhận diện lớp không, (3) có thể tách thành cá thể riêng không, (4) vẽ box và điền thuộc tính. Nếu chưa đủ bằng chứng, dùng `can_review` khi vẫn có box hợp lý; nếu không vẽ được box, ghi vấn đề theo ảnh và vùng.

## 2. Lớp và thuộc tính

### Đề xuất lớp

| Lớp | Định nghĩa thao tác | Ví dụ / cách phân biệt |
|---|---|---|
| `person` | Người sống nhìn thấy trực tiếp; gồm người đi bộ, lái xe và hành khách nếu nhận ra được cơ thể. | Không gán tượng, hình in trên biển quảng cáo hoặc ma-nơ-canh. |
| `car` | Ô tô chở người có thân xe kiểu sedan, hatchback, wagon hoặc SUV. | Bán tải có khoang chở hàng phía sau xếp vào `truck`. |
| `truck` | Xe chở hàng có cabin và thùng/sàn hàng phân biệt được; gồm xe bán tải và xe chở ô tô. | Hàng hóa không làm thay đổi lớp của xe. |
| `van` | Xe có khoang kín liền thân với cabin, không có thùng/sàn hàng tách biệt. | Khi không thấy cấu trúc đủ rõ để phân biệt van với bán tải, đánh dấu xem lại thay vì đoán. |
| `motorcycle` | Xe máy hoặc mô tô có động cơ; đề xuất gộp sidecar gắn cố định cùng một xe. | Xe đạp và xích lô đạp không thuộc lớp này. |
| `bus` *(đề nghị nhóm xem xét)* | Xe chở nhiều hành khách, có thân xe buýt/minibus nhận diện được qua cấu trúc khoang và cửa sổ. | Không phân loại van thành bus chỉ vì thân có cửa sổ. |
| `tuk_tuk` *(đề nghị nhóm xem xét)* | Xe ba bánh có động cơ với khoang khách/hàng tích hợp đặc trưng. | Xe máy gắn sidecar rời vẫn là `motorcycle` theo đề xuất này. |
| `ignore_region` | Vùng chứa cá thể thuộc phạm vi nhưng quá nhỏ hoặc quá dày để gán riêng đáng tin cậy. | Không dùng để che vật ngoài phạm vi như xe đạp, tượng hay hình in. |

Đề xuất taxonomy có `bus` và `tuk_tuk` vì chúng là phương tiện thật nhưng không được mô tả rõ bởi sáu lớp trong v0. Trước khi nhóm thông qua hai lớp này, không tự thêm nhãn vào lượt gán độc lập.

### Thuộc tính

| Thuộc tính | Quy tắc chọn |
|---|---|
| `occluded_level` | Ước lượng phần diện tích hình chiếu bị vật khác che, chỉ tính phần vật nằm trong ảnh: `0` = 0%; `1` = trên 0% đến 30%; `2` = trên 30% đến 70%; `3` = trên 70% nhưng vẫn nhận ra lớp. Dùng phần cơ thể/thân xe còn thấy làm căn cứ; tick `can_review` nếu sát ngưỡng hoặc khó ước lượng. |
| `truncated` | `yes` nếu khung ảnh cắt mất vật; `no` nếu vật chỉ chạm mép hoặc bị vật khác che. Có thể đồng thời bị che và bị cắt. |
| `can_review` | Tick khi đã có box hợp lý nhưng còn nghi ngờ lớp, biên box hoặc thuộc tính. Nếu không thể xác định vật/lớp hoặc không có căn cứ vẽ box, ghi `image`, mã `104`, vùng và lý do vào danh sách vấn đề ảnh. |

Với `ignore_region`, nếu CVAT yêu cầu thuộc tính thì đặt `occluded_level=0`, `truncated=no`; chỉ bật `can_review` khi vùng đó cần người khác quyết định.

## 3. Quy tắc vẽ box

| ID | Quy tắc |
|---|---|
| R104-01 | Chỉ gán người/phương tiện thật nhìn trực tiếp. Bỏ ảnh in, tượng, đồ chơi, bóng, phản chiếu và phương tiện rõ ràng ngoài taxonomy. Vật thật nhìn qua kính vẫn được gán nếu nhận diện được. Không gán bộ phận của xe chụp ảnh (ego vehicle), như gương hoặc mép cửa. |
| R104-02 | Box chữ nhật nhỏ nhất bao phần nhìn thấy của một cá thể, nằm trong khung ảnh. Với các phần nhìn thấy bị ngăn cách bởi vật che, dùng một box nếu có căn cứ chúng thuộc cùng cá thể; không mở rộng box qua phần chỉ phỏng đoán. |
| R104-03 | Vẽ riêng box phương tiện và từng người đủ điều kiện đang ngồi/đi trên đó; box được phép chồng lấn. Box người theo phần cơ thể nhìn thấy, gồm quần áo và mũ bảo hiểm. Sidecar gắn cố định được tính chung trong box xe máy theo đề xuất. |
| R104-04 | Với xe chở ô tô, vẽ xe chuyên chở thành một `truck`; từng ô tô trên sàn có thể có box `car` riêng nếu nhận diện được và cao ít nhất 20 px. Vật trưng bày không phải một xe hoàn chỉnh hoặc chỉ là mô hình không gán riêng. |
| R104-05 | Box phương tiện bao các bộ phận gắn cố định nhìn thấy; loại hàng hóa rời nhô ra. Phân biệt bán tải và van bằng cấu trúc cabin/thùng, không chỉ bằng hình dáng tổng thể. Nếu ảnh không cho thấy dấu hiệu phân biệt, ghi xem lại. |
| R104-06 | Đo chiều cao phần nhìn thấy trên ảnh gốc. Từ 20 px trở lên, gán riêng nếu nhận diện và tách được cá thể. Dưới 20 px, đề xuất dùng `ignore_region` sát cá thể/cụm khó tách. Trong đám đông, vẫn gán từng cá thể rõ trước; chỉ khoanh phần không thể tách. |
| R104-07 | Ảnh mờ không tự động loại vật: chỉ gán nếu hình dạng còn lại đủ để xác định lớp và vị trí box. Không kéo box theo vệt nhòe không thuộc phần nhận diện được. Nếu thiếu căn cứ, ghi vấn đề ảnh để reviewer xử lý. Giữ ảnh không có đối tượng trong COCO với 0 annotation. |

## 4. Ca cần đối chiếu trên ảnh gốc

Các quyết định dưới đây là giả thuyết ban đầu của người viết; cần kiểm tra ảnh gốc trước khi nộp riêng.

| Ảnh | Điểm cần quyết định | Rule | Đề xuất và lý do |
|---|---|---|---|
| `img_002.jpg` | Xe chở ô tô | R104-04 | Một box `truck` cho đầu kéo và sàn; thêm từng `car` chỉ khi thấy đủ hình dáng của một xe hoàn chỉnh và đạt 20 px. Cách này tránh gán từng mảng thân xe không nhận diện được thành ô tô. |
| `img_004.jpg` | Xe ba bánh kiểu tuk-tuk | R104-01 | Nếu xác nhận là xe có động cơ và khoang tích hợp, đề xuất taxonomy có `tuk_tuk`; cần nhóm chốt trước khi gán, không ép vào `motorcycle` chỉ để khớp v0. |
| `img_017.jpg`, `img_018.jpg`, `img_033.jpg` | Tượng, hình người, ma-nơ-canh | R104-01 | Không gán `person` vì không phải người sống xuất hiện trực tiếp; vẫn rà các đối tượng thật khác trong cùng ảnh. |
| `img_020.jpg` | Phản chiếu/gương | R104-01, R104-07 | Không tạo box cho ảnh phản chiếu hay gương của xe chụp. Nếu không còn vật thật thuộc lớp nào khác, ảnh hợp lệ với 0 annotation. |
| `img_021.jpg` | Người/phương tiện ở xa trong dòng đông | R104-06 | Gán riêng vật đủ 20 px và phân biệt được. Với phần nhỏ/dày không tách nổi, khoanh đúng vùng đó bằng `ignore_region`; không phủ lên các box rõ. |
| `img_026.jpg` | Người đi xe máy | R104-03 | Mỗi người nhìn thấy đủ điều kiện có box `person` riêng, đồng thời có một box `motorcycle`; việc ngồi trên xe không làm người mất nhãn. |
| `img_035.jpg` | Tuk-tuk chở hàng cao | R104-05 | Box xe chỉ bao kết cấu và mái gắn cố định; loại bao tải/hàng rời. Cần xác nhận ranh giới xe với hàng trên ảnh gốc. |
| `img_014.jpg` | Phương tiện nhòe cạnh người đi bộ | R104-07 | Gán người nếu rõ. Chỉ gán phương tiện khi phần thân còn thấy đủ để nhận dạng lớp; nếu không, ghi vùng và lý do thay vì đoán từ vệt nhòe. |

## 5. QC và lịch sử phiên bản

Áp dụng các ngưỡng hiện có trong `submission/taxonomy.json`, không sửa mục `rules`: box cao từ 50 px dùng ngưỡng IoU vị trí 0,85; box nhỏ hơn dùng 0,70. IAA ghép box 1–1 từ IoU 0,50; báo IoU trung bình với mục tiêu 0,85 và đồng thuận lớp 0,95 trên các cặp ghép. Báo riêng box không ghép; nếu không có cặp thì ghi N/A.

Đề xuất reviewer xem toàn bộ lô cuối và báo lỗi theo ảnh lẫn đối tượng, kèm tử số/mẫu số. Hold nếu thiếu bằng chứng hoặc quy tắc chưa chốt; Rework nếu tỷ lệ ảnh lỗi vượt 2% hoặc có lỗi lặp; Release khi bằng chứng/ngưỡng đạt và reviewer xác nhận. Với 40 ảnh, một ảnh lỗi là 2,5%, vì vậy cần nêu rõ số ảnh thay vì làm tròn tỷ lệ.

Trong gán độc lập, theo guideline và taxonomy v1.0 đã khóa. Đưa bất đồng sang calibration; mọi quyết định sửa cần ghi ảnh, mã người chốt, Rule ID, phạm vi sửa và kết quả kiểm lại. Bản cá nhân này được giữ nguyên làm mốc Pha 1.

| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| `v0.1-104` | Viết lại quy tắc theo thứ tự quyết định; nêu điều kiện riêng cho vật chở trên xe, vùng ignore và vật mờ; đề nghị nhóm xem xét `bus`, `tuk_tuk`. | V0 chưa định nghĩa đủ lớp phương tiện và chưa chỉ cách xử lý các tình huống trên; cần đưa các ca ảnh cụ thể vào thảo luận Pha 2. |
