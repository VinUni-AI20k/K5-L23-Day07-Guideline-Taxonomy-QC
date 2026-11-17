# Guideline gán nhãn — v1.0 (Bản cá nhân)

- **Tác giả:** Nguyễn Bình Anh (Mã thành viên: 104 — Nhóm G003)
- **Phiên bản:** v1.0 (Nâng cấp từ `guideline_v0_starter.md` sau khảo sát 40 ảnh `img_001.jpg` – `img_040.jpg`)
- **Loại nhãn:** Bounding box (hộp chữ nhật 2D) trên ảnh đường phố
- **Công cụ & Định dạng:** CVAT, xuất COCO 1.0 (đồng bộ với `submission/taxonomy.json`)

---

## 1. Mục tiêu

### 1.1. Mục đích huấn luyện mô hình
Bộ dữ liệu dùng để huấn luyện và kiểm thử mô hình phát hiện đối tượng giao thông (2D Object Detection) phục vụ hệ thống camera giám sát giao thông thông minh và xe tự lái (ADAS / Autonomous Driving). Dữ liệu bao quát nhiều điều kiện môi trường (ban ngày, ban đêm, trời mưa, phơi sáng chuyển động) và mật độ giao thông đa dạng.

### 1.2. Rủi ro nếu gán nhầm vật giả thành người hoặc phương tiện thật
Việc gán nhầm các đối tượng phi giao thông (tượng đài, bia mộ điêu khắc, ma-nơ-canh, mascot, xe mô hình/đồ chơi, hình in 2D trên biển quảng cáo/thân xe, hình phản chiếu qua gương/kính) thành `person` hoặc phương tiện (`car`, `truck`, `van`, `motorcycle`) gây ra các hậu quả nghiêm trọng:
1. **Phanh khẩn cấp ảo (Phantom Braking):** Xe tự lái nhận diện nhầm tượng ven đường, ảnh người trên pano quảng cáo hoặc xe phản chiếu trong gương chiếu hậu là vật cản đang lao tới, kích hoạt phanh gấp đột ngột gây tai nạn.
2. **Sai lệch ước lượng khoảng cách và kích thước 3D:** Xe đồ chơi mô hình trong tủ kính hoặc ảnh phản chiếu trên mặt kính có tỷ lệ kích thước và tọa độ không gian sai lệch hoàn toàn, làm nhiễu thuật toán theo dõi đa đối tượng (Multi-Object Tracking).
3. **Suy giảm độ chính xác (Precision) và làm hỏng bộ kiểm định QC:** Tạo ra hàng loạt dương tính giả (False Positives), khiến mô hình học nhầm đặc trưng bề mặt phẳng 2D hoặc vật liệu tĩnh (đá, nhựa, đồng).

---

## 2. Lớp và thuộc tính

### 2.1. Định nghĩa các lớp chuẩn (`submission/taxonomy.json` v0)

Mỗi đối tượng hợp lệ chỉ thuộc **đúng một** lớp duy nhất:

| Lớp | Định nghĩa & Ranh giới phân biệt |
| :--- | :--- |
| `car` | Ô tô con chở khách dưới 9 chỗ (sedan, hatchback, SUV, crossover, taxi 4–7 chỗ, xe cổ). Không bao gồm xe bán tải có thùng hàng hở phía sau hoặc xe van thùng kín. |
| `truck` | Xe tải các loại (xe tải nhẹ thùng bạt/thùng kín, xe bán tải pickup có thùng hàng tách rời cabin, xe đầu kéo, xe tải chuyên dụng chở ô tô, xe tải dịch vụ gắn thùng cao). |
| `van` | Xe thùng kín nguyên khối thân liền (minivan, xe chở khách cỡ nhỏ 9–16 chỗ như Hyundai Starex/Ford Transit, xe van chở hàng cỡ nhỏ không tách rời cabin và khoang sau). |
| `motorcycle` | Phương tiện cơ giới 2 bánh hoặc 3 bánh có gắn thùng bên (xe số, xe tay ga, mô tô phân khối lớn, xe máy điện, xe mô tô ba bánh sidecar). |
| `person` | Con người thật đang đi bộ, đứng, ngồi trên vỉa hè, ngồi trong khoang mở hoặc điều khiển/ngồi sau xe máy, xe đạp. Tuyệt đối không gán cho tượng, ma-nơ-canh, mascot hay hình in. |
| `ignore_region` | Vùng bỏ qua (không phải một vật thể đơn lẻ): khoanh vùng các đám đông hoặc cụm xe xếp chồng lớp dày đặc không thể tách rời, vệt nhòe chuyển động mạnh, hoặc các đối tượng thật có chiều cao `< 20 px`. Bỏ sót vật thể nằm trong vùng này không tính là lỗi. |

### 2.2. Đề xuất mở rộng lớp cho phiên bản `taxonomy.json` tiếp theo
Qua khảo sát thực tế 40 ảnh, bộ dữ liệu xuất hiện nhiều phương tiện đặc thù không thuộc nhóm 5 lớp cơ bản. Đề xuất bổ sung 3 lớp sau vào danh mục nhóm:
- **`bicycle` (Đề xuất):** Xe đạp thô sơ, xe đạp thể thao, xe đạp chở hàng rong và xe xích lô đạp. *Xử lý tạm thời ở v0:* Bỏ qua (không gán vào `motorcycle` để tránh nhiễu đặc trưng động cơ và tốc độ), hoặc tick `can_review` nếu xe đạp gắn động cơ điện lai.
- **`bus` (Đề xuất):** Xe buýt công cộng và xe khách cỡ trung/lớn (> 16 chỗ). *Xử lý tạm thời ở v0:* Gán tạm vào `truck` nếu thân dài khung lớn hoặc `van` nếu xe khách cỡ nhỏ (< 16 chỗ) và tick `can_review`.
- **`tuk_tuk` (Đề xuất):** Xe ba bánh chở khách/chở hàng khoang mở đặc trưng châu Á (tuk-tuk Thái Lan, auto rickshaw Ấn Độ). *Xử lý tạm thời ở v0:* Gán tạm vào `motorcycle` (do kết cấu 3 bánh ghi-đông xe máy) kèm tick `can_review` để thống nhất toàn nhóm.

### 2.3. Thuộc tính và ngưỡng đo lường định lượng

| Thuộc tính | Giá trị | Ngưỡng đo lường & Quy ước áp dụng |
| :--- | :--- | :--- |
| `occluded_level` | `0` (mặc định) | **0% bị che khuất:** Nhìn thấy trọn vẹn 100% đối tượng (nếu bị cắt bởi cạnh biên ảnh thì tính ở `truncated`, vẫn để `occluded_level = 0`). |
| | `1` | **1% – 30% bị che khuất:** Che khuất nhẹ (ví dụ: che một phần bánh xe, bàn chân, hoặc đứng sau hàng rào song thưa nhưng vẫn rõ toàn bộ dáng). |
| | `2` | **31% – 70% bị che khuất:** Che khuất trung bình (ví dụ: người ngồi trong cabin xe tuk-tuk/ô tô chỉ lộ phần thân trên, xe đỗ hàng sau chỉ lộ phần đầu hoặc đuôi). |
| | `3` | **> 70% bị che khuất:** Che khuất nặng (chỉ lộ một phần nhỏ như mũ bảo hiểm + vai, hoặc một góc cản xe nhưng vẫn đủ cơ sở phân tách độc lập). |
| `truncated` | `no` (mặc định) | Đối tượng nằm trọn vẹn bên trong 4 cạnh biên của bức ảnh. |
| | `yes` | Đối tượng chạm và bị cắt ngang bởi ít nhất 1 trong 4 cạnh biên khung ảnh. |
| `can_review` | `false` (mặc định) | Ca rõ ràng, tuân thủ đúng quy tắc chuẩn. |
| | `true` (tick) | Ca mơ hồ về ranh giới lớp (ví dụ: xe buýt, xe tuk-tuk, xe trưng bày tĩnh) cần đưa vào vòng calibration/review của nhóm. |

### 2.4. Ngưỡng kích thước tối thiểu cho `ignore_region`
Theo thông số `min_box_height_px: 20` trong `taxonomy.json`:
- **Đối tượng đơn lẻ có chiều cao `< 20 px`:** Không vẽ box lẻ; nếu nằm rải rác ở cuối đường thì bỏ qua hoặc gộp vào `ignore_region` nếu tụ thành cụm.
- **Cụm đối tượng chồng lớp / nhòe chuyển động:** Khoanh vùng `ignore_region` bao trọn đám đông xếp nhiều lớp hoặc vệt xe nhòe (motion blur) không thể xác định đường biên thực.

---

## 3. Quy tắc vẽ box

1. **Box ôm sát mép ngoài cùng (Tight Box):**
   - Bốn cạnh box phải chạm sát các điểm cực trị ngoài cùng của phần đối tượng nhìn thấy được; sai số khoảng trống tối đa `1–2 px` (đặc biệt quan trọng với vật lớn `>= 50 px` yêu cầu `IoU >= 0.85`).
   - Tuyệt đối không vẽ box đoán phần bị vật cản che khuất hoặc phần nằm ngoài khung ảnh.
2. **Không kéo giãn box theo hàng hóa mang vác rời:**
   - Người gánh hàng rong, người vác thanh kim loại dài hoặc xe đạp chở hàng cồng kềnh: box chỉ ôm sát cơ thể người hoặc khung phương tiện, **không** trùm ra phần quang gánh/thanh nhôm nhô ra ngoài.
   - *Ngoại lệ:* Thùng hàng cố định nguyên khối gắn trên khung xe tải hoặc hàng hóa chằng cố định trên giá nóc xe chuyên dụng được tính là một phần thân xe.
3. **Tách riêng người và phương tiện hai/ba bánh:**
   - Người lái và người ngồi sau trên `motorcycle` phải gán tách thành các box `person` độc lập và một box `motorcycle` riêng.
4. **Người ngồi bên trong khoang mở/cabin:**
   - Nếu nhìn thấy rõ tài xế hoặc hành khách bên trong xe qua kính chắn gió hoặc khoang hở, gán thêm box `person` ôm phần cơ thể nhìn thấy với `occluded_level` tương ứng (`2` hoặc `3`).
5. **Bỏ qua tuyệt đối vật giả, hình in và ảnh phản chiếu (Không gán nhãn):**
   - **Tượng và điêu khắc:** Tượng đài, tượng nhân vật giả tưởng, tượng trang trí, bia mộ điêu khắc hình xe → **Bỏ qua**.
   - **Ma-nơ-canh, mascot và mô hình:** Ma-nơ-canh tủ kính, mô hình nhân vật hoạt hình, xe đồ chơi/mô hình thu nhỏ → **Bỏ qua**.
   - **Hình in 2D:** Ảnh người/xe trên biển quảng cáo, áp phích, tranh vẽ tường rào, decal dán trên kính xe → **Bỏ qua**.
   - **Hình phản chiếu:** Ảnh xe/người phản chiếu trong gương chiếu hậu, kính mũ bảo hiểm tráng gương, mặt kính cửa hàng → **Bỏ qua**.

---

## 4. Ca khó (Edge Cases từ `img_001.jpg` – `img_040.jpg`)

| Ảnh | Tình huống | Quyết định | Lý do |
| :--- | :--- | :--- | :--- |
| `img_001.jpg` | Xe bán tải Suzuki bị cắt phần đầu bên phải; khách ngồi bàn ăn bị che khuất nửa dưới bởi bàn và thùng xe. | Gán `truck` (`truncated = yes`, `occluded_level = 0`); gán `person` (`occluded_level = 2` hoặc `3`) cho khách ngồi bàn. | Xe chạm biên phải khung hình; khách là người thật nhưng bị vật cản che thân dưới. |
| `img_002.jpg` | Xe tải lồng chuyên dụng 2 tầng chở 7 ô tô con trên sàn xe. | Gán 1 box `truck` cho xe tải đầu kéo/rơ-moóc và gán `car` (`occluded_level = 1` hoặc `2`) cho từng ô tô con trên sàn. | Các ô tô con giữ nguyên hình dạng xe thật trên đường; hệ thống tự lái cần nhận diện cả xe tải lớn lẫn xe được chở. |
| `img_003.jpg` | Người bán hàng rong gánh hai thúng mít lớn đi trên vỉa hè. | Gán `person` chỉ ôm sát cơ thể người bán hàng (`occluded_level = 0`), không kéo box trùm cả đôi quang gánh. | Quang gánh là hàng hóa mang vác tách rời; kéo box theo thúng làm sai lệch tỷ lệ hình học chuẩn của lớp `person`. |
| `img_004.jpg` | Hai xe tuk-tuk Thái Lan đỗ chờ khách ban đêm, tài xế ngồi bên trong khoang lái. | Gán `motorcycle` + tick `can_review` (hoặc `tuk_tuk` khi cập nhật taxonomy); gán `person` (`occluded_level = 2`) cho tài xế. | Tài xế lộ rõ thân trên trong khoang mở nên cần tách nhãn `person` độc lập; xe tuk-tuk tick `can_review` để thống nhất lớp. |
| `img_005.jpg` | Nhiều người đi xe máy chen chúc cự ly gần, xe máy tiền cảnh bị cắt ngang mép dưới ảnh. | Tách từng `person` và `motorcycle`; các xe ở đáy ảnh gán `truncated = yes`, xe phía sau gán `occluded_level = 2–3`. | Đảm bảo nguyên tắc tách người – xe và phản ánh đúng việc mất thông tin ở cạnh dưới khung hình. |
| `img_006.jpg` | Dòng xe máy và xe đạp dày đặc ở cuối đường có kích thước rất nhỏ (`< 20 px`). | Khoanh vùng `ignore_region` cho cụm phương tiện/người `< 20 px` ở cuối đường. | Tuân thủ ngưỡng `min_box_height_px: 20` trong `taxonomy.json`, tránh vẽ box lẻ gây nhiễu nhãn. |
| `img_007.jpg` | Xe tải Isuzu Elf bên phải bị cắt nửa thân do mép phải ảnh; người đứng sau đầu xe tải chỉ lộ chân. | Gán `truck` (`truncated = yes`) cho xe Isuzu; gán `person` (`occluded_level = 3`) cho người sau xe. | Xe chạm biên phải khung ảnh; người sau xe tuy bị che >70% nhưng vẫn nhận diện rõ đôi chân đang đứng. |
| `img_008.jpg` | Hàng xe máy đỗ san sát nhau ban đêm trên vỉa hè với nhiều lớp chồng chéo. | Gán `motorcycle` cho các xe lộ rõ cấu trúc (`occluded_level = 0–2`); gộp `ignore_region` cho các xe lớp trong bị che >70% trong vùng tối. | Tránh ép vẽ box đoán mù cho các xe bị che khuất hoàn toàn trong điều kiện thiếu sáng ban đêm. |
| `img_010.jpg` | Hai người ngồi chung một xe máy (`29-K1 588.58`); xe đạp chở chuối xanh và treo nón lá cồng kềnh. | Gán 2 box `person` + 1 box `motorcycle` tách rời; bỏ qua xe đạp thô sơ ở v0 (hoặc gán `bicycle` khi mở rộng taxonomy). | Tuân thủ quy tắc tách từng người trên xe và không gán nhầm xe đạp thô sơ vào lớp xe cơ giới `motorcycle`. |
| `img_011.jpg` | Bức tượng khổng lồ nhân vật Predator bên phải; mô tô ba bánh độ hình quái thú trưng bày; đám đông rất xa. | **Bỏ qua** tượng Predator; gán `ignore_region` cho đám đông xa; gán `motorcycle` + tick `can_review` cho xe trưng bày tĩnh. | Tượng Predator là vật giả phi giao thông, gán `person` sẽ gây lỗi nghiêm trọng cho bộ nhận diện người. |
| `img_012.jpg` | Thùng sau xe bán tải mở nắp chở đầy hàng chiếm phần lớn góc dưới phải khung hình. | Gán `truck` (`truncated = yes`, `occluded_level = 0`) ôm trọn phần đuôi xe và hàng hóa nằm trong lòng thùng. | Xe bị cắt bởi mép dưới và mép phải ảnh; hàng hóa nằm gọn trong thùng xe tải. |
| `img_014.jpg` | Hiệu ứng phơi sáng chuyển động (motion blur): 2 người đi bộ rõ nét, xe máy chạy ngang nhòe thành vệt dài. | Gán `person` (`occluded_level = 0`) cho 2 người đi bộ; gán `ignore_region` cho các vệt xe máy nhòe mờ. | Vệt mờ chuyển động không còn ranh giới hình học xác định; vẽ box theo vệt nhòe làm sai kích thước thật của xe. |
| `img_015.jpg` | Đầu ô tô đỏ bên trái và đuôi Mercedes bạc bên phải bị cắt ở rìa ảnh; vệt nhòe xe chạy ngang hậu cảnh. | Gán `car` (`truncated = yes`) cho hai xe ở tiền cảnh; gán `ignore_region` cho vệt mờ chuyển động ở hậu cảnh. | Hai xe tiền cảnh rõ biên vật thể nhưng chạm biên ảnh; xe chạy ngang bị nhòe hoàn toàn. |
| `img_016.jpg` | Người phụ nữ áo đỏ góc dưới phải chỉ lộ từ vai trở lên; xe tuk-tuk bên trái bị cắt nửa thân. | Gán `person` (`truncated = yes`, `occluded_level = 0`) và `motorcycle` (`truncated = yes`, `can_review = true`). | Cả hai đều bị cắt bởi cạnh biên khung hình (dưới và trái), không phải bị vật thể khác che khuất. |
| `img_017.jpg` | Bức tượng đồng Công tước xứ Wellington cưỡi ngựa (đội cọc tiêu giao thông trên đầu). | **Bỏ qua hoàn toàn**, không gán `person`. | Đây là tượng đài bằng đồng cố định, không phải người tham gia giao thông. |
| `img_018.jpg` | Ảnh chân dung ứng cử viên (Lukáš Zicha) trên pano quảng cáo lớn; các ô tô đỗ sau hàng rào sắt. | **Bỏ qua** hình người trên biển quảng cáo; gán `car` (`occluded_level = 1`) cho các ô tô sau hàng rào. | Hình in 2D trên biển quảng cáo là vật giả; hàng rào sắt mảnh chỉ che <30% diện tích ô tô. |
| `img_019.jpg` | Mô hình chuột hoạt hình Danger Mouse ngồi cạnh người lái xe thật trên xe diễu hành vàng; khán giả đứng dày đặc sau rào. | Gán `person` (`occluded_level = 2`) cho người lái xe thật; **Bỏ qua** mô hình chuột; gán `ignore_region` cho đám đông xếp chồng phía sau. | Mascot/mô hình nhân vật hoạt hình không phải người thật; khán giả phía sau đứng nhiều lớp không tách được từng người. |
| `img_020.jpg` | Hình ảnh chiếc ô tô đang chạy phía sau phản chiếu trong gương chiếu hậu ngoài xe. | **Bỏ qua hoàn toàn**, không gán `car` trong mặt gương. | Ảnh phản chiếu trong gương có tọa độ không gian 3D đảo ngược và sai khoảng cách thực tế. |
| `img_022.jpg` | Ảnh đen trắng chụp mô tô ba bánh có thùng bên (sidecar) và người ngồi bên trong thùng. | Gán `motorcycle` ôm cả xe và thùng sidecar; gán `person` (`occluded_level = 2`) cho người ngồi trong thùng. | Thùng sidecar gắn liền tạo thành một phương tiện thống nhất; người ngồi trong thùng lộ phần đầu và vai. |
| `img_024.jpg` | Mô hình ô tô màu vàng thu nhỏ đặt trên giá nóc của chiếc xe cổ AMC Pacer màu đen trong bảo tàng. | Gán `car` cho chiếc xe cổ màu đen; **Bỏ qua** chiếc mô hình xe màu vàng trên nóc. | Chiếc xe vàng là mô hình thu nhỏ không có khả năng vận hành, gán `car` sẽ gây nhiễu tỷ lệ kích thước. |
| `img_027.jpg` | Bia mộ điêu khắc bằng đá granit đen bóng hình chiếc xe bán tải cổ trong nghĩa trang. | **Bỏ qua hoàn toàn**, không gán `truck` hay `car`. | Là bia đá điêu khắc tĩnh tại nghĩa trang, không phải phương tiện giao thông. |
| `img_028.jpg` | Bức tượng ngựa màu trắng đặt trên thùng chiếc xe bán tải cổ đỗ bên đường. | Gán `truck` cho chiếc xe bán tải cổ; **Bỏ qua** tượng ngựa trên thùng xe. | Xe bán tải là phương tiện giao thông thật đỗ bên đường, còn tượng ngựa là vật trang trí tĩnh. |
| `img_029.jpg` | Hai người đi xe máy điện và xe đạp cùng vác bó thanh nhôm rất dài qua đường. | Gán `person` và `motorcycle` (xe máy điện) chỉ ôm sát người và xe; **không** kéo dài box theo bó thanh nhôm. | Kéo box trùm thanh nhôm sẽ tạo ra một hộp chữ nhật rỗng khổng lồ bao trùm cả khoảng không đường phố. |
| `img_032.jpg` | Đám đông đứng chờ tại trạm xe buýt + hình in người trên pano trạm buýt; đầu xe Honda xanh bị cắt góc trái. | Gán `person` cho người hàng trước rõ dáng; gán `ignore_region` cho cụm người xếp lớp phía sau; **Bỏ qua** hình in trên pano; gán `car` (`truncated = yes`) cho xe xanh. | Phân tách rõ người thật đứng tách biệt, cụm người bị che khuất dày đặc và hình in 2D trên trạm buýt. |
| `img_033.jpg` | Ma-nơ-canh trong tủ kính, poster người mẫu và hình phản chiếu gương chiếu hậu ô tô chồng lớp qua mặt kính. | **Bỏ qua 100%**, không gán bất kỳ nhãn `person` hay `car` nào. | Tất cả đều là vật giả (ma-nơ-canh, ảnh in) và hình phản chiếu qua kính cửa hàng. |
| `img_035.jpg` | Xe ba bánh tự động (auto rickshaw) chất bao tải hàng hóa cao gấp đôi thân xe. | Gán `motorcycle` + tick `can_review` ôm trọn cả phần hàng hóa cố định trên nóc xe; gán `person` (`occluded_level = 2`) cho tài xế. | Khối hàng hóa được chằng cố định trên nóc tạo thành chiều cao vật lý thực tế của phương tiện khi lưu thông. |
| `img_038.jpg` | Hàng chục ô tô đồ chơi mô hình thu nhỏ và thú cao su trưng bày sau tủ kính cửa hàng. | **Bỏ qua hoàn toàn**, không gán `car`. | Toàn bộ là đồ chơi mô hình tỷ lệ nhỏ trưng bày trong tủ kính. |
| `img_040.jpg` | Ảnh chân dung cô gái dán trên kính chắn gió xe taxi; hình phản chiếu xe cộ trên kính mũ bảo hiểm tráng gương. | **Bỏ qua** ảnh dán trên kính xe và hình phản chiếu trên mũ bảo hiểm; chỉ gán `person`, `motorcycle`, `car` (taxi) thật. | Tránh dương tính giả từ hình in quảng cáo dán trên phương tiện và bề mặt phản xạ gương. |

---

## 5. QC và phiên bản

### 5.1. Tiêu chuẩn kiểm soát chất lượng (QC)
Mỗi ảnh sau khi gán nhãn phải đạt các chỉ số quy định trong `submission/taxonomy.json`:
- **Độ chính xác vị trí (IoU):** `>= 0.85` đối với vật thể lớn (`>= 50 px`) và `>= 0.70` đối với vật thể nhỏ (`< 50 px`).
- **Độ đồng thuận liên người gán (IAA):** `IoU >= 0.85` và đồng thuận phân lớp `>= 0.95`.
- **Tỷ lệ lỗi tối đa cho phép:** `<= 2%` số ảnh toàn lô (`error_rate_img_max: 0.02`).
- **Quy trình 4 bước tự kiểm tra (Self-QC) trước khi nộp:**
  1. Rà soát toàn bộ vật giả (tượng, ma-nơ-canh, mô hình, biển quảng cáo, gương phản chiếu) đảm bảo không gán nhầm nhãn.
  2. Kiểm tra tách riêng 100% cặp `person` + `motorcycle` và không kéo box theo vật mang vác rời.
  3. Kiểm tra ngưỡng chiều cao tối thiểu `>= 20 px` và vùng `ignore_region`.
  4. Kiểm tra đầy đủ 3 thuộc tính (`occluded_level`, `truncated` = `yes`/`no`, `can_review`).

### 5.2. Lịch sử phiên bản (Changelog)

| Phiên bản | Ngày | Người thực hiện | Nội dung thay đổi |
| :--- | :--- | :--- | :--- |
| `v0` | — | Giảng viên | Bản khởi đầu (`guideline_v0_starter.md`) gồm 6 lớp cơ bản và 3 thuộc tính, chưa có ngưỡng định lượng và danh mục ca khó. |
| `v1.0` | 2026-11-16 | Nguyễn Bình Anh (Nhóm G003) | - Bổ sung bối cảnh mô hình ADAS/xe tự lái và phân tích rủi ro gán nhầm vật giả.<br>- Chuẩn hóa ranh giới 6 lớp hiện hành và đề xuất mở rộng 3 lớp (`bicycle`, `bus`, `tuk_tuk`).<br>- Định lượng hóa `occluded_level` (0%, 1–30%, 31–70%, >70%), `truncated` (`yes`/`no`), `can_review` và ngưỡng `< 20 px` cho `ignore_region`.<br>- Bổ sung 5 quy tắc vẽ box và bảng xử lý 28 tình huống ca khó từ tập 40 ảnh `img_001.jpg` – `img_040.jpg`. |
