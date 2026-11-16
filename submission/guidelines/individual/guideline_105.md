# Guideline gán nhãn — v0.1 — 048

- Phiên bản: v0.1 (bản cá nhân, đề xuất để họp)
- Ngày: 2026-11-16
- Người viết / duyệt: mã 048 / chưa duyệt
- Phạm vi rà soát: 40 ảnh `img_001`–`img_040`, phát hiện người và phương tiện trong ảnh đường phố.

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình phát hiện người và phương tiện thật trong ảnh. Bỏ sót người đi bộ, người đi xe máy hoặc xe thật có thể làm mô hình không nhận ra đối tượng giao thông; vì vậy gán mọi cá thể nhận diện được, kể cả khi bị che một phần. Không suy đoán phần khuất và không gán hình trang trí, hình in hay phản chiếu như vật thật.

## 2. Lớp và thuộc tính

### Lớp

| Lớp | Định nghĩa | Ví dụ | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô chở người, gồm sedan, hatchback, wagon và SUV. | Ô tô con trên đường. | Xe tải, van, tượng hoặc mô hình ô tô. |
| `truck` | Xe cơ giới chở hàng cỡ lớn, gồm cabin và thùng/khung chở hàng. | Xe tải chở hàng hoặc xe chở ô tô. | Van kín cỡ nhỏ; ô tô đang được chở. |
| `van` | Xe cỡ nhỏ có thân kín dạng hộp để chở người/hàng. | Van chở khách. | Pickup thùng hở, xe tải lớn. |
| `motorcycle` | Xe hai bánh có động cơ, gồm xe tay ga; sidecar gắn cố định được tính cùng xe. | Xe máy/xe tay ga. | Xe đạp, tuk-tuk hoặc xích lô. |
| `person` | Một người thật, kể cả người đi bộ, lái xe hoặc hành khách. | Người đi xe máy. | Tượng, người trên poster, hình vẽ. |
| `ignore_region` | Vùng có nhiều đối tượng mục tiêu chồng dày đến mức không thể tách từng cá thể đáng tin cậy. | Cụm xe máy dính liền ở xa. | Một xe đơn lẻ bị che nhưng vẫn nhận dạng được. |

Vật ngoài các lớp trên không gán nhãn. Không tạo lớp mới. Chỉ dùng `ignore_region` cho cụm vật thuộc phạm vi nhưng không tách được; không dùng cho tượng, hình in, phản chiếu hay phương tiện không thuộc taxonomy. Tuk-tuk và xích lô là phương tiện thật nhưng không có lớp phù hợp: ghi vấn đề cấp ảnh để reviewer quyết định, không ép vào lớp gần nhất.

### Thuộc tính

| Thuộc tính | Mức | Quy tắc |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Ước lượng tỷ lệ diện tích toàn vật bị vật khác che, không tính phần ngoài khung: `0` = 0%; `1` = >0–25%; `2` = >25–50%; `3` = >50% nhưng còn đủ dấu hiệu nhận dạng để đặt box. |
| `truncated` | `no`, `yes` | `yes` nếu vật thật bị mép ảnh cắt mất một phần; vật bị che bởi vật khác không phải truncated. |
| `can_review` | tick / không tick | Tick trên box đã tạo khi lớp hoặc thuộc tính còn nghi vấn; ghi rõ vùng và câu hỏi. Nếu chưa chắc có nên tạo box, ghi vấn đề cấp ảnh thay vì tạo box phỏng đoán. |

## 3. Quy tắc vẽ box

**R-01 — Box riêng cho từng vật.** Dùng hình chữ nhật song song cạnh ảnh, ôm sát biên ngoài của phần nhìn thấy. Không bao bóng, khoảng trống lớn, hàng hóa rời hoặc vật khác. Mỗi người và mỗi xe là một đối tượng riêng.

**R-02 — Người đi xe máy.** Vẽ một box `motorcycle` cho phần xe nhìn thấy và một box `person` cho từng người nhận diện được. Box người ôm phần thấy được từ đầu/mũ bảo hiểm đến chân/giày, không gồm xe; box xe không gồm người. Người lái và hành khách có box riêng nếu phân biệt được từng người. Không suy đoán phần bị che. Thử cùng quy tắc trên ảnh khác: trong `img_005`, người lái/khách phân biệt được và từng xe có box riêng; trong `img_023`, người trên xích lô vẫn là `person`, còn xích lô không có lớp phù hợp.

**R-03 — Xe chở xe.** Gán `truck` cho xe chở và một box `car` riêng cho mỗi ô tô thật trên giá nếu nhận ra được. Không gộp xe chở với hàng xe. Ví dụ `img_002`.

**R-04 — Che khuất, cắt mép và đám đông.** Box chỉ ôm phần thấy được. Gán đối tượng bị che nếu còn nhận dạng được; tách từng cá thể khi còn thấy ranh giới. Nếu một cụm thuộc lớp mục tiêu quá dày để tách, dùng một `ignore_region` cho cụm, không tạo box lớp thông thường gộp nhiều vật.

**R-05 — Vật quá nhỏ.** Chỉ gán nếu phần nhìn thấy rộng và cao ít nhất 10 px ở ảnh gốc, đồng thời nhận ra được lớp bằng hình dạng. Dưới ngưỡng thì bỏ qua, không phóng to để quyết định; ghi ảnh nếu đó là ca biên đáng lưu ý.

**R-06 — Tượng, hình in, đồ chơi và phản chiếu.** Không gán người/xe trên poster, tranh, màn hình, tượng, đồ chơi, xe mô phỏng hoặc ảnh phản chiếu trong gương/kính/vũng nước. Gán vật thật ở cạnh chúng nếu đủ điều kiện. Nếu không phân biệt được phản chiếu với vật thật, ghi `can_review` cấp ảnh.

**R-07 — Phương tiện ngoài taxonomy.** Tuk-tuk ở `img_004` và xích lô ở `img_023` không được ép thành `motorcycle`/`car`; ghi câu hỏi reviewer cấp ảnh. Sidecar gắn cố định với xe máy được tính cùng một box `motorcycle` nếu xe hai bánh chính nhận diện rõ.

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_002` | Xe tải chở nhiều ô tô | R-03 | Một box `truck`; mỗi ô tô nhìn rõ có box `car` riêng. | Xe chở và hàng chở là các đối tượng khác nhau. |
| `img_004` | Tuk-tuk ba bánh | R-07 | Không gán lớp hiện có; hỏi reviewer về phạm vi taxonomy. | Phương tiện thật nhưng không phải xe hai bánh hay ô tô con. |
| `img_005` | Nhiều người trên xe máy, bị che nhau | R-02, R-04 | Tách từng người và xe nhận diện được; box phần thấy; tick review nếu chưa chắc số người/ranh giới. | Không nội suy vùng khuất; người và xe là hai lớp riêng. |
| `img_007` | Dòng xe máy đông, vật ở xa nhỏ | R-04, R-05 | Tách cá thể đủ ngưỡng; cụm không tách được dùng `ignore_region`; bỏ qua vật dưới 10×10 px. | Tránh box tùy tiện cho vật không nhận dạng được. |
| `img_014` | Tượng người cưỡi ngựa | R-06 | Không gán người hoặc ngựa. | Đây là tượng, không phải người thật; ngựa ngoài taxonomy. |
| `img_015` | Người trên billboard | R-06 | Bỏ qua hình người in; gán xe thật phía dưới nếu đạt ngưỡng. | Hình in không phải người trong cảnh. |
| `img_018` | Cảnh/xe trong gương chiếu hậu | R-06 | Bỏ qua vật phản chiếu. | Phản chiếu không phải đối tượng độc lập. |
| `img_020` | Đám đông xe máy và người | R-04, R-05 | Tách cá thể đủ rõ; vùng dính không tách dùng `ignore_region`; vật quá nhỏ bỏ qua. | Không thể định vị box cá thể đáng tin cậy trong vùng quá dày. |
| `img_021` | Xe máy có sidecar | R-07 | Một box `motorcycle`, người có box `person` riêng. | Sidecar gắn liền được tính vào cấu hình xe máy. |
| `img_023` | Người đi xích lô | R-02, R-07 | Gán `person`; không gán xích lô; hỏi reviewer về taxonomy. | Người vẫn thuộc lớp dù phương tiện không thuộc lớp hiện có. |
| `img_026` | Tượng xe tải | R-06 | Không gán phương tiện. | Xe là tượng trang trí. |
| `img_027` | Người chở vật dài bằng xe | R-01, R-04 | Gán người và xe máy thật nếu thấy; không gồm vật chở trong box; xe đạp bỏ qua. | Vật chở không phải phần thân xe; xe đạp ngoài taxonomy. |
| `img_028` | Bãi xe máy sát nhau | R-04 | Box riêng cho xe tách được; cụm dính không tách dùng `ignore_region`. | Mỗi box lớp thường ứng với một xe. |
| `img_017` | Xe diễu hành hình ô tô, nhân vật hoạt hình | R-06 | Bỏ qua xe mô phỏng và hình hoạt hình; gán người thật nếu nhìn rõ. | Không phải ô tô giao thông thật. |

**Loại theo quy tắc:** tượng, hình in, phản chiếu, đồ chơi/xe mô phỏng, xe đạp và vật dưới ngưỡng được bỏ qua nếu bản chất rõ. **Cần reviewer:** phương tiện thật không có lớp, không chắc số người/ranh giới trong vùng che dày, hoặc không biết vật là phản chiếu hay thật. Không tick `can_review` cho một box chưa tồn tại; ghi vấn đề cấp ảnh thay vào đó.

## 5. QC và phiên bản

Rà đủ 40 ảnh; kiểm lớp và thuộc tính đúng tập giá trị, mỗi box ứng với một đối tượng, box không bao phần khuất hoặc vật khác. Reviewer xem mọi box `can_review`, `ignore_region` và vấn đề cấp ảnh. Nhóm cần chốt các đề xuất ngưỡng 10×10 px và mức che trước khi khóa guideline; nếu thay đổi quy tắc gán thì rà lại mọi ảnh cùng tình huống.

| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| v0.1 | Bổ sung quy tắc box, mức thuộc tính và quyết định ca biên có ID ảnh. | Làm rõ các điểm chưa quy định trong v0. |
