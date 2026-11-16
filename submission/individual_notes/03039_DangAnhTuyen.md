# Ghi chú cá nhân — 039

Bản nháp có AI hỗ trợ tổng hợp từ guideline và file COCO. Tôi cần đọc lại, bổ sung trải nghiệm thực tế và xác nhận nội dung trước khi nộp.

## 1. Ba ca khó trong bản guideline cá nhân

| Ảnh | Điểm guideline v0 còn thiếu | Đề xuất trong bản cá nhân |
|---|---|---|
| `img_002` | Xe tải đang chở ô tô thì có cần gán từng xe được chở hay không? | Vẽ một box cho xe tải và box riêng cho từng ô tô đủ điều kiện. |
| `img_004`, `img_035` | Tuk-tuk chưa có lớp riêng nên dễ bị xếp vào xe máy hoặc bỏ qua. | Ban đầu đề xuất để ngoài phạm vi và đưa ra họp nhóm để chốt. |
| `img_037` | Xe bán tải lắp nắp thùng cao dễ bị nhầm với van. | Đề xuất `truck` vì xe vẫn có cabin và thùng hàng riêng. |

## 2. Những điểm khác nhau khi thống nhất guideline

Trong bản cá nhân, tuk-tuk và xe buýt được đề xuất để ngoài phạm vi. Bản nhóm v1.0 đã bổ sung hai lớp `tuk_tuk` và `bus`, nên lượt gán nhãn dùng danh mục mới này. Nhóm cũng thống nhất xe bán tải có nắp thùng là `truck`, người và phương tiện được gán riêng, còn xe đạp và xích lô đạp chân nằm ngoài danh mục.

Phần cần tôi bổ sung trước khi nộp là lý do mình đồng ý hoặc còn băn khoăn với quyết định chung, dựa trên buổi họp thực tế.

## 3. Kết quả gán nhãn cá nhân

- Được phân công 24 ảnh theo `submission/qc/assignments/039.txt`.
- File đã xuất là `submission/labels/03039_DangAnhTuyen.json`, chứa 24 ảnh và 189 annotation bbox, tính cả vùng bỏ qua nếu có.
- Trong file xuất hiện tại, có 0 annotation bật `can_review`. Con số này thể hiện trạng thái cuối trong file, không xác định được tổng số lần đã tick rồi bỏ tick trong quá trình làm.
- Số bbox trên được tổng hợp từ file COCO, gồm nhãn tạo thủ công và nhãn có mô hình hỗ trợ.
- Cần bổ sung một ca tôi thực sự lưỡng lự khi gán, kèm ID ảnh, điểm khó và cách tôi đã xử lý.

## 4. Kết quả đối chiếu và calibration

Chưa có kết quả IAA và calibration trong bản ghi chú này. Sau khi nhóm đối chiếu nhãn, tôi sẽ bổ sung ca lệch liên quan đến mình, nguyên nhân và quyết định sửa quan trọng nhất.

## 5. Việc sử dụng AI

Đã dùng ChatGPT/Codex hỗ trợ soạn và chỉnh câu chữ guideline cá nhân, thiết lập task CVAT và tích hợp YOLO26n. YOLO26n hỗ trợ tạo bbox gợi ý cho `person`, `car`, `motorcycle`, `bus` và `truck`.

Các lớp `van`, `tuk_tuk`, `ignore_region` cùng mức che khuất và cắt mép cần được kiểm tra theo guideline v1.0. Trước khi nộp, tôi cần ghi cụ thể cách mình đã rà lại bbox, sửa nhãn sai và bổ sung đối tượng bị bỏ sót. Việc dùng mô hình cần được khai báo đúng vì quy định Day 07 dành bước quyết định và vẽ box cho người thật.

## 6. Bài học cá nhân

Cần bổ sung một điều tôi rút ra từ quá trình thực hiện và sẽ làm khác khi viết guideline lần sau. Có thể liên hệ với cách phân biệt lớp, chọn mức che khuất hoặc xử lý trường hợp ngoài phạm vi, dựa trên trải nghiệm thực tế của mình.
