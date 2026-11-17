# Guideline gán nhãn v1.1 — Day 07

> Bản calibration do reviewer 102 chốt ngày 17/11/2026 sau khi rà ảnh và đối chiếu các ca bất đồng. Bản này giữ taxonomy v1.0 và làm rõ quy tắc xử lý nhận diện xe, nhòe chuyển động.

- Phiên bản: `v1.1` (đã calibration; taxonomy giữ `v1.0`)
- Phạm vi: 40 ảnh đường phố, bounding box 2D, CVAT, xuất COCO 1.0
- Mã quy tắc: `R-01`–`R-09`; dùng các mã này thống nhất trong nhật ký, calibration và QC.

## 1. Mục tiêu

Tạo nhãn bounding box 2D nhất quán cho người và phương tiện cơ giới thật trong ảnh đường phố, phục vụ huấn luyện mô hình phát hiện đối tượng. Gán đúng từng cá thể thuộc phạm vi, đúng lớp và box ôm sát phần nhìn thấy. Tránh bỏ sót đối tượng đủ điều kiện, nhầm lớp, hoặc gán nhãn cho tượng, hình in và phản chiếu.

## 2. Lớp và thuộc tính

### Lớp

Taxonomy v1.0 gồm 9 lớp theo đúng tên và thứ tự trong CVAT Raw: `car`, `truck`, `van`, `motorcycle`, `person`, `ignore_region`, `three_wheeler`, `bus`, `bicycle`.

| Lớp | Định nghĩa thao tác | Ví dụ tham khảo | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô chở người kiểu sedan, hatchback, wagon hoặc SUV; không có khoang hàng tách biệt cabin. | Ô tô con; xe con trên xe chuyên chở (`img_002`). | Bán tải có thùng hàng thuộc `truck`; đồ chơi/mô hình không thuộc phạm vi. |
| `truck` | Xe cơ giới chở hàng có cabin và thùng/sàn hàng riêng; gồm xe bán tải và xe chuyên chở ô tô. Nắp thùng gắn cố định không đổi lớp bán tải. | Xe chuyên chở ô tô (`img_002`); xe tải thùng (`img_036`); bán tải (`img_037`). | Xe khoang kín liền thân với cabin thuộc `van`; xe buýt chở khách thuộc `bus`. |
| `van` | Xe cơ giới cỡ nhỏ/trung có khoang kín liền thân với cabin, chở hàng nhẹ hoặc hành khách; không có thùng/sàn hàng tách biệt. | Xe van thân hộp kín (`img_005`). | Bán tải có thùng riêng thuộc `truck`; xe buýt thân lớn thuộc `bus`. |
| `motorcycle` | Xe máy/mô tô có động cơ. Mô tô có sidecar cố định được gán một box `motorcycle` bao cụm xe gắn liền. | Xe máy/mô tô trên đường (`img_005`, `img_026`). | Xe đạp thuộc `bicycle`; tuk-tuk có khoang tích hợp thuộc `three_wheeler`. |
| `person` | Người thật hiện diện trực tiếp trong cảnh: người đi bộ, đứng/ngồi, người lái và hành khách nhìn thấy. | Người đi bộ hoặc người trên phương tiện (`img_026`). | Tượng, ma-nơ-canh, đồ chơi, hình người in và phản chiếu. |
| `ignore_region` | Vùng cục bộ chứa đối tượng thuộc phạm vi nhưng quá nhỏ hoặc quá dày/chồng lấp để gán riêng đáng tin cậy. Không đại diện cho một vật thể cụ thể. | Cá thể mục tiêu dưới 20 px hoặc phần cụm đông không thể tách. | Không dùng cho tượng, hình in, vật ngoài phạm vi, hoặc để phủ lên đối tượng nhìn rõ. |
| `three_wheeler` | Xe ba bánh có động cơ với khoang khách hoặc hàng tích hợp kiểu tuk-tuk/auto-rickshaw. | Tuk-tuk/auto-rickshaw (`img_004`, `img_016`, `img_035`, `img_040`). | Xích lô đạp không động cơ ngoài taxonomy; mô tô sidecar thuộc `motorcycle`. |
| `bus` | Xe cơ giới thân lớn được thiết kế chở nhiều hành khách, nhận diện qua khoang khách lớn, dãy cửa sổ/cửa lên xuống và cấu trúc thân xe buýt. | Xe buýt/xe khách (`img_009`, `img_031`, `img_037`, `img_040`). | Van/minibus nhỏ không có cấu trúc xe buýt rõ thuộc `van`; xe chở hàng thuộc `truck`. |
| `bicycle` | Xe đạp không động cơ, gồm xe đạp nhìn thấy rõ trong cảnh. | Xe đạp (`img_003`, `img_006`, `img_023`, `img_029`). | Xe máy thuộc `motorcycle`; tuk-tuk có động cơ thuộc `three_wheeler`; xích lô đạp không phải xe đạp thuộc lớp này. |

Xe đạp không động cơ thuộc lớp `bicycle`; xích lô đạp và phương tiện không động cơ khác không có lớp riêng nên không gán box phương tiện. Người thật trên các phương tiện đó vẫn gán `person` nếu nhìn thấy và đủ điều kiện. Động vật, hàng hóa rời, vật cản, tượng, ma-nơ-canh, đồ chơi/mô hình, hình in, ảnh phản chiếu và bộ phận của xe chủ chụp ảnh không được gán vào lớp người/phương tiện. Không dùng `ignore_region` cho vật ngoài phạm vi.

### Thuộc tính

Các thuộc tính sau được áp dụng cho 8 lớp đối tượng; `ignore_region` không có thuộc tính đối tượng.

| Thuộc tính | Giá trị | Định nghĩa / cách chọn |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Ước lượng phần đối tượng nằm trong ảnh bị vật khác che; không tính phần ngoài khung ảnh. `0`: 0%; `1`: >0% đến 30%; `2`: >30% đến 70%; `3`: >70% nhưng vẫn nhận diện được lớp. Nếu không còn đủ dấu hiệu nhận diện, không gán mức `3` một cách suy đoán; đánh dấu xem lại theo `R-08`. |
| `truncated` | `no`, `yes` | `yes` khi mép khung ảnh cắt mất một phần thực của đối tượng; `no` khi vật chỉ chạm mép hoặc bị vật khác che. Có thể đồng thời bị che và bị cắt. Không áp dụng ngưỡng phần trăm cắt riêng. |
| `can_review` | `false`, `true` | Bật (`true`) khi đã vẽ được box có căn cứ nhưng còn nghi ngờ lớp, biên box hoặc thuộc tính. Nếu chưa xác định được có đối tượng cần gán hay vùng box nằm ở đâu, ghi vấn đề cấp ảnh thay vì tự đoán. |

## 3. Quy tắc vẽ box

- **R-01 — Đúng phạm vi:** Chỉ gán người và phương tiện thật thuộc taxonomy. Gán xe đạp không động cơ là `bicycle`; xích lô đạp và phương tiện không động cơ khác không có lớp thì không gán box phương tiện. Không gán tượng, ma-nơ-canh, đồ chơi/mô hình, ảnh/hình in, phản chiếu, hoặc bộ phận của xe chủ chụp ảnh. Vật thật nhìn qua kính vẫn được gán nếu nhận diện được.
- **R-02 — Box phần nhìn thấy:** Dùng rectangle nhỏ nhất bao các phần nhìn thấy của cùng một đối tượng. Box không vượt khung ảnh và không mở rộng theo phần bị che hoặc phần bị cắt mà người gán không nhìn thấy. Các phần nhìn thấy tách rời nhưng thuộc cùng đối tượng có thể nằm trong một box.
- **R-03 — Người và xe là hai đối tượng:** Vẽ box riêng cho từng người và từng phương tiện, kể cả người đang lái/ngồi trên xe. Box được phép chồng nhau. Box người ôm phần cơ thể nhìn thấy; box xe ôm phần cấu tạo của xe nhìn thấy.
- **R-04 — Xe chở xe (`img_002`):** Vẽ một box `truck` cho xe vận chuyển và box `car` riêng cho từng ô tô thật được chở nếu nhận diện được và box đạt chiều cao tối thiểu 20 px. Không gộp xe con vào box `truck`; không tạo box cho mô hình hoặc vật không nhận diện được là một xe hoàn chỉnh.
- **R-05 — Cấu tạo xe và hàng hóa:** Tính bánh, thân, mui hoặc nắp thùng gắn cố định vào box xe. Không kéo box theo hàng hóa rời nhô ra. Bán tải có thùng hàng, kể cả nắp gắn cố định, thuộc `truck`; khoang kín liền thân thuộc `van`. Dùng `bus` cho xe buýt thân lớn; `three_wheeler` cho xe ba bánh có động cơ với khoang tích hợp; mô tô sidecar thuộc `motorcycle`.
- **R-06 — Vật nhỏ và cụm dày:** Đo chiều cao phần nhìn thấy trên ảnh gốc. Từ 20 px trở lên, gán riêng nếu nhận diện và tách được. Dưới 20 px hoặc trong cụm không thể tách đáng tin cậy, khoanh `ignore_region` sát phần đó. Gán riêng các đối tượng rõ trước; không dùng vùng ignore rộng để bỏ qua chúng.
- **R-07 — Che khuất và cắt mép:** Chọn `occluded_level` cho phần bị vật khác che, `truncated` cho phần bị biên ảnh cắt. Không dùng độ mờ làm mức che khuất và không coi vật chỉ chạm mép là bị cắt.
- **R-08 — Ca cần xem lại:** Nếu có thể vẽ box nhưng chưa chắc, chọn phương án có căn cứ nhất và bật `can_review=true`. Nếu chưa thể quyết định có gán hay chưa xác định được vị trí, ghi `image`, `annotator`, `region`, `note` vào `submission/qc/image_issues.csv`. Không tự tạo box/lớp để lấp chỗ thiếu.
- **R-09 — Nhận diện xe và nhòe chuyển động:** Phân lớp theo cấu tạo nhìn thấy: bán tải có nắp/chụp thùng gắn cố định vẫn là `truck`; khoang kín liền cabin là `van`; xe buýt thân lớn là `bus`. Với ảnh tối hoặc vật đang chuyển động, chỉ gán khi vẫn nhận diện chắc chắn lớp và vị trí của người/xe. Box ôm phần thân chính nhận diện được, không kéo theo vệt nhòe hay bóng phản chiếu. Nếu biết có đối tượng nhưng chưa chắc lớp/biên box thì bật `can_review`; nếu chưa xác định được vùng thì ghi `image_issues.csv` theo R-08. Áp dụng các ca `img_014`, `img_015`, `img_016`, `img_037` và kiểm tra nhất quán trên cả lô.

## 4. Ca khó tham chiếu

Các ID dưới đây được dẫn từ tài liệu lab và guideline cá nhân. Quyết định calibration đã đối chiếu ảnh gốc; không suy ra số lượng box cho vật không nhận diện rõ.

| Ảnh | Tình huống | Rule | Cách xử lý v1.0 |
|---|---|---|---|
| `img_002` | Xe chuyên chở nhiều ô tô | R-02, R-04 | Một `truck`; mỗi `car` nhìn đủ rõ và đạt 20 px có box riêng. |
| `img_004`, `img_016`, `img_035`, `img_040` | Tuk-tuk/auto-rickshaw | R-01, R-05 | Gán `three_wheeler`; box theo cấu tạo xe, không kéo theo hàng hóa rời. |
| `img_009`, `img_031`, `img_037`, `img_040` | Bus/xe khách cỡ lớn | R-05 | Gán `bus` khi cấu trúc xe buýt/khoang khách lớn nhận diện được; van thân liền nhỏ là `van`. |
| `img_037` | Bán tải gắn nắp thùng cao | R-05, R-09 | Gán `truck`; nắp gắn cố định thuộc cấu tạo xe. |
| `img_005`, `img_026` | Người lái/ngồi trên xe máy | R-02, R-03 | Box riêng cho từng người đủ điều kiện và một box xe; tự kiểm từng người nhìn thấy. |
| `img_011`, `img_017`, `img_027`, `img_033`, `img_038` | Tượng, ma-nơ-canh, đồ chơi/mô hình | R-01 | Không gán các vật giả như người/xe; vẫn gán đối tượng thật khác trong cùng ảnh. |
| `img_018`, `img_020` | Hình in hoặc phản chiếu | R-01 | Không gán hình in/phản chiếu thành người/xe thật. |
| `img_021`, `img_032` | Cá thể nhỏ hoặc cụm chồng lấp | R-06 | Gán cá thể tách được; dùng `ignore_region` cục bộ cho phần dưới ngưỡng/không tách được. |
| `img_003`, `img_006`, `img_023`, `img_029` | Xe đạp không động cơ | R-01, R-03 | Gán từng xe đủ điều kiện là `bicycle`; gán riêng người thật nhìn thấy nếu đủ điều kiện. Xích lô đạp không có lớp phương tiện. |

### Quyết định calibration đã chốt

- `img_002`: xe nhỏ sát mép phải là một `van`; giữ một box, bỏ truck trùng. Các ô tô trên xe chuyên chở vẫn là `car` riêng theo R-04.
- `img_008`: giữ box xe nền nhận diện được; loại box trùng/không đủ dấu hiệu trong vùng tối theo R-09.
- `img_014`: giữ hai người đi bộ rõ; bỏ box người/xe tạo theo vệt nhòe không nhận diện chắc lớp và thân xe theo R-09.
- `img_015`: giữ riêng các ô tô nhìn thấy; box xe không kéo theo phản chiếu mặt đường theo R-02/R-09.
- `img_016`: gán xe tuk-tuk bên trái là một `three_wheeler`; không giữ box `truck` trùng. Giữ riêng xe van và tuk-tuk bên phải.
- `img_037`: xe bán tải nắp cao là `truck`; box theo thân xe và nắp gắn cố định.
- `img_040`: xe màu vàng/xanh ở giữa là `three_wheeler`; taxi tiền cảnh có `occluded_level=1`, `truncated=yes` theo quyết định của 101, đã được 102 kiểm lại.

Chi tiết từng case, phương án box, sửa và kiểm lại nằm trong `submission/qc/calibration_decisions.csv`; phạm vi thay đổi ngữ nghĩa là toàn bộ 40 ảnh.

## 5. QC và lịch sử phiên bản

Giữ nguyên toàn bộ ngưỡng trong `submission/taxonomy.json → rules`. Báo tử số/mẫu số cho mọi tỷ lệ; IAA tự động chỉ tính các box ghép theo ngưỡng, nên cần reviewer kiểm bằng mắt cả box và vật bị bỏ sót. Giữ ảnh không có đối tượng trong COCO với entry ảnh và 0 annotation.

| Nội dung QC | Ngưỡng cố định |
|---|---:|
| Chiều cao box tối thiểu | `20 px` |
| Ngưỡng IoU cho box cao ≥ `50 px` | `0.85` |
| Ngưỡng IoU cho box thấp hơn `50 px` | `0.7` |
| IAA IoU trung bình | `0.85` |
| Đồng thuận lớp IAA | `95%` |
| IoU ghép cặp box | `0.5` |
| Tỷ lệ ảnh lỗi tối đa để xét Release | `2%` |

| Phiên bản | Thay đổi | Lý do / ca liên quan |
|---|---|---|
| `v0` | Sáu lớp ban đầu; thuộc tính và quy tắc ca khó còn khái quát. | V0 chưa làm rõ bus/tuk-tuk, xe chở xe, ngưỡng che khuất, vật giả và vật dưới 20 px. |
| `v1.0` | Chuẩn hóa bộ 9 lớp theo CVAT Raw; thêm định nghĩa thao tác cho `three_wheeler`, `bus`, `bicycle`; định lượng `occluded_level`; tách `truncated`; ban hành `R-01`–`R-08` cho phạm vi, box, xe/người, xe chở xe, kích thước và xử lý ca chưa chắc. | Tổng hợp các ca `img_002`, `img_003`, `img_004`, `img_006`, `img_009`, `img_018`, `img_020`, `img_021`, `img_035`, `img_037` và các bất đồng giữa guideline cá nhân. |
| `v1.1` | Bổ sung `R-09` cho nhận diện loại xe khi có nắp/chụp thùng và xử lý vật nhòe chuyển động/ảnh tối; hiệu chỉnh nhãn và thuộc tính theo quyết định 102. | `img_002`, `img_008`, `img_014`, `img_015`, `img_016`, `img_037`, `img_040`; kiểm lại toàn bộ 40 ảnh vì thay đổi ngữ nghĩa. |

Reviewer 102 chốt bản v1.1 ngày 17/11/2026. Taxonomy giữ nguyên v1.0; các nhãn cuối dùng guideline này. Mọi thay đổi ngữ nghĩa tiếp theo phải mở calibration mới, có quyết định, phạm vi và kiểm lại được ghi nhận.
