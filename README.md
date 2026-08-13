<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="Create Research Discussion Report turns project evidence into a formula-native, decision-ready academic DOCX">
</p>

把研究仓库、实验记录和已有 Word 草稿整理成一份简洁、可核验、能直接与他人讨论的学术报告。

它关注的不是“把内容写得更多”，而是把项目状态组织成一条清楚的研究论证：**问题与目标 → 初始化与完整优化流程 → 方法组件 → 分实验设置与结果 → 结论与边界 → 导师决策**。

## 适合什么任务

- 项目阶段总结与导师讨论报告
- 组会方法与实验汇报 DOCX
- 公式较多、需要原生 Word 公式的研究状态报告
- 已有报告内容零散、工程日志过多或结论边界不清的重构
- 需要向未参与项目的老师或同学解释比较方法与关键概念的报告

## 它会保留什么

| 报告要求 | 默认处理 |
| --- | --- |
| 研究证据 | 区分正式、探索、计划、负面和不可用证据 |
| 数学公式 | 展示公式和正文变量均使用 Word 原生 OMML |
| 数学字形 | 标量斜体，向量/矩阵粗斜体，函数与运算符正体 |
| 方法流程 | 交代初始化、变量传递、候选生成、拟合、选择和最终输出 |
| 中英文字体 | 中文宋体；英文与数学 Times New Roman |
| 实验结果 | 百分比保留两位小数；差值写为“高/低 XX.XX%” |
| 实验叙事 | 每项实验连续呈现设置、比较理由、结果、分析和边界 |
| 最终输出 | 简短结论、可考虑方向和真正需要导师决定的问题 |

## 报告结构

```text
1 研究问题与优化目标
  1.1 研究问题与任务说明
  1.2 目标函数
  1.3 变量含义

2 方法
  简要伪代码 → 初始化 → 变量传递 → 组件原理 → 选择与最终输出

3 实验
  设置与目的 → 对比方法及采用理由 → 结果 → 分析

4 结论与后续方向
5 待决策问题
```

## 为什么不是普通的 Word 改写

- **先核验证据。** 优先读取项目权威文档、当前 Git 状态和实验记录，不把聊天记忆当作当前事实。
- **不隐藏负面结果。** 混合方向、失败假设、缺失计时和未完成 outer-test 会与正面结果一起呈现。
- **让外部读者读得懂。** 每个比较方法都会说明原理、实验角色和采用理由；关键数据划分、求解器和选择概念会在首次出现时简要解释。
- **完整交代方法流程。** 对多阶段或迭代方法，说明初始状态如何得到、中间变量如何传递，以及候选如何拟合、筛选和最终重拟合。
- **公式可继续编辑。** OMML 公式不是图片，也不是普通 Unicode 文本。
- **交付前看实际页面。** 结构审计之后还要渲染并逐页检查表格、公式、字体和分页。

## 安装

### Windows PowerShell

```powershell
git clone https://github.com/Dreiot/create-research-discussion-report.git `
  "$env:USERPROFILE\.codex\skills\create-research-discussion-report"
```

### macOS / Linux

```bash
git clone https://github.com/Dreiot/create-research-discussion-report.git \
  ~/.codex/skills/create-research-discussion-report
```

重新启动或刷新 Codex 后即可调用。

## 使用示例

```text
Use $create-research-discussion-report to revise this project-stage DOCX.
Read the current project authorities, keep negative evidence, use native OMML,
and finish with the questions my advisor needs to decide.
```

也可以直接用中文：

```text
使用 $create-research-discussion-report，把这份项目状态报告整理成导师讨论版。
目标函数放在方法之前，每项实验连续说明设置、对比方法、结果和分析，允许覆盖原文件。
```

## 内置 DOCX 审计

skill 附带一个确定性检查器，用于核验字体、OMML、表格行分页保护以及百分比格式：

```bash
python scripts/audit_docx_report.py /path/to/report.docx
```

一次真实的公式密集型报告检查输出如下：

```text
OMML: 5 display, 19 inline
Tables: 48/48 protected rows
Math styles: p / i / b / bi
OK: report contract passed
```

这只是结构检查。最终交付仍必须经过 Word 或可靠 DOCX 渲染器的逐页视觉验收。

## 文件结构

```text
create-research-discussion-report/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── evidence-boundaries.md
│   ├── method-workflow.md
│   ├── math-and-results-style.md
│   └── report-structure.md
├── scripts/audit_docx_report.py
└── assets/readme/hero.svg
```

## 边界

- 默认不运行新实验、不访问受保护测试集、不发起外部平台任务。
- 不把 exploratory 结果提升为正式论文结论。
- 不以未检到相邻工作证明“首次”或“唯一”。
- 不把缺失计时解释为速度优势，也不把不显著解释为等效。
- 对外发布前仍应人工检查项目隐私、作者信息和未公开结果。

## License

[MIT](./LICENSE)
