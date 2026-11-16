# Guideline gán nhãn — v0.1-cá nhân — thành viên 101

> Bản cá nhân Pha 1, viết trước khi họp nhóm. **Không sửa sau khi họp** (so với v1.0 của nhóm).
> Bản nháp có AI hỗ trợ (xem `individual_notes/101.md`). TODO 101: mở lại từng ảnh được dẫn, sửa chỗ không đồng ý, rồi xoá dòng TODO này.

- Phiên bản: v0.1 (cá nhân, dựa trên v0 starter)
- Ngày: 2026-11-16
- Người viết: Nguyễn Thanh Thản-2A202603202 101 · Người duyệt: (nhóm, Pha 2)

## 1. Mục tiêu

Nhãn huấn luyện mô hình **phát hiện vật 2D** (bounding box) cho **người và phương tiện đường bộ thật**,
dùng cho camera giao thông / xe tự lái.

- **Sai nguy hiểm nhất:** bỏ sót người hoặc xe thật (mô hình học "không có gì" ở đó). Vì vậy
  vật thật mà mình không vẽ box được thì phủ `ignore_region`, **không bỏ trống**.
- **Sai thứ hai:** gán box cho vật không thật (tượng, ma-nơ-canh, ảnh in, phản chiếu, đồ chơi), làm mô hình báo động giả.
- Mọi quy tắc dưới đây trả lời câu hỏi: *"Camera đặt ở đường này có cần nhận ra vật này là người/xe để tránh không?"*

## 2. Lớp và thuộc tính

### 2.1 Lớp (mỗi box đúng một lớp)

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Xe 4 bánh chở người, khoang hành khách liền khối, tối đa ~9 chỗ: sedan, hatchback, SUV, wagon, taxi. | img_015 (xe đỏ, xe bạc), img_012 (Mazda SUV bạc), img_023 (sedan đen), img_040 (taxi xanh, SUV đen), img_024 (Pacer đen) | Pickup → `truck`; minivan thùng cao kiểu Hiace → `van` |
| `truck` | Xe chở hàng có **cabin tách khỏi thùng/sàn hàng**: xe tải, pickup (kể cả pickup có nắp thùng), đầu kéo, xe chở xe. | img_001 (xe tải nhỏ Suzuki), img_007 (Isuzu + Hilux có khung), img_036 (Veryca), img_037 (pickup có nắp thùng), img_028 (pickup cổ), img_002 (xe chở ô tô) | SUV (thùng sau liền cabin) → `car` |
| `van` | Xe thùng kín liền khối, mui cao, cửa trượt hông, chở người hoặc hàng, **dưới ~16 chỗ**. | img_005 (Hiace bạc phía sau), img_016 (xe trắng chữ TAXI bên phải) | Minibus/bus ≥ 16 chỗ (img_009) → ngoài taxonomy, xem R-07 |
| `motorcycle` | Xe 2 bánh có động cơ (xe máy, xe tay ga, mô tô), kể cả mô tô có thùng bên (sidecar). | img_006, img_021, img_030, img_022 (sidecar) | Xe đạp, xích lô, tuk-tuk, xe lam 3 bánh → ngoài taxonomy (R-07) |
| `person` | Người thật nhìn thấy trực tiếp: đi bộ, đứng, ngồi, người lái hoặc ngồi trên xe hở. | img_014, img_034, người lái xe máy img_026 | Tượng (img_017), ma-nơ-canh (img_033), người trên biển quảng cáo (img_018) → không gán |
| `ignore_region` | Vùng có vật thật thuộc taxonomy nhưng **không vẽ từng box được** (quá nhỏ, quá dày, quá mờ). Không phải một vật. | đám đông sau rào img_019, bãi xe dày phía sau img_030 | Không dùng cho vật không thật hoặc vật ngoài taxonomy |

**Vật không thuộc lớp nào:** **không gán, không vẽ `ignore_region`** (xem R-07, R-08). Ghi vào mục Ca khó nếu đáng bàn.

### 2.2 Thuộc tính (ngưỡng đo được)

**`occluded_level`**: phần trăm diện tích vật **bị vật khác che** (ước lượng theo hình dạng đầy đủ dự đoán được).
Phần nằm ngoài khung ảnh **không** tính vào đây (đó là `truncated`).

| Mức | Ngưỡng | Ví dụ |
|---|---|---|
| `0` | che ≤ 10% | xe tải img_036 |
| `1` | 10% < che ≤ 40% | xe máy có người ngồi che yên/hông (img_026) |
| `2` | 40% < che ≤ 70% | xe máy giữa dòng img_021 chỉ thấy đuôi xe và bánh |
| `3` | che > 70% **hoặc** không ước lượng được | người chỉ lộ đầu giữa đám xe img_005 |

- Người ngồi trên xe máy che xe → tính là che xe máy. Xe che chân người lái → tính là che người.
- Che bởi vật trong suốt hoặc hàng rào thưa (img_018) → chỉ tính phần thực sự bị khuất, thường là mức `1`.

**`truncated`**: `yes` nếu vật **bị mép ảnh cắt** (box chạm mép ảnh ≤ 2 px và vật còn tiếp bên ngoài). Ngược lại `no`.
Ví dụ `yes`: xe đỏ và xe bạc img_015, người áo đỏ góc phải img_016, người đội mũ bảo hiểm img_040.

**`can_review`**: tick khi box thuộc một ca trong mục 4b (cần reviewer) hoặc mình không chắc lớp hay ranh giới. Không tick bừa: ca đã có quy tắc thì làm theo quy tắc.

## 3. Quy tắc vẽ box

| Mã | Quy tắc |
|---|---|
| **R-01** Box sát phần nhìn thấy | Box ôm **phần nhìn thấy** (modal), lệch ≤ 2 px mỗi cạnh. Không đoán phần bị che. Gương chiếu hậu, ăng-ten, tay lái tính vào xe; bóng đổ và phản chiếu trên mặt đường không tính (img_015 mặt đường ướt). |
| **R-02** Người đi xe máy | **Tách box**: 1 `person` cho mỗi người (lái và từng người ngồi sau), 1 `motorcycle` cho xe. Box `person` bao cả mũ bảo hiểm, phần chân thấy được; box `motorcycle` bao xe từ bánh trước đến bánh sau/biển số, kể cả phần bị chân che nằm giữa (không cắt đôi xe). Ví dụ: img_026 → 2 `person` + 1 `motorcycle`; img_010 cặp bên trái → 2 `person` + 1 `motorcycle`. |
| **R-03** Người trên phương tiện khác | Người nhìn thấy **trực tiếp** (không qua kính) trên xe hở: xích lô, xe đạp, tuk-tuk, thùng pickup → gán `person` dù xe không có lớp (img_023 người đạp xích lô, img_035 người lái mô tô). Người ngồi trong cabin kín chỉ thấy **qua kính chắn gió** → không gán (tài xế xe tải img_002, ô tô img_015). |
| **R-04** Hàng hoá, vật mang theo | Hàng **chất cố định trên xe** là một phần xe (thùng hàng img_012, đống bao trên xe lam img_035 nếu xe được gán). Vật **người cầm hoặc vác** không thuộc box nào: thanh dài img_029 không mở rộng box xe máy; quang gánh img_003 không mở rộng box người (nón lá đội trên đầu thì tính vào box người). |
| **R-05** Che khuất | Vẫn gán vật bị che nếu nhận ra được lớp và thấy ≥ 20 px chiều cao; đặt `occluded_level` theo 2.2. Vật che > 70% mà **không nhận ra lớp** → không vẽ box, phủ `ignore_region` nếu nằm trong cụm (R-09). |
| **R-06** Cắt mép | Gán nếu phần trong ảnh **nhận ra được lớp**, `truncated=yes`. Chỉ lộ chi tiết không đủ nhận ra (chỉ hai gương chiếu hậu ở mép dưới img_040) → không gán. |
| **R-07** Ngoài taxonomy | Bus/minibus ≥ 16 chỗ (img_009, img_031, img_037, img_040), xe đạp, xích lô (img_023), tuk-tuk / xe lam 3 bánh (img_004, img_016, img_035, img_040), động vật → **không gán và không ép vào lớp gần nhất**, không vẽ `ignore_region`. Người trên các xe đó vẫn theo R-03. *(Đề xuất cho nhóm: bus và xe 3 bánh rất hay gặp, cân nhắc thêm lớp ở v1.x.)* |
| **R-08** Vật không thật | Tượng, mô hình, đồ chơi, ma-nơ-canh, hình in trên biển/tường, hình phản chiếu trong gương/kính/vũng nước → **không gán**, không `ignore_region`. Ví dụ img_017, img_027, img_028 (con ngựa), img_033, img_018, img_026 (tranh nền), img_020, img_038, img_024 (xe vàng thu nhỏ trên nóc). |
| **R-09** Vật nhỏ, đám đông | Vật thật cao **< 20 px** (`min_box_height_px`) → không vẽ box lớp; phủ chung bằng **một** `ignore_region` cho cả cụm. Cụm vật ≥ 20 px nhưng chồng nhau tới mức không tách được ranh giới từng vật (ước lượng > 50% số vật trong cụm che nhau mức `3`) → `ignore_region` cho cụm, vật tách được ở rìa vẫn gán riêng. Ví dụ: đám đông sau rào img_019, bãi xe phía sau img_030, đoàn xe xa img_021. |
| **R-10** Ảnh mờ chuyển động | Vật thật bị mờ: nếu vẫn ước lượng được ranh giới thì gán bình thường, tick `can_review`; nếu mờ thành vệt không tách được (dòng xe phía sau img_014) → `ignore_region`. |
| **R-11** Xe chủ (ego) | Phần xe của người chụp (khung cửa, gương img_020, thùng pickup ở tiền cảnh nếu người chụp đứng trong đó) → không gán. Pickup img_012 nhìn từ phía sau, thấy rõ là một xe đỗ → **gán** `truck`, `truncated=yes`. |
| **R-12** Xe kéo rơ-moóc / chở xe | Đầu xe + sàn chở + rơ-moóc nối liền = **một** box `truck`. Ô tô thật đang được chở trên sàn = `car` riêng, đặt `occluded_level` theo phần bị khung che (img_002). |
| **R-13** Ảnh không có vật | Ảnh không có vật nào cần gán vẫn phải có trong file COCO (không có annotation). Ví dụ dự kiến: img_017, img_020, img_027, img_033, img_038. |

## 4. Ca khó

### 4a. Ca loại / quyết định **theo quy tắc** (không cần hỏi)

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_005 | Nhiều người đi xe máy chồng nhau sát camera | R-02, R-05 | Mỗi người 1 `person`, mỗi xe nhận ra được 1 `motorcycle`; người lộ mặt/đầu nhưng thân bị che → `occluded_level=2/3` | Người thật ở gần, mô hình phải thấy |
| img_026 | Đôi nam nữ trên xe máy, nền là tranh in cảng biển | R-02, R-08 | 2 `person` + 1 `motorcycle`; không gán gì trên tranh | Tranh là hình in |
| img_002 | Xe chở ô tô, 8–9 xe con trên sàn, 1 người đứng cạnh rơ-moóc | R-12, R-03 | 1 `truck` cho cả tổ hợp; từng xe con `car` (che 1–3); người đứng = `person`; tài xế sau kính không gán | Xe được chở là xe thật |
| img_017 | Tượng người cưỡi ngựa đội nón giao thông | R-08 | Không gán (ảnh rỗng) | Tượng |
| img_027 | Bia mộ hình xe pickup | R-08 | Không gán | Tượng đá |
| img_028 | Pickup thật chở tượng ngựa; SUV đỏ phía sau | R-08, R-01 | Pickup `truck`; SUV `car` (`occluded_level=1`); ngựa không gán | Ngựa là tượng, xe là thật |
| img_024 | Xe Pacer đen chở mô hình Pacer vàng thu nhỏ trên nóc, bảo tàng xe | R-08 | Xe đen và các xe trưng bày = `car`; xe vàng không gán | Mô hình không chạy trên đường |
| img_038 | Tủ kính xe đồ chơi | R-08 | Không gán | Đồ chơi |
| img_033 | Ma-nơ-canh, ảnh in người, phần xe tải phản chiếu trên kính | R-08 | Không gán | Ma-nơ-canh, hình in và phản chiếu |
| img_018 | Biển quảng cáo có người; bãi ô tô sau hàng rào | R-08, R-05 | Người trên biển không gán; các ô tô `car`, `occluded_level=1` (rào thưa) | Hình in; xe thật bị rào che một phần |
| img_020 | Gương chiếu hậu phản chiếu đường và xe | R-08, R-11 | Không gán | Phản chiếu và xe chủ |
| img_009, img_031, img_037 | Bus / minibus | R-07 | Không gán | Ngoài taxonomy |
| img_004 | Hai tuk-tuk, tài xế ngồi trong | R-07, R-03 | Không gán tuk-tuk; tài xế thấy trực tiếp (không kính) → `person`, `occluded_level=2` | Xe 3 bánh ngoài taxonomy, người vẫn là người |
| img_023, img_006 | Xích lô, xe đạp | R-07, R-03 | Không gán xe; người đạp/ngồi → `person` | Như trên |
| img_029 | Người đi xe máy vác thanh dài, người đi xe đạp | R-04, R-02, R-07 | Xe máy box không gồm thanh; 2 `person`; xe đạp không gán | Vật cầm theo không thuộc xe |
| img_003 | Người bán hàng gánh quang, xe đạp, bãi xe máy xa | R-04, R-07, R-09 | Người không bao quang gánh; xe đạp không gán; xe máy xa < 20 px → `ignore_region` | |
| img_022 | Mô tô sidecar, ảnh đen trắng cũ | R-01 | 1 `motorcycle` bao cả sidecar; người lái `person` nếu ≥ 20 px | Sidecar gắn liền xe |
| img_040 | Người đội mũ bảo hiểm cắt mép; chỉ thấy gương xe máy; taxi, tuk-tuk, bus | R-06, R-07 | `person` `truncated=yes`; xe máy chỉ thấy gương → không gán; taxi và SUV `car`; tuk-tuk và bus không gán | Không nhận ra được xe từ hai cái gương |
| img_015 | Hai xe cắt mép trái/phải, xe mờ chuyển động phía sau, mặt đường phản chiếu | R-06, R-10, R-08 | 2 `car` `truncated=yes`; xe mờ phía sau gán nếu thấy ranh giới; phản chiếu trên mặt đường không gán | |
| img_012 | Pickup tiền cảnh nhìn từ sau, cắt mép | R-11, R-06 | `truck`, `truncated=yes` | Không phải xe của người chụp |
| img_013 | Đường đêm, người và xe ở xa | R-09 | Vật ≥ 20 px gán riêng, nhỏ hơn → `ignore_region` | |
| img_030, img_021 | Bãi xe máy / dòng xe dày đặc | R-09, R-02 | Hàng xe tiền cảnh gán riêng; khối phía sau không tách được → `ignore_region` | |

### 4b. Ca **cần hỏi reviewer** (tick `can_review` hoặc ghi vấn đề cấp ảnh)

| Ảnh | Tình huống | Rule ID | Quyết định tạm | Câu hỏi cho nhóm |
|---|---|---|---|---|
| img_019 | Xe "Dangermouse" diễu hành: xe thật chạy được, có người lái; nhân vật chuột ngồi cạnh | R-08 | Xe = `car` + `can_review`; người lái `person`; chuột không gán + `can_review`; đám đông sau rào → `ignore_region` | Xe giả tưởng nhưng chạy thật trên đường có tính là `car`? Chuột là người mặc đồ hoá trang hay tượng? |
| img_011 | Nhân vật Predator kim loại; hàng mô tô trang trí bằng kim loại | R-08 | Predator không gán (tượng); mô tô: `motorcycle` + `can_review` | Đây là xe chạy được hay tác phẩm điêu khắc hình mô tô? |
| img_009 | Toyota Coaster ~ 20 chỗ | R-07 | Không gán | Nhóm có thêm lớp `bus` không? Nếu không, minibus nên là `van` hay bỏ? |
| img_016, img_035 | Tuk-tuk / xe lam chiếm phần lớn ảnh | R-07 | Không gán | Bỏ một vật lớn trên đường thì mô hình học "không có gì". Có nên thêm lớp 3 bánh hay dùng `ignore_region`? |
| img_007 | Hilux có khung lồng/thùng phía sau | R-01 | `truck` + `can_review` | Pickup có kết cấu sau là `truck` hay `van`? |
| img_032 | Đám đông chờ xe buýt (~40 người cao ~60–90 px, chồng nhau) | R-09 | Gán riêng người ở rìa tách được; khối giữa → `ignore_region` | Ngưỡng "không tách được" có cần đo bằng số không (vd. ≥ 3 người che nhau mức 3)? |
| img_014 | Người đi xe máy mờ chuyển động sau hai người đi bộ | R-10 | 2 `person` rõ; dòng mờ → `ignore_region` | Mờ tới mức nào thì chuyển sang ignore? |
| img_001 | Nhóm khách ngồi sau bàn, che nhiều | R-05 | Gán từng người nhận ra, `occluded_level` 1–3 | Người chỉ lộ đầu/vai sau bàn: gán hay ignore? |

## 5. QC và phiên bản

- Ngưỡng theo `taxonomy.json → rules` (không đổi): box cao tối thiểu 20 px; IoU đạt ≥ 0.85 (box ≥ 50 px), ≥ 0.7 (nhỏ hơn); IAA IoU TB ≥ 0.85, cùng lớp ≥ 95%; lỗi theo ảnh ≤ 2% mới Release.
- **Ai quyết ca mơ hồ:** ca 4b đưa vào họp Pha 2; ca phát sinh lúc gán → `can_review`, chốt ở calibration (Pha 5), ghi vào `calibration_decisions.csv` với mã quy tắc.
- Đổi cách chọn vật, lớp, box hoặc thuộc tính = thay đổi **semantic** → tăng phiên bản và rà lại cả lô; sửa câu chữ = **editorial**.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu của giảng viên | — |
| v0.1-101 | Thêm định nghĩa lớp có ví dụ/phản ví dụ, ngưỡng % cho `occluded_level`, định nghĩa `truncated`, quy tắc R-01…R-13, bảng ca khó | Xem 40 ảnh: img_002, img_005, img_017, img_019, img_024, img_026, img_028… |
