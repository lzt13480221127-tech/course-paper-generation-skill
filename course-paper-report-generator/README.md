# Course Paper Report Generator Skill

一个用于生成、修订、深化和规范化中文课程论文/课程报告的 Codex Skill。它适合处理包含案例数据、算法比较、公式推导、图表、Word 排版、代码附录和管理分析的课程论文任务。

## 适用场景

当你需要完成以下任务时，可以使用本 skill：

- 基于已有 Word/PDF/Markdown 草稿继续修订课程论文；
- 将零散 prompt、数据表、图表和算法结果整理成正式论文；
- 深化结果分析，避免论文只停留在“图表罗列”；
- 统一中文论文排版，包括字体、段落、图题、表题、公式和参考文献；
- 生成论文配套 Python 主程序、Jupyter Notebook 图表代码或附录说明；
- 对算法类课程论文进行多算法比较、模型构建和管理含义分析。

## 核心能力

本 skill 强调“可提交课程论文”的完整闭环：

```text
案例问题 → 数据处理 → 模型定义 → 算法设计 → 计算过程 → 结果分析 → 管理解释 → 结论展望
```

它不会只生成提纲或 PPT 式文案，而是要求正文具备：

- 正式课程论文语言；
- 完整公式、变量解释和计算逻辑；
- 图表与正文分析对应；
- 多算法比较不预设最优结论；
- 结果解释同时覆盖数据层、算法层和管理层；
- Word 文档排版可直接提交。

## 目录结构

```text
course-paper-report-generator/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── analysis-patterns.md
│   ├── docx-workflow.md
│   ├── facility-planning-ga-extension.md
│   ├── formatting.md
│   └── structure.md
└── scripts/
    ├── check_docx_paper.py
    └── make_notebook_template.py
```

## 文件说明

| 文件 | 作用 |
|---|---|
| `SKILL.md` | skill 主入口，定义触发场景、总体工作流和质量要求 |
| `references/structure.md` | 课程论文标准结构与章节写法 |
| `references/analysis-patterns.md` | 描述性分析、比较分析、管理含义分析模板 |
| `references/formatting.md` | 字体、段落、图表、公式、引用、Notebook 图表规范 |
| `references/docx-workflow.md` | Word 文档解析、替换、排版和验证流程 |
| `references/facility-planning-ga-extension.md` | 设施规划/循环取货/遗传算法论文的历史 prompt 规范 |
| `scripts/check_docx_paper.py` | 快速检查 `.docx` 包结构、字体、图表标签等 |
| `scripts/make_notebook_template.py` | 生成论文图表 Jupyter Notebook 模板 |

## 安装方式

将整个文件夹复制到 Codex skills 目录，例如：

```powershell
Copy-Item -Recurse course-paper-report-generator $env:USERPROFILE\.codex\skills\
```

或放入项目级 skill 目录：

```text
.agents/skills/course-paper-report-generator/
```

之后在 Codex 中提出类似请求即可触发：

```text
使用 course-paper-report-generator 帮我基于当前 Word 草稿深化第六章，并统一图表与排版。
```

## 典型用法

### 1. 基于草稿深化论文

```text
请以当前 Word 为唯一主稿，在不改变数据和结论的前提下，扩写结果分析章节，统一图表编号、字体和表格格式，输出最终规范版论文。
```

### 2. 基于数据生成完整课程论文

```text
请读取这个 Excel 数据和 prompt，生成一篇正式课程论文，并输出 Word、Python 主程序和图表 notebook。
```

### 3. 提炼参考论文范式

```text
请阅读这篇 PDF，学习其分析思路和排版，提炼成可复用的论文生成 prompt 和 skill 规则。
```

### 4. 规范图表和 Notebook

```text
请为第四章所有图表生成 Jupyter Notebook 代码，要求中文标题、中文轴标题、300 dpi、bbox_inches='tight'，并避免纵轴标题被裁切。
```

## 论文质量规范

本 skill 默认遵守以下规则：

- 中文统一使用宋体；
- 英文与数字统一使用 Times New Roman；
- 正文段落首行缩进两字符；
- 标题行不缩进；
- 图题位于图下，格式为 `图x-x：图名`；
- 表题位于表上，格式为 `表x-x：表名`；
- 图表必须靠近对应分析段落；
- 表格第一行加粗、居中，黑白线条即可；
- 公式必须解释变量含义和业务含义；
- 参考文献必须在正文中形成对应引用；
- 不允许只罗列图表，必须有分析解释；
- 不允许预设某算法必然最优，必须基于指标结果下结论。

## 结果分析范式

每个重要图表后，建议按照以下四层写作：

```text
描述性分析：图表显示了什么？
比较分析：不同算法/方案/年份/路线之间差异是多少？
机制解释：为什么会出现这种差异？
管理含义：该结果对执行、排班、资源配置或决策有什么意义？
```

常用句式：

```text
从数据层看，……；从算法层看，……；从管理层看，……。
该低装载率并不意味着算法失效，而是容量约束与不可拆分需求共同作用的结果。
遗传算法并非所有单项指标下绝对最优，但在复杂约束表达、可扩展性和综合表现方面更适合作为核心方法。
```

## 脚本使用

检查 Word 文档：

```powershell
python scripts/check_docx_paper.py path\to\paper.docx
```

生成 Notebook 模板：

```powershell
python scripts/make_notebook_template.py figures_template.ipynb --figures 6
```

## 设计原则

这个 skill 的目标不是“替用户写一篇泛泛论文”，而是帮助用户把现有材料加工成具备课程提交标准的研究报告：

- 保留用户已有主题、数据和结论；
- 对薄弱章节做深化分析；
- 对图文关系做重组；
- 对 Word 格式做规范化；
- 对代码和图表生成流程做可复现封装。

## License

未指定开源许可证。上传到公开 GitHub 仓库前，建议根据实际用途补充许可证文件。
