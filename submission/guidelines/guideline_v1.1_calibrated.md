# Guideline gán nhãn đối tượng 2D — Phiên bản v1.1 (Calibrated Final)

> **Tài liệu đặc tả kỹ thuật chính thức v1.1** được toàn nhóm Group-01 hiệu chuẩn, hoàn thiện và đóng băng sau phiên Calibration Pha 5, giải quyết triệt để 399 ca bất thường và bất đồng IAA từ 4 lượt gán độc lập.

- **Phiên bản:** v1.1 (Calibrated Baseline)
- **Ngày ban hành:** 2026-11-17
- **Nhóm thực hiện:** Group-01 (Thành viên: 111, 222, 333, 444)
- **Trạng thái:** Bản khóa chính thức (Final Locked) nghiệm thu và bàn giao

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

## 2. Danh mục 9 Lớp và 3 Thuộc tính chuẩn (Taxonomy v1.1)

### 2.1. Danh mục 9 Lớp chuẩn

| Lớp | Định nghĩa chuẩn (1 câu) | Ví dụ thực tế trong 40 ảnh | Phản ví dụ / Tuyệt đối không gán |
|---|---|---|---|
| `car` | Xe ô tô con từ 4 đến 9 chỗ ngồi dùng chở người (sedan, SUV, hatchback, crossover, wagon, coupe). | Xe sedan trắng (`img_001`), xe sedan trong mưa (`img_015`), xe wagon (`img_024`), từng ô tô con trên sàn xe tải chở xe (`img_002`), xe diễu hành chế chạy trên phố (`img_019`). | Xe bán tải (`truck`), xe van chở hàng (`van`), tượng xe bia mộ (`img_027`), ô tô đồ chơi (`img_038`). |
| `truck` | Xe cơ giới chuyên dụng chở hàng có thùng hàng riêng biệt, xe đầu kéo, xe chuyên chở, xe bán tải (pickup) **và toàn bộ xe tải nhỏ / xe tải nhẹ**. | Xe chở xe Renault 380 (`img_002`), xe bán tải pickup (`img_001`, `img_012`), **bán tải màu trắng có nắp thùng cao composite (`img_037`)**, **xe tải nhẹ giao hàng (`img_007`, `img_036`)**. | Xe thùng kín thân liền một khối chở khách (`van`), ô tô con chở người (`car`), tượng xe đá (`img_027`). |
| `van` | Xe ô tô thân kín một khối cỡ nhỏ hoặc vừa chở khách hoặc bưu kiện nhẹ (minivan, blind van). | Xe chuyển phát nhanh bưu chính thân liền, minivan chở khách gia đình. | **Không gồm xe tải nhỏ** (toàn bộ xe tải nhỏ thuộc về `truck`), xe bán tải (`truck`), xe buýt cỡ lớn (`bus`). |
| `motorcycle` | Phương tiện cơ giới hai (2) hoặc ba (3) bánh có gắn động cơ (xe máy, mô tô phân khối lớn, xe ga, scooter, xe ba bánh có thùng bên sidecar). | Xe máy đường phố TP.HCM (`img_005`), xe máy chợ đêm (`img_008`), mô tô độ (`img_011`), xe trong hầm (`img_026`), **xe mô tô cổ có thùng bên sidecar (`img_022`)**. | Xe đạp thô sơ, xe xích lô (`bicycle`), xe tuk-tuk chở khách (`tuk_tuk`). |
| `bus` | Xe buýt hoặc xe khách chuyên dụng cỡ lớn chuyên chở nhiều hành khách. | Xe buýt lớn chở khách phía sau xích lô trong `img_009`, trạm dừng xe buýt `img_032`, giao thông Bangkok `img_040`. | Không gán nhầm vào `van` hay `truck` để tránh sai lệch hình thái và kích thước. |
| `bicycle` | Phương tiện thô sơ hai (2) hoặc ba (3) bánh chạy bằng sức người đạp, bao gồm cả **xe đạp và xe xích lô**. | Xe đạp thô sơ, **xe xích lô chở du khách tại Huế (`img_006`, `img_009`, `img_023`, `img_034`, `img_039`)**. | Xe máy có động cơ (`motorcycle`). Người đạp và hành khách ngồi trên xe xích lô/xe đạp gán thêm box `person`. |
| `tuk_tuk` | Xe cơ giới ba (3) bánh chở khách đặc thù có cabin mở (tuk-tuk, auto-rickshaw). | Hai chiếc tuk-tuk xanh (`img_004`), xe tuk-tuk phố Bangkok (`img_016`, `img_040`), xe auto-rickshaw (`img_035`). | Không gán ép vào `car` hay `motorcycle`. |
| `person` | Con người còn sống ở mọi tư thế: đi bộ, đứng, ngồi, lái xe hoặc ngồi sau phương tiện hở. | Người phụ nữ đứng cạnh xe (`img_001`), người đi xe máy (`img_005`, `img_026`), người qua đường (`img_014`), người cosplay Predator (`img_011`), người đạp xích lô và khách (`img_006`). | Tượng điêu khắc đá/đồng (`img_017`), hình ảnh người in trên pano quảng cáo (`img_018`), ma-nơ-canh (`img_033`), búp bê đồ chơi (`img_038`). |
| `ignore_region` | Vùng bỏ qua: cụm đám đông hoặc phương tiện ở rất xa ($<20\text{px}$) hoặc vùng hỗn loạn không gán từng vật. | Cụm người ở hậu cảnh bờ biển (`img_025`), cụm khán giả xem diễu hành ở xa (`img_019`), cụm xe dồn toa mờ nhạt ở cuối đường chân trời (`img_008`). | Bất kỳ vật thể đơn lẻ nào nhìn rõ có chiều cao $\ge 20\text{px}$. |

---

### 2.2. Thuộc tính đối tượng (Attributes)

| Thuộc tính | Kiểu / Giá trị | Mặc định | Định nghĩa & Ý nghĩa quy ước |
|---|---|---|---|
| `occluded` | `checkbox`<br>`[false, true]` | `false` | - `false`: Đối tượng nhìn thấy trọn vẹn bề mặt, không bị bất kỳ vật thể nào khác che chắn.<br>- `true`: Đối tượng bị che khuất một phần bất kỳ bởi vật thể khác phía trước. |
| `truncated` | `checkbox`<br>`[false, true]` | `false` | - `false`: Toàn bộ đối tượng nằm hoàn toàn bên trong khung hình.<br>- `true`: Đối tượng bị cắt ngang bởi ít nhất một trong bốn mép biên của ảnh (trái, phải, trên, dưới). |
| `can_review` | `checkbox`<br>`[false, true]` | `false` | Mặc định `false`. Sau phiên Calibration, 100% cờ `can_review` đều được giải tỏa về `false`. |

---

## 3. Quy chuẩn 9 Quy tắc gán nhãn chính thức (`R-01` đến `R-09`)

- **`R-01` (Ôm sát phần nhìn thấy - Tight Visual Boundary):**
  - Bounding box là hình chữ nhật nhỏ nhất bao trọn toàn bộ điểm ảnh nhìn thấy được (visible pixels) của vật. Bắt buộc clamp sát tọa độ $[0, 0, width, height]$.
- **`R-02` (Loại trừ đối tượng phi thực tế - Non-real Objects):**
  - Tuyệt đối không gán box cho tượng đài đồng/đá (`img_017`, `img_027`), ảnh in pano quảng cáo (`img_018`), gương phản chiếu (`img_020`), ma-nơ-canh tủ kính (`img_033`), đồ chơi mô hình (`img_038`).
- **`R-03` (Xe chở xe - Car Carrier):**
  - Với xe chuyên dụng chở ô tô (`img_002`): 1 box `truck` cho xe tải lớn + từng box `car` riêng cho mỗi ô tô con xếp trên 2 tầng giàn.
- **`R-04` (Người và phương tiện 2-3 bánh - Rider & Vehicle):**
  - Xe máy tách riêng `motorcycle` và `person`. Xích lô gán `bicycle` + `person` cho người đạp và khách. Xe mô tô sidecar (`img_022`) gán 1 box `motorcycle` gộp thân và thùng bên, người ngồi gán `person` riêng.
- **`R-05` (Phân định Xe tải nhỏ vs Xe van):**
  - Toàn bộ xe tải nhỏ/nhẹ có thùng hàng tách rời cabin (như CMC Veryca trong `img_036`) xếp vào `truck`.
- **`R-06` (Xe bán tải có nắp thùng cao):**
  - Xe bán tải gắn nắp thùng cao composite trong `img_037` được thống nhất xếp vào `truck`.
- **`R-07` (Hàng hóa cồng kềnh trên xe ba bánh / tuk-tuk):**
  - Box `tuk_tuk` ôm sát khung xe cơ giới; không bao đống hàng hóa cồng kềnh chất trên nóc (`img_035`).
- **`R-08` (Khung vỏ xe gắn trên nóc phương tiện):**
  - Vỏ xe trên nóc AMC Pacer trong `img_024` coi là hàng hóa, chỉ gán 1 box `car` cho xe đang lăn bánh.
- **`R-09` (Kích thước tối thiểu & Gom cụm đám đông):**
  - Chiều cao $< 20\text{px}$ không gán box đơn lẻ. Đám đông khán giả ở xa (`img_019`, `img_025`) gom vào `ignore_region`.

---

## 4. Bảng quyết định và Lịch sử phiên bản

| Phiên bản | Người cập nhật | Nội dung cập nhật chính |
|---|---|---|
| `v1.0` | Cả nhóm Group-01 | Thống nhất 9 lớp chuẩn, 3 thuộc tính nhị phân boolean, mã hóa 9 quy tắc `R-01` -> `R-09`. |
| `v1.1` | Cả nhóm Group-01 | Hiệu chuẩn sau phiên Calibration Pha 5: giải quyết 399 ca IAA, đồng thuận 100% về xích lô (`bicycle`), giải tỏa toàn bộ cờ `can_review`, đóng băng dữ liệu bàn giao. |
