# Guideline gán nhãn — v0.1 — 070

- Phiên bản: v0.1 (bản cá nhân đầu tiên, Pha 1)
- Ngày: 16/11/2026
- Người viết / duyệt: 070 (tự viết, chưa qua duyệt)

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình **phát hiện vật 2D** (bounding box) trên ảnh đường phố, cho camera giao thông hoặc xe tự lái. Mô hình phải tìm **người và phương tiện thật đang có mặt ngoài đường**.

Hai kiểu sai nguy hiểm nhất:
- **Bỏ sót** người hoặc xe thật (người đi bộ, xe máy bị che): xe tự lái không thấy vật cản.
- **Thừa box trên vật không thật** (tượng, ma-nơ-canh, đồ chơi, hình in, phản chiếu): mô hình học phát hiện ảo, báo động giả.

Phép thử chọn **lớp hay thuộc tính**: nếu mô hình 2D phải đoán thông tin đó lúc suy luận thì là **lớp**; nếu chỉ dùng để lọc ca khó hoặc QC thì là **thuộc tính**.

## 2. Lớp và thuộc tính

### Lớp (mỗi vật đúng một lớp)

v0 có 5 lớp. Qua 40 ảnh, tôi đề xuất **thêm `bus` và `tuk_tuk`** vì v0 không xếp được các xe này vào lớp nào mà không bị chia hai cách (img_009, 031, 037, 040 với xe buýt; img_004, 016, 035, 040 với tuk-tuk).

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con chở người, thân liền khối (sedan, hatchback, SUV, taxi, xe cổ chở khách). | img_023 (Honda đen), img_015 (xe đỏ, xe bạc), img_012 (Mazda bạc), img_024 (xe cổ trong bảo tàng) | Minivan 7+ chỗ → `van`; xe có thùng hàng tách → `truck` |
| `van` | Xe thùng kín cỡ nhỏ / minivan có cabin và khoang chở liền khối. | img_005 (minivan trắng phía sau), img_016 (minivan trắng) | Pickup có canopy (img_037) → `truck` vì cabin tách khoang hàng |
| `truck` | Xe có cabin tách riêng khoang hàng: xe tải, bán tải, bán tải có canopy hoặc bạt, đầu kéo. | img_001 (bán tải cũ), img_007 (cả xe Isuzu và bán tải), img_012 (bán tải phía trước), img_036 (xe tải xanh phủ bạt), img_037 (bán tải canopy), img_002 (đầu kéo chở xe) | Xe thùng kín liền khối → `van` |
| `bus` (đề xuất) | Xe chở khách thân dài, có hàng cửa sổ bên liên tục (xe buýt, xe khách, minibus kiểu Coaster). | img_009, img_031 (xa, bên phải), img_037 (xe xanh phía sau), img_040 (xe vàng phía sau) | Minivan (img_005, 016) → `van` |
| `tuk_tuk` (đề xuất) | Xe 3 bánh có động cơ, có mui hoặc khung, chở khách hoặc hàng. | img_004 (hai xe xanh), img_016 (xanh lá và xe bên trái), img_035 (hai xe vàng), img_040 (xe vàng sau taxi) | Xe máy có sidecar → `motorcycle`; xích lô đạp (img_023) không có lớp |
| `motorcycle` | Xe máy, mô tô, xe tay ga, kể cả xe có thùng bên (sidecar). Chỉ phần **xe**, không gồm người. | img_006, img_021, img_026, img_022 (xe có sidecar, 1 box ôm cả thùng bên) | Xe đạp, xích lô, xe đẩy: không có lớp |
| `person` | Người thật: đi bộ, đứng, ngồi trên xe, ngồi trong xe nếu thấy rõ. Mỗi người một box. | img_034 (người qua đường), img_014 (hai người đứng), img_005 (người đội mũ che mặt), img_004 (tài xế trong tuk-tuk) | Tượng, ma-nơ-canh, ảnh in, mascot nhồi bông |
| `ignore_region` | Vùng không gán từng vật: đám đông, cụm vật nhỏ dưới 20 px, vùng mờ không nhận dạng được. Bỏ sót trong vùng này không tính là lỗi. | img_032 (đám đông ở trạm), img_039 (người, xe xa), img_030 (dãy xe máy phía xa) | Không dùng để "né" vật rõ ràng ở gần |

**Vật không thuộc lớp nào** (xe đạp, xích lô đạp, xe đẩy, gánh hàng, hàng hóa, biển hiệu): **không gán**, không vẽ `ignore_region`. Nếu vật đó che hoặc nằm cạnh vật cần gán thì chỉ vẽ box cho vật có lớp. Ca nghi ngờ: tick `can_review` trên box liên quan, hoặc ghi vấn đề cấp ảnh.

### Thuộc tính

| Thuộc tính | Mức | Ngưỡng đo được |
|---|---|---|
| `occluded_level` | `0` | che ≤ 5% diện tích vật |
| | `1` | che > 5% đến 30% |
| | `2` | che > 30% đến 70% |
| | `3` | che > 70%, nhưng vẫn nhận ra chắc chắn lớp (nhìn thấy bánh xe, mũ bảo hiểm, đèn…). Nếu không nhận ra chắc → không gán, đưa vào `ignore_region` |
| `truncated` | `no` | vật nằm trọn trong ảnh, hoặc mất dưới 10% (ước theo chiều rộng hoặc cao) |
| | `yes` | phần ngoài mép ảnh ≥ 10% |
| `can_review` | tick | tôi không chắc lớp, ranh giới box hay có nên gán; ca cần họp. Không tick cho ca đã có quy tắc rõ |

Chỉ dùng thuộc tính `occluded_level` của nhóm, **không** dùng cờ `occluded` có sẵn của CVAT (phím `Q`).

## 3. Quy tắc vẽ box

- **P-01. Chỉ gán vật thật.** Không gán tượng, mô hình, đồ chơi, ma-nơ-canh, hình in trên biển hay xe, phản chiếu trong gương hoặc kính. Xe tĩnh đậu thật vẫn gán. Xe trong bảo tàng nhưng là xe thật (img_024) vẫn gán.
- **P-02. Người đi xe máy:** vẽ **một box `motorcycle`** ôm phần xe (từ bánh trước tới bánh sau, tay lái tới yên), và **một box `person` cho mỗi người** ngồi trên xe (kể cả người ngồi sau). Cho phép các box chồng lên nhau. Lý do: mô hình cần tách người và xe.
- **P-03. Box ôm sát phần nhìn thấy.** Vật bị che: vẽ phần thấy được, không đoán phần khuất. Cạnh box chạm mép vật, lệch tối đa vài pixel.
- **P-04. Vật cắt mép ảnh:** vẽ phần trong ảnh, không vẽ ra ngoài mép; đặt `truncated=yes` nếu mất ≥ 10%.
- **P-05. Vật nhỏ:** box cao < 20 px thì không vẽ từng vật. Nếu có cụm ≥ 3 vật nhỏ liền nhau thì dùng **một** `ignore_region` bao cụm.
- **P-06. Đám đông / cụm dày đặc:** vật nào còn tách ra được và cao ≥ 20 px thì vẽ box riêng. Phần chồng chéo không phân biệt được, hoặc cụm quá nhỏ (đám đông ở xa) thì `ignore_region`.
- **P-07. Xe chở xe và hàng quá khổ:** box `truck` ôm đầu kéo và khung chở, **không bao hàng** nhô ra khỏi thùng hoặc mui. Mỗi **ô tô được chở** nhìn thấy ≥ 30% vẫn gán box `car` riêng (box lồng nhau là hợp lệ). Hàng hóa không thuộc lớp (bao tải, ống dài) không gán, và không tính vào box xe.
- **P-08. Phân loại xe có thùng:** hỏi "cabin và khoang hàng tách rời hay liền khối?". Tách rời (kể cả bán tải có canopy) → `truck`; liền khối → `van`. Xe chở khách thân dài → `bus`.
- **P-09. Tuk-tuk và xe không có lớp:** xe 3 bánh có động cơ → `tuk_tuk`. Xe đạp, xích lô đạp, xe đẩy: không gán xe; người đạp hoặc đẩy vẫn gán `person`.
- **P-10. Xe giả tưởng nhưng chạy thật trên đường** (có biển số, có người lái): gán `car` và tick `can_review`. Mascot, thú nhồi bông ngồi trong xe: không gán.
- **P-11. Xe chủ (ego) và gương:** phần thân xe, gương chiếu hậu của xe đang chụp ảnh không gán. Vật trong hình phản chiếu của gương không gán.
- **P-12. Mờ chuyển động:** vật mờ nhưng nhận ra chắc lớp thì gán, ôm phần mờ nhìn thấy, tick `can_review`. Vệt mờ không nhận ra → `ignore_region`.

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_035 | Tuk-tuk vàng chở khối bao tải cao hơn thân xe nhiều lần | P-07, P-09 | Box `tuk_tuk` ôm thân xe tới mui, không bao khối bao tải; tick `can_review` | Hàng không phải lớp; bao cả khối làm box phình sai kích thước xe |
| img_016 | Hai tuk-tuk (bên trái chồng với minivan, bên phải xanh lá bị người che một phần), xe tay ga, người cắt mép phải-dưới | P-02, P-04, P-08, P-09 | `tuk_tuk` × 2, `van` × 1, `motorcycle` + `person` cho người đi xe tay ga, người cắt mép gán `person` + `truncated=yes` | Cabin minivan liền khối → `van`; vật chồng thì vẽ phần nhìn thấy |
| img_037 | Bán tải trắng có canopy cao, bus xanh phía sau (xa), người đi bộ | P-08 | Bán tải → `truck`; bus xanh → `bus`; người đi bộ → `person` | Cabin tách khoang hàng; canopy chỉ là phần thêm của khoang hàng |
| img_040 | Tuk-tuk vàng sau taxi và người đội mũ bảo hiểm, bus vàng ở xa, người ngồi xe máy bị cắt mép | P-03, P-04, P-09 | Gán `car` (taxi), `tuk_tuk`, `bus`, `person` + `truncated=yes`, xe máy `motorcycle` cắt mép; ảnh in mặt người trên kính taxi không gán | Vật nào còn thấy rõ ≥ 30% thì vẽ; hình in không phải người |
| img_004 | Hai tuk-tuk xanh có tài xế ngồi trong | P-02, P-09 | `tuk_tuk` × 2, `person` cho tài xế nhìn rõ | Người ngồi trong xe nhìn rõ qua khung mở thì gán |
| img_009 | Minibus kem ở giữa đường, có người trên xe máy phía sau, vật xa | P-05, P-08 | `bus` (xe khách); người xa < 20 px → `ignore_region` hoặc bỏ | Thân dài với hàng cửa sổ liên tục |
| img_002 | Xe đầu kéo Renault chở 8 ô tô trên hai sàn | P-07 | 1 `truck` ôm đầu kéo và khung chở; mỗi ô tô nhìn thấy ≥ 30% → 1 `car` | Hai người dễ vẽ khác nhau (1 box hay 9 box); chốt để mô hình học nhận ô tô kể cả khi nằm trên xe |
| img_017 | Tượng người cưỡi ngựa (có nón giao thông trên đầu) | P-01 | Không gán gì (không `person`) | Tượng không phải người thật; hai người dễ cùng vẽ sai |
| img_027, img_028 | Tượng/bia mộ hình pickup (027); tượng ngựa đứng trên thùng xe pickup thật (028) | P-01 | 027: không gán. 028: gán `truck` cho pickup, không gán ngựa | Chỉ xe thật mới gán |
| img_033, img_038 | Ma-nơ-canh và phản chiếu trong kính (033); tủ trưng bày xe mô hình, đồ chơi (038) | P-01 | Không gán | Không phải người hoặc xe thật |
| img_019 | Xe màu vàng hình dáng giả tưởng chạy diễu hành, có biển số, tài xế và mascot nhồi bông trong xe; khán giả sau rào | P-06, P-10 | `car` (tick `can_review`), `person` cho tài xế; mascot không gán; đám đông sau rào → `ignore_region` hoặc box riêng cho người ở gần | Xe chạy thật có biển số; cần họp nhóm |
| img_024 | Xe wagon đen, trên nóc có xe nhỏ màu vàng (mô hình), xe cổ khác phía sau | P-01 | `car` cho wagon đen và các xe cổ nhìn rõ; xe vàng trên nóc không gán, tick `can_review` | Xe trên nóc là mô hình hoặc vật trưng bày, không phải xe đang lưu thông |
| img_020 | Gương chiếu hậu có phản chiếu xe, cảnh đường | P-01, P-11 | Không gán | Phản chiếu không phải vật thật |
| img_014, img_015 | Người đứng sắc nét, xe máy mờ chuyển động (014); xe đỏ và bạc cắt mép + xe mờ phía sau (015) | P-03, P-04, P-12 | 014: 2 `person` rõ; vệt mờ → `ignore_region`. 015: `car` × 2 cắt mép (`truncated=yes`), xe nền nhận ra thì gán, tick `can_review` | Mờ chuyển động làm biên không rõ |
| img_021, img_030, img_032 | Dòng xe máy kẹt dày (021), bãi đỗ xe máy dày (030), đám đông ở trạm (032) | P-05, P-06 | Gán các vật phía gần tách được và cao ≥ 20 px; phần xa dày đặc → `ignore_region` | Tránh vẽ hàng trăm box không chắc |
| img_005, img_026 | Nhiều người đội mũ che mặt chồng nhau (005); xe máy chở hai người, bị cắt và mờ ở góc (026) | P-02, P-03, P-04 | Mỗi người nhìn thấy rõ 1 `person`, mỗi xe 1 `motorcycle`; xe cắt mép `truncated=yes` | Chồng lấn nặng; ghi `occluded_level` theo ngưỡng |
| img_023, img_029, img_006 | Xích lô đạp (023); người vác ống dài trên xe đạp và xe máy (029); xe đạp trong dòng xe (006) | P-09 | Xích lô, xe đạp không gán; người đạp gán `person`; ống dài không gán | Xe đạp, xích lô không có lớp |
| img_018, img_031, img_034, img_025, img_039, img_013 | Ảnh quảng cáo có mặt người và xe phía sau hàng rào (018); đường đêm xa (031); người qua đường, xe xa (034); nhiều người, xe xa (025, 039, 013) | P-01, P-05, P-06 | Không gán chân dung trên biển; người, xe ≥ 20 px gán; < 20 px → `ignore_region` | Vật quá nhỏ gán sai nhiều hơn là đúng |

## 5. QC và phiên bản

- Ngưỡng QC áp dụng (theo `taxonomy.json`, không đổi): IoU ≥ 0.85 với box cao ≥ 50 px, ≥ 0.7 với box nhỏ hơn; IAA IoU trung bình ≥ 0.85 và cùng lớp ≥ 95% trên cặp box ghép 1–1 (IoU ≥ 0.5); vật nhỏ < 20 px; lỗi theo ảnh ≤ 2%.
- Ai quyết ca mơ hồ: ca tôi không chắc thì tick `can_review` (trên box) hoặc ghi vấn đề cấp ảnh; ca nhiều người bất đồng thì đưa ra họp nhóm Pha 2, nhóm chốt bằng mã `R-xx`.
- Bản này giữ nguyên sau Pha 1 để đối chiếu với quyết định nhóm.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu của giảng viên | — |
| v0.1 (070) | Đề xuất thêm lớp `bus`, `tuk_tuk`; ngưỡng `occluded_level`, `truncated`; 12 quy tắc P-01…P-12; bảng ca khó | img_002, 004, 009, 016, 017, 019, 024, 035, 037, 040 và các ảnh khác trong bảng mục 4 |