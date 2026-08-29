# Source grounding

Use project sources to keep the report accurate without turning the report into a source inventory.

## Build a private fact sheet

Record only what is needed to write the requested document:

- the current research question or direction;
- the method or design actually used;
- the objective, inputs, outputs, and component roles;
- the experiment protocol and comparison rationale;
- the completed results and their aggregation units;
- important mixed, negative, incomplete, or unavailable findings;
- the strongest interpretation supported by those results.

Prefer current code, executed experiment outputs, maintained project documents, and the report being revised over chat recollection. When several result generations exist, determine which one the user means before combining them.

## Translate source state into natural prose

Use source status internally, then write it for a human reader:

| Source state | Reader-facing treatment |
| --- | --- |
| Completed result | State the result directly within the tested scope. |
| Preliminary or exploratory result | Use wording such as “当前实验显示” or “初步结果表明”. |
| Mixed or negative result | Place it beside the positive finding it qualifies. |
| Planned work | Describe it as a proposed next step, not a completed result. |
| Unavailable result | Mention it only when the absence changes the interpretation. |

Do not expose the private fact sheet, repository paths, hashes, commit identities, internal state strings, or a list of source files in the report by default. If the user explicitly requests provenance, add the smallest useful note or appendix rather than restructuring the whole document around source bookkeeping.

## Keep conclusions proportional

- Do not turn one favorable dataset into a general advantage.
- Do not turn a non-significant difference into equivalence.
- Do not infer efficiency from missing timing or memory measurements.
- Do not infer novelty merely because no identical formula was found.
- Preserve an important failure or heterogeneous result when omitting it would change the reader's conclusion.
