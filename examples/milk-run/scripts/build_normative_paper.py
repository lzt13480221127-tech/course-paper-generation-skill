from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape
from PIL import Image
import re
import shutil


OUT = Path.cwd()
FIG_DIR = OUT / "paper_figures_output"
DOCX_OUT = OUT / "规范课程论文_可编辑流程图版.docx"
FIG_LIST = OUT / "图片清单.md"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC_NS = "http://schemas.openxmlformats.org/drawingml/2006/picture"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"

EMU_PER_INCH = 914400
TWIPS_PER_INCH = 1440


class DocBuilder:
    def __init__(self):
        self.body = []
        self.rels = []
        self.media = []
        self.rid = 1
        self.pic_id = 1

    def _rpr(self, bold=False, size=24, color=None, superscript=False):
        parts = [
            '<w:rPr>',
            '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="宋体"/>',
            f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>',
        ]
        if bold:
            parts.append("<w:b/><w:bCs/>")
        if color:
            parts.append(f'<w:color w:val="{color}"/>')
        if superscript:
            parts.append('<w:vertAlign w:val="superscript"/>')
            parts.append('<w:sz w:val="18"/><w:szCs w:val="18"/>')
        parts.append("</w:rPr>")
        return "".join(parts)

    def _runs(self, text, bold=False, size=24, sup_refs=True, color=None):
        pieces = []
        if sup_refs:
            pos = 0
            for m in re.finditer(r"\[(\d+)\]", text):
                if m.start() > pos:
                    pieces.append(self._run(text[pos:m.start()], bold, size, color))
                pieces.append(self._run(m.group(0), bold, size, color, superscript=True))
                pos = m.end()
            if pos < len(text):
                pieces.append(self._run(text[pos:], bold, size, color))
            return "".join(pieces)
        return self._run(text, bold, size, color)

    def _run(self, text, bold=False, size=24, color=None, superscript=False):
        if text == "":
            return ""
        return f"<w:r>{self._rpr(bold=bold, size=size, color=color, superscript=superscript)}<w:t xml:space=\"preserve\">{escape(text)}</w:t></w:r>"

    def paragraph(self, text="", style="body", bold=False, size=None, align="left", sup_refs=True):
        if style == "title":
            ppr = '<w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr>'
            size = size or 32
            bold = True
        elif style == "abstract-title":
            ppr = '<w:pPr><w:jc w:val="center"/><w:spacing w:before="180" w:after="120"/></w:pPr>'
            size = size or 26
            bold = True
        elif style == "heading1":
            ppr = '<w:pPr><w:spacing w:before="300" w:after="160"/><w:outlineLvl w:val="0"/></w:pPr>'
            size = size or 28
            bold = True
        elif style == "heading2":
            ppr = '<w:pPr><w:spacing w:before="180" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr>'
            size = size or 25
            bold = True
        elif style == "caption":
            ppr = '<w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="160"/></w:pPr>'
            size = size or 21
        elif style == "formula":
            ppr = '<w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="80"/></w:pPr>'
            size = size or 23
        elif style == "reference":
            ppr = '<w:pPr><w:spacing w:after="80"/><w:ind w:hanging="420"/></w:pPr>'
            size = size or 21
            sup_refs = False
        else:
            jc = f'<w:jc w:val="{align}"/>' if align != "left" else ""
            ppr = f'<w:pPr>{jc}<w:spacing w:line="360" w:lineRule="auto" w:after="80"/><w:ind w:firstLine="480"/></w:pPr>'
            size = size or 24
        self.body.append(f"<w:p>{ppr}{self._runs(text, bold=bold, size=size, sup_refs=sup_refs)}</w:p>")

    def table(self, rows, caption=None):
        if caption:
            self.paragraph(caption, style="caption", bold=True)
        cols = len(rows[0])
        grid = "".join([f'<w:gridCol w:w="{int(9000 / cols)}"/>' for _ in range(cols)])
        out = [
            '<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/>',
            '<w:tblBorders><w:top w:val="single" w:sz="8" w:color="4F81BD"/>',
            '<w:left w:val="single" w:sz="4" w:color="D9E2F3"/><w:bottom w:val="single" w:sz="8" w:color="4F81BD"/>',
            '<w:right w:val="single" w:sz="4" w:color="D9E2F3"/><w:insideH w:val="single" w:sz="4" w:color="D9E2F3"/>',
            '<w:insideV w:val="single" w:sz="4" w:color="D9E2F3"/></w:tblBorders></w:tblPr>',
            f"<w:tblGrid>{grid}</w:tblGrid>",
        ]
        for r_idx, row in enumerate(rows):
            out.append("<w:tr>")
            for cell in row:
                shade = "4F81BD" if r_idx == 0 else ("F2F2F2" if r_idx % 2 == 0 else "FFFFFF")
                color = "FFFFFF" if r_idx == 0 else None
                out.append(
                    f'<w:tc><w:tcPr><w:shd w:fill="{shade}"/><w:tcMar>'
                    '<w:top w:w="80" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
                    '<w:bottom w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/>'
                    '</w:tcMar></w:tcPr>'
                    '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
                    f'{self._runs(str(cell), bold=(r_idx == 0), size=21, sup_refs=False, color=color)}</w:p></w:tc>'
                )
            out.append("</w:tr>")
        out.append("</w:tbl>")
        self.body.append("".join(out))
        self.paragraph("")

    def editable_flowchart(self, title, steps, caption):
        self.paragraph(title, style="caption", bold=True, size=24)
        out = [
            '<w:tbl><w:tblPr><w:jc w:val="center"/><w:tblW w:w="7600" w:type="dxa"/></w:tblPr>',
            '<w:tblGrid><w:gridCol w:w="7600"/></w:tblGrid>',
        ]
        for idx, step in enumerate(steps):
            out.append(
                '<w:tr><w:tc><w:tcPr><w:tcW w:w="7600" w:type="dxa"/>'
                '<w:tcBorders><w:top w:val="single" w:sz="10" w:color="000000"/>'
                '<w:left w:val="single" w:sz="10" w:color="000000"/>'
                '<w:bottom w:val="single" w:sz="10" w:color="000000"/>'
                '<w:right w:val="single" w:sz="10" w:color="000000"/></w:tcBorders>'
                '<w:tcMar><w:top w:w="120" w:type="dxa"/><w:left w:w="120" w:type="dxa"/>'
                '<w:bottom w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar></w:tcPr>'
                '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
                f'{self._runs(step, size=22, sup_refs=False)}</w:p></w:tc></w:tr>'
            )
            if idx < len(steps) - 1:
                out.append(
                    '<w:tr><w:tc><w:tcPr><w:tcW w:w="7600" w:type="dxa"/>'
                    '<w:tcMar><w:top w:w="0" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/></w:tcMar></w:tcPr>'
                    '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="0" w:before="0"/></w:pPr>'
                    f'{self._runs("↓", size=20, sup_refs=False)}</w:p></w:tc></w:tr>'
                )
        out.append("</w:tbl>")
        self.body.append("".join(out))
        self.paragraph(caption, style="caption")

    def editable_chromosome_diagram(self, caption):
        self.paragraph("改进遗传算法染色体编码与线路解码示意图", style="caption", bold=True, size=24)
        self.paragraph("染色体编码（示意）", style="heading2")
        genes = ["S03", "S08", "S01", "S11", "S04", "S17", "S06", "S05", "S14", "S09", "S22", "S15"]
        self.table([genes])
        self.paragraph("按容量约束解码", style="formula")
        self.paragraph("线路1：P → S03 → S08 → S01 → P")
        self.paragraph("线路2：P → S11 → S04 → S17 → P")
        self.paragraph("线路3：P → S06 → S05 → S14 → S09 → S22 → S15 → P")
        self.paragraph(caption, style="caption")

    def image(self, file_name, caption, width_inches=5.6):
        path = FIG_DIR / file_name
        if not path.exists():
            raise FileNotFoundError(path)
        with Image.open(path) as im:
            w, h = im.size
        height_inches = width_inches * h / w
        if height_inches > 6.2:
            height_inches = 6.2
            width_inches = height_inches * w / h
        cx = int(width_inches * EMU_PER_INCH)
        cy = int(height_inches * EMU_PER_INCH)
        rid = f"rId{self.rid}"
        self.rid += 1
        media_name = f"figure_{self.pic_id:02d}.png"
        target = f"media/{media_name}"
        self.rels.append((rid, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image", target))
        self.media.append((path, media_name))
        doc_pr_id = self.pic_id
        self.pic_id += 1
        drawing = f"""
        <w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="60"/></w:pPr><w:r><w:drawing>
        <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="{doc_pr_id}" name="Picture {doc_pr_id}"/><wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
        <a:graphic><a:graphicData uri="{PIC_NS}"><pic:pic>
        <pic:nvPicPr><pic:cNvPr id="{doc_pr_id}" name="{escape(file_name)}"/><pic:cNvPicPr/></pic:nvPicPr>
        <pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
        <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
        </pic:pic></a:graphicData></a:graphic>
        </wp:inline></w:drawing></w:r></w:p>
        """
        self.body.append(drawing)
        self.paragraph(caption, style="caption")

    def page_break(self):
        self.body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    def xml(self):
        sect = (
            '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
            '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>'
            '<w:cols w:space="425"/><w:docGrid w:linePitch="312"/></w:sectPr>'
        )
        ns = f'xmlns:w="{W_NS}" xmlns:r="{R_NS}" xmlns:wp="{WP_NS}" xmlns:a="{A_NS}" xmlns:pic="{PIC_NS}"'
        return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {ns}><w:body>{"".join(self.body)}{sect}</w:body></w:document>'

    def save(self, path):
        with ZipFile(path, "w", ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", content_types())
            z.writestr("_rels/.rels", package_rels())
            z.writestr("word/document.xml", self.xml())
            z.writestr("word/styles.xml", styles_xml())
            z.writestr("word/settings.xml", settings_xml())
            rel_items = [
                '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
                '<Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>',
            ]
            for rid, typ, target in self.rels:
                rel_items.append(f'<Relationship Id="{rid}" Type="{typ}" Target="{escape(target)}"/>')
            z.writestr("word/_rels/document.xml.rels", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="{REL_NS}">{"".join(rel_items)}</Relationships>')
            for src, name in self.media:
                z.write(src, f"word/media/{name}")


def content_types():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
</Types>"""


def package_rels():
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{REL_NS}">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""


def styles_xml():
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W_NS}">
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>
<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="宋体"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>
</w:styles>"""


def settings_xml():
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="{W_NS}"><w:defaultTabStop w:val="420"/><w:characterSpacingControl w:val="doNotCompress"/></w:settings>"""


def add_content(d: DocBuilder):
    d.paragraph("基于改进遗传算法的循环取货路径优化与物流平准化研究", style="title")
    d.paragraph("课程论文", style="abstract-title")
    d.paragraph("摘  要", style="abstract-title")
    d.paragraph("汽车零部件入厂物流具有供应商数量多、需求批量差异大、取货节拍稳定性要求高等特点。本文以24家供应商、6类物流需求的教学研究用虚拟扩展数据为对象，在固定取货4次/天、单车容量40 m³、供应商单次需求不可拆分的前提下，研究循环取货路径优化与物流平准化问题。文中首先梳理循环取货与车辆路径问题的理论基础，随后构建包含节约里程法、VRP扫描法、模拟退火算法和改进遗传算法的比较框架。在运输效率、计算效率、运载质量和管理可实施性四个维度下，四种算法的结果表明：模拟退火算法与改进遗传算法均得到15条固定循环线路、单次总里程480.4 km、日总里程1921.6 km、平均装载率83.25%的方案；其中模拟退火算法在本次运行中的时间更短，而改进遗传算法在编码表达、约束修复、多目标扩展以及平准化执行适配方面更具综合优势。")
    d.paragraph("关键词：循环取货；改进遗传算法；车辆路径问题；物流平准化；启发式算法；入厂物流")

    d.paragraph("一、引言", style="heading1")
    d.paragraph("车辆路径问题是物流配送与入厂取货优化的重要基础。汽车零部件入厂物流属于典型的多供应商、多品类、多频次场景，路径优化不仅影响运输成本，而且关系到准时化生产、线边补给和现场节拍控制。循环取货（Milk-run）是精益生产环境中应用广泛的入厂物流组织方式。与供应商各自送货相比，主机厂或第三方物流企业通过统一规划车辆路线，可以降低重复运输、提高装载率，并减少厂区到货波动。")
    d.paragraph("对于汽车企业而言，循环取货的目标并非单纯压缩里程，而是在成本、频次、容量约束和执行稳定性之间取得平衡。已有案例能够说明循环取货路径优化的基本逻辑，但在算法比较与复杂约束表达方面仍显不足。为更充分体现遗传算法在组合优化中的优势，本文引入24家供应商、6类物流需求的教学研究用虚拟扩展数据，以同一数据集对多种算法进行比较，并以改进遗传算法作为后续模型深化的主线。")
    d.paragraph("本文的研究目标包括：第一，在统一扩展数据与平准化约束条件下比较四种算法的表现，避免预设某一算法必然最优；第二，系统展示各算法的公式、计算逻辑、计算过程与计算结果，并通过图表说明差异；第三，在综合比较基础上，以改进遗传算法为核心构建适用于固定路线、固定频次和固定取货量的循环取货优化模型。")

    d.paragraph("二、文献综述", style="heading1")
    d.paragraph("车辆路径问题（Vehicle Routing Problem，VRP）研究如何在给定配送中心、需求点和约束条件下安排车辆服务路径，使总体运输成本最低。循环取货问题可以视为VRP在入厂物流场景中的典型应用，其本质在于车辆从中心节点出发，依次访问多个供应商并返回中心节点。在农产品配送、企业配送与冷链物流等应用中，节约里程法常被用于构造可解释的初始线路方案[1][4][5]。")
    d.paragraph("在构造型启发式算法中，VRP扫描法通过极角排序实现区域性分组，适合空间分布较规则的场景；节约里程法通过计算合并两条独立线路的节约值来构造方案，工程解释性强。已有连锁超市生鲜配送研究表明，扫描法能够快速完成区域聚类并降低人工分组难度[8]。多点物流配送车辆路径研究也说明，VRP模型的求解质量取决于容量、距离与节点组合结构的共同作用[9]。")
    d.paragraph("在元启发式算法中，模拟退火算法通过概率接受劣解跳出局部最优，适合路径邻域搜索；相关研究已将模拟退火与路径规划算法结合，用于提升复杂场景下的搜索质量[2]。遗传算法则通过种群并行搜索保留多种候选结构，并能通过适应度函数同时表达总里程、车辆数、装载率和约束惩罚。近年来，改进遗传算法在路径规划中的编码方式、交叉变异与修复机制不断完善[3]，并已用于快递配送与企业运输路径优化[6]。结合本文研究对象，循环取货路径优化不仅包含供应商分组问题，还涉及组内访问顺序、容量约束和平准化执行要求。因此，本研究将构造型启发式算法与元启发式算法同时纳入比较框架。")

    d.paragraph("三、A公司场景描述、问题界定与模型构建", style="heading1")
    d.paragraph("本文采用的扩展案例数据为教学研究用虚拟数据集，共包含24家供应商、6类物流需求以及以A公司总装工厂GT为中心构造的对称距离矩阵。供应商的物流需求类型包括标准件、电子件、结构件、大件模块、外饰件和包装耗材。单车容量设定为40 m³，固定取货频次为每天4次，即每天将同一批供应商按相同线路和相同取货量重复执行4轮。")
    d.paragraph("设供应商日需求量为 q_i，单次取货量为 p_i，则在固定4次/天的约束下，单次取货量可由式（1）得到：")
    d.paragraph("p_i = q_i / 4", style="formula")
    d.paragraph("对24家供应商的日需求量求和，可得单日总需求量为1998 m³；进一步除以4，可得单次总需求量为499.5 m³。由此得到：")
    d.paragraph("Σq_i = 1998 m³，Σp_i = 1998 / 4 = 499.5 m³", style="formula")
    d.paragraph("若仅从体积角度考虑，最少车辆数下界可由式（2）估算：")
    d.paragraph("m₀ = ceil(Σp_i / Q) = ceil(499.5 / 40) = 13", style="formula")
    d.paragraph("13辆车只是体积意义上的理论下界，并不等同于可执行车辆数。由于本文保留“供应商单次需求不可拆分”的假设，且多家供应商单次需求超过20 m³，车辆实际可行线路数还受到需求组合结构的影响，因此需要借助具体算法生成满足容量约束的固定循环线路。")
    d.table([
        ["指标", "数值", "说明"],
        ["供应商数量", "24家", "由原案例扩展，用于提高问题规模"],
        ["物流种类", "6类", "标准件、电子件、结构件、大件模块、外饰件、包装耗材"],
        ["单车容量", "40 m³", "与原案例保持一致"],
        ["固定取货频次", "4次/天", "满足取货平准化假设"],
        ["单日总需求量", "1998 m³", "由供应商数据汇总"],
        ["单次总需求量", "499.5 m³", "单日总需求量 / 4"],
        ["体积下界", "13辆", "ceil(499.5 / 40)"],
    ], "表3-1：扩展数据关键参数")
    d.table([
        ["符号", "含义"],
        ["N", "供应商集合，N={1,2,…,24}"],
        ["V", "节点集合，V=N∪{0}，其中0表示GT"],
        ["Q", "车辆容量，Q=40 m³"],
        ["q_i", "供应商i的日需求量"],
        ["p_i", "供应商i的单次取货量"],
        ["d_ij", "节点i与节点j之间的距离"],
        ["x_ijr", "线路r中车辆是否从i行驶到j"],
        ["y_ir", "供应商i是否由线路r服务"],
    ], "表3-2：模型符号说明表")
    d.paragraph("模型目标是在满足容量约束、唯一服务约束和平准化执行约束的前提下，使单次总里程与线路数量保持较优，同时尽量控制装载率离散程度。若线路r服务的供应商序列为 i₁,i₂,…,i_k，则线路单次里程与总里程可写为：")
    d.paragraph("L_r = d_{0,i₁} + Σ d_{i_h,i_{h+1}} + d_{i_k,0}", style="formula")
    d.paragraph("Z = Σ_r L_r，Z_day = 4Z", style="formula")
    d.paragraph("容量约束与唯一服务约束分别为：")
    d.paragraph("W_r = Σ_{i∈N} p_i y_ir ≤ Q，Σ_r y_ir = 1", style="formula")
    d.table([
        ["评价维度", "指标", "计算或解释"],
        ["运输效率", "线路数M、单次总里程Z、日总里程Z_day", "线路越少、里程越低越优"],
        ["计算效率", "运行时间", "反映算法求解速度"],
        ["运载质量", "平均装载率、装载率标准差", "平均装载率越高、标准差越低越优"],
        ["管理可实施性", "固定路线、固定频次、固定取货量", "反映方案能否稳定执行"],
    ], "表3-3：评价指标表")

    d.paragraph("四、算法设计、求解过程与结果比较", style="heading1")
    d.paragraph("本章在统一的24家供应商扩展案例基础上，按节约里程法、VRP扫描法、模拟退火算法、改进遗传算法四类方法依次展开。原正文中作为快速基准的节点路径最短法用于说明局部最近原则的局限，但最终比较和图表嵌入以正文预留的四种算法编号为准。")
    d.paragraph("4.1 节约里程法", style="heading2")
    d.paragraph("节约里程法以“先单独配送、后逐步合并”为基本思路。若供应商i和j原本分别由两条独立线路服务，则将二者合并后可节约的里程为：")
    d.paragraph("S_ij = d_0i + d_0j - d_ij", style="formula")
    d.paragraph("算法首先将每个供应商视为一条独立线路；其次计算任意两供应商组合的节约值，并按节约值从大到小排序；再次依次尝试合并线路，仅当合并后不违反容量约束且不破坏线路端点结构时才执行合并。在扩展案例中，节约里程法得到17条固定线路，单次总里程为527.8 km，日总里程为2111.2 km，平均装载率为73.46%，装载率标准差为14.75，运行时间为0.0003 s。")
    d.image("图6-1_节约里程法节点节约值排序图.png", "图6-1：节约里程法节点节约值排序图", 5.7)
    d.table([
        ["路线", "固定循环路线"],
        ["路线1", "GT→S01→S05→GT"], ["路线2", "GT→S02→GT"], ["路线3", "GT→S03→S12→GT"],
        ["路线4", "GT→S04→S08→GT"], ["路线5", "GT→S06→S18→GT"], ["路线6", "GT→S07→S23→GT"],
        ["路线7", "GT→S09→GT"], ["路线8", "GT→S10→GT"], ["路线9", "GT→S11→GT"],
        ["路线10", "GT→S13→GT"], ["路线11", "GT→S14→S22→GT"], ["路线12", "GT→S15→GT"],
        ["路线13", "GT→S16→S20→GT"], ["路线14", "GT→S17→GT"], ["路线15", "GT→S19→GT"],
        ["路线16", "GT→S21→GT"], ["路线17", "GT→S24→GT"],
    ], "表4-1：节约里程法固定循环线路表")
    d.paragraph("由图6-1和表4-1可知，节约里程法能够优先合并共用干线路径较明显的供应商组合，因此相较简单局部路径法具有更好的工程解释性；但其局部合并策略仍不足以充分搜索复杂组合空间。")
    d.paragraph("4.2 VRP扫描法", style="heading2")
    d.paragraph("VRP扫描法通过空间角度排序来实现线路分组。设供应商i相对于GT的平面坐标为(x_i,y_i)，则极角可表示为：")
    d.paragraph("θ_i = arctan(y_i / x_i)", style="formula")
    d.paragraph("算法首先计算所有供应商的极角并按极角排序，随后沿着排序序列依次将供应商装入当前车辆；当再加入一个供应商会使当前载重超过40 m³时，即刻结束该线路并开启下一辆车。在本案例中，VRP扫描法得到18条固定线路，单次总里程为536.9 km，日总里程为2147.6 km，平均装载率为69.38%，装载率标准差为12.56，运行时间为0.0011 s。")
    d.table([
        ["路线", "固定循环路线"],
        ["路线1", "GT→S14→S22→GT"], ["路线2", "GT→S02→GT"], ["路线3", "GT→S06→S18→GT"],
        ["路线4", "GT→S09→GT"], ["路线5", "GT→S13→GT"], ["路线6", "GT→S05→S01→GT"],
        ["路线7", "GT→S21→GT"], ["路线8", "GT→S17→GT"], ["路线9", "GT→S12→S08→GT"],
        ["路线10", "GT→S24→GT"], ["路线11", "GT→S04→GT"], ["路线12", "GT→S16→S20→GT"],
        ["路线13", "GT→S03→GT"], ["路线14", "GT→S11→GT"], ["路线15", "GT→S19→GT"],
        ["路线16", "GT→S15→GT"], ["路线17", "GT→S07→S23→GT"], ["路线18", "GT→S10→GT"],
    ], "表4-2：VRP扫描法固定循环线路表")
    d.paragraph("表4-2说明，扫描法能够保持一定的空间分区特征，但由于其主要依据角度顺序分组，并不直接优化装载率，因此在需求异质性较强的情况下容易形成较多低载重线路。")
    d.paragraph("4.3 模拟退火算法", style="heading2")
    d.paragraph("模拟退火算法属于基于邻域搜索的元启发式方法。其基本过程是：从一个初始可行解出发，通过交换、插入和逆序等邻域操作生成新解；若新解优于当前解，则直接接受；若新解劣于当前解，则以一定概率接受，以避免搜索过早陷入局部最优。其接受概率可写为：")
    d.paragraph("P = exp(-ΔC / T)", style="formula")
    d.paragraph("其中，ΔC为新解相对当前解的成本增量，T为当前温度。本文将线路数量、单次总里程、装载率均衡性与容量惩罚统一纳入成本函数，再对供应商序列实施局部扰动并重新解码为固定线路。本次计算中，模拟退火算法得到15条固定线路，单次总里程为480.4 km，日总里程为1921.6 km，平均装载率为83.25%，装载率标准差为14.76，运行时间为0.5212 s。")
    d.image("图6-5_模拟退火算法收敛曲线图.png", "图6-5：模拟退火算法收敛曲线图", 5.6)
    d.table([
        ["路线", "固定循环路线"],
        ["路线1", "GT→S05→S21→GT"], ["路线2", "GT→S22→S14→GT"], ["路线3", "GT→S01→S17→GT"],
        ["路线4", "GT→S13→GT"], ["路线5", "GT→S10→GT"], ["路线6", "GT→S24→GT"],
        ["路线7", "GT→S06→S18→GT"], ["路线8", "GT→S03→S07→GT"], ["路线9", "GT→S15→GT"],
        ["路线10", "GT→S02→GT"], ["路线11", "GT→S19→S23→GT"], ["路线12", "GT→S11→GT"],
        ["路线13", "GT→S09→S12→GT"], ["路线14", "GT→S16→S20→GT"], ["路线15", "GT→S04→S08→GT"],
    ], "表4-3：模拟退火算法固定循环线路表")
    d.paragraph("图6-5显示，模拟退火算法在迭代过程中逐步降低目标函数值，最终收敛到480.4 km的单次总里程。表4-3对应的线路结果表明，该方法能够在当前参数下获得与改进遗传算法相同的运输结果。")
    d.paragraph("4.4 改进遗传算法", style="heading2")
    d.paragraph("改进遗传算法以种群并行搜索为基本特征，能够同时处理供应商排序、线路划分和容量可行性等组合决策。本文采用“供应商排列—解码分割”的染色体结构，即在染色体中仅保留24家供应商的排列顺序，再在解码阶段依据车辆容量约束将其切分为若干条固定循环线路。算法的综合成本函数定义为：")
    d.paragraph("C = Z + αM + βσ_ρ + λP，Fitness = 1 / C", style="formula")
    d.paragraph("其中，Z为单次总里程，M为固定线路数量，σ_ρ为装载率标准差，P为不可行惩罚项，α、β、λ为权重系数。算法采用锦标赛选择与精英保留完成选择操作，采用顺序交叉保持供应商排列的相对顺序，并使用交换、插入、逆序三类变异增强搜索多样性。为避免交叉和变异产生供应商重复、遗漏或超载线路，本文进一步引入repair修复机制，对不可行个体进行去重、补全与重新分配。")
    d.paragraph("在参数设置为种群规模120、迭代次数260、交叉概率0.86、变异概率0.22、精英保留个体数6、随机种子20260521的条件下，改进遗传算法得到15条固定循环线路，单次总里程为480.4 km，日总里程为1921.6 km，平均装载率为83.25%，装载率标准差为14.76，运行时间为1.2971 s。")

    d.paragraph("五、改进遗传算法模型构建与参数设计", style="heading1")
    d.paragraph("本章在第四章计算结果基础上，进一步说明改进遗传算法如何将固定频次、固定取货量和固定线路等管理要求嵌入统一优化模型。相较于单纯输出一组较短路径，本文更关注该算法是否能够形成可重复执行、便于管理的循环取货方案。")
    d.editable_flowchart(
        "改进遗传算法整体求解框架图",
        [
            "输入供应商需求、距离矩阵与车辆容量参数",
            "生成初始种群并进行染色体编码",
            "按容量约束解码为固定循环线路",
            "计算总里程、装载率与惩罚项",
            "进行选择、交叉与变异操作",
            "调用 repair 修复机制恢复可行性",
            "保留精英个体并迭代更新种群",
            "达到终止条件后输出最优固定线路方案",
        ],
        "图5-1：改进遗传算法整体求解框架图",
    )
    d.paragraph("图5-1展示了改进遗传算法从数据输入、染色体编码、容量约束解码、适应度计算、遗传操作到repair修复和结果输出的完整流程。该流程使供应商分组与路径排序能够在同一染色体框架下表达。")
    d.editable_chromosome_diagram("图5-2：改进遗传算法染色体编码与线路解码示意图")
    d.paragraph("图5-2说明，染色体本身只保存供应商访问排列，线路边界由解码阶段根据车辆容量约束动态确定。这种设计避免在染色体中直接存放车辆编号，从而减少无效编码。")
    d.table([
        ["参数", "取值", "作用"],
        ["种群规模", "120", "保证候选路径结构多样性"],
        ["迭代次数", "260", "控制搜索深度"],
        ["交叉概率", "0.86", "促进优秀片段重组"],
        ["变异概率", "0.22", "通过交换、插入、逆序增强搜索扰动"],
        ["精英保留", "6", "避免当前最优个体丢失"],
        ["随机种子", "20260521", "保证计算可复核"],
    ], "表5-1：改进遗传算法参数设置表")
    d.image("图5-4_改进遗传算法迭代收敛过程图.png", "图5-4：改进遗传算法迭代收敛过程图", 5.6)
    d.paragraph("图5-4表明，改进遗传算法在前期快速降低目标函数值，随后进入较缓慢的局部改进阶段，最终稳定在480.4 km附近。该过程体现出种群搜索在全局探索和局部开发之间的平衡。")
    d.editable_flowchart(
        "改进遗传算法 repair 修复机制示意图",
        [
            "检测交叉/变异后个体是否存在重复节点",
            "删除重复节点，仅保留首次出现位置",
            "检测是否存在遗漏节点",
            "将遗漏节点按最近可行插入规则补回线路",
            "检查各线路是否超载",
            "将超载节点转移至负载较低且可行的线路",
            "若仍不可行，则新开线路或赋予惩罚值",
            "输出修复后的可行染色体",
        ],
        "图5-5：repair修复机制示意图",
    )
    d.paragraph("图5-5中的repair机制用于处理交叉、变异后可能出现的供应商重复、遗漏和线路超载问题。通过去重、补全、重新分配和必要惩罚，算法能够将大量候选个体拉回可行域，从而提升迭代稳定性。")

    d.paragraph("六、算例求解结果与比较分析", style="heading1")
    d.paragraph("本章汇总四种算法在统一扩展数据上的结果，并重点分析改进遗传算法固定线路方案。由于每天固定执行4次取货，单次总里程可直接乘以4得到日总里程；平均装载率和装载率标准差用于评价线路容量利用和均衡性。")
    d.image("图6-7_改进遗传算法收敛曲线图.png", "图6-7：改进遗传算法收敛曲线图", 5.6)
    d.image("图6-8_改进遗传算法固定循环线路图.png", "图6-8：改进遗传算法固定循环线路示意图", 5.4)
    route_rows = [["线路", "固定循环路线", "单次载重（m³）", "单次里程（km）", "装载率（%）"]]
    route_data = [
        ["路线1", "GT→S04→S08→GT", "38.00", "30.9", "95.00"],
        ["路线2", "GT→S12→S09→GT", "37.75", "44.3", "94.38"],
        ["路线3", "GT→S13→GT", "27.75", "19.2", "69.38"],
        ["路线4", "GT→S05→S21→GT", "40.00", "24.4", "100.00"],
        ["路线5", "GT→S02→GT", "25.25", "31.2", "63.12"],
        ["路线6", "GT→S06→S18→GT", "35.00", "34.2", "87.50"],
        ["路线7", "GT→S11→GT", "26.00", "36.4", "65.00"],
        ["路线8", "GT→S16→S20→GT", "37.75", "29.8", "94.38"],
        ["路线9", "GT→S10→GT", "22.25", "29.4", "55.62"],
        ["路线10", "GT→S14→S22→GT", "32.50", "33.4", "81.25"],
        ["路线11", "GT→S01→S17→GT", "39.75", "33.5", "99.38"],
        ["路线12", "GT→S24→GT", "30.00", "21.4", "75.00"],
        ["路线13", "GT→S03→S07→GT", "39.25", "37.8", "98.12"],
        ["路线14", "GT→S15→GT", "29.00", "36.4", "72.50"],
        ["路线15", "GT→S19→S23→GT", "39.25", "38.1", "98.12"],
    ]
    d.table(route_rows + route_data, "表6-1：改进遗传算法15条固定循环线路结果表")
    d.image("图6-9_改进遗传算法各固定线路装载率分布图.png", "图6-9：改进遗传算法各固定线路装载率分布图", 5.8)
    d.paragraph("表6-1和图6-9显示，多条线路装载率接近或达到95%以上，少数单供应商线路装载率较低。这并非算法失效，而是由“供应商单次需求不可拆分”和车辆容量上限共同决定的。若某供应商单次需求本身较高，则与其他中高需求供应商合并后容易超载，保留单独线路反而更符合容量可行性。")
    d.table([
        ["算法", "线路数", "单次总里程/km", "日总里程/km", "平均装载率/%", "装载率标准差", "运行时间/s"],
        ["节约里程法", "17", "527.8", "2111.2", "73.46", "14.75", "0.0003"],
        ["VRP扫描法", "18", "536.9", "2147.6", "69.38", "12.56", "0.0011"],
        ["模拟退火算法", "15", "480.4", "1921.6", "83.25", "14.76", "0.5212"],
        ["改进遗传算法", "15", "480.4", "1921.6", "83.25", "14.76", "1.2971"],
    ], "表6-2：四种算法综合结果表")
    for fname, cap in [
        ("图6-10_四种算法单次总里程对比图.png", "图6-10：四种算法单次总里程对比图"),
        ("图6-11_四种算法线路数对比图.png", "图6-11：四种算法线路数对比图"),
        ("图6-12_四种算法平均装载率对比图.png", "图6-12：四种算法平均装载率对比图"),
        ("图6-13_四种算法运行时间对比图.png", "图6-13：四种算法运行时间对比图"),
        ("图6-14_四种算法装载率标准差对比图.png", "图6-14：四种算法装载率标准差对比图"),
        ("图6-15_四种算法综合表现对比图.png", "图6-15：四种算法综合表现对比图"),
    ]:
        d.image(fname, cap, 5.5)
    d.paragraph("综合表6-2和图6-10至图6-15可以看出，不同算法在不同维度下各有优势。节约里程法与VRP扫描法运行时间极短，适合作为基准方案或初始解生成方法；模拟退火算法在本次运行中取得与改进遗传算法相同的运输结果，且运行时间更短；改进遗传算法虽然运行时间较长，但其编码表达、约束修复、多目标扩展和与平准化执行的适配能力更强。")

    d.paragraph("七、讨论、管理启示与研究不足", style="heading1")
    d.paragraph("加入平准化约束后，路径优化的评价标准不能只看单次总里程。固定路线、固定频次和固定取货量有助于降低供应商备货波动，减少日常调度沟通成本，并使A公司厂区的收货节拍更稳定。按照本文求解结果，改进遗传算法方案每天运行4轮，形成15条固定循环线路和60个日车次，虽然线路数高于体积下界，但能够保证全部供应商在不可拆分取货条件下满足容量约束。")
    d.paragraph("从管理实施角度看，固定线路可直接转化为车辆班次、司机路线、供应商发货窗口和厂区卸货计划。与每天重算的动态拼车方案相比，固定线路更适合标准作业、培训和异常管理。因此，本文并不把改进遗传算法理解为“单次结果最好”的万能方法，而是把它看作在运输效率、容量可行性和执行稳定性之间形成综合平衡的核心方法。")
    d.paragraph("本文仍存在局限。其一，扩展数据属于教学研究用虚拟数据，尚不能替代企业真实运营数据；其二，模型未引入严格时间窗、道路拥堵、装卸服务时间与线边库存容量；其三，当前结果以固定4次/天为前提，尚未比较不同取货频次下的车辆数、库存与运输成本变化。上述问题均可在现有改进遗传算法框架上继续扩展。")

    d.paragraph("八、结论", style="heading1")
    d.paragraph("本文基于24家供应商扩展数据研究循环取货路径优化与物流平准化问题。在统一扩展案例下，文中比较了节约里程法、VRP扫描法、模拟退火算法和改进遗传算法的公式、计算过程、计算结果及其管理含义。研究表明，构造型启发式算法适合快速生成基准方案，但在复杂扩展场景中难以同时兼顾线路数量、总里程与装载质量；模拟退火算法在本次运行中取得与改进遗传算法相同的运输结果，且运行时间更短；改进遗传算法则在复杂约束表达、repair修复机制、多目标扩展和平准化执行适配方面更具综合优势。")
    d.paragraph("因此，本文的结论并不是简单宣称改进遗传算法在所有指标下都最优，而是指出：在循环取货路径优化与物流平准化相结合的问题中，改进遗传算法更适合作为核心方法。其价值体现在能够把运输效率、容量可行性、固定线路和固定频次统一到同一求解框架中，从而形成具有课程研究价值和工程可实施性的物流优化方案。")

    d.paragraph("参考文献", style="heading1")
    refs = [
        "[1] 李明玉, 袁森. 基于改进节约里程法的生鲜农产品配送路径优化研究[J]. 农业科技创新, 2026, (04): 80-81.",
        "[2] 陈映津, 胡永华, 莫志瑜. 基于模拟退火算法与A*算法融合求解路径规划[J]. 物联网技术, 2026, 16(01): 129-131+134.",
        "[3] 张泽宇, 王雷, 寿林, 等. 改进遗传算法在路径规划中的应用研究[J]. 井冈山大学学报(自然科学版), 2025, 46(05): 80-90.",
        "[4] 张晓娟, 史金丹. 苏州市盒马鲜生冷链物流配送路径优化研究[J]. 消费与品牌传播, 2025, (18): 57-60.",
        "[5] 王语涵, 沈彤, 杨杜玉冰, 等. 基于节约里程法的企业配送线路优化研究——以北京长浩物流有限公司为例[J]. 中国市场, 2024, (15): 175-178.",
        "[6] 宁晓利, 王法波. 基于遗传算法的南阳顺丰速运配送路径优化[J]. 物流技术, 2023, 42(10): 61-63.",
        "[7] 赵安琪. 时序图中多约束下的路径及k个最近邻节点对问题研究[D]. 苏州大学, 2019.",
        "[8] 王钰祥, 孙琪. 基于扫描法的连锁超市生鲜配送路径优化[J]. 中国商论, 2016, (18): 1-2.",
        "[9] 王荣花. 多点物流配送车辆路径问题(VRP)优化与实证分析[J]. 现代营销(下旬刊), 2016, (36): 162-163.",
        "[10] 张雪梅. 浅析进口完税价格的估价方法[J]. 对外经贸实务, 2010, (07): 63-65.",
    ]
    for ref in refs:
        d.paragraph(ref, style="reference")


def write_figure_list():
    mapping = [
        ("图5-1", "图5-1_改进遗传算法整体求解框架图.png", "第五章"),
        ("图5-2", "图5-2_染色体编码与线路解码示意图.png", "第五章"),
        ("图5-4", "图5-4_改进遗传算法迭代收敛过程图.png", "第五章"),
        ("图5-5", "图5-5_repair修复机制示意图.png", "第五章"),
        ("图6-1", "图6-1_节约里程法节点节约值排序图.png", "第四章4.1"),
        ("图6-5", "图6-5_模拟退火算法收敛曲线图.png", "第四章4.3"),
        ("图6-7", "图6-7_改进遗传算法收敛曲线图.png", "第六章"),
        ("图6-8", "图6-8_改进遗传算法固定循环线路图.png", "第六章，错落位置关系示意"),
        ("图6-9", "图6-9_改进遗传算法各固定线路装载率分布图.png", "第六章"),
        ("图6-10", "图6-10_四种算法单次总里程对比图.png", "第六章"),
        ("图6-11", "图6-11_四种算法线路数对比图.png", "第六章"),
        ("图6-12", "图6-12_四种算法平均装载率对比图.png", "第六章"),
        ("图6-13", "图6-13_四种算法运行时间对比图.png", "第六章"),
        ("图6-14", "图6-14_四种算法装载率标准差对比图.png", "第六章"),
        ("图6-15", "图6-15_四种算法综合表现对比图.png", "第六章"),
    ]
    lines = ["# 图片清单", "", "| 图号 | 文件名 | 插入位置 |", "|---|---|---|"]
    lines += [f"| {a} | {b} | {c} |" for a, b, c in mapping]
    FIG_LIST.write_text("\n".join(lines), encoding="utf-8")


def main():
    if not FIG_DIR.exists():
        raise SystemExit("缺少 paper_figures_output，请先运行配图代码。")
    d = DocBuilder()
    add_content(d)
    d.save(DOCX_OUT)
    write_figure_list()
    # The local figure script is the final editable version when figure layout is revised.
    print(DOCX_OUT)
    print(FIG_LIST)


if __name__ == "__main__":
    main()
