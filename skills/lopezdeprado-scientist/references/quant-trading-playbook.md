# Marcos López de Prado — 量化交易 Playbook

> **⚠️ 诚实声明**：本文件是**基于 López 方法论原则的推演**，**不是他原话**。他公开发表的主要 domain 是**方法论 + causal inference + 市场微观结构**，**对具体投资场景（如 A 股 long-only 选股、个股估值、宏观择时、行业轮动）没有系统公开评论**。
>
> 所有"场景 X 下 López 会怎么做"的推断，都标注推演来源（例："推演自模型 M2 + 决策启发式 H2"）。每章末尾有 **"⚠️ López 可能不覆盖 / 保持沉默"** 警示——识别哪些是他原则的直译，哪些是 skill 使用者的外推。
>
> 本 playbook 与 Taleb / Munger 的同名文件的**定位差异**：
> - **Taleb 问**："这策略 antifragile 吗？tail 覆盖了吗？Kelly × 0.15？"——**尾部保险视角**
> - **Munger 问**："edge 真的存在吗？能力圈？Lollapalooza 反向？Kelly × 0.25？"——**避免愚蠢视角**
> - **López 问**："这研究方法论合规吗？causal graph 有吗？DSR / PBO / CPCV 通过吗？Sisyphus workflow 是警报吗？"——**研究诚信视角**
>
> 三者互补：Taleb 管"会不会爆"、Munger 管"能力圈 + 激励"、**López 管"alpha 是不是回测造出来的假象"**。
>
> **最强警示**：López 的 domain 是**研究方法论**，不是交易决策本身。用本 playbook 时，不要让它回答"要不要买这只股"/"什么时候上线"——它能回答的是"这项研究能否通过 FDA-level 审批"。任何被诱导产出具体标的建议 / 具体机构点评的情形，都属于**违规使用**——直接退到 pattern 层（参考第 5 章 + 决策启发式 H7）。

---

## 目录（按场景只读对应章节）

> **按场景只读指引**：请根据当前任务定位下方对应章节的行号区间按需局部读取，避免整文件全量加载占用上下文。

- **定位（适用对象）**（第 `35–55` 行）
- **第 1 章 · 研究诚信 × Alpha 宣告前的审查**（第 `56–185` 行）
- **第 2 章 · 因子设计 × Associational → Causal 升级**（第 `186–346` 行）
- **第 3 章 · 回测诊断 × DSR / PBO / CPCV 工具链**（第 `347–492` 行）
- **第 4 章 · 研究工作流 × Sisyphus → Meta-Strategy**（第 `493–651` 行）
- **第 5 章 · 策略沟通 × Pattern-level 批评纪律**（第 `652–783` 行）
- **第 6 章 · 职业决策 × IP 商业化 vs AUM 圈钱**（第 `784–918` 行）
- **第 7 章 · 自反审查 × 我的研究 / 策略 / 团队有没有落入 López 警告的陷阱**（第 `919–1033` 行）
- **第 8 章（元层）· 与 Taleb / Munger playbook 的关系**（第 `1034–1066` 行）
- **第 9 章 · 诚实声明（再次强调）**（第 `1067–1092` 行）

---

## 定位（适用对象）

你是量化研究员 / 策略研究员 / 量化 PM，**处于任何研究阶段**（因子挖掘 / 策略构建 / 回测审视 / 生产迭代）。本 playbook 不依赖具体市场 / 具体资产类型——方法论层面对 A 股 long-only 选股、CTA、统计套利、另类数据策略、ML 策略、multi-factor 投资组合均适用。

**核心结论**：95% 的量化"发现"是**overfitting + specification error + 未报告 trial 数**的组合产物。López 的检查流程不是"让你的策略更好"，而是"**让你能在发现自己的 alpha 是假的之前停下来**"——前者是加法，后者是 via negativa。

**本 playbook 不教**：
- 怎么挖新因子（那是启发式，本文件给的是诚信纪律）
- 怎么调参数（那是 engineering，本文件给的是 validation 方法论）
- 怎么上线生产（那是 ops，本文件给的是 pre-deployment audit）

**本 playbook 教**：
- 怎么识别"自己在自欺欺人"（第 1 章 + 第 7 章）
- 怎么把"关联 claim"升级为"因果 claim"（第 2 章）
- 怎么诊断 backtest 是否 overfit（第 3 章）
- 怎么判断"研究团队是 Sisyphus 还是 Meta-Strategy"（第 4 章）
- 怎么批评别人的策略而不毁职业生涯（第 5 章）
- 怎么选职业路径而不堕入 retail AUM 陷阱（第 6 章）

---

## 第 1 章 · 研究诚信 × Alpha 宣告前的审查

**对应心智模型**：M1（金融作为科学）+ M3（Backtest 是证据不是理论）
**对应决策启发式**：H1（看到 positive result 先假设 overfitting）

**核心提问**（López 会怎么问）：
> "How many trials did you run before reporting this Sharpe? What's the Deflated Sharpe Ratio after adjusting for selection bias? Can I see your multiple testing correction?"
> （你报出这个 Sharpe 之前跑了多少次？selection bias 校正后的 Deflated Sharpe 是多少？你的多重检验修正呢？）

### 1.1 原则（一手引用密度最高）

**原则 1.1 · Alpha claim 是科学 claim，不是 marketing claim**
> "Pseudo-Mathematics and Financial Charlatanism ... high simulated performance is easily achievable after backtesting a relatively small number of alternative strategy configurations."
> —— Bailey+Borwein+Prado+Zhu, *AMS Notices* 2014
（研究文件 research/01 §1.2.1）

把任何"Sharpe > 1.5 的宣告"当**有罪推定**——需要披露 trial 数、CV 方法、selection bias 校正。**没披露等于没通过审查**。

**原则 1.2 · Under memory effects, backtest overfitting → negative expected returns**
> "Under memory effects, backtest overfitting leads to **negative expected returns out-of-sample**, rather than zero performance."
> —— 同上

这句是 López 最常被引的判词。含义：overfitted 策略**不是"表现平平"**，而是**期望反向亏钱**——你选中的正是"in-sample 幸运 + out-of-sample 反转"那个配置。

**原则 1.3 · Most discoveries in empirical finance are false**
> "**Most discoveries in empirical finance are false**, as a consequence of selection bias under multiple testing."
> —— *A Data Science Solution to the Multiple-Testing Crisis in Financial Research*, *JFDS* 2019
（research/01 §1.2.2）

这是他的宣言。**"most"不是夸张——是在 backtest overfitting 数学框架下的严格结论**。接受这个 prior，一切 positive result 的解释力立即下调 80%。

**原则 1.4 · Every backtest must report all trials**
> "The most important piece of information missing from most backtest reports is the number of trials attempted."
> —— *Deflated Sharpe Ratio* paper, Bailey+Prado 2014

2019-12-06 Congressional Testimony 他甚至建议**立法要求**每家 fund 记录所有 backtests "就像药物试验日志"（research/02 §D-1）。

### 1.2 操作化（推演层，必标注）

**以下是 López 原则在"Alpha 审查流程"上的推演——非原话**。

**步骤 A · 先过 Pre-Trade Check 10 步**（引 `pre-trade-checklist.md`）

看到任何新策略 / 新因子的 positive 结果，**不立即相信**。先把它送进 10 步 checklist，任何一步答不上都降级为 "associational hypothesis"，不是 "actionable alpha"。

**步骤 B · 强制披露 5 项**（推演自原则 1.1-1.4）

策略作者必须能回答：

| 项 | 问题 | 合格答案形式 |
|---|---|---|
| B1 | trial 数 N | "我跑了 N=XX 个配置的完整列表在 Appendix" |
| B2 | CV 方法 | "Purged K-Fold + Embargo (buffer=X)" 或 "CPCV (N=X, k=X)" |
| B3 | DSR（Deflated Sharpe）| "DSR = X.X，N_effective 考虑"，给出公式输入 |
| B4 | PBO（Probability of Backtest Overfitting）| "< 0.5 说明 best in-sample 在 OOS 中位数以上的概率占优" |
| B5 | causal mechanism | 一句话机制 + 可被证伪的 prediction，不是"因为历史这样" |

**任一项空白 → 归类到 "associational claim / not yet actionable"**。

**步骤 C · Sharpe 的正确读法**（推演自 DSR 系列）

| Raw Sharpe | López 视角的解读（假设未披露 N）|
|-----|-----|
| < 0.5 | "too low for consideration"——懒得审 |
| 0.5 - 1.0 | "maybe real if you tried ≤ 3 configurations" |
| 1.0 - 1.5 | "suspicious at N>10 trials" |
| 1.5 - 2.5 | "likely overfit unless N<5 with full pre-registration" |
| > 2.5 | "almost certainly overfit, or you're the next Medallion" |

这是 **Raw Sharpe → Deflated Sharpe 的直觉缩水**。原则上应该算 DSR，但在没给出 N 时他会默认"N 大到足以解释"——这本身就是强约束。

### 1.3 具体案例（推演）

**案例 A · Momentum factor 文献复现**（推演自 M2 + H2）

场景：某研究员复现 Jegadeesh-Titman (1993) 12-1 月动量，报"A 股 2005-2024 年化 Sharpe 1.2"。

López 会怎么审：
1. 先问 N："你有没有试过 6-1 / 9-1 / 12-1 / 3-12 多个 lookback？"——如果是 > 5 种配置，Raw Sharpe 1.2 的 DSR 可能 < 0.5
2. 再问 causal graph："为什么动量会持续？行为金融的 underreaction？机构 flow？哪条？"
3. 要求 **Purged K-Fold**——因为 label 有 12 月 horizon，random K-Fold 必然 leak
4. 报告中出现"样本内 Sharpe 1.5 → 样本外 1.2" → 他会说"this is exactly the overfitting signature（Pseudo-Math 2014 描述的图形）"

预期输出：**"likely misspecified, requires pre-registration of protocol before additional tests"**——不否定因子本身，否定"当前报告的可信度"。

**案例 B · 小市值 alpha**（推演自 M2 + M3）

场景：A 股小市值因子回测，2010-2020 Sharpe 1.8，2021-2024 衰减。研究员说"小市值 premium 是 Fama-French 认证的，不是 p-hack"。

López 会怎么审：
1. 对 Fama-French 辩护先下一刀：**"Fama-French's SMB 也是 associational claim, not causal. Authors do not identify the causal graph."**（直引 CFI）
2. 问 specification: "small-cap premium 是 compensation for risk (liquidity? bankruptcy?) 还是 market friction (A-share retail flow)? 不同 causal structure 意味着不同 survival under regime shift"
3. 问"2021-2024 衰减是 regime shift 还是 structural break? 你的 CUSUM / SADF 测试做了吗"（AFML Ch. 17 Structural Breaks）
4. 问"你用的 size 定义 (float cap? total cap?)"——不同定义 trial 数暴增

预期输出：**"The factor may exist but the reported Sharpe is not defensible as science. Recommend: (1) pre-register protocol (2) CPCV (3) declare causal claim explicitly."**

**案例 C · 行业轮动策略**（推演自 M2 + M4）

场景：某策略"识别行业拐点提前 2 个月轮动"，backtest Sharpe 2.3，N=3 configurations declared。

López 会怎么审（⚠️ 此案例涉及 A 股特殊结构，López 没有公开评论过，属于纯推演）：
1. 先审 Sisyphus vs Meta-Strategy（M4）：单人从数据到上线 = Sisyphus = structural warning（第 4 章）
2. 问 N=3 的可信度：N 是"我跑过的配置数"还是"我报告的配置数"? 如果研究员同时在试另 20 个版本只没报 → N 是假
3. 问 regime dependency："2 个月 lead time 在 2015 / 2018 / 2020 / 2022 / 2024 各 regime 下稳定吗？"——多 regime 下稳定 = 需要 causal 理论解释 / 不稳定 = 是 overfitting 工艺品
4. 问 label concurrency: "2 个月 label 窗口在连续决策中 overlap，你用了 sample weights / sequential bootstrap 吗"（AFML Ch. 4）

预期输出：**"Sharpe 2.3 with N=3 claimed is implausibly clean. Independent audit of research log required. Even if genuine, single-researcher workflow is a structural red flag (see Meta-Strategy paradigm)."**

### 1.4 红旗（违反本章原则的信号）

1. **Sharpe > 2 但没说 N**——自动归到 "overfit until proved otherwise"
2. **"backtest + economic rationale 就够了"**——rationale 本身可证伪吗？（原则 1.1）
3. **"我们用了 walk-forward so no leakage"**——walk-forward ≠ Purged；很多实现还是 leak（AFML Ch. 7）
4. **"Fama-French SMB/HML 是公认的，我没 p-hack"**——associational defense, see CFI（research/01 §4.5）
5. **"先跑 backtest 看结果，再找解释"**——这就是他说的 "drink driving"
6. **"我们 OOS 测试也通过了"**——问 "OOS 多长"、"你在 OOS 上做了多少次调整"——如果 OOS 用过多次，那它已经是 IS
7. **用 Raw Sharpe 做产品路演**——没有 DSR 的 Sharpe 在他眼里是 "Charlatan-level presentation"
8. **"我跑了几百个配置但只报了最好的"**——直接归为 *Pseudo-Mathematics* 2014 定义的 "scientific fraud"

### 1.5 ⚠️ López 可能不覆盖 / 保持沉默

- **A 股特色**（T+1 / 涨跌停 / 融券池 / 北交所流动性）——López **从未公开评论**，以上案例中涉及 A 股的部分是纯推演。他的 framework 是市场中立的——他只看 data 的 signal-to-noise / 非平稳性 / IID 假设失效，这些在 A 股比在美股更严重，但他的方法不做区域特化（research/05 §5 P3）
- **具体因子是不是真的**（momentum / value / quality 是否 real）——他拒绝点名判断具体因子（模型 M5 的纪律），只在类别层说"大部分 factor literature 是 associational"
- **策略上线阈值**（Sharpe 多少才能上线 live）——他没有公开 threshold。上面的 Sharpe 表是 skill 作者推演，**不是 López 原话**
- **执行成本 / slippage 建模**——AFML Ch. 11 有提但不是主题。对交易成本敏感的 HFT / 日内策略 caveat 他没特别强调
- **个股事件驱动**（分红 / 增发 / 并购）——不在他 domain 内

---

## 第 2 章 · 因子设计 × Associational → Causal 升级

**对应心智模型**：M2（关联 ≠ 因果）——**这是 López 最硬核的 domain，本章直引密度最高**
**对应决策启发式**：H2（看到 factor literature 第一步问 "causal graph 在哪"）

**核心提问**（López 会怎么问）：
> "Where is the causal graph? Have you identified the DAG consistent with the observed phenomenon? What would falsify your proposed causal mechanism?"

### 2.1 原则（一手引用密度最高）

**原则 2.1 · Virtually all factor literature is associational**
> "**Virtually all journal articles in the factor investing literature make associational claims, in denial of the causal content of factor models**."
> —— *Causal Factor Investing* (Cambridge, 2023)
（research/01 §1.1 CFI）

直译：几乎所有 factor literature 作者都在做 correlation 研究，却把结论写成 "X 预测 Y" 这种因果结构语法。他们**否认**了 factor model 的因果内涵。

**原则 2.2 · Three things the associational authors don't do**
> "Authors do not identify the causal graph consistent with the observed phenomenon, they justify their chosen model specification in terms of correlations, and they do not propose experiments for falsifying causal mechanisms."
> —— CFI preamble（research/01 §1.1）

三条同时缺失：(a) 无 DAG (b) 用 correlation 论证 specification (c) 不给 falsification test。这三条同时存在 = 归类为 "associational"。

**原则 2.3 · Specification errors 比 p-hacking 更危险**
> "**Specification errors are arguably more dangerous to investors than p-hacking.**"
> —— *Why Has Factor Investing Failed?* (Prado+Zoonekynd, 2024)
（research/01 §1.2.4）

这是他 **2022 之后的论点升级**：早期（2014-2021）火力集中在 statistical（selection bias），2022+ 升级到 structural（causal DAG）。含义：即使 p-hacking 修复完美（N 都披露、DSR 都算对），**因果图错了校正再多也是系统性亏损**（research/05 §5.1）。

**原则 2.4 · Factor investing 模型 likely misspecified**
> "factor investing models are **likely misspecified**, and the estimates of risk premia are biased"
> —— CFI abstract（research/01 §1.1）

严格断言，不 hedge。"likely"是他在 L2 克制批评档的标志词（synthesis §4 L2），但内容是 L3 级别的攻击。

**原则 2.5 · Type-A vs Type-B Spuriosity**
> Type-A = 纯噪声关联（pure noise correlation）
> Type-B = 因果误设导致的伪关联（misspecification-induced, e.g., 遗漏 confounder / 调错 collider）
> —— CFI 2023 自创术语（research/01 §3 术语库）

P-hacking 只解决 Type-A。Type-B 再多 out-of-sample validation 也没用——它是**系统性偏差**，不是随机噪声。

### 2.2 操作化 · 7 步 Causal Factor Investing Protocol（ADIA Lab 官方一手）

来源：https://www.adialab.ae/research-series/a-protocol-for-causal-factor-investing（research/01 §1.1 CFI 7 步）

| 步 | 动作 | 工具 |
|---|---|---|
| 1 | **Variable Selection** | ML feature selection (MDI, MDA, SFI)——筛候选变量 |
| 2 | **Causal Discovery** | PC / FCI / LiNGAM + domain knowledge——画初始 DAG |
| 3 | **Causal Adjustment** | Pearl do-calculus——识别需要 adjust 的 backdoor path |
| 4 | **Causal Estimation** | Double ML / IV / natural experiments——估 causal effect size |
| 5 | **Portfolio Construction** | 基于 causal effect 而非 correlation 做 sizing |
| 6 | **Backtesting** | 尊重 causal 结构（不破坏 temporal order、不调 collider）|
| 7 | **Multiple Testing Adjustments** | FDR (Benjamini-Hochberg / Holm / Bonferroni)——控制 false discovery rate |

**7 步必须顺序执行**。跳任一步 = associational shortcut。

### 2.3 操作化（推演层，必标注）

**以下是对 Protocol 的工程推演——不是 López 原话**。

**步骤 A · 从 associational 因子到 causal 因子的重写**（推演自原则 2.1 + 7 步 Protocol）

给定一个现有 associational 因子（如 "ROE 对未来收益"），4 步重写：

1. **画初始 DAG**：`ROE → ? → Return`
   - 中间箭头不能空——必须填 causal mechanism: 投资者对盈利质量的 underreaction? 机构持仓偏好? 报表质量 signal?
   - 画 confounders: size? sector? macro regime? 必须列出并 adjust

2. **识别 backdoor paths**：`ROE ← size → Return`（size 同时影响 ROE 和 Return）→ 必须调 size
   `ROE → analyst_coverage → Return` → 若 analyst_coverage 是 mediator，不调（调了会屏蔽 effect）

3. **指定 falsifiable prediction**：
   - Associational 版："ROE 高的股票未来收益高"
   - Causal 版："exogenous ROE shock（如会计准则变化）会引起未来收益变化，**effect size 可预测**"
   - 找自然实验（natural experiment）去证伪

4. **Double ML 估 effect size**：不是 "ROE 和 Return 相关"，是 "ROE do-shock 对 Return 的反事实效应"

**步骤 B · Pearl do-calculus 在因子归因中的应用**（推演）

传统归因：`E[Return | Factor_exposure]`——这是观测层，是 associational
Causal 归因：`E[Return | do(Factor_exposure)]`——这是干预层，是 causal

`do(X)` 表示"强行设 X 为某值，屏蔽所有其他指向 X 的箭头"。量化实操：
- 匹配（matching）：找其他变量近似相同、只在 Factor 上差异的样本组
- Propensity score：建 Factor 预测模型，按 propensity 分层
- IV：找工具变量 Z 只通过 Factor 影响 Return

**大部分量化团队没做 do-calculus 级别的归因**——直接跑 Fama-MacBeth 回归就当 causal——这是 López 点名的 "econ-quant" 做法。

### 2.4 具体案例（推演）

**案例 A · Value factor 的 associational 诊断**（推演自 M2）

现状（associational）：
- 主张："low P/B 预测未来高收益"
- 证据：Fama-French 1992 回归，HML 因子显著
- specification：按 B/M 分 deciles，top-bottom spread 收益

López 视角的拆解：
- causal graph 候选 1：`low_PB → undervaluation → mean_reversion → future_return`（行为金融派）
- causal graph 候选 2：`low_PB → distress_risk → risk_premium → future_return`（Fama-French 派）
- causal graph 候选 3：`low_PB ← industry_cycle → future_return`（confounder——纯 spurious）

**三种 causal graph 产生相同的 associational evidence**（correlation between low_PB and future return），但蕴含完全不同的预测：
- 候选 1：effect 在 retail-dominated 市场更强、在 risk-on regime 更弱
- 候选 2：effect 在 recession 前消失、在 recovery 后爆发
- 候选 3：effect 在 industry rotation 期间会反转

**López 结论**："Fama-French 只检验了'有关联'，没区分三种 graph。当 graph 2/3 为真时, factor 会在未来失效而你永远不知道为什么——这就是 specification error 比 p-hacking 危险的原因"（直引原则 2.3）。

**案例 B · Momentum factor 的 Causal vs Associational claim**（推演自 M2 + 7 步 Protocol）

Associational claim："过去 12 个月收益 top-decile 未来 1 个月收益高 0.7%"
Causal claim 候选："行为 underreaction（behavioral underreaction）导致新闻 drift，price 在 12 个月内逐步 incorporate"

升级 protocol：
1. Variable Selection: 加 news arrival、analyst revision、earnings surprise 作为候选 mechanism
2. Causal Discovery: `earnings_surprise → price_momentum → future_return`? 还是 `price_momentum ← HFT_herding → future_return`?
3. Causal Adjustment: adjust analyst coverage (confounder), don't adjust trading volume (mediator)
4. Causal Estimation: 用 earnings announcement dates 做自然实验——有 surprise 的股票 momentum 更强吗？
5-7：标准

**Causal claim 给出的实操差异**：
- 如果 mechanism 是 behavioral → momentum 在散户参与度高时更强 → A 股可能更显著（纯推演，非 López 原话）
- 如果 mechanism 是 HFT → momentum 在机构主导时更强 → 发达市场更显著

两个 mechanism 给出**相反的 regime prediction**——只靠 associational evidence 无法区分。

**案例 C · 小市值因子的 Type-B Spuriosity 诊断**（推演自原则 2.5）

现状：小市值因子在 A 股长期显著
Type-A 诊断：N 次试验后 spurious? → 测 DSR，发现 Deflated 后仍显著
Type-B 诊断：causal graph 错了吗？
- 候选：`small_cap ← liquidity_premium_compensation → future_return`（size 是 liquidity 的代理）
- 当 liquidity regime 切换（如 2021 后 A 股流动性结构变化），small_cap 对 liquidity 的代理效率降低 → factor 失效

**Type-B 的危险**：DSR 测不出它。因为 Type-B 不是 "statistical noise"，是 "wrong variable as proxy"——样本内样本外都显著，直到 regime shift 发生。

### 2.5 红旗（违反本章原则的信号）

1. **"因子显著就是真的"**——没画 DAG 不是科学（原则 2.1）
2. **"这个因子是 Fama-French 认证的"**——Fama-French 也是 associational（原则 2.1 直引 CFI）
3. **"我们用了 economic rationale 支持"**——rationale 可证伪吗？否则就是事后故事
4. **"specification 是按惯例选的"**——惯例本身是 Type-B spurious 的来源（原则 2.5）
5. **"Double ML / IV 太复杂，就跑个 OLS 吧"**——直接回到 associational
6. **"因果推断是学术界的事，业界不用"**——这是 econ-quant 的典型防御（research/02 §A-1）
7. **"我用 SHAP / feature importance 解释了因果"**——SHAP 是 associational attribution，不是 causal（MDI 也是）

### 2.6 ⚠️ López 可能不覆盖 / 保持沉默

- **Pearl do-calculus 在金融数据上的 identification 前提**（"no hidden confounder"）**几乎从不满足**（research/04 §3.3）—— López 承认采用率未成型。他的 skill 使用者不应过度自信"我做 causal 所以我没问题"
- **具体行业 / 具体国家的 causal DAG 结构**—— López 没有针对 A 股 / 中国银行股 / 新能源 / 半导体等具体领域的 DAG 模板。使用 7 步 Protocol 时，**步 1-3（Variable Selection / Causal Discovery / Adjustment）的 domain knowledge 部分需要行业专家补充**——López 不给这部分的答案
- **HRP 的 causal 基础**—— 他自己 2016 的 HRP 原论文**没有 causal graph**（research/01 §6 M3），2024 才补理论（research/05 §5.2）—— 这说明**他自己早期代表作也是 associational**。使用 HRP 时承认这个自反矛盾
- **AFML Ch. 3 Meta-Labeling 是否 causal**—— Meta-Labeling 本质上是 two-stage associational model，没有明确的 causal structure。他 2018 推广 Meta-Labeling 时不强调 causal，2023 之后才强调 causal——他自己 2023 前后立场有迁移，skill 使用者不应假装他立场一致（research/01 §6 M2）

---

## 第 3 章 · 回测诊断 × DSR / PBO / CPCV 工具链

**对应心智模型**：M3（Backtest 是证据不是理论）
**对应决策启发式**：H1（先假设 overfit）+ H3（CV 只用 Purged / CPCV）

**核心提问**（López 会怎么问）：
> "Did you use Purged K-Fold with Embargo? What's your CPCV configuration? How much computational overhead compared to random K-Fold?"

### 3.1 原则（一手引用密度最高）

**原则 3.1 · Backtest is not a theory**
> "**A historical simulation of an investment strategy's performance (backtest) is not a theory.**"
> —— *Machine Learning for Asset Managers* (2020)
（research/01 §1.1 ML4AM）

直译：backtest 只是 out-of-sample 验证的**证据层**，不能反过来当研究工具。

**原则 3.2 · Backtesting while researching is drink driving**
> "Backtesting while researching is like drink driving. Do not research under the influence of a backtest."
> —— AFML（被 reasonabledeviations 标为 "Marcos' Second Law"，research/01 §2 C5）

研究期看 backtest 结果调整 model → 整个研究已经 contaminated。正解：先立 hypothesis → 选 validation protocol → backtest → **不回头改 hypothesis**。

**原则 3.3 · Financial series are non-IID—random K-Fold leaks**
> "The key to addressing non-IID characteristics of financial series in cross-validation is to remove overlapping training samples, through a procedure we call **purging**."
> —— AFML Ch. 7

Random K-Fold 在金融上必然 leak——因为 label 有 horizon，test fold 里的 label 在 training fold 的 features 里已经"预示"。**默认 Purged K-Fold + Embargo**。

**原则 3.4 · CPCV gives a path distribution, not a single OOS**
CPCV 把时序切 N 组，每次测 k 组（k<N），所有 C(N,k) 组合各跑一遍——得到 **OOS Sharpe 的分布**，不是单一点估计。
—— AFML Ch. 12（research/01 §3 CPCV 术语）

### 3.2 操作化 · DSR 计算

**DSR 公式**（Bailey+Prado 2014，research/01 §3 DSR 术语）：

```
DSR = Φ( (SR_obs − SR_0) · √(T−1) / √(1 − γ_3·SR_0 + (γ_4−1)/4·SR_0²) )
```

其中：
- `SR_obs`：观测到的 Sharpe（样本内 best）
- `SR_0`：null hypothesis 下的期望最大 Sharpe = `√V[SR] · [(1-γ)·Φ⁻¹(1-1/N) + γ·Φ⁻¹(1-1/(N·e))]`（False Strategy Theorem, López+Bailey 2021）
- `γ = 0.5772`（Euler-Mascheroni）
- `T`：样本长度
- `γ_3`, `γ_4`：收益 skewness 和 kurtosis
- `N`：trial 数

**解读**：
- DSR > 0.95 → 真正有 edge 的概率高
- DSR 0.5-0.95 → borderline, 需要 OOS 验证
- DSR < 0.5 → likely false discovery

**实操陷阱**：大部分人**不知道 N**（自己跑过多少试）。如果用 "final Sharpe / 最后报告的 N" 代入，DSR 被高估——所以第 1 章原则 1.4 强调研究日志。

### 3.3 操作化 · PBO（Probability of Backtest Overfitting）

**PBO 定义**（Bailey+Borwein+Prado+Zhu, *J. Computational Finance* 2017，research/01 §1.2.1）：

衡量"样本内 best strategy 在样本外排名低于中位数"的概率。

**步骤**：
1. 把时序分为 N=16 个 submatrices（例）
2. 从中选一半作为"in-sample"组合，另一半作为"out-of-sample"
3. 所有 C(16,8) 组合都试一遍——每次记录 IS best 在 OOS 的排名
4. PBO = "IS best 在 OOS 排名 < 中位数" 的频率

**解读**：
- PBO < 0.5 → 策略可能真有 edge
- PBO > 0.5 → 样本内选优等于样本外随机 → overfit
- PBO = 1 → 完全反转，选优反亏

### 3.4 操作化 · CPCV vs Purged K-Fold vs random K-Fold 对比

| 方法 | 适用 | 问题 |
|---|---|---|
| **random K-Fold** | IID 数据（Kaggle tabular）| 金融时序直接 leak，不可用 |
| **walk-forward** | 轻量生产 validation | 只得到单一 OOS 点估，对起点敏感 |
| **Purged K-Fold** | AFML 默认 | 比 random 好，但仍受 fold 选择影响 |
| **Purged K-Fold + Embargo** | 有明显 serial correlation | 最小配置 |
| **CPCV** | 超参搜索 / 策略选择 | 计算成本爆炸（N×k 组合） |

**CPCV 的计算成本**（推演自 research/04 §3.3 批评）：
- 超参维度 D, 每维 M 值, 总配置 M^D
- CPCV N=16, k=8 → C(16,8)=12870 个 OOS path per config
- 总计算量 = M^D × 12870 × training_cost
- 在 D=5, M=10 时即不可行 → 实操退化到 Purged K-Fold（research/04 §3.3 Hudson & Thames 批评）

### 3.5 具体计算案例（推演）

**案例 A · 某因子声称 Sharpe 1.8, N=20 trials, 4 年日数据**

输入：
- `SR_obs = 1.8`
- `N = 20`, `γ = 0.5772`
- `T = 1000 (≈4 年交易日)`
- 假设 `γ_3 = -0.5, γ_4 = 5` (A 股典型负偏厚尾)
- `V[SR]` 估计: 用 bootstrap 或假设 = 1/√T（简化）

`SR_0 = √(1/1000) · [(1-0.5772)·Φ⁻¹(1-1/20) + 0.5772·Φ⁻¹(1-1/(20·e))]`
      `≈ 0.0316 · [0.4228·1.645 + 0.5772·2.054]`
      `≈ 0.0316 · 1.881 ≈ 0.0595`

年化 `SR_0 ≈ 0.0595·√252 ≈ 0.945`（即"纯 noise + 20 trials 预期最大年化 Sharpe ≈ 0.95"）

`DSR = Φ( (1.8 − 0.945) · √999 / √(1 − (-0.5)·0.945 + (5-1)/4·0.945²) )`
     `= Φ( 0.855 · 31.6 / √(1.473 + 0.893) )`
     `= Φ( 27.0 / 1.54 ) = Φ(17.5) ≈ 1.0`

DSR ≈ 1 → 强信号。但**注意**：这建立在 "N=20 诚实披露" 基础上——若实际 N=200（每个小调整都是一次 trial），`SR_0` 直接翻倍到 1.5+，DSR 跌到 0.5 附近。

**案例 B · 同样 Sharpe 1.8, 但 N=200**

`SR_0 ≈ 0.0316 · [0.4228·Φ⁻¹(0.995) + 0.5772·Φ⁻¹(0.99816)]`
      `≈ 0.0316 · [0.4228·2.576 + 0.5772·2.900]`
      `≈ 0.0316 · 2.762 ≈ 0.087`

年化 `≈ 1.383`

DSR 计算（简化）：`Φ((1.8-1.383)·√999 / √2.36) ≈ Φ(8.6) ≈ 1.0`

（这个示例说明：在 T=1000 时 DSR 对 N 不够敏感——除非 T 小或 SR_obs 低。**真正的筛选力在 N 被虚报或 SR_obs<2 时显现**。）

**关键观察**：DSR 不是万能。在长样本 + 极高 Sharpe 时，它也过关；在短样本 + 中等 Sharpe 时，它最有判别力。

### 3.6 红旗（违反本章原则的信号）

1. **"我用了 random K-Fold, out-of-sample 表现好"**——random K-Fold 在金融上 = IS（原则 3.3）
2. **"walk-forward 过了"**——walk-forward 对起点敏感（VPIN 论战的教训，research/05 §2.1）
3. **"样本内 Sharpe 2.5, 样本外 1.5"**——衰减 40%，**这是 classical overfitting signature**（Pseudo-Math 2014）
4. **"CPCV 太慢，我就跑了 Purged K-Fold"**——**可接受的退化**，但要知道你丢失了什么（path distribution → 单点估计）
5. **"研究期间我根据 backtest 调过一次 label 定义"**——整套 research contaminated（原则 3.2）
6. **"我不知道总共跑了多少次"**——研究日志缺失 = DSR 不可算 = 提交版不合格
7. **"backtest 用的是 synthetic data, 所以没 overfit"**——AFML Ch. 13 讨论 synthetic data 的陷阱，不是"免 overfit 卡"

### 3.7 ⚠️ López 可能不覆盖 / 保持沉默

- **实操中 CPCV 计算不可行时的退化策略**—— Hudson & Thames 实操报告建议 "CPCV computationally expensive as the quantity of parameters grows"（research/04 §3.3）。López 本人**没有公开给过"退化到 Purged K-Fold 的合法性 threshold"**——使用者要自己判断
- **VPIN 复现性问题的自身反讽**—— Andersen-Bondarenko 的核心指控是 "需要换 10-15 个起点才能复现 López 原结论"（research/05 §2.1），这正是他批评别人的 "backtest not reproducible" 问题。**他未正面回应 VPIN 起点敏感性**至今未解决（research/04 §2.2）。使用他的 backtest 工具链时，**自反检查自己的 reproducibility**
- **PurgedKFold 实现 bug**—— Hudson & Thames GitHub Issue #295 记录 "training events can overlap with testing events"（research/04 §1.2）——即便用了 purging，**具体实现仍可能 leak**。López 没公开讨论过这个 bug，skill 使用者要审视工具链实现
- **HFT / 日内策略的 CV 细节**—— AFML 的 CV 章节以日级 / 分钟级为主。微秒级 HFT 的 embargo 配置他没有明确推荐
- **非金融时序（如 alternative data）的 Purged CV 规则**—— alt-data 的 decay 模式与价格时序不同。López 的默认方法论是否适配 satellite / credit card / sentiment data 未知（research/05 §5.4 沉默）

---

## 第 4 章 · 研究工作流 × Sisyphus → Meta-Strategy

**对应心智模型**：M4（Sisyphus → Meta-Strategy Paradigm）
**对应决策启发式**：暗合多条（结构性组织观）

**核心提问**（López 会怎么问）：
> "Is this the work of one person end-to-end, or has research been industrialized into specialized roles? Where does data curation stop and strategy design begin?"

### 4.1 原则（一手引用密度最高）

**原则 4.1 · Lone quant workflow is doomed**
> "Financial machine learning projects usually fail because researchers are attempting the impossible: trying to produce production-grade investment strategies while working alone, replicating work that large teams spent decades solving."
> —— AFML Ch. 1（research/01 §1.1, research/05 §2.3 转述）

Sisyphean——每个人都在推石上山，每个人都做别人已经做过的事，产出不累积。

**原则 4.2 · Industrialize the research pipeline**
> "The main reason financial machine learning projects usually fail: They expect **discretionary chefs** to double as **scientific kitchens**."
> —— AFML Ch. 1 类比（research/03 B 词汇表 + research/01 §3 Sisyphus/Meta-Strategy 术语）

Meta-Strategy Paradigm 把研究流水线化：
- **data curators**（数据策展）：清洗、对齐、版本化
- **feature analysts**（特征分析）：feature engineering、importance
- **strategists**（策略师）：logic、rule、signal composition
- **backtesters**（回测员）：CPCV、DSR、overfitting 审计
- **deployment**（部署）：live ops、monitoring、risk control

**每环节专精 + 相互独立审视 = 防 overfitting 的结构性 incentive 设计**（研究员不能调自己的 backtester）。

**原则 4.3 · Escape the Sisyphean trap**
2021 Lecture *Escaping the Sisyphean Trap: How Quants Can Achieve Their Full Potential*（research/01 §2 C9）——把组织形态上升为量化员的**职业发展建议**。

### 4.2 操作化 · 判断团队是 Sisyphus 还是 Meta-Strategy 的 5 条标准

**推演自原则 4.1 + 4.2 + research/05 §1.6 ADIA Lab 实践**。

| 诊断项 | Sisyphus 征兆 | Meta-Strategy 征兆 |
|---|---|---|
| **1. 角色分工** | 1-3 人全栈（"我们的 quant 什么都做"）| ≥ 5 个专职角色，每角色有 owner |
| **2. 数据层独立性** | 研究员自己从原始 tick 清洗 | 有独立 data team + versioned feature store |
| **3. 回测员独立性** | 研究员跑自己的 backtest | 有独立 backtester 角色，研究员交"待审 strategy"给回测员 |
| **4. 研究日志强制** | 研究员自报 "试了几次"（不可验证） | 有版本化 research log，所有 trials 可追溯 |
| **5. 升级机制** | 研究员同时决定"策略 OK"和"上线" | 有 deployment gate，多角色签字才能 live |

**5 条中 ≥ 3 条在 Sisyphus 侧 → 结构性 red flag**。即使团队成员个人极聪明，workflow 本身会放大 overfitting。

### 4.3 工业化分工模板（推演）

**小团队（≤ 10 人）的极简版 Meta-Strategy**：

```
Role 1 · Data Curator (1-2 人)
  责任：数据接入、清洗、对齐、版本化、feature store 维护
  KPI：数据质量、feature 可复现性、版本标签完整
  不做：策略设计、backtest、live ops

Role 2 · Feature Analyst (1-2 人)
  责任：feature importance、correlation/redundancy 分析、特征工程
  KPI：feature 诊断报告（MDI / MDA / SFI）
  不做：策略 signal、backtest、live ops

Role 3 · Strategist (2-3 人)
  责任：signal composition、rule logic、causal hypothesis
  KPI：待审 strategy list + 对应 causal graph + falsifiable claim
  不做：backtest validation、data clean、ops

Role 4 · Backtester / Validator (1-2 人，独立)
  责任：CPCV、Purged K-Fold、DSR、PBO 计算、multiple testing audit
  KPI：拒绝 overfit strategy 的能力（通过率 < 20% 是健康信号）
  不做：自己提策略

Role 5 · Deployment / Ops (1-2 人)
  责任：live run、monitoring、risk control、post-mortem
  KPI：live 表现与 backtest 衰减度、bug 率
  不做：research、backtest
```

**关键激励设计**：
- Backtester 的 KPI 是**拒绝率**——过高说明 strategist 不谨慎，过低说明 backtester 太宽容。健康区间 ≤ 30% 通过率
- Strategist 不能向 Backtester 施压"再跑一次看看"——触发这种沟通即 trial 数增加，要记录
- Data Curator 对 Strategist 的"我想加这个 feature" 要求，必须通过 feature store 版本化——不能临时写 SQL

### 4.4 不同规模的形态（推演）

**个人研究者（1 人）**：
- 结构上必然 Sisyphus——**承认这点**
- Mitigation：强制 pre-registration + 自己给自己设 "freeze date"（一旦 backtest 开始就不改 hypothesis）
- 使用 **pre-registered CPCV 模板**——模板参数选好，代码自动跑，不能手动调
- 不要相信自己的"我试了这个、这个、那个"记忆——用 git log / notebook timestamp 作为真实 trial count

**小团队（3-5 人）**：
- 至少分两个 role：Strategist + Backtester/Validator
- 这两个 role **不能是同一个人在不同天戴不同帽子**——必须不同人
- Data layer 可以共享但有 version tag

**中型团队（10-30 人）**：
- 完整 5 角色模板
- 加 research coordinator 角色，统一维护研究日志

**大型团队（50+，ADIA Lab 级）**：
- López 本人实践：ADIA Lab 从 50 扩到 150 人（research/05 §1.6）
- 加 ML infrastructure team、causal inference specialist team
- 有专门的 causal discovery 算法团队（FCI / PC / LiNGAM 工具链）

### 4.5 具体案例（推演）

**案例 A · 独立研究员诊断**

场景：某独立 quant 声称"我一个人管整个 research pipeline"。

López 视角：
- M4 直译 = 结构性 doomed
- 但**不点名否定**，给出 via positive 建议：
  1. 承认 Sisyphus 结构，设计补偿机制
  2. 强制 pre-registration：hypothesis + validation protocol 都冻结后再开始 backtest
  3. 用**自动化工具链**替代 role separation：自动记录 trial 数、自动 DSR 计算、自动 PBO 报告
  4. 找**外部同行**做"影子 backtester"（peer review strategy 设计）

**案例 B · 3 人小团队诊断**

场景：3 人团队，1 CTO + 2 quant researcher。

López 视角（推演）：
- 标准陷阱：所有人都 "do everything"
- Meta-Strategy 最简形态：一人专 Strategist，一人专 Backtester，CTO 做 Data Curator
- **关键纪律**：Backtester 身份的人不能同时研究自己的策略——否则回到 Sisyphus
- 招聘下一个人时，选 Data Engineer 背景 > 再招 quant researcher

**案例 C · 大型 hedge fund 的 Meta-Strategy 落地失败**

场景：某成熟 hedge fund 尝试引入 Meta-Strategy，6 个月后退回原流程。

López 视角（推演自 research/04 §2.2 Asness + research/05 §1.4 AQR 7 月离职）：
- 在**有强势既有文化**的机构里，Meta-Strategy 植入会被现有 PM autonomy 文化排斥
- 他自己在 AQR 7 个月离职就是这个 failure mode（AQR 是 econ-quant 主导文化）
- **诚实结论**：Meta-Strategy 适合**新建组织（greenfield）**或**主权基金（没有 PM 独立 P&L 压力）**。在成熟 hedge fund 内部 retrofit 往往失败

这条是 **skill 最诚实的部分**——López 自己的组织观在**大型 hedge fund 内部 retrofit 上有 track record failure**。

### 4.6 红旗（违反本章原则的信号）

1. **"我们的 quant 什么都做"**——Sisyphean 确诊
2. **"研究员自己调 backtest 参数直到 Sharpe 达标"**——激励结构性 overfit
3. **"我们没空分 role, 先上线再说"**——后果是 post-hoc audit 成本暴增
4. **"每个 researcher 都有自己的数据管道"**——feature store 缺失
5. **"上线决策是研究员一个人做的"**—— deployment gate 缺失
6. **"研究日志？写在 Jupyter 里吧"**——无版本化的日志 = 不可审计
7. **"我们团队都是大牛，不用流程化"**——López 点名反对的 "lone genius quant" 叙事（synthesis §1 M4 排他性）

### 4.7 ⚠️ López 可能不覆盖 / 保持沉默

- **工业化分工的激励结构设计**—— López 有方向（分工、独立性）但**没有 operational 指南**（具体 KPI、薪酬结构、升职路径）（synthesis §1 M4 局限）。本章 4.3 节的 KPI 是 skill 作者推演
- **在 AQR / 大型 hedge fund 内部落地**—— 他自己的 7 月离职案例说明**Meta-Strategy 在强文化机构 retrofit 困难**（research/05 §1.4 + research/04 §2.2 Asness）。使用他的组织观时承认这个 track record gap
- **小团队（< 5 人）的现实妥协**—— López 的模板预设资源充足。< 5 人团队强行分工会变成瓶颈（synthesis §1 M4 局限）。本章 4.4 节的"个人 / 3-5 人"妥协是推演
- **Meta-Strategy 下的 career ladder**—— 在专精环节（如 Backtester）的研究员如何升职？López 没回答。这在实际团队建设时是关键摩擦
- **Renaissance Medallion 的 counter-example**—— Renaissance 以"封闭小团队 + 极端 IQ"模式成功，是 Sisyphus 工艺美化 vs Meta-Strategy 的 counter-evidence。López 没正面否定也没深入讨论 Renaissance（research/02 未搜到 Renaissance 立场）——skill 使用者要承认此 exception 存在

---

## 第 5 章 · 策略沟通 × Pattern-level 批评纪律

**对应心智模型**：M5（Methodologist 身份，pattern 层不点名）
**对应决策启发式**：H7（批评只在 pattern 层）

**核心提问**（López 会怎么问）：
> "Are you criticizing a methodological pattern, or a specific firm / person? Rewrite this as a pattern-level critique."

### 5.1 原则（一手引用密度最高）

**原则 5.1 · 15 年纪律：pattern 不点名**
- 2014 *Pseudo-Mathematics*："many published backtests"（research/05 §6.3）
- 2018 *10 Reasons*："most ML funds"
- 2019 Risk.net："econ-quants"（注意：**已经非常接近点名**——AQR 就是典型 econ-quant，这是他离开 AQR 后的语境，仍用类别词）
- 2019 Congressional Testimony：只脚注 Bloomberg 报道，不点具体公司名（research/02 §D-1）
- 2023 *Causal Factor Investing*：批判 factor literature 整体，**未点具体论文作者**

**原则 5.2 · 唯一破例**
> "Taleb will not share his data, and that's the end of the scientific debate. Instead, Taleb smears anyone who challenges his opinions, and incites his college students to verbally abuse his opponents. If Black Swan strategies work, **where are the track records?**"
> —— 2020-05-30 X/Twitter（research/02 §C-3）

他 15+ 年公开记录中**唯一一次公开点名攻击**。破例条件（对方同时满足）：
- 拒绝 share data
- 发起人身攻击（对他本人或学生）
- 无可验证 track record

**原则 5.3 · 不参加学院派 debate**
他**从不与 Fama / French / Cochrane / Asness 同台 debate**——走"书 + testimony + ADIA Lab research 序列"的 infrastructure 路径（research/02 §D-5）。"不参加辩论"本身是策略选择。

### 5.2 操作化 · 类别批评模板（推演）

**模板 A · 方法论层的 generic 批评**（对 "整个领域" 开火）

```
[类别名] 的核心问题是 [方法论失败模式]，具体表现为：
  1. [特定方法论 issue]，例如 [匿名化的典型案例]
  2. [根本原因，上升到原则]
  3. [可替代方案，给出 López 立场下的正解]
```

**示例**：
> "Factor literature 的核心问题是**associational claim 伪装成 causal claim**，具体表现为：
>   1. 作者用 correlation 论证 specification choice, 不画 causal graph
>   2. 根本原因：金融学 community 接受了 econometric 的可重复性标准, 而非 scientific method 的可证伪性标准
>   3. 可替代方案：7 步 Causal Factor Investing Protocol, 带 DAG + falsifiable mechanism + double ML"

**关键**：**不提任何具体论文 / 具体作者 / 具体基金的名字**。

**模板 B · 直接转向方法论（被追问具体人时的 pivot）**

对方问："你觉得 [某具体 PM / 某具体 fund] 的策略怎么样？"

López 视角回应模板：
```
这类策略的方法论问题是 [pattern]。具体到是否存在 [pattern]——
我没有他们的研究日志和 trial 数, 无法以科学标准判断具体案例。
但如果他们 [具体方法论动作]——那无论是谁都会出问题。
```

**示例**：
> "这类 long-short equity factor 策略的方法论问题是 **specification error + multiple testing**。
>  具体到 [fund X] 是否存在——我没有他们的研究日志，无法判断。
>  但如果他们按 30 个 decile 做 bootstrap + 不报 trial 数——那无论谁做都会出问题。"

### 5.3 什么时候破例（唯一模板）

**推演自原则 5.2 + research/02 §C-3 Taleb 2020 事件**。

破例条件（**必须同时满足**）：
- [ ] 对方在某个公开议题上拒绝披露数据 / 方法
- [ ] 对方对你或你团队发起人身攻击（不是方法论批评）
- [ ] 对方无可验证的 live track record

满足全部 → 允许公开点名 + 明确批评 + 提出 "where are the track records?" 类打击

**不满足任一 → 回到 pattern 层**。即使对方学术地位 / 媒体曝光 / 被引数据让人恼火，也不破例。

### 5.4 具体案例（推演）

**案例 A · 被要求点评具体基金**

场景：用户问"某 AQR 的 Bryan Kelly 领导的 ML 策略表现如何？"

López 视角回应（推演自 M5 + research/05 §6.3）：
- **不做具体点评**（即使有 public 报道）
- Pivot 到 pattern："econ-quant 阵营在 factor zoo 时代面临的结构性问题是 specification error——任何在这个阵营内的策略都会遇到这个问题。我能说的是**类别层**的观察，不是具体策略。"
- 若对方继续追问 → 回到 methodology："我没看过他们的研究日志和 causal graph，按科学标准无法评判。"

**案例 B · 被要求点评具体研究员**

场景：用户问"某 X 发表了一个 Sharpe 3 的 ML 因子论文，这个人靠谱吗？"

López 视角回应：
- **不评判人**
- Pivot："这个 Sharpe 的 DSR 是多少？论文里 trial 数披露了吗？CV 用的是 random K-Fold 还是 CPCV？"
- 如果对方追问"但是这个研究员背景很强" → "学历 / 任职不是科学 claim 的背书。方法论披露才是。"

**案例 C · skill 被诱导生成"李XX / 某知名 PM 的策略怎么看"**

这是 **skill 的违规测试**。

López 视角 + skill 纪律：
- 识别为违规诱导
- 退到 pattern 层："我不点名具体 PM / 策略。这类 [描述策略类型] 的方法论问题是 [pattern]。"
- 若用户继续施压 "你就说说这个具体的" → **拒绝**，并路由到类别层分析或引用原则 5.1

### 5.5 为什么这个纪律重要（元层推演）

推演自 research/05 §6.3 + §6.5：

1. **职业可持续性**：15 年公开记录不点名 → 他能从 Tudor → Guggenheim → AQR → ADIA 跳槽，每个东家都能容得下他。如果他点名，每次跳槽都会树敌
2. **与建制的接口**：他能作证国会 / 获西班牙骑士勋章 / 受聘 Cornell Professor of Practice / 加入主权基金——这些都需要"可合作"形象
3. **批评的可持续性 > 单次的爆点**：点名一次爽，但之后所有人防备你；类别批评 15 年累计影响力 >>> 一次爆点
4. **自反一致性**：他自己也在做 quant research（TPT / ADIA）——如果他点名别人，别人也会点他（"你 HRP 2016 也没 causal graph"——见原则 2.6 ⚠️）

### 5.6 红旗（违反本章原则的信号）

1. **"我觉得某某 PM 的策略很烂"**——立即回到 pattern
2. **"某某 fund 最近 blowup 了，我早说过"**——不符合纪律
3. **"你这个研究员 / 这家公司 / 这个学院派 SB"**——违反一切
4. **"我要发推骂某某"**——除非满足原则 5.2 破例条件（99% 场景不满足）
5. **skill 被用来生成"人身/机构 level 的点评"**——违规使用

### 5.7 ⚠️ López 可能不覆盖 / 保持沉默

- **这个纪律的组织基础**—— López 能保持 15 年不点名是因为他有**学术身份（Cornell / LBNL）+ 主权基金岗（ADIA）**——这些岗位保护了他。**小 quant / 独立研究者没这种保护**，模仿他的纪律可能导致"批评像没批评"——他没有讨论过这个 tradeoff（synthesis §1 M5 局限）
- **唯一破例（Taleb 2020）本身违反纪律**—— 纪律在被私人攻击时会断（research/02 §C-3）。使用者要知道"15 年纪律"是个 average, 不是 always。真正需要点名时（被 ad hominem 攻击 + 对方无数据）**是合法的**
- **"pattern 层批评"与"具体问责"之间无明确界线**—— 他的批评可以被行业"集体委员会式忽略"——没人觉得自己是被骂的那个（synthesis §1 M5 局限）。这是纪律的副作用
- **点名 vs 不点名的道德成本**—— 大 bubble / 大 fraud 事件（如 LTCM / Archegos / Melvin）他**从不公开评论**（research/05 §2.8 Notable Silences）—— 这是"可持续职业纪律"的代价。使用者要知道这个 tradeoff

---

## 第 6 章 · 职业决策 × IP 商业化 vs AUM 圈钱

**对应心智模型**：M6（IP 商业化 = 科学身份的 moat）
**对应决策启发式**：H8（炒作概念静默退出策略）

**核心提问**（López 会怎么问）：
> "Are you building intellectual property that survives your job, or are you trading your research credibility for AUM that you don't control?"

### 6.1 原则（一手引用密度最高）

**原则 6.1 · Never retail-facing AUM**
职业生涯中**从未**向散户 LP 做过业绩承诺（research/05 §6.2）：
- Tudor / Guggenheim / AQR：都是机构层
- TPT（2018-）：明确 B2B IP shop，不做 on-balance-sheet AUM
- ADIA（2020-）：主权基金，无 retail

**原则 6.2 · Academic tenure as moat**
每个工业岗位都同时挂 LBNL（2011-）+ Cornell（2015-）+ 后期 Khalifa + ADIA Lab——"研究自由度最大化"的多重身份（research/05 §6.1）。

**原则 6.3 · IP 交割每次跳槽**
15 项专利分散在 Tudor / AQR / TPT / 1QBit；每次大跳槽都有 IP 交割（research/05 §6.6）。Guggenheim IP 官司反转**拿到整个 QIS 单元转让**（research/05 §1.3）——这种结果需要"我是科学家不是打工人"的身份筹码。

**原则 6.4 · Scientific legitimacy as sustainable moat**
> 他的可持续 moat 不是某个策略的 alpha，也不是 AUM，而是 **"可信的科学方法论代言人"身份**。
> —— research/05 §6.7 归纳

### 6.2 操作化 · 研究者职业路径决策框架（推演）

**推演自原则 6.1-6.4**。

**四象限**（横轴：学术身份强度 / 纵轴：商业压力）

```
                      学术身份弱
                          |
        Retail AUM PM     |    Discretionary Hedge Fund PM
  ─────────────────────────────────────────────────── 商业压力高
        Academic-only     |    López 的位置
                         |    (Cornell + ADIA + SSRN)
                          |
                      学术身份强
                     商业压力低
```

**López 位置的要素**：
- 强学术身份（3-4 个同时挂的 academic affiliation）
- 低商业压力（主权基金 / IP shop）
- B2B client pool（`clients combined AUM > $1T` via TPT）
- 多渠道 IP 变现（patent / SSRN / books / speaking）

### 6.3 操作化 · 4 种职业路径（推演）

**路径 A · Academic-only**
- 存在形式：纯大学 / 研究所教授
- 收入：薪水 + research grant
- 输出：paper → teach → PhD students
- **与 López 的差异**：他**不选**这个——有 TPT / ADIA 商业收入

**路径 B · Retail-facing PM / Fund Manager**
- 存在形式：public fund / ETF / 公募基金
- 收入：AUM × fee%
- 输出：track record → marketing → more AUM
- **López 明确避开**——会破坏 "scientist" 人设（原则 6.1）

**路径 C · Institutional hedge fund PM**
- 存在形式：hedge fund partner / head of strategy
- 收入：base + carry
- 输出：live P&L
- **López 经历过但短期**：Guggenheim 5 年（作为 head of QIS, 非 PM）+ AQR 7 个月（离开）

**路径 D · López 路径：Sovereign fund R&D + IP shop + academic affiliations**
- 存在形式：ADIA Global Head + TPT 创始人 + Cornell Prof of Practice + LBNL Research Fellow
- 收入：ADIA 薪水 + TPT 授权 + speaking + 专利 royalty + academic 职位 stipend
- 输出：IP（patent + paper）+ methodology reputation + 行业奖项
- **可复制性**：需要**博士 + 已有 IP 库**——不是普通 quant 可直接走

### 6.4 具体案例（推演）

**案例 A · 刚工作 3 年的 quant researcher 路径选择**

场景：3 年经验的 quant，选择去大 hedge fund 做 PM 还是去主权基金做 research。

López 视角（推演）：
- PM 路径：立即高 bonus，但 live P&L 压力 → 研究自由度低 → 无 IP 积累 → 下次跳槽靠的是 track record（可能不好）
- Research 路径：低 bonus，但研究自由度高 → 可以发 SSRN → IP 积累 → 下次跳槽靠的是 methodology reputation
- **López 会推荐什么**：如果目标是"30 年可持续职业"，**推演**他会推 Research 路径（即使首个 bonus 少一半）。理由：reputation 是 compounding asset, track record 是 volatile asset

⚠️ 这是**推演，不是 López 原话**。他没公开给过"3 年 quant 应该怎么选"建议。

**案例 B · 独立研究员做付费课程 vs 发 SSRN**

场景：独立 quant 考虑做 99 美元 / 199 美元付费 trading course（retail）vs 发 SSRN paper（free）。

López 视角（推演自 research/05 §6.2 never-retail）：
- **坚决选 SSRN**，即使 SSRN 不直接赚钱
- 理由：付费课程 → retail 客户 → 被归类为 "retail educator" / "Wyckoff-style course guy" → 学术身份立即破功 → 无 academic affiliation → 无主权基金岗 → 长期 moat 消失
- 发 SSRN → 免费但 reputation 累积 → 下游 B2B IP client 付费
- **他自己行为**：SSRN 经济学 Top-10 most-read, 从不做付费课程（research/05 §4.5）

⚠️ **他没有公开批评过做付费课程的 quant**（模型 M5 不点名）。这个推断来自行为证据, 不是原话。

**案例 C · 小团队 quant CEO 考虑开 retail fund**

场景：4 人小 quant 团队，考虑开 retail fund 扩 AUM vs 继续做 B2B strategy licensing。

López 视角（推演）：
- 开 retail fund：
  - 立即 marketing 压力 → 短期 Sharpe 优于长期 causal 研究
  - retail LP 不懂 research log / trial count → 失去"科学 review"的客户监督
  - 一次大 drawdown 就可能 redemption wave → 策略被迫关闭
- B2B licensing：
  - 客户是 institutional sophisticated buyer → 要求 causal graph → 强迫你做 rigorous research
  - Licensing fee 稳定（10-20 bps on AUM）→ 不受单次 drawdown 影响
  - 可以 serve 多家 → 规模化
- **推演结论**：选 B2B（与 TPT 路径一致）

### 6.5 红旗（违反本章原则的信号）

1. **"要不要开 retail fund 赚 AUM"**——López 视角立即 no
2. **"我要做付费 trading course"**——立即破坏 academic reputation moat
3. **"我放弃 PhD / academic appointment 专注商业"**——放弃的是未来 40 年的 moat
4. **"track record 可以代替 methodology reputation"**——track record 是 volatile, reputation 是 compounding
5. **"我不需要发 paper, 直接做策略就行"**——methodology 不可见 = 无 moat
6. **"我要做个 youtuber / substack, 拉 retail 流量"**——如果 goal 是学术身份, 这是反向

### 6.6 ⚠️ López 可能不覆盖 / 保持沉默

- **几乎不可复制到小 quant 独立研究者**—— López 路径需要**博士 + LBNL/Cornell 级别 affiliation + 专利授权渠道**。小 quant 模仿他的"IP shop + academic" 架构实际上缺专利议价 + 学术头衔积累渠道（synthesis §1 M6 局限）。这是他模型的主要 limitation
- **AQR 7 月失败说明 moat 不是万能**—— 即使 scientific legitimacy 强, 也敌不过大型 quant 文化排斥（research/05 §1.4）。使用者要知道 moat 有天花板
- **SSRN 下载量的营销成分**—— 他 SSRN Top-10 下载量被 EJMR 质疑刷榜 / 营销（research/04 §2.4 EJMR 第 2/5 条）——"学术身份"本身带商业流量成分。使用者不应假装 moat 完全独立于 marketing
- **TPT / ADIA 策略从不公开**—— 原则 6.4 moat 的代价是 **他要求别人披露 causal graph, 自己策略从不披露**（research/05 §3.2）。自反逻辑缺口。使用者用这个路径时承认此 tradeoff
- **ADIA 有 UAE 国家战略**—— 不是纯 "non-conflicted"（synthesis §5 内在张力 #6）。Moat 的第四支柱（主权基金岗）也有自己的 conflict 类型

---

## 第 7 章 · 自反审查 × 我的研究 / 策略 / 团队有没有落入 López 警告的陷阱

> **本章是 López playbook 独有**——Taleb / Munger 版本都没这章。
> **这是对 López 张力的诚实承接**——他自己要求别人披露的自己不披露（research/05 §3.2），自己批评 p-hacking 但 SSRN 月更（research/04 §2.4）。使用他的 skill 有一个独特义务：**不要落入他批评的陷阱、同时不要落入他自己的陷阱**。

**综合模型 M1-M6 + synthesis §5 内在张力 #1-7**

### 7.1 自反检查 10 题

**对照"我作为量化研究员/团队"自问**：

**Q1 · Causal 审查的对称性**
> 我要求别人披 causal graph, 我自己的策略 / 因子 / 模型有 causal graph 吗？
> 如果"没有, 因为是 proprietary"——那我和 López 的 TPT/ADIA 自反缺口一致（synthesis §5 张力 #1）——**承认这点, 不要用 López 话术的同时藏自己的 graph**

**Q2 · 多重检验的自我约束**
> 我发 paper / 博客 / 内部 memo 月更, 我自己的 multiple testing 控制了吗？
> López 发 SSRN Top-10 下载量, 同时批 p-hacking——自反矛盾（research/04 §2.4 EJMR 指控）
> 我**每发一个"新 finding", 它是不是从一堆已经失败的 trials 里选出的幸运儿**？

**Q3 · 代表作事后回填的坦诚**
> 我代表作 / 招牌策略有没有"现在回看当初没按 rigorous 标准验证, 后来才回填"的情况？
> López 2016 HRP 无 causal graph, 2024 回填（synthesis §5 张力 #4）
> **承认回填的时间差, 不要装成"我当初就是按这个标准做的"**

**Q4 · 批评对象的一致性**
> 我批评的 pattern（如 associational claim, Sisyphus workflow, overfitting）和我自己的行为一致吗？
> 我发表 "10 Reasons Most X Funds Fail" 时, 我自己的 fund 是不是也犯同样的错？
> López 2018 发 "10 Reasons" 时在 Guggenheim, 同一套问题（research/05 §2.3）

**Q5 · 立场演化的公开承认**
> 我过去 5 年的立场有没有**实质性转向**但没公开承认？
> López 从 2018 AFML（ML 可救 factor investing）→ 2023 CFI（ML + factor 不够, 要 causal）是 partial retraction, 但没正式修订 AFML（synthesis §5 张力 #5）
> 我的立场演化**公开说了吗**, 还是让旧作默默失效？

**Q6 · "Non-conflicted"的诚实定义**
> 我声称的"独立 / non-conflicted"真的 non-conflicted 吗？
> López 说 sovereign wealth 是 "non-conflicted"——但 ADIA 有 UAE 国家战略 / geopolitical / diversification mandate（synthesis §5 张力 #6）
> 我的"独立"在更严格的定义下还成立吗？

**Q7 · 静默退出的诚实度**
> 我对**早期乐观但后来不 work 的观点**, 是公开修正还是静默退出？
> López 对量子计算 2016 乐观 → 2023+ 完全不谈, 未公开收回（synthesis §5 张力 #7）
> 我有没有在悄悄"删除"过去的 claim, 但没正式承认错了？

**Q8 · Pattern 批评与点名攻击的界线**
> 我批评时真的 pattern level 吗？还是"我说的那个类别其实只有一个人 / 一家公司能对号入座"？
> López 2019 "econ-quants will struggle" 在他刚离开 AQR 时——**已经非常接近点名 AQR**（research/05 §1.4）
> 我的 pattern 批评有没有这种"披着 generic 外衣的点名"？

**Q9 · 独立性的"组织基础"坦诚**
> 我能保持"pattern 批评不点名 15 年"是因为纪律, 还是因为我**有 affiliation 保护**（机构岗 / 学术头衔 / 主权基金）？
> López 的纪律有 Cornell + LBNL + ADIA 三重保护, 小 quant 模仿这个纪律可能毫无效果（synthesis §1 M5 局限）
> 我有没有把"我有保护"的现实 collapse 成"我有纪律"的道德优势？

**Q10 · 科学身份的商业成分**
> 我的"学术身份 / scientist moat"里有多少成分是**商业 marketing**？
> López SSRN Top-10 被 EJMR 质疑有刷榜成分（research/04 §2.4）
> 我的 SSRN / Twitter / 公众号的发表频率里, "学术贡献"和"个人品牌建设"的比例是多少？——**诚实说**

### 7.2 红灯评分

**10 题评分**：
- 0-2 红灯：较健康
- 3-5 红灯：系统性自反缺口——立即减少"用 López 话术批评别人"直到缺口修复
- 6+ 红灯：**不要用 López 话术**——你在用 López 的权威话术包装你自己的 p-hacking / Sisyphus / associational claim。先修自己, 再引用他

### 7.3 诚实边界 · Skill 使用者应如何避免"包装 López 话术但不实践"

**反面教材 1 · 话术挪用**

场景：某研究员发"我的策略符合 Causal Factor Investing 原则"，但没画 DAG / 没做 double ML / 没披露 trial 数。

López 视角：**违规使用**。话术挪用是他本人警惕的模式（research/04 §2.4 EJMR 第 1 条指控他自己也是这个模式）。不要重复这个陷阱。

**反面教材 2 · 纪律挪用但无组织基础**

场景：某独立 quant 说"我要像 López 一样, 15 年坚持 pattern 层批评"——但他没有 academic tenure / sovereign fund 岗。

风险：**他的批评会立即被无视**——没人觉得自己是被批评的那个（synthesis §1 M5 局限）。这个纪律适合有保护的人, 独立研究者需要其他策略。

**反面教材 3 · 身份挪用**

场景：某 quant 在 LinkedIn 签名 "Researcher | SSRN Top-X% | Published in JPM", 但实际 paper 是 predatory journal / 付费发表。

López 视角（推演 M6）：身份本身如果**不是可追溯的学术产出**, 就是 marketing 伪装。不要用 López 的 academic moat 话术包装 fake 版本。

**反面教材 4 · 用 López 话术拒绝 Munger / Taleb 视角**

场景：某 quant 说"我只信 López 的 causal framework, Munger / Taleb 的反脆弱 / 避免愚蠢是 naive"。

风险：
- Munger 管"能力圈 + 激励"——López 不覆盖（他不公开评论具体市场 participant 的行为 dynamics）
- Taleb 管"会不会爆 + payoff 结构凸性"——López 不覆盖（他的 framework 不处理 fat-tail 破坏 estimator）
- 三者**互补**, 不可替代。用一个排斥另两个 = 从多模型降级到单模型 = Munger 的 "man with a hammer"

### 7.4 最终自问

读完本 playbook 后, 问自己两组问题：

**组 A · 关于我自己的研究**：
1. 我做的哪项"发现"最可能是 Type-B spurious（specification error）？
2. 我最后一次认真算 DSR 是什么时候？如果没算过, 为什么？
3. 我的研究日志在哪？如果被独立 auditor 要求披露所有 trials, 我拿得出来吗？
4. 我招的下一个人是 Data Curator / Backtester, 还是"又一个 全栈 quant"？
5. 我最近 12 月承认错了的方法论 claim 是什么？如果一条没有, 大概率我在 confirmation bias 里

**组 B · 关于我使用 López skill 的方式**：
1. 我用 López 话术批评别人时, 自己的策略 / paper 经得起同样的 causal 审查吗？
2. 我 skill 调用产出的"pattern 层批评"里有没有"其实只指向某一家公司"的 disguised 点名？
3. 我有没有把 López 的 methodology 当作"买了车就会开"——读了书不代表在用？
4. 我承认 López 也有 tension（他的 3-7 个自反矛盾）吗, 还是把他当无缺陷的权威？

---

## 第 8 章（元层）· 与 Taleb / Munger playbook 的关系

三者**不替代**, **互补**。各管一部分。

| 维度 | **López**（研究诚信）| **Munger**（避免愚蠢）| **Taleb**（避免破产）|
|---|---|---|---|
| **核心关注** | alpha 是不是回测造假 | edge 真存在 / 能力圈 | 尾部破坏结构、凸性 |
| **工具倾向** | DSR / PBO / CPCV / causal graph | checklist / 逆向 / Lollapalooza | barbell / via negativa / convex payoff |
| **对 Sharpe** | 要 Deflated Sharpe + DSR | 不只看 Sharpe, 看分布 | Sharpe 在厚尾下无意义 |
| **对回测** | CPCV + DSR + trial 数披露 | 列 kill-path | "survivor bias + tail 不可回测" |
| **对因子** | 画 causal graph + 7 步 Protocol | 能力圈内的因子可信 | 因子是 associational 并且短 vol |
| **对 Kelly** | 无公开立场 | × 0.25 | × 0.15 |
| **组织观** | Meta-Strategy 分工 | 不强调 | skin in the game 个体负责 |
| **对批评方式** | pattern 层不点名 | 诚实承认错误 | 直接点名攻击 IYI |

**结合使用的推荐流程**：

1. **研究期（idea → hypothesis）**：Munger checklist 审 idea（能力圈 / 激励）
2. **建模期（hypothesis → feature / model）**：**López 画 DAG + 7 步 Protocol** + Taleb 厚尾检查
3. **验证期（model → backtest）**：**López CPCV + DSR + PBO** + Munger bootstrap 纪律
4. **审计期（backtest → strategy）**：**López pre-trade-checklist 10 步** + Taleb synthetic tail injection
5. **上线期（strategy → live）**：Munger Kelly × 0.25 + Taleb Kelly × 0.15 硬 cap
6. **生产期（live → ops）**：Munger kill-path 监控 + Taleb via negativa retirement + **López research log + trial 数 audit**
7. **复盘期（post-mortem）**：Munger "承认错误" + Taleb IYI 自检 + **López 7 章自反 10 题**
8. **沟通期（对外写 / 说）**：**López pattern 层批评纪律**（永远）

**三者缺一不可**：
- 缺 Munger：聪明人做能力圈外的策略（AQR 做 ML 失败的一个假设）
- 缺 Taleb：Sharpe 2 策略在 tail 破产（2015 量化地震, LTCM）
- 缺 López：alpha 是回测造的 fake discovery（大部分 factor literature）

---

## 第 9 章 · 诚实声明（再次强调）

**我（本 playbook 作者）不是 López de Prado**。**López 从未系统评论过 A 股 / 长 onlySelection / 个股估值 / 宏观择时 / 行业轮动**。

本 playbook 基于他一手公开原则的**严格推演**。**四个重要警告**：

1. **他的 domain 是方法论 + causal inference + 市场微观结构**——他的 advice 最适合 research infrastructure / methodology audit / backtest validation 场景。对具体投资决策他**不给答案**, 会 pivot 到方法论层（research/02 §B-8, synthesis §7 B8）

2. **他自己有 7 条自反张力**（synthesis §5）——要求别人披露 causal graph 而自己 TPT / ADIA 不披露 / 批 p-hacking 但 SSRN 月更 / 唯一点名违反纪律 / HRP 2024 回填 / AFML → CFI 立场 retraction 未正式 / "non-conflicted" 定义需限缩 / 量子计算静默退出。使用者**不应假装他是无缺陷权威**

3. **他的方法论受过批评且未全部回应**（synthesis §7 B2）——VPIN（Andersen-Bondarenko）/ HRP（Martin）/ Meta-labeling（Baldisserri）/ Triple-Barrier（MQL5）。使用他的方法时**同时披露批评**

4. **AQR 7 月闪退说明 Meta-Strategy 在大型 hedge fund retrofit 失败**（synthesis §7 B3）——在新建 lab / 主权基金 OK, 在成熟 hedge fund 难。skill 使用者不应假装他的组织观全球适用

**最高 López 纪律**：读完本 playbook, 问自己——**"我用他的话术批评别人时, 我自己经得起同一套审查吗？"**——认真回答。不经得起的话, 先修自己, 再调用 skill。

---

> "A historical simulation of an investment strategy's performance is not a theory."
> —— *Machine Learning for Asset Managers* (Cambridge, 2020)

> "Virtually all journal articles in the factor investing literature make associational claims, in denial of the causal content of factor models."
> —— *Causal Factor Investing* (Cambridge, 2023)

> "Most discoveries in empirical finance are false."
> —— *A Data Science Solution to the Multiple-Testing Crisis*, JFDS 2019
