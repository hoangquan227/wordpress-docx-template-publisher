# -*- coding: utf-8 -*-
"""Soạn văn bản hành chính/công văn DOCX đúng thể thức Nghị định 30/2020/NĐ-CP
(khổ A4, lề chuẩn, Times New Roman, quốc hiệu tiêu ngữ) — dùng lại được cho mọi
mẫu công văn/giấy giới thiệu/giấy đề nghị của doanh nghiệp.

Không hard-code nội dung cụ thể — các hàm ở đây là KHỐI XÂY DỰNG (building
blocks), ghép lại theo nhu cầu từng văn bản cụ thể trong script gọi riêng.

Dùng: xem README.md, mục "Dùng".
"""
from docx import Document
from docx.shared import Pt, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn


def tao_van_ban():
    """Tạo Document mới, đã set khổ A4 + lề + phông theo Nghị định 30/2020/NĐ-CP
    Phụ lục I: lề trên/dưới 20-25mm, lề trái 30-35mm (chừa chỗ đóng file), lề
    phải 15-20mm, Times New Roman 13-14pt."""
    doc = Document()
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(22)
    section.bottom_margin = Mm(22)
    section.left_margin = Mm(32)
    section.right_margin = Mm(18)

    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(13.5)
    rpr = style.element.get_or_add_rPr()
    rFonts = rpr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = rpr.makeelement(qn('w:rFonts'), {})
        rpr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    return doc


def doan(doc, text='', align=None, bold=False, italic=False, size=13.5, space_after=6):
    """Thêm 1 đoạn văn bản với định dạng chuẩn Times New Roman."""
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(space_after)
    if align:
        para.alignment = align
    run = para.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.name = 'Times New Roman'
    return para


def quoc_hieu_tieu_ngu(doc, ten_don_vi, so_hieu=''):
    """Khối tiêu đề công văn: tên đơn vị (trái) + quốc hiệu tiêu ngữ (phải), 2 cột."""
    tbl = doc.add_table(rows=1, cols=2)
    c1, c2 = tbl.rows[0].cells
    r = c1.paragraphs[0].add_run(ten_don_vi)
    r.bold = True
    r.font.size = Pt(13)
    r.font.name = 'Times New Roman'
    if so_hieu:
        pp = c1.add_paragraph()
        rr = pp.add_run(so_hieu)
        rr.font.size = Pt(13)
        rr.font.name = 'Times New Roman'

    c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = c2.paragraphs[0].add_run('CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM')
    r2.bold = True
    r2.font.size = Pt(12.5)
    r2.font.name = 'Times New Roman'
    pp2 = c2.add_paragraph()
    pp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = pp2.add_run('Độc lập - Tự do - Hạnh phúc')
    r3.bold = True
    r3.font.size = Pt(13.5)
    r3.font.name = 'Times New Roman'
    pp3 = c2.add_paragraph()
    pp3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r4 = pp3.add_run('———————')
    r4.font.size = Pt(12)
    r4.font.name = 'Times New Roman'
    return tbl


def tieu_de_van_ban(doc, ten_loai, ten_phu=None):
    """Tên loại văn bản — in hoa, đậm, canh giữa (vd 'GIẤY GIỚI THIỆU', 'CÔNG VĂN')."""
    doan(doc, ten_loai, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, space_after=2)
    if ten_phu:
        doan(doc, ten_phu, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=12, space_after=14)


def ky_ten(doc, chuc_vu, ghi_chu='(Ký, ghi rõ họ tên, đóng dấu)', so_dong_trong=3):
    """Khối ký tên — canh phải, đủ chỗ trống để ký tay khi in."""
    tbl = doc.add_table(rows=1, cols=2)
    c1, c2 = tbl.rows[0].cells
    c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = c2.paragraphs[0].add_run(chuc_vu)
    r.bold = True
    r.font.size = Pt(13)
    r.font.name = 'Times New Roman'
    pp = c2.add_paragraph()
    pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = pp.add_run(ghi_chu)
    r2.italic = True
    r2.font.size = Pt(11)
    r2.font.name = 'Times New Roman'
    for _ in range(so_dong_trong):
        pp2 = c2.add_paragraph()
        pp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return tbl
