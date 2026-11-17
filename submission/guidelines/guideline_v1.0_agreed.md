# Guideline gán nhãn — v1.0 — Thống nhất nhóm (101, 102, 103, 104)

> **Bản đặc tả gán nhãn chính thức v1.0 của nhóm**, được hợp nhất từ 4 bản guideline cá nhân (`guideline_101.md`, `guideline_102.md`, `guideline_103.md`, `guideline_104.md`) sau phiên họp giải quyết toàn bộ các bất đồng ở Pha 2 và thống nhất bổ sung các lớp phương tiện thực tế (`bus`, `tuk_tuk`, và lớp `bicycle` gộp chung xe đạp & xích lô). Bản này được **khóa cứng** để cả 4 thành viên thực hiện lượt gán nhãn mù đôi độc lập ở Pha 3.

- **Phiên bản:** `v1.0`
- **Ngày thống nhất:** 2026-11-16
- **Thành viên tham gia:** `101`, `102`, `103`, `104`
- **Phạm vi áp dụng:** Bộ dữ liệu 40 ảnh giao thông đường phố (`data/images/img_001.jpg` đến `img_040.jpg`)
- **Định dạng nhãn & Công cụ:** CVAT, xuất COCO 1.0 (Bounding Box 2D trục đứng `[x, y, width, height]`)

---

## 1. Mục tiêu

- **Mục đích mô hình:** Huấn luyện và đánh giá mô hình phát hiện đối tượng 2D (2D Bounding Box Detection) phục vụ bài toán nhận diện giao thông đô thị, giám sát camera giao thông thông minh (ITS) và hỗ trợ lái xe tự động (ADAS / Autonomous Driving) trong điều kiện đường phố đô thị hỗn hợp.
- **Rủi ro an toàn và tác động khi gán sai:**
  - *Bỏ sót (`bo_sot` - False Negative):* Bỏ sót người đi bộ (`person`), người đi xe đạp/xích lô (`bicycle` + `person`) hoặc người đi xe máy (`motorcycle`) là lỗi đặc biệt nghiêm trọng, có thể dẫn đến việc hệ thống tự lái không kích hoạt phanh và gây va chạm chết người trực tiếp.
  - *Gán thừa vật giả / ảo (`thua` - False Positive):* Gán nhầm tượng đài, hình người in trên biển quảng cáo, ma-nơ-canh, đồ chơi hoặc hình phản chiếu qua gương chiếu hậu sẽ khiến hệ thống nhận dạng nhầm là chướng ngại vật thật, kích hoạt hiện tượng **phanh gấp ảo** (*phantom braking*), gây tai nạn dồn toa từ các phương tiện phía sau.
  - *Sai lệch vị trí / kích thước / gộp box (`sai_vi_tri_kich_thuoc`):* Gộp chung người lái và xe máy/xe đạp thành một box duy nhất, hoặc kéo box phình to ôm cả hàng hóa cồng kềnh ngoài phạm vi sẽ làm mô hình ước tính sai khổ rộng an toàn và khoảng cách vật lý của phương tiện.

---

## 2. Lớp và thuộc tính

### 2.1. Phân loại lớp đối tượng (`classes`)

Nhóm đã thống nhất mở rộng danh mục lên **9 lớp chuẩn** (bổ sung `bus`, `tuk_tuk`, và **gộp xe đạp & xe xích lô vào 1 lớp duy nhất là `bicycle`** để giải quyết triệt để toàn bộ các phương tiện xuất hiện trong 40 ảnh).

| Lớp | Định nghĩa chuẩn (một câu) | Ví dụ thực tế trong 40 ảnh | Phản ví dụ / Dễ nhầm lẫn |
|---|---|---|---|
| `car` | Ô tô con chở người từ 4 đến 9 chỗ ngồi (sedan, hatchback, SUV, crossover, wagon, taxi). | Ô tô con trên phố; taxi trắng `img_031`, taxi vàng/hồng `img_040`; wagon AMC Pacer `img_024`; xe cơ sở diễu hành `img_019`. | Xe bán tải pickup (`truck`); xe van thùng kín (`van`); xe mô hình đồ chơi trên kệ `img_037`, `img_038` (**không gán**). |
| `truck` | Xe tải chở hàng, xe đầu kéo, xe chuyên chở và **xe bán tải (pickup truck)** có khoang cabin tách rời thùng/sàn chở phía sau. | Xe chuyên chở ô tô `img_002`; xe bán tải đỗ trước quán `img_001`, `img_012`, `img_028`; xe tải nhẹ CMC Veryca `img_036`; bán tải nắp thùng cao Master 75 `img_037`. | Tượng đá hình xe bán tải ở nghĩa trang `img_027` (**không gán**); xe van thùng kín liền khối (`van`); SUV 7 chỗ (`car`). |
| `van` | Xe thùng kín liền một khối từ cabin đến đuôi xe, chuyên chở hàng hóa hoặc chở khách 9-16 chỗ (minivan, panel van, xe cứu thương). | Minivan màu bạc chạy ngang đường `img_005`; xe van cứu thương/chuyên dụng `img_011`. | Xe bán tải có nắp thùng cao `img_036`, `img_037` (vẫn là `truck` vì cabin tách rời thùng); xe buýt cỡ lớn (`bus`). |
| `bus` | Xe buýt công cộng, xe khách cỡ lớn hoặc minibus chở nhiều hành khách. | Xe buýt lớn phía sau đoàn xích lô `img_009`; xe buýt tại ngã tư `img_031`; xe buýt tại trạm dừng `img_032`; xe buýt trên đại lộ `img_040`. | Minivan 7-9 chỗ liền khối (`van`); xe tải thùng kín (`truck`). |
| `tuk_tuk` | Xe cơ giới ba bánh chở khách hoặc chở hàng có buồng lái hở và động cơ (tuk-tuk, auto-rickshaw, xe lam). | 2 xe tuk-tuk màu xanh đỗ vỉa hè `img_004`; xe tuk-tuk trên phố Bangkok `img_016`, `img_040`; xe auto-rickshaw chở bao tải `img_035`. | Xe mô tô 2 bánh (`motorcycle`); xe xích lô đạp chân (`bicycle`). |
| `motorcycle` | Xe gắn máy, xe mô tô 2 bánh hoặc 3 bánh có gắn động cơ (bao gồm xe số, xe tay ga, mô tô phân khối lớn, xe máy độ và mô tô có thùng phụ sidecar). | Dòng xe máy trên đường `img_005`, `img_008`, `img_014`, `img_021`, `img_026`, `img_030`; mô tô cổ gắn thùng phụ sidecar `img_022`. | Xe đạp (`bicycle`); xe xích lô đạp chân (`bicycle`); xe tuk-tuk 3 bánh (`tuk_tuk`). |
| `bicycle` | **Phương tiện thô sơ 2 hoặc 3 bánh đạp chân bằng sức người (gộp chung cả xe đạp, xe chở hàng thô sơ và xe xích lô chở khách).** | Xe đạp chở giỏ mít `img_003`, xe đạp chở phật thủ `img_010`, xe đạp chở thanh nhôm `img_029`; đoàn xe xích lô du lịch ở Huế `img_006`, `img_009`, `img_023`, `img_034`, `img_039`. | Xe máy/mô tô có động cơ (`motorcycle`); xe tuk-tuk có động cơ (`tuk_tuk`); xe lăn/xe đẩy trẻ em (**không gán**). |
| `person` | Cơ thể con người thật còn sống (người đi bộ, người đứng/ngồi bên đường, người điều khiển hoặc hành khách trên xe hở: xe máy, xe đạp, xích lô, tuk-tuk). | Người đứng ở `img_001`; người đi bộ `img_014`, `img_025`; người lái và người ngồi sau xe máy `img_005`, `img_026`; tài xế tuk-tuk `img_004`; người đạp và hành khách xích lô `img_006`. | Tượng đồng Wellington `img_017` (**không gán**); ảnh chân dung trên billboard `img_018` (**không gán**); ma-nơ-canh `img_033` (**không gán**); tượng Predator `img_011` (**không gán**); búp bê `img_038` (**không gán**). |
| `ignore_region` | Vùng đánh dấu không yêu cầu gán chi tiết từng vật: đám đông người hoặc bãi xe quá dày đặc/ở xa dính chùm có chiều cao < 20 px không thể tách cá thể. | Đám đông người xem diễu hành ở xa `img_011`, `img_019`; cụm người đi dạo bờ biển xa `img_025`; bãi xe máy dính chùm phía xa `img_021`, `img_030`. Bỏ sót vật trong vùng này **không tính là lỗi QC**. | Vật thể ở cự ly gần hoặc nhìn rõ từng cá thể riêng biệt (vẫn phải gán box riêng). |

---

### 2.2. Quy định thuộc tính đối tượng (`attributes`)

Mọi đối tượng thuộc 8 lớp phương tiện và người bắt buộc gán đủ 3 thuộc tính (lớp `ignore_region` không có thuộc tính):

1. **`occluded_level` (Mức độ che khuất):**
   - **`0` - Không bị che:** 0% đến < 10% diện tích vật thể bị che khuất (nhìn thấy gần như trọn vẹn toàn bộ đường viền).
   - **`1` - Che khuất nhẹ:** Từ **10% đến 30%** diện tích vật thể bị che bởi vật khác (ví dụ: người lái xe máy/xe đạp bị giỏ xe che một phần chân; ô tô sau hàng rào thưa `img_018`).
   - **`2` - Che khuất trung bình đến nặng:** Từ **31% đến 70%** diện tích vật thể bị che khuất (ví dụ: người ngồi sau xe máy bị người lái che phần lớn thân mình trong `img_005`; xích lô bị xe khác che một phần bánh).
   - **`3` - Che khuất cực nặng:** Trên **70%** diện tích bị che khuất nhưng mắt người vẫn nhận dạng chắc chắn được lớp nhờ đặc trưng nhận diện then chốt (mũ bảo hiểm + vai, hoặc bánh xe + ghi đông).
   - *Ngưỡng loại bỏ:* Nếu vật thể bị che khuất trên **90%** hoặc không đủ căn cứ nhận diện chắc chắn $\rightarrow$ **Không gán box**.

2. **`truncated` (Cắt mép ảnh):**
   - **`no`:** Toàn bộ phần nhìn thấy của vật thể nằm gọn bên trong khung ảnh (0% bị cắt mép).
   - **`yes`:** Vật thể bị cắt bởi ít nhất một trong bốn mép ảnh (trên, dưới, trái, phải).
   - *Lưu ý quan trọng:* Vật bị vật khác che khuất ở giữa bức ảnh là `occluded`, **tuyệt đối không đánh dấu** `truncated = yes`.

3. **`can_review` (Đánh dấu cần hội ý):**
   - **`false` (mặc định không tick):** Quyết định gán nhãn rõ ràng, tự tin theo đúng quy tắc.
   - **`true` (tick chọn):** Áp dụng cho các tình huống biên còn phân vân về lớp, ranh giới box bị tối/nhòe nặng (`img_007`, `img_013`, `img_015`) để đưa ra thảo luận tại buổi họp calibration Pha 5.

---

## 3. Quy tắc vẽ Bounding Box (Chuẩn hóa mã `R-01` đến `R-11`)

- **`R-01` (Ôm sát phần nhìn thấy - Tight Visible Box):**
  - Bounding Box phải ôm sát các pixel thực tế nhìn thấy được của vật thể (*visible bounding box*), sai số biên cho phép ≤ 2 px.
  - Tuyệt đối **không phỏng đoán phần bị che khuất** để vẽ box rộng ra (không vẽ amodal box trên ảnh 2D).
  - Nếu một vật bị thanh rào chắn hoặc cột đèn cắt thành 2 phần rời nhau (`img_018`): vẽ **1 box duy nhất** bao trọn các phần nhìn thấy của đối tượng đó và đặt `occluded_level` phù hợp.

- **`R-02` (Tách riêng Người và Xe máy - Rider & Vehicle Separation):**
  - Trên xe máy (`img_005`, `img_008`, `img_014`, `img_021`, `img_026`, `img_030`): **Bắt buộc tách thành các box độc lập**, tuyệt đối không vẽ 1 box gộp chung người và xe.
  - Box `person`: Ôm trọn cơ thể người nhìn thấy từ đỉnh mũ bảo hiểm / đầu xuống đến phần thân/chân nhìn thấy trên xe. Balo, túi xách đeo trên người tính vào box `person`. Đặt `occluded_level = 1` hoặc `2`.
  - Box `motorcycle`: Ôm trọn khung xe máy, bánh xe, đầu xe, tay lái và gương chiếu hậu nhìn thấy. Đặt `occluded_level = 1` hoặc `2` do bị người lái che một phần thân xe.
  - **Nhiều người trên cùng một xe máy (`img_026`):** Gán từng box `person` riêng cho từng người (1 box cho người lái, 1 box cho người ngồi sau) và 1 box `motorcycle` chung cho chiếc xe.

- **`R-03` (Xe chuyên dụng chở ô tô - Car Carrier):**
  - Trong ảnh xe đầu kéo chở ô tô con (`img_002`):
    - Gán **1 box `truck`** lớn cho xe tải/đầu kéo chở hàng (bao gồm cabin và giàn sàn chở hàng chuyên dụng).
    - Gán **từng box `car` riêng biệt** cho mỗi chiếc ô tô con nhìn thấy trên cả hai tầng giàn sàn (đặt `occluded_level = 1` hoặc `2` do khung giàn che). Lý do: Mô hình xe tự lái cần nhận diện chướng ngại vật ô tô để tính toán va chạm.

- **`R-04` (Quy tắc gán Xe 3 bánh Tuk-tuk và Xe buýt):**
  - Xe tuk-tuk / auto-rickshaw 3 bánh (`img_004`, `img_016`, `img_035`, `img_040`): Gán đúng lớp **`tuk_tuk`**. Tài xế hoặc hành khách ngồi trong khoang lái hở nếu nhìn thấy rõ cơ thể thì gán thêm box **`person`** riêng (`occluded_level = 2`).
  - Xe buýt, xe khách (`img_009`, `img_031`, `img_032`, `img_037`, `img_040`): Gán đúng lớp **`bus`**.

- **`R-05` (Quy tắc gán Xe đạp và Xe xích lô - Lớp `bicycle`):**
  - **Gộp chung xe đạp và xe xích lô vào lớp `bicycle`**:
    - Xe đạp chở hàng / xe đạp thể thao (`img_003`, `img_010`, `img_029`): Gán 1 box **`bicycle`** ôm trọn khung xe, bánh xe, tay lái và giỏ hàng gắn trên xe. Gán 1 box **`person`** riêng cho người đạp xe hoặc dắt xe.
    - Xe xích lô du lịch (`img_006`, `img_009`, `img_023`, `img_034`, `img_039`): Gán 1 box **`bicycle`** ôm trọn kết cấu xích lô (3 bánh xe, khung sườn, tay lái, khoang/ghế ngồi phía trước và mái che của xích lô).
    - **Tách riêng người:** Bắt buộc gán box **`person`** riêng cho tài xế đạp xích lô phía sau và **từng box `person` riêng** cho mỗi hành khách ngồi ở khoang trước của xích lô. Không gộp người và xe xích lô thành 1 box.

- **`R-06` (Loại trừ đối tượng giả lập / Phi sinh học - False Targets):**
  - **Tượng đài / Điêu khắc:** KHÔNG gán `person` cho tượng người cưỡi ngựa bằng đồng (`img_017`); KHÔNG gán `truck`/`car` cho bia mộ điêu khắc hình xe bán tải bằng đá (`img_027`).
  - **Hình in 2D / Biển quảng cáo:** KHÔNG gán `person` cho hình ảnh chính khách in trên billboard bầu cử (`img_018`) hoặc hình ca sĩ/diễn viên trên poster (`img_030`).
  - **Ma-nơ-canh & Đồ chơi trưng bày:** KHÔNG gán `person` cho ma-nơ-canh thời trang trong tủ kính (`img_033`); KHÔNG gán `car` hay `person` cho mô hình xe đồ chơi, búp bê trên kệ kính (`img_037`, `img_038`).
  - **Ảnh phản chiếu qua gương:** KHÔNG gán box cho ô tô hay người phản chiếu trong gương chiếu hậu (`img_020`) hoặc phản chiếu trên vách kính cửa hàng (`img_033`).
  - **Xe diễu hành / Mascot (`img_019`):** Xe ô tô màu vàng có biển số chạy thật gán `car`; người lái xe bên phải gán `person`; tượng mascot chuột Danger Mouse màu trắng gắn trên xe là đạo cụ biểu diễn, **không gán**.
  - **Tượng gắn trên phương tiện (`img_028`):** Xe bán tải thật gán `truck`; tượng con ngựa "yorse" chở trên thùng xe được xem là hàng hóa tĩnh, **không gán**.
  - **Khung vỏ xe gắn trên giá nóc xe (`img_024`):** Xe AMC Pacer đang chạy bên dưới gán `car`; khung vỏ xe phế liệu gác trên giá nóc là hàng hóa/phụ kiện, **không gán thêm `car`**.

- **`R-07` (Hàng hóa cồng kềnh, quá tải trên phương tiện):**
  - Xe bán tải chở hàng nhô khỏi thùng (`img_012`): Box `truck` ôm theo thân xe và cabin, không kéo mở rộng theo từng mớ rau hay thùng xốp nhỏ nhô lên.
  - Xe máy, xe đạp hoặc tuk-tuk chở hàng quá khổ khổng lồ (`img_029`, `img_035`): Box phương tiện (`motorcycle`, `bicycle`, `tuk_tuk`) **chỉ ôm phần kết cấu cơ giới nhìn thấy của xe** (khung xe, bánh xe, đầu xe). Tuyệt đối **không kéo box phương tiện phình to** để bọc cả khối xốp khổng lồ hay núi bao tải cao ngất ngưởng.

- **`R-08` (Người ngồi trong xe kín vs Người trên xe hở):**
  - Người ngồi trong khoang kín của ô tô/xe tải/xe van (nhìn xuyên qua kính đóng kín): **Không gán `person`** (box của xe đã bao toàn bộ).
  - Người ngồi trên phương tiện hở (xe máy, xe đạp/xích lô `bicycle`, mô tô sidecar `img_022`, tuk-tuk hở): **Bắt buộc gán box `person` riêng**.

- **`R-09` (Ngưỡng kích thước tối thiểu & Đám đông - `ignore_region`):**
  - Vật thể có chiều cao phần nhìn thấy **< 20 px** (`rules.min_box_height_px = 20`): Không gán box cá thể.
  - Cụm đám đông người đi bộ hoặc bãi xe máy dính chùm dày đặc ở hậu cảnh xa không thể phân định ranh giới từng cá thể (`img_011`, `img_019`, `img_021`, `img_025`, `img_030`, `img_032`): Dùng **1 box `ignore_region`** bao trùm cả cụm.

- **`R-10` (Xe chủ - Ego Vehicle):**
  - Phần thân xe, gương chiếu hậu hoặc nắp ca-pô của xe chủ gắn camera chụp ra nằm sát mép ảnh (`img_013`, `img_015`, `img_020`): **Không gán box**.

- **`R-11` (Nhòe chuyển động và Thiếu sáng):**
  - Vật bị nhòe chuyển động (*motion blur*) hoặc trong điều kiện thiếu sáng (`img_007`, `img_013`, `img_014`, `img_015`): Nếu mắt thường vẫn nhận diện chắc chắn được hình thể và lớp phương tiện thì vẫn vẽ box ôm phần nhìn thấy; nếu chưa chắc chắn thì tick chọn `can_review = true`.

---

## 4. Bảng phân tích Ca khó trong 40 ảnh

Bảng tổng hợp quyết định thống nhất cho toàn bộ các tình huống biên được phát hiện trong 40 ảnh thực tế:

| Ảnh | Tình huống phát hiện | Rule ID | Quyết định thống nhất nhóm | Lý do giải quyết bất đồng giữa các thành viên |
|---|---|---|---|---|
| `img_001.jpg` | Xe bán tải cũ chở hàng đỗ trước quán ăn bên đường | `R-01`, `R-02` | Gán `truck` cho xe bán tải; gán `person` cho người phụ nữ đứng cạnh; khách ngồi ăn nhìn rõ gán `person`. | Xe bán tải có cabin tách rời thùng chở hàng sau $\rightarrow$ thuộc `truck` (thống nhất phân loại pickup là `truck`). |
| `img_002.jpg` | Xe tải chuyên dụng (`Renault 380`) chở 7 ô tô con trên hai tầng giàn sàn | `R-01`, `R-03` | Gán 1 box `truck` cho xe tải chở hàng (ôm cả cabin và giàn sàn); gán 7 box `car` riêng cho từng ô tô trên sàn; gán 1 `person` đứng cạnh. | Giải quyết bất đồng: 102 ban đầu không gán xe trên giàn, nhưng nhóm chốt theo 101/103/104 là phải gán `car` vì xe tự lái cần nhận biết chướng ngại vật ô tô để tránh va chạm. |
| `img_003.jpg` | Người phụ nữ đẩy xe đạp chở giỏ mít to ở Hà Nội | `R-05` | Gán 1 box `person` cho người phụ nữ; **gán 1 box `bicycle`** cho chiếc xe đạp chở giỏ mít. | Thống nhất bổ sung lớp `bicycle` gộp xe đạp và xích lô; giỏ mít gắn sau xe tính vào box `bicycle`. |
| `img_004.jpg` | 2 xe tuk-tuk màu xanh đỗ trên vỉa hè ban đêm | `R-04`, `R-08` | Gán 2 box `tuk_tuk` cho 2 xe; gán box `person` cho tài xế ngồi trong khoang hở nếu nhìn thấy rõ. | Giải quyết bất đồng: Thay vì ép vào `motorcycle` (101, 103) hay bỏ ngoài lớp (102, 104), nhóm bổ sung lớp `tuk_tuk` vào taxonomy v1.0 để phân loại chính xác. |
| `img_005.jpg` | Dòng người đi xe máy chụp cận cảnh ở TP.HCM, phía sau có minivan và ô tô | `R-01`, `R-02` | Tách riêng từng box `person` và `motorcycle` cho từng cặp; xe phía mép ảnh đặt `truncated=yes`; xe van bạc gán `van`, ô tô con bên trái gán `car`. | Cả 4 thành viên đồng thuận 100%: bắt buộc tách riêng người và xe máy; người ngồi giữa bị che nhiều đặt `occluded_level=2`. |
| `img_006.jpg` | Đoàn xích lô đạp chân chở khách du lịch ở Huế | `R-05` | **Gán box `bicycle` cho từng xe xích lô**; gán box `person` riêng cho từng tài xế đạp xích lô và khách ngồi trên xe. | Thống nhất xe xích lô thuộc lớp `bicycle`; tách riêng box xe và box người. |
| `img_007.jpg` | Xe tải giao hàng trong kho tối ban đêm | `R-01`, `R-11` | Gán `truck` cho các xe tải nhìn rõ kết cấu; đặt `occluded_level=1`, chạm mép đặt `truncated=yes`. | Thiếu sáng nhưng kết cấu xe tải rõ ràng, vẽ box ôm phần nhìn thấy. |
| `img_008.jpg` | Chợ đêm Pattaya, xe máy đỗ và người đi lại đông đúc | `R-02`, `R-09` | Gán riêng `person` và `motorcycle` cho các xe/người ở tiền cảnh; cụm người dính chùm phía xa dùng `ignore_region`. | Thống nhất phân tách tiền cảnh rõ ràng và gom hậu cảnh xa. |
| `img_009.jpg` | Tour xích lô ở Huế, phía sau có xe buýt lớn | `R-04`, `R-05` | Gán box `bus` cho xe buýt phía sau; **gán `bicycle` cho các xích lô**; gán `person` cho người đạp và khách trên xích lô. | Bổ sung lớp `bus` và `bicycle` giúp giải quyết trọn vẹn cả xe khách và xe xích lô trong cùng một bức ảnh. |
| `img_010.jpg` | Người bán phật thủ trên phố cổ Hà Nội cạnh xe đạp/xe máy chở sọt | `R-02`, `R-05` | Gán `person` cho người bán hàng; gán `bicycle` cho xe đạp (hoặc `motorcycle` nếu là xe máy). | Tách riêng người và phương tiện; sọt hàng gắn sau xe tính vào box phương tiện. |
| `img_011.jpg` | Người mặc trang phục hóa trang Predator bên dàn mô tô độ | `R-02`, `R-06`, `R-09` | Người mặc đồ Predator vẫn là **người thật** $\rightarrow$ gán `person`; dàn mô tô độ gán `motorcycle`; xe cứu thương phía sau gán `van`; đám đông xa gán `ignore_region`. | Thống nhất: Người mặc trang phục hóa trang vẫn là con người còn sống tham gia giao thông, không phải tượng tĩnh. |
| `img_012.jpg` | Xe bán tải chở thùng xốp rau củ nhô lên khỏi thùng | `R-01`, `R-07` | Gán `truck`, box ôm thân xe và cabin, không kéo mở rộng theo các thùng xốp rời nhô lên cao. | Thống nhất box phương tiện không bị méo mó theo hàng hóa rời nhỏ. |
| `img_013.jpg` | Phố đêm sau mưa, góc nhìn từ sau thùng xe | `R-10`, `R-11` | Gán các ô tô con và xe bán tải phía trước; phần thành thùng xe chủ ở tiền cảnh sát mép ảnh $\rightarrow$ **không gán** (ego vehicle). | Thống nhất loại trừ xe chủ (`R-10`). |
| `img_014.jpg` | Người đi bộ băng qua đường giữa dòng xe máy bị motion blur | `R-02`, `R-11` | Gán `person` cho người đi bộ; gán `person` và `motorcycle` cho các xe máy nhìn rõ ranh giới; xe quá nhòe tick `can_review`. | Nhận diện đối tượng trong điều kiện giao thông thực tế. |
| `img_015.jpg` | Phố mưa mờ nhòe nước mưa trên kính lái | `R-10`, `R-11` | Gán các xe nhận diện được; vệt đèn nhòe không rõ lớp khoanh `ignore_region`; gạt nước/kính xe chủ không gán. | Tránh gán tọa độ ngẫu nhiên không thể tái lập. |
| `img_016.jpg` | Xe tuk-tuk và xe bán tải nắp thùng cao trên phố Bangkok | `R-01`, `R-04` | Gán `tuk_tuk` cho xe tuk-tuk; gán `truck` cho xe bán tải gắn nắp thùng cao Master 75. | Xe bán tải có nắp thùng cao vẫn là `truck` vì cabin tách rời thùng hàng. |
| `img_017.jpg` | Tượng đồng Công tước Wellington cưỡi ngựa ở Glasgow | `R-06` | **Không gán bất kỳ box nào** (ảnh rỗng `0` annotation trong file COCO). | Cả 4 thành viên đồng thuận 100%: tượng điêu khắc tĩnh không phải người/xe thật. |
| `img_018.jpg` | Biển quảng cáo chính trị in hình chân dung, phía dưới là ô tô sau rào sắt | `R-01`, `R-06` | **Không gán** hình người trên biển quảng cáo; gán các ô tô thật phía dưới là `car` với `occluded_level=1`. | Tránh lỗi dương tính giả tai hại trên billboard 2D. |
| `img_019.jpg` | Xe diễu hành Hamley gắn tượng chuột Dangermouse khổng lồ | `R-01`, `R-06`, `R-09` | Gán `car` cho xe cơ sở bên dưới; gán `person` cho tài xế ngồi lái; tượng chuột bông trên xe **không gán**; đám đông hai bên rào chắn gom `ignore_region`. | Thống nhất tách bạch xe thật, người thật và đạo cụ hóa trang. |
| `img_020.jpg` | Cầu vồng và xe phản chiếu qua gương chiếu hậu ô tô | `R-06`, `R-10` | **Không gán bất kỳ box nào** (ảnh rỗng `0` annotation trong file COCO). | Hình ảnh trong gương là ảnh ảo phản chiếu; khung gương là xe chủ. |
| `img_021.jpg` | Dòng xe máy dừng đèn đỏ dày đặc lúc chập tối | `R-02`, `R-09` | Gán riêng `person` và `motorcycle` cho các xe ở tiền cảnh/trung cảnh nhìn rõ; dải xe máy dính chùm phía xa gom vào `ignore_region`. | Thống nhất ranh giới gán chi tiết tiền cảnh và gom hậu cảnh xa. |
| `img_022.jpg` | Xe mô tô cổ có gắn thùng phụ sidecar | `R-02` | Gán 1 box `motorcycle` ôm trọn cả xe mô tô và thùng phụ sidecar; gán 1 box `person` cho người ngồi trong sidecar. | Thùng phụ gắn liền xe tạo thành một thể phương tiện thống nhất. |
| `img_023.jpg` | Xích lô du lịch ở Huế đi ngược chiều ô tô con đen | `R-01`, `R-05` | **Gán `bicycle` cho xích lô**; gán `person` cho người đạp và khách; gán `car` cho ô tô con đen. | Áp dụng đúng quy tắc gán xích lô vào lớp `bicycle`. |
| `img_024.jpg` | Xe AMC Pacer chở khung vỏ xe ô tô phế liệu trên giá nóc | `R-01`, `R-06` | Gán 1 box `car` cho xe AMC Pacer đang chạy; khung vỏ xe trên giá nóc là hàng hóa phế liệu $\rightarrow$ **không gán thêm `car`**. | Tránh gán nhầm vỏ xe rỗng không vận hành thành phương tiện giao thông. |
| `img_025.jpg` | Đi dạo bờ biển Pattaya, người đi bộ và xe cộ bên đường | `R-02`, `R-09` | Gán `person` cho người đi bộ đủ lớn ($\ge 20\text{ px}$); đám đông nhỏ ở bãi biển xa gom `ignore_region`; gán `truck`, `motorcycle` bên đường. | Tuân thủ ngưỡng chiều cao tối thiểu 20 px. |
| `img_026.jpg` | Cặp đôi nam nữ trên xe máy trong hầm chui Sài Gòn | `R-01`, `R-02` | Tách thành **3 box riêng**: 1 `person` (lái xe nam), 1 `person` (ngồi sau nữ), 1 `motorcycle` (chiếc xe). | Ca chuẩn kiểm tra quy tắc tách 2 người trên 1 xe máy. |
| `img_027.jpg` | Tượng đài đá tạc hình xe bán tải ở nghĩa trang Oak Hill | `R-06` | **Không gán bất kỳ box nào** (ảnh rỗng `0` annotation trong file COCO). | Tượng đá điêu khắc tĩnh, tuyệt đối không gán `truck`/`car`. |
| `img_028.jpg` | Xe bán tải chở tượng con ngựa ("yorse") trên thùng xe | `R-01`, `R-06` | Gán 1 box `truck` cho xe bán tải; tượng ngựa trên thùng là vật trang trí $\rightarrow$ **không gán nhãn**. | Thống nhất không gán tượng động vật chở trên xe. |
| `img_029.jpg` | Người đi xe máy và người đi xe đạp cùng vác một bó thanh nhôm rất dài | `R-02`, `R-05`, `R-07` | Gán `motorcycle` + `person` cho người xe máy; **gán `bicycle` + `person`** cho người đi xe đạp; box không mở rộng theo thanh nhôm dài. | Thống nhất gán xe đạp vào lớp `bicycle` và khống chế ranh giới box theo thân xe. |
| `img_030.jpg` | Bãi xe máy dày đặc có nhân viên áo xanh, phía trên có biển quảng cáo in hình ca sĩ | `R-02`, `R-06`, `R-09` | Bỏ hình người trên biển quảng cáo; gán `person` cho nhân viên; gán `motorcycle` cho xe tiền cảnh; cụm xe dính chùm phía xa gom `ignore_region`. | Kết hợp loại trừ biển quảng cáo và gom vùng đám đông xe. |
| `img_031.jpg` | Ngã tư đường Kangding ban đêm có xe buýt lớn và taxi | `R-01`, `R-04` | Gán `bus` cho xe buýt; gán `car` cho taxi trắng; gán `motorcycle` và `person` cho xe máy. | Phân loại rõ `bus` và `car`. |
| `img_032.jpg` | Điểm dừng xe buýt ETS giờ cao điểm, đám đông chờ xe buýt lớn | `R-04`, `R-09` | Gán `bus` cho xe buýt lớn; người ở hàng trước nhìn rõ gán `person`; cụm người phía sau dính chùm gom `ignore_region`. | Xử lý đám đông trạm xe buýt và phương tiện công cộng lớn. |
| `img_033.jpg` | Tủ kính ma-nơ-canh và bóng phản chiếu xe tải trên kính | `R-06` | **Không gán bất kỳ box nào** (ảnh rỗng `0` annotation trong file COCO). | Ma-nơ-canh không phải người thật; bóng xe trên kính là phản chiếu. |
| `img_034.jpg` | Sang đường giữa đoàn xích lô du lịch ở Huế | `R-05` | **Gán `bicycle` cho các xích lô nhìn rõ**; gán `person` cho người đi bộ, người đạp và khách xích lô; gán `car` cho ô tô. | Áp dụng đúng quy tắc gán xích lô vào `bicycle`. |
| `img_035.jpg` | Xe tuk-tuk chở núi bao tải phế liệu cao ngất ngưởng ở Hyderabad | `R-04`, `R-07` | Gán `tuk_tuk`, box chỉ ôm thân xe và bánh xe tuk-tuk (không kéo cao ôm trọn núi bao tải); gán `person` cho tài xế và người đi xe máy bên cạnh; gán `car` cho ô tô con. | Giải quyết dứt điểm: vừa phân lớp đúng `tuk_tuk`, vừa khống chế box không phình to theo hàng quá khổ. |
| `img_036.jpg` | Xe tải nhẹ đầu bằng CMC Veryca | `R-01` | Gán `truck` (có khoang chở hàng riêng phía sau cabin). | Thuộc định nghĩa `truck`. |
| `img_037.jpg` | Xe bán tải GO Transit gắn nắp thùng cao Master 75, phía sau có xe buýt | `R-01`, `R-04` | Gán `truck` cho xe bán tải nắp thùng cao; gán `bus` cho xe buýt phía sau. | Bản chất khung gầm là pickup truck $\rightarrow$ gán `truck`. |
| `img_038.jpg` | Tủ kính trưng bày bộ sưu tập xe đồ chơi, búp bê, vịt cao su | `R-06` | **Không gán bất kỳ box nào** (ảnh rỗng `0` annotation trong file COCO). | Toàn bộ là mô hình đồ chơi thu nhỏ. |
| `img_039.jpg` | Tour xích lô ở Huế chạy dọc đường | `R-05` | **Gán `bicycle` cho các xe xích lô**; gán `person` cho người đạp và khách ngồi. | Áp dụng quy tắc gán xích lô vào lớp `bicycle`. |
| `img_040.jpg` | Kẹt xe trung tâm Bangkok: xe buýt, taxi, tuk-tuk, người trên cầu vượt | `R-01`, `R-04` | Gán `bus` cho xe buýt; gán `car` cho taxi; gán `tuk_tuk` cho tuk-tuk; người trên cầu vượt nếu cao $\ge 20\text{ px}$ gán `person`, nhỏ hơn gom `ignore_region`. | Đủ cả 4 lớp phương tiện cơ giới đường bộ chính trong cùng một bối cảnh. |

---

## 5. QC và Quản lý phiên bản

### 5.1. Ngưỡng kiểm soát chất lượng (giữ nguyên mục `rules` trong `taxonomy.json`)

- **Chiều cao box tối thiểu (`min_box_height_px`):** `20 px` (vật nhỏ hơn 20 px không gán box riêng mà đưa vào `ignore_region`).
- **Ngưỡng IoU đánh giá:**
  - Box lớn (chiều cao $\ge 50\text{ px}$): **IoU $\ge 0.85$**.
  - Box nhỏ (chiều cao $20\text{ px} – 49\text{ px}$): **IoU $\ge 0.70$**.
- **Ngưỡng đo độ đồng thuận IAA (Pha 4):**
  - Ghép cặp box 1–1 tại ngưỡng `match_iou >= 0.50`.
  - Yêu cầu **IoU trung bình $\ge 0.85$** và **Đồng thuận lớp $\ge 95\%$** trên các cặp box ghép được.
  - Phải hoàn thành **100% lượt gán** được phân công trong `assignment.csv`.
- **Ngưỡng nghiệm thu lô (QC Release - Pha 6):**
  - Duyệt toàn bộ 40 ảnh (`full`).
  - Tỷ lệ ảnh có lỗi $\le 2\%$ (với 40 ảnh, chỉ cần $\ge 1$ ảnh lỗi $= 2.5\% > 2\%$ hoặc có lỗi hệ thống lặp lại $\rightarrow$ buộc phải chọn **Rework**, không được Release).

### 5.2. Lịch sử thay đổi phiên bản (`v0 → v1.0`)

| Phiên bản | Ngày | Người thực hiện | Tóm tắt thay đổi | Căn cứ giải quyết bất đồng từ các bản cá nhân |
|---|---|---|---|---|
| `v0` | 2026-11-16 | Giảng viên | Bản sơ lược khởi đầu: chỉ có 5 lớp định tính, chưa có quy tắc ca biên. | Chưa giải quyết được xe chở xe, tuk-tuk, xe buýt, xe đạp/xích lô, tượng, phản chiếu... |
| `v1.0` | 2026-11-16 | Nhóm `101`, `102`, `103`, `104` | 1. Bổ sung các lớp mới `bus`, `tuk_tuk`, và **gộp xe đạp & xích lô thành lớp `bicycle`** (nâng tổng số lên 9 lớp trong `taxonomy.json`).<br>2. Định lượng hóa 3 mức thuộc tính (`occluded_level`, `truncated`, `can_review`) bằng ngưỡng % đo được.<br>3. Thống nhất tuyệt đối 11 quy tắc chuẩn hóa `R-01` đến `R-11` (bao gồm `R-05` gán nhãn cho xe đạp và xích lô).<br>4. Giải quyết triệt để bất đồng về xe chở xe (`img_002`), tuk-tuk (`img_004`), xe buýt (`img_009`), đoàn xích lô (`img_006`, `img_034`, `img_039`), hàng quá khổ (`img_035`), tượng tĩnh (`img_017`, `img_027`) và biển quảng cáo (`img_018`).<br>5. Lập bảng phân tích 40 ca cụ thể. | Đối chiếu, dung hòa 4 bản cá nhân (`guideline_101.md`, `guideline_102.md`, `guideline_103.md`, `guideline_104.md`) và thống nhất yêu cầu quản lý phương tiện đạp chân thô sơ. |
