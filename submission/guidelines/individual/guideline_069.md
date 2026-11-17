# Guideline gán nhãn — v0.1 — Thành viên 102

> Bản guideline cá nhân (Pha 1) được xây dựng độc lập bởi Thành viên 102 dựa trên khảo sát 40 ảnh dữ liệu thực tế và khắc phục các điểm mơ hồ của bản v0.

- Phiên bản: v0.1 (Bản cá nhân)
- Ngày: 2026-11-16
- Người viết / duyệt: Thành viên 102

---

## 1. Mục tiêu

- **Mục đích mô hình**: Huấn luyện mô hình phát hiện đối tượng 2D (2D Object Detection) phục vụ bài toán giám sát giao thông thông minh và xe tự hành (ADAS / Autonomous Driving).
- **Nhiệm vụ nhãn**: Phát hiện và định vị chính xác vị trí, kích thước (bounding box) cùng các thuộc tính trạng thái của người tham gia giao thông và các phương tiện di chuyển trên đường phố.
- **Rủi ro khi gán sai**:
  - Bỏ sót hoặc gán sai người (`Person`, `Driver`) dẫn đến nguy cơ va chạm gây nguy hiểm trực tiếp đến tính mạng con người.
  - Nhầm lẫn giữa tượng (`Statue`) hoặc hình in/phản chiếu với người thật khiến hệ thống phanh gấp không cần thiết.
  - Nhầm lẫn kích thước phương tiện (như xe tải `Truck`, xe khách `bus` hay xe kéo `other_vehicle`) dẫn đến ước tính sai khoảng cách an toàn và quỹ đạo di chuyển.

---

## 2. Lớp và thuộc tính

### Lớp

| Lớp | Định nghĩa (một câu) | Ví dụ thực tế | Phản ví dụ / Dễ nhầm với (Miss understanding) |
|---|---|---|---|
| `Person` | Là con người, đang đi bộ hoặc đứng/ngồi trên vỉa hè, lề đường (không điều khiển phương tiện). | Người đi bộ qua đường, người đứng cạnh xe bán tải (`img_001.jpg`, `img_010.jpg`, `img_014.jpg`, `img_025.jpg`). | `Statue` (tượng người, ma-nơ-canh), `Driver` (người đang điều khiển phương tiện giao thông). |
| `Driver` | Là con người đang trực tiếp ngồi điều khiển phương tiện giao thông. | Người lái xe máy (`img_005.jpg`, `img_008.jpg`, `img_026.jpg`), người đạp xích lô (`img_006.jpg`, `img_009.jpg`), tài xế xe tuk-tuk (`img_035.jpg`). | `Person` (người đi bộ hoặc hành khách ngồi sau không lái), `Statue` (tượng nhân vật mô phỏng người lái). |
| `Car` | Là phương tiện giao thông, có từ 4 bánh trở lên và thường được dùng để chở người. | Ô tô con 4-7 chỗ, sedan, SUV lưu thông trên đường hoặc được chở trên sàn xe tải (`img_002.jpg`, `img_024.jpg`, `img_040.jpg`). | `van` (xe thùng kín cỡ nhỏ chở hàng/người có khoang ca-bin to liền phía sau). |
| `Truck` | Là phương tiện giao thông có từ 4 bánh trở lên, thường được dùng để chở hàng, thường sẽ có một thùng hàng ở phía sau. | Xe bán tải chở hàng hở thùng (`img_001.jpg`, `img_012.jpg`), xe tải chuyên dụng chở ô tô (`img_002.jpg`), xe tải giao hàng (`img_007.jpg`, `img_036.jpg`). | `van` (xe thùng kín liền khối, không có thùng hàng riêng biệt phía sau), `Statue` (tượng đài tạc hình xe tải như `img_027.jpg`). |
| `van` | Là phương tiện giao thông, có 4 bánh trở lên và có thể được dùng để chở người hoặc chở hàng, thường sẽ có một cabin to ở phía sau. | Xe tải van thùng kín, xe bán tải gắn nắp thùng kín cao kéo dài chở hàng (`img_037.jpg`). | `Car` (ô tô con chở người thông thường không có cabin to kéo dài), `Truck` (xe có thùng hàng rời tách biệt). |
| `Motorcycle` | Là phương tiện giao thông, có 2 bánh xe và có bô (ống xả). | Xe máy, mô tô gắn máy chạy xăng/động cơ có bô (`img_005.jpg`, `img_008.jpg`, `img_026.jpg`, `img_030.jpg`). | `Bicycle` (xe đạp 2 bánh không có ống xả), `3_wheelers_vehicle` (xe 3 bánh hoặc xe máy gắn sidecar như `img_022.jpg`). |
| `Bicycle` | Là phương tiện giao thông, có 2 bánh xe nhưng mà không có bô. | Xe đạp thường, xe đạp địa hình, xe đạp trợ lực không có ống xả bô (`img_010.jpg`, `img_021.jpg`). | `Motorcycle` (xe 2 bánh chạy bằng động cơ có ống xả bô). |
| `3_wheelers_vehicle` | Là phương tiện giao thông, nhưng mà có 3 bánh xe. | Xe tuk-tuk chở khách (`img_004.jpg`, `img_016.jpg`, `img_035.jpg`), xe xích lô 3 bánh (`img_006.jpg`, `img_009.jpg`, `img_023.jpg`), xe mô tô gắn thùng phụ sidecar 3 bánh (`img_022.jpg`). | `Motorcycle` (xe 2 bánh), `Bicycle` (xe đạp 2 bánh). |
| `Statue` | Là bức tượng, có thể có hình dáng con người, động vật, phương tiện,... | Tượng quái vật Predator (`img_011.jpg`), tượng đài tướng quân cưỡi ngựa (`img_017.jpg`), tượng đài xe bán tải bằng đá (`img_027.jpg`), ma-nơ-canh (`img_033.jpg`), đồ chơi/mô hình (`img_038.jpg`). | `Person` (người thật đi bộ), `Driver` (người thật đang lái xe), `Truck`/`Car` (xe thật đang hoạt động). |
| `other_vehicle` | Phương tiện giao thông khác không thuộc các lớp trên (ví dụ: xe đẩy hàng, xe kéo tay thô sơ). | Xe kéo tay thô sơ, xe đẩy chở hàng trên đường (`img_028.jpg`). | `3_wheelers_vehicle`, `Truck`. |
| `ignore_region` | Vùng bỏ qua không gán nhãn từng vật riêng lẻ. | Vùng đám đông dày đặc ở quá xa, hình phản chiếu lớn trên vũng nước/gương, các vật thể nhỏ hơn ngưỡng 20x20 pixel. | Các đối tượng riêng lẻ nhìn rõ, kích thước ≥ 20x20 pixel. |

**Quy định với vật không thuộc lớp nào**:
- Các vật thể như động vật, cây cối, cột đèn, biển báo, công trình kiến trúc: **Không gán bounding box**.
- Vùng đám đông dày đặc ở hậu cảnh xa xôi hoặc cụm vật thể nhỏ li ti không thể phân định ranh giới: Gán vùng `ignore_region` hoặc bỏ qua không gán box.

---

### Thuộc tính (Attributes)

Mỗi bounding box được gán các thuộc tính tương ứng với các mức định lượng cụ thể:

1. **`occluded_level`** (Mức độ che khuất):
   - **`0`**: Không bị che — toàn bộ đường bao và bề mặt đối tượng nhìn thấy rõ ràng 100%, không bị cản trở bởi bất kỳ vật thể nào.
   - **`1`**: Bị che một phần bởi các đối tượng/vật thể khác (tỉ lệ che khuất từ 1% đến dưới 80%), hoặc đối tượng bị mất một phần do bị mép ảnh cắt ngang.
   - **`2`**: Bị che khuất trên 80%, các chi tiết nhận dạng bị che phần lớn, không xác định rõ ranh giới hình học.
   - **`3`**: Bị che khuất hoàn toàn hoặc không xác định được mức che, đối tượng chỉ thấy mờ mờ, lẫn vào hậu cảnh và không rõ ranh giới.

2. **`truncated`** (Bị cắt bởi mép ảnh):
   - **`no`**: Vật thể nằm trọn vẹn bên trong khung ảnh, không chạm hoặc bị cắt bởi bất kỳ cạnh nào của ảnh.
   - **`yes`**: Một phần thân thể hoặc bộ phận của vật thể vượt ra ngoài mép viền của bức ảnh.

3. **`can_review`** (Cần xem lại / Ca nghi vấn):
   - **`false`**: Tự tin với quyết định gán nhãn, box ôm sát và đúng lớp.
   - **`true`**: Tick khi người gán phân vân về lớp (ví dụ giữa `van` và `Truck`, giữa `Statue` và `Person`), hoặc ranh giới bị che khuất khó xác định, cần reviewer hoặc cả nhóm xem xét lại ở phiên calibration.

---

## 3. Quy tắc vẽ box (Bounding Box Guidelines)

Quy tắc chung cốt lõi: **Bounding box phải ôm sát vật thể (Tight Bounding Box)**, chỉ bao trọn phần hình ảnh nhìn thấy được của đối tượng, không vẽ box bao phần suy đoán ảo trong không gian bị che khuất.

- **Mã quy tắc `R-01` [Ôm sát vật thể]**: Mép trên, dưới, trái, phải của bounding box phải tiếp xúc chính xác với các điểm ngoài cùng của vật thể nhìn thấy. Không vẽ box quá rộng thừa nhiều nền (padding) và không cắt lẹm vào chi tiết vật thể.
- **Mã quy tắc `R-02` [Quy tắc vẽ box cho Person]**:
  - **Chiều cao**: Bounding box phải ôm được từ phần đỉnh đầu (hoặc đỉnh mũ/nón nếu có đội) xuống đến gót chân của đối tượng.
  - **Chiều ngang**: Phải ôm được hai điểm xa nhất của cơ thể (thường là mép ngoài bàn tay, mép cùi chỏ, gót bàn chân hoặc mũi chân khi đang sải bước).
  - **Phụ kiện đi kèm**: Box phải bao trọn các vật thể mà người đó mang theo liền trên cơ thể như nón bảo hiểm, mũ, balo mang sau lưng, túi xách đeo bên người. (Không bao vật thể độc lập đặt dưới đất).
- **Mã quy tắc `R-03` [Quy tắc vẽ box cho phương tiện giao thông]**:
  - Áp dụng cho: `Car`, `bus`, `Bicycle` (bike), `Truck`, `van`, `Motorcycle`, `3_wheelers_vehicle`, `other_vehicle`.
  - **Chiều cao**: Phải bao trọn từ điểm cao nhất của xe (mui xe, đầu xe, giá nóc) xuống đến điểm tiếp xúc của bánh xe với mặt đất.
  - **Chiều rộng/ngang**: Phải ôm trọn chiều dài dài nhất của xe nhìn thấy (từ mép cản trước đến cản sau, hoặc mép gương chiếu hậu hai bên).
  - Đối với các phương tiện còn lại (`other_vehicle`, `3_wheelers_vehicle`), áp dụng nguyên tắc tương tự: bao trọn toàn bộ cấu trúc thân xe và điểm bánh xe chạm đất.
- **Mã quy tắc `R-04` [Ca khó: Người điều khiển phương tiện (Driver vs Vehicle)]**:
  - Khi một người (`Person`/`Driver`) ngồi điều khiển các phương tiện giao thông (tất cả các lớp xe):
    - **Vẽ 1 bounding box riêng cho người điều khiển**: Gán lớp `Driver` (hoặc `Person`), box bao trọn phần cơ thể nhìn thấy của người lái kèm mũ bảo hiểm, balo.
    - **Vẽ 1 bounding box riêng cho phương tiện giao thông**: Bao trọn thân xe từ điểm cao nhất của xe đến bánh xe tiếp đất.
    - Hai bounding box này được phép giao nhau (overlap) ở vùng tiếp xúc giữa người và phương tiện.
- **Mã quy tắc `R-05` [Loại trừ phản chiếu, vũng nước, đổ bóng]**:
  - **Tuyệt đối KHÔNG vẽ bounding box** cho các hình ảnh phản chiếu qua gương chiếu hậu xe hơi/xe máy, hình phản chiếu qua mặt kính tủ trưng bày, hình phản chiếu trên vũng nước đọng mặt đường, và bóng đổ của vật thể trên mặt đường.
- **Mã quy tắc `R-06` [Ngưỡng kích thước tối thiểu]**:
  - Các đối tượng có kích thước nhỏ hơn **20x20 pixel** thì **không vẽ bounding box** (để tránh nhiễu và sai số định vị cho mô hình phát hiện vật).
- **Mã quy tắc `R-07` [Tượng và ma-nơ-canh]**:
  - Bức tượng điêu khắc (đá, đồng, kim loại), ma-nơ-canh trong tủ kính, nhân vật mô hình nếu nhìn rõ và có kích thước ≥ 20x20 pixel thì gán nhãn `Statue`.
  - Không gán `Statue` thành `Person` hay `Driver`. Tranh vẽ phẳng, áp phích, biển quảng cáo hai chiều (`billboard`) không vẽ bounding box.

---

## 4. Ca khó và ví dụ trên 40 ảnh thực tế

Dưới đây là bảng tổng hợp các tình huống biên cụ thể được phát hiện từ bộ dữ liệu 40 ảnh (`img_001.jpg` đến `img_040.jpg`), kèm mã quy tắc và quyết định gán nhãn:

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_001.jpg` | Người phụ nữ đứng cạnh đuôi xe bán tải chở hàng hở thùng. | `R-01`, `R-02`, `R-03` | Vẽ box `Person` ôm từ đỉnh đầu đến gót chân bao gồm cả túi xách mang theo; vẽ box `Truck` cho xe bán tải từ mui đến bánh chạm đất. | Tách biệt người đi bộ và phương tiện chở hàng 4 bánh có thùng hàng phía sau. |
| `img_002.jpg` | Xe tải chuyên dụng cỡ lớn chở 8 ô tô con trên hai tầng giá đỡ. | `R-03` | Vẽ 1 box lớn `Truck` bao trọn xe tải chở hàng; vẽ các box `Car` riêng cho từng ô tô con nhìn thấy trên giá đỡ (nếu ≥ 20x20 px). | Xe tải chở hàng là phương tiện chuyên dụng; các ô tô con trên sàn vẫn là đối tượng hình thái xe con hoàn chỉnh cần phát hiện. |
| `img_004.jpg` | Hai xe tuk-tuk đỗ cạnh nhau trên vỉa hè ban đêm. | `R-03` | Gán lớp `3_wheelers_vehicle` cho mỗi xe tuk-tuk; vẽ box ôm sát mui xe đến bánh tiếp đất. | Tuk-tuk là phương tiện giao thông 3 bánh đặc thù, không xếp vào `Motorcycle` hay `Car`. |
| `img_005.jpg` | Nhiều người lái xe máy lưu thông trên đường phố đông đúc. | `R-02`, `R-03`, `R-04` | Vẽ box riêng cho `Driver` (gồm mũ bảo hiểm) và vẽ box riêng cho `Motorcycle` (gồm thân xe, bô xe và bánh tiếp đất). Hai box chồng lấn lên nhau. | Quy tắc ca khó tách biệt người điều khiển phương tiện và chính phương tiện đó. |
| `img_006.jpg` | Người đạp xích lô chở khách qua chỗ ùn tắc. | `R-03`, `R-04` | Vẽ box `3_wheelers_vehicle` cho xe xích lô (xe 3 bánh); vẽ box `Driver` riêng cho người đạp; vẽ box `Person` cho khách ngồi trên xe. | Xích lô là xe 3 bánh; người đạp là `Driver`, khách là `Person`. |
| `img_011.jpg` | Bức tượng nhân vật quái thú Predator đứng cạnh hàng xe mô tô phân khối lớn. | `R-07` | Gán nhãn `Statue` cho bức tượng Predator; KHÔNG gán nhãn `Person`. Vẽ box `Motorcycle` cho các xe mô tô. | Đây là tượng mô hình/nhân vật hóa trang cố định, không phải người thật đang tham gia giao thông. |
| `img_012.jpg` | Xe bán tải chở hàng đầy thùng xe với thùng carton và bao tải. | `R-03` | Gán `Truck`, box bao trọn ca-bin, hàng hóa chất cao trên thùng xe và bánh xe chạm đất. | Hàng hóa gắn liền trên thùng xe tải là một phần khổ hàng của phương tiện giao thông. |
| `img_017.jpg` | Tượng đài Công tước Wellington cưỡi ngựa trên quảng trường. | `R-07` | Gán nhãn `Statue` cho cả bức tượng người và ngựa; tuyệt đối không gán `Person` hay `Driver`. | Tác phẩm điêu khắc nghệ thuật cố định, mô hình xe tự hành cần phân biệt để không phanh nhầm. |
| `img_018.jpg` | Biển quảng cáo chính trị tấm lớn (billboard) in hình chân dung một người đàn ông. | `R-05`, `R-07` | KHÔNG vẽ bounding box cho hình chân dung trên biển quảng cáo. | Hình ảnh in phẳng 2D trên biển hiệu/billboard không phải đối tượng thật di chuyển trên mặt đường. |
| `img_020.jpg` | Cảnh đường phố và cầu vồng phản chiếu qua gương chiếu hậu ô tô. | `R-05` | KHÔNG vẽ bounding box cho bất kỳ xe hoặc người nào xuất hiện trong mặt kính gương chiếu hậu. | Theo quy tắc `R-05`, hình ảnh phản chiếu qua gương bị loại trừ để tránh làm sai lệch tọa độ thực tế. |
| `img_022.jpg` | Xe mô tô cổ có gắn thùng phụ (sidecar) chở người bên cạnh. | `R-03`, `R-04` | Gán `3_wheelers_vehicle` cho toàn bộ cụm xe máy + sidecar (tổng 3 bánh); vẽ box `Driver` cho người lái và box `Person` cho người ngồi trong sidecar. | Xe gắn sidecar trở thành phương tiện 3 bánh; người lái và người ngồi cạnh được tách box riêng. |
| `img_027.jpg` | Bia tưởng niệm hình xe bán tải bằng đá hoa cương trong nghĩa trang. | `R-07` | Gán `Statue` (hoặc bỏ qua); KHÔNG gán nhãn `Truck`. | Tượng điêu khắc bằng đá mô phỏng xe tải, không có động cơ, không phải phương tiện giao thông thật. |
| `img_028.jpg` | Xe bán tải chở mô hình ngựa trang trí (yorse) đỗ ven đường. | `R-01`, `R-03`, `R-07` | Gán `Truck` cho xe bán tải; mô hình trang trí xem như hàng hóa trên xe hoặc Statue, không gán động vật. | Là mô hình ngựa trang trí trên thùng xe, phương tiện chính là xe tải chở hàng. |
| `img_033.jpg` | Ma-nơ-canh mặc trang phục đứng trong tủ kính cửa hàng thời trang. | `R-07` | Gán nhãn `Statue`; không gán nhãn `Person`. | Ma-nơ-canh là tượng hình người nhân tạo, không có khả năng chuyển động như người thật. |
| `img_035.jpg` | Xe ba bánh Auto Rickshaw chở người và hàng hóa quá tải chật ních. | `R-03`, `R-04` | Gán `3_wheelers_vehicle` cho xe ba bánh; vẽ box `Driver` riêng cho tài xế; hành khách ngồi sau nếu lộ rõ vẽ box `Person` và đánh dấu `occluded_level = 2` hoặc `3`. | Xe ba bánh giao thông chở người; phân tách người điều khiển và đánh dấu mức độ che khuất cao. |
| `img_037.jpg` | Xe bán tải lắp nắp thùng cao kín mít phía sau (`Master 75 Truck Cap`). | `R-03` | Gán lớp `van` (hoặc `Truck` và tick `can_review = true` để đưa ra họp nhóm Pha 2). | Dễ nhầm lẫn giữa bán tải cải tạo thùng kín và xe van chở đồ; cần gắn cờ xem xét đồng thuận nhóm. |
| `img_038.jpg` | Tủ kính đồ chơi trưng bày nhiều mô hình xe hơi nhỏ và búp bê. | `R-05`, `R-06`, `R-07` | KHÔNG vẽ bounding box cho các mô hình xe hơi và búp bê có kích thước < 20x20 pixel hoặc bị phản chiếu qua tủ kính. | Vi phạm ngưỡng kích thước tối thiểu và là vật thể đồ chơi/phản chiếu trong tủ kính. |

---

## 5. QC và phiên bản

### Ngưỡng kiểm soát chất lượng (QC Thresholds)

- **Ngưỡng kích thước tối thiểu**: Loại bỏ và không vẽ box cho các vật thể có chiều cao hoặc chiều rộng nhỏ hơn 20 pixel (`min_box_height_px = 20`).
- **Ngưỡng IoU kiểm tra box ôm sát**:
  - Đối với vật thể lớn (cạnh lớn ≥ 50 pixel): Yêu cầu IoU giữa các annotator ≥ 0.85 (`iou_thr_large = 0.85`).
  - Đối với vật thể nhỏ (cạnh lớn < 50 pixel): Yêu cầu IoU ≥ 0.70 (`iou_thr_small = 0.70`).
- **Quy trình xử lý ca mơ hồ**:
  - Khi người gán phân vân không thể chắc chắn về nhãn lớp hoặc ranh giới, tick chọn thuộc tính `can_review = true`.
  - Không tự ý phán đoán chủ quan; tổng hợp các ca `can_review` vào danh sách nghi vấn để họp hiệu chuẩn (calibration) cả nhóm ở Pha 2 và Pha 5. Người duyệt cuối cùng là Trưởng nhóm hoặc thống nhất biểu quyết nhóm.

### Lịch sử thay đổi (Changelog)

| Phiên bản | Ngày | Người thực hiện | Thay đổi chính | Lý do / Căn cứ |
|---|---|---|---|---|
| `v0.1` | 2026-11-16 | Thành viên 102 | Khởi tạo guideline cá nhân từ v0; bổ sung định nghĩa chi tiết cho 9 lớp (`Person`, `Driver`, `Car`, `Truck`, `van`, `Motorcycle`, `Bicycle`, `3_wheelers_vehicle`, `Statue`) và lớp phụ `other_vehicle`; định lượng rõ 4 mức `occluded_level`; chuẩn hóa 7 quy tắc vẽ box (`R-01` đến `R-07`) bao gồm tách người lái và xe, loại trừ bóng đổ/phản chiếu và ngưỡng 20x20 px. | Khảo sát thực tế 40 ảnh (`img_001.jpg` đến `img_040.jpg`), khắc phục sự mơ hồ định tính của bản khởi đầu v0 nhằm chuẩn bị cho buổi họp thống nhất v1.0. |
