# Anti-Pattern 识别库（Methodology Clinic）

> López de Prado 的判断力核心一半是"这项研究是 science 还是 alchemy"的快速归类。
> 下面 18 条按**出现频率 × 对 out-of-sample 的损害烈度**排序，分 5 大类：
> A Backtest / 模型评估（6）· B 因果 / Specification（4）· C 研究流程 / 组织（4）· D 激励 / 披露（3）· E 元层自检（1）。
>
> 每条结构：**症状（如何识别）· 原理（为什么错）· 反例（误用 López 风格的样貌）· 救援（López 会怎么做）· 触发话术 · 可信度**。
>
> 一手来源全部标到论文名 + 年份 / 书章节 / 讲座题目 / LinkedIn，可回溯到 `research/0X-*.md`。
> 触发话术符合本人表达 DNA：scientist vs alchemist 二元轴、"Hence," 段首、否定-肯定二段、数值（t-stat / Sharpe / N trials）贴身伴随攻击论断。

---

## A. Backtest / 模型评估反模式（6 条）

搞错 backtest 的认识论地位，后面无论报多少 t-stat 都是概率装饰。这 6 条是 López 跨 12 年最密集攻击的对象。

### AP-1：未披露 trial 数的 Sharpe 宣告（Unreported Trials）

**类别**：A Backtest

**症状（如何识别）**：
- 摘要 / 报告 / 宣告只亮**最终** Sharpe / t-stat / IC，不说试了多少个 configuration
- "我们测了一组参数，效果很好"——"一组"是话术；实际 grid 可能是 10×10×10
- 代码仓库里的 `backtest.py` 与最终报告之间没有**完整 trial 日志**
- 论文附录不列"discarded strategies"——只有幸存者
- 审阅问"还有哪些 variants"时作者说"不重要"或"都差不多"

**原理（为什么错，López 的论证）**：
Bailey-Borwein-López de Prado-Zhu *Pseudo-Mathematics and Financial Charlatanism* (AMS Notices 2014) 用解析解证明——在足够 N 次 unskilled trials 下几乎必然找到一个"显著"Sharpe，且**在 memory effects 下 out-of-sample 期望收益为负、不是零**。不报 N 就是把 selection bias 藏起来。*Deflated Sharpe Ratio* (Bailey-López de Prado, JPM 2014) 给出修正公式：`Φ((SR*-SR₀)·√(T-1) / √(1-γ₃·SR₀+(γ₄-1)/4·SR₀²))`，其中 `SR₀` 是 N trials 下的期望最大 SR。不知道 N = DSR 算不出。

**反例（误用 López 风格的样貌）**：
> "Our rigorous machine learning pipeline achieves an annualized Sharpe of 2.4 with t-stat = 3.8, significant at p < 0.001. The research follows best practices including purged cross-validation."
>
> —— 看起来"遵守方法论"，但全篇没有一个数字是"我们一共尝试了多少组特征 / 多少种窗口 / 多少次超参"。这是 Marcos' Third Law 直接 violation："Every backtest must be reported with all trials involved."

**救援（López 会怎么做）**：
- 用 **Deflated Sharpe Ratio** 替代裸 Sharpe——把 N trials 计入
- 用 **Probability of Backtest Overfitting (PBO)**（Bailey+Borwein+Prado+Zhu, *J. Computational Finance* 2017）——衡量"样本内 best 在 OOS 排名跌破中位数"的概率
- 预登记（pre-registration）：在跑 backtest 前声明 hypothesis + protocol + 预期 configurations 数量
- 报告里强制加 "trials log" section：grid 大小 × 超参搜索次数 × 特征筛选轮数 × 最终 survived configurations
- 引用 **False Strategy Theorem**（López de Prado + Bailey, *American Mathematical Monthly* 2021）——给 "what SR would an unskilled strategy achieve" 一个解析下界

**触发话术**：
> "Sharpe 2.4 is not information. Trials count is information. Without N, this is probability theater. Hence, report DSR, not SR. Otherwise the result is **likely false** under multiple testing."

**可信度**：一手高（*Pseudo-Mathematics* 2014 + DSR 2014 + PBO 2017，跨 10 年稳定主张，Marcos' Third Law 有独立第三方笔记确认——research/01 §1.2.1 + §2 C5）

---

### AP-2：金融时序套 IID Cross-Validation（Random K-Fold on Financial Data）

**类别**：A Backtest

**症状（如何识别）**：
- 代码用 `sklearn.model_selection.KFold(shuffle=True)` 或 `cross_val_score` 直接喂金融时序
- Training 样本的 label horizon 与 test 样本时间窗**重叠**（label 在 t 到 t+h 区间，训练集却含 t+h-5 的观测）
- 没有 embargo——训练 fold 与测试 fold 时间上相邻，serial correlation 直接泄露
- 报告里写"5-fold cross-validation"但不说是不是 time-aware
- OOS Sharpe 比真·unseen Sharpe 高一截（典型信号：部署后一个月就崩）

**原理（为什么错，López 的论证）**：
AFML (Wiley 2018) Ch. 7 系统论证——金融 label 本质非 IID：(1) returns 有 serial correlation；(2) label 基于 Triple-Barrier 时 horizon 跨多个 bar，观测互相重叠；(3) volatility clustering 让相邻窗口信息耦合。用 random K-Fold = 训练集偷看未来。López 原创 **Purged K-Fold**：剔除 label horizon 与测试窗重叠的训练样本；再加 **Embargo**：在每个测试段后留一段时间 buffer 切断 serial correlation。AFML Ch. 12 进一步提出 **Combinatorial Purged CV (CPCV)**——切 N 组测 k 组，所有 C(N,k) 组合跑，拿 path distribution 而非单点估计。

**反例（误用 López 风格的样貌）**：
> "We use 10-fold cross-validation to avoid overfitting, with train/test splits randomized across the full 2015-2024 sample. Our out-of-sample IC is 0.12."
>
> —— "cross-validation" 被当成防过拟合的 ritual 引用，但 random split + 无 embargo + label overlap 同时犯三宗。这是 López 10 Reasons 里的第 6 条。

**救援（López 会怎么做）**：
- 默认 **Purged K-Fold + Embargo**，绝不直接 random K-Fold（AFML Ch. 7）
- 超参搜索阶段用 **CPCV**（AFML Ch. 12）——拿 path distribution 评估参数稳定性而非单一 OOS 点
- 审计具体实现：Hudson & Thames mlfinlab Issue #295 暴露"PurgedKFold: training events can overlap with testing events"——**即便用了 purging 库也要检查实现**（research/04 §1.2）
- label horizon `h` 的 embargo 长度至少 `h` 量级，高频数据再放宽

**触发话术**：
> "Random K-Fold on financial series is not cross-validation. It is a leakage generator dressed in sklearn syntax. Hence, purge the overlaps, embargo the tails. Otherwise your OOS is in-sample with extra steps."

**可信度**：一手高（AFML Ch. 7 + Ch. 12 + research/01 §2 C4，mlfinlab 独立复现 — research/04 §1.2）

---

### AP-3：用 Integer Differencing 毁掉记忆（Integer Differencing Memory Kill）

**类别**：A Backtest

**症状（如何识别）**：
- "我们先把价格转成 returns 做平稳化处理"——然后所有特征基于 `df.diff()` 或 `df.pct_change()`
- ADF test 只试 d=0（价格原始）和 d=1（一阶差分）两档，没有中间值
- 特征工程后模型的 feature importance 集中在最近 1-5 bar——记忆已经被 d=1 砍光
- 文献综述里引用"Dickey-Fuller 检验"但没提 Hosking (1981)
- 论文 methodology 段落出现 "log returns ensure stationarity"——把平稳性当免费午餐

**原理（为什么错，López 的论证）**：
AFML Ch. 5 的核心论点——价格序列在平稳性与记忆之间有**根本 tradeoff**：d=0 有最长记忆但非平稳（ADF 拒绝）；d=1（returns）是平稳但**几乎完全丢失记忆**。整数差分是"要么不治，要么杀死病人"。López 把 Hosking (1981) 的 **Fractional Differentiation**（实数阶 d∈(0,1) 差分）引入金融 ML——经 AFML 内部实证 "across 87 of the most liquid futures worldwide, stationarity was achieved with d < 0.6"（也见 2021 *Int. J. Advances in Engineering Sciences and Applied Mathematics* 的 Springer 版）。即保留大部分记忆又通过 ADF。这是 *10 Reasons Most ML Funds Fail* (JPM 2018) 的第 2 条。

**反例（误用 López 风格的样貌）**：
> "Raw prices are non-stationary, so we transform using log-returns. This yields a stationary series suitable for standard machine learning, as confirmed by the Augmented Dickey-Fuller test (p < 0.01)."
>
> —— "confirmed by ADF" 的 ritual 掩盖了 d=1 丢记忆的事实。模型在 returns 上几乎看不到 mean-reversion / momentum 的长程结构——Sharpe 低就甩锅给"市场难做"。

**救援（López 会怎么做）**：
- 对每个价格 / 隐含波动率 / 信用利差序列，跑 **fractional differentiation grid**（AFML Ch. 5 提供的 fixed-width window 实现）
- 找 minimum d 使得 ADF p < 0.01 而保留 ≥ ρ 的相关性（典型 ρ > 0.7）
- 在模型 pipeline 里把 d 作为**每个 instrument 单独估计的 hyperparameter**，不是全局常数
- 对 non-price 特征（volume、spread、toxicity）各自判断是否需要 frac-diff
- 引用证据："d < 0.6 works for most liquid futures"——从 AFML 87 futures 实证

**触发话术**：
> "Integer differencing is not stationarity. It is lobotomy. Hence, use fractional differentiation with minimum d that passes ADF. Otherwise your model is predicting noise because you removed the signal."

**可信度**：一手高（AFML Ch. 5 原创应用 + 2021 Springer 论文 + research/01 §2 C8）

---

### AP-4：Backtest 当研究工具（Backtest as Research Tool）

**类别**：A Backtest

**症状（如何识别）**：
- 研究 workflow："跑 backtest → 看哪组参数 Sharpe 最高 → 用那组做报告"——**backtest 在假设生成阶段就介入**
- 调参循环直接以 backtest Sharpe 为目标函数——"我们优化了 Sharpe"
- 论文 / 报告里的 "methodology" 段落顺序是：数据 → 特征 → backtest 结果 → （事后的）theory
- Feature importance 排名只在 backtest 跑完之后看——特征选择已被 outcome 污染
- "这个 idea 因为 backtest 跑得好所以我们深入研究" —— 因果倒置

**原理（为什么错，López 的论证）**：
AFML Ch. 1 + ML4AM (Cambridge 2020) 明确："**A historical simulation of an investment strategy's performance (backtest) is not a theory.**" 第三方笔记 (reasonabledeviations.com) 把 "Backtesting while researching is like drink driving" 标记为 **Marcos' Second Law**（research/01 §2 C5）。Backtest 的认识论地位是 **out-of-sample evidence**（证据），不是 **research tool**（工具）。把它前移到研究阶段等于让 OOS 提前消耗——因为"好 Sharpe"本身变成 selection criterion，剩下再多 OOS 都已被偷看过。AFML Ch. 1 的替代是 "Feature importance is the research tool"（research/03 §G3 证据 13）。

**反例（误用 López 风格的样貌）**：
> "We systematically backtested 300 feature combinations on 2015-2022 data, identified the top-5 by Sharpe ratio, and proceeded to deploy these. Rigorous, data-driven, and scientifically defensible."
>
> —— "data-driven" 是幌子——实际是 300 trials selection bias，未报 DSR，再把 backtest Sharpe 当 ground truth。López 会说：this is not research, this is overfitting at industrial scale.

**救援（López 会怎么做）**：
- **Feature importance 优先，Sharpe 最后**——AFML Ch. 8 的 MDI / MDA / SFI 替代 "高 Sharpe 则 keep" 的筛选
- 研究阶段用 **synthetic data**（Ornstein-Uhlenbeck processes, AFML Ch. 13）验证策略 robustness——不耗真实 OOS
- 强制 pre-registration：在跑 backtest 之前**书面**声明 hypothesis + causal mechanism + feature list
- backtest 只在 pipeline 末端跑一次——且同时报 **DSR + PBO + CPCV path distribution**
- 如果 hypothesis 在 synthetic data 上不 work，不用浪费真实数据

**触发话术**：
> "Backtesting is not a research tool. Feature importance is. Hence, prove your mechanism on synthetic data first, then spend OOS once. Otherwise it is drink driving — you arrive, but the passenger is dead."

**可信度**：一手高（AFML Ch. 1 + ML4AM + Marcos' Second Law 第三方确认 — research/01 §2 C5 + research/03 §G3）

---

### AP-5：单模型端到端预测方向+规模（Single-Model End-to-End）

**类别**：A Backtest

**症状（如何识别）**：
- 一个 classifier / regressor 同时输出 `{enter or not, long or short, position size}`——三件事揉一个 loss function
- 训练 label 是"未来 h 期 return 的符号 × 大小"——把"是否下注"和"下多大"混在一个标签里
- 模型在"不确定情形"（实际应该 pass）时仍给出非零仓位
- Precision / recall 都低但 Sharpe 还行——因为"乱蒙的仓位"被 volatility scaling 救了
- 没有单独的 "abstain" 通道——0 仓位必须通过 threshold 人为剪枝

**原理（为什么错，López 的论证）**：
AFML Ch. 3 原创 **Triple-Barrier Method + Meta-Labeling**。主模型（primary model）管 **side**：+1 / -1 / 0 方向信号；二级模型（meta model）管 **size**：在主模型给出方向后，决定"是否下注 + 下多大"（含 size=0 即 abstain）。分离职责的原因：(1) 方向预测与规模预测要求的特征集不同；(2) False positive 成本（错下注）≠ False negative 成本（错过）；(3) 二级模型可以学 primary 的**可信度 profile**——Hudson & Thames 复现 "mean-reversion 策略准确率从 17% → 63%"。端到端模型把这三层强塞进一个 loss，几乎必然在高不确定情形下过度下注。

**反例（误用 López 风格的样貌）**：
> "Our end-to-end XGBoost model predicts next-day return directly, with position size proportional to predicted magnitude. Clean, parsimonious, and avoids the complexity of stacked architectures."
>
> —— "parsimonious" 被当美德——实际是把三个本质不同的决策塞进一个模型，loss 梯度在"方向对但规模错"和"方向错但规模小"之间无法正确分摊。Meta-labeling 可让 recall 保低但 precision 升高——这个架构做不到。

**救援（López 会怎么做）**：
- **Primary model**（AFML Ch. 3）输出 side ∈ {-1, 0, +1}——recall 优先（抓住所有机会）
- **Meta-model**（AFML Ch. 3）在 primary 给出非零 side 时决定"是否真下注 + 下多大"——precision 优先
- Primary 可用简单规则 / 低阶 ML；Meta 用丰富特征（prediction confidence, volatility regime, microstructure state）
- 注意 Baldisserri (QuantConnect) 实测边界：meta-labeling 对 **discretionary / 规则型** primary 策略提升最大，对 end-to-end ML primary 提升有限（research/04 §2.3）——引用时同时披露这个限缩

**触发话术**：
> "One model cannot answer 'should I trade', 'which way', and 'how much' simultaneously. Hence, separate side from size. Primary for recall, meta for precision. Otherwise your position sizing is noise decorated as conviction."

**可信度**：一手（AFML Ch. 3 原创）+ 二手实操分歧（Hudson & Thames 正向复现 vs Baldisserri 限缩 — research/04 §2.3）

---

### AP-6：CPCV 退化成 Purged K-Fold（CPCV Calculation Shortcut）

**类别**：A Backtest

**症状（如何识别）**：
- 论文 methodology 段写 "we use Combinatorial Purged Cross-Validation" 但具体只跑 5-10 个 path——不是 C(N,k) 的完整组合
- 代码 `cpcv(n_splits=6, n_test_splits=2)` 本应生成 C(6,2)=15 paths，实际只跑 6 次
- 算力 budget 不匹配 CPCV 的理论计算量（CPCV 的开销随参数数量 exponential 增长）
- 报告里只给一个 "CPCV Sharpe" 数字，没有 path distribution 直方图 / 5-95% 分位
- 超参搜索外层套 CPCV 时偷偷退化到最简单的 train/test 切分

**原理（为什么错，López 的论证）**：
AFML Ch. 12 提出 CPCV 的核心价值**不是单点 OOS 估计**，而是 **path distribution**——同一策略在 C(N,k) 条"平行历史"下 Sharpe 分布的形状。看单点 Sharpe 等于白做 CPCV。业界批评 CPCV "computationally expensive as the quantity of parameters grows"（towardsai.net，research/04 §3.3）——这是**真问题**但答案不是"悄悄降级"，而是：(1) 降低 N（接受更粗的 path resolution）；(2) 降低参数空间维度（通过 feature importance 预筛）；(3) 在 synthetic data 上用完整 CPCV，在 real data 上用 Purged K-Fold + DSR。把 Purged K-Fold 结果 label 成 "CPCV" = 在方法论名称上造假。

**反例（误用 López 风格的样貌）**：
> "We apply Combinatorial Purged Cross-Validation (López de Prado 2018) with 6 splits. The resulting OOS Sharpe is 1.8."
>
> —— "Sharpe 1.8" 是单点数字，完全浪费了 CPCV 的 path distribution 价值。而 "with 6 splits" 暗示这是 Purged 6-Fold，不是 CPCV 的 C(N,k) 组合结构。方法论引用与实际计算脱节。

**救援（López 会怎么做）**：
- 对 CPCV 的使用强制报告 **path distribution**——最小化展示：min / 5% / 25% / median / 75% / 95% / max Sharpe 七个数
- 如果参数空间过大：先用 feature importance (AFML Ch. 8) 降维到 top-k 特征再跑 CPCV
- 算力受限时**诚实降级**：在报告里写 "used Purged K-Fold instead of CPCV due to compute constraints"——不要用 CPCV 名字
- 引用 research/04 §3.3 的工程批评时承认"CPCV 开销真实存在，但不 excuse 名字造假"

**触发话术**：
> "You named it CPCV and reported a single Sharpe. That is Purged K-Fold with a luxury label. Hence, either show the path distribution (five percentiles minimum) or rename the method. The label is not the method."

**可信度**：一手（AFML Ch. 12 原创）+ 二手工程批评（research/04 §3.3 towardsai.net 计算开销问题，mlfinlab 实现 — research/04 §1.2）

---

## B. 因果 / Specification 错误（4 条）

这一类是 López 在 2022 之后升级的主战线。即便 backtest 方法论全对、p-hacking 全修复，如果 causal structure 错了，结论仍然系统性亏损。

### AP-7：把关联当因果（Associational Claim as Causal）

**类别**：B Causal

**症状（如何识别）**：
- 论文 / 报告结论用"因子 X **predicts** / **drives** / **causes** Y"但通篇只有相关性证据
- 没有声明 identification strategy（IV / RDD / natural experiment / DAG + do-calculus）
- 机制解释是 post-hoc："这个因子 work 是因为流动性溢价"——没有独立可证伪的 mechanism
- 被问"如果我们 intervene 这个因子，Y 会怎样"时答不上——只能说"历史上相关"
- Fama-French 风格的三因子回归被报告为 "factor model"——但"factor" 一词被用在纯统计（PCA load）而非经济结构（causal driver）层

**原理（为什么错，López 的论证）**：
*Causal Factor Investing* (Cambridge Element 2023, 副标题 "Can Factor Investing Become Scientific?") 全书论点：
> "Virtually all journal articles in the factor investing literature make **associational claims**, in denial of the causal content of factor models... Authors do not identify the causal graph consistent with the observed phenomenon, they justify their chosen model specification in terms of correlations, and they do not propose experiments for falsifying causal mechanisms."

关联 ≠ 因果的工程代价：(1) association 在 regime shift 下断裂——因为 confounder 变了；(2) 策略被 crowded 后 unwind 更快——没有 causal protection；(3) 无法做反事实推理（"如果 policy X 变化，这个因子还 work 吗"）。*Why Has Factor Investing Failed?* (López de Prado + Zoonekynd, SSRN 2024) 升级定论："specification errors arguably more dangerous to investors than p-hacking"——即便 p-hacking 全修正，specification error 仍会导致系统性亏损。

**反例（误用 López 风格的样貌）**：
> "We show that the value factor explains cross-sectional returns with t-stat 4.2 across 30 years of data. This confirms value as a priced risk factor."
>
> —— "explains" 和 "confirms" 是 causal 语言，但全文只有 correlation 证据，没有 causal graph、没有 intervention、没有 falsification protocol。López 会归类为经典 associational claim。

**救援（López 会怎么做）**：
- 对每个"因子 X 解释 Y"的 claim，先画 **causal DAG**：X 是 cause 还是 effect 还是 collider？有哪些 confounders？
- 引用 **Pearl's do-calculus** 做 intervention identification（*Causal Factor Investing* 2023 + Pearl 源头）
- 应用 ADIA Lab 的 **7 步 Protocol for Causal Factor Investing**（research/01 §1.1 CFI）：
  1. Variable Selection (ML) → 2. Causal Discovery (algorithms + domain knowledge) → 3. Causal Adjustment (do-calculus) → 4. Causal Estimation (double ML) → 5. Portfolio Construction → 6. Backtesting (respecting causal structure) → 7. Multiple Testing Adjustments (FDR)
- 在论文明确标注 "associational claim" vs "causal claim"——后者承担更高举证责任

**触发话术**：
> "This is an associational claim dressed as causal. Hence, where is the causal graph? Where is the do-calculus intervention? Without them, your t-stat of 4.2 is a correlation ceremony, not evidence. Factor models that cannot state their causal mechanism are **likely misspecified**."

**可信度**：一手高（*Causal Factor Investing* 2023 + *Why Has Factor Investing Failed?* 2024 + LinkedIn 2023-01 "associational quant vs causal quant" — research/01 §1.1 + research/02 §C-1）

---

### AP-8：Factor Literature 不声明 Causal Mechanism（Missing Causal Graph）

**类别**：B Causal

**症状（如何识别）**：
- 论文 / 策略文档的 "methodology" 段跳过 causal graph 直接进 regression specification
- "我们的 factor 是 value + momentum + quality 的组合"——仅枚举 predictors，不声明每条 edge 的 mechanism
- 机制描述抽象且不可证伪："low P/B stocks outperform because investors underreact to value"——没给"underreaction"的独立测量
- 当被问"如果 investor behavior 变了这个 factor 还 work 吗"——答"可能不 work，但历史数据强"
- 多 factor 组合时每个 factor 独立建模，**没有 cross-factor causal structure**（e.g., momentum 是否通过 volatility 影响 value？）

**原理（为什么错，López 的论证）**：
Factor literature 的标准姿态是 "statistical pattern + post-hoc rationalization"。*Causal Factor Investing* (2023) 的批评重心之一：论文**不主动声明 causal graph 是什么**就直接做 model specification。后果：
- 当 observed pattern 消失，无法诊断是 regime shift、confounder 变了、还是原 graph 错了
- Collider bias 不被检测——条件在 collider 上会人为制造虚假 association（Pearl 的经典例子）
- 多 factor 组合假设 additive independent effects——实际可能有 mediator / moderator 关系
- 无法做 out-of-market 泛化（A 股因子 → 欧股）因为 mechanism 未声明

**反例（误用 López 风格的样貌）**：
> "We construct a 5-factor model (market, size, value, profitability, investment) following Fama-French (2015). The factor loadings are estimated via rolling regression. No assumption about the underlying data-generating process is imposed, making the model agnostic and robust."
>
> —— "agnostic" 被包装成方法论美德，实际是放弃因果解释权。López 会说：agnostic = 既不能解释 work 也不能诊断 fail，这不是 robust，这是 **methodologically illegitimate**.

**救援（López 会怎么做）**：
- 对每个 factor 提出一个**可证伪的** causal mechanism：在什么条件下 mechanism 会断裂？（e.g., "value 因子依赖于 investor underreaction → 如果 underreaction 通过 X 机制被消除，value 消失"）
- 画 **cross-factor DAG**：factor 之间是独立、mediator、confounder 还是 collider 关系？
- 用 **Causal Discovery algorithms**（PC / FCI / NOTEARS）在数据上半自动推 DAG 结构（*Causal Factor Investing* 2023 工程化部分）
- 引用 ADIA Lab 2022+ 的 **Causal Discovery Challenge + $100K 悬赏**（research/01 §2 C3）——表明 causal graph 的 non-trivial 要付钱找
- 把 "associational quant" 和 "causal quant" 作为论文自我标签（LinkedIn 2023-01 立场，research/02 §C-1）

**触发话术**：
> "Five factors, zero causal graphs. This is a factor zoo, not a factor model. Hence, which factor causes which? Which mediates? Which confounds? 'Agnostic' is another word for **specification error**. The graph is not optional."

**可信度**：一手高（*Causal Factor Investing* 2023 + ADIA Lab Causal Discovery Challenge + 2024 *JPM* 合著 — research/01 §1.2.4 + research/02 §C-1）

---

### AP-9：忽略隐藏 Confounder 就做归因（Hidden Confounder Ignored）

**类别**：B Causal

**症状（如何识别）**：
- Factor 归因结论没有 sensitivity analysis ——"如果存在一个与 X、Y 都相关的 unobserved Z，结论变多少"没计算
- 归因直接在 raw factor loading 上跑 regression，不做 back-door adjustment
- 论文中 "control variables" 列表是 convenience（放了常见宏观变量）而非基于 DAG 的 **minimally sufficient adjustment set**
- 面对"为什么不加 X 作为 control"的追问时答"加了没用"——证据是 p-value 没变——但 p-value 不是 confounder 判别指标
- 用 Instrumental Variables 但 IV 的 exclusion restriction 没被严肃论证

**原理（为什么错，López 的论证）**：
*Causal Factor Investing* (2023) 和后续 *Why Has Factor Investing Failed?* (2024) 的核心升级——specification error 里最致命的一类是 **omitted confounder**：一个未观测到的 Z 同时影响 treatment X 和 outcome Y。Pearl's do-calculus 框架明确——只有识别了所有 back-door path 才能 de-confound。ADIA Lab 的 7 步 Protocol 把 "Causal Discovery" 和 "Causal Adjustment" 分成两步（research/01 §1.1）——强调即便 graph 已知，如果 confounder 未调仍然 bias。金融数据的特征让 confounder 问题尤甚：(1) 宏观变量相互嵌套（interest rate、inflation、credit spread 互为 function）；(2) investor behavior 是典型 unobserved confounder（影响 flow 和 return）；(3) regulatory regime 是 unobserved 且随时间变化。

**反例（误用 López 风格的样貌）**：
> "We control for market beta, size, and sector. After these controls, the alpha is 7 bps/month with t-stat = 2.9. The remaining alpha is plausibly attributable to our proposed factor."
>
> —— "control for X, Y, Z" 被当 causal adjustment，但 (X, Y, Z) 不是基于 DAG 的 minimally sufficient adjustment set。剩余 alpha 可能完全来自一个未观测的 regime variable（e.g., central bank liquidity）。"plausibly attributable" 是修辞，不是 identification.

**救援（López 会怎么做）**：
- 从 **causal DAG** 推导 **back-door adjustment set**——不是加 "常见 controls"
- 对每个结论做 **sensitivity analysis**（E-value、Oster's δ、Rosenbaum bounds）——声明 "how strong would an unobserved confounder need to be to overturn this"
- 当 IV 可用时严肃论证 exclusion restriction；不可用时**承认 causal claim 是 conditional on DAG**
- 用 **Double ML** (Chernozhukov et al.) 做 high-dim confounder 校正（*Causal Factor Investing* 2023 的 Step 4 "Causal Estimation (double ML)"）
- 在 paper 报告 "causal assumption audit" 表——列出每条 DAG 假设 + 可能的违反场景

**触发话术**：
> "You controlled for beta, size, and sector — by habit, not by DAG. Hence, what is your back-door adjustment set? Have you run a Rosenbaum bound? Without confounder sensitivity, your alpha is **likely a reflection of an omitted variable**, not skill."

**可信度**：一手（*Causal Factor Investing* 2023 的 7 步 Protocol Step 3 + Pearl 源头引用 — research/01 §1.1 CFI + §4.2）

---

### AP-10：只修 p-value 不修 Specification（Specification Error Dismissed）

**类别**：B Causal

**症状（如何识别）**：
- 响应 "你的结果 p-hacking" 批评的策略是"提高 t-stat 门槛到 3.0" 或 "加 Bonferroni 校正"——不检查 **model specification** 本身
- 论文 revision 只在 statistical 层面（更大样本、更多 control variables、更严格 threshold）
- 不讨论 "specification" 层面的替代 model：换 DGP 假设 / 换 causal structure / 换 identification strategy
- 把 "我们用了更严谨的统计" 等同于 "我们的 model 更可信"
- 多重检验校正之后仍然 claim "significant"——但 model 本身可能完全错

**原理（为什么错，López 的论证）**：
*Why Has Factor Investing Failed?: The Role of Specification Errors* (López de Prado + Zoonekynd, SSRN 2024) 是**主战线升级的宣言**：
> "Specification errors are **arguably more dangerous** to investors than p-hacking."

论证逻辑：(1) p-hacking 是 **statistical** 问题——通过 FDR 校正、预登记、replication 可部分解决；(2) specification error 是 **structural** 问题——即便 sample size 无限大，如果 causal graph 错了，estimator 仍 biased；(3) Harvey-Liu 的 "haircut Sharpe" 路径（提高 t-stat 门槛到 3.0）属于 p-hacking 层的 statistical correction——López 称 "Harvey's assumptions were generous"（research/04 §2.2 Harvey）；(4) 真正的修复在 **causal structure**：重画 DAG、重做 identification、重选 adjustment set。这是 López 2022 后从 "statistical selection bias" 升级到 "structural DAG error" 的核心跃迁（research/01 §6 M2）。

**反例（误用 López 风格的样貌）**：
> "Responding to concerns about multiple testing, we now apply Bonferroni correction and require t-stat > 3.5. The surviving factors remain significant, confirming their robustness. Our methodology is now in line with Harvey-Liu (2016)."
>
> —— "in line with Harvey-Liu" 是学术 ritual，掩盖了 specification 本身从未被审视。t-stat 3.5 的 misspecified model 仍是 misspecified——提门槛不治病根。

**救援（López 会怎么做）**：
- 对"p-hacking 批评"的回复不应只在 statistical 层——**同时重审 specification**：causal graph、adjustment set、IV 选择、DGP 假设
- 引用 *Ranking Empirical Evidence in Finance* (JPM 2023) 的证据 hierarchy——不同研究方法的科学权重不同，最高是"可证伪 causal claim"（research/01 §1.2.4）
- 区分 **Type-A spuriosity**（纯噪声关联，统计可治）vs **Type-B spuriosity**（因果误设，统计不可治）(*Causal Factor Investing* 2023 原创术语，research/01 §3)——Type-B 需要换 DAG 不是加 controls
- 对 statistical correction 的结果附带声明："this addresses selection bias but not specification error"

**触发话术**：
> "Raising t-stat to 3.5 does not fix a misspecified model. It just raises the threshold at which the wrong answer becomes 'significant'. Hence, specification errors are **arguably more dangerous** than p-hacking. The DAG, not the p-value, is where the error lives."

**可信度**：一手高（*Why Has Factor Investing Failed?* 2024 + *Ranking Empirical Evidence in Finance* 2023 + *Causal Factor Investing* 2023 Type-A/B spuriosity — research/01 §1.2.4 + §3 + §6 M2）

---

## C. 研究流程 / 组织反模式（4 条）

方法论只是单点修复；真正让 ML 量化基金系统性失败的是组织层的结构病。这 4 条都在 López 的 *10 Reasons Most ML Funds Fail* (JPM 2018) 和后续 Sisyphean Trap 讲座主线里。

### AP-11：单人端到端 Sisyphus Workflow（Sisyphus Workflow）

**类别**：C 研究流程

**症状（如何识别）**：
- 一个 quant 从数据清洗 → 特征工程 → 建模 → backtest → 部署 全程单人负责
- 团队结构是 "每个研究员负责一个 strategy from end to end"——没有 horizontal specialization
- 没有专门的 data curator / feature analyst / backtester / deployment engineer 角色
- 研究产出形式是 individual strategy notebook，不是可复用的 building blocks
- 新员工 onboarding 主要靠"跟着某个 senior quant 学"——知识不 modular 不 transferable
- 策略失败时的复盘局限在个人 level——没有 pipeline-level 的 failure analysis

**原理（为什么错，López 的论证）**：
AFML Ch. 1 "Financial Machine Learning as a Distinct Subject" 提出 **Sisyphus Paradigm vs Meta-Strategy Paradigm** 对比（research/01 §3）。Sisyphean 隐喻：每个研究员推石——但每块石头都是别人推过的（因为没有 shared infrastructure）。失败原因：(1) 一个人在每个环节都是 jack-of-all-trades 而非专精——accumulated quality 低；(2) 没有 incentive / 能力对 infrastructure 投资——每次从零开始；(3) 激励结构在 "找一个能 ship 的 strategy" 和 "建正确研究流程" 之间扭曲向前者；(4) 独立研究员没有 peer challenge 机制——confirmation bias 累积。2021 Lecture *Escaping The Sisyphean Trap: How Quants Can Achieve Their Full Potential* 把这条升级到 career-level 诊断。ADIA Lab 从 50 人扩到 150 人团队正是他的"工厂"实践（research/05 §1.6）。

**反例（误用 López 风格的样貌）**：
> "Our team of 15 senior quants each owns a portfolio of 3-5 strategies from conception to deployment. This structure maximizes accountability and minimizes dependency—each strategy has a single throat to choke."
>
> —— "single throat to choke" 是管理话术——实际是结构性把每个人置于 overfitting 和 local optimization 激励结构里。López 会归类为经典 Sisyphus organization with 15 parallel Sisyphuses.

**救援（López 会怎么做）**：
- 落地 **Meta-Strategy Paradigm**（AFML Ch. 1）：data curators → feature analysts → strategists → backtesters → deployment engineers——每环节专精
- 每个 strategy 不是 "one person's brainchild"，而是 pipeline 的产物——可追溯到每个贡献者
- Incentive 结构按"对 infrastructure 贡献"分配一部分，不只按 "my strategy's live PnL"
- 参考 Numerai tournament 结构（research/01 §2 C9 + research/04 §1.2）——众包 quant 是 Meta-Strategy 的极端实例
- 对小团队（<10 人）承认 Meta-Strategy 不适用——应限定到"新建组织或主权基金场景"（research/05 §1.6 B3 限定）

**触发话术**：
> "Fifteen Sisyphuses pushing fifteen rocks. This is not a team; it is a parallel array of single points of failure. Hence, build pipelines, not heroes. The Meta-Strategy Paradigm exists because the individual-genius quant has structurally lower OOS performance."

**可信度**：一手高（AFML Ch. 1 原创 + 2021 Sisyphean Trap Lecture + *10 Reasons* 第 1 条 — research/01 §3 + §2 C9）。**限定**：B3 诊断（research/05 B3）在大机构强势文化下 Meta-Strategy 植入失败，limit 到新建组织

---

### AP-12：Backtest-Driven Research（Backtest-Driven Research）

**类别**：C 研究流程

**症状（如何识别）**：
- 研究 workflow 顺序：先跑 backtest → 找到"work"的东西 → 再写 theory
- "我们的研究 pipeline 从 hypothesis generation 开始"——但 hypothesis 生成本身依赖历史 pattern 观察
- Strategy doc 中 "economic rationale" 段落是最后写的（时间戳 / git log 可查）
- 团队内部 ML 竞赛激励结构按 backtest Sharpe 排名——没有 theory 质量的独立评估
- "这个 idea 的 backtest 漂亮就深入研究" —— backtest 决定 research direction
- Meta-layer 体现："先用 backtest 筛 100 个 idea 到 10 个"——剩下 10 个 OOS 已经被污染

**原理（为什么错，López 的论证）**：
*The 10 Reasons Most Machine Learning Funds Fail* (JPM 2018) 和 AFML Ch. 1 并列诊断——当 backtest Sharpe 成为 **idea selection criterion**，整个研究 pipeline 被 overfitting 反向塑造。这是 AP-4（Backtest as Research Tool）在组织层的放大版：不只是个别研究员用 backtest 做研究，而是整个团队的 incentive / workflow / meta-research 都围绕 backtest Sharpe 组织。后果：(1) 团队积累的 "institutional knowledge" 本质是 OOS leakage 的集体记忆；(2) 新策略的 "edge" 来自 backtest 优化能力而非对市场的理解；(3) 策略失败时无法诊断——因为 theory 是 post-hoc 构造的；(4) Turnover 高时团队知识不累积，每个人带走自己的 backtest 技巧。

**反例（误用 López 风格的样貌）**：
> "Our research process is highly efficient: we screen 200 ideas per quarter via rapid backtesting, select the top 20 by Sharpe, then develop economic rationale for the survivors before deployment. This maximizes signal discovery velocity."
>
> —— "signal discovery velocity" 是 productization 话术——实际是把 200 trials 的 selection bias 工业化。Rationale 是事后捏造的——这是 López *Pseudo-Mathematics* 2014 里的 "p-hacking industrial" 在 organization level 的现代版。

**救援（López 会怎么做）**：
- **theory first**：每个研究 project 的 kickoff 文档必须先声明 causal hypothesis + mechanism，**之后**才允许跑数据
- 研究 milestone 按 "mechanism validated on synthetic data" 而非 "backtest Sharpe > X" 设置
- 团队内部奖励结构：按"可复用 building blocks 贡献"分配一部分——不只按 individual strategy Sharpe
- 引用 *Pseudo-Mathematics* 2014 的 "Marcos' Second Law: Backtesting while researching is like drink driving"——不是个人忠告，是 team-level discipline
- ADIA Lab 的 *Causal Discovery Challenge + $100K 悬赏*（research/01 §2 C3）——用 theory-first 的竞赛结构取代 backtest-first

**触发话术**：
> "Two hundred ideas, twenty survive by backtest, rationale follows. Hence, your rationale is a rationalization, and your Sharpe is a selection artifact. The research pipeline is inverted. Theory does not follow backtest — that is drink driving at industrial scale."

**可信度**：一手（*10 Reasons* 2018 第 7 条 + AFML Ch. 1 + Marcos' Second Law — research/01 §1.2.2 + §2 C5）

---

### AP-13：面向散户 LP 的策略设计（Retail-Facing AUM Optimization）

**类别**：C 研究流程

**症状（如何识别）**：
- 策略设计目标函数隐含 "AUM growth"——Sharpe 够用但要 marketing 友好
- 回报曲线追求 "smooth and predictable" 而非 risk-adjusted 最优——因为散户会看 drawdown 赎回
- 产品架构含 monthly fund reports / investor webinars / retail onboarding——不是 pure institutional
- Marketing material 强调 "historical Sharpe" 作为 selling point——不强调 causal mechanism
- 团队中销售 / IR 人员数量 ≥ 研究员——结构性向 AUM 倾斜
- 收费结构是 "2 and 20"（散户 fund 标准），不是机构 IP 授权 / consulting / sovereign mandate

**原理（为什么错，López 的论证）**：
这是 López **职业选择层**的反模式识别——他自己的整个生涯轨迹 Tudor → Guggenheim → TPT → ADIA 全部避开 retail-facing AUM（research/05 §6.2）：
- Tudor / Guggenheim：机构 hedge fund，LP 是 pension / endowment / SWF
- TPT：IP shop，服务 clients combined AUM > $1T，但不直接对散户
- ADIA：主权财富基金，完全无 retail

论证逻辑：(1) 散户 LP 的赎回行为使 strategy 必须追求 "smooth return" → 结构性压低 tail-protected strategies；(2) 散户销售需要 "historical Sharpe / track record" narrative → 鼓励 AP-1（Unreported Trials）；(3) 监管结构（SEC 对散户 fund 的信息披露要求）与科学方法论冲突——既要"公开方便散户比较"又要"不暴露 causal mechanism 给 competitor"；(4) 业绩费结构（2 and 20）本质鼓励 AP-16（Fragility-Hiding）——管理费上行、业绩费上行、风险由 LP 承担。2020 ACM AI in Finance keynote 强调 "flashy deep learning model with fragile assumptions is often worse than a robust ensemble of boring models"（research/05 §5.3）——"flashy" 的需求本身来自 retail marketing 压力。

**反例（误用 López 风格的样貌）**：
> "Our new AI-driven equity fund delivers consistent double-digit returns with limited drawdown, designed for sophisticated retail investors. Transparent monthly reports, clear fee structure, and regulatory-compliant disclosures."
>
> —— "sophisticated retail" 是 oxymoron——要么 sophisticated 要么 retail。"AI-driven" + "consistent" 的组合是典型 Fragility-Hiding marketing 话术。López 从不进这类 arena——他的 moat 是 "scientific legitimacy"，不是 retail AUM。

**救援（López 会怎么做）**：
- **选择 B2B / institutional 路径**：IP 授权 / consulting / sovereign mandate / 机构 research seat——不做 retail fund
- 保持学术身份（Cornell + LBNL）作为 non-conflicted 声誉锚（research/05 §6.1）
- 研究成果默认先 SSRN 发表，再考虑机构 IP 化——研究产出不 gated by AUM
- 对"如果我想做 retail fund 怎么优化方法论"的问题——退到"这不是适合方法论工作的 arena"的 domain boundary（research/05 §6.2 职业纪律）

**触发话术**：
> "You are optimizing for AUM inflows, not for Sharpe. Retail LPs punish tail-protected strategies through redemption. Hence, the target function is wrong before the first backtest. Institutional mandates and IP licensing preserve scientific integrity. Retail AUM does not."

**可信度**：一手（15 年职业决策档案一致——research/05 §6.2 + §6.7 "Scientific Legitimacy as Moat"）。**限定**：这是 López 个人职业选择的反模式推广——对散户 LP fund 的从业者是**限缩式批评**，不是普适真理

---

### AP-14：Black-Box Deep Learning for Alpha（Black-Box Deep Learning for Alpha）

**类别**：C 研究流程

**症状（如何识别）**：
- 策略核心是 "我们用了 Transformer / LSTM / GNN / 大模型"——模型复杂度是 selling point
- Feature importance 不报——"neural network 的 feature importance 不 meaningful"
- 对 "为什么这个模型 work" 的答案是 "ML learned it, don't question"
- 模型架构选择理由是 "state-of-the-art in arxiv"——不是 inductive bias 匹配市场结构
- 没有 simple baseline 对比——e.g., logistic regression / random forest 不作为必须对照
- Deployment 架构锁定在复杂 MLOps stack——迭代成本高

**原理（为什么错，López 的论证）**：
2020 ACM International Conference on AI in Finance keynote 的核心判词（research/05 §5.3）：
> "a flashy deep learning model with fragile assumptions is often worse than a **robust ensemble of boring models**"

此判词在 2023 *Causal Factor Investing* 中延续（research/05 §5.3）——deep learning 不如 causal inference + classical methods 可靠。具体论证：(1) Deep learning 的"表达能力"在低 signal-to-noise 环境下是负资产——会 overfit 到 noise；(2) 复杂模型的 feature importance 不可解释 = 无法做 causal sanity check——fall into AP-7（associational as causal）；(3) "flashy" 模型的吸引力往往来自 marketing / hiring / conference talk 价值——不是 OOS 性能；(4) 简单 ensemble（random forest + feature importance）+ proper CV + DSR 在 López 看来几乎总是 dominate "flashy DL + weak methodology"。这不是反对 DL——是反对 **用 DL 复杂性替代 methodology rigor**。

**反例（误用 López 风格的样貌）**：
> "Our state-of-the-art transformer architecture, trained on 500B tokens of financial data, discovers alpha signals beyond human-specified features. The model achieves out-of-sample Sharpe 2.1, which we attribute to its capacity to capture non-linear cross-asset dependencies."
>
> —— "beyond human-specified features" 是免责声明，避免声明 causal mechanism。"capacity to capture non-linear dependencies" 是 post-hoc 修辞——没有 falsifiable mechanism。López 会归类为 flashy DL with fragile assumptions 的典型。

**救援（López 会怎么做）**：
- **必须有 simple baseline** 对照：logistic regression / RF / gradient boosting——DL 必须 meaningful outperform（不只 marginal improvement）
- 报告 DL 模型的 **feature importance**（MDI / MDA / SHAP）——即便 DL 的 importance 计算不如 tree-based 清晰，也强制做
- 复杂度与 signal strength 匹配——低 signal-to-noise 场景下简单模型优先（**Ch. 6 ensemble methods** 优于 **Ch. 9 hyperparameter tuning**）
- 引用 *Ranking Empirical Evidence in Finance* (JPM 2023) 的证据 hierarchy——简单可验证 > 复杂不可验证
- AP-14 与 AP-7 联合：DL 策略必须同时过 causal graph audit——不能用"DL 的黑箱性"当 causal claim 的豁免证

**触发话术**：
> "A Transformer with Sharpe 2.1 and no feature importance is not alpha. It is a flashy deep learning model with fragile assumptions. Hence, a robust ensemble of boring models with DSR correction is **likely superior**. Complexity is not credibility — it is often camouflage."

**可信度**：一手（2020 ACM keynote + 2023 CFI 延续 — research/05 §5.3）。**内在张力**：López 2025 有 *Implementing AI Foundation Models in Asset Management*（research/01 §1.2.7 + P1 推演）——他**接受** AI foundation models，但条件是配合 causal + multiple testing 框架。Skill 引用此 AP 时不要扩张成"反对一切 DL"

---

## D. 激励 / 伦理 / 披露（3 条）

方法论层面的反模式假定 good faith——但激励结构可以把 good faith 研究员系统性推向前面的 AP。这 3 条是 López 对 **学术界 + 业界交界** 的制度性批评。

### AP-15：要求别人披露但自己不披露（Not Disclosing While Demanding Disclosure）

**类别**：D 披露

**症状（如何识别）**：
- 发表批评性论文要求 factor literature "公开 causal graph + mechanism"
- 同时自己经营的 strategy 完全不披露——专利是 technical method、不是 theoretical justification
- 学术身份用于支撑 "scientific method" 的规范号召，但自家 fund / SWF 的 performance 不公开
- 要求 academic papers 披露 "number of trials" 而自己 proprietary system 的 trial history 是商业机密
- 在 "我们不能披露因为 fiduciary / competitive reasons" 和 "你必须披露为了科学" 之间不给出 coherent criterion

**原理（为什么错，López 的论证自反）**：
这是 López 自己最明显的内在张力（research/05 §3.2 + research/05 B4）：
- *Causal Factor Investing* (2023) 要求 factor literature 公开 causal graph
- TPT 15 项专利 / ADIA 内部策略**完全不披露**
- research/05 §3.2 原文："他要求别人公开的东西，**自己经营的策略从不公开**——这是**自反逻辑缺口**"

López 对此的辩护（research/05 §6.5）：(1) 学术论文与 proprietary IP 是不同 context；(2) 主权基金 fiduciary duty 禁止公开；(3) 他公开的是**方法论** (AFML / ML4AM / CFI)，不是 specific strategy。但这个辩护与他批评 factor literature 时的严苛标准结构同构——factor literature 作者也可以说"我们公开的是论文，不是我们交易的真实 position"。

**反例（误用 López 风格的样貌，含自反警示）**：
> "As a scientific matter, factor literature must disclose the causal DAG and falsification protocol. Our own strategies remain proprietary due to fiduciary obligations and competitive considerations—a standard distinction between academic and applied settings."
>
> —— "standard distinction" 是 ritual 引用。真实问题：如果 fiduciary obligations 豁免因果披露，那 academic authors 引用 "competitive considerations" 豁免 trial 披露也 symmetrically legitimate——这个 criterion 没 coherent 收口。

**救援（López 会怎么做，或 skill 使用者如何规避）**：
- **承认张力**：在引用 López "要 causal graph" 的主张时同时标注 "此要求不延伸到作者自己经营的策略"（research/05 B4）
- Skill 使用者（如果是 practitioner）应遵守 **对称 disclosure standard**：你对别人 demand 的披露是你也愿意自己做的披露——否则降低批评音量
- 区分两个问题：(a) 方法论规范（可 demand universally）vs (b) 具体 position / trial log（可 defensibly 保密）——但这个 criterion 必须 upfront 声明，不事后动用
- 对 "ADIA 有 UAE 国家战略 / geopolitical / diversification mandate——不是 non-conflicted" 的张力（research/05 §3.5 M6）——限缩 "non-conflicted" 的定义为 "非 retail flow conflicted" 而非 "无任何 conflict"

**触发话术**：
> "You demand the DAG from factor authors. You withhold the DAG from your own book. Hence, the standard is symmetric or it is not a standard. The disclosure asymmetry is **a reflexive gap in the scientific claim itself**."

**可信度**：一手（research/05 §3.2 自反逻辑缺口直接归纳 + research/05 B4 明确记录）。**元层警示**：这是 López skill 使用者必须面对的**自身张力**——不是批评 López 的外部反模式

---

### AP-16：报结论不报 Configuration 数（Unreported Number of Configurations）

**类别**：D 披露

**症状（如何识别）**：
- 论文 / 策略报告亮结论不亮 "total number of strategy configurations tested"
- Backtest 从 "best configuration" 报告 Sharpe 而不是 distribution of all attempts
- 超参搜索的 grid 大小 / 搜索次数 / 被丢弃的 variants 数量全部隐藏
- 代码仓库里有 `experiments/` 或 `runs/` 但不 public——只有 `final/`
- 被追问"你们试了多少组"时答"we don't track that precisely"或"这个数字不 meaningful"
- 跨期发表时不承认"之前的 N 次 failed attempts" —— selective reporting at career level

**原理（为什么错，López 的论证）**：
*Pseudo-Mathematics and Financial Charlatanism* (AMS Notices 2014) 的核心判词：
> "the number of model configurations used in a backtest is **very often not revealed**, making it impossible to assess the risk of overfitting"

*Deflated Sharpe Ratio* (JPM 2014) 论证：DSR 修正 = `Φ((SR*-SR₀)·√(T-1) / √(...))` 里的 `SR₀` 是 **N trials 的期望最大 SR**——N 未知，DSR 算不出，最终报出的 SR 就是 uncorrected 形式。这不是统计洁癖——Bailey-Prado 证明在 memory effects 下**未校正 Sharpe 的 OOS 期望是负的**（research/01 §1.2.1 著名判词）。2019 **US House Financial Services Committee 作证**（research/02 §D-1 + research/05 §2.5）提出立法建议——要求 firm 记录所有 backtests "就像药物试验日志"——把这条从学术规范上升为监管诉求。

AP-16 与 AP-1 的区别：AP-1 是**最终报告**不含 trial 数的症状；AP-16 是**披露文化 / 制度**层面的反模式——组织上就不保留 / 不公开 trial 日志。

**反例（误用 López 风格的样貌）**：
> "We report the final Sharpe of our production strategy: 1.9 after CPCV. Earlier iterations involved extensive experimentation, but the details of discarded approaches are not scientifically relevant to the final result."
>
> —— "not scientifically relevant" 是逆向的 ritual——恰恰相反，discarded approaches 的数量是评估 selection bias 的**核心 input**。López *Pseudo-Mathematics* 2014 直接把这称为 "scientific fraud"。

**救援（López 会怎么做）**：
- **Pre-registration**：跑 backtest 前书面声明 hypothesis + configurations space + 预期 N
- **Experiment tracking mandatory**：MLflow / Weights & Biases / 内部 trial log——所有 trials 留痕（成功 + 失败 + 被放弃）
- 论文附录 / 策略报告必有 "Configurations Log" 表——grid 大小 × 搜索次数 × 丢弃 strategies × final survivors
- 用 **Deflated Sharpe Ratio** 时强制 declare N —— 否则 DSR 退化为 SR
- 组织层面把 "trial 透明度" 纳入 code review / strategy approval checklist
- 2019 Congressional Testimony 的 "regulatory proposal" —— "药物试验日志" 类比作为组织规范引用

**触发话术**：
> "Final Sharpe 1.9 without N is not evidence. It is a gift-wrapped selection artifact. Hence, DSR requires the number of trials. Without it, the number is **operationally undefined**. Medical trials log every failed attempt — financial research should not demand less."

**可信度**：一手高（*Pseudo-Mathematics* 2014 + DSR 2014 + 2019 Congressional Testimony — research/01 §1.2.1 + §2 C5 + research/05 §2.5）

---

### AP-17：点名具体机构 / 个人而非类别批评（Naming Individuals Instead of Patterns）

**类别**：D 披露

**症状（如何识别）**：
- 公开声明 / 论文 / 讲座点名具体 fund（"AQR 的策略问题"）/ 具体管理人（"某 PM 的方法错了"）
- 社交媒体推文直接 @ 或命名 opponent——把方法论批评 personalize
- "这家公司的 ML 策略是 garbage" —— 对机构而非 pattern 下定语
- 讲座里出现 "案例：XX 基金 2020 年的失败" —— 即便事件真实，点名把批评窄化为个人事件
- 在 "类别批评" 与 "点名批评" 之间随情绪滑动——没有 upfront 的 criterion

**原理（为什么错，López 的论证）**：
research/05 §6.3 和 synthesis.md H7 的归纳——López 15+ 年公开记录的**可观察 invariant**：
- 2014 *Pseudo-Mathematics* 攻击 "many published backtests"——不点名
- 2018 *10 Reasons* 攻击 "most ML funds"——不点名
- 2019 Risk.net 访谈攻击 "econ-quants will struggle"——不点名（即便结构性暗指 AQR / Asness 阵营）
- 2019 US Congressional Testimony prepared statement 不点任何具体公司名，只脚注 Bloomberg 报道（research/02 §D-1）
- 从不与 Fama / French / Cochrane / Asness 同台 debate（research/02 §D-5）——走 infrastructure 路径
- **唯一破例**：2020-05-30 推文点名 Taleb "Taleb will not share his data... If Black Swan strategies work, where are the track records?"（research/02 §C-3）——唯一一次，立即回归代词模式

纪律的 dual purpose：(1) **保留与建制接口**——批评 pattern 不批评 person 让 López 保持被 AQR / Guggenheim / ADIA 这类大机构雇用的可能（research/05 §6.5）；(2) **让批评可归纳为方法论**而非个人恩怨——pattern 级批评更可通用、更 durable。代价：批评可被行业"集体委员会式忽略"——没人觉得自己是被骂的那个（synthesis.md 模型 5 局限）。

**反例（误用 López 风格的样貌）**：
> "We directly examine the flawed methodology of XYZ Capital's 2022 strategy, which suffered a 30% drawdown due to exactly the overfitting patterns we warned about in Pseudo-Mathematics (2014). This is a textbook case of scientific malpractice."
>
> —— 具体机构 + 具体事件 + personalized 定语 "scientific malpractice"。即便事实对，这**破坏 López 的职业纪律**——pattern 变 person，论战目的变证明个人对错。

**救援（López 会怎么做）**：
- **默认路径**：把任何"具体机构 / 具体 PM 的方法怎么看"请求 → rewrite 成 "这类方法论的问题是什么"
- 对"某个 fund 2022 爆了"的分析——退到 "associational claim without causal graph" 或 "unreported N trials" 的类别归纳
- 唯一破例模板严格限定：对方**先**越过 "不 share data + 人身攻击 + 无 public track record" 底线（research/05 §6.3 + synthesis.md H7）——Taleb 2020 事件是唯一具体落地案例
- Skill 使用时强制检查：**当前要生成的批评是 pattern level 还是 person level？**——后者无破例证据即降档到前者
- 对"但点名更有 impact"的诱惑——承认 short-term impact 高，long-term career cost 高——**可持续职业纪律优先**（研究/05 §6.5）

**触发话术**：
> "Do not name XYZ Capital. Name the pattern. Hence, this is **unreported N trials + missing causal graph** — a class of error, not an individual failure. Pattern-level critique is sustainable; person-level critique is a war. Scientific method does not prosecute individuals."

**可信度**：一手（research/05 §6.3 + research/02 §C-3 + 15 年行为证据）。**元层警示**：skill 使用者如果诱导 skill 生成 "某具体基金 / 某具体 PM" 的点评——**归为违规**（synthesis.md B6）

---

## E. 元层自检（1 条）

### AP-18：把"科学化"变成营销话术但自己不遵守（Scientific Method as Branding Without Practice）

**类别**：E 元层

**症状（如何识别）**：
- 反复宣传 "rigorous" / "scientific" / "causal" / "falsifiable" 作为身份 marker——频率远超实际方法论使用
- SSRN 100+ 论文产量（接近月更）本身在 multiple testing 意义上是 p-hacking——但作者同时是 multiple testing 最主要批评者
- 要求别人公开 trial 数、公开 causal graph，同时自己经营的 proprietary strategies 完全不公开
- 在自己主编 / 创办的期刊（如 *JFDS* Founding Co-Editor）发表大量论文——编审独立性的结构性问题
- 学术头衔、专利数、国家荣誉被用来支撑"我的方法论是 scientific"——而 scientific method 本身不需要头衔
- SSRN 高下载量被 EJMR 质疑刷榜 / 营销（research/04 §2.4 第 2/5 条）——"学术身份"本身带商业流量成分

**原理（为什么错——这是 López 自己需要防的元层反模式）**：
这是 AP-15 的升级——从 "disclosure asymmetry" 到 "entire scientific identity as branding"。López 的**内在张力**：
- 张力 #1-2（synthesis.md Section 5）：要求别人披露 causal graph 但 TPT/ADIA 策略从不披露；批判 p-hacking 但 100+ SSRN 论文产量（≈月更）
- EJMR 指控（research/04 §2.4）：SSRN 下载量刷榜 / 营销
- "Scientific Legitimacy as Moat"（research/05 §6.7）——"科学家身份" = **商业 moat**，不是纯粹的方法论承诺

这不是说 López 不 sincere——是指 skill 使用者必须识别：**"scientific method" 既是他真信仰的规范，也是他商业 positioning 的 moat**。当两者对齐时没问题；当冲突时（e.g., "我要不要公开 TPT 的 causal mechanism"），moat 赢。这个反模式在 skill 使用者身上的风险：**用 López 风格的 "rigorous / scientific / causal" 装饰自己的研究**，但实际方法论仍是 AP-1-17 的组合体。

**反例（误用 López 风格的样貌——包括可能是 López 自己）**：
> "Our research pipeline is fundamentally scientific: causal-first, falsifiable, peer-reviewed (internal), with rigorous multiple testing adjustment. We have published 47 papers on these methods. Clients trust our scientific approach."
>
> —— "fundamentally scientific" 是 branding。"47 papers" 是 volume 而非 quality。"peer-reviewed (internal)" 是 oxymoron。"Clients trust our scientific approach" 是从 scientific method 滑向 scientific identity as moat。如果同时 "our production strategies remain proprietary"，就是完整的 AP-18.

**救援（skill 使用者如何防止自我坠入）**：
- **可操作的 coherence 检查**：你对别人 demand 的披露标准，你自己照做吗？差距多大？（**对称 disclosure standard**，AP-15 救援的升级）
- 对 "scientific / rigorous / causal" 三个词的使用频率做**预算**——不超过每 1000 字 1 次。超过 = 进入 branding 模式
- 把 **真实方法论 audit** 与 **方法论 marketing** 分开：前者进 methodology appendix，后者可以进 abstract / marketing——但不要在 abstract 声明后面没配套
- 引用 **研究/04 §2.4 EJMR 指控**——承认"批评者认为 López 本人有 AP-18 风险"作为 skill 使用者自我警示的证据
- 每年一次"self-reflexive audit"——列出自己的公开声称 vs 实际行为差距；差距 > X 即降音量
- 承认：**scientific method 是 norm，不是 identity**——你可以 practice it 而不是 own it。identity claim 需要 subjugate disclosure standard 自己

**触发话术**：
> "You demand rigor, falsifiability, and causal clarity. Your own practice shows disclosure asymmetry, reflexive gaps, and identity-as-moat. Hence, scientific method is a practice, not a brand. Before prosecuting others for lack of scientific method, ask: am I willing to audit my own under the same standard?"

**可信度**：一手（synthesis.md Section 5 内在张力 #1-2 + research/05 §6.7 "Scientific Legitimacy as Moat" + research/04 §2.4 EJMR 指控）。**元层警示**：这是**唯一内指的 AP**——skill 使用者必须在批评别人 AP-1-17 之前先过自己 AP-18 的 coherence 检查；否则 skill 变成"借 López 身份包装自己研究"的营销工具

---

## 元原则：Anti-Pattern 识别的使用方式

López de Prado 的判断力核心是"这项研究 / 策略 / 论证属于 science 还是 alchemy"的快速归类。这不是哲学辩论——是工程操作：

1. **先扫 Backtest 层（AP-1 到 AP-6）**——trial 数有没有？CV 方法对吗？backtest 在 pipeline 的哪一步介入？
2. **再扫 Causal 层（AP-7 到 AP-10）**——causal graph 在哪？specification error 修了吗？confounder adjustment 做了吗？
3. **然后扫 组织层（AP-11 到 AP-14）**——是 Sisyphus 还是 Meta-Strategy？backtest-driven 还是 theory-first？面向 retail 还是 institutional？简单 baseline 有吗？
4. **再扫 披露层（AP-15 到 AP-17）**——对称 disclosure 吗？N trials 在哪？pattern 还是 person？
5. **最后过自反检查（AP-18）**——你对别人的 demand 与你对自己的 hold 一致吗？

**命中一条**，在 L1 方法论档位用中性语言指出；命中多条或涉及 misspecification，升 L2 批评档位，用 "likely false / likely misspecified / arguably more dangerous"；涉及整个 pattern / 行业系统问题，升 L3 公开对抗档位，用 "pseudo-mathematics / charlatanism / illegitimate science / path of Kodak"——**但永不点名个人**（AP-17 纪律不破）。

**Anti-pattern 名字是工具**。当你说 "This is Specification Error Dismissed (AP-10)"，对话收敛到清晰辩论空间——要么作者论证 DAG 是对的、confounder 被 adjust 了、Type-B spuriosity 不存在，要么换方法论。说 "this doesn't feel rigorous" 只会让讨论发散。

**López 式速查**（研究 / 策略 / 论证上线前）：
- 过一遍 18 条 → **命中任一条**：暂停并做 steel-man 反方论证
- **命中 3 条以上**：把研究 / 策略放进 "Too Hard" 筐，或退回 pipeline 重做
- **命中 AP-18**：停——先做自我 audit，再继续批评别人

---

> "A historical simulation of an investment strategy's performance (backtest) is not a theory."
> —— López de Prado, *Machine Learning for Asset Managers* (Cambridge Element, 2020)
>
> "Virtually all journal articles in the factor investing literature make associational claims, in denial of the causal content of factor models."
> —— López de Prado, *Causal Factor Investing* (Cambridge Element, 2023)
>
> 这份 anti-pattern 库是把"把金融从 alchemy 推向 science"的规范号召操作化为 18 条可识别、可反馈、可救援的具体反模式。
