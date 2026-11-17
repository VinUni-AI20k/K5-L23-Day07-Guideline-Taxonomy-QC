# Guideline gán nhãn — v0.1-individual — Thành viên 103

- Phiên bản: `v0.1-103` (Bản đề xuất cá nhân của thành viên `103` trước cuộc họp Pha 2)
- Ngày: 2026-11-16
- Người viết: `103`
- Công cụ & Định dạng: CVAT, xuất COCO 1.0 (bounding box 2D trục đứng `[x, y, width, height]`)

---

## 1. Mục tiêu

Bộ nhãn dùng để huấn luyện và đánh giá mô hình **phát hiện người và phương tiện giao thông đường bộ 2D (Object Detection)** phục vụ bài toán nhận diện giao thông đô thị / hỗ trợ lái xe (ADAS) và giám sát giao thông đường phố.

- **Tác động của lỗi gán nhãn:**
  - **Bỏ sót (`bo_sot` - False Negative):** Nguy hiểm cao đối với an toàn giao thông nếu bỏ sót người đi bộ (`person`), người đi xe máy (`motorcycle`) hoặc xe đang lưu thông gần.
  - **Gán thừa vật không thật (`thua` - False Positive):** Gán nhầm tượng đá/đồng, ma-nơ-canh, mô hình đồ chơi, ảnh in trên biển quảng cáo hoặc ảnh phản chiếu làm mô hình học sai đặc trưng hình học và phanh/cảnh báo giả.
  - **Box lỏng hoặc gộp sai (`sai_vi_tri_kich_thuoc`):** Gộp chung người lái và xe máy thành 1 box hoặc vẽ tràn sang phần bị che khuất làm giảm chất lượng локаlization (IoU).

---

## 2. Lớp và thuộc tính

### 2.1. Bảng định nghĩa lớp (mỗi đối tượng thật thuộc đúng một lớp)

| Lớp | Định nghĩa (một câu) | Ví dụ trong bộ ảnh | Phản ví dụ / Dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con chở người (sedan, hatchback, SUV, crossover, wagon, xe thể thao 4 bánh). | Ô tô con đỗ sau hàng rào (`img_018`), wagon cổ (`img_024`), xe con trên đường (`img_035`, `img_040`), xe con gắn biểu tượng hóa trang có biển số thật (`img_019`). | Xe bán tải có thùng hàng hở/nắp thùng (`truck`), xe van thùng kín (`van`), mô hình ô tô đồ chơi (`img_038` - không gán). |
| `truck` | Xe tải chở hàng, xe đầu kéo, và **xe bán tải (pickup truck)** có thùng hàng phía sau (kể cả có lắp nắp thùng/cầu hàng). | Xe bán tải đỗ trước quán ăn (`img_001`), xe đầu kéo chở ô tô (`img_002`), xe tải kho hàng (`img_007`), pickup chở hàng (`img_012`), tải nhẹ (`img_036`), pickup có nắp thùng (`img_037`). | Tượng đá hình xe bán tải ở nghĩa trang (`img_027` - không gán), SUV 7 chỗ khoang liền (`car`). |
| `van` | Xe thùng kín cỡ nhỏ/trung chuyên chở người hoặc hàng hóa có ca-bin liền khối với khoang sau (minivan,厢式/panel van, minibus). | Xe van màu bạc chạy ngang đường (`img_005`), xe van cứu thương/chuyên dụng ở lễ hội (`img_011`). | Xe hatchback/wagon cỡ nhỏ (`car` - `img_024`), xe tải có thùng hàng tách rời ca-bin (`truck`). |
| `motorcycle` | Xe gắn máy, mô tô 2 bánh hoặc xe máy 3 bánh có động cơ (bao gồm xe máy độ, moto sidecar, tuk-tuk / auto-rickshaw có động cơ). | Xe máy đang chạy (`img_005`, `img_026`, `img_030`), xe máy độ (`img_011`), mô tô 3 bánh/sidecar (`img_022`), đề xuất gộp tuk-tuk/auto-rickshaw (`img_004`, `img_035`) hoặc tách quy tắc riêng khi họp nhóm. | Người ngồi trên xe máy (`person` - vẽ box riêng), xe đạp/xích lô đạp chân không động cơ (`img_006`, `img_009`, `img_034` - ngoài phạm vi). |
| `person` | Con người thật (người đi bộ, người đứng/ngồi quán vỉa hè, người lái hoặc ngồi sau xe máy, người ngồi trong phương tiện nếu nhìn thấy rõ phần cơ thể). | Người đi xe máy (`img_005`, `img_030`), người đi bộ/bán hàng (`img_003`, `img_010`, `img_014`), người mặc đồ hóa trang Predator (`img_011`), người ngồi lái trong xe (`img_004`, `img_019`). | Tượng người (`img_017`), ma-nơ-canh (`img_033`), ảnh người in trên biển quảng cáo (`img_018`), búp bê/đồ chơi (`img_038`), phần mascot chuột bông gắn trên xe (`img_019`). |
| `ignore_region` | Vùng ảnh chứa đám đông/bãi xe quá dày đặc không thể tách từng cá thể, hoặc vùng chứa vật thật nhưng nhỏ hơn ngưỡng kích thước tối thiểu (`cao < 20 px`). | Đám đông người xem lễ hội ở xa (`img_011`, `img_019`), dãy người/xe quá nhỏ ở hậu cảnh xa (`img_025`, `img_040`). | Không dùng `ignore_region` để bọc tượng, biển quảng cáo hay đồ chơi (những vật không thật đó phải **bỏ qua không vẽ box**). |

### 2.2. Xử lý vật ngoài phạm vi (Out-of-Taxonomy)

- **Phương tiện thô sơ không động cơ (xe đạp, xích lô đạp chân, xe đẩy hàng tay):** Không thuộc 5 lớp đối tượng trên → **Không gán box cho phương tiện**, nhưng **vẫn gán `person`** cho người đạp xích lô, hành khách ngồi trên xích lô và người đi xe đạp (ví dụ: `img_003`, `img_006`, `img_009`, `img_010`, `img_023`, `img_034`, `img_039`).
- **Phương tiện 3 bánh có động cơ (Tuk-tuk `img_004`, Auto-rickshaw `img_035`):** Đề xuất đưa ra họp nhóm ở Pha 2:
  - *Phương án A (Đề xuất ưu tiên):* Xếp vào `motorcycle` (vì cấu trúc tay lái ghi-đông, khung sườn mô tô 3 bánh có động cơ) và tick `can_review` nếu biên giới loại xe mơ hồ.
  - *Phương án B:* Loại khỏi phạm vi phương tiện, chỉ gán `person` bên trong.
- **Xe buýt lớn (`img_032`):** Đề xuất thảo luận nhóm xem không gán (vì không có lớp `bus`) hay bọc `ignore_region` nếu che khuất phương tiện khác; người đứng chờ ở trạm vẫn gán `person`.

### 2.3. Thuộc tính và ngưỡng đo lường cụ thể

Mỗi đối tượng (`car`, `truck`, `van`, `motorcycle`, `person`) bắt buộc gán đủ 3 thuộc tính:

| Thuộc tính | Kiểu | Giá trị | Ngưỡng định lượng & Quy tắc chọn |
|---|---|---|---|
| `occluded_level` | `select` | `0` | **Thấy rõ (0% – < 10% diện tích bị che):** Vật hầu như nguyên vẹn, không bị vật khác chắn trước mặt. |
| | | `1` | **Che ít (10% – 50% diện tích bị che):** Bị che một phần (ví dụ: người lái xe máy bị phần đầu xe/người trước che chân, ô tô sau hàng rào thưa `img_018`), nhưng nhìn rõ hình dáng chính. |
| | | `2` | **Che nhiều (> 50% – 80% diện tích bị che):** Chỉ nhìn thấy một phần nhỏ (ví dụ: người ngồi sau xe máy bị che khuất phần lớn thân mình trong `img_005`, xe lấp sau xe khác). |
| | | `3` | **Che rất nặng (> 80%) hoặc không xác định được mức che:** Chỉ lộ một chi tiết rất nhỏ hoặc vùng tối/nhòe khó ước lượng tỷ lệ bị che. |
| `truncated` | `select` | `no` | Toàn bộ phần nhìn thấy của vật nằm gọn bên trong khung ảnh (cách mép ảnh ≥ 2 px). |
| | | `yes` | Bất kỳ phần thực tế nào của vật bị **cắt bởi 1 trong 4 cạnh biên của bức ảnh** (ví dụ: nửa người/xe ở rìa ảnh `img_005`, `img_011`). *Lưu ý: Vật bị che bởi vật khác ở giữa ảnh là `occluded`, KHÔNG phải `truncated`.* |
| `can_review` | `checkbox` | `false` / `true` | Chọn `true` (tick) khi gặp ca biên chưa chắc chắn về lớp, ranh giới box bị tối/nhòe nặng (`img_007`, `img_013`, `img_031`), hoặc ca đặc biệt cần nhóm đối chiếu khi Calibration. |

---

## 3. Quy tắc vẽ box (Mã hóa quy tắc `R-xx`)

- **`R-01` (Ôm sát phần nhìn thấy - Visible Box):**
  - Box phải **ôm sát phần diện tích thực sự nhìn thấy được (visible pixels)** của đối tượng với sai số biên ≤ 2 px.
  - **Không đoán phần bị che** (không vẽ amodal box mở rộng ra vùng bị vật khác che khuất hoàn toàn).
  - Nếu một vật bị vật chắn cắt làm 2 phần rời nhau nhưng rõ ràng cùng 1 đối tượng (ví dụ: ô tô nhìn xuyên qua song sắt hàng rào ở `img_018`, hoặc xe trên giá đỡ `img_002`), vẽ **1 box duy nhất** bao trọn các phần nhìn thấy của đối tượng đó và đặt `occluded_level` tương ứng (`1` hoặc `2`).

- **`R-02` (Tách rời Người và Phương tiện - Rider & Vehicle):**
  - Người đi xe máy / mô tô (`img_005`, `img_008`, `img_026`, `img_030`): **Tách riêng box `person` và box `motorcycle`**, tuyệt đối không vẽ 1 box gộp cả người lẫn xe.
  - Box `person` bao gồm toàn bộ cơ thể nhìn thấy của người đó và **mũ bảo hiểm đang đội trên đầu** / trang phục mặc trên người (kể cả trang phục hóa trang như Predator ở `img_011`).
  - Box `motorcycle` bao gồm thân xe, bánh xe, tay lái, gương chiếu hậu và **hàng hóa/thùng hàng buộc cố định trên xe** (`img_029`, `img_035`).

- **`R-03` (Người ngồi bên trong phương tiện có buồng lái):**
  - Nếu nhìn thấy rõ người ngồi trong khoang lái qua kính chắn gió hoặc xe mui trần/tuk-tuk (`img_004`, `img_019`, `img_035`) và phần nhìn thấy của người có chiều cao **≥ 20 px**: gán thêm box `person` cho người đó với `occluded_level = 2` (do bị thân xe che phần dưới). Nếu chỉ thấy bóng mờ tối dưới 20 px thì không gán.

- **`R-04` (Loại trừ vật không thật, phản chiếu và Ego-vehicle):**
  - **Không gán box** cho:
    1. Tượng điêu khắc người/ngựa/xe bằng đá, đồng, nhựa (`img_017` tượng cưỡi ngựa, `img_027` bia mộ hình xe bán tải, `img_028` mô hình ngựa trên thùng xe, phần thú bông trắng Danger Mouse trong `img_019`).
    2. Ma-nơ-canh trưng bày (`img_033`) và búp bê, xe mô hình đồ chơi (`img_038`).
    3. Hình ảnh người/xe in trên áp phích, biển quảng cáo 2D (`img_018` - biển bầu cử).
    4. Hình ảnh phản chiếu qua gương chiếu hậu, vũng nước, mặt kính (`img_020` ô tô phản chiếu trong gương, `img_033` phản chiếu trên kính).
    5. Phần thân xe chủ (ego-vehicle) nơi đặt máy ảnh chụp ra (`img_015`, `img_020`).

- **`R-05` (Xe chở xe - Car Carrier):**
  - Trong ảnh xe đầu kéo chở nhiều ô tô con (`img_002`):
    - Gán **1 box `truck`** cho xe tải/đầu kéo chở hàng (bao gồm đầu kéo và rơ-moóc sàn chở).
    - Gán **các box `car` riêng biệt** cho từng chiếc ô tô con đang nằm trên sàn chở (mỗi xe 1 box ôm phần nhìn thấy, gắn `occluded_level = 1` hoặc `2` do khung sắt rơ-moóc che).

- **`R-06` (Ngưỡng vật nhỏ và Đám đông - `ignore_region`):**
  - Đối tượng thật có chiều cao phần nhìn thấy **< 20 px** (theo `rules.min_box_height_px = 20` trong `taxonomy.json`): **Không gán lớp đối tượng cá별**, mà dùng box `ignore_region` bao quanh khu vực chứa các vật nhỏ đó.
  - Khu vực đám đông người đi bộ hoặc hàng xe máy ở xa chồng lấn dày đặc (> 5 đối tượng dính liền không thể phân tách ranh giới từng cá thể, ví dụ hậu cảnh `img_011`, `img_019`, `img_025`, `img_040`): vẽ **1 box `ignore_region`** bao trùm cụm đám đông đó.

---

## 4. Ca khó (Phân tích trên bộ 40 ảnh thực tế)

| Ảnh | Tình huống | Rule ID | Quyết định đề xuất | Lý do & Phân loại (Quy tắc / Cần Review) |
|---|---|---|---|---|
| `img_002` | Xe đầu kéo (`Renault 380`) chở 7 ô tô con trên 2 tầng giá đỡ, có 1 người đứng cạnh đuôi xe. | `R-05` | Gán 1 `truck` (xe chở), 7 `car` (từng xe trên giá, `occluded_level=1,2`), 1 `person` đứng cạnh, 1 `van` nhỏ ở xa bên phải. | **Cần chốt nhóm (Pha 2):** Thống nhất box `truck` chỉ ôm đầu kéo hay ôm cả khung rơ-moóc cam để tránh lệch IoU. |
| `img_004` | Hai xe tuk-tuk 3 bánh màu xanh đỗ cạnh nhau ban đêm, có tài xế ngồi trong. | `R-02`, `R-03` | Đề xuất gán 2 `motorcycle` cho 2 xe tuk-tuk + 2 `person` cho 2 tài xế ngồi trong (`occluded_level=2`), tick `can_review`. | **Cần chốt nhóm (Pha 2):** Taxonomy không có lớp `tuk-tuk`/`three-wheeler`; cần chốt gộp vào `motorcycle` hay loại trừ. |
| `img_005` | Nhiều người đi xe máy chụp cận cảnh ở TP.HCM, cắt mép dưới, có người ngồi sau bị che nặng; phía sau có xe van bạc và ô tô con. | `R-01`, `R-02` | Tách riêng từng `person` (5 người, `truncated=yes` cho người ở mép dưới) và từng phần `motorcycle` nhìn thấy; xe bạc lớn phía sau gán `van`, xe bên trái gán `car`. | **Áp dụng theo quy tắc:** Ví dụ điển hình để kiểm tra tách người/xe, `truncated=yes` và `occluded_level=2` cho người ngồi giữa bị che. |
| `img_006`, `img_009`, `img_023`, `img_034`, `img_039` | Đoàn xích lô du lịch ở Huế chở khách trên đường phố. | `R-02` | **Không gán** chiếc xích lô (xe đạp 3 bánh không động cơ); **gán `person`** cho người đạp xích lô và hành khách ngồi trên xe; gán `motorcycle`/`car` cho xe cơ giới xung quanh. | **Loại theo quy tắc:** Xích lô là phương tiện thô sơ sức người, không thuộc `motorcycle`. |
| `img_011` | Người mặc bộ đồ hóa trang quái vật Predator đứng trước dàn mô tô độ; phía xa là đám đông lễ hội rất nhỏ. | `R-02`, `R-06` | Người mặc đồ Predator vẫn là **người thật** → gán `person` (`truncated=yes`); dàn xe độ phía trước gán `motorcycle`; xe cứu thương/chuyên dụng gán `van`; đám đông nhỏ ở xa gán `ignore_region`. | **Cần chốt nhóm / Tick `can_review`:** Dàn xe máy độ hình xương có ranh giới phức tạp, cần thống nhất số box `motorcycle` ở tiền cảnh. |
| `img_017` | Tượng đồng Công tước Wellington cưỡi ngựa đội nón chóp giao thông ở Glasgow. | `R-04` | **Không gán bất kỳ box nào** (ảnh rỗng `0` annotation trong COCO). | **Loại theo quy tắc:** Tượng điêu khắc không phải người thật; nếu 2 người cùng gán `person` thì IAA cao giả tạo nhưng vẫn là lỗi `thua`. |
| `img_018` | Biển quảng cáo bầu cử (billboard) có hình người đàn ông lớn; phía dưới là 4 ô tô đỗ sau hàng rào sắt. | `R-01`, `R-04` | **Không gán** hình người trên biển quảng cáo; gán 4 box `car` cho 4 ô tô thật phía dưới hàng rào với `occluded_level=1` (bị song sắt và biển báo chắn một phần). | **Loại theo quy tắc (biển quảng cáo) + Quy tắc che khuất (`R-01`):** Hàng rào thưa không tách ô tô thành nhiều box nhỏ. |
| `img_019` | Xe độ vàng "Danger Mouse" trong lễ diễu hành: có 1 người thật ngồi lái bên phải và 1 mô hình chuột trắng bên trái; hai bên vỉa hè là đám đông dày đặc. | `R-03`, `R-04`, `R-06` | Xe vàng có biển số và bánh chạy thật → gán 1 `car`; người đàn ông ngồi lái → gán 1 `person` (`occluded_level=2`); mô hình chuột trắng → **không gán**; đám đông hai bên rào chắn → gán `ignore_region` cho vùng quá dày/nhỏ, gán `person` cho người tiền cảnh rõ. | **Cần chốt nhóm (Pha 2):** Ranh giới giữa gán từng `person` ở hàng đầu rào chắn và bọc `ignore_region` cho đám đông phía sau. |
| `img_020` | Ảnh chụp vào gương chiếu hậu của ô tô đang chạy: thấy thân xe chủ (ego) và 1 ô tô phía sau phản chiếu trong gương. | `R-04` | **Không gán bất kỳ box nào** (ảnh rỗng `0` annotation). | **Loại theo quy tắc:** Ô tô trong gương là ảnh phản chiếu (reflection), còn khung cửa/gương là ego-vehicle. |
| `img_021` | Đám đông người đi xe máy dừng đèn đỏ dày đặc lúc chập tối; phía xa hàng trăm mũ bảo hiểm/xe dính liền. | `R-02`, `R-06` | Tách riêng `person` và `motorcycle` cho các xe ở tiền cảnh/trung cảnh nhìn rõ; gán `car` cho ô tô bên trái; dùng 1 box `ignore_region` bao trùm biển người/xe quá nhỏ và chồng lấp ở hậu cảnh xa. | **Cần chốt nhóm (Pha 2):** Thống nhất ranh giới từ hàng xe nào ở trung cảnh trở đi thì gộp vào `ignore_region`. |
| `img_022` | Ảnh đen trắng chụp mô tô cổ có gắn thùng xe bên cạnh (sidecar) và 1 người ngồi trong thùng. | `R-02`, `R-03` | Gán 1 box `motorcycle` ôm trọn cả thân mô tô lẫn thùng sidecar gắn liền; gán 1 box `person` (`occluded_level=2`) cho người ngồi trong sidecar. | **Cần chốt nhóm (Pha 2):** Thống nhất mô tô 3 bánh (sidecar) vẽ 1 box `motorcycle` chung cho cả xe và thuyền bên. |
| `img_023` | Xích lô đạp chân ở Huế chạy cùng chiều với xe máy, ngược chiều với ô tô con màu đen. | `R-02` | **Không gán** chiếc xích lô; gán `person` cho người đạp xích lô, người đi bộ và người đi xe máy; gán `car` cho ô tô đen; gán `motorcycle` cho xe máy đang chạy và xe đỗ rõ. | **Loại theo quy tắc:** Xích lô đạp chân không có động cơ nên không thuộc `motorcycle`. |
| `img_024` | Ô tô cổ AMC Pacer màu đen trưng bày trong nhà, trên giá nóc có đặt một khung vỏ xe màu vàng không có động cơ/nội thất. | `R-01`, `R-04` | Gán `car` cho xe đen chính giữa và các ô tô thật đỗ xung quanh; khung vỏ xe màu vàng trên nóc là mô hình/vỏ rỗng trưng bày → **không gán** (hoặc tick `can_review` để chốt nhóm). | **Cần chốt nhóm (Pha 2):** Phân biệt xe thật (`car`) với khung vỏ mô hình đặt trên nóc xe trong `img_024`. |
| `img_025` | Phố đi bộ ven biển có người đi dạo, ghế bố bãi biển phía trái và dòng xe bán tải/xe máy ba gác chạy bên phải. | `R-02`, `R-06` | Gán `person` cho người đi bộ/ngồi đủ lớn (`≥ 20 px`); bọc `ignore_region` cho đám đông nhỏ li ti ở xa; bên phải gán `truck` cho xe bán tải vàng-xanh và bạc, `motorcycle` + `person` cho xe máy kéo thùng. | **Áp dụng theo quy tắc:** Kết hợp ngưỡng chiều cao `20 px` và `ignore_region` ở hậu cảnh xa. |
| `img_026` | Hai người ngồi trên một xe máy chạy trong đường hầm, phía sau là tranh tường vẽ tàu cảng. | `R-01`, `R-02` | Tách thành **3 box riêng**: 1 `person` (nam cầm lái, `occluded_level=1`), 1 `person` (nữ ngồi sau, `occluded_level=0`), 1 `motorcycle` (`occluded_level=1`, `truncated=yes` ở bánh dưới). | **Áp dụng theo quy tắc:** Ca chuẩn cho quy tắc tách từng người ngồi trên cùng 1 xe máy. |
| `img_027` | Đài tưởng niệm/bia mộ bằng đá đen tạc hình chiếc xe bán tải cổ tại nghĩa trang. | `R-04` | **Không gán bất kỳ box nào** (ảnh rỗng `0` annotation). | **Loại theo quy tắc:** Tượng đá mô phỏng hình xe bán tải, không phải phương tiện thật. |
| `img_028` | Xe bán tải thật đỗ ven đường, trên thùng xe chở mô hình con ngựa giả; phía sau có ô tô đỏ đỗ ven đường. | `R-01`, `R-04` | Gán `truck` cho xe bán tải (box chỉ ôm thân xe bán tải, **không** kéo cao lên ôm phần tượng con ngựa trắng); **không gán** tượng ngựa; gán `car` (`occluded_level=1`) cho ô tô đỏ phía sau. | **Loại theo quy tắc (`R-04`):** Tượng ngựa không thuộc taxonomy và không phải cấu trúc thân xe `truck`. |
| `img_029` | Một người đi xe máy và một người đi xe đạp cùng vác chung một bó thanh nhôm rất dài chắn ngang ảnh. | `R-01`, `R-02` | Gán `person` + `motorcycle` cho người và xe máy ở giữa; người đi xe đạp bên trái và bên phải chỉ gán `person` (**không gán xe đạp**); box `person`/`motorcycle` **không** mở rộng theo thanh nhôm dài. | **Cần chốt nhóm (Pha 2):** Vật vác rời/quá khổ (thanh nhôm dài) không gộp vào box `person` hay `motorcycle` để tránh làm lệch IoU nghiêm trọng. |
| `img_030` | Bãi đỗ xe máy dày đặc, có nhân viên mặc áo xanh đứng giữa, phía trên bên trái có biển quảng cáo in hình 4 ca sĩ/diễn viên. | `R-01`, `R-04`, `R-06` | **Không gán** 4 hình người trên biển quảng cáo (`R-04`); gán `person` cho nhân viên áo xanh; gán `motorcycle` cho các xe máy tách biệt được ở tiền cảnh/trung cảnh; dùng `ignore_region` cho dải xe chồng lấp quá dày ở hậu cảnh. | **Loại theo quy tắc + Đám đông:** Tránh lỗi `thua` trên poster quảng cáo và thống nhất vùng `ignore_region` cho bãi xe xa. |
| `img_033` | Ma-nơ-canh nhựa trong tủ kính cửa hàng, chồng bóng phản chiếu của người và xe tải ngoài đường lên mặt kính. | `R-04` | **Không gán bất kỳ box nào** (ảnh rỗng `0` annotation). | **Loại theo quy tắc:** Ma-nơ-canh không phải người thật; hình xe và người trên kính chỉ là bóng phản chiếu. |
| `img_035` | Xe lam 3 bánh (auto-rickshaw) chở các bao tải chất cao gấp đôi nóc xe tại Ấn Độ. | `R-02` | Đề xuất gán `motorcycle` (hoặc theo quyết định nhóm cho xe 3 bánh) và **box bao gồm cả khối bao tải hàng hóa** đang chất trên xe; gán `person` cho tài xế trong xe và người đi mô tô bên phải; gán `car` cho 2 ô tô trắng. | **Cần chốt nhóm (Pha 2):** Box phương tiện chở hàng cồng kềnh (`img_012`, `img_029`, `img_035`) có bao gồm phần hàng hóa nhô ra ngoài khung xe hay chỉ ôm thân xe. |
| `img_037` | Xe bán tải GO Transit lắp nắp thùng kín (truck cap) phía sau. | `R-01` | Gán lớp `truck` (vì bản chất khung gầm là pickup truck có thùng hàng tách biệt ca-bin dù lắp thêm nắp chụp). | **Loại trừ nhầm lẫn lớp:** Tránh nhầm giữa `truck` (pickup có nắp thùng) và `van` / `car` (SUV). |
| `img_038` | Tủ kính trưng bày hàng chục mô hình ô tô đồ chơi, búp bê, vịt cao su. | `R-04` | **Không gán bất kỳ box nào** (ảnh rỗng `0` annotation). | **Loại theo quy tắc:** Toàn bộ là mô hình đồ chơi thu nhỏ. |

---

## 5. QC và phiên bản

### 5.1. Ngưỡng chất lượng (giữ nguyên từ `submission/taxonomy.json`)
- **Chiều cao box tối thiểu (`min_box_height_px`):** `20 px` (vật nhỏ hơn 20 px phải đưa vào `ignore_region`).
- **Ngưỡng IoU đạt chuẩn:**
  - Box lớn (chiều cao `≥ 50 px`): **IoU ≥ 0.85**.
  - Box nhỏ (chiều cao `20 px – 49 px`): **IoU ≥ 0.70**.
- **Ngưỡng đồng thuận liên người gán (IAA):**
  - Ghép cặp 1–1 tại ngưỡng `match_iou >= 0.50`.
  - Yêu cầu **IoU trung bình ≥ 0.85** và **Đồng thuận lớp (Class agreement) ≥ 95%** trên các cặp box ghép được, đồng thời hoàn thành **100% lượt gán** theo `assignment.csv`.
- **Ngưỡng nghiệm thu lô (QC Release):**
  - Duyệt toàn bộ 40 ảnh. Tỷ lệ ảnh có lỗi **`error_rate_img_max` ≤ 2%** (tức là trên 40 ảnh, nếu có **từ 1 ảnh lỗi trở lên = 2.5% > 2%** hoặc có lỗi hệ thống lặp lại thì phải chọn **Rework**, không được Release).

### 5.2. Quy trình xử lý ca mơ hồ & Lịch sử phiên bản
- Khi gán độc lập ở Pha 3: Tuyệt đối tuân thủ `guideline_v1.0_agreed.md`. Nếu gặp đối tượng khó phân định, tick `can_review = true` trên box hoặc ghi nhận vào danh sách để tổng hợp sang `submission/qc/image_issues.csv`.
- Ở Pha 5 (Calibration - nhiệm vụ chính của thành viên `103`): Tổng hợp mọi ca bất đồng từ `calibration_candidates.csv`, họp nhóm chốt quyết định vào `calibration_decisions.csv`, cập nhật `guideline_v1.1_calibrated.md` + `guideline_change.json` và tạo bộ nhãn cuối `labels_calibrated.json`.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| `v0` | Bản khởi đầu của giảng viên. | Chưa có ngưỡng thuộc tính, chưa có quy tắc tách người/xe máy và xử lý tượng/đồ chơi/phản chiếu. |
| `v0.1-103` | Bản guideline cá nhân của thành viên `103`: bổ sung định nghĩa 6 lớp kèm phản ví dụ, định lượng ngưỡng `occluded_level` (0 / 10-50% / 50-80% / >80%), quy tắc `R-01` đến `R-06` và phân tích 15 nhóm ảnh ca khó thực tế. | Chuẩn bị đầu vào thảo luận với 3 thành viên (`101`, `102`, `104`) để thống nhất `v1.0` ở Pha 2. |
