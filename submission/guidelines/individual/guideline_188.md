# Guideline gán nhãn cá nhân — v0.1 — 03188

- **Phiên bản:** v0.1 (đề xuất cá nhân, dựa trên taxonomy v0)
- **Ngày:** 2026-11-16
- **Người viết:** thành viên 03188
- **Người duyệt:** chưa duyệt
- **Loại nhãn:** bounding box 2D trên ảnh đường phố
- **Công cụ / định dạng:** CVAT, xuất COCO 1.0

## 1. Mục tiêu và phạm vi

Gán nhãn người và các loại phương tiện được liệt kê dưới đây để huấn luyện mô hình phát hiện vật thể trên ảnh đường phố. Chỉ gán những gì có bằng chứng trực tiếp trong ảnh; không suy đoán vật bị che hoàn toàn hoặc nằm ngoài khung hình. Ưu tiên nhất quán giữa người gán: khi chưa thể xác định chắc chắn, ghi nhận bằng `can_review` thay vì tự tạo lớp hay quy tắc mới.

Mỗi vật thể mục tiêu nhìn thấy được có một box riêng, trừ trường hợp vật quá nhỏ hoặc không thể tách riêng theo quy tắc `ignore_region` ở mục 2. Không tạo nhãn cho vật ngoài taxonomy.

## 2. Lớp và thuộc tính

### 2.1. Lớp

| Lớp | Gán khi | Không nhầm với |
|---|---|---|
| `car` | Ô tô chở người, gồm sedan, hatchback, coupe và SUV. | Xe có khoang chở hàng riêng hoặc thùng hàng rõ ràng (`truck`); xe thân kín kiểu van (`van`). |
| `truck` | Xe tải có thùng/khoang chở hàng riêng, kể cả thùng hở hoặc thùng chuyên dụng. | SUV và xe chở khách (`car`); xe thân kín nhỏ kiểu van (`van`). |
| `van` | Xe thân kín, khoang lái nối với khoang chở hàng/hành khách, hình dáng van cỡ nhỏ. | Xe tải có thùng hàng tách biệt (`truck`); ô tô chở khách thông thường (`car`). |
| `motorcycle` | Xe máy, mô tô, xe tay ga hoặc xe gắn máy hai bánh có động cơ nhìn thấy được. | Xe đạp không có động cơ: ngoài taxonomy, không gán nhãn. |
| `person` | Người thật nhìn thấy được, gồm người đi bộ, người lái và hành khách. | Tượng, hình nộm, hình in trên biển/quảng cáo hoặc hình người phản chiếu: không phải người thật, không gán `person`. |
| `ignore_region` | Vùng nhỏ, khoanh sát khu vực có đối tượng thuộc phạm vi nhưng không thể gán riêng đáng tin cậy, như vật mục tiêu có chiều cao box dưới 20 px hoặc cụm quá dày không thể tách từng vật. | Không dùng thay cho lớp ngoài taxonomy, vùng nền lớn, vật bị che hoàn toàn hoặc vùng chỉ “không chắc”. |

**Quy tắc chọn lớp:** chọn theo cấu tạo và công năng thể hiện rõ trong ảnh, không dựa riêng vào màu sắc, kích thước ước đoán hay suy đoán từ bối cảnh. Nếu vẫn phân vân giữa hai lớp sau khi áp dụng định nghĩa, chọn lớp có bằng chứng tốt nhất và bật `can_review`.

**Đối tượng ngoài taxonomy:** không gán lớp mới và không dùng `ignore_region` chỉ vì đối tượng không được hỗ trợ. Ví dụ: xe buýt, xe đạp, động vật, biển báo và vật thể không phải người/xe trong danh sách thì bỏ qua. Nếu không rõ một hình dạng có phải đối tượng mục tiêu hay không, đánh dấu `can_review` khi có box mục tiêu hợp lý; nếu không thể xác định cả vùng/vật cần box, ghi vào danh sách vấn đề ảnh sau khi khóa nhãn.

### 2.2. Thuộc tính

| Thuộc tính | Giá trị | Quy tắc chọn |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Ước lượng phần diện tích hình chiếu của vật bị vật khác che. `0`: không bị che; `1`: bị che trên 0% và dưới 25%; `2`: từ 25% đến 50%, tính cả hai mốc; `3`: trên 50% nhưng vẫn nhận diện được vật và lớp. Không tính phần nằm ngoài khung ảnh là bị che. |
| `truncated` | `no`, `yes` | `yes` chỉ khi vật tiếp tục vượt ra ngoài một cạnh khung ảnh; nếu vật nằm trọn trong ảnh nhưng bị vật khác che thì chọn `no`. |
| `can_review` | `false`, `true` | Mặc định `false`. Chọn `true` khi còn nghi ngờ đáng kể về sự hiện diện, lớp, ranh giới box hoặc thuộc tính; chỉ bật cờ không thay thế cho việc chọn nhãn tốt nhất có thể. |

Nếu vật bị che quá nhiều đến mức không thể nhận diện là người/lớp xe nào, không đoán lớp. Chỉ gán khi có bằng chứng nhận diện; nếu vùng đó có thể là vật mục tiêu nhưng chưa thể kết luận, ghi vấn đề để reviewer xử lý.

## 3. Quy tắc vẽ box

1. **Một vật, một box.** Box chữ nhật song song với cạnh ảnh, ôm sát phần vật nhìn thấy. Không bao gồm bóng đổ, khoảng trống xung quanh hoặc phần bị che được suy đoán.
2. **Chỉ phần nhìn thấy.** Với vật bị che, vẽ theo các điểm ngoài cùng còn nhìn thấy của chính vật; không vẽ xuyên qua vật che. Gán `occluded_level` theo mức che ở mục 2.
3. **Vật bị cắt bởi khung ảnh.** Vẽ từ phần vật nhìn thấy đến đúng cạnh ảnh, không mở rộng box ra ngoài ảnh; đặt `truncated=yes`. Một vật chỉ bị vật khác che không phải là bị cắt mép.
4. **Người đi xe máy:** tạo một box `person` cho người và một box `motorcycle` cho xe nếu cả hai nhìn thấy và đủ điều kiện gán riêng. Không gộp người và xe vào một box; phần cơ thể đang khuất sau xe không được ước lượng để mở rộng box người.
5. **Nhiều người hoặc xe:** mỗi cá thể nhận một box riêng khi có thể phân biệt ranh giới. Không gộp nhiều cá thể vào một box mục tiêu. Chỉ dùng `ignore_region` cho cụm mục tiêu quá dày/nhỏ đến mức không thể tách đáng tin cậy.
6. **Ngưỡng vật nhỏ:** nếu chiều cao box của người hoặc xe mục tiêu nhỏ hơn 20 px, không tạo box lớp mục tiêu; khoanh vùng nhỏ tương ứng bằng `ignore_region`. Từ 20 px trở lên, gán lớp bình thường nếu có thể nhận diện. Không mở rộng box chỉ để vượt ngưỡng.
7. **Ảnh phản chiếu, tượng, hình in, đồ chơi:** không gán `person`/phương tiện cho ảnh phản chiếu, tượng, hình in hoặc vật mô hình; chúng không phải đối tượng thật cần phát hiện trong cảnh. Không tạo `ignore_region` cho các vật này.
8. **Xe chở xe hoặc vật gắn/liền kề:** gán riêng mỗi phương tiện thuộc taxonomy khi từng xe nhìn thấy và có thể phân định box. Không gán nhãn cho phần hàng hóa ngoài taxonomy. Nếu phần che khiến không xác định được số/lớp xe, gán những vật nhận diện được và bật `can_review` cho box liên quan.
9. **Vùng bỏ qua:** chỉ vẽ `ignore_region` quanh vùng mục tiêu không thể gán riêng theo quy tắc vật nhỏ/đám đông; giữ vùng nhỏ nhất bao phủ phần cần bỏ qua. Không phủ lên các đối tượng mục tiêu khác vẫn có thể gán, và không dùng vùng này để che lỗi chưa giải quyết.
10. **Ảnh không có vật mục tiêu:** không tạo annotation giả. Ảnh vẫn phải có trong file COCO theo danh sách phân công.

## 4. Ca khó và quyết định áp dụng

Các tình huống dưới đây là quy tắc xử lý, không khẳng định rằng tình huống đó xuất hiện trong một ảnh cụ thể. Khi gặp ca thực tế, ghi đúng tên ảnh (`img_0xx`), vùng, quyết định và lý do trong ghi chú cá nhân/QC.

| Tình huống | Quyết định | Lý do |
|---|---|---|
| Người đang lái hoặc ngồi trên xe máy | Hai box riêng `person` và `motorcycle` nếu cả hai nhìn thấy; vùng cơ thể khuất không được suy diễn. | Hai lớp mô tả hai đối tượng khác nhau; box cần theo phần nhìn thấy. |
| Người/xe bị che một phần | Vẽ box phần nhìn thấy; gán mức `occluded_level` theo tỷ lệ diện tích bị che. | Giữ ranh giới annotation dựa trên bằng chứng trong ảnh. |
| Người/xe bị cắt ở mép ảnh | Vẽ phần nằm trong ảnh và đặt `truncated=yes`. | Cắt khung khác với bị che bởi vật khác. |
| Vật mục tiêu rất nhỏ hoặc nhóm người quá dày | Dùng `ignore_region` cho phần không thể gán riêng; vẫn gán riêng các vật còn phân biệt được. | Tránh box thiếu tin cậy mà không bỏ qua phần có thể gán. |
| Tượng, hình người trên biển/quảng cáo, hoặc ảnh phản chiếu | Không gán `person`. | Đây không phải người thật trong cảnh. |
| Loại xe khó phân biệt giữa `car`, `truck`, `van` | Dùng cấu tạo nhìn thấy được theo bảng lớp; nếu bằng chứng chưa đủ, chọn nhãn tốt nhất và bật `can_review`. | Không phân loại chỉ theo kích thước hoặc suy đoán. |
| Đối tượng có thể thuộc lớp ngoài taxonomy | Không tạo lớp mới/`ignore_region`; ghi vấn đề nếu ảnh hưởng đến quyết định gán vật mục tiêu. | Giữ nguyên taxonomy và làm rõ ca chưa được quy định. |

Nếu chưa thể xác định box/lớp dù đã áp dụng quy tắc, bật `can_review` trên box liên quan. Nếu chưa vẽ được box hợp lý, ghi ảnh, vùng và lý do vào `image_issues.csv` sau khi khóa nhãn; không dùng `can_review` như một nhãn thay thế.

## 5. QC và phiên bản

### 5.1. Tự kiểm trước khi nộp

- Mọi người/xe thuộc taxonomy và nhìn thấy đủ điều kiện đều đã được gán; không có box cho vật ngoài phạm vi.
- Mỗi vật có đúng một box lớp mục tiêu; người và xe máy không bị gộp.
- Box ôm sát phần nhìn thấy, nằm trong ảnh; `truncated` và `occluded_level` được phân biệt đúng.
- Vật dưới 20 px và cụm không thể tách được xử lý bằng `ignore_region`, không phải box lớp mục tiêu nhỏ.
- `can_review` chỉ bật khi cần reviewer; ghi lại ca không thể gán vào danh sách vấn đề ảnh.
- Tên ảnh, lớp và thuộc tính khớp taxonomy; ảnh không có vật mục tiêu vẫn có trong COCO.

### 5.2. Ngưỡng QC của lab

Không thay đổi các ngưỡng trong `submission/taxonomy.json`. Dùng các ngưỡng hiện có để đối chiếu:

| Chỉ số | Ngưỡng |
|---|---:|
| Chiều cao tối thiểu của box lớp mục tiêu | 20 px |
| IoU box lớn (chiều cao từ 50 px) | 0.85 |
| IoU box nhỏ (chiều cao dưới 50 px) | 0.70 |
| Ngưỡng ghép cặp box khi tính IAA | IoU từ 0.50 |
| IAA yêu cầu | IoU trung bình từ 0.85; cùng lớp từ 95% |
| Tỷ lệ ảnh có lỗi tối đa để Release | 2% sau khi duyệt toàn bộ lô |

IoU là giao trên hợp diện tích của hai box. IAA được tính trên các cặp box ghép 1–1; cần xem riêng box chưa ghép, lớp, vùng `ignore_region` và lỗi bỏ sót/thừa. Chỉ số cao không chứng minh nhãn đúng nếu mọi người cùng hiểu sai một quy tắc. Ghi số liệu kèm tử số/mẫu số; thiếu lượt gán, thiếu bằng chứng hoặc mới duyệt lấy mẫu thì chưa đủ căn cứ Release.

### 5.3. Phiên bản và thay đổi

| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| v0.1 | Viết lại định nghĩa lớp, thuộc tính, box, vật nhỏ, ca ngoài taxonomy và quy trình QC. | Làm rõ những điểm chưa đủ quyết định thống nhất trong guideline khởi đầu. |

Bản này là đề xuất cá nhân, không tự ý thay taxonomy hay ngưỡng QC của lab. Nhóm cần thống nhất và khóa guideline/taxonomy v1.0 trước khi gán độc lập. Sau đó, mọi thay đổi ảnh hưởng đến lớp, vật được gán, box hoặc thuộc tính phải tăng phiên bản, ghi ca dẫn đến thay đổi và xác định phạm vi rà soát; thay đổi quy tắc có thể làm đổi nhãn thì phải kiểm lại toàn bộ phạm vi bị ảnh hưởng.
