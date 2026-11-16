# Guideline cá nhân — Nguyễn Văn Nhất — bản nháp v0.1

- Phiên bản: `v0.1-draft`, đề xuất cá nhân trước buổi thống nhất nhóm.
- Thành viên: Nguyễn Văn Nhất — `2A202603278` — Người 4, phụ trách QC và bàn giao.
- Trạng thái: Bản nháp, chưa phải guideline thống nhất.
- Nguồn đối chiếu: `guideline/guideline_v0_starter.md`, `submission/taxonomy.json`, `docs/QC_CHEATSHEET.md` và 40 ảnh `img_001.jpg`–`img_040.jpg`.
- Ảnh đã được đối chiếu khi soạn: tổng quan 40 ảnh, xem kỹ ảnh gốc 005, 006, 019, 024, 027, 028. Khi gán vẫn cần mở ảnh gốc để đo, nhất là vật nhỏ ở xa.

## 1. Mục tiêu

Nhãn dùng cho bài toán phát hiện người và phương tiện trong ảnh đường phố. Bản này bổ sung những chỗ v0 còn nói chung chung, như “box ôm sát vật” hoặc “bị che ít”, để khi gán không phải tự hiểu lại ở từng ảnh.

Các lỗi cần chú ý là bỏ sót người, gộp người với xe và gán nhầm tượng hoặc ảnh in. Bộ ảnh còn có bãi xe, cửa hàng đồ chơi và vật trưng bày nên không thể chỉ thấy hình dáng giống xe là gán. Phạm vi đánh giá của bài này là 40 ảnh được giao.

### Điểm cần chú ý khi làm QC

Phần việc của Nhất là QC và bàn giao, nên ghi chú phải đủ rõ để người khác tìm lại và sửa được. Chẳng hạn, thay vì ghi “xe này giống xe tải”, cần chỉ ra cabin tách với thùng hàng ở đâu và dẫn quy tắc tương ứng.

Khi kiểm lại bản nháp, ưu tiên ba việc: người và xe có được tách đúng không, vật đó là thật hay mô phỏng, và vùng `ignore_region` có phủ lên vật vẫn gán được không. Phần dưới là cách xử lý đề xuất; các ca chưa chắc được ghi riêng để hỏi nhóm.

### Các lựa chọn của bản này

Bản này đề xuất giữ taxonomy hiện tại cho lượt gán đầu tiên. Xe đạp, bus và xe ba bánh chưa có lớp tương ứng thì ghi rõ là ngoài phạm vi, thay vì tự đưa thêm lớp vào Task. Lý do là khi kiểm COCO, cần biết một vật không có box vì bị bỏ sót hay vì đã được loại theo quy tắc. Nếu nhóm muốn mở rộng lớp, cần sửa taxonomy và guideline cùng lúc trước khi gán.

Mức che đề xuất là 0%, đến 30%, đến 60% và trên 60%. Mốc 60% nhằm đưa những vật bị che phần lớn vào nhóm cần chú ý khi kiểm; đây là lựa chọn của bản nháp, không phải ngưỡng bắt buộc của lab. Tỉ lệ này chỉ ước lượng được, nên ca sát mốc cần ghi lý do thay vì coi kết quả là phép đo chính xác.

Đối với vật chưa rõ thật hay mô hình, ưu tiên để lại câu hỏi cụ thể cho nhóm. Ví dụ ở img_024, câu hỏi cần giải quyết là “vật màu vàng trên nóc là xe thật chưa hoàn thiện hay vỏ trưng bày?”, không chỉ ghi chung chung “ảnh khó”.

**R-01 — Phạm vi:** Chỉ gán đối tượng vật lý thật thuộc năm lớp đích bên dưới, có đủ dấu hiệu nhận diện và phần nhìn thấy đạt chiều cao tối thiểu. `ignore_region` là vùng đánh giá bỏ qua, không phải lớp phương tiện. Xét vật đang đi, đang đỗ, trong bãi, trong nhà và đang được vận chuyển theo cùng tiêu chí; vị trí không tự quyết định lớp.

## 2. Lớp và thuộc tính

### 2.1. Các lớp

Giữ đúng sáu tên lớp hiện có, chưa thêm lớp mới trong bản cá nhân.

| Lớp | Cách phân biệt | Ví dụ trong bộ ảnh | Trường hợp dễ nhầm |
|---|---|---|---|
| `car` | Ô tô chở người dạng sedan, hatchback, wagon, SUV hoặc MPV; không có thùng hàng hở tách cabin và không có thân xe tải chuyên dụng. | Ô tô ở img_015; taxi xanh img_040; wagon đen phía dưới img_024. | Xe pickup có thùng riêng là truck; xe buýt ngoài taxonomy; không phân lớp chỉ theo kích thước. |
| `truck` | Xe tải hoặc pickup có cabin và khu vực chở hàng tách biệt về cấu trúc, gồm thùng hở, thùng kín gắn sau cabin và xe chuyên chở ô tô. | Xe tải chở ô tô img_002; pickup img_012; xe tải nhỏ thùng kín img_036. | Van có khoang hàng liền thân không tự thành truck chỉ vì chở hàng; tượng pickup img_027 không phải xe thật. |
| `van` | Xe dạng van với thân cao, khoang sau liền thân, dùng chở hàng hoặc minivan/minibus nhỏ có kiến trúc thân van rõ ràng. | Xe van chở hàng img_037; xe bạc thân van ở img_005. | MPV kiểu ô tô con thuộc car; xe tải thùng gắn riêng thuộc truck; xe buýt lớn ngoài taxonomy. Không đoán số ghế từ ảnh. |
| `motorcycle` | Xe hai bánh có động cơ, gồm mô tô và scooter/xe tay ga; nhãn chỉ bao phần xe. | Xe ở img_006, img_008, img_026. | Xe đạp, xích lô, tuk-tuk ba bánh không thuộc đề xuất lớp này. |
| `person` | Người thật ở mọi tư thế: đi bộ, ngồi, lái xe, hành khách hoặc đi xe đạp; từng người là một đối tượng. | Người qua đường img_014, img_034; người lái và người ngồi sau img_006. | Tượng, ma-nơ-canh, người trong hình in, đồ chơi và người chỉ xuất hiện qua phản chiếu. |
| `ignore_region` | Vùng khoanh hẹp nơi có đối tượng đích nhưng không thể gán từng vật đáng tin cậy do quá nhỏ, quá che hoặc không tách được cá thể. | Phần đám đông xa trong img_021 nếu đo trên ảnh gốc cho thấy không đạt điều kiện tách vật. | Không bao cả ảnh, cả đoàn xe hoặc vật khó phân lớp để né quyết định. Không dùng cho mọi vật ngoài taxonomy. |

**R-02 — Phân lớp xe:** Xét cấu trúc cabin/thùng trước, sau đó kiến trúc thân xe và chức năng thể hiện được trong ảnh. Biển quảng cáo, màu sơn, nhãn hiệu hoặc đang chở hàng không đủ để quyết định lớp. Chỗ giáp ranh car/van hoặc van/bus chưa đủ bằng chứng phải đưa reviewer, không tự suy ra số ghế hay tải trọng.

**R-03 — Ngoài taxonomy:** Không vẽ nhãn cho xe đạp, xích lô, xe buýt lớn, tuk-tuk/xe ba bánh hoặc động vật. Người thật trên các phương tiện đó vẫn được xét độc lập. Không tạo `ignore_region` chỉ vì một vật nằm ngoài lớp đích; chỉ dùng khi có vùng đối tượng đích không thể gán theo R-09. Mở rộng taxonomy cần nhóm thống nhất trước pha gán độc lập.

### 2.2. Thuộc tính cho năm lớp đối tượng

| Thuộc tính | Các mức cố định | Quy tắc điền đề xuất |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Ước lượng phần hình dáng chiếu 2D bị **vật khác** che trong phần đối tượng nằm trong ảnh: `0` không bị che; `1` bị che trên 0% đến 30%; `2` trên 30% đến 60%; `3` trên 60% hoặc không đủ cơ sở ước lượng vì che khuất. Mức 3 vẫn phải có bằng chứng nhận ra cá thể và lớp. Nếu không ước lượng được mức che, đồng thời bật can_review. |
| `truncated` | `no`, `yes` | `yes` khi một phần đối tượng thực sự nằm ngoài khung ảnh; `no` khi đối tượng không bị khung ảnh cắt. Chạm sát biên chưa đủ để kết luận nếu vật vẫn hiện trọn vẹn. |
| `can_review` | checkbox: `false`, `true` | `true` khi chưa chắc lớp, ranh giới cá thể, mức che, tính thật/giả hoặc cách áp dụng quy tắc; ghi vấn đề cụ thể để reviewer xử lý. Không dùng để bỏ qua mọi quyết định. |

**R-04 — Tách che khuất và cắt mép:** Không tính phần nằm ngoài ảnh là occlusion. Một vật có thể vừa `truncated=yes`, vừa có mức che lớn hơn 0. Không coi phần vốn không nhìn thấy do góc chụp, như mặt sau xe, là bị che. Cờ `occluded` có sẵn trong CVAT không thay cho thuộc tính `occluded_level`.

Các mốc 30% và 60% là đề xuất mới để làm rõ v0, cần nhóm chốt; chúng không thay các ngưỡng cố định trong `taxonomy.rules`. Không cần và không được mở rộng box để tính mức che. `ignore_region` không có ba thuộc tính trên theo cấu hình CVAT của repo.

## 3. Quy tắc vẽ box

### 3.1. Hình học và phần nhìn thấy

**R-05 — Box phần nhìn thấy:** Vẽ hình chữ nhật song song trục ảnh, nhỏ nhất bao tất cả các phần nhìn thấy thuộc **cùng một đối tượng**. Không dự đoán đầu xe/chân người nằm sau vật khác hoặc ngoài ảnh. Nếu các phần nhìn thấy rời nhau nhưng chắc chắn cùng vật, dùng một box bao chung; khoảng trống hoặc vật che ở giữa có thể nằm trong hình chữ nhật.

- Xe: bao thân, bánh, gương và bộ phận gắn cố định nhìn thấy; không bao bóng đổ, phản sáng trên đường, khói hoặc hàng hóa rời.
- Xe chở xe: xe vận chuyển và các ô tô được chở là cá thể riêng; khung bệ chở thuộc xe vận chuyển. Box xe vận chuyển có thể chứa xe khác do hình học, nhưng không mở rộng box chỉ để ôm hàng hóa.
- Người: bao đầu/mũ đang đội, thân và tay/chân nhìn thấy. Không mở rộng theo túi xách, hàng đang gánh hoặc cây dài đang mang. Quần áo đang mặc thuộc người.
- Box nằm trong kích thước ảnh gốc; chiều rộng và chiều cao dương. Không lấy kích thước trên thumbnail làm kích thước để xét ngưỡng.

### 3.2. Người và phương tiện

**R-06 — Tách người và xe:** Mỗi người một box `person`; mỗi xe đích một box theo lớp xe. Không có lớp rider. Box người không bao cả xe, box xe không mở rộng theo đầu/người ngồi trên xe. Các box có thể giao nhau.

- Một xe máy với một người lái và một người ngồi sau tạo **3 box**, nếu cả ba cá thể đều nhận diện được và đạt ngưỡng phần nhìn thấy.
- Một người đi xe đạp tạo **1 box person** nếu đủ điều kiện; xe đạp nằm ngoài taxonomy.
- Áp dụng thử: cặp người áo đỏ/áo vàng trên xe phía trái img_006 có đề xuất 2 box người và 1 box xe máy. Với hai người trên xe ở img_026, dùng cùng nguyên tắc; không gộp thành một box lớn.
- img_005 có người và xe chồng lấp/cắt mép: chỉ nối các phần xe khi đủ bằng chứng cùng cá thể. Không suy ra số xe từ số mũ bảo hiểm.
- Người trong cabin sau kính trong suốt vẫn là người thật nếu nhận diện được; hình phản chiếu trên kính không tạo người thứ hai.

### 3.3. Vật thật, đồ mô phỏng và phản chiếu

**R-07 — Loại vật mô phỏng:** Không gán tượng, ma-nơ-canh, ảnh in, biển quảng cáo, đồ chơi hoặc vật chỉ xuất hiện trong gương/phản chiếu. Không tạo ignore_region cho chúng chỉ vì giống lớp đích. Ví dụ: tượng người/ngựa img_017, tượng pickup img_027, ma-nơ-canh img_033, ô tô đồ chơi img_038.

Xe thật trưng bày hoặc đang được chở vẫn có thể gán. Xe độ có ngoại hình hoạt hình không tự bị loại vì lạ hình dáng. Nếu ảnh chưa đủ để xác định là phương tiện thật hay mô hình/vỏ trưng bày, xử lý theo R-11.

**R-08 — Xe chủ camera:** Không gán phần chiếc xe đang mang camera, kể cả bộ phận nhìn trực tiếp và ảnh xe chủ trong gương. Xe khác nằm ngoài gương vẫn xét theo quy tắc chung. img_020 là ca xe chủ/gương cần loại, không biến toàn bộ mặt gương thành ignore_region.

### 3.4. Vật nhỏ, đám đông và vùng bỏ qua

**R-09 — Chiều cao tối thiểu và ignore:** Đo `h = ymax - ymin` của box phần nhìn thấy trên ảnh gốc. Nếu `h >= 20 px`, xét gán cá thể theo các quy tắc khác; nếu `h < 20 px`, không gán box lớp đối tượng, khoanh ignore_region hẹp cho vùng có vật đích nhỏ. Đúng 20 px được gán; đúng 50 px thuộc nhóm ngưỡng box lớn.

Trong đám đông/bãi xe:

1. Tách và gán mọi cá thể nhận diện được, đạt ngưỡng, kể cả khi chúng nằm sát nhau.
2. Chỉ khoanh phần còn lại không thể tách chắc chắn do chồng lấp, che hoặc quá nhỏ. Không đặt một ignore lớn phủ những cá thể đã đủ điều kiện.
3. Nếu một hình chữ nhật ignore sẽ phủ cả vật cần gán, chia vùng nhỏ hơn. Nếu vẫn không tránh được, ghi vấn đề cấp ảnh để reviewer quyết, không âm thầm miễn kiểm vật rõ ràng.
4. Không tạo person/motorcycle giả định bên trong vùng chỉ có vài nét không xác định được cá thể. Nếu không chắc vùng đó có vật đích, ghi vấn đề cấp ảnh thay vì gán ignore theo phỏng đoán.

**R-10 — Nhận diện và độ mờ:** Chỉ gán khi có dấu hiệu trực quan đủ nhận ra lớp và cá thể. Bóng người/vệt đèn/khối mờ không tự thành đối tượng. Một đầu người đủ lớn vẫn có thể tạo person nếu chắc chắn là người thật; box bao đầu nhìn thấy, không suy diễn toàn thân. Người bị che nặng nhưng không phân biệt được từng cá thể xử lý theo R-09.

### 3.5. Khi cần reviewer

**R-11 — Không chắc có thể định vị:** Nếu nhận ra vật và có thể vẽ box nhưng phân lớp/thuộc tính còn nghi vấn, chọn phương án dự kiến, bật `can_review` và ghi lý do. Nếu chưa xác định được có vật đích hoặc chưa vẽ được box đáng tin cậy, ghi `image, annotator, region, note` để sau khi khóa nhãn nhóm thu vào `submission/qc/image_issues.csv`. Không tự điền mã người khác, không tạo nhãn rỗng thay cho việc chưa làm.

Trước khi gán độc lập, nhóm cần chốt các ca giáp ranh có thể đổi nghĩa quy tắc. Trong pha gán dùng đúng v1.0 đã khóa; không tự sửa quy tắc dựa vào nhãn của thành viên khác.

## 4. Ca khó theo ảnh

Bảng này ghi cách xử lý dự kiến, chưa phải nhãn đã gán. Riêng img_009, img_019 và img_024 cần xem lại với nhóm; kích thước vật nhỏ phải đo trên ảnh gốc.

| Ảnh | Tình huống và điểm v0 còn thiếu | Rule ID | Quyết định đề xuất | Lý do / cần kiểm lại |
|---|---|---|---|---|
| img_001 | Pickup và người ở gần thùng xe; v0 chưa tách hàng khỏi xe. | R-02, R-05 | Pickup thuộc truck; người thật tách person; không mở box truck theo thanh/hàng chở rời. | Căn cứ cabin/thùng; người có thể che một phần xe. |
| img_002 | Ô tô nằm trên xe chuyên chở. | R-01, R-05 | Một truck cho xe chở; mỗi ô tô thật nhận diện được là car riêng nếu đủ điều kiện. | Đang được vận chuyển không làm ô tô mất lớp; không đếm cứng số xe khi phần xa chưa rõ. |
| img_004 | Tuk-tuk ba bánh dễ bị gán motorcycle. | R-03 | Không gán tuk-tuk theo taxonomy đề xuất; người bên trong xét riêng nếu nhìn rõ. | Cần nhóm chốt phạm vi motorcycle trước pha gán. |
| img_005 | Nhiều người/xe chồng lên nhau, người cắt mép dưới ảnh, van phía sau. | R-02, R-04, R-06 | Tách từng người và xe đủ nhận diện; người bị khung cắt đặt truncated=yes; van phía sau không gộp vào xe máy. | Không suy ra toàn bộ xe bị che; kiểm liên kết bộ phận trên ảnh gốc. |
| img_006 | Hai người cùng xe bên trái; người đi xe đạp bên phải. | R-03, R-06 | Cặp trên xe máy trái: 2 person + 1 motorcycle nếu đạt ngưỡng; người xe đạp vẫn person, xe đạp không gán. | Kiểm quy tắc tách người/xe trên trường hợp khác nhau trong cùng ảnh. |
| img_009 | Xe chở khách thân dài, khó phân van/minibus với bus. | R-02, R-11 | Cần reviewer: đề xuất van nếu xác nhận kiến trúc thân van; nếu bus thì ngoài taxonomy. | Không chốt số ghế hay loại xe chỉ từ độ dài trên ảnh tổng quan. |
| img_011 | Tượng/sinh vật trang trí lớn và người thật phía xa. | R-07, R-09 | Loại vật trang trí; người thật phía xa xét riêng theo chiều cao gốc. | Không mặc định mọi hình giống người đều là person. |
| img_012 | Pickup chở thùng giấy và túi hàng. | R-02, R-05 | Truck; box theo xe nhìn thấy, không mở theo kiện hàng; kiểm truncated ở phần xe cắt biên. | Hàng rời không phải bộ phận của xe; cắt mép khác che khuất. |
| img_014 | Người rõ giữa các xe máy bị nhòe chuyển động. | R-10, R-11 | Person cho người đủ nhận diện; chỉ gán xe/người nhòe nếu nhận diện được cá thể và lớp. | Mờ không tự đồng nghĩa occluded_level=3; không suy ra nhãn từ vệt màu. |
| img_015 | Ô tô sát hai mép và phản chiếu trên mặt đường ướt. | R-04, R-07 | Gán ô tô thật, truncated=yes nếu khung cắt; không gán xe phản chiếu dưới đường. | Không tạo box trùng từ cùng một xe. |
| img_017 | Tượng người cưỡi ngựa. | R-07 | Không gán person hay phương tiện cho cụm tượng. | Hình dáng giống người không đủ; tượng là ca loại theo quy tắc. |
| img_018 | Chân dung trên biển và các ô tô sau hàng rào. | R-04, R-07, R-09 | Loại chân dung in; ô tô thật xét riêng, có mức che do hàng rào nếu nhìn đủ rõ. | Hàng rào không tự tạo ignore cho cả bãi xe. |
| img_019 | Xe vàng kiểu hoạt hình, người thật và đầu nhân vật lớn. | R-07, R-11 | Đề xuất car nếu xác nhận đây là xe thật có chức năng vận hành; loại đầu nhân vật giả; người thật vẫn person. Cần reviewer xác nhận tính chất xe. | Không loại vì hình dáng lạ; ảnh tĩnh chưa đủ chứng minh chức năng hoặc vật liệu. |
| img_020 | Gương chiếu hậu và thân xe mang camera. | R-07, R-08 | Không gán xe chủ hoặc xe chỉ thấy qua phản chiếu. | Không phải ảnh trống toàn bộ mặc định: vẫn kiểm vật đích trực tiếp ngoài gương. |
| img_021 | Đám đông người đi xe máy, vật xa rất nhỏ. | R-06, R-09 | Gán từng người/xe rõ và đạt ngưỡng; chỉ ignore phần xa không thể tách hoặc thấp hơn 20 px. | Không dùng một ignore_region bao cả dòng xe. |
| img_022 | Xe máy và người rất xa trong cảnh đơn sắc. | R-09, R-10 | Đo box nhìn thấy trên ảnh gốc; gán nếu đạt ngưỡng và rõ lớp, nếu không dùng ignore hẹp cho vật đích nhỏ. | Không quyết định nhỏ hơn 20 px chỉ từ contact sheet. |
| img_023 | Người đạp xích lô ở tiền cảnh. | R-03, R-06 | Person cho người; xích lô ngoài taxonomy; ô tô và xe máy khác xét độc lập. | Không gộp người với phương tiện ba bánh không động cơ. |
| img_024 | Vật hình xe vàng thiếu nhiều phần nằm trên wagon đen. | R-05, R-07, R-11 | Wagon đen đề xuất car; xe vàng cần reviewer xác minh xe thật chưa hoàn thiện hay vỏ/mô hình. Nếu xe thật đủ nhận diện thì gán riêng; nếu mô hình thì loại. | Bánh xe và dáng xe chưa đủ kết luận; không mặc định mọi vật chở trên xe đều thật. |
| img_026 | Hai người cùng xe máy, ảnh tối/mờ. | R-06, R-10 | Dùng cùng nguyên tắc 2 person + 1 motorcycle khi đủ nhận diện và kích thước. | Là ảnh kiểm chéo quy tắc đã dùng ở img_006; không tạo lớp rider. |
| img_027 | Bia/tượng hình pickup trong nghĩa trang. | R-07 | Loại vật hình pickup; không gán truck. | Mở ảnh gốc thấy bệ và cấu trúc tượng; ví dụ cùng hình dáng khác bản chất. |
| img_028 | Pickup thật chở tượng ngựa, ô tô đỏ phía sau. | R-02, R-05, R-07 | Pickup thuộc truck; không bao tượng ngựa trong phạm vi phần xe; car phía sau xét riêng. | Phân biệt xe thật với tượng pickup img_027; tượng ngựa không phải person hay lớp xe. |
| img_029 | Người/xe chở các thanh dài che ngang ảnh. | R-04, R-05 | Không mở box người/xe theo thanh đang chở; đánh giá che khuất riêng cho vật bị thanh chắn. | Hàng hóa không phải bộ phận thân người hoặc xe. |
| img_030 | Bãi xe máy đỗ sát và che nhau. | R-01, R-09 | Gán từng motorcycle tách được; không bỏ vì xe đang đỗ; ignore chỉ vùng còn lại không tách được. | Cần xác định đúng cá thể để không gộp nhiều xe. |
| img_032 | Đám đông phía bên kia đường, ô tô tiền cảnh cắt mép. | R-04, R-09 | Người đủ điều kiện gán riêng; vùng đông không tách được xử lý hẹp; car bị khung cắt đặt truncated=yes. | Đám đông không có nghĩa được phép bỏ mọi người. |
| img_033 | Ma-nơ-canh ở cửa hàng. | R-07 | Không gán person cho ma-nơ-canh. | Ca loại theo quy tắc; không cần đưa mọi ma-nơ-canh sang calibration. |
| img_035 | Xe ba bánh chở tải cao và người đi xe máy phía trước. | R-03, R-06 | Xe ba bánh ngoài taxonomy; người và xe máy đủ điều kiện vẫn gán riêng. | Khối hàng lớn không làm phương tiện thành truck theo định nghĩa đề xuất. |
| img_036 | Xe tải rất nhỏ có thùng kín gắn sau cabin. | R-02 | Truck, không phải van chỉ vì kích thước nhỏ. | Ranh giới dựa cấu trúc cabin/thùng. |
| img_037 | Xe van hàng thân liền; xe bus ở phía trái. | R-02, R-03 | Van cho xe tiền cảnh; bus ngoài taxonomy; người cạnh bus xét riêng. | Không gán mọi xe thân dài thành van. |
| img_038 | Các ô tô đồ chơi trong tủ. | R-07 | Không gán car/truck/van cho mô hình đồ chơi. | Không đặt ignore_region để thay quyết định loại vật giả. |
| img_040 | Người đội mũ che mặt, taxi và nhiều xe phía sau. | R-02, R-06, R-10 | Người thật vẫn person dù không thấy mặt; taxi là car; các xe nền xét che/kích thước. | Không cần nhận diện danh tính; chỉ cần nhận ra lớp người. |

### Những chỗ cần hỏi nhóm

Nên đặt các cặp ảnh sau cạnh nhau khi trao đổi:

- **img_006 và img_026:** cùng nguyên tắc tách người/xe có còn áp dụng nhất quán khi đổi góc nhìn và ánh sáng không?
- **img_027 và img_028:** dấu hiệu nào giúp phân biệt tượng hình xe với xe thật đang chở tượng, thay vì chỉ nhìn hình dáng?
- **img_021 và img_030:** khi cảnh đông, vùng nào thực sự không thể tách cá thể và vùng nào vẫn phải gán? Cần chỉ rõ ranh giới để reviewer không miễn kiểm quá rộng.

Các điểm cần chốt trước khi gán:

1. Xe đạp, tuk-tuk và xích lô có giữ ngoài taxonomy không? Nếu có, vẫn gán người trên xe theo R-06.
2. Xe ở img_009 xếp van hay loại vì là bus? Cần chỉ ra dấu hiệu phân biệt để dùng lại cho ảnh khác.
3. Nhóm có dùng các mốc che 30% và 60% trong bản này không?
4. Xe ở img_019 và vật hình xe ở img_024 là xe thật hay mô hình? Nếu ảnh chưa đủ rõ thì xem thêm nguồn ảnh.
5. Thử khoanh vùng ignore trên img_021 hoặc img_030 để kiểm tra xem các thành viên có hiểu cùng một cách không.

### Các ảnh ưu tiên khi nhận nhãn để kiểm

Danh sách này là kế hoạch rà lỗi, chưa phải kết quả QC. Chọn các ảnh sau vì mỗi ảnh giúp kiểm một điểm khác nhau của guideline.

| Ảnh | Cách kiểm dự kiến | Dấu hiệu cần ghi lại nếu thấy lỗi |
|---|---|---|
| img_021 | Xem người/xe rõ ở gần trước, sau đó kiểm ranh giới vùng ignore phía xa. | Vật đủ rõ bị vùng ignore phủ; người và xe bị gộp. |
| img_023 | Kiểm người đạp xích lô riêng với phương tiện. | Bỏ người vì xe ngoài taxonomy, hoặc gán xích lô thành motorcycle. |
| img_027 và img_028 | Đặt cạnh nhau để kiểm bản chất vật, rồi mới đọc tên lớp. | Tượng pickup bị gán truck; box xe thật mở rộng theo tượng ngựa. |
| img_029 | So cạnh box với phần người/xe, không chạy theo đầu các thanh dài. | Box quá rộng vì bao cả hàng hóa. |
| img_030 | Lần theo từng thân xe và bánh xe nhìn thấy, tránh đếm một xe hai lần. | Hai box cho cùng xe hoặc một box gộp nhiều xe. |
| img_033 và img_038 | Kiểm có box người/xe nào đặt trên vật trưng bày không. | Ma-nơ-canh hoặc ô tô đồ chơi bị gán lớp đích. |
| img_036 và img_037 | Đối chiếu cabin–thùng của truck với thân liền của van. | Phân lớp theo kích thước lớn/nhỏ thay vì kết cấu. |
| img_040 | Kiểm người đội mũ và taxi riêng; xem tiếp vật phía nền. | Bỏ người vì không thấy mặt hoặc chỉ kiểm vật lớn ở tiền cảnh. |

## 5. QC và phiên bản

### 5.1. Ngưỡng cố định lấy từ taxonomy

Không sửa mục `rules` để làm đẹp số đo.

| Trường | Giá trị | Cách áp dụng |
|---|---:|---|
| min_box_height_px | 20 | Xét chiều cao box phần nhìn thấy trên ảnh gốc. |
| match_iou | 0.5 | Ghép box 1–1 không phân biệt lớp khi so sánh. |
| large_px | 50 | Box cao từ 50 px thuộc nhóm lớn. |
| iou_thr_large | 0.85 | Ngưỡng so box lớn theo script. |
| iou_thr_small | 0.70 | Ngưỡng so box nhỏ từ 20 đến dưới 50 px. |
| iaa_iou | 0.85 | IoU trung bình trên các cặp ghép. |
| iaa_class | 0.95 | Tỉ lệ cùng lớp trên các cặp ghép. |
| error_rate_img_max | 0.02 | Tỉ lệ ảnh lỗi tối đa trong điều kiện Release. |

IAA cần đủ lượt gán trước khi tính; báo số cặp và mẫu số, ghi N/A khi không có cặp. Box chưa ghép và bất đồng ignore phải đọc riêng. Hai người cùng bỏ sót hoặc cùng phân lớp sai vẫn có thể có IAA tốt.

### 5.2. Kiểm và xử lý bất đồng

Khi đến bước QC, nên xem ảnh gốc trước để tìm vật bị bỏ sót, sau đó mới xem từng box về lớp, độ sát và thuộc tính. Nếu chỉ nhìn box có sẵn thì dễ bỏ qua vật chưa được ai gán.

Trình tự kiểm dự kiến cho một ảnh:

1. **Chưa bật box:** nhìn từ trái sang phải, ghi vị trí những người và xe đích đủ nhận diện. Chưa ghi ảnh sạch ở bước này.
2. **Bật box:** đối chiếu các vị trí vừa ghi với nhãn, rồi kiểm phần nhìn thấy và thuộc tính của từng vật.
3. **Xem lại vùng bỏ qua và mép ảnh:** đây là hai chỗ dễ bỏ sót khi chỉ tập trung vào vật lớn ở giữa ảnh.
4. **Ghi phiếu:** mỗi lỗi có ID box hoặc mô tả vùng tìm được trên ảnh. Nếu vẫn còn câu hỏi chưa giải quyết thì ghi câu hỏi, không đổi thành `khong` để hoàn tất phiếu.

Với ví dụ “thiếu người phía trái xe máy”, cần chỉ rõ người mặc gì, nằm ở vùng nào hoặc vị trí tương đối với xe. Ghi đủ để người sửa tìm đúng vật, nhất là khi một ảnh có nhiều người sát nhau.

Ghi lỗi theo thứ tự: **ảnh → vị trí/object_id → lỗi → rule ID → đề xuất sửa**. Ví dụ giả định nếu img_027 bị gán truck: “Vật hình pickup trên bệ là tượng, không phù hợp R-07; bỏ box truck.” Hiện chưa có nhãn để xác nhận lỗi này.

- Trước nộp độc lập, tự kiểm ảnh được giao, box trong biên, lớp/thuộc tính và cả ảnh không có đối tượng. Không xem nhãn của thành viên khác.
- Ca chắc chắn ngoài phạm vi theo R-03/R-07 được loại nhất quán; ca chưa rõ thực tế hoặc chưa rõ quy tắc đưa reviewer theo R-11.
- Sau khi khóa nhãn, cả nhóm so IAA và calibration; người 1 cập nhật guideline, người 3 ghi quyết định/sửa nhãn. Ca đổi nghĩa quy tắc phải rà lại cả lô, không chỉ ảnh bị cờ.
- Người 4 tổ chức QC trên nhãn cuối, reviewer nên khác người sửa. Duyệt toàn bộ 40 ảnh; phiếu mỗi vòng nằm tại `submission/qc/reviews/round-NN/qc_review.csv` do script tạo.
- Script kiểm định dạng và số đo; reviewer cần đọc ảnh để phát hiện bỏ sót chung, nhãn giả, box không sát và áp dụng sai phạm vi.
- Hold khi thiếu bằng chứng, có ca chưa chốt hoặc mới chỉ lấy mẫu; Rework khi ảnh lỗi vượt 2% hoặc lỗi lặp theo script; Release khi bằng chứng đầy đủ và reviewer xác nhận. Với 40 ảnh, một ảnh lỗi là 2,5%, vượt ngưỡng.
- Báo riêng ảnh lỗi/ảnh đã duyệt, annotation lỗi/annotation đã duyệt và số vật bỏ sót. Không điền `khong` trước khi xem ảnh hoặc tự sinh số liệu QC.

### 5.3. Lịch sử phiên bản

| Phiên bản | Thay đổi | Cơ sở / trạng thái |
|---|---|---|
| v0 (giảng viên) | Lớp và quy tắc khởi đầu còn ngắn, chưa có ca khó. | Giữ nguyên file nguồn. |
| v0.1-draft (bản này) | Đề xuất phạm vi lớp, ngưỡng che, phần nhìn thấy, tách người/xe, vật mô phỏng, vật nhỏ, reviewer và ca theo ID ảnh. | Soạn với AI từ bộ ảnh; chờ người 4 kiểm lại và buổi thống nhất. |

