# Guideline gán nhãn — v1.1 (dự thảo editorial chờ nhóm phê duyệt)

> **Trạng thái: CHƯA ĐƯỢC NHÓM PHÊ DUYỆT — KHÔNG DÙNG LÀM CĂN CỨ PHÁT HÀNH NHÃN CUỐI.** Đây là bản làm rõ quy trình áp dụng guideline v1.0 sau khi xem kết quả IAA. Không đổi taxonomy, định nghĩa lớp, thuộc tính, rule R-01–R-11 hoặc ngưỡng. Guideline gốc có hiệu lực vẫn là [guideline_v1.0_agreed.md](guideline_v1.0_agreed.md).

## 1. Căn cứ và phạm vi

IAA v1.0 ghi nhận 40 ảnh, 4 thành viên, 80/80 lượt gán, 295 cặp box ghép, IoU TB 0.969 và 289/295 cùng lớp (98.0%). Script phát hiện 230 ca cần xem trên 32 ảnh: 125 bỏ sót/thừa, 42 thuộc tính, 27 ignore, 24 IoU thấp, 6 sai lớp, 6 `can_review`. Đây là bất đồng cần xem, không phải lỗi đã xác nhận hoặc bằng chứng bên nào đúng. Cặp `101|102` đạt IoU TB 0.999 nhưng chỉ 38/41 cùng lớp (92.7%), thấp hơn ngưỡng lớp 95%.

`consensus_draft.json` và mọi bảng/crop tự động chỉ là công cụ định vị. Box trung bình, lớp đa số hoặc thuộc tính đa số không được coi là đúng nếu chưa đối chiếu ảnh gốc theo v1.0.

## 2. Làm rõ cách áp dụng taxonomy hiện hành

Các quy tắc dưới đây diễn giải lại quyết định đã có trong v1.0; không tạo lớp hoặc ngưỡng mới.

### 2.1. Phân biệt `car`, `truck`, `van`

- `car`: ô tô con chở người theo định nghĩa và ví dụ trong bảng lớp v1.0; gồm sedan, hatchback, SUV, crossover, wagon và taxi.
- `truck`: xe tải, đầu kéo, xe chuyên chở và pickup có cabin tách rời thùng/sàn chở phía sau.
- `van`: xe thùng kín liền khối từ cabin đến đuôi, dùng chở hàng hoặc khách theo định nghĩa taxonomy (minivan, panel van, xe cứu thương).
- Không phân loại chỉ theo màu, kích thước nhìn tương đối hoặc vật đang chở. Dùng cấu trúc xe và định nghĩa lớp. Nếu ảnh không cho phép phân biệt cabin/thùng hay thân liền khối, đánh dấu `can_review` và ghi case; không tự đổi định nghĩa.
- Xe buýt, tuk-tuk và xe đạp/xích lô đã có lớp riêng `bus`, `tuk_tuk`, `bicycle` trong taxonomy v1.0; không ép chúng vào ba lớp trên.

### 2.2. `ignore_region` và đối tượng nhỏ

- Gán từng đối tượng riêng khi nhận diện được và đủ căn cứ vẽ box. Không dùng `ignore_region` để né ca khó hoặc thay thế đối tượng nhìn rõ.
- Theo R-09 và `rules.min_box_height_px = 20`, đối tượng có chiều cao phần nhìn thấy dưới 20 px không gán box cá thể; vùng đám đông/bãi xe dày ở xa, không thể tách cá thể, được xử lý bằng `ignore_region` như v1.0 quy định.
- `ignore_region` là vùng bỏ qua theo định nghĩa hiện hành, không phải một nhãn phương tiện và không có các thuộc tính đối tượng.
- Nếu có bất đồng về vùng ignore, kiểm tra vật thật, kích thước, khả năng tách cá thể và mức độ vùng phủ theo ảnh gốc; không kết luận từ riêng sự tồn tại của box ignore.

### 2.3. `occluded_level`, `truncated`, `can_review`

- `occluded_level`: ước lượng phần đối tượng bị vật khác che theo các mức 0–3 và các mô tả/giới hạn trong mục 2.2 của v1.0. Không đánh đồng che khuất với bị cắt mép. Nếu mức che hoặc khả năng nhận diện chưa rõ, dùng `can_review` thay vì tự chuẩn hóa theo đa số.
- `truncated`: chỉ đánh dấu `yes` khi vật thể bị cắt bởi ít nhất một cạnh ảnh; vật bị vật khác che ở giữa ảnh không vì thế thành truncated. Box vẫn nằm trong biên ảnh.
- `can_review`: dùng `true` cho lớp, ranh giới box hoặc thuộc tính chưa chắc theo R-11 và hướng dẫn v1.0; giữ lại trong danh sách calibration đến khi có quyết định và kiểm lại. Không gỡ cờ chỉ để làm sạch dữ liệu.
- Các ngưỡng phần trăm và quy tắc loại trừ giữ nguyên nguyên văn theo v1.0. Nếu gặp vùng ranh giới chưa được mô tả rõ, ghi lại để nhóm thống nhất; bản dự thảo này không tự đặt ngưỡng thay thế.

### 2.4. Bounding box và các quy tắc đối tượng

- Theo R-01, vẽ một box ôm sát phần nhìn thấy, không suy đoán phần bị che và không gộp nhiều đối tượng. Box không vượt khỏi khung ảnh.
- Theo R-02/R-04/R-05/R-08, gán người và phương tiện thành các đối tượng riêng đúng lớp; áp dụng hướng dẫn riêng cho hành khách/xe hở và xe chở trên xe tại v1.0.
- Vật tượng, mô hình, hình in và phản chiếu xử lý theo R-06; không gán thành người/phương tiện thật.
- Hàng hóa cồng kềnh không làm box phương tiện phình ra ngoài phần kết cấu xe theo R-07.
- Các trường hợp biên giữa hai lớp hoặc box rất nhỏ/nhòe phải trỏ về ảnh, `case_id` và rule; không sửa lớp hoặc box chỉ dựa vào IAA.

## 3. Quy trình Calibration đề xuất (editorial)

1. Tra từng `case_id` trong `calibration_candidates.csv`; mở ảnh gốc và lớp phủ của đúng annotator. Bảng đề xuất/crop chỉ giúp định vị.
2. Phân loại câu hỏi: đối tượng có thuộc phạm vi không; lớp nào theo taxonomy; box có ôm phần nhìn thấy; thuộc tính nào theo ảnh; có bỏ sót hoặc ignore nhầm không.
3. Ghi lý do và rule v1.0 trong `calibration_decisions.csv`. Khi chưa đủ căn cứ, giữ tiền tố `CHỜ REVIEW THỦ CÔNG:` và mô tả điều còn thiếu.
4. Chỉ ghi người chốt, phiếu sửa và reviewer khi hành động tương ứng đã thực sự diễn ra. Không suy ra người đúng từ đa số hoặc từ box trung bình.
5. Người được nhóm giao sửa thực hiện trên CVAT và xuất COCO đúng phạm vi/phiên bản do `prepare_calibration.py` yêu cầu. Reviewer kiểm ảnh, quyết định và export; sau đó chạy quy trình `build_final.py` và QC theo README.
6. Nếu thay đổi ngữ nghĩa quy tắc hoặc taxonomy, tuân theo yêu cầu phạm vi toàn lô và versioning trong scripts; bản v1.1 này không đề xuất thay đổi ngữ nghĩa.

## 4. Tình trạng hiện tại

- 230/230 ca IAA còn chờ nhóm xác nhận; chưa có sửa CVAT hoặc kiểm lại được ghi nhận.
- Taxonomy v1.0 và các ngưỡng hiện hành không đổi.
- Bản v1.1 chỉ là bản làm rõ cách điều tra bất đồng; cần nhóm duyệt và điền lịch sử phiên bản sau khi thực sự thông qua.
- Cho tới khi hoàn tất quyết định, sửa/export và QC có bằng chứng, trạng thái bàn giao vẫn là **Hold**.
