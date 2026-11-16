# HƯỚNG DẪN TỰ ĐỘNG PHÂN VIỆC & TẠO TASK TRÊN CVAT (NHÓM T005)

Script `scripts/setup_cvat.py` đã được nâng cấp toàn diện, **hỗ trợ linh hoạt cả 3 hình thức máy chủ CVAT**:
1. **CVAT Cloud:** `https://app.cvat.ai` (máy nào cũng vào được).
2. **CVAT Local:** `http://localhost:8080` (nhập username và password của máy local).
3. **Tự nhập đường dẫn link tùy chọn:** Tự gõ IP máy chủ của nhóm (ví dụ `http://192.168.1.15:8080`, máy chủ phòng lab, v.v.).

---

## 1. Bảng Câu Lệnh Cho Từng Thành Viên Nhóm T005

Mỗi bạn mở Terminal tại thư mục của repo và chạy đúng câu lệnh của mình:

| Thành viên | Mã sinh viên | Câu lệnh chạy Terminal |
|:---|:---:|:---|
| **NGUYỄN ĐỨC CƯỜNG** | `2A202603040` | `python scripts/setup_cvat.py "NGUYỄN ĐỨC CƯỜNG" 2A202603040` |
| **HOÀNG NHẬT ANH** | `2A202603183` | `python scripts/setup_cvat.py "HOÀNG NHẬT ANH" 2A202603183` |
| **NGUYỄN BÁ DUY** | `2A202603192` | `python scripts/setup_cvat.py "NGUYỄN BÁ DUY" 2A202603192` |
| **ĐỖ HUY KIÊN** | `2A202603216` | `python scripts/setup_cvat.py "ĐỖ HUY KIÊN" 2A202603216` |
| **PHẠM MẠNH HÙNG** | `2A202603240` | `python scripts/setup_cvat.py "PHẠM MẠNH HÙNG" 2A202603240` |

---

## 2. Menu Lựa Chọn Máy Chủ & Đăng Nhập Khi Chạy Lệnh

Ngay khi gõ câu lệnh trên, Terminal sẽ hiện menu để bạn chọn máy chủ:

```text
============================================================
          CHỌN MÁY CHỦ CVAT BẠN MUỐN KẾT NỐI
============================================================
  [1] CVAT Cloud (https://app.cvat.ai)  [Mặc định]
  [2] CVAT Local máy này (http://localhost:8080)
  [3] Tự nhập đường dẫn link CVAT (URL tùy chọn / LAN / IP máy khác)
============================================================
Nhập lựa chọn của bạn (1, 2 hoặc 3) [mặc định 1]:
```

### 👉 LỰA CHỌN 1: Nếu chọn [1] - CVAT Cloud (`https://app.cvat.ai`)
* Terminal hỏi tài khoản `app.cvat.ai`:
  * Nếu đăng ký trực tiếp bằng Email/Pass: Chọn `[1]` và nhập Email + Mật khẩu.
  * Nếu đăng nhập qua Google: Chọn `[2]` và dán chuỗi **Personal Access Token** (Lấy tại `https://app.cvat.ai` $\rightarrow$ Avatar góc phải $\rightarrow$ Profile $\rightarrow$ Personal access tokens).

### 👉 LỰA CHỌN 2: Nếu chọn [2] - CVAT Local (`http://localhost:8080`)
* Terminal sẽ hỏi **Username** và **Password** trên CVAT Local:
  * Bạn nhập Username và Password tài khoản local của mình.
  * *(Nếu chạy trên máy chủ host của bạn Duy: có thể nhấn Enter để dùng tài khoản mặc định `basduy05`)*.

### 👉 LỰA CHỌN 3: Nếu chọn [3] - Tự nhập đường dẫn link máy chủ tùy chọn
* Terminal sẽ yêu cầu bạn dán link máy chủ:
  ```text
  Nhập đường dẫn link máy chủ CVAT (VD: http://192.168.1.15:8080):
  ```
* Sau đó nhập tiếp **Username** và **Password** tương ứng của máy chủ đó!

---

## 3. Chạy Nhanh Một Dòng Lệnh Không Cần Hỏi (Dành cho thành thạo)

Bạn có thể truyền thẳng các tham số `--server` và `--auth` vào lệnh:

```bash
# Ví dụ 1: Chạy thẳng trên CVAT Local với tài khoản/mật khẩu
python scripts/setup_cvat.py "NGUYỄN BÁ DUY" 2A202603192 --server http://localhost:8080 --auth "admin:password"

# Ví dụ 2: Tự nhập đường dẫn link IP máy của bạn trong mạng LAN
python scripts/setup_cvat.py "HOÀNG NHẬT ANH" 2A202603183 --server http://192.168.1.15:8080 --auth "anh:123456"

# Ví dụ 3: Chạy thẳng trên CVAT Cloud với Email và Mật khẩu
python scripts/setup_cvat.py "ĐỖ HUY KIÊN" 2A202603216 --server https://app.cvat.ai --auth "kien@gmail.com:matkhau"
```

---

## 4. Kết Quả Sau Khi Tạo Task

Hệ thống sẽ:
1. Đảm bảo phân chia đúng **24 ảnh** của bạn từ `data/images/`.
2. Tạo Project `Day07_T005` (nếu chưa có).
3. Tạo Task `day07-<MSHV>-<HoTen>` và upload đúng 24 ảnh.
4. Trả về đường link:
   ```text
   🎉 TẠO TASK THÀNH CÔNG CHO: HOÀNG NHẬT ANH (2A202603183)!
     - Server   : https://app.cvat.ai (hoặc link bạn chọn)
     - Task ID  : 123456
     - Số ảnh   : 24 ảnh
     - Bấm vào link dưới đây để mở CVAT và gán nhãn ngay:
       👉 https://app.cvat.ai/tasks/123456 👈
   ```

---

## 5. Export Dữ Liệu & Kiểm Tra Sau Khi Gán Xong

1. **Export nhãn:** Vào giao diện Task $\rightarrow$ **Actions** $\rightarrow$ **Export task dataset** $\rightarrow$ Chọn **COCO 1.0** (bỏ tick *Save images*).
2. **Đổi tên:** Lấy file `instances_default.json` đổi tên thành `<MSHV>_<HoTen>.json` rồi bỏ vào thư mục `submission/labels/`:
   * `2A202603040_NguyenDucCuong.json`
   * `2A202603183_HoangNhatAnh.json`
   * `2A202603192_NguyenBaDuy.json`
   * `2A202603216_DoHuyKien.json`
   * `2A202603240_PhamManhHung.json`
3. **Kiểm tra tự động:**
   ```bash
   python scripts/validate_labels.py --all
   ```
