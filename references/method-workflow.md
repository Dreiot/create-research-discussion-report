# Method explanation depth

Use the least detail that lets the intended reader understand the design and the reported result.

## Choose a depth level

### Compact overview

Use by default for progress summaries and result-focused reports. State:

- the task and inputs;
- the objective or central design idea;
- the role of the important components;
- the output used by the experiments.

Do not add pseudocode, initialization details, or every alternating update unless they are needed for the discussion.

### Component explanation

Use when the report compares design choices or mechanisms. Explain the inputs, transformation, output, and purpose of each component that affects the comparison. Include only the state transfer needed to understand the tested hypothesis.

### Reconstructable workflow

Use only when the user requests a technical method explanation or when the scientific interpretation depends on exact execution details. Then show, as applicable:

1. inputs, fixed parameters, and data partitions;
2. initialization of states used by the first update;
3. the main transformations or optimization steps;
4. candidate generation, fitting, and selection;
5. stopping conditions or fixed budgets;
6. final output and evaluation boundary.

Keep the workflow conceptual and source-grounded. Do not invent implementation details absent from the current code or design.

## Explain only consequential details

Include a seed, fallback, invalid-state rule, solver setting, or intermediate variable only when it affects reproducibility, a comparison, or the interpretation of a result. Otherwise omit it from the main report.

If detailed workflow is useful but would interrupt the main narrative, place it in a compact appendix only when the user wants that depth.
