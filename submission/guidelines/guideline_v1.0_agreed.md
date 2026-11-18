# Guideline gán nhãn — v1.0 agreed

- Phiên bản: `v1.0`
- Ngày: 2026-11-16
- Cơ sở tổng hợp: `guideline_101.md` đến `guideline_105.md` (Pha 1)
- Phạm vi: phát hiện người và phương tiện đường bộ trong bộ 40 ảnh `img_001.jpg`–`img_040.jpg`
- Công cụ / định dạng: CVAT, bounding box, COCO 1.0
- Taxonomy áp dụng: [`submission/taxonomy.json`](../taxonomy.json), phiên bản `v1.0`

## 1. Mục tiêu và nguyên tắc

Gán người thật và phương tiện thuộc taxonomy có mặt trong ảnh. Mỗi vật thể được nhận diện và đạt ngưỡng kích thước có một box riêng, thuộc đúng một lớp. Box ôm sát phần nhìn thấy, không bao phần khuất được suy đoán, nền rộng, bóng, hay hàng hóa rời.

Hai lỗi cần tránh là bỏ sót người/phương tiện thật và gán nhầm vật không thật thành người/phương tiện. Mức che, cắt mép và cờ xem lại là thuộc tính phục vụ lọc/QC, không phải lớp.

## 2. Taxonomy: lớp và ranh giới

Mỗi đối tượng chỉ có một lớp. Dùng các định nghĩa dưới đây và cùng thứ tự phân loại ở mục 2.2.

| Lớp | Định nghĩa | Bao gồm / dễ nhầm |
|---|---|---|
| `person` | Người thật; mỗi cá nhân một box. | Người đi bộ, đứng/ngồi cạnh xe, lái hoặc ngồi trên bất kỳ phương tiện nào; người trong cabin nếu phần thấy được đủ nhận ra. Không gồm tượng, ma-nơ-canh, mascot, hình in/vẽ. |
| `bicycle` | Xe đạp hai bánh chạy bằng sức người, nhận ra khung và bàn đạp. | Gồm xe đạp chở hàng/giỏ. Không gồm xe máy, xích lô hoặc xe đẩy. Người đạp là một `person` riêng. |
| `motorcycle` | Xe hai bánh có động cơ, gồm xe số, mô tô, scooter và xe tay ga. | Sidecar gắn cố định được tính cùng xe; vẽ một box ôm xe và sidecar. Người trên xe vẫn có box `person` riêng. |
| `car` | Ô tô chở người có thân liền khối. | Sedan, hatchback, wagon, SUV, MPV, taxi, xe cổ và ô tô cá nhân; không gồm pickup, van hoặc bus. |
| `van` | Xe kín cỡ nhỏ/vừa, cabin và khoang chở liền khối. | Hiace, van taxi/giao hàng. Minibus có thân dài và dãy cửa sổ hành khách là `bus`. |
| `truck` | Xe có cabin và khoang hàng tách nhau. | Xe tải, bán tải/pickup (kể cả có canopy/nắp thùng/bạt), xe ben, đầu kéo và xe chở ô tô. Không tạo lớp `container`: xe đầu kéo hoặc xe kéo container/car-carrier là `truck`. |
| `bus` | Xe buýt, xe khách hoặc minibus có thân chở khách dài hay dãy cửa sổ hành khách. | Xe buýt nhìn từ phía sau vẫn là `bus`; Hiace/van ngắn không có cấu trúc xe khách dài là `van`. |
| `three_wheeler` | Phương tiện ba bánh chở người/hàng. | Tuk-tuk, auto-rickshaw và xích lô đạp/xích lô máy. Không gồm xe máy hai bánh có sidecar. Người điều khiển là `person` riêng. |
| `ignore_region` | Vùng chứa đối tượng thuộc các lớp trên nhưng không thể tách/định vị riêng đáng tin cậy. | Là vùng để bỏ qua khi QC, không phải một đối tượng. Không dùng cho vật ngoài taxonomy, hình in, tượng, phản chiếu, hoặc một vật đơn lẻ chỉ vì nhỏ. |

### 2.1. Vật ngoài phạm vi

Không gán lớp cho xe đạp điện/xe đồ chơi nếu không thể xác định là xe thuộc lớp nào; xích lô nếu ba bánh được xếp `three_wheeler`; xe đẩy, xe thô sơ không có trong taxonomy, thuyền, động vật, hàng hóa, biển hiệu, đồ trang trí. Người đạp hoặc đẩy vẫn gán `person` nếu đạt điều kiện. Vật ngoài phạm vi không được đưa vào `ignore_region`.

Không gán tượng, tượng sáp, ma-nơ-canh, búp bê/thú bông, mascot, nhân vật vẽ, người/xe in trên poster, màn hình, biển quảng cáo, xe mô hình, vật trưng bày không phải phương tiện thật, phản chiếu trong gương/kính/mặt nước, bóng đổ, hoặc phần thân/gương của xe đang chụp ảnh (ego vehicle).

Xe thật đang đỗ, trong gara/bãi xe, trên xe chở, hoặc trong diễu hành vẫn được gán nếu nhận diện được là phương tiện thật và thuộc taxonomy. Xe diễu hành có khả năng tự chạy được gán theo loại xe; mascot/trang trí gắn trên xe không gán.

### 2.2. Thứ tự phân lớp phương tiện

Khi phân vân, dùng lần lượt và dừng ở lớp đầu tiên phù hợp:

1. Là hình ảnh, tượng, mô hình, đồ chơi, phản chiếu hoặc không phải phương tiện thật → không gán.
2. Ba bánh, không phải sidecar gắn với xe máy → `three_wheeler`.
3. Xe hai bánh có động cơ, kể cả sidecar → `motorcycle`.
4. Xe khách thân dài/dãy cửa sổ hành khách → `bus`.
5. Cabin và khoang hàng tách nhau → `truck`.
6. Thân kín liền cabin, cỡ nhỏ/vừa → `van`.
7. Ô tô chở người còn lại → `car`.
8. Xe đạp có bàn đạp và không động cơ → `bicycle`.

## 3. Thuộc tính

Chỉ dùng đúng thuộc tính và giá trị đã khai báo trong taxonomy. Gán trên từng box vật thể; `ignore_region` để mặc định.

| Thuộc tính | Giá trị / cách áp dụng |
|---|---|
| `occluded_level` | Tỷ lệ diện tích toàn vật bị vật khác che; không tính phần nằm ngoài khung ảnh. `0`: dưới 10%; `1`: từ 10% đến dưới 40%; `2`: từ 40% đến dưới 70%; `3`: từ 70% trở lên nhưng vẫn nhận ra chắc chắn lớp. Nếu không nhận ra chắc lớp thì không tạo box lớp. |
| `truncated` | `no` nếu vật nằm trọn trong ảnh; `yes` nếu vật thật tiếp tục ra ngoài bất kỳ mép ảnh nào. Box chỉ nằm trong khung ảnh. Cắt mép không tính là che khuất; nếu vừa bị che vừa cắt mép thì điền cả hai thuộc tính. |
| `can_review` | Tick trên box đã tạo khi còn nghi vấn thực sự về lớp, ranh giới box hoặc thuộc tính; ghi ảnh/vùng/lý do trong ghi chú. Nếu chưa chắc có vật hoặc chưa đủ cơ sở tạo box, không vẽ box phỏng đoán; ghi vấn đề cấp ảnh. Ca đã có quyết định rõ trong guideline thì không tick. |

Các mức che được ước lượng nhất quán; không dùng cờ `occluded` riêng của CVAT thay cho `occluded_level`. Mũ bảo hiểm được tính là phần người khi người đang đội mũ; không bao cả xe vào box người.

## 4. Quy tắc gán box

**R-01 — Một vật, một box, một lớp.** Box chữ nhật song song cạnh ảnh, ôm sát phần nhìn thấy. Không gộp người/xe khác nhau và không gộp người với phương tiện.

**R-02 — Người trên phương tiện.** Tạo một box phương tiện và một box `person` cho mỗi người nhận diện được, kể cả người ngồi sau. Box được phép chồng nhau tại điểm tiếp xúc. Box `person` không gồm bánh/thân xe; box phương tiện không kéo lên đầu người. Người trong cabin chỉ gán khi thấy đủ dấu hiệu để nhận ra là người.

**R-03 — Che khuất.** Vẽ phần nhìn thấy, không ước lượng/nội suy phần nằm sau vật khác. Đối tượng bị che vẫn được gán nếu phần còn lại nhận diện chắc lớp và cao tối thiểu 20 px. Ghi `occluded_level` theo mục 3. Quy tắc áp dụng cho cả người và phương tiện; không có ngưỡng loại riêng theo lớp.

**R-04 — Cắt mép ảnh.** Gán nếu phần còn trong ảnh đủ nhận diện và đạt ngưỡng chiều cao. Box dừng ở mép ảnh, đặt `truncated=yes` khi vật tiếp tục ra ngoài ảnh. Không vẽ phần ngoài ảnh dù có thể suy đoán hình dạng.

**R-05 — Ngưỡng kích thước.** Dùng `min_box_height_px = 20` trên phần nhìn thấy ở ảnh gốc. Vật thuộc taxonomy thấp hơn 20 px không có box lớp riêng. Không bỏ qua vật đạt 20 px chỉ vì ở xa nếu vẫn nhận diện chắc lớp.

**R-06 — `ignore_region` và đám đông.** Khi nhiều người/phương tiện mục tiêu chồng dày, quá nhỏ hoặc mờ đến mức không thể định vị riêng, vẽ một vùng bao đúng phần không thể tách và gán `ignore_region`. Vật đủ lớn, tách được ở rìa/tiền cảnh vẫn có box riêng. Không gộp box lớp thường vào vùng ignore. Không dùng ignore cho một vật đơn lẻ dưới 20 px, tượng, hình in, phản chiếu hay vật ngoài taxonomy.

**R-07 — Box xe và hàng hóa.** Box xe ôm các bộ phận của chính phương tiện; không kéo theo ống, bao tải, thùng hàng rời, cuộn dây, trái cây hoặc vật nhô ra. Nếu hàng che xe, vẽ phần xe thấy được và đánh mức che nếu phù hợp.

**R-08 — Xe chở xe.** Một `truck` bao cabin/đầu kéo và khung chở thuộc cùng xe. Mỗi ô tô thật được chở, nếu nhận ra được và cao tối thiểu 20 px, có box `car` riêng; box lồng nhau được phép. Xe máy/xe khác được chở chỉ gán nếu nhận diện chắc thuộc lớp đã khai báo và đạt ngưỡng.

**R-09 — Tuk-tuk, xích lô, sidecar.** Tuk-tuk/auto-rickshaw và xích lô ba bánh là `three_wheeler`. Xe máy hai bánh gắn sidecar là một `motorcycle`, không phải `three_wheeler`. Người lái/người chở là `person` riêng nếu nhận diện và đạt ngưỡng.

**R-10 — Vật không thật và phản chiếu.** Không vẽ box lớp hoặc `ignore_region` cho tượng, ma-nơ-canh, ảnh in, mô hình, mascot, phản chiếu, bóng hoặc xe chủ. Nếu vật thật nằm cạnh chúng, vẫn gán vật thật theo quy tắc thông thường.

**R-11 — Mờ, thiếu sáng, mưa.** Tối hoặc mưa không tự động loại đối tượng. Nếu người/phương tiện còn nhận diện chắc chắn và đạt 20 px, tạo box; tick `can_review` khi ranh giới/lớp còn mơ hồ. Vệt sáng/bóng phản chiếu không phải phương tiện. Nếu một dải mục tiêu có nhiều vật không thể tách, dùng `ignore_region`; nếu chỉ là nền mờ thì không gán gì.

**R-12 — Không chắc chắn.** Không dùng `can_review` để hợp thức hóa box đoán. Tick trên box có cơ sở nhưng còn tranh chấp; nếu chưa biết có đối tượng hay không, ghi issue cấp ảnh gồm mã ảnh, vùng, điều chưa rõ và lý do. Các quyết định đã có trong mục 6 không cần review lại.

## 5. Quy tắc phân loại các ranh giới thường gặp

| Tình huống | Quyết định |
|---|---|
| Pickup/bán tải, kể cả Suzuki nhỏ, pickup lớn, thùng bạt hoặc canopy | `truck`, vì cabin tách khỏi khoang hàng. |
| Xe kín liền khối kiểu Hiace/van taxi | `van`. |
| Minibus/xe khách có dãy cửa sổ hành khách, thân dài | `bus`. |
| Container hoặc xe chở ô tô nhiều tầng | Xe kéo là `truck`; không có lớp `container`; từng ô tô nhìn thấy là `car`. |
| Tuk-tuk/auto-rickshaw | `three_wheeler`. |
| Xích lô ba bánh | `three_wheeler`; người đạp là `person`. |
| Xe máy có sidecar | Một `motorcycle` gồm sidecar; người lái là `person` riêng. |
| Xe đạp có bàn đạp | `bicycle`; người đạp là `person` riêng. |
| Người ngồi trên xe máy | Một `person` cho mỗi người và một `motorcycle`; không gom thành một box. |
| Ô tô thật nằm trên giá chở xe | Một `car` riêng nếu đủ ngưỡng; không coi là hàng hóa. |
| Xe thật đậu trong gara/bảo tàng | Gán lớp xe nếu là phương tiện thật; không gán xe mô hình/trang trí. |

## 6. Ca tham chiếu trong bộ ảnh

Các quyết định này áp dụng quy tắc chung cho những ví dụ được nêu trong năm bản cá nhân. Không liệt kê mọi box của ảnh; chỉ chốt tình huống có thể gây bất đồng.

| Ảnh | Quyết định v1.0 |
|---|---|
| `img_001` | Bán tải là `truck`; người thật là `person`; đặt `truncated=yes` cho vật bị mép ảnh cắt. |
| `img_002` | Đầu kéo và sàn chở là một `truck`; ô tô nhìn thấy trên sàn là các `car` riêng; người nhìn thấy là `person`. |
| `img_003` | Xe đạp là `bicycle`, xe máy là `motorcycle`, người là `person`; hàng/quang gánh không gán. |
| `img_004` | Hai tuk-tuk là hai `three_wheeler`; tài xế nhìn rõ là `person`. |
| `img_005`–`img_006` | Tách mỗi người trên xe máy thành `person`, mỗi xe thành `motorcycle`; ở `img_006` xe đạp là `bicycle`. |
| `img_007`–`img_008` | Bán tải/xe tải là `truck`; xe máy tách được gán riêng; tuk-tuk xa là `three_wheeler` nếu nhận diện được và đạt 20 px. |
| `img_009` | Minibus là `bus`; khách qua kính là `person` nếu nhận diện đủ chắc; xe máy/người ngoài xe gán riêng. |
| `img_010` | Xe ga là `motorcycle`, xe đạp là `bicycle`, mỗi người là `person`; hàng hóa không gán. |
| `img_011` | Tượng Predator không phải `person`; xe độ còn nhận diện là xe máy thì `motorcycle`; đám đông không tách được là `ignore_region`. |
| `img_012` | Pickup là `truck`, SUV/ô tô là `car`; thùng carton/túi không gán và không kéo dài box xe. |
| `img_013`–`img_015` | Gán người/xe thật đủ rõ; không gán tượng, bóng hoặc phản chiếu; dải xe mờ không tách được dùng `ignore_region`. |
| `img_016` | Tuk-tuk là `three_wheeler`; van taxi là `van`; xe tay ga là `motorcycle`; người và hàng hóa xử lý riêng. |
| `img_017` | Tượng người cưỡi ngựa và chim: không gán box, không tạo ignore. |
| `img_018` | Chân dung trên biển không gán; ô tô thật sau hàng rào gán `car`, mức che theo tỷ lệ thực tế. |
| `img_019` | Xe diễu hành có khả năng chạy là `car`; tài xế và người thật tách riêng; mascot không gán; đám đông không tách được là `ignore_region`. |
| `img_020` | Xe chủ/gương và cảnh phản chiếu: không gán. |
| `img_021` | Xe máy/người phía trước tách được gán riêng; xe bus cuối đường là `bus` nếu nhận ra và đạt ngưỡng; cụm xa không tách được là `ignore_region`. |
| `img_022` | Xe máy sidecar là một `motorcycle`; người lái là `person` nếu đạt ngưỡng. |
| `img_023` | Xích lô ba bánh là `three_wheeler`; người đạp là `person`; xe đạp khác là `bicycle`; poster không gán. |
| `img_024` | Xe thật trong gara và ô tô thật được chở đều là `car`; xe mô hình/trang trí hoặc phản chiếu không gán. |
| `img_025`–`img_026` | Người/xe đủ rõ gán riêng; sidecar thuộc `motorcycle`; hai người trên một xe máy là hai `person` và một `motorcycle`; tranh tường không gán. |
| `img_027` | Pickup tượng trên bệ: không gán. |
| `img_028` | Pickup thật là `truck`; ngựa tượng trên thùng không gán; ô tô phía sau là `car`. |
| `img_029` | Scooter là `motorcycle`, xe đạp là `bicycle`, người là `person`; ống thép không gán và không thuộc box xe. |
| `img_030` | Xe máy tách được gán riêng; phần bãi xe dày không tách được là `ignore_region`; poster không gán. |
| `img_031` | Xe buýt là `bus`; các xe/người khác gán theo lớp nếu nhận diện và đạt ngưỡng; phản chiếu nền ướt và hình vẽ không gán. |
| `img_032` | Người tách được gán riêng; ô tô cắt mép là `car` + `truncated=yes`; van là `van`; ảnh in trên bảng không gán. |
| `img_033` | Ma-nơ-canh, ảnh người và phản chiếu: không gán, không tạo ignore. |
| `img_034` | Xe đạp là `bicycle`, xe máy là `motorcycle`, ô tô là `car`, người là `person`; người/xe cắt mép đặt `truncated=yes`. |
| `img_035` | Auto-rickshaw là `three_wheeler`; bao tải không kéo dài box; xe máy/người/ô tô gán riêng. |
| `img_036`–`img_037` | Xe thùng bạt/pickup canopy là `truck`; xe buýt là `bus`; xe máy/người tách riêng; poster không gán. |
| `img_038` | Xe mô hình, đồ chơi, búp bê/thú bông và phản chiếu: không gán. |
| `img_039` | Xe máy, xe đạp và người đủ ngưỡng gán theo lớp; cụm cuối phố dưới ngưỡng/không tách được dùng `ignore_region`. |
| `img_040` | Taxi/SUV là `car`, tuk-tuk là `three_wheeler`, xe buýt là `bus`, xe máy/người bị cắt mép đặt truncated; hình dán/ảnh phản chiếu không gán. |

## 7. Quy trình QC và phiên bản

Các ngưỡng số của QC lấy từ `submission/taxonomy.json` và được giữ nguyên trong v1.0: chiều cao box tối thiểu 20 px; ngưỡng IoU box lớn/nhỏ; ngưỡng ghép; IAA; tỷ lệ lỗi tối đa theo ảnh. Không tự thay đổi chúng khi gán.

QC tối thiểu cho mỗi lượt:

1. Đủ 40 ảnh trong dữ liệu COCO, kể cả ảnh không có box.
2. Mọi lớp và thuộc tính đúng tên/giá trị trong taxonomy.
3. Mỗi box lớp khớp một vật; box chỉ phủ phần nhìn thấy và không gồm người/xe khác hoặc hàng hóa rời.
4. `ignore_region` chỉ phủ phần cụm mục tiêu không thể tách; không che các box mục tiêu đã gán riêng.
5. Xem lại mọi box có `can_review`, mọi vùng ignore và mọi issue cấp ảnh.
6. Ghi mẫu số khi báo cáo IAA; nếu quy tắc gán thay đổi sau khi khóa nhãn, ghi phiên bản mới và rà lại toàn bộ ảnh chịu ảnh hưởng.

Trong lượt gán độc lập, annotator tự quyết theo v1.0, không phối hợp để làm giống nhãn người khác. Ca chưa giải quyết được ghi mã ảnh, vùng, lý do; nhóm chốt trong calibration và cập nhật guideline phiên bản kế tiếp.

## 8. Lịch sử phiên bản và quyết định tổng hợp

| Phiên bản | Nội dung |
|---|---|
| `v0` | Taxonomy khởi đầu còn thiếu ranh giới `bus`, xe ba bánh và các ca khó. |
| `v1.0` | Tổng hợp năm guideline cá nhân; bổ sung/định nghĩa `bicycle`, `bus`, `three_wheeler`; chốt pickup=`truck`, Hiace=`van`, minibus=`bus`, sidecar thuộc `motorcycle`, car-carrier=`truck` cộng từng `car`; thống nhất box người/xe, hàng hóa, vật giả/ảnh phản chiếu, vật nhỏ, đám đông, che khuất, cắt mép và quy trình review. |

### Cách xử lý các đề xuất khác nhau giữa năm bản

- Dùng lớp `bicycle` theo đề xuất và ví dụ cụ thể trong bản 103 để gán nhất quán xe đạp xuất hiện trong bộ ảnh; không ép xe đạp vào `motorcycle`.
- Dùng lớp tổng quát `three_wheeler` để bao phủ tuk-tuk/auto-rickshaw và xích lô ba bánh; không tách riêng `tuk_tuk` và không ép chúng vào `motorcycle`/`truck`.
- Không tạo lớp `container`: container/car-carrier là cấu hình của `truck`; ô tô được chở vẫn là `car` riêng.
- Chọn ngưỡng kích thước taxonomy 20 px thay cho đề xuất 10 px; chỉ dùng `ignore_region` cho cụm mục tiêu không tách được, không phải vật đơn lẻ ngoài ngưỡng.
- Chốt các mốc che 10% / 40% / 70%; `truncated=yes` khi có bất kỳ phần vật nào ra ngoài mép ảnh. Hai thuộc tính biểu thị hai hiện tượng khác nhau.
- Khi guideline cá nhân mâu thuẫn về nội suy box, áp dụng thống nhất: luôn box phần nhìn thấy, không vẽ phần khuất hoặc phần ngoài ảnh.
