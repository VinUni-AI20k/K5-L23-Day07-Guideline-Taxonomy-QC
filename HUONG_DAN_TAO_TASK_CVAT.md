# HƯỚNG DẪN CHIA ẢNH VÀ TỰ ĐỘNG TẠO TASK CVAT QUA TERMINAL (NHÓM T005)

Tài liệu này hướng dẫn chi tiết cách:
1. **Chia 40 ảnh cho 5 thành viên**, đảm bảo mỗi ảnh có **> 2 người gán** ($K = 3$ người gán độc lập/ảnh) và khối lượng công việc cân bằng đều 100%.
2. **Chạy câu lệnh Terminal** để tự động tạo Project/Task và upload đúng danh sách ảnh được phân công lên CVAT (không cần upload thủ công từng ảnh).
3. **Quy ước đặt tên file và kiểm tra nhãn** sau khi gán.

---

## 1. Danh Sách Thành Viên & Phân Bổ Công Việc

### 1.1. Danh sách thành viên (Đã chuẩn hóa MSSV & Họ tên)

| STT | MSHV | Họ và tên | Tên không dấu (<HoTen>) | File nhãn nộp |
|---|---|---|---|---|
| 1 | `2A202603040` | NGUYỄN ĐỨC CƯỜNG | `NguyenDucCuong` | `submission/labels/2A202603040_NguyenDucCuong.json` |
| 2 | `2A202603183` | HOÀNG NHẬT ANH | `HoangNhatAnh` | `submission/labels/2A202603183_HoangNhatAnh.json` |
| 3 | `2A202603192` | NGUYỄN BÁ DUY | `NguyenBaDuy` | `submission/labels/2A202603192_NguyenBaDuy.json` |
| 4 | `2A202603216` | ĐỖ HUY KIÊN | `DoHuyKien` | `submission/labels/2A202603216_DoHuyKien.json` |
| 5 | `2A202603240` | PHẠM MẠNH HÙNG | `PhamManhHung` | `submission/labels/2A202603240_PhamManhHung.json` |

---

### 1.2. Công thức chia ảnh thỏa mãn đề bài (> 2 người gán)

- **Số ảnh**: 40 ảnh (`img_001.jpg` đến `img_040.jpg`).
- **Số thành viên**: 5 người.
- **Yêu cầu đề bài**: Mỗi ảnh phải có **> 2 người gán** $\rightarrow$ chọn $K = 3$ người gán độc lập cho mỗi ảnh.
- **Tổng số lượt gán**:
  $$\text{Tổng lượt gán} = 40 \times 3 = 120 \text{ lượt}$$
- **Số ảnh mỗi người cần gán**:
  $$\text{Số ảnh / người} = \frac{120}{5} = 24 \text{ ảnh}$$

Mỗi thành viên được giao **chính xác 24 ảnh**. Mỗi ảnh trong 40 ảnh đều có **đúng 3 người gán**, đảm bảo độ phủ và tính toán độ đồng thuận (IAA - Inter-Annotator Agreement) chính xác.

---

## 2. Bước 1: Sinh Nhãn & Chia Việc Trong Terminal

Mở Terminal (hoặc PowerShell) tại thư mục gốc của project:

```bash
cd c:\Users\basduy05\Downloads\VINAI\lab\lab-day7\K5-L23-Day07-T005-Guideline-Taxonomy-QC
```

### 2.1. Sinh file nhãn cho CVAT từ taxonomy

```bash
python scripts/make_cvat_labels.py
```
*Lệnh này sinh file `cvat/labels_generated.json` chứa 6 lớp (`car`, `truck`, `van`, `motorcycle`, `person`, `ignore_region`) và các thuộc tính `occluded_level`, `truncated`, `can_review`.*

### 2.2. Chạy lệnh chia ảnh cho 5 thành viên

```bash
python scripts/split_assign.py --members 2A202603040,2A202603183,2A202603192,2A202603216,2A202603240 --copy-images
```

> **Kết quả sau khi chạy**:
> - Mỗi thành viên nhận đủ **24 ảnh**.
> - Danh sách ảnh của từng người được ghi tại: `submission/qc/assignments/<MSHV>.txt`.
> - Ảnh được copy tự động vào thư mục riêng: `work/<MSHV>/images/` (mỗi thư mục đúng 24 file ảnh).
> - File ma trận phân công: `submission/qc/assignment.csv`.

---

## 3. Bước 2: Tự Động Tạo Task Trên CVAT Bằng Terminal

Đã có script tự động: `scripts/create_cvat_task.py` (dùng thư viện `cvat-sdk` tích hợp sẵn). Script này tự động đọc danh sách ảnh từ `work/<MSHV>/images/` và gửi lên CVAT.

### Cách 1: Từng thành viên tự tạo Task cho tài khoản cá nhân (Khuyên dùng)

Mỗi bạn mở terminal và chạy lệnh tương ứng với MSHV của mình:

#### 1. Nguyễn Đức Cường (`2A202603040`):
```bash
python scripts/create_cvat_task.py --mshv 2A202603040 --auth "username:password"
```

#### 2. Hoàng Nhật Anh (`2A202603183`):
```bash
python scripts/create_cvat_task.py --mshv 2A202603183 --auth "username:password"
```

#### 3. Nguyễn Bá Duy (`2A202603192`):
```bash
python scripts/create_cvat_task.py --mshv 2A202603192 --auth "username:password"
```

#### 4. Đỗ Huy Kiên (`2A202603216`):
```bash
python scripts/create_cvat_task.py --mshv 2A202603216 --auth "username:password"
```

#### 5. Phạm Mạnh Hùng (`2A202603240`):
```bash
python scripts/create_cvat_task.py --mshv 2A202603240 --auth "username:password"
```

*(Thay `username:password` bằng tài khoản CVAT của bạn. Nếu không truyền `--auth`, terminal sẽ tự hỏi username và mật khẩu ẩn).*

---

### Cách 2: Một người đại diện tạo sẵn cả 5 Task cho cả nhóm

Nếu nhóm dùng chung một tài khoản CVAT hoặc server CVAT của trường:

```bash
python scripts/create_cvat_task.py --all --project-name "Day07_T005" --auth "username:password"
```

*Lệnh trên sẽ tự động:*
1. Tạo 1 Project mới có tên `Day07_T005` với đầy đủ bộ nhãn chuẩn từ `cvat/labels_generated.json`.
2. Tạo 5 Task tương ứng (`day07-2A202603040`, `day07-2A202603183`, ...).
3. Upload chính xác 24 ảnh vào từng Task.
4. In ra các đường link trực tiếp (URL) để từng người bấm vào là gán nhãn được ngay!

---

### Cách 3: Tạo Task gắn vào một Project đã có sẵn

Nếu bạn đã có sẵn Project trên CVAT (ví dụ Project ID là `12345`):

```bash
python scripts/create_cvat_task.py --mshv 2A202603192 --project-id 12345 --auth "username:password"
```

---

## 4. Bước 3: Gán Nhãn & Export Dữ Liệu Sau Khi Hoàn Thành

### 4.1. Thực hiện gán nhãn trên CVAT
- Mở link task do script in ra (ví dụ: `https://app.cvat.ai/tasks/123456`).
- Vẽ bounding box theo đúng quy tắc của nhóm trong `guideline_v1.0_agreed.md`.
- Nhớ điền đủ thuộc tính: `occluded_level`, `truncated`, `can_review`.
- Với vùng quá đông hoặc quá nhỏ (< 20px): gán lớp `ignore_region`.

### 4.2. Export nhãn ra file COCO 1.0
1. Trên giao diện Task CVAT: bấm menu **Actions → Export task dataset**.
2. Chọn định dạng: **COCO 1.0**.
3. **Bỏ chọn (Tắt)** ô `Save images`.
4. Bấm **Export** $\rightarrow$ tải file `.zip` về máy.
5. Giải nén file `.zip`, lấy file `annotations/instances_default.json`.
6. Đổi tên file và lưu vào thư mục `submission/labels/`:

| Thành viên | Tên file xuất cần lưu vào repo |
|---|---|
| Nguyễn Đức Cường | `submission/labels/2A202603040_NguyenDucCuong.json` |
| Hoàng Nhật Anh | `submission/labels/2A202603183_HoangNhatAnh.json` |
| Nguyễn Bá Duy | `submission/labels/2A202603192_NguyenBaDuy.json` |
| Đỗ Huy Kiên | `submission/labels/2A202603216_DoHuyKien.json` |
| Phạm Mạnh Hùng | `submission/labels/2A202603240_PhamManhHung.json` |

---

## 5. Bước 4: Kiểm Tra Tính Hợp Lệ Của Nhãn

Sau khi đã lưu file JSON vào `submission/labels/`, chạy lệnh sau để kiểm tra tự động:

```bash
python scripts/validate_labels.py --all
```

Nếu màn hình báo kết quả không có lỗi (0 ERROR), nhãn của bạn đã hoàn toàn hợp lệ và sẵn sàng cho các bước tính toán độ đồng thuận IAA (`scripts/qc_compare.py`).
