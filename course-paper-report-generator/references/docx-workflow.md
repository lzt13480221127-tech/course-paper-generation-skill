# DOCX Workflow

Use this workflow when editing a Word course paper.

## Inspect

1. Open the `.docx` as a ZIP.
2. Read `word/document.xml` for paragraphs, headings, captions, tables, and image references.
3. Read `word/_rels/document.xml.rels` for image relationship IDs.
4. Count media under `word/media/`.
5. Identify the paragraphs or chapter range to replace.

## Preserve

- Preserve the user-designated manuscript as the main source.
- Preserve existing images and tables unless the user asks to remove or consolidate them.
- Preserve algorithm result values exactly.
- Preserve references unless they are clearly irrelevant or uncited and the user asks for cleanup.

## Replace Chapter Safely

When replacing a chapter:

1. Locate start paragraph by exact heading text.
2. Locate end paragraph by next chapter heading.
3. Remove only the target range.
4. Insert new paragraphs, retained images, retained tables, and captions.
5. Reuse existing image relationship IDs where possible.
6. Validate that deleted figure captions are no longer present.

## Font Normalization

In `word/document.xml` and `word/styles.xml`, set:

- `w:eastAsia="宋体"`
- `w:ascii="Times New Roman"`
- `w:hAnsi="Times New Roman"`
- `w:cs="Times New Roman"`

For headings and captions, keep consistent font treatment unless the user supplies a template.

## Figure Handling

When exact Word wrapping cannot be fully controlled via XML, still ensure:

- image paragraph centered;
- caption centered;
- image near related text;
- no duplicate/redundant figure remains;
- image size is reasonable in the document.

If the user specifically requires top-and-bottom wrapping and fixed position, prefer editing through Word automation or verify OOXML drawing anchors if available.

## Validation Commands

Use the bundled script:

```bash
python scripts/check_docx_paper.py path/to/paper.docx
```

Manual checks:

```python
from zipfile import ZipFile
z = ZipFile("paper.docx")
print(z.testzip())
print([n for n in z.namelist() if n.startswith("word/media/")])
s = z.read("word/document.xml").decode("utf-8")
print("图6-8：" in s)
```

Report validation results in the final response.
