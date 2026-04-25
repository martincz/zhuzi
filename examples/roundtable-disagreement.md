# Roundtable 示例 · 多席位真分歧

> 展示 roundtable 的核心价值：**保留分歧不强行收敛**。两席走完全不同路径，orchestrator 不仲裁，让用户拍板。

输入：

```text
/zhuzi:roundtable 我准备用 4 倍杠杆做 vol selling，过去 3 年回测 Sharpe 2.5，最大回撤 12%，该不该上 100k 实盘
```

默认输出形态：

---

## 主持人结论

**两席结论相反**：Munger 给"过"（在能力圈内 + 数据支持），Taleb 给"停"（4x 杠杆 + vol selling 是典型 fragile barbell 反面，3 年样本不含 tail）。这不是表面分歧，是路径根本不同——一个看 base rate 与激励，一个看 ruin risk。**建议**：先回答一个问题——你能承受 100% 损失（清零）吗？能 → 听 Munger；不能 → 听 Taleb。

## 议题卡

**目标**：产出一张决策表，含是否上线（locked）/ 不做的事（deferred）/ 做完后的验证信号

**召开席位**
- `munger-reviewer` · 涉及决策质量、激励、能力圈
- `taleb-reviewer` · 4x 杠杆 + vol selling 含 ruin risk 与 tail

**弃权席位**
- `lopezdeprado-reviewer` · 议题不含因子研究 / multiple testing 主张（议题已申明 backtest 范围）
- `linus-engineer` · 无代码落地维度

**暂不讨论**
- 不讨论换策略
- 不讨论换券商 / 加保证金机制

## 什么算过关

**1. 风险预算明确**：给出最大可承受损失（绝对值 + 占总流动资产 %），且账户最大回撤触发硬止损规则

**2. 样本充分性**：声明回测样本是否包含 ≥ 1 次 vol crash 事件（2008 / 2018 Volmageddon / 2020-03 / 2024-08 等）

**暂不涉及**：策略选择 / 券商 / 保证金计算

## 席位短评

| 席位 | 结论 | 最大风险 | 必须满足 | 分歧 | 信心 |
|---|---|---|---|---|---|
| Munger | 过 | 见下方展开 | 见下方展开 | 与 Taleb 路径相反 | medium · 与 Taleb 有分歧 |
| Taleb | 停 | 见下方展开 | 见下方展开 | 与 Munger 路径相反 | high · 本席位 core 领域 |

### Munger 展开

**最大风险**：
- `行为金融偏误`（用户被近 3 年好结果激励，忽略 base rate）· vol selling 长期 base rate 是定期被 wipe out 的策略类
- `激励错位`（建议者拿管理费、客户承担清零风险）· 如果是自有资金没这层问题，但要问"为什么不是我亲戚的钱"

**必须满足**：
- 100k 必须是"loss 全部不影响生活"的钱
- 有硬止损规则且写下来贴在屏幕上
- 至少经历 1 次本人亲历过的 drawdown 事件再加杠杆

### Taleb 展开

**最大风险**：
- `Mediocristan 指标审 Extremistan 问题`（试 N 次后对观察 Sharpe 打折才算真显著，而 vol selling 的 Sharpe 在 fat tail 下连数学意义都没有）· Sharpe 2.5 是 Sharpe ratio，意味着假设 normal distribution——vol selling 的 P&L 极度非 normal
- `ergodicity 违反`（单人长期路径和平行宇宙平均是两回事）· 4x 杠杆下 1 次 -25% 回撤就清零，不会有"长期"
- `3 年样本不含 tail`· 2022-2025 是低 vol 期，无 Volmageddon 量级事件

**必须满足**：
- 4x 杠杆 + vol selling 在数学上等于 short tail option，定期清零是其性质而非 bug
- 要做就 barbell：90% 不动，10% 做这个，承认 10% 会清零
- 不要用 Sharpe / max drawdown 作为决策指标，看 worst-case payoff

## 做完会怎样

如果按 Munger 路径上 100k：账户每天有 vol risk premium 收益（约日均 0.3-0.5%），直到一次 vol spike 出现——历史上每 3-5 年一次，触发时 4x 杠杆基本清零。如果按 Taleb 路径走 barbell（10k 上、90k 不动）：日均收益降到 1/10，但 worst-case 损失也是 1/10，长期能复利。两路径的 expected value 在 normal 下 Munger 高，在 fat tail 下 Taleb 高。

**验证信号**：上线后若出现单日 vol spike > 50%（VIX +30 点 / VVIX > 150）账户能否扛住——不能扛住就是 Taleb 对；扛住且 12 个月后 walpha 仍正就是 Munger 对。**这个判定要等真正一次 tail event 才能完成，不是 1 个月内能验证的**。

## 决策表

| 分类 | 内容 | 下一步 |
|---|---|---|
| `locked` | 不在 roundtable 内拍板"该不该上"——这是用户自己的 ruin risk 容忍度问题 | 用户回答"100k 全部归零是否影响生活"决定路径 |
| `deferred` | 不讨论换策略<br>不讨论换券商<br>不讨论加保证金机制 | 不另开议题 |

## 下一步

用户需要先回答 ruin risk 问题。回答"能承受清零"→ 按 Munger 路径执行；回答"不能"→ 按 Taleb barbell 路径执行。要展开席位完整原文或 YAML，说"展开原文"。

---

## 协议笔记

这个例子的价值在于：**两席给完全相反的路由（`go` vs `kill`）orchestrator 不强行调和**。如果硬要"折中建议 2x 杠杆"——那是把 Munger 和 Taleb 的判断都打折了，变成一个谁都不会拍板的妥协。

正确做法是把分歧的**根因**呈现出来（Munger 看 base rate / Taleb 看 ruin），让用户决定自己站哪一侧。这是 roundtable 区别于"几个 prompt 塞给一个 agent"的地方。
