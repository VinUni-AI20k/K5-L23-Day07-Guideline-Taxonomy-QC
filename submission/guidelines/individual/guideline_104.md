# Guideline gán nhãn — v0.1 (bản cá nhân) — 104

- Phiên bản: v0.1 
- Ngày: 2026-11-16
- Người viết: 104
- Phạm vi: 40 ảnh 
## 1. Mục tiêu

Nhãn huấn luyện mô hình phát hiện vật 2D (người, phương tiện) trên ảnh đường phố, dùng cho camera giao thông và bài toán đếm/ theo vết phương tiện.

- Sai ở đâu thì nguy hiểm:
  - Gán `person` lên tượng, ma-nơ-canh, hình in quảng cáo → mô hình học "người giả", báo động giả ở nơi đông người.
  - Bỏ sót xe bị che một phần → mô hình bỏ qua vật thật khi đường đông, nguy hiểm cho bài toán an toàn.
  - Box không ôm sát (bao cả hàng hóa, bao cả khung chở) → mô hình học kích thước sai, ảnh hưởng ước lượng khoảng cách.
- Ưu tiên khi phải chọn: **nhất quán giữa các người gán** quan trọng hơn "đẹp từng box". Một quy tắc xấu nhưng mọi người áp giống nhau vẫn đo được IAA; hai quy tắc tốt nhưng khác nhau thì IAA vô nghĩa.

## 2. Lớp và thuộc tính

### Lớp

Bộ lớp dùng cho lượt gán độc lập: 5 lớp của v0 + `ignore_region`. Hai lớp **đề xuất bổ sung** ở Pha 2 (`bus`, `tuk_tuk`) ghi rõ là đề xuất, chưa dùng khi chưa chốt.

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô con hoặc SUV chở người, có 4 bánh, thân kín. | img_002: xe con chở trên sàn; img_035: xe trắng bên phải | Xe bán tải có nắp thùng cao (img_037) → `truck`; xe con đồ chơi trong tủ kính (img_038) → không gán |
| `truck` | Xe tải hoặc xe có thùng/khung chở hàng riêng, khối lượng lớn. | img_002: xe đầu kéo chở ô tô; img_024: xe chở thân vỏ xe | Xe van thùng kín cỡ nhỏ → `van` |
| `van` | Xe thùng kín cỡ nhỏ, thường 1 khối liền, cửa sau kín. | xe giao hàng cỡ nhỏ | Xe 7 chỗ/SUV cỡ lớn → `car` |
| `motorcycle` | Xe hai bánh có động cơ, kể cả xe máy điện. | img_035: xe máy giữa ảnh | Xe đạp, xích lô không động cơ (img_006, img_029, img_039) → không gán |
| `person` | Người thật, đang đứng, đi hoặc ngồi lộ rõ thân người. | người đi bộ trên vỉa hè | Tượng (img_011, img_017, img_027), ma-nơ-canh (img_033), hình in trên biển quảng cáo (img_018) → không gán |
| `ignore_region` | Vùng không gán từng vật: đám đông dày, cụm vật cao dưới 20 px. | vùng chợ đông không tách được từng người | Không dùng để che lỗi bỏ sót vật to, rõ |
| `bus` | Xe khách cỡ lớn, thân dài, nhiều cửa sổ. | img_009, img_031, img_037, img_040 | Xe tải có thùng kín cỡ lớn → `truck` |
| `tuk_tuk`  | Xe ba bánh chở khách/kia, ca-bin hở. | img_004, img_016, img_035 | Xe ba bánh chở hàng thùng kín → `truck` nếu thùng hàng rõ |


Vật không thuộc lớp nào:
- Tượng, ma-nơ-canh, đồ chơi, hình in, phản chiếu: **không gán box**. Nếu cụm chiếm > 10% ảnh và dễ gây nhầm: một `ignore_region` + một dòng trong `submission/qc/image_issues.csv`.
- Xe đạp, xích lô, xe ba gác không động cơ: **không gán box** (chưa có lớp). Ghi `image_issues.csv` để Pha 2 quyết.
- Vật thật nhưng không xác định được lớp: `can_review` + gán lớp gần nhất, ghi lý do trong `image_issues.csv`.

### Thuộc tính

| Thuộc tính | Mức cố định | Nghĩa từng mức | Ngưỡng đo được |
|---|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | 0 = không bị che; 1 = che nhẹ; 2 = che vừa; 3 = che nặng nhưng vẫn nhận dạng chắc chắn | Đo **tỉ lệ diện tích phần bị che / diện tích vật nếu không bị che**: `0` = 0%; `1` = 1–30%; `2` = 31–70%; `3` = 71–95%. Che > 95% hoặc không nhận dạng được lớp → không gán box, ghi `image_issues.csv`. Ước lượng theo 1/3 diện tích, không đoán theo cảm giác. |
| `truncated` | `no`, `yes` | Vật bị cắt bởi mép ảnh | `yes` khi **ít nhất một cạnh của box chạm biên ảnh và vật thật sự bị cắt** (không thấy hết thân/bánh). Vật nằm sát biên nhưng trọn vẹn → `no`. Box vẽ dừng đúng biên ảnh, không vẽ phần ngoài ảnh. |
| `can_review` | `true`, `false` | Đánh dấu box cần người khác xem lại | Tick `true` khi: (a) lưỡng lự giữa hai lớp; (b) ranh giới box có thể chênh > 20% một chiều; (c) `occluded_level` rơi đúng ranh giới 30% hoặc 70%; (d) vật thuộc ca chưa có quy tắc. Không tick tràn lan: mỗi lần tick phải nêu được lý do trong `image_issues.csv`. |

Cờ `occluded` của CVAT (phím `Q`) **không dùng** — script chỉ đọc `occluded_level`.

## 3. Quy tắc vẽ box

Mã quy tắc dùng tạm thời ở bản cá nhân; nhóm chốt lại mã ở Pha 2.

- **R-01 — Ôm sát phần nhìn thấy.** Box chỉ bao phần vật thật sự nhìn thấy trong ảnh, không suy diễn phần bị che hay phần ngoài khung. Phần bị che mã hóa bằng `occluded_level`, phần bị cắt bằng `truncated`. Không bao vật khác, không bao bóng đổ, không bao phần đường trống.
- **R-02 — Vật bị che.** Che 1–95% vẫn gán nếu nhận dạng chắc chắn lớp; đặt `occluded_level` theo ngưỡng mục 2. Che > 95% hoặc không chắc lớp → không gán, ghi vấn đề cấp ảnh.
- **R-03 — Cắt mép ảnh.** Box dừng ở biên ảnh, `truncated = yes`. Vật chỉ còn một phần rất nhỏ (< 20 px chiều cao nhìn thấy) → xử theo R-07.
- **R-04 — Người đi xe máy: 2 box.** Một box `motorcycle` ôm cả xe (2 bánh, yên, tay lái, phần thân xe); một box `person` chỉ ôm phần cơ thể người nhìn thấy — **không** ôm xe, không ôm mũ bảo hiểm rời. Nếu người ngồi sau (xe ôm) → thêm một box `person` riêng, cùng quy tắc. Không gộp người và xe thành một box.
- **R-05 — Người ngồi trong xe kín.** Chỉ thấy qua kính, không rõ thân người → **không gán** `person`. Thấy rõ ≥ 50% thân trên qua cửa sổ mở hoặc ca-bin hở → gán `person` với `occluded_level = 2`. Ca này là chỗ v0 mơ hồ (v0 ghi "người ngồi trên xe"), đưa ra Pha 2 chốt.
- **R-06 — Xe chở xe (car carrier).** Một box `truck` ôm toàn bộ xe vận chuyển: ca-bin, khung chở, bánh. Mỗi xe con chở trên đó, nếu nhìn thấy **≥ 50% thân xe**, gán một box `car` riêng — box `car` được phép nằm trong box `truck` (box lồng nhau là hợp lệ). Xe con bị che > 50% bởi khung/ xe khác: vẫn gán nếu nhận dạng được, `occluded_level` theo R-02. Lý do: mô hình cần phát hiện từng xe con, không chỉ xe vận chuyển.
- **R-07 — Vật quá nhỏ.** Vật có chiều cao nhìn thấy **< 20 px** (`rules.min_box_height_px = 20`): không gán box riêng. Nếu là cụm dày đặc → một `ignore_region` ôm cụm. Nếu lẻ tẻ → bỏ qua, ghi `image_issues.csv` nếu có thể gây tranh luận.
- **R-08 — Đám đông.** Từ 8 người trở lên đứng sát nhau, không tách được từng người → một `ignore_region` ôm cả cụm, không vẽ box lẻ. Dưới 8 người tách được → vẽ từng `person`.
- **R-09 — Tượng, ma-nơ-canh, đồ chơi, hình in.** Không gán `person` trong mọi trường hợp, kể cả khi rất giống người thật. Ghi `image_issues.csv` nếu vật chiếm > 10% ảnh.
- **R-10 — Phản chiếu.** Không gán vật chỉ thấy qua gương chiếu hậu, kính xe, mặt nước, kính cửa hàng. Xe chủ (ego vehicle) và gương của xe chủ không gán box. Vật thật nằm trực tiếp trong khung ảnh vẫn gán bình thường.
- **R-11 — Xe bị che một phần bởi xe khác.** Gán bình thường với `occluded_level` tương ứng; không cắt box theo đường che.
- **R-12 — Motion blur / ảnh mờ.** Vẫn gán nếu nhận dạng được lớp; đặt `can_review = true` nếu chỉ đoán được lớp chứ không chắc. Ảnh mờ hoàn toàn không nhận dạng được → không gán, ghi `image_issues.csv`.
- **R-13 — `ignore_region` chỉ dùng đúng mục đích.** Chỉ cho đám đông/cụm vật dưới 20 px/ vật không thuộc lớp nào chiếm vùng lớn. Không dùng `ignore_region` để che lỗi bỏ sót vật to, rõ; không đặt `ignore_region` phủ lên box của người khác.
- **R-14 — Thứ tự vẽ.** Vẽ từ vật lớn đến vật nhỏ, lưu `Ctrl+S` sau mỗi ảnh. Box không được vượt biên ảnh (script `build_final.py` sẽ từ chối cả lô nếu có box vượt biên).

Ảnh không có vật thật (0 box) vẫn phải có mặt trong Task và trong COCO export: **img_017, img_020, img_027, img_033, img_038** (danh sách theo mô tả lab — người viết phải tự kiểm lại từng ảnh).

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_002 | Xe đầu kéo chở ô tô trên 2 sàn | R-06 | 1 `truck` + mỗi xe con thấy ≥ 50% thân là 1 `car` | Xe con là vật thật, mô hình phải phát hiện được; box lồng nhau hợp lệ |
| img_004 | Tuk-tuk 3 bánh chở khách | đề xuất `tuk_tuk` | Chờ Pha 2 chốt lớp; tạm `can_review` | v0 không có lớp phù hợp, gán `truck`/`car` đều sai nghĩa |
| img_006 | Xe đạp / xích lô không động cơ | — | Không gán box, ghi `image_issues.csv` | Không thuộc lớp nào trong taxonomy |
| img_009 | Xe buýt cỡ lớn | đề xuất `bus` | Chờ Pha 2; tạm `can_review` | v0 thiếu lớp `bus` |
| img_011 | Tượng đồng | R-09 | Không gán | Vật không thật, không phải người |
| img_014, img_015 | Motion blur | R-12 | Gán nếu nhận dạng được, `can_review = true` | Chất lượng ảnh kém, dễ lệch |
| img_016 | Tuk-tuk / bán tải nắp thùng cao | R-09, đề xuất `tuk_tuk` | Tách ca: tuk-tuk chờ lớp mới; bán tải nắp cao → `truck` | Nắp thùng cao làm thân xe giống xe tải |
| img_017 | Tượng đá | R-09 | Không gán, ảnh 0 box | Không phải người thật |
| img_018 | Chân dung trên biển quảng cáo | R-09 | Không gán `person` | Hình in 2D, không phải người |
| img_020 | Phản chiếu qua gương chiếu hậu | R-10 | Không gán; xe chủ và gương không gán | Chỉ thấy vật qua gương, không phải vật trong khung |
| img_024 | Xe chở thân vỏ ô tô trên nóc | R-06 | Chỉ gán `truck`; thân vỏ rỗng không gán `car` | Thân vỏ không phải xe hoàn chỉnh |
| img_027 | Tượng xe bán tải | R-09 | Không gán | Tượng, không phải phương tiện |
| img_029, img_039 | Xe đạp / xích lô | — | Không gán, ghi `image_issues.csv` | Ngoài taxonomy |
| img_031 | Xe buýt | đề xuất `bus` | Chờ Pha 2; tạm `can_review` | Như img_009 |
| img_033 | Ma-nơ-canh trong tủ kính | R-09 | Không gán | Vật trưng bày |
| img_035 | Tuk-tuk chở bao tải cao trên nóc | R-01, đề xuất `tuk_tuk` | Box `tuk_tuk` chỉ ôm thân xe, **không** bao khối bao tải; bao tải không gán | Bao tải là hàng hóa, không phải phần xe |
| img_037 | Bán tải nắp thùng cao + xe buýt | R-01 + ca chờ chốt | Bán tải → `truck`; xe buýt → đề xuất `bus` | Nắp thùng cao làm ranh giới `van`/`truck` mơ hồ |
| img_038 | Tủ kính đồ chơi, xe mô hình | R-09 | Không gán, ảnh 0 box | Đồ chơi, không phải phương tiện thật |
| img_040 | Xe buýt | đề xuất `bus` | Chờ Pha 2; tạm `can_review` | Như img_009 |

Ca cần hỏi reviewer (không tự quyết): lớp cho tuk-tuk, lớp cho xe buýt, người ngồi trong xe kín (R-05), ranh giới `van`/`truck` với bán tải nắp thùng cao.

Ca loại theo quy tắc (tự tin loại, không cần hỏi): tượng, ma-nơ-canh, đồ chơi, hình in quảng cáo, phản chiếu gương, xe đạp không động cơ.

## 5. QC và phiên bản

Ngưỡng QC áp dụng (lấy từ `submission/taxonomy.json` mục `rules`, không đổi):

| Ngưỡng | Giá trị | Dùng ở đâu |
|---|---|---|
| `min_box_height_px` | 20 | R-07, cảnh báo box quá nhỏ |
| `match_iou` | 0.5 | Ghép cặp box giữa 2 người gán |
| `iaa_iou` | 0.85 | IoU trung bình phải đạt |
| `iaa_class` | 0.95 | Tỉ lệ cùng lớp phải đạt |
| `error_rate_img_max` | 0.02 | Vượt 2% ảnh lỗi → Rework |
| `iou_thr_large` / `iou_thr_small` | 0.85 / 0.7 | QC box lớn / nhỏ |
| `large_px` | 50 | Ranh giới box lớn / nhỏ |

- Ai quyết ca mơ hồ: người viết guideline v1.0 (nhóm trưởng) + người review cuối; mọi ca phải có một dòng trong `calibration_decisions.csv` với `quy_tac_ghi_vao_guideline`.
- Script kiểm được: cấu trúc COCO, biên ảnh, lớp/thuộc tính, đủ lượt gán, IoU, bỏ sót/thừa. Script **không** kiểm được: box có ôm sát vật thật không, vật mà cả nhóm cùng bỏ sót, cả nhóm cùng hiểu sai.
- Ca nào sửa quy tắc (đổi cách chọn vật, lớp, ranh giới box, thuộc tính) → tăng phiên bản guideline; nếu là `semantic` thì phải kiểm lại cả 40 ảnh.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản giảng viên: 5 lớp, 3 thuộc tính định tính | Bản khởi đầu |
| v0.1 | Thêm ngưỡng phần trăm cho `occluded_level`, 14 quy tắc vẽ box, bảng ca khó | v0 không trả lời: tuk-tuk, xe buýt, xe chở xe, tượng, phản chiếu, người ngồi trong xe |
