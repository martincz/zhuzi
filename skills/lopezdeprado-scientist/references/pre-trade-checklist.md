# Pre-Trade Research Integrity Check · 10 步研究诚信审查清单

> López de Prado 的 **Research Integrity Audit**——在一项策略 / 因子 / 论文 / 回测**被宣告为 alpha 之前**，先用 10 步检查它是否通过"科学化"门槛。不是 Taleb 的 fragility 审查（payoff 结构 / 厚尾 / 凸性），也不是 Munger 的 edge 审查（能力圈 / Lollapalooza / 护城河），而是 **方法论合规性（Methodological Compliance）**：
>
> - **Taleb 问**："这策略在厚尾下会不会爆？Sharpe 是否 meaningless？turkey 覆盖了吗？" → payoff 结构
> - **Munger 问**："edge 真的存在吗？能力圈外？Lollapalooza？激励合理吗？" → 认知与动机
> - **López 问**："这项研究是**科学**吗？可证伪吗？试了几次？causal graph 在哪？specification 对吗？backtest 是证据还是被当研究工具？" → 方法论合规
>
> 三者互补不重复——同一个策略在 Munger 某步答得上、在 Taleb 答不上（或在 López 答不上）都是信号。
>
> **本 10 步基于**：
> - CFI 7 步 Protocol for Causal Factor Investing（research/01 §1.1 CFI；ADIA Lab 官方）
> - AFML Ch. 3/5/7/12/14 的具体方法论规范
> - *Pseudo-Mathematics* (2014) + *Deflated Sharpe* (2014) + *10 Reasons ML Funds Fail* (2018) 的反模式诊断
> - 2019-12-06 Congressional Testimony 提出的"研究日志立法"要求（research/05 §2.5）
> - *Causal Factor Investing* (2023) 对 "associational vs causal" 的二分

---

## 使用方法

收到一份策略报告 / 因子论文 / 回测结果 / 研究 notebook 时，按 1 → 10 顺序走。每步答得出"这个研究通过了 X 检查因为 Y" → 继续下一步。答不上就停——这项研究还没达到"可以被称为 alpha"的科学门槛。

**前 3 步**（Claim Classification / Causal Graph / Variable Selection）审视研究的**科学性质**。
**中 4 步**（Confounder Audit / Data Structure / CV Protocol / Trial Count）审视**数据与建模规范**。
**后 3 步**（DSR & PBO / FDR / Sisyphus vs Meta-Strategy）审视**选择偏误校正与组织流程**。

**不能跳步**：Step 1 分类错了（associational claim 被当 causal），后 9 步都在**替错误答案打磨**。Step 5 数据结构错了（用 time bar 做 labeling），Step 6 Purged K-Fold 无济于事。López 在 *Pseudo-Mathematics* 2014 原话：整个研究流水线是**级联失效**——前段错，后段放大。

---

## Step 1: Claim Classification（声明分类：Associational 还是 Causal？）

**问题**：这项研究声称的是"X 与 Y 有关联"（associational）还是"X 导致 Y"（causal）？**作者自己分得清吗？**

**为什么这步**：
López 2023 *Causal Factor Investing* 整本书的起点就是这个二分——"virtually all journal articles in the factor investing literature make **associational claims**, in denial of the causal content of factor models"（research/01 §1.1 CFI）。Factor 模型在数学形式上是 causal claim（β 系数表示"因子暴露 → 收益"的因果），但作者在解释层只声明关联。这种 **claim type 与 model structure 不匹配** 是 Type-B Spuriosity 的源头（research/01 §3 Type-A/Type-B Spuriosity 术语）。LinkedIn 2023-01 首次公开 "associational quant" vs "causal quant" 二分（research/02 §C-1）——这是他为整个行业打的分类标签。

**诊断方法（具体可执行）**：
- 读论文 abstract + introduction，找三类表述：
  - **Associational**（可接受但需明示）："X is correlated with Y" / "X predicts Y in-sample" / "a significant relationship between X and Y"
  - **Causal**（需要 causal graph 支撑）："X causes Y" / "X drives Y's premium" / "investing in X because of Y mechanism"
  - **混淆**（红旗）：形式上 associational，但推出的投资结论依赖 causal reading —— 这是 factor literature 的标准病
- 看作者是否明确声明其 claim type—**未声明默认按 associational 对待**，所有 causal-sounding 结论打折扣
- Pass 门槛：作者明示 claim type，且 claim 与后续分析方法（纯统计 vs 因果推断）一致

**红旗（违反这步的信号）**：
- 论文通篇未区分 "correlation" 与 "causation"；结论句用 "explains"、"drives"、"due to" 等因果动词但证据层只有回归 t-stat
- 投资建议基于 "因子 X 有 premium" 但没有 X → Y 的因果机制假说
- 作者混用 "associational" 和 "causal" 的结论（如：摘要声称"我们发现 X 预测 Y"，建议栏写"投资 X 以获取 Y premium"——后者是 causal claim 套 associational 证据的外壳）

**救援（如果 fail 了怎么办）**：
- 强制作者重写结论层——把所有 causal 语言降级到 associational（"X is statistically associated with Y in our sample"）；或
- 要求作者补 causal graph 与 mechanism 假说（进入 Step 2）
- 推荐阅读 *Causal Factor Investing* Ch.1 + *Ranking Empirical Evidence in Finance* (2023, JPM 49(9))——López 明确的证据层级

**Skill 运行时的触发话术**（L2 克制批评档位）：
> "这篇论文的 claim type 不清——形式上是关联，结论层却是因果。在明示之前，按 associational 对待，投资结论打折扣。"

**对应反模式（来自 synthesis.md 反模式库 AP-2 "把关联当因果"）**：
AP-2

---

## Step 2: Causal Graph 可见性（DAG 与 Mechanism 披露）

**问题**：如果声明是 causal，**作者公开了 causal DAG 吗？mechanism 的可证伪形式是什么？**

**为什么这步**：
CFI (2023) 对 factor literature 的核心指控原文："**Authors do not identify the causal graph consistent with the observed phenomenon, they justify their chosen model specification in terms of correlations, and they do not propose experiments for falsifying causal mechanisms**"（research/01 §1.1 CFI）。没有 DAG 就没法讨论 confounder / collider / mediator——后续 Step 4 的 do-calculus 修正无从谈起。López 2022 ADIA Lab 推出 Causal Discovery Challenge + 10 万美元悬赏（research/01 §2 C3），就是把这个要求工程化——**causal discovery 必须作为独立研究阶段存在**，不能塞进 feature engineering 里含糊过去。

**诊断方法（具体可执行）**：
- 找论文里的 DAG 图或 causal structure 伪代码。**没有 = fail**
- 如果有 DAG，检查：
  - 节点是否包含已知的 confounder candidates（如 size factor 分析必须考虑 liquidity / beta / profitability）
  - 边的方向是否由**领域知识**（domain knowledge）确定，而非数据驱动——CFI 7 步 Protocol 的 Step 2 明说 Causal Discovery 需要 "algorithms + domain knowledge" 双轨（research/01 §1.1 CFI 7 步）
  - 是否有 "我们选择这个 DAG 而非其他候选 DAG" 的论证
- Pass 门槛：公开的 DAG + mechanism 描述 + 可证伪 predictions（Popper 式——这条路走得通应该看到 X，看不到 X 则 mechanism 伪）

**红旗（违反这步的信号）**：
- 论文用 "we control for A, B, C" 替代 DAG——这是 econometric 老做法，控制什么变量凭作者拍脑袋，不是 causal analysis
- DAG 存在但**未披露 mechanism**——图画了但不说"为什么这个因果方向是这个方向"
- Mechanism 是 post-hoc rationalization：先跑回归，再编故事解释为什么这么 work（2019 Risk.net 访谈 López 原话的 econ-quant 典型流程："They form a theory, they select the data that helps them prove that theory, they run some thousands of linear regressions, they report only the result with the lowest p-value"——research/02 §A-1）

**救援（如果 fail 了怎么办）**：
- 强制作者补 DAG——即便是手工画的简版。有 DAG 就能讨论 confounder，没有就没法审
- 应用 CFI 7 步 Protocol Step 2（Causal Discovery）：用 PC / FCI / NOTEARS 等 causal discovery 算法跑一遍数据，**再**与 domain knowledge 反复校准。算法输出 = starting point，不是 final answer
- 把 Step 2 未通过的研究归类到 "associational claim"（回 Step 1），不给 causal 认定

**Skill 运行时的触发话术**（L2 克制批评档位）：
> "Causal graph 未披露。投资结论依赖因果读解，但证据链在 associational 层停下。这篇论文的 claim 与 methodology 不匹配。"

**对应反模式**：
AP-2（把关联当因果）

---

## Step 3: Variable Selection Discipline（特征选择纪律：MDI/MDA 替代 p-value）

**问题**：特征是怎么选的？**用 p-value 筛？还是用 feature importance（MDI/MDA/SFI）？**

**为什么这步**：
AFML Ch. 8 专章 "Feature Importance" (research/01 §1.1 AFML)，以及 ML4AM Topic 5 "Feature importance replacing p-values"（research/01 §1.1 ML4AM 七大主题），确立了 López 对变量选择的立场——**p-value 是单次假设检验的产物，在多特征筛选场景下系统性偏高**。MDI (Mean Decrease Impurity) 基于树模型内部 impurity 下降，MDA (Mean Decrease Accuracy) 基于 OOS permutation，SFI (Single Feature Importance) 基于单因子独立检验。三者交叉才可信。他在 AFML Ch. 8 原话（转述）："**Backtesting is not a research tool. Feature importance is.**"（research/03 §A1 证据 1）——这是 López 最招牌的二段否肯。

**诊断方法（具体可执行）**：
- 看变量选择章节用的是什么：
  - **p-value / t-stat 门槛**（如 p < 0.05, t > 2.0）→ fail
  - **Harvey-Liu haircut**（t > 3.0 多重检验修正）→ partial pass，但 López 评价 "even Harvey's assumptions were generous"（research/04 §2.2 Harvey）——只做 statistical correction 不触碰 causal structure，仅算改进版 p-value
  - **MDI / MDA / SFI 任一个**→ 基础 pass
  - **MDI + MDA + SFI 三者交叉** → 最优 pass
- 检查是否做 **Orthogonalization**——相关特征互相吃掉 importance，要先做 PCA / Clustering 再算 importance（AFML Ch. 8 推荐 Clustered MDA）
- Pass 门槛：至少 MDA（OOS permutation-based），且在相关特征下用 Clustered 版本

**红旗（违反这步的信号）**：
- 纯 stepwise regression + p-value 筛变量——典型 econ-quant 做法，López 2019 Risk.net "run some thousands of linear regressions, report only the result with the lowest p-value" 直指此（research/02 §A-1）
- Feature importance 算了，但**只报 MDI**——MDI 对高基数特征有系统偏好（e.g., 连续变量 vs 离散变量），不做 MDA 交叉是跛脚
- 相关特征不做聚类直接排序——相关的 10 个特征瓜分 importance，每个都"不重要"的假象

**救援（如果 fail 了怎么办）**：
- 替换 p-value 门槛为 MDA（最关键的一个）
- 相关特征多时加 Clustered MDA（AFML Ch. 8）
- 看不懂 feature importance 排序 → 读 AFML Ch. 8 全章 + Hudson & Thames mlfinlab 的 `feature_importance` 模块实现

**Skill 运行时的触发话术**（L1 技术层）：
> "变量选择用 p-value 做门槛——这在多特征筛选下系统性偏高。替换为 MDA，相关特征用 Clustered 版本。"

**对应反模式（synthesis.md 反模式库 AP-7 "不报 trial 数的 Sharpe 宣告"的上游病）**：
AP-7（上游）

---

## Step 4: Confounder / Collider Audit（do-calculus 因果调整）

**问题**：DAG 里的 confounder 是否被 adjust？collider 是否**被避开**（不该 condition on）？

**为什么这步**：
这是 López **最硬核的技术贡献**之一——把 Pearl 的 do-calculus 系统化应用到金融因子分析（research/01 §4.2 Pearl）。CFI 7 步 Protocol 的 Step 3 "Causal Adjustment (do-calculus)" 和 Step 4 "Causal Estimation (double ML)"（research/01 §1.1 CFI）是 López 区别于 Harvey-Liu 的关键——后者只做 statistical correction，前者触碰 causal structure。核心区分：

- **Confounder**（Z → X, Z → Y）：必须 condition on，否则 X-Y 的关联被 Z 的共同影响污染。典型金融例：size 与 value 之间，profitability 是 confounder（盈利公司通常 smaller 市值 + higher book-to-market）——不控 profitability 就看不到真正的 size 与 value 的独立关系
- **Collider**（X → Z ← Y）：**禁止 condition on**，否则会在 X 和 Y 之间制造虚假关联（Berkson's paradox / selection bias）。典型金融例：同时控制"在样本中存活"和"某因子暴露"——生存本身是 collider，条件化就制造虚假因子效应

这是为什么 Step 2 的 DAG 不可替代——没有 DAG 你分不清 Z 是 confounder 还是 collider，"控制变量越多越好"的 econometric 直觉在 collider 上会反向伤害研究。López 在 *Why Has Factor Investing Failed?* (2024, Zoonekynd) 的核心论点升级："**specification errors arguably more dangerous to investors than p-hacking**"（research/01 §1.2.4 + §6 M2）——specification error 就是 DAG 画错导致的 confounder/collider 误处理，比单纯 p-hacking 深一层。

Double ML（Chernozhukov 2018）是 CFI 7 步的 Step 4 推荐工具——用 ML 估计 nuisance functions，然后再算 causal estimate，比纯线性回归 robust。

**诊断方法（具体可执行）**：
- 基于 Step 2 的 DAG，列出：
  - 所有**潜在 confounder**（Z 同时影响 X 和 Y）——被 adjust 了吗？
  - 所有**潜在 collider**（X 和 Y 的共同后代）——被**排除**出 adjustment set 了吗？
  - 所有**mediator**（X → M → Y 中的 M）——论文想估计 total effect 还是 direct effect？决定 M 该不该控制
- 看方法论：
  - 纯 OLS + "控制一堆变量" → 不分 confounder / collider，极高概率翻车（看似严格，其实 specification error）
  - Propensity Score Matching → 只 handle 观察到的 confounder
  - Instrumental Variables → 需要 valid instrument（金融里极少）
  - **Double/Debiased ML** → CFI 7 步 Step 4 推荐，对 nuisance function 稳健
  - **do-calculus 推导** → 理想——显式写出 backdoor adjustment formula
- 敏感性分析：假设存在一个 **未观察到的 confounder U**，它的 strength 要多大才能翻转结论？（E-value / Rosenbaum bound）——这是 Pearl 派要求的 "how sensitive is your causal claim to hidden confounders"

**红旗（违反这步的信号）**：
- "我们控制了 size, value, profitability, momentum" 但没说为什么这几个是 confounder 而不是 mediator 或 collider——看起来严格，其实是 econometric 本能反应
- 控制"生存偏差"（survival in sample）作为 control variable——selection bias 被加重而非减轻（collider conditioning）
- 论文报 β 系数 + t-stat 但从未报 **sensitivity to unobserved confounder**——金融里隐 confounder 几乎必然存在（research/01 §6 M1 局限："Pearl 的 do-calculus 在金融数据上的 identification 前提（无隐藏 confounder）几乎从不满足"）
- 用 Double ML 但没报 cross-fitting / 交叉拟合的 OOS 稳定性——Double ML 的 theoretical guarantee 依赖 cross-fitting，跳过就退回 naive regression

**救援（如果 fail 了怎么办）**：
- 基于 DAG 重推 backdoor adjustment formula，得出**应该**控制哪些变量
- 把原论文的 control variable set 与 backdoor set **逐项对比**：
  - 在 backdoor set 但未控制 → 遗漏 confounder，结论打大折扣
  - 不在 backdoor set 但被控制 → 可能是 collider，结论可能被制造出来
- 补 **sensitivity analysis**：假设存在 strength = ρ 的 unobserved confounder，β 的符号什么时候翻转？ρ 越小才能翻转 = 结论越脆弱
- 推荐阅读：Pearl *Causality* (2009) + Hernán *Causal Inference: What If* (2020) + CFI Ch. 1-2 + Chernozhukov Double ML 原论文

**Skill 运行时的触发话术**（L2 克制批评档位）：
> "控制变量表看起来详尽，但没有 DAG 支撑——区分不了 confounder / collider / mediator。specification error 比 p-hacking 更致命，这篇结论可能是后者的假象修正前者的真伤。"

**对应反模式**：
AP-2（把关联当因果）、AP-11（specification error 未识别——新）

**注意**：这一步是 López 最难通过的门槛。现实中**几乎所有金融论文都部分 fail**（research/01 §6 M1 "causal 派目前在金融没有可公开验证的业绩优势"）。Skill 使用时的纪律：不因为"难"就放低标准；标注为 "fails Step 4; conclusion should be restated as associational"，而不是 "close enough"。

---

## Step 5: Data Structure Audit（数据结构：Tick/Volume/Dollar Bars + FracDiff）

**问题**：数据 bar 是 time-based 还是 information-based？价格序列做了什么 differencing 得到平稳序列？

**为什么这步**：
AFML Ch. 2 (Financial Data Structures) + Ch. 5 (Fractionally Differentiated Features) 是 López 原创方法论的硬核（research/01 §1.1 AFML）。两个核心论点：

1. **Time bar 不对应信息流**：每天 X:30 收一根 bar 是人类时钟驱动，但市场信息是 event-driven。Tick bar（固定成交笔数）、Volume bar（固定成交量）、Dollar bar（固定成交金额）更贴近"信息到达节奏"——同等 bar 数下波动率更稳定、IID 性更好、Kurtosis 更低。AFML Ch. 2 给出实证——Dollar bar 的 IID 性显著优于 time bar

2. **Integer differencing 毁记忆**：return = 价格的一阶差分（d=1），取出平稳序列但丢掉所有 memory（长程相关被消除）。Fractional Differentiation (Hosking 1981，López AFML Ch. 5 首次金融化) 用实数阶 d ∈ (0, 1)，保证平稳同时保留最多 memory。他的 2021 Springer 论文实证 "across 87 of the most liquid futures worldwide, stationarity was achieved with d < 0.6"（research/01 §2 C8）——大部分资产 d ≈ 0.3-0.5 就够，保留了 50-70% 的原始 memory

这一步的 fail 通常**不影响论文结论对错**，但**影响 signal-to-noise**——用 time bar + integer diff 做的 ML 模型，特征里的 signal 被数据结构本身稀释了 30-60%。AFML Ch. 1 "The 10 Reasons Most Machine Learning Funds Fail" 把这两条列为独立的失败原因（research/05 §2.3；research/01 §1.2.2）。

**诊断方法（具体可执行）**：
- 数据粒度是什么？
  - Daily close → time bar，特征工程层面跛脚但可用
  - 5-min bar / 1-min bar → time bar，intraday 场景**严重**吃亏信号
  - Tick / Volume / Dollar bar → pass
- 做 stationarity 转换了吗？用什么方法？
  - raw price → 非平稳，ML 模型容易学到 spurious trend
  - log return / return → 整数阶 diff，丢 memory
  - Fractional Differentiation (d ∈ (0, 1)) → pass
- Pass 门槛：Dollar / Volume bar（intraday）或 daily close（EOD 策略） + FracDiff 或明确声明用 return 并承认 memory loss

**红旗（违反这步的信号）**：
- 所有特征用 return（r_t = log(P_t / P_{t-1})），ML 模型在 feature importance 里看到的全是短期 momentum / reversal——memory 被整数差分完全吃掉
- Intraday 策略用 5-min time bar——"固定时间节奏" 的特征工程遇到"事件驱动信息"的市场，signal 稀释到信噪比接近噪声
- 做了 ADF 检验证明平稳但没有讨论 memory preservation——典型 econometric 做法（stationarity 优先于 memory），López 在 AFML Ch. 5 明确反对

**救援（如果 fail 了怎么办）**：
- 重构 data pipeline 用 Dollar bar（对中国 A 股推荐——税制导致 Dollar bar 信息密度最高）或 Volume bar
- 价格转 FracDiff(d) with d minimizing ADF p-value subject to stationarity——AFML Ch. 5 Algorithm 5.3 给了代码
- 工具：Hudson & Thames `mlfinlab.features.fracdiff` + `mlfinlab.data_structures`（research/04 §1.2 Hudson & Thames 社区一致采用）

**Skill 运行时的触发话术**（L1 技术层）：
> "数据结构层有信噪比损失。Time bar + integer diff = signal 被数据选择稀释。这不影响结论对错，但限定了你能看见的 alpha 上限。"

**对应反模式**：
AP-5（Integer differencing 毁记忆）

---

## Step 6: CV Protocol（交叉验证：Purged K-Fold / Embargo / CPCV）

**问题**：做 cross-validation 用的什么方法？**是不是直接套了 random K-Fold？**

**为什么这步**：
金融时序**非 IID**——价格有自相关、波动率聚类、长程依赖。Random K-Fold 的前提是样本 IID，把未来数据塞进训练集、过去数据塞进测试集是常事（look-ahead bias），模型在 OOS 看起来漂亮实际是偷看答案（research/01 §2 C4；AFML Ch. 7）。López 三个原创 CV 工具：

- **Purged K-Fold**（AFML Ch. 7）：移除"label horizon 与测试集 label 重叠"的训练样本。例如用 [t, t+5] 的未来 5 日收益做 label，测试集含 t'=T 的样本时，训练集的 t ∈ [T-5, T+5] 必须全部 purge
- **Embargo**（AFML Ch. 7）：Purging 之外再加时间 buffer（通常 1-2% 样本长度），阻断 serial correlation 造成的更远距离信息泄露
- **Combinatorial Purged Cross-Validation / CPCV**（AFML Ch. 12）：切 N 组，每次测 k 组（k < N），所有 C(N, k) 组合跑一遍——得到 path distribution 而非单一 OOS 估计。在超参搜索阶段特别重要——不用 CPCV 的话，hyperparameter tuning 本身就是 overfitting 的主要来源

这个 step 是 López 对学界最具**可执行落地**的贡献之一——有 Hudson & Thames `mlfinlab.cross_validation` 的工业级实现，不用自己造轮子。但注意 AFML Ch. 7 的 Purged K-Fold 有实现细节问题（mlfinlab Issue #295 "training events can overlap with testing events"——research/04 §1.2）；即便用了 purging，还要审视具体实现（research/01 H3 决策启发式）。

**诊断方法（具体可执行）**：
- 看 CV 方法：
  - `sklearn.model_selection.KFold` (random K-Fold) → fail
  - `sklearn.model_selection.TimeSeriesSplit` (expanding window) → 部分 pass，但不 purge label horizon
  - Purged K-Fold (AFML Ch. 7) → 基础 pass
  - Purged K-Fold + Embargo → 标准 pass
  - CPCV → 优秀 pass（在超参搜索阶段是必需的）
- 检查 **label horizon 与 CV fold 长度的比**：label horizon 占 fold 长度 > 10% → purge 掉 10%+ 训练数据，要估计 information loss
- 超参搜索用了什么方法？
  - Grid search + 单一 K-Fold → 不报 CPCV path distribution，几乎必然 overfitting
  - CPCV + path distribution 报告 → pass
- Pass 门槛：至少 Purged K-Fold + Embargo；超参搜索用 CPCV

**红旗（违反这步的信号）**：
- 论文用 `sklearn.KFold` 或 `train_test_split` 随机切分
- 声明 "time series split" 但没有 purge 标签重叠期——AFML Ch. 7 明确 TimeSeriesSplit 不够
- 超参搜索报告单一 best score，不报 CPCV path distribution 或至少多 fold 方差——overfitting 到 CV 本身
- Label 用 Triple-Barrier 但 CV 不 purge——Triple-Barrier 的 label horizon 本来就是变长的，不 purge 必然 leakage

**救援（如果 fail 了怎么办）**：
- 替换 CV 方法为 Purged K-Fold + Embargo (embargo = 1%-2% of total samples)
- 超参搜索换 CPCV：N=10, k=2 或 N=6, k=2 是常见配置（AFML Ch. 12）
- 报告 path distribution 的 median / 5%-95% 区间，而非单一 mean
- 工具：Hudson & Thames `mlfinlab.cross_validation.PurgedKFold` + `CombinatorialPurgedGroupKFold`

**Skill 运行时的触发话术**（L1 技术层）：
> "CV 用 random K-Fold，非 IID 时序套 IID 方法——look-ahead leakage。替换为 Purged K-Fold + Embargo，超参搜索用 CPCV 拿 path distribution。"

**对应反模式**：
AP-6（Random K-Fold 泄露）

---

## Step 7: Trial Count Disclosure（披露试验次数：DSR / PBO 的前提）

**问题**：你在报告最终 Sharpe 之前，**试了多少个配置？** 这个数是否被**完整披露**？

**为什么这步**：
López 跨 10 年最持久的一条主张——"**Every backtest must be reported with all trials involved**"（C5 真信念，跨 5 个独立来源，research/01 §2 C5）。*Pseudo-Mathematics* 2014 原文 "**the number of model configurations used in a backtest is very often not revealed**"（research/01 §1.2.1）；*Deflated Sharpe Ratio* 2014 "most important piece of information missing ... is the number of trials attempted"（research/01 §1.2.1）。

这是**立法级主张**——2019-12-06 Congressional Testimony 第 1 条建议就是立法要求 firm 记录所有 backtests "就像药物试验日志" （research/02 §D-1 + research/05 §2.5）。他把 "未披露 trial 数的 Sharpe" 与**医药行业的非 reporting 违规**做直接类比——在医药领域是 scientific fraud。

为什么关键：Step 8 的 DSR 和 PBO 计算**完全依赖 N**（试验次数）。没有 N，你没法校正 selection bias。作者声称 "Sharpe = 2.5" 但不说试了多少——可能是试了 1 个的真 Sharpe 2.5，也可能是试了 100 个里挑的最好那个（期望 Sharpe under H0 ≈ 2.5，毫无 signal）。

**诊断方法（具体可执行）**：
- 论文里找 **"number of trials / configurations / hyperparameter combinations tested"** 这类说明。没有 = fail
- 即便有，检查是否包含：
  - Different strategies tested（策略变体数）
  - Different feature sets tested（特征组合数）
  - Different hyperparameters（超参 grid 大小）
  - Different in-sample periods tested（时间窗口数）
  - **全部相乘** = 真实 N。单独报某一层是不够的
- Pass 门槛：完整 N（所有层的试验数相乘）+ 论文在 DSR 或 PBO 计算中**实际使用** N

**红旗（违反这步的信号）**：
- Sharpe 数字出现，无 N 披露
- N 披露但 "数量级模糊" —— "tried dozens of configurations" 不够，要具体数字
- 披露的 N 明显低估——只算超参 grid 大小，不算策略变体数 / 特征变体数 / 时间窗口数
- 作者声明 "we didn't do multiple testing because we had a strong prior"——这是最危险的辩护，prior 本身是人选的，不进 N 就是隐藏了 selection

**救援（如果 fail 了怎么办）**：
- 强制披露——回去数：
  1. 尝试过多少种 label 方式？（Fixed-Horizon / Triple-Barrier / Trend-Scanning / Meta-Labeling...）
  2. 尝试过多少种 feature set？
  3. 超参 grid 多大？
  4. In-sample window 尝试了几个？
  5. 全部相乘
- 如果数不出来（因为 exploratory research 时没记录）——这正是 Congressional Testimony 要求的 "backtest log" 要解决的问题（research/05 §2.5）。下次从研究开始就维护 trial log
- 参照 Bailey+López de Prado *Deflated Sharpe Ratio* (2014, JPM) paper 的 Table 1 格式——每个 trial 都要列

**Skill 运行时的触发话术**（L3 公开对抗档位——对整个行业的 systemic 病）：
> "N 没披露。这在制药行业是 scientific fraud，在 quant finance 是惯例——这个惯例本身是问题。没有 N，你的 Sharpe 和抛硬币得来的中位数 Sharpe 无法区分。"

**对应反模式**：
AP-7（不报 trial 数的 Sharpe 宣告）、AP-1（p-hacking / backtest overfitting 的上游）

---

## Step 8: Deflated Sharpe Ratio & PBO（选择偏误校正：DSR / PBO / MinBTL）

**问题**：对 Sharpe 做了 selection bias 修正吗？**Deflated Sharpe 是多少？PBO 是多少？**

**为什么这步**：
Step 7 披露了 N，Step 8 才能**真正算**修正后的统计量。López + Bailey 的三件套：

- **Probabilistic Sharpe Ratio (PSR)** (Bailey + López 2012)：考虑样本长度 + 前 4 阶矩（skew + kurtosis）的"真实 SR 超过阈值的概率"
- **Deflated Sharpe Ratio (DSR)** (Bailey + López 2014, JPM 40(5))：在 PSR 基础上把 benchmark SR 替换为 "**N 次 unskilled trials 的期望最大 SR**"。公式核心：
  ```
  DSR = Φ((SR_observed - E[max_SR | N, H0]) · √(T-1) / √(1 - γ3·SR_obs + (γ4-1)/4 · SR_obs²))
  ```
  其中 E[max_SR | N, H0] 是 N 次 null trials 的 expected max（False Strategy Theorem 给出解析解，research/01 §3 False Strategy Theorem 术语）
- **Probability of Backtest Overfitting (PBO)** (Bailey+Borwein+Prado+Zhu 2017, J. Computational Finance)：衡量 "样本内 best strategy 在样本外排名跌到中位数以下" 的概率。PBO > 50% → 样本内选 best 在样本外比随机差，灾难

经验门槛（Bailey + López 2014 paper + 社区使用）：
- DSR > 0.95 → 可能是真 signal（但不是充分条件，见 Step 4 的 causal check）
- DSR < 0.9 → 高概率是 selection artifact
- PBO < 0.5 → 基础通过
- PBO > 0.5 → 样本外表现大概率比随机差（注意：不是"表现差"，是"比 median bad"）

注意 **MinBTL**（Minimum Backtest Length, *Pseudo-Mathematics* 2014, research/01 §3 MinBTL 术语）——给定 N，避免 overfitting 所需的最短 backtest 长度。N = 10 需要 ~2 年日数据；N = 100 需要 ~10 年；N = 1000 需要 ~100 年——现实中 quant 研究 N 常常远超 MinBTL 允许的范围。

**诊断方法（具体可执行）**：
- 论文是否报告：
  - 原始 Sharpe
  - PSR
  - DSR（或 Haircut Sharpe Ratio by Harvey-Liu 作为替代——两派解法，见 research/01 §M4）
  - PBO
- 如未报告 → 强制用 `pypbo` 库或 Hudson & Thames `mlfinlab.backtest_statistics` 补算
- 检查 **γ3, γ4** 是否实际计算——skew + kurtosis 不算的话 DSR 退化为 PSR + unskilled-trials correction，少一层保护
- Pass 门槛：DSR > 0.95 + PBO < 0.5 + 策略 backtest 长度 > MinBTL(N)

**红旗（违反这步的信号）**：
- 只报 Sharpe 不报 DSR / PBO
- 报 DSR 但 N = 1（假装只试了一个配置）—— Step 7 失败的延续
- DSR < 0.95 但作者声明 "close enough"——López 的门槛是**硬线**不是软线
- PBO > 0.5 但继续推进 → 回测告诉你 OOS 会差于随机，你还要上线

**救援（如果 fail 了怎么办）**：
- 用 `pypbo` 或 `mlfinlab` 重算 DSR, PBO, MinBTL
- DSR < 0.95 → 结论降级为 "association without established signal"，不作为 alpha 宣告
- PBO > 0.5 → 灾难，重做 Step 7（降低 N）或 Step 6（CV 方法问题）
- backtest length < MinBTL(N) → 或者收集更长历史，或者降 N（重新设计研究流程，少试）

**Skill 运行时的触发话术**（L2-L3 克制批评 → 对抗档位）：
> "Sharpe 2.5 without N is a number without meaning. DSR 算出来 0.3——这是 80% 以上的概率由 selection bias 制造。这篇论文的 finding 在 OOS 几乎确定 revert。"

**对应反模式**：
AP-1（p-hacking / backtest overfitting）、AP-7（不报 trial 数）

---

## Step 9: FDR / Multiple Testing Adjustment（多重检验修正：BH / BY）

**问题**：如果同时检验多个假设（多个因子 / 多个策略变体 / 多个 subgroup），用什么**多重检验修正**控制 False Discovery Rate？

**为什么这步**：
这是 López **另一项硬核技术贡献**，和 Step 4 的 causal audit 一起构成 CFI 7 步 Protocol 的 Step 7（research/01 §1.1 CFI 7 步 Protocol）。核心论点来自 *A Data Science Solution to the Multiple-Testing Crisis in Financial Research* (2019, JFDS)——一手 abstract "**Most discoveries in empirical finance are false, as a consequence of selection bias under multiple testing**"（research/01 §1.2.2）。这是 C1 真信念（"大部分金融实证发现是假的"）的最直接技术兑现（research/01 §2 C1）。

两个门派：
- **FWER 控制**（Family-Wise Error Rate）：Bonferroni / Holm，控制"至少一个假发现"的概率。保守到金融场景几乎不可用（太多假设同时检验时全部不显著）
- **FDR 控制**（False Discovery Rate）：Benjamini-Hochberg (BH, 1995) / Benjamini-Yekutieli (BY, 2001)，控制"所有声明显著中的假发现比例"。金融研究推荐 BH 或 BY——BY 对相关假设更 robust（金融因子相关性强，BY 更合适）

**López 与 Harvey-Liu 的差异**：Harvey-Liu haircut（2014-2015）走 statistical correction 路径，提高 t-stat 门槛到 3.0 并做 FDR 修正；López 走 data science 路径——DSR + PBO + CPCV 联合使用。两派解同一问题——Harvey 是 econometric assumption-driven，López 是 data-intensive（research/01 §M4 "对 Harvey-Liu 的定位"）。**López 原话**："**even Harvey's assumptions were generous**"（research/04 §2.2 Harvey）——Harvey 的 N 估计偏低，真实 N 更大，门槛要更严。

经验门槛：
- FDR α = 5% 是最宽松下限；金融场景推荐 FDR α = 1% 或更低
- 如果不做 FDR，单次 p < 0.05 在 N = 50 假设下，期望假发现 = 2.5 个——你看到的"显著"几乎必然是选出来的

**诊断方法（具体可执行）**：
- 论文是否做多重假设检验？
  - 检验多个因子 / 多个策略变体 / 多个子样本（如按行业、按时间段分组）—是，则必须 FDR
  - 单一假设检验—不需要 FDR，但 Step 7 的 trial count 仍要披露
- 用的什么方法？
  - 纯 p < 0.05 无修正 → fail
  - Bonferroni → 可接受但过保守
  - BH (Benjamini-Hochberg) → 基础 pass
  - BY (Benjamini-Yekutieli) → 推荐（相关假设 robust）
  - DSR 联合使用 → 最优（金融场景 López 自己的组合拳）
- Pass 门槛：BH or BY at α ≤ 5%；或 DSR > 0.95 + 披露 N

**红旗（违反这步的信号）**：
- 做了多个 subgroup 分析，每个都 p < 0.05，但不做 FDR 修正——典型 "data dredging 的 subgroup 变种"
- 检验多个因子组合，"只报显著的"——未报不显著的数量 = 隐藏的 N
- 用 Bonferroni 并声称"足够严格"但忽略了 hypothesis 之间的相关结构——BY 才是合适方法
- Harvey-Liu haircut at t > 3.0 但未报实际 haircut 后 t-stat 分布——门槛提高了但实际分布可能仍偏低

**救援（如果 fail 了怎么办）**：
- 用 `statsmodels.stats.multitest.multipletests` (method='fdr_bh' or 'fdr_by') 重算
- FDR 修正后，原显著结果大概率大量翻转（典型金融场景：factor zoo 200+ 因子，FDR 修正后可能只剩个位数显著）
- 把结论从 "X predicts Y (p < 0.05)" 改写为 "X predicts Y (FDR-adjusted q < 0.05, N = [N_total])"
- 阅读 *A Data Science Solution to the Multiple-Testing Crisis in Financial Research* (2019, JFDS)——López 的 working paper 层级的完整说明

**Skill 运行时的触发话术**（L3 公开对抗档位——这是 factor zoo 的核心病）：
> "Most discoveries in empirical finance are false. 你报的 17 个显著因子，FDR 修正后大概率剩 2-3 个，甚至零。Factor zoo 是 multiple testing 工业化的产物，不是 alpha 工业化的产物。"

**对应反模式**：
AP-1（p-hacking / backtest overfitting）、AP-7（不报 trial 数的 Sharpe 宣告）

---

## Step 10: Sisyphus vs Meta-Strategy（组织层审查：研究流水线是否工业化）

**问题**：这项研究是**一个人端到端做的**（Sisyphus paradigm）还是**分工的研究流水线**（Meta-Strategy paradigm）？

**为什么这步**：
López 对量化研究失败的结构性诊断——**组织论比技术论更根本**。AFML Ch. 1 "Financial Machine Learning as a Distinct Subject" 原创 Sisyphus vs Meta-Strategy 二分（research/01 §1.1 AFML + §3 术语）。*10 Reasons Most ML Funds Fail* 第 1 条就是 Sisyphus paradigm（research/05 §2.3）。2021 Lecture *Escaping the Sisyphean Trap: How Quants Can Achieve Their Full Potential*（research/01 §2 C9）是这个论点的演讲版。ADIA Lab 从 50 人扩到 150 人团队（research/05 §1.6）是他的组织实验。

**Sisyphus paradigm**：一个人从数据清洗、特征工程、建模、回测到部署全链路负责。三大病：
1. **能力圈错配**：没人同时是 data engineer + feature analyst + ML scientist + backtester + risk manager + deployment engineer——每一环都被一个"非专家"做
2. **激励错位**：同一人做研究又做回测，有 "把回测调漂亮" 的动机——Step 7 的 trial count 永远不会被如实披露
3. **知识不累积**：每个项目重起炉灶，上个项目的失败教训不进入工具链

**Meta-Strategy paradigm**：研究流水线化分工：
- **Data curators**（专精数据质量 / bar construction）
- **Feature analysts**（专精 feature importance / orthogonalization）
- **Strategists**（专精 label / CV / bet sizing）
- **Backtesters**（**独立的**做 DSR / PBO / FDR，不受策略作者影响）
- **Deployment engineers**（独立的做 live trading infrastructure）
- **Risk managers**（独立的做 fragility 审视，对标 Taleb 的视角）

关键设计：**backtester 必须与 strategist 组织上分离**——这是 step 7 trial count 诚实披露的激励保障。strategist 有动机不报 N，independent backtester 没有。

**但注意 López 自己的 ADIA 实验限制**（research/01 §6 M4 模型 4 局限）：
- 他 AQR 7 个月失败（research/05 §1.4）暗示 Meta-Strategy 在**有强势既有文化**的机构里未必能植入——小 lab / sovereign / 新组可以，大型 hedge fund 做不到
- "工厂模型"需要 AUM / 资源规模——10 人以下团队强行分工反而变成瓶颈
- 激励结构怎么设计他**没有** operational 指南——只有方向没有 recipe（research/05 §6.1）

所以这一步的审查**不是纯技术 checklist**——是组织诊断，有实际 context。

**诊断方法（具体可执行）**：
- 研究团队规模多少人？
  - 1 人 → Sisyphus
  - 2-5 人且分工模糊 → 弱 Sisyphus
  - 6+ 人且分工清晰（上述 6 个岗位至少分 3 组） → 基础 Meta-Strategy
  - 团队 15+ 且 backtester 与 strategist 组织分离 → 标准 Meta-Strategy
- 研究流程是什么？
  - "我试了很多配置，最后这个 work 了" → Sisyphus 单人循环
  - "data team 清数据 → feature team 做特征 → strategy team 定 label + CV → backtester team 做 DSR/PBO/FDR 盲测" → Meta-Strategy
- Backtester 是否**独立**评估（不是 strategist 自己跑自己的）？——这是 Step 7 诚实的组织保障
- Pass 门槛：至少 3 个独立角色分工 + backtester 独立

**红旗（违反这步的信号）**：
- 论文作者 1 人或 2 人（小研究可以，生产策略不够）
- 没有 "independent backtester" 或 "independent validation team" 的机制
- 研究 log / trial log 不存在（organizational memory = 0）——Congressional Testimony 立法建议的前提是"有 log 可查"
- 团队分工但 backtester 向 strategist 汇报——激励仍在 strategist 一侧
- "我们是 small team 做不到工业化"——ADIA Lab 之前也是小 team，这是 excuse 不是事实

**救援（如果 fail 了怎么办）**：
- 小团队 → 至少引入 **Chinese wall** 做 independent backtesting：strategist 交代码，backtester **不看 strategy 逻辑**只跑 DSR/PBO/FDR 流水线（"盲测"）
- 引入 **trial log 基础设施**：每次 backtest 自动 log 到共享 DB（MLflow / DVC），N 自动累计
- 引入 **post-mortem 习惯**：每个 fail 的策略都写 post-mortem，进入 team knowledge base（防止 Sisyphus 的 "知识不累积" 病）
- 大团队（15+）→ 明确分工，参考 AFML Ch. 1 的 5 角色清单
- 参考 Numerai tournament 的"众包 quant"结构——"Meta-Strategy"组织观的开源实例（research/01 §2 C9 + research/04 §1.2 Numerai）

**Skill 运行时的触发话术**（L2 克制批评档位）：
> "这是 Sisyphean workflow——一个人端到端，激励上注定 trial count 不诚实。技术再严格也救不了组织结构错了。"

**对应反模式**：
AP-4（单人英雄 Sisyphus workflow）、AP-7（不报 trial 数的激励由组织结构决定）

---

## 元原则

**10 步全过一遍的时间**：研究审查场景 15-30 分钟；生产策略上线前审查可能需要 2-4 小时（特别是 Step 4 causal audit 和 Step 9 FDR 计算）。

**不能跳步**：
- Step 1 claim classification 错了 → 后 9 步在**替错误答案打磨**
- Step 4 confounder audit 没做 → Step 8 DSR 再高也可能是 selection 的 causal false positive
- Step 10 组织层 fail → Step 7 trial count 披露在激励上不成立，后面技术步骤的诚实性全崩

**Step 1-3 是 "claim" 层审查**，Step 4-7 是 "data & model" 层审查，Step 8-9 是 "statistics" 层修正，Step 10 是 "organization" 层保障。**任一层 fail 整个研究都不成立**。

**每步都有独立 fail 模式**，不要合并判定。一项研究可能 Step 1-3 都 pass 但 Step 4 fail——结论是 "associational signal with unclear causal identification"，不是 "alpha"。

**Congressional Testimony 立法视角**（research/05 §2.5）：这 10 步如果被强制性立法（就像药物试验日志），factor zoo 论文的 90%+ 会停止发表——这不是技术建议，是**伦理要求**。López 的论点："在医药领域是 scientific fraud，在 quant finance 是惯例——这个惯例本身是问题"。

---

## 速查卡（10 步 + 10 个核心指标）

| Step | 审查点 | 核心指标 | Pass 门槛 | 对应 López 一手来源 |
|------|--------|----------|-----------|---------------------|
| 1 | Claim Classification | claim type 声明 | 明示 associational/causal + 一致性 | CFI (2023) + LinkedIn 2023-01 |
| 2 | Causal Graph 可见性 | DAG 公开 + mechanism | DAG + 可证伪 predictions | CFI Ch.1 + CFI 7 步 Protocol Step 2 |
| 3 | Variable Selection | MDA / Clustered MDA | MDA 至少，相关特征用 Clustered | AFML Ch. 8 + ML4AM Topic 5 |
| 4 | Confounder / Collider | backdoor adjustment set | DAG-based adjustment + sensitivity | CFI Ch.2 + Protocol Step 3-4 (do-calculus + Double ML) |
| 5 | Data Structure | bar type + FracDiff d | Dollar/Volume bar + d ∈ (0, 1) | AFML Ch. 2 + Ch. 5 + 2021 Springer |
| 6 | CV Protocol | Purged K-Fold + Embargo + CPCV | 至少 Purged + Embargo；超参用 CPCV | AFML Ch. 7 + Ch. 12 |
| 7 | Trial Count | N（全部层相乘） | 完整 N 披露 | *Pseudo-Mathematics* (2014) + Congressional Testimony (2019) |
| 8 | DSR & PBO | DSR, PBO, MinBTL | DSR > 0.95, PBO < 0.5, T > MinBTL(N) | *Deflated Sharpe* (2014) + *PBO* (2017) |
| 9 | FDR Adjustment | BH / BY q-value | q < 0.05 with correlation-robust method | *Data Science Solution to Multiple-Testing Crisis* (2019) |
| 10 | Sisyphus vs Meta | 分工 + independent backtester | 至少 3 独立角色 + backtester 独立 | AFML Ch. 1 + 2021 Lecture |

**10 个核心数字**（一项 alpha 宣告前必须报告的）：
1. **DSR** (Deflated Sharpe Ratio)——最好 > 0.95
2. **PBO** (Probability of Backtest Overfitting)——必须 < 0.5
3. **FDR q-value**（BH 或 BY 修正）——必须 < 0.05（推荐 < 0.01）
4. **t-stat** (Harvey-Liu haircut 后)——推荐 > 3.0
5. **raw Sharpe** ——披露但不作为决策依据
6. **Purged CV score** (mean + 5%-95% interval from CPCV paths)
7. **FracDiff d**——实际使用的 differencing 阶数（理想 d < 0.6）
8. **causal graph coverage**（DAG 节点数 / 潜在 confounder 数比例——> 80% 为好）
9. **Trial count N**（所有层相乘）+ MinBTL(N) 核对
10. **Sisyphus score**（1 = 单人 / 10 = 完整 Meta-Strategy）——组织层诊断

---

## 与 Taleb / Munger 10 步的对比

| Step | Munger 版本 | Taleb 版本 | **López 版本** | 差异 |
|------|-------------|------------|----------------|------|
| 1 | Edge 的经济学解释 | Fragility 三态路由 | **Claim Classification** | Munger 问"edge 在哪"，Taleb 问"结构凸凹"，López 问"声明类型——关联还是因果" |
| 2 | 样本外验证 | Payoff 凸性 | **Causal Graph 可见性** | 三者完全不同视角——样本外 / 凸性 / DAG |
| 3 | 逆向 Kill-Path | 分布 class 判断 | **Variable Selection Discipline** | López 问"特征怎么选"——p-value 还是 feature importance |
| 4 | 交易成本与容量 | Turkey 检查 | **Confounder / Collider Audit** | López 唯一用 do-calculus 的那一步——specification error 审查 |
| 5 | 最大回撤路径 | Kill-Path via Negativa | **Data Structure Audit** | López 问"bar 和 differencing 对吗"——信号噪声比 |
| 6 | 能力圈 | Skin in the Game | **CV Protocol** | López 问"CV 方法对吗"——Purged / Embargo / CPCV |
| 7 | Lollapalooza | Ergodicity 诊断 | **Trial Count Disclosure** | López 问"N 报了吗"——DSR/PBO 的前提 |
| 8 | 反确认 | Lindy 门槛 | **DSR & PBO** | López 问"Sharpe 修正后是多少"——selection bias 校正 |
| 9 | 安全边际 / Kelly | Kelly × 0.15 | **FDR Adjustment** | López 问"多重检验修正了吗"——factor zoo 的核心病 |
| 10 | "Nothing to add" | "Do Nothing" | **Sisyphus vs Meta-Strategy** | López 问"组织结构工业化了吗"——技术层的激励保障 |

**三者互补不重复**：
- **Munger 查认知 / 激励 / 能力圈** —— "你想清楚了吗 / 你懂吗 / 你会被偏误带跑吗"
- **Taleb 查分布 / 尾部 / 凸性** —— "你会爆吗 / payoff 结构对吗 / 厚尾覆盖了吗"
- **López 查科学性 / 方法论 / 选择偏误** —— "这是科学吗 / N 披露了吗 / causal graph 在哪"

**结合使用**：量化场景下把三套 checklist 做 cross-reference——同一策略在 Munger 某步答得上、在 Taleb 答不上、在 López 答不上（或任两者组合）都是信号。通常：
- López 在 Munger 上游——先审研究诚信，再审 edge 经济学（一个 associational signal 即便 Munger 答得出 edge，也不是 alpha）
- Taleb 在 López 下游——研究通过了 López 10 步，Taleb 再问"即便真有 signal，厚尾下你的仓位能活下来吗"
- 三者 full pass = 学术严谨 + 商业 edge + 尾部生存，三重验证

---

## 一句话记忆

> "**A backtest is not a theory.** Feature importance is. Causal graph is. Trial count disclosure is. DSR is. FDR is. Independent backtester is. 不是这些东西给你 alpha，是没有这些东西**你给市场 alpha**。"

— 基于 López 方法论核心主张的综合复述，具体出处：AFML 引言 "A historical simulation of an investment strategy's performance (backtest) is not a theory"（research/01 §1.1 ML4AM）+ "Backtesting is not a research tool. Feature importance is."（research/03 §A1 证据 1）

---

**文件终结**。本 checklist 是 Skill 运行时的研究诚信审查工具。任一步 fail → 结论层降级，不做 alpha 宣告。
