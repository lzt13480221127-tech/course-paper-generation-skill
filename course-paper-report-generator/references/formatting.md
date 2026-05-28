# Formatting and Output Standards

Use these standards for Chinese course papers and reports.

## Fonts and Paragraphs

- Chinese text: 宋体.
- English letters and numbers: Times New Roman.
- PPT Chinese text, if producing slides: 微软雅黑.
- Body font size: follow the user template; common default is 小四 or 12pt.
- Main title: centered, bold, larger than body.
- Chapter headings: no first-line indent.
- Body paragraphs: first-line indent two Chinese characters.
- Keep line spacing consistent across the document.

## Figure Rules

- Figure captions go below the figure.
- Caption format: `图x-x：图名`.
- Subfigure caption format: `图5-2（a）：……`.
- All figures must be centered.
- In Word, prefer top-and-bottom wrapping when possible.
- Keep figures close to the first paragraph that analyzes them.
- Do not keep figures that repeat a table unless they support a specific argument.
- Use high-resolution PNG, normally at least 300 dpi.
- All chart text must be Chinese where appropriate:
  - title;
  - x-axis label;
  - y-axis label;
  - legend;
  - annotation.
- Legends must not cover the main plotting area. Put them outside or below when needed.

## Matplotlib Chart Safety

For notebook/script chart generation:

```python
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel("横坐标标题", labelpad=12)
ax.set_ylabel("纵坐标标题", labelpad=16)
plt.subplots_adjust(left=0.14, right=0.96, top=0.88, bottom=0.22)
plt.tight_layout()
plt.savefig("figure.png", dpi=300, bbox_inches="tight")
```

Use larger left margins when y-axis titles are long.

## Table Rules

- Table titles go above the table.
- Title format: `表x-x：表名`.
- First row: bold and centered.
- Use black-and-white lines; no fill color unless required.
- Fit within page margins.
- Place analysis after the table.
- Do not let the table stand alone without explanation.

## Formula Rules

- Use formal paper-style equations, not raw broken LaTeX.
- Define every symbol before or immediately after the formula.
- Formula paragraphs should be centered when possible.
- Number important formulas consistently if the paper uses numbered equations.
- Avoid duplicated corrupted formula strings such as `Q=40m3Q=40...`.

## Citation Rules

- Every reference in the bibliography should have an in-text citation.
- Use `[n]` superscript style when requested.
- Keep citation numbering consistent with the reference list.
- Do not cite unstable or unverified sources unless verified.
- If a reference cannot be verified, say so or omit it.

## Chapter-Specific Figure Placement

For algorithm papers:

- Method chapter: keep framework, encoding, decoding, convergence mechanism, repair mechanism diagrams.
- Result chapter: keep result tables, convergence curves, load/score distributions, algorithm comparison charts.
- Remove duplicate diagrams that repeat the same function across method and result chapters.

## Final Quality Checklist

Before final delivery, check:

- title matches the user’s required title;
- main data and results are unchanged;
- chapter numbering is continuous;
- figure/table numbering is continuous and non-conflicting;
- removed figures are actually absent;
- retained figures are near corresponding analysis;
- all figures and tables are explained;
- body is formal, not instruction-like;
- `.docx` package integrity passes;
- output paths are provided.
