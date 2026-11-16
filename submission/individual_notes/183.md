# Ghi chú cá nhân — 2A202603183 - Hoàng Nhật Anh

- Thành viên: Hoàng Nhật Anh (MSHV: 2A202603183, Mã thành viên: 183 / Nhóm T005)
- Vai trò trong nhóm: Thành viên phụ trách quản lý tài liệu guideline, đối soát logic quy tắc gán nhãn và kiểm thử kịch bản.

---

## 1. Pha 1: Ba ca khó tôi tìm ra trong 40 ảnh

| Ảnh | v0 không trả lời được gì | Quyết định ban đầu của tôi |
|---|---|---|
| `img_002.jpg` | Guideline v0 không quy định cách xử lý xe chuyên chở ô tô mang nhiều tầng xe. | Gán 1 box `truck` cho toàn bộ tổ hợp xe chuyên chở (đầu kéo + rơ-moóc sàn chở); mỗi xe ô tô con thật nằm trên sàn chở là một box `car` riêng biệt (`occluded_level = 1` hoặc `2`). |
| `img_024.jpg` | Không rõ vật trang trí dạng ô tô nhỏ màu vàng đặt trên nóc chiếc xe wagon đen có được gán thành xe con không. | Gán 1 box `car` cho chiếc wagon đen thật; loại bỏ vật màu vàng trên nóc vì là mô hình/vỏ trưng bày thu nhỏ, không phải xe thật được chuyên chở. |
| `img_029.jpg` | Thanh kim loại dài và bó hàng vượt xa khỏi thân xe máy, v0 chưa xác định biên box xe ôm đến đâu. | Bounding box của `motorcycle` chỉ ôm phần thân vỏ cơ học và bánh xe; thanh kim loại là hàng hóa rời, không mở rộng box xe theo thanh kim loại để tránh làm méo mó đặc trưng hình học của mô hình học máy. |

---

## 2. Pha 2: Chỗ tôi bất đồng với nhóm
- **Đề xuất tách riêng lớp `cyclo` so với gộp vào `bicycle`:**
  - *Quan điểm ban đầu của tôi:* Tôi đề xuất tách riêng 4 lớp mới gồm `bus`, `bicycle`, `cyclo`, `tuk_tuk`. Trong đó xích lô 3 bánh (`cyclo`) có kích thước và cấu trúc khác xe đạp 2 bánh thông thường.
  - *Thảo luận nhóm:* Duy và cả nhóm phân tích rằng trong 40 ảnh chỉ có 2 ảnh xích lô (`img_006`, `img_023`). Cả xe đạp và xích lô đều là phương tiện thô sơ đạp bằng sức người (human-powered pedal vehicles), cùng dải vận tốc chậm. Việc thêm lớp `cyclo` làm tăng độ phức tạp của taxonomy lên 10 lớp và phân tán mẫu huấn luyện.
  - *Kết luận thống nhất:* Tôi hoàn toàn đồng ý với nhóm gộp xích lô vào lớp **`bicycle`** (với định nghĩa mở rộng gồm xe đạp và xe xích lô đạp chân). Nhóm chốt taxonomy 9 lớp chính thức.
- **Quy tắc hàng hóa rời cồng kềnh (`img_012`, `img_029`, `img_035`):**
  - Tôi bảo vệ quan điểm: Box xe chỉ bám theo thân vỏ cơ học và phụ kiện gắn cố định, không kéo box theo hàng hóa rời (nông sản, bao xốp, thanh sắt). Nhóm đã thống nhất 100% đưa quy tắc chuẩn hóa này vào Guideline v1.0.

---

## 3. Pha 3: Ảnh tôi đã gán
- Số ảnh được giao: 24 ảnh (theo phân công tại `assignment.csv`).
- Số box đã vẽ: ~190 box trên 24 ảnh.
- Số lần tick `can_review`: 4 lần (các ca diễu hành `img_019`, xe chở xe `img_002`, xe chở hàng quá tải `img_035`, cosplay `img_011`).
- Ca lưỡng lự nhất: `img_011.jpg` (nhân vật Predator). Cần xác định kỹ đây là người thật mặc trang phục cosplay hay tượng triển lãm. Sau khi phóng to quan sát nếp gấp vải và tư thế đứng, quyết định gán `person` và bật `can_review=true`.

---

## 4. Pha 4–5: Tôi lệch ở đâu
- Các ca có tên tôi trong `calibration_candidates.csv` chủ yếu lệch ở biên cắt mép chân người đi xe máy/xe đạp và mức ước lượng che khuất giữa mức 1 (dưới 30%) và mức 2 (trên 30%).
- Quyết định calibration quan trọng nhất: Thống nhất áp dụng ngưỡng che $30\% - 70\%$ và chuẩn hóa quy tắc xe buýt `bus` không gán hành khách nhìn qua kính kín.

---

## 5. Dùng AI
- Công cụ: Antigravity Assistant.
- Công việc: Hỗ trợ rà soát 40 ảnh, lập bảng đối chiếu tiêu chuẩn COCO và kiểm tra tính toàn vẹn của file dữ liệu.
- Cách kiểm tra: Mở trực tiếp từng file ảnh gốc trong `data/images/`, đối chiếu với `schemas/taxonomy.schema.json` và chạy lệnh `python scripts/check_submission.py`.

---

## 6. Bài học
- Một điều tôi sẽ làm khác khi viết guideline lần sau: Xây dựng quy tắc biên cho hàng hóa rời và ranh giới phương tiện thô sơ ngay từ đầu để tránh phải tranh luận kéo dài giữa các thành viên.
