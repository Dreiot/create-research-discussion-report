# Method workflow and initialization

Use this reference for iterative, alternating, solver-based, multi-stage, or candidate-selection methods. The goal is not to reproduce a derivation; it is to let a neighboring researcher reconstruct one complete optimization pass without reading the code.

## 1. Start with a compact algorithm view

Place concise pseudocode near the beginning of the method section when the method has at least three dependent stages, nontrivial initialization, repeated updates, candidate generation and selection, or different data splits serving different roles.

Show, in order:

1. Inputs, fixed hyperparameters, and data partitions.
2. Initialization of every state used in the first update.
3. The main transformation, optimization, or candidate-generation steps.
4. Parameter fitting or refitting performed for each candidate.
5. Selection criterion and deterministic tie-breaking when present.
6. Stopping condition or fixed iteration/repeat budget.
7. Final refit and final output.

Keep the pseudocode conceptual and evidence-bound. Do not invent implementation details that are absent from the approved sources.

## 2. Make initialization explicit

For every model state, latent representation, mask, projection, center, weight, or solver variable used before its first update, state:

- its initial value or construction rule;
- whether it is fixed, random, data-derived, warm-started, or solver-produced;
- which data partition is used to construct it;
- its dimensions when dimensions prevent ambiguity;
- the random seed and repeat mechanism when randomness matters;
- how invalid states such as an empty subset, all-zero mask, singular system, or failed solver result are handled.

If there is no unique initial solution, say so directly. For example, distinguish a fixed rule library from multiple solver-generated nonempty candidate masks.

When an initial state produces the first intermediate representation, show that transfer explicitly, such as initial projection to latent representation, raw firing to normalized firing, or candidate mask to refitted model.

## 3. Connect objective, components, and variables

After presenting the complete objective, explain what the objective does and does not optimize. Map each objective term to the component or update that realizes it.

For every important variable that does not appear in the top-level objective, assign one role:

- intermediate representation;
- auxiliary optimization variable;
- parameter fitted conditionally after candidate generation;
- solver encoding or submitted coefficient;
- validation or selection metric;
- threshold or decision rule;
- final-evaluation quantity.

State where the variable is created, what consumes it next, and whether it changes the optimized energy, the fitted predictor, the selected structure, or only the reported evaluation.

Do not imply that minimizing a candidate-generation objective automatically minimizes validation error or yields the final trained model unless the evidence explicitly proves that equivalence.

## 4. Preserve stage and data boundaries

Keep these stages visibly distinct when applicable:

| Stage | Required explanation |
| --- | --- |
| Mechanism | The mathematical relation or inductive bias being introduced |
| Candidate generation | What is searched or proposed and under which objective |
| Fitting or refitting | Which parameters are estimated for a fixed candidate |
| Structure selection | Which split, metric, and tie-break choose among candidates |
| Final refit | Which data are reused after the structure is frozen |
| Final evaluation | Which protected or held-out data are accessed, and whether this has actually occurred |

If the current evidence stops before final evaluation, end the algorithm at the verified boundary and label all later steps as protocol, not completed results.

## 5. Method-completeness gate

Before accepting the report, verify that a reader can answer all of the following from the document alone:

- What is the first computable state after the raw input?
- How is every state needed by the first update initialized?
- What passes from one component to the next?
- Which objective term or procedural role explains each important variable?
- How are candidates generated, fitted, compared, and selected?
- What stops the optimization or fixes its budget?
- Which data partition is used at every stage?
- What is refitted after selection, and what is the final output?
- Which steps are verified results and which remain planned protocol?

If any answer requires opening source code or relying on project history, add one concise explanation, equation, symbol-table entry, or pseudocode line to the report.
