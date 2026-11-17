# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 5
- Lượt gán đủ **120/120**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 914 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 120 | 914 | 0.785 | 95.8% | 48.8% | 92.1% | 367/352 | 15 | CHƯA ĐẠT |
| 101|102 | 13 | 111 | 0.844 | 93.7% | 46.8% | 92.8% | 32/40 | 1 | CHƯA ĐẠT |
| 101|103 | 12 | 123 | 0.737 | 99.2% | 59.3% | 94.3% | 10/125 | 0 | CHƯA ĐẠT |
| 101|104 | 12 | 103 | 0.838 | 97.1% | 59.2% | 95.1% | 23/35 | 0 | CHƯA ĐẠT |
| 101|105 | 11 | 74 | 0.769 | 97.3% | 37.8% | 95.9% | 38/31 | 0 | CHƯA ĐẠT |
| 102|103 | 13 | 131 | 0.739 | 94.7% | 36.6% | 89.3% | 37/43 | 0 | CHƯA ĐẠT |
| 102|104 | 11 | 88 | 0.854 | 92.0% | 59.1% | 87.5% | 31/4 | 0 | CHƯA ĐẠT |
| 102|105 | 11 | 44 | 0.817 | 90.9% | 36.4% | 84.1% | 37/11 | 14 | CHƯA ĐẠT |
| 103|104 | 11 | 89 | 0.743 | 97.8% | 59.6% | 91.0% | 41/8 | 0 | CHƯA ĐẠT |
| 103|105 | 12 | 67 | 0.732 | 97.0% | 52.2% | 95.5% | 71/26 | 0 | CHƯA ĐẠT |
| 104|105 | 14 | 84 | 0.790 | 96.4% | 33.3% | 92.9% | 47/29 | 0 | CHƯA ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 1919 ({'bo_sot_thua': 460, 'iou_thap': 530, 'sai_thuoc_tinh': 498, 'sai_lop': 38, 'bat_dong_ignore': 377, 'co_can_review': 16}), trên 38 ảnh cần calibration.
