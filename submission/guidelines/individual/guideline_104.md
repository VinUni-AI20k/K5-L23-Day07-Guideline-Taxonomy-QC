# Guideline gán nhãn — v0.1 cá nhân — 104

- Phiên bản: v0.1
- Ngày: 2026-11-16
- Người viết / duyệt: 104

## 1. Mục tiêu

Nhãn cho mô hình phát hiện người và phương tiện trên ảnh đường phố. Mục tiêu là gán đúng đối tượng có thật trong khung hình, không gán phản chiếu, tượng, biển quảng cáo, hay các vật không phải người/xe. Box phải ôm sát phần nhìn thấy của đối tượng và không được thừa quá nhiều vùng nền.

Mục tiêu quan trọng: cùng một ảnh, mọi người đọc quy tắc như nhau. Nếu không chắc, ưu tiên đánh dấu `can_review` và ghi rõ lý do để reviewer xác nhận thay vì gán ngẫu nhiên.

## 2. Lớp và thuộc tính

### Lớp

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con, SUV, hatchback, xe cá nhân thông thường. | ô tô nhỏ, SUV, sedan. | Xe tải, xe chở hàng, xe máy. |
| `truck` | Xe tải, xe có thùng / cabin riêng, thường lớn hơn ô tô và có tải-trọng rõ ràng. | xe tải, xe container nhỏ, xe thùng lớn. | Xe con, van, xe chở khách. |
| `van` | Xe thùng kín cỡ nhỏ hoặc xe thương mại nhỏ. | van nhỏ, xe giao hàng nhỏ, xe chở hàng cỡ vừa. | Xe tải lớn, ô tô con. |
| `motorcycle` | Xe máy / mô tô, bao gồm cả người ngồi trên xe nếu hai vật được phân biệt rõ. | xe máy, mô tô, xe tay ga. | Người đi bộ, người ngồi trên xe nhưng không thấy xe. |
| `person` | Người đi bộ; người ngồi trên xe máy hoặc trên xe chở hàng nếu thân người nhìn thấy rõ. | người đi bộ, người đứng ở góc, người ngồi sau xe máy. | Phản chiếu trong gương, tượng, biển người. |
| `ignore_region` | Vùng không cần gán vật riêng: phản chiếu, tượng, biển, thùng, ô tô không phải phương tiện thực tế trong khung hình, chi tiết không phải traffic participant. | tượng đài, phản chiếu kính, biển quảng cáo, tấm kính đẹp, bóng phản xạ. | Người thật, xe thật, vật thực tế nằm trong ảnh. |

### Thuộc tính

| Thuộc tính | Giá trị | Nghĩa | Quy tắc dùng |
|---|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Mức che khuất | `0` = thấy rõ > 80%; `1` = che ít 20–40%; `2` = che nhiều 40–70%; `3` = hầu như không xác định được thân vật. |
| `truncated` | `no`, `yes` | Vật cắt mép ảnh | Nếu > 20% chiều cao hoặc > 20% chiều rộng bị cắt khỏi khung ảnh thì đánh `yes`. |
| `can_review` | `true`, `false` | Dấu hiệu cần người xem lại | Tick khi không chắc về lớp, box, hay có tranh chấp giữa vật thật và phản chiếu / vật quá nhỏ. |

Chú ý: `ignore_region` không yêu cầu thuộc tính phức tạp; với vùng ignore, nếu dùng box thì box chỉ để đánh dấu vùng bỏ qua, không đếm đối tượng.

## 3. Quy tắc vẽ box

1. Gán một box cho mỗi vật thực sự tồn tại trong ảnh, không gán phản chiếu hoặc vật không thật.
2. Box ôm sát phần nhìn thấy của vật: không thừa nhiều nền, nhưng cũng không cắt mất phần quan trọng của vật. Nếu vật bị che hoặc cắt mép, box vẫn ôm phần thấy được và ghi `occluded_level` / `truncated` tương ứng.
3. Với người đi xe máy:
   - Nếu cả người và xe đều thấy rõ, gán 2 box riêng: 1 box cho `motorcycle`, 1 box cho `person`.
   - Nếu người và xe bị che lẫn nhau, vẫn gán theo phần nào nhìn thấy được; nếu chỉ thấy người mà không thấy xe rõ, chỉ gán `person`; nếu thấy xe rõ nhưng người thì không rõ, chỉ gán `motorcycle`.
   - Nếu xe máy quá nhỏ hoặc chỉ thấy một phần rất nhỏ, có thể bỏ qua nếu chiều cao box < 20 px hoặc vật quá mờ không đủ nhận dạng. Cần ghi rõ trong `can_review` nếu đang ngờ.
4. Vật bị che: lấy phần nhìn thấy. Ví dụ: một người đứng phía sau xe, chỉ thấy nửa người; box bao nửa người nhìn thấy, không gán vùng bị che giấu.
5. Vật quá nhỏ: nếu vật nhỏ hơn ngưỡng 20 px theo chiều cao và không đủ để phân loại được, bỏ qua. Nếu có thể xác định rõ lớp và vẫn > 20 px thì gán.
6. Tượng, biển quảng cáo, phản chiếu, bóng, cửa kính phản quang: không label; dùng `ignore_region` khi đây là một vùng có nhiều hiện tượng lặp hoặc nhiều vật không cần đếm.
7. Xe chở xe / hàng hóa trên xe:
   - Nếu đó là phương tiện chính bản thân xe chở hàng, phân loại theo loại xe chính (không gán thêm “hàng hóa” như lớp riêng).
   - Nếu vật được chở là một xe máy/ô tô khác rõ ràng và độc lập, có thể gán thêm vật đó nếu đủ rõ và không quá nhỏ; nếu không chắc thì `can_review`.
8. Đối tượng ở mép ảnh:
   - Gán nếu phần nhìn thấy đủ rõ để nhận dạng và có thể xác định lớp.
   - Nếu chỉ còn 1 nửa hoặc thậm chí một phần quá nhỏ, cần `can_review` hoặc bỏ qua nếu dưới ngưỡng.

## 4. Ca khó

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_005 | Người ngồi trên xe máy trong không gian đông người; chỉ thấy thân người + phần xe rõ. | R-01 | `motorcycle` + `person` nếu thấy rõ cả hai; nếu chỉ thấy xe hoặc người mà không đủ, gán riêng từng phần theo phần nhìn thấy. | Quy tắc chung: người và xe là 2 vật khác nhau; không gom thành 1 box. |
| img_006 | Người đi xe máy ở góc gần, phần người và xe chồng lên nhau. | R-01 | `motorcycle` + `person` và kiểm tra `occluded_level` phù hợp. | Hình dung người trên xe là 2 đối tượng, không phải 1 vật. |
| img_011 | Người đi bộ và xe máy ngoài phố, đám đông. | R-02 | Gán rõ những vật đủ lớn và rõ ràng; vật quá nhỏ/cù lỳ, bỏ qua hoặc `can_review`. | Phải tránh gán mọi vật trong đám đông vì nhiều đường viền mờ, vật nhỏ. |
| img_013 | Một người đi trong đêm, chụp cận cảnh; có khoảng sáng, người và xe máy. | R-03 | Nếu phần người nhìn thấy đủ và có xe máy riêng rõ thì gán cả 2. Nếu chỉ là bóng mờ, xem như `can_review`. | Phần nhìn thấy phải đủ rõ để nhận dạng lớp. |
| img_017 | Tượng người cưỡi ngựa, có cờ / phao / nón an toàn trên đầu. | R-04 | `ignore_region` hoặc không gán. | Đây là tượng trang trí, không phải người/xe thực tế trên đường. |
| img_018 | Bảng quảng cáo / poster / cổng, phản bay trên không. | R-05 | `ignore_region` | Không phải đối tượng giao thông; là vật trang trí / tấm quảng cáo. |
| img_020 | Gương chiếu phản xạ của ô tô và người đi; hình phản chiếu trong gương xe. | R-06 | Không gán phản chiếu; `ignore_region` nếu cần. | Phản chiếu không phải vật thật trong khung hình. |
| img_021 | Bức tường có biển, xe xuất hiện trong gương. | R-06 | Không gán phản chiếu; ưu tiên vật thật trong ảnh. | Vật trong gương chỉ là hình phản chiếu, không phải đối tượng cần đếm. |
| img_023 | Nhiều ô tô quá xa / quá nhỏ; dạng vừa thấy rõ nhưng rất nhỏ. | R-07 | Bỏ qua nếu chiều cao < 20 px; nếu > 20 px và nhận dạng rõ thì gán. | Dùng ngưỡng vật quá nhỏ để kiểm soát noise. |
| img_031 | Xe cắt mép ảnh, chỉ thấy một nửa. | R-08 | Gán nếu phần còn lại đủ rõ để phân loại; `truncated=yes`. | Chỉ tag phần nhìn thấy, không cần đoán phần bị che mất. |
| img_033 | Người đi bộ ở mép ảnh, hiển thị nửa người. | R-08 | Gán `person` nếu nửa người đủ rõ; nếu chỉ là bóng mờ thì `can_review`. | Nếu phần nhìn thấy cho phép nhận dạng, gán. |
| img_035 | Xe máy / người chụp ở nơi có diện tích nhỏ. | R-09 | Nếu size nhỏ nhưng thấy rõ -> gán; nếu mờ/khó nhận dạng -> `can_review` và xem reviewer. | Quy tắc phụ: việc nhận dạng rõ hơn so với kích thước. |
| img_039 | Những vật ở xa, tương tự cọc, khung, đèn. | R-10 | Không gán nếu không xác định rõ là người/xe. | Bỏ qua những đối tượng không chắc chắn. |

### Phân loại ca khó

- Ca thuộc quy tắc: người trên xe máy, xe chở hàng, vật nhỏ dưới ngưỡng, phần mép ảnh, vật che chắn nhưng còn thấy rõ, phản chiếu trong gương, tượng vẻ ngoài không phải đối tượng giao thông.
- Ca cần hỏi reviewer: vật quá nhỏ nhưng vẫn lạ, mờ do đêm, phản chiếu/đèn sáng quá mạnh, người/xe bị che gần như mất hẳn, vật ở mép ảnh mà không đủ thông tin để phân lớp chắc chắn.

## 5. QC và phiên bản

Ngưỡng QC áp dụng:
- Không gán phản chiếu, tượng, biển quảng cáo, đồ trang trí.
- Box phải ôm sát vật thật, không kéo quá rộng.
- Nếu không chắc, dùng `can_review` và ghi ảnh + vùng + lý do vào nhật ký.
- Các ca làm hai người hiểu khác nhau phải ghi trong guideline để reviewer quyết định trước khi khóa nhãn.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0.1 | Viết lại quy tắc cho người/xe, vật nhỏ, phản chiếu, tượng và mép ảnh | Cần làm rõ chỗ mơ hồ từ starter v0 |
| v0 | Khởi đầu sơ sài | Chưa đủ để gán thống nhất |

## Tự kiểm

- Nếu đọc lại ảnh `img_005` / `img_006` / `img_013`, tôi sẽ gán `person` và `motorcycle` riêng khi thấy cả hai rõ; nếu chỉ thấy một phần, gán theo phần còn lại.
- Với `img_017` và `img_018`, tôi không gán vì chúng là tượng / billboard / trang trí, không phải người hoặc xe.
- Với `img_020` và `img_021`, tôi bỏ qua phản chiếu trong gương và chỉ gán đối tượng thật nằm trong khung hình.
- Với `img_023` và `img_039`, tôi bỏ qua vật quá nhỏ hoặc không đủ rõ.
- Với `img_031` và `img_033`, tôi gán theo phần nhìn thấy nếu rõ ràng, đồng thời đánh `truncated=yes` nếu cắt mép ảnh.

Khi cả nhóm đã thống nhất guideline, bản này sẽ là cơ sở để so sánh và sửa cho v1.0. 
