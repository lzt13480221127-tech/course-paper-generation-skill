"""Quick structural checks for a Chinese course-paper .docx file.

This script is intentionally lightweight. It inspects the OOXML package for
common issues: package integrity, media count, required strings, duplicate or
removed figure labels, and font declarations.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from zipfile import BadZipFile, ZipFile


def read_docx_text(docx: Path):
    with ZipFile(docx) as z:
        bad = z.testzip()
        names = z.namelist()
        document_xml = z.read("word/document.xml").decode("utf-8", errors="replace")
        styles_xml = z.read("word/styles.xml").decode("utf-8", errors="replace") if "word/styles.xml" in names else ""
    text = re.sub(r"<[^>]+>", "", document_xml)
    media = [n for n in names if n.startswith("word/media/") and not n.endswith("/")]
    return bad, document_xml, styles_xml, text, media


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    parser.add_argument("--must-contain", action="append", default=[], help="String that must appear in document.xml")
    parser.add_argument("--must-not-contain", action="append", default=[], help="String that must not appear in document.xml")
    args = parser.parse_args()

    if not args.docx.exists():
        print(f"ERROR: file not found: {args.docx}")
        return 2

    try:
        bad, document_xml, styles_xml, text, media = read_docx_text(args.docx)
    except BadZipFile:
        print("ERROR: not a valid .docx zip package")
        return 2

    ok = True
    print(f"file: {args.docx}")
    print(f"package_integrity: {'OK' if bad is None else 'BAD: ' + str(bad)}")
    print(f"media_count: {len(media)}")
    print(f"has_songti: {'宋体' in document_xml or '宋体' in styles_xml}")
    print(f"has_times_new_roman: {'Times New Roman' in document_xml or 'Times New Roman' in styles_xml}")

    fig_labels = re.findall(r"图\d+(?:-\d+)?[：:]", text)
    table_labels = re.findall(r"表\d+(?:-\d+)?[：:]", text)
    print(f"figure_label_count: {len(fig_labels)}")
    print(f"table_label_count: {len(table_labels)}")

    for s in args.must_contain:
        found = s in document_xml
        print(f"must_contain {s!r}: {found}")
        ok = ok and found

    for s in args.must_not_contain:
        found = s in document_xml
        print(f"must_not_contain {s!r}: {not found}")
        ok = ok and not found

    if bad is not None:
        ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
