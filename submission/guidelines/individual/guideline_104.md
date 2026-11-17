# Guideline gán nhãn cá nhân — bản lưu hiện có — mã 104

> Bản tổng hợp hồ sơ cho thấy file này chứa một bản guideline cá nhân v0.1, nhưng tác giả/nội dung chưa được thành viên 104 xác nhận trong báo cáo. 104 cần rà lại đây có phải bản đã viết độc lập ở Pha 1 hay không trước khi nộp; không xem phần bổ sung báo cáo là xác nhận thay thành viên.

> Copy file này (hoặc `guideline_v0_starter.md`) rồi viết. Một guideline đủ gồm **5 phần**. Câu nào của v0
> làm hai người đọc ra hai cách khác nhau thì phải viết lại cho một cách hiểu duy nhất.

- Phiên bản: v0.1
- Ngày: 16/11/2026
- Người duyệt: Chưa duyệt (guideline cá nhân)

## 1. Mục tiêu

Bộ dữ liệu được sử dụng để huấn luyện và đánh giá mô hình AI phát hiện đối tượng (Object Detection) trong ảnh giao thông đường phố bằng Bounding Box.

Mục tiêu:
- Xác định vị trí các đối tượng xuất hiện trong ảnh.
- Phân loại đối tượng theo danh sách lớp đã quy định.
- Đảm bảo các thành viên gán nhãn nhất quán, hạn chế sai lệch giữa những người gán nhãn.
- Tạo dữ liệu có chất lượng để phục vụ huấn luyện và đánh giá mô hình AI.

Các lỗi cần hạn chế:
- Bỏ sót người hoặc phương tiện tham gia giao thông.
- Gán sai lớp đối tượng.
- Vẽ Bounding Box không chính xác.
- Gán nhãn không thống nhất khi đối tượng bị che khuất hoặc bị cắt bởi mép ảnh.
- Gán nhãn các đối tượng không thuộc phạm vi bộ dữ liệu.

Ưu tiên độ chính xác, tính nhất quán và khả năng kiểm tra lại kết quả gán nhãn.


## 2. Lớp và thuộc tính

### 2.1. Lớp

Mỗi đối tượng chỉ được gán một lớp phù hợp nhất.

| Lớp | Định nghĩa | Ví dụ | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| car | Ô tô con dùng chở người, không có khoang hàng chuyên dụng | Sedan, SUV, hatchback | Xe tải, xe van |
| truck | Xe có kết cấu chuyên dùng chở hàng hoặc kéo hàng | Xe tải thùng, xe ben, xe đầu kéo | Xe con, xe van nhỏ |
| van | Xe dạng thùng kín cỡ nhỏ, có khoang chở hàng hoặc hành khách | Xe van giao hàng | Xe tải lớn, SUV |
| motorcycle | Phương tiện cơ giới hai hoặc ba bánh thuộc nhóm mô tô, xe máy | Xe tay ga, xe số, mô tô | Xe đạp, xe điện dạng xe đạp |
| person | Người thật xuất hiện trong ảnh, kể cả đang đi bộ hoặc điều khiển phương tiện | Người đi bộ, người ngồi trên xe máy | Tượng, ma-nơ-canh, người trên biển quảng cáo |
| ignore_region | Vùng khó phân biệt từng đối tượng hoặc không thể gán nhãn đáng tin cậy | Đám đông quá dày, vùng đối tượng quá mờ | Đối tượng vẫn nhìn rõ và có thể gán riêng |

**Đối tượng không thuộc lớp nào:**
- Không tự ý tạo thêm lớp mới.
- Không gán nhãn những đối tượng ngoài danh sách.
- Chỉ sử dụng ignore_region khi thực sự không thể gán riêng đáng tin cậy, không dùng để thay thế việc gán nhãn đối tượng khó.
- Nếu chưa chắc đối tượng thuộc lớp nào, ghi nhận để nhóm xem xét.

### 2.2. Thuộc tính

#### Thuộc tính 1: occluded_level

Mô tả mức độ đối tượng bị vật khác che khuất.

- 0: Không bị che, nhìn thấy gần như toàn bộ đối tượng.
- 1: Bị che nhẹ, ước lượng phần bị che lớn hơn 0% đến 30%.
- 2: Bị che nhiều, phần bị che lớn hơn 30% đến 70%.
- 3: Bị che rất nhiều, phần bị che lớn hơn 70%, nhưng vẫn đủ căn cứ xác định lớp.

Tỉ lệ che được ước lượng dựa trên hình dạng đầy đủ của đối tượng.

#### Thuộc tính 2: truncated

Mô tả đối tượng bị cắt bởi mép ảnh.

- no: Đối tượng nằm hoàn toàn trong ảnh.
- yes: Một phần đối tượng nằm ngoài khung ảnh.

Đối tượng bị vật khác che nhưng không vượt mép ảnh thì truncated = no.

#### Thuộc tính 3: can_review

Đánh dấu đối tượng cần kiểm tra lại.

- Không tick: Người gán nhãn xác định được lớp, box và thuộc tính.
- Tick: Chưa chắc chắn về lớp, box hoặc thuộc tính.

Các trường hợp can_review phải được đưa ra thảo luận trong quá trình calibration.


## 3. Quy tắc vẽ box

### R01. Nguyên tắc chung
- Sử dụng Bounding Box (Rectangle) để gán nhãn.
- Mỗi đối tượng hợp lệ được gán một box riêng.
- Box phải ôm sát phần nhìn thấy của đối tượng.
- Không vẽ box quá rộng, chứa nhiều nền không cần thiết.
- Không gộp nhiều đối tượng thành một box.

### R02. Đối tượng bị che khuất
- Chỉ vẽ box bao quanh phần nhìn thấy được.
- Không tự ước lượng phần cơ thể hoặc phương tiện nằm sau vật cản.
- Nếu vẫn xác định được đối tượng, tiếp tục gán nhãn.
- Đặt occluded_level theo mức độ che khuất.
- Nếu không chắc chắn, đánh dấu can_review.

### R03. Đối tượng bị cắt bởi mép ảnh
- Chỉ vẽ box trong phạm vi ảnh.
- Không kéo box vượt ra ngoài mép ảnh.
- Đặt truncated = yes.
- Nếu đồng thời bị vật khác che, đánh dấu thêm occluded_level phù hợp.

### R04. Người điều khiển phương tiện
- Người và phương tiện là hai đối tượng riêng.
- Người đi xe máy: một box person và một box motorcycle.
- Không gộp người và xe thành một box.
- Người ngồi trong ô tô chỉ được gán person khi đủ căn cứ nhận diện và có thể xác định vùng nhìn thấy.

### R05. Đối tượng quá nhỏ hoặc quá mờ
- Chỉ gán nhãn khi có đủ đặc điểm để nhận diện lớp.
- Không đoán loại phương tiện khi hình ảnh không đủ rõ.
- Đối tượng nhỏ nhưng vẫn xác định được lớp thì tiếp tục gán.
- Nếu khó xác định, đánh dấu can_review hoặc ghi nhận vấn đề cấp ảnh.

### R06. Hình phản chiếu và hình in
- Không gán nhãn người hoặc xe xuất hiện trong tranh, ảnh quảng cáo và màn hình.
- Không gán nhãn hình phản chiếu trên kính hoặc gương.
- Chỉ gán nhãn đối tượng thật xuất hiện trực tiếp trong cảnh.

### R07. Tượng, đồ chơi và mô hình
- Không gán nhãn tượng người, ma-nơ-canh hoặc đồ chơi thành person.
- Không gán nhãn xe mô hình thành phương tiện thật.
- Nếu không chắc đối tượng là thật hay mô hình, đánh dấu can_review.

### R08. Đám đông
- Nếu từng người có thể phân biệt được, gán box riêng cho từng người.
- Nếu nhiều người chồng lấn quá mức, không thể xác định từng người, xem xét ignore_region.
- Không dùng ignore_region chỉ để tiết kiệm thời gian.

### R09. Xe chủ (ego vehicle)
- Không gán box cho xe chứa camera khi chỉ nhìn thấy một phần thân xe ở sát mép ảnh.
- Các phương tiện khác xuất hiện trong ảnh vẫn được gán bình thường.
- Nếu không xác định được xe có thuộc ego vehicle hay không, đánh dấu can_review.

### R10. Phương tiện đặc biệt
- Xe chở một phương tiện khác: gán riêng các đối tượng nhìn thấy nếu đủ căn cứ.
- Xe tuk-tuk hoặc phương tiện không thuộc các lớp hiện có: không tự ý thêm lớp.
- Xe giả tưởng hoặc tượng phương tiện: không gán thành xe thật.
- Trường hợp khó phân biệt car, truck và van phải được đưa vào calibration.

### R11. Kiểm tra trước khi lưu
- Kiểm tra không bỏ sót đối tượng thuộc phạm vi gán nhãn.
- Kiểm tra mỗi box có đúng lớp.
- Kiểm tra occluded_level, truncated và can_review.
- Kiểm tra không có box trùng lặp không cần thiết.
- Lưu kết quả trước khi chuyển sang ảnh tiếp theo.


## 4. Ca khó
| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_001.jpg | Xe bán tải có thùng hàng, dễ nhầm car/truck | R10 | Gán `truck` | Có khoang chở hàng riêng phía sau cabin; không phân loại theo dáng đầu xe. |
| img_002.jpg | Xe chở nhiều ô tô, các xe bị khung chở che khuất | R02, R10 | Gán riêng `truck` và từng `car` nhìn thấy đủ căn cứ; vẽ theo phần nhìn thấy | Không gộp xe chở và xe được chở; đặt mức che khuất cho từng xe. |
| img_003.jpg | Nhiều người điều khiển/ngồi trên xe máy chồng lấn | R02, R04, R08 | Gán riêng từng `person` và `motorcycle` còn phân biệt được | Người và xe là hai đối tượng; không gộp các cá thể bị che nhau. |
| img_004.jpg | Xe tuk-tuk ba bánh có người lái | R04, R10 | Không gán tuk-tuk vào lớp xe hiện có; gán `person` nếu nhận diện được | Tuk-tuk không phải lớp trong taxonomy; người thật vẫn thuộc lớp `person`. |
| img_009.jpg | Xe khách cỡ nhỏ/minibus, có thể bị nhầm với `van` | R05, R10 | Cần review; không ép thành `van` nếu chưa thống nhất | Taxonomy không có lớp bus; hình dáng xe khách không đủ căn cứ để tự đổi định nghĩa `van`. |
| img_011.jpg | Tượng/quái vật trưng bày cạnh cảnh đường phố | R07 | Không gán tượng là `person`; chỉ gán phương tiện/người thật nếu đủ rõ | Đây là vật thể điêu khắc, không phải người thật. |
| img_013.jpg | Xe chuyển động bị nhòe; xe ở hai mép ảnh bị cắt | R03, R05 | Box xe nhận diện được trong khung ảnh và đặt `truncated=yes` khi chạm mép; xe nhòe chưa rõ lớp: Cần review | Không kéo box ra ngoài ảnh hoặc đoán lớp cho vùng không đủ chi tiết. |
| img_014.jpg | Xe bán tải chở hàng, dễ nhầm car/truck | R10 | Gán `truck` | Thùng chở hàng tách biệt phía sau cabin nên thuộc `truck`. |
| img_015.jpg | Tuk-tuk và xe máy/người lái; một số đối tượng sát mép ảnh | R03, R04, R10 | Loại tuk-tuk khỏi lớp xe; gán riêng người và xe máy nhìn thấy, đặt `truncated=yes` nếu bị cắt | Không xem tuk-tuk là xe máy chỉ vì có ba bánh; người lái là đối tượng riêng. |
| img_016.jpg | Tượng người cưỡi ngựa | R07 | Không gán tượng thành `person` | Hình người là tượng, không phải người thật. |
| img_017.jpg | Người trên biển quảng cáo; phương tiện thật phía sau hàng rào | R02, R06 | Bỏ người in trên biển; chỉ gán xe thật nhìn thấy được, đặt mức che khuất phù hợp | Hình in không thuộc cảnh thật; hàng rào che một phần các xe. |
| img_018.jpg | Xe màu vàng đặt trên nóc một xe khác trong không gian trưng bày | R07, R10 | Cần review xem xe vàng là phương tiện thật hay mô hình; gán xe đen nếu nhận diện được | Chỉ gán riêng xe thứ hai khi đủ căn cứ phân biệt phương tiện thật với mô hình trưng bày. |
| img_019.jpg | Xe diễu hành kiểu giả tưởng, có mascot và đám đông | R07, R08, R10 | Không gán xe giả tưởng/mascot như xe thật hoặc `person`; gán người thật phân biệt được | Xe và mascot là vật trưng bày; chỉ gán người thật, không gộp đám đông. |
| img_020.jpg | Đám đông xe máy dày, người và xe che lẫn nhau | R02, R08 | Gán riêng đối tượng phân biệt được; chỉ dùng `ignore_region` cho vùng không thể tách cá thể | Không bỏ qua cả vùng chỉ vì đông; box từng người/xe khi còn đủ căn cứ. |
| img_021.jpg | Cảnh đường và phương tiện chỉ xuất hiện trong gương chiếu hậu | R06 | Không gán các hình phản chiếu trong gương | Đây là ảnh phản chiếu, không phải đối tượng xuất hiện trực tiếp trong cảnh. |
| img_022.jpg | Xe máy cổ có gắn sidecar | R10 | Gán một `motorcycle` cho tổ hợp xe máy-sidecar | Sidecar là bộ phận của phương tiện; không tách thành một xe riêng. |
| img_023.jpg | Xe xích lô/xe đạp ba bánh có người điều khiển | R04, R10 | Không gán xe đạp/xích lô vào lớp xe hiện có; gán `person` nhìn thấy được | Đây không phải phương tiện cơ giới thuộc lớp `motorcycle`. |
| img_025.jpg | Người và phương tiện ở rất xa, kích thước nhỏ | R05 | Chỉ gán khi đủ đặc điểm nhận diện lớp; đối tượng quá nhỏ/mờ chưa chắc: Cần review | Không suy đoán lớp từ các chi tiết không phân biệt được. |
| img_026.jpg | Người minh họa trên pano cạnh người lái xe máy thật | R04, R06 | Bỏ người minh họa; gán riêng `person` và `motorcycle` thật | Hình trên pano là hình in; người thật và xe máy là hai đối tượng riêng. |
| img_027.jpg | Tượng xe bán tải bằng đá | R07, R10 | Không gán tượng thành `truck` hoặc `car` | Đây là mô hình/tượng, không phải phương tiện thật. |
| img_028.jpg | Xe bán tải thật chở tượng ngựa | R07, R10 | Gán xe là `truck`; không gán tượng ngựa thành đối tượng thật | Phân biệt phương tiện thật với vật điêu khắc đặt trên thùng xe. |
| img_029.jpg | Bãi xe máy đỗ sát và chồng lấn; có hình người trên áp phích | R02, R06, R08 | Gán riêng xe phân biệt được; bỏ hình người in; Cần review vùng xe không thể tách | Không gộp xe thật thành một box; hình in không phải người trong cảnh. |
| img_030.jpg | Người hoạt hình trên biển hiệu và phương tiện/người thật ở xa trong cảnh tối | R05, R06 | Bỏ hình hoạt hình; chỉ gán đối tượng thật đủ nhận diện, trường hợp mờ/nhỏ: Cần review | Phân biệt hình in với người thật và không đoán lớp trong vùng thiếu chi tiết. |
| img_031.jpg | Đám đông chờ xe; ô tô xanh bị cắt ở mép trái | R03, R08 | Gán người tách biệt được; gán phần xe nhìn thấy và đặt `truncated=yes` | Người trong đám đông vẫn gán riêng nếu nhận diện được; box xe không vượt mép ảnh. |
| img_032.jpg | Hai người trên xe máy trước hình minh họa khổ lớn | R04, R06 | Gán riêng người và xe máy thật; bỏ hình minh họa | Hình vẽ nền không phải đối tượng thật; người và xe không gộp thành một box. |
| img_033.jpg | Ma-nơ-canh và hình phản chiếu trong cửa kính cửa hàng | R06, R07 | Không gán ma-nơ-canh thành `person` hoặc gán hình phản chiếu | Không phải người thật xuất hiện trực tiếp trong cảnh. |
| img_034.jpg | Người đi bộ/đi xe máy ở sát mép phải, một phần bị cắt | R03, R04 | Gán riêng người và xe máy; đặt `truncated=yes` cho đối tượng bị mép ảnh cắt | Không bỏ người chỉ vì đang đi cạnh xe; không vẽ box vượt khung ảnh. |
| img_035.jpg | Xe tuk-tuk chở hàng và xe máy trong cùng cảnh | R04, R10 | Loại tuk-tuk khỏi lớp xe; gán xe máy và người thật nhìn thấy được | Không tự thêm lớp cho tuk-tuk; người điều khiển vẫn gán riêng. |
| img_036.jpg | Xe bán tải có nắp khoang hàng kín, dễ nhầm `van`/`truck` | R10 | Gán `truck` | Hình dáng cabin và thùng hàng tách biệt cho thấy đây là xe bán tải, không phải van liền thân. |
| img_037.jpg | Xe đồ chơi/mô hình và đồ chơi hình người trong tủ trưng bày | R07 | Không gán các mô hình thành xe thật hoặc `person` | Các vật thể là đồ chơi trưng bày, không phải đối tượng giao thông thật. |
| img_039.jpg | Ảnh người in trên xe taxi; xe ở tiền cảnh bị cắt khung | R03, R06 | Bỏ ảnh in; gán xe thật nhìn thấy được và đặt `truncated=yes` nếu bị cắt | Ảnh in không phải người thật; box xe chỉ nằm trong phạm vi ảnh. |


## 5. QC và phiên bản

### 5.1. Nguyên tắc kiểm tra chất lượng

- Kiểm tra tính chính xác và nhất quán của nhãn.
- Kiểm tra đúng lớp, vị trí box và các thuộc tính.
- Kiểm tra các đối tượng bị che khuất, cắt mép ảnh và trường hợp khó.
- Kiểm tra các box có đánh dấu can_review.
- Kiểm tra trường hợp bỏ sót hoặc gán thừa đối tượng.
- Mỗi ảnh phải được gán nhãn độc lập theo phân công.
- Không tự ý sửa nhãn của thành viên khác khi chưa thống nhất.

### 5.2. Ngưỡng QC

Áp dụng các trạng thái sau:

- Release: Kết quả kiểm tra đạt yêu cầu, không có lỗi lặp và được người kiểm xác nhận.
- Rework: Tỷ lệ ảnh lỗi lớn hơn 2% hoặc xuất hiện lỗi lặp.
- Hold: Thiếu bằng chứng, guideline chưa thống nhất hoặc dữ liệu có vấn đề cần xác minh.

Mặc định kiểm tra toàn bộ 40 ảnh.

Với 40 ảnh, chỉ cần 1 ảnh lỗi đã tương đương 2,5%, vượt ngưỡng 2%.

Các ngưỡng trong taxonomy.json phải được giữ nguyên theo yêu cầu bài tập.

### 5.3. Xử lý trường hợp mơ hồ

- Người gán nhãn đánh dấu can_review hoặc ghi nhận vấn đề cấp ảnh.
- Các thành viên thảo luận trường hợp chưa thống nhất.
- Nhóm quyết định dựa trên guideline và bằng chứng từ ảnh.
- Mỗi trường hợp cần ghi mã Rule ID, quyết định và lý do.
- Nếu thay đổi quy tắc, phải cập nhật phiên bản guideline.
- Nếu thay đổi làm ảnh hưởng cách gán nhãn của cả bộ dữ liệu, phải rà soát lại toàn bộ lô.

Người phụ trách tổng hợp QC: 104.

Người chốt các trường hợp mơ hồ: Nhóm thống nhất trong buổi calibration; ghi mã thành viên thực tế vào nhật ký quyết định.

Người kiểm tra lại: Thành viên khác với người trực tiếp sửa nhãn, khi có thể.

### 5.4. Lịch sử phiên bản

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0.1 | Xây dựng guideline cá nhân, bổ sung định nghĩa lớp, thuộc tính, quy tắc R01–R11 và các ca khó | Làm rõ những tình huống mơ hồ trong guideline v0 |
| v1.0 | Chưa thực hiện – chờ nhóm thống nhất | Đối chiếu guideline của 4 thành viên |
| v1.1 | Chưa thực hiện – chỉ cập nhật khi có calibration | Sửa các quy tắc hoặc trường hợp bất đồng thực tế |

### 5.5. Ghi nhận và bàn giao QC

- Ghi nhận kết quả IAA do script tạo.
- Theo dõi các trường hợp cần calibration.
- Đối chiếu nhãn cuối với guideline đã thống nhất.
- Ghi nhận lỗi QC theo từng ảnh và Rule ID.
- Lập báo cáo QC_REPORT.md.
- Chỉ xác nhận Release khi đã kiểm tra và đủ bằng chứng.
- Nếu chưa đạt, ghi Hold hoặc Rework cùng nguyên nhân.
- Kiểm tra đầy đủ các file bắt buộc trước khi đóng gói bài nộp.
