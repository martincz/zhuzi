# Roundtable Seat Registry

> 这是 `/zhuzi:roundtable` 的席位权威表。若 `roundtable.md`、README、AGENTS、agent 描述段对当前席位或默认 `stages` 的说法不一致，以本文件为准。

## 当前席位

| 席位 | agent | 职责 | 默认 `stages` | 擅长领域（议题匹配关键词） |
|---|---|---|---|---|
| 风险结构 | `taleb-reviewer` | 尾部风险、fragility、凸性、barbell、skin in the game | `[1]` | 不确定性 / 尾部风险 / 脆弱性 / 凸性 / ruin risk / barbell / 冗余 / 选择权 / 依赖链风险 / skin-in-the-game / 厚尾分布 |
| 决策质量 | `munger-reviewer` | 愚蠢清单、认知偏误、激励结构、能力圈、机会成本 | `[1]` | 投资决策 / 商业判断 / 产品策略 / 组织决策 / 认知偏误审视 / 能力圈边界 / 机会成本 / 安全边际 / 激励结构 / 护城河 / Lollapalooza |
| 证据质量 | `lopezdeprado-reviewer` | 研究诚信、associational vs causal、实验/评估设计、backtest overfitting、DSR/PBO/CPCV | `[1]` | 研究方法论 / 实验设计 / 因果声明 / benchmark / A-B test / eval / data leakage / backtest overfitting / p-hacking / multiple testing / specification error / Deflated Sharpe / Purged K-Fold / CPCV / 研究流程诊断 |
| 代码 | `linus-engineer` | 架构、可行性、review、重构、实施、good taste | `[2]` 或 `[1,2]` | 软件架构 / 数据结构 / API 边界 / 并发 / 性能 / 可靠性 / 代码实施 / 可行性评估 / 重构 / 工程纪律 / 技术选型 / good taste 审视 |

## 召开纪律

- 语义匹配优先于关键词精确命中。`激励结构` 和 `激励设计` 算同一域。
- Quick 模式下评议席位默认不超过 3 个；超过时优先保留最可能发现 hard blocker 或真实分歧的席位。
- `N >= 1` 合法。`N = 0` 时停止流水线；`N = 1` 时退化为单席位 roundtable。

## 默认 `stages` 规则

| 席位 | 策略/投资/商业/组织决策 | 研究/实验/因果评估 | 纯代码实施议题 | 工程决策议题 | 混合议题 |
|---|---|---|---|---|---|
| Taleb | 含不确定性 / 尾部 / 脆弱性 → `[1]` | 仅在评估暴露尾部风险时 `[1]` | 弃权 | 仅在工程方案有系统性脆弱性时 `[1]` | `[1]` |
| Munger | 含判断质量 / 激励 / 能力圈 / 机会成本 → `[1]` | 仅在指标激励或研究者偏误关键时 `[1]` | 弃权 | 弃权 | `[1]` |
| López | evidence claim 关键时 `[1]` | 含实验 / 因果 / benchmark / eval / 回测 → `[1]` | 弃权 | 弃权 | `[1]` |
| Linus | 弃权 | 弃权 | `[2]` | `[1,2]` | `[1,2]` |

## 补充规则

### López 必召开触发词

议题含 `研究方法论 / 实验设计 / benchmark / eval / A-B test / 因果声明 / causal claim / data leakage / selection bias / backtest 审视 / 因子诚信 / 过拟合诊断 / trial 披露 / CV 方法 / Sharpe deflation / factor zoo / specification / Sisyphus workflow` 任一关键词时，López 必召开，即使议题不是量化金融。

### Linus `stages=[1,2]`

- 阶段 1：工程视角评议题，关注 good taste、数据结构、anti-pattern，不评判当前 codebase 是否承载得住。
- 阶段 2：可行性 gate，吸收阶段 1 和其他席位结论，评估能否干净落地。

## 扩席位维护清单

1. 先新建共享 seat contract：`zhuzi/seats/<name>-reviewer.md`（或 `-engineer.md`），把职责、越权边界、输出契约和 seat-specific 字段要求放进去。
2. 再为需要支持的 runtime 新建薄 adapter：Claude shipped adapter 放 `runtimes/claude/agents/<name>-reviewer.md`（或 `-engineer.md`）；若 Codex roundtable 也要支持，同步补 `runtimes/codex/agents/<name>-reviewer.md`（或 `-engineer.md`）。
3. 更新本文件的当前席位表和默认 `stages` 规则。
4. 更新 `docs/INVENTORY.md` 与 `zhuzi/manifests/shipped-surface.json`。
5. 若新增 native verdict 或 route 语义，更新 `zhuzi/references/verdict-schema.md`。
