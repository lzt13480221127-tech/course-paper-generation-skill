---
name: course-paper-report-generator
description: Generate, revise, deepen, format, and package Chinese course papers/reports from user-provided drafts, data, figures, code, PDFs, or prompts. Use when Codex needs to create or edit a formal course thesis/report with algorithms, case data, calculations, formulas, charts, tables, Word/PDF formatting, notebook/code appendices, cross-references, management analysis, or reusable paper-generation prompts.
---

# Course Paper Report Generator

Use this skill to turn drafts, datasets, prompts, and reference papers into a complete, submission-ready Chinese course paper/report. The default target is a formal course-paper style, not a PPT script, outline, or casual summary.

## Core Workflow

1. **Read source artifacts first.**
   - Inspect the user's current main draft, data workbook, PDFs, prompts, code, and figure assets.
   - Treat the user-designated file as the only main manuscript when they say so.
   - Do not overwrite case data, algorithm results, titles, or core conclusions unless the user explicitly asks.

2. **Identify the paper type and main line.**
   - Determine the case object, research question, algorithm/model, data source, required output format, and grading constraints.
   - Avoid dual-track designs unless the user explicitly requests them. Keep one coherent research main line.

3. **Build the argument before formatting.**
   - Use the pattern: business/case problem → data and preprocessing → model/indicator definition → algorithm design → computation → result analysis → management meaning → conclusion.
   - Every result section must include description, comparison, explanation, and management interpretation.

4. **Generate or revise deliverables.**
   - For Word deliverables, preserve useful existing content and revise the requested parts.
   - For code deliverables, provide runnable Python scripts and notebooks that reproduce figures and results.
   - For chart deliverables, generate high-resolution images with Chinese titles, Chinese axis labels, readable legends, and non-cropped labels.

5. **Validate before finalizing.**
   - Check docx integrity, figure/table numbering, core values, title, font defaults, references, and whether requested figures/tables remain or are removed.
   - Report what changed and provide clickable paths.

## Paper-Writing Rules

- Keep the language formal, continuous, and thesis-like.
- Do not write task-instruction phrases such as “根据要求完成” or “本任务需要”.
- Do not only list charts and tables; explain what they mean.
- Do not claim one algorithm is absolutely best unless the metrics prove it.
- When comparing algorithms, use quantitative differences and causal explanation.
- When data is synthetic, expanded, teaching-only, or assumed, explicitly state that in the paper.
- Keep the original research topic and case data stable unless the user asks for redesign.

## Required Analysis Pattern

For every major result table or figure, write at least one paragraph with:

1. **Descriptive analysis**: what the table/figure shows and the key values.
2. **Comparative analysis**: how methods, groups, years, routes, or indicators differ.
3. **Mechanism explanation**: why the difference occurs, based on data structure or algorithm logic.
4. **Management meaning**: what the result implies for decision-making, execution, resource allocation, or improvement.

Use this sentence pattern when useful:

> 从数据层看，……；从算法层看，……；从管理层看，……。

## Algorithm/Model Chapter Rules

For algorithm-based papers, include:

- parameter and variable definitions;
- formal objective function or scoring function;
- constraints and assumptions;
- algorithm input, output, and calculation logic;
- encoding/data structure if relevant;
- fitness/cost function if relevant;
- selection, crossover, mutation, neighborhood search, repair, or other mechanisms if relevant;
- parameter settings and reproducibility notes;
- code/notebook appendix placeholders when code is required.

## Figure and Table Rules

Follow `references/formatting.md` for full rules. Minimum requirements:

- Chinese body font: 宋体.
- English and numbers: Times New Roman.
- Body paragraphs: first-line indent two Chinese characters.
- Headings: no indent.
- Figure captions below figures: `图x-x：……`.
- Table titles above tables: `表x-x：……`.
- Figures centered, near the analysis text, with balanced spacing.
- Tables should be black-and-white, fit page width, first row bold and centered.
- Do not keep redundant figures that repeat the same information as a table unless they support a specific analysis.

## Resource Guide

Load these files only when needed:

- `references/structure.md`: standard paper section logic and chapter templates.
- `references/analysis-patterns.md`: result-analysis, algorithm-comparison, and management-meaning templates.
- `references/formatting.md`: Word, figure, table, formula, citation, and notebook chart requirements.
- `references/docx-workflow.md`: practical `.docx` editing and validation workflow.
- `references/facility-planning-ga-extension.md`: preserved prior prompt for facility-planning / milk-run / genetic algorithm papers.

Scripts:

- `scripts/check_docx_paper.py`: quick structural check for `.docx` papers.
- `scripts/make_notebook_template.py`: create a reusable matplotlib notebook skeleton for paper figures.

## Final Response Rules

When work is complete, provide:

- output file paths;
- brief summary of major revisions;
- validation performed;
- any remaining limitations, such as missing source data or unavailable fonts.
