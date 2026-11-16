# Guideline gán nhãn — v0.1 (bản cá nhân) — 101

- Phiên bản: v0.1-101 (bản cá nhân)
- Phạm vi: bounding box 2D cho ảnh đường phố (bộ lab 40 ảnh `img_001` … `img_040`), CVAT → COCO 1.0
- Người viết: 101

Guideline viết **tổng quát theo loại tình huống**, không theo từng ảnh. Mục 4 liệt kê một số ảnh khó làm ví dụ.

---

## 0. Tra nhanh khi gán

| Thấy gì | Làm gì | Quy tắc |
|---|---|---|
| Ô tô con, SUV, MPV, hatchback, wagon, taxi | box `car` | R-05 |
| Xe thùng kín liền khối, cửa trượt, cỡ nhỏ (kiểu Hiace, Transit) | box `van` | R-05 |
| Pickup (có hoặc không nắp thùng), xe tải, xe thùng, đầu kéo | box `truck` | R-05 |
| Xe máy, tay ga, mô tô (kể cả có thùng bên) | box `motorcycle`, chỉ phần xe | R-02 |
| Người đi bộ, người ngồi trên xe hở | box `person` riêng cho từng người | R-03 |
| Người ngồi kín trong cabin | không box | R-04 |
| Xe thật ngoài 5 lớp (xe buýt, ba bánh, xích lô, xe đạp…) | box `ignore_region` | R-06 |
| Vật không thật (tượng, ma-nơ-canh, đồ chơi, hình in, phản chiếu) | không box, không ignore | R-07 |
| Xe thật nhưng kiểu lạ (xe diễu hành, xe độ) | gán theo lớp tương đương | R-08 |
| Xe/vật được chở trên xe khác | không box riêng | R-09 |
| Vật cao < 20 px, cụm dày không tách được | `ignore_region` | R-12, R-13 |
| Chưa chắc | tick `can_review` | R-17 |

---

## 1. Mục tiêu

Nhãn dùng để huấn luyện và đánh giá mô hình **phát hiện người và phương tiện trên ảnh 2D đường phố** (camera giao thông, hỗ trợ lái), đặc biệt trong bối cảnh nhiều xe máy, xe ba bánh, đường đông và ban đêm.

Sai ở đâu thì nguy hiểm:

- **Bỏ sót người hoặc xe thật**: mô hình không thấy vật cản. Nguy hiểm nhất.
- **Gán box cho vật giả** (tượng, ma-nơ-canh, hình in, phản chiếu): mô hình báo động giả.
- **Cùng một tình huống mỗi người gán một kiểu** (xe máy lúc gộp người, lúc tách): IAA thấp, mô hình học tín hiệu nhiễu.

Ba nguyên tắc để quyết ca chưa có quy tắc:

1. **"Mô hình có phải đoán ra điều này không?"** Điều không nhìn thấy trong ảnh (phần bị che hoàn toàn, người sau kính tối) thì không gán.
2. **Gán cái nhìn thấy, đo được, lặp lại được.** Hai người độc lập phải ra cùng kết quả; tránh quy tắc dựa vào cảm giác.
3. **Vật thật mà ngoài phạm vi thì `ignore_region`; vật không thật thì không đánh dấu gì.** Vùng ignore báo "ở đây có vật thật nhưng không dạy mô hình", nên mô hình không bị phạt khi phát hiện nó. Vật giả thì mô hình phải học là *không phải* người hay xe.

---

## 2. Lớp và thuộc tính

### 2.1 Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa (một câu) | Ví dụ | Dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô chở người bốn bánh, thân kín, gầm thấp: sedan, hatchback, SUV, MPV, wagon, taxi, xe thể thao. | Sedan, SUV, taxi. | Van → `van`; pickup → `truck`; xe buýt → ngoài lớp. |
| `van` | Xe thùng kín thân cao liền khối, thường có cửa trượt, chở người hoặc hàng nhẹ, cỡ ≤ ~15 chỗ. | Hiace, Transit, xe khách nhỏ thùng kín. | SUV/MPV thân thấp → `car`; xe buýt dài → ngoài lớp. |
| `truck` | Xe có thùng hàng tách riêng hoặc xe thương mại chở hàng: pickup, xe tải nhỏ có bạt, xe thùng, đầu kéo. | Pickup, xe tải có bạt, xe chở xe. | Van thùng liền cabin → `van`; xe ba bánh chở hàng → ngoài lớp. |
| `motorcycle` | Xe hai bánh có động cơ, kể cả có thùng bên (sidecar). | Xe số, tay ga, mô tô, xe điện hai bánh. | Xe đạp, xe ba bánh → ngoài lớp. |
| `person` | Người thật, đang đi, đứng, ngồi, kể cả người ngồi trên xe hở. | Người đi bộ, người bán rong, người lái và người ngồi sau xe máy. | Tượng, ma-nơ-canh, hình người in, linh vật nhồi bông → không gán (R-07). |
| `ignore_region` | Vùng không dạy mô hình: vật thật ngoài 5 lớp, vật quá nhỏ, cụm quá dày. Bỏ sót trong vùng này không tính là lỗi. | Xe buýt, tuk-tuk, cụm xe máy nền xa. | Không dùng để né ca khó mà vẫn gán được (R-16). |

**Vật không thuộc lớp nào:**

- **Phương tiện hoặc người thật nhưng ngoài 5 lớp** (xe buýt, tuk-tuk, xích lô, xe đạp, xe lam, xe lăn, xe kéo tay…) → `ignore_region` (R-06).
- **Không phải phương tiện hay người** (động vật, cọc tiêu, biển báo, cây, nhà, thùng rác, hàng hóa đơn lẻ) → không gán gì.
- **Không thật** (tượng, ma-nơ-canh, đồ chơi…) → không gán gì (R-07).
- Không tự tạo lớp mới khi gán. Thêm lớp (ví dụ `bus`, `bicycle`) chỉ làm bằng cách đổi taxonomy và phát hành phiên bản guideline mới.

### 2.2 Thuộc tính

#### `occluded_level`: mức bị vật hoặc người khác che (R-10)

Ước lượng theo **diện tích** phần bị che trên tổng diện tích vật nếu nhìn đầy đủ **ở tư thế hiện tại** (người đang ngồi xe thì tính theo dáng ngồi, không tính như đang đứng).

| Mức | Phần bị che | Neo nhận biết bằng mắt |
|---|---|---|
| `0` | ≤ 10% | thấy gần trọn vẹn |
| `1` | > 10% đến 40% | mất một góc, một bánh hoặc một chân |
| `2` | > 40% đến 75% | thấy khoảng nửa vật hoặc ít hơn |
| `3` | > 75%, vẫn nhận ra lớp | chỉ thấy mảnh nhỏ (đầu và vai, nửa bánh và đèn) |

- Phân vân giữa hai mức → chọn **mức cao hơn**.
- Phần bị cắt bởi mép ảnh **không tính** vào che khuất (dùng `truncated`).
- Phần bị che bởi chính phụ kiện của vật (mũ, áo mưa, hàng mang theo) không tính.
- Thấy dưới ~10% diện tích hoặc không xác định được lớp → không gán box lớp; xử lý theo R-13.
- Cờ `occluded` có sẵn của công cụ gán nhãn **không dùng**; chỉ dùng thuộc tính `occluded_level`.

#### `truncated`: bị cắt bởi mép ảnh (R-11)

| Giá trị | Khi nào |
|---|---|
| `no` | Vật nằm trọn trong khung, hoặc phần ngoài khung dưới ~5%. |
| `yes` | Còn rõ một phần vật nằm ngoài khung (≥ ~5%): cạnh box trùng mép ảnh (cách ≤ 2 px) và vật tiếp tục ra ngoài. |

Chỉ xét mép **ảnh**. Vật vừa bị cắt mép vừa bị che thì gán cả hai thuộc tính.

#### `can_review`: nhờ người khác xem lại (R-17)

Tick khi: (a) phân vân giữa hai lớp, (b) gặp loại vật guideline chưa nói tới, (c) mức che thật sự lưng chừng ở vật nổi bật, (d) vật mờ hoặc tối khó nhận. Không tick tràn lan: nếu quá ~10% box trong một ảnh bị tick, guideline còn thiếu quy tắc và phải báo nhóm.

---

## 3. Quy tắc vẽ box

### R-01. Box chung

- Box ôm **phần nhìn thấy** của vật, không đoán phần bị che.
- Cạnh box sát biên vật, sai số mục tiêu ≤ 2 px; không chừa lề rộng, không cắt mất thân vật.
- **Gồm:** thân xe, bánh, gương, tay lái, baga hoặc giá đồ gắn chặt, hàng chất gọn trong hoặc trên xe.
- **Không gồm:** bóng đổ, phản chiếu trên nền ướt, ăng-ten hoặc cần mảnh, vật dài nhô xa khỏi thân (ống, cần), dây cáp.
- Người: box từ đỉnh đầu (gồm mũ, nón) đến chỗ thấp nhất thấy được, gồm đồ mang sát người (ba lô, túi). Đồ gánh hoặc vật dài nhô xa khỏi người thì bỏ ra khỏi box.
- Một vật đúng một box; không vẽ hai box chồng khít cho cùng một vật.

### R-02. Xe máy

- `motorcycle` là **chỉ phần xe** (thân, bánh, tay lái, gương, baga, hàng chất lên xe). **Không** gộp người ngồi vào box xe.
- Xe có thùng bên: một box ôm cả xe và thùng bên.
- Xe đậu không người vẫn là `motorcycle`, cùng quy tắc.

### R-03. Người trên xe

- Mỗi người (người lái, từng người ngồi sau, trẻ em ngồi trước) là **một box `person` riêng**, ôm phần nhìn thấy của riêng người đó.
- Box `person` và box xe được phép **chồng lấn**.
- Tính `occluded_level` theo tư thế ngồi. Người ngồi sau bị người trước che thường là mức 1–2.
- Người ngồi trên phương tiện hở (xe đạp, xích lô, tuk-tuk không cửa, xe lam, thùng pickup hở) vẫn là `person`; phương tiện đó xử lý theo R-06.

### R-04. Người trong cabin kín

- Người ngồi **trong cabin kín** (ô tô, xe tải, xe buýt, van, nhìn qua kính) → **không gán `person`**, kể cả khi thấy mặt.
- Người ngồi trên hoặc trong phương tiện **hở hoặc bán hở** (xe máy, tuk-tuk, xích lô, thùng pickup hở) → gán `person`.
- Lý do: qua kính phản xạ hoặc tối, phần nhìn thấy không ổn định giữa người gán.
- Cabin mở hoàn toàn, người thấy rõ (xe không mui, cửa mở) → gán và tick `can_review`.

### R-05. Phân lớp ô tô (cây quyết định)

1. Có thùng hàng **tách riêng** (thùng mở, bạt, thùng rời), hoặc là đầu kéo, xe chuyên dụng chở hàng → `truck`. **Pickup, kể cả có nắp thùng, thuộc nhóm này**: một box ôm cabin, thùng, nắp và hàng chất gọn trong thùng.
2. Thân kín liền khối cao, cửa trượt hoặc kính hông kéo dài, cỡ ≤ ~15 chỗ → `van`.
3. Xe buýt hoặc xe khách dài, hơn ~15 chỗ → ngoài lớp (R-06).
4. Còn lại (sedan, hatchback, SUV, MPV, wagon, xe thể thao) → `car`.
5. Vẫn phân vân giữa hai lớp → chọn lớp gần nhất theo hình dáng nhìn từ ngoài và tick `can_review`.

### R-06. Xe thật ngoài 5 lớp → `ignore_region`

- Gồm xe buýt, tuk-tuk, xe lam, xích lô, xe đạp, xe ba bánh chở hàng, xe lăn, xe kéo tay.
- Vẽ **một box `ignore_region` ôm cả xe** (kể cả hàng chất trên xe), mỗi xe một box.
- Người ngồi hoặc lái xe hở vẫn gán `person` (R-03); box `person` nằm trong vùng ignore là bình thường.
- Chỉ vẽ ignore khi vật cao ≥ 20 px và nhận ra rõ là phương tiện; nhỏ hơn theo R-12.
- **Không** gán `motorcycle` hay `truck` chỉ vì "gần giống".

### R-07. Vật không thật → không gán, không ignore

Gồm tượng, ma-nơ-canh, búp bê, linh vật nhồi bông, xe đồ chơi, mô hình, bia hoặc công trình hình xe, hình in (áp phích, pano, tranh tường, hình dán), và mọi **phản chiếu** (gương, kính, mặt đường ướt).

- Ngoại lệ: **người thật mặc trang phục hóa trang** vẫn là `person` nếu rõ là người đang đứng hoặc đi.
- Không chắc là người thật hay mô hình → không box, và ghi vấn đề cấp ảnh (ảnh, vùng, lý do) để người quyết định xem.
- Xe thật chạy được nhưng dựng kiểu giả tưởng là R-08, không phải R-07.

### R-08. Xe thật nhưng kiểu lạ

- Tiêu chí "thật": có bánh chạy được, biển số hoặc người lái, đang trên đường (hoặc trong bảo tàng, showroom xe đúng nghĩa).
- Xe diễu hành, xe độ, xe cổ → gán theo **lớp tương đương về kích thước và hình dáng**, tick `can_review`.
- Xe trong bảo tàng hoặc showroom vẫn là xe thật → gán như xe ngoài đường.

### R-09. Xe hoặc vật được chở trên xe khác

- **Xe và hàng được chở là hàng hóa của xe chở.** Không box riêng; chúng nằm trong box xe chở (R-01).
- Xe chở xe: một box `truck` ôm cả đầu kéo, khung và các xe trên khung.
- Vật nhỏ đặt trên nóc hoặc thùng xe khác (xe mô hình, tượng): không box riêng; box của xe bên dưới ôm xe đó, **không** kéo lên phần nhô cao.
- Người ngồi hoặc bám trên xe tải vẫn `person` (hở).
- Người đứng dưới đất cạnh xe vẫn `person`.

### R-10. Mức che khuất

Áp dụng bảng `occluded_level` ở mục 2.2. Che bởi hàng rào hoặc vật mảnh (hàng rào thưa, dây, cành cây) → mức 1–2 tùy mật độ. Che bởi kính tủ trưng bày chứa vật giả → R-07.

### R-11. Cắt mép ảnh

Áp dụng `truncated` ở mục 2.2. Box kéo sát mép ảnh, không vượt ra ngoài khung.

### R-12. Vật nhỏ

- Chiều cao box < 20 px: **không** vẽ box lớp (đây là ngưỡng tối thiểu của taxonomy).
- Một vật nhỏ đơn lẻ → không gán gì.
- Từ 3 vật nhỏ trở lên gần nhau → một `ignore_region` ôm cụm (R-13).
- Vật ở sát ngưỡng 20 px: đo bằng công cụ của phần mềm gán nhãn, không đoán bằng mắt. Từ 20 px trở lên **phải gán** nếu nhận ra lớp.

### R-13. Đám đông và cụm dày

- Gán từng `person` hoặc `motorcycle` khi: cao ≥ 20 px, thấy ≥ ~25% và nhận ra lớp.
- Phần nền xa, cụm không tách được ranh giới hoặc quá nhỏ → **một `ignore_region`** ôm cụm (có thể vài vùng nếu cụm rời nhau).
- Không cố gán mọi vật trong cụm đặc; ưu tiên **nhất quán** hơn số lượng.
- Phân vân ở ranh giới cụm: dùng ignore sớm, vì bất đồng ở đây làm IAA tụt.

### R-14. Xe chủ (ego) và phần xe của camera

- Phần thân xe mà camera gắn lên hoặc ngồi trong (mui, bảng điều khiển, gương nhìn từ trong xe, nắp ca-pô của xe chụp) → **không gán**.
- Xe khác ở sát camera, bị cắt mép → vẫn gán, `truncated=yes`.

### R-15. Điều kiện ảnh khó

- **Mờ chuyển động:** gán nếu nhận ra lớp; box ôm lõi của vật, không ôm vệt mờ kéo dài. Không nhận ra: ignore nếu cả cụm, nếu không thì không gán.
- **Ban đêm, thiếu sáng:** gán những gì **thấy được**; chỉ thấy đốm sáng hoặc đèn hậu mà không nhận ra lớp → không gán, không đoán.
- **Qua kính, hàng rào, dây:** xe thật phía sau vật mảnh vẫn gán, `occluded_level` theo R-10.
- **Ảnh đen trắng, ảnh cũ:** luật không đổi.

### R-16. Cách dùng `ignore_region`

- Chỉ dùng cho: (a) vật thật ngoài 5 lớp, (b) vật nhỏ dưới 20 px, (c) cụm quá dày, (d) vật thấy quá ít không nhận ra lớp.
- **Không** dùng để né ca khó khi vật vẫn nhận ra và thuộc 5 lớp: phải gán, tick `can_review` nếu chưa chắc.
- Vùng ignore không phủ lên box lớp đã gán, trừ box nằm trong vật ngoài lớp (người trên tuk-tuk).
- Nhiều vùng ignore sát nhau cùng một loại, ranh giới không rõ → gộp thành một vùng.

### R-17. `can_review`

- **Có:** ngoại lệ của R-04 và R-07, R-08, phân vân `van`/`car`/`truck`, mức che lưng chừng ở vật nổi bật.
- **Không:** ca guideline đã quy định rõ, chỉ lệch tọa độ nhỏ.
- Chỗ **không vẽ được box** (vật lạ, vùng hỗn hợp): ghi vấn đề cấp ảnh (ảnh, vùng, lý do) để người quyết định xem.

### R-18. Ảnh không có vật cần gán

- Ảnh vẫn nằm trong lô gán và **không vẽ gì**; ảnh không có annotation được hiểu là "đã gán, không có vật".
- Không "gán bù" box lên vật giả cho đủ số lượng.

### R-19. Box lồng nhau và trùng lặp

- Chỉ cho phép lồng: `person` trong `ignore_region` (xe ngoài lớp); `person` chồng `motorcycle` (R-03).
- Hai box cùng lớp không chồng khít (IoU > ~0.7 trên cùng một vật): xóa bớt.
- Không vẽ `ignore_region` bọc quanh vật đã có box lớp.

---

## 4. Ca khó tiêu biểu

Một số ảnh đại diện cho các nhóm tình huống; các ảnh còn lại áp dụng quy tắc ở mục 3.

| Ảnh | Tình huống | Rule | Quyết định | Lý do |
|---|---|---|---|---|
| `img_026` | Hai người trên một xe máy, nền là tranh in | R-02, R-03, R-07 | 1 `motorcycle` + 2 `person`; tranh không gán | Người và xe tách box; hình in không thật. |
| `img_005` | Nhiều người đội mũ bảo hiểm che chồng nhau | R-03, R-10 | `person` từng người, `occluded_level` 1–3 | Che chồng nặng: phân vân thì chọn mức cao hơn. |
| `img_002` | Xe chở ô tô nhiều tầng | R-09 | 1 `truck` ôm cả khung và xe trên khung | Xe được chở là hàng của xe chở. |
| `img_004` | Tuk-tuk, tài xế ngồi trong | R-06, R-03 | `ignore_region` cho xe; `person` cho tài xế | Xe ngoài 5 lớp; người trong xe hở vẫn gán. |
| `img_017` | Tượng người cưỡi ngựa | R-07, R-18 | Không gán gì | Tượng không phải người thật; ảnh vẫn tính là đã gán. |
| `img_019` | Xe diễu hành giả tưởng, có biển số, đang chạy | R-08, R-04, R-07 | `car` + `can_review`; mascot và người trong cabin kín không gán | Xe thật chạy được gán theo lớp tương đương. |
| `img_030` | Bãi xe máy đậu dày đặc | R-13, R-10 | Xe phía trước gán từng chiếc; nền sau vào `ignore_region` | Cụm không tách được ranh giới. |
| `img_015` | Hai xe sát camera bị cắt mép, nền mờ | R-11, R-15 | `car` với `truncated=yes`; xe nền chỉ gán nếu nhận ra lớp | Cắt mép và mờ chuyển động. |

---

## 5. QC và phiên bản

- **Ngưỡng chất lượng áp dụng:** box cao ≥ 50 px → IoU ≥ 0.85, nhỏ hơn → IoU ≥ 0.7; đồng thuận trung bình IoU ≥ 0.85 và cùng lớp ≥ 95%; box lớp cao < 20 px không hợp lệ; tỉ lệ ảnh lỗi > 2% thì làm lại.
- **Tự kiểm trước khi bàn giao nhãn:** (1) đủ ảnh được giao, kể cả ảnh không có vật; (2) không có box lớp cao < 20 px; (3) mọi `ignore_region` có lý do theo R-16; (4) vật giả không có box.
- **Ca mơ hồ:** tick `can_review`. Quyết định cuối do người được giao quyết và ghi lại kèm mã quy tắc `R-xx`.
- **Loại lỗi cần người xem bằng mắt:** box không ôm sát, sai lớp, vật cả nhóm cùng bỏ sót, cả nhóm cùng hiểu sai quy tắc (ví dụ cùng gán box lên tượng).
- **Phiên bản:** mọi thay đổi làm đổi nhãn đều tăng phiên bản guideline và ghi vào bảng dưới.

| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| v0 | Bản khởi đầu | — |
| v0.1-101 | Bản cá nhân: R-01…R-19, ngưỡng thuộc tính, ca khó tiêu biểu | Khảo sát bộ ảnh lab |
