# Guideline gán nhãn — v0.1 — 343 (nhóm G003)

- Phiên bản: v0.1 (sửa từ `guideline_v0_starter.md`)
- Ngày: 2026-11-16
- Người viết / duyệt: 343 / nhóm duyệt ở Pha 2
- Loại nhãn: bounding box trên ảnh đường phố · CVAT, xuất COCO 1.0

---

## 1. Mục tiêu

Huấn luyện mô hình **phát hiện người và phương tiện** trên ảnh đường phố 2D (camera giao thông, xe tự lái),
bối cảnh Việt Nam / Đông Nam Á.

Sai nguy hiểm nhất: bỏ sót người hoặc xe thật; box hụt phần hàng chở trên xe; gán box cho tượng, đồ chơi,
hình in, ảnh phản chiếu (mô hình báo vật cản giả).

## 2. Lớp và thuộc tính

### Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa | Ví dụ | Dễ nhầm với |
|---|---|---|---|
| `person` | Người thật đi bộ, đứng, hoặc ngồi trên xe hở. | img_014; người đạp xích lô img_023 | Tượng, ma-nơ-canh, búp bê (img_038) → không gán. Người trong xe kín → không gán. |
| `car` | Ô tô con ≤ 9 chỗ. | img_023; ô tô trên giá img_002 | Pickup → `truck`. |
| `truck` | Xe có thùng hàng tách khỏi cabin: xe tải, pickup, đầu kéo (kèm rơ-moóc = 1 box). | img_002, img_012 | Tượng pickup img_027 → không gán. |
| `van` | Xe thùng kín cỡ nhỏ, thân liền; minibus ≤ 16 chỗ. | | SUV → `car`. |
| `motorcycle` | Xe máy, mô tô, xe máy điện: người cưỡi trên yên, không mui, không khoang khách; tính cả xe có sidecar. | img_029 (xe điện), img_022 (sidecar) | Tuk-tuk → `other_vehicle`. |
| `bicycle` | **Mới.** Xe đạp 2 bánh có bàn đạp, khung hở, không vỏ. | img_029 (bên phải), img_003 | Xích lô → `other_vehicle`. |
| `other_vehicle` | **Mới.** Xe thật không thuộc các lớp xe trên: tuk-tuk, xe lam, xích lô, ba gác, xe buýt. | img_004, img_023, img_035 | Xe mô hình, đồ chơi → không gán. |
| `ignore_region` | Vùng không gán từng vật; bỏ sót ở đây không tính lỗi. | Vệt nhòe img_014 | Không dùng cho tượng, đồ chơi. |

- **R-01 Chỉ gán vật thật.** Tượng, mô hình, đồ chơi, hình in, ma-nơ-canh, ảnh phản chiếu → không gán và
  **không** đặt `ignore_region` (để làm mẫu âm). Ví dụ: img_017, img_018, img_027, img_033, img_038.
- **R-02 Xe lạ → `other_vehicle`**, không ép vào lớp gần giống.
- **R-03 Xe đỗ, trưng bày, xe độ** vẫn gán như xe thường, theo kết cấu gốc. Không chắc là xe hay điêu khắc → tick `can_review`.
- Động vật, xe đẩy tay, cọc tiêu, biển báo → không gán. Không chắc lớp → chọn lớp gần nhất và tick `can_review`.

### Thuộc tính

| Thuộc tính | Giá trị | Ý nghĩa |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Phần trăm bị vật khác che: 0 là < 10%, 1 là 10–39%, 2 là 40–69%, 3 là ≥ 70% (vẫn nhận ra lớp). |
| `truncated` | `no`, `yes` | `yes` khi box chạm mép ảnh (≤ 2 px) và vật còn phần nằm ngoài khung. |
| `can_review` | tick / không | Tick khi không chắc lớp, không chắc biên box (nhòe, tối) hoặc ca chưa có trong guideline. |

Cách tính che: người và chiếc xe họ đang lái che nhau thì không tính; kính trong suốt, nhòe, phần ngoài ảnh
không tính. Phân vân giữa hai mức → chọn mức cao hơn.

## 3. Quy tắc vẽ box

1. **R-04** Box ôm sát phần nhìn thấy (lệch ≤ 2 px), không đoán phần bị che. Bao cả gương, biển TAXI, giá nóc; bỏ ăng-ten, bóng đổ.
2. **R-05** Người trên xe hở: mỗi người 1 box `person` + 1 box xe (xe máy chở 2 người = 3 box). Box `person` gồm mũ, ba lô; không gồm đồ cầm, gánh. Người trong xe kín: không gán.
3. **R-06** Hàng đặt, buộc lên xe → bao vào box xe. Hàng người cầm, vác → không bao. Xe được chở trên xe khác vẫn gán box riêng.
4. **R-07** Vật nhòe, tối: gán nếu nhận ra lớp và thấy biên, tick `can_review`. Không tách được → `ignore_region`.
5. **R-08** Vật bị cắt mép ảnh: box dừng ở mép, `truncated=yes`.
6. **R-09** Vật cao < 20 px → `ignore_region` (gộp các vật nhỏ nằm sát nhau).
7. **R-10** Đám đông, dãy xe đỗ: vật tách được gán riêng; cụm ≥ 3 vật không tách được → một `ignore_region`.
8. **R-11** Xe chủ (capo, taplo, gương) và ảnh phản chiếu: không gán.

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_004 | Tuk-tuk có tài xế ngồi trong | R-02, R-05 | 2 `other_vehicle` + 2 `person` (tài xế bên trái `occluded_level=2`). | Không phải xe máy (2 bánh) hay ô tô; xe hở hông nên thấy người lái. |
| img_035, img_002, img_012, img_029 | Xe chở hàng cồng kềnh | R-06 | Hàng chất trên xe bao vào box (img_035: box kéo tới đỉnh đống bao; img_002: `truck` bao cả xe trên giá, mỗi ô tô thêm 1 `car`). Ống do người cầm ở img_029: không bao. | Hàng chất trên xe là kích thước thật của vật cản; hàng cầm tay không gắn với dáng xe. |
| img_011 | Xe máy độ trưng bày, tượng Predator | R-03, R-01 | `motorcycle` + `can_review`; Predator không gán. **Cần reviewer.** | Xe cỡ thật nhưng biến đổi nhiều, chưa chắc là xe hay điêu khắc. |
| img_014 | Người và xe máy nhòe mạnh | R-07 | Xe ở giữa và ở mép phải: `person` + `motorcycle`, tick `can_review` (xe mép phải `truncated=yes`). Vệt nhòe bên trái: `ignore_region`. | Mô hình cần học xe nhòe, nhưng biên không chắc nên đưa vào calibration. |
| img_023 | Xích lô | R-02, R-05 | `other_vehicle` + `person` cho người đạp. | 3 bánh, có thùng khách; gộp vào `bicycle` làm lẫn lớp. |
| img_027 | Tượng đài hình xe pickup | R-01 | Không gán, không `ignore_region`. | Không phải xe thật; giữ làm mẫu âm. |
| img_038 | Tủ kính ô tô đồ chơi | R-01, R-11 | Không gán gì (kể cả búp bê, phản chiếu). Ảnh vẫn có trong COCO với 0 box. | Ảnh đối chứng âm; mọi box đều là lỗi `thua`. |

Ca chưa chốt: tick `can_review`, ghi ảnh, vùng, lý do và đưa ra họp. Dẫn mã R-xx trong nhật ký QC.

## 5. QC và phiên bản

- Ngưỡng: ghép cặp IoU ≥ 0.5; IoU đạt ≥ 0.85 (box cao ≥ 50 px) hoặc ≥ 0.7 (nhỏ hơn); IAA cùng lớp ≥ 95%; lỗi theo ảnh ≤ 2%.
- Ca mơ hồ: người gán tick `can_review`; nhóm chốt ở Pha 2 và Pha 5; người điều phối (102) quyết khi không thống nhất.
- Mọi thay đổi làm đổi nhãn đều tăng phiên bản. Thêm lớp mới thì cập nhật `taxonomy.json`.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu | — |
| v0.1 | Thêm `bicycle`, `other_vehicle`; ngưỡng thuộc tính; R-01…R-11; 7 ca khó | img_004, img_023, img_035 (xe lạ); img_029 (hàng); img_011, img_027, img_038 (vật không thật); img_014 (nhòe) |
