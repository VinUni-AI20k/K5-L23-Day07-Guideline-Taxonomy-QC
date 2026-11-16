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
| `truck` | Xe chở hàng có thùng tách rời hoặc thùng hở (gồm cả xe bán tải/pickup và bán tải gắn nắp thùng cao). | Xe tải thùng, xe ben, pickup thùng hở, bán tải nắp thùng cao (`img_037`). | Không gồm xe tải van kín liền thân (`van`). |
| `van` | Xe thùng kín liền thân cỡ nhỏ/trung chở hàng hoặc chở khách kiểu minibus. | Xe van giao hàng, xe khách 16 chỗ. | Không gồm SUV/MPV gia đình (`car`), bán tải nắp thùng cao (`truck`), hay xe buýt cỡ lớn (`bus`). |
| `bus` | Xe chở khách cỡ lớn (> 24 chỗ) thân dài liền khối. | Xe buýt nội đô, xe khách lớn (`img_009`). | Không gồm xe khách 16 chỗ/minibus (`van`). |
| `motorcycle` | Xe hai bánh gắn động cơ. | Xe máy, xe tay ga, mô tô, xe máy điện. | Không gồm xe đạp không động cơ, không gồm tuk-tuk/xe 3 bánh (`tuktuk`), không gộp người ngồi vào box xe. |
| `tuktuk` | Xe 3 bánh gắn động cơ có mái che hoặc cabin chở khách/hàng. | Xe tuk-tuk, xe lam 3 bánh (`img_004`, `img_035`). | Không gồm xe máy 2 bánh (`motorcycle`), không gồm xích lô đạp không động cơ. |
| `person` | Con người thật đang đứng, đi bộ hoặc ngồi/lái trên phương tiện. | Người đi bộ, người lái xe máy, người ngồi sau. | Không gồm tượng, ma-nơ-canh, hình in quảng cáo, bóng phản chiếu. |
| `ignore_region` | Vùng không gán từng vật: đám đông dày đặc hoặc cụm vật quá nhỏ (`< 20 px`). | Đám đông xa, bãi xe xa chồng lấn. | Không dùng cho 1–2 vật thuộc các lớp trên nhìn rõ và cao ≥ 20 px. |

- **Quy tắc định nghĩa cho các ca mở rộng / giáp ranh:**
  1. **Tuk-tuk / xe 3 bánh (`img_004`, `img_035`):** Gán lớp **`tuktuk`** (tách riêng khỏi `motorcycle` vì có 3 bánh và cabin/mái che; người lái/khách ngồi bên trong nếu thấy rõ vẫn gán `person`).
  2. **Xe buýt (`img_009`):** Gán lớp **`bus`** (tách riêng khỏi `van` do kích thước lớn > 24 chỗ).
  3. **Xe bán tải nắp thùng cao (`img_037`):** Gán lớp **`truck`** (xe pickup có cabin bán tải phía trước và thùng lắp nắp kín cao ngang nóc phía sau, giữ nhất quán theo dòng bán tải).

### Thuộc tính
| Thuộc tính | Giá trị | Nghĩa từng mức & Ngưỡng đo được |
|---|---|---|
| `occluded_level` | `0` | Không bị che (`0%` diện tích bị vật khác che). |
| | `1` | Có bị che (`> 0%` diện tích bị vật khác che khuất nhưng vẫn nhận diện được vật). |
| `truncated` | `no` | Vật nằm trọn trong khung ảnh, không bị cạnh ảnh cắt. |
| | `yes` | Một phần thân vật bị cắt trực tiếp bởi ít nhất 1 cạnh khung ảnh. |
| `can_review` | `false` / `true` | Tick `true` khi ca mơ hồ chưa có quy tắc, để đưa ra họp calibration. |

## 3. Quy tắc vẽ box
| Rule ID | Tên quy tắc | Nội dung quy tắc |
|---|---|---|
| `R-01` | **Ôm sát phần nhìn thấy** | Box khít rìa ngoài cùng phần nhìn thấy của vật; không đoán vẽ ra ngoài vùng bị che khuất hoặc ngoài mép ảnh. Bị che > 0% gắn `occluded_level = 1`; chạm/cắt mép ảnh gắn `truncated = yes`. |
| `R-02` | **Tách người đi xe máy** | Tách riêng **1 box `motorcycle`** (chỉ ôm bánh, khung, tay lái, gương, yếm) + **1 box `person`** cho mỗi người ngồi trên xe (từ đỉnh đầu/mũ tới hết chân). *(Kiểm thử chéo: đạt trên `img_005` cận cảnh và `img_006` góc xa).* |
| `R-03` | **Ngưỡng tối thiểu `< 20 px`** | Vật đơn lẻ cao `< 20 px` → **loại theo quy tắc** (không gán). Cụm nhiều vật `< 20 px` tụ lại → khoanh 1 box `ignore_region`. |
| `R-04` | **Loại vật không thật** | Tượng, ma-nơ-canh, đồ chơi/xe mô hình giả tưởng, hình in trên biển/thân xe, ảnh phản chiếu qua gương → **loại theo quy tắc** (không gán). |
| `R-05` | **Xe chở xe** | Chỉ gán box cho xe chở (`truck`); không gán các xe đang nằm trên thùng chở. |
| `R-06` | **Lớp mở rộng & giáp ranh** | Tuk-tuk / xe 3 bánh có mái che → `tuktuk`; xe khách lớn > 24 chỗ → `bus`; xe bán tải nắp thùng cao → `truck`. |
| `R-07` | **Đám đông chồng lấn** | Tách box từng vật nhìn rõ ở tiền cảnh (`≥ 20 px`); cụm chồng lấn dày đặc phía sau không tách được ranh giới → khoanh 1 `ignore_region`. |
| `R-08` | **Cần hỏi reviewer (`can_review`)** | Tick `can_review = true` đối với vật chuyển động bị mờ nặng không rõ biên (`img_014`) hoặc cụm đám đông lưỡng lự giữa tách box với `ignore_region`. |

- **Tóm tắt phân biệt:** **Loại / Xử lý ngay theo quy tắc** (`R-01` → `R-07`) vs **Cần hỏi reviewer** (`R-08`).

## 4. Ca khó
| Ảnh | Tình huống | Rule ID | Phân loại | Quyết định | Lý do |
|---|---|---|---|---|---|
| `img_002` | Xe tải chở nhiều ô tô trên thùng | `R-05` | Theo quy tắc | Chỉ gán xe chở (`truck`), bỏ xe trên thùng | Xe bị chở không tự lưu thông; gán dễ làm rối mô hình |
| `img_004`, `img_035` | Tuk-tuk / xe 3 bánh | `R-06` | Theo quy tắc | Gán `tuktuk` | Tách lớp riêng cho phương tiện 3 bánh có cabin/mái che, tránh lẫn với `motorcycle` và `car` |
| `img_009` | Xe buýt cỡ lớn | `R-06` | Theo quy tắc | Gán `bus` | Xe chở khách > 24 chỗ kích thước lớn, tách riêng khỏi `van` |
| `img_037` | Xe bán tải có nắp thùng cao | `R-06` | Theo quy tắc | Gán `truck` | Bản chất là xe bán tải (pickup), chỉ gắn thêm nắp thùng |
| `img_011`, `img_017`, `img_027`, `img_033`, `img_038` | Tượng, ma-nơ-canh, xe giả tưởng/mô hình | `R-04` | Loại theo quy tắc | Không gán | Không phải người/phương tiện thật tham gia giao thông |
| `img_020` | Hình phản chiếu qua gương chiếu hậu | `R-04` | Loại theo quy tắc | Không gán vật trong gương | Là ảnh ảo phản chiếu, gán sẽ dạy sai ngữ cảnh không gian |
| `img_006`, `img_008` | Nhiều vật thể, bị che khuất, ánh sáng tối | `R-01`, `R-02`, `R-03` | Theo quy tắc | Gán phần nhìn thấy ≥ 20 px, gắn `occluded_level = 1` | Che khuất nhau nhiều nhưng vẫn nhận diện được lớp |
| `img_014` | Người đi bộ bị mờ (motion blur) | `R-01`, `R-08` | Hỏi reviewer | Gán `person` phần nhìn thấy, tick `can_review` | Biên vật mờ dễ gây lệch IoU < 0.85 |
| `img_021`, `img_030` | Đám đông xe máy dày đặc, vật `< 20 px` | `R-03`, `R-07`, `R-08` | Quy tắc + Hỏi | Tách xe/người rõ ở tiền cảnh (`occluded_level = 1`); cụm chồng lấn/`< 20 px` phía sau → `ignore_region` | Mật độ quá dày, gán hết dễ bỏ sót và IoU thấp |

## 5. QC và phiên bản
- Ngưỡng QC (`taxonomy.json`): IoU TB ≥ 0.85, đồng thuận lớp ≥ 95%, tỉ lệ ảnh lỗi ≤ 2%.
- Ca chưa chốt khi gán Pha 3: tick `can_review = true`, không tự ý sửa guideline trước Pha 5.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 → v0.1 | Bổ sung ngưỡng % `occluded_level`, quy tắc tách người/xe máy, ngưỡng `< 20 px`, phân loại ca loại vs ca hỏi reviewer | Vá các chỗ mơ hồ của `v0` trước khi họp Pha 2 |
