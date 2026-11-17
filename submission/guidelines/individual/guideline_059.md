# Guideline gán nhãn — v0.1 (Bản đề xuất cá nhân - Thành viên `<mã>`)

- Phiên bản: v0.1 (Cá nhân)
- Loại nhãn: bounding box (hộp chữ nhật) trên ảnh đường phố
- Công cụ: CVAT, xuất COCO 1.0

---

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình phát hiện **người và phương tiện** tham gia giao thông trên ảnh đường phố (phục vụ camera giám sát giao thông và hệ thống xe tự lái). Dữ liệu cần đảm bảo tính nhất quán cao về ranh giới hộp (bounding box), phân loại phương tiện đặc thù và xử lý triệt để các đối tượng gây nhiễu.

---

## 2. Lớp và thuộc tính

### 2.1. Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa chi tiết & Ranh giới phân loại |
|---|---|
| `car` | Ô tô con chở người (sedan, hatchback, SUV, crossover, taxi, xe thể thao, xe bán tải cabin kép). |
| `truck` | Xe tải chuyên chở hàng hóa (xe tải thùng, xe ben, xe đầu kéo, xe bồn, xe chở xe). |
| `van` | Xe thùng kín cỡ nhỏ, xe bán tải (minivan, xe khách cỡ nhỏ dưới 16 chỗ, xe chở hàng thùng liền khối). |
| `motorcycle` | Xe gắn máy 2 bánh, mô tô phân khối lớn, xe tay ga, xe điện dáng xe máy. |
| `person` | Người thật đang tham gia giao thông (người đi bộ, người điều khiển phương tiện, người ngồi sau xe máy/xe đạp, người đứng/ngồi trên vỉa hè). |
| `ignore_region` | Vùng tập trung quá đông đối tượng nhỏ ở hậu cảnh hoặc vùng không thể tách rời từng vật thể riêng lẻ (ví dụ: bãi đỗ xe dày đặc ở xa, đám đông người đi bộ ở tít cuối đường). |

### 2.2. Thuộc tính

| Thuộc tính | Giá trị | Ý nghĩa & Tiêu chí định lượng |
|---|---|---|
| `occluded_level` | `0` | **Thấy rõ hoàn toàn** (bị che khuất $< 10\%$). |
| | `1` | **Bị che ít** (bị che khuất từ $10\%$ đến $< 40\%$, vẫn nhận diện rõ toàn bộ cấu trúc). |
| | `2` | **Bị che nhiều** (bị che khuất từ $40\%$ đến $< 75\%$, phải suy đoán một phần khung xe/cơ thể). |
| | `3` | **Bị che gần hết / Không rõ** (bị che $\ge 75\%$, chỉ lộ một phần nhỏ như bánh xe hoặc đầu người). |
| `truncated` | `no` | Toàn bộ vật thể nằm gọn bên trong khung hình. |
| | `yes` | Vật thể bị cắt ngang bởi một hoặc nhiều cạnh mép của ảnh. |
| `can_review` | `false` / `true` | Tick `true` khi gặp ca mơ hồ (ví dụ: phân vân giữa `car` và `van`, xe độ chế lạ, hoặc không chắc có nên vẽ hay bỏ qua) để đưa ra thảo luận nhóm. |

---

## 3. Quy tắc vẽ box

1. **Nguyên tắc ôm sát (Tight Bounding Box):**
   - Box phải ôm sát mép ngoài cùng của phần vật thể **nhìn thấy được** (bao gồm cả gương chiếu hậu, bánh xe, ba-lô đang đeo trên người).
   - **Không** kéo rộng box để đoán phần bị che khuất quá sâu hoặc phần bị cắt ở mép ảnh.
   - **Không** bao gồm bóng đổ (shadow) trên mặt đường hoặc khói bụi.
2. **Quy tắc đối với người đi xe máy (`person` + `motorcycle`):**
   - **Tách riêng 2 box:** Vẽ 1 box lớp `motorcycle` bao toàn bộ chiếc xe (từ bánh trước đến đuôi xe, từ tay lái/gương xuống mặt đất) và 1 box riêng lớp `person` bao toàn bộ người lái (từ đỉnh mũ bảo hiểm đến bàn chân đặt trên gác chân).
   - Nếu có người ngồi sau: Mỗi người ngồi sau được gán thêm 1 box `person` độc lập.
3. **Ngưỡng kích thước tối thiểu:**
   - Bỏ qua các đối tượng ở quá xa có kích thước chiều rộng hoặc chiều cao $< 15\text{ pixels}$ (hoặc diện tích $< 225\text{ px}^2$). Nếu có nhiều vật nhỏ tụm lại, dùng 1 box `ignore_region` bao chung vùng đó.

---

## 4. Ca khó (Tổng hợp từ 40 ảnh)

Dưới đây là các tình huống thực tế xuất hiện trong tập dữ liệu và quy tắc xử lý đề xuất:

| Tình huống đặc biệt | Mã ảnh ví dụ | Quyết định xử lý | Lý do / Giải thích quy tắc |
|---|---|---|---|
| **Người giả (Tượng, Ma-nơ-canh, Hình vẽ quảng cáo)** | `img_033`  | **Loại theo quy tắc (Không vẽ box)** | Không phải người thật tham gia giao thông; gán nhãn sẽ làm sai lệch mô hình phát hiện người đi bộ. |
| **Xe giả tưởng / Mô hình trưng bày / Tượng xe** | `img_002`  | **Loại theo quy tắc (Không vẽ box)** | Không phải phương tiện giao thông thực tế hoạt động trên đường. |
| **Hình phản chiếu qua gương / Cửa kính cửa hàng** | `img_020`  | **Loại theo quy tắc (Không vẽ box)** | Chỉ là ảnh ảo phản xạ, không tồn tại vật thể thực tại vị trí pixel đó. |
| **Xe chở xe (Xe tải chở ô tô con hoặc chở xe máy)** | `img_002` *(điền mã ảnh)* | **Gán nhãn cả hai (Xe chở + Xe được chở)** | Vẽ 1 box `truck` cho xe tải lớn bên dưới, đồng thời vẽ các box `car`/`motorcycle` riêng cho từng xe nằm trên thùng nếu nhìn thấy rõ hình dạng. |
| **Xe ba gác / Tuk-tuk / Xe lôi** | `img_004`  | **Gán tạm `motorcycle` hoặc `van` + Tick `can_review`** | Chưa có lớp riêng trong taxonomy v0; cần hỏi reviewer/nhóm ở Pha 2 để thống nhất quy về một lớp chung hay bỏ qua. |
| **Xe đạp / Người đi xe đạp** | `img_003` | **Vẽ box `person` cho người; xe đạp tick `can_review` hoặc bỏ qua** | Taxonomy v0 chỉ định nghĩa `motorcycle`, không có lớp `bicycle`. Tuyệt đối không gán nhầm xe đạp thành `motorcycle`. |
| **Người ngồi bên trong ô tô (qua kính chắn gió)** | `img_010` | **Loại theo quy tắc (Không vẽ box `person`)** | Người ngồi trong cabin được coi là một phần của phương tiện `car`/`truck`/`van` đang di chuyển, tránh chồng lấn box không cần thiết. |
| **Vật bị che khuất nặng ($\ge 75\%$) chỉ lộ bánh xe/nóc xe** | `img_011` | **Không vẽ box nếu không nhận diện được loại xe** | Nếu chỉ thấy 1 phần nhỏ không đủ cơ sở phân biệt `car`, `van` hay `truck` thì bỏ qua để tránh nhiễu nhãn. |

---

## 5. QC và phiên bản

- **Quản lý phiên bản:** Mọi thay đổi làm thay đổi định nghĩa lớp, cách chọn vật hoặc ranh giới vẽ box đều phải tăng phiên bản guideline (`v0.1` $\rightarrow$ `v1.0` $\rightarrow$ `v1.1`).
- **Xử lý ca mơ hồ:** Bắt buộc tick thuộc tính `can_review = true` đối với mọi box chưa chắc chắn 100% để tổng hợp vào danh sách thảo luận khi họp nhóm ở Pha 2 và Calibration ở Pha 5.
- **Tự kiểm trước khi nộp:** Đảm bảo không có box nào bị gán nhầm lớp `ignore_region` cho đối tượng đơn lẻ rõ nét, và 100% ảnh không có đối tượng vẫn phải được lưu trong file export COCO 1.0.
