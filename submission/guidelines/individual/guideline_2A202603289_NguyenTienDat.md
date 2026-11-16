# Guideline gán nhãn Bounding Box – Phiên bản cá nhân

**Phiên bản:** v1 (cá nhân)  
**Loại nhãn:** Bounding box  
**Công cụ:** CVAT → COCO 1.0  
**Mục tiêu:** Phát hiện người và phương tiện trên ảnh đường phố (giao thông / xe tự lái).

---

## 1. Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa ngắn gọn |
|-----|---------------------|
| `car` | Ô tô con 4 bánh (sedan, hatchback, SUV, taxi). |
| `truck` | Xe tải, xe bán tải (pickup), xe chở xe. |
| `van` | Xe van / xe thùng kín cỡ nhỏ-trung. |
| `bus` | Xe buýt các loại. |
| `motorcycle` | Xe máy, scooter, mô tô, tuk-tuk / xe ba bánh. |
| `bicycle` | Xe đạp (có hoặc không có người ngồi). |
| `person` | Người (đi bộ, ngồi, đứng, lái xe, ngồi sau). |
| `ignore_region` | Vùng quá nhỏ, quá mờ, quá xa hoặc không thuộc các lớp trên. |

**Không gán:**
- Xe đồ chơi, mô hình, tượng, mannequin
- Biển hiệu, cột đèn, ghế, thùng rác, cây cối
- Hàng hóa trên xe (chỉ gán phương tiện mang chúng)

---

## 2. Thuộc tính (bắt buộc)

| Thuộc tính | Giá trị | Ý nghĩa |
|------------|---------|---------|
| `occluded_level` | `0` / `1` / `2` / `3` | 0 = rõ ràng<br>1 = che ≤ 30%<br>2 = che 30–70%<br>3 = che > 70% hoặc rất khó nhận |
| `truncated` | `no` / `yes` | `yes` nếu bị cắt bởi mép ảnh |
| `can_review` | tick / không | Tick khi không chắc chắn về lớp hoặc mức che |

---

## 3. Quy tắc vẽ box

1. Gán tất cả người và phương tiện thuộc các lớp trên (kể cả nhỏ hoặc hơi xa nếu còn nhận ra).
2. Box ôm sát vật, không thừa nền nhiều, không cắt mất phần quan trọng (bánh xe, đầu người…).
3. Một vật = một box. Không gộp nhiều xe thành một.
4. Người ngồi trên xe máy / tuk-tuk / xe đạp → gán riêng `person` + gán phương tiện tương ứng.
5. Xe chồng lên nhau (xe trên xe chở xe, xe máy đỗ dày) → gán từng chiếc, dùng `occluded_level` phù hợp.
6. Vật bị cắt mép ảnh → vẫn gán + `truncated = yes`.
7. Ảnh mờ / chuyển động nhẹ → vẫn gán nếu còn nhận diện được.
8. Hàng hóa trên xe **không** gán riêng.

---

## 4. Ca khó thường gặp

| Tình huống | Cách xử lý |
|------------|------------|
| Tuk-tuk / xe ba bánh | `motorcycle` |
| Xe bán tải (pickup) | `truck` |
| Xe chở xe (car carrier) | `truck` + từng `car` trên đó |
| Người đội mũ / khẩu trang / áo phản quang | Vẫn `person` |
| Người ngồi sau xe máy | 2 box `person` riêng |
| Xe máy / ô tô đỗ dày, che nhau | Gán những chiếc thấy ≥ 30%, dùng `occluded_level` 1–2 |
| Xe rất xa / rất nhỏ | `ignore_region` hoặc tick `can_review` |
| Ảnh đêm / mưa / đường ướt | Vẫn gán bình thường nếu nhận ra |
| Xe đạp + người | Gán cả `bicycle` và `person` |
| Tượng / mannequin / xe mô hình | Không gán |

---

## 5. QC nhanh

- Đã gán hết người + phương tiện rõ ràng chưa?
- Box có ôm sát không?
- Lớp đúng chưa (đặc biệt `truck` / `van` / `car`, `motorcycle` / tuk-tuk)?
- Đã điền `occluded_level` và `truncated` chưa?
- Chỗ phân vân đã tick `can_review` chưa?

---

**Ghi chú nhóm:**  
Khi tổng hợp 4 người cần thống nhất thêm:
- Có giữ `bicycle` và `bus` không?
- Tuk-tuk có tách thành lớp riêng không?
- Ngưỡng kích thước tối thiểu để gán (ví dụ < 20px → ignore).
