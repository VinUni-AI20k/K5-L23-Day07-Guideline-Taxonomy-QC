# Ghi chú cá nhân — 2A202603255 - Doãn Thị Phương Thảo

## 1. Pha 1: các ca cần chú ý khi gán nhãn

Dựa trên file `instances_default.json`, một số ảnh có tình huống đáng chú ý cần kiểm tra lại theo guideline:

| Ảnh | Tình huống thể hiện trong file nhãn | Điểm cần lưu ý khi rà soát |
|---|---|---|
| `img_002.jpg` | Có xe tải và nhiều ô tô | Phân biệt box của xe tải với từng ô tô; không gộp nhiều phương tiện thành một box nếu guideline yêu cầu gán riêng từng đối tượng. |
| `img_011.jpg` | Có nhiều người và một vùng `ignore_region` | Kiểm tra ranh giới giữa từng người và vùng không thể gán nhãn rõ ràng, tránh box chồng lấn không cần thiết. |
| `img_019.jpg` | Có nhiều người và một vùng `ignore_region` | Rà soát các đối tượng nhỏ/đông người và xác định đúng phạm vi vùng bỏ qua theo guideline. |
| `img_021.jpg` | Nhiều xe máy, trong đó có box bị cắt ở mép ảnh | Với đối tượng bị cắt bởi biên ảnh, cần giữ box theo phần nhìn thấy và đánh dấu `truncated` phù hợp. |
| `img_032.jpg` | Có số lượng box lớn nhất trong tập ảnh (24 box) | Kiểm tra đủ từng đối tượng, đặc biệt các người/xe ở gần nhau để tránh bỏ sót hoặc gán trùng. |

*Lưu ý: Bảng trên được rút ra từ cấu trúc và thuộc tính trong file JSON; cần đối chiếu ảnh gốc và guideline để xác nhận quyết định gán nhãn cuối cùng.*

## 2. Pha 2: những điểm cần đối chiếu với nhóm

File JSON cá nhân không chứa guideline phiên bản của từng thành viên hoặc kết quả họp calibration, vì vậy chưa thể kết luận chính xác điểm nào tôi khác nhóm. Các nội dung cần đối chiếu:

- **Người trên phương tiện:** kiểm tra nhóm có gán `person` cho người ngồi/lái trên xe hay chỉ gán người đi bộ.
- **Phương tiện ngoài các lớp phổ biến:** thống nhất cách xử lý `bus`, `bicycle`, `tuktuk` và các trường hợp không chắc chắn.
- **Vùng `ignore_region`:** thống nhất khi nào dùng vùng bỏ qua thay vì tạo box cho từng đối tượng.
- **Đối tượng bị che khuất hoặc cắt khỏi ảnh:** thống nhất cách điền `occluded_level` và `truncated`.

Sau khi có guideline nhóm và kết quả calibration, bổ sung quyết định cuối cùng và lý do đồng thuận/khác biệt tại đây.

## 3. Pha 3: ảnh tôi đã gán

- Có **24 ảnh** trong file, tổng cộng **187 bounding box**.
- Phân bố nhãn theo lớp:

| Lớp | Số box |
|---|---:|
| `person` | 84 |
| `motorcycle` | 44 |
| `car` | 33 |
| `truck` | 5 |
| `bus` | 5 |
| `bicycle` | 6 |
| `tuktuk` | 4 |
| `van` | 1 |
| `ignore_region` | 5 |
| **Tổng** | **187** |

- Ảnh có số box nhiều nhất là `img_032.jpg` với **24 box**.
- `img_033.jpg` không có annotation trong file JSON.
- Có **14 box** được đánh dấu `truncated = yes`.
- Có **1 box** được đánh dấu `can_review = true`.
- Với thuộc tính `occluded_level` được ghi nhận trong các annotation: mức `0` có 153 box, mức `1` có 11 box, mức `2` có 16 box và mức `3` có 2 box. 5 annotation không có trường `occluded_level` trong attributes.

## 4. Pha 4–5: tôi lệch ở đâu

Chưa có file kết quả IAA, bảng so sánh annotation giữa các thành viên hoặc biên bản calibration đi kèm, nên chưa thể xác định các trường hợp tôi gán khác nhóm.

Sau khi nhóm chạy IAA và họp calibration, bổ sung:
- Các ảnh/đối tượng có nhãn khác với đa số nhóm.
- Loại sai khác: bỏ sót đối tượng, sai class, box quá rộng/hẹp, xử lý che khuất/cắt biên chưa thống nhất.
- Quy tắc đã thống nhất sau calibration và những box cần sửa lại.

## 5. Dùng AI

- Sử dụng ChatGPT để hỗ trợ đọc/diễn giải yêu cầu bài lab, rà soát cấu trúc báo cáo và thống kê dữ liệu từ file JSON.
- Các thống kê trong mục 3 được tính trực tiếp từ `instances_default.json`.
- File JSON là kết quả export nhãn; bản thân file không cho biết công cụ AI có trực tiếp vẽ/chỉnh box hay không. Vì vậy, phần mô tả quy trình gán nhãn cần được bổ sung theo đúng những thao tác thực tế đã thực hiện trong CVAT.

## 6. Bài học

- Cần thống nhất cách xử lý các trường hợp người trên phương tiện, phương tiện ít gặp và `ignore_region` trước khi gán nhãn hàng loạt.
- Khi đối tượng bị che khuất hoặc nằm sát biên ảnh, cần kiểm tra đồng thời class, tọa độ box, `occluded_level` và `truncated`.
- Với ảnh đông đối tượng, nên rà soát lần lượt toàn ảnh để hạn chế bỏ sót hoặc tạo box trùng.
- Sau khi export, cần kiểm tra lại số ảnh, số annotation, phân bố class và các thuộc tính đặc biệt để phát hiện dữ liệu thiếu hoặc chưa nhất quán.

---

**Nguồn thống kê:** `instances_default.json` (COCO format), gồm 24 ảnh và 187 annotations.

**Các phần cần tự bổ sung sau khi đối chiếu thực tế:** quyết định cá nhân ở các ca khó, điểm khác biệt với nhóm, kết quả IAA/calibration và quy trình sử dụng AI/CVAT thực tế.
