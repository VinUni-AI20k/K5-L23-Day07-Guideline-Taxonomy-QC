# Guideline gán nhãn — v0.1 cá nhân — 2A202603344 - Nguyễn Đức Hạnh

> Bản Pha 1, viết trước khi họp nhóm. Không sửa file này sau khi nhóm chốt `guideline_v1.0_agreed.md`.
> Mục 4 gắn đúng ảnh `img_001.jpg` … `img_040.jpg` sau khi xem từng khung. Quyết định dưới đây là quyết định dùng khi gán, không còn ô chờ điền.

- Phiên bản: v0.1-personal
- Ngày: 2026-11-16
- Người viết: 2A202603344 - Nguyễn Đức Hạnh
- Loại nhãn: bounding box (hộp chữ nhật), export COCO 1.0
- Công cụ: CVAT
- So với v0: v0 có năm lớp xe/người, mức che không có %, và không có ca khó. Bộ 40 ảnh có xe ba bánh, xe chở xe, bán tải, xe khách, người ngồi trên xe, hàng hóa, vật không thật, phản chiếu, vật nhỏ và đám đông. Bản này chốt một cách gán cho từng ca đó.

---

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình phát hiện **người thật** và **phương tiện giao thông đường bộ thật** trên ảnh đường phố (camera giao thông hoặc xe tự lái).

Mô hình cần đoán **lớp** của từng vật. Mức che, bị cắt mép và cờ xem lại chỉ dùng để lọc và QC, nên là thuộc tính.

Sai nguy hiểm:

- Bỏ sót người hoặc xe thật đang ở trên đường, trên vỉa hè, hoặc đang được chở.
- Gán tượng, ma-nơ-canh, hình in, phản chiếu, đồ chơi thành người hoặc xe.
- Gộp người đang ngồi trên xe vào box xe, hoặc gộp nhiều xe thật thành một box.

Vật không thuộc lớp nào ở mục 2: không vẽ box lớp. Vùng có nhiều người hoặc xe thuộc lớp nhưng không tách từng vật được, hoặc từng vật cao dưới 20 px: vẽ `ignore_region`.

Ảnh chỉ có vật ngoài phạm vi vẫn nằm trong tập xuất COCO, với 0 box. Đó là `img_017.jpg`, `img_020.jpg`, `img_027.jpg`, `img_033.jpg`, `img_038.jpg`.

---

## 2. Lớp và thuộc tính

Mỗi vật thật thuộc **đúng một** lớp. Một vật, một box.

Phép thử khi phân vân thêm lớp: *mô hình có phải đoán ra điều này không?* Có → lớp. Chỉ để lọc hoặc QC → thuộc tính.

### Lớp

| Lớp | Định nghĩa (một câu) | Ví dụ trong bộ ảnh | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `person` | Người thật, phần nhìn thấy đủ để nhận ra là người. | Người đứng cạnh bán tải `img_001`; người lái và ngồi sau xe máy `img_026`; khách nhìn thấy trong xe khách `img_009`. | Tượng kỵ sĩ `img_017`; chân dung trên biển `img_018`; mascot chuột `img_019`; ma-nơ-canh `img_033`; búp bê `img_038`; hình dán mặt người trên kính taxi `img_040`. |
| `bicycle` | Xe hai bánh chạy bằng sức người, có khung và bàn đạp của xe đạp. | Xe đạp giỏ trước `img_003`; xe đạp trong dòng xe `img_006`; xe đạp chở mẹt trái cây `img_010`; xe đạp chở ống `img_029`. | Xe ga, xe số, xe scooter. Xe máy gắn sidecar. |
| `motorcycle` | Xe máy hai bánh có động cơ, kể cả xe ga; sidecar gắn liền vẫn thuộc xe này. | Xe ga và xe số `img_005`, `img_006`; xe ga chở hai người `img_026`; xe máy có sidecar `img_022`, `img_025`; xe độ còn bánh và yên `img_011`. | Xe đạp. Tuk-tuk và xích lô. Ống thép, cuộn dây, thùng hàng không phải một xe thứ hai. |
| `car` | Ô tô chở người, không có thùng hàng tách khỏi cabin. | Sedan đỏ trên sàn `img_002`; Mazda SUV `img_012`; Civic `img_023`; wagon trong nhà xe `img_024`; taxi xanh `img_040`. | Bán tải là `truck`. Xe khách là `bus`. Xe mô hình trong tủ `img_038` và xe diễu hành chỉ khi không phải xe chạy được. Xe Danger Mouse có biển số và người lái vẫn là `car` (`img_019`). |
| `van` | Xe thùng kín liền một khối với cabin, cỡ nhỏ đến vừa, kể cả xe 7–16 chỗ kiểu Hiace. | Van bạc `51LD-70-65` `img_005`; van taxi bạc `img_016`. | SUV là `car`. Bán tải có nắp thùng là `truck` (`img_037`). Minibus có dãy cửa sổ khách là `bus` (`img_009`). |
| `truck` | Xe có cabin và khoang hàng tách nhau: xe tải, đầu kéo, bán tải, xe ben, xe thùng bạt. | Bán tải Suzuki `img_001`; xe chở ô tô `img_002`; Isuzu ELF và bán tải `img_007`; Veryca thùng bạt `img_036`; bán tải gắn nắp thùng cao `img_037`. | Van kín liền cabin. Wagon không thùng sau (`img_024`) là `car`. Tượng bán tải trên bệ `img_027` không phải `truck`. |
| `bus` | Xe chở khách thân dài hoặc xe buýt thành phố, có dãy cửa sổ hành khách hoặc đuôi xe buýt có số tuyến. | Minibus `75B-0946` `img_009`; xe buýt số 821 nhìn từ sau `img_031`; xe buýt GO `img_037`; xe buýt 511 `img_040`. | Hiace và van taxi là `van`. |
| `three_wheeler` | Phương tiện ba bánh chở người hoặc hàng, người lái ngồi trong cabin hoặc trên yên xích lô, không phải xe máy có sidecar. | Hai tuk-tuk `img_004`; tuk-tuk `img_016`, `img_040`; xích lô đạp `img_023`; auto-rickshaw `img_035`. | Xe máy hai bánh. Sidecar (`img_022`, `img_025`) là `motorcycle`. Ô tô bốn bánh. |
| `ignore_region` | Vùng chứa người hoặc xe thuộc các lớp trên nhưng không gán từng vật. Không phải một lớp vật thể. | Đám mũ bảo hiểm xa `img_021`; đám người lễ hội xa `img_011`; dải xe nhoè `img_014`. | Một xe rõ, đủ lớn. Tượng, đồ chơi, phản chiếu không đưa vào vùng này. |

Thứ tự chốt khi một xe có thể rơi vào hai lớp. Dừng ở bước đầu tiên đúng:

1. Tượng, mô hình, đồ chơi, xe lễ hội không chạy được, hình in, phản chiếu → không có lớp xe.
2. Ba bánh, người lái ngồi trong cabin hoặc đạp xích lô → `three_wheeler`.
3. Xe máy hai bánh kèm thùng sidecar → `motorcycle` (một box cho cả xe và sidecar).
4. Khung xe đạp, bàn đạp, không động cơ → `bicycle`.
5. Hai bánh có động cơ → `motorcycle`.
6. Có thùng hàng tách khỏi cabin, kể cả thùng hở, thùng bạt, nắp thùng, nắp cao → `truck`.
7. Thân dài hoặc đuôi xe buýt, dãy cửa sổ hành khách → `bus`.
8. Thùng kín liền cabin, cỡ Hiace/Transit → `van`.
9. Ô tô chở người còn lại, kể cả sedan, hatchback, SUV, wagon, MPV → `car`.

Ranh giới đã chốt trên ảnh thật:

- Hiace bạc có vài cửa sổ bên (`img_005`, `img_016`) là `van`. Minibus dài hơn, nhiều cửa sổ khách dọc thân (`img_009`) là `bus`.
- Nắp thùng cao trên bán tải (`img_037`, Master 75) không biến bán tải thành `van`.
- Wagon không có thùng sau (`img_024`) là `car`.
- Sidecar không phải `three_wheeler`.

### Vật không thuộc lớp nào

Không vẽ box lớp cho:

- Tượng và đài: kỵ sĩ đồng `img_017`; tượng Predator `img_011`; tượng bán tải trên bệ đá `img_027`; ngựa tượng trong thùng xe `img_028`; tượng trang trí quán `img_013`.
- Ma-nơ-canh và người trong ảnh trưng bày `img_033`. Búp bê, thú bông `img_038`. Mascot chuột ngồi trên xe `img_019`. Nhân vật vẽ trên tường `img_031`.
- Chân dung và hình người in: biển bầu cử `img_018`; poster `img_030`; người trên áp phích ngân hàng `img_036`; hình dán trên kính taxi `img_040`; poster cửa hàng `img_023`.
- Phản chiếu trên gương, kính, mũ, mặt đường ướt: gương `img_020`; kính tủ `img_033` và `img_038`; mặt đường `img_013`, `img_015`, `img_031`; kính mũ `img_040`.
- Đồ chơi và xe mô hình trong tủ `img_038`.
- Hàng hóa không phải xe: thùng và túi trên bán tải `img_012`; bao tải trên rickshaw `img_035`; ống thép `img_029`; cuộn dây `img_016`; mẹt trái cây `img_010`; tranh tàu trên tường `img_026`.
- Thuyền ngoài biển `img_025`, chó `img_009`, chim `img_017`, nón giao thông, giày và áo treo `img_007`.
- Phần xe gắn camera: gương và cửa xe chủ trong `img_020`.

Những vật đó không đưa vào `ignore_region`. `ignore_region` chỉ phủ người hoặc xe thuộc lớp mà không gán riêng được.

### Thuộc tính

Gắn trên mọi box lớp vật (`person`, `bicycle`, `motorcycle`, `car`, `van`, `truck`, `bus`, `three_wheeler`). Box `ignore_region` để mặc định, không chấm mức che.

Cách tính phần trăm che, dùng chung cho mọi lớp:

- Hình dung toàn bộ vật nếu không có vật khác đè lên. Phần nằm ngoài khung ảnh không tính vào % che.
- % che = diện tích bị vật khác đè / diện tích toàn bộ vật đó.
- Hàng rào, cỏ, bàn, người khác, thân xe khác đều là vật che. Cắt bởi mép ảnh thì chỉ làm `truncated`.

| Thuộc tính | Mức | Ngưỡng | Ý nghĩa |
|---|---|---|---|
| `occluded_level` | `0` | Dưới 10% diện tích bị vật khác che | Thấy gần hết. Người đứng `img_034`, bán tải nhìn nghiêng `img_028`. |
| | `1` | Từ 10% đến dưới 40% | Che ít. Ô tô sau hàng rào `img_018`; xe bị người đi bộ che một phần `img_034`. |
| | `2` | Từ 40% đến dưới 70% | Che nhiều, vẫn nhận ra lớp. Ô tô sàn dưới `img_002`; người trong tuk-tuk `img_040`. |
| | `3` | Từ 70% trở lên, và vẫn nhận ra đúng lớp | Chỉ còn một phần. Khách chỉ lộ đầu sau cửa kính `img_009`. Không còn nhận ra lớp thì không vẽ box. |
| `truncated` | `no` | Toàn bộ vật nằm trong khung | Có thể vẫn bị che. |
| | `yes` | Vật tiếp tục ra ngoài mép ảnh | Box dừng ở mép. Bán tải cắt mép phải `img_001`; người cắt mép dưới `img_040`. |
| `can_review` | không tick | Quy tắc trên áp dụng được | Kể cả ca khó đã có dòng ở mục 4. |
| | tick | Đã chọn lớp theo thứ tự mục 2 nhưng đo chiều cao sát 20 px, hoặc sau thứ tự đó vẫn còn đúng hai lớp | Vẫn chọn một lớp. Không để trống lớp. Không tick để gán tượng hoặc đồ chơi thành xe. |

Ngưỡng kích thước lấy từ `taxonomy.json`, mục `rules`, không đổi số: box lớp chỉ vẽ khi chiều cao **phần nhìn thấy** ≥ 20 px. Thấp hơn thì không vẽ box lớp; gom vào `ignore_region` theo mục 3.

---

## 3. Quy tắc vẽ box

1. **R-01 — Một vật, một box, một lớp.** Không gộp hai người. Không gộp xe và người. Không gộp hai xe.
2. **R-02 — Ôm sát phần nhìn thấy.** Box chạm mép ngoài của phần đang thấy. Không vẽ nốt phần khuất sau vật khác. Không chừa viền nền.
3. **R-03 — Người và xe là hai box.** Người lái, ngồi sau, ngồi trong cabin, đứng cạnh xe hoặc cầm xe đều là `person` riêng. Box người không bao bánh xe. Box xe không kéo lên tới đầu người. Hai box được chồng ở chỗ người chạm xe. Áp cho `img_004`, `img_005`, `img_006`, `img_010`, `img_016`, `img_023`, `img_026`, `img_029`, `img_034`, `img_035`.
4. **R-04 — Chốt lớp theo thứ tự mục 2.** Không chọn lớp theo đồ đang chở hay theo biển hiệu taxi.
5. **R-05 — Bị che.** Box ôm phần nhìn thấy. `occluded_level` theo ngưỡng mục 2. Che từ 70% trở lên mà không còn nhận ra lớp: không vẽ.
6. **R-06 — Bị cắt mép.** Box dừng ở mép, `truncated = yes`. Phần ngoài khung không cộng vào % che. Vừa cắt mép vừa bị vật khác che: đặt cả hai thuộc tính.
7. **R-07 — Không phải người thật hoặc xe thật.** Tượng, ma-nơ-canh, mascot, hình in, phản chiếu, đồ chơi: không box lớp, không `can_review` để gán tạm.
8. **R-08 — Xe chủ.** Capo, gương, cửa, taplo của xe gắn camera không phải một xe trên đường. `img_020` không có box.
9. **R-09 — Quá nhỏ.** Chiều cao phần nhìn thấy dưới 20 px: không box lớp. Cụm vật nhỏ, hoặc một vật nhỏ đứng một mình, nhận một `ignore_region` quanh đúng vùng đó.
10. **R-10 — Đám đông.** Vật tách được biên và cao ≥ 20 px thì từng box. Phần mà quá nửa số vật không tách được biên: một `ignore_region` cho phần đó, và không vẽ thêm box lớp bên trong vùng ignore. Vật đứng riêng phía trước vẫn có box. `ignore_region` không đè lên vật đã gán.
11. **R-11 — Hàng hóa.** Bao, thùng, túi, ống, cuộn dây, mẹt trái cây, tranh vẽ không có box. Box xe ôm thân xe (cabin, khung, bánh, gương, sidecar gắn liền). Không kéo box tới đầu ống hay đỉnh chồng bao.
12. **R-12 — Xe chở xe.** Mỗi xe thật một box nếu nhận ra lớp và cao ≥ 20 px. Xe kéo và rơ-moóc sàn của cùng một xe đầu kéo là một `truck`.
13. **R-13 — Nhoè, tối, mưa đêm.** Nhận ra lớp thì vẽ. Không nhận ra từng vật thì `ignore_region` nếu đó là dải người hoặc xe, hoặc bỏ qua nếu chỉ là nền. Vệt sáng trên mặt đường ướt không phải xe thứ hai.
14. **R-14 — `can_review`.** Ca đã có trong mục 2 và 4 thì không tick. Chỉ tick khi đo sát ngưỡng 20 px hoặc thứ tự lớp vẫn để hai lớp cùng đúng. Ghi chú ngắn trên box.

Người trên xe, cách đếm box:

| Tình huống | Số box | Ảnh đối chứng |
|---|---|---|
| Một người, một xe máy | 1 `person` + 1 `motorcycle` | `img_034` (người mũ xanh, mép phải) |
| Hai người, một xe máy | 2 `person` + 1 `motorcycle` | `img_006` (xe Lead), `img_010`, `img_026` |
| Người lái trong tuk-tuk hoặc xích lô | 1 `person` + 1 `three_wheeler` | `img_004`, `img_023`, `img_040` |
| Người đi bộ cạnh xe, không ngồi trên xe | `person` riêng, xe riêng | `img_001`, `img_003`, `img_032` |
| Khách chỉ lộ đầu qua cửa kính, vẫn nhận ra người | `person`, mức che 2 hoặc 3 | `img_009` |
| Không nhận ra người trong kính, chỉ còn một mảng tối | Không box người | Các cửa kính tối không rõ đầu |

---

## 4. Ca khó

Quy tắc mục 2 và 3 là quyết định. Bảng này gắn ảnh đã xem. Một ảnh có nhiều tình huống thì nhiều dòng.

| Ảnh | Tình huống | Rule | Quyết định | Lý do |
|---|---|---|---|---|
| `img_004.jpg`, `img_008.jpg`, `img_016.jpg`, `img_035.jpg`, `img_040.jpg` | Tuk-tuk, auto-rickshaw | R-03, R-04 | `three_wheeler`. Người lái nhìn thấy là `person` riêng. | Ba bánh, người ngồi trong cabin. v0 không có lớp này. |
| `img_023.jpg` | Xích lô, người đạp phía sau, ghế khách phía trước | R-03, R-04 | `three_wheeler` + `person` cho người đạp. Ghế không thấy khách thì không thêm người. | Cùng nhóm ba bánh với tuk-tuk. Không phải `bicycle` vì có hai bánh ghế khách và một bánh sau. |
| `img_022.jpg`, `img_025.jpg` | Xe máy gắn sidecar | R-04, R-11 | Một `motorcycle` ôm xe và sidecar. Người lái là `person` nếu phần nhìn thấy cao ≥ 20 px. | Người lái ngồi trên yên xe máy. Sidecar là khoang gắn thêm, không phải tuk-tuk. |
| `img_002.jpg` | Đầu kéo Renault và sàn hai tầng đang chở ô tô | R-12 | Một `truck` cho cả đầu kéo và sàn. Mỗi ô tô nhận ra lớp trên hai sàn là một `car`. Người đứng cuối sàn là `person`. | Mỗi xe thật là một đối tượng. Gộp ô tô vào xe kéo làm mất xe đang được chở. |
| `img_024.jpg` | Wagon đen chở một thân xe vàng có bánh trên nóc; các xe khác trong nhà xe | R-12 | Mỗi xe là `car`, kể cả thân xe vàng trên nóc và wagon đen. Xe vàng không phải `truck`. | Wagon không có thùng hàng riêng. Thân xe có bánh, đang được chở, vẫn là xe. |
| `img_001.jpg`, `img_012.jpg`, `img_028.jpg` | Bán tải thùng hở | R-04, R-11 | `truck`. Hàng trong thùng (sắt, thùng carton, túi, tượng ngựa) không có box. | Thùng sau tách khỏi cabin. Tượng ngựa `img_028` không phải người. |
| `img_037.jpg` | Bán tải GO gắn nắp thùng cao, đứng cạnh xe buýt | R-04 | Bán tải là `truck`. Hai xe buýt xanh là `bus`. Người đi bộ bên trái là `person`. | Nắp thùng là đồ gắn lên thùng bán tải, không phải thân van liền cabin. |
| `img_036.jpg` | Veryca xanh, cabin và thùng bạt tách nhau, xe máy đậu hai bên | R-04 | Veryca là `truck`. Từng xe máy tách được là `motorcycle`. Người trên áp phích ngân hàng không phải `person`. | Thùng hàng tách cabin. Bạt phủ không biến nó thành `van`. |
| `img_009.jpg` | Minibus màu kem, dãy cửa sổ khách, người ngồi trong xe | R-03, R-04 | `bus`. Mỗi đầu người nhận ra sau kính là `person`, `occluded_level` 2 hoặc 3. | Dài hơn Hiace và có dãy cửa sổ hành khách. Khác `img_005`. |
| `img_005.jpg`, `img_016.jpg` | Van bạc liền cabin (Hiace, van taxi) | R-04 | `van`. Người ngồi xe máy phía trước là `person`, không gộp vào van. | Thân kín liền cabin, không phải xe buýt dài. |
| `img_031.jpg`, `img_040.jpg` | Xe buýt nhìn từ sau hoặc từ xa, có số tuyến | R-04, R-13 | `bus` khi đuôi hoặc thân xe buýt còn nhận ra (số 821, số 511). | Nhìn từ sau vẫn là xe buýt, không hạ xuống `van`. |
| `img_006.jpg`, `img_010.jpg`, `img_026.jpg` | Hai người trên một xe máy | R-03 | 2 `person` + 1 `motorcycle`. | Hai người thật. Box chồng ở chỗ hai người chạm nhau và chạm xe. |
| `img_003.jpg`, `img_010.jpg`, `img_029.jpg`, `img_039.jpg` | Xe đạp cạnh xe máy | R-04 | Khung và bàn đạp → `bicycle`. Xe ga hoặc xe số → `motorcycle`. Người đứng cầm xe vẫn là `person`. | `img_003` có cả xe đạp giỏ và xe máy. `img_029` có scooter và xe đạp cùng chở một ống. |
| `img_012.jpg`, `img_016.jpg`, `img_029.jpg`, `img_035.jpg` | Hàng nhô ra ngoài thân xe | R-11 | Box dừng ở thân xe. Ống, bao tải, cuộn dây, túi không có box và không kéo dài box. | Hàng không phải phương tiện. Mức che của xe tính phần thân bị hàng đè. |
| `img_009.jpg`, `img_019.jpg`, `img_040.jpg` | Người thật sau kính, và hình người không thật ở gần | R-03, R-07 | Người lái Danger Mouse, khách minibus, người lái tuk-tuk: `person`. Mascot chuột, áp phích, hình dán trên kính: không box. | Chỉ người thật. Xe parade có biển `YR04 NUM` và người lái là `car`. |
| `img_011.jpg`, `img_017.jpg`, `img_027.jpg`, `img_028.jpg` | Tượng người hoặc tượng xe | R-07 | `img_017` và `img_027`: 0 box. Predator `img_011`: không phải `person`. Bán tải thật `img_028`: `truck`; ngựa tượng không box. Xe độ có bánh và yên ở `img_011`: `motorcycle`. | Tượng trên bệ hoặc tượng lớn hơn người thật không tham gia giao thông. Xe độ còn là xe. |
| `img_018.jpg`, `img_030.jpg`, `img_033.jpg`, `img_036.jpg`, `img_038.jpg` | Hình in, ma-nơ-canh, mô hình | R-07 | Không box cho chân dung, poster, ma-nơ-canh, búp bê, xe mô hình. `img_033` và `img_038`: 0 box. `img_018` và `img_030`: chỉ box người thật và xe thật. | Hình và đồ chơi không đi trên đường. |
| `img_013.jpg`, `img_015.jpg`, `img_020.jpg`, `img_031.jpg`, `img_033.jpg` | Phản chiếu | R-07, R-08 | Không box hình trong gương, trên kính, trên mặt đường ướt. `img_020`: 0 box, gương là xe chủ. Xe đang đậu thật ở `img_015` và `img_018` vẫn được box. | Phản chiếu không phải thêm một vật. |
| `img_014.jpg` | Hai người rõ, nền xe bị nhoè chuyển động | R-10, R-13 | Hai người đi bộ là `person`. Dải xe chỉ còn vệt, không tách được từng xe: `ignore_region`. | Còn nhận ra lớp thì mới có box lớp. |
| `img_004.jpg`, `img_007.jpg`, `img_008.jpg`, `img_013.jpg`, `img_026.jpg`, `img_031.jpg` | Đêm hoặc mưa, vật chính vẫn nhận ra | R-13 | Vẽ đủ lớp nhận ra. Vệt đèn trên nền ướt không thành xe mới. Khăn hồng và giày ở `img_007` không phải `person`. | Tối không phải lý do bỏ người hoặc xe còn nhận ra. |
| `img_008.jpg`, `img_011.jpg`, `img_021.jpg`, `img_030.jpg`, `img_032.jpg` | Nhiều người hoặc nhiều xe | R-09, R-10 | `img_032`: từng người tách được một box. `img_021` và `img_030`: box từng xe phía trước tách được; khối phía sau không tách được thì một `ignore_region`. `img_011`: người gần và xe độ thì box; đám xa không tách được thì `ignore_region`. | Đám đông tách được thì không gom. Đám không tách được thì không đoán biên. |
| `img_001.jpg`, `img_005.jpg`, `img_012.jpg`, `img_015.jpg`, `img_016.jpg`, `img_032.jpg`, `img_034.jpg`, `img_040.jpg` | Vật chạm mép khung | R-06 | `truncated = yes`. Box dừng ở mép. Người mũ bảo hiểm `img_040` là `person` cắt mép dưới; gương dưới góc trái thuộc taxi xanh, không phải một xe máy. | Cắt mép và bị che là hai thuộc tính. |
| `img_018.jpg`, `img_030.jpg` | Xe thật bị che bởi hàng rào, dây hoặc xe khác | R-05 | Box phần nhìn thấy. Hàng rào và cỏ `img_018` đưa các ô tô vào `occluded_level` 1 nếu phần che từ 10% đến dưới 40%. | Thanh rào là vật che, không bỏ xe. |

Cách dùng `can_review` sau khi đã xem 40 ảnh:

| Chỗ còn đo khi gán | Chọn trước | Khi nào tick |
|---|---|---|
| Đầu người trên xe sidecar `img_022` | `person` nếu phần mũ và đầu cao ≥ 20 px, cùng một `motorcycle` | Tick nếu đo trong khoảng 18–22 px |
| Xe rất nhỏ cuối đường `img_021`, `img_025`, `img_039` | Box lớp nếu nhận ra và cao ≥ 20 px; không thì `ignore_region` | Tick nếu nhận ra là xe nhưng không chốt được `bus` với `truck` |
| Một đốm trong cabin không rõ là đầu người | Không vẽ | Tick chỉ khi đã vẽ vì vẫn nghi là người |

Các ca sau đây đã chốt, không tick `can_review`: nắp thùng `img_037` là `truck`; sidecar là `motorcycle`; minibus `img_009` là `bus`; Hiace là `van`; xe parade `img_019` là `car`; tượng `img_027` không phải xe.

### Chỉ mục 40 ảnh

| Ảnh | Trong khung | Quyết định gán |
|---|---|---|
| `img_001.jpg` | Quán vỉa hè, bán tải Suzuki thùng hở chở thanh sắt, người đứng và người ngồi bàn. | `truck` cho bán tải, `truncated = yes` ở mép phải. Từng người đứng và ngồi là `person`. Bàn và người khác che thì tăng `occluded_level`. Biển hotdog không phải người. |
| `img_002.jpg` | Xe đầu kéo chở ô tô hai sàn, một người đứng cuối sàn. | Một `truck` cho đầu kéo và sàn. Mỗi ô tô trên sàn là `car` (sedan đỏ, xe xanh, sedan trắng, các SUV bạc sàn trên; xe trắng, xe tối màu và SUV bạc sàn dưới). Xe sàn dưới bị khung và xe khác che: mức 2 nếu còn nhận ra. Người cuối sàn là `person`. |
| `img_003.jpg` | Vỉa hè Hà Nội: xe đạp giỏ, xe máy, người gánh hàng, người đội nón. | `bicycle` cho xe đạp, `motorcycle` cho từng xe máy. Người đứng, người gánh, người ngồi xe là `person` từng người. Quang gánh và hàng không có box. Xe và người phía cuối phố: box nếu cao ≥ 20 px và tách được, không thì `ignore_region`. |
| `img_004.jpg` | Hai tuk-tuk xanh đậu cạnh nhau, mỗi xe có người lái. | Hai `three_wheeler`. Mỗi người lái một `person`, mức che theo phần cabin đè lên người. Nón giao thông không có lớp. |
| `img_005.jpg` | Nhiều người trên xe máy, sát mép dưới; van bạc `51LD-70-65` phía sau. | Mỗi người một `person`, mỗi xe máy một `motorcycle`, `truncated = yes` với người và xe bị cắt mép. Van là `van`, mức che theo phần người và xe máy đè lên. |
| `img_006.jpg` | Tắc đường: taxi trắng, xe ga chở hai người, xe số, xe đạp, người đi xe đạp. | Taxi là `car`. Xe ga và xe số là `motorcycle`. Xe có bàn đạp là `bicycle`. Mỗi người một `person` (xe Lead có hai người). Xe xa không tách được thì `ignore_region`. Không có xích lô trong khung này. |
| `img_007.jpg` | Nhà kho đêm: bán tải trắng, xe thùng ngay sau nó, Isuzu ELF bên phải, nền ướt. | Ba `truck`: bán tải, xe thùng đèn xanh bị bán tải che, Isuzu cắt mép phải. Khăn hồng, giày và áo treo không phải người. Phản chiếu đèn trên nền không phải xe. |
| `img_008.jpg` | Chợ đêm, dãy xe máy đậu, người mặc áo phản quang, tuk-tuk phía xa. | Từng xe máy tách được là `motorcycle`. Người đứng hoặc ngồi trên xe là `person`. Tuk-tuk xa, nếu còn nhận ra ba bánh và cao ≥ 20 px, là `three_wheeler`. Khối người dưới mái không tách được thì `ignore_region`. |
| `img_009.jpg` | Minibus kem `75B-0946` ngang phố, khách sau kính, xe máy và người trên vỉa hè. | `bus`. Khách còn thấy đầu là `person` mức 2 hoặc 3. Người áo vàng và người đi xe máy là `person`. Xe máy là `motorcycle`. Chó và biển quảng cáo không có lớp. |
| `img_010.jpg` | Xe ga chở hai người, người bán hàng, xe đạp mẹt trái cây, người ngồi trên xe ga khác. | Xe ga là `motorcycle` (hai người phía trái = hai `person`). Xe đạp dưới mẹt chuối là `bicycle`. Người đứng bán và người ngồi xe bên phải là `person`. Chuối, túi và nón lá không có box. |
| `img_011.jpg` | Tượng Predator, xe máy độ kim loại, đám người lễ hội, xe trắng phía xa. | Predator không phải `person`. Xe còn bánh, yên, tay lái là `motorcycle`, một box cho cả phần trang trí gắn trên xe. Người gần, tách được, cao ≥ 20 px là `person`. Đám xa không tách được là `ignore_region`. |
| `img_012.jpg` | Nhìn vào thùng bán tải đầy thùng carton và túi; SUV Mazda bên trái; một bán tải và một ô tô phía trước. | Bán tải cận cảnh là `truck`, `truncated = yes` vì thùng bị mép dưới cắt. Hàng không có box. Mazda là `car`. Xe thùng hở phía trước là `truck`. Ô tô nhỏ xa hơn là `car` nếu cao ≥ 20 px. |
| `img_013.jpg` | Đêm mưa, hai người đi trên vỉa hè, xe và xe máy xa, tượng trang trí, nền phản chiếu. | Hai người đi bộ là `person`. Không box bóng của họ trên nền ướt. Xe máy đậu và ô tô xa là lớp tương ứng nếu cao ≥ 20 px. Tượng con vật và nón giao thông không có lớp. |
| `img_014.jpg` | Hai người đi bộ rõ nét, xe phía sau nhoè mạnh. | Hai `person`. Dải phương tiện nhoè không tách được từng xe: một `ignore_region`. Không gán người mờ chỉ còn vệt. |
| `img_015.jpg` | Phố mưa, ô tô đỏ và SUV bạc cắt hai mép, ô tô đậu dọc nhà, nền ướt. | Mỗi ô tô thật là `car`, xe cắt mép thì `truncated = yes`. Xe nhoè giữa phố nếu còn nhận ra thân ô tô thì `car`. Không box hình phản chiếu trên mặt đường và trên kính cửa hàng. |
| `img_016.jpg` | Hai tuk-tuk cắt hai mép, xe Vespa chở cuộn dây, van taxi, người áo đỏ sát camera. | Hai `three_wheeler`, `truncated = yes`. Vespa là `motorcycle`, người lái là `person`, cuộn dây không kéo box. Van taxi là `van`. Ô tô đen phía sau là `car` nếu nhận ra. Người áo đỏ là `person`, cắt mép phải và mép dưới. |
| `img_017.jpg` | Tượng đồng người cưỡi ngựa, đội nón giao thông, có chim. | 0 box. Tượng, ngựa, nón và chim đều ngoài lớp. Không vẽ `ignore_region`. |
| `img_018.jpg` | Biển bầu cử có chân dung; bãi ô tô sau hàng rào. | Chân dung không phải `person`. Từng ô tô sau rào là `car` (SUV tối, sedan đen, sedan bạc, các xe hai bên). `occluded_level` 1 khi rào và cỏ che từ 10% đến dưới 40%. `truncated = yes` với xe cắt mép trái hoặc phải. |
| `img_019.jpg` | Xe parade vàng biển `YR04 NUM`, người lái, mascot chuột, đám đông sau rào. | Xe là `car`. Người lái là `person`. Mascot không phải `person`. Từng người tách được và cao ≥ 20 px là `person`. Chỗ đầu người dính thành một mảng thì `ignore_region` đúng mảng đó. Đầu người cắt mép dưới phải là `person`, `truncated = yes`. |
| `img_020.jpg` | Gương chiếu hậu xe chủ, trong gương có xe và cầu vồng. | 0 box. Gương và cửa là xe chủ. Xe trong gương là phản chiếu. |
| `img_021.jpg` | Dòng xe máy dày đặc lúc chập choạng, vài ô tô, xe buýt xa. | Phía trước: mỗi xe máy một `motorcycle`, mỗi người một `person`. Ô tô trắng và ô tô xanh là `car`. Xe buýt cuối đường là `bus` nếu nhận ra và cao ≥ 20 px. Khối mũ phía xa không tách từng người được: `ignore_region`. |
| `img_022.jpg` | Ảnh trắng đen, xe máy có sidecar trên đường đất, thấy mũ người lái. | Một `motorcycle` ôm xe và sidecar. `person` cho người lái khi phần nhìn thấy cao ≥ 20 px; sát ngưỡng thì tick `can_review`. |
| `img_023.jpg` | Xích lô, người đạp quay lưng, Civic đen, xe máy và người trên phố. | Xích lô là `three_wheeler`. Người đạp là `person`. Civic là `car`. Xe máy xa và người đứng, người ngồi là lớp tương ứng nếu đủ cao. Mặt người trên poster bên phải không box. |
| `img_024.jpg` | Nhà xe: wagon đen, thân xe vàng trên nóc, wagon gỗ, xe cam và hàng xe phía trong. | Tất cả là `car`, mỗi xe một box, kể cả xe vàng trên nóc. Phản chiếu trên sơn đen không phải xe thêm. Không có người. |
| `img_025.jpg` | Lối đi biển, người đi bộ, người ngồi ghế, đường bên phải có xe máy sidecar, taxi và SUV. | Người đi bộ tách được là `person`. Người và xe quá nhỏ phía xa: `ignore_region` cho cụm đó. Xe máy và sidecar là một `motorcycle`, người mặc đỏ là `person`. Taxi vàng-xanh và SUV bạc là `car`. Thuyền ngoài biển không có lớp. |
| `img_026.jpg` | Đêm, hai người trên xe máy đỏ, phía sau là tranh tường cảng và tàu. | 1 `motorcycle` + 2 `person`. Tranh tàu không phải xe. Người phía trước che một phần người lái: mức che của người lái theo % bị che. |
| `img_027.jpg` | Tượng bán tải đen trên bệ đá trong nghĩa trang. | 0 box. Đó là đài, không phải xe đang ở trên đường. |
| `img_028.jpg` | Bán tải nâu cổ đậu trên phố, ngựa tượng đứng trong thùng, ô tô đỏ phía sau. | Bán tải là `truck`. Ngựa tượng không có box. Ô tô đỏ là `car`, bị bán tải che một phần. |
| `img_029.jpg` | Người trên scooter và người trên xe đạp cùng đỡ một ống thép dài. | Scooter là `motorcycle`, xe đạp là `bicycle`, mỗi người một `person`. Box không chạy theo ống ra ngoài thân xe. Người đi bộ và người đạp phía xa: box nếu cao ≥ 20 px. |
| `img_030.jpg` | Bãi xe máy dày, người mặc đồ xanh, poster chân dung. | Từng xe máy tách được biên là `motorcycle`, mức che theo xe đè lên nhau. Chỗ không tách được biên: `ignore_region`. Người đứng là `person`. Poster không phải `person`. |
| `img_031.jpg` | Phố đêm ướt: SUV trắng, ô tô, xe buýt số 821, xe máy, người trên vỉa hè, nhân vật vẽ trên nhà. | SUV và các ô tô là `car`. Xe buýt là `bus`. Xe máy là `motorcycle`. Người trên vỉa hè là `person` nếu tách được và đủ cao. Không box phản chiếu trên mặt đường. Nhân vật vẽ trên tường không phải `person`. |
| `img_032.jpg` | Bến xe buýt, hàng người đứng tách nhau, ô tô xanh cắt mép, van trắng và xe trong bãi. | Từng người tách được một `person`, mức che khi người đứng chồng lên nhau. Ô tô xanh là `car`, `truncated = yes`. Van trắng là `van`. Ô tô trong bãi là `car` nếu đủ cao. Nón giao thông không có lớp. Hình trên bảng chờ xe, nếu là ảnh in, không phải `person`. |
| `img_033.jpg` | Tủ kính: ma-nơ-canh, ảnh người mặc váy, phản chiếu gương xe. | 0 box. Ma-nơ-canh và ảnh không phải `person`. Gương xe nằm trên kính là phản chiếu. |
| `img_034.jpg` | Người đi bộ băng qua đường, sedan đen, xe máy, xe đạp, người mũ xanh cắt mép phải. | Người áo sọc là `person`. Sedan là `car`, bị người che một phần nên mức 1 nếu phần che từ 10% đến dưới 40%. Xe số và xe ga là `motorcycle`, xe có khung đạp là `bicycle`, mỗi người lái một `person`. Người và xe mép phải: `truncated = yes`. |
| `img_035.jpg` | Auto-rickshaw vàng chất bao, rickshaw vàng thứ hai, xe máy, ô tô trắng. | Mỗi rickshaw một `three_wheeler`. Bao tải không kéo box lên đỉnh chồng hàng. Người lái nhìn thấy là `person`. Xe máy và người mũ bảo hiểm là `motorcycle` + `person`. Ô tô trắng là `car`. |
| `img_036.jpg` | Veryca xanh thùng bạt, xe máy đậu kín hai bên, áp phích có người. | Veryca là `truck`. Từng xe máy tách được là `motorcycle`. Người trong áp phích không box. Phản chiếu nhà trên kính lái không phải xe. |
| `img_037.jpg` | Bán tải trắng nắp thùng cao, hai xe buýt xanh, một người đi bộ. | Bán tải là `truck`. Hai xe buýt là `bus`. Người là `person`. |
| `img_038.jpg` | Tủ đồ chơi: xe mô hình, vịt cao su, búp bê, thú bông. | 0 box. Phản chiếu trên kính tủ cũng không box. |
| `img_039.jpg` | Phố nhỏ: xe máy trong cửa hàng, người đi bộ, xe ga, xe đạp, xe máy, xe đậu. | Xe trong cửa hàng và xe đang đi là `motorcycle` hoặc `bicycle` đúng loại. Mỗi người đi bộ hoặc đang lái một `person`. Ô tô xa là `car` nếu đủ cao. Cụm người và xe cuối phố dưới 20 px: `ignore_region`. Biển hiệu quán không phải người. |
| `img_040.jpg` | Người mũ bảo hiểm sát camera, taxi xanh, tuk-tuk, SUV đen, xe buýt 511. | Người mũ bảo hiểm là `person`, `truncated = yes` ở mép dưới. Taxi xanh là `car`. Gương góc dưới trái thuộc taxi. Tuk-tuk là `three_wheeler`; người lái thấy sau kính là `person` mức 2. SUV là `car`. Xe buýt 511 là `bus`. Hình dán mặt người trên kính và hình trong kính mũ không box. |

---

## 5. QC và phiên bản

Ngưỡng lấy từ mục `rules` của taxonomy. Không sửa các số này.

| Việc | Ngưỡng |
|---|---|
| Không gán từng vật | Chiều cao phần nhìn thấy < 20 px → `ignore_region` |
| IoU khi so box | Cao ≥ 50 px: IoU ≥ 0.85. Cao từ 20 đến dưới 50 px: IoU ≥ 0.7 |
| IAA | IoU trung bình ≥ 0.85 và cùng lớp ≥ 95%, luôn ghi mẫu số (số cặp box) |
| Release | Tỉ lệ ảnh có ít nhất một lỗi ≤ 2% sau QC. Trên 2%, hoặc lỗi lặp một kiểu, hoặc IAA dưới ngưỡng → Rework. Guideline chưa rõ hoặc ảnh hỏng → Hold. |

Ai quyết ca mơ hồ: trong Pha 1 và Pha 3, người gán tick `can_review` và không hỏi người kia đang gán gì. Pha 2 và Pha 5 cả nhóm xem ảnh rồi chốt một quyết định, ghi vào guideline phiên bản mới.

Ảnh 0 box vẫn phải có trong COCO: `img_017.jpg`, `img_020.jpg`, `img_027.jpg`, `img_033.jpg`, `img_038.jpg`.

| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| v0 | Năm lớp `car`, `truck`, `van`, `motorcycle`, `person` và `ignore_region`. Mức che 0–3 không có %. Không có ca khó. | Bản giảng viên, cố ý chưa đủ. |
| v0.1-personal | Thêm `bicycle`, `bus`, `three_wheeler`. Bán tải, thùng bạt và nắp thùng là `truck`. Hiace là `van`. Minibus và xe buýt là `bus`. Sidecar là một `motorcycle`. Ngưỡng che 10 / 40 / 70%. Tách `truncated` khỏi % che. Quy tắc người trên xe, xe chở xe, hàng hóa, vật không thật, xe chủ, vật nhỏ, đám đông. Mục 4 chốt trên `img_001.jpg` … `img_040.jpg`. | Những chỗ v0 để hai người gán khác nhau, đối chiếu đúng khung ảnh. |
