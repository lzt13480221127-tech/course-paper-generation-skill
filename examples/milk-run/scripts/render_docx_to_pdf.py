from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import xml.etree.ElementTree as ET
import re
from PIL import Image, ImageDraw, ImageFont


CWD = Path.cwd()
DOCX = CWD / "规范课程论文_可编辑流程图版.docx"
PDF = CWD / "规范课程论文_可编辑流程图版.pdf"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}

PAGE_W, PAGE_H = 1240, 1754
MARGIN_X, MARGIN_Y = 105, 95
CONTENT_W = PAGE_W - 2 * MARGIN_X

FONT_SONG = "C:/Windows/Fonts/simsun.ttc"
FONT_SONG_B = "C:/Windows/Fonts/simsunb.ttf"
FONT_TIMES = "C:/Windows/Fonts/times.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_SONG_B if bold else FONT_SONG, size)


F_TITLE = font(34, True)
F_H1 = font(28, True)
F_H2 = font(24, True)
F_BODY = font(22)
F_CAPTION = font(19)
F_TABLE = font(17)
F_REF = font(18)


def text_width(draw, text, fnt):
    if not text:
        return 0
    return draw.textbbox((0, 0), text, font=fnt)[2]


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(line)
            line = ""
            continue
        cand = line + ch
        if text_width(draw, cand, fnt) <= width or not line:
            line = cand
        else:
            lines.append(line)
            line = ch
    if line:
        lines.append(line)
    return lines or [""]


class PdfRenderer:
    def __init__(self):
        self.pages = []
        self.new_page()

    def new_page(self):
        self.img = Image.new("RGB", (PAGE_W, PAGE_H), "white")
        self.draw = ImageDraw.Draw(self.img)
        self.y = MARGIN_Y
        self.pages.append(self.img)

    def ensure(self, h):
        if self.y + h > PAGE_H - MARGIN_Y:
            self.new_page()

    def para(self, text, kind="body"):
        if not text.strip():
            self.y += 10
            return
        if kind == "title":
            fnt, bold, before, after, indent, center = F_TITLE, True, 0, 24, 0, True
        elif kind == "h1":
            fnt, bold, before, after, indent, center = F_H1, True, 24, 14, 0, False
        elif kind == "h2":
            fnt, bold, before, after, indent, center = F_H2, True, 18, 10, 0, False
        elif kind == "caption":
            fnt, bold, before, after, indent, center = F_CAPTION, False, 6, 18, 0, True
        elif kind == "formula":
            fnt, bold, before, after, indent, center = F_BODY, False, 8, 8, 0, True
        elif kind == "ref":
            fnt, bold, before, after, indent, center = F_REF, False, 2, 8, 0, False
        else:
            fnt, bold, before, after, indent, center = F_BODY, False, 0, 8, 44, False
        self.y += before
        width = CONTENT_W - indent
        lines = wrap(self.draw, text, fnt, width)
        line_h = int(fnt.size * 1.55)
        self.ensure(len(lines) * line_h + after)
        for i, line in enumerate(lines):
            x = MARGIN_X + (indent if i == 0 else 0)
            if center:
                x = (PAGE_W - text_width(self.draw, line, fnt)) // 2
            self.draw.text((x, self.y), line, fill="black", font=fnt)
            self.y += line_h
        self.y += after

    def table(self, rows):
        if not rows:
            return
        cols = max(len(r) for r in rows)
        col_w = CONTENT_W // cols
        row_heights = []
        wrapped = []
        for row in rows:
            wr = []
            max_lines = 1
            for cell in row:
                lines = wrap(self.draw, cell, F_TABLE, col_w - 14)
                wr.append(lines)
                max_lines = max(max_lines, len(lines))
            wrapped.append(wr)
            row_heights.append(max(36, max_lines * 24 + 14))
        total_h = sum(row_heights) + 18
        self.ensure(total_h)
        for r_idx, row in enumerate(wrapped):
            h = row_heights[r_idx]
            x = MARGIN_X
            fill = (79, 129, 189) if r_idx == 0 else ((242, 242, 242) if r_idx % 2 == 0 else (255, 255, 255))
            for c_idx in range(cols):
                self.draw.rectangle([x, self.y, x + col_w, self.y + h], outline=(145, 170, 205), fill=fill)
                lines = row[c_idx] if c_idx < len(row) else [""]
                ty = self.y + 7
                for line in lines:
                    tw = text_width(self.draw, line, F_TABLE)
                    color = "white" if r_idx == 0 else "black"
                    self.draw.text((x + (col_w - tw) / 2, ty), line, fill=color, font=F_TABLE)
                    ty += 24
                x += col_w
            self.y += h
        self.y += 18

    def image(self, pil_img):
        img = pil_img.convert("RGB")
        w, h = img.size
        scale = min(CONTENT_W / w, 720 / h)
        nw, nh = int(w * scale), int(h * scale)
        self.ensure(nh + 20)
        resized = img.resize((nw, nh), Image.LANCZOS)
        self.img.paste(resized, ((PAGE_W - nw) // 2, self.y))
        self.y += nh + 8

    def save(self):
        self.pages[0].save(PDF, "PDF", resolution=150.0, save_all=True, append_images=self.pages[1:])


def extract_items():
    with ZipFile(DOCX) as z:
        doc = ET.fromstring(z.read("word/document.xml"))
        rels = ET.fromstring(z.read("word/_rels/document.xml.rels"))
        rid_to_target = {r.attrib["Id"]: "word/" + r.attrib["Target"] for r in rels}
        items = []
        for child in doc.find("w:body", NS):
            tag = child.tag.split("}")[-1]
            if tag == "p":
                blips = child.findall(".//a:blip", NS)
                if blips:
                    rid = blips[0].attrib.get(f"{{{NS['r']}}}embed")
                    if rid in rid_to_target:
                        items.append(("image", Image.open(BytesIO(z.read(rid_to_target[rid]))).copy()))
                    continue
                txt = "".join(t.text or "" for t in child.findall(".//w:t", NS))
                if txt.strip():
                    items.append(("p", txt))
            elif tag == "tbl":
                rows = []
                for tr in child.findall("w:tr", NS):
                    row = []
                    for tc in tr.findall("w:tc", NS):
                        row.append("".join(t.text or "" for t in tc.findall(".//w:t", NS)))
                    rows.append(row)
                items.append(("table", rows))
        return items


def classify(text, seen_title=[False]):
    if text == "基于改进遗传算法的循环取货路径优化与物流平准化研究":
        return "title"
    if text in {"摘  要", "课程论文"}:
        return "caption"
    if text.startswith(("一、", "二、", "三、", "四、", "五、", "六、", "七、", "八、")) or text == "参考文献":
        return "h1"
    if re.match(r"^\d+\.\d+\s", text):
        return "h2"
    if text.startswith(("图", "表")) and "：" in text:
        return "caption"
    if text.startswith("["):
        return "ref"
    if any(sym in text for sym in ["=", "Σ", "ceil", "exp(", "Fitness"]) and len(text) < 90:
        return "formula"
    return "body"


def main():
    r = PdfRenderer()
    for kind, value in extract_items():
        if kind == "p":
            r.para(value, classify(value))
        elif kind == "table":
            r.table(value)
        elif kind == "image":
            r.image(value)
    r.save()
    print(PDF)


if __name__ == "__main__":
    main()
