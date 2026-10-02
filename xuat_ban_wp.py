# -*- coding: utf-8 -*-
"""Đăng file lên WordPress Media Library và chèn link tải vào đúng chỗ trong
nội dung một bài viết đã tồn tại, qua WordPress REST API (Application Password).

⛔ Bài học quan trọng (rút ra từ ca thật): nội dung bài viết lấy qua
`GET /wp/v2/posts` trả về **HTML đã lưu**, không phải văn bản thuần. Chuỗi cần
tìm để thay thế PHẢI khớp đúng HTML thật (ví dụ `<strong>...</strong>`), không
phải câu hiển thị trên trang. Luôn kiểm tra chuỗi tìm có khớp TRƯỚC khi ghi đè
— nếu không khớp, ghi phần nội dung xung quanh ra FILE (không print ra console
trên Windows, dễ vỡ do console không phải UTF-8) để tự đọc lại và sửa chuỗi tìm
cho đúng, thay vì đoán mù.

Yêu cầu: `pip install requests`. File `.env.wordpress` (không commit) gồm:
    WP_URL=https://domain.example
    WP_USER=ten-dang-nhap
    WP_APP_PASSWORD=mat-khau-ung-dung-wordpress
(Tạo Application Password tại wp-admin → Users → Profile → Application Passwords.)
"""
import base64
import sys

import requests


def doc_env(duong_dan='.env.wordpress'):
    env = {}
    with open(duong_dan, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                env[k] = v
    return env


def dang_nhap(env):
    token = base64.b64encode(f"{env['WP_USER']}:{env['WP_APP_PASSWORD']}".encode()).decode()
    return {'Authorization': f'Basic {token}'}


def tai_len_media(env, headers, duong_dan_file, ten_file, content_type):
    """Tải 1 file lên Media Library, trả về (id, source_url)."""
    h = dict(headers)
    h['Content-Disposition'] = f'attachment; filename="{ten_file}"'
    h['Content-Type'] = content_type
    with open(duong_dan_file, 'rb') as f:
        data = f.read()
    r = requests.post(f"{env['WP_URL']}/wp-json/wp/v2/media", headers=h, data=data, timeout=30)
    r.raise_for_status()
    j = r.json()
    return j['id'], j['source_url']


def lay_bai_theo_slug(env, headers, slug):
    r = requests.get(f"{env['WP_URL']}/wp-json/wp/v2/posts", params={'slug': slug},
                      headers=headers, timeout=30)
    posts = r.json()
    if not posts:
        raise RuntimeError(f'Không tìm thấy bài slug={slug}')
    post = posts[0]
    content = post['content'].get('raw')
    if content is None:
        r2 = requests.get(f"{env['WP_URL']}/wp-json/wp/v2/posts/{post['id']}",
                           params={'context': 'edit'}, headers=headers, timeout=30)
        content = r2.json()['content']['raw']
    return post['id'], content


def thay_va_cap_nhat(env, headers, post_id, content, chuoi_tim, chuoi_thay, file_loi='doan-khong-khop.txt'):
    """Thay chuoi_tim bằng chuoi_thay trong content, cập nhật bài. Nếu chuoi_tim
    không khớp, ghi ngữ cảnh ra file_loi rồi dừng — KHÔNG đoán mù, KHÔNG tự sửa
    chuỗi tìm."""
    if chuoi_tim not in content:
        idx = content.find(chuoi_tim[:20])  # thử khớp một phần để định vị gần đúng
        doan = content[max(0, idx - 100):idx + 300] if idx >= 0 else '[không tìm thấy cả phần đầu chuỗi]'
        with open(file_loi, 'w', encoding='utf-8') as f:
            f.write(f'vi_tri_gan_dung: {idx}\n---\n{doan}')
        raise RuntimeError(f'Chuỗi tìm không khớp HTML thật — xem {file_loi} để sửa lại chuỗi tìm')
    content_moi = content.replace(chuoi_tim, chuoi_thay)
    r = requests.post(f"{env['WP_URL']}/wp-json/wp/v2/posts/{post_id}", headers=headers,
                       json={'content': content_moi}, timeout=30)
    r.raise_for_status()
    return r.status_code


if __name__ == '__main__':
    print('Đây là thư viện — import các hàm vào script riêng cho từng việc. '
          'Xem README.md mục "Dùng" để có ví dụ đầy đủ.', file=sys.stderr)
