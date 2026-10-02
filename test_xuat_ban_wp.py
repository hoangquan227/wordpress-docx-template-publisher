# -*- coding: utf-8 -*-
"""Phép thử logic tìm/thay (không gọi mạng thật)."""
import os

from xuat_ban_wp import thay_va_cap_nhat


class _FakeResp:
    status_code = 200

    def raise_for_status(self):
        pass

    def json(self):
        return {}


def test_khop_dung_thi_bao_loi_ro_rang_khong_gia_vo_thanh_cong(monkeypatch):
    # Giả lập requests.post để không gọi mạng thật
    import xuat_ban_wp
    goi = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        goi['content'] = json['content']
        return _FakeResp()

    monkeypatch.setattr(xuat_ban_wp.requests, 'post', fake_post)

    content = '<p>Trước <strong>A</strong> sau</p>'
    thay_va_cap_nhat({'WP_URL': 'http://x'}, {}, 1, content, '<strong>A</strong>', '<strong>B</strong>')
    assert goi['content'] == '<p>Trước <strong>B</strong> sau</p>', goi['content']


def test_khong_khop_thi_bao_loi_va_ghi_file_khong_duoc_im_lang_ghi_de(monkeypatch, tmp_path):
    import xuat_ban_wp
    gọi_post = {'da_goi': False}

    def fake_post(*a, **kw):
        gọi_post['da_goi'] = True
        return _FakeResp()

    monkeypatch.setattr(xuat_ban_wp.requests, 'post', fake_post)

    file_loi = str(tmp_path / 'loi.txt')
    content = '<p>Không có chuỗi cần tìm ở đây</p>'
    try:
        thay_va_cap_nhat({'WP_URL': 'http://x'}, {}, 1, content, '<strong>KHONG_TON_TAI</strong>', 'X', file_loi)
        raise AssertionError('Đáng lẽ phải raise RuntimeError khi chuỗi không khớp')
    except RuntimeError:
        pass
    assert gọi_post['da_goi'] is False, 'KHÔNG được gọi API cập nhật khi chưa chắc chắn khớp'
    assert os.path.exists(file_loi), 'Phải ghi file ngữ cảnh để tự kiểm tra lại'


if __name__ == '__main__':
    import types

    class _MP:
        def setattr(self, obj, name, val):
            setattr(obj, name, val)

    mp = _MP()
    test_khop_dung_thi_bao_loi_ro_rang_khong_gia_vo_thanh_cong(mp)
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        class _Path:
            def __init__(self, base):
                self.base = base

            def __truediv__(self, name):
                return os.path.join(self.base, name)

        test_khong_khop_thi_bao_loi_va_ghi_file_khong_duoc_im_lang_ghi_de(mp, _Path(d))
    print('OK: 2/2 phep thu qua')
