# Guideline gán nhãn — v1.0 (đã thống nhất) — nhóm G003

- Phiên bản: v1.0
- Ngày: 2026-11-16
- Người viết / duyệt: 343 soạn / cả nhóm G003 duyệt ở Pha 2; người điều phối: 069
- Loại nhãn: bounding box trên ảnh đường phố · CVAT, xuất COCO 1.0
- Trạng thái: **khóa** cho lượt gán độc lập ở Pha 3. Mọi thay đổi sau thời điểm này phải tăng phiên bản (xem mục 5).

---

## 1. Mục tiêu

Huấn luyện mô hình **phát hiện người và phương tiện** trên ảnh đường phố 2D (camera giao thông, xe tự lái),
bối cảnh Việt Nam / Đông Nam Á. Mô hình phải tách được **người đi bộ** (`person`) khỏi **người đang ở trên xe**
(`rider`), vì hai nhóm này di chuyển với tốc độ và hướng khác nhau.

Sai nguy hiểm nhất:

- Bỏ sót người hoặc xe thật.
- Box hụt phần hàng chở trên xe.
- Gán box cho mô hình, tượng, đồ chơi, hình in, ma-nơ-canh, ảnh phản chiếu, khiến mô hình báo vật cản giả.

## 2. Lớp và thuộc tính

### Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `person` | Người thật **không** ở trên xe: đi bộ, đứng, ngồi ghế/vỉa hè, gánh hàng, dắt xe. | Cô gái đi bộ và khách ngồi quán img_001; người gánh hàng và người đứng dắt xe đạp img_003 | Người đang ngồi trên xe máy, xe đạp, xích lô → `rider`. Tượng, ma-nơ-canh, búp bê, hình in (img_017, img_033, img_038) → không gán. |
| `rider` | **Mới.** Người thật đang ngồi hoặc đứng **trên** `motorcycle`, `bicycle` hoặc `other_vehicle` không có khoang kín; gồm cả người lái và người ngồi sau. | Người đi xe máy giữa ảnh img_003; người đi xe máy nhòe img_014; người đạp xích lô img_023; tài xế tuk-tuk img_004 | Người dắt xe, đứng cạnh xe, chân không còn trên xe → `person` (img_003, người áo đỏ). Người ngồi trong `car`, `truck`, `van`, xe buýt → không gán. Tượng người cưỡi ngựa img_017 → không gán. |
| `car` | Ô tô con ≤ 9 chỗ | img_023; ô tô trên giá img_002 | Pickup → `truck`. |
| `truck` | Xe có thùng hàng tách khỏi cabin: xe tải, pickup, đầu kéo (kèm rơ-moóc = 1 box). | img_001 (pickup chở ống), img_002, img_012 | Tượng pickup img_027 → không gán. |
| `van` | Xe thùng kín cỡ nhỏ, thân liền; minibus ≤ 16 chỗ. | | SUV → `car`. |
| `motorcycle` | Xe máy, mô tô, xe máy điện: người cưỡi trên yên, không mui, không khoang khách; tính cả xe có sidecar. | img_029 (xe điện), img_022 (sidecar) | Tuk-tuk → `other_vehicle`. |
| `bicycle` | Xe đạp 2 bánh có bàn đạp, khung hở, không vỏ. | img_029 (bên phải), img_003 | Xích lô → `other_vehicle`. |
| `other_vehicle` | Xe thật không thuộc các lớp xe trên: tuk-tuk, xe lam, xích lô, ba gác, xe buýt. | img_004, img_023, img_035 | Xe mô hình, đồ chơi → không gán. |

Vật **không thuộc lớp nào** (động vật, xe đẩy tay, cọc tiêu, biển báo, mô hình, tượng, đồ chơi): **không gán**. v1.0 không
dùng vùng ignore. Vật thật không gán được (quá nhỏ, nhòe, lẫn trong đám đông) thì cũng không gán, theo R-07, R-09, R-10.

> Lưu ý kỹ thuật: `ignore_region` vẫn có trong `submission/taxonomy.json` vì script bắt buộc phải có
> (`scripts/common.py` kiểm `ignore_class`), nên nó vẫn hiện trong CVAT. **Không vẽ box lớp này.**

- **R-01 Chỉ gán vật thật; mô hình không gán box.** Mô hình xe hoặc người (kể cả mô hình cỡ thật), tượng, đồ chơi,
  hình in, ma-nơ-canh, ảnh phản chiếu → không gán box nào, dù trông giống hệt người hoặc xe.
  Ví dụ: img_017, img_018, img_027, img_033, img_038.
- **R-02 Xe lạ → `other_vehicle`**, không ép vào lớp gần giống.
- **R-03 Xe thật đang đỗ, trưng bày, xe độ** vẫn gán như xe thường, theo kết cấu gốc. Mô hình, điêu khắc hình xe → theo R-01, không gán. Không chắc là xe thật hay điêu khắc → gán và tick `can_review`.
- Không chắc lớp → chọn lớp gần nhất và tick `can_review`.

### Thuộc tính

| Thuộc tính | Giá trị | Ý nghĩa |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Phần trăm bị vật khác che: 0 là < 10%, 1 là 10–39%, 2 là 40–69%, 3 là ≥ 70% (vẫn nhận ra lớp). |
| `truncated` | `no`, `yes` | `yes` khi box chạm mép ảnh (≤ 2 px) và vật còn phần nằm ngoài khung. |
| `can_review` | tick / không | Tick khi không chắc lớp (kể cả phân vân `person` hay `rider`), không chắc biên box (nhòe, tối) hoặc gặp ca chưa có trong guideline. |

Cách tính che: `rider` và chiếc xe họ đang ở trên che nhau thì không tính; kính trong suốt, nhòe và phần ngoài
ảnh không tính. Phân vân giữa hai mức → chọn mức cao hơn.

## 3. Quy tắc vẽ box

1. **R-04** Box ôm sát phần nhìn thấy (lệch ≤ 2 px), không đoán phần bị che. Bao cả gương, biển TAXI, giá nóc; bỏ ăng-ten, bóng đổ.
2. **R-05 Người và xe hở.** Mỗi người trên xe hở 1 box `rider` + 1 box cho xe (xe máy chở 2 người = 2 `rider` + 1 `motorcycle` = 3 box).
   - Phép thử `person` / `rider`: người đang ngồi trên yên, ghế xe hoặc đứng trên sàn xe → `rider`, kể cả khi xe dừng và chân chống đất. Người đã rời xe (dắt xe, đứng cạnh, ngồi trên xe đỗ để nghỉ mà xe không có người lái) → `person`; phân vân → chọn `rider` và tick `can_review`.
   - Box `rider` gồm mũ, ba lô và phần chân trên xe; không gồm đồ cầm tay, gánh.
   - Người ngồi trong `car`, `truck`, `van`, xe buýt: không gán.
3. **R-06** Hàng đặt, buộc lên xe → bao vào box xe. Hàng người cầm, vác → không bao. Xe được chở trên xe khác vẫn gán box riêng.
4. **R-07** Vật nhòe, tối: gán nếu nhận ra lớp và thấy biên, tick `can_review`. Không tách được biên → không gán; ghi ảnh, vùng và lý do để nhóm đưa vào `submission/qc/image_issues.csv`.
5. **R-08** Vật bị cắt mép ảnh: box dừng ở mép, `truncated=yes`.
6. **R-09** Vật có box cao < 20 px → không gán, kể cả khi nhiều vật nhỏ nằm sát nhau.
7. **R-10** Đám đông, dãy xe đỗ: gán riêng từng vật tách được biên và cao ≥ 20 px. Phần còn lại không tách được thì không gán.
8. **R-11** Xe chủ (capo, taplo, gương) và ảnh phản chiếu (kính, gương, vũng nước): không gán.

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_038 | Tủ kính trưng bày: hai kệ dưới là ô tô đồ chơi; kệ trên có vịt cao su, tượng chuột, búp bê, xe ba bánh đồ chơi có hình nhân; mặt kính phản chiếu đường phố. | R-01, R-11 | Không gán box nào (kể cả búp bê, xe đồ chơi, hình phản chiếu). Ảnh vẫn có trong COCO với 0 box. | Toàn bộ là đồ chơi và phản chiếu, không có vật cản thật. Đây là ảnh đối chứng âm: mọi box trên ảnh đều tính lỗi `thua`. |
| img_017 | Tượng đồng người cưỡi ngựa, đội nón giao thông, có chim đậu trên lưng ngựa. | R-01 | Không gán: không `rider`/`person` cho tượng người, không gán ngựa và chim. | Tượng không phải người thật; dáng "người ngồi trên vật cưỡi" rất dễ bị gán nhầm `rider`. Động vật không thuộc lớp nào. |
| img_027 | Bia mộ bằng đá đen tạc hình xe pickup cỡ gần như thật, đặt trên bệ trong nghĩa trang. | R-01, R-03 | Không gán, không tick `can_review`. | Có bệ đá, không có cửa kính thật, đặt giữa bãi cỏ nghĩa trang → điêu khắc, không phải xe đỗ (R-03 chỉ áp dụng cho xe thật). Giữ làm mẫu âm cho lớp `truck`. |
| img_033 | Cửa kính cửa hàng: ma-nơ-canh trắng, ảnh in người mẫu bên trái, mặt kính phản chiếu thân xe trắng có gương chiếu hậu bên phải. | R-01, R-11 | Không gán box nào: ma-nơ-canh và người mẫu trong ảnh in không gán `person`; xe trắng chỉ là phản chiếu, không gán. | Không có người hay xe thật trong khung hình; xe nằm ngoài ảnh, chỉ thấy qua phản chiếu. Gán vào sẽ dạy mô hình báo vật cản giả. |

Ca chưa chốt: tick `can_review` trên box, hoặc ghi ảnh, vùng, lý do nếu chưa vẽ được box, rồi đưa ra họp. Dẫn mã R-xx trong nhật ký QC.

## 5. QC và phiên bản

- Ngưỡng (giữ nguyên `rules` trong `taxonomy.json`): ghép cặp IoU ≥ 0.5; IoU đạt ≥ 0.85 (box cao ≥ 50 px) hoặc ≥ 0.7 (nhỏ hơn); IAA cùng lớp ≥ 95%; lỗi theo ảnh ≤ 2%; box cao tối thiểu 20 px.
- Ca mơ hồ: người gán tick `can_review`; nhóm chốt ở Pha 2 và Pha 5; người điều phối (069) quyết khi không thống nhất.
- Mọi thay đổi làm đổi nhãn đều tăng phiên bản. Thêm hoặc bỏ lớp thì cập nhật `taxonomy.json` và chạy lại `scripts/make_cvat_labels.py`.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu. | — |
| v1.0 | Thêm lớp `bicycle`, `other_vehicle`, `rider` (`person` chỉ còn người không ở trên xe, R-05); bỏ `ignore_region` (vật < 20 px, cụm không tách được, vùng nhòe → không gán, R-07, R-09, R-10); mô hình, tượng, đồ chơi, phản chiếu không gán box (R-01, R-11); giữ `can_review`; ngưỡng đo được cho thuộc tính; chốt 4 ca khó. | Bản cá nhân lệch nhau về người trên xe: 343 gộp vào `person`, 042 dùng thuộc tính `role`, 069 tách `Driver`/`Person`. Chọn **lớp** vì mô hình phải tự đoán khi suy luận; gộp cả người ngồi sau vì nhìn ảnh khó biết ai lái (img_003, img_014, img_023, img_004). Xe lạ: img_004, img_023, img_035. Vật không thật: img_038, img_017, img_027, img_033. `ignore_region` vẫn nằm trong `taxonomy.json` do script bắt buộc nhưng không vẽ. |
