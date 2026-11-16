# Guideline gán nhãn — v0.2 (bản cá nhân, Pha 1) — mã 102

- Phiên bản: v0.2-102 (sửa từ v0)
- Ngày: 2026-11-16
- Người viết / duyệt: 102 / chưa duyệt (chờ họp nhóm Pha 2)

## 1. Mục tiêu
Nhãn dùng huấn luyện mô hình phát hiện vật 2D (bounding box) cho camera giao thông / xe tự lái: tìm **người và phương tiện thật đang có mặt trên đường**.
Sai nguy hiểm nhất ở hai chỗ: (a) gán nhãn cho vật giả (tượng, đồ chơi, hình in, phản chiếu) làm mô hình báo động giả; (b) bỏ sót hoặc gộp nhầm người đi xe máy trong dòng xe dày, làm mô hình đếm thiếu / sai.

## 2. Lớp và thuộc tính

### Lớp
Mỗi vật thật thuộc đúng một lớp. Chỉ dùng 6 lớp của taxonomy v0.

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con chở người, thân kín, gồm sedan, hatchback, SUV, taxi con. | img_007 (xe Mazda), img_031 (taxi trắng), img_019 (xe thật chạy lễ hội, có tài xế) | Pickup có thùng hở → `truck`. Xe mô hình / xe trên kệ → không gán (R-06). |
| `truck` | Xe có khoang chở hàng riêng: tải, bán tải (pickup, kể cả có nắp/bạt), xe đầu kéo, xe chở xe. | img_002 (xe chở xe), img_013 (bán tải), img_035 (tải nhỏ phủ bạt), img_036 (bán tải có nắp) | SUV → `car`. Xe buýt → ngoài lớp (R-04). |
| `van` | Xe thùng kín cỡ nhỏ, khoang hành khách/hàng liền khối với cabin (minivan, xe tải van). | img_005 (van bạc) | Pickup có nắp thùng (img_036) vẫn là `truck` vì cabin tách khỏi thùng. Xe buýt mini (img_009) → ngoài lớp. |
| `motorcycle` | Xe hai bánh có động cơ (xe máy, tay ga, mô tô), kể cả có thùng bên (sidecar). | img_006, img_010, img_022 (có sidecar) | Xe đạp, xích lô, xe đạp điện không bánh phụ → ngoài lớp (R-04). |
| `person` | Người thật, đi bộ hoặc ngồi trên xe **hở** (xe máy, xe đạp, xích lô, tuk-tuk). | img_014 (hai người đi bộ), img_011 (người ngồi xe máy) | Người ngồi trong xe kín (xuyên kính) → không gán (R-07). Ma-nơ-canh, tượng, ảnh in → không gán (R-06). |
| `ignore_region` | Vùng chứa nhiều vật không tách nổi hoặc vật giả hàng loạt; bỏ sót trong vùng này không tính lỗi. | img_030 (bãi xe máy dày), img_037 (kệ xe đồ chơi) | Không dùng để "né" ca khó mà vẫn nhìn rõ — vật nhìn rõ phải có box. |

**Vật không thuộc lớp nào** (xe buýt, tuk-tuk/xe ba bánh, xe đạp, xích lô, động vật): **không vẽ box, không ép vào lớp gần nhất**. Ghi vào `image_issues.csv` (ảnh, vùng, lý do) và đề xuất nhóm thêm lớp mới ở Pha 2 (R-04). Nếu nằm trong cụm không tách được thì cho vào `ignore_region`.

### Thuộc tính
**`occluded_level`** (tỉ lệ diện tích vật bị che, ước lượng bằng mắt trên hộp đầy đủ của vật):

| Mức | Nghĩa |
|---|---|
| 0 | Che dưới 10% (thấy gần trọn). |
| 1 | Che 10% đến dưới 40%. |
| 2 | Che 40% đến 80%, vẫn nhận ra lớp. |
| 3 | Che trên 80%, hoặc phải đoán lớp. **Không gán box**; nếu có cả cụm thì dùng `ignore_region`. Riêng vật 3 nhưng chắc chắn lớp thì vẽ box và tick `can_review`. |

**`truncated`**: `yes` khi vật bị cắt bởi **mép ảnh** và phần bị cắt dài ≥ 5% kích thước vật (ví dụ img_040 xe taxi mất nửa dưới); còn lại `no`. Bị vật khác che **không** phải truncated.

**`can_review`**: tick khi lớp, ranh giới vật/vật giả, hoặc mức che chưa chắc (R-09).

## 3. Quy tắc vẽ box
- **R-01 Ôm sát phần nhìn thấy.** Box ôm phần nhìn thấy của vật; không đoán phần bị che. Sai lệch cho phép theo ngưỡng taxonomy (IoU ≥ 0.85 vật cao ≥ 50 px; ≥ 0.7 vật nhỏ hơn).
- **R-02 Người đi xe máy = nhiều box.** Mỗi người (cả người ngồi sau, cả trẻ em) một box `person` bao đầu tới chân thấy được; xe một box `motorcycle` bao thân xe, bánh, tay lái. Các box được phép chồng nhau. Hàng hóa, túi, ba lô đeo trên người thì nằm trong box người; hàng chằng buộc sau xe thì nằm trong box xe (ví dụ img_011, img_026, img_006).
- **R-03 Vật bị che / cắt mép.** Vẽ box phần nhìn thấy, ghi `occluded_level`; cắt mép thì box dừng đúng tại mép ảnh, `truncated=yes`.
- **R-04 Ngoài lớp.** Xe buýt, tuk-tuk, xe ba bánh, xe đạp, xích lô: không box, ghi issue (img_004, img_009, img_023, img_031, img_035). Người ngồi/đạp trên chúng vẫn là `person` (R-07).
- **R-05 Vật quá nhỏ.** Box cao < 20 px (`min_box_height_px`) thì không gán; nếu thuộc cụm đông thì cho vào `ignore_region` (img_021 phía xa, img_034 phía xa).
- **R-06 Vật giả.** Tượng, ma-nơ-canh, xe đồ chơi/mô hình, hình in trên biển quảng cáo, phản chiếu (kính, gương), mộ/điêu khắc hình xe: **không gán** (img_012, img_016, img_017, img_018, img_027, img_033, img_037). Xe thật nhưng là xe hóa trang/diễu hành vẫn đi trên đường (img_019) → gán `car`, hình nhân gắn trên xe không gán.
- **R-07 Người và xe.** Người ngồi trong xe kín (nhìn qua kính) không gán `person`; box `car/truck/van` bao cả xe. Người ngồi trên xe hở (xe máy, xe đạp, xích lô, tuk-tuk) gán `person` riêng.
- **R-08 Vật chở trên vật.** Xe/hàng được chở trên xe khác (xe chở xe, xe trên nóc, tượng/ngựa trên thùng) **không gán riêng**; box của xe chở bao thân xe, **không** nới ra để ôm hàng thò ra ngoài (img_002, img_024, img_028, img_029, img_035).
- **R-09 Xe chủ (ego) và đám đông.** Phần xe chủ thấy trong ảnh (gương, đầu xe, thùng xe mình đứng) không gán; chưa chắc là xe chủ hay xe khác thì gán và tick `can_review` (img_013, img_018). Đám đông/dòng xe dày: gán từng vật cao ≥ 20 px còn tách được, phần không tách được → `ignore_region` (img_021, img_030, img_032).
- **R-10 Nhòe chuyển động.** Vật nhòe nhưng vẫn nhận ra lớp → gán, `occluded_level` không tính nhòe, tick `can_review` (img_014).

## 4. Ca khó
| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_011 | Hai người ngồi xe máy, một người đứng cạnh sạp chuối | R-02 | 1 `motorcycle` + 2 `person` (người lái, người sau) + 1 `person` đứng; box được chồng | v0 không nói số box; tách để mô hình học riêng người và xe |
| img_004 | Hai xe tuk-tuk, tài xế ngồi trong | R-04, R-07 | Không box xe; tài xế `person` (tick `can_review`); ghi issue "chưa có lớp tuk-tuk" | Ép vào `motorcycle`/`car` làm sai định nghĩa lớp |
| img_002 | Xe chở xe, 6 ô tô trên giàn, người đứng bên phải | R-08 | 1 `truck` bao cả xe + giàn; ô tô trên giàn không gán; 1 `person` bên phải | Ô tô là hàng hóa; gán sẽ báo trùng với box xe tải |
| img_024 | Ô tô đen, trên nóc có xe đồ chơi/mô hình màu vàng | R-06, R-08 | 1 `car` (đen), box dừng ở nóc xe; xe vàng không gán | Vật giả, và là hàng chở trên xe |
| img_033 | Ma-nơ-canh, phản chiếu kính, gương xe tải | R-06 | Không gán gì; ghi issue cấp ảnh "không có vật thật" | Chỉ có ma-nơ-canh và phản chiếu |
| img_037 | Kệ kính chứa xe mô hình và đồ chơi | R-06 | 1 `ignore_region` bao kệ; không gán từng xe | Nhìn giống xe thật nhưng là mô hình |
| img_017 | Tượng người cưỡi ngựa, nón giao thông trên đầu | R-06 | Không gán gì | Tượng, không phải người/xe thật |
| img_027 | Mộ điêu khắc hình xe bán tải | R-06 | Không gán gì | Điêu khắc, không phải xe |
| img_028 | Xe bán tải cổ, trên thùng có tượng ngựa | R-06, R-08 | 1 `truck`; ngựa không gán | Ngựa là tượng chở trên xe |
| img_021 | Dòng xe máy rất dày giờ cao điểm | R-05, R-09 | Gán xe và người phía trước (cao ≥ 20 px, thấy rõ); phía xa → `ignore_region` | Không thể tách chính xác từng vật xa |
| img_030 | Bãi gửi xe máy dày đặc | R-03, R-09 | Gán xe hàng trước (occluded 1–2); phía sau → `ignore_region` | Che lẫn nhau nhiều, nhiều xe mức 3 |
| img_032 | Đám đông chờ xe buýt, hàng sau bị che | R-03, R-09 | Gán người hàng trước; cụm sau không tách được → `ignore_region` | Che lẫn nhau, ranh giới người không rõ |
| img_022 | Xe máy sidecar, ảnh đen trắng cũ, người ngồi xa | R-02, R-03 | 1 `motorcycle` bao cả sidecar; `person` nếu cao ≥ 20 px, tick `can_review` | Sidecar là một phần xe; người nhỏ, che nhiều |
| img_018 | Gương chiếu hậu thấy xe phía sau | R-06, R-09 | Không gán; xe trong gương chỉ là phản chiếu | Phản chiếu, kèm xe chủ |
| img_013 | Thùng bán tải ở tiền cảnh, xe khác phía trước | R-09 | Xe phía trước (bán tải, Mazda) gán; thùng tiền cảnh không gán; tick `can_review` | Có thể là xe chủ |
| img_040 | Mũ bảo hiểm người đi xe che gần hết ảnh, taxi, tuk-tuk bị cắt mép | R-03 | `person` (occluded 1); taxi `car` `truncated=yes`; tuk-tuk không gán (R-04) | Cắt mép và che nhiều |
| img_029 | Ống dài vắt qua hai người đi xe máy và xe đạp | R-02, R-04 | 1 `motorcycle` + 2 `person`; ống không nằm trong box; xe đạp không gán | Hàng hóa không thuộc lớp nào |

## 5. QC và phiên bản
- Áp dụng ngưỡng QC trong `taxonomy.json` (giữ nguyên `rules`): `min_box_height_px=20`, `iou_thr_large=0.85` (vật cao ≥ `large_px=50`), `iou_thr_small=0.7`, IAA `iaa_iou=0.85`, `iaa_class=0.95`, lỗi tối đa `error_rate_img_max=2%`.
- Ca mơ hồ: tick `can_review`; ca không vẽ được box thì ghi vào `image_issues.csv`. Người quyết ca khó là người điều phối của nhóm (ghi vào `calibration_decisions.csv`).
- Quy tắc nào đổi cách chọn vật, lớp, box hoặc thuộc tính (ví dụ thêm lớp mới) là thay đổi **semantic**, phải tăng phiên bản và kiểm lại cả lô.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu của giảng viên | — |
| v0.2-102 | Thêm ngưỡng thuộc tính, R-01…R-10, 17 ca khó | img_004, img_011, img_002, img_033, img_037, img_021 |
