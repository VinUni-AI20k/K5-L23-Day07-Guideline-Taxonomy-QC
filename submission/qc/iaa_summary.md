# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 4
- Lượt gán đủ **80/80**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 370 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 40 | 370 | 0.922 | 94.3% | 77.6% | 95.7% | 48/87 | 0 | CHƯA ĐẠT |
| 111|222 | 6 | 32 | 0.980 | 75.0% | 62.5% | 96.9% | 0/1 | 0 | CHƯA ĐẠT |
| 111|333 | 9 | 109 | 0.982 | 100.0% | 94.5% | 100.0% | 2/5 | 0 | ĐẠT |
| 111|444 | 5 | 57 | 0.844 | 98.2% | 77.2% | 86.0% | 10/20 | 0 | CHƯA ĐẠT |
| 222|333 | 5 | 50 | 0.985 | 92.0% | 94.0% | 94.0% | 1/6 | 0 | CHƯA ĐẠT |
| 222|444 | 9 | 82 | 0.878 | 98.8% | 58.5% | 98.8% | 26/21 | 0 | ĐẠT |
| 333|444 | 6 | 40 | 0.830 | 82.5% | 62.5% | 92.5% | 9/34 | 0 | CHƯA ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 399 ({'bo_sot_thua': 134, 'iou_thap': 62, 'sai_thuoc_tinh': 97, 'co_can_review': 74, 'bat_dong_ignore': 11, 'sai_lop': 21}), trên 32 ảnh cần calibration.
