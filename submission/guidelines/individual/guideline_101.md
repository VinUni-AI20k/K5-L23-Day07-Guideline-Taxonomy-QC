# Guideline gán nhãn — v0.1-indiv — Thành viên 101

- **Phiên bản:** v0.1-indiv
- **Ngày:** 2026-11-16
- **Người viết:** Thành viên 101
- **Đối tượng áp dụng:** Bộ dữ liệu 40 ảnh giao thông đường phố hỗn hợp

---

## 1. Mục tiêu

- Mục đích mô hình: Huấn luyện mô hình phát hiện đối tượng 2D phục vụ bài toán giám sát giao thông thông minh và hỗ trợ lái xe tự động trong điều kiện đường phố đô thị phức hợp.
- Rủi ro an toàn và hậu quả khi gán sai:
  - *Bỏ sót:* Bỏ sót người đi bộ (`person`) hoặc phương tiện đang lưu thông (`motorcycle`, `car`, `truck`) là lỗi nghiêm trọng nhất, có thể dẫn đến quyết định không phanh và va chạm chết người trực tiếp trong xe tự lái.
  - *Dương tính giả với vật tĩnh/ảo (False Positive):* Gán nhầm tượng đài, hình người in trên biển quảng cáo, ma-nơ-canh hoặc bóng xe phản chiếu qua gương chiếu hậu sẽ khiến hệ thống nhận dạng nhầm là vật thể thật đang cản đường, gây hiện tượng phanh gấp ảo dẫn đến tai nạn dồn toa từ phía sau.
  - *Sai lệch kích thước / ranh giới:* Ôm cả hàng hóa cồng kềnh ngoài phạm vi hoặc gộp chung xe chở xe thành một khối duy nhất sẽ làm mô hình ước tính sai khoảng cách an toàn và khổ rộng vật thể, gây va quệt khi chuyển làn.

---

## 2. Lớp và thuộc tính

### 2.1. Phân loại lớp đối tượng (`classes`)

| Lớp | Định nghĩa | Ví dụ thực tế trong dữ liệu | Phản ví dụ / Dễ nhầm lẫn |
|---|---|---|---|
| `car` | Phương tiện cơ giới chở người từ 4 đến 9 chỗ ngồi (sedan, hatchback, SUV, crossover, taxi). | Ô tô con trên phố; xe taxi ở `img_040.jpg`; xe wagon AMC Pacer ở `img_024.jpg`. | Xe bán tải pickup (`truck`), xe van thùng kín (`van`), xe mô hình đồ chơi trong tủ kính (`img_038.jpg` - **không gán**), xe diễu hành gắn tượng hoạt hình (`img_019.jpg` - gắn cờ review). |
| `truck` | Phương tiện cơ giới chuyên dụng chở hàng hóa có khoang cabin tách rời với thùng/sàn chở phía sau, bao gồm cả xe bán tải (pickup truck). | Xe chở ô tô ở `img_002.jpg`; xe bán tải ở `img_001.jpg`, `img_012.jpg`, `img_028.jpg`; xe tải nhẹ CMC Veryca ở `img_036.jpg`. | Tượng đá hình xe bán tải ở nghĩa trang (`img_027.jpg` - **không gán**); xe van thùng kín liền khối (`van`). |
| `van` | Phương tiện cơ giới chở hàng hoặc chở khách (9-16 chỗ) có thiết kế thùng kín liền một khối từ cabin đến đuôi xe, không có sàn thùng tách rời. | Minivan chở khách; xe cứu thương; xe van chuyển phát hàng liền khối. | Xe bán tải gắn nắp thùng cao Master 75 ở `img_037.jpg` (về bản chất là xe pickup/`truck` gắn nắp thùng phụ kiện); xe buýt cỡ lớn (`bus`). |
| `motorcycle` | Phương tiện cơ giới 2 bánh hoặc 3 bánh có gắn động cơ (xe máy số, xe tay ga, xe mô tô phân khối lớn, mô tô gắn thùng phụ sidecar, xe tuk-tuk, xe auto rickshaw). | Xe máy lưu thông trên đường ở `img_005.jpg`, `img_008.jpg`, `img_014.jpg`, `img_026.jpg`; mô tô có thuyền phụ sidecar ở `img_022.jpg`. | Xe đạp chở hàng không động cơ (`img_003.jpg`, `img_010.jpg` - **không gán**); xe xích lô đạp chân (`img_006.jpg`, `img_023.jpg`, `img_034.jpg`, `img_039.jpg` - **không gán**). |
| `person` | Cơ thể con người thật còn sống (người đi bộ, người đứng/ngồi bên đường, người đang điều khiển hoặc ngồi sau phương tiện). | Người đứng ở `img_001.jpg`; người đi bộ ở `img_014.jpg`, `img_025.jpg`; người lái và người ngồi sau xe máy ở `img_005.jpg`, `img_026.jpg`. | Tượng đồng người cưỡi ngựa (`img_017.jpg` - **không gán**); ảnh chân dung trên billboard (`img_018.jpg` - **không gán**); ma-nơ-canh tủ kính (`img_033.jpg` - **không gán**); tượng Predator (`img_011.jpg` - **không gán**); búp bê đồ chơi (`img_038.jpg` - **không gán**). |
| `ignore_region` | Vùng đánh dấu không gian không yêu cầu gán chi tiết từng vật (đám đông quá dày đặc ở xa, cụm xe mờ nhòe hậu cảnh cao < 20 px). | Khu vực người đi bộ quá xa ở bờ biển `img_025.jpg`; cụm xe ở hậu cảnh xa tít `img_031.jpg`. Bỏ sót vật trong vùng này **không bị tính là lỗi QC**. | Vật thể ở cự ly gần hoặc nhìn rõ từng cá thể riêng biệt. |
| `bus` | Xe buýt. | `img_009.jpg`, `img_031.jpg`, `img_032.jpg`, `img_037.jpg`, `img_040.jpg`. | Vật thể ở cự ly gần hoặc nhìn rõ từng cá thể riêng biệt. | Vì xe lớn ít bị nhầm lẫn|
| `biclecal` | Xe thô sơ không có động cơ, xe đạp, xe xích lô chở khách. | |Nếu gặp xe và người thì gán phương tiện và người riêng |

---

### 2.2. Quy định thuộc tính đối tượng (`attributes`)

Mọi thuộc tính đều được định lượng bằng ngưỡng phần trăm đo được rõ ràng:

1. **`occluded_level` (Mức độ che khuất):**
   - **`0` - Không bị che:** 0% diện tích vật thể bị che bởi vật khác (nhìn thấy trọn vẹn toàn bộ đường viền).
   - **`1` - Che khuất nhẹ:** Từ **1% đến 30%** diện tích vật thể bị che khuất bởi vật khác.
   - **`2` - Che khuất trung bình/nặng:** Từ **31% đến 70%** diện tích vật thể bị che khuất.
   - **`3` - Che khuất cực nặng:** Trên **70%** diện tích bị che khuất nhưng con người vẫn nhận dạng chắc chắn được vật thể dựa vào các dấu hiệu đặc trưng (ví dụ: thấy 1 phần bánh xe + đèn pha, hoặc mũ bảo hiểm + vai).
   - *Ngưỡng loại bỏ:* Nếu vật thể bị che khuất trên **90%** và không đủ căn cứ nhận diện chắc chắn $\rightarrow$ **Không gán box**.

2. **`truncated` (Cắt mép ảnh):**
   - **`no`:** Toàn bộ vật thể nằm trọn vẹn trong biên ảnh (0% bị cắt mép).
   - **`yes`:** Vật thể bị cắt bởi ít nhất một mép ảnh (biên trên, dưới, trái, phải).

---

## 3. Quy tắc vẽ Bounding Box

1. **Nguyên tắc ôm sát phần nhìn thấy:**
   - Box chỉ ôm sát các pixel thực tế nhìn thấy được của vật thể.
   - Tuyệt đối không phỏng đoán phần bị che khuất để vẽ box rộng ra .
2. **Quy tắc gán Người và Xe máy (`person` & `motorcycle`):**
   - **Tách làm 2 box độc lập:**
     - 1 box `person`: Ôm trọn từ đỉnh mũ bảo hiểm / đầu người xuống đến phần thân/chân nhìn thấy được trên xe. Đặt `occluded_level = 1` hoặc `2` tùy mức bị đầu/yên xe che.
     - 1 box `motorcycle`: Ôm trọn khung xe máy, bánh xe, đầu xe và gương xe nhìn thấy được. Đặt `occluded_level = 1` hoặc `2` do bị người ngồi trên xe che một phần thân.
   - **Nhiều người trên cùng 1 xe (`img_026.jpg`):** Gán từng box `person` riêng cho từng người (người lái và người ngồi sau), và 1 box `motorcycle` chung cho chiếc xe.
3. **Quy tắc Xe chuyên dụng chở ô tô (`img_002.jpg`):**
   - Gán 1 box `truck` lớn bao trùm toàn bộ xe tải chở hàng (bao gồm cabin và sàn chuyên dụng).
   - Gán bổ sung từng box `car` riêng biệt cho mỗi chiếc ô tô con được chở trên cả 2 tầng sàn nếu nhìn thấy rõ.
4. **Quy tắc Hàng hóa trên phương tiện (`img_012.jpg`, `img_029.jpg`, `img_035.jpg`):**
   - *Hàng hóa trong thùng xe bán tải (`img_012.jpg`):* Box `truck` ôm theo thân xe và thành thùng; nếu hàng hóa cao hơn cabin nhưng là hàng rời nhỏ thì box chỉ ôm trọn mép trên cabin và thành xe.
   - *Hàng hóa cồng kềnh, quá khổ trên xe máy/tuk-tuk (`img_029.jpg`, `img_035.jpg`):* Box phương tiện chỉ ôm phần kết cấu cơ giới của xe (bánh xe, khung xe, kính chắn gió). Không kéo box phương tiện phình to để ôm trọn cả khối xốp/bao tải khổng lồ phía trên.
5. **Quy tắc Loại trừ đối tượng giả lập / Phi sinh học :**
   - **Tượng điêu khắc / Tượng đài (`img_017.jpg`, `img_027.jpg`):** Không gán `person` cho tượng người cưỡi ngựa bằng đồng; không gán `truck`/`car` cho khối đá điêu khắc hình xe bán tải ở nghĩa trang.
   - **Ảnh in 2D / Biển quảng cáo (`img_018.jpg`):** Không gán `person` cho hình ảnh chính khách in trên billboard tấm lớn.
   - **Ma-nơ-canh & Búp bê (`img_033.jpg`, `img_038.jpg`):** Không gán `person` cho ma-nơ-canh trưng bày quần áo hoặc búp bê đồ chơi.
   - **Mô hình / Đồ chơi thu nhỏ (`img_038.jpg`):** Không gán `car` cho xe ô tô đồ chơi trong tủ kính.
   - **Hình phản chiếu qua gương (`img_020.jpg`):** Không gán box cho ảnh ảo phản chiếu qua gương chiếu hậu xe ô tô.
   - **Tượng trang trí gắn trên xe (`img_028.jpg`):** Xe bán tải chở tượng ngựa "yorse" $\rightarrow$ gán box `truck` cho xe bán tải; tượng ngựa xem là hàng hóa tĩnh, không gán nhãn.
   - **Thân vỏ xe gắn trên nóc xe (`img_024.jpg`):** Chỉ gán 1 box `car` cho xe đang hoạt động bên dưới; khung vỏ xe gắn trên giá nóc là hàng hóa/phế liệu, không gán thêm `car`.
6. **Quy tắc Ngưỡng kích thước tối thiểu & Đám đông:**
   - **Ngưỡng kích thước:** Bỏ qua không gán các đối tượng có chiều cao $< 20\text{ px}$ (theo tiêu chuẩn `min_box_height_px = 20` trong `taxonomy.json`).
   - **Đám đông dày đặc:** Nếu người hoặc xe ở xa dính chùm không thể tách bạch box riêng lẻ $\rightarrow$ gom thành một vùng `ignore_region`.

---

## 4. Bảng phân tích Ca khó trong 40 ảnh

Bảng phân tích các tình huống biên cụ thể được phát hiện khi khảo sát 40 ảnh thực tế:

| Ảnh | Tình huống phát hiện | Rule ID đề xuất | Quyết định cá nhân | Lý do |
|---|---|---|---|---|
| `img_001.jpg` | Xe bán tải cũ chở hàng đỗ trước quán ăn | `R-TRUCK-01` | Gán `truck` cho xe bán tải; gán `person` cho người phụ nữ đứng cạnh. | Xe bán tải có khoang cabin tách rời thùng chở hàng sau $\rightarrow$ thuộc `truck`. |
| `img_002.jpg` | Xe tải chuyên dụng chở 8 ô tô con trên hai tầng | `R-CARRIER-01` | Gán 1 box `truck` bao toàn bộ xe tải chở; gán thêm 8 box `car` cho từng ô tô trên sàn. | Mô hình xe tự lái cần nhận biết chướng ngại vật ô tô con để tránh va chạm. |
| `img_003.jpg` | Người phụ nữ đẩy xe đạp chở giỏ mít to | `R-NONMOTOR-01` | Gán 1 box `person` cho người phụ nữ; **không gán** box cho xe đạp. | Taxonomy v0 chỉ định nghĩa phương tiện cơ giới (`motorcycle`), không gán xe đạp thô sơ. |
| `img_004.jpg` | 2 xe tuk-tuk 3 bánh màu xanh đỗ trên vỉa hè | `R-TUKTUK-01` | Tạm gán `motorcycle`, tick `can_review = true`. Đề xuất nhóm thêm lớp `tuk_tuk`. | Phương tiện 3 bánh có động cơ, không khớp hoàn toàn 4 lớp xe cơ giới v0. |
| `img_005.jpg` | Dòng người đi xe máy dày đặc ở TP.HCM | `R-MOTO-RIDER-01` | Tách riêng box `person` và box `motorcycle` cho từng cặp; đặt `occluded_level = 1` hoặc `2`. | Đảm bảo mô hình học được cả đặc trưng người lái lẫn phương tiện. |
| `img_006.jpg` | Đoàn xích lô đạp chân chở khách ở Huế | `R-NONMOTOR-02` | Gán box `person` cho tài xế và hành khách; **không gán** xích lô. | Xích lô là phương tiện thô sơ đạp chân, ngoài phạm vi taxonomy cơ giới. |
| `img_007.jpg` | Xe tải trong kho mờ tối ban đêm | `R-LOWLIGHT-01` | Gán `truck`, đặt `occluded_level = 1`, `truncated = yes` nếu chạm mép. | Dù thiếu sáng nhưng kết cấu xe tải nhìn rõ, box ôm phần nhìn thấy. |
| `img_011.jpg` | Tượng nhân vật giả tưởng Predator bên xe mô tô | `R-STATUE-01` | Gán các xe mô tô là `motorcycle`; **không gán** `person` cho tượng Predator. | Tượng giả tưởng không phải con người thật, tránh gây phanh gấp ảo. |
| `img_012.jpg` | Xe bán tải chở thùng xốp rau củ lồi khỏi thùng | `R-OVERLOAD-01` | Gán `truck`, box ôm thân xe và cabin, không mở rộng theo hàng rời nhô lên. | Tránh làm méo mó kích thước vật lý của phương tiện giao thông. |
| `img_014.jpg` | Người đi bộ và xe máy bị nhòe chuyển động (motion blur) | `R-BLUR-01` | Vẫn gán `person` và `motorcycle` nếu mắt người nhận biết rõ viền; đặt `can_review = true` nếu biên quá nhòe. | Mô hình cần nhận diện vật thể trong điều kiện thực tế mưa/chuyển động. |
| `img_015.jpg` | Phố mưa mờ ảo nhòe đèn xe | `R-RAIN-01` | Gán các xe nhận diện được; xe quá nhòe ở xa khoanh `ignore_region`. | Tránh gán các box có tọa độ ngẫu nhiên không thể tái lập. |
| `img_016.jpg` | Xe tuk-tuk và xe bán tải nắp thùng cao trên phố Bangkok | `R-TUKTUK-02` | Gán tuk-tuk là `motorcycle` (tick `can_review`); gán bán tải là `truck`. | Thống nhất quy tắc xử lý tuk-tuk và xe bán tải có nắp thùng. |
| `img_017.jpg` | Tượng đồng Wellington cưỡi ngựa đội nón giao thông | `R-STATUE-02` | **Không gán box** `person` hay phương tiện cho tượng và con ngựa. | Đây là di tích/tượng điêu khắc tĩnh, hoàn toàn không phải con người thật. |
| `img_018.jpg` | Biển quảng cáo chính trị in hình chân dung | `R-BILLBOARD-01` | **Không gán box** `person` cho ảnh in trên billboard. | Hình ảnh 2D tĩnh không di chuyển, gán sẽ gây dương tính giả tai hại. |
| `img_019.jpg` | Xe diễu hành Hamley gắn tượng chuột Dangermouse khổng lồ | `R-NOVELTY-01` | Gán `car` ôm thân xe cơ sở bên dưới; tick `can_review = true`. | Thân xe là ô tô, tượng hoạt hình khổng lồ trên nóc là đạo cụ diễu hành. |
| `img_020.jpg` | Cầu vồng và xe phản chiếu qua gương chiếu hậu | `R-MIRROR-01` | **Không gán box** cho bất kỳ hình ảnh ảo nào bên trong mặt gương. | Gương chiếu hậu phản chiếu ảnh ảo, vật thật nằm ở vị trí khác. |
| `img_022.jpg` | Xe mô tô cổ có thùng phụ sidecar | `R-SIDECAR-01` | Gán 1 box `motorcycle` ôm trọn cả xe mô tô và thùng phụ sidecar; gán box `person` cho người ngồi. | Thùng phụ gắn cố định vào xe máy tạo thành một khối phương tiện duy nhất. |
| `img_024.jpg` | Xe AMC Pacer chở thân vỏ xe ô tô phế liệu trên nóc | `R-CARGO-01` | Gán 1 box `car` cho xe đang chạy; **không gán** `car` cho vỏ xe phế liệu gác trên giá nóc. | Vỏ xe trên nóc chỉ đóng vai trò hàng hóa chuyên chở, không phải phương tiện vận hành. |
| `img_026.jpg` | Cặp đôi nam nữ trên xe máy trong hầm chui | `R-MOTO-RIDER-02` | Gán 2 box `person` riêng biệt cho 2 người; gán 1 box `motorcycle` cho xe máy. | Hai cơ thể riêng biệt, mỗi người có nguy cơ tổn thương độc lập khi va chạm. |
| `img_027.jpg` | Tượng đài đá tạc hình xe bán tải ở nghĩa trang | `R-STATUE-03` | **Không gán box** `truck` hay `car` cho khối tượng đá. | Khối điêu khắc trang trí tĩnh, gán sẽ gây phanh gấp ảo. |
| `img_028.jpg` | Xe bán tải chở tượng con ngựa ("yorse") trên thùng | `R-CARGO-02` | Gán 1 box `truck` cho xe bán tải; **không gán** box cho tượng ngựa. | Tượng ngựa là hàng trang trí chở trên thùng xe, không phải sinh vật hay phương tiện. |
| `img_029.jpg` | Xe máy chở một núi xốp khổng lồ che kín người | `R-OVERLOAD-02` | Box `motorcycle` ôm phần khung xe và bánh xe nhìn thấy; tick `can_review = true`. | Không kéo box xe máy to bằng cả khối hàng xốp cồng kềnh. |
| `img_032.jpg` | Đám đông chờ xe buýt và xe buýt lớn | `R-CROWD-01` | Gán xe buýt là `truck` (tick `can_review`, đề xuất lớp `bus`); cụm người dày đặc khoanh `ignore_region`. | Đám đông quá dày không thể tách box từng người một cách đáng tin cậy. |
| `img_033.jpg` | Ma-nơ-canh thời trang trong tủ kính cửa hàng | `R-MANNEQUIN-01` | **Không gán box** `person` cho ma-nơ-canh. | Ma-nơ-canh là vật thể tĩnh vô tri, không phải con người thật. |
| `img_035.jpg` | Xe tuk-tuk chở núi bao tải quá khổ chất cao trên nóc | `R-OVERLOAD-03` | Gán `motorcycle` (hoặc `tuk_tuk`), box ôm thân xe; tick `can_review = true`. | Box phương tiện không bao khối bao tải cồng kềnh cao gấp đôi xe. |
| `img_036.jpg` | Xe tải nhỏ đầu bằng CMC Veryca | `R-TRUCK-02` | Gán `truck`. | Có khoang chở hàng riêng biệt phía sau $\rightarrow$ thuộc định nghĩa `truck`. |
| `img_037.jpg` | Xe bán tải GO Transit gắn nắp thùng cao Master 75 | `R-PICKUP-CAP-01` | Gán `truck`, tick `can_review = true` (đưa ra nhóm thảo luận `truck` vs `van`). | Bản chất khung gầm là xe bán tải, nắp thùng cao là phụ kiện lắp thêm. |
| `img_038.jpg` | Bộ sưu tập ô tô đồ chơi và búp bê trong tủ kính | `R-TOY-01` | **Không gán box** `car` hay `person` cho đồ chơi mô hình. | Đồ chơi thu nhỏ không tham gia giao thông. |

---

## 5. QC và quản lý phiên bản

### 5.1. Ngưỡng kiểm soát chất lượng áp dụng

Tuân thủ nghiêm ngặt các ngưỡng được định nghĩa trong `submission/taxonomy.json`:
- Chiều cao box tối thiểu: `min_box_height_px = 20 px`.
- Ngưỡng IoU box lớn ($\ge 50\text{ px}$): `0.85`.
- Ngưỡng IoU box nhỏ ($< 50\text{ px}$): `0.70`.
- Ngưỡng đánh giá độ đồng thuận IAA giữa 2 annotator: IoU $\ge 0.85$; Tỷ lệ khớp lớp $\ge 95\%$.
- Tỷ lệ ảnh có lỗi tối đa cho phép để bàn giao (Release): $\le 2\%$ (tương đương tối đa không quá 0 ảnh lỗi trên lô 40 ảnh).

### 5.2. Cơ chế xử lý trường hợp mơ hồ và lịch sử phiên bản

- **Cơ chế xử lý:** Khi gặp đối tượng chưa thể xác định chắc chắn theo guideline, annotator bắt buộc tick `can_review = true` trên giao diện CVAT. Nếu là vấn đề cấp ảnh chưa vẽ được box, ghi lại vào nhật ký để đưa ra phiên calibration.
- **Lịch sử thay đổi:**

| Phiên bản | Ngày | Người thực hiện | Tóm tắt thay đổi | Căn cứ từ ảnh thực tế |
|---|---|---|---|---|
| `v0` | 2026-11-16 | Giảng viên | Bản sơ lược khởi đầu, định nghĩa định tính 5 lớp. | Chưa bao quát các tình huống biên đường phố. |
| `v0.1-indiv` | 2026-11-16 | Thành viên `101` | Hoàn thiện định lượng 3 thuộc tính (ngưỡng % đo được); bổ sung 6 nhóm quy tắc ứng xử (người đi xe máy, xe chở xe, tượng, quảng cáo, phản chiếu, hàng cồng kềnh); lập bảng phân tích 28 ca khó chi tiết. | Khảo sát thực tế toàn bộ 40 ảnh `img_001.jpg` đến `img_040.jpg`. |
