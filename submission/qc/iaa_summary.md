# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 5
- Lượt gán đủ **120/120**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 689 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 120 | 689 | 0.846 | 98.3% | 53.4% | 85.9% | 167/381 | 0 | CHƯA ĐẠT |
| 034|048 | 13 | 45 | 0.857 | 100.0% | 100.0% | 100.0% | 30/22 | 0 | ĐẠT |
| 034|070 | 12 | 68 | 0.820 | 100.0% | 25.0% | 72.1% | 43/31 | 0 | CHƯA ĐẠT |
| 034|344 | 12 | 91 | 0.910 | 98.9% | 71.4% | 72.5% | 10/52 | 0 | ĐẠT |
| 034|354 | 11 | 67 | 0.845 | 95.5% | 35.8% | 76.1% | 12/43 | 0 | CHƯA ĐẠT |
| 048|070 | 13 | 80 | 0.819 | 100.0% | 33.8% | 90.0% | 11/30 | 0 | CHƯA ĐẠT |
| 048|344 | 11 | 51 | 0.878 | 96.1% | 76.5% | 74.5% | 10/45 | 0 | ĐẠT |
| 048|354 | 11 | 37 | 0.806 | 100.0% | 59.5% | 83.8% | 2/49 | 0 | CHƯA ĐẠT |
| 070|344 | 11 | 73 | 0.843 | 97.3% | 37.0% | 89.0% | 9/46 | 0 | CHƯA ĐẠT |
| 070|354 | 12 | 66 | 0.841 | 98.5% | 60.6% | 98.5% | 11/38 | 0 | CHƯA ĐẠT |
| 344|354 | 14 | 111 | 0.829 | 97.3% | 55.9% | 99.1% | 29/25 | 0 | CHƯA ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 1389 ({'bo_sot_thua': 393, 'co_can_review': 91, 'iou_thap': 252, 'sai_thuoc_tinh': 372, 'bat_dong_ignore': 269, 'sai_lop': 12}), trên 38 ảnh cần calibration.
