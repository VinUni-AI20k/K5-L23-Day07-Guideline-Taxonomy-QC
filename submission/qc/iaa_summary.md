# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 4
- Lượt gán đủ **80/80**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 295 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 40 | 295 | 0.969 | 98.0% | 92.2% | 92.5% | 102/37 | 1 | ĐẠT |
| 101|102 | 10 | 41 | 0.999 | 92.7% | 82.9% | 85.4% | 2/0 | 1 | CHƯA ĐẠT |
| 101|104 | 10 | 102 | 0.992 | 97.1% | 100.0% | 100.0% | 77/0 | 0 | ĐẠT |
| 102|103 | 10 | 74 | 0.950 | 100.0% | 78.4% | 87.8% | 6/24 | 0 | ĐẠT |
| 103|104 | 10 | 78 | 0.942 | 100.0% | 100.0% | 91.0% | 17/13 | 0 | ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 230 ({'bo_sot_thua': 125, 'sai_lop': 6, 'iou_thap': 24, 'sai_thuoc_tinh': 42, 'bat_dong_ignore': 27, 'co_can_review': 6}), trên 32 ảnh cần calibration.
