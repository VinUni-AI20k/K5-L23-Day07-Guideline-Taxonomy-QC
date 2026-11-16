# Guideline gán nhãn cá nhân — bản nháp v0.1

- Người viết: Lê Văn Khởi (`2A202603290`)
- Ngày: 16/11/2026
- Định dạng: Bounding Box 2D trên CVAT, xuất COCO 1.0

## 1. Mục tiêu

Bộ nhãn này dùng để huấn luyện mô hình thị giác máy tính (Object Detection) phát hiện người và phương tiện trong môi trường giao thông đô thị.
- **Rủi ro bỏ sót (False Negative - FN):** Nếu mô hình bỏ sót người đi bộ hoặc xe đang di chuyển, hệ thống hỗ trợ lái hoặc xe tự lái có nguy cơ không nhận diện kịp chướng ngại vật, tiềm ẩn rủi ro va chạm mất an toàn giao thông.
- **Rủi ro nhận nhầm (False Positive - FP):** Nếu mô hình nhận nhầm hình in trên biển quảng cáo, hình phản chiếu qua gương, tượng hoặc ma-nơ-canh thành người/xe thật, hệ thống có khả năng đưa ra cảnh báo sai hoặc phanh khẩn cấp không cần thiết (phantom braking), tiềm ẩn nguy cơ mất an toàn cho các phương tiện đi phía sau.

Do làm việc trên ảnh tĩnh 2D, người gán không thể dựa vào chuyển động để phán đoán. Bản nháp này ưu tiên hình dáng, đặc trưng thị giác và cấu trúc vật lý nhìn thấy được. Các ca mơ hồ, có nhiều cách hiểu hợp lý hoặc nằm ở ranh giới giữa hai lớp sẽ được đánh dấu `can_review = true` kèm câu hỏi cụ thể để đưa ra thảo luận trong buổi họp Calibration; tuyệt đối không tự suy đoán.

## 2. Lớp và thuộc tính

### 2.1. Lớp (Taxonomy)

> **Lưu ý về Taxonomy:** Bảng dưới đây gồm 6 lớp chuẩn theo `submission/taxonomy.json` hiện tại (`car`, `truck`, `van`, `motorcycle`, `person`, `ignore_region`) và **4 lớp đề xuất mở rộng** (`bus`, `three_wheeler`, `bicycle`, `other_vehicle`) dựa trên quan sát sơ bộ 40 ảnh thực tế (chứa xích lô, xe tuk-tuk, xe buýt). Bốn lớp này được đưa vào để nhóm thảo luận và biểu quyết ở Pha 2; chưa dùng để gán nhãn chính thức nếu nhóm chưa thông qua.

| Lớp | Định nghĩa (một câu) | Ví dụ thực tế | Phản ví dụ / Dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con chở người dưới 9 chỗ ngồi (gồm sedan, hatchback, coupe, SUV, MPV gia đình). | Toyota Vios, Mazda CX-5, Mitsubishi Xpander. | Xe bán tải (pickup) có thùng hàng hở (cá nhân tôi xếp vào `truck`); xe thương mại 16 chỗ (xếp vào `van`). |
| `truck` | Xe tải, xe đầu kéo, xe chuyên dụng hoặc xe có sàn/thùng chở hàng riêng biệt. | Xe tải chở hàng, xe ben, xe chở xe (*car carrier*), xe bán tải (*pickup* thùng hở). | Không đổi lớp thành `car` kể cả khi xe tải đang chạy rỗng không có hàng. |
| `van` | Xe thương mại thân kín dạng hộp cỡ nhỏ đến trung (9–16 chỗ) hoặc xe tải van chở hàng liền khối. | Xe cứu thương, Ford Transit 16 chỗ, Toyota HiAce, xe bưu chính bọc kín. | Xe MPV/SUV gia đình dưới 9 chỗ (xếp `car`); xe buýt lớn trên 16 chỗ (xếp `bus`). |
| `bus` *(đề xuất)* | Xe cỡ lớn thiết kế chuyên dụng để chở khối lượng lớn hành khách (thường trên 16 chỗ). | Xe buýt nội đô, xe khách 29–45 chỗ. | Xe van 16 chỗ dạng hộp (xếp vào `van`, không xếp `bus`). |
| `three_wheeler` *(đề xuất)* | Phương tiện có cấu hình ba bánh (cơ giới hoặc sức người đạp). | Xe tuk-tuk, xích lô chở khách, xe lôi, mô tô có gắn sidecar 3 bánh. | Không gán cho xe máy hai bánh thông thường; không gán cho xe đẩy hàng 4 bánh. |
| `motorcycle` | Xe cơ giới hai bánh có tay lái (ghi-đông). | Xe số (Honda Wave), xe tay ga (Vespa, SH), mô tô phân khối lớn. | Xe đạp điện, xe trợ lực (xếp `bicycle` nếu chạy bàn đạp); người điều khiển xe máy tách thành box `person` riêng. |
| `bicycle` *(đề xuất)* | Xe hai bánh vận hành chủ yếu bằng sức đạp chân của con người. | Xe đạp thể thao, xe đạp mini, xe đạp trợ lực điện có bàn đạp. | Xe máy điện chạy hoàn toàn bằng tay ga không cần đạp (xếp vào `motorcycle`). |
| `other_vehicle` *(đề xuất)* | Xe đẩy, xe kéo có bánh không thuộc các lớp phương tiện trên. | Xe đẩy hàng bằng tay, xe kéo rác, xe ba gác tự chế không động cơ. | Gánh hàng rong không có bánh không phải xe (không gán xe). |
| `person` | Con người đang sống nhìn thấy trong ảnh (đi bộ, lái xe, hành khách). | Người đi bộ qua đường, tài xế xe máy, người ngồi trên xích lô. | Tượng người, ma-nơ-canh, hình in người trên biển quảng cáo/áo quần (không gán nhãn). |
| `ignore_region` | Vùng chứa cụm đối tượng quá nhỏ hoặc quá dày đặc không thể tách rời nhất quán. | Đám đông người ở hậu cảnh rất xa, bãi đỗ xe dày đặc ở khoảng cách xa. | Không dùng một vùng ignore lớn để bao trùm các vật thể riêng lẻ đủ kích thước gán nhãn. |

### 2.2. Thuộc tính

Ngưỡng kích thước tối thiểu theo quy định là **chiều cao ≥ 20 px**. Đối tượng nhỏ hơn 20 px không gán box riêng.

| Thuộc tính | Giá trị | Ngưỡng đo lường & Quy tắc dự kiến |
|---|---|---|
| `occluded_level` | `0` | Che khuất từ 0% đến 10% (vật thể nhìn thấy gần như trọn vẹn). |
|  | `1` | Che khuất trên 10% đến 35% (bị che một phần nhỏ nhưng nhận diện rất rõ). |
|  | `2` | Che khuất trên 35% đến 70% (bị che đáng kể nhưng cấu trúc nhận diện lớp vẫn rõ). |
|  | `3` | Che khuất trên 70% đến ngưỡng nhận diện tối đa (~85%). Nếu bị che > 85% không còn đủ đặc trưng nhận diện thì KHÔNG gán; nếu còn phân vân thì gán và bật `can_review`. |
| `truncated` | `no` | Toàn bộ vật thể nằm trọn vẹn trong khung hình ảnh (kể cả khi nằm sát mép). |
|  | `yes` | Vật thể thực tế bị cắt cụt bởi ít nhất một mép ảnh (vật tiếp tục đi ra ngoài biên ảnh). |
| `can_review` | `false` | Nhãn lớp, viền box và thuộc tính đã rõ ràng theo đúng quy tắc. |
|  | `true` | Tình huống mơ hồ, có nhiều cách hiểu, hoặc chưa có tiền lệ trong guideline; bắt buộc ghi chú lý do để thảo luận ở Pha Calibration. |

*Lưu ý kỹ thuật:*
- **Quy tắc độc lập giữa Che khuất và Cắt mép:** `truncated` chỉ xét phần vật thể bị cắt bởi mép ảnh; `occluded_level` chỉ xét phần vật thể bị che bởi các vật thể khác trong bối cảnh. Tuyệt đối không cộng dồn phần cắt mép vào độ che khuất để tránh phạt trùng lặp hai lần.
- Phần trăm che khuất được ước lượng dựa trên tổng thể hình dáng cấu trúc vật lý của vật thể đó, không tính theo tỷ lệ diện tích bounding box.
- Với lớp `ignore_region`: Không áp dụng thuộc tính `occluded_level` và `truncated` (để giá trị mặc định).

## 3. Quy tắc vẽ Bounding Box

1. **Ôm sát biên nhìn thấy (Tightness):** Box phải ôm khít biên ngoài cùng của phần vật thể thực tế nhìn thấy được. Với vật thể bị che khuất một phần, tuyệt đối không tự tưởng tượng để vẽ phần bị khuất.
2. **Loại trừ bóng đổ và chi tiết siêu mảnh:** Không kéo dài box để bao trùm bóng đổ (*Drop shadow*) của người hoặc xe in trên mặt đường. Không cố kéo box để ôm các chi tiết phụ siêu mảnh không mang đặc trưng nhận dạng (dây ăng-ten radio, cán cờ gắn trên xe).
3. **Tách biệt người và phương tiện:** Người lái và hành khách trên các phương tiện hở (xe máy, xe đạp, xích lô, tuk-tuk) phải được gán thành các box `person` riêng biệt, cho phép chồng lấn (*overlap*) với box của xe; không gộp chung người vào box xe.
4. **Người ngồi trong cabin kín:** Người ngồi bên trong cabin xe con (`car`), xe tải (`truck`), hoặc xe buýt (`bus`) kín cửa kính thì **không gán box `person`** (trừ trường hợp thò hẳn phần thân trên ra ngoài cửa sổ).
5. **Phụ kiện cố định và hàng hóa rời:** 
   - Tính các bộ phận cố định của xe (gương chiếu hậu, bánh xe dự phòng treo sau) vào box của phương tiện.
   - Hàng hóa cồng kềnh, rời rạc chở sau xe không tự động nhập vào box xe nếu làm phình to box; nếu hàng che khuất một phần xe thì tăng `occluded_level` của xe.
   - Với người gánh hàng rong, box `person` ôm cơ thể và phụ kiện gắn liền (quần áo, nón mũ, balo đeo); **không tính đòn gánh và thúng hàng** vào box người.
6. **Vật thể không thật (False objects):** Tuyệt đối không gán box cho người/xe xuất hiện trên biển quảng cáo (pano), màn hình điện tử, bóng phản chiếu qua gương/mặt kính, tượng đài, tượng trang trí, ma-nơ-canh hoặc mô hình đồ chơi.
7. **Xe chủ (Ego-vehicle):** Không gán box cho các bộ phận của xe chở camera (nắp capo, cần gạt nước, gương chiếu hậu bên trong) lọt vào góc dưới khung hình.
8. **Ngưỡng kích thước & Ignore:** Vật thể riêng lẻ có chiều cao từ 20 px trở lên mới vẽ box riêng. Cụm đối tượng dày đặc dưới 20 px hoặc ở quá xa thì dùng `ignore_region` bao quanh cả cụm.
9. **Chất lượng ảnh kém:** Trong điều kiện thiếu sáng, ảnh mờ hoặc nhiễu hạt, chỉ gán khi còn đủ đặc trưng nhận dạng lớp và ranh giới vật thể. Nếu không chắc chắn, bật `can_review = true`.

## 4. Ca khó cá nhân và câu hỏi cần chốt

| Ảnh | Tình huống quan sát sơ bộ | Quyết định cá nhân đề xuất | Trạng thái |
|---|---|---|---|
| `img_002.jpg` | Xe chở xe (*car carrier*) đang cõng các ô tô con trên sàn. | Đề xuất gán 1 box `truck` cho xe tải lớn; các ô tô con trên thùng coi là hàng hóa, không tạo box `car` riêng (tránh nhầm lẫn xe đang tham gia giao thông). | Chưa chốt; cần nhóm biểu quyết thống nhất phạm vi bài toán. |
| `img_003.jpg` | Người bán hàng rong gánh hoa quả/đồ vật trên phố. | Gán 1 box `person` ôm người (không ôm đòn gánh và thúng hàng). Đồ gánh không có bánh nên không gán phương tiện. | Quy tắc cá nhân dự kiến. |
| `img_004.jpg` | Hai xe tuk-tuk đỗ cạnh nhau trên vỉa hè ban đêm. | Đề xuất xếp vào lớp `three_wheeler`; tách riêng từng xe nếu nhìn rõ ranh giới; nếu che nhau thì đánh `occluded_level`. | Chờ nhóm duyệt lớp `three_wheeler`. |
| `img_011.jpg` | Nhân vật hóa trang (Predator) bên cạnh dàn xe máy độ. | Nếu là người thật mặc trang phục hóa trang thì gán `person`; nếu là tượng mô hình tĩnh thì không gán. | Quy tắc cá nhân dự kiến (nếu không phân biệt được thì bật `can_review`). |
| `img_017.jpg`, `img_027.jpg` | Tượng người cưỡi ngựa / Bia tưởng niệm hình xe bán tải. | Không gán box người hoặc phương tiện vì đây là công trình kiến trúc/tượng nghệ thuật, không phải đối tượng thật. | Quy tắc cá nhân dự kiến. |
| `img_018.jpg` | Biển quảng cáo (billboard/pano) bầu cử có in hình người. | Không gán box `person` cho hình in 2D trên biển hiệu. | Quy tắc cá nhân dự kiến. |
| `img_020.jpg` | Cầu vồng và ngoại cảnh phản chiếu trong gương chiếu hậu ô tô. | Không tạo box cho vật thể chỉ xuất hiện qua bóng gương phản chiếu; không suy đoán thân xe ngoài khung hình. | Quy tắc cá nhân dự kiến. |
| `img_022.jpg` | Xe mô tô 3 bánh có thùng phụ bên cạnh (*motorcycle with sidecar*). | Đề xuất xếp vào `three_wheeler` (xe 3 bánh); gán box `person` riêng cho người ngồi trên xe. | Chờ nhóm duyệt lớp `three_wheeler`. |
| `img_028.jpg` | Xe bán tải chở tượng lớn trên thùng (*yorse* theo metadata). | Đề xuất gán box `truck` cho xe bán tải; tượng động vật trên thùng không thuộc taxonomy người/phương tiện nên không gán. | Đề xuất sơ bộ từ metadata; cần xác minh trực tiếp trên ảnh gốc trước khi chốt. |
| `img_029.jpg` | Xe máy chở khối hàng cồng kềnh quá khổ (*dangerous load*). | Box `motorcycle` chỉ ôm thân xe, không bao trọn khối hàng cồng kềnh; người lái bị che khuất thì đánh giá `occluded_level`. | Đề xuất sơ bộ từ metadata; cần xác minh trực tiếp trên ảnh gốc trước khi chốt. |
| `img_033.jpg`, `img_038.jpg` | Ma-nơ-canh trong tủ kính / Tủ trưng bày mô hình đồ chơi trẻ em. | Ma-nơ-canh và đồ chơi, mô hình tĩnh không phải người và xe thật -> Không gán nhãn. | Quy tắc cá nhân dự kiến. |
| `img_035.jpg` | Xe lam/tuk-tuk chở khách quá tải (*overloaded rickshaw*). | Gán `three_wheeler` cho xe; gán `person` cho các hành khách nhìn rõ phần thân; cụm người bên trong bị che lấp quá sâu thì bật `can_review`. | Đề xuất sơ bộ từ metadata; cần xác minh trực tiếp trên ảnh gốc trước khi chốt. |

## 5. QC và phiên bản

- **Quy trình tự kiểm (Self-check):** Mỗi ảnh được rà soát tối thiểu hai lượt độc lập: Lượt 1 kiểm tra độ bao phủ (không bỏ sót đối tượng, chọn đúng lớp); Lượt 2 kiểm tra độ khít của bounding box, các giá trị thuộc tính (`occluded_level`, `truncated`) và cờ `can_review`.
- **Giới hạn của công cụ tự động:** Script `validate_labels.py` chỉ kiểm tra được tính hợp lệ về mặt cú pháp (schema, tọa độ trong khung ảnh, thuộc tính hợp lệ); không thể thay thế con người kiểm tra độ ôm khít của box hay phát hiện vật thể bị bỏ sót. Do đó, việc đối chiếu trực quan (*Visual Inspection*) là bắt buộc.
- **Xử lý bất đồng (Disagreement):** Ghi nhận khách quan mọi trường hợp lệch nhãn giữa các thành viên, phân tích nguyên nhân gốc rễ (*Root cause analysis*) tại buổi họp Calibration. Tuyệt đối không chỉnh sửa số liệu IAA thủ công.
- **Chỉ số mục tiêu:** Mean IoU ≥ 0.85 (vật thể lớn) và độ đồng thuận lớp ≥ 95% là mốc tham chiếu chất lượng, kết quả thực tế sẽ được báo cáo trung thực sau pilot.

| Phiên bản | Thay đổi chính | Trạng thái |
|---|---|---|
| v0.1 | Bản nháp cá nhân: Đề xuất mở rộng taxonomy (thêm 4 lớp), chuẩn hóa ngưỡng thuộc tính, bổ sung quy tắc Bounding Box và danh sách ca khó ban đầu. | Chờ thảo luận và thống nhất tại cuộc họp nhóm Pha 2 (để ra v1.0). |
