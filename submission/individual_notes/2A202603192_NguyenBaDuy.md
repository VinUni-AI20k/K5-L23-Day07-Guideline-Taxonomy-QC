# Ghi chú cá nhân — 2A202603192 - Nguyễn Bá Duy

- Thành viên: Nguyễn Bá Duy (MSHV: 2A202603192, Mã thành viên: 192 / Nhóm T005)
- Vai trò trong nhóm: Điều phối viên (Leader), phụ trách chia ảnh, thiết lập pipeline CVAT và tổng hợp báo cáo QC.

---

## 1. Pha 1: Ba ca khó tôi tìm ra trong 40 ảnh

| Ảnh | v0 không trả lời được gì | Quyết định ban đầu của tôi |
|---|---|---|
| `img_020.jpg` | Guideline v0 không đề cập đến hiện tượng ảnh phản chiếu trong gương chiếu hậu (rearview mirror) của xe buồng lái. | **Không gán box** cho bất kỳ ô tô hay xe máy nào nhìn thấy trong mặt gương phản chiếu. Nếu gán, xe tự lái sẽ phát hiện vật cản ảo ngay phía trước xe chủ, gây hiện tượng phanh khẩn cấp vô căn cứ (Phantom Braking). Khung gương khoanh `ignore_region` hoặc bỏ qua. |
| `img_029.jpg` | Guideline v0 không nói rõ ranh giới bounding box khi xe máy chở khối hàng hóa khổng lồ vượt gấp 3-4 lần kích thước xe và người lái gần như bị che lấp. | Box `motorcycle` bao gồm cả khung xe và toàn bộ khối hàng cồng kềnh gắn liền vì khối hàng là vật cản động lực học trực tiếp; gán 1 box `person` cho phần nhìn thấy của người lái (`occluded_level = 2` hoặc `3`). |
| `img_038.jpg` | Guideline v0 định nghĩa `car` là ô tô con, `person` là người, nhưng không có điều khoản loại trừ mô hình đồ chơi thu nhỏ hoặc búp bê trưng bày ở sạp hàng. | **Không gán** các mô hình xe đồ chơi và búp bê thành `car`/`person`. Khoanh toàn bộ quầy hàng đồ chơi vào `ignore_region` để không làm ô nhiễm bộ dữ liệu huấn luyện xe tự lái. |

---

## 2. Pha 2: Chỗ tôi bất đồng với nhóm
- **Vấn đề phân loại xe Tuk-tuk / Auto Rickshaw (`img_004`, `img_035`, `img_040`):**
  - Thành viên khác ban đầu đề xuất xếp vào `motorcycle` vì xe có 3 bánh và tay lái ghi-đông.
  - Quan điểm của tôi: Tuk-tuk là phương tiện cơ giới chở khách nhiều chỗ, có mui che kín, cấu trúc khoang hành khách dạng ca-bin, vận hành tương đương taxi cỡ nhỏ trong đô thị châu Á. Do đó, xếp vào `car` là an toàn và hợp lý nhất theo chuẩn phân loại ADAS.
  - Kết quả thống nhất: Cả nhóm đồng thuận phân loại Tuk-tuk thành `car`, đồng thời ghi chú rõ ràng vào `guideline_v1.0_agreed.md`.
- **Vấn đề xe Xích lô (`img_006`, `img_009`, `img_023`):**
  - Một số bạn đề xuất gán `motorcycle`.
  - Quan điểm của tôi: Xích lô là xe thô sơ 3 bánh dùng sức người đạp chân, hoàn toàn không có động cơ đốt trong hoặc động cơ điện. Vì vậy, không gán nhãn phương tiện, chỉ gán nhãn `person` cho người đạp và hành khách ngồi trên xe. Nhóm đã biểu quyết thông qua quan điểm này 100%.

---

## 3. Pha 3: Ảnh tôi đã gán
- Số ảnh được giao: 24 ảnh (thuộc tập 40 ảnh của nhóm T005, theo phân bổ `assignment.csv`).
- Số box dự kiến đã vẽ: ~180 box trên 24 ảnh.
- Số lần bật cờ `can_review`: 3 lần (tại các ảnh có xe độ diễu hành `img_019`, xe chở rau củ `img_012`, và xe máy chở hàng quá tải `img_029`).
- Ca lưỡng lự nhất: `img_019.jpg` (xe ô tô diễu hành hình Danger Mouse). Ban đầu phân vân liệu có nên coi là `car` hay xếp vào mô hình/vật trang trí. Tuy nhiên, sau khi quan sát thấy người lái ngồi trong điều khiển xe di chuyển trên lòng đường công cộng, tôi quyết định gán `car` để bảo đảm an toàn va chạm.

---

## 4. Pha 4–5: Tôi lệch ở đâu
- Trong quá trình đối chiếu IAA: Một số lệch phổ biến xảy ra ở ranh giới vẽ box người ngồi trên xe máy (phần gót chân có bao gồm bàn đạp xe hay không).
- Quyết định calibration quan trọng nhất: Thống nhất quy tắc vẽ box tách biệt giữa người lái và xe máy (2 box chồng lấn: box người lấy từ đỉnh nón bảo hiểm đến bàn chân, box xe máy lấy từ đỉnh ghi-đông đến mặt tiếp đất của bánh xe).

---

## 5. Dùng AI
- Công cụ sử dụng: Antigravity Assistant (Gemini/Claude).
- Mục đích sử dụng: Hỗ trợ viết script tự động hóa chia task CVAT, kiểm tra tính toàn vẹn của dữ liệu và rà soát các trường hợp biên an toàn (Edge Cases) trong 40 ảnh giao thông.
- Cách kiểm tra kết quả: Kiểm chứng thủ công từng ảnh thực tế trong `data/images/`, chạy `python scripts/check_submission.py` và chạy bộ kiểm thử `python -m unittest discover -s tests -v` để đảm bảo không có bất kỳ lỗi logic nào.

---

## 6. Bài học
- Một điều tôi sẽ làm khác khi viết guideline lần sau: Luôn định nghĩa tiêu chí định lượng (ngưỡng pixel, tỷ lệ diện tích %) và bảng phân loại rõ ràng các trường hợp ngoại lệ ngay từ bản v0 để giảm thiểu tối đa các tranh chấp và chi phí hiệu chuẩn (calibration) về sau.
