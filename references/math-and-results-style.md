# Mathematics and result presentation

## Word mathematics

Use Office Math Markup Language (OMML), not equation screenshots or Unicode pseudo-formulas.

| Element | Style |
| --- | --- |
| scalar, parameter, index | italic |
| vector or matrix | bold italic |
| identity or fixed upright matrix symbol | bold upright when appropriate |
| function name, operator, digit, punctuation | upright |
| transpose marker | upright |

Give mathematical runs explicit Times New Roman declarations and set the document math font to Times New Roman.

Include only equations needed for the report's argument. Explain a symbol at first use. Add a symbol table only when several symbols recur and the table improves reading.

## Result tables

- Show only the metrics and comparisons relevant to the requested discussion.
- When repeated runs are available, use `平均值 ± 标准差` by default and state the aggregation unit once.
- Convert rates to percentages when that improves readability and use consistent precision, normally two decimals.
- Express absolute differences naturally, for example `提高 1.12 个百分点` or `降低 1.12 个百分点`; do not describe them as relative percentage changes.
- Include confidence intervals, sample counts, wins/ties/losses, or missing fields only when they affect the conclusion or the user requests them.
- Prefer one compact summary table to long per-run or per-sample output.
- Preserve an important negative or heterogeneous result beside the positive finding it qualifies.

## Font normalization

Set ordinary runs and styles to:

- `w:ascii`, `w:hAnsi`, `w:cs`: `Times New Roman`
- `w:eastAsia`: `宋体`

Remove `asciiTheme`, `hAnsiTheme`, `eastAsiaTheme`, and `cstheme` so theme fonts do not override the requested type system.
