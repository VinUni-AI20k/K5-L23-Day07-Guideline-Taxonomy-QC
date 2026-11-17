# Guideline gán nhãn — bản nháp cá nhân CP1 — 102

> **Bản nháp có AI hỗ trợ soạn.** Các ví dụ ảnh dưới đây được tổng hợp từ tài liệu lab và các bản nháp đang có trong repo; thành viên 102 cần tự mở ảnh gốc, xác minh ví dụ và sửa quyết định trước khi nộp. Các lớp `bus` và `tuk_tuk` là đề xuất cho CP2, chưa thuộc taxonomy v0 hiện tại.

- Phiên bản: `v0.1-102` (bản nháp, chưa duyệt)
- Ngày: `2026-11-16`
- Người viết: `102` (AI hỗ trợ soạn; cần tự kiểm nội dung)
- Người duyệt: chờ nhóm rà soát ở CP2

## 1. Mục tiêu

Tạo nhãn bounding box 2D cho người và phương tiện cơ giới thật trong ảnh đường phố để huấn luyện mô hình phát hiện vật thể. Mỗi đối tượng thuộc phạm vi cần được phát hiện đúng lớp và có box bám sát phần nhìn thấy. Bỏ sót người hoặc phương tiện, gán nhầm lớp, hay gán box cho vật giả đều làm nhiễu nhãn huấn luyện.

## 2. Lớp và thuộc tính

### Lớp

Sáu lớp đầu là lớp có trong taxonomy v0. `bus` và `tuk_tuk` là lớp đề xuất bổ sung ở CP2; chỉ dùng chúng sau khi nhóm khóa taxonomy v1.0. Ảnh ví dụ cần được người viết kiểm tra trực tiếp trước khi nộp.

| Lớp | Định nghĩa đề xuất | Ví dụ tham khảo | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô chở người kiểu sedan, hatchback, wagon hoặc SUV; không có thùng hàng tách biệt cabin. | Ô tô con ở `img_023.jpg`; ô tô con được chở ở `img_002.jpg`. | Bán tải có thùng hàng thuộc `truck`; xe mô hình thuộc ngoài phạm vi. |
| `truck` | Xe cơ giới chở hàng có khoang/thùng/sàn hàng riêng; gồm xe bán tải và xe chuyên chở ô tô. | Xe chở ô tô ở `img_002.jpg`; xe tải ở `img_036.jpg`. | Xe thân kín liền khối cỡ nhỏ thuộc `van`; tượng xe tải không phải vật thật. |
| `van` | Xe cơ giới có khoang kín liền khối với cabin, thường cỡ nhỏ hoặc trung bình, chở hàng nhẹ hoặc hành khách. | Xe thân hộp kín ở `img_005.jpg`. | Xe có thùng hàng riêng thuộc `truck`; xe buýt thân lớn thuộc `bus` nếu nhóm thêm lớp đó. |
| `bus` *(đề xuất CP2)* | Xe cơ giới thân lớn được thiết kế chở nhiều hành khách, thường có khoang khách và dãy cửa sổ/cửa lên xuống rõ. | Xe buýt ở `img_009.jpg`, `img_031.jpg` hoặc `img_037.jpg`. | Van/minibus nhỏ không có dấu hiệu thân xe buýt; cần nhóm chốt ca biên. |
| `tuk_tuk` *(đề xuất CP2)* | Xe ba bánh có động cơ với khoang chở khách hoặc hàng tích hợp, kiểu tuk-tuk/auto-rickshaw. | Tuk-tuk ở `img_004.jpg`, `img_016.jpg` hoặc `img_035.jpg`. | Xích lô đạp không động cơ ngoài phạm vi; mô tô có sidecar cần nhóm chốt cách xếp lớp. |
| `motorcycle` | Xe máy hoặc mô tô có động cơ. Đề xuất xếp mô tô có sidecar cố định vào lớp này. | Xe máy có người lái ở `img_005.jpg` hoặc `img_026.jpg`. | Xe đạp không động cơ; tuk-tuk nếu nhóm duyệt lớp riêng. |
| `person` | Người thật hiện diện trực tiếp trong cảnh, gồm người đi bộ, người đứng/ngồi và người lái hoặc ngồi trên phương tiện. | Người đi bộ hoặc người trên xe ở `img_026.jpg`. | Tượng, ma-nơ-canh, hình người in trên biển, đồ chơi và ảnh phản chiếu. |
| `ignore_region` | Vùng cục bộ chứa đối tượng thuộc phạm vi nhưng quá nhỏ hoặc quá dày/chồng lấp để gán riêng đáng tin cậy. Đây là vùng bỏ qua, không phải lớp vật thể. | Cụm người/xe ở xa trong `img_021.jpg` hoặc `img_032.jpg`, sau khi kiểm kích thước và khả năng tách. | Không dùng để bỏ qua xe đạp, tượng, hình in hay vật khác vốn ngoài phạm vi. |

**Đối tượng ngoài phạm vi:** Taxonomy v0 không có lớp xe đạp/xích lô không động cơ, động vật, hàng hóa rời hay vật cản. Đề xuất không gán box cho các vật đó và không dùng `ignore_region` để đánh dấu chúng. Người thật đi hoặc ngồi trên các phương tiện này vẫn thuộc lớp `person` nếu nhìn thấy và đạt ngưỡng. Tượng, ma-nơ-canh, đồ chơi/mô hình, hình in và phản chiếu không phải người/phương tiện thật trong cảnh nên không gán lớp mục tiêu.

### Thuộc tính

| Thuộc tính | Giá trị | Định nghĩa / cách chọn |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Ước lượng phần đối tượng bị vật khác che; không tính phần nằm ngoài khung ảnh. `0`: không bị che; `1`: che trên 0% đến 30%; `2`: che 31% đến 70%; `3`: che trên 70% nhưng vẫn nhận diện được lớp. Nếu không thể nhận diện chắc chắn, ghi vấn đề hoặc tick `can_review` khi vẫn vẽ được box có căn cứ. Ngưỡng 30%/70% là đề xuất để nhóm xác nhận ở CP2. |
| `truncated` | `no`, `yes` | `yes` khi một phần thực của đối tượng bị cắt bởi mép ảnh; `no` nếu vật chỉ chạm mép hoặc bị vật khác che. Có thể đồng thời `truncated=yes` và `occluded_level > 0`. |
| `can_review` | tick / không tick | Tick khi đã vẽ được box nhưng còn chưa chắc về lớp, ranh giới hoặc thuộc tính. Nếu chưa xác định được có đối tượng nào cần vẽ hoặc không xác định được vùng box, ghi vấn đề cấp ảnh (`image`, `annotator`, `region`, `note`) thay vì tự đoán. |

`ignore_region` không cần các thuộc tính đối tượng trong cấu hình CVAT theo script của repo. Khi chọn `occluded_level`, dùng thuộc tính trong panel Objects của CVAT; cờ `occluded` mặc định của CVAT không thay thế thuộc tính này.

## 3. Quy tắc vẽ box

Các mã `R-01`–`R-08` dưới đây là mã tạm cho bản cá nhân; nhóm có thể thống nhất cách đánh số lại ở CP2.

- **R-01 — Chỉ gán vật thật thuộc phạm vi:** Gán người và phương tiện cơ giới thật trong cảnh. Không gán tượng, ma-nơ-canh, đồ chơi/mô hình, hình in trên biển/áp phích, phản chiếu hoặc bộ phận của xe chủ chụp ảnh. Vật ngoài phạm vi không chuyển thành `ignore_region`.
- **R-02 — Box ôm phần nhìn thấy:** Dùng rectangle nhỏ nhất bao các phần nhìn thấy của cùng một đối tượng. Không suy đoán phần bị che khuất hoặc phần nằm ngoài ảnh. Nếu nhiều phần nhìn thấy thuộc cùng một đối tượng, một box có thể bao các phần đó.
- **R-03 — Tách người và phương tiện:** Mỗi người và mỗi phương tiện là đối tượng riêng, kể cả người đang lái/ngồi trên xe; box có thể chồng nhau. Box người ôm phần cơ thể nhìn thấy, box xe ôm phần cấu tạo xe nhìn thấy.
- **R-04 — Xe chở xe (`img_002`):** Đề xuất một box `truck` cho xe vận chuyển và box `car` riêng cho từng ô tô thật được chở nếu nhìn nhận diện được và đạt ngưỡng kích thước. Không gộp toàn bộ các xe con vào box của xe chở.
- **R-05 — Ranh giới thân xe và hàng hóa:** Tính các bộ phận cố định của xe (thân, bánh, mui/nắp gắn cố định) vào box xe; không kéo box theo hàng hóa rời nhô ra. Đề xuất xếp bán tải có thùng hàng/nắp thùng cố định vào `truck`; nhóm cần kiểm và chốt ca `img_037` với `van` ở CP2.
- **R-06 — Vật nhỏ và vùng dày:** Ngưỡng trong taxonomy là chiều cao box `20 px`. Đối tượng mục tiêu dưới `20 px`, hoặc cá thể trong cụm dày không thể tách đáng tin cậy, được đánh dấu bằng vùng `ignore_region` sát khu vực đó. Gán riêng các cá thể rõ và đủ ngưỡng; không dùng vùng rộng che các box có thể gán.
- **R-07 — Thuộc tính che khuất và cắt mép:** Chọn `occluded_level` theo phần bị vật khác che; chọn `truncated=yes` khi mép ảnh thật sự cắt mất đối tượng. Hai trường hợp độc lập, không dùng độ mờ làm mức che khuất.
- **R-08 — Ca chưa chắc:** Nếu vẫn vẽ được box có căn cứ, chọn phương án hợp lý nhất và tick `can_review`. Nếu chưa thể xác định có nên vẽ hoặc vùng nào thuộc đối tượng, ghi vào danh sách vấn đề cấp ảnh để nhóm/reviewer quyết sau khi khóa lượt gán.

## 4. Ca khó

Các quyết định trong bảng là **đề xuất ban đầu**, dựa trên mô tả trong tài liệu lab và guideline đang có; thành viên 102 cần tự kiểm từng ảnh gốc và sửa quyết định/lý do trước khi gửi riêng.

| Ảnh | Tình huống | Rule ID | Đề xuất ban đầu | Lý do / việc cần tự kiểm |
|---|---|---|---|---|
| `img_002.jpg` | Xe chở nhiều ô tô | R-02, R-04 | Một box cho `truck`; từng ô tô thật đủ rõ/đủ kích thước có box `car` riêng. | Kiểm xe con nào nhìn đủ rõ để nhận diện và đo được chiều cao box. |
| `img_004.jpg`, `img_016.jpg`, `img_035.jpg`, `img_040.jpg` | Tuk-tuk/auto-rickshaw | R-01, R-05 | Đề xuất thêm lớp `tuk_tuk` ở CP2; không gộp với `motorcycle`. | Xác nhận phương tiện có động cơ và khoang xe đặc trưng; lớp chưa có trong taxonomy v0. |
| `img_009.jpg`, `img_031.jpg`, `img_037.jpg`, `img_040.jpg` | Bus/xe khách cỡ lớn | R-05 | Đề xuất lớp `bus` riêng; minibus/van là ca cần phân biệt theo cấu tạo và chức năng nhìn thấy. | Nhóm cần thống nhất ranh giới `bus`–`van` trước khi khóa taxonomy. |
| `img_037.jpg` | Bán tải gắn nắp thùng cao | R-05 | Đề xuất `truck` vì có thùng hàng phía sau; tính nắp gắn cố định vào hình dạng xe. | Tự kiểm dấu hiệu cabin và thùng; nhóm cần thống nhất ranh giới với `van`. |
| `img_005.jpg`, `img_026.jpg` | Người lái/ngồi trên xe máy | R-02, R-03 | Tách box người và box xe; mỗi người nhìn thấy là một đối tượng riêng. | Tự kiểm từng người, phần cơ thể thấy được và box xe; không điền số lượng box khi chưa kiểm ảnh. |
| `img_011.jpg`, `img_017.jpg`, `img_027.jpg`, `img_033.jpg`, `img_038.jpg` | Tượng, ma-nơ-canh, mô hình/đồ chơi | R-01 | Đề xuất không gán người/xe cho vật trưng bày hoặc đồ chơi. | Kiểm xem trong cùng ảnh còn người/phương tiện thật nào thuộc phạm vi không. |
| `img_018.jpg`, `img_020.jpg` | Hình in hoặc phản chiếu | R-01 | Đề xuất không gán hình người/xe in trên vật thể hoặc ảnh phản chiếu. | Phân biệt hình trong cảnh thật với hình biểu diễn/ảnh phản chiếu. |
| `img_021.jpg`, `img_032.jpg` | Nhiều đối tượng ở xa hoặc chồng lấp | R-06 | Gán riêng vật đủ lớn/tách được; chỉ khoanh vùng phần nhỏ hoặc không thể tách. | Đo chiều cao trên ảnh gốc; không dùng `ignore_region` thay cho việc gán vật rõ. |
| `img_006.jpg`, `img_023.jpg`, `img_029.jpg` | Xe đạp hoặc xích lô không động cơ | R-01, R-03 | Đề xuất không gán box phương tiện; vẫn gán người thật nhìn thấy nếu đạt điều kiện. | Xác nhận phân biệt xe đạp/xích lô với phương tiện cơ giới. |

## 5. QC và phiên bản

Các ngưỡng sau lấy nguyên từ `submission/taxonomy.json → rules`; không sửa chúng.

| Nội dung | Ngưỡng |
|---|---:|
| Chiều cao box tối thiểu | `20 px` |
| IoU box cao từ `50 px` | `0.85` |
| IoU box thấp hơn `50 px` | `0.7` |
| IoU trung bình IAA | `0.85` |
| Đồng thuận lớp IAA | `95%` |
| IoU ghép cặp box | `0.5` |
| Tỷ lệ ảnh lỗi tối đa để xét Release | `2%` |

Giữ đủ ảnh được giao trong COCO, kể cả ảnh không có annotation. Reviewer cần kiểm cả box và vật bị bỏ sót bằng mắt; script chỉ kiểm cấu trúc, thuộc tính, kích thước/giới hạn box và mức đồng thuận, không chứng minh box ôm đúng vật hoặc cả nhóm không cùng hiểu sai.

| Phiên bản | Thay đổi | Lý do / ca liên quan |
|---|---|---|
| `v0` | Bản khởi đầu có sáu lớp và mô tả thuộc tính còn định tính. | Cần làm rõ ca che khuất, cắt mép, vật nhỏ và vật ngoài phạm vi. |
| `v0.1-102` | Bản nháp này định lượng thuộc tính, nêu quy tắc box và ghi các đề xuất cho ca khó; `bus`/`tuk_tuk` chờ CP2. | Các tình huống cần kiểm: `img_002`, `img_004`, `img_009`, `img_035`, `img_037` và ảnh có vật giả/phản chiếu. |
