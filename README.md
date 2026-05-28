# Course Paper Generation Skill

一套面向课程论文、课程报告、案例研究和算法实验论文的 Codex Skill。它沉淀自循环取货路径优化课程论文项目，但目标是通用化：从材料、数据、草稿或要求出发，生成结构完整、图表可复现、Word/PDF 可交付的标准课程论文。

## 项目定位

这个仓库目前包含两套相关 skill：

```text
course-paper-generation-skill/        # 早期通用课程论文生成 skill
course-paper-report-generator/        # 本次整理的课程报告生成与规范排版 skill
```

其中，`course-paper-report-generator/` 更强调以下能力：

- 基于现有 Word/PDF 草稿做深化修改，而不是推翻重写；
- 统一课程论文的字体、段落、图题、表题、公式和参考文献格式；
- 强化“结果展示 + 描述性分析 + 比较分析 + 管理解释”的写作闭环；
- 生成或检查论文配套 Python/Jupyter Notebook 图表代码；
- 对算法类、案例类、设施规划类课程报告进行图文重组和质量校验。

示范案例位于：

```text
examples/milk-run/
```

## 能力范围

- 解析课程要求、评分标准、草稿、数据和参考文献。
- 构建论文题目、摘要、目录、章节逻辑和论证链。
- 生成或重构 Word/PDF 课程论文。
- 生成可复现图表、流程图、算法对比图和表格。
- 保留修订版本，避免覆盖用户已经确认的成果。
- 对标题层级、引用、图表编号、公式、数据口径和交付格式做质量检查。

## 目录结构

```text
.
├── README.md
├── requirements.txt
├── course-paper-generation-skill/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   └── scripts/
├── course-paper-report-generator/
│   ├── README.md
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   └── scripts/
└── examples/milk-run/
    ├── scripts/
    └── outputs/
```

## 安装使用

把需要使用的 skill 目录安装到 Codex skills 目录，或作为独立技能仓库管理。

例如安装本次整理的课程报告生成 skill：

```powershell
Copy-Item -Recurse course-paper-report-generator $env:USERPROFILE\.codex\skills\
```

典型触发提示词：

```text
使用 course-paper-report-generator 帮我基于当前 Word 草稿深化第六章，并统一图表与排版。
```

## 示例

`examples/milk-run/` 保留了循环取货路径优化论文项目的核心脚本和最终输出，可作为这个 skill 的真实样例：

- 路径优化与算法对比；
- 论文图表生成；
- Word/PDF 课程论文交付；
- 结果分析与管理含义扩写。
