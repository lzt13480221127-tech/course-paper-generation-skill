# Report Generation Rules

Use this reference when a course paper/report task involves final DOCX/PDF integration, figure generation, formula-heavy sections, route or algorithm comparison, or iterative user feedback about layout and figures.

## Core Principle

Use the user's provided final draft as the authoritative text. Do not rewrite the research content unless the user explicitly asks for content rewriting. Normalize structure, formatting, formulas, figures, tables, citations, and export artifacts around the given draft.

The expected output is a submission-ready Word document and PDF document. Prefer editable Word structures over image screenshots whenever the user may need to revise diagrams, flowcharts, route lists, tables, or captions later.

## Required Inputs

When available, use these inputs in priority order:

1. User-provided final paper draft or latest DOCX as the main text.
2. User-provided integration prompt or course-report prompt as formatting and content rules.
3. Figure-generation code and generated PNGs.
4. Reference paper or format example.
5. User's latest revision instructions, which override earlier assumptions.

If multiple drafts exist, prefer the newest file that appears most complete, but compare older versions for missing formulas, tables, references, and figure numbering.

## Standard Workflow

1. Read the user prompt, integration prompt, course-report prompt, and available paper draft.
2. Identify the authoritative main text and avoid deleting or shortening important content.
3. Run the provided figure code once first, then inspect generated image count, file names, resolution, Chinese font rendering, axis labels, legends, and caption placement.
4. If figures have issues, minimally modify the code without changing data meaning or calculation results.
5. Build or revise DOCX with course-report formatting: Chinese font 宋体; English and numbers Times New Roman; body paragraphs first-line indent two Chinese characters; headings and captions no first-line indent.
6. Preserve complete analytical paths: original formula, variable explanation, substitution process, calculation result, and corresponding conclusion.
7. Insert tables and figures according to body logic and the user's latest numbering rule.
8. Add in-text reference markers as superscript `[n]` where natural. Do not force weak references into unrelated sentences.
9. Keep “结论” and “参考文献” as separate sections.
10. Export DOCX and PDF. If Word COM export is blocked, generate PDF by an available local fallback and clearly state which artifact is the editable master.

## Recommended Structure

Use this structure for logistics, path-optimization, algorithm, and case-study course reports unless the assignment provides a stronger one:

1. 题目
2. 摘要
3. 关键词
4. 一、引言
5. 二、文献综述
6. 三、场景描述、问题界定与模型构建
7. 四、算法设计、求解过程与结果比较
8. 五、核心算法模型构建与参数设计
9. 六、算例求解结果与比较分析
10. 七、讨论、管理启示与研究不足
11. 八、结论
12. 参考文献

For early chapters, prefer coherent paragraphs over overly fragmented bullet points. For model and algorithm chapters, include formulas, symbol tables, parameter tables, route/result tables, and interpretive conclusions.

## Figure Rules

- PNG figures should not contain bottom captions like `图6-10：xxx` inside the image. The Word document should add captions separately.
- Figure titles and axis titles should be Chinese when the chart itself needs a title or axis label.
- Avoid squeezing or distorting images. Keep aspect ratio.
- Check legends do not cover chart title, labels, data, or radar axes.
- If a legend overlaps, move it to the upper-right corner or outside the plotting area.
- Do not insert redundant route maps for every algorithm. Use route/result tables for algorithm-by-algorithm comparison unless the user asks for all maps.

## Editable Diagram Rules

Prefer Word-editable structures for:

- algorithm framework flowcharts;
- chromosome encoding/decoding diagrams;
- repair mechanism diagrams;
- simple process diagrams.

Implement these as Word tables, shapes, or editable text-box-like structures rather than PNG screenshots. Keep every node's text editable. Use PNG only for data visualizations, convergence curves, bar charts, radar charts, and maps that benefit from plotting.

## Route Map Rules

Route maps should not use evenly distributed circular layouts unless the user explicitly requests abstract topology. For supplier route illustrations:

- Use staggered, uneven relative coordinates to suggest approximate supplier position relationships.
- Mark coordinates as schematic if not real GIS coordinates.
- Show only one representative route map when many algorithms are compared.
- Prefer tables for detailed route lists: algorithm, route number, fixed loop route, load, distance, and loading rate.
- The representative route map should support explanation, not replace tabular comparison.

## Table Rules

- Table header: bold and centered.
- Prefer clean academic styling: dark blue or restrained header, white or light-gray body rows.
- Keep route tables readable; route strings can be the main carrier of route comparison.
- Include at minimum: symbol explanation table, evaluation indicator table, algorithm comprehensive result table, and core algorithm fixed route result table.

## Formula Rules

- Do not use garbled LaTeX screenshots.
- Use readable report-style equations in text or editable formula-like paragraphs.
- Preserve raw formula, variable meaning, numeric substitution, final result, and conclusion sentence.
- Example pattern: `m₀ = ceil(Σp_i / Q) = ceil(499.5 / 40) = 13`, followed by an explanation that the result is only a theoretical lower bound, not necessarily the executable route count.

## Citation Rules

- Use `[n]` as superscript in the body.
- Add citations where the literature naturally supports the method or scenario.
- Keep references as a separate final section.
- If one reference is weakly related, keep it in the reference list when the user requires it, but do not force an unnatural body citation.

## DOCX/PDF Technical Rules

- If embedding PNGs into DOCX by OpenXML, use ASCII internal media names such as `figure_01.png`, not Chinese file names, to avoid Word display failures.
- If an existing DOCX is open and cannot be overwritten, generate a new versioned file name instead of forcing overwrite.
- For PDF export, first try Word/Office export when permitted; if blocked, use a local renderer as fallback and state that DOCX is the editable master.
- Always validate DOCX image relationships, embedded image count, PDF page count, and key figure/table captions.

## Iteration Memory From Milk-Run Case

### Initial Integration Request

The user requested use of the final paper body as main text, running the provided figure script, embedding generated PNGs at reserved figure positions, applying course report formatting, preserving formulas and derivations, adding superscript `[n]` citations, exporting DOCX/PDF, and resolving figure-number mismatches according to body-reserved numbering.

Rule learned: treat final draft as authoritative, but use the integration prompt to normalize structure, figures, formulas, and citations.

### Word Image Display Fix

The user reported images did not display in Word. The fix was to regenerate DOCX with internal image names like `figure_01.png` while keeping visible Chinese captions unchanged.

Rule learned: use ASCII media names inside DOCX packages even when source PNG file names are Chinese.

### Route Map Revision

The user requested route maps should not use uniform circular supplier distribution, should look staggered and show approximate supplier relationships, and should not be repeated for every algorithm. Route comparison should use tables.

Rule learned: use maps only for spatial intuition; use tables for route comparison.

### Editable Diagrams And Caption Cleanup

The user requested the first three diagrams be editable Word structures, all images remove built-in bottom captions, and the radar chart legend move to the upper right.

Rule learned: for process diagrams, prioritize Word editability. For plotted images, keep the plot clean and let Word handle figure captions.

## Final Quality Checklist

Before delivering, verify:

- Main text was not accidentally shortened or rewritten beyond formatting and necessary transitions.
- Chapter structure matches course-report requirements.
- Formulas and calculation explanations remain intact.
- Figure images do not contain embedded bottom captions.
- Word contains separate captions or caption placeholders for figures.
- Flowcharts and simple diagrams are editable when requested.
- Route maps are not overused; route comparisons appear in tables.
- Radar/bar/line chart legends and labels do not overlap.
- References are separated from conclusion.
- In-text citations use superscript `[n]`.
- DOCX and PDF both exist and have reasonable file sizes.
