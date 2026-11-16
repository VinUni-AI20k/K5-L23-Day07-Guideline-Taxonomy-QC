# Guideline gán nhãn dữ liệu — Bản thống nhất của nhóm (v1.0 Agreed)

- **Nhóm thực hiện:** Nhóm T005
- **Các thành viên tham gia thống nhất:**
  - `040` - NGUYỄN ĐỨC CƯỜNG (Reviewer bản cuối)
  - `183` - HOÀNG NHẬT ANH (Quản lý tài liệu)
  - `192` - NGUYỄN BÁ DUY (Điều phối viên - Leader)
  - `216` - ĐỖ HUY KIÊN (Trưởng ban Đo lường IAA)
  - `240` - PHẠM MẠNH HÙNG (Hiệu chuẩn nhãn)
- **Phiên bản:** `v1.0` (Đã biểu quyết và chốt quy chuẩn toàn nhóm sau Pha 1)
- **Ngày ban hành:** 2026-11-16
- **Phạm vi áp dụng:** Toàn bộ quá trình gán nhãn 40 ảnh trên CVAT trong Pha 3.
- **Kỷ luật thực thi:** **Tuyệt đối không sửa đổi guideline này trong suốt quá trình gán nhãn Pha 3**. Mọi ca phát sinh còn mơ hồ chỉ tick thuộc tính `can_review = true` và ghi chép để mang ra phiên họp Hiệu chuẩn (Calibration - Pha 5).

---

## 1. Mục tiêu ứng dụng và Bối cảnh An toàn

### 1.1. Mục tiêu bộ dữ liệu
Bộ dữ liệu gồm 40 ảnh cảnh quan đường phố đô thị châu Á (chụp tại Việt Nam, Thái Lan, Ấn Độ, Đài Loan...) với đặc trưng giao thông hỗn hợp, mật độ phương tiện dày đặc và nhiều loại xe phi quy chuẩn. Bounding Box được gán nhãn theo định dạng chuẩn COCO 1.0 nhằm phục vụ:
1. **Hệ thống Xe tự hành (Autonomous Vehicles - AV):** Cung cấp dữ liệu huấn luyện cho mạng nơ-ron nhận diện vật cản 2D (2D Object Detection), ước tính khoảng cách an toàn, theo dõi đối tượng (Object Tracking) và dự đoán quỹ đạo chuyển động trong thời gian thực.
2. **Hệ thống Giao thông Thông minh (Intelligent Transportation Systems - ITS):** Phân tích mật độ giao thông, đếm lưu lượng phương tiện theo làn, cảnh báo nguy cơ ùn tắc và phát hiện vi phạm hành lang an toàn.

### 1.2. Phân tích rủi ro an toàn kỹ thuật (Safety Hazards & Failure Modes)
Mọi quy chuẩn trong văn bản này được xây dựng dựa trên nguyên tắc **"An toàn là trên hết" (Safety-First)** nhằm loại bỏ các lỗi suy luận nguy hiểm của mô hình:
- **Nguy cơ Bỏ sót (False Negative - Nguy hiểm tính mạng):** Bỏ sót người đi bộ (`person`) hoặc xe máy (`motorcycle`) đang hòa cùng dòng xe đông đúc sẽ khiến thuật toán điều khiển coi không gian đó là "trống trải" (free drivable space), dẫn đến tai nạn đâm va trực diện không phanh.
- **Nguy cơ Gán nhầm vật giả (False Positive - Phantom Braking):** Gán box cho các vật thể tĩnh vô tri như tượng đài, ma-nơ-canh, hình in 2D trên biển quảng cáo hoặc bóng phản chiếu qua gương sẽ tạo ra tín hiệu sai (toxic gradients). Mô hình sẽ học sai đặc trưng và kích hoạt hệ thống phanh khẩn cấp vô cớ khi xe đang chạy tốc độ cao, gây tai nạn liên hoàn cho các xe phía sau.
- **Nguy cơ Sai lệch phân loại (Misclassification):** Gán nhầm xe tải chở hàng (`truck`) thành ô tô con (`car`) dẫn đến ước tính sai kích thước vật lý, trọng tâm và khoảng cách phanh an toàn.

---

## 2. Danh mục Lớp và Thuộc tính Đối tượng (Taxonomy v1.0)

Bộ nhãn chuẩn hóa gồm **6 lớp đối tượng** và **3 thuộc tính**, khớp 100% với `submission/taxonomy.json` (phiên bản `v1.0`).

### 2.1. Định nghĩa chuẩn hóa 6 lớp đối tượng

| Lớp | Định nghĩa cốt lõi thống nhất | Ví dụ thực tế trong 40 ảnh | Phản ví dụ / Tuyệt đối KHÔNG gán | Quy tắc ranh giới Bounding Box |
|:---|:---|:---|:---|:---|
| `car` | Phương tiện cơ giới 3-4 bánh có động cơ, kết cấu thân vỏ kín hoặc bán hở dùng chở người hoặc chở khách công cộng cỡ nhỏ. **Bao gồm cả xe Tuk-tuk / Auto Rickshaw 3 bánh.** | Ô tô sedan, hatchback, SUV, Crossover, Taxi, xe Tuk-tuk / Auto Rickshaw (`img_004.jpg`, `img_035.jpg`, `img_040.jpg`), xe diễu hành Dangermouse có người lái (`img_019.jpg`). | Xe bán tải thùng hở (`truck`), xe van khoang kín (`van`), xe mô hình đồ chơi (`img_038.jpg`), tượng đài tạc hình xe (`img_027.jpg`). | Bounding box ôm sát toàn bộ thân xe nhìn thấy (cản trước/sau, gương chiếu hậu, mui xe). |
| `truck` | Phương tiện cơ giới chuyên dụng chở hàng hóa, có cabin điều khiển tách biệt với thùng chở hàng phía sau (thùng hở, thùng lửng, sàn phẳng hoặc rơ-moóc). **Bao gồm xe bán tải (pickup truck).** | Xe tải chở hàng ban đêm (`img_007.jpg`), xe tải nhỏ thùng hở (`img_036.jpg`), xe chuyên dụng chở ô tô (`img_002.jpg`), xe bán tải chở nông sản (`img_001.jpg`, `img_012.jpg`). | Xe van chở hàng khoang liền cabin (`van`), xe ô tô du lịch 7 chỗ (`car`), xe kéo tay thô sơ (không gán). | Box ôm sát cabin và thùng xe cơ học. Không bao gồm phần hàng hóa rời nhô cao/xòe ra ngoài thùng xe. |
| `van` | Xe ô tô thân thùng kín cỡ nhỏ đến vừa, khoang lái và khoang chở hàng gắn liền thành một khối khí động học. **Bao gồm xe bán tải có gắn nắp thùng kín cao (truck cap / canopy).** | Xe chở hàng khoang kín (Ford Transit van, Suzuki Blind Van, Hyundai Solati van), xe bán tải gắn nắp chụp thùng cao ngang nóc cabin (`img_037.jpg`). | Xe bán tải thùng hở (`truck`), xe SUV gia đình (`car`), xe buýt cỡ lớn (`bus` - ngoài taxonomy). | Box ôm sát thân vỏ ngoài cùng của khối thùng kín. |
| `motorcycle` | Phương tiện cơ giới 2-3 bánh chạy bằng động cơ đốt trong hoặc động cơ điện. **Bao gồm cả mô tô gắn thùng phụ bên hông (sidecar).** | Xe máy số, xe tay ga (scooter), mô tô phân khối lớn trong `img_005.jpg`, `img_008.jpg`, `img_026.jpg`, `img_029.jpg`, mô tô sidecar trong `img_022.jpg`. | Xe đạp thể thao, xe xích lô đạp chân (`img_006.jpg`, `img_009.jpg`, `img_023.jpg`, `img_034.jpg`), xe đẩy hàng rong (`img_003.jpg`). | Box ôm từ đỉnh tay lái/gương chiếu hậu đến điểm tiếp đất của bánh xe. Tách rời với box người lái. |
| `person` | Cơ thể con người sinh học còn sống ở mọi tư thế: đi bộ, đứng, ngồi, nằm, điều khiển phương tiện hoặc hành khách. | Người đi bộ qua đường (`img_014.jpg`), người lái xe máy, người ngồi sau (`img_026.jpg`, `img_029.jpg`), người đạp xích lô và khách ngồi xích lô (`img_006.jpg`), người mặc đồ cosplay (`img_011.jpg`). | Ma-nơ-canh (`img_033.jpg`), tượng đài điêu khắc (`img_017.jpg`, `img_027.jpg`), hình người in trên biển quảng cáo (`img_018.jpg`), búp bê đồ chơi (`img_038.jpg`). | Ôm sát từ đỉnh đầu (hoặc nón bảo hiểm) đến gót chân (hoặc phần cơ thể nhìn thấy). Không gán người ngồi kín trong cabin ô tô tối màu. |
| `ignore_region` | Vùng hình chữ nhật đánh dấu khu vực không gán chi tiết từng đối tượng do quá xa, mờ nhòe, hoặc tập hợp đông đúc dưới ngưỡng phát hiện; không tính lỗi phạt khi bỏ sót trong vùng này. | Cụm người đi bộ ở hậu cảnh xa xôi có chiều cao $< 20\text{ px}$ (`img_025.jpg`), khu chợ đêm lùi sâu trong ngõ tối (`img_008.jpg`), quầy trưng bày đồ chơi (`img_038.jpg`), xe buýt lớn ngoài taxonomy (`img_032.jpg`). | Mọi phương tiện hoặc con người nhìn thấy rõ ranh giới và có chiều cao $\ge 20\text{ px}$. | Vẽ 1 bounding box bao quanh toàn bộ cụm vật thể nhỏ/che khuất nặng. |

---

### 2.2. Quy tắc đối với vật thể nằm ngoài Taxonomy (Out-of-Taxonomy)
1. **Xe xích lô đạp chân / Cyclo (`img_006.jpg`, `img_009.jpg`, `img_023.jpg`, `img_034.jpg`, `img_039.jpg`):**
   - Không có động cơ cơ giới $\rightarrow$ **TUYỆT ĐỐI KHÔNG GÁN BOX PHƯƠNG TIỆN**.
   - Bắt buộc gán **box `person` riêng biệt** cho người đạp xích lô và từng hành khách ngồi trên xe nếu nhìn thấy rõ.
2. **Xe buýt cỡ lớn / Transit Bus (`img_032.jpg`):**
   - Xe chở khách công cộng kích thước lớn không thuộc định nghĩa `car` hay `truck` $\rightarrow$ Vẽ 1 box **`ignore_region`** bao quanh thân xe buýt để tránh việc mô hình bị phạt sai âm/sai dương.
3. **Xe đẩy hàng rong, xe đạp (`img_003.jpg`):**
   - Không gán box phương tiện; chỉ gán box `person` cho người bán hàng / người đạp xe.

---

### 2.3. Quy định Thuộc tính Đối tượng với Ngưỡng Đo Lường Định Lượng

Để đảm bảo độ đồng thuận IAA giữa các thành viên đạt $\ge 95\%$, các mức thuộc tính được định lượng hóa theo tỷ lệ diện tích:

#### 1. Thuộc tính `occluded_level` (Mức độ che khuất):
- **Mức `0` (Nhìn rõ hoàn toàn):** Vật thể hiển thị rõ ràng, diện tích bị che khuất $< 10\%$ tổng diện tích bề mặt.
- **Mức `1` (Che khuất nhẹ):** Bị che khuất từ $10\%$ đến dưới $35\%$ diện tích (ví dụ: bánh xe máy bị vỉa hè che, chân người bị gờ tường che).
- **Mức `2` (Che khuất trung bình):** Bị che khuất từ $35\%$ đến dưới $70\%$ diện tích (ví dụ: nửa thân xe bị xe khác chạy song song che, người ngồi sau xe máy bị người lái che phần thân dưới).
- **Mức `3` (Che khuất nặng):** Bị che khuất $\ge 70\%$ diện tích. Chỉ còn nhìn thấy một phần nhỏ (ví dụ: đầu người đội mũ bảo hiểm, góc đèn hậu xe), nhưng vẫn nhận dạng được nhờ ngữ cảnh xung quanh.

#### 2. Thuộc tính `truncated` (Bị cắt bởi mép biên ảnh):
- **Giá trị `yes`:** Bounding box của vật thể chạm sát vào mép khung hình ($x=0, y=0, x=\text{width}$, hoặc $y=\text{height}$) VÀ phần bị cắt ngoài khung ảnh ước tính chiếm $\ge 5\text{ px}$.
- **Giá trị `no`:** Toàn bộ vật thể nằm trọn vẹn trong khung hình (hoặc mép box cách biên ảnh $\ge 2\text{ px}$).

#### 3. Thuộc tính `can_review` (Đánh dấu trường hợp nghi vấn):
- **Giá trị `true`:** Bật cờ khi gặp trường hợp cực kỳ phân vân, ca dị thường chưa có tiền lệ trong guideline v1.0.
- **Giá trị `false` (mặc định):** Các ca đã tuân thủ rõ ràng quy tắc.

---

## 3. Quy chuẩn Kỹ thuật Vẽ Bounding Box

1. **Nguyên tắc Viền nhìn thấy thực tế (Visible Boundary Principle):**
   - Bounding box phải ôm sát các pixel thực sự nhìn thấy của vật thể (tight bounding box).
   - Tuyệt đối **KHÔNG vẽ ước lượng phần vô hình bị che khuất**. Nếu người bị che mất nửa dưới, box `person` chỉ ôm từ đỉnh đầu đến ranh giới che khuất. Vẽ ước lượng sẽ gây sai lệch nghiêm trọng chỉ số IoU giữa các người gán.

2. **Quy tắc Ghép đôi Người & Xe máy (Coupling Rule):**
   - Khi có người điều khiển hoặc ngồi sau xe máy, bắt buộc vẽ **2 box riêng biệt** chồng lấn tự nhiên:
     - 1 box `person`: Ôm trọn người từ đỉnh đầu/mũ bảo hiểm đến gót chân/bàn đạp.
     - 1 box `motorcycle`: Ôm toàn bộ kết cấu cơ học của xe máy (từ tay lái/gương đến điểm tiếp đất của bánh xe).

3. **Quy tắc Người trong Cabin Ô tô / Xe tải:**
   - **KHÔNG gán box `person`** cho người ngồi kín bên trong ô tô con, xe tải hoặc xe buýt nếu cửa kính đóng hoặc bị bóng lóa, vì box phương tiện đã đại diện cho toàn bộ vật thể cơ học đó.
   - Chỉ gán `person` nếu là xe mui trần mở hoàn toàn và thân người nhô hẳn ra ngoài không gian.

4. **Quy tắc Hàng hóa chuyên chở:**
   - **Hàng hóa trong thùng xe tải / bán tải (`img_012.jpg`):** Box `truck` ôm cả thân xe và phần hàng hóa nằm gọn trong thùng xe.
   - **Hàng hóa cồng kềnh trên xe máy (`img_010.jpg`, `img_029.jpg`):**
     - Box `motorcycle` ôm trọn khung sườn xe và các khối hàng cồng kềnh gắn chặt vào thân xe (vì khối hàng này định hình thể tích cản trở vật lý của phương tiện trên làn đường).
     - Box `person` ôm phần cơ thể người lái nhìn thấy được (`occluded_level = 2` hoặc `3`).

5. **Xe chuyên dụng chở phương tiện khác (`img_002.jpg`):**
   - Gán 1 box `truck` bao toàn bộ xe tải chở hàng mẹ (từ đầu kéo đến đuôi sàn rơ-moóc).
   - Mỗi chiếc xe ô tô con được xếp trên giàn giáo nếu nhìn thấy rõ ràng hình dạng sẽ được gán **1 box `car` riêng biệt**, thuộc tính đặt `occluded_level = 1` hoặc `2`.

6. **Xe mô tô 3 bánh có thùng bên (Sidecar, `img_022.jpg`):**
   - Vẽ 1 box `motorcycle` lớn bao quát toàn bộ thân mô tô và thùng phụ gắn liền bên hông.
   - Gán từng box `person` riêng biệt cho người lái mô tô và hành khách ngồi trong thùng phụ.

7. **Vật thể giả tạo và Hiện tượng quang học (Tuyệt đối KHÔNG GÁN BOX):**
   - **Tượng đài, tác phẩm điêu khắc (`img_017.jpg`, `img_027.jpg`):** Bỏ qua hoàn toàn.
   - **Ma-nơ-canh trong/ngoài tiệm thời trang (`img_033.jpg`):** Bỏ qua hoàn toàn.
   - **Hình chân dung/phương tiện in trên biển quảng cáo (`img_018.jpg`):** Bỏ qua hoàn toàn.
   - **Mô hình đồ chơi thu nhỏ (`img_019.jpg`, `img_038.jpg`):** Bỏ qua hoàn toàn (nếu phức tạp khoanh `ignore_region`).
   - **Bóng phản chiếu qua gương chiếu hậu (`img_020.jpg`):** Bỏ qua hoàn toàn hình ảo trong gương.
   - **Người thật mặc trang phục hóa trang cosplay (`img_011.jpg` Predator):** **BẮT BUỘC GÁN `person`** vì bên trong là cơ thể người sinh học thực tế đang di chuyển.

8. **Ngưỡng kích thước tối thiểu (Minimum Size Threshold):**
   - Mọi đối tượng đơn lẻ có chiều cao $< 20\text{ px}$ **tuyệt đối không gán box riêng**.
   - Nếu là cụm người/xe dầy đặc ở cự ly xa, khoanh 1 box bao quát lớp `ignore_region`.

---

## 4. Bảng Phân Tích & Chốt Quyết Định Các Ca Khó Trong 40 Ảnh

Dưới đây là 10 ca thử thách điển hình đã được toàn bộ nhóm T005 phân tích và chốt quy tắc xử lý dứt khoát:

| STT | Mã ảnh | Hiện tượng quan sát thực tế | Vấn đề tranh cãi ở v0 | Quyết định thống nhất nhóm (v1.0) | Rule ID & Cơ sở lý luận an toàn |
|:---:|:---|:---|:---|:---|:---|
| 1 | `img_004.jpg`<br/>`img_035.jpg` | Xe Tuk-tuk / Auto Rickshaw 3 bánh chở khách tại Thái Lan / Ấn Độ. | v0 không có định nghĩa xe 3 bánh, dễ gây tranh cãi giữa `car`, `motorcycle` và `truck`. | **Gán box lớp `car`** cho toàn bộ thân xe tuk-tuk. Gán box `person` cho tài xế và hành khách nhìn thấy rõ. | **RULE-01 (Tuk-tuk as Car):** Phương tiện cơ giới 3 bánh có cabin, mái che chở khách, chiếm diện tích mặt đường tương đương ô tô mini. Gán `car` giúp xe tự lái giữ khoảng cách an toàn. |
| 2 | `img_002.jpg` | Xe tải chuyên dụng Renault chở nhiều xe ô tô con trên sàn rơ-moóc 2 tầng. | Gán 1 box xe tải hay gán cả các xe ô tô con bên trên? | Gán **1 box `truck`** cho xe tải mẹ; gán **từng box `car`** riêng cho các xe con trên sàn giàn giáo (`occluded_level = 1` hoặc `2`). | **RULE-02 (Vehicle on Vehicle):** Xe con trên giàn vẫn mang đầy đủ đặc trưng thị giác của xe con. Gán cả hai giúp mô hình phát hiện đa tầng đối tượng. |
| 3 | `img_012.jpg` | Xe bán tải (pickup truck) chở đầy nông sản bao tải rau củ trên thùng xe tại Hà Nội. | Dễ nhầm giữa ô tô con (`car`) và xe tải (`truck`). | Gán **1 box `truck`** bao toàn bộ thân xe bán tải và phần hàng hóa nằm gọn trong thùng. | **RULE-03 (Pickup as Truck):** Xe bán tải có kết cấu thùng hàng hở riêng biệt phía sau, công năng chở hàng $\rightarrow$ xếp vào `truck`. |
| 4 | `img_037.jpg` | Xe bán tải có gắn thêm nắp chụp thùng cao ngang nóc cabin (Master 75 Truck Cap). | Dễ nhầm lẫn giữa `truck`, `car` và `van`. | Gán **1 box `van`** bao quanh toàn bộ thân vỏ xe. | **RULE-04 (Canopy Pickup as Van):** Nắp chụp biến thùng hở thành khoang kín liền khối $\rightarrow$ đạt chuẩn định nghĩa của `van`. |
| 5 | `img_022.jpg` | Xe mô tô 3 bánh có thùng phụ chở khách bên hông (Sidecar). | Gán 1 box hay 2 box phương tiện? | Gán **1 box `motorcycle`** bao toàn bộ thân mô tô + thùng phụ. Gán **2 box `person`** riêng cho người lái và hành khách. | **RULE-05 (Sidecar Handling):** Thùng phụ gắn cố định vào xe máy tạo thành một khối cơ giới 3 bánh. Hai người chuyển động độc lập cần được theo dõi riêng. |
| 6 | `img_029.jpg` | Xe máy chở khối hàng xốp cồng kềnh khổng lồ che khuất người lái. | Hàng cồng kềnh có được vẽ chung vào box xe máy không? | Gán **1 box `motorcycle`** bao gồm khung xe và khối hàng gắn chặt vào xe; gán **1 box `person`** cho phần cơ thể người lái nhìn thấy. | **RULE-06 (Overloaded Motorbike):** Khối hàng di chuyển cùng xe tạo thành kích thước cản trở vật lý thực tế của phương tiện trên làn đường. |
| 7 | `img_011.jpg` | Người hóa trang trang phục quái vật ngoài hành tinh Predator đứng cạnh xe mô tô. | Người mặc trang phục cosplay dị thường có gán là `person` không? | **Bắt buộc gán box `person`** (`occluded_level = 0`). | **RULE-07 (Cosplay as Person):** Bên trong là con người sinh học đang di chuyển. Mô hình xe tự lái phải phát hiện được để bảo vệ tính mạng con người. |
| 8 | `img_027.jpg`<br/>`img_017.jpg` | Tượng đài tạc xe pickup bằng đá hoa cương (`img_027`) và tượng Wellington cưỡi ngựa (`img_017`). | Có hình dáng phương tiện/người nhưng là tượng điêu khắc. | **TUYỆT ĐỐI KHÔNG GÁN BOX.** | **RULE-08 (No Statues):** Tượng tĩnh vô tri. Gán box sẽ gây ra hiện tượng phanh khẩn cấp vô cớ (Phantom Braking). |
| 9 | `img_033.jpg` | Ma-nơ-canh mặc áo khoác đứng trong/ngoài tiệm thời trang Buchanan. | Dễ nhầm từ cự ly xa là người thật đang đứng. | **TUYỆT ĐỐI KHÔNG GÁN BOX.** | **RULE-09 (No Mannequins):** Ma-nơ-canh không có hành vi chuyển động giao thông. |
| 10 | `img_020.jpg`<br/>`img_018.jpg` | Xe phản chiếu trong gương chiếu hậu (`img_020`) và ảnh người in trên biển billboard (`img_018`). | Hình ảnh ảo và hình in 2D phẳng. | **TUYỆT ĐỐI KHÔNG GÁN BOX.** | **RULE-10 (No Virtual/2D Artifacts):** Không có nguy cơ va chạm cơ học trong thế giới thực. |

---

## 5. Quy trình Kiểm Soát Chất Lượng (QC) và Lịch Sử Thay Đổi

### 5.1. Ngưỡng kiểm soát chất lượng (QC Metrics & Thresholds)
Nhóm T005 cam kết tuân thủ tuyệt đối các ngưỡng QC trong `submission/taxonomy.json` và `docs/QC_CHEATSHEET.md`:
- **Ngưỡng kích thước box tối thiểu:** Chiều cao $\ge 20\text{ px}$.
- **Ngưỡng trùng khớp hình học (IoU Thresholds):**
  - Đối với box có chiều cao $\ge 50\text{ px}$: $\text{IoU} \ge 0.85$.
  - Đối với box có chiều cao từ $20\text{ px}$ đến $< 50\text{ px}$: $\text{IoU} \ge 0.70$.
  - Ngưỡng ghép cặp box (Matching IoU): $\text{IoU} \ge 0.50$.
- **Ngưỡng độ đồng thuận liên gán nhãn (Inter-Annotator Agreement - IAA):**
  - $\text{IoU trung bình} \ge 0.85$ trên toàn bộ các cặp box đã ghép.
  - $\text{Đồng thuận lớp (Class Agreement)} \ge 95\%$.
- **Ngưỡng chấp thuận phát hành tập nhãn (Release Threshold):** Tỉ lệ ảnh có lỗi sau kiểm định $\le 2\%$.

### 5.2. Quy trình xử lý ca mơ hồ trong lúc gán nhãn (Pha 3)
1. Gán theo quy tắc gần nhất trong guideline v1.0.
2. Đánh dấu thuộc tính `can_review = true`.
3. Ghi lại mã ảnh và mô tả vào sổ tay cá nhân.
4. Tuyệt đối không tự ý trao đổi hoặc sửa nhãn giữa chừng trong Pha 3 để đảm bảo tính độc lập tuyệt đối khi đo IAA ở Pha 4.

### 5.3. Bảng Lịch sử Phiên bản (Version History)

| Phiên bản | Ngày | Người thực hiện | Tóm tắt thay đổi cốt lõi | Ca thực tế kích hoạt |
|:---:|:---:|:---:|:---|:---|
| `v0` | 2026-11-16 | Giảng viên | Bản sơ sài đề bài cung cấp (cố ý thiếu ca khó, chưa có ngưỡng thuộc tính). | Đề bài khởi tạo ban đầu. |
| `v1.0` | 2026-11-16 | Toàn bộ Nhóm T005 | 1. Bổ sung mục tiêu an toàn và phân tích rủi ro phanh ma (Phantom Braking).<br/>2. Chính thức xếp xe Tuk-tuk / Auto Rickshaw 3 bánh vào lớp `car`.<br/>3. Phân biệt rõ xe bán tải thùng hở (`truck`) và bán tải gắn nắp chụp canopy (`van`).<br/>4. Định lượng ngưỡng phần trăm diện tích cho `occluded_level` ($< 10\%, 10-35\%, 35-70\%, \ge 70\%$).<br/>5. Định lượng ngưỡng mép biên ảnh cho `truncated` ($\ge 5\text{ px}$).<br/>6. Quy chuẩn quy tắc vẽ box cho xe chở xe (`img_002`), xe sidecar (`img_022`), xe chở hàng xốp (`img_029`).<br/>7. Cấm tuyệt đối gán box cho tượng đá, ma-nơ-canh, hình in quảng cáo, ảnh ảo trong gương chiếu hậu. | Thống nhất từ các bất đồng và phát hiện trong 40 ảnh thực tế sau Pha 1. |
