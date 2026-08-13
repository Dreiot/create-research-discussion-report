---
name: create-research-discussion-report
description: Create or substantially revise evidence-grounded Chinese academic advisor discussion reports in DOCX from project authorities, current reports, experiment summaries, and local artifacts. Use for project-stage reports, group-meeting discussion documents, method-and-experiment summaries, formula-heavy research status reports, or revisions that must reduce engineering noise, preserve negative evidence and claim boundaries, explain initialization and end-to-end optimization flows to readers outside the project, render formulas and inline variables as native Word OMML, normalize Chinese/English fonts, and end with concise decisions for a supervisor.
---

# Create Research Discussion Report

Turn heterogeneous project state into a concise, decision-ready academic DOCX. Treat the report as a research argument, not a project log.

## Workflow

### 1. Establish authority and scope

- Read the requested DOCX completely.
- Locate the actual project root and read current authorities such as `AGENTS.md`, `docs/PROJECT_CORE.md`, and `docs/CURRENT_STAGE.md` when present.
- Verify branch, HEAD, remote relationship, index, and worktree before using repository claims.
- Separate formal accepted evidence, exploratory evidence, plans, failures, and unavailable evidence.
- Do not run experiments, access a protected test set, or upgrade a claim unless the user explicitly authorizes it.
- Confirm whether the source may be overwritten. Preserve unrelated files and edits.

### 2. Build a compact evidence packet

Record the research question, exact objective, variable meanings, component roles, experiment settings, comparison rationale, results, negative evidence, claim ceiling, open decisions, and source locations. Omit task IDs, credentials, retries, internal logs, and other engineering noise from the report body.

Read [references/evidence-boundaries.md](references/evidence-boundaries.md) when the project has formal/exploratory evidence tiers, protected artifacts, or governance files.

### 3. Plan the narrative

Use this default order unless the project requires a small adaptation:

1. 研究问题与优化目标
2. 方法
3. 实验
4. 结论与后续方向
5. 待决策问题

Place the complete objective and a short symbol table before component explanations. Group every experiment as a continuous unit: setting and purpose, comparison methods and why they are used, results, analysis, and boundary. Keep “根据目前结果下一步可考虑的方向” short and actionable.

Read [references/report-structure.md](references/report-structure.md) before drafting or restructuring the report.

### 4. Explain for an adjacent researcher

- Define the main model or task in one short paragraph.
- For iterative, alternating, solver-based, or three-stage-plus methods, begin the method section with compact pseudocode that exposes initialization, state transfer, fitting, selection, stopping, and final output.
- Trace every recurring state from its first value through each update. State whether initialization is fixed, random, data-derived, warm-started, or solver-produced; include seeds, repeats, and invalid-state handling when they affect interpretation.
- Map the complete objective to its procedural components. For any method variable absent from the top-level objective, identify it as an intermediate representation, auxiliary variable, fitted parameter, solver variable, selection metric, or final-evaluation quantity, and state where it enters the workflow.
- Explain every comparison method in one or two sentences: its principle, role, and reason for inclusion.
- Explain unfamiliar concepts where first used, including data splits, selection criteria, solver roles, Pareto/non-dominance, or hardware backends.
- Prefer plain academic prose. Avoid tutorial detours and AI-styled headings.
- Distinguish mechanism, candidate generation, fitting, selection, and final evaluation.

Read [references/method-workflow.md](references/method-workflow.md) whenever the method has nontrivial initialization, iterative updates, multiple optimization stages, candidate generation and selection, or data-split-dependent fitting.

### 5. Author native Word mathematics

- Use native OMML for every display equation and inline mathematical variable.
- Use italic for scalars and indices, bold italic for vectors and matrices, bold upright for fixed matrix symbols when appropriate, and upright for functions, operators, digits, and transpose marks.
- State the objective before describing components. Explain every symbol or component appearing in an equation.
- Do not leave caret notation, Unicode pseudo-formulas, or raw Greek variables in ordinary Word text.

Read [references/math-and-results-style.md](references/math-and-results-style.md) before generating equations, tables, or numeric summaries.

### 6. Format results for discussion

- Display absolute rates and AUC values as percentages with two decimals.
- Display AUC differences as `高 1.12%` or `低 1.12%`, preserving direction without `pp`.
- State once that these are absolute differences after percentage conversion, not relative change rates.
- Keep counts, rule numbers, W/T/L, sample sizes, confidence intervals, and unavailable fields visible where relevant.
- Preserve negative and mixed findings next to positive findings.

### 7. Apply the document style

- Use 宋体 for Chinese text.
- Use Times New Roman for Latin text and mathematics.
- Normalize run-level, style-level, and OMML font declarations after generation; remove theme-font indirection.
- Use restrained academic headings, compact tables, repeating table headers, and `w:cantSplit` on table rows.
- Prefer 5–8 information-dense pages for an ordinary advisor discussion report; never create blank or nearly blank spill pages solely to force section starts.

Use the installed `documents` capability for DOCX authoring and rendering. Reuse a trusted local template only when its styles and evidence boundary match the task.

### 8. Validate before delivery

1. Run `python scripts/audit_docx_report.py <report.docx>`.
2. Render the latest DOCX through Word or the available DOCX renderer.
3. Inspect every page at readable zoom.
4. Check formulas, inline variables, fonts, table wrapping, repeated headers, page breaks, and footer fields.
5. Apply the method-completeness gate in `references/method-workflow.md`; do not accept a method section if a reader cannot reconstruct initialization, state transfer, selection, and final output without opening the code.
6. Reopen the final target after overwrite and verify its hash or content identity against the accepted staging file.

Do not deliver until structural audit and visual inspection both pass.

## Output contract

- Deliver the requested DOCX only unless the user requests previews or source scripts.
- State the evidence date and limitations in the report.
- End with a small set of genuine supervisor decisions, not generic next steps.
- Report what was overwritten and what was deliberately left untouched.
