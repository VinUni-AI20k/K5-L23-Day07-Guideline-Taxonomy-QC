# Guideline gán nhãn — bản nháp cá nhân CP1 — 102

> Bản nháp để tiếp tục tự hoàn thiện sau khi xem đủ 40 ảnh. Các dòng **[TỰ QUYẾT ĐỊNH]** là chỗ cần ghi quyết định và lý do của bạn; nội dung này chưa phải guideline v1.0 của nhóm.

- Phiên bản: Bản nháp CP1 (tham chiếu guideline v0)
- Ngày hoàn thiện: [điền ngày]
- Người viết: 102
- Người duyệt: [chưa duyệt / điền sau]

## 1. Mục tiêu

Tạo nhãn bounding box 2D cho người và phương tiện trong ảnh đường phố để huấn luyện mô hình phát hiện vật thể, chẳng hạn cho camera giao thông hoặc xe tự lái. Bỏ sót vật thể hoặc gán sai lớp có thể làm mô hình học sai đối tượng cần phát hiện.

## 2. Lớp và thuộc tính

### Lớp

Các mô tả dưới đây lấy từ guideline v0 và taxonomy v0. Hãy bổ sung ví dụ, phản ví dụ sau khi tự xem ảnh; quyết định cuối cùng cho các lớp mới hoặc ca ngoài phạm vi sẽ được nhóm thảo luận ở CP2.

| Lớp | Định nghĩa trong v0 | Ví dụ (ảnh) | Phản ví dụ / dễ nhầm (ảnh) |
|---|---|---|---|
| `car` | Ô tô con; taxonomy v0 nêu cả SUV. | [TỰ BỔ SUNG] | [TỰ BỔ SUNG] |
| `truck` | Xe tải; taxonomy v0 mô tả là xe có thùng hàng riêng. | [TỰ BỔ SUNG] | [TỰ BỔ SUNG] |
| `van` | Xe thùng kín cỡ nhỏ. | [TỰ BỔ SUNG] | [TỰ BỔ SUNG] |
| `motorcycle` | Xe máy, mô tô. | [TỰ BỔ SUNG] | [TỰ BỔ SUNG] |
| `person` | Người đi bộ hoặc người ngồi trên xe. | [TỰ BỔ SUNG] | [TỰ BỔ SUNG] |
| `ignore_region` | Vùng không gán từng vật; taxonomy v0 mô tả là nơi bỏ sót từng vật không tính lỗi. Đây là vùng bỏ qua, không phải một vật thể. | [TỰ BỔ SUNG] | [TỰ BỔ SUNG] |

**Đối tượng không khớp lớp nào:** v0 chưa quy định rõ cách xử lý. **[TỰ QUYẾT ĐỊNH]** Ghi cách bạn đề xuất xử lý từng nhóm ngoài phạm vi (ví dụ: không gán, dùng `ignore_region`, hoặc đánh dấu để reviewer xem) và dẫn ảnh minh họa. Không tự thêm lớp vào taxonomy cá nhân.

### Thuộc tính

| Thuộc tính | Giá trị trong taxonomy v0 | Mô tả hiện có | Ngưỡng / quy tắc áp dụng của tôi |
|---|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | v0 mô tả lần lượt là thấy rõ, bị che ít, bị che nhiều, không rõ; các mức này chưa có ranh giới định lượng. | **[TỰ QUYẾT ĐỊNH]** Ghi ngưỡng phần trăm bị che cho từng mức; nêu cách xử lý khi không thể xác định chắc chắn. |
| `truncated` | `no`, `yes` | Cho biết vật thể có bị cắt ở mép ảnh không. | **[TỰ QUYẾT ĐỊNH]** Ghi rõ khi nào chọn `yes`, nhất là vật chạm mép nhưng chưa rõ có bị cắt. |
| `can_review` | tick / không tick | Đánh dấu box cần người review khi người gán chưa chắc. | Tick khi còn bất định; ghi tình huống cụ thể vào bảng ca khó. |

## 3. Quy tắc vẽ box

### Quy tắc nền từ v0

1. Dùng bounding box chữ nhật 2D trên vật thể được gán.
2. Theo v0, gán box cho người và phương tiện trong ảnh; box ôm sát vật thể.
3. Chọn một lớp và điền các thuộc tính của taxonomy cho từng box. Nếu chưa chắc, có thể tick `can_review`.

### Các điểm tôi cần tự chốt sau khi xem ảnh

- **Phần nhìn thấy và che khuất:** [TỰ QUYẾT ĐỊNH] Box chỉ ôm phần nhìn thấy hay ước lượng toàn bộ vật? Nêu cách áp dụng nhất quán khi vật bị che.
- **Vật bị cắt mép ảnh:** [TỰ QUYẾT ĐỊNH] Cách vẽ box trong khung ảnh và cách gán `truncated`.
- **Vật nhỏ:** taxonomy quy định `min_box_height_px = 20`; [TỰ QUYẾT ĐỊNH] ghi cách xử lý vật thấp hơn 20 px và khi nào dùng `ignore_region`.
- **Tượng, ma-nơ-canh, đồ chơi, hình in và phản chiếu:** [TỰ QUYẾT ĐỊNH] ghi vật nào thuộc phạm vi nhãn và vật nào bị loại, kèm ảnh.
- **Người đi xe máy:** [TỰ QUYẾT ĐỊNH] ghi số box, lớp và phạm vi box cho người và xe; thử áp dụng cùng quy tắc trên một ảnh khác.
- **Xe chở xe:** [TỰ QUYẾT ĐỊNH] ghi cách gán xe chở và các xe được chở.
- **Đám đông, xe đạp/xích lô và phương tiện chưa có lớp:** [TỰ QUYẾT ĐỊNH] ghi cách xử lý hoặc đánh dấu để hỏi reviewer.

## 4. Ca khó

Bảng dưới đây là các ảnh/tình huống được hướng dẫn lab gợi ý để khảo sát. Hãy xem ảnh gốc và tự điền quyết định cùng lý do; không coi câu hỏi gợi ý là đáp án. `R-xx` sẽ được nhóm chốt và đặt tên ở CP2.

| Ảnh | Tình huống cần xem | Rule ID | Quyết định ban đầu của tôi | Lý do / điều cần hỏi reviewer |
|---|---|---|---|---|
| `img_002` | Xe chở các xe khác: cần xác định box cho xe chở và xe được chở. | [để CP2 chốt] | [TỰ QUYẾT ĐỊNH] | [TỰ GHI] |
| `img_004`, `img_016`, `img_035` | Tuk-tuk / phương tiện ba bánh; xem taxonomy v0 có lớp phù hợp không. | [để CP2 chốt] | [TỰ QUYẾT ĐỊNH] | [TỰ GHI] |
| `img_009`, `img_031`, `img_037`, `img_040` | Xe buýt hoặc phương tiện cỡ lớn; xem cách phân lớp theo v0. | [để CP2 chốt] | [TỰ QUYẾT ĐỊNH] | [TỰ GHI] |
| `img_011`, `img_017`, `img_027` | Tượng; phân biệt vật thật với hình dạng giống người/phương tiện. | [để CP2 chốt] | [TỰ QUYẾT ĐỊNH] | [TỰ GHI] |
| `img_018`, `img_020`, `img_033`, `img_038` | Hình người/phương tiện trên biển, phản chiếu, ma-nơ-canh hoặc đồ chơi. | [để CP2 chốt] | [TỰ QUYẾT ĐỊNH] | [TỰ GHI] |
| `img_037` | Bán tải gắn nắp thùng cao; ranh giới giữa `van` và `truck`. | [để CP2 chốt] | [TỰ QUYẾT ĐỊNH] | [TỰ GHI] |
| [ảnh người đi xe máy] | Số box, lớp và phần được bao trong từng box; thử lại quy tắc trên ảnh thứ hai. | [để CP2 chốt] | [TỰ QUYẾT ĐỊNH] | [TỰ GHI] |

## 5. QC và phiên bản

### Ngưỡng QC cố định trong taxonomy v0

| Nội dung | Ngưỡng hiện hành |
|---|---:|
| Chiều cao box tối thiểu | `20 px` |
| Ngưỡng IoU cho box cao từ `50 px` | `0.85` |
| Ngưỡng IoU cho box thấp hơn `50 px` | `0.7` |
| IAA IoU trung bình | `0.85` |
| Đồng thuận lớp | `95%` |
| Ngưỡng lỗi theo ảnh để xét Release | `2%` |
| IoU ghép cặp box khi so sánh | `0.5` |

Không sửa các ngưỡng trong mục `rules` của `taxonomy.json`. **[TỰ BỔ SUNG]** Ghi cách bạn sẽ đánh dấu ca chưa chắc, người/ vai trò nhận câu hỏi ở CP2, và cách theo dõi thay đổi guideline sau khi nhóm thống nhất.

| Phiên bản | Thay đổi | Lý do / ca liên quan |
|---|---|---|
| v0 | Bản khởi đầu từ `guideline/guideline_v0_starter.md`; mô tả lớp và thuộc tính còn khái quát. | Cần khảo sát 40 ảnh để tìm các điểm chưa rõ. |
| Bản nháp CP1 | Ghi lại cấu trúc và các câu hỏi cần tự quyết; chưa phải bản đã khóa. | Hoàn thiện sau khi tự xem ảnh; các quy tắc chung sẽ được đối chiếu ở CP2. |
