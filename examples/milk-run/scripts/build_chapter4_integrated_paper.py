from __future__ import annotations

import json
import math
from datetime import UTC, datetime
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile

from PIL import Image, ImageDraw, ImageFont


OUT = Path("基于遗传算法的循环取货路径优化与物流平准化研究_第四章替换嵌图版.docx")
FIG_DIR = Path("chapter4_figures")
FIG_DIR.mkdir(exist_ok=True)

CN_FONT = "宋体"
EN_FONT = "Times New Roman"

ALGORITHMS = ["节点路径最短法", "扫描法", "节约里程法", "遗传算法", "模拟退火算法"]
RESULTS = [
    {"算法": "节点路径最短法", "线路数": 16, "单次总里程/km": 555.6, "日总里程/km": 2222.4, "平均装载率/%": 78.05, "装载率标准差": 16.59, "运行时间/s": 0.0001},
    {"算法": "扫描法", "线路数": 18, "单次总里程/km": 536.9, "日总里程/km": 2147.6, "平均装载率/%": 69.38, "装载率标准差": 12.56, "运行时间/s": 0.0011},
    {"算法": "节约里程法", "线路数": 17, "单次总里程/km": 527.8, "日总里程/km": 2111.2, "平均装载率/%": 73.46, "装载率标准差": 14.75, "运行时间/s": 0.0003},
    {"算法": "遗传算法", "线路数": 15, "单次总里程/km": 480.4, "日总里程/km": 1921.6, "平均装载率/%": 83.25, "装载率标准差": 14.76, "运行时间/s": 1.2971},
    {"算法": "模拟退火算法", "线路数": 15, "单次总里程/km": 480.4, "日总里程/km": 1921.6, "平均装载率/%": 83.25, "装载率标准差": 14.76, "运行时间/s": 0.5212},
]

GA_ROUTES = [
    ("路线1", "GT→S04→S08→GT", 38.00, 30.9, 95.00),
    ("路线2", "GT→S12→S09→GT", 37.75, 44.3, 94.38),
    ("路线3", "GT→S13→GT", 27.75, 19.2, 69.38),
    ("路线4", "GT→S05→S21→GT", 40.00, 24.4, 100.00),
    ("路线5", "GT→S02→GT", 25.25, 31.2, 63.12),
    ("路线6", "GT→S06→S18→GT", 35.00, 34.2, 87.50),
    ("路线7", "GT→S11→GT", 26.00, 36.4, 65.00),
    ("路线8", "GT→S16→S20→GT", 37.75, 29.8, 94.38),
    ("路线9", "GT→S10→GT", 22.25, 29.4, 55.62),
    ("路线10", "GT→S14→S22→GT", 32.50, 33.4, 81.25),
    ("路线11", "GT→S01→S17→GT", 39.75, 33.5, 99.38),
    ("路线12", "GT→S24→GT", 30.00, 21.4, 75.00),
    ("路线13", "GT→S03→S07→GT", 39.25, 37.8, 98.12),
    ("路线14", "GT→S15→GT", 29.00, 36.4, 72.50),
    ("路线15", "GT→S19→S23→GT", 39.25, 38.1, 98.12),
]

COLORS = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2"]


def cn_title(size=44):
    return ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", size)


def cn(size=30):
    return ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", size)


def en(size=28):
    return ImageFont.truetype("C:/Windows/Fonts/times.ttf", size)


def draw_axes(draw, ml, mt, pw, ph, y_max, y_step, y_label, x_label, title, right_label=None):
    W = ml + pw + 160
    draw.text((W / 2, 58), title, font=cn_title(), anchor="mm", fill="#222")
    draw.line((ml, mt, ml, mt + ph), fill="#333", width=3)
    draw.line((ml, mt + ph, ml + pw, mt + ph), fill="#333", width=3)
    tick_values = (
        [round(i * y_step, 2) for i in range(int(round(y_max / y_step)) + 1)]
        if y_step < 1
        else list(range(0, int(y_max) + 1, int(y_step)))
    )
    for v in tick_values:
        y = mt + ph - ph * v / y_max
        draw.line((ml - 8, y, ml + pw, y), fill="#dddddd", width=1)
        draw.text((ml - 18, y), f"{v:g}", font=en(), anchor="rm", fill="#333")
    draw.text((ml + pw / 2, mt + ph + 95), x_label, font=cn(), anchor="mm", fill="#222")
    draw.text((56, mt + ph / 2), y_label, font=cn(), anchor="mm", fill="#222")
    if right_label:
        draw.line((ml + pw, mt, ml + pw, mt + ph), fill="#666", width=3)
        draw.text((ml + pw + 115, mt + ph / 2), right_label, font=cn(), anchor="mm", fill="#222")


def bar_chart(metric, title, y_label, path, y_max=None, y_step=None, fmt="{:.1f}"):
    W, H = 1700, 1000
    ml, mt, mr, mb = 190, 130, 100, 220
    pw, ph = W - ml - mr, H - mt - mb
    vals = [r[metric] for r in RESULTS]
    y_max = y_max or math.ceil(max(vals) * 1.18)
    y_step = y_step or max(1, math.ceil(y_max / 7))
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    draw_axes(d, ml, mt, pw, ph, y_max, y_step, y_label, "算法类型", title)
    group = pw / len(vals)
    bw = group * 0.54
    for i, (name, val) in enumerate(zip(ALGORITHMS, vals)):
        cx = ml + group * (i + 0.5)
        y1 = mt + ph
        y0 = y1 - ph * val / y_max
        d.rectangle((cx - bw / 2, y0, cx + bw / 2, y1), fill=COLORS[i])
        d.text((cx, y0 - 15), fmt.format(val), font=en(30), anchor="mb", fill="#222")
        d.text((cx, y1 + 44), name.replace("算法", ""), font=cn(27), anchor="mm", fill="#222")
    img.save(path)


def fig_4_3(path):
    W, H = 1800, 1050
    ml, mt, mr, mb = 190, 130, 190, 260
    pw, ph = W - ml - mr, H - mt - mb
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    draw_axes(d, ml, mt, pw, ph, 100, 20, "平均装载率（%）", "算法类型", "图4-3 五种算法平均装载率与装载率标准差对比图", "装载率标准差")
    for v in range(0, 21, 5):
        y = mt + ph - ph * v / 20
        d.text((ml + pw + 18, y), str(v), font=en(), anchor="lm", fill="#333")
    group = pw / len(RESULTS)
    bw = group * 0.28
    for i, row in enumerate(RESULTS):
        cx = ml + group * (i + 0.5)
        v1 = row["平均装载率/%"]
        y1 = mt + ph
        y0 = y1 - ph * v1 / 100
        d.rectangle((cx - bw - 8, y0, cx - 8, y1), fill="#4C78A8")
        d.text((cx - bw / 2 - 8, y0 - 12), f"{v1:.1f}%", font=en(25), anchor="mb", fill="#222")
        v2 = row["装载率标准差"]
        y02 = y1 - ph * v2 / 20
        d.rectangle((cx + 8, y02, cx + bw + 8, y1), fill="#F58518")
        d.text((cx + bw / 2 + 8, y02 - 12), f"{v2:.2f}", font=en(25), anchor="mb", fill="#222")
        d.text((cx, y1 + 44), row["算法"].replace("算法", ""), font=cn(27), anchor="mm", fill="#222")
    d.rectangle((W / 2 - 180, H - 95, W / 2 - 145, H - 70), fill="#4C78A8")
    d.text((W / 2 - 130, H - 82), "平均装载率", font=cn(28), anchor="lm", fill="#222")
    d.rectangle((W / 2 + 35, H - 95, W / 2 + 70, H - 70), fill="#F58518")
    d.text((W / 2 + 85, H - 82), "装载率标准差", font=cn(28), anchor="lm", fill="#222")
    img.save(path)


def fig_4_4(path):
    W, H = 1700, 1000
    ml, mt, mr, mb = 210, 130, 100, 220
    pw, ph = W - ml - mr, H - mt - mb
    vals = [math.log10(r["运行时间/s"]) for r in RESULTS]
    labels = [r["运行时间/s"] for r in RESULTS]
    ymin, ymax = -4.3, 0.3
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    d.text((W / 2, 58), "图4-4 五种算法运行时间对比图", font=cn_title(), anchor="mm", fill="#222")
    d.line((ml, mt, ml, mt + ph), fill="#333", width=3)
    d.line((ml, mt + ph, ml + pw, mt + ph), fill="#333", width=3)
    for tick in [-4, -3, -2, -1, 0]:
        y = mt + ph - ph * (tick - ymin) / (ymax - ymin)
        d.line((ml - 8, y, ml + pw, y), fill="#ddd", width=1)
        d.text((ml - 18, y), f"10^{tick}", font=en(), anchor="rm", fill="#333")
    group = pw / len(vals)
    bw = group * 0.54
    for i, val in enumerate(vals):
        cx = ml + group * (i + 0.5)
        y1 = mt + ph
        y0 = y1 - ph * (val - ymin) / (ymax - ymin)
        d.rectangle((cx - bw / 2, y0, cx + bw / 2, y1), fill=COLORS[i])
        d.text((cx, y0 - 15), f"{labels[i]:.4f}", font=en(30), anchor="mb", fill="#222")
        d.text((cx, y1 + 44), ALGORITHMS[i].replace("算法", ""), font=cn(27), anchor="mm", fill="#222")
    d.text((ml + pw / 2, H - 75), "算法类型", font=cn(), anchor="mm", fill="#222")
    d.text((60, mt + ph / 2), "运行时间（s，对数坐标）", font=cn(), anchor="mm", fill="#222")
    img.save(path)


def fig_4_5(path):
    W, H = 1900, 1000
    ml, mt, mr, mb = 185, 130, 100, 210
    pw, ph = W - ml - mr, H - mt - mb
    vals = [row[4] for row in GA_ROUTES]
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    draw_axes(d, ml, mt, pw, ph, 120, 20, "装载率（%）", "遗传算法固定线路编号", "图4-5 遗传算法固定线路装载率分布图")
    group = pw / len(vals)
    bw = group * 0.58
    for i, val in enumerate(vals):
        cx = ml + group * (i + 0.5)
        y1 = mt + ph
        y0 = y1 - ph * val / 120
        color = "#54A24B" if val >= 80 else "#F58518"
        d.rectangle((cx - bw / 2, y0, cx + bw / 2, y1), fill=color)
        d.text((cx, y0 - 12), f"{val:.1f}%", font=en(24), anchor="mb", fill="#222")
        d.text((cx, y1 + 35), f"R{i+1}", font=en(27), anchor="mm", fill="#222")
    y100 = mt + ph - ph * 100 / 120
    d.line((ml, y100, ml + pw, y100), fill="#B00020", width=3)
    d.text((ml + pw - 5, y100 - 10), "100%容量上限", font=cn(27), anchor="rb", fill="#B00020")
    img.save(path)


def fig_4_6(path):
    W, H = 1900, 1050
    ml, mt, mr, mb = 180, 130, 90, 290
    pw, ph = W - ml - mr, H - mt - mb
    keys = ["单次总里程/km", "线路数", "运行时间/s", "平均装载率/%", "装载率标准差"]
    names = ["里程得分", "线路数得分", "计算效率得分", "装载率得分", "均衡性得分"]
    cols = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2"]
    series = {k: [r[k] for r in RESULTS] for k in keys}
    scores = []
    for idx, k in enumerate(keys):
        vals = series[k]
        mn, mx = min(vals), max(vals)
        if k == "平均装载率/%":
            scores.append([(v - mn) / (mx - mn) for v in vals])
        else:
            scores.append([(mx - v) / (mx - mn) for v in vals])
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    draw_axes(d, ml, mt, pw, ph, 1.0, 0.2, "归一化得分（越高越优）", "算法类型", "图4-6 五种算法综合结果汇总图")
    # redraw fractional y labels
    d.rectangle((0, mt - 10, ml - 12, mt + ph + 10), fill="white")
    d.line((ml, mt, ml, mt + ph), fill="#333", width=3)
    for v in [0, .2, .4, .6, .8, 1.0]:
        y = mt + ph - ph * v
        d.line((ml - 8, y, ml + pw, y), fill="#ddd", width=1)
        d.text((ml - 18, y), f"{v:.1f}", font=en(), anchor="rm", fill="#333")
    group = pw / len(RESULTS)
    bw = group * 0.13
    for i, row in enumerate(RESULTS):
        cx = ml + group * (i + 0.5)
        for j, sc in enumerate(scores):
            val = sc[i]
            x0 = cx + (j - 2) * bw * 1.12 - bw / 2
            x1 = x0 + bw
            y1 = mt + ph
            y0 = y1 - ph * val
            d.rectangle((x0, y0, x1, y1), fill=cols[j])
        d.text((cx, mt + ph + 44), row["算法"].replace("算法", ""), font=cn(27), anchor="mm", fill="#222")
    lx = W / 2 - 520
    ly = H - 120
    for j, name in enumerate(names):
        d.rectangle((lx + j * 205, ly, lx + j * 205 + 30, ly + 22), fill=cols[j])
        d.text((lx + j * 205 + 38, ly + 11), name, font=cn(24), anchor="lm", fill="#222")
    img.save(path)


FIGS = [
    (FIG_DIR / "图4-1_五种算法单次总里程对比图.png", lambda p: bar_chart("单次总里程/km", "图4-1 五种算法单次总里程对比图", "单次总里程（km）", p, 620, 100, "{:.1f}")),
    (FIG_DIR / "图4-2_五种算法线路数对比图.png", lambda p: bar_chart("线路数", "图4-2 五种算法线路数对比图", "固定循环线路数（条）", p, 20, 2, "{:.0f}")),
    (FIG_DIR / "图4-3_五种算法平均装载率与装载率标准差对比图.png", fig_4_3),
    (FIG_DIR / "图4-4_五种算法运行时间对比图.png", fig_4_4),
    (FIG_DIR / "图4-5_遗传算法固定线路装载率分布图.png", fig_4_5),
    (FIG_DIR / "图4-6_五种算法综合结果汇总图.png", fig_4_6),
]

for path, fn in FIGS:
    fn(path)


def esc(value):
    return escape(str(value))


def run(text, bold=False, size=24, sup=False):
    props = [
        f'<w:rFonts w:ascii="{EN_FONT}" w:hAnsi="{EN_FONT}" w:eastAsia="{CN_FONT}" w:cs="{EN_FONT}"/>',
        f'<w:sz w:val="{size}"/>',
        f'<w:szCs w:val="{size}"/>',
    ]
    if bold:
        props.append("<w:b/><w:bCs/>")
    if sup:
        props.append('<w:vertAlign w:val="superscript"/>')
    return "<w:r><w:rPr>" + "".join(props) + f'</w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


def para(text="", style=None, align=None, bold=False, size=24, first=True, before=0, after=120):
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')
    if first:
        ppr.append('<w:ind w:firstLineChars="200"/>')
    ppr.append(f'<w:spacing w:before="{before}" w:after="{after}" w:line="360" w:lineRule="auto"/>')
    return "<w:p><w:pPr>" + "".join(ppr) + "</w:pPr>" + run(text, bold=bold, size=size) + "</w:p>"


def paruns(parts, first=True, after=120):
    ppr = '<w:ind w:firstLineChars="200"/>' if first else ""
    runs = []
    for item in parts:
        if isinstance(item, tuple):
            text, is_sup = item
            runs.append(run(text, sup=is_sup, size=20 if is_sup else 24))
        else:
            runs.append(run(item))
    return f'<w:p><w:pPr>{ppr}<w:spacing w:after="{after}" w:line="360" w:lineRule="auto"/></w:pPr>' + "".join(runs) + "</w:p>"


def heading(text, level=1):
    return para(text, style=f"Heading{level}", bold=True, size=30 if level == 1 else 26, first=False, before=160, after=120)


def formula(text, num):
    return para(f"{text}        （{num}）", align="center", first=False, after=90)


def caption(text):
    return para(text, align="center", first=False, size=21, after=120)


def table_caption(text):
    return para(text, align="center", first=False, bold=True, size=22, after=80)


def table(headers, rows):
    cols = len(headers)
    grid = "".join('<w:gridCol w:w="1500"/>' for _ in range(cols))

    def cell(v, bold=False):
        return (
            '<w:tc><w:tcPr><w:tcW w:w="1500" w:type="dxa"/></w:tcPr>'
            '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="0" w:line="300" w:lineRule="auto"/></w:pPr>'
            + run(v, bold=bold, size=19)
            + "</w:p></w:tc>"
        )

    xml = [
        '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/>'
        '<w:tblLook w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
        f"<w:tblGrid>{grid}</w:tblGrid>",
        "<w:tr>" + "".join(cell(h, True) for h in headers) + "</w:tr>",
    ]
    for row in rows:
        xml.append("<w:tr>" + "".join(cell(v) for v in row) + "</w:tr>")
    xml.append("</w:tbl>")
    return "".join(xml) + para("", first=False, after=60)


def image_xml(rid, cx=5600000, cy=3300000):
    n = rid.replace("rId", "")
    return f'''
<w:p>
 <w:pPr><w:jc w:val="center"/><w:spacing w:after="80"/></w:pPr>
 <w:r><w:drawing>
  <wp:inline distT="0" distB="0" distL="0" distR="0"
   xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
   xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
   xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
   <wp:extent cx="{cx}" cy="{cy}"/>
   <wp:docPr id="{n}" name="Picture {n}"/>
   <wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
   <a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
    <pic:pic>
     <pic:nvPicPr><pic:cNvPr id="{n}" name="figure.png"/><pic:cNvPicPr/></pic:nvPicPr>
     <pic:blipFill><a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
     <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
    </pic:pic>
   </a:graphicData></a:graphic>
  </wp:inline>
 </w:drawing></w:r>
</w:p>'''


body = []
body.append(para("基于遗传算法的循环取货路径优化与物流平准化研究", align="center", bold=True, size=36, first=False, after=420))
body.append(para("课程论文修订稿", align="center", size=24, first=False, after=620))
body.append(heading("摘要", 1))
body.append(para("汽车零部件入厂物流具有供应商数量多、需求批量差异大、取货节拍稳定性要求高等特点。本文基于24个供应商、6类物流需求的教学研究用虚拟扩展数据，研究循环取货路径优化与物流平准化问题。扩展案例中单车容量为40 m³，固定取货频次为4次/天，单日总需求量为1998 m³，单次总需求量为499.5 m³。本文比较节点路径最短法、扫描法、节约里程法、遗传算法和模拟退火算法在运输效率、计算效率、运载质量和管理可实施性方面的表现。计算结果表明，遗传算法与模拟退火算法均得到15条固定循环线路、单次总里程480.4 km、日总里程1921.6 km、平均装载率83.25%的方案。模拟退火在本次运行中时间更短，但遗传算法在复杂约束表达、可扩展性和repair修复机制方面更适合作为本文核心方法。"))
body.append(para("关键词：循环取货；遗传算法；车辆路径问题；物流平准化；启发式算法；入厂物流", bold=True, first=False))

body.append(heading("第一章 引言", 1))
body.append(paruns(["车辆路径问题是物流配送与入厂取货优化的重要基础。Dantzig和Ramser较早提出车辆调度问题", ("[1]", True), "，为后续VRP研究奠定了基础。汽车零部件入厂物流具有多供应商、多品类、多频次和强节拍约束等特征，路径优化不仅影响运输成本，也影响准时化生产和线边库存稳定性。"]))
body.append(para("循环取货即Milk-run，是精益生产环境下常见的入厂物流组织方式。其核心在于由主机厂或第三方物流企业统一规划取货路线，车辆按照固定或半固定路径依次到供应商处取货，再返回工厂。本文聚焦24供应商扩展案例，不再采用原始案例与扩展案例的双层结构，而是围绕扩展数据主线展开建模、计算和方案筛选。"))

body.append(heading("第二章 理论基础与文献综述", 1))
body.append(paruns(["循环取货问题可视为带容量约束车辆路径问题在入厂物流中的应用。Laporte对VRP精确算法与近似算法进行了系统综述", ("[7]", True), "，Toth和Vigo从模型和算法角度进一步整理了车辆路径问题研究体系", ("[8]", True), "。在启发式算法中，节约里程法由Clarke和Wright提出", ("[2]", True), "，扫描法由Gillett和Miller提出", ("[3]", True), "，二者均适合作为路径优化的基准构造方法。"]))
body.append(paruns(["遗传算法由Holland提出", ("[4]", True), "，并经Goldberg系统化应用于搜索与优化问题", ("[5]", True), "。模拟退火算法由Kirkpatrick等引入组合优化领域", ("[6]", True), "。与单纯构造型启发式算法相比，遗传算法和模拟退火算法更适合在较大组合空间中搜索高质量解，但也需要更多参数设置与计算时间。"]))

body.append(heading("第三章 扩展案例数据与问题定义", 1))
body.append(para("本文使用的扩展数据为教学研究用虚拟数据，包含24家供应商、6类物流需求、固定取货频次4次/天和单车容量40 m³。该数据用于提高课程论文算例复杂度，并不代表企业真实运营数据。每家供应商的单次取货量由日需求量平均分摊得到。"))
body.append(formula("p_i=q_i/4", 1))
body.append(formula("Σq_i=1998 m³，Σp_i=1998/4=499.5 m³", 2))
body.append(formula("m_0=ceil(499.5/40)=13", 3))
body.append(para("式（3）给出的13辆车只是体积下界。由于供应商单次需求不可拆分，实际可行线路数还受到供应商需求组合结构影响。因此，本文通过多种算法构造可执行线路，并在结果比较基础上筛选核心方法。"))

body.append(heading("第四章 算法比较、计算过程与方案筛选", 1))
body.append(heading("4.1 扩展案例下的算法比较思路", 2))
body.append(para("在24个供应商、6类物流需求的扩展案例中，循环取货路径优化问题的复杂度明显提高。该扩展数据为教学研究用虚拟数据，目的在于增加供应商数量、物流品类和需求结构差异，从而更充分地比较不同启发式与元启发式算法在入厂物流路径优化中的适用性。扩展案例中，单车容量为40 m³，固定取货频次为4次/天，单日总需求量为1998 m³，单次总需求量为499.5 m³。"))
body.append(para("本章比较的算法包括节点路径最短法、扫描法、节约里程法、遗传算法和模拟退火算法。比较维度包括四个方面：运输效率，主要考察线路数、单次总里程和日总里程；计算效率，主要考察算法运行时间；运载质量，主要考察平均装载率和装载率标准差；管理可实施性，主要考察算法结果是否便于形成固定线路、固定频次和固定取货量的平准化执行方案。"))
body.append(table_caption("表4-1 五种算法综合结果表"))
body.append(table(["算法", "线路数", "单次总里程/km", "日总里程/km", "平均装载率", "装载率标准差", "运行时间/s"], [
    [r["算法"], str(r["线路数"]), f'{r["单次总里程/km"]:.1f}', f'{r["日总里程/km"]:.1f}', f'{r["平均装载率/%"]:.2f}%', f'{r["装载率标准差"]:.2f}', f'{r["运行时间/s"]:.4f}'] for r in RESULTS
]))
body.append(heading("4.2 节点路径最短法的计算逻辑与结果", 2))
body.append(para("节点路径最短法可理解为最近邻法，其基本思想是车辆从GT出发，在未访问且满足剩余容量约束的供应商中，选择距离当前位置最近的供应商作为下一访问节点；当当前车辆无法继续装载任何未服务供应商时，结束该线路并返回GT，再启用下一辆车继续服务剩余供应商。"))
body.append(para("在本案例中，该方法首先将24个供应商均标记为未访问；其次从GT出发，计算当前位置到所有未访问供应商的距离；再次在满足容量约束的候选供应商中选择距离最近者加入当前线路，并更新车辆剩余容量；最后当当前车辆无法继续加入供应商时，该线路闭合为“GT—若干供应商—GT”。计算结果表明，节点路径最短法得到16条线路，单次总里程555.6 km，日总里程2222.4 km，平均装载率78.05%，装载率标准差16.59，运行时间0.0001 s。该方法速度最快，但局部贪心特征明显，难以充分适应扩展案例的组合复杂性。"))
body.append(image_xml("rId2"))
body.append(caption("图4-1 五种算法单次总里程对比图"))
body.append(heading("4.3 扫描法的计算逻辑与结果", 2))
body.append(para("扫描法是一种基于空间分布特征的路径构造方法。其基本思想是以GT为原点，计算各供应商相对于GT的极角，然后按照极角从小到大排序，并沿着角度方向逐步将供应商划入车辆线路。当当前线路累计单次取货量超过车辆容量之前，继续加入下一个供应商；若加入后将超过40 m³，则结束当前线路并开启新线路。"))
body.append(formula("θ_i=arctan(y_i/x_i)", 4))
body.append(para("扫描法计算结果为18条线路，单次总里程536.9 km，日总里程2147.6 km，平均装载率69.38%，装载率标准差12.56，运行时间0.0011 s。与节点路径最短法相比，扫描法的单次总里程有所降低，说明按空间区域组织线路能够减少部分跨区域绕行。但扫描法得到的线路数最多，平均装载率最低，说明仅依据空间极角分组容易造成车辆容量利用不足。"))
body.append(image_xml("rId3"))
body.append(caption("图4-2 五种算法线路数对比图"))
body.append(heading("4.4 节约里程法的计算逻辑与结果", 2))
body.append(para("节约里程法的基本思想是：初始状态下，每个供应商分别由一条单独线路服务，即GT—供应商—GT。若将两个供应商合并到同一条线路中，则可节约的里程为："))
body.append(formula("S_ij=d_0i+d_0j-d_ij", 5))
body.append(para("在本案例中，节约里程法首先计算所有供应商两两组合的节约值，并按节约值从大到小排序。随后依次尝试合并线路，只有在满足车辆容量约束且合并后不破坏线路端点结构的情况下才执行合并。计算结果显示，节约里程法得到17条线路，单次总里程527.8 km，日总里程2111.2 km，平均装载率73.46%，装载率标准差14.75，运行时间0.0003 s。该方法解释性较强，适合作为基准方案或初始解生成方法，但仍难以充分搜索复杂线路划分与访问顺序组合。"))
body.append(image_xml("rId4"))
body.append(caption("图4-3 五种算法平均装载率与装载率标准差对比图"))
body.append(heading("4.5 遗传算法的计算逻辑与结果", 2))
body.append(para("遗传算法是一种群体搜索型元启发式算法，适合处理路径排序、车辆分组和容量约束同时存在的组合优化问题。在本案例中，遗传算法采用“供应商排列—解码分割”的思路。染色体由24个供应商编号组成，每个供应商在染色体中出现一次。解码阶段根据车辆容量40 m³，将供应商序列切分为若干固定循环线路，并对线路内部访问顺序进行距离评价。"))
body.append(formula("C=Z+αM+βσ_ρ+λP", 6))
body.append(formula("Fitness=1/C", 7))
body.append(para("其中，Z为单次总里程，M为线路数，σ_ρ为装载率标准差，P为违反容量约束或供应商遗漏、重复等不可行惩罚项。算法通过选择、交叉和变异操作不断更新种群，并通过repair修复机制处理供应商重复、遗漏和线路超载。计算结果显示，遗传算法得到15条固定循环线路，单次总里程480.4 km，日总里程1921.6 km，平均装载率83.25%，装载率标准差14.76，运行时间1.2971 s。"))
body.append(table_caption("表4-2 遗传算法15条固定循环线路结果表"))
body.append(table(["线路", "固定循环路线", "单次载重/m³", "单次里程/km", "装载率"], [[a, b, f"{c:.2f}", f"{d:.1f}", f"{e:.2f}%"] for a, b, c, d, e in GA_ROUTES]))
body.append(image_xml("rId5"))
body.append(caption("图4-4 五种算法运行时间对比图"))
body.append(image_xml("rId6", cx=5800000, cy=3050000))
body.append(caption("图4-5 遗传算法固定线路装载率分布图"))
body.append(heading("4.6 模拟退火算法的计算逻辑与结果", 2))
body.append(para("模拟退火算法是一种基于邻域搜索的元启发式算法。其基本思想是从一个初始解出发，通过交换、插入、逆序等邻域操作生成新解；若新解优于当前解，则直接接受；若新解劣于当前解，则以一定概率接受，以避免算法过早陷入局部最优。其接受概率通常表示为："))
body.append(formula("P=exp(-ΔC/T)", 8))
body.append(para("在本案例中，模拟退火算法以已有可行解作为初始方案，通过随机交换供应商位置、移动供应商位置和逆序局部片段等方式改变路径结构。每次扰动后，重新按照容量约束解码为固定循环线路，并计算单次总里程、线路数量和装载质量。计算结果显示，模拟退火算法得到15条线路，单次总里程480.4 km，日总里程1921.6 km，平均装载率83.25%，装载率标准差14.76，运行时间0.5212 s。本次运行中，模拟退火取得了与遗传算法相同的运输结果，且运行时间更短。"))
body.append(heading("4.7 综合比较与方案筛选", 2))
body.append(para("综合五种算法结果可以看出，不同算法具有不同优势。节点路径最短法、扫描法和节约里程法运行时间均极短，适合快速生成初始方案。其中，节点路径最短法逻辑最简单，扫描法能够反映供应商空间分布，节约里程法具有较强工程解释性。但这三类方法均属于构造型启发式算法，在24供应商扩展案例中难以充分搜索复杂组合空间，最终线路数和总里程均不如遗传算法和模拟退火算法。"))
body.append(para("从运输效率看，遗传算法和模拟退火算法均得到15条线路、单次总里程480.4 km、日总里程1921.6 km，表现优于其他三种算法。从计算效率看，模拟退火算法运行时间为0.5212 s，低于遗传算法的1.2971 s；而三种构造型启发式算法运行时间更短，但解的质量相对较弱。从运载质量看，遗传算法和模拟退火算法平均装载率均为83.25%，高于其他算法；扫描法虽然装载率标准差最低，但其平均装载率仅为69.38%，车辆容量利用不足。"))
body.append(image_xml("rId7", cx=5800000, cy=3200000))
body.append(caption("图4-6 五种算法综合结果汇总图"))
body.append(para("因此，本文并不将遗传算法表述为所有单项指标下的绝对最优算法。就运行时间而言，模拟退火算法和构造型启发式算法更具优势；就解释性而言，节约里程法更易被现场管理人员理解；就空间分区而言，扫描法具有一定直观性。但从综合表现看，遗传算法在运输效率、线路数量、装载率、复杂约束表达和后续模型扩展方面更适合作为本文核心方法。尤其是在固定线路、固定频次和固定单次取货量的平准化要求下，遗传算法能够通过编码、适应度函数和repair修复机制同时处理线路划分与路径排序问题。基于上述比较，下一章将进一步围绕遗传算法展开模型构建，重点说明其决策变量、目标函数、约束条件、染色体编码和改进求解机制。"))

body.append(heading("第五章 改进后的遗传算法模型构建", 1))
body.append(para("基于第四章的比较结果，遗传算法被选为本文的核心方法。设供应商集合为N，GT为节点0，节点集合为V=N∪{0}。若线路r服务供应商集合N_r，则线路单次载重和单次里程分别为W_r=Σp_i与L_r。模型目标是在满足单车容量、供应商唯一服务和平准化执行约束的前提下，使单次总里程和固定线路数保持较优。遗传算法通过染色体编码表达供应商排列，通过解码分割形成固定线路，通过repair机制保持可行性，并可在后续进一步加入时间窗、装卸能力和库存约束。"))
body.append(heading("第六章 讨论：平准化约束与管理可实施性", 1))
body.append(para("加入平准化约束后，路径优化评价标准不能只看单次总里程。固定路线、固定频次和固定取货量能够降低供应商备货波动，减少调度沟通成本，并使GT厂区收货节拍更加稳定。遗传算法方案每天运行4轮，形成15条固定线路、60个日车次，虽然车辆数高于体积下界，但能够保证所有供应商在不可拆分取货条件下满足容量约束。"))
body.append(para("本文仍存在局限。第一，扩展数据为教学研究用虚拟数据，尚不能替代企业真实运营数据。第二，模型未加入严格时间窗、道路拥堵、装卸服务时间和线边库存容量。第三，当前结果以固定4次/天为前提，尚未进一步比较不同取货频次下的车辆数、库存和运输成本变化。"))
body.append(heading("第七章 结论", 1))
body.append(para("本文基于24供应商扩展数据研究循环取货路径优化与物流平准化问题。五种算法比较表明，最近邻法、扫描法和节约里程法适合快速生成基准方案，但在扩展数据中难以同时兼顾线路数、总里程和装载质量。遗传算法与模拟退火在本次运行中均取得单次总里程480.4 km、日总里程1921.6 km的结果，其中模拟退火运行时间更短，遗传算法在复杂约束表达、修复机制和多目标扩展方面更具综合优势。"))
body.append(para("因此，本文结论不是简单宣称遗传算法在所有指标下最优，而是认为遗传算法更适合作为GT类入厂物流循环取货路径优化的核心方法。其价值体现在能够把运输效率、容量可行性、固定线路和平准化执行统一到同一求解框架中，从而形成具有课程研究价值和工程可实施性的物流优化方案。"))
body.append(heading("参考文献", 1))
refs = [
    "[1] Dantzig G B, Ramser J H. The Truck Dispatching Problem[J]. Management Science, 1959, 6(1): 80-91.",
    "[2] Clarke G, Wright J W. Scheduling of Vehicles from a Central Depot to a Number of Delivery Points[J]. Operations Research, 1964, 12(4): 568-581.",
    "[3] Gillett B E, Miller L R. A Heuristic Algorithm for the Vehicle-Dispatch Problem[J]. Operations Research, 1974, 22(2): 340-349.",
    "[4] Holland J H. Adaptation in Natural and Artificial Systems[M]. Ann Arbor: University of Michigan Press, 1975.",
    "[5] Goldberg D E. Genetic Algorithms in Search, Optimization, and Machine Learning[M]. Reading: Addison-Wesley, 1989.",
    "[6] Kirkpatrick S, Gelatt C D, Vecchi M P. Optimization by Simulated Annealing[J]. Science, 1983, 220(4598): 671-680.",
    "[7] Laporte G. The Vehicle Routing Problem: An Overview of Exact and Approximate Algorithms[J]. European Journal of Operational Research, 1992, 59(3): 345-358.",
    "[8] Toth P, Vigo D, editors. The Vehicle Routing Problem[M]. Philadelphia: SIAM, 2002.",
]
for ref in refs:
    body.append(para(ref, first=False, after=80))


styles = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
 <w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="{EN_FONT}" w:hAnsi="{EN_FONT}" w:eastAsia="{CN_FONT}" w:cs="{EN_FONT}"/><w:sz w:val="24"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
 <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:rPr><w:rFonts w:ascii="{EN_FONT}" w:hAnsi="{EN_FONT}" w:eastAsia="{CN_FONT}" w:cs="{EN_FONT}"/><w:sz w:val="24"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:outlineLvl w:val="0"/><w:spacing w:before="240" w:after="120"/></w:pPr><w:rPr><w:b/><w:rFonts w:ascii="{EN_FONT}" w:hAnsi="{EN_FONT}" w:eastAsia="{CN_FONT}" w:cs="{EN_FONT}"/><w:sz w:val="30"/></w:rPr></w:style>
 <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:outlineLvl w:val="1"/><w:spacing w:before="180" w:after="100"/></w:pPr><w:rPr><w:b/><w:rFonts w:ascii="{EN_FONT}" w:hAnsi="{EN_FONT}" w:eastAsia="{CN_FONT}" w:cs="{EN_FONT}"/><w:sz w:val="26"/></w:rPr></w:style>
 <w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:basedOn w:val="TableNormal"/><w:qFormat/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4" w:color="666666"/><w:left w:val="single" w:sz="4" w:color="666666"/><w:bottom w:val="single" w:sz="4" w:color="666666"/><w:right w:val="single" w:sz="4" w:color="666666"/><w:insideH w:val="single" w:sz="4" w:color="666666"/><w:insideV w:val="single" w:sz="4" w:color="666666"/></w:tblBorders></w:tblPr></w:style>
</w:styles>'''

document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
 xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 mc:Ignorable="w14 wp14">
 <w:body>{''.join(body)}
 <w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="851" w:footer="992"/><w:cols w:space="425"/><w:docGrid w:type="lines" w:linePitch="312"/></w:sectPr>
 </w:body>
</w:document>'''

content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="xml" ContentType="application/xml"/>
 <Default Extension="png" ContentType="image/png"/>
 <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
 <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
 <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
 <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''
rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'''
doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
 <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_1.png"/>
 <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_2.png"/>
 <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_3.png"/>
 <Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_4.png"/>
 <Relationship Id="rId6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_5.png"/>
 <Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/fig4_6.png"/>
</Relationships>'''

now = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>基于遗传算法的循环取货路径优化与物流平准化研究</dc:title><dc:creator>Codex</dc:creator><cp:lastModifiedBy>Codex</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>'''
app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Microsoft Word</Application></Properties>'''

with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document)
    z.writestr("word/_rels/document.xml.rels", doc_rels)
    z.writestr("word/styles.xml", styles)
    for i, (path, _) in enumerate(FIGS, start=1):
        z.writestr(f"word/media/fig4_{i}.png", path.read_bytes())
    z.writestr("docProps/core.xml", core)
    z.writestr("docProps/app.xml", app)

print(OUT.resolve())
