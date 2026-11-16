# Guideline gán nhãn — v0.1 — Thành viên 193 (Cao Thị Thúy Hiền)

> **Bản guideline cá nhân của thành viên 193**  
> Khảo sát độc lập trên toàn bộ 40 ảnh (`img_001.jpg` đến `img_040.jpg`), đặc biệt tập trung vào tập 27 ảnh được phân công trong `submission/qc/assignments/193.txt`.

- **Phiên bản**: v0.1-draft
- **Ngày lập**: 2026-11-16
- **Thành viên thực hiện**: Cao Thị Thúy Hiền (Mã: 193)
- **Công cụ áp dụng**: CVAT (Computer Vision Annotation Tool), xuất định dạng COCO 1.0

---

## 1. Mục tiêu và Yêu cầu An toàn

- **Mục đích sử dụng**: Tập dữ liệu bounding box 2D này được xây dựng để huấn luyện mô hình học sâu (Object Detection) nhận diện người và phương tiện giao thông đường phố, phục vụ trực tiếp cho hệ thống hỗ trợ lái xe nâng cao (ADAS) và xe tự hành (Autonomous Vehicles).
- **Phân tích rủi ro an toàn**:
  - **Bỏ sót vật thể (False Negative)**: Bỏ sót người đi bộ, người điều khiển xe máy hoặc xe đang lưu thông có thể dẫn tới tai nạn va chạm chết người.
  - **Phát hiện nhầm (False Positive)**: Nhận nhầm các vật thể tĩnh vô hại (tượng điêu khắc, hình vẽ biển quảng cáo, ma-nơ-canh, ảnh phản chiếu qua gương) thành chướng ngại vật thật sẽ khiến xe tự hành phanh gấp bất ngờ trên đường cao tốc/đô thị, gây nguy cơ tai nạn liên hoàn từ phía sau.
  - **Sai lệch kích thước box (Loose Box)**: Box vẽ quá rộng bao trùm cả khoảng không hoặc hàng hóa biến dạng sẽ làm sai lệch ước lượng khoảng cách và thời gian tới va chạm (TTC - Time to Collision).

---

## 2. Danh mục Lớp và Thuộc tính (Taxonomy Cá nhân)

### 2.1. Định nghĩa 8 lớp đối tượng

| Lớp | Định nghĩa (1 câu) | Ví dụ thực tế trong ảnh | Phản ví dụ / Dễ nhầm lẫn | Xử lý khi ngoài danh mục |
|---|---|---|---|---|
| `car` | Xe ô tô con từ 4 đến 9 chỗ phục vụ cá nhân hoặc dịch vụ (Sedan, Hatchback, SUV, Crossover, CUV). | Ô tô lưu thông bình thường (`img_001.jpg`, `img_010.jpg`, `img_021.jpg`, `img_040.jpg`); các ô tô con nằm trên sàn xe chở hàng (`img_002.jpg`). | Xe bán tải pickup cỡ lớn (thuộc `truck`); xe ô tô đồ chơi mô hình trong tủ kính (`img_038.jpg` - không gán). | Bỏ qua, không gán. |
| `truck` | Phương tiện vận chuyển hàng hóa cơ giới có thùng hàng riêng biệt, xe đầu kéo container, xe tải chở ô tô chuyên dụng, xe bán tải (pickup). | Xe tải chở hàng (`img_001.jpg`), xe tải chuyên dụng chở ô tô 2 tầng (`img_002.jpg`), xe bán tải nắp thùng cao (`img_037.jpg`). | Xe van chở khách/giao hàng nhỏ liền khối (`van`); xe 3 bánh chở hàng (`tuk_tuk`). | Bỏ qua. |
| `van` | Xe ô tô thùng kín liền khối cỡ nhỏ đến trung bình, thường dùng chở 9–16 hành khách hoặc vận chuyển hàng bưu kiện đô thị. | Xe van chở hàng cỡ nhỏ, xe van cứu thương đô thị, xe van chở khách gia đình. | Xe buýt lớn vận chuyển công cộng (`bus`); xe tải có khoang cabin tách rời thùng (`truck`). | Bỏ qua. |
| `bus` | Xe buýt công cộng nội đô hoặc xe khách đường dài trên 16 chỗ ngồi chuyên dùng chở hành khách. | Xe buýt lưu thông công cộng (`img_009.jpg`, `img_031.jpg`, `img_037.jpg`, `img_040.jpg`). | Xe ô tô con 7 chỗ (`car`); xe tải thùng kín cỡ lớn (`truck`). | Bỏ qua. |
| `tuk_tuk` | Xe cơ giới 3 bánh có động cơ dùng để vận chuyển hành khách hoặc chở hàng hóa (xe lam, tuk-tuk, xe lôi 3 bánh). | Xe tuk-tuk chở khách đường phố (`img_004.jpg`, `img_016.jpg`), xe 3 bánh chở hàng (`img_035.jpg`). | Xe máy 2 bánh (`motorcycle`); xích lô hoặc xe đạp 3 bánh không động cơ (`img_029.jpg` - không gán). | Bỏ qua. |
| `motorcycle` | Xe mô tô, xe gắn máy 2 bánh vận hành bằng động cơ đốt trong hoặc động cơ điện. | Xe máy lưu thông trên đường (`img_003.jpg`, `img_005.jpg`, `img_010.jpg`, `img_023.jpg`). | Xe đạp đẩy tay, xe đạp thể thao không động cơ (`img_006.jpg`, `img_029.jpg` - không gán). | Bỏ qua. |
| `person` | Người thật tham gia giao thông: người đi bộ, người đứng/ngồi ven đường, người đang điều khiển hoặc ngồi sau phương tiện. | Người đi bộ qua đường (`img_001.jpg`), người điều khiển xe máy (`img_005.jpg`, `img_010.jpg`). | Tượng đồng/tượng đá người (`img_011.jpg`, `img_017.jpg` - không gán); ma-nơ-canh cửa hiệu (`img_033.jpg` - không gán); ảnh chân dung trên pano quảng cáo (`img_018.jpg` - không gán). | Bỏ qua. |
| `ignore_region` | Vùng đánh dấu bỏ qua: khu vực tập trung đám đông xa xôi, cụm xe bị tắc nghẽn dày đặc hoặc đối tượng có chiều cao $< 20\text{ px}$. | Cụm phương tiện mờ ảo ở đường chân trời. Bỏ sót đối tượng trong vùng này không tính là lỗi QC. | Bất kỳ đối tượng đơn lẻ nào nhìn rõ và cao $\ge 20\text{ px}$ (phải vẽ box độc lập). | - |

---

### 2.2. Thuộc tính đối tượng và ngưỡng đo lường định lượng

1. **`occluded_level`** (Mức độ bị che khuất - đo bằng tỷ lệ diện tích bị che lấp):
   - **Mức `0` (Nhìn rõ hoàn toàn)**: Diện tích bị che khuất $< 1\%$. Toàn bộ đường bao vật thể hiển thị trọn vẹn trong tầm nhìn.
   - **Mức `1` (Che ít)**: Vật thể bị che khuất từ $1\%$ đến $30\%$ diện tích (ví dụ: bánh xe bị nắp cống hoặc vỉa hè che khuất nhẹ; người ngồi trên xe máy bị ghi-đông che phần chân dưới).
   - **Mức `2` (Che trung bình)**: Vật thể bị che khuất từ $31\%$ đến $70\%$ diện tích (ví dụ: chỉ nhìn thấy nửa thân trước của ô tô, hoặc chỉ nhìn thấy nửa người trên của người điều khiển).
   - **Mức `3` (Che nghiêm trọng)**: Vật thể bị che khuất $> 70\%$ diện tích nhưng người gán vẫn nhận dạng chắc chắn loại vật thể dựa trên các đặc trưng còn sót lại (ví dụ: chỉ lộ đầu và gương chiếu hậu của ô tô qua khe hở giữa hai xe khác).
2. **`truncated`** (Bị cắt bởi viền mép ảnh):
   - **`no`**: Vật thể nằm hoàn toàn bên trong khung ảnh, không tiếp xúc hoặc không bị cắt bởi bất kỳ cạnh nào của ảnh.
   - **`yes`**: Bất kỳ bộ phận nào của vật thể bị cắt ngang bởi 4 cạnh mép ảnh (dù chỉ cắt một phần nhỏ viền lốp xe, gương chiếu hậu hoặc đỉnh mũ bảo hiểm).
3. **`can_review`** (Cờ nghi ngờ cần hội chẩn):
   - **`false`** (mặc định): Tự tin với quyết định gán lớp và ranh giới box.
   - **`true`** (tick chọn): Đánh dấu khi đối tượng bị mờ nhòe do tốc độ (motion blur), thiếu sáng, hoặc có tranh cãi về ranh giới box để đưa ra thảo luận tại buổi họp Calibration.

---

## 3. Quy tắc vẽ Bounding Box chi tiết

- **Nguyên tắc ôm sát phần nhìn thấy (Tight Box)**:
  - Bounding box 2D phải tiếp xúc với các điểm cực viền (trái, phải, trên, dưới) của **phần nhìn thấy được** của vật thể.
  - Tuyệt đối không vẽ "phỏng đoán" mở rộng box bao phủ những vùng bị vật cản che khuất hoàn toàn.
- **Quy tắc phân tách Người và Xe máy (`img_005.jpg`, `img_010.jpg`, `img_023.jpg`)**:
  - Áp dụng nguyên tắc **2 box riêng biệt đè lên nhau**:
    1. Box lớp `motorcycle`: Ôm trọn vẹn toàn bộ các bộ phận của xe máy (từ lốp trước, lốp sau, gương chiếu hậu, biển số đến đuôi xe).
    2. Box lớp `person`: Ôm trọn vẹn toàn bộ người điều khiển hoặc người ngồi sau (từ đỉnh mũ bảo hiểm/đầu đến gót chân).
  - Hai box này sẽ có phần diện tích giao nhau tự nhiên (IoU chồng lấn).
- **Quy tắc Xe chuyên dụng chở ô tô (`img_002.jpg`)**:
  - Gán 1 box lớn lớp `truck` bao toàn bộ thân xe tải chuyên dụng (cabin + toàn bộ khung sàn nâng 2 tầng).
  - **Đồng thời** gán từng box riêng biệt lớp `car` cho toàn bộ **8 chiếc ô tô con** đang được chuyên chở trên hai tầng sàn (gán `occluded_level=1` hoặc `2` tùy theo mức độ bị khung sàn che).
  - *Lập luận*: Đối với xe tự hành, việc nhận diện từng chiếc ô tô con phía trên là thiết yếu để ước lượng chiều cao, trọng tâm và khoảng cách an toàn tránh va chạm.
- **Quy tắc Xe 3 bánh tuk-tuk chở hàng cồng kềnh (`img_035.jpg`)**:
  - Gán lớp `tuk_tuk`.
  - Box chỉ ôm sát khung cabin, thân xe và khoang chở hàng gắn liền nguyên bản của phương tiện.
  - **Không** kéo dãn box để bao trùm khối bao tải hàng hóa chất cao ngất ngưởng trên nóc xe, nhằm bảo tồn tỷ lệ hình học chuẩn (aspect ratio) của phương tiện đường phố.
- **Quy tắc loại trừ tuyệt đối đối tượng phi giao thông (Out of Scope)**:
  - **Tượng điêu khắc nghệ thuật** (`img_011.jpg`, `img_017.jpg` - tượng đồng người và ngựa; `img_027.jpg` - tượng đá hình xe bán tải): **Tuyệt đối không gán box**.
  - **Hình ảnh phản chiếu qua gương** (`img_020.jpg`): Không gán box cho ô tô phản chiếu trong gương chiếu hậu.
  - **Ma-nơ-canh và đồ chơi** (`img_033.jpg` - ma-nơ-canh trong tủ kính; `img_038.jpg` - ô tô đồ chơi trẻ em): **Tuyệt đối không gán box**.
  - **Hình in pano quảng cáo** (`img_018.jpg`): Không gán box cho khuôn mặt/người in trên biển quảng cáo 2D phẳng.
- **Quy tắc Phương tiện thô sơ không động cơ (`img_006.jpg`, `img_029.jpg`)**:
  - Xe đạp, xe xích lô đạp chân: Không gán lớp `motorcycle`. Nếu người đang đạp xe trên đường, chỉ gán 1 box `person` cho người (hoặc đánh dấu `ignore_region` cho cụm xe đạp nếu ở xa).
- **Quy tắc Đối tượng mờ nhòe do chuyển động (`img_014.jpg`, `img_015.jpg`)**:
  - Nếu đối tượng bị motion blur nhưng vẫn nhận dạng rõ hình bóng và phương tiện $\rightarrow$ Vẫn vẽ box ôm sát vệt mờ nhìn thấy và tick cờ `can_review = true`.
- **Ngưỡng kích thước tối thiểu và Vùng bỏ qua**:
  - Bất kỳ đối tượng nào có chiều cao thực tế dưới 20 pixel ($< 20\text{ px}$) không gán box đơn lẻ.
  - Sử dụng lớp `ignore_region` để bao bọc các vùng đám đông hoặc cụm xe ùn tắc ở đường chân trời.

---

## 4. Bảng ca khó khảo sát độc lập qua 40 ảnh

| ID Ảnh | Tình huống quan sát | Mã quy tắc | Quyết định cá nhân ban đầu | Lý do chi tiết |
|---|---|---|---|---|
| `img_001.jpg` | Xe tải thùng hở chở người và xe con phía trước. | `R-01` | Gán riêng 1 box `truck`, 1 box `car`, và các box `person` cho người đi bộ. | Nhận diện rõ ràng từng thực thể tham gia giao thông trên đường. |
| `img_002.jpg` | Xe tải chở hàng 2 tầng mang 8 ô tô con. | `R-02` | Gán 1 box `truck` cho xe tải mẹ và gán đủ 8 box `car` cho 8 xe con trên sàn. | Ban đầu từng băn khoăn xem xe con là hàng hóa tĩnh, nhưng chốt gán đủ để mô hình xe tự lái đo đạc chính xác chướng ngại vật rơi rớt. |
| `img_004.jpg` | Xe 3 bánh chở khách tuk-tuk. | `R-03` | Gán lớp `tuk_tuk`, không gán `car` hay `motorcycle`. | Đây là phương tiện cơ giới 3 bánh đặc thù đô thị châu Á, cần lớp riêng để học đúng đặc trưng hình học. |
| `img_005.jpg` | Hai người điều khiển xe máy đi song song. | `R-01` | Gán 2 box `person` và 2 box `motorcycle` đè nhau tương ứng. | Đảm bảo mô hình phân biệt được tư thế người điều khiển và kích thước xe máy. |
| `img_014.jpg` | Xe ô tô chuyển động nhanh bị vệt mờ chuyển động (motion blur). | `R-08` | Vẫn gán box `car` ôm sát vệt thân xe nhìn thấy; tick `can_review`. | Phương tiện đang di chuyển thực tế trên đường, không được phép bỏ sót dù bị mờ nhòe. |
| `img_017.jpg` | Tượng đồng hai nhân vật lịch sử đứng cạnh tượng ngựa kim loại. | `R-05` | **Không gán box** cho tượng người. | Công trình nghệ thuật điêu khắc công viên tĩnh, không có hành vi di chuyển; nếu gán sẽ gây cảnh báo giả. |
| `img_018.jpg` | Chân dung người mẫu in trên tấm pano quảng cáo lớn ven đường. | `R-06` | **Không gán box**. | Hình vẽ 2D phẳng trên bảng hiệu, không phải thực thể sống tham gia giao thông. |
| `img_020.jpg` | Hình ảnh xe ô tô phản chiếu sắc nét trong gương chiếu hậu xe chủ. | `R-06` | **Không gán box** cho xe trong gương. | Ảo ảnh quang học 2D; nếu gán box tại vị trí gương sẽ gây lỗi sai lệch tính toán khoảng cách 3D nghiêm trọng. |
| `img_027.jpg` | Khối tượng đá nguyên khối tạc hình xe bán tải pickup trưng bày. | `R-05` | **Không gán box** `truck` hay `car`. | Tác phẩm điêu khắc nghệ thuật bằng đá khối, không có động cơ hay khả năng di chuyển. |
| `img_029.jpg` | Xe xích lô chở hàng chạy bằng bàn đạp chân. | `R-07` | Không gán `motorcycle`; chỉ gán 1 box `person` cho người đạp xe. | Phương tiện không động cơ, không thuộc định nghĩa xe cơ giới. |
| `img_031.jpg` | Xe buýt lớn chở khách nội đô đi ở làn giữa. | `R-04` | Gán lớp `bus`, chọn `occluded_level=1`. | Xe buýt công cộng kích thước lớn, phân biệt rõ với xe van và xe con. |
| `img_033.jpg` | Ma-nơ-canh thời trang trưng bày đứng trong tủ kính showroom. | `R-05` | **Không gán box** `person`. | Vật vô tri trong nhà, không có nguy cơ xuất hiện trên làn đường di chuyển. |
| `img_035.jpg` | Xe tuk-tuk chở hàng hóa bao tải chất cao ngất ngưởng. | `R-03`, `R-07` | Gán 1 box `tuk_tuk` ôm sát cabin và sàn xe; **không bao khối bao tải**; tick `can_review`. | Khối hàng hóa biến dạng bất quy tắc; bao trùm hàng sẽ làm hỏng tỷ lệ kích thước xe của mô hình nhận diện. |
| `img_037.jpg` | Xe bán tải gắn nắp thùng cao (Master 75) chạy cạnh xe buýt lớn. | `R-04`, `R-08` | Gán xe buýt là `bus`; gán xe bán tải thùng cao là `truck`. | Xe bán tải dù gắn nắp thùng phụ kiện về bản chất cấu trúc khung gầm và đăng kiểm vẫn là xe tải chở hàng. |
| `img_038.jpg` | Dãy xe ô tô mô hình đồ chơi trẻ em trưng bày trong tủ kính. | `R-05` | **Không gán box** `car`. | Đồ chơi kích thước mini trong nhà, ngoài phạm vi giao thông thực tế. |
| `img_040.jpg` | Đuôi xe buýt công cộng cỡ lớn dừng đỗ ven đường. | `R-04` | Gán lớp `bus`, chọn `truncated=no`. | Xác định chính xác phương tiện giao thông công cộng từ góc nhìn phía sau. |

---

## 5. Kiểm soát Chất lượng (QC) và Lịch sử Phiên bản

### 5.1. Tiêu chí Kiểm soát Chất lượng áp dụng
- **Chỉ số tương đồng vị trí (IoU)**: Đạt $\ge 0.85$ đối với box lớn ($\ge 50\text{ px}$) và đạt $\ge 0.70$ đối với box nhỏ ($< 50\text{ px}$).
- **Độ đồng thuận phân lớp (Class Agreement)**: Đạt $\ge 95\%$ trên tổng số cặp box ghép được.
- **Tỷ lệ ảnh lỗi tối đa**: $\le 2.0\%$ (với lô 40 ảnh, chỉ cần 1 ảnh lỗi là vượt ngưỡng $\rightarrow$ buộc phải Rework).
- **Quyền quyết định ca nghi ngờ**: Các ca được tick cờ `can_review=true` sẽ được đưa ra buổi họp Calibration toàn nhóm để thống nhất và biểu quyết theo số đông.

### 5.2. Lịch sử Thay đổi Phiên bản
| Phiên bản | Ngày | Người thực hiện | Tóm tắt thay đổi | Cơ sở / Lý do |
|---|---|---|---|---|
| `v0` | 2026-11-16 | Giảng viên | Bản starter sơ sài, định tính, chỉ có 5 lớp cơ bản, chưa xử lý ca biên. | Tài liệu gốc phòng lab. |
| `v0.1-draft` | 2026-11-16 | 193 (Cao Thị Thúy Hiền) | 1. Bổ sung 2 lớp mới: `bus` và `tuk_tuk` (tổng 8 lớp).<br>2. Định lượng chính xác 4 mức phần trăm cho `occluded_level`.<br>3. Quy định gán 8 xe con trên xe tải chở ô tô (`R-02`).<br>4. Quy định vẽ box ôm thân tuk-tuk, bỏ bao tải cồng kềnh (`R-07`).<br>5. Loại bỏ toàn bộ tượng đá, tranh ảnh, ma-nơ-canh, đồ chơi (`R-05`). | Khảo sát độc lập trên 40 ảnh thực tế đường phố. |
