# Human-facing Chinese academic writing

## Write for the reader, not the production process

The report should answer what was studied, how it was designed, what was observed, and what the result means. Internal preparation work should remain invisible.

Do not add these items by default:

- “证据来源” or repository-source sections;
- Git branch, commit, hash, file path, or artifact identity;
- internal workflow state, terminal string, or implementation bookkeeping label;
- repetitive “边界”“尚未建立”“禁止表述” boxes;
- task IDs, retries, raw logs, or full per-run result dumps.

If one of these details is scientifically necessary, translate it into ordinary academic language and place it where it affects interpretation.

## Use Chinese-first terminology

- Prefer the established Chinese academic term.
- At first occurrence, write `中文名称（必要的英文缩写）`; afterwards use the Chinese term or abbreviation consistently.
- Preserve exact variables, APIs, code identifiers, and standard abbreviations when translation would destroy identity, for example `Q_submit`, OLS, TSK, NMI, or ACC.
- Preserve official dataset, benchmark, method, product, and corpus names when their established identity is English. Names such as `Caltech101-7`, `Reuters-1200`, `UCI Mfeat`, and `MHEALTH` should not be translated merely to make the surrounding prose look more Chinese.
- Do not repeatedly alternate between Chinese and English names for the same concept.

Prefer these forms in reader-facing prose:

| Avoid as default prose | Prefer |
| --- | --- |
| baseline | 对比方法；必要时首次写“对比方法（baseline）” |
| fit | 拟合 |
| runner | 运行程序或执行器 |
| checkpoint | 检查点、中间结果或已保存模型，按语境选择 |
| quota | 配额；必要时首次保留 quota |
| claim | 论文主张或结论 |
| evidence closure | 结果完整性或数据完整性检查 |
| matched uniform | 同结构均匀权重对照 |

Keep a method's official short name when it functions as an identity. Explain it once rather than translating it differently in each section.

## Use a two-character first-line indent for body prose

- Give ordinary body paragraphs an exact two-Chinese-character first-line indent.
- In WordprocessingML, prefer `w:ind w:firstLineChars="200"` on the body or `Normal` style. This expresses two character units and is more robust than approximating the indent with points.
- Explicitly reset every table-cell paragraph to zero first-line indentation, zero spacing before and after, and single line spacing so it does not inherit body-paragraph formatting. In WordprocessingML, set both `w:firstLineChars="0"` and `w:firstLine="0"`; setting only the character value can still leave Word reporting the inherited point-based indent. Center all table-cell paragraphs, including headers and descriptor columns.
- Do not indent titles, headings, table cells, captions, equations, lists, callouts, code blocks, source lines, or short labels.
- Do not insert spaces or full-width spaces manually to imitate paragraph indentation.

## Use natural academic prose

- Lead with the finding or design choice, then explain the supporting detail.
- Prefer paragraphs of connected sentences over status labels and fragments.
- Use headings that describe the research content, not the production workflow.
- Avoid repeated meta-language such as “本节将”“需要指出的是”“从证据角度看”.
- State one limitation once, next to the result it qualifies.
- Use a callout only when it improves navigation; do not convert every conclusion into a boxed notice.

## Let the user decide only when it matters

Ask the user when two plausible presentations would materially change emphasis or length, such as:

- a compact method overview versus a detailed algorithm explanation;
- one primary metric versus several metric families;
- a short main document versus a long appendix;
- overwriting an existing file versus creating a new edition.

Do not ask about routine heading wording, ordinary table styling, or other reversible details when a clear professional default exists.
