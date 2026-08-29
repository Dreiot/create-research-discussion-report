---
name: create-research-discussion-report
description: Create or substantially revise human-readable Chinese academic discussion reports in DOCX from concrete method designs, code, experiment results, figures, and project materials. Use for early- or mid-stage direction discussions, project progress summaries, method-and-experiment reports, group meetings, or formula-heavy research documents that need adaptive organization, Chinese-first terminology, concise result presentation, native Word mathematics, and visually verified delivery.
---

# Create Research Discussion Report

Turn concrete project designs and results into a natural Chinese academic report for a supervisor or neighboring researcher. The report should read like a human research discussion, not a project log, repository inventory, or process record.

## Workflow

### 1. Understand the report purpose and source material

- Read the requested DOCX completely when revising an existing report.
- Read the actual method design, relevant code, experiment summaries, tables, figures, and current project documents needed to support the requested content.
- When a governed repository has current authority files, use them to avoid stale or contradictory statements. Treat Git state, file paths, internal statuses, and source inventories as drafting context rather than report content.
- Do not run new experiments, access protected data, or change the project method unless the user explicitly requests that work.
- Preserve the original file unless the user authorizes overwrite or the requested target is unambiguous.

### 2. Choose the appropriate depth and organization

Identify what the report is meant to accomplish: explore a direction, explain a design, summarize a stage, discuss experiments, compare alternatives, or consolidate current conclusions. Select only the content blocks that serve that purpose.

There is no mandatory chapter sequence. An early-stage report may place a diagnostic experiment beside the direction it informs; a method-design report may lead with a design choice; a result-focused report may move quickly from protocol to tables. Organize material along the shortest coherent research argument rather than a fixed template.

Ask the user only when an unresolved presentation choice would materially change the document, such as:

- brief method overview versus reconstructable technical explanation;
- which competing result families or metrics should be foregrounded;
- whether a long appendix is wanted;
- whether an existing file may be overwritten.

When one choice is clearly supported by the request and materials, proceed with that choice.

Read [references/report-structure.md](references/report-structure.md) before drafting or substantially restructuring a report.

### 3. Ground the report in current project facts

Build a compact private fact sheet containing the research question, method identity, objective, component roles, experiment settings, comparison rationale, results, limitations, and current conclusions. Use it to keep the report accurate, but do not expose repository paths or internal project bookkeeping in the reader-facing document.

Preserve mixed, negative, incomplete, and unavailable results when they affect the interpretation. State them in natural research language next to the conclusion they qualify.

Read [references/source-grounding.md](references/source-grounding.md) when the project has several code paths, experiment generations, superseded results, or conflicting drafts.

### 4. Write for a human academic reader

- Lead each substantive section with the result, design choice, or question it addresses.
- Prefer connected academic prose over status labels, one-line fragments, internal identifiers, or repeated disclaimer boxes.
- Use Chinese terminology by default. Give a necessary English abbreviation or exact code identity at first occurrence, then use the Chinese term or abbreviation consistently.
- Keep exact variables, APIs, code identifiers, and standard abbreviations unchanged when translation would destroy identity, such as `Q_submit`, OLS, or TSK.
- Keep official proper names in their established form when translation would make identification harder. This includes dataset and benchmark names such as `Caltech101-7`, `Reuters-1200`, `UCI Mfeat`, and `MHEALTH`, as well as official method, product, and corpus names.
- Do not create a “证据来源” section or show Git SHAs, repository paths, hashes, internal workflow states, artifact identities, terminal strings, or similar implementation bookkeeping unless the user explicitly requests those details for the report.
- Explain an unfamiliar comparison method in one or two sentences: its principle, experimental role, and reason for inclusion.
- Mention a limitation once where it changes interpretation. Do not repeat the same boundary throughout the report.

Read [references/human-writing-style.md](references/human-writing-style.md) before drafting or rewriting the reader-facing prose.

### 5. Match method detail to the discussion need

By default, explain the research problem, objective, inputs and outputs, and the role of the important components. Do not automatically expand initialization, alternating updates, solver states, or the full optimization process.

Use a reconstructable workflow, pseudocode, state transfer, stopping rule, or detailed initialization only when the user requests a method explanation, when the design choice under discussion depends on those details, or when omitting them would make the reported result scientifically ambiguous.

Read [references/method-workflow.md](references/method-workflow.md) only when the report needs more than a compact method overview.

### 6. Author mathematics and results clearly

- Use native Word OMML for display equations and mathematical variables that need mathematical typesetting.
- State only the equations needed for the report's argument. Explain symbols at first use; add a symbol table only when it materially improves readability.
- Use italic for scalars and indices, bold italic for vectors and matrices, and upright type for functions, operators, digits, and transpose marks.
- Prefer compact result tables. Show only the metrics and comparisons relevant to the user's question.
- Use mean ± standard deviation by default when repeated runs are available, and state the aggregation unit once.
- Center each table on the page. Center numeric headers and result cells; a descriptor column may remain left-aligned when that reads better.
- In a comparable per-dataset result table, bold the complete displayed cell for the best method under each dataset, metric, budget, and experimental setting. Determine the best value from unrounded data, respect whether the metric is higher- or lower-is-better, and bold all exact ties.
- Preserve negative and mixed results beside positive findings. Do not dump complete per-run rows when a summary answers the research question.

Read [references/math-and-results-style.md](references/math-and-results-style.md) before generating equations, tables, or numeric summaries.

### 7. Apply the document style

- Use 宋体 for Chinese text and Times New Roman for Latin text and mathematics.
- Normalize run-level, style-level, and OMML font declarations; remove theme-font indirection.
- Give ordinary body paragraphs a two-Chinese-character first-line indent. Do not apply it to titles, headings, table cells, captions, equations, lists, callouts, code blocks, source lines, or short labels.
- Use restrained academic headings, compact tables, repeating table headers, and `w:cantSplit` on table rows.
- Match the page count to the actual material. Do not pad the report to reach a target length or create blank spill pages.

Use the installed `documents` capability for DOCX authoring and rendering. Reuse a trusted local template only when it suits the audience and requested content.

### 8. Validate before delivery

1. Run `python scripts/validate_docx_report.py <report.docx>`.
2. Render the latest DOCX through Word or the available DOCX renderer.
3. Inspect every page at readable zoom.
4. Check formulas, fonts, table wrapping, repeated headers, page breaks, and footer fields.
5. Confirm that tables are centered and that every comparable per-dataset result cell with the best method is correctly bolded, including ties.
6. Confirm that the visible report contains only the requested level of method detail and results.
7. Reopen the final target after overwrite and verify its hash or content identity against the accepted staging file.

Do not deliver until structural validation and visual inspection both pass.

## Output contract

- Deliver the requested DOCX only unless the user requests previews or source scripts.
- Do not add source inventories, repository bookkeeping, mandatory decision sections, or generic next steps to fill space.
- End with the strongest supported interpretation of the current design or results. Include a user or supervisor decision only when a genuine unresolved choice remains.
- If a presentation detail is materially ambiguous, let the user decide; otherwise use the clearest human-readable default.
- Report outside the document what was overwritten and what was deliberately left untouched.
