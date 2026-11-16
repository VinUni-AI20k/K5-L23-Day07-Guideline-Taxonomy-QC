# Guideline gán nhãn — v0.1 — 229 - Phan Hải Đăng

- Phiên bản: v0.1 (cá nhân)
- Ngày: 2026-11-16
- Người viết / duyệt: 229 - Phan Hải Đăng

## 1. Mục tiêu
Bộ nhãn dùng để huấn luyện mô hình phát hiện **người và phương tiện giao thông** trên ảnh đường phố châu Á (camera giao thông / hỗ trợ lái).
- **Sai sót nguy hiểm nhất:** Bỏ sót `person` hoặc phương tiện đang lưu thông; nhận nhầm vật giả (tượng, ma-nơ-canh, đồ chơi, phản chiếu, hình in) thành vật thật; gộp nhiều vật thành 1 box.

## 2. Lớp và thuộc tính

### Lớp (mỗi vật thuộc đúng một lớp)
| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con 4–7 chỗ có khoang hành lý liền thân. | Sedan, hatchback, SUV, MPV, taxi. | Không gồm xe bán tải có thùng hàng (`truck`), không gồm xe van/minibus (`van`). |
| `truck` | Xe chở hàng có thùng tách rời hoặc thùng hở (gồm cả xe bán tải/pickup và bán tải gắn nắp thùng cao). | Xe tải thùng, xe ben, pickup thùng hở, bán tải nắp cao (`img_037`). | Không gồm xe tải van kín liền thân (`van`). |
| `van` | Xe thùng kín liền thân cỡ nhỏ/trung chở hàng hoặc chở khách kiểu minibus. | Xe van giao hàng, xe khách 16 chỗ. | Không gồm SUV/MPV gia đình (`car`), bán tải nắp thùng cao (`truck`), hay xe buýt cỡ lớn (`ignore_region`). |
| `motorcycle` | Xe hai bánh gắn động cơ. | Xe máy, xe tay ga, mô tô, xe máy điện. | Không gồm xe đạp không động cơ, không gồm tuk-tuk/xe 3 bánh (`ignore_region`), không gộp người ngồi vào box xe. |
| `person` | Con người thật đang đứng, đi bộ hoặc ngồi/lái trên phương tiện. | Người đi bộ, người lái xe máy, người ngồi sau. | Không gồm tượng, ma-nơ-canh, hình in quảng cáo, bóng phản chiếu. |
| `ignore_region` | Vùng không gán từng vật: đám đông dày đặc, cụm vật `< 20 px`, hoặc phương tiện ngoài 5 lớp chính (tuk-tuk, xe buýt cỡ lớn). | Đám đông xa, bãi xe chồng lấn, tuk-tuk (`img_004`, `img_035`), xe buýt (`img_009`). | Không dùng cho 1–2 vật thuộc 5 lớp chính nhìn rõ và cao ≥ 20 px. |

- **Quy tắc định nghĩa dứt khoát cho các ca giáp ranh / ngoài 5 lớp:**
  1. **Tuk-tuk / xe 3 bánh (`img_004`, `img_035`):** Phương tiện 3 bánh có mái che/cabin chở khách → gán **`ignore_region`** (vì không thuộc `motorcycle` 2 bánh cũng không phải `car`).
  2. **Xe buýt (`img_009`):** Xe chở khách cỡ lớn (> 24 chỗ, thân dài hơn hẳn `van`) → gán **`ignore_region`** (không gán nhầm sang `van` hay `truck`).
  3. **Xe bán tải nắp thùng cao (`img_037`):** Xe pickup có cabin và thùng sau lắp nắp kín cao ngang nóc → gán **`truck`** (giữ nhất quán theo bản chất xe bán tải, không chuyển sang `van`).

### Thuộc tính
| Thuộc tính | Giá trị | Nghĩa từng mức & Ngưỡng đo được |
|---|---|---|
| `occluded_level` | `0` | Không bị che (`0%` diện tích bị vật khác che). |
| | `1` | Có bị che (`> 0%` diện tích bị vật khác che khuất nhưng vẫn nhận diện được vật). |
| `truncated` | `no` | Vật nằm trọn trong khung ảnh, không bị cạnh ảnh cắt. |
| | `yes` | Một phần thân vật bị cắt trực tiếp bởi ít nhất 1 cạnh khung ảnh. |
| `can_review` | `false` / `true` | Tick `true` khi ca mơ hồ chưa có quy tắc, để đưa ra họp calibration. |

## 3. Quy tắc vẽ box
1. **Ôm sát phần nhìn thấy:** Box khít rìa ngoài cùng phần nhìn thấy của vật; không đoán vẽ ra ngoài vùng bị che khuất hoặc ngoài mép ảnh.
2. **Người đi xe máy:**
   - **Lớp & Số box:** Tách riêng **1 box `motorcycle`** + **1 box `person`** cho **mỗi người** ngồi trên xe (1 người lái = 2 box; chở thêm 1 người sau = 3 box).
   - **Phần được bao:** Box `motorcycle` chỉ ôm khít **phần xe** (bánh, khung, tay lái, gương, yếm), không kéo lên bao đầu người lái. Box `person` ôm khít phần nhìn thấy của **người** (từ đỉnh đầu/mũ bảo hiểm tới hết chân/bàn chân); nếu chân bị yếm xe che thì gắn `occluded_level = 1`.
   - **Kiểm thử chéo trên 2 ảnh:** Áp dụng quy tắc trên vào `img_005` (cận cảnh, thấy rõ chân/đầu → tách 2 box rõ ràng) và thử lại trên `img_006` (góc xa, nhiều xe nối đuôi → vẫn tách được `motorcycle` + `person` cho các xe cao ≥ 20 px; xe bị che phần dưới đánh `occluded_level = 1`).
3. **Vật quá nhỏ (`< 20 px`):** Vật đơn lẻ cao `< 20 px` → **loại theo quy tắc** (không gán). Cụm nhiều vật `< 20 px` tụ lại → khoanh 1 `ignore_region`.
4. **Phân biệt "Ca loại theo quy tắc" vs "Ca cần hỏi reviewer":**
   - **Ca LOẠI / XỬ LÝ NGAY theo quy tắc:**
     1. Vật đơn lẻ có chiều cao **< 20 px** → bỏ qua không gán.
     2. Vật không phải thực thể giao thông thật (**tượng, ma-nơ-canh, đồ chơi/mô hình, hình in, ảnh phản chiếu qua gương**) → loại, không gán.
     3. Vật bị che khuất một phần nhưng nhận diện chắc chắn lớp và cao ≥ 20 px → gán phần nhìn thấy với `occluded_level = 1`.
   - **Ca CẦN HỎI REVIEWER (tick `can_review` nếu gặp biên mờ/khó tách):**
     1. Vật chuyển động bị mờ nặng (`img_014`) không xác định chắc ranh giới box.
     2. Cụm đám đông chồng lấn ở ranh giới giữa tách box từng vật với khoanh `ignore_region` (`img_021`, `img_030`).

## 4. Ca khó
| Ảnh | Tình huống | Phân loại | Quyết định | Lý do |
|---|---|---|---|---|
| `img_002` | Xe tải chở nhiều ô tô trên thùng | Theo quy tắc | Chỉ gán xe chở (`truck`), không gán xe trên thùng | Xe bị chở không tự lưu thông; gán dễ làm rối mô hình |
| `img_004`, `img_035` | Tuk-tuk / xe 3 bánh | Theo quy tắc | Gán `ignore_region` | Không thuộc 5 lớp phương tiện chính, tránh lệch giữa `motorcycle` và `car` |
| `img_009` | Xe buýt cỡ lớn | Theo quy tắc | Gán `ignore_region` | Xe > 24 chỗ ngoài taxonomy gốc, không gộp vào `van` hay `truck` |
| `img_037` | Xe bán tải có nắp thùng cao | Theo quy tắc | Gán `truck` | Bản chất là xe bán tải (pickup), chỉ gắn thêm nắp thùng |
| `img_011`, `img_017`, `img_027`, `img_033`, `img_038` | Tượng, ma-nơ-canh, xe giả tưởng/mô hình | Loại theo quy tắc | Không gán | Không phải người/phương tiện thật tham gia giao thông |
| `img_020` | Hình phản chiếu qua gương chiếu hậu | Loại theo quy tắc | Không gán vật trong gương | Là ảnh ảo phản chiếu, gán sẽ dạy sai ngữ cảnh không gian |
| `img_006`, `img_008` | Nhiều vật thể, bị che khuất, ánh sáng tối | Theo quy tắc | Gán phần nhìn thấy ≥ 20 px, gắn `occluded_level = 1` | Che khuất nhau nhiều nhưng vẫn nhận diện được lớp |
| `img_014` | Người đi bộ bị mờ (motion blur) | Hỏi reviewer | Gán `person` phần nhìn thấy, tick `can_review` | Biên vật mờ dễ gây lệch IoU < 0.85 |
| `img_021`, `img_030` | Đám đông xe máy dày đặc, vật `< 20 px` | Quy tắc + Hỏi | Tách xe/người rõ ở tiền cảnh (`occluded_level = 1`); cụm chồng lấn/`< 20 px` phía sau → `ignore_region` | Mật độ quá dày, gán hết dễ bỏ sót và IoU thấp |

## 5. QC và phiên bản
- Ngưỡng QC (`taxonomy.json`): IoU TB ≥ 0.85, đồng thuận lớp ≥ 95%, tỉ lệ ảnh lỗi ≤ 2%.
- Ca chưa chốt khi gán Pha 3: tick `can_review = true`, không tự ý sửa guideline trước Pha 5.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 → v0.1 | Bổ sung ngưỡng % `occluded_level`, quy tắc tách người/xe máy, ngưỡng `< 20 px`, phân loại ca loại vs ca hỏi reviewer | Vá các chỗ mơ hồ của `v0` trước khi họp Pha 2 |
