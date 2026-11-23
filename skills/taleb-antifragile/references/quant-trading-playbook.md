# Quant Trading Playbook · 量化交易应用推演

> **⚠️ 顶部诚实声明**（比 Munger playbook 的声明更严格）：
>
> 本文档是**基于 Taleb 公开原则（Incerto 五部曲 + 技术论文）对量化场景的推演**，**非 Taleb 原话**。
>
> Taleb 本人的核心 domain 是 tail hedge / long vol / dynamic hedging / option-based convexity——他（和 Universa 的 Spitznagel）**没有公开系统评论过 long-only 因子选股**（像 IndustroQuant 这种 A 股场景）。他公开批评过"主动基金经理"这一大类，公开称赞过的只有 convex payoff 结构、Kelly 保守化、tail 保护。
>
> 本文档的量化映射由 skill 作者根据 Taleb 的 10 个核心概念（Antifragility / Convexity / Barbell / Via Negativa / Fat Tails / Ergodicity / Skin in the Game / Lindy / IYI / Turkey + Ludic fallacy）推演到 **A 股 long-only 量化选股** 场景，读者使用时**必须警惕"推演"和"原话"的差别**——Taleb 可能反对其中某些具体 translation（例如他会质疑"long-only 本身能不能 antifragile"——答案可能是"最多 robust"）。
>
> **每章末尾有 "⚠️ Taleb 可能反驳" 警示**。读完本 playbook 的自检：**"Taleb 会在哪条建议上说'这是 Ludic fallacy'?"**

---

## 定位（适用对象）

下文以早期 IndustroQuant 工作流为示例。配置、时点和数值属于示例假设，现行项目以本身的验证与授权为准。

你是 A 股 long-only 量化选股策略的主理人（参考对象：**IndustroQuant**），已有成熟方法论栈：

- 因子诊断三件套（IC 时序 + 分位组回测 + 交互分析）
- Bootstrap 强制验证
- Paired replay production verdict
- Phase-Adaptive Scoring（按 regime 选因子/权重）
- 严格 baseline 完整性检查、版本命名绑定
- 反 look-ahead bias、反 overfitting 的三层守卫
- 秒级 replay 基础设施

这份 playbook **不是教你怎么做量化**——你已经懂。它是把 Taleb 的 10 个核心概念翻译成**对你已有方法论的补强点和盲点识别器**。

**核心结论**：A 股 long-only 选股**结构上是 fragile**——最多能做到 robust，很难真 antifragile（需要 option-like 结构）。承认这点比装成 antifragile 诚实。**IQ 的产品定位**：A 股 beta + alpha 产品，不适合 absolute return 定位。

---

## 一、Fat Tails → 回测诊断的三件套补强

### Taleb 原则

> "The Black Swan logic makes what you don't know far more relevant than what you do know." — *Black Swan* Prologue
> "The Sharpe ratio is meaningless under fat tails." — Real World Risk Institute 讲稿

核心：A 股日收益率**确定属于 Extremistan**——每 18-24 个月一次 fat tail 事件（2015 / 2016 / 2018 / 2020 / 2022 / 2024-10 / **2026-03-23**）。用正态假设（Sharpe、volatility、VaR）评估在 Extremistan 里是 **class error**（类别错误），不是"精确度不够"。

### 你的三件套的隐性正态假设

| 三件套组件 | 隐性假设 | Fat Tails 下的失效 |
|----------|---------|------------------|
| **IC 时序** | IC_mean + IC_IR (mean/std) | std 在厚尾下不是真实离散度；IC_IR 被少数 tail day dominated |
| **分位组回测** | 5 组等分、Q1-Q5 spread | 中间 3 组折叠可能掩盖极端分位的非线性 |
| **交互分析** | 双因子极端分位交叉收益 | 极端分位 n 本身小，tail event 下均值估计不稳定 |

### 对 IQ 的具体补强

**1. IC 时序 → 加偏度/峰度维度**

若 IC 时序报告目前只有 IC_mean / IC_std / IC_IR，可考虑增加：
- 加 **IC_skewness**（负偏警告——因子在尾部是损失放大器）
- 加 **IC_kurtosis**（>3 厚尾，>5 极厚尾）
- 加 **IC_CVaR_5%**（最差 5% 日的平均 IC）——严重负 = crisis 中反向

**2. 分位组 → 加极端分位层**

- 加 **Top 1% / Bottom 1%** 独立评估
- 对极端分位做 **bootstrap 区间**（点估计在 n<50 下无意义）
- 看"极端分位 payoff 是凸还是凹"——凸是反脆弱，凹是脆弱

**3. Paired replay → 加 tail event case study**

对已标注的 tail events（2015 / 2018 / 2020 / 2022 / 2024-10 / **2026-03-23**）做**逐事件 delta 比较**——不只看均值，看"2026-03-23 前后 5 日策略 A vs B 的 drawdown 差异"。

**4. Bootstrap 的继承偏差（最深盲点）**

即使按示例做 200 轮 bootstrap，仍有一个风险：历史样本 tail event 不足 → bootstrap 只是把"正态低估偏差"乘 200 遍。

**补救（synthetic tail injection）**：
- 在 bootstrap 基础上注入 **人为 ±5σ 事件**（按 Extremistan 规律，A 股每 5-7 年一次 -20% 单月）
- 看策略在合成尾部下的 drawdown——这是"stress test that actually stresses"

### 实操清单

- [ ] IC 时序扩展：加 skewness / kurtosis / CVaR_5%
- [ ] 分位组加 Top 1% / Bottom 1% 层，bootstrap CI
- [ ] Paired replay 附 "tail event delta table"
- [ ] Bootstrap 后加 **synthetic tail bootstrap**——注入 ±5σ 合成事件

### ⚠️ Taleb 可能反驳

"你们 long-only 选股本质上是在 Extremistan 里卖保险——任何基于 factor 的股票选择都有隐含的 short vol payoff。单靠补 skewness 指标救不了结构性问题"。**合理回应**：long-only 选股作为**总投资组合的一部分**（不是全部）是可以的；IQ 角色是 A 股 beta+alpha 产品而非 absolute return——诚实定位很重要。

---

## 二、Antifragility → 仓位注入凸性

### Taleb 原则

> "The Triad: Fragile / Robust / Antifragile. Volatility hurts the fragile, leaves the robust unchanged, benefits the antifragile." — *Antifragile* Book I

### A 股 long-only 在三档的位置

| 组件 | 默认状态 | 注入反脆弱的位置 |
|-----|---------|----------------|
| **选股层（factor scoring）** | 脆弱（多 beta，短 vol） | 难以直接改——factor 本身没有 gamma |
| **仓位层（position sizing）** | 可调——**主战场** | Drawdown-reactive 加仓（有硬 cap）、crisis 时反向加仓 |
| **组合层** | 可调 | Barbell：核心 + 卫星 |
| **对冲层** | A 股难做 | 期权（如能用）、股指期货动态对冲 |

### 对 IQ 的具体建议

**1. 仓位管理规则的反脆弱化**

| 市场状态 | 脆弱做法 | **反脆弱做法** |
|---------|---------|--------------|
| 回撤中 | 不敢加仓（散户心理）| 按 drawdown quantile **反向加仓**：-10% 加 10%，-20% 加 20%，有硬 cap |
| 波动率飙升 | 降仓 | **分两层**：realized σ 上升降仓（稳健）；implied σ overshoot 时加仓（反脆弱） |
| 恐慌日（如 2026-03-23）| 止损 | **crisis rebalancing rule**：跌幅超 X% 触发再平衡而非减仓 |

警示：反脆弱加仓必须有**硬约束**（绝对亏损上限、Kelly × 0.15 position cap）。Taleb 本人做的是 **"barbell: 90% 极度安全 + 10% 可以放大加仓的 convex 头寸"**——不是全仓反向加码。

**2. Gamma-positive 的量化等价物**

A 股 long-only 无真 gamma，但有 **convex-like 特征的因子**：
- **反转因子**（跌越多反弹越大）
- **波动率越高越有效的因子**
- **市场 beta 越低越有效的因子**（熊市后期反弹因子）

IQ 已经使用这些（`feedback_regime_conditional_coupling` 中 "H attribution 调出来吃熊市后期反弹"的权重）——**Taleb 视角下这已经是半个 barbell**。

### 实操清单

- [ ] Meta layer 加 **drawdown-reactive position sizing**（按预设表加仓，有硬 cap）
- [ ] Phase-Adaptive 权重表重构为 **barbell 形态**（"稳健 80% + 凸性 20%"显式标注）
- [ ] 写 **crisis playbook**：触发条件 + 具体动作（含"什么条件下加仓"）
- [ ] Gamma-like 因子**显式标记为"凸性仓位"**，与稳健因子分开管理

### ⚠️ Taleb 可能反驳

"Drawdown-reactive buying 是民科版 long vol——没有真正凸性，只是在卖保险被动挨打后 double down。真正反脆弱必须在收益函数本身有凸性（option-like）"。这个反驳严肃：**long-only 选股的天然 payoff 是凹的**，加仓规则只是让损失被时间平滑，不能改变结构。

---

## 三、Barbell Strategy → 因子组合设计

### Taleb 原则

> "Never put your money in 'medium risk' investments. Put 85-90% in extremely safe, 10-15% in extremely speculative."

核心：**不做 middle ground**。"中等风险"的尾部损失被 diversification 掩盖，tail event 时相关性到 1，你承担激进的损失但没有激进的上行 = **伪稳健**。

### A 股选股的 barbell 翻译

| 维度 | Middle Ground（错误） | **Barbell（正确）** |
|-----|-------------------|---------------|
| **因子类型** | 价值 + 动量混合"中性" | 大盘低波 80% + 小盘反转 20% |
| **持仓集中度** | 50-100 只"适度分散" | 极分散（300+）+ 极集中（3-5 只特博） |
| **持仓时间** | 中期（1-3 月）| 长期核心 + 超短期卫星 |
| **Phase 权重** | 全 phase 温和适配 | 两档明确，中间 phase 拆为 80/20 线性组合 |

### 对 IQ 的具体建议

**1. Phase-Adaptive Scoring 是不是 barbell？**

重读 `project_phase_adaptive_scoring`：**部分是 barbell**——熊市后期用 beta 反弹因子（激进）、平时稳健因子（保守）。但 AC/NEUTRAL 的"中间档"隐式编码 regime 假设，是 "pretending to be balanced"。

**修正方向**：
- **两档化 phase 权重**：只分 "safe phase" 和 "aggressive phase"，中间 phase 归入两端之一
- 如果中间档必须存在，**显式地**拆成 "80% safe + 20% aggressive" 线性组合
- 不让任何一档权重"对全 regime 温和适配"——那是 middle ground

**2. 因子组合的 barbell-ness 测试**

- 按"稳定性 / 凸性"给每个因子打分
- 检查总权重分布——中间（middle ground）还是两端（barbell）
- 权重集中在中间 50% 区间 → tail 表现差

**3. IQ-specific 实现**

- 对每个因子标注 **"stability score"**（IC_IR 标准差、regime-dependent 反转频率）和 **"convexity score"**（极端分位 payoff / 均值 payoff 比）
- Barbell constraint：60% 给 stability > 0.8，30% 给 convexity > 2.0，10% 缓冲

### 实操清单

- [ ] 对所有因子跑 **barbell scoring**（stability + convexity 双维度）
- [ ] 检查每个 phase 权重表是否存在 middle ground 嫌疑
- [ ] 中间 phase 显式拆为 barbell（80% 稳健 + 20% 凸性），不是隐式 regime 假设
- [ ] 新增 factor 时强制声明"稳健端还是凸性端"

### ⚠️ Taleb 可能反驳

"Barbell 本义是跨资产类（90% 国债 + 10% 期权）——资产层的极端对比。**因子层 barbell 是 stretched metaphor**，所有 equity factor 在 tail event 里一起挨打"。**合理回应**：承认因子内 barbell 是局部凸性注入，不是真跨类 barbell——但仍比 middle ground 好。

---

## 四、Via Negativa → 因子筛选方法

### Taleb 原则

> "Knowledge grows by subtraction much more than by addition... what we know to be wrong cannot turn out to be right." — *Antifragile* Prologue
> "Chess grandmasters usually win by not losing; people become rich by not going bust." — *Antifragile* Ch. 20

核心：**删除一个 bad thing >> 添加一个 good thing**。Asymmetry in tails——bad thing 的尾部损失往往 > good thing 的尾部收益。

### IQ 现状（via positiva 倾向）

看 `feedback_incremental_factor_experiment`（逐因子递增）+ `feedback_exhaustive_factor_sweep`（全因子穷举）——方法论偏"持续寻找可加的因子"。

**Taleb 视角批评**：只加不减。但：
- IC 衰减的因子不删 = 持续承担 tail 损失
- 曾经有效的因子（2020 前的 quality、2022 前的小盘反转）在 regime shift 后**不会自动失效**——会在 tail event 反向伤你
- 每季度清理 IC 衰减 > 50% 的因子 = via negativa

**IQ 已经做了一些 via negativa**：
- `feedback_no_lookahead_bias` 禁用某些行业信号
- v27 之前禁用 PE 行业信号
- `feedback_walpha_direct_diagnostic`（2026-04-19）砍 2 个 signal+ 因子（MB profit / WQ market_fit），+0.36pp 改善

**Taleb 视角**：**加大 via negativa 比例**，让"删除"成为**定期动作**而非"偶然发现"。

### 对 IQ 的具体建议

**1. 季度性 factor retirement review（via negativa schedule）**

当前 IQ 无**主动 retirement** 流程。建议：
- 每季度末做一次 factor retirement review
- 触发删除（命中任一）：
  - IC_IR 过去 12 月 < 0.1 且趋势下行
  - 过去 12 月有 ≥2 次 tail event 时该因子是损失放大器（CVaR_5% 严重负）
  - 该因子在 phase × regime 2D 分解 ≥50% 的格子无效或反向
- **纪律**，不是判断——到触发条件就删，不"再观察一个月"

**2. "删除优于添加"的优先级**

Research backlog 重排：
- **P0**：删除一个疑似已失效因子（verification cost 低，价值高）
- **P1**：修复已发现的 bug / data leakage
- **P2**：添加新的、有经济学解释的因子
- **P3**：添加新的、纯 data mining 的因子（通常应拒绝）

当前 IQ backlog 看起来偏 P2/P3。Taleb 视角建议**重心前移**。

**3. Baseline 清洗的 via negativa**

在识别基线数据缺口后，记录受影响切片和排除理由。分析中可排除不可验证样本，原始记录仍需保全。
- 行业历史数据明显缺失 → 删除而非插值
- Corporate action 数据不全 → 退出样本池，不"近似处理"

### 实操清单

- [ ] 建立 **quarterly factor retirement review**（固定日程）
- [ ] Research backlog 重排：P0 删除 > P1 修复 > P2 加经济学因子 > P3 拒绝 data mining
- [ ] 扫一遍当前 factor set，标注"哪些在 via negativa 触发条件边缘"
- [ ] 2026 Q2 末前做一次**激进删除轮次**：预期删 20-30% 现有因子

### ⚠️ Taleb 可能反驳

"Via negativa 是针对 lifestyle / 医疗 / 复杂系统（intervention 的 tail cost 大）。在量化这种可快速 A/B test 的领域，**添加和删除相对对称**——可以 rollback。"**合理回应**：不对称性存在但比 Taleb 原 domain 弱，季度审议是合理 overlay，不是教条。

---

## 五、Ergodicity → 仓位管理与破产风险

### Taleb 原则

> "If a single entity has a zero in its payoff... The path matters. The 'average' is not a useful summary for nonergodic systems." — Peters & Taleb 2019
> "Would you play Russian roulette for $10M? The expected value is positive. The path is not." — *Skin in the Game* Ch. 19

核心：
- **单人时间均值 ≠ 群体集合均值**
- 你只有一次 lifetime——不能用"平均 Sharpe"决策
- Kelly 最大化集合均值——对单人是**破产加速器**
- Taleb / Spitznagel 推荐 **Kelly × 0.1 到 0.25**（比 Munger × 0.25 更保守）

### 典型 ergodicity 错误（IQ 场景）

- "回测 20 年年化 20%" = **集合均值**（你运行这个策略无数次的平均）
- 你作为**单一交易员**，能否 20 年里**不爆仓**？= **时间均值**
- 两者在厚尾下差距巨大——集合均值 +20% 的策略可能 70% 个体路径最终破产

### 对 IQ 的具体建议

**1. 时间均值视角的回测报告**

当前 IQ 报告通常是集合均值。补强：
- 报告**单次完整回测路径** final NAV distribution（bootstrap 200 路径终点分布）
- 标注"最差 5% 路径终值"——如果 < 初始资金的 30%，破产信号
- 区分"回测 alpha 均值 +1.6%"（集合）vs "中位数路径 alpha"（时间）

**2. Kelly-based position cap**

- 计算策略的 **full Kelly fraction**（基于历史 walpha / volatility²）
- **实际仓位 ≤ full Kelly × 0.15**（比 Munger × 0.25 更激进）
- 单一策略上限 = 总资本 30%

**3. 破产概率的显式追踪**

回测报告加一栏：**"运行 10 年破产概率"**
- 定义破产：净值 < 初始资金 × 0.3
- 算法：200 个 bootstrap 路径运行 10 年，看多少命中破产线
- 这个数字远比 Sharpe 有信息量

**4. 话语规范**

团队报告里常说"年化 15%"——这是集合均值。Taleb 视角纠正：
- 说清"中位数路径年化 X%，最差 25% 路径年化 Y%"
- 决策基于 Y（或更保守的百分位），不是 X

### 实操清单

- [ ] Bootstrap 报告模板加 **final NAV distribution**
- [ ] 每策略上线前计算 **full Kelly**，实际 ≤ × 0.15
- [ ] 回测报告加 **10 年破产概率估计**
- [ ] 团队话语规范：主指标改为"中位数路径 alpha"而非"alpha 均值"

### ⚠️ Taleb 可能反驳

"Kelly × 0.15 仍然太激进——对无 tail hedge 的 long-only equity，应 × 0.1，且要有 circuit breaker（绝对 drawdown 到 X% 停止整策略）。"这个立场在实际基金管理中**过保守**（会 underperform benchmark）——需要在 "Taleb 保守"和"产品角色定位"之间权衡。

---

## 六、Turkey Problem → 回测样本选择

### Taleb 原则

> "Consider a turkey that is fed every day... On the afternoon of the Wednesday before Thanksgiving, something unexpected will happen." — *Black Swan* Ch. 4

### 典型 turkey 错误

- 回测只用 2014-2024（其中 2016-2019 相对平稳）
- 回测起点在熊市尾部或牛市起点（看起来干净）
- 回测结束在最近——可能处于相对平稳期

### A 股 mandatory tail event list

任何回测区间必须覆盖 ≥3 个（否则视为 "turkey window"，结论不可信）：

- 2007-2008 金融危机（如数据可溯）
- **2015 6-8 月股灾**（千股跌停 + 熔断导入）
- 2016 1 月熔断机制
- **2018 全年贸易战**（A 股 3500 → 2400）
- **2020 2-3 月 COVID 暴跌**
- **2022 俄乌 + 上海封控**
- **2024-10 以色列-伊朗升级**（区域 tail）
- **2026-03-23 A 股大跌**（见 `project_market_crash_20260323`）

### 对 IQ 的具体建议

**1. 回测起点纪律**

- 不从牛市起点（作弊）
- **从最近一次重大 tail event 的顶部开始**（如 2015-06-12 或 2021-02-10 抱团顶）
- 策略必须证明"能熬过至少一次周期"

**2. 每个 tail event 的强制包含**

`project_market_crash_20260323` 已要求"回测覆盖 2026-03-23 前后 15 个交易日"。扩展：
- 建立 **mandatory tail event list**
- 任何回测区间覆盖 ≥3 个 tail event
- 报告附 **tail event coverage table**

**3. 策略验收的 tail-specific 指标**

当前 IQ bootstrap 标准（胜率 > 70% 且 P5 > -0.5%）是全样本的。补强：
- 要求策略在**每个 tail event 独立窗口**不能 catastrophic
- "catastrophic" 定义：event 窗口 drawdown < -15% 或 alpha < -5%
- 哪怕全样本 bootstrap 过，任一 tail event catastrophic → 仓位层 / crisis playbook 加保护

**4. 回测不可终止在平稳期**

- 不要用"回测到今日"作为主版本
- 用"回测到最近一次 tail event 后 3 个月"作为验收窗口

### 实操清单

- [ ] 建立 **A 股 mandatory tail event list**
- [ ] 回测起点规则：**从最近一次 tail event 顶部**
- [ ] 验收增加 **"per-tail-event catastrophic check"**
- [ ] Release notes 包含 **tail coverage table**

### ⚠️ Taleb 可能反驳

"你们的 tail event list 都是**已知的、已观察的**——这仍然是 turkey's 1000th day 之前的 991 天。真正的 tail 是**未见过的那种**（A 股机制性改革、外资全面撤出、某大型央企违约）。list-based coverage 本身还是在 Ludic fallacy 陷阱里"。——**这个反驳正确**，见下章处理。

---

## 七、Ludic Fallacy → 模型 vs 真实世界

### Taleb 原则

> "Ludic fallacy: the misuse of games to model real-life situations." — *Black Swan* Ch. 9

核心：**用赌场规则（已知概率）处理真实世界（未知概率）**。量化最大风险：把历史分布当成未来分布的样本。

### IQ 场景中的 Ludic fallacy

- Bootstrap 假设历史样本可 resample——但只能 resample **已观察的分布**
- IC_IR / Sharpe / bootstrap CI 都建立在"分布已知且稳定"的前提
- 任何参数化风险模型（GARCH、copula、factor model）都在这个陷阱里
- 即使 `feedback_no_lookahead_bias` 做到完美，也只排除"未来信息泄露"，不排除"分布结构性变化"

**IQ 的部分防线**：
- `feedback_production_paired_replay` 的 "phase × regime 交互" 承认历史分布是 structured，不是 i.i.d. —— anti-Ludic
- `project_phase_adaptive_scoring` 接受"不同 phase 因子行为不同" —— anti-Ludic

**但仍不够**：未来可能有 IQ 从未见过的 phase（央行直接干预选股、A 股 MSCI 化、AI 主导的 HFT 挤压）。

### 对 IQ 的具体建议

**1. Synthetic tail injection（已在第一章提过的补救）**

深入展开：
- Bootstrap 外，再跑 **synthetic tail bootstrap**
- **人为注入 tail events**：按 Extremistan 规律，A 股每 5-7 年应有一次 -20% 月度
- 策略在 synthetic tail 下的 drawdown 评估
- Taleb 的 **"barbell stress test"**：不只用历史，加合成极端情景

**2. EVT 外推 vs Bootstrap resample**

Bootstrap 是 resample——只能取已见的。更激进（基于 EVT / Extreme Value Theory）：
- 用 EVT 拟合历史尾部（Generalized Pareto Distribution, GPD）
- **外推**到未见的更极端区域
- 用外推后的分布做 risk scenario
- 比 bootstrap 更接近 "acknowledge the unknown"

警示：EVT 也是模型，Taleb 承认 "no-good-choice-but-less-bad"——不是完美答案。

**3. "Two separate backtests"**

每次策略验收跑两次：
- **Actual**：历史真实路径（bootstrap 可 resample）
- **Counterfactual**：EVT 外推的合成路径（synthetic stress test）
- 两次都 pass 才发布
- Counterfactual 只 fail 时不一定否决，但**仓位层必须加保护**

**4. "Humility markers" in reporting**

每次策略报告明确标注：
- "这个 Sharpe 是 i.i.d. 假设下的"
- "这个 CI 来自过去 X 年样本，不代表未来"
- "已知 blind spots：[具体列出]"

### 实操清单

- [ ] Bootstrap 外加 **synthetic tail injection**
- [ ] 研究 EVT / GPD 拟合 A 股尾部，用于 counterfactual backtest
- [ ] 策略验收改为 **actual + counterfactual 双 pass**
- [ ] 报告模板加 **"humility markers"**——明确列建模假设和未知盲点

### ⚠️ Taleb 可能反驳

"EVT 的使用要谨慎——*Fat Tails* 批评过 EVT 在极厚尾分布下的不稳定性。真正推荐是 **'有凸性保护的 barbell'**——仓位层放 tail hedge（期权），不是模型层试图'更好地建模尾部'。"对 A 股 long-only 这是结构性困难，需要权衡。

---

## 八、Skin in the Game → 研究员职业激励

### Taleb 原则

> "Surgeons should not look like surgeons." — *Skin in the Game* Ch. 8
> "Never ask the barber if you need a haircut."

核心：**没有下行风险暴露的人，激励扭曲**。量化研究员典型激励：年度奖金挂钩（上行 bonus）但亏损不 claw back（下行 no downside）= asymmetric incentive。

### IQ 的激励结构问题

- 研究员开发策略、回测好看、上线 → 拿 bonus
- 策略上线 6 月后 tail event 扩大 drawdown → 研究员可能已离职
- **研究员自己的钱不在这个策略** → 无 skin
- 激励：让回测好看 ≠ 让实盘长期 robust

**IQ 部分自然保护**：
- 作为主理人自己的产品，skin in the game 相对高
- 未来团队化时，这个自然保护削弱

### 对 IQ 的具体建议

**1. 研究员 skin in the game 设计**（团队化情况）

- 研究员个人资金 ≥ 1% 投入自己开发的策略
- Bonus 递延 ≥ 2 年，视实盘表现调整
- Drawdown > X% 时 bonus clawback
- **最严格（Taleb 式）**：研究员**多数资金**必须在自己开发策略里

**2. Skin in the game 的自我检查**

每次策略发布前问：
- 如果我把**未来 3 年生活费**全放这策略，我会放吗？
- 如果回撤 30%，我**今年生活质量**下降多少？
- 如果**父母养老金**在这里，我会推荐吗？

这些不是情绪化，是把 abstract risk 翻译成 concrete path-dependent consequence（回到 ergodicity）。

**3. Team norms（团队化时）**

- 禁止"研究员提议，主理人买单"的 agency 结构
- 任何策略提议附 "researcher's own position"
- 研究员说"我不会把我的钱放进来" → 策略 default 不上线

**4. 公开透明的 track record**

- 每策略的研究员姓名、上线日、仓位、实际 PnL 公开
- 长期保留，防止"跳船逃责"

### 实操清单

- [ ] （主理人自检）我自己的钱在 IQ 策略的比例？低于 30% = skin 不够
- [ ] （未来团队化）建立 researcher-position attribution 制度
- [ ] Bonus 结构至少 2 年 deferred，drawdown > X% 触发 clawback
- [ ] 策略发布前强制"父母养老金 test"

### ⚠️ Taleb 可能反驳

"任何靠'他人资金'做 research 的量化都是 fragilista。" 这立场对 buy-side vs sell-side 差异不敏感，也不考虑资金池效应——实际需要在"强 skin in the game"和"规模化运营"之间权衡。

---

## 九、Lindy Effect → 因子筛选的存活时间启发

### Taleb 原则

> "If a book has been in print for fifty years, I can expect it to be in print another fifty." — *Antifragile* Ch. 20

核心：**存在时间越长 → 预期剩余寿命越长**。因子和学术理论是非易耗品，适用 Lindy。

### Lindy 因子分层

| 因子家族 | 学术首次发现 | Lindy 年龄 | 信心度 |
|---------|------------|-----------|--------|
| 价值（P/B, P/E）| 1934 Graham | 90+ 年 | ★★★★★ |
| 低波动率 | 1972 Haugen | 50+ 年 | ★★★★★ |
| 动量（12-month）| 1993 Jegadeesh-Titman | 30+ 年 | ★★★★☆ |
| 质量（ROE）| 1990s FF 扩展 | 30 年 | ★★★★☆ |
| 规模 | 1981 Banz | 40 年（recent decay 警告）| ★★★☆☆ |
| ML-derived 新因子 | 2020+ | < 5 年 | ★☆☆☆☆ |
| 另类数据因子 | 2015+ | < 10 年 | ★☆☆☆☆ |

### 对 IQ 的具体建议

**1. 因子 admission 的 Lindy 门槛**

| 因子年龄 | 阈值 | 要求 |
|---------|------|------|
| Lindy（> 30 年）| 最低 | IC + paired replay 验证即可 |
| 近期学术（10-30 年）| 中等 | + 经济学机制 + ≥2 regime 验证 |
| 新因子（< 10 年）| 最高 | + 经济学机制 + paired replay + ≥3 regime 验证 + **显式失效时间假设** + 监控机制 |
| Data-mined（纯 feature）| 拒绝 | 不入库 |

**2. Lindy-weighted 权重 cap**

- < 10 年因子总权重 ≤ 20%
- 单一 < 10 年因子 ≤ 5%
- 剩余 80% 给 Lindy 因子

**3. 学术阅读纪律**

- 优先 1970s-2000s 经典（Fama、French、Black-Scholes、Merton、Graham、Treynor、Jensen）
- 对 2020+ 新因子论文**保持警惕**——大多数 5 年内被证明"数据挖矿"
- 阅读顺序：Lindy 经典 → 最近 10 年高影响 → 近期新 paper（谨慎）

**4. 因子退役时的 Lindy 考量**

季度 factor retirement review：
- Lindy 因子（> 30 年）短期 IC 衰减 → **谨慎处理**（可能是 regime shift 暂时）
- 非 Lindy 因子（< 10 年）短期 IC 衰减 → **直接删**

### 实操清单

- [ ] 对所有因子标注 **"学术诞生年份"** 和 **Lindy age**
- [ ] 建立 factor admission tiered criteria（4 档）
- [ ] Non-Lindy 因子（< 10 年）总权重 ≤ 20%
- [ ] 阅读清单优先 1970s-2000s 经典

### ⚠️ Taleb 可能反驳

"学术 Lindy ≠ market Lindy——价值因子学术 90 年，但 A 股市场 Lindy 可能只有 20 年（A 股本身年轻）"。**合理回应**：对 A 股场景，Lindy 年龄按"A 股上市以来"打折扣，不是全球学术年限。

---

## 十、IYI → 量化研究的自我警惕

### Taleb 原则

> "The Intellectual Yet Idiot subscribes to theories, reads the New York Times, and wears a suit. The IYI is unable to spot nonsense." — *Skin in the Game* Ch. 9
> "Beware the person who gives advice, telling you that a certain action on your part is 'good for you' while it is also good for him."

核心：**IYI = 复杂理论 + 无 skin + 对真实世界无感**。量化研究员天然高风险——掌握复杂 ML 但不一定理解市场为什么给机会。

### 量化研究员的 IYI 症状

1. **技术复杂，理解简单**：会 XGBoost / neural net，讲不清"市场为什么给这个 alpha"
2. **不懂市场结构**：交易过但没在交易台坐过、不知 limit vs market 冲击差异、不知 short squeeze 时融券池发生什么
3. **用工具不懂假设**：用 Sharpe 不知 Gaussian 假设、用 VaR 不知厚尾失效、用 bootstrap 不知 i.i.d. 限制
4. **引权威但没读原文**：引 Fama-French 不知 1992 论文市场背景、引 Kelly 但没读 1956 原论文
5. **没 skin**：帮别人决定买不买，自己不会买同样
6. **教条不反思**：相信 EMH 或 ML alpha，tail event 之后没更新 prior

### IQ 研究员的季度自检清单

**A. Skin in the game 层**
- [ ] 我在 IQ 策略的自有资金 ≥ 年收入 10%？
- [ ] 策略亏 20% 时我会**失眠**吗（不是"难过"——是"晚上睡不着"）？
- [ ] 我给**父母**推荐过 IQ 策略吗？

**B. 市场理解层**
- [ ] 我能**不看指标 / 纯直觉**，判断当前市场状态（亢奋 / 恐慌 / 平静 / 转折）吗？
- [ ] 我理解 A 股的 T+1、涨跌停、融券池限制在危机中如何**反身自我强化**吗？
- [ ] 我知道 **2015 股灾具体机制**吗（不是"因为杠杆"——是"杠杆盘如何强平，强平如何触发更多强平"）？
- [ ] 我读过鲁兆、杨百万、游资大佬的访谈吗？

**C. 工具理解层**
- [ ] 我能解释 Sharpe 在什么假设下有意义、什么条件失效？
- [ ] 我知道 bootstrap 的 i.i.d. 假设在 regime-dependent 数据下的失效？
- [ ] 我知道 Kelly 对单人的破产风险（不只是"× 0.25 是标准"，而是**为什么**）？
- [ ] 我用的任何指标，我能一句话说清"它假设了什么、什么时候不适用"？

**D. 读过原文层**
- [ ] Fama-French (1992) 原论文读过？
- [ ] Grinold-Kahn *Active Portfolio Management* 核心章节读过？
- [ ] Taleb *Dynamic Hedging*（1997）翻过？这是他唯一 practical 量化书
- [ ] Spitznagel *Safe Haven*（2021）读过？long vol / tail hedge 的 practitioner 视角

**E. 反身更新层**
- [ ] **2026-03-23 tail event 之后**，我更新了哪些 prior？如果"一个都没更新" = IYI 标志
- [ ] 过去 12 月主动承认并改正的 IQ 方法论错误？
- [ ] 我有没有一个**曾经坚信、现在推翻**的量化观点？没有 = 12 月没成长 or confirmation bias

### 实操清单

- [ ] 每季度过一遍 A/B/C/D/E 自检，**记录红灯项**（≥3 红灯 = IYI 警告）
- [ ] 读过 Taleb *Dynamic Hedging* 核心章节（tail hedge, gamma 管理）
- [ ] 读过 Spitznagel *Safe Haven* 全书
- [ ] 读过中国市场 practitioner 访谈 ≥ 5 篇
- [ ] 每季度记录"这季度推翻的旧观点"——零条 = IYI 警告

### 招聘警示

招研究员时不只看 ML 技术水平，看**市场感 + skin 倾向**：
- 面试问"2015 年 6-8 月 A 股具体发生了什么"——不能答具体机制 = IYI 风险
- 问"你用 Sharpe 时的失效条件是什么"——不能答 = IYI 风险

### ⚠️ Taleb 可能反驳

"IYI 是 rhetorical device，不是 scientific category。"——承认。但作为自检工具，focus 在 **"学术训练 + 缺 skin + 不反思"** 的 conjunction（不是单独的学术训练）——上面清单已写清。

---

## 十一、额外专题

### 11.1 Convexity 思维替代预测思维

**Taleb 原则**：
> "Don't try to predict what will happen. Construct positions where, if good things happen, payoff is non-linear (convex). If bad things happen, losses are bounded." — *Antifragile* Ch. 12

**量化翻译**：
- 不要问"下次 tail event 什么时候来"——预测思维在 Extremistan 下失败
- 问"我的 payoff 结构是凸还是凹"——convexity 思维

**对 long-only 的限制**：
- Long-only equity payoff 天然凹（capped upside at ∞, bounded loss at -100%——但 path dependency 下 -100% = 破产，实际 loss 不 bounded）
- 真正 convex 需要期权（call long）或结构化头寸
- Long-only 框架内**局部 convex** 做法（见第二、三章）

**对 IQ 的启示**：研究 priority 排序时，"如何让 payoff 更凸" 排在"如何更准预测" 之前。

### 11.2 Naive 经验主义 vs 穷尽的反证

**Taleb 原则**：
> "Naive empiricism: just because something happened in the past does not mean it will in the future." — *Black Swan* Ch. 5

**量化翻译**：
- "过去 10 年 bootstrap 过了" ≠ "未来 10 年会过"
- 必须**主动构建**"能让策略破产的情景"——不是等它们来
- 比"发现新因子"重要 10 倍

**具体做法（red team exercise）**：
1. 每季度一次让一个不同角色扮演"想让这策略失效"的对手
2. 找 **5 个能让策略大幅回撤的场景**
3. 对每个场景检查现有机制（仓位、crisis playbook、risk budget）是否有防御
4. 缺防御 → 优先补上，不等发生

---

## 十二、读者最易误用的概念（警示清单）

**误用 1：把 Barbell 当"经典价值+动量组合"**

Barbell 关键是**极端 + 极端 + 拒绝中间**。"60% 价值 + 40% 动量" 不是 barbell——是 middle ground。真正 barbell 是 80% 国债 + 20% 深虚值 call，或因子层 80% 最稳健 + 20% 最凸性。若 barbell 仍在 middle ground = 没理解。

**误用 2：把 Antifragile 当"保守 + 加一点进攻"**

Antifragile 不是"攻守兼备"。是**特定设计让下行有限、上行凸性**。long-only 选股框架内很难真正实现——只能 robust。**不要把 robust 说成 antifragile**——术语滥用导致 overconfidence。

**误用 3：把 Via Negativa 当"懒得做新东西的借口"**

Via Negativa 要求**主动删除已失效的**，不是"不做新东西"。若团队借 "via negativa" 停止所有新因子研究 = 误用。正确：主动、规律、纪律性地删除过时的，同时继续做审慎的新因子研究（Lindy-biased admission criteria）。

---

## 十三、最后的诚实声明（再次强调）

**我（本 skill 作者）不是 Taleb。Taleb 也从未系统评论过 A 股 long-only 因子量化选股**。

本 playbook 基于 Taleb 公开原则（Incerto 五部曲 + 技术论文）的推演。**三个重要警告**：

1. **Taleb 的 domain 是 tail hedge / long vol**——他的 advice 最适合有能力做 convex payoff 的资金（Universa、tail hedge fund）。对 long-only equity，他的 advice 是 **"你们结构上就是 fragile，最多做到 robust"**——严肃对待。

2. **Taleb 可能认为 long-only factor investing 本质是 short vol**：卖保险式 payoff——大多数时候小赚，tail event 大亏。对 A 股选股策略定位（beta + alpha 产品 vs absolute return）有重大影响。**IQ 作为 A 股选股产品不适合 absolute return 定位**——明确作为"风险产品"更诚实。

3. **Taleb 对量化整体态度悲观**——他在 *Fooled by Randomness* Ch. 2 嘲讽过 "quant who doesn't know he's a turkey"。用他的视角审视量化时，**假设他会反对更多，而不是更少**——保持谦卑。

**最高 Taleb 纪律**：读完本 playbook，问自己——**"Taleb 会在哪条具体推演上说'这是 Ludic fallacy'?"**——然后认真回答。

---

## 十四、与 Munger Playbook 的关系

IQ 已经有 Munger 的 `quant-trading-playbook.md`。Taleb playbook 不是替代——是**补充视角**。两者分工：

| 维度 | **Munger** | **Taleb** |
|-----|--------|-------|
| **核心关注** | 避免愚蠢（认知偏误）| 避免破产（数学分布）|
| **工具倾向** | checklist 式筛查 | 凸性设计 / via negativa |
| **对 Sharpe 的态度** | "不只看 Sharpe，看分布" | "Sharpe 在厚尾下无意义" |
| **对回撤的态度** | "列 kill-path，设 exit rule" | "回撤是反脆弱机会（反向加仓有硬 cap）" |
| **对新因子的态度** | "能力圈之外扔 Too Hard 筐" | "Lindy 门槛 + 证据阈值" |
| **Kelly 建议** | × 0.25 | **× 0.15**（更激进保守）|
| **对"中等"态度** | 中等 = 稳健 | **中等 = 最脆弱**（barbell 拒绝中间）|

**结合使用**：

1. **研究期**：Munger checklist 审 idea（能力圈、激励、反方）
2. **建模期**：Munger anti-pattern 查漏 + IQ 三件套 + **Taleb 的厚尾检查**
3. **验证期**：Munger bootstrap 纪律 + **Taleb synthetic tail injection**
4. **上线期**：Munger Kelly × 0.25 + **Taleb Kelly × 0.15 硬帽**
5. **生产期**：Munger kill-path 监控 + **Taleb via negativa retirement**
6. **复盘期**：Munger "承认错误" + **Taleb IYI 自检**

Munger 给结构化纪律，Taleb 给对尾部的敬畏。**两者缺一不可**。

---

> "Don't tell me what you think, tell me what you have in your portfolio."
> —— Nassim Taleb, *Skin in the Game*
>
> 读完这份 playbook 的下一步：看看你的实际组合，它真的 embody 了上面的原则吗？还是你只读了文字，没改动作？
