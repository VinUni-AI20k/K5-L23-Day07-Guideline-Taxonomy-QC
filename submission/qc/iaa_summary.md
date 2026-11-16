# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 4
- Lượt gán đủ **80/80**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 321 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 40 | 321 | 1.000 | 100.0% | 100.0% | 100.0% | 0/0 | 0 | ĐẠT |
| 194|202 | 6 | 27 | 1.000 | 100.0% | 100.0% | 100.0% | 0/0 | 0 | ĐẠT |
| 194|231 | 9 | 88 | 1.000 | 100.0% | 100.0% | 100.0% | 0/0 | 0 | ĐẠT |
| 194|236 | 5 | 52 | 1.000 | 100.0% | 100.0% | 100.0% | 0/0 | 0 | ĐẠT |
| 202|231 | 5 | 35 | 1.000 | 100.0% | 100.0% | 100.0% | 0/0 | 0 | ĐẠT |
| 202|236 | 9 | 65 | 1.000 | 100.0% | 100.0% | 100.0% | 0/0 | 0 | ĐẠT |
| 231|236 | 6 | 54 | 1.000 | 100.0% | 100.0% | 100.0% | 0/0 | 0 | ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 0 ({}), trên 0 ảnh cần calibration.
