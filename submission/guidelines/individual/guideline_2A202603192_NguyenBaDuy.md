# Guideline gán nhãn — v0.3-individual — 2A202603192 - Nguyễn Bá Duy

- Phiên bản: v0.3 (Bản cá nhân cập nhật chuẩn hóa các lớp phương tiện: `bus`, `tuk_tuk`, `bicycle`)
- Ngày: 2026-11-16
- Người viết: Nguyễn Bá Duy (MSSV: 2A202603192, Mã thành viên: 192 / Điều phối viên nhóm T005)
- Nhiệm vụ: Đề xuất quy chuẩn gán nhãn cá nhân sau khi nghiên cứu 24 ảnh được phân công trong bộ 40 ảnh cảnh giao thông đường phố châu Á, cập nhật chuẩn hóa hệ thống 9 lớp hoàn chỉnh (`car`, `truck`, `van`, `bus`, `motorcycle`, `tuk_tuk`, `bicycle`, `person`, `ignore_region`).

---

## 1. Mục tiêu và Ý nghĩa An toàn
- Tập dữ liệu này được xây dựng để huấn luyện mô hình thị giác máy tính phát hiện đối tượng (Object Detection 2D) cho hệ thống lái xe tự động (Autonomous Driving - AD) và giám sát giao thông thông minh (ITS) tại môi trường giao thông hỗn hợp châu Á.
- Hệ quả an toàn trong vận hành xe tự lái:
  - **Bỏ sót người (`person`), xe đạp (`bicycle`) hoặc xe máy (`motorcycle`):** Là lỗi nghiêm trọng nhất (Critical Safety Hazard). Hệ thống không phát hiện được yếu tố tổn thương (Vulnerable Road Users - VRU), dẫn đến nguy cơ đâm va trực diện gây tử vong.
  - **Tách bạch phương tiện công cộng cỡ lớn (`bus`) và phương tiện đặc thù châu Á (`tuk_tuk`, `bicycle`):** 
    - Lớp `bus` (xe buýt, xe khách) có kích thước khổng lồ, điểm mù lớn và thường xuyên tấp lề đón trả khách. Tách biệt `bus` với `car`/`van`/`truck` giúp xe tự lái dự đoán điểm dừng đỗ công cộng và giữ khoảng cách an toàn rộng hơn.
    - Lớp `tuk_tuk` giúp phân biệt chính xác xe 3 bánh cơ giới chở khách (có động cơ, tốc độ trung bình, kết cấu hở) với ô tô con 4 bánh (`car`) và mô tô 2 bánh (`motorcycle`).
    - Lớp `bicycle` giúp nhận diện phương tiện thô sơ di chuyển chậm (xe đạp, xe xích lô đạp chân), hỗ trợ hệ thống tính toán gia tốc và quỹ đạo tránh vượt phù hợp.
  - **Gán nhãn sai cho ảo ảnh quang học (hình phản chiếu gương, tượng điêu khắc, đồ chơi, ma-nơ-canh):** Khiến xe tự lái phanh gấp vô cớ (Phantom Braking) khi di chuyển tốc độ cao, dẫn đến nguy cơ tai nạn liên hoàn từ các xe phía sau.

---

## 2. Lớp đối tượng và Thuộc tính đo lường

### 2.1 Định nghĩa 9 lớp đối tượng trong Taxonomy v1.0

| Lớp | Định nghĩa cốt lõi | Ví dụ hợp lệ trong ảnh giao thông | Phản ví dụ / Không gán |
|:---|:---|:---|:---|
| `car` | Phương tiện cơ giới 4 bánh có động cơ, kết cấu thân vỏ kín hoặc bán hở dùng chở người hoặc chở khách cỡ nhỏ (dưới 9 chỗ). | Sedan, SUV, Crossover, Hatchback, Taxi 4 bánh, xe diễu hành Dangermouse có người lái (`img_019`). | Xe bán tải chở hàng (`truck`), xe van chở hàng kín (`van`), xe buýt chở khách (`bus`), xe tuk-tuk 3 bánh (`tuk_tuk`). |
| `truck` | Phương tiện cơ giới chuyên dụng chở hàng hóa, có thùng hàng riêng biệt (thùng hở, thùng lửng, rơ-moóc hoặc sàn phẳng). | Xe tải thùng, xe ben chở đất, xe bồn, xe đầu kéo container, xe chuyên dụng chở xe con (`img_002`), xe bán tải (pickup truck, `img_012`, `img_036`). | Xe van chở hàng kín khoang liền cabin (`van`), xe ô tô con (`car`), xe buýt (`bus`), xe kéo tay thô sơ (không gán). |
| `van` | Xe ô tô thân thùng kín cỡ nhỏ đến vừa (khoảng 9-16 chỗ hoặc chở hàng kín), khoang lái và khoang chở hàng gắn liền thành một khối khí động học. | Xe chở hàng kín Ford Transit van, Mercedes Sprinter thùng kín, Suzuki Blind Van, xe bán tải gắn nắp thùng kín cao (truck cap / canopy, `img_037`). | Xe bán tải thùng hở (`truck`), SUV chở gia đình (`car`), xe buýt cỡ lớn (`bus`). |
| `bus` | Phương tiện cơ giới chở khách công cộng cỡ vừa và lớn (trên 16 chỗ), xe buýt hai tầng, xe khách đường dài. | Xe buýt nội đô tuyến đường phố (`img_032`), xe khách liên tỉnh, xe buýt trường học, xe đưa đón công nhân cỡ lớn. | Xe van 9-16 chỗ chở hàng kín (`van`), xe ô tô con chở khách 7 chỗ (`car`), xe tải (`truck`). |
| `motorcycle` | Phương tiện cơ giới 2-3 bánh chạy động cơ đốt trong hoặc động cơ điện. | Xe máy số, xe tay ga (scooter), xe mô tô phân khối lớn, xe ba bánh có gắn thùng phụ bên hông (sidecar, `img_022`). | Xe đạp, xe xích lô đạp chân (`bicycle`), xe tuk-tuk 3 bánh (`tuk_tuk`). |
| `tuk_tuk` | Phương tiện cơ giới 3 bánh gắn động cơ đốt trong hoặc động cơ điện, có kết cấu cabin/mái che dùng chở khách hoặc chở hàng nhẹ. | Xe Tuk-tuk Thái Lan (`img_035`), xe Auto Rickshaw Ấn Độ (`img_004`, `img_040`), xe lam 3 bánh. | Xe máy 2 bánh thông thường (`motorcycle`), xe ô tô con 4 bánh (`car`), xe buýt (`bus`), xe xích lô đạp chân (`bicycle`). |
| `bicycle` | Phương tiện thô sơ 2-3 bánh vận hành bằng bàn đạp sử dụng sức người (hoặc trợ lực điện nhẹ). | Xe đạp thể thao, xe đạp thông thường, xe xích lô du lịch đạp chân (`img_006`, `img_009`, `img_023`, `img_034`, `img_039`). | Xe máy chạy xăng (`motorcycle`), xe tuk-tuk có động cơ (`tuk_tuk`), xe đẩy tay hàng rong (không gán). |
| `person` | Cơ thể con người sống ở mọi tư thế: đi bộ, đứng, ngồi trên phương tiện, lái xe, đạp xe, bốc dỡ hàng hóa. | Người đi bộ qua đường (`img_014`), người lái xe máy, người ngồi sau xe máy (`img_029`), người đạp xích lô và khách ngồi xích lô (`img_006`), hành khách tại trạm xe buýt (`img_032`). | Ma-nơ-canh trong tủ kính (`img_033`), tượng đài điêu khắc (`img_017`, `img_027`), hình người in trên biển quảng cáo (`img_018`), búp bê đồ chơi (`img_038`). |
| `ignore_region` | Vùng không gian trong ảnh không gán chi tiết từng đối tượng do quá xa, mờ nhòe, hoặc tập hợp đông đúc dưới ngưỡng phát hiện; không tính lỗi phạt khi bỏ sót trong vùng này. | Cụm người đi bộ ở hậu cảnh xa xôi có chiều cao $< 20\text{ px}$, xe bị che khuất $> 80\%$, biển quảng cáo in hình phương tiện lớn, tủ trưng bày đồ chơi phức tạp. | Bất kỳ phương tiện hay con người nào nhìn thấy rõ ranh giới và có chiều cao $\ge 20\text{ px}$. |

### 2.2 Thuộc tính đo lường định lượng

1. **`occluded_level` (Mức độ che khuất - đo theo diện tích hình chiếu):**
   - `0`: Nhìn thấy rõ $\ge 90\%$ diện tích thân xe hoặc cơ thể người.
   - `1`: Bị che khuất nhẹ từ $10\%$ đến $35\%$ diện tích bởi vật cản khác (cột đèn, xe khác, mép cây).
   - `2`: Bị che khuất trung bình từ $35\%$ đến $70\%$ diện tích (vẫn nhận diện được đặc trưng chính như bánh xe, đầu xe, thân trên người).
   - `3`: Bị che khuất nặng $> 70\%$ diện tích nhưng còn đủ manh mối nhận biết (đầu người đội mũ, góc gương xe).
2. **`truncated` (Bị cắt bởi mép biên ảnh):**
   - `no`: Toàn bộ ranh giới vật thể nằm trọn vẹn trong khung hình ảnh.
   - `yes`: Vật thể bị cắt cụt bởi mép viền ảnh $\ge 5\text{ px}$.
3. **`can_review` (Đánh dấu trường hợp nghi ngờ/tranh chấp):**
   - `true`: Bật cờ khi gặp trường hợp mơ hồ (ví dụ: xe độ kỳ dị, hình dạng khó phân biệt giữa van và bus, người bị che khuất ở ranh giới 20px) để đưa ra hội chẩn nhóm (Calibration).
   - `false`: Trường hợp rõ ràng, tuân thủ đúng quy tắc.

---

## 3. Quy tắc vẽ Bounding Box (Quy chuẩn kỹ thuật)

1. **Nguyên tắc biên nhìn thấy thực tế (Visible Boundary Principle):**
   - Bounding box phải ôm sát các pixel thực sự nhìn thấy được của vật thể. Không tự suy diễn mở rộng box vào phần không nhìn thấy (bị che khuất hoàn toàn hoặc nằm ngoài mép ảnh).
2. **Quy tắc cho Xe buýt (`bus`):**
   - Box `bus` ôm sát toàn bộ thân vỏ xe buýt nhìn thấy được (từ nóc xe đến đáy lốp xe tiếp đất).
   - Hành khách ngồi bên trong cửa sổ kính xe buýt: **Không gán box `person` riêng lẻ** để tránh gây rối loạn bộ đếm hành khách. Chỉ gán `person` cho tài xế hoặc hành khách đang đứng thò nửa người ra ngoài cửa lên xuống hoặc bước xuống mặt đường.
3. **Quy tắc ghép đôi Người - Phương tiện 2/3 bánh (Coupling & Overlap):**
   - Khi có người điều khiển hoặc ngồi trên xe máy (`motorcycle`), xe đạp/xích lô (`bicycle`), hoặc xe tuk-tuk hở cabin (`tuk_tuk`):
     - Vẽ **1 box `person`**: Ôm trọn vẹn người từ đỉnh đầu (hoặc đỉnh nón bảo hiểm) đến mép gót chân/bàn đạp chân.
     - Vẽ **1 box phương tiện (`motorcycle`, `bicycle`, hoặc `tuk_tuk`)**: Ôm toàn bộ kết cấu cơ học của xe (từ ghi-đông/mái che đến điểm tiếp đất của bánh xe). Hai box này chấp nhận chồng lấn hình học lên nhau.
4. **Quy tắc hàng hóa và phụ kiện phương tiện:**
   - Hàng hóa nằm trong lòng thùng xe tải/xe bán tải: Box `truck` ôm cả thân xe và khối hàng hóa.
   - Xe máy chở hàng hóa cồng kềnh bất thường (`img_029`):
     - Box `motorcycle` ôm trọn vẹn khung sườn xe và các khối hàng gắn chặt vào thân xe.
     - Box `person` ôm phần cơ thể người lái nhìn thấy được (`occluded_level = 2` hoặc `3`).
   - Xe mô tô có thùng phụ bên hông (Sidecar, `img_022`): Vẽ 1 box `motorcycle` lớn bao quát toàn bộ xe máy + thùng phụ bên hông; vẽ từng box `person` cho người lái và người ngồi trong sidecar.
5. **Ngưỡng kích thước tối thiểu (Minimum Size Threshold):**
   - Mọi đối tượng có chiều cao hình chiếu $< 20\text{ px}$ **tuyệt đối không gán box đơn lẻ**. Nếu nằm trong khu vực đông đúc, gom toàn bộ cụm đó vào 1 box `ignore_region`.

---

## 4. Phân tích chi tiết các ca khó thực tế trong 24 ảnh được phân công

Dưới đây là các ca thử thách tiêu biểu trong danh sách 24 ảnh thuộc nhiệm vụ gán của Nguyễn Bá Duy:

| Mã ảnh | Hiện tượng quan sát | Đề xuất quyết định | Cơ sở lý luận & Ý nghĩa an toàn |
|:---|:---|:---|:---|
| `img_032.jpg` | Trạm dừng xe buýt nội đô đông đúc người chờ và xe buýt lớn ghé trạm. | Gán 1 box `bus` cho thân xe buýt. Gán từng box `person` cho người chờ xe có chiều cao $\ge 20\text{ px}$. Đám đông chen chúc ở quá xa $< 20\text{ px}$ khoanh vào `ignore_region`. | Xe buýt là phương tiện công cộng cỡ lớn cần cảnh báo vùng đệm an toàn; người chờ xe ở mép đường là đối tượng VRU có nguy cơ ngã vào làn xe. |
| `img_035.jpg` | Xe Tuk-tuk / Auto Rickshaw 3 bánh chở đông đảo hành khách tại Ấn Độ / Thái Lan. | Gán 1 box `tuk_tuk` cho toàn bộ thân xe tuk-tuk. Gán box `person` cho tài xế và từng hành khách nhìn thấy rõ $\ge 20\text{ px}$ (`occluded_level = 1` hoặc `2`). | Tuk-tuk là phương tiện cơ giới 3 bánh đặc thù có động cơ, được định danh chuẩn bằng lớp `tuk_tuk`. Hành khách hở một phần cơ thể cần được theo dõi để tránh va quệt. |
| `img_006.jpg` | Xe xích lô du lịch chở khách nước ngoài tại Huế. | Gán 1 box `bicycle` cho toàn bộ khung xe xích lô 3 bánh đạp chân. Gán 2 box `person`: 1 cho người đạp xích lô phía sau, 1 cho du khách ngồi phía trước. | Xích lô vận hành bằng sức người đạp chân, thuộc phân loại phương tiện thô sơ `bicycle`. Hai người trên xe cần được nhận diện độc lập để đảm bảo an toàn VRU. |
| `img_012.jpg` | Xe bán tải chở đầy các bao tải rau củ quả dạng lưới xanh di chuyển trên đường Hà Nội. | Gán 1 box `truck` bao quanh toàn bộ thân xe bán tải và phần rau củ chất đầy trên thùng xe (`occluded_level = 0`, `truncated = no`). | Thùng hàng hở phía sau đạt chuẩn phân loại `truck`. Hàng hóa là một phần thể tích cản trở mà cảm biến xe tự lái cần nhận diện để giữ khoảng cách an toàn. |
| `img_020.jpg` | Hình ảnh nhìn từ trong buồng lái xe, quan sát thấy các xe ô tô và xe máy phản chiếu trong gương chiếu hậu (rearview mirror). | **Không gán box** cho các phương tiện và người nhìn thấy trong mặt gương phản chiếu. Khung gương của xe chủ có thể khoanh `ignore_region` hoặc không gán. | Hình ảnh phản chiếu trong gương là vật thể ảo. Gán nhãn xe ở đây sẽ khiến hệ thống tự lái nhận diện có vật cản ngay trước mặt xe chủ, kích hoạt phanh khẩn cấp vô lý (Phantom Braking). |
| `img_029.jpg` | Xe máy chở khối lượng hàng hóa xốp cồng kềnh khổng lồ trên đường phố Việt Nam, người lái gần như bị che lấp. | Gán 1 box `motorcycle` bao gồm khung xe máy và toàn bộ khối hàng hóa cồng kềnh gắn liền. Gán 1 box `person` cho người lái xe (`occluded_level = 2` hoặc `3`). | Khối hàng khổng lồ di chuyển cùng vận tốc xe máy tạo thành một chướng ngại vật đồng nhất trên đường; người lái vẫn cần được nhận diện để bảo vệ tính mạng. |
| `img_019.jpg` | Xe ô tô diễu hành hình nhân vật hoạt hình Danger Mouse màu vàng, có bánh xe, khung gầm và người lái bên trong. | Gán 1 box `car` bao quát toàn bộ thân xe diễu hành độc dị này. Gán 1 box `person` cho người điều khiển nhìn thấy trong cabin (`occluded_level = 2`). | Dù hình thù kỳ dị, đây vẫn là phương tiện cơ giới 4 bánh có người lái lưu thông trên mặt đường, mang đầy đủ động học va chạm của một chiếc `car`. |
| `img_022.jpg` | Xe mô tô cổ 3 bánh gắn thùng phụ chở khách bên hông (Sidecar). | Gán 1 box `motorcycle` bao quát cả thân mô tô và thùng phụ bên cạnh. Gán 2 box `person` riêng biệt: 1 cho người điều khiển mô tô và 1 cho hành khách ngồi trong thùng phụ. | Thùng phụ gắn cố định vào xe máy tạo thành một phương tiện cơ giới 3 bánh; 2 người ngồi độc lập cần được theo dõi chuyển động riêng biệt. |
| `img_038.jpg` | Quầy hàng lưu niệm trưng bày nhiều mô hình xe ô tô thu nhỏ (toy cars) và búp bê đồ chơi. | **Tuyệt đối không gán** các mô hình xe đồ chơi thành `car` và búp bê thành `person`. Khoanh 1 vùng `ignore_region` cho toàn bộ sạp hàng trưng bày nếu nằm ở cự ly gần. | Đồ chơi thu nhỏ không phải là người tham gia giao thông và không gây nguy hiểm va chạm cơ giới. Gán nhãn sẽ gây nhiễu nghiêm trọng cho bộ trích xuất đặc trưng của mạng nơ-ron. |

---

## 5. Quy trình Kiểm soát Chất lượng (QC) và Lịch sử Phiên bản

### 5.1 Tiêu chí nghiệm thu QC
- **Độ trùng khớp hình học (Geometric IoU):** IoU giữa các annotator độc lập đối với cùng một đối tượng phải đạt $\ge 0.85$ (với vật thể cao $\ge 50\text{ px}$) và $\ge 0.70$ (với vật thể cao từ $20\text{ px}$ đến $< 50\text{ px}$).
- **Đồng thuận phân lớp (Classification Agreement):** Tỉ lệ đồng thuận nhãn lớp đối với các box bắt cặp $\ge 95\%$.
- **Cơ chế xử lý tranh chấp:**
  - Bật thuộc tính `can_review = true` trên box hoặc ghi vào `image_issues.csv` khi phát hiện các trường hợp mơ hồ để đưa ra phiên hiệu chuẩn (Calibration) của nhóm.

### 5.2 Lịch sử phiên bản
- **`v0.1` (2026-11-16):** Bản khởi tạo độc lập của Nguyễn Bá Duy dựa trên taxonomy 6 lớp cơ bản.
- **`v0.2` (2026-11-16):** Bổ sung 2 lớp phương tiện chuyên biệt `tuk_tuk` (xe 3 bánh có động cơ) và `bicycle` (xe đạp, xích lô).
- **`v0.3` (2026-11-16):** Bổ sung lớp `bus` (xe buýt, xe khách công cộng cỡ lớn) hoàn thiện hệ thống 9 lớp; xác lập quy tắc không gán hành khách bên trong cửa sổ xe buýt trừ trường hợp thò người ra ngoài hoặc lên xuống xe.
