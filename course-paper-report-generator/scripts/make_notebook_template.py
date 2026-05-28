"""Create a reusable matplotlib notebook template for course-paper figures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


BASE_CELL = r'''# 基础数据单元
# 用途：定义图表所需数据、字体和输出目录

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

output_dir = "paper_figures"
os.makedirs(output_dir, exist_ok=True)
'''

FIG_CELL = r'''# 图X-X：图名
# 用途：说明该图在论文中的论证作用
# 对应论文位置：第X章
# 展示指标：填写指标名称

fig, ax = plt.subplots(figsize=(10, 6))

# TODO: replace with actual plotting code
x = ["A", "B", "C"]
y = [1, 2, 3]
ax.bar(x, y)

ax.set_title("图X-X 图名", fontsize=16, pad=18)
ax.set_xlabel("横坐标标题", fontsize=12, labelpad=12)
ax.set_ylabel("纵坐标标题", fontsize=12, labelpad=16)
ax.grid(axis="y", linestyle="--", alpha=0.35)

plt.subplots_adjust(left=0.14, right=0.96, top=0.88, bottom=0.22)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "图X-X_图名.png"), dpi=300, bbox_inches="tight")
plt.show()
'''


def code_cell(source: str):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def markdown_cell(source: str):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--figures", type=int, default=3)
    args = parser.parse_args()

    cells = [
        markdown_cell("# 课程论文图表生成 Notebook\n\n每张图一个代码单元，所有图片以 300 dpi PNG 保存。"),
        code_cell(BASE_CELL),
    ]
    for _ in range(args.figures):
        cells.append(code_cell(FIG_CELL))

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    args.output.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
