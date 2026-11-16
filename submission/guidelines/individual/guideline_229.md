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
| `truck` | Xe chở hàng có thùng tách rời hoặc thùng hở (gồm cả xe bán tải/pickup). | Xe tải thùng, xe ben, pickup thùng hở. | Không gồm xe tải van kín liền thân (`van`). **Ca giáp ranh (`img_037`):** bán tải gắn nắp thùng cao dễ nhầm với `van` → cần hỏi reviewer chốt `truck` hay `van`. |
| `van` | Xe thùng kín liền thân cỡ nhỏ/trung chở hàng hoặc chở khách kiểu minibus. | Xe van giao hàng, xe khách 16 chỗ. | Không gồm SUV/MPV gia đình (`car`), không gồm xe tải thùng rời (`truck`), không gồm xe buýt lớn (`img_009`). |
| `motorcycle` | Xe hai bánh gắn động cơ. | Xe máy, xe tay ga, mô tô, xe máy điện. | Không gồm xe đạp không động cơ; không gộp người ngồi vào box xe. **Ca giáp ranh (`img_004`, `img_035`):** tuk-tuk / xe 3 bánh có cabin không nằm rõ trong `motorcycle` → tạm xếp `ignore_region` và hỏi reviewer. |
| `person` | Con người thật đang đứng, đi bộ hoặc ngồi/lái trên phương tiện. | Người đi bộ, người lái xe máy, người ngồi sau. | Không gồm tượng, ma-nơ-canh, hình in quảng cáo, bóng phản chiếu. |
| `ignore_region` | Vùng không gán từng vật (đám đông dày đặc, cụm vật `< 20 px`, hoặc tạm dùng cho ca ngoài taxonomy chờ chốt). | Đám đông xa, bãi xe xa chồng lấn, tạm phủ tuk-tuk (`img_004`, `img_035`) / bus (`img_009`). | Không dùng cho 1–2 vật thuộc 5 lớp chính nhìn rõ và cao ≥ 20 px. |

- **Định nghĩa & hướng xử lý các ca ngoài 5 lớp / giáp ranh (cần hỏi reviewer ở Pha 2):**
  1. **Tuk-tuk / xe 3 bánh (`img_004`, `img_035`):** Phương tiện 3 bánh có mái che/cabin chở khách. Không có trong 5 lớp gốc v0 → **tạm xếp `ignore_region`** để tránh người gán `motorcycle`, người gán `car`; đề xuất họp Pha 2 chốt gộp vào `motorcycle` hoặc thêm lớp mới (`tuktuk`).
  2. **Xe buýt (`img_009`):** Xe chở khách cỡ lớn (> 24 chỗ, thân dài hơn hẳn `van`). Nằm ngoài 5 lớp gốc v0 → **không gán nhầm sang `van`/`truck`**, tạm xếp `ignore_region` và đề xuất họp Pha 2 thêm lớp `bus` (hoặc giữ `ignore_region` nếu bài toán không cần).
  3. **Xe bán tải có nắp thùng cao (`img_037`):** Xe pickup có khung gầm/cabin bán tải nhưng phía sau lắp nắp thùng kín cao ngang nóc. Nằm giữa `truck` và `van` → đề xuất giữ **`truck`** (theo bản chất xe bán tải), nhưng đưa ra họp Pha 2 chốt 1 quy tắc duy nhất (`truck` hoặc `van`).

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
4. **Phân biệt "Ca loại theo quy tắc" vs "Ca cần hỏi reviewer khi họp nhóm":**
   - **Ca LOẠI / XỬ LÝ NGAY theo quy tắc** *(tiêu chí đã rõ, không cần hỏi họp)*:
     1. Vật đơn lẻ có chiều cao **< 20 px** → bỏ qua không gán.
     2. Vật không phải thực thể giao thông thật (**tượng, ma-nơ-canh, đồ chơi/mô hình, hình in, ảnh phản chiếu qua gương**) → loại, không gán.
     3. Vật bị che khuất một phần nhưng vẫn nhận diện chắc chắn lớp và cao ≥ 20 px → gán phần nhìn thấy với `occluded_level = 1`.
   - **Ca CẦN HỎI REVIEWER trong cuộc họp nhóm Pha 2** *(nằm ngoài/giáp ranh taxonomy `v0`, dễ hiểu 2 kiểu)*:
     1. **Xe chở xe (`img_002`):** Chỉ gán `truck` hay gán thêm từng `car` trên thùng?
     2. **Phương tiện ngoài 5 lớp gốc (`img_004, img_009, img_035, img_037`):** Tuk-tuk, xe buýt, bán tải nắp thùng cao → gom lớp nào, `ignore_region`, hay thêm lớp mới?
     3. **Hình mờ chuyển động (`img_014`) & Đám đông dày (`img_021, img_030`):** Ngưỡng mờ tối đa được gán và ranh giới khi nào dừng tách box chuyển sang `ignore_region`?

## 4. Ca khó
| Ảnh | Tình huống | Phân loại | Quyết định đề xuất | Lý do |
|---|---|---|---|---|
| `img_002` | Xe tải chở nhiều ô tô trên thùng | Hỏi reviewer | Chỉ gán xe chở (`truck`), bỏ xe trên thùng | Xe bị chở không tự lưu thông; gán dễ làm rối mô hình |
| `img_004`, `img_035` | Tuk-tuk / xe 3 bánh | Hỏi reviewer | Tạm xếp `ignore_region` (đề xuất họp chốt `motorcycle` hoặc thêm lớp) | Không có trong 5 lớp gốc v0, dễ lệch lớp giữa người gán |
| `img_009`, `img_037` | Xe buýt / bán tải nắp thùng cao | Hỏi reviewer | Bus: hỏi nhóm thêm lớp hoặc `ignore_region`; Bán tải nắp cao: xếp `van` hay `truck` | Dễ nhầm ranh giới `car` / `van` / `truck` |
| `img_011`, `img_017`, `img_027`, `img_033`, `img_038` | Tượng, ma-nơ-canh, xe giả tưởng/mô hình | Loại theo quy tắc | Không gán | Không phải người/phương tiện thật tham gia giao thông |
| `img_020` | Hình phản chiếu qua gương chiếu hậu | Loại theo quy tắc | Không gán vật trong gương | Là ảnh ảo phản chiếu, gán sẽ dạy sai ngữ cảnh không gian |
| `img_006`, `img_008` | Nhiều vật thể, bị che khuất, ánh sáng tối | Quy tắc + Hỏi | Gán phần nhìn thấy ≥ 20 px, gắn `occluded_level = 1` | Che khuất nhau nhiều nhưng vẫn nhận diện được lớp |
| `img_014` | Người đi bộ bị mờ (motion blur) | Hỏi reviewer | Gán `person` phần nhìn thấy, tick `can_review` | Biên vật mờ dễ gây lệch IoU < 0.85 |
| `img_021`, `img_030` | Đám đông xe máy dày đặc, vật `< 20 px` | Quy tắc + Hỏi | Tách xe/người rõ ở tiền cảnh (`occluded_level = 1`); cụm chồng lấn/`< 20 px` phía sau → `ignore_region` | Mật độ quá dày, gán hết dễ bỏ sót và IoU thấp |

## 5. QC và phiên bản
- Ngưỡng QC (`taxonomy.json`): IoU TB ≥ 0.85, đồng thuận lớp ≥ 95%, tỉ lệ ảnh lỗi ≤ 2%.
- Ca chưa chốt khi gán Pha 3: tick `can_review = true`, không tự ý sửa guideline trước Pha 5.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 → v0.1 | Bổ sung ngưỡng % `occluded_level`, quy tắc tách người/xe máy, ngưỡng `< 20 px`, phân loại ca loại vs ca hỏi reviewer | Vá các chỗ mơ hồ của `v0` trước khi họp Pha 2 |
