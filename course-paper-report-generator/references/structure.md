# Standard Course Paper Structure

Use this structure when the user asks for a complete Chinese course paper/report.

## Default Section Logic

1. **Title**
   - Preserve the user-specified title exactly unless asked to optimize it.
   - If a subtitle is unnecessary or forbidden, remove it.

2. **Abstract**
   - Use the sequence: background → case/data → method → key result → conclusion/management value.
   - Include concrete metrics when available.

3. **Keywords**
   - 4-7 terms.
   - Include the case domain, method, and key management concept.

4. **Introduction**
   - Start from the industry/business/case problem, not the algorithm.
   - Explain why the problem matters.
   - State the research object, questions, method route, and paper contribution.

5. **Literature Review**
   - Only review concepts and methods that support the case.
   - Avoid unrelated literature padding.
   - Every listed reference should be cited in the body.

6. **Data and Case Description**
   - State data source, data nature, fields, sample size, time range if any.
   - If the data is synthetic/expanded/teaching-only, say so clearly.
   - Include preprocessing or transformation logic.

7. **Model and Indicator Definition**
   - Define sets, variables, parameters, objective functions, constraints, and evaluation metrics.
   - Explain each formula in business language.

8. **Algorithm Design / Method Construction**
   - Explain why the algorithm is suitable.
   - Show encoding, cost/fitness function, operations, repair logic, parameters, and reproducibility setup.
   - Keep method diagrams here.

9. **Calculation and Results**
   - Keep result charts/tables here.
   - Analyze results rather than displaying them.
   - Use the “description + comparison + mechanism + management meaning” structure.

10. **Discussion / Management Implications**
   - Translate calculations into execution, scheduling, resource allocation, strategy, or process-control implications.
   - Discuss limitations honestly.

11. **Conclusion**
   - Summarize findings by research question.
   - Avoid merely repeating the abstract.
   - Include method value, case conclusion, implementation value, and future work.

12. **References**
   - Keep numbering consistent with in-text citations.
   - Do not list uncited references.

13. **Appendix**
   - Put complete routes, full code, notebook instructions, robustness checks, expanded figures, and extra comparisons here.

## Algorithm Comparison Chapter Template

Use this when a chapter compares several algorithms:

1. Comparison setting and metrics.
2. Algorithm A: basic idea, calculation logic, result, interpretation.
3. Algorithm B: basic idea, calculation logic, result, interpretation.
4. Algorithm C: basic idea, calculation logic, result, interpretation.
5. Core algorithm: detailed mechanism, result, strengths and limitations.
6. Comprehensive comparison and final method selection.
7. Transition to the next modeling chapter.

Do not say “algorithm X is best” without specifying the metric. Prefer:

> Algorithm X is not absolutely optimal in every single metric, but it is more suitable as the core method because it performs better in integrated quality, constraint handling, and extensibility.
