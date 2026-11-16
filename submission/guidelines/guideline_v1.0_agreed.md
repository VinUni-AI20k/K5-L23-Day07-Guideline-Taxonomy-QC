# Guideline gán nhãn đối tượng 2D — Phiên bản v1.0 (Thống nhất nhóm)

> **Tài liệu đặc tả kỹ thuật chính thức** được cả nhóm thống nhất tại Pha 2 sau khi đối chiếu, tranh luận và giải quyết các bất đồng từ các bản cá nhân, áp dụng cho toàn bộ 40 ảnh của bộ dữ liệu `data/images/`.

- **Phiên bản:** v1.0 (Agreed Baseline)
- **Ngày ban hành:** 2026-11-16
- **Nhóm thực hiện:** Group-01 (Thành viên: 111, 222, 333, 444)
- **Trạng thái:** Bản khóa (Locked) cho lượt gán độc lập Pha 3

---

## 1. Mục tiêu và Phạm vi ứng dụng

- **Hệ thống đích:** Huấn luyện và kiểm thử mô hình thị giác máy tính phát hiện đối tượng 2D (2D Object Detection) phục vụ:
  - Hệ thống hỗ trợ lái xe nâng cao và tự hành (ADAS/Autonomous Driving).
  - Hệ thống điều hành và giám sát giao thông thông minh đô thị (ITS).
- **Mục tiêu nhận diện:** Xác định vị trí (bounding box) và phân loại chính xác các **thực thể tham gia giao thông thực tế (dynamic traffic participants)** có khả năng tự chuyển động hoặc trực tiếp chiếm dụng không gian lòng đường.
- **Mức độ rủi ro khi gán sai:**
  - *Bỏ sót (False Negative - `bo_sot`):* Bỏ sót người đi bộ hoặc người đi xe máy/xe đạp là lỗi nguy hiểm nhất, dẫn tới nguy cơ va chạm gây tử vong trong điều khiển tự hành.
  - *Gán thừa trên vật thể phi thực (False Positive - `thua`):* Gán box lên tượng đài, tranh ảnh quảng cáo billboard, ma-nơ-canh, bóng phản chiếu sẽ gây ra hiện tượng phanh ảo (phantom braking) cực kỳ nguy hiểm trên xa lộ.
  - *Sai lệch kích thước / lỏng box (`sai_vi_tri_kich_thuoc`):* Gây ước lượng sai khoảng cách tiếp xúc (Time-to-Collision) và cự ly an toàn.

---

## 2. Danh mục Lớp và Thuộc tính (Taxonomy)

### 2.1. Danh mục 9 Lớp chuẩn

Mỗi đối tượng hợp lệ phải thuộc đúng **một lớp duy nhất**:

| Lớp | Định nghĩa chuẩn (1 câu) | Ví dụ thực tế trong 40 ảnh | Phản ví dụ / Tuyệt đối không gán |
|---|---|---|---|
| `car` | Xe ô tô con từ 4 đến 9 chỗ ngồi dùng chở người (sedan, SUV, hatchback, crossover, wagon, coupe). | Xe sedan trắng (`img_001`), xe sedan trong mưa (`img_015`), xe wagon (`img_024`), từng ô tô con trên sàn xe tải chở xe (`img_002`), xe diễu hành chế chạy trên phố (`img_019`). | Xe bán tải (`truck`), xe van chở hàng (`van`), tượng xe bia mộ (`img_027`), ô tô đồ chơi (`img_038`). |
| `truck` | Xe cơ giới chuyên dụng chở hàng có thùng hàng riêng biệt, xe đầu kéo, xe chuyên chở, xe bán tải (pickup) **và toàn bộ xe tải nhỏ / xe tải nhẹ**. | Xe chở xe Renault 380 (`img_002`), xe bán tải pickup (`img_001`, `img_012`), **bán tải màu trắng có nắp thùng cao composite (`img_037`)**, **xe tải nhẹ giao hàng (`img_007`, `img_036`)**. | Xe thùng kín thân liền một khối chở khách (`van`), ô tô con chở người (`car`), tượng xe đá (`img_027`). |
| `van` | Xe ô tô thân kín một khối cỡ nhỏ hoặc vừa chở khách hoặc bưu kiện nhẹ (minivan, blind van). | Xe chuyển phát nhanh bưu chính thân liền, minivan chở khách gia đình. | **Không gồm xe tải nhỏ** (toàn bộ xe tải nhỏ thuộc về `truck`), xe bán tải (`truck`), xe buýt cỡ lớn (`bus`). |
| `motorcycle` | Phương tiện cơ giới hai (2) hoặc ba (3) bánh có gắn động cơ (xe máy, mô tô phân khối lớn, xe ga, scooter, xe ba bánh có thùng bên sidecar). | Xe máy đường phố TP.HCM (`img_005`), xe máy chợ đêm (`img_008`), mô tô độ (`img_011`), xe trong hầm (`img_026`), **xe mô tô cổ có thùng bên sidecar (`img_022`)**. | Xe đạp thô sơ, xe xích lô (`bicycle`), xe tuk-tuk chở khách (`tuk_tuk`). |
| `bus` | Xe buýt hoặc xe khách chuyên dụng cỡ lớn chuyên chở nhiều hành khách. | Xe buýt lớn chở khách phía sau xích lô trong `img_009`, trạm dừng xe buýt `img_032`, giao thông Bangkok `img_040`. | Không gán nhầm vào `van` hay `truck` để tránh sai lệch hình thái và kích thước. |
| `bicycle` | Phương tiện thô sơ hai (2) hoặc ba (3) bánh chạy bằng sức người đạp, bao gồm cả **xe đạp và xe xích lô**. | Xe đạp thô sơ, **xe xích lô chở du khách tại Huế (`img_006`, `img_009`, `img_023`, `img_034`, `img_039`)**. | Xe máy có động cơ (`motorcycle`). Người đạp và hành khách ngồi trên xe xích lô/xe đạp gán thêm box `person`. |
| `tuk_tuk` | Xe cơ giới ba (3) bánh chở khách đặc thù có cabin mở (tuk-tuk, auto-rickshaw). | Hai chiếc tuk-tuk xanh (`img_004`), xe tuk-tuk phố Bangkok (`img_016`), xe auto-rickshaw (`img_035`). | Không gán ép vào `car` hay `motorcycle`. |
| `person` | Con người còn sống ở mọi tư thế: đi bộ, đứng, ngồi, lái xe hoặc ngồi sau phương tiện hở. | Người phụ nữ đứng cạnh xe (`img_001`), người đi xe máy (`img_005`, `img_026`), người qua đường (`img_014`), người cosplay Predator (`img_011`), người đạp xích lô và khách (`img_006`). | Tượng điêu khắc đá/đồng (`img_017`), hình ảnh người in trên pano quảng cáo (`img_018`), ma-nơ-canh (`img_033`), búp bê đồ chơi (`img_038`). |
| `ignore_region` | Vùng bỏ qua: cụm đám đông hoặc phương tiện ở rất xa ($<20\text{px}$) hoặc vùng hỗn loạn không gán từng vật. | Cụm người ở hậu cảnh bờ biển (`img_025`), cụm xe dồn toa mờ nhạt ở cuối đường chân trời (`img_008`). | Bất kỳ vật thể đơn lẻ nào nhìn rõ có chiều cao $\ge 20\text{px}$. |

---

### 2.2. Thuộc tính đối tượng (Attributes)

Nhóm thống nhất tối giản hóa thuộc tính: **Chuyển `occluded` và `truncated` về dạng giá trị Boolean nhị phân (`true` / `false`)**, không phân cấp theo level phần trăm (%) phức tạp:

| Thuộc tính | Kiểu / Giá trị | Mặc định | Định nghĩa & Ý nghĩa quy ước |
|---|---|---|---|
| `occluded` | `checkbox`<br>`[false, true]` | `false` | - `false`: Đối tượng nhìn thấy trọn vẹn bề mặt, không bị bất kỳ vật thể nào khác che chắn.<br>- `true`: Đối tượng bị che khuất một phần bất kỳ bởi vật thể khác phía trước (xe trước, vỉa hè, cột đèn, hàng hóa...). Không cần đo % diện tích. |
| `truncated` | `checkbox`<br>`[false, true]` | `false` | - `false`: Toàn bộ đối tượng nằm hoàn toàn bên trong khung hình.<br>- `true`: Đối tượng bị cắt ngang bởi ít nhất một trong bốn mép biên của ảnh (trái, phải, trên, dưới). Không cần đo % diện tích. |
| `can_review` | `checkbox`<br>`[false, true]` | `false` | - `false`: Box rõ ràng, chuẩn theo quy tắc.<br>- `true`: Tick chọn khi annotator còn phân vân về ranh giới hoặc phân lớp để đưa ra thảo luận tại phiên Calibration. |

---

## 3. Quy tắc vẽ Bounding Box (Gắn mã `R-01` đến `R-09`)

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
| `v1.0` | Cả nhóm thống nhất | - Bổ sung các lớp: `bus`, `bicycle` (gồm cả xích lô), `tuk_tuk`.<br>- Chuyển xe tải nhỏ từ `van` sang `truck` (`img_036.jpg` là `truck`).<br>- Thống nhất `motorcycle` bao gồm cả 2 và 3 bánh (`img_022.jpg` gán `motorcycle` gộp sidecar).<br>- Tối giản thuộc tính: `occluded` và `truncated` chuyển về `true`/`false`, bỏ chia cấp độ %.<br>- Gắn mã quy tắc chính thức từ `R-01` đến `R-09`.<br>- Chốt các ca khó trọng tâm: `img_037.jpg` gán `truck`, `img_022.jpg` gán `motorcycle` không tách. | Họp nhóm thống nhất Pha 2. |
