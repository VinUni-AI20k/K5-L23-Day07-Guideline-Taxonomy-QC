# CP2 — Bảng đối chiếu đề xuất từ 5 guideline cá nhân

> Bảng làm việc để phục vụ buổi chốt CP2. Đây là tổng hợp văn bản, **không phải biên bản xác nhận nhóm đã họp**. Các thành viên cần đối chiếu các ID với ảnh gốc trước khi khóa v1.0.

## Các điểm bất đồng và phương án đưa ra CP2

| Chủ đề / ảnh | Ý kiến trong các bản cá nhân | Phương án dự thảo cho v1.0 | Căn cứ / việc cần nhóm kiểm tra |
|---|---|---|---|
| `occluded_level` | 101 đề xuất các mốc 25%/50%. 103, 104, 105 dùng mốc 30%/70%. 102 hiện theo mốc 30%/70%. | `0` = 0%; `1` = >0–30%; `2` = >30–70%; `3` = >70% nếu vẫn nhận diện được lớp. | Khớp ví dụ ngưỡng trong phần hướng dẫn CP1; không có ngưỡng thuộc tính này trong `taxonomy.json → rules`. Xác nhận nhóm muốn dùng mốc này. |
| Người đi xe máy (`img_005`, `img_026` theo các bản cá nhân) | Các bản có quyết định chi tiết đều đề xuất box riêng cho từng `person` và một box cho phương tiện; có thể chồng box. | Tách người và xe thành các instance riêng; không gộp người với xe. | Cần từng người tự kiểm ảnh và xác nhận người nào đủ nhìn thấy để gán. Không chốt số box cụ thể từ mô tả văn bản. |
| Xe chở xe (`img_002`) | Các bản có nội dung đều đề xuất một box cho `truck` và box riêng cho từng ô tô con thực sự được chở. | Một `truck` cho xe chuyên chở; từng `car` riêng nếu nhận diện được và chiều cao box đạt ngưỡng 20 px. | Kiểm trực tiếp từng xe con trên ảnh gốc; ảnh không được tính box cho mô hình/vỏ xe trưng bày. |
| Tuk-tuk (`img_004`, `img_016`, `img_035`, `img_040`) | 101 đề xuất tên `three_wheeler`; 103, 104, 105 đề xuất `tuk_tuk`; 102 cũng theo `tuk_tuk`. | Dùng tên lớp `tuk_tuk` cho xe ba bánh có động cơ và khoang khách/hàng tích hợp kiểu tuk-tuk/auto-rickshaw. | Phần CP2 của HTML chỉ định bộ nhãn 8 lớp có `tuk_tuk`, không có `three_wheeler`. Xác nhận ranh giới với mô tô sidecar và xích lô đạp. |
| Bus (`img_009`, `img_031`, `img_037`, `img_040`) | 101, 103, 104, 105 đề nghị có lớp `bus`; 102 đề xuất cùng hướng. | Thêm `bus`, tách xe buýt thân lớn khỏi `van` và `truck`. | Dùng dấu hiệu thiết kế/khoang hành khách nhìn thấy; nhóm rà ca minibus/van trước khi khóa. |
| `truck` hay `van` (`img_037`) | 103, 104, 105 đề xuất bán tải có thùng/nắp cao vẫn là `truck`; 101 cũng định nghĩa `truck` theo khoang hàng riêng. | Xếp bán tải vào `truck`, kể cả có nắp thùng cố định; `van` là khoang kín liền thân với cabin. | Xác nhận dấu hiệu cabin–thùng trên ảnh. Không dùng riêng màu sắc hoặc chiều cao xe để phân lớp. |
| Vật ngoài phạm vi | 101 đề xuất thêm `bicycle` và `three_wheeler`; 103, 104, 105 để xe đạp/xích lô không động cơ ngoài taxonomy, nhưng vẫn gán người thật trên đó. | Bộ lớp v1.0 không thêm `bicycle`/`three_wheeler`; không gán phương tiện không động cơ. Gán `person` riêng nếu đủ điều kiện. Không dùng `ignore_region` cho vật ngoài phạm vi. | HTML CP2 liệt kê chính xác 8 lớp dự kiến, không gồm xe đạp. Xác nhận nhóm giữ phạm vi này. |
| Tượng, ma-nơ-canh, đồ chơi, hình in, phản chiếu | Các bản 101, 103, 104, 105 thống nhất loại khỏi lớp người/phương tiện; 102 theo đề xuất đó. | Không gán các vật biểu diễn/ảnh phản chiếu như người hoặc phương tiện thật. Vẫn gán đối tượng thật khác trong cùng ảnh. | Đối chiếu ảnh được nêu trong các bản (`img_011`, `017`, `018`, `020`, `027`, `033`, `038`). |
| Vật nhỏ / vùng dày (`img_021`, `img_032` theo bản cá nhân) | Các bản đề xuất ngưỡng 20 px; vật thuộc lớp mục tiêu quá nhỏ hoặc cụm không thể tách dùng `ignore_region`. | Gán riêng đối tượng cao ≥20 px nếu nhận diện/tách được. Dưới 20 px hoặc phần cụm không thể tách: vẽ `ignore_region` sát phần đó. | Chỉ dùng `ignore_region` cho đối tượng mục tiêu khó gán; vẫn gán riêng các vật rõ. Kiểm kích thước trên ảnh gốc. |
| `truncated` | 101, 103, 104 định nghĩa là có phần vật bị mép ảnh cắt; 105 thêm ngưỡng cắt ≥5%. | `yes` khi mép ảnh thực sự cắt mất một phần đối tượng; `no` nếu chỉ chạm mép. Không đặt thêm mốc 5%. | Ngưỡng 5% không có trong taxonomy hay quy tắc lab; giữ thuộc tính nhị phân và tách riêng khỏi che khuất. |
| QC mở rộng trong guideline 105 | 105 thêm Cohen/Fleiss Kappa, ngưỡng đào tạo, tỷ lệ throughput và quy trình review riêng. | Không đưa các chỉ số đó vào rubric v1.0; dùng đúng ngưỡng và script hiện có của repo. | `RULES.md` yêu cầu giữ nguyên `rules`; CP2 chỉ cần schema và Project CVAT đồng bộ. |

## Tình trạng đầu vào cần xử lý

- `guideline_102.md` là bản nháp có AI hỗ trợ soạn; các ví dụ/đề xuất trong đó cần mã 102 tự kiểm ảnh trước khi coi là ý kiến cá nhân đã xác nhận.
- `guideline_103.md` và `guideline_104.md` cùng đề xuất nhiều quy tắc, nhưng là hai file khác nhau; dùng từng file như một ý kiến riêng và xác nhận đúng người viết trước khi ghi biên bản nhóm.
- `guideline_105.md` có nội dung QC ngoài quy định hiện có; không chép các ngưỡng/phương pháp mới vào `taxonomy.json`.
- Các mô tả ảnh trong bảng lấy từ tài liệu và guideline, chưa được AI xác minh bằng cách nhìn ảnh. Nhóm cần tự kiểm ảnh gốc ở các hàng trên.

## Trạng thái chốt

Các phương án trong cột thứ ba đã được dùng để soạn `guideline_v1.0_agreed.md` và `taxonomy.json` cho bước rà soát. Hãy coi CP2 hoàn tất và khóa cho CP3 sau khi cả nhóm xác nhận các điểm trên, đặc biệt mốc che khuất, lớp `tuk_tuk`, phạm vi xe đạp, và phân lớp `img_037`.
