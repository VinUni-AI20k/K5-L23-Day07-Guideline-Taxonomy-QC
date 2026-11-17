# Guideline gán nhãn — v1 — phương tiện giao thông đường phố

- Phiên bản: v1 (đủ 40 ảnh, img_001–img_040)
- Ngày: 16/11/2026
- Người viết / duyệt: …

> Mục có dấu **[GIẢ ĐỊNH]** hoặc **[CẦN XÁC NHẬN]** là chỗ tôi suy ra từ ảnh, cần bạn xác nhận. Bản v1 đã dùng đủ 40 ảnh (img_001–img_040).

## 1. Mục tiêu

**[GIẢ ĐỊNH]** Nhãn dùng để huấn luyện mô hình phát hiện đối tượng (bounding box) cho cảnh đường phố Đông Nam Á và châu Âu: phương tiện và người, ngày lẫn đêm, mật độ xe máy cao.

Sai ở đâu thì nguy hiểm:

- Bỏ sót người hoặc xe máy bị che một phần trong đám đông xe (ảnh 3, 5, 6, 10).
- Gán nhầm vật không thật (tượng, hình in, xe đồ chơi) thành vật thật, làm mô hình học sai (ảnh 1, 11, 17, 18, 19).
- Box lệch hoặc gộp người và xe làm sai khoảng cách, sai số lượng.

## 2. Lớp và thuộc tính

### Lớp

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `person` | Người thật, đứng, đi, ngồi, hoặc đang trên xe. | Người bán hàng gánh (ảnh 3), người ngồi quán (ảnh 1), người lái và người ngồi sau xe máy (ảnh 5, 6). | Tượng, hình người in trên biển quảng cáo, linh vật bông, ma-nơ-canh (ảnh 11, 17, 18, 19, 33). |
| `car` | Ô tô con, SUV, van nhỏ, taxi, bán tải cabin kép chở người. | Nissan đỏ (ảnh 2), Mazda (ảnh 12), van bạc (ảnh 5, 16), Hilux trắng (ảnh 7). | Xe tải thùng, minibus (dễ nhầm với `bus`), xe tuk-tuk. |
| `truck` | Xe tải, xe chở hàng có thùng, xe đầu kéo, xe chở xe. | Isuzu ELF (ảnh 7), Suzuki Carry thùng hở (ảnh 1), xe chở ô tô (ảnh 2). | Bán tải cabin kép chở người (là `car`). |
| `bus` | Xe khách, minibus từ khoảng 15 chỗ trở lên. | Minibus be (ảnh 9), xe buýt nền (ảnh 8). | Van 7–12 chỗ (là `car`). |
| `motorbike` | Xe máy, xe tay ga, xe gắn máy hai bánh có động cơ (kể cả scooter điện; xe có sidecar hoặc thùng kéo gắn liền tính một box, R16). | Xe đỗ đầy vỉa hè (ảnh 3, 8, 10), xe đang chạy (ảnh 6). | Xe đạp; xe đồ chơi hoặc tượng xe máy bằng sắt vụn (ảnh 11). |
| `bicycle` | Xe đạp thường, xe đạp có giỏ, xe đạp chở hàng, xích lô đạp ba bánh. | Xe đạp giỏ (ảnh 3, 6), xe đạp chở chuối (ảnh 10). | Xe máy. |
| `tuk_tuk` | Xe ba bánh chạy động cơ, chở khách hoặc chở hàng, có mui (gồm auto-rickshaw Ấn Độ). | Tuk-tuk xanh dương (ảnh 4), tuk-tuk xanh lá (ảnh 16). | Xe ba gác chở hàng không mui (xem mục chưa chốt). |

**Vật không thuộc lớp nào thì làm gì:**

- Tượng, điêu khắc, hình in, phản chiếu, linh vật: **không gán nhãn, không tạo vùng ignore** (xem mục 3).
- Cụm vật không tách được từng cái (đám đông, dãy xe máy đỗ sát): tạo **vùng ignore** (`crowd_ignore`).
- Vật có thể là lớp mới nhưng chưa có lớp: **không gán**, ghi vào mục "Chưa chốt" ở cuối phần 4. Ví dụ: nón giao thông (ảnh 4, 13, 17), biển số, gánh hàng, xe ba gác.

### Thuộc tính

Mỗi box có 3 thuộc tính, mức cố định:

| Thuộc tính | Mức | Nghĩa / ngưỡng |
|---|---|---|
| `occlusion` | 0 | Thấy hơn 75% vật. |
| | 1 | Thấy 50–75%. |
| | 2 | Thấy 25–50%. |
| | 3 | Thấy dưới 25%: **không vẽ**, để vào vùng ignore nếu thành cụm, nếu không thì bỏ. |
| `truncated` | 0 | Không bị cắt mép ảnh. |
| | 1 | Bị cắt dưới 30% diện tích vật. |
| | 2 | Bị cắt từ 30% trở lên (vẫn vẽ nếu còn nhận ra lớp, xem R03). |
| `role` (chỉ `person`) | walking | Đi bộ, đứng, ngồi, bán hàng (không ở trên xe). |
| | riding | Đang ở trên xe máy, xe đạp, tuk-tuk (cả người lái và người ngồi sau). |

Cờ cấp box: `can_review` = có, khi chưa chắc về lớp hoặc ranh giới. Ghi mã quy tắc (R-xx) vào nhật ký QC.

**[GIẢ ĐỊNH]** Ngưỡng kích thước tối thiểu: vật có chiều cao hoặc chiều rộng dưới 12 px trên ảnh gốc thì không vẽ (xem R09). Hãy chỉnh theo độ phân giải thật của bộ dữ liệu.

## 3. Quy tắc vẽ box

**R01 — Box ôm sát phần nhìn thấy.** Cạnh box chạm điểm ngoài cùng của phần nhìn thấy, không chừa viền thừa. Không thêm vào phần ước đoán bị che. Gương chiếu hậu, cần ăng-ten, tay lái tính vào xe; gánh hàng và túi treo tay lái **không** tính vào `person` hay `motorbike`.

**R02 — Vật bị che.** Vẽ khi còn thấy từ 25% trở lên (occlusion 0–2). Dưới 25% thì bỏ. Ví dụ: xe trắng sau lưng người (ảnh 1), xe van sau đầu người lái (ảnh 5), xe sau hàng rào (ảnh 18).

**R03 — Vật bị cắt mép ảnh.** Vẽ box đến sát mép ảnh, không kéo ra ngoài. Vẽ khi phần còn lại đủ để nhận ra lớp (ví dụ thấy nguyên đầu xe đỏ và bánh xe ảnh 15). Chỉ thấy một mảnh nhỏ (vài chục pixel, hoặc không phân biệt được loại) thì bỏ.

**R04 — Phản chiếu.** Không gán nhãn xe, người, vật phản chiếu trên mặt đường ướt, kính cửa hàng, hoặc **trong gương chiếu hậu** (ảnh 13, 15, 20). Cảnh qua gương chiếu hậu bị méo và nhỏ, không phải vật nhìn trực tiếp.

**R05 — Hình in, biển quảng cáo, tranh.** Không gán nhãn mặt người, đồ ăn, xe in trên banner hay biển quảng cáo (ảnh 1: bánh hot dog in; ảnh 18: ảnh chân dung trên biển ứng cử). Chữ và logo cũng không có nhãn.

**R06 — Tượng, điêu khắc, mô hình tĩnh.** Không gán `person`, `motorbike`, `car` cho tượng, đầu tượng, hay xe sắt vụn trưng bày (ảnh 11: đầu tượng nhân vật và xe tạo hình bằng sắt vụn; ảnh 17: tượng người cưỡi ngựa). Nón giao thông đặt trên tượng cũng bỏ.

**R07 — Xe đồ chơi, xe diễu hành, linh vật.** Xe thật có động cơ, có người lái thật, chạy trên đường, dù bị độ thành hình dáng khác thì vẫn gán `car` + `can_review` (ảnh 19: xe vàng diễu hành). Linh vật bông, hình nhân vật hoạt hình trên xe: **không** gán `person`.

**R08 — Xe chủ (ego).** Không vẽ xe quay camera: thùng xe trong khung (ảnh 12), thân xe và gương nhìn từ ghế lái (ảnh 20). Xe khác phía trước thì vẽ bình thường.

**R09 — Vật quá nhỏ.** Không vẽ khi chiều cao hoặc rộng dưới 12 px **[GIẢ ĐỊNH]** hoặc không phân biệt được lớp (người và xe xa ở ảnh 3 nền, ảnh 9 xa, ảnh 13 phía sau). Nếu một cụm vật nhỏ nằm sát nhau, dùng `crowd_ignore` (R10).

**R10 — Đám đông, cụm xe đỗ.**

- Người đứng chen nhau mà không tách ra được từng người: một vùng `crowd_ignore` (ảnh 19: đám đông sau hàng rào). Người ở hàng đầu tách được rõ thì vẫn vẽ từng người.
- Dãy xe máy đỗ sát nhau: vẽ **từng xe** có thấy từ 25% trở lên (ảnh 8, 10); phần còn lại chỉ thấy bánh hoặc yên thì vào `crowd_ignore`.

**R11 — Người và xe.** Vẽ **hai box riêng**: một `person`, một `motorbike` (hoặc `bicycle`, `tuk_tuk`), cho phép chồng lên nhau. Người ngồi sau cũng có box `person` riêng với `role = riding`. Không vẽ box gộp người + xe. Xe máy chở hai, ba người ở ảnh 5, 6: mỗi người một box.

**R12 — Xe chở trên xe.** Xe nằm trên xe chở ô tô (ảnh 2): vẽ box `truck` cho xe chở và box `car` cho **từng** xe nhìn thấy từ 25% trở lên, ghi `can_review`. **[CẦN XÁC NHẬN]** nếu mô hình chỉ cần xe đang chạy thì bỏ xe chở trên.

**R13 — Mờ chuyển động, thiếu sáng.** Vẫn vẽ khi nhận ra được lớp dù mờ (ảnh 14, 15) hoặc tối (ảnh 7, 13). Không đoán lớp từ ánh đèn đơn thuần; khi không chắc, vẽ và ghi `can_review`, hoặc bỏ nếu không thấy thân vật.

**R14 — Qua kính, qua dây điện, qua hàng rào.** Vật hơi bị che bởi dây điện, hàng rào thưa, kính cửa sổ vẫn vẽ như bình thường, tính `occlusion` theo phần thật sự nhìn thấy (ảnh 9, 16, 18). Nếu cả ảnh bị mờ hoặc chói do kính, ghi **vấn đề cấp ảnh** (`image_issue: glass_glare`).

**R15 — Phân loại ranh giới.**

- Bán tải cabin kép (4 cửa) cỡ dân dụng chở người: `car` (ảnh 7). Bán tải cabin đơn, thùng hở, kể cả xe cổ và xe thùng nhỏ như Suzuki Carry: `truck` (ảnh 1, 28, 36). Xe công vụ hạng nặng bánh đôi có thùng hoặc box lớn: `truck` (ảnh 37).
- Van 7–12 chỗ (kể cả taxi van): `car`. Từ khoảng 15 chỗ trở lên: `bus`.
- Tuk-tuk và xe ba bánh có động cơ, có mui, chở khách, kể cả auto-rickshaw Ấn Độ: `tuk_tuk` (ảnh 4, 16, 35).
- Xích lô đạp ba bánh (không động cơ): `bicycle` + `can_review` (ảnh 23).

**R16 — Xe có sidecar hoặc thùng kéo.** Một box `motorbike` ôm cả xe và sidecar hoặc thùng gắn liền (ảnh 22, 25). Người ngồi trong sidecar: `person`, `role = riding`.

**R17 — Mô hình, đồ chơi, ma-nơ-canh, vật tạo hình.** Mở rộng R06: không gán xe mô hình, xe đồ chơi sau kính, ma-nơ-canh, bia mộ hình xe, tượng đặt trên xe (ảnh 24, 27, 28, 33, 38). Xe thật chở hoặc đỡ những vật đó vẫn gán theo quy tắc thường (ảnh 24, 28).

**R18 — Xe thật trưng bày trong nhà.** Xe thật ở bảo tàng, showroom (ảnh 24): gán `car` + `can_review` cho từng xe thấy từ 25%; dãy xe xếp sát ở phía sau gom vào `crowd_ignore`. **[CẦN XÁC NHẬN]** Nếu bộ dữ liệu chỉ lấy cảnh đường thì bỏ cảnh trong nhà.

**R19 — Hàng hóa chất trên xe.** Box ôm thân xe (khung, thùng, cabin), không ôm hàng chất cao hoặc nhô ra ngoài: bao hàng ở ảnh 35, ống dài ở ảnh 29. Xe chở quá khổ ghi `can_review`. Hàng nằm gọn trong thùng thì không tách box.

**R20 — Mật độ rất cao.** Trong cảnh dày đặc (ảnh 21, 30): vẽ từng xe và từng người thấy từ 25% và cao từ 12 px; phần xa còn lại gom thành một vùng `crowd_ignore` mỗi cụm, không để vùng ignore đè lên box đã vẽ. Người đứng chờ sát nhau (ảnh 32): tách được từng người thì vẽ từng người, không thì ignore.

**R21 — Vật chỉ lộ một phần ở mép ảnh.** Người bị cắt mép nhưng còn thấy đầu và thân thì vẽ `person` (`truncated` = 1 hoặc 2). Xe của người đó chỉ lộ gương hoặc tay lái (ảnh 40) thì không vẽ.

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_001 | Bán tải Suzuki cũ, người xăm hình đứng chắn thân xe; banner in hình hot dog; người ngồi quán đêm | R02, R05, R15 | `truck` + `person` từng người; không gán hình in; xe hơi bị che nhưng vẫn >50% | Hình in không phải vật thật; xe còn thấy rõ. |
| img_002 | Xe chở ô tô, nhiều xe xếp tầng; một người đứng nhỏ ở đuôi xe | R12, R02, R09 | `truck` + từng `car` thấy ≥25%, `can_review`; người nhỏ chỉ vẽ nếu ≥12 px | Chưa chốt có cần xe chở trên không. |
| img_003 | Vỉa hè Hà Nội: xe đạp giỏ, xe máy đỗ, người bán rong gánh hai thúng, nón lá | R01, R10, R11, R02 | Vẽ từng xe và người thấy ≥25%; gánh hàng nằm ngoài box người; xe nền xa dùng `crowd_ignore` | Gánh hàng không là lớp. |
| img_004 | Hai tuk-tuk ban đêm, tài xế ngồi trong, nón giao thông gần | R15, R11 | `tuk_tuk` + `person` (`riding`) cho tài xế thấy rõ; nón giao thông không gán | Chưa có lớp nón (xem chưa chốt). |
| img_005 | Cận cảnh xe máy, người đội mũ che mặt, người ngồi sau, van phía sau bị che | R02, R03, R11 | Box `person` từng người; `motorbike` cắt mép: vẽ nếu thấy ≥25%; van `car` `occlusion=2` | Xe và người chồng nhiều. |
| img_006 | Xe máy chở 2–3 người đi từ phía sau, xe đạp, taxi cắt mép trái | R03, R11, R10 | Mỗi người một box; taxi `car` cắt mép; xe đạp xa dùng `crowd_ignore` nếu dính | Cụm xe xa không tách. |
| img_007 | Gara tối, nước sàn, bán tải trắng và xe tải Isuzu sát nhau, đèn xanh | R13, R15, R03 | `car` (bán tải Hilux) và `truck` (Isuzu ELF); `can_review` nếu phần thân khuất | Xe tối nhưng nhận ra. |
| img_008 | Hàng xe máy đỗ ban đêm, người mặc áo gi-lê xe ôm số 4, số 7; xe có hộp giao hàng | R10, R11, R13 | Từng `motorbike` thấy ≥25%; người xe ôm `person` `riding` hoặc `walking` theo tư thế; bus nền xa `bus` nếu rõ | Gi-lê xe ôm không tạo lớp mới. |
| img_009 | Minibus ở giữa, xe máy nhỏ xa, dây điện chằng chịt, biển quảng cáo | R14, R05, R09, R15 | `bus` cho minibus; xe máy xa vẽ nếu ≥12 px; biển không gán | Dây điện không che quá 25%. |
| img_010 | Hà Nội: xe máy đỗ, hai người ngồi xe máy, bán chuối xe đạp, xe tay ga xám | R02, R11, R10 | `bicycle` cho xe chở chuối; từng `motorbike` và `person` | Xe đạp chở hàng vẫn là `bicycle`. |
| img_011 | Lễ hội: đầu tượng nhân vật lớn tiền cảnh, xe bằng sắt vụn trưng bày, xe cứu thương nền | R06, R10 | Không gán tượng và xe sắt vụn; gán `car` cho xe cứu thương nếu rõ; người nền xa dùng `crowd_ignore` | Tượng không là vật thật. |
| img_012 | Thùng bán tải tiền cảnh chở hàng, Mazda bên trái, xe tải khác phía trước | R08, R02 | Bỏ thùng xe chủ; vẽ `car` Mazda; xe tải phía trước `truck` nếu ≥25% | Xe chủ không gán. |
| img_013 | Đêm ướt, đèn đường, xe nhỏ xa, người đi bộ, phản chiếu trên mặt đường | R04, R09, R13 | Không gán phản chiếu; người đi bộ `person`; xe xa vẽ nếu ≥12 px | Phản chiếu không phải vật thật. |
| img_014 | Hai người đi bộ rõ nét, xe máy mờ chuyển động phía sau | R13, R02 | `person` hai người; xe máy mờ vẽ + `can_review` nếu không rõ loại | Mờ chuyển động vẫn có vật thật. |
| img_015 | Trời mưa: xe đỏ cắt mép trái, xe xám cắt mép phải, xe mờ chuyển động nền, phản chiếu mặt đường | R03, R04, R13 | `car` cho cả hai xe cắt mép, xe nền mờ vẽ; bỏ phản chiếu | Cắt mép vẫn nhận rõ lớp. |
| img_016 | Bangkok: tuk-tuk xanh dương và xanh lá (cắt mép), Vespa, van taxi, bán tải; người tiền cảnh | R03, R15, R14 | `tuk_tuk` cho hai xe, Vespa là `motorbike`, van `car`, bán tải `truck`/`car` theo R15; người tiền cảnh `person` | Chụp qua cửa kính, chú ý chói. |
| img_017 | Tượng người cưỡi ngựa đội nón giao thông, chim biển | R06, R05 | **Không gán** tượng, nón, chim | Tượng và vật trang trí không phải lớp. |
| img_018 | Biển quảng cáo có ảnh chân dung ứng cử viên; xe sau hàng rào; chụp qua kính | R05, R14, R02 | Không gán `person` cho ảnh trên biển; xe sau hàng rào gán `car` theo phần thấy | Hình in; hàng rào không quá che. |
| img_019 | Xe diễu hành vàng, linh vật chuột, đám đông sau rào chắn | R07, R10 | `car` + `can_review`; không gán linh vật; đám đông `crowd_ignore`; trẻ em rõ ở hàng đầu vẽ `person` | Xe thật có người lái. |
| img_020 | Gương chiếu hậu có xe nhỏ phản chiếu, cầu vồng, giọt nước | R04, R08 | Không gán xe trong gương; bỏ thân xe chủ | Phản chiếu và xe chủ. |
| img_021 | Ngã tư Sài Gòn giờ cao điểm: hàng trăm xe máy chen nhau, ô tô lẫn trong dòng | R20, R02, R11 | Vẽ từng xe máy và người thấy từ 25% và cao từ 12 px ở phía trước; phần xa dày đặc gom `crowd_ignore`; ô tô ở trái là `car` | Phía trước vẫn tách được từng xe. |
| img_022 | Ảnh đen trắng cũ: xe máy gắn sidecar trên đường rừng, có người trong sidecar | R16, R09 | Một box `motorbike` ôm cả xe và sidecar; `person` (`riding`) nếu cao từ 12 px; `can_review` | Sidecar là một phần của xe. |
| img_023 | Xích lô đạp ba bánh nhìn từ phía sau, Honda đen bên trái, xe máy xa, dãy xe đỗ ven đường | R15, R11, R10 | Xích lô: `bicycle` + `can_review`; người đạp: `person` (`riding`); Honda: `car`; xe máy đang chạy: `motorbike` nếu từ 12 px; dãy xe đỗ xa: `crowd_ignore` | Không có động cơ nên không phải `tuk_tuk`. |
| img_024 | Khu trưng bày xe cổ trong nhà: Pacer đen, xe mô hình vàng đặt trên nóc, nhiều xe xếp sát | R17, R18, R10 | `car` + `can_review` cho xe thật thấy từ 25%; không gán xe mô hình trên nóc; xe san sát phía sau gom `crowd_ignore` | Mô hình không phải xe thật; xe trưng bày chưa chốt. |
| img_025 | Bờ biển Pattaya: người đi bộ, người ngồi ghế bãi biển, taxi xanh vàng, xe máy kéo thùng hàng | R16, R09, R10 | `person` từng người đi bộ rõ; nhóm ngồi ghế ở xa gom `crowd_ignore`; taxi: `car`; xe máy kèm thùng: một box `motorbike` + `person` (`riding`) | Thùng kéo gắn liền với xe. |
| img_026 | Ban đêm: hai người trên xe máy đỏ, tường rào in tranh cảng biển và tàu | R05, R13, R03 | `motorbike` (cắt mép dưới) + hai `person` (`riding`); không gán tàu, cảng in trên tường | Hình in; thiếu sáng nhưng xe rõ. |
| img_027 | Bia mộ đá đen hình xe bán tải trong nghĩa trang | R06, R17 | Không gán | Vật tạo hình tĩnh, không phải xe. |
| img_028 | Bán tải cổ cabin đơn, trên thùng có tượng ngựa trắng; SUV đỏ phía sau | R17, R15 | `truck` cho bán tải cổ; không gán ngựa; SUV đỏ: `car` | Xe thật, tượng chỉ là hàng trên thùng. |
| img_029 | Một người đi xe máy điện, một người dắt xe đạp, vác ống dài ngang qua; người đi bộ ở xa | R19, R11, R09 | `motorbike` + `person` (`riding`); `bicycle` + `person`; box không ôm ống dài; người xa vẽ nếu từ 12 px | Vật nhô dài không tính vào box. |
| img_030 | Bãi giữ xe máy Honda chật cứng, dây rào, nhân viên áo xanh đi bộ, poster in người | R20, R05, R10 | Vẽ từng xe thấy từ 25% ở hàng trước; hàng sau gom `crowd_ignore`; `person` cho nhân viên; không gán poster | Xe chồng khít, hình in. |
| img_031 | Phố đêm Đài Loan sau mưa: đường ướt, bus, ô tô, xe máy, biển neon, người đi bộ bên phải | R04, R13, R09 | Gán `car`, `bus`, `motorbike`, `person` thấy rõ; bỏ phản chiếu trên đường; xe bị chói đèn: `can_review` | Mặt đường phản chiếu nhiều. |
| img_032 | Đám người đứng chờ xe buýt sau dải bê tông, nón giao thông cam, xe xanh cắt mép trái, bãi xe phía sau | R20, R03, R02 | `person` từng người tách được; cụm đứng sát nhau: `crowd_ignore`; `car` xanh cắt mép (`truncated`); nón không gán; xe trong bãi sau người: `car` nếu từ 25% | Đông nhưng một phần tách được. |
| img_033 | Cửa kính cửa hàng: ma-nơ-canh, ảnh in người mặc váy, phản chiếu gương xe van | R04, R05, R17 | Không gán | Ma-nơ-canh, hình in và phản chiếu. |
| img_034 | Ngã tư Huế chiều ngược sáng: người băng đường, sedan đen, xe máy và xe đạp rải rác, người đeo ba lô cắt mép phải | R03, R09, R13 | `person` (`walking`); `car` sedan; `motorbike` từng xe từ 12 px; `person` + `motorbike` cắt mép phải (`truncated` = 2); nhóm xa dính nhau gom `crowd_ignore` | Ngược sáng nhưng vẫn nhận ra lớp. |
| img_035 | Ấn Độ: auto-rickshaw chở bao hàng cao gấp đôi thân xe, auto khác, xe máy, ô tô trắng | R19, R15, R11 | `tuk_tuk` cho cả hai auto-rickshaw, box ôm thân xe không ôm hàng, `can_review`; `motorbike` + `person` (`riding`); `car` trắng | Hàng nhô cao không tính vào box. |
| img_036 | Xe tải nhỏ phủ bạt xanh đỗ lề, dãy xe máy đỗ hai bên, biển số đã làm mờ | R15, R10, R02 | `truck`; xe máy từng xe thấy từ 25%; phần còn lại `crowd_ignore`; không gán biển số | Thân xe tải rõ, biển số không phải lớp. |
| img_037 | Xe công vụ bánh đôi có box lớn, hai xe buýt xanh hai bên (một chiếc bị cắt mép, một chiếc bị che), người đi bộ nhỏ | R15, R03, R02, R09 | `truck` cho xe công vụ; `bus` cho từng xe buýt thấy từ 25%; `person` nếu từ 12 px | Bán tải hạng nặng xếp `truck`. |
| img_038 | Kệ kính cửa hàng đồ chơi: hàng chục xe mô hình, vịt cao su, chuột bông | R17, R04 | Không gán | Đồ chơi, mô hình sau kính. |
| img_039 | Phố Huế nhiều dây điện: người đi bộ, xe máy chạy chậm, xe máy đỗ, bảng quảng cáo | R14, R05, R09 | Gán `person`, `motorbike`, `bicycle` thấy từ 25% và từ 12 px; không gán bảng quảng cáo; dây điện không tính là che | Dây điện mảnh, không che đáng kể. |
| img_040 | Cận cảnh người đội mũ bảo hiểm đen ở tiền cảnh, gương xe máy lộ ở đáy ảnh; taxi xanh đỏ, tuk-tuk vàng, SUV, bus phía sau | R21, R03, R05, R02 | `person` tiền cảnh (`truncated`); không vẽ `motorbike` vì chỉ lộ gương; `car` cho taxi và SUV; `tuk_tuk`; `bus`; không gán ảnh dán trên kính taxi | Xe của người này gần như ngoài khung. |

**Chưa chốt** (cần quyết trước khi gán đại trà):

- Xe chở trên xe chở ô tô (ảnh 2): giữ từng xe `car` + `can_review` (R12) hay bỏ?
- Xe thật trưng bày trong nhà (ảnh 24): giữ `car` + `can_review` (R18) hay bỏ vì không phải cảnh đường?
- Xích lô đạp (ảnh 23): gộp vào `bicycle` hay tạo lớp `cyclo`?
- Trẻ em trên xe hoặc được bế (ảnh 19): `person` chung hay lớp riêng?
- Xe ba gác không mui: chưa gặp trong 40 ảnh; nếu gặp thì không gán, ghi `can_review` và xin quyết định lớp mới.

**Đã chốt trong v1:** không tạo lớp `traffic_cone` và `license_plate`, nón giao thông và biển số không gán nhãn (ảnh 4, 13, 17, 32, 36); bán tải chia theo R15; hàng chất trên xe không tính vào box (R19).

## 5. QC và phiên bản

**[GIẢ ĐỊNH]** Ngưỡng QC áp dụng:

- Duyệt ngẫu nhiên 10–20% ảnh mỗi lô; ảnh có `can_review` duyệt 100%.
- Lô đạt khi box sát (IoU với bản duyệt ≥0,8) và lớp đúng ≥95% trên mẫu.
- Ca mơ hồ: người duyệt viết quyết định cuối và cập nhật mục 4 trước khi gán tiếp.

Ai quyết ca mơ hồ: …

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản nháp đầu: 7 lớp, 3 thuộc tính, 15 quy tắc | Từ 20 ảnh đầu (img_001–img_020) |
| v1 | Thêm R16–R21, sửa R15, chốt nón giao thông, biển số, xích lô, bán tải; thêm 20 ca khó | 20 ảnh mới img_021–img_040 |