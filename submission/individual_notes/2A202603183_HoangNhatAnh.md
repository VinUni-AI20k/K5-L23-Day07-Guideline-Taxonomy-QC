# Ghi chú cá nhân — 2A202603183 - Hoàng Nhật Anh

- Nhóm: **T005**.
- Ngày lập: **16/11/2026**.
- Trạng thái: ghi chú dự thảo; các phần chưa thực hiện được ghi rõ để bổ sung theo tiến độ thực tế.
- Theo [mẫu ghi chú cá nhân](../../docs/INDIVIDUAL_NOTE_TEMPLATE.md). Quy tắc chi tiết và bảng 40 ảnh nằm trong [guideline cá nhân](../guidelines/individual/guideline_2A202603183_HoangNhatAnh.md).

## 1. Pha 1: ba ca khó tôi tìm ra trong 40 ảnh

Ba ca dưới được trích từ guideline dự thảo có hỗ trợ AI, cần Hoàng Nhật Anh tự xem ảnh và xác nhận trước khi ghi nhận là quyết định cá nhân.

| Ảnh | v0 không trả lời được gì | Quyết định ban đầu trong dự thảo |
|---|---|---|
| [img_004](../../data/images/img_004.jpg) | Tuk-tuk thuộc lớp nào; người ngồi trong xe có box riêng không? | Đề xuất thêm `tuk_tuk`; mỗi xe một box, người thật nhìn thấy và đủ ngưỡng kích thước có box riêng. |
| [img_024](../../data/images/img_024.jpg) | Vật dạng ô tô màu vàng trên nóc wagon là xe thật được chở hay mô hình/vỏ trưng bày? | Gán wagon thật là `car`; đề xuất loại vật vàng, cần tự kiểm và đưa ra họp xác nhận. |
| [img_027](../../data/images/img_027.jpg) | Tượng pickup rất giống xe thật có được gán không? | Loại tượng khỏi nhãn xe, giữ làm nền âm tính; không dùng ignore chỉ để che tượng. |

## 2. Pha 2: chỗ tôi bất đồng với nhóm

Chưa có thông tin về cuộc họp hoặc guideline của các thành viên khác, nên chưa ghi bất đồng hay kết luận của nhóm. Các câu hỏi chuẩn bị họp được chuyển từ guideline sang đây:

| Mã | Câu hỏi cần chốt | Đề xuất ban đầu | Ảnh liên quan |
|---|---|---|---|
| H01 | Thêm lớp hay loại khỏi phạm vi các loại xe v0 đang thiếu? | Thêm `bus`, `bicycle`, `cyclo`, `tuk_tuk`; không ép vào lớp gần giống. | 003, 004, 006, 009, 016, 023, 029, 031, 035, 037, 039, 040. |
| H02 | Xe độ/tác phẩm kim loại và nhân vật hóa trang được phân biệt bằng chứng nào? | Xem lại `img_011` ở kích thước gốc; chưa khẳng định bản chất các vật nghi vấn. | 011. |
| H03 | Xe diễu hành vật lý có thuộc car; nhân vật bên cạnh là người hay hình nộm? | Xe đề xuất `car` có review; nhân vật chỉ là `person` nếu có căn cứ là người thật. | 019. |
| H04 | Vật vàng trên nóc wagon là xe thật hay mô hình/vỏ trưng bày? | Đề xuất loại vật vàng; gán wagon thật. | 024; đối chiếu 002, 038. |
| H05 | Đầu kéo và rơ-moóc chở xe đếm mấy box? | Một truck cho tổ hợp, xe được chở là các box riêng. | 002. |
| H06 | Có căn cứ loại pickup tiền cảnh như xe chủ không? | Chỉ loại khi chứng minh là ego; tạm đề xuất gán phần pickup nhìn thấy. | 012, 020. |
| H07 | Chốt ngưỡng che, biên box theo phần thấy, hàng rời và ignore. | Kiểm ranh giới 20/50 px và 30/70% theo mục 2.3, 3 của guideline. | 001, 014, 015, 018, 021, 029, 032, 035, 040. |

Sau cuộc họp, bổ sung: điểm khác với thành viên nào, nhóm chốt gì, lý do đồng ý/chưa đồng ý. H01–H07 hiện chỉ là câu hỏi chuẩn bị, không phải quyết định đã được nhóm thông qua.

## 3. Pha 3: ảnh tôi đã gán

- Số ảnh được giao: **24**, theo [danh sách phân công](../qc/assignments/2A202603183.txt).
- Số ảnh đã gán, số box đã vẽ, số lần tick `can_review`: **chưa ghi nhận; bổ sung sau khi gán thực tế**.
- Ca lưỡng lự nhất khi gán: **chưa ghi nhận**. Các ca dự kiến cần chú ý: `img_011`, `img_024`, `img_040`.

```text
img_001.jpg  img_003.jpg  img_004.jpg  img_006.jpg
img_007.jpg  img_010.jpg  img_011.jpg  img_013.jpg
img_015.jpg  img_017.jpg  img_018.jpg  img_020.jpg
img_022.jpg  img_023.jpg  img_024.jpg  img_027.jpg
img_028.jpg  img_029.jpg  img_031.jpg  img_032.jpg
img_035.jpg  img_037.jpg  img_039.jpg  img_040.jpg
```

Gán độc lập theo v1.0 đã thống nhất, export COCO 1.0 thành `submission/labels/2A202603183_HoangNhatAnh.json`, rồi chạy:

```powershell
python scripts/validate_labels.py submission/labels/2A202603183_HoangNhatAnh.json
```

Chưa có kết quả chạy kiểm tra file nhãn được ghi nhận trong ghi chú này.

## 4. Pha 4–5: tôi lệch ở đâu

- Các ca có mã `2A202603183` trong `calibration_candidates.csv`: **bổ sung sau khi có nhãn và chạy so sánh**.
- Nguyên nhân lệch do guideline mơ hồ hay cách áp dụng quy tắc: **chưa có dữ liệu để kết luận**.
- Quyết định calibration quan trọng nhất và phiên bản quy tắc tương ứng: **bổ sung sau cuộc họp calibration**.
- Chưa ghi IAA, số lỗi QC hoặc quyết định Release/Hold/Rework khi chưa có kết quả thực tế.

## 5. Dùng AI

- Công cụ: **Codex/ChatGPT**.
- Cách sử dụng: đọc hướng dẫn trong repo, xem 40 ảnh gốc và ảnh tổng hợp, hỗ trợ soạn guideline, đề xuất quy tắc/ca khó, sau đó tách ghi chú cá nhân theo mẫu. AI chưa tạo box hoặc nhãn COCO.
- Kiểm tra kỹ thuật đã làm: đối chiếu đủ 40 dòng ca ảnh, đủ 5 phần guideline, danh sách 24 ảnh khớp phân công và đường dẫn tham chiếu tồn tại. Những kiểm tra này không xác nhận quyết định thị giác đã đúng hoặc học viên đã tự duyệt.
- Phần Hoàng Nhật Anh cần tự xác nhận: mở ảnh gốc, đối chiếu từng quyết định, đặc biệt các ca chưa rõ `011`, `019`, `024`, vấn đề ego ở `012` và các ngưỡng che/ignore.
- [RULES.md](../../RULES.md) giới hạn dùng AI để nhìn ảnh rồi quyết định nhãn và yêu cầu ca khó phản ánh nhận định của học viên. Bản dự thảo hiện có hỗ trợ AI ở phần này; ghi rõ nguồn hỗ trợ, không coi đó là bằng chứng tự làm độc lập hoặc đã tự kiểm xong.

## 6. Bài học

Điểm rút ra từ việc tổ chức tài liệu: guideline cần tập trung vào định nghĩa lớp, thuộc tính, quy tắc box, ca khó và QC; quá trình làm bài, phân công, bất đồng, sử dụng AI và bài học được ghi riêng trong `individual_notes`.

Điều dự kiến áp dụng lần sau: ghi ngay mã ảnh, điều v0 chưa trả lời và lý do của quyết định khi tự xem ảnh; phân biệt rõ đề xuất cá nhân với quyết định đã được nhóm chốt. Bổ sung bài học thực tế sau khi hoàn thành gán nhãn và calibration.
