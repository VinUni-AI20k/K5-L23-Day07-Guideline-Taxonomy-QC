# Guideline gán nhãn — v0-cá-nhân — 154

- Phiên bản: v0-cá-nhân (bản độc lập, chưa họp nhóm)
- Người viết: `154`
- Phạm vi ví dụ: img_021 → img_040 (ảnh 001–020 do thành viên khác xem; phần quy tắc chung vẫn áp dụng cho cả 40 ảnh)
- Nguyên tắc nền: **mô hình chỉ nên học thứ nó nhìn thấy được trên ảnh 2D**. Điều gì phải đoán (phần bị che, vật ngoài khung, vật thật hay giả khi không đủ dấu hiệu) thì không đưa vào nhãn, mà tick `can_review`.

## 1. Mục tiêu

Nhãn dùng huấn luyện mô hình phát hiện **người và phương tiện** trên ảnh đường phố (camera giao thông, xe tự lái). Sai nguy hiểm nhất ở hai chỗ:

- **Bỏ sót người** (đặc biệt người đi bộ, người ngồi xe máy): hậu quả an toàn lớn nhất.
- **Báo nhầm vật giả là vật thật** (tượng, ma-nơ-canh, đồ chơi, hình in, phản chiếu): mô hình sinh cảnh báo giả, phanh nhầm.

Vì vậy guideline này ưu tiên: người và xe thật thì gán đủ; vật giả thì **không gán** để mô hình học đó là nền.

## 2. Lớp và thuộc tính

### Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Xe ô tô chở người, thân liền, kể cả SUV, taxi, sedan, hatchback. | img_034 (sedan đen), img_031 (SUV trắng, sedan), img_040 (taxi xanh đỏ, SUV đen) | Xe bán tải có thùng hở → `truck`. Xe giả/mô hình → không gán. |
| `truck` | Xe có thùng hàng riêng phía sau cabin: xe tải, bán tải (pickup), xe thùng bạt. | img_036 (xe tải nhỏ xanh), img_037 (bán tải trắng có mui), img_028 (bán tải nâu) | Xe tải nhưng thùng kín nhỏ như xe van → `van`. Tượng pickup đá granite (img_027) → không gán. |
| `van` | Xe thùng kín liền khối, cabin và thùng không tách (cỡ nhỏ đến vừa). | img_033 (cạnh xe trắng có gương, chưa chắc, xem R-14) | Pickup có mui trùm thùng như img_037 vẫn là `truck` vì cabin và thùng tách rõ. |
| `motorcycle` | Xe hai bánh có động cơ: xe máy, xe ga, mô tô; xe mô tô có thùng phụ (sidecar) tính **một** vật. | img_021, img_026, img_029 (xe ga), img_022 (mô tô + sidecar) | Xe đạp → không thuộc lớp (R-07). Xe ba bánh (tuk-tuk) → không phải `motorcycle`. |
| `person` | Người thật nhìn thấy trên ảnh: đi bộ, đứng, ngồi, ngồi trên xe, đạp xe. | img_034 (người đi bộ), img_032 (đám người chờ xe buýt), img_026 (2 người trên xe) | Ma-nơ-canh, tượng, người trong hình in/áp phích, hình phản chiếu → không gán (R-06). |
| `ignore_region` | Vùng/vật **có thật** nhưng không có lớp hoặc không tách được từng vật; bỏ sót ở đây không tính lỗi. | xe buýt (img_031, img_037, img_040), tuk-tuk (img_035), cyclo (img_023), bãi xe dày (img_030) | Không dùng cho vật giả (vật giả thì không vẽ gì). |

**Vật không thuộc lớp nào:**

1. Vật thật nhưng không có lớp (xe buýt, tuk-tuk, cyclo, xe đạp, xe kéo): vẽ `ignore_region` ôm vật đó (R-07).
2. Vật giả (tượng, mô hình, đồ chơi, ma-nơ-canh, hình in, phản chiếu): **không vẽ gì** (R-06).
3. Đề xuất cho họp nhóm: nếu nhóm thấy xe ba bánh/xe buýt xuất hiện nhiều thì thêm lớp mới (ví dụ `bus`, `three_wheeler`); bản cá nhân chưa tự thêm vì taxonomy v0 cố định.

### Thuộc tính

**`occluded_level`** — tính theo **tỉ lệ diện tích vật bị che so với toàn bộ vật khi giả định thấy đủ**. Rider ngồi trên xe, bánh xe nằm trên mặt đường **không** tính là che.

| Mức | Nghĩa | Ngưỡng |
|---|---|---|
| `0` | Thấy rõ | che < 10% |
| `1` | Che ít | 10% – 40% |
| `2` | Che nhiều | > 40% – 75% |
| `3` | Che gần hết, chỉ còn vài chi tiết nhận ra | > 75% (vẫn gán nếu nhận ra được lớp; nếu không thì R-10) |

**`truncated`** — `yes` khi **có bất kỳ phần nào của vật nằm ngoài mép ảnh** (≥ khoảng 5% vật); ngược lại `no`. Chỉ xét mép ảnh, không xét bị vật khác che (đó là `occluded_level`).

**`can_review`** — tick khi: lớp mơ hồ, không chắc vật thật hay giả, phần nhìn thấy < 15% vật, hoặc quy tắc chưa đủ để quyết. Không tick bừa: ca đã có quy tắc rõ thì quyết luôn.

## 3. Quy tắc vẽ box

**R-01. Box ôm sát phần nhìn thấy.** Không vẽ cả phần bị che mà bạn đoán ra (không amodal). Cạnh box chạm điểm ngoài cùng của phần thấy được. Mục tiêu IoU ≥ 0.85 với vật cao ≥ 50 px, ≥ 0.7 với vật nhỏ hơn (theo `rules` trong taxonomy).

**R-02. Vật nhỏ.** Vật có chiều cao box **< 20 px** thì **không gán** (không `ignore_region`). Ví dụ các xe máy xa cuối đường ở img_034, img_039.

**R-03. Người trên xe máy: 2 loại box riêng, chồng nhau được.**
- Mỗi người (kể cả người ngồi sau, trẻ em) là **một box `person`**, bao từ đầu tới phần thân/chân nhìn thấy.
- Xe là **một box `motorcycle`** bao thân xe và hai bánh, **không** cố bao phần thân trên của người.
- Hai box được phép chồng lên nhau. Người ngồi trên xe **không** tính là bị che bởi xe (`occluded_level` chỉ tăng khi có vật khác chắn).
- Ví dụ: img_026 → 2 `person` + 1 `motorcycle`; img_022 → `person` nhỏ trong sidecar + 1 `motorcycle` (bao cả sidecar).

**R-04. Cắt mép ảnh.** Vẽ box tới sát mép ảnh, `truncated=yes`. Ví dụ img_034 (người ngồi xe máy ở mép phải), img_032 (xe xanh mép trái), img_026 (bánh xe máy bị cắt đáy).

**R-05. Đám đông và bãi xe dày.**
- Vật nào **tách được** từ ranh giới thấy rõ và còn thấy ≥ 30% thì gán riêng.
- Phần còn lại dính vào nhau không tách nổi → một `ignore_region` ôm cả cụm.
- Ví dụ: img_032 (~30 người chờ xe buýt, gán từng người ở hàng trước, cụm dính ở giữa thì `ignore_region`); img_021 (rừng xe máy: gán các xe và người ở hàng đầu, hàng sau thành `ignore_region`); img_030 (bãi xe: xe nổi bật phía trước gán, phần chồng chất phía sau `ignore_region`).

**R-06. Vật giả: không vẽ gì.** Tượng, đồ chơi, mô hình thu nhỏ, ma-nơ-canh, người/xe trong hình in hay áp phích, phản chiếu trên kính hoặc mặt đường ướt. Đây là mẫu âm (nền).
- Nếu vật giả nằm trên/trong vật thật (ngựa tượng trên xe, xe vàng mô hình trên nóc), box vật thật vẫn ôm cả cụm và **không** thêm box cho vật giả.

**R-07. Vật thật không có lớp → `ignore_region`.** Xe buýt, tuk-tuk, cyclo, xe đạp, xe ba gác. Người điều khiển/ngồi trên xe vẫn gán `person` riêng (xem R-08).

**R-08. Người trong xe.**
- Người ngồi trên xe hở (xe máy, xe đạp, cyclo, tuk-tuk hở) thì gán `person`.
- Người ngồi trong cabin kín, nhìn qua kính chắn (ô tô, cabin xe tải) thì **không gán**.

**R-09. Phần nhô ra của hàng hóa.** Hàng nhô ngoài thân xe (ống dài, bao hàng chồng cao) **không** mở rộng box: box ôm thân xe/người. Ngoại lệ: hàng chất bên trong thùng/bám sát thân xe thì thuộc box xe. Ví dụ img_029 (ống dài trên vai và xe: box không kéo dài theo ống), img_035 (bao hàng chất cao trên tuk-tuk: nằm trong `ignore_region` của xe).

**R-10. Quá mờ, quá che.** Nhận ra được lớp thì gán (`occluded_level=3`). Không nhận ra được là vật gì thì không gán, ghi vào `image_issues.csv`.

**R-11. Xe chủ (ego).** Phần capô, kính trước, gương của xe chụp ảnh nếu thấy ở mép dưới/khung → không gán.

**R-12. Phản chiếu.** Xe, người phản chiếu trên mặt đường ướt hoặc kính (img_031, img_033) là R-06, không gán. Chỉ gán khi chính vật thật đứng đó.

**R-13. Xe đậu trong nhà (bảo tàng, showroom).** Xe thật trưng bày vẫn là `car` nếu thấy rõ ≥ 30% và cao ≥ 20 px. Ví dụ img_024: Pacer đen, xe cam, xe kem gán `car`; xe nhỏ xa dưới ngưỡng bỏ qua theo R-02.

**R-14. Xe bị cắt chỉ còn một góc.** Chỉ còn gương, tay nắm hoặc mảnh nhỏ: nếu < 15% thân thì **không** vẽ box, tick `can_review` ở nơi gần nhất hoặc ghi vấn đề cấp ảnh. Chi tiết img_033: cạnh xe trắng + gương chiếm khoảng một phần ba khung → gán `van`, `truncated=yes`, `can_review`.

**R-15. Ảnh không có vật hợp lệ.** Vẫn nộp ảnh đó trong COCO với 0 box (ví dụ img_038).

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_021 | Rừng xe máy giờ cao điểm, nhiều người đội mũ bảo hiểm | R-03, R-05 | Gán xe và người ở hàng đầu; hàng sau dính nhau → `ignore_region` | Tách được thì gán, không thì ignore |
| img_022 | Mô tô có sidecar, ảnh đen trắng, người ngồi sidecar nhỏ | R-03 | 1 `motorcycle` ôm cả sidecar + 1 `person` nếu cao ≥ 20 px; `can_review` cho box người | Sidecar là một phần xe |
| img_023 | Cyclo đạp, người đạp ở trên; ô tô; xe máy xa; người ngồi mép phải | R-07, R-03 | Cyclo → `ignore_region`; người đạp → `person`; sedan → `car`; xe máy xa + người → gán nếu ≥ 20 px | Cyclo không phải xe máy |
| img_024 | Xe vàng (mô hình/xe trình diễn) đặt trên nóc Pacer đen; nhiều xe cổ phía sau | R-06, R-13 | Không box cho xe vàng; Pacer đen `car`; các xe nền gán theo R-13 | Xe vàng không phải xe đang lưu thông, dễ gây nhầm lớp |
| img_025 | Đường dạo bờ biển, người xa ngồi ghế, một xe máy kéo thùng hàng | R-02, R-03 | Người đi bộ và người ngồi ghế gán nếu ≥ 20 px; xe máy kéo thùng → `motorcycle` + `person` | Thùng kéo không phải lớp riêng, tạm không box |
| img_026 | 2 người trên 1 xe ga ban đêm trước áp phích tàu biển | R-03, R-04, R-06 | 2 `person` + 1 `motorcycle` (`truncated=yes`) ; áp phích không gán | Hình in là R-06 |
| img_027 | Xe tải pickup bằng đá granite trên mộ | R-06 | Không gán | Tượng đài, không phải xe |
| img_028 | Bán tải thật chở **tượng ngựa**; SUV đỏ phía sau | R-06, R-09 | Bán tải → `truck` (box ôm cả thân xe, ngựa không có box riêng); SUV đỏ → `car` | Ngựa là tượng |
| img_029 | Người chở ống dài trên xe ga, người dắt xe đạp bên phải | R-09, R-07 | Xe ga → `motorcycle`; 2 `person`; xe đạp → `ignore_region`; box không kéo theo ống | Hàng nhô không thuộc box |
| img_030 | Bãi xe máy đông, bảo vệ đứng giữa | R-05, R-03 | Bảo vệ → `person`; xe nổi ở trước → `motorcycle`, phần còn lại `ignore_region` | Chồng chéo, tách không nổi |
| img_031 | Đường đêm mưa: xe, xe buýt, người đi bộ, phản chiếu đèn trên đường | R-12, R-07 | Xe → `car`; xe máy → `motorcycle`+`person`; xe buýt → `ignore_region`; phản chiếu → không gán | Đây là ca có phản chiếu |
| img_032 | ~30 người đứng chờ xe buýt, xe xanh bị cắt mép trái, nón cảnh báo | R-05, R-04 | Người hàng trước gán riêng; cụm dính → `ignore_region`; xe xanh `car`, `truncated=yes`; nón không gán | Đám đông |
| img_033 | Ma-nơ-canh, hình in phụ nữ phản chiếu, mảnh xe trắng có gương | R-06, R-14 | Ma-nơ-canh, hình in: không gán; xe trắng: `van`, `truncated=yes`, `can_review` | Cần reviewer chốt có phải xe thật |
| img_034 | Người đi bộ ngang đường; sedan đen; xe máy xa; người ngồi xe máy mép phải | R-02, R-04 | Người đi bộ `person`; sedan `car`; xe máy mép phải: `person`+`motorcycle`, `truncated=yes`; xe máy xa nhỏ hơn 20 px không gán | Ngưỡng 20 px |
| img_035 | Tuk-tuk chất hàng cao, xe máy và người chạy trước, sedan trắng nhỏ | R-07, R-09, R-03 | Tuk-tuk → `ignore_region` (cả bao hàng); xe máy → `motorcycle` + `person`; xe trắng `car` | Tuk-tuk không có lớp |
| img_036 | Xe tải nhỏ xanh có mui bạt; dãy xe máy đỗ phía sau | R-05, R-11 | Xe tải → `truck`; xe máy đỗ nổi → `motorcycle`; dãy dính → `ignore_region` | Pickup có thùng hàng |
| img_037 | Xe bán tải trắng có mui, hai xe buýt, người đi bộ | R-07 | Bán tải → `truck`; buýt → `ignore_region`; người → `person` | Bán tải thuộc truck |
| img_038 | Tủ kính đồ chơi, xe mô hình, vịt cao su | R-06, R-15 | Không gán gì, giữ ảnh trong COCO với 0 box | Toàn vật giả |
| img_039 | Phố Huế, xe máy đỗ, người đi bộ, người đạp xe, cyclo mép phải | R-02, R-07 | Gán người ≥ 20 px, xe ≥ 20 px; xe đạp/cyclo → `ignore_region` | Nhiều vật xa nhỏ |
| img_040 | Cận cảnh người đội mũ bảo hiểm, taxi xanh đỏ bị che, tuk-tuk, xe buýt | R-03, R-14, R-07 | Người → `person` (`truncated=yes`); taxi → `car`, `occluded_level=1`; xe máy chỉ thấy gương → không box + `can_review`; tuk-tuk, buýt → `ignore_region` | Một phần xe bị che |

**Cần hỏi reviewer (chưa tự quyết được):** img_022 (người trong sidecar quá nhỏ), img_025 (xe máy kéo thùng), img_033 (mảnh xe trắng thật hay phản chiếu), img_040 (xe máy chỉ thấy gương).
**Loại theo quy tắc (không cần hỏi):** img_027, img_038 (vật giả), phản chiếu img_031, ma-nơ-canh img_033, xe vàng img_024.

## 5. QC và phiên bản

- Ngưỡng QC: lấy từ `taxonomy.json` mục `rules` (IoU ≥ 0.85 vật lớn, ≥ 0.7 vật nhỏ, đồng thuận lớp ≥ 0.95, lỗi theo ảnh ≤ 2%). Không sửa.
- Người quyết ca mơ hồ: ban đầu `can_review`; ở họp nhóm thì người điều phối (`164`) chốt.
- Mọi thay đổi làm đổi nhãn thì tăng phiên bản và ghi mã quy tắc.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0-cá-nhân | Thêm R-01 → R-15, ngưỡng cho `occluded_level`, `truncated`; 20 ca khó từ img_021–img_040 | Guideline v0 chưa có quy tắc cho xe máy-người, vật giả, tuk-tuk, đám đông |
