#!/usr/bin/env python3
"""Create a clean workspace for a course paper or report task."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PROFILES = [
    "course-paper",
    "case-study",
    "algorithm-case-study",
    "data-analysis-report",
    "literature-review",
]


def write_if_missing(path: Path, text: str) -> None:
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--profile", choices=PROFILES, default="course-paper")
    parser.add_argument("--language", choices=["zh", "en", "bilingual"], default="zh")
    parser.add_argument("--title", default="")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    dirs = [
        "source",
        "data/raw",
        "data/processed",
        "references",
        "assets/templates",
        "assets/images",
        "figures",
        "tables",
        "scripts",
        "planning",
        "output/private",
        "output/versions",
        "output/final",
    ]
    for folder in dirs:
        (workspace / folder).mkdir(parents=True, exist_ok=True)

    manifest = {
        "profile": args.profile,
        "language": args.language,
        "title": args.title,
        "source_dir": "source",
        "raw_data_dir": "data/raw",
        "figures_dir": "figures",
        "output_dir": "output",
    }
    write_if_missing(
        workspace / "paper_task.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
    write_if_missing(
        workspace / "planning" / "outline.md",
        "# Outline\n\n## Requirement Notes\n\n## Argument Spine\n\n## Evidence Map\n",
    )
    write_if_missing(
        workspace / "planning" / "revision-log.md",
        "# Revision Log\n\n",
    )
    write_if_missing(
        workspace / "planning" / "quality-check.md",
        "# Quality Check\n\n- [ ] Requirements matched\n- [ ] Figures numbered\n- [ ] Tables numbered\n- [ ] Citations checked\n- [ ] DOCX checked\n- [ ] PDF checked\n",
    )
    print(f"Created course paper workspace: {workspace}")


if __name__ == "__main__":
    main()

