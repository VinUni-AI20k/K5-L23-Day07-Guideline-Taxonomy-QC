# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 5
- Lượt gán đủ **120/120**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 777 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 120 | 777 | 0.844 | 89.3% | 74.5% | 86.9% | 260/248 | 0 | CHƯA ĐẠT |
| 042|059 | 13 | 71 | 0.722 | 87.3% | 60.6% | 91.5% | 29/30 | 0 | CHƯA ĐẠT |
| 042|063 | 12 | 111 | 0.898 | 85.6% | 81.1% | 86.5% | 18/60 | 0 | CHƯA ĐẠT |
| 042|069 | 12 | 117 | 0.985 | 99.1% | 73.5% | 90.6% | 4/10 | 0 | ĐẠT |
| 042|343 | 11 | 52 | 0.869 | 90.4% | 76.9% | 78.8% | 26/13 | 0 | CHƯA ĐẠT |
| 059|063 | 13 | 85 | 0.699 | 84.7% | 75.3% | 95.3% | 26/67 | 0 | CHƯA ĐẠT |
| 059|069 | 11 | 65 | 0.735 | 86.2% | 61.5% | 84.6% | 25/20 | 0 | CHƯA ĐẠT |
| 059|343 | 11 | 48 | 0.734 | 91.7% | 85.4% | 93.8% | 26/9 | 0 | CHƯA ĐẠT |
| 063|069 | 11 | 90 | 0.920 | 90.0% | 84.4% | 80.0% | 26/13 | 0 | CHƯA ĐẠT |
| 063|343 | 12 | 61 | 0.842 | 85.2% | 68.9% | 78.7% | 38/12 | 0 | CHƯA ĐẠT |
| 069|343 | 14 | 77 | 0.884 | 89.6% | 74.0% | 85.7% | 42/14 | 0 | CHƯA ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 1261 ({'bo_sot_thua': 508, 'co_can_review': 90, 'iou_thap': 309, 'sai_thuoc_tinh': 271, 'sai_lop': 83}), trên 36 ảnh cần calibration.
