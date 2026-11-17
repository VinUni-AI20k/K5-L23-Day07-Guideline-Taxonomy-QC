# Guideline gán nhãn — v0 (bản khởi đầu)

> **Đây là bản do giảng viên viết nhanh. Nó CHƯA đủ dùng.**
> Đừng sửa file này. Hãy copy sang `submission/guidelines/individual/` rồi sửa bản của bạn
> (xem `GUIDE.md`, Pha 1).

- Phiên bản: v0
- Ngày: 16/11/2026
- Người viết: Nguyễn Huy Thiên Hòa
---

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình phát hiện **người và phương tiện** trên ảnh đường phố
(ví dụ cho camera giao thông hoặc xe tự lái).

## 2. Lớp và thuộc tính

### Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa |
|---|---|
| `car` | Ô tô chở người như sedan, suv, taxi. |
| `truck` | Xe có thùng hàng hoặc thùng chuyên dụng tách khỏi cabin: xe tải, bán tải, xe bồn, xe trộn bê tông. |
| `van` | Xe thùng kín cỡ nhỏ. |
| `motorcycle` | Xe máy, mô tô hai bánh có động cơ. |
| `bike`| Xe đạp, không có động cơ|
| `person` | Người thật, người đi bộ, đứng, ngồi trên xe hở, người lái xe. |
| `ignore_region` | Vùng không cần gán từng vật. |
| `cyclo`| Xích lô chở người. |
| `motorized three-wheeler cart` | Xe ba bánh có động cơ dùng để chở hàng hóa |
| `tuk-tuk`| Xe ba bánh có động cơ dùng để chở người|

### Thuộc tính

| Thuộc tính | Giá trị | Ý nghĩa |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Mức bị che: 0 là thấy rõ, 1 là bị đối tượng khác che hoặc mép ảnh cắt, 2 là bị che hơn 80%, 3 là vật bị nhòe, mờ, tối. |
| `truncated` | `no`, `yes` | Vật bị cắt ở mép ảnh. |
| `can_review` | tick / không | Tick khi bạn không chắc, để người khác xem lại. |

## 3. Quy tắc vẽ box

1. Ôm sát phần nhìn thấy, không chừa nền, không cắt vào đối tượng.
2. Đối với người thì vẽ bao gồm cả các món đeo trên người như nón bảo hiểm, túi đeo, balo.
3. Đói với phương tiện thì vẽ từ điểm cao nhất của xe (nóc, mái, cần, gương) đến đáy bánh chạm đất, không vẽ bóng đổ.
4. Đối với người điều khiển ngồi trên xe hở thì tách ra 2 box : một cho người và một cho phương tiện.
5. Đối với người ngồi trong xe kín, chỉ thấy được qua cửa sổ : Không gán.
6. Vật thể quá nhỏ không gán.
7. Không gán phản chiếu, poster, mannequin, tượng, mô hình.
8. Với xe chở hàng, xe chở xe khác thì xem xe được chở như hàng, không phải xe.


## 4. Ca khó

(chưa có)

## 5. QC và phiên bản

- Mọi thay đổi làm đổi nhãn đều tăng phiên bản guideline.
- Ca mơ hồ: tick `can_review`.
