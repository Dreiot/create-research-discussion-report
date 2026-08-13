# Mathematics and result style

## Word mathematics

Use Office Math Markup Language (OMML), not plain text or an equation screenshot.

| Element | Style |
| --- | --- |
| scalar, parameter, index | italic |
| vector or matrix | bold italic |
| identity or fixed upright matrix symbol | bold upright when appropriate |
| function name, operator, digit, punctuation | upright |
| transpose marker | upright |

Render inline variables with `m:oMath`. Render display equations with `m:oMathPara` containing `m:oMath`. Give every math run explicit Times New Roman declarations and set the document math font to Times New Roman.

After the objective, explain every symbol, including dimensions or fixed values when they matter. Do not repeat a symbol as raw ordinary text later; insert inline OMML.

## Result conversion

- Convert `0.9534` to `95.34%`.
- Convert an absolute AUC difference of `-0.0112` to `低 1.12%`.
- Convert an absolute AUC difference of `+0.0112` to `高 1.12%`.
- Convert a positive gap shift of `0.0208` to `上移 2.08%`.
- Keep two decimals for all percentages.
- Do not remove direction. Do not present the converted absolute difference as a relative percentage improvement.

Include one note such as:

> 绝对指标和差值均换算为百分数并保留两位小数；“高/低”表示差值方向，不表示相对变化率。

Keep counts and denominators alongside percentages when they aid interpretation, for example `80.00%（8/10）`.

## Font normalization

Set all ordinary runs and styles to:

- `w:ascii`, `w:hAnsi`, `w:cs`: `Times New Roman`
- `w:eastAsia`: `宋体`

Remove `asciiTheme`, `hAnsiTheme`, `eastAsiaTheme`, and `cstheme` so theme fonts do not override the requested type system.
