# Guideline gán nhãn — v0.1 cá nhân — LeMinhThang

- Phiên bản: v0.1 — dự thảo cá nhân, chưa khóa để gán nhãn.
- Ngày: 16/11/2026.
- Người viết: Lê Minh Thắng, có AI hỗ trợ soạn thảo; cần tự kiểm lại.
- Người duyệt: Chưa duyệt, chờ họp nhóm.
- Phạm vi: `img_001`–`img_020`. Cần xem thêm 20 ảnh còn lại trước khi hoàn thiện bài cá nhân.
- Công cụ: CVAT, bounding box, xuất COCO 1.0.

## 1. Mục tiêu

Tạo nhãn để huấn luyện mô hình phát hiện người và phương tiện trên ảnh đường phố, phục vụ quan sát giao thông.

Ưu tiên tránh bỏ sót người, nhầm người với tượng hoặc hình in, nhầm loại xe và gộp nhiều vật thể vào một box. Những lỗi này có thể khiến mô hình nhận diện sai tình huống giao thông.

## 2. Lớp và thuộc tính

### Lớp

Mỗi vật thể chỉ có một lớp. Các lớp `bicycle`, `bus`, `three_wheeler` là đề xuất bổ sung, chưa được sử dụng chính thức trước khi nhóm chốt taxonomy.

| Lớp | Định nghĩa | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con có khoang chở người, gồm sedan, hatchback, SUV và MPV thân xe con. | Ô tô đỏ trên xe vận chuyển ở `img_002`; SUV ở `img_015`. | Pickup có thùng hàng riêng thuộc `truck`. |
| `truck` | Xe tải hoặc xe có thùng/sàn chở hàng riêng, gồm pickup. | Pickup ở `img_001`; xe chở xe ở `img_002`; xe tải thùng ở `img_007`. | Van thân kín liền khối. |
| `van` | Xe thân hộp kín liền khối, dùng chở hàng hoặc ít người, không có thùng hàng tách biệt. | Xe phía sau nhóm người ở `img_005`. | Xe buýt, pickup, MPV thân xe con. |
| `motorcycle` | Xe máy hoặc mô tô hai bánh có động cơ. | Xe tay ga ở `img_008`, `img_010`. | Xe đạp và tuk-tuk ba bánh. |
| `person` | Người thật, gồm người đi bộ, người lái và hành khách trên xe. | Người bán hàng ở `img_003`; người ngồi trên xe ở `img_010`. | Tượng, ma-nơ-canh, hình người in trên biển. |
| `bicycle` — đề xuất | Xe đạp có bàn đạp, không phải xe máy. | Xe đạp ở `img_003`, `img_006`. | Xe máy; xe đẩy bán hàng. |
| `bus` — đề xuất | Phương tiện thiết kế chở nhiều hành khách, có khoang khách dài và nhiều hàng ghế. | Xe khách ở `img_009`. | Van ít chỗ hoặc xe tải thùng. |
| `three_wheeler` — đề xuất | Phương tiện cơ giới ba bánh kiểu tuk-tuk. | Tuk-tuk ở `img_004`, `img_016`. | Xe máy hai bánh. |
| `ignore_region` | Vùng chứa mục tiêu quá nhỏ hoặc không thể phân biệt đáng tin cậy để gán từng vật. | Nhóm người quá nhỏ ở xa hoặc vùng xe nhòe không tách được. | Không dùng để bỏ qua vật rõ chỉ vì khó vẽ. |

**Vật ngoài danh sách lớp:**

- Không gán cây, nhà, hàng hóa, biển quảng cáo, động vật và xe đẩy nếu taxonomy không có lớp tương ứng.
- Không tự tạo lớp trong lúc gán.
- Trường hợp cần lớp mới phải đưa ra họp nhóm.
- `ignore_region` không phải lớp chứa mọi vật ngoài phạm vi.

### Thuộc tính

Áp dụng cho các box vật thể; không diễn giải mức che khuất của cả vùng `ignore_region` như một vật.

| Thuộc tính | Giá trị cố định | Quy tắc |
|---|---|---|
| `occluded_level` | `0` | Không bị vật khác che. |
| `occluded_level` | `1` | Bị che trên 0% đến dưới 30%. |
| `occluded_level` | `2` | Bị che từ 30% đến 70%. |
| `occluded_level` | `3` | Bị che trên 70%. |
| `truncated` | `yes` / `no` | `yes` khi vật thực sự bị mép ảnh cắt mất; còn lại là `no`. |
| `can_review` | tick / không tick | Tick khi chưa chắc lớp, biên box hoặc thuộc tính. |

Tỉ lệ che là ước lượng phần diện tích hình chiếu của vật bị vật khác che so với toàn vật. Phần mất do mép ảnh được ghi bằng `truncated`, không tính vào mức che.

Nếu không thể ước lượng đáng tin cậy, tick `can_review`; không dùng mức `3` để thay cho “không biết”.

## 3. Quy tắc vẽ box

### R-01 — Một vật, một box

Mỗi vật thể phân biệt được có một box riêng. Không gộp nhiều người hoặc nhiều xe vào một box vật thể.

### R-02 — Ôm sát phần nhìn thấy

Box là hình chữ nhật nhỏ nhất bao toàn bộ phần nhìn thấy thuộc vật đó. Không đoán và kéo box tới phần bị che.

Nếu vật có nhiều phần nhìn thấy rời nhau do che khuất, một box bao tất cả các phần nhìn thấy của cùng vật; khoảng trống giữa chúng có thể nằm trong box.

### R-03 — Vật bị che

Vẫn gán nếu xác định được vật, lớp và biên phần nhìn thấy. Điền `occluded_level` theo mức che.

Nếu chỉ thấy mảnh quá mơ hồ, ghi vấn đề cấp ảnh để reviewer xem; không đoán lớp.

### R-04 — Cắt mép ảnh

Vẽ tới biên phần nhìn thấy trong ảnh và đặt `truncated=yes`. Không kéo box ra ngoài ảnh.

### R-05 — Người và xe tách riêng

Người lái, mỗi hành khách và phương tiện có box riêng nếu đủ điều kiện gán.

Box người không bao cả xe; box xe không cố ý bao người. Các box vẫn có thể chồng nhau do hình dạng và vị trí vật thể.

### R-06 — Xe chở xe

Gán một box cho xe vận chuyển, gồm cabin và kết cấu chở hàng, không mở rộng chỉ để bao hàng hóa.

Mỗi ô tô thật được chở trên đó có một box riêng nếu nhận diện được. Không coi các ô tô này là bộ phận của xe vận chuyển.

### R-07 — Vật không thật và phản chiếu

Không gán lớp người hoặc phương tiện cho:

- Tượng, ma-nơ-canh, đồ chơi và mô hình trưng bày.
- Hình in trên biển, poster hoặc màn hình.
- Vật chỉ xuất hiện qua phản chiếu trong gương hoặc kính.

Không cần tạo `ignore_region` chỉ vì đó là tượng hoặc hình in.

### R-08 — Xe có ngoại hình đặc biệt

Không kết luận xe là đồ chơi chỉ vì hình dáng giống hoạt hình. Nếu có bằng chứng là phương tiện thật, phân lớp theo chức năng và kết cấu.

Nếu chưa phân biệt được xe hoạt động thật với đạo cụ hoặc mô hình, ghi “chưa chốt, cần họp”; không tự kết luận chỉ từ ngoại hình.

### R-09 — Xe chủ, phụ kiện và hàng hóa

- Bỏ qua phần xe chủ mang camera nếu xác định chắc chắn; không suy ra xe chủ chỉ vì xe ở sát máy ảnh.
- Gương, bánh và bộ phận gắn liền thuộc box xe.
- Hàng hóa hoặc đồ người cầm không có box riêng nếu ngoài taxonomy; không mở rộng box người để bao hàng hóa.

### R-10 — Vật quá nhỏ

Đo chiều cao box phần nhìn thấy trên ảnh gốc:

- Cao từ **20 px** trở lên: gán từng vật nếu nhận diện được.
- Cao dưới **20 px**: không gán box vật thể, dùng `ignore_region` bao vùng mục tiêu quá nhỏ.

Không thu nhỏ ảnh hiển thị rồi dùng kích thước đó để đo.

### R-11 — Đám đông và xe dày đặc

Gán từng vật đủ rõ, kể cả khi các box chồng nhau. Chỉ dùng `ignore_region` ở vùng không thể tách từng vật hoặc gồm các mục tiêu dưới ngưỡng.

Không phủ vùng ignore lên vật rõ đã gán nếu có thể tránh được.

### R-12 — Nhòe, tối và nhìn qua kính

- Vẫn gán khi đủ bằng chứng xác định lớp và biên.
- Không kéo box theo toàn bộ vệt nhòe nếu không xác định được đó là thân vật.
- Vùng không thể xác định đáng tin cậy: dùng ignore phù hợp hoặc ghi vấn đề cấp ảnh.
- Người thật nhìn trực tiếp xuyên qua kính có thể được gán; hình phản chiếu trên kính thì không.
- Không dùng độ tối hay nhòe để thay cho mức che khuất.

## 4. Ca khó

Các quyết định dưới đây là đề xuất cá nhân, cần tự kiểm lại ảnh và thống nhất trong cuộc họp.

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_001` | Pickup và người bị bàn/xe che; xe bị cắt mép. | R-03, R-04 | Đề xuất pickup là `truck`; gán riêng người đủ rõ, ghi thuộc tính từng vật. | Không gộp người với xe; tách che khuất và cắt mép. |
| `img_002` | Xe tải vận chuyển nhiều ô tô. | R-06 | Một box xe vận chuyển và các box riêng cho từng ô tô nhận diện được. | Các ô tô là vật độc lập, dù đang được chở. |
| `img_003` | Người gánh hàng, xe đạp và xe máy xen nhau. | R-05, R-09 | Tách người và phương tiện; không bao cả quang gánh vào box người. Đề xuất thêm `bicycle`. | Hàng hóa không phải bộ phận cơ thể. |
| `img_004` | Tuk-tuk và tài xế trong cabin. | R-05 | Đề xuất lớp `three_wheeler`; người thật đủ rõ có box riêng. | Tuk-tuk khác xe máy hai bánh. |
| `img_005` | Nhiều người ngồi sát nhau, xe bị che. | R-01, R-03, R-05 | Tách từng người và từng xe nhận diện được; không đoán xe chỉ từ việc thấy người đội mũ. | Tránh thêm box không có bằng chứng. |
| `img_006` | Xe đạp, xe máy và người tham gia giao thông. | R-05, R-10 | Tách người với xe; kiểm kích thước vật ở xa. | Tránh gộp người–xe và bỏ qua ngưỡng nhỏ. |
| `img_007` | Pickup gắn kết cấu chở hàng và xe tải trong khu vực tối. | R-02, R-12 | Đề xuất các xe chở hàng có thùng riêng là `truck`; bao phần kết cấu gắn liền nhìn thấy được. | Không phân lớp chỉ theo kích thước cabin. |
| `img_008` | Nhiều xe máy đỗ sát nhau vào ban đêm. | R-01, R-11, R-12 | Gán từng xe đủ rõ; chỉ ignore vùng thực sự không tách được. | Không bỏ cả cụm xe vì mật độ cao. |
| `img_009` | Xe khách có thể nhầm với van. | Mục 2 | Đề xuất `bus`; cần nhóm chốt ranh giới bus/van. | Taxonomy v0 chưa có lớp bus. |
| `img_010` | Người ngồi trên xe cạnh xe hàng, chân và thân bị che. | R-03, R-05, R-09 | Box riêng từng người và xe máy; không bao xe hàng vào box người. | Che khuất không làm các vật thành một đối tượng. |
| `img_011` | Tượng, mô hình kim loại giống sinh vật hoặc xe. | R-07, R-10 | Không gán mô hình trưng bày thành người/xe thật; kiểm riêng người và phương tiện thật phía sau. | Phân biệt vật thật với mô hình. |
| `img_012` | Pickup nhìn từ phía sau, có hàng trong thùng và bị cắt mép. | R-04, R-09 | Đề xuất `truck`, không gán hàng hóa. Không tự coi là xe chủ; tick review nếu chưa rõ. | Vị trí gần camera chưa chứng minh là xe chủ. |
| `img_013` | Đường phố tối, vật nhỏ ở xa. | R-10, R-12 | Gán vật đủ rõ và đủ kích thước; ignore vùng mục tiêu quá nhỏ hoặc không nhận diện được. | Không dựa vào bóng sáng để đoán vật. |
| `img_014` | Xe máy và người bị nhòe chuyển động. | R-12 | Gán phần nhận diện đáng tin cậy; vùng nhòe không xác định được cần ignore hoặc ghi vấn đề. | Không đoán biên theo vệt chuyển động. |
| `img_015` | Ô tô bị cắt hai bên ảnh, xe phía sau bị nhòe. | R-04, R-12 | Xe bị cắt có `truncated=yes`; xử lý xe nhòe theo bằng chứng thực tế. | Cắt mép khác với bị che hoặc nhòe. |
| `img_016` | Tuk-tuk, van, xe máy và người chồng lấn. | R-03, R-05 | Tách từng vật, đề xuất tuk-tuk là `three_wheeler`. | Không gộp các phương tiện vì box giao nhau. |
| `img_017` | Tượng người cưỡi ngựa. | R-07 | Không gán người trên tượng thành `person`. | Đây là tượng, không phải người thật. |
| `img_018` | Hình người trên biển quảng cáo, ô tô sau hàng rào. | R-03, R-07 | Bỏ hình người in; gán ô tô thật đủ điều kiện, có mức che phù hợp. | Hình in khác vật thật bị hàng rào che. |
| `img_019` | Xe hình hoạt hình, nhân vật hóa trang và đám đông. | R-08, R-11 | Chưa chốt xe là phương tiện thật hay đạo cụ; đưa họp nhóm. Không gán nhân vật thành người nếu chưa xác nhận có người bên trong. | Không đủ căn cứ để kết luận chức năng chỉ từ ngoại hình. |
| `img_020` | Xe chỉ xuất hiện trong gương, có phần xe mang camera. | R-07, R-09 | Không gán xe phản chiếu; bỏ phần xe chủ xác định chắc chắn. | Tránh coi ảnh phản chiếu là vật xuất hiện trực tiếp trong cảnh. |

Khi có box nhưng chưa chắc: tick `can_review`. Khi chưa thể vẽ box: ghi mã ảnh, vị trí và lý do trong vấn đề cấp ảnh. Dẫn Rule ID khi ghi nhật ký QC.

## 5. QC và phiên bản

### Ngưỡng kiểm tra

Giữ nguyên các ngưỡng `rules` của lab:

- Chiều cao box tối thiểu: **20 px**.
- IoU cho box cao từ **50 px**: **≥ 0,85**.
- IoU cho box cao từ **20 đến dưới 50 px**: **≥ 0,70**.
- IAA: IoU trung bình **≥ 0,85**, đồng thuận lớp **≥ 95%**, tính trên các cặp box ghép được.
- Báo riêng box không ghép được; IAA cao không tự chứng minh nhãn đúng.
- Duyệt toàn bộ lô để xét Release; tỉ lệ ảnh lỗi **≤ 2%**, không có lỗi lặp theo quy định lab.
- Luôn ghi tử số/mẫu số. Với lô 40 ảnh, 1 ảnh lỗi là **1/40 = 2,5%**, vượt ngưỡng.

### Xử lý và trách nhiệm

- Người gán tự kiểm ảnh, lớp, box và thuộc tính trước khi xuất COCO.
- Reviewer kiểm tra; ca chưa rõ do cả nhóm thảo luận, người được phân công ghi quyết định.
- Lưu dấu vết ảnh cần sửa, quy tắc áp dụng, người chốt và người kiểm lại.
- Đổi ý nghĩa quy tắc phải rà lại các ảnh chịu ảnh hưởng; không chỉ sửa ảnh đang tranh luận.
- Bản cá nhân được giữ nguyên sau họp. Quyết định nhóm được viết vào v1.0 và cập nhật v1.1 sau calibration.

### Lịch sử thay đổi

| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| v0 | Guideline khởi đầu của lab. | Quy tắc còn sơ sài. |
| v0.1 cá nhân | Đề xuất làm rõ lớp, mức che, quy tắc box và 20 ca khó. | Quan sát `img_001`–`img_020`; chưa xem đủ 40 ảnh, chưa được nhóm duyệt. |