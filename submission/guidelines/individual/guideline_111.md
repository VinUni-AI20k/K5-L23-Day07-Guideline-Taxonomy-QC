# Guideline gán nhãn — v0.1-draft — Thành viên 111

- Phiên bản: v0.1-draft (Pha 1 — Khảo sát độc lập 40 ảnh)
- Ngày: 2026-11-16
- Người viết: Thành viên 111 (Mã kiểm định: 111)

---

## 1. Mục tiêu

- **Mục đích mô hình:** Dữ liệu phục vụ huấn luyện mô hình 2D Object Detection đa lớp (bounding box) cho các hệ thống camera giao thông thông minh (ITS) và hệ thống hỗ trợ lái xe nâng cao (ADAS / Xe tự hành) hoạt động trong môi trường đô thị phức tạp.
- **Rủi ro an toàn & Vùng nguy hiểm:**
  - *Bỏ sót (False Negative - Bỏ sót người đi bộ hoặc xe máy):* Nguy cơ va chạm chết người trực tiếp trong giao thông thực tế. Đây là lỗi nghiêm trọng nhất.
  - *Nhận diện nhầm (False Positive - Gán box lên tượng đài, tranh ảnh quảng cáo, hình in):* Dẫn đến hiện tượng "phanh ma" (phantom braking), gây nguy cơ xe phía sau đâm dồn toa.
  - *Sai lệch kích thước / Không ôm sát:* Gây ước lượng sai khoảng cách (depth estimation) và thời gian va chạm (Time-to-Collision - TTC).

---

## 2. Lớp và thuộc tính

### 2.1. Lớp đối tượng (Classes)

Mỗi đối tượng hợp lệ trong ảnh được gán vào đúng một lớp duy nhất:

| Lớp | Định nghĩa (một câu) | Ví dụ cụ thể trong tập ảnh | Phản ví dụ / Dễ nhầm với |
|---|---|---|---|
| `car` | Phương tiện cơ giới 4 bánh chuyên chở người cỡ nhỏ (sedan, hatchback, SUV, crossover). | Xe sedan màu trắng đỗ ven đường trong `img_001.jpg`, các xe con trên giá vận chuyển `img_002.jpg`. | Không gán xe mô hình đồ chơi (`img_038.jpg`); không gán xe bán tải thùng hở (`truck`). |
| `truck` | Xe cơ giới chuyên dụng chở hàng hóa nặng, có cabin lái tách rời thùng xe hoặc xe bán tải (pickup truck). | Xe chở ô tô chuyên dụng `img_002.jpg`, xe tải chở hàng trong kho `img_007.jpg`, xe bán tải `img_012.jpg`. | Không gán đài tưởng niệm/tượng xe bán tải bằng đá granite trong `img_027.jpg`; không gán xe đẩy tay. |
| `van` | Xe tải nhẹ hoặc xe chở khách thân liền khối hình hộp chữ nhật (không có thùng hàng hở tách rời). | Xe tải nhẹ thân kín CMC Veryca trong `img_036.jpg`. | Dễ nhầm với `car` cỡ lớn hoặc `bus`. Nếu có kính toàn bộ thân xe và chở > 16 người thì kiến nghị lớp `bus`. |
| `motorcycle` | Phương tiện cơ giới hai hoặc ba bánh gắn động cơ đốt trong hoặc động cơ điện (xe máy, mô tô, scooter). | Xe máy di chuyển dày đặc trong `img_005.jpg`, `img_008.jpg`, `img_026.jpg`, `img_030.jpg`. | Không gán xe đạp không động cơ hoặc xích lô trong `img_006.jpg`, `img_023.jpg`, `img_039.jpg`. |
| `person` | Con người còn sống (thân thể thật), bao gồm người đi bộ, người điều khiển hoặc hành khách trên xe. | Người phụ nữ đứng cạnh xe trong `img_001.jpg`, người lái và ngồi sau xe máy trong `img_005.jpg`, `img_026.jpg`. | Không gán tượng đồng (`img_017.jpg`), ảnh chân dung in trên biển quảng cáo (`img_018.jpg`), ma-nơ-canh (`img_033.jpg`). |
| `ignore_region` | Vùng chữ nhật bao quanh khu vực đông đúc, các đối tượng quá nhỏ hoặc vùng không thể tách bạch box. | Vùng người và xe quá xa, mờ nhòe ở hậu cảnh trong `img_008.jpg`, `img_025.jpg`. | Không dùng để che lấp các đối tượng tiền cảnh rõ nét (> 20 px) nhằm trốn việc gán nhãn. |

#### Xử lý đối tượng ngoài taxonomy v0:
- **Xe tuk-tuk / Auto-rickshaw (`img_004.jpg`, `img_016.jpg`, `img_035.jpg`):** v0 không có định nghĩa. Tạm thời tick `can_review` và kiến nghị nhóm bổ sung lớp `tuk_tuk` ở Pha 2 vì đây là phương tiện giao thông cơ giới 3 bánh phổ biến tại châu Á, có đặc trưng hình học khác hẳn xe con 4 bánh và xe máy 2 bánh.
- **Xe buýt cỡ lớn (`img_009.jpg`, `img_032.jpg`, `img_040.jpg`):** v0 thiếu lớp `bus`. Kiến nghị nhóm thêm lớp `bus` ở Pha 2.
- **Xích lô / Xe đạp (`img_006.jpg`, `img_023.jpg`, `img_039.jpg`):** Không gán box cho xe phi cơ giới; chỉ gán box `person` cho người đạp xe và hành khách ngồi trên đó.

---

### 2.2. Thuộc tính đối tượng (Attributes)

Mỗi bounding box bắt buộc phải xác định 3 thuộc tính đo lường định lượng:

| Thuộc tính | Kiểu / Giá trị | Ngưỡng định lượng & Ý nghĩa chi tiết |
|---|---|---|
| `occluded_level` | `select`<br>`["0", "1", "2", "3"]` | **0 (Không bị che):** Nhìn thấy trọn vẹn 100% diện tích viền ngoài của vật.<br>**1 (Che ít):** Bị che khuất từ 1% đến 30% diện tích bề mặt (ví dụ: bánh xe bị mép vỉa hè hoặc xe trước che nhẹ).<br>**2 (Che nhiều):** Bị che khuất từ 31% đến 70% diện tích nhưng các đặc trưng chính của vật vẫn nhận dạng chắc chắn.<br>**3 (Che nghiêm trọng):** Bị che trên 70% diện tích, chỉ còn thấy một phần nhỏ (ví dụ chỉ thấy đầu xe nhô ra) nhưng mắt người vẫn khẳng định được sự tồn tại của vật. |
| `truncated` | `select`<br>`["no", "yes"]` | **no:** Toàn bộ đối tượng nằm trọn vẹn bên trong khung ảnh.<br>**yes:** Đối tượng bị cắt ngang bởi ít nhất một mép biên của khung hình (top, bottom, left, right). |
| `can_review` | `checkbox`<br>`[false, true]` | **false:** Box rõ ràng, áp dụng đúng quy tắc chuẩn.<br>**true:** Bật cờ khi annotator cảm thấy ca biên lưỡng lự (chưa rõ phân lớp hoặc ranh giới cắt box) để đưa ra phiên calibration của nhóm. |

---

## 3. Quy tắc vẽ Bounding Box

1. **Nguyên tắc ôm sát phần nhìn thấy (Tight Visual Boundary):**
   - Bounding box phải là hình chữ nhật nhỏ nhất bao trọn toàn bộ **các phần điểm ảnh nhìn thấy được (visible pixels)** của đối tượng.
   - Không mở rộng box để "phỏng đoán" những phần bị che lấp hoàn toàn sau vật thể khác.
2. **Quy tắc Người và Xe máy (Rider & Motorcycle):**
   - **Tách rời:** Mỗi người ngồi trên xe máy (người lái, người ngồi sau) được vẽ 1 box `person` riêng biệt (ôm từ đỉnh mũ bảo hiểm đến chân/chỗ tiếp xúc với xe).
   - Thân xe máy được vẽ 1 box `motorcycle` riêng biệt (bao gồm cả bánh xe, thân xe, ghi-đông, gương chiếu hậu).
   - Cho phép hai box `person` và `motorcycle` giao nhau (overlap) tại khu vực ngồi.
3. **Quy tắc Xe chở xe (Car carrier - `img_002.jpg`):**
   - Vẽ 1 box lớn `truck` bao quanh toàn bộ chiếc xe chở ô tô chuyên dụng (cabin và giàn sàn xe).
   - Với mỗi chiếc xe ô tô con được chở trên sàn: Nếu diện tích nhìn thấy >= 30% và nhận dạng rõ đặc trưng, vẽ thêm 1 box `car` riêng cho từng xe con đó (`occluded_level` tương ứng).
4. **Quy tắc Hàng hóa quá khổ / Đồ chở trên xe (`img_029.jpg`, `img_035.jpg`):**
   - Nếu hàng hóa chở trên xe máy / tuk-tuk chất cao phình to quá cỡ (bao tải, kiện hàng), box `motorcycle` / `tuk_tuk` chỉ bao trọn thân xe cơ giới; không kéo phình box bao trọn đống bao tải lơ lửng trên không làm biến dạng tỷ lệ khung vỏ xe.
5. **Vật thể không có thật / Đồ vật trưng bày (Non-real objects):**
   - **Tuyệt đối không gán:** Tượng đài (`img_017.jpg`, `img_027.jpg`), ma-nơ-canh cửa hàng (`img_033.jpg`), mô hình đồ chơi (`img_038.jpg`), hình người/xe in trên poster/billboard quảng cáo (`img_018.jpg`).
   - Lý do: Mô hình tự hành chỉ cần phát hiện các đối tượng thật có khả năng cử động hoặc phương tiện đang tham gia giao thông.
6. **Ảnh phản chiếu gương / Kính (`img_020.jpg`):**
   - Không gán box cho ảnh ảo phản chiếu qua gương chiếu hậu hoặc cửa kính vì tọa độ thực tế không tồn tại trên mặt đường.
7. **Xe của chủ phương tiện gắn camera (Ego-vehicle):**
   - Nếu nắp capo hoặc viền kính của xe quay phim xuất hiện ở mép dưới ảnh, không gán nhãn cho phần thân vỏ xe này.
8. **Ngưỡng kích thước tối thiểu (Minimum Size Threshold):**
   - Không gán bounding box riêng lẻ cho các vật thể có chiều cao hoặc chiều rộng **nhỏ hơn 20 pixels** (quá xa, mất nét).
   - Nếu có cụm đối tượng nhỏ hoặc đám đông dày đặc ở phía xa, gom toàn bộ vào một vùng `ignore_region`.

---

## 4. Bảng ca khó khảo sát trong 40 ảnh

Dưới đây là các tình huống thực tế khảo sát độc lập từ `img_001.jpg` đến `img_040.jpg` mà guideline v0 chưa xử lý được:

| Ảnh | Tình huống thực tế | Mã đề xuất | Quyết định cá nhân của annotator 111 | Lý do chuyên môn |
|---|---|---|---|---|
| `img_002.jpg` | Xe tải 2 tầng chuyên dụng chở 8 ô tô con trên thùng. | `R-02` | Gán 1 box `truck` cho xe tải lớn, và gán 8 box `car` riêng cho từng ô tô con trên sàn xe. | Mô hình cần phát hiện ô tô con để tránh va chạm chiều cao và hỗ trợ phân loại phương tiện trên đường. |
| `img_004.jpg` | Hai chiếc xe tuk-tuk 3 bánh đỗ cạnh nhau trên vỉa hè. | `R-04` | Đề xuất bổ sung lớp `tuk_tuk` (nếu chưa có thì tạm tick `can_review`). Không gán ép vào `car` hay `motorcycle`. | Tuk-tuk có 3 bánh và cabin mở, nếu ép vào `car` sẽ phá vỡ phân phối tỷ lệ khung hình (aspect ratio) của ô tô con. |
| `img_005.jpg` | Đám đông hàng chục người đi xe máy chen chúc trên đường phố. | `R-03` | Tách riêng từng người (`person`) và từng xe (`motorcycle`). Các xe quá xa < 20 px đưa vào `ignore_region`. | Quy tắc tách giúp mô hình học được mối quan hệ giữa người điều khiển và phương tiện, tránh nhầm lẫn khi người xuống xe. |
| `img_006.jpg` | Xe xích lô chở khách du lịch trên đường phố Huế. | `R-05` | Không gán box cho chiếc xích lô. Chỉ gán 1 box `person` cho người đạp xích lô và 1 box `person` cho khách ngồi. | Xích lô là xe phi cơ giới, không có trong danh mục phương tiện cơ giới của bài toán. |
| `img_009.jpg` | Xe buýt lớn chở khách xuất hiện rõ nét ở hậu cảnh sau xích lô. | `R-04` | Kiến nghị bổ sung lớp `bus`. Tạm thời tick `can_review` để thảo luận nhóm. | Xe buýt có kích thước vượt trội, nếu gán `van` hay `truck` sẽ làm mô hình học sai hình thái nhận dạng. |
| `img_017.jpg` | Tượng công tước Wellington cưỡi ngựa bằng đồng, trên đầu có nón giao thông. | `R-01` | **Không gán bất kỳ box nào.** | Tượng kim loại là vật thể tĩnh vĩnh cửu của cảnh quan kiến trúc, không thể tự di chuyển, tránh gây lỗi phantom braking. |
| `img_018.jpg` | Biển quảng cáo pano chính trị khổ lớn in hình chân dung người. | `R-01` | **Không gán box `person`.** | Hình in 2D trên biển hiệu không phải người thật tham gia giao thông. |
| `img_020.jpg` | Gương chiếu hậu phản chiếu hình ảnh cầu vồng và xe cộ phía sau. | `R-01` | **Không gán box** cho các ảnh phản chiếu trong gương. | Vị trí vật phản chiếu là ảnh ảo quang học, không phản ánh vị trí 3D thực của vật thể trước đầu xe. |
| `img_024.jpg` | Xe wagon AMC Pacer, trên nóc xe có gắn một vỏ khung ô tô cũ. | `R-06` | Gán 1 box `car` cho chiếc xe lăn bánh. Khung vỏ xe trên nóc chỉ tính là hành lý/hàng hóa, không gán box xe thứ hai. | Vỏ xe trên nóc không có động cơ, bánh xe hay người điều khiển độc lập; không hoạt động như một phương tiện. |
| `img_027.jpg` | Bia mộ / Tượng đài kỷ niệm tạc hình xe bán tải bằng đá granite trong nghĩa trang. | `R-01` | **Không gán box `truck` hay `car`.** | Vật thể điêu khắc bằng đá cố định tại nghĩa trang, không phải phương tiện vận tải. |
| `img_033.jpg` | Ma-nơ-canh mặc trang phục thời trang đứng trong tủ kính cửa hàng. | `R-01` | **Không gán box `person`.** | Ma-nơ-canh làm bằng nhựa/thạch cao, không di chuyển, không có thân nhiệt hay hành vi con người. |
| `img_035.jpg` | Xe auto-rickshaw chở đống bao tải hàng hóa cồng kềnh khổng lồ trên nóc và đuôi xe. | `R-07` | Box phương tiện chỉ ôm gọn thân xe; không bao trùm khối hàng hóa phồng to phía trên. | Giúp mô hình định vị chính xác trọng tâm và kích thước khung gầm phương tiện. |
| `img_037.jpg` | Xe bán tải công cộng GO Transit gắn nắp thùng kín cao (Master 75 Truck Cap). | `R-08` | Gán lớp `truck` (hoặc `van` tùy nhóm chốt ở Pha 2). Tạm tick `can_review`. | Tình huống lai giữa bán tải gắn nắp và xe van thùng kín, cần thống nhất quy tắc định danh toàn nhóm. |
| `img_038.jpg` | Tủ kính trưng bày bộ sưu tập hàng chục mô hình ô tô đồ chơi và búp bê. | `R-01` | **Không gán bất kỳ box nào.** | Toàn bộ là đồ chơi mô hình thu nhỏ kích thước chỉ vài centimet nằm sau tủ kính. |

---

## 5. QC và Lịch sử Phiên bản

### 5.1. Tiêu chuẩn QC đề xuất áp dụng cho bản thân
- **Độ phủ nhãn:** 100% số ảnh được giao phân công phải được mở kiểm tra và xuất nhãn COCO đầy đủ (kể cả ảnh rỗng 0 annotation).
- **Độ chính xác hình học:** Box phải ôm sát mép ngoài của điểm ảnh vật thể nhìn thấy, dung sai ước lượng không vượt quá 2-3 pixels.
- **Thái độ xử lý ca mơ hồ:** Không tự ý đoán mò khi gặp ca lai; chủ động bật cờ `can_review = true` để đưa ra thảo luận tại phiên Calibration.

### 5.2. Lịch sử thay đổi

| Phiên bản | Người cập nhật | Nội dung thay đổi chính | Căn cứ từ ảnh thực tế |
|---|---|---|---|
| `v0` | Giảng viên | Bản khởi đầu thô sơ, chỉ có 5 lớp định tính, thiếu quy tắc đo lường. | Bản starter template. |
| `v0.1-draft` | Thành viên 111 | - Bổ sung ngưỡng định lượng phần trăm cho `occluded_level`.<br>- Thêm quy tắc loại trừ vật giả (tượng, đồ chơi, hình in, ảnh phản chiếu).<br>- Quy tắc tách riêng `person` và `motorcycle`.<br>- Quy tắc gán xe chở xe và loại bỏ hàng hóa cồng kềnh.<br>- Bổ sung đề xuất lớp `tuk_tuk` và `bus`. | Khảo sát độc lập 40 ảnh (`img_001.jpg` đến `img_040.jpg`). |
