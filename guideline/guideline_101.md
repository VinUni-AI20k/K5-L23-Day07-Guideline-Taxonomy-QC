# Guideline gán nhãn 2D — bộ ảnh Day 07 

> **Trạng thái:** Dự thảo cá nhân để thảo luận

- Phiên bản: `v0.1-draft`
- Phạm vi: `data/images/img_001.jpg` đến `img_040.jpg`
- Công cụ / định dạng: CVAT Rectangle, COCO 1.0
- Mục tiêu: tạo bounding box 2D nhất quán cho người và phương tiện nhìn thấy trong ảnh.

## 1. Nguyên tắc chung

1. Chỉ gán nhãn dựa trên thông tin quan sát được trong ảnh. Không suy diễn phần bị che, danh tính
   hay đặc điểm không nhìn thấy.
2. Mỗi đối tượng thật, nhận dạng được và đạt ngưỡng kích thước có một box riêng. Box có thể
   chồng lấn khi các vật thật chồng lấn trên ảnh.
3. Box bao phần nhìn thấy của đối tượng; không kéo box qua vật che để ước đoán phần khuất.
4. Áp dụng cùng quy tắc cho ảnh màu, ảnh đen trắng, ảnh mờ, ảnh trong nhà và ảnh đông người.
   Bối cảnh hoặc màu sắc không tự quyết định lớp.
5. Mọi ảnh được phân công phải có trong COCO, kể cả ảnh không có đối tượng thuộc phạm vi.
   Ảnh không có annotation là kết quả hợp lệ nếu đã được kiểm tra.
6. Không tự tạo lớp ngoài taxonomy đã được nhóm duyệt. Nếu gặp vật có vẻ thuộc phạm vi nhưng
   chưa có lớp phù hợp, đánh dấu `can_review` nếu có thể tạo annotation và ghi lại vấn đề.

## 2. Danh mục lớp đề xuất

Các lớp đánh dấu **(thêm)** chưa có trong `submission/taxonomy.json`. Cần được nhóm duyệt và
thêm vào taxonomy/CVAT trước khi dùng. Không tự ý đổi taxonomy sau khi đã khóa lượt gán.

| Lớp | Định nghĩa thao tác | Không dùng lớp này cho |
|---|---|---|
| `car` | Ô tô con, hatchback, sedan, wagon, SUV và pickup hạng nhẹ. Pickup vẫn là `car` dù có nắp thùng hoặc chở đồ. | Xe tải chở hàng, xe buýt, xe máy, tuk-tuk hoặc mô hình thu nhỏ. |
| `truck` | Xe tải chở hàng, xe tải sàn phẳng và xe đầu kéo có cấu trúc xe tải rõ ràng. Xe thật được chở trên xe tải được gán box riêng nếu nhận dạng được và đủ kích thước. | Pickup hạng nhẹ, van nhỏ kín, xe buýt hoặc mô hình. |
| `van` | Xe van/xe giao hàng nhỏ với khoang hàng kín, hình dáng van rõ ràng. | Pickup, xe buýt hoặc xe tải chở hàng nặng. |
| `bus` **(thêm)** | Xe buýt chở nhiều hành khách, gồm xe buýt đô thị và xe khách. | Xe tải có cabin và thùng hàng, hoặc van. |
| `motorcycle` | Phương tiện hai bánh có động cơ: xe máy, mô tô, scooter có khung/ghế xe máy. | Xe đạp không động cơ, tuk-tuk hoặc xe ba bánh có động cơ. |
| `three_wheeler` **(thêm)** | Phương tiện đường bộ ba bánh có động cơ, gồm tuk-tuk/auto-rickshaw và xe ba bánh chở hàng. | Xe máy hai bánh, xe đạp ba bánh không động cơ hoặc mô hình. |
| `bicycle` **(thêm)** | Xe đạp không động cơ, xe đạp chở hàng và xích lô/cycle-rickshaw đạp bằng sức người. | Xe máy có động cơ hoặc xe đẩy không có cấu tạo xe đạp. |
| `person` | Người thật nhìn thấy đủ để nhận dạng, gồm người đi bộ và người đang lái/ngồi trên phương tiện. Mỗi người có box riêng. | Tượng, mannequin, hình người in trên biển/poster, ảnh hoặc phản chiếu. |
| `ignore_region` | Vùng chứa đối tượng thuộc phạm vi nhưng không thể tách/gán nhãn tin cậy, thường do quá nhỏ hoặc quá đông. Đây không phải lớp đối tượng. | Vùng có đối tượng rõ ràng, đủ kích thước để gán riêng. |

### Quy tắc chọn lớp cho trường hợp biên

- Phân loại phương tiện theo cấu tạo nhìn thấy, không theo nhãn hiệu, màu sơn hay nơi xuất hiện.
- Tuk-tuk/xe ba bánh có động cơ dùng `three_wheeler`, không ép vào `motorcycle`.
- Xe đạp và xích lô đạp dùng `bicycle`; người trên xe dùng `person` riêng.
- Pickup dùng `car`; xe tải chở hàng dùng `truck`; xe buýt dùng `bus`.
- Nếu không phân biệt được hai lớp dựa trên bằng chứng trong ảnh, không đoán: đánh dấu
  `can_review` và ghi ca cần xem xét.

**CẦN CHỐT:** Nhóm phải quyết định có thêm `bus`, `three_wheeler`, `bicycle` vào taxonomy hay
không. Nếu không thêm, hãy thống nhất một quy tắc ánh xạ thay thế duy nhất trước khi gán.

### Danh mục mã quy tắc

| Mã | Quy tắc |
|---|---|
| `R-01` | Chỉ gán đối tượng thật, nhìn thấy và nhận dạng được; loại tượng, hình in, phản chiếu và mô hình. |
| `R-02` | Chọn lớp theo định nghĩa đã duyệt trong taxonomy; không tự tạo lớp hoặc đoán ca chưa rõ. |
| `R-03` | Tách box người, phương tiện và từng phương tiện được chở; không gộp các đối tượng độc lập. |
| `R-04` | Box ôm phần nhìn thấy; không ước đoán phần khuất; `truncated` chỉ áp dụng cho mép ảnh. |
| `R-05` | Ngưỡng chiều cao 20 px và cách dùng `ignore_region`. |
| `R-06` | Gán `occluded_level`, `truncated` và `can_review` theo bảng thuộc tính. |
| `R-07` | Ghi nhận bất định, ca cần reviewer và vấn đề cấp ảnh; không tự ý phân xử. |
| `R-08` | Giữ ngưỡng QC, phiên bản và dấu vết calibration theo quy trình lab. |

## 3. Quy tắc vẽ box

### 3.1 Phương tiện

- Vẽ Rectangle sát đường viền nhìn thấy của thân phương tiện.
- Bao gồm bộ phận gắn liền, có ý nghĩa nhận dạng; bỏ qua chi tiết nhỏ như anten hoặc móc kéo nhỏ.
- Không gộp hàng hóa rời, người, phương tiện khác hay bóng đổ vào box của xe.
- Xe tải chở ô tô: một box cho xe tải và một box cho từng ô tô thật nhìn thấy, đủ kích thước.
  Box được phép chồng lấn nếu cần.
- Tuk-tuk chở hàng: box ôm phương tiện, không bao cả khối hàng rời trên xe.
- Taxonomy hiện không có lớp rơ-moóc. Gán phần xe có động cơ; ghi chú rơ-moóc nếu việc không
  gán riêng có thể ảnh hưởng đến quyết định. **CẦN CHỐT** nếu gặp trường hợp thực tế.

### 3.2 Người

- Mỗi người có một box riêng, chỉ bao phần cơ thể nhìn thấy.
- Người lái/ngồi trên xe máy hoặc xe đạp không gộp vào box xe. Nhiều người trên cùng xe vẫn
  tách riêng nếu có thể nhận dạng từng người.
- Không gộp túi nhỏ hoặc vật đang cầm vào box người. Vật lớn đang đẩy/kéo không thuộc box người.
- Chỉ gán người trong cabin khi hình người nhìn thấy đủ rõ để nhận dạng; không suy đoán từ bóng
  hoặc hình mờ không xác định được.

### 3.3 Che khuất, cắt mép và ảnh mờ

- **Bị che:** box chỉ bao phần nhìn thấy; không ước lượng phần nằm sau vật che.
- **Bị cắt bởi mép ảnh:** box chỉ bao phần trong khung; đặt `truncated=yes` khi vật có dấu hiệu
  tiếp tục ra ngoài ảnh. Bị che bởi vật khác không đồng nghĩa với truncated.
- **Chuyển động/nhòe:** vẫn gán nếu nhận dạng được lớp và ranh giới phần nhìn thấy. Nếu không
  chắc lớp hoặc box, dùng `can_review=true`; nếu không thể tạo annotation, ghi vào
  `image_issues.csv`.

## 4. Ngưỡng kích thước và vùng bỏ qua

- Chỉ tạo box đối tượng nếu chiều cao box trên ảnh gốc **từ 20 px trở lên**.
- Đối tượng thuộc phạm vi nhưng thấp hơn 20 px không được gán box đối tượng; dùng
  `ignore_region` phù hợp để đánh dấu vùng bỏ qua.
- Trong đám đông, gán riêng từng người/phương tiện nhận dạng được và đạt ngưỡng. Dùng
  `ignore_region` cho phần còn lại không thể tách; không để vùng ignore phủ các đối tượng đã
  gán rõ ràng.
- Không dùng `ignore_region` để né quyết định về lớp hoặc box của một vật nhìn thấy rõ.

## 5. Thuộc tính

| Thuộc tính | Giá trị | Quy tắc |
|---|---|---|
| `occluded_level` | `0` | Không bị đối tượng khác che. |
| `occluded_level` | `1` | Ước tính 1–30% hình dạng vật bị che; phần còn lại đủ nhận dạng. |
| `occluded_level` | `2` | Ước tính 31–70% bị che; vẫn nhận dạng chắc chắn được lớp. |
| `occluded_level` | `3` | Ước tính trên 70% bị che nhưng phần nhìn thấy vẫn đủ nhận dạng. |
| `truncated` | `no` | Không có dấu hiệu vật tiếp tục vượt ra ngoài khung ảnh. |
| `truncated` | `yes` | Vật bị khung ảnh cắt mất một phần. |
| `can_review` | `false` | Người gán tự tin về lớp, box và quy tắc áp dụng. |
| `can_review` | `true` | Có nhiều cách hiểu hợp lý hoặc ảnh không đủ rõ để quyết định chắc chắn. Ghi lý do/ID ảnh trong nhật ký QC. |

Phần trăm che khuất chỉ để chọn mức thuộc tính, không dùng để mở rộng box ra phần không nhìn
thấy. Nếu mức che không thể ước lượng nhất quán, đánh dấu `can_review=true`.

## 6. Đối tượng không gán nhãn

Không gán nhãn cho:

- Tượng, tượng sáp, mannequin và đồ chơi/mô hình thu nhỏ.
- Người hoặc phương tiện in trên poster/biển quảng cáo/màn hình; ảnh hoặc phản chiếu trong gương,
  kính.
- Vật trang trí/phi thực tế nếu rõ ràng không phải phương tiện đường bộ thật.
- Đối tượng không nhận dạng được; đối tượng dưới ngưỡng; phần đám đông đã đánh dấu
  `ignore_region`.

Xe thật kích thước thật trong showroom/trưng bày vẫn được gán nhãn nếu thuộc lớp và nhận dạng
được. Không nhầm xe thật với xe mô hình.

## 7. Danh sách rà soát đủ 40 ảnh

Đây là checklist khảo sát dựa trên nội dung ảnh nhìn ở kích thước thu nhỏ, không phải nhãn tham
chiếu đã xác nhận. Trước khi gán, mở ảnh gốc để quyết định từng đối tượng; không coi mô tả dưới
đây là xác nhận lớp hoặc số lượng box.

| Ảnh | Tình huống cần kiểm tra trên ảnh gốc | Rule |
|---|---|---|
| `img_001.jpg` | Người đi bộ, xe và hàng hóa trên xe; tách từng vật. | `R-01`, `R-03` |
| `img_002.jpg` | Xe tải chở ô tô: box xe chở và box riêng cho từng ô tô thật đủ điều kiện. | `R-02`, `R-03` |
| `img_003.jpg` | Người, xe đạp/phương tiện chở đồ; không gộp người và xe. | `R-02`, `R-03` |
| `img_004.jpg` | Tuk-tuk/xe ba bánh và người xung quanh; xác nhận lớp. | `R-02`, `R-03` |
| `img_005.jpg` | Người ngồi trên xe máy cạnh ô tô; tách box. | `R-03`, `R-06` |
| `img_006.jpg` | Giao thông đông, người đi xe máy và xe đạp; áp dụng ngưỡng. | `R-02`, `R-03`, `R-05` |
| `img_007.jpg` | Xe trong khu vực gara; bối cảnh trong nhà không loại xe thật. | `R-01`, `R-02` |
| `img_008.jpg` | Nhiều xe máy và người; mỗi đối tượng tách riêng nếu đủ rõ. | `R-03`, `R-05` |
| `img_009.jpg` | Xe buýt trên đường; xác nhận lớp `bus` trong taxonomy. | `R-02` |
| `img_010.jpg` | Chợ đông người và xe; xử lý phần không thể tách bằng ignore. | `R-03`, `R-05` |
| `img_011.jpg` | Tượng/điêu khắc trong cảnh đường phố; không gán như vật thật. | `R-01` |
| `img_012.jpg` | Xe và hàng cồng kềnh; box xe không bao hàng hóa rời. | `R-02`, `R-03` |
| `img_013.jpg` | Cảnh phố ban đêm; chỉ gán vật nhận dạng được. | `R-01`, `R-07` |
| `img_014.jpg` | Người/phương tiện bị nhòe chuyển động; đánh dấu nếu không chắc. | `R-06`, `R-07` |
| `img_015.jpg` | Ô tô trong cảnh phản sáng; phân biệt xe thật với ảnh phản chiếu. | `R-01`, `R-07` |
| `img_016.jpg` | Tuk-tuk, ô tô và người; xác nhận lớp xe ba bánh. | `R-02`, `R-03` |
| `img_017.jpg` | Tượng người/nhân vật; không gán thành `person`. | `R-01` |
| `img_018.jpg` | Hình người/phương tiện trên biển quảng cáo; không gán nội dung in. | `R-01` |
| `img_019.jpg` | Xe kiểu dáng lạ trong sự kiện: xác minh xe thật hay đạo cụ. **CẦN CHỐT** nếu không rõ. | `R-01`, `R-07` |
| `img_020.jpg` | Phương tiện/phong cảnh phản chiếu trong gương; không gán phản chiếu. | `R-01` |
| `img_021.jpg` | Đám đông và giao thông dày; gán vật tách được, ignore phần còn lại. | `R-03`, `R-05` |
| `img_022.jpg` | Ảnh đen trắng, vật ở xa; không suy đoán vật không nhận dạng được. | `R-01`, `R-05` |
| `img_023.jpg` | Xe đạp/xích lô, người và ô tô; xác nhận lớp và tách box. | `R-02`, `R-03` |
| `img_024.jpg` | Ô tô trưng bày/xe chở trên nóc; phân biệt xe thật và mô hình. | `R-01`, `R-03` |
| `img_025.jpg` | Người đi bộ và phương tiện ở xa; áp dụng ngưỡng 20 px. | `R-03`, `R-05` |
| `img_026.jpg` | Người đang đi xe máy; người và xe là hai đối tượng riêng. | `R-03` |
| `img_027.jpg` | Tượng xe/pickup trong công viên; không gán như phương tiện thật. | `R-01` |
| `img_028.jpg` | Xe cổ cùng vật thể trang trí/tượng trên xe; tách vật nếu là vật thật. | `R-01`, `R-03`, `R-07` |
| `img_029.jpg` | Xe đạp/xích lô và phương tiện khác; xác nhận lớp xe đạp. | `R-02`, `R-03` |
| `img_030.jpg` | Nhiều xe máy đỗ sát nhau; box riêng khi ranh giới nhận dạng được. | `R-03`, `R-05` |
| `img_031.jpg` | Phố ban đêm với phương tiện; nhận dạng lớp từ bằng chứng nhìn thấy. | `R-02`, `R-07` |
| `img_032.jpg` | Trạm/đường đông người và xe buýt; xử lý đám đông theo ngưỡng. | `R-02`, `R-05` |
| `img_033.jpg` | Mannequin trong cửa hàng; không gán thành `person`. | `R-01` |
| `img_034.jpg` | Người qua đường và phương tiện; tách box, kiểm tra cắt mép. | `R-03`, `R-06` |
| `img_035.jpg` | Tuk-tuk/xe ba bánh chở hàng; box xe không bao hàng rời. | `R-02`, `R-03` |
| `img_036.jpg` | Xe van giao hàng; phân biệt `van` với `truck` theo cấu tạo. | `R-02` |
| `img_037.jpg` | Xe buýt/van/pickup; áp dụng định nghĩa lớp đã chốt, không suy đoán theo nắp thùng. | `R-02`, `R-07` |
| `img_038.jpg` | Xe mô hình trong cửa hàng; không gán thành ô tô thật. | `R-01` |
| `img_039.jpg` | Phố đông với xe đạp, xe máy và người; tách đối tượng, dùng ignore khi cần. | `R-02`, `R-03`, `R-05` |
| `img_040.jpg` | Xe buýt, xe máy/người và ô tô; kiểm tra từng lớp và box riêng. | `R-02`, `R-03` |

## 8. QC và phiên bản

- Giữ nguyên các ngưỡng bắt buộc trong taxonomy/schema: chiều cao box tối thiểu 20 px; IoU box
  lớn 0.85, box nhỏ 0.70; IAA IoU 0.85; đồng thuận lớp 0.95; tỷ lệ lỗi ảnh tối đa 0.02;
  ngưỡng ghép IoU 0.5.
- Dùng Rule ID trong ghi chú quyết định/QC để nối ca bất đồng với quy tắc tương ứng.
- IAA đo mức đồng thuận, không chứng minh nhãn đúng. Cần xem ảnh gốc và cân nhắc khả năng cả
  nhóm cùng bỏ sót hoặc cùng áp dụng sai quy tắc.
- Mỗi bất đồng cần có ảnh, đối tượng/vùng, Rule ID, quyết định, người chốt và kết quả kiểm lại
  trong artifact QC tương ứng.
- Nếu thay đổi cách chọn vật, lớp, box hoặc thuộc tính, tăng phiên bản guideline và đánh giá
  lại phạm vi ảnh theo quy trình calibration. Không chỉnh nhãn độc lập đã khóa để làm chúng
  trông đồng thuận hơn.
- Người gán đánh dấu `can_review`; nhóm/reviewer chốt theo quy trình calibration. Giữ các phiếu
  và vòng QC cũ để truy vết.

| Phiên bản | Thay đổi | Trạng thái |
|---|---|---|
| `v0.1-draft` | Đề xuất quy tắc thao tác và danh sách ca biên cho 40 ảnh. Cần nhóm xác nhận các lớp mới và ca `img_019.jpg`. | Dự thảo; chưa dùng cho lượt gán độc lập. |

## Tham khảo

- Waymo Open Dataset, *Labeling Specifications*, mục 2D: tham khảo nguyên tắc box theo phần
  nhìn thấy, không suy diễn phần bị che và chỉ gán đối tượng nhận dạng được. Guideline này được
  viết riêng cho bộ ảnh Day 07 và taxonomy của lab, không sao chép taxonomy Waymo:
  https://github.com/waymo-research/waymo-open-dataset/blob/master/docs/labeling_specifications.md
- Quy trình/ngưỡng của lab: `GUIDE.md`, `RULES.md`, `docs/QC_CHEATSHEET.md`,
  `schemas/taxonomy.schema.json`.
