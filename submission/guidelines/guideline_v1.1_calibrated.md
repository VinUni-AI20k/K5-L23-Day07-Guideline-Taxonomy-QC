# Guideline gán nhãn — v1.1 (sau calibration) — nhóm G003

- Phiên bản: v1.1 (kế thừa v1.0, ngày 2026-11-16)
- Ngày: 2026-11-17
- Người viết / duyệt: 343 soạn / cả nhóm G003 duyệt ở họp calibration Pha 5; người điều phối: 069
- Loại nhãn: bounding box trên ảnh đường phố · CVAT, xuất COCO 1.0
- Taxonomy: giữ nguyên `submission/taxonomy.json` **v1.0** (không thêm, bớt lớp hay thuộc tính, không có `taxonomy_v1.1.json`).
- Trạng thái: áp dụng cho Task calibration (Pha 5) và nhãn bàn giao `labels_calibrated.json`. Loại thay đổi: **semantic** (xem mục 5).

> **Thay đổi so với v1.0, đọc trước khi sửa nhãn.** Quy tắc đánh dấu **(sửa v1.1)** đổi cách gán; phải kiểm lại cả lô 40 ảnh.
> - R-05: phép thử `person` / `rider` theo tư thế nhìn thấy, bỏ tiêu chí "ngồi nghỉ trên xe đỗ".
> - R-08: `truncated` xác định hoàn toàn bằng vị trí box so với mép ảnh.
> - R-10: đám đông, dãy xe đỗ: gán mọi vật nhận ra được, kể cả bị che nhiều.
> - R-12 (mới): cách ước lượng `occluded_level`.
> - R-13 (mới), R-14 (mới): phép thử phân lớp xe theo kết cấu nhìn thấy.
> - R-15 (mới): `can_review` phải được chốt và tắt trong nhãn bàn giao.
> - R-04, R-06: chỉ làm rõ câu chữ và cách kiểm, không đổi nghĩa.

---

## 1. Mục tiêu

Huấn luyện mô hình **phát hiện người và phương tiện** trên ảnh đường phố 2D (camera giao thông, xe tự lái),
bối cảnh Việt Nam / Đông Nam Á. Mô hình phải tách được **người đi bộ** (`person`) khỏi **người đang ở trên xe**
(`rider`), vì hai nhóm này di chuyển với tốc độ và hướng khác nhau.

Sai nguy hiểm nhất, theo thứ tự ưu tiên:

1. Bỏ sót người hoặc xe thật, kể cả khi bị che nhiều hoặc đứng trong đám đông.
2. Gán box cho mô hình, tượng, đồ chơi, hình in, ma-nơ-canh, ảnh phản chiếu, khiến mô hình báo vật cản giả.
3. Box hụt phần vật hoặc hàng chở trên xe; box lỏng chứa nhiều nền.

Khi hai cách gán đều có vẻ hợp lý, chọn cách **đo được từ ảnh** (vị trí, tư thế, kết cấu nhìn thấy), không chọn cách phải đoán ý định hay bối cảnh ngoài khung hình.

## 2. Lớp và thuộc tính

### Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `person` | Người thật **không có điểm tựa trên xe**: đi bộ, đứng, ngồi ghế/vỉa hè, gánh hàng, dắt xe, đứng cạnh hoặc dựa vào xe. | Cô gái đi bộ và khách ngồi quán img_001; người gánh hàng và người đứng dắt xe đạp img_003 | Người đang ngồi trên yên/ghế hoặc đứng trên sàn xe hở → `rider` (R-05). Tượng, ma-nơ-canh, búp bê, hình in (img_017, img_033, img_038) → không gán. |
| `rider` | Người thật **ngồi trên yên, ghế, baga hoặc đứng trên sàn / bàn để chân** của `motorcycle`, `bicycle` hoặc `other_vehicle` không có khoang kín; gồm người lái và người ngồi sau; **không phụ thuộc xe đang chạy hay đỗ** (sửa v1.1). | Người đi xe máy giữa ảnh img_003; người đi xe máy nhòe img_014; người đạp xích lô img_023; tài xế tuk-tuk img_004 | Hai chân trên mặt đất và không ngồi trên xe → `person`. Người ngồi trong `car`, `truck`, `van`, xe buýt → không gán. Tượng người cưỡi ngựa img_017 → không gán. |
| `car` | Ô tô thân liền khối, **có capo nhô rõ phía trước**, ≤ 9 chỗ: sedan, hatchback, SUV, MPV. | img_023; ô tô trên giá img_002 | Pickup, kể cả có nắp thùng → `truck`; đầu xe ngắn, nóc hộp → `van` (R-13). |
| `truck` | Xe có **thùng hàng tách khỏi cabin** (thấy khe hoặc ranh giới giữa cabin và thùng): xe tải, pickup (kể cả có nắp/mui thùng cao), đầu kéo (kèm rơ-moóc = 1 box). | img_001 (pickup chở ống), img_002, img_012; pickup nắp thùng cao img_016, img_037 | Tượng pickup img_027 → không gán. |
| `van` | Xe thân liền dạng hộp, **đầu xe ngắn hoặc phẳng, nóc cao**; minibus ≤ 16 chỗ. | | SUV, MPV có capo rõ → `car`. Xe khách > 16 chỗ → `other_vehicle`. |
| `motorcycle` | Xe máy, mô tô, xe máy điện: 2 bánh, có ốp thân hoặc sàn để chân, **không thấy bàn đạp**; tính cả xe có sidecar. | img_029 (xe điện), img_022 (sidecar) | Có bàn đạp và khung hở → `bicycle`. Tuk-tuk, xe lam → `other_vehicle` (R-14). |
| `bicycle` | Xe 2 bánh **thấy bàn đạp và khung hở**, kể cả xe đạp điện có bàn đạp. | img_029 (bên phải), img_003 | Xích lô → `other_vehicle`. |
| `other_vehicle` | Xe thật không thuộc các lớp xe trên: tuk-tuk, xe lam, xích lô, ba gác, xe khách / xe buýt > 16 chỗ. | Tuk-tuk img_004, img_016, img_035; xích lô img_023; xe buýt img_009, img_031, img_037, img_040 | Xe mô hình, đồ chơi → không gán. |

Vật **không thuộc lớp nào** (động vật, xe đẩy tay, cọc tiêu, biển báo, mô hình, tượng, đồ chơi): **không gán**. Không dùng
vùng ignore. Vật thật không gán được (cao < 20 px, không xác định được biên) thì không gán, theo R-07, R-09, R-10.

> Lưu ý kỹ thuật: `ignore_region` vẫn có trong `submission/taxonomy.json` vì script bắt buộc phải có
> (`scripts/common.py` kiểm `ignore_class`), nên nó vẫn hiện trong CVAT. **Không vẽ box lớp này.**

- **R-01 Chỉ gán vật thật; mô hình không gán box.** Mô hình xe hoặc người (kể cả mô hình cỡ thật), tượng, đồ chơi,
  hình in, ma-nơ-canh, ảnh phản chiếu → không gán box nào, dù trông giống hệt người hoặc xe.
  Ví dụ: img_017, img_018, img_027, img_033, img_038.
- **R-02 Xe lạ → `other_vehicle`**, không ép vào lớp gần giống. Trước khi dùng R-02, áp dụng phép thử R-13, R-14.
- **R-03 Xe thật đang đỗ, trưng bày, xe độ** vẫn gán như xe thường, theo kết cấu gốc. Mô hình, điêu khắc hình xe → theo R-01, không gán.
- **R-13 Phép thử lớp xe 4 bánh trở lên (mới v1.1).** Xét theo thứ tự, dừng ở điều kiện đầu tiên đúng:
  1. Xe khách / xe buýt > 16 chỗ (thân dài, nhiều hàng cửa sổ) → `other_vehicle`.
  2. Thấy khe hoặc ranh giới tách cabin với thùng hàng phía sau, kể cả thùng có nắp hoặc mui cao → `truck`.
  3. Thân liền dạng hộp, đầu xe ngắn hoặc phẳng, nóc cao → `van`.
  4. Thân liền, có capo nhô rõ phía trước → `car`.
- **R-14 Phép thử xe 2–3 bánh (mới v1.1).**
  - Xe 3 bánh có thùng, ghế khách hoặc mái (tuk-tuk, xe lam, ba gác máy, xích lô) → **1 box `other_vehicle` cho cả xe**, bao luôn phần đầu giống xe máy; không vẽ thêm box `motorcycle`. Người ngồi trên xe → `rider` (R-05).
  - Xe 2 bánh thấy bàn đạp và khung hở → `bicycle`; không thấy bàn đạp, có ốp thân hoặc sàn để chân → `motorcycle`.
- Không chắc lớp sau khi đã áp dụng R-13, R-14 → chọn lớp gần nhất và tick `can_review` (R-15).

### Thuộc tính

| Thuộc tính | Giá trị | Ý nghĩa |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Phần trăm **toàn bộ vật** bị vật khác che: 0 là < 10%, 1 là 10–39%, 2 là 40–69%, 3 là ≥ 70% (vẫn nhận ra lớp). Cách ước lượng: R-12. |
| `truncated` | `no`, `yes` | `yes` khi **ít nhất một cạnh box cách mép ảnh ≤ 2 px**; ngược lại `no` (sửa v1.1, R-08). |
| `can_review` | tick / không | Cờ tạm khi gán: không chắc lớp, không chắc biên box, hoặc ca chưa có trong guideline. Nhãn bàn giao phải tắt hết (R-15). |

- **R-12 Cách ước lượng `occluded_level` (mới v1.1).**
  1. Hình dung khung của **toàn bộ vật**, kể cả phần bị che. Không ước lượng trên box đã vẽ, vì box chỉ ôm phần nhìn thấy (R-04) nên gần như luôn ra mức 0.
  2. Tính phần diện tích bị **bất kỳ vật nào đứng trước** che: xe khác, người khác, cột, cây, biển, hàng hóa, kể cả vật không thuộc lớp nào.
  3. Không tính: `rider` và chiếc xe họ đang ở trên che nhau; kính trong suốt; vùng nhòe; phần nằm ngoài khung ảnh (thuộc `truncated`).
  4. Mốc nhanh: 0 = không bị che hoặc chỉ khuất một góc nhỏ; 1 = khuất dưới khoảng 2/5; 2 = khuất từ khoảng 2/5 đến dưới 7/10; 3 = chỉ còn thấy ≤ 3/10 vật.
  5. Phân vân giữa hai mức → chọn mức cao hơn.

## 3. Quy tắc vẽ box

1. **R-04** Box ôm sát phần nhìn thấy (lệch ≤ 2 px), không đoán phần bị che. Bao cả gương, biển TAXI, giá nóc; bỏ ăng-ten, bóng đổ.
   - Cách kiểm (làm rõ v1.1): phóng to ≥ 100% khi chỉnh cạnh; mỗi cạnh trong 4 cạnh phải chạm điểm ảnh ngoài cùng của phần nhìn thấy; không chừa dải nền. Box `person` / `rider` gồm cả tóc, mũ và bàn chân nhìn thấy.
   - Ở Pha 4, khi lệch `iou_thap`, box của một người to hơn box của người còn lại theo trung vị 1.34 lần diện tích. Box lỏng là lỗi `sai_vi_tri_kich_thuoc` khi QC.
2. **R-05 Người và xe hở (sửa v1.1).** Mỗi người trên xe hở 1 box `rider` + 1 box cho xe (xe máy chở 2 người = 2 `rider` + 1 `motorcycle` = 3 box).
   - Phép thử chỉ dựa trên **tư thế nhìn thấy**:
     - `rider`: người **ngồi trên yên, ghế, baga, thùng** của xe hở, hoặc **hai chân đứng trên sàn / bàn để chân** của xe. Áp dụng **dù xe đang chạy, dừng đèn đỏ hay đỗ bên đường**, chân chống đất hay không.
     - `person`: người **không ngồi trên xe và không đứng trên xe**: dắt xe, đứng cạnh, dựa vào xe, một chân đặt lên xe nhưng chưa ngồi.
   - Bỏ tiêu chí v1.0 "ngồi trên xe đỗ để nghỉ → `person`", vì không xác định được ý định từ ảnh và mâu thuẫn với "xe dừng, chân chống đất → `rider`".
   - Không thấy phần hông vì bị che, nhưng thân người nằm ngay trên yên xe → `rider`.
   - Box `rider` gồm mũ, ba lô và phần chân trên xe; không gồm đồ cầm tay, gánh. Box `rider` và box xe chồng lên nhau là bình thường.
   - Người ngồi trong `car`, `truck`, `van`, xe buýt: không gán.
3. **R-06** Hàng đặt, buộc lên xe → bao vào box xe, **kể cả hàng chất cao quá nóc hoặc tràn ra ngoài thân xe** (làm rõ v1.1, ví dụ bao tải trên tuk-tuk img_035). Hàng người cầm, vác → không bao. Xe được chở trên xe khác: box xe chở bao cả các xe đang chở, **và** mỗi xe được chở nhìn thấy ≥ 20 px vẫn có box riêng (img_002).
4. **R-07** Vật nhòe, tối: gán nếu nhận ra lớp và thấy biên, tick `can_review`. Không tách được biên → không gán; ghi ảnh, vùng và lý do để nhóm đưa vào `submission/qc/image_issues.csv`.
5. **R-08 Vật bị cắt mép ảnh (sửa v1.1).** Box dừng ở mép. `truncated=yes` khi và chỉ khi có cạnh box cách mép ảnh ≤ 2 px; không xét thêm "vật còn phần ngoài khung hay không".
6. **R-09** Vật có box cao < 20 px → không gán, kể cả khi nhiều vật nhỏ nằm sát nhau.
7. **R-10 Đám đông, dãy xe đỗ, hậu cảnh (sửa v1.1).** Gán **riêng từng vật thật** khi đủ cả ba điều kiện:
   - nhận ra lớp nhờ ít nhất một bộ phận đặc trưng: đầu hoặc vai người; bánh hoặc cụm yên–tay lái của xe 2 bánh; đèn, bánh hoặc cửa kính của ô tô;
   - xác định được biên trái, phải, trên, dưới của phần nhìn thấy;
   - phần nhìn thấy cao ≥ 20 px.

   Áp dụng cả khi vật bị che ≥ 70% (`occluded_level=3`), là xe đang đỗ trong dãy, hoặc là người ở xa / trong quán / sau người khác. Chỉ bỏ khi không xác định được biên. Lý do: bỏ sót là sai nguy hiểm nhất (mục 1).
8. **R-11** Xe chủ (capo, taplo, gương) và ảnh phản chiếu (kính, gương, vũng nước): không gán.
9. **R-15 Chốt `can_review` (mới v1.1).** `can_review` chỉ là cờ tạm khi gán độc lập. Trong Task calibration, mỗi box có cờ phải được chốt lại theo R-01 → R-14, sửa lớp/box nếu cần rồi **tắt cờ**. Nhãn bàn giao không còn box nào `can_review=true`. Không chốt được → ghi vào `calibration_decisions.csv`, người điều phối (069) quyết.

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_038 | Tủ kính trưng bày: hai kệ dưới là ô tô đồ chơi; kệ trên có vịt cao su, tượng chuột, búp bê, xe ba bánh đồ chơi có hình nhân; mặt kính phản chiếu đường phố. | R-01, R-11 | Không gán box nào (kể cả búp bê, xe đồ chơi, hình phản chiếu). Ảnh vẫn có trong COCO với 0 box. | Toàn bộ là đồ chơi và phản chiếu, không có vật cản thật. Đây là ảnh đối chứng âm: mọi box trên ảnh đều tính lỗi `thua`. |
| img_017 | Tượng đồng người cưỡi ngựa, đội nón giao thông, có chim đậu trên lưng ngựa. | R-01 | Không gán: không `rider`/`person` cho tượng người, không gán ngựa và chim. | Tượng không phải người thật. Pha 4 vẫn có 1/3 người gán `person` lên tượng → giữ nguyên R-01, xóa box khi calibration. |
| img_027 | Bia mộ bằng đá đen tạc hình xe pickup cỡ gần như thật, đặt trên bệ trong nghĩa trang. | R-01, R-03 | Không gán, không tick `can_review`. | Có bệ đá, không có cửa kính thật → điêu khắc, không phải xe đỗ. Giữ làm mẫu âm cho lớp `truck`. |
| img_033 | Cửa kính cửa hàng: ma-nơ-canh trắng, ảnh in người mẫu, mặt kính phản chiếu thân xe trắng. | R-01, R-11 | Không gán box nào. | Không có người hay xe thật trong khung hình; xe chỉ thấy qua phản chiếu. |
| img_016, img_037 | Pickup gắn nắp / mui thùng cao. | R-13 | `truck`. | Pha 4 lệch 4 kiểu lớp (`car` / `truck` / `van` / `other_vehicle`): img_016 có 7 ca `sai_lop`, img_037 có 5 ca. Kết cấu gốc vẫn là cabin tách thùng. |
| img_009, img_031, img_037, img_040 | Xe buýt / xe khách cỡ lớn. | R-13 | `other_vehicle`. | Riêng img_040 có 4 ca `car` ↔ `other_vehicle`. Xe > 16 chỗ không thuộc `van`. |
| img_004, img_016, img_035 | Tuk-tuk 3 bánh, phần đầu giống xe máy. | R-14, R-05 | 1 box `other_vehicle` cho cả xe; tài xế và khách ngồi trên xe → `rider`. | img_004 lệch `motorcycle` ↔ `other_vehicle` và `car` ↔ `other_vehicle`. Tách đầu xe thành `motorcycle` làm đếm trùng phương tiện. |
| img_035 | Bao tải chất cao trên nóc tuk-tuk. | R-06 | Box `other_vehicle` bao cả khối hàng. | Hụt hàng chở là sai nguy hiểm (mục 1); thống nhất một cách vẽ để hết ca `iou_thap`. |
| img_003, img_021, img_008, img_029, img_010 | Người ở trên hoặc sát xe hai bánh: đang dừng, đỗ, dắt xe. | R-05 | Theo phép thử tư thế: ngồi / đứng trên xe → `rider`; không có điểm tựa trên xe → `person`. | 43/83 ca `sai_lop` ở Pha 4 là `person` ↔ `rider`, tập trung ở 5 ảnh này (28 ca). Tiêu chí "ý định ngồi nghỉ" của v1.0 không đo được. |
| img_003, img_006, img_032, img_008, img_039 | Đám đông, dãy xe máy đỗ, người ở hậu cảnh. | R-10, R-12 | Gán từng vật đạt đủ 3 điều kiện của R-10, kể cả bị che nhiều. | 5 ảnh này chiếm 202/508 ca `bo_sot_thua`; 370/508 box chưa ghép cao ≥ 50 px, nên nguyên nhân không phải quy tắc vật nhỏ (R-09) mà là bỏ qua vật bị che. |

Ca chưa chốt: tick `can_review` trên box, hoặc ghi ảnh, vùng, lý do nếu chưa vẽ được box, rồi đưa ra họp. Dẫn mã R-xx trong `calibration_decisions.csv` và `qc_review.csv`.

## 5. QC và phiên bản

- Ngưỡng (giữ nguyên `rules` trong `taxonomy.json`): ghép cặp IoU ≥ 0.5; IoU đạt ≥ 0.85 (box cao ≥ 50 px) hoặc ≥ 0.7 (nhỏ hơn); IAA cùng lớp ≥ 95%; lỗi theo ảnh ≤ 2%; box cao tối thiểu 20 px.
- Ca mơ hồ: người gán tick `can_review`; nhóm chốt ở Pha 2 và Pha 5; người điều phối (069) quyết khi không thống nhất.
- Mọi thay đổi làm đổi nhãn đều tăng phiên bản. Thêm hoặc bỏ lớp thì cập nhật taxonomy (tăng version) và chạy lại `scripts/make_cvat_labels.py`.
- v1.1 là thay đổi **semantic** (`submission/guideline_change.json`): R-05, R-08, R-10, R-12, R-13, R-14, R-15 đổi cách gán → `pham_vi = lo`, kiểm lại cả 40 ảnh trong Task calibration, xuất phát từ `consensus_draft.json`.

Bảng tra dùng khi điền `calibration_decisions.csv` (loại ca do `qc_compare.py` sinh ở Pha 4):

| Loại ca Pha 4 | Số ca | Quy tắc v1.1 chính | Phạm vi |
|---|---|---|---|
| `sai_lop` `person` ↔ `rider` (và 2 ca `motorcycle` ↔ `rider`/`person` do ghép box) | 45 | R-05 | `lo` |
| `sai_lop` giữa các lớp xe | 38 | R-13, R-14 | `lo` |
| `bo_sot_thua` | 508 | R-10 (vật bị che, đám đông); R-01 (vật không thật); R-09 (box < 20 px) | `lo` |
| `iou_thap` | 309 | R-04 (box ôm sát); R-06 (hàng chở) | `anh` |
| `sai_thuoc_tinh` `occluded_level` | 198 | R-12 | `lo` |
| `sai_thuoc_tinh` `truncated` | 102 | R-08 | `lo` |
| `co_can_review` | 90 | R-15 + quy tắc của lớp liên quan | `lo` |

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu. | — |
| v1.0 | Thêm lớp `bicycle`, `other_vehicle`, `rider` (`person` chỉ còn người không ở trên xe, R-05); bỏ `ignore_region` (vật < 20 px, cụm không tách được, vùng nhòe → không gán, R-07, R-09, R-10); mô hình, tượng, đồ chơi, phản chiếu không gán box (R-01, R-11); giữ `can_review`; ngưỡng đo được cho thuộc tính; chốt 4 ca khó. | Bản cá nhân lệch nhau về người trên xe: 343 gộp vào `person`, 042 dùng thuộc tính `role`, 069 tách `Driver`/`Person`. Chọn **lớp** vì mô hình phải tự đoán khi suy luận; gộp cả người ngồi sau vì nhìn ảnh khó biết ai lái (img_003, img_014, img_023, img_004). Xe lạ: img_004, img_023, img_035. Vật không thật: img_038, img_017, img_027, img_033. `ignore_region` vẫn nằm trong `taxonomy.json` do script bắt buộc nhưng không vẽ. |
| v1.1 | **Semantic.** Sửa R-05 (phép thử `person`/`rider` theo tư thế, áp dụng cả xe đỗ), R-08 (`truncated` theo vị trí box ≤ 2 px từ mép), R-10 (gán mọi vật nhận ra được trong đám đông / dãy xe đỗ, kể cả bị che ≥ 70%). Thêm R-12 (ước lượng che trên toàn bộ vật), R-13 (thứ tự phép thử `other_vehicle` / `truck` / `van` / `car`; pickup có nắp thùng → `truck`; xe buýt → `other_vehicle`), R-14 (xe 3 bánh = 1 box `other_vehicle`; bàn đạp → `bicycle`), R-15 (chốt và tắt `can_review`). Làm rõ câu chữ R-04, R-06. Taxonomy giữ v1.0. | IAA trước calibration (`iaa_summary.md`, 120/120 lượt gán, mẫu số 777 cặp box ghép): IoU TB 0.844 < 0.85, cùng lớp 89.3% < 95% → chưa đạt. 1261 ca trên 36 ảnh: `bo_sot_thua` 508, `iou_thap` 309, `sai_thuoc_tinh` 271 (`occluded_level` 198, trong đó 87 ca lệch ≥ 2 mức; `truncated` 102), `co_can_review` 90, `sai_lop` 83 (43 ca `person`/`rider`; 38 ca giữa các lớp xe, nhiều nhất ở img_016, img_037, img_040, img_004, img_035, img_028, img_031). |
