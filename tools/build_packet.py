"""Build the three standalone research packets. Run: python tools/build_packet.py."""
import argparse
import os
import re
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

try:  # used for verification and QA images; the packets build without them
    from pypdf import PdfReader
    import fitz
except ImportError:
    PdfReader = None
    fitz = None

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'local/private/pdf-qa'
FONT = 'PilotUnicode'
FONT_PATH = os.environ.get('DEKSIRIP_FONT', r'C:\Windows\Fonts\ARIALUNI.ttf')
pdfmetrics.registerFont(TTFont(FONT, FONT_PATH))
META = {
 'ru': ('DEKSIRIP: модель и предложение пилота', 'Версия 0.2 | 3 ноября 2026 | Для академической критики', 'Вопросы, источники и контакт', 'Владимир Круглов | Независимый исследователь'),
 'en': ('DEKSIRIP: model and pilot proposal', 'Version 0.2 | 3 November 2026 | For academic criticism', 'Questions, sources and contact', 'Vladimir Kruglov | Independent researcher'),
 'zh': ('DEKSIRIP：模型与试点提案', '版本 0.2 | 2026年11月3日 | 征求学术批评', '研究问题、资料与联系方式', 'Vladimir Kruglov | 独立研究者'),
}
END = {
 'ru': '''## Вопросы исследователю
1. Достаточно ли ясна и проверяема экономическая гипотеза? Какие предположения несовместимы?
2. Какие китайские или международные примеры ближе всего к этой комбинации институтов?
3. Какие стимулы к труду, правила распределения дефицита и границы ответственности необходимо уточнить?
4. Какой минимальный пилот, сравнение и критерии остановки позволят получить убедительный результат?

## Официальные источники и границы выводов
[1] Государственный комитет КНР по развитию и реформам, 23 марта 2023. Уведомление о первой группе типовых практик демонстрационной зоны общего процветания Чжэцзяна (№ 252). Документ описывает отбор практик, включая сокращение различий и выравнивание базовых общественных услуг.

[2] Министерство финансов КНР, 25 января 2024. Материал о пилотах общего процветания в Пинху. Описывает совместное финансирование, использование коллективных активов и распределение доходов; приводит результаты отдельных проектов и прогнозы.

Эти материалы подтверждают существование отдельных практик. Они не доказывают эффективность всей модели DEKSIRIP, её новизну или отсутствие похожего эксперимента. Это исходный список, а не систематический обзор; независимая оценка причинных эффектов ещё нужна.

## Контакт и чтение без GitHub
Владимир Круглов, независимый исследователь.
Email: vladimirkruq5@gmail.com
Этот PDF содержит самостоятельное введение, пример, предложение пилота, вопросы и источники. Для первого чтения GitHub не нужен. Ответить и запросить дополнительные материалы можно по электронной почте.
Дополнительные версии и обновления: https://github.com/jetcar/deksirip-pilot
''',
 'en': '''## Questions for a researcher
1. Is the economic hypothesis clear and testable? Which assumptions are incompatible?
2. Which Chinese or international cases are closest to this combination of institutions?
3. Which work incentives, scarcity-allocation rules and boundaries of responsibility need clarification?
4. What minimal pilot, comparison and stopping criteria could produce credible evidence?

## Official sources and limits of inference
[1] National Development and Reform Commission, 23 March 2023. Notice on the first set of typical practices from Zhejiang's common-prosperity demonstration zone (No. 252). Describes selected practices, including narrowing disparities and equalizing basic public services.

[2] Ministry of Finance of China, 25 January 2024. Report on common-prosperity village pilots in Pinghu. Describes joint financing, collective-asset use and income distribution, with reported project results and forecasts.

These documents establish individual practices. They do not prove the effectiveness or novelty of the full DEKSIRIP model, or the absence of a similar experiment. This is an initial reading list, not a systematic review; independent causal evaluation is still needed.

## Contact and reading without GitHub
Vladimir Kruglov, independent researcher.
Email: vladimirkruq5@gmail.com
This PDF provides a standalone introduction, example, pilot proposal, questions and sources. GitHub is not needed for a first reading. Comments and requests for further materials are welcome by email.
Additional versions and updates: https://github.com/jetcar/deksirip-pilot
''',
 'zh': '''## 请研究者评议的问题
1. 经济假设是否清晰且可检验？哪些假设可能不相容？
2. 哪些中国或国际案例最接近这一制度组合？
3. 哪些劳动激励、稀缺资源分配规则和责任边界还需要明确？
4. 怎样的最小试点、比较方法和停止标准能够产生可信证据？

## 官方资料与推论边界
[1] 国家发展和改革委员会，2023年3月23日。关于印发浙江高质量发展建设共同富裕示范区第一批典型经验的通知（发改就业〔2023〕252号）。介绍所选经验，包括缩小差距和促进基本公共服务均等化。

[2] 中华人民共和国财政部，2024年1月25日。浙江省平湖财政推进一事一议共富乡村试点探索众筹发展共富体新模式。介绍共同融资、集体资产利用及收益分配，包含部分项目已报告的结果和预期数据。

这些资料说明单独的实践确实存在，并不能证明 DEKSIRIP 整体模型有效或具有原创性，也不能证明类似实验从未进行过。这是初步资料清单，而非系统文献综述；仍需独立的因果评估。

## 联系方式与离线阅读
Vladimir Kruglov，独立研究者。
电子邮箱：vladimirkruq5@gmail.com
本 PDF 独立包含模型简介、示例、试点提案、研究问题和参考资料，首次阅读无需访问 GitHub。欢迎通过电子邮件提出批评或索取进一步材料。
其他语言版本与更新：https://github.com/jetcar/deksirip-pilot
''',
}
SOURCES = [
 'https://www.ndrc.gov.cn/xxgk/zcfb/tz/202303/t20230323_1351675.html',
 'https://www.mof.gov.cn/zhengwuxinxi/xinwenlianbo/zhejiangcaizhengxinxilianbo/202401/t20240124_3927140.htm',
]

def inline(s):
    s = s.replace('**', '').replace('`', '').replace('—', '-').replace('–', '-')
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: m[1] if not m[2].startswith(('https:', 'mailto:')) else m[1]+' ('+m[2]+')', s)
    return escape(s)

def styles(lang):
    common = dict(fontName=FONT, wordWrap='CJK' if lang=='zh' else None)
    return {
        'body': ParagraphStyle('body', fontSize=10, leading=14, spaceAfter=6, **common),
        'title': ParagraphStyle('title', fontSize=19, leading=24, spaceAfter=13, textColor=colors.HexColor('#17324D'), **common),
        'h': ParagraphStyle('h', fontSize=12, leading=16, spaceBefore=10, spaceAfter=6, keepWithNext=True, textColor=colors.HexColor('#17324D'), **common),
        'meta': ParagraphStyle('meta', fontSize=8, leading=11, spaceAfter=8, textColor=colors.HexColor('#526577'), **common),
        'flow': ParagraphStyle('flow', fontSize=9, leading=12, spaceBefore=5, spaceAfter=8, backColor=colors.HexColor('#EEF4F7'), borderPadding=8, **common),
        'quote': ParagraphStyle('quote', fontSize=8, leading=11, spaceAfter=8, textColor=colors.HexColor('#526577'), **common),
    }

def parse(md, st):
    story, buf, flow = [], [], None
    def flush():
        if buf:
            story.append(Paragraph(inline(' '.join(buf)), st['body']))
            buf.clear()
    for raw in md.splitlines():
        line = raw.strip()
        if line.startswith('```'):
            flush()
            if flow is None: flow=[]
            else:
                story.append(Paragraph(inline(' → '.join(x for x in flow if x != '↓')), st['flow']))
                flow=None
        elif flow is not None:
            flow.append(line)
        elif not line: flush()
        elif line.startswith('>'):
            flush()
            story.append(Paragraph(inline(line.lstrip('> ').strip()), st['quote']))
        elif line.startswith('#'):
            flush()
            story.append(Paragraph(inline(line.lstrip('# ')), st['title' if line.startswith('# ') else 'h']))
        elif line.startswith('- ') or re.match(r'^\d+\. ',line):
            flush()
            buf.append(line)
        else: buf.append(line)
    flush()
    return story

def build(lang):
    st=styles(lang)
    overview=(ROOT/f'docs/model-at-a-glance-{lang}.md').read_text(encoding='utf-8')
    concept=(ROOT/f'docs/concept-note-{lang}.md').read_text(encoding='utf-8')
    # The packet contains the cited overview itself; omit the web-only scope section.
    concept=re.split(r'(?m)^## (?:8\.|八、)',concept)[0]
    concept=re.sub(r'(?m)^\*\*(?:Версия|Version|版本).*\n?', '', concept)
    prop={'ru':'## Что является общим','en':'## What is common','zh':'## 哪些是公共的'}[lang]
    split=overview.index(prop)
    pilot=re.search(r'(?m)^## (?:4\.|四、)',concept)
    if not pilot: raise ValueError(f'Pilot section missing: {lang}')
    blocks=[overview[:split],overview[split:],concept[:pilot.start()],concept[pilot.start():],END[lang]]
    story=[]
    for i,block in enumerate(blocks):
        if i: story.append(PageBreak())
        if i==0:
            story += [Paragraph(inline(META[lang][0]),st['title']),Paragraph(inline(META[lang][1]),st['meta'])]
        if i==4: story.append(Paragraph(inline(META[lang][2]),st['title']))
        story+=parse(block,st)
        if i==4:
            for n,url in enumerate(SOURCES,1):
                story.append(Paragraph(f'[{n}] <link href="{url}" color="#246386">{url}</link>',st['meta']))
    def footer(c,d):
        c.setFont(FONT,8)
        c.setFillColor(colors.HexColor('#526577'))
        c.drawString(19*mm,12*mm,'DEKSIRIP | 0.2 | 2026-11-03')
        c.drawRightString(A4[0]-19*mm,12*mm,str(d.page))
    target=ROOT/f'papers/concept-note-{lang}.pdf'
    SimpleDocTemplate(str(target),pagesize=A4,leftMargin=19*mm,rightMargin=19*mm,topMargin=16*mm,bottomMargin=19*mm,title=META[lang][0],author='Vladimir Kruglov').build(story,onFirstPage=footer,onLaterPages=footer)

    if PdfReader is None or fitz is None:
        print(f'{lang}: {target.name}, {target.stat().st_size} bytes '
              '(install pypdf and PyMuPDF for verification and QA images)')
        return

    reader=PdfReader(target)
    text='\n'.join(p.extract_text() for p in reader.pages)
    assert 'vladimirkruq5@gmail.com' in text and 'ndrc.gov.cn' in text
    assert not any(x in text for x in ['technical-architecture-','local/private/'])
    print(f'{lang}: {len(reader.pages)} pages, {target.stat().st_size} bytes')
    doc=fitz.open(target)
    for i,p in enumerate(doc): p.get_pixmap(matrix=fitz.Matrix(1,1)).save(QA/f'{lang}-{i+1}.png')
    from PIL import Image, ImageOps, ImageDraw
    thumbs=[]
    for i in range(len(doc)):
        im=Image.open(QA/f'{lang}-{i+1}.png').convert('RGB')
        im.thumbnail((420,600))
        thumb=Image.new('RGB',(440,630),'#d6dce3'); thumb.paste(im,(10,20))
        ImageDraw.Draw(thumb).text((10,5),f'{lang} / {i+1}',fill='black'); thumbs.append(thumb)
    sheet=Image.new('RGB',(440*len(thumbs),630),'white')
    for i,im in enumerate(thumbs): sheet.paste(im,(i*440,0))
    sheet.save(QA/f'{lang}-contact.png')

if __name__=='__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    if PdfReader is not None and fitz is not None:
        QA.mkdir(parents=True,exist_ok=True)
    for lang in ('ru','en','zh'): build(lang)
