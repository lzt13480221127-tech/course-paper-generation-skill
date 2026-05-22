---
name: course-paper-generation
description: Create, revise, standardize, and export Chinese or bilingual course papers, course reports, case-study papers, algorithm experiment papers, and data-analysis reports from DOCX, PDF, notes, grading rubrics, datasets, notebooks, scripts, charts, or draft outlines. Use when the user asks for 课程论文, 课程报告, 案例分析论文, 算法论文, 数据分析报告, academic course paper, report-to-paper conversion, Word/PDF deliverables, reproducible figures, formula-heavy sections, references, figure/table numbering, or polishing a paper into a formal submission.
---

# Course Paper Generation

Generate editable, submission-ready course papers and reports with reproducible logic, figures, tables, formulas, and revision history.

## Quick Start

1. Create a task workspace:
   ```bash
   python scripts/create_workspace.py ./my-course-paper --profile course-paper
   ```
2. Put source materials in the workspace:
   - `source/`: rubrics, assignment requirements, drafts, DOCX/PDF, notes.
   - `data/raw/`: CSV, Excel, JSON, screenshots, experiment logs.
   - `references/`: papers, book excerpts, citation notes.
   - `assets/`: user-provided templates, figures, school requirements.
3. Read the assignment requirement first. Identify topic, course, submission format, word count, required sections, citation style, deadline, and scoring emphasis.
4. Build the argument spine before writing prose: research question, method, evidence, result, interpretation, and limitation.
5. Generate or revise the paper in versioned outputs. Never overwrite a user-approved deliverable.
6. Run the quality gates in [references/quality-gates.md](references/quality-gates.md) before final delivery.

## Core Workflow

1. **Requirement extraction**: summarize explicit constraints, hidden grading signals, required file types, and forbidden shortcuts.
2. **Material audit**: classify available materials into theory, data, methods, figures, draft text, and references.
3. **Paper plan**: choose a structure from [references/paper-structures.md](references/paper-structures.md), then adapt it to the assignment.
4. **Evidence map**: map each major claim to a proof object: formula, table, chart, algorithm result, case evidence, or citation.
5. **Data and figure pass**: generate reproducible charts and tables using [references/figures-and-tables.md](references/figures-and-tables.md).
6. **Writing pass**: write formal academic prose. Avoid conversational filler, task-instruction language, and unsupported claims.
7. **Document assembly**: produce editable DOCX when possible; export PDF only after DOCX layout is checked.
8. **Revision pass**: preserve user edits and version outputs according to [references/revision-safety.md](references/revision-safety.md).
9. **Final check**: verify title levels, citations, formulas, numbering, data consistency, page layout, and file naming.

## Default Chinese Course Paper Structure

Use this when the assignment does not provide a stronger template:

1. Title
2. Abstract and keywords
3. Introduction: background, problem, significance, research path
4. Literature or theory basis
5. Method, model, algorithm, or analytical framework
6. Data, case, calculation, or experiment
7. Results and discussion
8. Conclusion and limitations
9. References
10. Appendix when code, raw tables, or extended derivations are needed

## Writing Rules

- Prefer formal academic Chinese for Chinese course papers.
- Give derivation and interpretation, not only final numbers.
- Every chart and table must answer a concrete analytical question.
- Keep terminology consistent across title, abstract, headings, figures, and tables.
- Use Chinese figure and table captions unless the assignment requests English.
- Use citation markers consistently; if real sources are missing, ask for sources or clearly mark placeholders for the user to replace.
- Do not fabricate datasets, references, school templates, or teacher requirements.

## When To Read References

- Need to choose a paper structure: read [references/paper-structures.md](references/paper-structures.md).
- Need formal wording and section-level expectations: read [references/academic-writing.md](references/academic-writing.md).
- Need charts, formulas, tables, or algorithm results: read [references/figures-and-tables.md](references/figures-and-tables.md).
- Revising an existing DOCX/PDF: read [references/revision-safety.md](references/revision-safety.md).
- Before delivery: read [references/quality-gates.md](references/quality-gates.md).

## Scripts

- `scripts/create_workspace.py`: create a clean paper workspace with source, data, references, figures, planning, and output folders.
- `scripts/course_paper_plot_style.py`: apply a restrained academic Matplotlib style for paper figures.

