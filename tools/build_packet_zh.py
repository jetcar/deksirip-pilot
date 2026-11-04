"""Rebuild papers/concept-note-zh.pdf from the Chinese Markdown sources.

Run from anywhere:  python tools/build_packet_zh.py

The geometry below was measured from the packets built by the author's
original tool, so that a rebuilt Chinese packet looks like the English and
Russian ones: A4, text left at 59.86 pt, frame width 477.1 pt, footer
baseline at 34 pt, leading 20 pt for 10 pt body, headings in navy #172F4D.

Requires reportlab and the Arial Unicode MS font (the one the original
packets embed). Set DEKSIRIP_FONT to point at another copy if needed.
"""

import os
import re
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
)

FONT = "ArialUni"
FONT_CANDIDATES = [
    os.environ.get("DEKSIRIP_FONT", ""),
    r"C:/Windows/Fonts/ARIALUNI.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/usr/share/fonts/truetype/msttcorefonts/Arial_Unicode.ttf",
]

PAGE_W, PAGE_H = A4
TEXT_X = 59.858
FOOTER_X = 53.858
FRAME_RIGHT = 536.968
FRAME_W = FRAME_RIGHT - TEXT_X
TOP_MARGIN = 56.0
BOTTOM_MARGIN = 56.0
FOOTER_Y = 34.016

NAVY = "#172F4D"
GREY = "#526678"
BOX = "#EEF4F7"

FOOTER = "DEKSIRIP | 0.2 | 2026-11-03"

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DEFAULT_OUT = ROOT / "papers" / "concept-note-zh.pdf"


def find_font():
    for candidate in FONT_CANDIDATES:
        if candidate and Path(candidate).exists():
            return candidate
    sys.exit(
        "Arial Unicode MS not found. Install it or set DEKSIRIP_FONT to its path."
    )


def style(name, size, leading, color="#000000", **kw):
    return ParagraphStyle(
        name,
        fontName=FONT,
        fontSize=size,
        leading=leading,
        textColor=color,
        wordWrap="CJK",
        **kw,
    )


S = {
    "title": style("title", 19, 24, NAVY, spaceAfter=2),
    "meta": style("meta", 8, 11, GREY, spaceAfter=14),
    "note": style("note", 8, 11, GREY, spaceAfter=10),
    "h1": style("h1", 19, 24, NAVY, spaceBefore=4, spaceAfter=6),
    "h2": style("h2", 12, 20, NAVY, spaceBefore=20, spaceAfter=0),
    "body": style("body", 10, 20, "#000000", spaceAfter=0),
    "list": style("list", 10, 20, "#000000", leftIndent=14, spaceAfter=0),
    "flow": style(
        "flow", 9, 13, "#000000", backColor=BOX, borderPadding=6,
        spaceBefore=6, spaceAfter=10,
    ),
    "fn": style("fn", 8, 10, GREY, spaceBefore=6),
}

LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")
CJK = re.compile(r"[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]")


def clean(text):
    text = LINK.sub(r"\1", text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text.replace("**", "")


def smart_join(parts):
    """Join wrapped Markdown lines: no space between two CJK characters."""
    out = parts[0]
    for p in parts[1:]:
        if CJK.match(out[-1]) and CJK.match(p[0]):
            out += p
        else:
            out += " " + p
    return out


def para(text, kind="body"):
    return Paragraph(clean(text), S[kind])


def md_to_flowables(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    out, buf = [], []
    i = 0

    def flush():
        if buf:
            out.append(para(smart_join(buf), "body"))
            buf.clear()

    while i < len(lines):
        s = lines[i].strip()

        if s.startswith("```"):
            flush()
            i += 1
            block = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                step = lines[i].strip().strip("↓").strip()
                if step:
                    block.append(step)
                i += 1
            out.append(para("  →  ".join(block), "flow"))
            i += 1
            continue

        if s.startswith("# "):
            flush()
            out.append(para(s[2:].strip(), "h1"))
        elif s.startswith("## "):
            flush()
            out.append(para(s[3:].strip(), "h2"))
        elif s.startswith("> "):
            # Per-file translation note. The packet carries one note on the
            # cover instead, so a five-page document states it once.
            flush()
        elif s.startswith("- "):
            flush()
            out.append(Paragraph("·  " + clean(s[2:].strip()), S["list"]))
        elif re.match(r"^\d+\.\s", s):
            flush()
            out.append(para(s))
        elif s:
            buf.append(s)
        else:
            flush()
        i += 1

    flush()
    return out


def cover():
    return [
        para("DEKSIRIP：模型与试点提案", "title"),
        para("版本 0.2  |  2026年11月3日  |  征求学术批评", "meta"),
        para(
            "翻译说明：本文件由人工智能翻译，未经母语者审校。如遇歧义，以英文版为准，"
            "英文版见 github.com/jetcar/deksirip-pilot。",
            "note",
        ),
    ]


def questions_page():
    story = [para("问题、来源与联系方式", "h1")]
    story.append(para("供研究者的问题", "h2"))
    for q in [
        "1. 经济假设是否清晰且可检验？哪些假设互不兼容？",
        "2. 哪些中国或国际案例最接近这一制度组合？",
        "3. 哪些劳动激励、稀缺分配规则和责任边界需要说明？",
        "4. 什么样的最小试点、对照组和停止标准才能产生可信的证据？",
    ]:
        story.append(para(q))

    story.append(para("官方来源与推论边界", "h2"))
    story.append(
        para(
            "[1] 国家发展和改革委员会，2023年3月23日。《关于推广浙江共同富裕示范区"
            "第一批典型经验的通知》（第252号）。介绍了缩小差距、基本公共服务均等化等"
            "做法。"
        )
    )
    story.append(
        para(
            "[2] 中国财政部，2024年1月25日。关于平湖共同富裕村庄试点的报告。介绍了"
            "联合融资、集体资产使用和收益分配，并给出项目结果与预测。"
        )
    )
    story.append(
        para(
            "这些文件确立的是单项做法，不能证明 DEKSIRIP 整体模型的有效性或新颖性，"
            "也不能证明不存在类似实验。这只是初步阅读清单，不是系统综述；仍需要独立"
            "的因果评估。"
        )
    )

    story.append(para("联系方式与无需 GitHub 的阅读方式", "h2"))
    story.append(
        para(
            "Vladimir Kruglov，独立研究者。电子邮件：vladimirkruq5@gmail.com。本 PDF "
            "提供独立的介绍、示例、试点提案、问题和来源。第一次阅读不需要 GitHub。"
            "欢迎通过电子邮件提出意见或索取更多材料。其他版本与更新："
            "https://github.com/jetcar/deksirip-pilot"
        )
    )
    story.append(
        para(
            "[1] https://www.ndrc.gov.cn/xxgk/zcfb/tz/202303/t20230323_1351675.html",
            "fn",
        )
    )
    story.append(
        para(
            "[2] https://www.mof.gov.cn/zhengwuxinxi/xinwenlianbo/"
            "zhejiangcaizhengxinxilianbo/202401/t20240124_3927140.htm",
            "fn",
        )
    )
    return story


def on_page(canvas, doc):
    canvas.setFont(FONT, 8)
    canvas.setFillColor(GREY)
    canvas.drawString(FOOTER_X, FOOTER_Y, FOOTER)
    canvas.drawRightString(FRAME_RIGHT, FOOTER_Y, str(doc.page))


def build(out_path):
    doc = BaseDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=TEXT_X,
        rightMargin=PAGE_W - FRAME_RIGHT,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title="DEKSIRIP：模型与试点提案",
        author="Vladimir Kruglov",
    )
    frame = Frame(
        TEXT_X,
        BOTTOM_MARGIN,
        FRAME_W,
        PAGE_H - TOP_MARGIN - BOTTOM_MARGIN,
        id="body",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=on_page)])

    story = cover()
    story += md_to_flowables(DOCS / "model-at-a-glance-zh.md")
    story.append(PageBreak())
    story += md_to_flowables(DOCS / "concept-note-zh.md")
    story.append(PageBreak())
    story += questions_page()

    doc.build(story)
    print("written:", out_path)


if __name__ == "__main__":
    pdfmetrics.registerFont(TTFont(FONT, find_font()))
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT)
