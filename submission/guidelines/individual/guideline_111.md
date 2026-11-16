# Guideline gán nhãn — v1.0-agreed — Thành viên 111

- Phiên bản: v1.0 (Thống nhất nhóm Pha 2 — Cập nhật bản thành viên 111)
- Ngày: 2026-11-16
- Người viết / Hiệu chỉnh: Thành viên 111

---

## 1. Mục tiêu

- **Mục đích mô hình:** Dữ liệu phục vụ huấn luyện mô hình 2D Object Detection đa lớp (bounding box) cho các hệ thống camera giám sát giao thông thông minh (ITS) và hệ thống hỗ trợ lái xe nâng cao (ADAS / Xe tự hành) trong đô thị.
- **Rủi ro an toàn & Vùng nguy hiểm:**
  - *Bỏ sót (False Negative - Bỏ sót người đi bộ, người đi xe máy/xe đạp):* Nguy cơ va chạm trực tiếp gây tai nạn nghiêm trọng trong thực tế.
  - *Nhận diện nhầm (False Positive - Gán nhầm tượng đài, tranh ảnh quảng cáo, ma-nơ-canh):* Dẫn đến hiện tượng phanh gấp ngoài ý muốn (phantom braking), nguy cơ xe phía sau đâm dồn toa.
  - *Sai lệch kích thước bounding box:* Làm ước tính sai khoảng cách vật thể và thời gian tới va chạm (Time-to-Collision - TTC).

---

## 2. Lớp và thuộc tính

### 2.1. Danh mục lớp đối tượng (Classes)

Mỗi đối tượng hợp lệ trong ảnh được phân loại vào đúng một lớp duy nhất:

| Lớp | Định nghĩa thống nhất (một câu) | Ví dụ cụ thể trong tập 40 ảnh | Phản ví dụ / Lưu ý tránh nhầm |
|---|---|---|---|
| `car` | Phương tiện cơ giới 4 bánh chuyên chở người cỡ nhỏ (sedan, hatchback, SUV, crossover). | Xe sedan màu trắng trong `img_001.jpg`, các xe con trên sàn chở hàng `img_002.jpg`. | Không gán xe mô hình đồ chơi (`img_038.jpg`); không gán xe bán tải thùng hàng (`truck`). |
| `truck` | Xe cơ giới chở hàng (xe tải lớn, xe đầu kéo chuyên dụng, xe bán tải/pickup) **và toàn bộ các loại xe tải nhỏ/xe tải nhẹ**. | Xe chở ô tô `img_002.jpg`, xe tải trong kho `img_007.jpg`, xe bán tải `img_012.jpg`, **xe tải nhỏ CMC Veryca `img_036.jpg`**, **xe bán tải nắp thùng cao màu trắng `img_037.jpg`**. | Không gán tượng đài/bia mộ xe bán tải bằng đá trong `img_027.jpg`. |
| `van` | Xe thùng kín cỡ nhỏ chở người hoặc hàng hóa, thân liền khối hình hộp (minivan, xe chở khách cỡ vừa). | Xe thùng kín thân liền khối. | **Không bao gồm xe tải nhỏ** (toàn bộ xe tải nhỏ đã được chuyển sang lớp `truck`). |
| `motorcycle` | Phương tiện cơ giới hai (2) hoặc ba (3) bánh có gắn động cơ (xe máy, mô tô, scooter, xe mô tô gắn thùng bên sidecar). | Dòng xe máy trong `img_005.jpg`, `img_008.jpg`, `img_026.jpg`, **xe mô tô có thùng bên sidecar `img_022.jpg`**. | Không gán xe đạp thô sơ hoặc xích lô (`bicycle`). |
| `bus` | Xe buýt hoặc xe khách chuyên dụng cỡ lớn chuyên chở nhiều người. | Xe buýt lớn chở khách phía sau xích lô trong `img_009.jpg`, `img_032.jpg`, `img_040.jpg`. | Không gán nhầm vào `van` hay `truck` để tránh sai lệch hình thái. |
| `bicycle` | Phương tiện thô sơ hai (2) hoặc ba (3) bánh chạy bằng sức người đạp, bao gồm cả **xe đạp và xe xích lô**. | Xe đạp, **xe xích lô chở khách/hàng trong `img_006.jpg`, `img_009.jpg`, `img_023.jpg`, `img_034.jpg`, `img_039.jpg`**. | Không gán nhầm sang `motorcycle` (xích lô không có động cơ). Người đạp xích lô/khách ngồi gán thêm box `person`. |
| `tuk_tuk` | Xe cơ giới ba (3) bánh chở khách đặc thù có cabin mở (tuk-tuk, auto-rickshaw). | Hai chiếc tuk-tuk xanh trong `img_004.jpg`, xe tuk-tuk phố Bangkok `img_016.jpg`, xe auto-rickshaw chở hàng `img_035.jpg`. | Không gán ép vào `car` (khác tỷ lệ) hay `motorcycle`. |
| `person` | Con người thật còn sống (người đi bộ, người điều khiển phương tiện hoặc hành khách ngồi trên xe). | Người phụ nữ đứng cạnh xe `img_001.jpg`, người đi xe máy `img_005.jpg`, người đạp xích lô và khách `img_006.jpg`. | Tuyệt đối không gán tượng đồng (`img_017.jpg`), ảnh in quảng cáo (`img_018.jpg`), ma-nơ-canh (`img_033.jpg`). |
| `ignore_region` | Vùng hình chữ nhật đánh dấu khu vực bỏ qua (không phải vật): vùng đám đông dày đặc, vật thể quá xa mờ nhòe. | Cụm người/xe quá nhỏ mờ ở hậu cảnh xa trong `img_008.jpg`, `img_025.jpg`. | Không dùng để che lấp tùy tiện các đối tượng tiền cảnh rõ nét (> 20 px). |

---

### 2.2. Thuộc tính đối tượng (Attributes)

Nhóm đã thống nhất tối giản hóa thuộc tính: **Chuyển `occluded` và `truncated` về dạng giá trị Boolean nhị phân (`true` / `false`)**, không phân cấp theo level phần trăm (%) phức tạp.

| Thuộc tính | Kiểu / Giá trị | Mặc định | Định nghĩa & Ý nghĩa quy ước |
|---|---|---|---|
| `occluded` | `checkbox`<br>`[false, true]` | `false` | - `false`: Đối tượng nhìn thấy trọn vẹn bề mặt, không bị bất kỳ vật thể nào khác che chắn.<br>- `true`: Đối tượng bị che khuất một phần bất kỳ bởi vật thể khác phía trước (xe trước, vỉa hè, cột đèn, hàng hóa...). Không cần đo % diện tích. |
| `truncated` | `checkbox`<br>`[false, true]` | `false` | - `false`: Toàn bộ đối tượng nằm hoàn toàn bên trong khung hình.<br>- `true`: Đối tượng bị cắt ngang bởi ít nhất một trong bốn mép biên của ảnh (trái, phải, trên, dưới). Không cần đo % diện tích. |
| `can_review` | `checkbox`<br>`[false, true]` | `false` | - `false`: Box rõ ràng, chuẩn theo quy tắc.<br>- `true`: Tick chọn khi annotator còn phân vân về ranh giới hoặc phân lớp để đưa ra thảo luận tại phiên Calibration. |

---

## 3. Quy tắc vẽ Bounding Box (Gắn mã `R-01`, `R-02`…)

Các quy tắc trọng tâm được mã hóa chuẩn để truy vết trong nhật ký QC và phiên Calibration:

- **`R-01` (Ôm sát phần nhìn thấy - Tight Visual Boundary):**
  - Bounding box là hình chữ nhật nhỏ nhất bao trọn toàn bộ điểm ảnh nhìn thấy được (visible pixels) của vật.
  - Vì thuộc tính `occluded` và `truncated` chỉ mang giá trị `true`/`false`, người gán **không cần ước lượng phần trăm (%) nhìn thấy**, nhưng **bắt buộc phải ôm sát đường viền nhìn thấy thực tế**, không kéo dài box để phỏng đoán phần bị che khuất sau vật khác.

- **`R-02` (Loại trừ vật thể không có thật - Non-real Objects):**
  - Tuyệt đối **không gán bounding box** cho các đối tượng mô phỏng nhân tạo tĩnh hoặc ảnh ảo:
    - Tượng đài nghệ thuật/lịch sử bằng đồng, đá (`img_017.jpg`, `img_027.jpg`).
    - Ma-nơ-canh trưng bày trong cửa hàng thời trang (`img_033.jpg`).
    - Xe mô hình, búp bê, đồ chơi thu nhỏ trong tủ kính (`img_038.jpg`).
    - Tranh, ảnh, pano, biển quảng cáo in hình người hoặc phương tiện (`img_018.jpg`).
    - Ảnh phản chiếu qua gương chiếu hậu hoặc cửa kính (`img_020.jpg`).

- **`R-03` (Xe chở xe - Car Carrier):**
  - Với phương tiện chuyên dụng chở nhiều ô tô con (`img_002.jpg`):
    - Gán 1 box lớn lớp `truck` bao toàn bộ thân xe tải vận chuyển (bao gồm cabin và hệ thống sàn/giàn chở).
    - Đồng thời gán từng bounding box lớp `car` riêng lẻ cho mỗi chiếc ô tô con được xếp trên 2 tầng giàn (nếu thấy rõ đặc trưng nhận dạng).

- **`R-04` (Người và phương tiện 2-3 bánh - Rider & Vehicle):**
  - *Xe máy thông thường (`img_005.jpg`, `img_026.jpg`):* Tách riêng 1 box `motorcycle` cho thân xe máy và từng box `person` riêng cho người lái xe và người ngồi sau.
  - *Xe đạp / Xích lô (`img_006.jpg`, `img_034.jpg`, `img_039.jpg`):* Gán 1 box `bicycle` cho thân xe xích lô / xe đạp, và gán từng box `person` cho người đạp xe cùng hành khách ngồi trên đó.
  - *Xe mô tô có thùng bên sidecar (`img_022.jpg`):* **Gán 1 box `motorcycle` gộp toàn bộ thân xe mô tô cùng thùng bên (sidecar), không tách rời.** Người ngồi trên xe gán box `person` riêng.

- **`R-05` (Phân định Xe tải nhỏ vs Xe van):**
  - **Xe tải nhỏ/xe tải nhẹ được xếp vào lớp `truck`**, không xếp vào `van`.
  - Mọi phương tiện có cabin lái gắn liền với thùng hàng riêng biệt phía sau (dù kích thước nhỏ như chiếc CMC Veryca trong `img_036.jpg`) đều được gắn nhãn là `truck`.
  - Lớp `van` chỉ áp dụng cho xe thùng kín chở khách/hàng có thiết kế thân vỏ liền khối hình hộp (minivan, xe transit).

- **`R-06` (Xe bán tải có nắp thùng cao):**
  - Xe bán tải gắn nắp thùng cao màu trắng (Master 75 Truck Cap) trong `img_037.jpg` được thống nhất gán nhãn là **`truck`**.

- **`R-07` (Hàng hóa cồng kềnh trên xe ba bánh / tuk-tuk):**
  - Với xe ba bánh, tuk-tuk chở hàng cồng kềnh (`img_035.jpg`): Bounding box lớp `tuk_tuk` chỉ ôm sát khung xe và các bộ phận cơ giới; **không kéo phình box để bao trọn đống bao tải hàng hóa phồng to chất cao trên nóc và đuôi xe**, nhằm giữ đúng tỷ lệ hình học chuẩn của xe.

- **`R-08` (Khung vỏ xe gắn trên nóc phương tiện khác):**
  - Với xe wagon AMC Pacer trong `img_024.jpg`: Gán 1 box `car` cho chiếc xe lăn bánh chính. Khung vỏ xe cũ gắn trên giá nóc được coi là hành lý/hàng hóa, không gán thêm box phương tiện thứ hai.

- **`R-09` (Ngưỡng kích thước tối thiểu & Đám đông xa):**
  - Không gán box đơn lẻ cho các đối tượng có chiều cao **nhỏ hơn 20 pixels** (vật thể quá xa, nhòe nét).
  - Các cụm đối tượng quá nhỏ hoặc đám đông dày đặc ở hậu cảnh được gom chung vào một vùng `ignore_region`.

---

## 4. Bảng ca khó khảo sát trong 40 ảnh

Bảng tổng hợp chi tiết các ca khó trọng tâm sau khi nhóm đã chốt quyết định ở Pha 2:

| Ảnh | Tình huống thực tế trên ảnh | Mã quy tắc | Quyết định thống nhất của nhóm | Lý do chuyên môn |
|---|---|---|---|---|
| `img_036.jpg` | Xe tải nhẹ CMC Veryca trên đường phố Đài Bắc. | `R-05` | **Gán nhãn `truck`.** | Nhóm thống nhất chuyển toàn bộ xe tải nhỏ về lớp `truck`, loại bỏ khỏi lớp `van`. Xe có cabin lái tách rời thùng hàng sau. |
| `img_037.jpg` | Xe bán tải màu trắng có gắn nắp thùng cao (Master 75 Truck Cap). | `R-06` | **Gán nhãn `truck` cho chiếc xe màu trắng.** | Bản chất đây là xe bán tải (pickup truck) gắn thêm phụ kiện nắp thùng bảo vệ, xếp vào lớp `truck`. |
| `img_022.jpg` | Xe mô tô cổ có gắn thêm thùng bên chở người (sidecar) Fortepan 4915. | `R-04` | **Gán 1 box `motorcycle` bao toàn bộ thân xe và thùng bên (không tách ra).** Người ngồi gán `person`. | Sidecar là bộ phận gắn liền của phương tiện cơ giới 3 bánh này, gộp chung để giữ đúng vùng chiếm dụng không gian của xe. |
| `img_006.jpg` | Đoàn xe xích lô chở khách du lịch trên đường phố Huế. | `R-04` | **Gán box `bicycle` cho chiếc xích lô.** Người đạp và khách ngồi gán box `person`. | Nhóm thống nhất bổ sung lớp `bicycle` cho xe đạp và xích lô phi cơ giới. |
| `img_004.jpg` | Hai chiếc xe tuk-tuk màu xanh đỗ cạnh nhau trên vỉa hè Pattaya. | `R-07` | **Gán nhãn `tuk_tuk` cho từng chiếc xe.** | Đã bổ sung lớp chuyên biệt `tuk_tuk`, không còn phải ép vào `car` hay `motorcycle`. |
| `img_009.jpg` | Xe buýt lớn chở khách xuất hiện rõ nét ở hậu cảnh sau đoàn xích lô. | `R-05` | **Gán nhãn `bus`.** | Đã bổ sung lớp chuyên biệt `bus` cho xe khách/xe buýt cỡ lớn. |
| `img_002.jpg` | Xe chuyên dụng 2 tầng chở 8 ô tô con trên sàn xe (Renault 380 car carrier). | `R-03` | Gán 1 box `truck` cho xe tải lớn, gán 8 box `car` riêng cho từng xe con trên sàn giàn. | Phục vụ mô hình phát hiện đầy đủ chướng ngại vật ô tô con để tránh va chạm. |
| `img_017.jpg` | Tượng công tước Wellington cưỡi ngựa bằng đồng đội nón giao thông. | `R-02` | **Không gán bất kỳ box nào.** | Tượng kim loại là công trình điêu khắc tĩnh vĩnh cửu, không phải người thật tham gia giao thông; tránh lỗi phanh ma. |
| `img_018.jpg` | Biển hiệu quảng cáo pano chính trị in hình chân dung người. | `R-02` | **Không gán box `person`.** | Hình in 2D trên biển hiệu không phải người thật. |
| `img_020.jpg` | Ảnh phản chiếu cầu vồng và xe cộ qua gương chiếu hậu. | `R-02` | **Không gán box.** | Ảnh ảo quang học qua gương không có tọa độ thực trước mũi xe. |
| `img_024.jpg` | Xe wagon AMC Pacer có khung vỏ xe cũ gắn trên giá nóc xe. | `R-08` | Gán 1 box `car` cho xe đang lăn bánh. Khung vỏ xe trên nóc coi là hàng hóa, không gán box. | Vỏ xe trên nóc không có động cơ, bánh xe hay người điều khiển độc lập. |
| `img_027.jpg` | Bia mộ / Đài tưởng niệm tạc hình xe bán tải bằng đá granite trong nghĩa trang. | `R-02` | **Không gán box `truck`.** | Khối đá điêu khắc trong nghĩa trang, không phải xe cơ giới. |
| `img_033.jpg` | Ma-nơ-canh mặc quần áo thời trang đứng trong tủ kính cửa hàng Buchanan Street. | `R-02` | **Không gán box `person`.** | Ma-nơ-canh làm bằng nhựa/thạch cao, không có hành vi người thật. |
| `img_035.jpg` | Xe auto-rickshaw chở hàng đống bao tải cồng kềnh phồng to ở Hyderabad. | `R-07` | Gán box `tuk_tuk` ôm sát thân xe cơ giới; không bao đống bao tải phồng to trên nóc. | Giúp mô hình giữ đúng hình thái kích thước chuẩn của phương tiện. |
| `img_038.jpg` | Tủ kính trưng bày hàng chục mô hình ô tô đồ chơi và búp bê tại Munich. | `R-02` | **Không gán bất kỳ box nào.** | Đồ chơi mô hình thu nhỏ trưng bày sau kính. |

---

## 5. QC và Lịch sử Phiên bản

### 5.1. Tiêu chuẩn QC áp dụng
- **Phân công & Độ phủ:** 100% số ảnh được phân công phải được mở kiểm tra và xuất nhãn COCO 1.0 đầy đủ.
- **Tiêu chí chấp nhận thuộc tính:** Thuộc tính `occluded` và `truncated` được đánh dấu nhị phân chính xác (`true`/`false`), không cần phân vân đo đạc tỷ lệ phần trăm.
- **Bắt buộc gán mã quy tắc:** Mọi tranh chấp, nghi vấn hoặc sửa đổi trong phiên Calibration và Review QC sau này đều phải dẫn chiếu trực tiếp đến một trong các mã từ `R-01` đến `R-09`.

### 5.2. Lịch sử phiên bản

| Phiên bản | Người cập nhật | Nội dung cập nhật chính | Căn cứ từ quyết định nhóm |
|---|---|---|---|
| `v0` | Giảng viên | Bản sơ khởi định tính, thiếu nhiều lớp và thuộc tính mơ hồ. | Bản starter template của lab. |
| `v0.1-draft` | Thành viên 111 | Bản khảo sát độc lập ban đầu của thành viên 111 (Pha 1). | Khảo sát 40 ảnh ban đầu. |
| `v1.0-agreed` | Thành viên 111 (Thống nhất nhóm) | - Bổ sung các lớp: `bus`, `bicycle` (gồm cả xích lô), `tuk_tuk`.<br>- Chuyển xe tải nhỏ từ `van` sang `truck` (`img_036.jpg` là `truck`).<br>- Thống nhất `motorcycle` bao gồm cả 2 và 3 bánh (`img_022.jpg` gán `motorcycle` gộp sidecar).<br>- Tối giản thuộc tính: `occluded` và `truncated` chuyển về `true`/`false`, bỏ chia cấp độ %.<br>- Gắn mã quy tắc chính thức từ `R-01` đến `R-09`.<br>- Chốt các ca khó trọng tâm: `img_037.jpg` gán `truck`, `img_022.jpg` gán `motorcycle` không tách. | Họp nhóm thống nhất Pha 2. |
