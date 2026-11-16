# Guideline gán nhãn Bounding Box – Phiên bản cá nhân

**Phiên bản:** v0 (cá nhân)  
**Loại nhãn:** Bounding box  
**Công cụ:** CVAT → xuất COCO 1.0  

## 1. Mục tiêu

Guideline này dùng để gán nhãn bounding box cho bài toán **phát hiện người và phương tiện** trên ảnh đường phố.

Mục đích chính:
- Tạo dữ liệu huấn luyện cho mô hình object detection phục vụ camera giao thông hoặc xe tự lái.
- Đảm bảo các box được vẽ nhất quán, chính xác và có thể dùng được ở mức production.
- Xử lý tốt các tình huống thực tế thường gặp trên đường phố Việt Nam / Đông Nam Á (xe máy đông, che khuất nhiều, ánh sáng yếu, phương tiện đa dạng).

Chỉ gán những đối tượng thuộc các lớp được định nghĩa ở mục 2. Các đối tượng khác bỏ qua hoặc đưa vào `ignore_region` nếu cần.

---

## 2. Lớp (mỗi vật thuộc đúng một lớp)

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

## 3. Thuộc tính (bắt buộc)

| Thuộc tính | Giá trị | Ý nghĩa |
|------------|---------|---------|
| `occluded_level` | `0` / `1` / `2` / `3` | 0 = rõ ràng<br>1 = che ≤ 30%<br>2 = che 30–70%<br>3 = che > 70% hoặc rất khó nhận |
| `truncated` | `no` / `yes` | `yes` nếu bị cắt bởi mép ảnh |
| `can_review` | tick / không | Tick khi không chắc chắn về lớp hoặc mức che |

---

## 4. Quy tắc vẽ box (chi tiết)

### 4.1. Nguyên tắc chung
1. Gán **tất cả** người và phương tiện thuộc các lớp đã định nghĩa, kể cả khi đối tượng nhỏ hoặc ở xa, miễn là còn nhận diện được rõ ràng.
2. Box phải **ôm sát** đối tượng nhất có thể:
   - Không để thừa quá nhiều nền xung quanh.
   - Không được cắt mất các phần quan trọng (đầu người, bánh xe, thân xe…).
3. Mỗi đối tượng chỉ được gán **một box**. Không được gộp nhiều xe máy hoặc nhiều người vào cùng một box.
4. Thứ tự ưu tiên khi có nhiều lớp chồng lên nhau: gán đầy đủ từng đối tượng riêng biệt.

### 4.2. Quy tắc với người (`person`)
- Người đi bộ, đứng, ngồi, đang lái xe, ngồi sau xe máy đều phải được gán.
- Người đội mũ bảo hiểm, khẩu trang, áo phản quang, đội nón lá… vẫn gán bình thường là `person`.
- Người bị che khuất một phần vẫn gán, điền đúng mức `occluded_level`.
- Người chỉ lộ một phần rất nhỏ (ví dụ chỉ thấy đầu hoặc chân) → cân nhắc dùng `ignore_region` hoặc tick `can_review`.

### 4.3. Quy tắc với phương tiện
- Xe máy / tuk-tuk / xe đạp có người ngồi → gán **cả** phương tiện **và** từng người riêng.
- Xe bị chồng lên nhau (xe trên xe chở xe, xe máy đỗ dày đặc) → gán từng chiếc một, sử dụng `occluded_level` phù hợp.
- Xe bị cắt bởi mép ảnh → vẫn gán và đánh dấu `truncated = yes`.
- Hàng hóa, thùng hàng, ống sắt, túi đồ trên xe **không** được gán riêng, chỉ gán phương tiện.

### 4.4. Các trường hợp đặc biệt
- Ảnh bị mờ do chuyển động hoặc ánh sáng yếu: vẫn gán nếu còn nhận ra được hình dạng tổng thể.
- Ảnh đêm / mưa / đường ướt phản chiếu: vẫn gán bình thường.
- Đối tượng quá nhỏ hoặc quá xa khiến không chắc chắn về lớp → dùng `ignore_region` hoặc tick `can_review`.

---

## 5. Ca khó thường gặp

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

## 6. Quy trình QC 

Trước khi nộp bài, người gán nhãn phải tự kiểm tra theo checklist sau:

### 6.1. Kiểm tra độ đầy đủ
- [ ] Đã gán hết tất cả người nhìn thấy rõ trong ảnh chưa?
- [ ] Đã gán hết tất cả phương tiện thuộc các lớp chưa?
- [ ] Có bỏ sót xe máy / người ở góc ảnh hoặc phía xa không?

### 6.2. Kiểm tra chất lượng box
- [ ] Box có ôm sát đối tượng không? (không thừa nền quá nhiều)
- [ ] Box có bị cắt mất đầu người, bánh xe, thân xe không?
- [ ] Có bị gộp nhiều đối tượng vào một box không?

### 6.3. Kiểm tra lớp và thuộc tính
- [ ] Lớp có đúng không? (đặc biệt phân biệt `car` / `van` / `truck`, `motorcycle` / tuk-tuk)
- [ ] `occluded_level` đã điền đúng mức độ che khuất chưa?
- [ ] `truncated` đã đánh dấu đúng với các vật bị cắt mép ảnh chưa?
- [ ] Những chỗ còn phân vân đã tick `can_review` chưa?

### 6.4. Kiểm tra các ca đặc biệt
- [ ] Xe chở xe (car carrier) đã gán cả xe lớn và từng xe con chưa?
- [ ] Người ngồi sau xe máy đã được gán riêng chưa?
- [ ] Xe đạp đã được gán `bicycle` (nếu có trong danh sách lớp) chưa?

**Chỉ nộp khi tất cả các mục trên đều đạt.**


