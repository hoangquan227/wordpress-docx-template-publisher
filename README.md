# wordpress-docx-template-publisher

Hai việc hay đi cùng nhau khi làm nội dung cho website WordPress tiếng Việt:
1. **Soạn file DOCX** đúng thể thức văn bản hành chính Việt Nam (Nghị định 30/2020/NĐ-CP) —
   công văn, giấy giới thiệu, giấy đề nghị, mẫu cam kết...
2. **Đăng file đó lên WordPress** (Media Library) và **chèn link tải vào đúng chỗ** trong
   một bài viết đã có sẵn, qua REST API — không cần vào `wp-admin` thao tác tay.

## Vì sao tách thành thư viện

Ca thật (dự án TCKN, 02/10/2026): một bài viết hướng dẫn nhắc tới "Giấy giới thiệu/công văn
chỉ định" như một loại chứng từ cần có, nhưng không có file mẫu nào để khách tải — chỉ nói
suông. Soạn file DOCX đúng thể thức (Times New Roman, lề 30-35mm trái để chừa chỗ đóng file,
quốc hiệu tiêu ngữ...) rồi đăng lên WordPress và chèn link vào đúng câu trong bài, toàn bộ
qua script, không mở Word/trình duyệt thao tác tay.

## Cài đặt

```bash
pip install python-docx requests
```

## Dùng

### 1. Soạn DOCX

```python
from tao_cong_van import tao_van_ban, doan, quoc_hieu_tieu_ngu, tieu_de_van_ban, ky_ten
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = tao_van_ban()
quoc_hieu_tieu_ngu(doc, '[TÊN CÔNG TY]', 'Số: ……/CV')
doan(doc, '[Thành phố], ngày …… tháng …… năm ……', align=WD_ALIGN_PARAGRAPH.RIGHT, italic=True)
tieu_de_van_ban(doc, 'GIẤY GIỚI THIỆU', '(Kiêm công văn chỉ định khám sức khoẻ định kỳ)')
doan(doc, 'Kính gửi: ……………………………', bold=True)
doan(doc, 'Nội dung công văn...')
ky_ten(doc, 'ĐẠI DIỆN [TÊN CÔNG TY]')
doc.save('ra.docx')
```

### 2. Đăng lên WordPress + chèn link vào bài

Tạo `.env.wordpress` (đừng commit vào git):
```
WP_URL=https://domain-cua-ban.com
WP_USER=ten-dang-nhap
WP_APP_PASSWORD=mat-khau-ung-dung-wordpress
```
(Tạo Application Password tại `wp-admin` → Users → Profile → Application Passwords.)

```python
from xuat_ban_wp import doc_env, dang_nhap, tai_len_media, lay_bai_theo_slug, thay_va_cap_nhat

env = doc_env()
headers = dang_nhap(env)

_id, url_file = tai_len_media(
    env, headers, 'ra.docx', 'ten-file.docx',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document')

post_id, content = lay_bai_theo_slug(env, headers, 'slug-bai-viet')

thay_va_cap_nhat(
    env, headers, post_id, content,
    chuoi_tim='<strong>Giấy giới thiệu/công văn chỉ định</strong> — thay vai trò hợp đồng ở mục 7.2.',
    chuoi_thay=f'<strong>Giấy giới thiệu/công văn chỉ định</strong> — thay vai trò hợp đồng ở mục 7.2 '
               f'(<a href="{url_file}">tải mẫu DOCX</a>).')
```

## ⛔ Bẫy đã gặp (ghi lại để khỏi mò lại)

1. **Chuỗi tìm phải khớp đúng HTML đã lưu, không phải chữ hiển thị trên trang.**
   WordPress lưu nội dung dạng HTML (`<strong>`, `<li>`...), không phải văn bản thuần —
   tìm đúng câu hiển thị trên web rồi copy-paste vào code SẼ KHÔNG khớp nếu câu đó nằm
   trong thẻ in đậm/gạch đầu dòng. **Luôn lấy nội dung thật qua API trước, soi đúng cấu
   trúc HTML, rồi mới viết chuỗi tìm.**
2. **Không khớp thì KHÔNG được tự đoán/tự sửa chuỗi tìm rồi thử lại mù quáng** — hàm
   `thay_va_cap_nhat()` cố tình **raise lỗi và ghi ngữ cảnh ra file** thay vì tự động dò,
   để người gọi tự đọc và sửa đúng (xem `test_xuat_ban_wp.py` — phép thử xác nhận hàm
   KHÔNG gọi API cập nhật khi chưa chắc khớp).
3. **In tiếng Việt ra console trên Windows dễ vỡ** (`UnicodeEncodeError: 'charmap' codec`) —
   không phải lỗi dữ liệu, chỉ là console Windows không mặc định UTF-8. Ghi kết quả debug
   ra FILE thay vì `print()` khi cần xem nội dung tiếng Việt dài.
4. **Lề trái văn bản hành chính Việt Nam rộng hơn các lề khác (30-35mm)** — để chừa chỗ
   đóng file/bấm ghim khi in giấy thật, không phải lỗi căn lề.

## Phép thử

```bash
pip install pytest
python -m pytest test_xuat_ban_wp.py -q
```

## Giấy phép

MIT
