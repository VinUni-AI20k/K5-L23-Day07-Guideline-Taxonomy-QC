# Guideline gán nhãn — v0.1 — Thành viên 333 (Check-in CP1)

> Bản guideline cá nhân do Thành viên 333 khởi thảo độc lập tại **Pha 1 (Checkpoint CP1)**, phát triển từ bản khởi đầu `guideline_v0_starter.md`. Bản này tập trung giải quyết triệt để các câu hỏi và tình huống mơ hồ phát hiện qua quá trình soi thực tế bộ 40 ảnh đường phố (`img_001.jpg` đến `img_040.jpg`), làm cơ sở để đối chiếu bất đồng tại buổi họp nhóm Pha 2.

- **Phiên bản:** v0.1 (Bản cá nhân Pha 1 — CP1)
- **Ngày:** 2026-11-16
- **Người viết:** Thành viên 333
- **Định dạng nhãn:** Bounding box 2D (hộp chữ nhật ôm sát phần nhìn thấy) trên ảnh đường phố
- **Công cụ áp dụng:** CVAT v2.74.1, xuất chuẩn COCO 1.0

---

## 1. Mục tiêu

Dữ liệu gán nhãn được dùng để huấn luyện và kiểm thử mô hình phát hiện vật thể 2D (2D Object Detection như YOLO, Faster R-CNN) cho bài toán hỗ trợ lái xe nâng cao (ADAS) và camera giao thông thông minh.

Trong môi trường giao thông phức tạp, đặc biệt là đô thị Việt Nam và châu Á, gán nhãn sai hoặc mơ hồ sẽ dẫn đến những nguy cơ an toàn nghiêm trọng:
- **Bỏ sót người (`person`) và xe máy (`motorcycle`):** Là lỗi nguy hiểm nhất (đe dọa tính mạng), vì hệ thống phanh tự động khẩn cấp (AEB) sẽ không được kích hoạt khi có người đi bộ hoặc người đi xe máy xuất hiện.
- **Gán nhầm vật giả thành vật thật (tượng đá/đồng, xe đồ chơi, hình ảnh phản chiếu trong gương):** Khiến mô hình nhận diện chướng ngại vật ảo, kích hoạt hiện tượng phanh giật đột ngột ("phanh ma" - phantom braking), gây nguy cơ tai nạn dồn toa từ phía sau.
- **Vẽ box sai ranh giới (bao cả hàng cồng kềnh, không ôm sát phần nhìn thấy):** Gây sai lệch tỷ lệ khung hình, làm mô-đun ước lượng khoảng cách 3D và tính toán thời gian va chạm (Time-to-Collision - TTC) bị sai lệch hoàn toàn.

---

## 2. Lớp và thuộc tính

### 2.1. Phân loại lớp đối tượng (Classes)

Bộ nhãn kế thừa danh mục lớp từ taxonomy v0 nhưng định nghĩa chặt chẽ với ranh giới rõ ràng:

| Lớp | Định nghĩa (một câu) | Ví dụ cụ thể | Phản ví dụ / Dễ nhầm với |
|---|---|---|---|
| `car` | Xe ô tô con từ 4 đến 9 chỗ ngồi chở người (sedan, SUV, hatchback, coupe). | Xe con trên sàn xe chở xe ở `img_002.jpg`; xe chạy trên đường ở `img_015.jpg`. | Xe mô hình đồ chơi trong tủ kính (`img_038.jpg`); tượng xe bán tải bằng đá (`img_027.jpg`). |
| `truck` | Xe ô tô tải có kết cấu khung gầm chịu lực và khoang chở hàng riêng biệt (gồm cả xe bán tải chở hàng, xe tải nhẹ, xe đầu kéo, xe chở xe). | Xe chở ô tô 2 tầng Renault 380 (`img_002.jpg`); xe bán tải chở hàng đầy thùng (`img_001.jpg`, `img_012.jpg`, `img_028.jpg`). | Xe SUV chở đồ trong cốp (`car`); xác vỏ xe phế liệu trên nóc (`img_024.jpg`). |
| `van` | Xe ô tô dạng thùng kín liền khối chở người cỡ trung hoặc chở hàng nhẹ bưu chính. | Xe van giao hàng ban đêm trên phố ở `img_031.jpg`. | Xe tải thùng hở (`truck`); xe khách buýt lớn (`bus`). |
| `motorcycle` | Phương tiện giao thông hai bánh có động cơ gắn máy (gồm xe máy, xe ga, mô tô và mô tô có thùng phụ sidecar). | Xe máy lưu thông trên đường ở `img_005.jpg`, `img_026.jpg`; mô tô có thùng phụ `img_022.jpg`. | Xe ba bánh tuk-tuk (`img_004.jpg`, `img_035.jpg`); xe đạp/xích lô đạp chân (`img_006.jpg`). |
| `person` | Con người còn sống trong mọi tư thế (đi bộ, đứng, ngồi, lái xe hoặc hành khách). | Người phụ nữ bên xe tải `img_001.jpg`; người lái xe máy `img_005.jpg`, `img_026.jpg`. | Tượng điêu khắc (`img_011.jpg`, `img_017.jpg`); ma-nơ-canh thời trang (`img_033.jpg`); hình in chân dung trên biển quảng cáo (`img_018.jpg`). |
| `ignore_region` | Vùng nhãn hình chữ nhật đánh dấu khu vực bỏ qua không gán nhãn chi tiết. | Đám đông người và xe li ti ở hậu cảnh xa tít (`img_008.jpg`, `img_025.jpg`, `img_040.jpg`). | Vật thể đơn lẻ nhìn rõ, có chiều cao $\ge 20\text{ px}$ (bắt buộc phải gán box riêng). |

#### Giải đáp quy định cho các vật thể nằm ngoài danh mục trên:
1. **Xe tuk-tuk (`img_004.jpg`, `img_035.jpg`):** Bản v0 **chưa có lớp cho tuk-tuk**. Không được gán ép vào `car` (sai phân phối hình học) hay `motorcycle` (sai số bánh và kết cấu buồng lái). Trong bản v0.1 cá nhân, **tạm thời chưa gán hoặc tick cờ `can_review = true`** và đề xuất bổ sung lớp `tuk_tuk` ở Pha 2.
2. **Xe buýt cỡ lớn (`img_009.jpg`, `img_031.jpg`, `img_037.jpg`, `img_040.jpg`):** Bản v0 chưa có lớp `bus`. Tạm thời gán `truck` kèm `can_review = true` và đề xuất bổ sung lớp `bus` ở Pha 2.
3. **Xe thô sơ đạp chân (xe đạp, xích lô `img_006.jpg`, `img_023.jpg`):** Không gán box cho khung xe đạp/xích lô (vì không có động cơ cơ giới), nhưng **bắt buộc gán box `person`** cho người đạp và hành khách ngồi trên xe.

---

### 2.2. Thuộc tính đối tượng (Attributes có ngưỡng đo được)

Thay thế các từ ngữ định tính ("che ít", "che nhiều") của v0 bằng các ngưỡng định lượng chính xác:

#### 1. `occluded_level` (Mức độ che khuất bởi vật thể khác)
- **`0` (Không bị che):** Nhìn thấy trọn vẹn, diện tích bị che khuất $< 1\%$ (thấy $\ge 99\%$).
  > **Lưu ý đặc biệt ca `img_015.jpg`:** Xe chạy nhanh bị nhòe vệt chuyển động (motion blur) hoặc nhòe mưa **KHÔNG PHẢI là occluded**. Occluded chỉ tính khi có một vật thể vật lý khác che chắn tầm nhìn. Do đó, nếu xe lộ toàn thân dù bị nhòe mờ thì vẫn chọn `occluded_level = 0`.
- **`1` (Che khuất ít):** Diện tích vật thể bị che khuất từ $1\%$ đến $30\%$.
- **`2` (Che khuất nhiều):** Diện tích vật thể bị che khuất từ $31\%$ đến $70\%$.
- **`3` (Che khuất rất nặng):** Diện tích bị che khuất $> 70\%$ đến $95\%$, phần lộ ra vẫn nhận diện chắc chắn được lớp. Nếu bị che $> 95\%$ không nhận diện được thì không gán.

#### 2. `truncated` (Bị cắt bởi mép ảnh)
- **`no`:** Toàn bộ đối tượng nằm hoàn toàn bên trong khung ảnh.
- **`yes`:** Đối tượng bị cắt cụt bởi ít nhất một mép cạnh của bức ảnh.

#### 3. `can_review` (Đánh dấu cần xem lại)
- **`false` (mặc định):** Tự tin với quyết định gán nhãn.
- **`true`:** Đánh dấu khi gặp ca biên còn tranh cãi (như tuk-tuk, hàng cồng kềnh, nắp thùng bán tải, xe custom) để đưa ra thảo luận tại buổi họp nhóm Pha 2.

---

## 3. Quy tắc vẽ box chi tiết

Quy định dứt khoát cho các tình huống biên phát hiện từ 40 ảnh:

- **R-01 — Ôm sát phần nhìn thấy (Visible box):**
  Box chỉ bao trọn các pixel thuộc phần nhìn thấy thực tế của vật thể. Không tự suy đoán vẽ trùm qua phần bị che khuất.
- **R-02 — Tách rời người và xe máy (`img_005.jpg`, `img_026.jpg`):**
  Người ngồi trên xe máy bắt buộc tách thành 2 box riêng rẽ:
  + Box `person`: Ôm trọn người từ đỉnh đầu/mũ bảo hiểm đến chân/gác chân.
  + Box `motorcycle`: Ôm trọn khung xe hai bánh.
  + Nếu chở 2 người (`img_026.jpg`): Vẽ 2 box `person` và 1 box `motorcycle`.
- **R-03 — Xe máy ghép / Thùng phụ sidecar (`img_022.jpg`):**
  Phương tiện mô tô có thùng phụ bên hông gán chung **1 box `motorcycle`** bao cả thân mô tô và thùng phụ (vì thùng phụ gắn liền cơ khí tạo thành kết cấu xe 3 bánh). Người lái và người ngồi trong thùng phụ gán mỗi người một box `person` riêng.
- **R-04 — Xe chở hàng cồng kềnh (`img_029.jpg`, `img_035.jpg`) — CÓ BAO HÀNG KHÔNG?:**
  **QUYẾT ĐỊNH: KHÔNG BAO KHỐI HÀNG QUÁ KHỔ!**
  + Bounding box của phương tiện chỉ ôm trọn phần thân khung xe cơ giới (bánh xe, buồng lái, sàn xe).
  + Khối bao tải khổng lồ phình to trên tuk-tuk (`img_035.jpg`) hay chồng chậu nhựa chất cao vút trên xe máy (`img_029.jpg`) là hàng hóa rời quá khổ dị thường. Kéo box bao cả hàng hóa sẽ làm phình to box gấp 3-4 lần, làm méo mó tỉ lệ hình học của xe và khiến hai người gán không thể khớp IoU. Gán box cho thân xe và tick `can_review = true`.
- **R-05 — Xe bán tải gắn nắp thùng cao / Xe nhà ở lưu động (`img_037.jpg`):**
  Chiếc xe GO Transit gắn nắp thùng cao Master 75 Truck Cap là xe bán tải (pickup) gắn thêm nắp đậy khoang hàng. **Quyết định: Gán `truck`** (do nền tảng khung gầm xe tải bán tải có đầu cabin và thùng hàng riêng biệt), đồng thời tick `can_review = true` để đưa ra thảo luận thống nhất giữa `truck` và `van` ở Pha 2.
- **R-06 — Xe tùy biến / Xe hóa trang custom (`img_019.jpg` Dangermouse car):**
  Chiếc xe diễu hành đồ chơi Hamley's Toy Parade bản chất là khung gầm xe ô tô con tự hành được chế tác vỏ ngoài hình con chuột. **Quyết định: Gán `car`** bao toàn bộ thân xe đang lưu thông trên đường, tick `can_review = true`.
- **R-07 — Xe bán tải chở tượng ngựa (`img_028.jpg`) — CÓ BAO CON NGỰA KHÔNG?:**
  **QUYẾT ĐỊNH: KHÔNG BAO TƯỢNG NGỰA!**
  Gán 1 box `truck` cho xe bán tải (thùng xe chở hàng hóa thông thường bao theo viền thùng xe). Tuyệt đối **không vẽ box riêng cho con ngựa** vì đây là tượng ngựa trang trí ("yorse"), không phải động vật sống và không thuộc taxonomy.
- **R-08 — Tượng người và tượng xe (`img_011.jpg`, `img_017.jpg`, `img_027.jpg`):**
  **QUYẾT ĐỊNH: TUYỆT ĐỐI KHÔNG GÁN NHÃN (0 annotation)!**
  + `img_011.jpg`: Tượng Predator (không phải `person`).
  + `img_017.jpg`: Tượng đồng Công tước Wellington và tượng ngựa đá (không phải `person`).
  + `img_027.jpg`: Bia mộ bằng đá tạc hình xe bán tải Pickup Truck Monument (không phải `truck` hay `car`).
- **R-09 — Xe phản chiếu trong gương chiếu hậu (`img_020.jpg`):**
  **QUYẾT ĐỊNH: TUYỆT ĐỐI KHÔNG GÁN NHÃN!**
  Ảnh phản chiếu trong gương chiếu hậu là ảnh ảo quang học 2D, không phản ánh vị trí vật lý thực của phương tiện trong không gian 3D.
- **R-10 — Xe mô hình đồ chơi và ma-nơ-canh trong tủ kính (`img_033.jpg`, `img_038.jpg`):**
  **QUYẾT ĐỊNH: TUYỆT ĐỐI KHÔNG GÁN NHÃN (0 annotation)!**
  Xe đồ chơi thu nhỏ và búp bê trong tủ kính (`img_038.jpg`) hay ma-nơ-canh trong tiệm quần áo (`img_033.jpg`) không phải là phương tiện hay người thật tham gia giao thông.
- **R-11 — Xe chuyên dụng chở ô tô (`img_002.jpg`):**
  Gán 1 box `truck` cho xe tải chở; gán riêng từng box `car` cho mỗi chiếc xe con nhìn thấy rõ trên 2 tầng sàn.

---

## 4. Bảng phân tích các ca khó tìm thấy trong 40 ảnh

Bảng chi tiết giải đáp toàn bộ danh sách 11 câu hỏi/ca biên của tôi và các ca cốt lõi của bài lab:

| Ảnh | Tình huống / Câu hỏi phát hiện | Rule áp dụng | Quyết định cá nhân của tôi (CP1) | Lý do lập luận kỹ thuật |
|---|---|---|---|---|
| `img_004.jpg` | **Xe tuk-tuk thuộc lớp gì?** | Mục 2.1 | Không gán ép vào `car` hay `motorcycle`; tick `can_review = true`. Đề xuất tạo lớp `tuk_tuk`. | Xe 3 bánh có động cơ khác hẳn ô tô con về kích thước và khác xe máy về động học; gán ép sẽ làm sai phân phối đặc trưng. |
| `img_015.jpg` | **Xe chạy nhanh bị nhem (motion blur) là occluded hay thường?** | R-01, Mục 2.2 | **Là thường (`occluded_level = 0`)**; không phải occluded. Vẽ box ôm vệt mờ, tick `can_review`. | Occluded chỉ tính khi bị vật thể vật lý khác che chắn. Nhòe mờ chuyển động là hiện tượng quang học cảm biến, xe vẫn lộ toàn bộ thân. |
| `img_017.jpg` | **Không đánh nhãn tượng (không xác định)?** | R-08 | **Đúng, KHÔNG đánh nhãn nào (0 annotation)**. | Tượng đồng Duke of Wellington là công trình điêu khắc tĩnh, không có nguy cơ giao thông. Gán nhãn sẽ gây báo động giả (phanh ma). |
| `img_019.jpg` | **Xe custom (xe diễu hành Dangermouse) thì đánh nhãn gì?** | R-06 | **Gán nhãn `car`**, tick `can_review = true`. Không gán các hình nộm trang trí. | Bản chất là khung gầm xe ô tô con tự hành được lưu thông trên đường trong lễ hội diễu hành. |
| `img_020.jpg` | **Không đánh nhãn xe phản chiếu trong gương?** | R-09 | **Đúng, TUYỆT ĐỐI KHÔNG gán nhãn** cho xe hoặc người trong gương chiếu hậu. | Ảnh phản chiếu là ảnh ảo 2D, sai lệch hoàn toàn khoảng cách vật lý và hướng di chuyển trong không gian 3D. |
| `img_022.jpg` | **Xe máy ghép (mô tô có thùng phụ sidecar)?** | R-03 | **Gán 1 box `motorcycle`** bao cả xe và thùng phụ; gán các box `person` riêng cho từng người. | Thùng phụ gắn liền cơ khí với xe máy tạo thành 1 phương tiện 3 bánh duy nhất; người ngồi trong thùng vẫn là con người. |
| `img_027.jpg` | **Xe tượng (bia mộ tạc hình xe bán tải)?** | R-08 | **KHÔNG gán nhãn (0 annotation)**. | Đây là khối đá hoa cương điêu khắc bia mộ trong nghĩa trang, hoàn toàn không phải xe cơ giới. |
| `img_028.jpg` | **Có bao con ngựa không?** | R-07 | **KHÔNG bao con ngựa!** Chỉ gán 1 box `truck` cho xe bán tải chở đồ. | Con ngựa trong thùng là tượng điêu khắc trang trí chở theo ("yorse"), không thuộc taxonomy và không phải sinh vật sống. |
| `img_035.jpg` | **Xe chở hàng cồng kềnh thì có bao hàng không?** | R-04 | **KHÔNG bao khối bao tải khổng lồ!** Chỉ ôm khung xe tuk-tuk, tick `can_review = true`. | Khối hàng chất quá khổ bất thường; nếu bao cả hàng sẽ làm méo tỉ lệ khung xe và gây tụt IoU nghiêm trọng khi đo IAA. |
| `img_037.jpg` | **Xe nhà ở lưu động (bán tải gắn nắp thùng cao) là lớp gì?** | R-05 | **Gán lớp `truck`**, tick `can_review = true` để đưa ra họp nhóm chốt giữa `truck` và `van`. | Kết cấu gốc là xe bán tải chở hàng có nắp thùng cao Master 75 Truck Cap che kín khoang tải. |
| `img_038.jpg` | **Xe đồ chơi trong tủ kính?** | R-10 | **KHÔNG gán nhãn (0 annotation)**. | Mô hình xe ô tô thu nhỏ và búp bê trong tủ kính không tham gia giao thông thực tế. |
| `img_002.jpg` | Xe chuyên dụng chở 8 ô tô con trên hai tầng sàn. | R-11 | Gán 1 box `truck` cho xe tải chở; gán 8 box `car` riêng cho 8 ô tô con trên sàn. | Xe chở xe là 1 thể vận hành (`truck`), từng xe con trên sàn là phương tiện nhìn thấy rõ cần nhận diện độc lập. |
| `img_005.jpg` | Dòng xe máy đông đúc tại ngã tư TP.HCM. | R-02 | Tách riêng box `person` cho từng người và box `motorcycle` cho từng xe. | Quy tắc phân tách người và xe máy cần nhất quán để mô hình học độc lập đặc trưng. |

---

## 5. QC và phiên bản

### 5.1. Ngưỡng kiểm soát chất lượng áp dụng

- **Độ phủ (Coverage):** $100\%$ số ảnh được phân công (kể cả các ảnh 0 annotation như `img_017.jpg`, `img_020.jpg`, `img_027.jpg`, `img_038.jpg` vẫn phải có mặt trong file COCO export).
- **Độ đồng thuận diện tích (IoU):** $\ge 0.85$ với box lớn ($\ge 50\text{ px}$), $\ge 0.70$ với box nhỏ. IoU trung bình giữa các người gán phải $\ge 0.85$.
- **Đồng thuận phân lớp (IAA class agreement):** $\ge 95\%$.
- **Tỷ lệ ảnh lỗi nghiệm thu (Release):** $\le 2.0\%$ trên toàn bộ lô (với lô 40 ảnh: yêu cầu $0/40$ ảnh lỗi).

### 5.2. Thẩm quyền quyết định và xử lý ca mơ hồ

- Ở Pha 1 (CP1): Tự quyết định theo logic cá nhân, đánh dấu cờ `can_review = true` trên các box phân vân để đưa ra họp nhóm.
- Ở Pha 2: Cả nhóm đối chiếu các ca cờ `can_review` và bảng ca khó để biểu quyết thống nhất đưa vào guideline v1.0.

### 5.3. Lịch sử thay đổi phiên bản

| Phiên bản | Nội dung thay đổi | Căn cứ và lý do thay đổi |
|---|---|---|
| `v0` | Bản khởi đầu của giảng viên. | Khung sơ lược, chưa định lượng che khuất, chưa có quy tắc cho tượng, phản chiếu, đồ chơi, tuk-tuk, hàng cồng kềnh. |
| `v0.1` | Bản cá nhân của Thành viên 333 (CP1):<br>- Giải đáp dứt khoát 11 câu hỏi/ca biên thực tế: không gán tượng (`017`, `027`), không gán gương (`020`), không gán đồ chơi (`038`), không bao tượng ngựa (`028`), không bao hàng quá khổ (`035`), xe nhem motion blur không phải occluded (`015`), xe custom gán `car` (`019`), xe máy ghép sidecar gán `motorcycle` (`022`), xe bán tải thùng cao gán `truck` (`037`).<br>- Định lượng 4 mức `occluded_level` theo tỷ lệ % cụ thể.<br>- Đề xuất bổ sung lớp `tuk_tuk` và `bus` cho Pha 2. | Khảo sát thực tế toàn bộ 40 bức ảnh đường phố tại Pha 1. |
