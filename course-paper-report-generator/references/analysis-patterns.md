# Analysis Patterns

Use these reusable patterns to deepen course-paper analysis.

## Result Analysis Pattern

For each major table/figure, write one paragraph with four layers:

1. **Describe**: identify the main value, trend, distribution, or contrast.
2. **Compare**: quantify differences between algorithms, groups, years, routes, or indicators.
3. **Explain**: connect the difference to data structure, constraints, or algorithm mechanism.
4. **Interpret**: state what the result means for management, implementation, or decision-making.

Example:

> 表x-x显示，A方法的单次总里程为……，低于B方法……。这一差异主要来自……。从管理角度看，……。

## Data / Algorithm / Management Closure

For important results chapters, form a closed explanation:

> 从数据层看，……。从算法层看，……。从管理层看，……。

Use this when a chapter has many charts but weak analysis.

## Algorithm Comparison Pattern

When comparing algorithms, include:

- transport or prediction efficiency;
- computation efficiency;
- solution quality;
- robustness/stability;
- interpretability;
- management implementability.

Avoid:

> A算法效果最好。

Prefer:

> 在总里程指标上，A与B均达到……；在运行时间上，B更快；但A在约束表达、修复机制和多目标扩展方面更适合作为本文核心方法。

## Quantitative Difference Sentences

Use exact differences when possible:

- `A方法比B方法少……条线路。`
- `A方法单次总里程比B方法减少……km，降幅约为……%。`
- `A方法平均装载率比B方法提高……个百分点。`
- `A方法运行时间比B方法多/少……s。`

Then explain why:

- `原因在于……`
- `这说明……`
- `该结果并不意味着……，而是……`

## Low-Quality Result Interpretation

When a route/group has lower load, score, frequency, or centrality, do not label it as failure too quickly. Explain constraint causes:

- capacity bound;
- indivisible demand;
- spatial distance;
- time window;
- sparse data;
- role specialization;
- sample selection;
- objective-function tradeoff.

Reusable sentence:

> 该低值并不必然表示算法失效，而是……共同作用的结果。

## Management Implication Pattern

Convert results into management meaning:

1. State the operational issue.
2. Link it to a result.
3. Explain the recommended action.
4. Explain the expected benefit.

Example:

> 固定路线可以直接转化为司机班次和供应商发货窗口。由于表x-x中的线路均满足容量约束，企业可将其作为标准作业基础，从而降低每日调度沟通成本。

## Conclusion Pattern

Conclusion should answer research questions:

1. What was modeled?
2. Which method was used?
3. What were the main numerical findings?
4. Why do the findings matter?
5. What remains for future work?

Avoid repeating the abstract word-for-word.
