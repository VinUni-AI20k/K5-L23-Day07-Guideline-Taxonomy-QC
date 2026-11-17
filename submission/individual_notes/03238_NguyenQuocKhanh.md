# Ghi chú cá nhân — 03238 (Nguyễn Quốc Khánh)

> Copy file này thành `submission/individual_notes/<mã>.md`. Mỗi thành viên một file, ngắn gọn (khoảng một trang), tự viết.

## 1. Pha 1: ba ca khó tôi tìm ra trong 40 ảnh
| Ảnh | v0 không trả lời được gì | Quyết định ban đầu của tôi |
|---|---|---|
| `img_014` | Người đi xe máy đi nhanh bị mờ chuyển động (motion blur) trong điều kiện thiếu sáng. v0 hoàn toàn không có quy định về ngưỡng mờ nhòe, không nêu rõ khi vật thể bị mờ vệt chuyển động thì có được vẽ box hay phải bỏ qua. | Vẫn gán tách 2 box `motorcycle` và `person` nếu mắt người vẫn nhận diện được cấu trúc; tick `can_review = true`. Mờ chuyển động không tự động loại bỏ nếu mắt người vẫn nhận biết được đối tượng (R-06, R-08). |
| `img_017` | Tượng đá danh nhân cưỡi ngựa, đầu có đội nón giao thông. v0 chỉ ghi chung "gán box cho mọi người và phương tiện", không phân biệt giữa người thật tham gia giao thông với tượng đài điêu khắc nghệ thuật (dễ gây lỗi False Positive / phanh ma). | **Tuyệt đối không gán box** (cả người cưỡi lẫn con ngựa). Tượng điêu khắc nghệ thuật, không phải người thật tham gia giao thông; đóng vai trò mẫu âm nền / hard negative (R-04). |
| `img_019` | Đám đông cổ vũ có nhiều người chen chúc, không xác định được từng object riêng lẻ. v0 chỉ ghi chung chung `ignore_region` là "Vùng không cần gán từng vật", không đưa ra tiêu chí cụ thể khi nào thì gom đám đông vào vùng bỏ qua. | Đánh nhãn là `ignore_region` bao trùm toàn bộ đám đông cổ vũ vì quá nhiều người chen chúc, không thể xác định và tách ranh giới của từng đối tượng riêng biệt (R-01, R-07). |

> *(Ghi chú khảo sát thêm ở Pha 1: Ngoài 3 ca tiêu biểu trên, tôi cũng đã ghi nhận và đề xuất hướng xử lý cho các ca biên khác như xe chở xe `img_002`, xe tuk-tuk chở khách `img_004`, xe che khuất khó phân biệt `img_016`, bãi đỗ xe dày đặc `img_030`, ma-nơ-canh `img_033`, tuk-tuk chở hàng cao trên nóc `img_035`... làm cơ sở thống nhất tại Pha 2).*

## 2. Pha 2: chỗ tôi bất đồng với nhóm
- Chỗ nào bản của tôi khác bản của bạn? Cuối cùng nhóm chốt gì, tôi đồng ý / chưa đồng ý vì sao?

## 3. Pha 3: ảnh tôi đã gán
- Số ảnh được giao: **24** | Số box đã vẽ: **246** | Số lần tôi tick `can_review`: **14**
- Phân bố lớp đã gán: 103 `person`, 74 `motorcycle`, 40 `car`, 8 `van`, 5 `bicycle`, 4 `truck`, 4 `traffic_sign`, 3 `tuk_tuk`, 3 `bus`, 2 `ignore_region`.
- Ca tôi lưỡng lự nhất khi gán:
  - **`img_016.jpg` (Xe mép trái bị che khuất nặng):** Phương tiện ở rìa bên trái chỉ lọt vào khung hình một phần nhỏ góc đầu và mui che nắng (`truncated = yes`). Tôi phân vân gay gắt giữa việc định danh đây là xe `tuk_tuk` hay ô tô con (`car`). Nhìn kết cấu khung sườn và mui bạt có nét đặc trưng của tuk-tuk, nhưng góc nhìn quá hẹp gây rủi ro nhầm lẫn cao. Tôi quyết định gán `tuk_tuk`, ôm sát mép nhìn thấy và tick `can_review = True` để đưa ra nhóm cùng phân tích.
  - Ngoài ra, tại **`img_023.jpg`**, cụm 6 xe máy ở góc trái đỗ chen chúc, che khuất nhau sâu (`occluded_level` mức 2–3) khiến tôi lưỡng lự giữa việc tách từng box `motorcycle` (bằng cách nội suy theo ranh giới bộ phận nhìn thấy) hay gom vào một box `ignore_region`. Tôi đã chọn tách từng box và bật `can_review` trên cả 6 box.

## 4. Pha 4–5: tôi lệch ở đâu
- Trong `calibration_candidates.csv`, các ca có tên tôi: tôi lệch vì guideline mơ hồ hay vì tôi chưa nắm quy tắc?
- Quyết định calibration nào tôi thấy quan trọng nhất?

## 5. Dùng AI
- **Công cụ sử dụng:** Trợ lý AI (Google Antigravity / Gemini) kết hợp các kịch bản kiểm thử Python.
- **Mục đích sử dụng:**
  - Hỗ trợ rà soát, đối chiếu và chuẩn hóa văn bản guideline (so sánh các điểm bất đồng giữa 5 bản cá nhân từ Pha 1 để đưa vào guideline v1.0 chung của nhóm).
  - Viết và chạy các đoạn mã Python tự động kiểm tra cú pháp, cấu trúc dữ liệu COCO 1.0 của file `submission/labels/238.json` (trích xuất thống kê số lượng ảnh, tổng số box, phân bố category, đếm số box có cờ `can_review`).
  - Tra cứu nhanh đặc tả kỹ thuật COCO format và quy ước tính IoU.
  *(Cam kết: Không sử dụng bất kỳ công cụ AI nào để gán nhãn tự động thay thế mắt người — toàn bộ 24 ảnh và 246 box đều do tôi tự quan sát và vẽ thủ công trên CVAT).*
- **Cách tôi kiểm tra kết quả:**
  - Chạy các script thẩm định chính thức của bài lab: `py scripts/validate_labels.py submission/labels/238.json` và `py scripts/check_submission.py` để đảm bảo file nhãn không có lỗi cấu trúc, đủ 24 ảnh theo phân công.
  - Đối chiếu thủ công từng số liệu thống kê (24 ảnh, 246 box, 14 can_review) với giao diện trực quan trên CVAT.
  - Tự đọc lại toàn bộ nội dung văn bản để đảm bảo tính logic, khách quan và phản ánh đúng thực tế quá trình làm việc của bản thân và nhóm.

## 6. Bài học
- Một điều tôi sẽ làm khác khi viết guideline lần sau:
