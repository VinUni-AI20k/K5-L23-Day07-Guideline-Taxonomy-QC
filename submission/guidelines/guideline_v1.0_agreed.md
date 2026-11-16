# Guideline gán nhãn — v1.0 — Nhóm Lab 402

> Tài liệu đặc tả gán nhãn chính thức của Nhóm Lab 402 cho bài toán phát hiện đối tượng 2D trên ảnh giao thông đường phố (Day 07). Bản này được xây dựng trên cơ sở đối chiếu, tổng hợp và giải quyết triệt để các bất đồng giữa 5 bản guideline cá nhân (`03039`, `03223`, `03224`, `03228`, `03238`) sau khi khảo sát độc lập toàn bộ 40 ảnh thực tế (`img_001.jpg` đến `img_040.jpg`). Cập nhật v1.0: Đơn giản hóa thuộc tính che khuất (`occluded_level`) thành nhị phân, không chia level.

- **Phiên bản:** v1.0 
- **Ngày thống nhất:** 16/11/2026
- **Nhóm thực hiện:** Nhóm Lab 402
  - **Người điều phối:** 328 (Nguyễn Quốc Khánh)
  - **Người review bản cuối:** 228 (Đoàn Quang Minh)
  - **Thành viên tham gia:** 03039 (Đặng Anh Tuyền), 03223 (Nguyễn Chí Tài), 03224 (Nguyễn Quốc Việt), 228 (Đoàn Quang Minh), 328 (Nguyễn Quốc Khánh)

---

## 1. Mục tiêu

- **Mô hình sử dụng nhãn:**
  - Bộ nhãn phục vụ huấn luyện và đánh giá các mô hình học sâu thị giác máy tính phát hiện vật thể 2D (2D Object Detection như YOLOv8/v10, Faster R-CNN, RT-DETR) chạy thời gian thực trên ảnh đường phố đô thị.
  - Ứng dụng trọng tâm trong hệ thống hỗ trợ lái xe nâng cao (ADAS), xe tự hành (Autonomous Vehicles) và hệ thống camera giám sát giao thông thông minh (ITS / ITMS) trong điều kiện giao thông hỗn hợp (mixed traffic).

- **Mục đích gán nhãn:**
  - Định vị tọa độ 2D (bounding box chữ nhật song song trục) và phân loại chính xác các tác nhân tham gia giao thông cốt lõi (người, ô tô con, xe tải, xe van, xe buýt, xe tuk-tuk, xe máy).
  - Cung cấp dữ liệu chuẩn mực để các module nhận thức phía sau thực hiện ước lượng khoảng cách (Monocular 3D / Depth estimation), theo dõi đối tượng (Multi-Object Tracking - MOT) và dự đoán quỹ đạo tránh va chạm (Collision Avoidance).
  - Phân tách rõ ràng giữa các phương tiện/con người thật đang tham gia giao thông với các yếu tố gây nhiễu thị giác (tượng đài, ma-nơ-canh, đồ chơi, hình in quảng cáo 2D phẳng, bóng đổ, ảnh phản chiếu qua kính/gương).

- **Phân tích rủi ro & các sai sót nguy hiểm (Failure Analysis):**
  - **Bỏ sót vật thể (False Negative - FN) — Cực kỳ nguy hiểm:**
    - Bỏ sót người đi bộ (`person`), người đi xe máy (`motorcycle`) hoặc ô tô ở cự ly gần: Hệ thống điều khiển tự động sẽ không kích hoạt phanh tự động khẩn cấp (AEB), dẫn đến va chạm trực tiếp gây chết người hoặc thương vong nặng nề.
    - Bỏ sót phương tiện lớn (`truck`, `bus`) ở các góc giao cắt: Dẫn đến tai nạn liên hoàn nghiêm trọng.
  - **Nhận diện nhầm vật thể (False Positive - FP) — Nguy hiểm cao:**
    - Nhận diện nhầm ma-nơ-canh trong tủ kính, tượng đá/đồng, hình in chân dung trên biển quảng cáo, tranh vẽ tường hoặc ảnh phản chiếu thành người/xe thật: Dẫn đến hiện tượng "phanh ma" (phantom braking) — phương tiện tự hành phanh gấp bất ngờ giữa đường ở tốc độ cao, gây nguy cơ bị các phương tiện phía sau đâm dồn toa.
  - **Sai lệch Bounding Box (Bounding Box Drift / Low IoU) — Nguy hiểm:**
    - Box vẽ lẹm cắt cụt bánh xe/đầu người hoặc vẽ quá rộng bao gồm nhiều nền: Làm sai lệch thuật toán ước lượng khoảng cách 3D từ camera đơn (monocular depth), dẫn đến tính sai thời gian tới điểm va chạm (Time-to-Collision - TTC) và kích hoạt phản xạ đánh lái/phanh sai thời điểm.
  - **Nhận diện sai lớp (Misclassification) — Rủi ro cao:**
    - Nhầm xe tải nặng (`truck`) hoặc xe buýt (`bus`) thành ô tô con (`car`): Khiến hệ thống ước tính sai kích thước khối bao, điểm mù và gia tốc phanh, gây nguy hiểm khi vượt xe hoặc chuyển làn.

---

## 2. Lớp và thuộc tính

### 2.1. Giải quyết bất đồng giữa các bản cá nhân từ Pha 1

Sau khi đối chiếu 5 bản guideline cá nhân, nhóm đã phân tích và thống nhất các quyết định trọng tâm sau:

1. **Bổ sung lớp `tuk_tuk` (Xe ba bánh có động cơ):**
   - *Bất đồng:* Bản 03039, 03223, 228 ban đầu để ngoài taxonomy vì v0 không có lớp; bản 03224 đề xuất `three_wheeler`; bản 328 đề xuất `tuk_tuk`.
   - *Quyết định v1.0:* Bổ sung chính thức lớp `tuk_tuk`.
   - *Lý do:* Xe ba bánh chở khách xuất hiện thường xuyên trong ảnh (`img_004`, `img_016`, `img_035`). Đây là phương tiện cơ giới di chuyển nhanh trong luồng giao thông. Nếu bỏ qua hoặc ép vào `motorcycle`/`car` sẽ làm sai bản chất hình học và hành vi của phương tiện.
2. **Bổ sung lớp `bus` (Xe buýt, xe khách cỡ lớn):**
   - *Bất đồng:* Bản 03039, 03223, 228 ban đầu coi là ngoài taxonomy hoặc phân vân ép vào `van`; bản 03224, 328 đề xuất lớp `bus`.
   - *Quyết định v1.0:* Bổ sung chính thức lớp `bus`.
   - *Lý do:* Xe buýt lớn (`img_009`, `img_031`, `img_037`, `img_040`) có kích thước to lớn vượt trội (chở trên 16-20 chỗ), kết cấu đặc thù, hoàn toàn khác biệt với xe thùng nhỏ `van` và xe chở hàng `truck`.
3. **Quy tắc xe chuyên chở ô tô con (`img_002`):**
   - *Bất đồng:* Bản 228 đề xuất chỉ gán 1 box `truck` cho toàn bộ xe chở và không gán các xe con bên trên (coi là hàng); các bản 03039, 03223, 03224, 328 đề xuất gán cả xe tải và từng ô tô con trên sàn.
   - *Quyết định v1.0:* Thống nhất vẽ 01 box `truck` bao toàn bộ xe chuyên chở VÀ vẽ từng box `car` riêng cho mỗi ô tô con nhìn thấy trên giá chở (thỏa mãn chiều cao $\ge 20\text{ px}$).
   - *Lý do:* Dưới góc nhìn camera 2D, các ô tô trên sàn vẫn mang đầy đủ đặc trưng thị giác của `car`. Việc gán box giúp mô hình học phát hiện đối tượng bị che khuất một phần trong không gian 3D thay vì bỏ sót.
4. **Phân loại xe bán tải (Pickup) có nắp thùng cao (`img_037`):**
   - *Bất đồng:* Phân vân giữa `truck` và `van`.
   - *Quyết định v1.0:* Thống nhất gán `truck`.
   - *Lý do:* Cấu trúc nguyên bản là khung gầm xe bán tải (cabin rời và thùng hàng tách biệt). Nắp thùng kín lắp thêm (hardtop canopy) chỉ là phụ kiện che chắn, không biến xe thành xe thân hộp liền khối kiểu `van`.
5. **Xử lý xe đạp, xích lô (`img_003`, `img_006`, `img_023`, `img_029`):**
   - *Bất đồng:* Bản 03224, 328 đề xuất thêm lớp `bicycle`; các bản 03039, 03223, 228 đề xuất loại vì là bài toán phương tiện cơ giới.
   - *Quyết định v1.0:* Không bổ sung lớp `bicycle`. Phương tiện thô sơ không có động cơ (xe đạp, xích lô đạp chân) nằm ngoài taxonomy (không vẽ box phương tiện). TUY NHIÊN, người điều khiển/ngồi trên xe đạp, xích lô vẫn BẮT BUỘC gán box `person`.
6. **Xử lý tượng, mô hình đồ chơi, tranh ảnh 2D (`img_011`, `img_017`, `img_018`, `img_024`, `img_027`, `img_033`, `img_038`):**
   - *Bất đồng:* Bản 328 từng đề xuất các lớp `person_model`, `car_model`; các bản khác đề xuất loại bỏ.
   - *Quyết định v1.0:* Thống nhất KHÔNG tạo các lớp `_model` trong taxonomy. Tất cả các tượng, ma-nơ-canh, xe mô hình đồ chơi, tranh vẽ/biển quảng cáo 2D phẳng, ảnh phản chiếu qua kính/gương đều là vật thể phi thực tế $\rightarrow$ **TUYỆT ĐỐI KHÔNG GÁN NHÃN** `person` hay `car` (đóng vai trò hard negatives).
7. **Đơn giản hóa thuộc tính che khuất (Không chia level `occluded`):**
   - *Bất đồng ban đầu:* Bản v0 và các bản cá nhân chia 4 mức `occluded_level` ($0, 1, 2, 3$) với các ngưỡng $30\%, 70\%$, dẫn đến sự bất đồng chủ quan liên tục giữa các người gán (người ước lượng che $25\%$ chọn mức 1, người ước lượng $35\%$ chọn mức 2), làm giảm điểm đồng thuận IAA giả tạo.
   - *Quyết định v1.0:* Thống nhất **KHÔNG CHIA LEVEL** cho thuộc tính che khuất. Chuyển `occluded_level` sang dạng nhị phân kiểu `checkbox` (`false`: không che, `true`: bị che).
   - *Lý do:* Giúp thao tác trên CVAT nhanh chóng (chỉ cần 1 click checkbox), triệt tiêu tranh chấp ranh giới giữa các mức $30\%$ hay $70\%$, tập trung độ chuẩn xác vào vị trí bounding box và phân lớp.

---

### 2.2. Danh mục 8 lớp đối tượng (Taxonomy v1.0)

Mỗi đối tượng hợp lệ trong ảnh phải thuộc đúng một lớp trong bảng sau:

| Lớp | Định nghĩa chuẩn (một câu) | Ví dụ thực tế trong bộ ảnh | Phản ví dụ / Dễ nhầm với |
|---|---|---|---|
| `car` | Phương tiện giao thông cơ giới 4 bánh có thân liền mạch, chủ yếu dùng chở người và hành lý gia đình (sedan, hatchback, SUV, crossover, MPV, xe wagon, taxi). | Xe đen `img_023`, xe wagon `img_024`, các ô tô con trên sàn xe chở xe `img_002`, xe taxi `img_040`. | Xe bán tải (pickup) thuộc `truck`; xe thân hộp liền chở khách 16 chỗ thuộc `van`; mô hình xe đồ chơi (`img_038`) bị loại. |
| `truck` | Phương tiện cơ giới đường bộ có cabin điều khiển và khu vực/thùng chở hàng tách biệt về kết cấu (xe tải, xe đầu kéo, xe chở ô tô, xe bán tải/pickup kể cả loại có nắp thùng cao). | Xe chở ô tô `img_002`, xe tải nhỏ mui bạt `img_007`, `img_036`, xe bán tải `img_012`, `img_028`, `img_037`. | Xe van thùng kín liền khối thuộc `van`; tượng xe mộ đá (`img_027`) bị loại; thùng hàng rời không gán riêng. |
| `van` | Phương tiện cơ giới dạng thân hộp kín một khối (monovolume), khoang lái và khoang hàng/hành khách thông liền nhau (minivan, xe van chở hàng, xe chở khách cỡ nhỏ 9–16 chỗ). | Xe van xám phía sau dòng người `img_005`, xe van trắng Hiace `img_016`. | Xe buýt lớn chở khách trên 20 chỗ (`img_009`) thuộc `bus`; xe tải thùng kín rời cabin (`img_036`) thuộc `truck`. |
| `bus` | Phương tiện giao thông cơ giới cỡ lớn chuyên dụng vận chuyển số lượng lớn hành khách (xe buýt nội đô, xe khách liên tỉnh, minibus trên 16–20 chỗ). | Xe buýt chạy giữa phố `img_009`, `img_031`, xe buýt lớn phía sau `img_037`, xe buýt cắt mép `img_040`. | Xe van 9–16 chỗ thân nhỏ thuộc `van`; xe tải thùng dài thuộc `truck`. |
| `tuk_tuk` | Phương tiện giao thông cơ giới 3 bánh chuyên chở khách hoặc hàng nhẹ đặc trưng đô thị (tuk-tuk, xe lam, auto-rickshaw có động cơ). | Xe tuk-tuk chở khách `img_004`, `img_016`, xe tuk-tuk chất hàng cao trên nóc `img_035`. | Xe máy gắn sidecar (`img_022`) thuộc `motorcycle`; xích lô đạp chân (`img_023`) ngoài taxonomy. |
| `motorcycle` | Phương tiện cơ giới hai bánh có động cơ (xe máy, xe tay ga, mô tô phân khối lớn), bao gồm cả mô tô có gắn thùng bên hông (sidecar). | Xe máy di chuyển `img_005`, `img_008`, `img_010`, `img_026`, mô tô gắn sidecar `img_022`. | Xe đạp không động cơ (ngoài taxonomy); xe ba bánh tuk-tuk thuộc `tuk_tuk`. |
| `person` | Con người thật ở mọi tư thế (đi bộ, đứng, ngồi, lái xe, hành khách) nhìn thấy trực tiếp trong ảnh và đạt kích thước tối thiểu. | Người bán hàng `img_003`, `img_010`, người lái xe máy `img_005`, `img_026`, người đi bộ `img_034`, `img_040`. | Ma-nơ-canh `img_033`, tượng người `img_017`, mặt người in trên biển quảng cáo `img_018`, hình người in trên thân xe taxi `img_040`. |
| `ignore_region` | Vùng đánh dấu khu vực chứa cụm đối tượng quá nhỏ ($h < 20\text{ px}$) hoặc đám đông xếp chồng chéo quá dày đặc không thể phân ranh giới chính xác từng vật thể. | Cụm xe máy đỗ ken đặc hậu cảnh `img_030`, `img_036`, đám đông người/xe ở xa tít `img_021`, `img_032`. | Không dùng để thay thế cho vật đơn lẻ to rõ; không dùng cho vùng trống không có đối tượng. |

---

### 2.3. Quy tắc đối với vật thể không thuộc lớp nào

- **Phương tiện thô sơ và vật dụng đường phố (Xe đạp, xích lô, xe cút kít, xe đẩy hàng):** Không vẽ bounding box cho phương tiện. Tuy nhiên, người lái hoặc người đẩy xe vẫn được vẽ box `person` ôm sát phần cơ thể nhìn thấy.
- **Hàng hóa, phụ kiện rời nhô ra (Thanh kim loại dài, giỏ hàng, gánh hàng rong):** Không gán box riêng. Nếu hàng hóa nhô ra quá lớn ($> 20\%$ kích thước xe) thì không kéo dài box phương tiện theo hàng (xem quy tắc `R-11`).
- **Động vật (chim bồ câu, chó, mèo, ngựa thật):** Bỏ qua hoàn toàn, không vẽ box.
- **Bối cảnh hạ tầng tự nhiên và đô thị (Mặt đường, vỉa hè, bầu trời, tòa nhà, cây cối, cột đèn):** Không gán box (coi là background).
- **Vật thể lạ, hiếm gặp ngoài danh mục (Xe cứu thương chuyên dụng, xe công trình):** Người gán không tự ý chế lớp mới; gán lớp gần nhất có thể hoặc tick `can_review = true` và ghi vào `image_issues.csv` để đưa ra họp tại Pha 4.

---

### 2.4. Thuộc tính chuẩn hóa (Attributes)

Mọi bounding box thuộc 7 lớp đối tượng (ngoại trừ `ignore_region`) đều phải được gán đủ 3 thuộc tính đo lường định lượng được dưới đây:

| Tên thuộc tính | Kiểu / Giá trị | Mặc định | Ý nghĩa | Ngưỡng đo lường định lượng cụ thể | Quy tắc liên kết |
|---|---|---|---|---|---|
| `occluded_level` | `checkbox`<br>(`true`, `false`) | `false` | Đánh giá vật thể có bị che khuất bởi vật cản khác (cột, cây cối, xe khác, người khác) hay không. *(Không chia level 0, 1, 2, 3).* | • `false` (Không tick / mặc định): Nhìn thấy trọn vẹn hoặc phần bị che khuất không đáng kể ($< 5\%$ diện tích).<br>• `true` (Tick chọn checkbox): Vật thể bị che khuất một phần bởi vật thể khác.<br>*(Lưu ý: Nếu bị che quá nặng $> 90\%$ không còn nhận dạng chắc chắn thì bỏ qua không gán).* | `R-02` |
| `truncated` | `select`<br>(`no`, `yes`) | `no` | Đánh giá vật thể có bị đường viền khung ảnh cắt cụt hay không. | • `no`: Vật thể nằm trọn vẹn trong khung ảnh hoặc mép ngoài chỉ chạm sát viền làm mất $< 10\%$ diện tích.<br>• `yes`: Một cạnh của box tiếp xúc đúng mép ảnh và phần thân vật thể bị cắt mất từ $10\%$ diện tích trở lên.<br>*(Lưu ý: Nếu phần lọt vào ảnh quá nhỏ $< 20\text{ px}$ chiều cao/rộng thì bỏ qua không gán).* | `R-03` |
| `can_review` | `checkbox`<br>(`true`, `false`) | `false` | Đánh dấu các ca biên, ca khó hoặc trường hợp còn phân vân để kiểm tra chéo. | • `false`: Tự tin gán theo đúng quy tắc guideline.<br>• `true`: Bật khi phân vân giữa 2 lớp (vd: bán tải nắp kín giữa `truck`/`van`), vật bị che khuất nghiêm trọng khó xác định, hoặc vật thể mờ nhòe. | `R-12` |

> *Lưu ý về thuộc tính của `ignore_region`:* Sử dụng giá trị kỹ thuật mặc định (`occluded_level=false`, `truncated=no`, `can_review=false`) để phục vụ xuất COCO hợp lệ.

---

## 3. Quy tắc vẽ box

Mọi thành viên bắt buộc tuân thủ 12 quy tắc chuẩn hóa dưới đây (mã hóa từ `R-01` đến `R-12` để dẫn chiếu trong QC và Calibration):

### R-01: Bounding Box ôm sát phần nhìn thấy (Tight Box — Visible Pixels Only)
- Bounding box là hình chữ nhật đứng (axis-aligned rectangle) tiếp xúc sát 4 điểm cực trị (trên, dưới, trái, phải) của **phần điểm ảnh thực tế nhìn thấy được** của vật thể.
- **Tuyệt đối KHÔNG ước lượng hay vẽ bù** phần thân thể hoặc bộ phận xe bị khuất sau vật khác hoặc nằm ngoài khung hình.
- Độ dung sai viền nền (background margin) cho phép tối đa 3–5 pixel. Không được cắt lẹm chi tiết nhìn thấy của vật và không vẽ thừa khoảng trống nền.

### R-02: Xử lý che khuất và vật thể bị chia cắt (Occlusion Handling — Không chia level)
- Box chỉ bao bọc các phần thực tế nhìn thấy của vật thể; phần bị che bởi vật cản phía trước nằm trong bounding box nhưng thuộc tính `occluded_level` được đánh dấu tick chọn (`true`).
- **Nguyên tắc không chia level:**
  - `occluded_level = false` (mặc định / không tick): Áp dụng khi vật thể nhìn thấy trọn vẹn, không có vật khác chắn trước mặt (hoặc che lấp không đáng kể $< 5\%$).
  - `occluded_level = true` (tick chọn checkbox): Áp dụng cho mọi trường hợp vật thể bị một vật khác che khuất một phần thân thể hoặc phương tiện. Nhóm **không phân chia thành các mức 1, 2, 3** để loại bỏ hoàn toàn sự tranh cãi về tỷ lệ $30\%$ hay $70\%$.
- **Trường hợp vật thể bị che cắt rời thành 2 mảnh nhìn thấy:**
  - Nếu hai mảnh nhìn thấy rõ ràng thuộc về cùng một đối tượng duy nhất (ví dụ: thân xe ô tô bị cột đèn chắn ngang chính giữa): Vẽ **01 box duy nhất** bao trọn cả hai mảnh phần nhìn thấy, tick chọn `occluded_level = true`.
  - Nếu phần bị che quá lớn ($> 80\%$) và hai mảnh nằm quá xa nhau khiến không thể khẳng định chắc chắn chúng thuộc cùng một vật: Không gán box gộp to mà chỉ gán phần nhận diện được chắc chắn hoặc bật `can_review = true`.
- Nếu vật thể bị che khuất trên $90\%$ diện tích và không còn đủ đặc trưng nhận diện chắc chắn: **Bỏ qua không gán**.

### R-03: Xử lý vật thể bị cắt ở mép ảnh (Truncation & Boundary Coordinates)
- Bounding box phải nằm hoàn toàn trong tọa độ ảnh: $0 \le x_{\min} < x_{\max} \le W$, $0 \le y_{\min} < y_{\max} \le H$. Box dừng đúng tại đường biên ảnh, không mở rộng ra ngoài canvas.
- Gán `truncated = yes` khi một mép box trùng đường biên ảnh và vật thể bị cắt mất từ $10\%$ diện tích trở lên.
- Nếu phần lọt vào ảnh có chiều cao/rộng $< 20\text{ px}$ hoặc không đủ đặc trưng để xác định lớp: Bỏ qua không gán.

### R-04: Loại bỏ vật không thật, hình in, tranh vẽ, mô hình và phản chiếu (Real vs. Non-Real)
- **Tượng người, ma-nơ-canh (`img_011`, `img_017`, `img_033`):** Không gán nhãn `person`.
- **Mô hình đồ chơi, tượng xe, mộ đá (`img_024`, `img_027`, `img_038`):** Không gán nhãn phương tiện (`car`/`truck`).
- **Hình ảnh 2D (Biển quảng cáo `img_018`, tranh tường `img_026`, ảnh in trên thân xe taxi `img_040`):** Không vẽ box cho các hình in phẳng 2D.
- **Ảnh phản chiếu và bóng đổ (`img_015`, `img_020`):** Tuyệt đối không vẽ box cho hình ảnh ảo phản chiếu qua gương chiếu hậu, cửa kính xe, mặt đường ướt; không đưa bóng đổ trên mặt đất vào bounding box.
- **Nhìn xuyên qua kính:** Người hoặc xe nhìn thấy rõ qua cửa kính trong suốt vẫn được gán nhãn bình thường.

### R-05: Loại bỏ xe chủ mang camera (Ego Vehicle)
- Bộ phận thuộc chính chiếc xe chở camera chụp ảnh xuất hiện ở rìa mép ảnh (gương chiếu hậu, nắp ca-pô, mép kính lái như ở `img_020`): **Không vẽ box phương tiện**, không gán nhãn.

### R-06: Ngưỡng kích thước tối thiểu và độ mờ nhòe (Min Box Size Threshold)
- **Ngưỡng kích thước:** Bỏ qua tất cả các vật thể có chiều cao hoặc chiều rộng **nhỏ hơn 20 pixels** ($h < 20\text{ px}$).
- **Mờ nhòe do chuyển động (Motion blur) hoặc thiếu sáng ban đêm (`img_013`, `img_014`):** Nếu vẫn phân biệt được lớp và ranh giới vật thể $\ge 20\text{ px}$ thì vẫn vẽ box và tick `can_review = true`. Nếu chỉ còn là vệt sáng nhòe không xác định được hình dạng thì bỏ qua hoàn toàn.

### R-07: Đám đông dày đặc và vùng bỏ qua (`ignore_region`)
- Khi một nhóm người hoặc cụm phương tiện xếp chồng chéo quá dày đặc ở hậu cảnh (như hàng xe máy đỗ ken đặc ở `img_030`, `img_036` hoặc đám đông xa ở `img_021`, `img_032`) mà việc tách từng box đơn lẻ là bất khả thi hoặc chiều cao vật $< 20\text{ px}$: Vẽ **01 box `ignore_region`** bao trùm toàn bộ khu vực đó.
- Các vật thể ở tiền cảnh đủ lớn ($\ge 20\text{ px}$) và tách biệt rõ ràng vẫn phải được vẽ box riêng bình thường.

### R-08: Tách rời người điều khiển và phương tiện (Person & Vehicle Separation)
- Áp dụng nguyên tắc **tách rời từng cá thể thành từng box độc lập:**
  - **Box `person`:** Bao gồm toàn bộ cơ thể người lái hoặc hành khách nhìn thấy (đầu, mũ bảo hiểm, thân, tay chân). Mỗi người trên xe được gán **01 box `person` riêng**. Không kéo dài box theo túi xách, gánh hàng rời.
  - **Box phương tiện (`motorcycle`, `tuk_tuk`, `car`):** Bao trùm toàn bộ thân xe, bánh xe, tay lái, gương xe.
  - Hai box này được phép chồng lấn hình học (overlap) lên nhau tại vùng ngồi. Thuộc tính `occluded_level` được đánh giá theo độ che khuất thực tế giữa người và xe.
  - *Ví dụ:* 01 xe máy chở 2 người (`img_026`) sẽ có tổng cộng **3 box riêng biệt**: 1 `motorcycle` và 2 `person`.

### R-09: Xe chuyên chở ô tô và hàng hóa trên xe (Car Carrier & Cargo)
- **Phương tiện vận chuyển (`truck` trên `img_002`):** Vẽ 01 box `truck` bao toàn bộ đầu kéo, khung gầm và kết cấu sàn giá chở.
- **Các ô tô con trên sàn xe chở xe (`img_002`):** Vẽ **từng box `car` riêng biệt** cho mỗi ô tô con nhìn thấy rõ trên giá sàn (thỏa mãn $h \ge 20\text{ px}$), gán `occluded_level` từ 1 đến 2 do bị khung giàn sắt che một phần.

### R-10: Xử lý phương tiện đặc thù (Sidecar & Xe bán tải)
- **Xe mô tô có thùng bên hông (Sidecar trên `img_022`):** Vẽ **01 box `motorcycle` duy nhất** bao trọn cả xe mô tô và phần thùng xe bên hông gắn cố định.
- **Xe bán tải (Pickup):** Bán tải thùng hở (`img_012`, `img_028`) hoặc bán tải lắp thêm nắp thùng cao composite (`img_037`) đều được xếp thống nhất vào lớp **`truck`**.

### R-11: Phụ kiện gắn liền vs. Hàng hóa nhô ra ngoài (Cargo Overhang)
- **Hàng hóa/phụ kiện gắn liền:** Thùng xe, mui bạt gắn cố định, gương chiếu hậu là bộ phận của xe, được tính vào box xe.
- **Hàng hóa nhô ra quá mức:** Nếu hàng hóa chở trên xe máy hoặc xe tải (như ống kim loại dài vắt ngang ở `img_029` hay hàng chất quá dài) nhô ra vượt quá $20\%$ chiều dài thân xe: **Không kéo dài box xe theo phần nhô ra đó**, box xe chỉ ôm theo ranh giới kết cấu thân xe. Box người cũng không kéo dài theo đòn gánh hay gậy dài (`img_003`).

### R-12: Cơ chế gắn cờ xem lại (`can_review`) và nhật ký vấn đề cấp ảnh
- Khi gặp trường hợp phân vân ranh giới lớp hoặc thuộc tính ở ca khó: Người gán vẫn vẽ box theo nhận định cá nhân tốt nhất, nhưng **bắt buộc tick chọn `can_review = true`**.
- Nếu gặp đối tượng nghi vấn nhưng **không thể vẽ được box** (do quá mờ hoặc tranh chấp phạm vi): Ghi lại vào tệp `submission/qc/image_issues.csv` (gồm 4 trường: `image,annotator,region,note`) để toàn nhóm cùng giải quyết trong buổi họp QC.

---

## 4. Bảng ca khó và quyết định của nhóm (Edge Cases trên 40 ảnh)

Dưới đây là bảng tổng hợp các tình huống biên điển hình được phát hiện từ 5 bản cá nhân trên 40 ảnh thực tế, kèm theo Rule ID và quyết định thống nhất của nhóm:

| Ảnh | Tình huống / Đối tượng thực tế | Rule ID | Quyết định thống nhất của nhóm | Lý do & Thảo luận |
|---|---|---|---|---|
| `img_001` | Người đứng sát và ngồi trên thùng xe bán tải | R-01, R-08, R-10 | Tách riêng xe bán tải là `truck`; mỗi người nhìn thấy rõ vẽ 01 box `person`. | Xe bán tải có cabin và thùng hàng riêng; người và xe phải tách riêng từng box. |
| `img_002` | Xe tải chuyên chở 6–7 ô tô con trên hai tầng giá | R-01, R-09 | 01 box `truck` cho xe chở xe; vẽ từng box `car` riêng cho mỗi ô tô con trên sàn (đạt $\ge 20\text{ px}$). | Đã giải quyết bất đồng giữa bản 228 và các bản khác; ô tô trên sàn vẫn mang đặc trưng thị giác của `car`. |
| `img_003` | Người phụ nữ gánh hàng rong, xe đạp và xe máy phía sau | R-03, R-08, R-11 | Gán `person` cho người gánh hàng (không bao gồm đòn gánh/thúng hàng); gán `motorcycle` và `person` đi kèm; không gán box xe đạp. | Xe đạp ngoài taxonomy; đòn gánh nhô ra là hàng rời không đưa vào box người. |
| `img_004` | Hai xe tuk-tuk chở khách, tài xế ngồi bên trong | R-01, R-08 | Gán mỗi xe là `tuk_tuk`; tài xế nhìn thấy rõ trong buồng lái gán thêm 01 box `person`. | Đã bổ sung lớp `tuk_tuk` trong v1.0 để định danh chính xác xe 3 bánh. |
| `img_005` | Nhóm 4–5 người đi xe máy chen chúc, xe van xám bị che phía sau | R-02, R-08 | Tách từng box `person` cho mỗi người; vẽ phần nhìn thấy của xe máy `motorcycle`; xe van phía sau gán `van` với `occluded_level=true` (bị che khuất). | Che khuất dày đặc; đánh dấu tick chọn `occluded_level=true` vì xe van bị che thân trước. |
| `img_006` | Dòng xe máy, taxi bên trái và người đi xe đạp | R-01, R-08 | Gán cặp `motorcycle` + `person`; taxi gán `car`; người đạp xe chỉ gán `person` (không gán xe đạp). | Xe đạp không động cơ nằm ngoài taxonomy. |
| `img_007` | Xe tải Isuzu nhỏ và xe bán tải trắng trong nhà để xe | R-01, R-10 | Cả 2 xe đều gán lớp `truck`. | Cả 2 đều có kết cấu cabin và thùng chở hàng tách biệt. |
| `img_008` | Cụm nhiều xe máy đỗ cạnh nhau | R-01, R-07 | Các xe máy phân biệt được ranh giới rõ ràng thì gán từng box `motorcycle`; nếu có cụm quá xa/chồng lấn thì dùng `ignore_region`. | Ưu tiên gán cá thể nếu tách được ranh giới. |
| `img_009` | Xe buýt lớn chở khách di chuyển giữa phố | R-01 | Gán lớp `bus` cho xe buýt; người đứng chờ ở vỉa hè gán `person`. | Đã bổ sung lớp `bus` trong v1.0; không ép vào `van`. |
| `img_010` | Hai người ngồi trên xe máy đỗ, người bán rau cạnh xe đẩy | R-08, R-11 | 01 box `motorcycle` + 02 box `person` trên xe; 01 box `person` cho người bán hàng; không gán xe đẩy/sọt rau. | Tách đúng từng cá thể; xe đẩy rau ngoài taxonomy. |
| `img_011` | Mô hình nhân vật Predator đứng cạnh xe mô tô độ | R-04, R-01 | **Không gán box** cho tượng Predator; xe mô tô thật bên cạnh gán `motorcycle`. | Predator là tượng mô hình trang trí nhân tạo, không phải người thật. |
| `img_012` | Xe bán tải bốc dỡ hàng, xe SUV xám phía trước | R-01, R-10 | Xe bán tải gán `truck` (`truncated=yes` nếu chạm biên); SUV gán `car`; người bốc hàng gán `person`. | Bán tải là `truck`; hàng trong thùng gắn liền với xe. |
| `img_013` | Cảnh đường phố ban đêm, ánh đèn lóa và mờ chuyển động | R-06, R-12 | Chỉ gán box cho các xe và người còn nhận dạng rõ hình khối và cao $\ge 20\text{ px}$; tick `can_review = true` nếu phân vân. | Không gán cho các vệt đèn nhòe vô định hình. |
| `img_014` | Người đi xe máy ban đêm bị mờ chuyển động (motion blur) | R-06, R-08 | Vẫn gán `motorcycle` và `person` nếu nhận diện được cấu trúc; tick `can_review = true`. | Mờ chuyển động không tự động loại bỏ nếu mắt người vẫn nhận biết được đối tượng. |
| `img_015` | Xe con đỏ cắt mép trái, xe bạc cắt mép phải, vũng nước phản chiếu | R-03, R-04 | Xe đỏ và xe bạc gán `car` với `truncated=yes`; **tuyệt đối không gán** ảnh xe phản chiếu dưới vũng nước ướt. | Phản chiếu qua mặt nước là ảnh ảo. |
| `img_016` | Hai xe tuk-tuk, xe van Hiace trắng, xe máy xanh | R-01, R-08 | Hai xe 3 bánh gán `tuk_tuk`; xe Hiace gán `van`; xe máy và người gán `motorcycle` + `person`. | Phân biệt rõ ranh giới giữa `tuk_tuk` và `van`. |
| `img_017` | Tượng đá danh nhân cưỡi ngựa, đầu có đội nón giao thông | R-04 | **Tuyệt đối không gán box** (cả người cưỡi lẫn con ngựa). | Tượng điêu khắc nghệ thuật, không phải người thật tham gia giao thông. |
| `img_018` | Biển hiệu quảng cáo lớn in hình chân dung khuôn mặt người | R-04 | **Không gán box** cho mặt người trên biển quảng cáo. | Hình in 2D phẳng trên pa-nô, không phải thực thể 3D. |
| `img_019` | Xe ô tô vàng diễu hành có biển số, chở thú nhồi bông to, đám đông xa | R-01, R-04, R-07 | Xe ô tô vàng gán `car`; người lái bên trong gán `person`; không gán thú bông; đám đông dày đặc sau rào chắn gán `ignore_region`. | Xe thật có động cơ lưu thông vẫn gán `car`; thú bông bị loại; đám đông dày xa dùng ignore. |
| `img_020` | Gương chiếu hậu ô tô phản chiếu hình xe phía sau và mép cửa xe chụp | R-04, R-05 | **Không gán bất kỳ box nào** cho hình ảnh trong gương chiếu hậu hoặc viền mép cửa xe chụp ảnh. | Gương và cửa thuộc xe chủ mang camera (`R-05`); hình trong gương là ảnh ảo phản chiếu (`R-04`). |
| `img_021` | Dòng xe máy và người ở cự ly rất xa | R-06, R-07 | Các đối tượng tiền cảnh cao $\ge 20\text{ px}$ gán riêng; cụm xe máy xa tít mờ nhạt gom vào 01 box `ignore_region`. | Khóa ngưỡng kích thước $20\text{ px}$. |
| `img_022` | Xe mô tô phân khối lớn gắn thùng bên hông (Sidecar) | R-10 | Vẽ **01 box duy nhất** lớp `motorcycle` bao trọn cả xe mô tô và thùng sidecar gắn liền; người lái gán `person`. | Thùng bên hông gắn cố định vào kết cấu xe mô tô. |
| `img_023` | Ô tô sedan Honda đen, người đạp xích lô chở khách | R-01, R-08 | Ô tô gán `car`; người đạp xích lô và khách gán từng box `person`; không vẽ box cho xe xích lô. | Xích lô không động cơ nằm ngoài taxonomy. |
| `img_024` | Xe wagon cổ trưng bày, trên nóc có đặt mô hình ô tô nhỏ màu vàng | R-01, R-04 | Xe wagon lớn gán `car` (xe thật trong showroom); **không gán box** cho mô hình xe vàng trên nóc. | Xe thật trưng bày vẫn là phương tiện thật; xe nhỏ trên nóc là mô hình đồ chơi trang trí. |
| `img_026` | Hai người ngồi trên xe máy đỏ di chuyển, tranh tường phía sau | R-04, R-08 | 01 box `motorcycle` + 02 box `person` (người lái và người ngồi sau); không vẽ box cho tranh vẽ tường. | Tranh tường là hình 2D phẳng; người và xe máy tách riêng. |
| `img_027` | Bia mộ/khối đá tạc hình xe bán tải | R-04 | **Không gán box** cho khối đá tạc hình xe. | Tượng đá điêu khắc tĩnh, đóng vai trò mẫu âm nền. |
| `img_028` | Xe bán tải cổ chở tượng ngựa trắng trên thùng xe | R-04, R-10 | Xe bán tải gán `truck`; **không gán box** cho tượng con ngựa trên thùng xe. | Tượng ngựa là hàng trang trí, không phải sinh vật sống hay phương tiện. |
| `img_029` | Xe máy chở ống kim loại dài vắt ngang, người đi xe đạp bên cạnh | R-08, R-11 | Gán `motorcycle` + `person` lái; box xe máy không kéo dài theo ống kim loại nhô xa; người đi xe đạp chỉ gán `person`. | Hàng hóa nhô quá dài không đưa vào box xe; xe đạp không gán. |
| `img_030` | Bãi đỗ xe máy dày đặc nhiều dãy chồng chéo | R-07 | Khoanh 01 hoặc vài box `ignore_region` bao trùm cụm xe máy chen chúc không thể tách rời; xe nào ở rìa ngoài đứng đơn lẻ rõ ràng vẫn gán `motorcycle`. | Áp dụng đúng quy tắc xử lý cụm đám đông ken đặc. |
| `img_033` | Tủ kính thời trang có ma-nơ-canh và hình ảnh người phản chiếu | R-04 | **Tuyệt đối không gán box** nào. | Ma-nơ-canh và bóng phản chiếu qua kính đều không phải người thật. |
| `img_035` | Xe tuk-tuk chở các bao tải hàng chất cao trên nóc | R-01, R-11 | Gán `tuk_tuk` bao trọn cả thân xe và khối hàng buộc cố định trên nóc xe; tài xế gán `person`. | Hàng chằng buộc trên nóc gắn liền với khối thể tích di chuyển của xe. |
| `img_036` | Xe tải nhỏ chở hàng có mui bạt | R-01, R-10 | Gán lớp `truck` bao gồm cả cabin và thùng mui bạt phía sau. | Kết cấu xe tải thùng riêng biệt rõ ràng. |
| `img_037` | Xe bán tải trắng lắp nắp thùng cao composite, xe buýt xa | R-01, R-10 | Bán tải nắp thùng cao gán `truck`; xe buýt phía sau gán `bus`; người đi bộ gán `person`. | Đã thống nhất bán tải nắp thùng là `truck`. |
| `img_038` | Tủ kính trưng bày nhiều hàng xe mô hình đồ chơi | R-04 | **Tuyệt đối không gán box** cho các xe đồ chơi trong tủ. | Xe đồ chơi thu nhỏ, không phải phương tiện giao thông. |
| `img_040` | Người đi xe máy cắt mép, xe taxi cắt mép, xe buýt xa | R-03, R-08 | Người gán `person` (`truncated=yes`); xe taxi gán `car` (`truncated=yes`); xe buýt gán `bus`; không gán mặt người in quảng cáo trên xe taxi. | Cắt mép ảnh xử lý chuẩn tọa độ biên; loại bỏ ảnh in quảng cáo 2D. |

---

## 5. QC và quản lý phiên bản

### 5.1. Ngưỡng QC áp dụng (Khóa cứng theo hệ thống)

Toàn bộ quá trình kiểm tra chất lượng (QC) và đo lường độ đồng thuận liên gán nhãn (IAA) bắt buộc tuân thủ nghiêm ngặt các ngưỡng kỹ thuật đã cấu hình:

| Tiêu chí kỹ thuật | Giá trị ngưỡng | Ý nghĩa & Ứng dụng |
|---|---|---|
| Kích thước box tối thiểu | $h \ge 20\text{ px}$ | Chiều cao box $< 20\text{ px}$ bắt buộc gom vào `ignore_region`, không gán riêng rẽ. |
| Ngưỡng IoU box lớn | $\text{IoU} \ge 0.85$ | Áp dụng cho các box có chiều cao $h \ge 50\text{ px}$. |
| Ngưỡng IoU box nhỏ | $\text{IoU} \ge 0.70$ | Áp dụng cho các box có chiều cao $20\text{ px} \le h < 50\text{ px}$. |
| Ngưỡng ghép box (Match IoU) | $\text{IoU} \ge 0.50$ | Mức trùng lặp không gian tối thiểu để script tự động ghép 2 box của 2 người gán vào cùng một cặp đối tượng so sánh. |
| Chỉ số đồng thuận vị trí (IAA IoU) | $\ge 0.85$ | Điểm IoU trung bình trên toàn bộ các cặp box ghép được phải đạt tối thiểu $85\%$. |
| Chỉ số đồng thuận lớp (IAA Class) | $\ge 95\%$ | Tỉ lệ thống nhất nhãn lớp trên các cặp box ghép được phải đạt tối thiểu $95\%$. |
| Tỉ lệ lỗi tối đa theo ảnh | $\le 2.0\%$ | Đảm bảo tính khắt khe của bộ dữ liệu bàn giao (tương đương 0 ảnh lỗi trong lô 40 ảnh để đạt quyết định Release). |

---

### 5.2. Quy trình xử lý ca mơ hồ trong lượt gán độc lập

1. **Trong lúc gán độc lập (Pha 3):**
   - Nghiêm cấm trao đổi, thảo luận hoặc xem bài gán của nhau để bảo đảm tính khách quan tuyệt đối của phép đo mù đôi IAA.
   - Khi gặp ca khó hoặc đối tượng biên chưa hoàn toàn chắc chắn: Người gán tự đưa ra quyết định hợp lý nhất dựa trên guideline v1.0, đồng thời **bật cờ `can_review = true`** trên box đó.
   - Nếu đối tượng nằm ở vùng tranh chấp không thể vẽ được box: Ghi lại mã ảnh, tọa độ ước lượng và thắc mắc vào tệp `submission/qc/image_issues.csv`.
2. **Trong buổi họp đối chiếu và hiệu chuẩn (Calibration - Pha 4):**
   - Nhóm chạy script tính toán IAA (`scripts/measure_iaa.py`), lọc toàn bộ các ca lệch nhãn, lệch box hoặc các box có gắn cờ `can_review`.
   - Cả nhóm cùng mở ảnh gốc đối chiếu, thảo luận dưới sự chủ trì của Người điều phối (328) và Người review (228) để chốt quyết định duy nhất cho từng ca.
   - Toàn bộ quyết định sửa đổi được ghi lại minh bạch trong `submission/qc/calibration_decisions.csv` và cập nhật guideline lên phiên bản `v1.0`.

---

### 5.3. Lịch sử thay đổi phiên bản

| Phiên bản | Ngày | Nội dung thay đổi trọng tâm | Lý do / Ca thực tế kích hoạt |
|---|---|---|---|
| `v0` | 16/11/2026 | Bản khung khởi tạo từ Giảng viên (chỉ có 5 lớp cơ bản: `car`, `truck`, `van`, `motorcycle`, `person`). Định nghĩa định tính, thiếu quy tắc ca biên. | Điểm xuất phát của bài lab; chưa đủ chi tiết để gán thực tế. |
| `v1.0` | 16/11/2026 | **Bản thống nhất ban đầu của nhóm:**<br>1. Bổ sung thêm 2 lớp mới: `bus` và `tuk_tuk` (nâng tổng số lên 8 lớp).<br>2. Khóa cứng 12 quy tắc vẽ box (`R-01` $\rightarrow$ `R-12`): tách người và xe máy (`R-08`), gán ô tô con trên xe tải chuyên chở (`R-09`), loại bỏ tượng/mô hình/ảnh in/phản chiếu/xe chủ (`R-04`, `R-05`), khóa kích thước tối thiểu $20\text{ px}$ (`R-06`), xử lý bán tải có mui là `truck` (`R-10`).<br>3. Lập bảng hướng dẫn xử lý 35+ ca khó trên toàn bộ 40 ảnh. | Đối chiếu và giải quyết toàn diện bất đồng giữa 5 bản cá nhân (`03039`, `03223`, `03224`, `03228`, `03238`) trên các ca `img_002`, `img_004`, `img_009`, `img_011`, `img_017`, `img_024`, `img_037`. |
| `v1.0` | 16/11/2026 | **Đơn giản hóa thuộc tính che khuất (`occluded_level`):** Chuyển từ phân chia 4 mức level ($0, 1, 2, 3$) sang trạng thái nhị phân kiểu checkbox (`false`: không che, `true`: bị che). Bỏ toàn bộ việc ước lượng tỷ lệ phần trăm $30\%, 70\%$ phức tạp để loại bỏ bất đồng chủ quan giữa các người gán nhãn, tăng tốc thao tác trên CVAT và nâng cao độ đồng thuận IAA. | Quyết định thống nhất toàn nhóm trước khi bước vào Pha 3 gán nhãn độc lập. |
