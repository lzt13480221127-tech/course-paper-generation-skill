# Course Paper Generation Skill

一套面向课程论文、课程报告、案例研究和算法实验论文的 Codex Skill。它沉淀自循环取货路径优化课程论文项目，但目标是通用化：从材料、数据、草稿或要求出发，生成结构完整、图表可复现、Word/PDF 可交付的标准课程论文。

## 项目定位

这个项目适合上传为独立 GitHub 仓库，建议仓库名：

```text
course-paper-generation-skill
```

核心 skill 位于：

```text
course-paper-generation-skill/
```

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
└── examples/milk-run/
    ├── scripts/
    └── outputs/
```

## 安装使用

把 `course-paper-generation-skill/` 目录安装到 Codex skills 目录，或作为独立技能仓库管理。

常用脚手架：

```bash
python course-paper-generation-skill/scripts/create_workspace.py ./my-course-paper --profile algorithm-case-study
```

图表风格工具：

```python
from course_paper_plot_style import apply_course_paper_style
apply_course_paper_style(plt)
```

## 示例

`examples/milk-run/` 保留了循环取货路径优化论文项目的核心脚本和最终输出，用作这个 skill 的真实样例：

- 路径优化与算法对比
- 论文图表生成
- Word/PDF 课程论文交付

