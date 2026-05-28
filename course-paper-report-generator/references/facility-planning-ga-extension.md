# Facility Planning / Genetic Algorithm Extension Prompt

This preserves the user's prior prompt for a facility-planning, milk-run, and genetic-algorithm course paper. Use it when the current task involves the same paper family or the user asks to continue the prior logistics paper workflow.

## Core Requirements

1. Paper title:

   《基于遗传算法的循环取货路径优化与物流平准化研究》

2. If the original GT case data is too small, use the user-provided Excel workbook:

   - Read the explanation sheet first.
   - State clearly that the expanded data is teaching/research synthetic expansion data, used to increase problem complexity and better show the advantages of genetic algorithms.

3. Strengthen literature review and algorithm comparison:

   - Node shortest path / nearest neighbor method.
   - Sweep method.
   - Savings mileage method.
   - Genetic algorithm.
   - Simulated annealing.

   For each method, explain basic idea, suitable scenarios, strengths, and weaknesses.

4. Compare algorithms by multiple dimensions:

   - transport efficiency: total mileage and trips/routes;
   - computation efficiency: runtime and solving complexity;
   - loading quality: load rate and balance;
   - management implementability: suitability for fixed routes and leveling.

5. Conclusion logic:

   Genetic algorithm is not necessarily absolutely optimal under every single metric, but is more suitable as the core method in integrated performance, extensibility, and complex constraint handling.

6. Genetic algorithm chapter must include:

   - parameter definitions;
   - variable definitions;
   - chromosome encoding;
   - fitness function;
   - selection, crossover, mutation, repair mechanism;
   - algorithm parameters such as population size, iterations, crossover probability, mutation probability, elitism;
   - appendix/method notes for main program code and visualization notebook code.

7. Figure and chart requirements:

   - Axis titles must be complete and not cropped.
   - Legends must not block the main plot.
   - Prefer high-resolution paper-friendly figures.
   - Explain the meaning of figures in captions or body text.

8. References:

   - Every reference must correspond to an in-text citation.
   - Use numbered in-text citations.
   - Reference sequence and body citation sequence must match.

9. Style:

   - Formal course paper style.
   - Do not write as PPT copy.
   - Do not assume one algorithm is best before computing.
   - Keep genetic algorithm as the main line, based on sufficient comparison.

10. Outputs:

   - complete paper report;
   - genetic algorithm Python code;
   - runnable notebook code for all figures.
