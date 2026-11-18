# Guideline gán nhãn — cá nhân
**MSHV:** 26A202603354  
**Họ tên:** Nguyễn Tiến Thịnh  
**Phiên bản:** v0.1 (cá nhân – Pha 1)  
**Loại nhãn:** bounding box (hộp chữ nhật) trên ảnh đường phố  
**Công cụ:** CVAT, xuất COCO 1.0

> Bản này viết độc lập ở Pha 1. Không sửa lại sau khi họp nhóm. Bản thống nhất sẽ nằm ở file khác.

---

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình phát hiện **người và phương tiện** trên ảnh đường phố (camera giao thông hoặc xe tự lái).

Chỉ gán những vật **thật**, có thể nhận diện được trong thực tế.  
Không gán hình in, phản chiếu, vật trưng bày trên kệ.

---

## 2. Lớp và thuộc tính

### 2.1. Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa | Ví dụ | Phản ví dụ / ca dễ nhầm |
|---|---|---|---|
| `car` | Ô tô con, SUV, sedan, hatchback | Toyota Vios, Honda Civic, Kia Morning, SUV | Bán tải, van, bus, container |
| `truck` | Xe tải thùng mở hoặc có thùng hàng riêng, không phải container | Xe tải nhẹ, xe ben, xe tải thùng mở | Bán tải nhỏ, container, van |
| `van` | Xe thùng kín cỡ nhỏ đến trung bình, bao gồm xe 16 chỗ | Xe tải kín, xe 16 chỗ | Minibus (xếp vào `bus`), xe khách lớn |
| `bus` | Xe khách, minibus, xe buýt | Minibus, xe buýt thành phố | Xe 16 chỗ (xếp vào `van`) |
| `motorcycle` | Xe máy, mô tô, scooter | Honda Wave, Yamaha Exciter, xe máy điện, scooter | Xe đạp, xe ba bánh (chưa chốt) |
| `container` | Xe container, xe kéo rơ-moóc container, xe chở xe nhiều tầng (car carrier) | Xe container, xe chở ô tô 2–3 tầng | Xe tải thường |
| `person` | Người (đi bộ hoặc ngồi trên bất kỳ phương tiện nào) | Người đi bộ, người ngồi trên xe máy, người trong ô tô (nếu nhìn thấy rõ) | Hình người in trên biển quảng cáo |
| `ignore_region` | Vùng không cần / không nên gán từng vật | Đám đông quá dày chỉ thấy đầu, vùng xa mờ >70%, biển quảng cáo có xe in sẵn, xe trưng bày trên kệ | — |

**Ghi chú về bán tải (pickup) — chưa chốt:**  
Muốn phân biệt 2 loại:
- Loại chở hàng nhỏ kiểu Suzuki 5 tạ
- Loại lớn hơn kiểu Ford

Hiện tại **chưa quyết định** xếp vào `truck` / `van` hay tách lớp mới. Cần họp nhóm.

**Ghi chú về xe ba bánh / tuk-tuk / xích lô máy — chưa chốt:**  
Chưa quyết định xếp vào `motorcycle`, `truck` hay `ignore_region`.

### 2.2. Thuộc tính

| Thuộc tính | Giá trị | Ý nghĩa & ngưỡng đo được |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | **0**: nhìn thấy ≥ 90%<br>**1**: bị che 10–40%<br>**2**: bị che 40–70%<br>**3**: bị che >70% nhưng vẫn nhận diện được (chủ yếu áp dụng cho xe) |
| `truncated` | `no`, `yes` | Vật bị cắt bởi mép ảnh. Chỉ vẽ phần nhìn thấy. |
| `can_review` | tick / không | Tick khi không chắc, để người khác xem lại. |

**Quy tắc đặc biệt về mức che:**
- **Người**: nếu bị che khoảng ≥ 80% → **không gán**.
- **Xe**: nếu bị che khoảng 80% nhưng phần còn lại có tỷ lệ đoán được cao → vẫn gán và đặt `occluded_level = 3`.

---

## 3. Quy tắc vẽ box

1. Gán box cho mọi người và phương tiện thỏa điều kiện trong mục 2.
2. Box **ôm sát** vật (không để khoảng trống lớn, không cắt mất phần quan trọng của vật).
3. **Người ngồi trên xe**: vẫn gán `person` riêng (bao gồm cả mũ bảo hiểm nếu nhìn thấy).
4. **Vật bị cắt mép ảnh (`truncated = yes`)**:
   - Chỉ vẽ phần nhìn thấy.
   - Trường hợp người:
     - Nếu chỉ còn nửa thân dưới và vẫn đoán được là người → vẽ full box theo tỷ lệ cơ thể ước lượng.
     - Nếu chỉ còn từ eo trở lên → chỉ vẽ phần nhìn thấy.
5. **Không gán** các trường hợp sau:
   - Hình in trên biển quảng cáo, poster, màn hình LED.
   - Phản chiếu trên kính, gương chiếu hậu, mặt nước.
   - Xe / người trong gương chiếu hậu.
   - Xe trưng bày trên kệ / giá để hàng.
6. **Ảnh bị motion blur**:
   - Nếu mờ đến mức tỷ lệ đoán được < 50% → dùng `ignore_region`.
   - Nếu vẫn đoán được ≥ 50% → vẫn gán bình thường.
7. Kích thước tối thiểu: giữ nguyên theo taxonomy hiện tại (`min_box_height_px = 20`). Nếu vật nhỏ hơn và không nhận diện rõ thì không gán.
8. Đám đông quá dày đặc (chỉ nhìn thấy đầu) hoặc vùng xa mờ >70% → dùng `ignore_region`, không gán từng người/xe.

---

## 4. Ca khó

*(Phần này sẽ được bổ sung sau khi xem kỹ 40 ảnh. Các ca tiêu biểu cần ghi rõ ảnh, tình huống, quyết định và lý do.)*

| Ảnh | Tình huống | Quyết định của tôi | Lý do / ghi chú |
|---|---|---|---|
| img_002 | Xe chở xe nhiều tầng (car carrier) | Gán `container` | Theo quyết định đã chốt |
| img_020 | Xe / cảnh vật trong gương chiếu hậu | Không gán | Phản chiếu, không phải vật thật |
| | | | |
| | | | |
| | | | |

> Các ca còn lại sẽ được điền sau khi rà soát toàn bộ 40 ảnh. Những chỗ chưa chắc sẽ tick `can_review` và ghi chú.

---

## 5. QC và phiên bản

- Mọi thay đổi làm đổi cách gán nhãn đều tăng phiên bản guideline.
- Ca còn mơ hồ khi gán: tick `can_review` + ghi chú rõ ràng.
- Bản này là **bản cá nhân Pha 1**.  
  Sau khi họp nhóm sẽ có bản thống nhất `guideline_v1.0_agreed.md`.

### Lịch sử thay đổi (cá nhân)

| Phiên bản | Thay đổi chính | Lý do |
|---|---|---|
| v0 (starter) | Bản gốc của giảng viên | — |
| v0.1 (cá nhân) | Thêm lớp `bus`, `container`; làm rõ quy tắc che khuất, truncated, không gán hình in/phản chiếu; quy tắc đặc biệt cho người bị che ≥80% | Dựa trên quan sát 40 ảnh và quyết định cá nhân |

---

**Các điểm còn chưa chốt (cần họp nhóm):**
1. Phân loại chi tiết 2 loại bán tải (Suzuki 5 tạ vs Ford).
2. Xe ba bánh / tuk-tuk / xích lô máy.
3. Ranh giới chính xác giữa xe 16 chỗ (`van`) và minibus (`bus`).
4. Một số quy tắc truncated với người (cần ví dụ ảnh cụ thể để thống nhất).
