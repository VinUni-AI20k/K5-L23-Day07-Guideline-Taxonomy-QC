# Guideline gán nhãn đối tượng 2D — Phiên bản v1.0 (Thống nhất nhóm)

> **Tài liệu đặc tả kỹ thuật chính thức** được cả nhóm thống nhất tại Pha 2 sau khi đối chiếu, tranh luận và giải quyết các bất đồng từ các bản cá nhân, áp dụng cho toàn bộ 40 ảnh của bộ dữ liệu `data/images/`.

- **Phiên bản:** v1.0 (Agreed Baseline)
- **Ngày ban hành:** 2026-11-16
- **Nhóm thực hiện:** Group-01 (Thành viên: 111, 222, 444)
- **Trạng thái:** Bản khóa (Locked) cho lượt gán độc lập Pha 3

---

## 1. Mục tiêu và Phạm vi ứng dụng

- **Hệ thống đích:** Huấn luyện và kiểm thử mô hình thị giác máy tính phát hiện đối tượng 2D (2D Object Detection) phục vụ:
  - Hệ thống hỗ trợ lái xe nâng cao và tự hành (ADAS/Autonomous Driving).
  - Hệ thống điều hành và giám sát giao thông thông minh đô thị (ITS).
- **Mục tiêu nhận diện:** Xác định vị trí (bounding box) và phân loại chính xác các **thực thể tham gia giao thông thực tế (dynamic traffic participants)** có khả năng tự chuyển động hoặc trực tiếp chiếm dụng không gian lòng đường.
- **Mức độ rủi ro khi gán sai:**
  - *Bỏ sót (False Negative - `bo_sot`):* Bỏ sót người đi bộ hoặc người đi xe máy là lỗi nguy hiểm nhất, dẫn tới nguy cơ va chạm gây tử vong trong điều khiển tự hành.
  - *Gán thừa trên vật thể phi thực (False Positive - `thua`):* Gán box lên tượng đài, tranh ảnh quảng cáo billboard, ma-nơ-canh, bóng phản chiếu sẽ gây ra hiện tượng phanh ảo (phantom braking) cực kỳ nguy hiểm trên xa lộ.
  - *Sai lệch kích thước / lỏng box (`sai_vi_tri_kich_thuoc`):* Gây ước lượng sai khoảng cách tiếp xúc (Time-to-Collision) và cự ly an toàn.

---

## 2. Danh mục Lớp và Thuộc tính (Taxonomy)

### 2.1. Danh mục 6 Lớp chuẩn

Mỗi đối tượng hợp lệ phải thuộc đúng **một lớp duy nhất**:

| Lớp | Định nghĩa chuẩn (1 câu) | Ví dụ thực tế | Phản ví dụ / Tuyệt đối không gán |
|---|---|---|---|
| `car` | Xe ô tô con từ 4 đến 9 chỗ ngồi dùng chở người (sedan, SUV, hatchback, crossover, wagon, coupe). | Xe sedan trong mưa (`img_015`), xe wagon (`img_024`), từng ô tô con trên sàn xe tải (`img_002`), xe diễu hành chế chạy trên phố (`img_019`). | Xe bán tải (`truck`), xe van chở hàng (`van`), tượng xe bia mộ (`img_027`), ô tô đồ chơi (`img_038`). |
| `truck` | Xe cơ giới chuyên dụng chở hàng có thùng hàng riêng biệt, xe đầu kéo, xe chuyên chở và xe bán tải (pickup). | Xe chở xe Renault 380 (`img_002`), xe bán tải pickup (`img_001`, `img_012`), bán tải có nắp thùng ngủ/thùng cao (`img_037`), xe tải nhẹ giao hàng (`img_007`, `img_036`). | Xe thùng kín thân liền một khối (`van`), ô tô con chở người (`car`), tượng xe đá (`img_027`). |
| `van` | Xe ô tô thân kín một khối cỡ nhỏ hoặc vừa chở khách hoặc bưu kiện nhẹ (minivan, blind van). | Xe chuyển phát nhanh bưu chính thân liền, minivan chở khách gia đình. | Xe bán tải có nắp thùng cao composite (`truck`), SUV cỡ lớn (`car`), xe buýt cỡ lớn (`img_032`). |
| `motorcycle` | Phương tiện cơ giới hai bánh (xe máy, mô tô phân khối lớn, xe ga, scooter) và xe ba bánh có thùng bên (sidecar). | Xe máy đường phố TP.HCM (`img_005`), xe máy chợ đêm (`img_008`), mô tô độ (`img_011`), xe trong hầm (`img_026`), xe sidecar (`img_022`). | Xe đạp thô sơ, xe xích lô (`img_006`, `img_009`), xe tuk-tuk 3 bánh (`img_004`, `img_035`). |
| `person` | Con người còn sống ở mọi tư thế: đi bộ, đứng, ngồi, lái xe hoặc ngồi sau phương tiện hở. | Người phụ nữ đứng cạnh xe (`img_001`), người đi xe máy (`img_005`, `img_026`), người qua đường (`img_014`), người cosplay Predator (`img_011`). | Tượng điêu khắc đá/đồng (`img_017`), hình ảnh người in trên pano quảng cáo (`img_018`), ma-nơ-canh (`img_033`), búp bê đồ chơi (`img_038`). |
| `ignore_region` | Vùng bỏ qua: cụm đám đông hoặc phương tiện ở rất xa ($<20\text{px}$) hoặc vùng hỗn loạn không gán từng vật. | Cụm người ở hậu cảnh bờ biển (`img_025`), cụm xe dồn toa mờ nhạt ở cuối đường chân trời. | Bất kỳ vật thể đơn lẻ nào nhìn rõ có chiều cao $\ge 20\text{px}$. |

### 2.2. Quy ước xử lý đối tượng ngoài danh mục v1.0
- **Xe Tuk-tuk / Auto Rickshaw (`img_004`, `img_035`):** Phương tiện cơ giới 3 bánh chở khách. Tạm thời phân loại vào lớp **`car`** (do có cabin bảo vệ hành khách và động cơ cơ giới), đồng thời **bắt buộc tick `can_review=true`** để theo dõi hiệu chỉnh ở Pha 5.
- **Xích lô / Cyclo (`img_006`, `img_009`, `img_023`, `img_034`, `img_039`):** Phương tiện thô sơ đạp bằng chân. **Chỉ gán `person`** cho người đạp xe và du khách ngồi trên xích lô; bản thân chiếc xe xích lô **KHÔNG gán box** (nếu cụm xích lô quá đông gây rối thì phủ `ignore_region`).
- **Xe buýt công cộng / Bus (`img_032`):** Phương tiện chở khách cỡ lớn. Tạm thời phân loại vào **`truck`** (nhóm xe thương mại tải trọng lớn), đồng thời **tick `can_review=true`**.

### 2.3. Hệ thống Thuộc tính (Attributes) với Định lượng chuẩn

| Thuộc tính | Kiểu dữ liệu | Giá trị | Định lượng chi tiết & Ngưỡng đo lường |
|---|---|---|---|
| `occluded_level` | Select | `0`, `1`, `2`, `3` | **Tỷ lệ diện tích bề mặt vật thể bị che khuất:**<br/>- `0`: Không che khuất (diện tích bị che $< 10\%$).<br/>- `1`: Bị che khuất nhẹ ($10\% \le \text{che} \le 35\%$).<br/>- `2`: Bị che khuất đáng kể ($35\% < \text{che} \le 80\%$).<br/>- `3`: Bị che khuất nghiêm trọng ($> 80\%$, chỉ còn thấy một phần nhỏ nhận diện được qua ngữ cảnh). |
| `truncated` | Select | `no`, `yes` | **Bị cắt mép ảnh:**<br/>- `no`: Toàn bộ vật thể nằm trọn vẹn bên trong khung ảnh.<br/>- `yes`: Viền ngoài của vật thể bị cắt ngang bởi ít nhất một cạnh viền ảnh ($x=0, y=0, x=W, y=H$). |
| `can_review` | Checkbox | `true`, `false` | **Đánh dấu cần xem xét lại:** Tick `true` với tất cả các ca ngoài taxonomy (Tuk-tuk, Xe buýt), xe chở hàng quá khổ dị thường, xe mờ trong mưa, hoặc ranh giới phân vân. |

---

## 3. Hệ thống Quy tắc vẽ Bounding Box (Core Rules)

Mọi annotator phải tuân thủ nghiêm ngặt 10 quy tắc kỹ thuật sau:

* **`R-01` — Nguyên tắc Modal Bounding Box (Chỉ ôm pixel nhìn thấy):** Bounding box là hình chữ nhật nhỏ nhất bao quanh toàn bộ các điểm ảnh thực tế nhìn thấy được của vật thể. Tuyệt đối **không vẽ ước lượng (Amodal)** bao trùm phần bị vật cản khác che khuất.
* **`R-02` — Phân tách Người và Phương tiện hở (Rider & Motorcycle):**
  - Khi có người điều khiển hoặc ngồi trên xe máy (`motorcycle`): Bắt buộc vẽ **2 box riêng biệt**:
    1. Box `person`: Ôm trọn cơ thể người từ đỉnh nón bảo hiểm đến bàn chân đặt trên để chân (cho phép chồng lên thân xe).
    2. Box `motorcycle`: Ôm trọn chiếc xe từ bánh trước, bánh sau đến đuôi xe.
  - Xe chở 2 người (`img_026`): Vẽ **3 box độc lập** (2 box `person` cho 2 người và 1 box `motorcycle` cho xe).
* **`R-03` — Loại trừ Người trong Phương tiện kín (Cabin Exclusion):**
  - Người ngồi bên trong ô tô con (`car`), cabin xe tải (`truck`), hoặc xe thùng (`van`) nhìn qua kính chắn gió: **KHÔNG vẽ box `person`**. Chiếc xe được coi là một thực thể bao trùm toàn bộ không gian bên trong.
* **`R-04` — Xe máy có ghế/thùng bên hông (Sidecar — `img_022`):**
  - Gán **1 box `motorcycle` duy nhất** bao trọn toàn bộ cụm phương tiện (khung xe máy 2 bánh + thùng thuyền bên hông).
  - Người lái xe máy: 1 box `person`.
  - Người ngồi trong thùng thuyền bên: 1 box `person` riêng (đánh dấu `occluded_level=1` hoặc `2`).
* **`R-05` — Xe bán tải có chỗ ngủ tích hợp / Nắp thùng cao (`img_037`):**
  - Gán nhãn **`truck`**, box bao trọn cả cabin xe và phần nắp thùng ngủ/thùng cao composite tích hợp phía sau.
* **`R-06` — Xe chở xe chuyên dụng (Car Carrier — `img_002`):**
  - Vẽ 1 box `truck` bao toàn bộ chiếc xe tải chuyên dụng (kể cả khung sàn rơ-moóc chở xe).
  - Vẽ từng box `car` riêng cho từng chiếc ô tô con đang nằm trên sàn xe nếu chiều cao $\ge 20\text{px}$ (đánh dấu `occluded_level=1` hoặc `2` do bị khung sắt che).
* **`R-07` — Hàng hóa trên phương tiện & Hàng quá khổ (`img_012`, `img_029`):**
  - Hàng hóa nằm trong lòng thùng xe tải/bán tải (`img_012`): Box `truck` bao trọn cả phần hàng hóa trong thùng.
  - Xe máy chở hàng cồng kềnh dài hơn xe (`img_029`): Box `motorcycle` **chỉ bao trọn phần khung xe máy thực tế** nhìn thấy; phần hàng hóa cồng kềnh nhô ra ngoài không tính vào xe, đồng thời bắt buộc tick `can_review=true`.
* **`R-08` — Bài trừ Thực thể phi thực & Phản chiếu ảo (Tránh lỗi `thua`):**
  - **TUYỆT ĐỐI KHÔNG GÁN NHÃN** cho: Tượng điêu khắc đá/đồng (`img_017`, `img_027`), hình ảnh người in trên pano quảng cáo (`img_018`), ma-nơ-canh trước cửa hàng (`img_033`), mô hình đồ chơi/búp bê trong tủ kính (`img_038`), và hình ảnh phản chiếu qua gương chiếu hậu (`img_020`).
  - **Ngoại lệ:** Người mặc trang phục hóa trang (Cosplay Predator — `img_011`): **VẪN GÁN `person`** vì đây là người thật đang sống tham gia hoạt động trên đường phố.
* **`R-09` — Xe quá mờ do mưa, tốc độ, thiếu sáng (`img_013`, `img_015`):**
  - Nếu mắt người vẫn nhận diện được hình bóng (silhouette) và xác định được ranh giới tương đối: **Vẫn vẽ box**, đánh dấu `occluded_level=3` và tick `can_review=true`.
  - Nếu xe quá mờ, vỡ nét hoàn toàn không thể xác định biên giới: **Không vẽ box đơn lẻ**. Nếu là một vùng nhiều xe mờ ở xa: khoanh vùng gán lớp `ignore_region`.
* **`R-10` — Đám đông xe máy & Ngưỡng kích thước nhỏ (`img_005`, `img_008`, `img_030`):**
  - Tiền cảnh & Trung cảnh (chiều cao $\ge 20\text{px}$): Kiên trì vẽ tách từng cặp box (1 `person` + 1 `motorcycle`). Box chồng lấn nhau là bình thường, đánh dấu `occluded_level=1` hoặc `2`.
  - Hậu cảnh xa (chiều cao $< 20\text{px}$ hoặc dồn cục không rõ biên): Vẽ box bao quanh toàn cụm và gán lớp `ignore_region`.
  - Vật đơn lẻ $< 20\text{px}$: Không vẽ box lẻ.

---

## 4. Bảng tra cứu các ca điển hình từ 40 ảnh thực tế

| ID Ảnh | Mô tả tình huống thực tế | Rule ID | Quyết định kỹ thuật của nhóm | Lập luận căn cứ |
|---|---|---|---|---|
| `img_001` | Người phụ nữ đứng cạnh xe bán tải | `R-01`, `R-02` | 1 box `person` (người phụ nữ), 1 box `truck` (xe bán tải). | Bán tải có thùng riêng thuộc `truck`; người đứng tách biệt có box riêng. |
| `img_002` | Xe chuyên dụng chở nhiều ô tô con | `R-06` | 1 box `truck` cho xe chuyên chở; các box `car` riêng cho từng xe con trên sàn ($\ge 20\text{px}$). | Nhận diện cả phương tiện chuyên chở lẫn đối tượng ô tô con đang vận chuyển. |
| `img_004` | Hai xe Tuk-tuk màu xanh đỗ trên vỉa hè | `R-01` | Gán `car`, tick `can_review=true`. | Cơ giới 3 bánh có cabin, tạm quy ước `car` theo taxonomy v1.0. |
| `img_005` | Đoàn xe máy dày đặc tại TP.HCM | `R-02`, `R-10` | Tách độc lập từng box `person` và `motorcycle`. Hậu cảnh xa $< 20\text{px}$ gom vào `ignore_region`. | Đảm bảo tính nhất quán, tránh bỏ sót người tham gia giao thông. |
| `img_006` | Xích lô chở du khách tại Huế | `R-01` | Chỉ gán `person` cho người đạp và du khách; xe xích lô không gán box. | Xích lô là xe thô sơ không thuộc taxonomy phương tiện cơ giới. |
| `img_011` | Cosplay Predator đứng cạnh mô tô độ | `R-08`, `R-02` | 1 box `person` (Predator), 1 box `motorcycle` (xe mô tô độ). | Người thật mặc đồ hóa trang vẫn là thực thể sống tham gia giao thông. |
| `img_012` | Xe bán tải chở đầy rau củ trên thùng | `R-07` | 1 box `truck` bao trọn cả xe và khối rau củ trên thùng. | Hàng trong thùng là một phần thể tích chuyên chở của phương tiện. |
| `img_017` | Tượng kỵ sĩ Duke of Wellington | `R-08` | **KHÔNG GÁN** nhãn `person` hay phương tiện. | Tượng điêu khắc bằng đồng không phải thực thể sống, gán sẽ bị phạt lỗi `thua`. |
| `img_018` | Pano quảng cáo in chân dung chính khách | `R-08` | **KHÔNG GÁN** nhãn `person`. | Hình ảnh 2D tĩnh trên biển bảng không tham gia giao thông. |
| `img_020` | Cầu vồng và xe trong gương chiếu hậu | `R-08` | **KHÔNG GÁN** nhãn xe trong mặt kính gương. | Ảnh ảo quang học phản chiếu qua gương. |
| `img_022` | Xe máy cổ có thùng bên (Sidecar) | `R-04` | 1 box `motorcycle` bao toàn bộ thân xe và thùng bên; box `person` cho người ngồi. | Sidecar là biến thể 3 bánh gắn liền của xe mô tô. |
| `img_026` | Cặp đôi đi chung xe máy trong hầm | `R-02` | 2 box `person` (2 người), 1 box `motorcycle` (chiếc xe). | Hai con người độc lập có nguy cơ chấn thương riêng biệt khi va chạm. |
| `img_027` | Bia mộ đá hoa cương hình xe bán tải | `R-08` | **KHÔNG GÁN** nhãn `truck` hay `car`. | Khối đá điêu khắc tĩnh trong nghĩa trang không phải phương tiện giao thông. |
| `img_029` | Xe máy chở hàng khổng lồ quá khổ | `R-07`, `R-02` | 1 `person`, 1 `motorcycle` ôm thân xe; tick `can_review=true`. | Kiện hàng dị biệt làm biến dạng biên xe, cần đưa ra hiệu chỉnh tập thể. |
| `img_032` | Xe buýt công cộng tại trạm dừng | `R-01` | Gán `truck`, tick `can_review=true`. | Xe chở khách cỡ lớn, tạm thời xếp vào nhóm xe thương mại nặng. |
| `img_033` | Ma-nơ-canh trước cửa hàng thời trang | `R-08` | **KHÔNG GÁN** nhãn `person`. | Vật vô tri giả lập con người, gán sẽ gây lỗi phanh ảo. |
| `img_036` | Xe tải nhẹ CMC Veryca thùng lửng | `R-01` | Gán `truck`. | Xe tải nhẹ có thùng hàng riêng biệt thuộc `truck`. |
| `img_037` | Xe bán tải có nắp thùng cao composite | `R-05` | Gán `truck`. | Khung gầm bán tải gắn thêm nắp phụ kiện vẫn là `truck`. |
| `img_038` | Tủ kính bày đồ chơi, xe mô hình | `R-08` | **KHÔNG GÁN** `car` hay `person`. | Đồ chơi trong nhà/trong tủ kính không tham gia giao thông. |

---

## 5. Thống nhất và Giải quyết Bất đồng giữa các thành viên

Trong phiên họp Pha 2, nhóm đã ghi nhận và giải quyết các điểm bất đồng ban đầu như sau:

1. **Về việc gán người trong ô tô kín:** 
   - *Ý kiến ban đầu:* Thành viên 445 đề xuất nếu nhìn thấy rõ tài xế qua kính lái thì vẫn nên gán `person`.
   - *Quyết định thống nhất của nhóm:* Tuân thủ quy tắc `R-03` (Cabin Exclusion) — không gán `person` cho người ngồi trong xe kín. Lý do: tránh tạo ra các box chồng chéo không cần thiết và giúp detector tập trung vào bảo vệ người đi bộ và người đi xe hở (vulnerable road users).
2. **Về xe Tuk-tuk (`img_004`) và Xe buýt (`img_032`):**
   - *Ý kiến ban đầu:* Đề xuất sửa đổi taxonomy ngay lập tức để thêm lớp `bus` và `tuktuk`.
   - *Quyết định thống nhất của nhóm:* Không vội sửa đổi schema ở v1.0 để giữ tính tương thích với project ban đầu; tạm quy ước vào `car`/`truck` và gắn cờ `can_review=true`. Nếu ở Pha 4-5 phát sinh bất đồng lớn, nhóm sẽ nâng cấp taxonomy ở `v1.1`.
3. **Về tượng và ma-nơ-canh:**
   - *Thống nhất 100%:* Cả nhóm đồng thuận tuyệt đối loại trừ tượng, ảnh in và ma-nơ-canh theo quy định tránh lỗi `thua` của lab.

---

## 6. Tiêu chí Kiểm định Chất lượng (QC Targets)
- **IoU chấp nhận:** $\ge 0.85$ với vật lớn ($\ge 50\text{px}$); $\ge 0.70$ với vật nhỏ ($< 50\text{px}$).
- **Độ đồng thuận IAA:** IoU trung bình $\ge 0.85$, tỷ lệ cùng lớp $\ge 95\%$.
- **Tỷ lệ lỗi theo ảnh để Release:** $\le 2\%$ trên toàn bộ 40 ảnh.
