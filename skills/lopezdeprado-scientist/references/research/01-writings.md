# Marcos López de Prado — 系统性著作调研

调研截止：2026-04-21。本文档只覆盖**系统性长文本**（书、SSRN 论文、期刊文章、讲座系列），不碰 LinkedIn 碎片（除非用作立场确认的二级佐证）。

信源黑名单已执行：零知乎、零公众号、零 CSDN、零百度百科。

---

## 0. 作者定位速记（用于后续章节的参照坐标）

- **当前身份**（2026-04）：Global Head of Quantitative R&D, Abu Dhabi Investment Authority (ADIA) + founding board member, ADIA Lab + Professor of Practice, Cornell ORIE + Research Fellow, Lawrence Berkeley National Lab。
  - 来源：https://www.quantresearch.org/Vita.htm（一手，他本人维护的 CV 页）
- **职业轨迹**：Tudor Investment Corp（2008-2013, Head of Global Quant Research）→ Guggenheim Partners（2013-2018, Senior Managing Director, 管 $13B, IR 2.3）→ AQR（Partner, first Head of Machine Learning）→ True Positive Technologies（创始人，服务 clients combined AUM > $1T）→ ADIA（current）。
  - 来源：https://www.truepositive.com/leadership；https://www.linkedin.com/in/lopezdeprado/（一手）
- **学历**：双博士——Financial Econometrics（2003, Universidad Complutense de Madrid）+ Mathematical Finance（2011, 同校）+ 博后 Harvard + Cornell。
  - 来源：https://www.quantresearch.org/Vita.htm（一手）
- **奖项**：Quant of the Year 两次（2019 研究员、2021 买方）+ Bernstein Fabozzi / Jacobs Levy Award（2024）+ 西班牙 Royal Order of Civil Merit Knight Officer（2024）+ National Award for Academic Excellence, Spain（1999）。
  - 来源：https://www.quantresearch.org/Vita.htm（一手）
- **SSRN 排名**：Economics Top-10 most-read authors；Lecture 1/10 单篇下载 17,787 次（2026-04 统计）。
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3270329（一手 SSRN 计数）

---

## 1. 著作清单

### 1.1 三本核心书

#### 《Advances in Financial Machine Learning》（AFML, Wiley, 2018）

- **ISBN**：978-1-119-48208-6，372 页，24 章，分 5 部分（Part I-V）
- **来源**：https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086（一手出版商页）；https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3104847（一手 SSRN 的 Ch. 1 全文）
- **完整章节结构**（综合自 Cornell ORIE 5256 讲义 + SSRN Ch.1 全文 + reasonabledeviations.com 第三方笔记，可信度：骨架一手 + 细节二手）：

  **Part I - Data Analysis**
  - Ch. 1 Financial Machine Learning as a Distinct Subject（含 Sisyphus Paradigm vs Meta-Strategy Paradigm）
  - Ch. 2 Financial Data Structures（tick/volume/dollar bars + imbalance bars + ETF trick）
  - Ch. 3 Labeling（Triple-Barrier Method + Meta-Labeling）
  - Ch. 4 Sample Weights（label uniqueness + sequential bootstrap + time-decay）
  - Ch. 5 Fractionally Differentiated Features

  **Part II - Modelling**
  - Ch. 6 Ensemble Methods（bagging, RF, boosting）
  - Ch. 7 Cross-Validation in Finance（Purged K-Fold CV + Embargo）
  - Ch. 8 Feature Importance（MDI, MDA, SFI）
  - Ch. 9 Hyper-Parameter Tuning with CV

  **Part III - Backtesting**
  - Ch. 10 Bet Sizing
  - Ch. 11 The Dangers of Backtesting（"seven sins" 列表）
  - Ch. 12 Backtesting through Cross-Validation（Combinatorial Purged CV / CPCV）
  - Ch. 13 Backtesting on Synthetic Data（Ornstein-Uhlenbeck）
  - Ch. 14 Backtest Statistics（含 Deflated Sharpe Ratio）
  - Ch. 15 Understanding Strategy Risk
  - Ch. 16 Machine Learning Asset Allocation（HRP）

  **Part IV - Useful Financial Features**
  - Ch. 17 Structural Breaks（CUSUM, Chow-type DF, SADF）
  - Ch. 18 Entropy Features（Shannon, mutual info, Lempel-Ziv, PIN）
  - Ch. 19 Microstructural Features（Kyle's λ, Amihud's λ, VPIN）

  **Part V - High-Performance Computing Recipes**
  - Ch. 20-22 HPC, multiprocessing（内容精简，3 章）

  - 来源：https://reasonabledeviations.com/notes/adv_fin_ml/（二手，但作者公开 GitHub + 笔记对照原书）；https://www.oreilly.com/library/view/advances-in-financial/9781119482086/（一手，O'Reilly 托管的目录）

- **核心定位（一手自述）**："establishes a new scientific discipline that blends ML, statistics, and financial microstructure into a systematic research methodology"（出版商摘要）
- **市场地位**：被业内广泛称"the industry bible"，AQR 内部培训教材，Cornell ORIE 5256 指定用书

#### 《Machine Learning for Asset Managers》（ML4AM, Cambridge Element, 2020）

- **出版**：Cambridge University Press, Elements in Quantitative Finance series，141 页（短小精悍）
- **来源**：https://www.cambridge.org/core/books/machine-learning-for-asset-managers/6D9211305EA2E425D33A9F38D0AE3545（一手）；https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3558728（一手 SSRN Ch.1）
- **核心定位**："seven complex problems or topics where applying new techniques developed by ML specialists will add value"（一手，出版商页）
- **七大主题**（综合自 CFA Institute 书评 + Medium 章节摘要 + gmarti 博客，可信度：二手但三处交叉确认）：
  1. Covariance matrix noise（Marcenko-Pastur theorem 去噪）
  2. Detoning covariance（剥离 market component）
  3. Distance matrices and entropy（mutual information, variation of information 替代 correlation）
  4. Financial labeling（Fixed-Horizon / Triple-Barrier / **Trend-Scanning** / Meta-labeling——此书首次系统引入 Trend-Scanning）
  5. Feature importance replacing p-values（MDI, MDA）
  6. Portfolio optimization（HRP + **Nested Clustered Optimization / NCO** 首次系统化，基于 2019 SSRN paper 3469961）
  7. Overfitting testing（Deflated Sharpe, CPCV, Monte Carlo, FWER）
  - 来源：https://rpc.cfainstitute.org/blogs/enterprising-investor/2021/book-review-machine-learning-for-asset-managers（二手, CFA 官方书评）；https://medium.com/moataz-book-summary/book-summary-machine-learning-for-asset-managers-f8e2bd4315e0（二手）
- **与 AFML 的关系**：ML4AM 不是 AFML 的缩写版而是**互补版**——更偏资产管理经理视角（covariance, portfolio），AFML 更偏策略研究员视角（labeling, backtesting）。NCO 和 Trend-Scanning 是 ML4AM 独家首次系统化。
- **关键主张**（一手）："**A historical simulation of an investment strategy's performance (backtest) is not a theory**"——直接把 backtest 从理论地位踢到证据地位。

#### 《Causal Factor Investing》（CFI, Cambridge Element, 2023）

- **出版**：Cambridge University Press, Elements in Quantitative Finance, Open Access（免费下载）
- **来源**：https://www.cambridge.org/core/books/causal-factor-investing/9AFE270D7099B787B8FD4F4CBADE0C6E（一手）；https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4205613（一手 SSRN 预印版 "Can Factor Investing Become Scientific?"）；https://www.quantresearch.org/QF_Causal_Factor_Investing.pdf（一手，quantresearch 镜像）
- **结构**：Preamble + 3 主章（Causal Inference / Econometrics / Factor Investing）——他本人描述为 "the three chapters on causal inference, econometrics and factor investing"（一手摘要）
- **最激进的论点**（一手直引）：
  - "Virtually all journal articles in the factor investing literature make **associational claims**, in denial of the causal content of factor models."
  - "Authors do not identify the causal graph consistent with the observed phenomenon, they justify their chosen model specification in terms of correlations, and they do not propose experiments for falsifying causal mechanisms."
  - "factor investing models are likely **misspecified**, and the estimates of risk premia are biased"
  - 来源：Cambridge Element 摘要 + SSRN 预印版摘要（都是一手）
- **副标题** "Can Factor Investing Become Scientific?" 本身就是定罪——暗示当前 factor investing 不是科学
- **7 步 Protocol for Causal Factor Investing**（从 ADIA Lab 页面）：
  1. Variable Selection (ML)
  2. Causal Discovery (algorithms + domain knowledge)
  3. Causal Adjustment (do-calculus)
  4. Causal Estimation (double ML)
  5. Portfolio Construction
  6. Backtesting (respecting causal structure)
  7. Multiple Testing Adjustments (FDR)
  - 来源：https://www.adialab.ae/research-series/a-protocol-for-causal-factor-investing（一手, ADIA Lab 官方）

#### 其他书（辅助位，不是焦点但要建档）

- 《Asset Management: Tools and Issues》（World Scientific, 2020，与 Fabozzi + Stoyanov 合著）
- 《High Frequency Trading: New Realities for Traders, Markets and Regulators》（Risk Books, 2013，与 Easley + O'Hara 编辑）
- 《Advances in High Frequency Strategies》（Complutense University, 2011，博士论文书籍化）
- 《Invertir en Hedge Funds》（Díaz de Santos, 2003，第一本博士论文书籍化，西班牙语，偏历史兴趣）
  - 来源：https://www.quantresearch.org/Publications.htm（一手）

### 1.2 核心 SSRN 论文（按主题分组，按可信度和引用量排序）

#### 1.2.1 Backtest Overfitting 主线（与 Bailey 合作）

- **"Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance"**（Bailey, Borwein, López de Prado, Zhu）
  - 发表：*Notices of the American Mathematical Society* 61(5), May 2014, pp. 458-471
  - 来源：https://www.ams.org/notices/201405/rnoti-p458.pdf（一手 AMS 版）；https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2308659（一手 SSRN）
  - 核心主张（一手 abstract）："high simulated performance is easily achievable after backtesting a relatively small number of alternative strategy configurations, a practice denoted **backtest overfitting**"
  - 著名判词："Under memory effects, backtest overfitting leads to **negative expected returns out-of-sample, rather than zero performance**"——这是量化界最常被引的一句之一
  - 可信度：一手（同行评议 AMS 期刊）

- **"The Probability of Backtest Overfitting"** (PBO)
  - 作者：Bailey, Borwein, López de Prado, Zhu
  - 发表：*Journal of Computational Finance* 20(4), 2017, pp. 39-70
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253（一手）
  - 贡献：引入 PBO 指标——衡量"样本内 best strategy 在样本外排名低于中位数"的概率

- **"The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality"**
  - 作者：Bailey, López de Prado
  - 发表：*Journal of Portfolio Management* 40(5), 2014, pp. 94-107
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551（一手）；https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf（一手 PDF）

- **"Deflating the Sharpe Ratio"**（单作者短文, 2014）
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2465675（一手）

- **"The False Strategy Theorem: A Financial Application of Experimental Mathematics"**
  - 作者：López de Prado, Bailey
  - 发表：*American Mathematical Monthly* 128(9), 2021, pp. 825-831
  - 来源：https://www.quantresearch.org/Publications.htm（一手列表）
  - 核心：给出 "unskilled strategies 在 N 次试验下的期望最大 Sharpe" 的解析解

- **"Detection of False Investment Strategies Using Unsupervised Learning"**
  - 作者：López de Prado, Lewis
  - 发表：*Quantitative Finance* 19(9), 2019, pp. 1555-1565
  - 来源：https://www.quantresearch.org/Publications.htm（一手）

#### 1.2.2 ML Funds 失败诊断

- **"The 10 Reasons Most Machine Learning Funds Fail"**
  - 发表：*Journal of Portfolio Management* 44(6), 2018, pp. 120-133
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3104816（一手 SSRN）；https://www.garp.org/white-paper/the-10-reasons-most-machine-learning-funds-fail（GARP 白皮书版）
  - ⚠️ 具体 10 条原文抓取失败（PDF binary 无法解析，Garp 页也只有摘要），需补一手。**Hudson Thames 把它浓缩到 7 条**版本（mlfinlab docs），但原版 10 条。
  - 从讲义和大纲可确认的至少几条主题：Sisyphus paradigm（个人英雄主义）/ integer differentiation 破坏平稳性 / IID CV 被直接套用到时序 / 回测当研究工具 / backtest 不上报 trial 数 / 信号-噪声比低被忽视
  - 可信度：主题确认（多源交叉）；具体条目编号未一手验证

- **"Beyond Econometrics: A Roadmap Towards Financial Machine Learning"**
  - 发表：*Journal of Financial Data Science* 4(3), 2022, pp. 1-21
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3365282（一手 SSRN）

- **"A Data Science Solution to the Multiple-Testing Crisis in Financial Research"**
  - 发表：*Journal of Financial Data Science* 1(1), 2019, pp. 99-110
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3177057（一手）
  - 核心主张（一手，二手转述）："**Most discoveries in empirical finance are false, as a consequence of selection bias under multiple testing**"——极强的宣言

#### 1.2.3 Portfolio Optimization 系列

- **"Building Diversified Portfolios that Outperform Out-Of-Sample"**（HRP 首发论文）
  - 发表：*Journal of Portfolio Management* 42(4), 2016, pp. 59-69
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678（一手）
  - 核心：HRP 解决 CLA 三大问题——instability, concentration, underperformance；关键性能宣告："**HRP can compute a portfolio on an ill-degenerated or even a singular covariance matrix**"

- **"A Robust Estimator of the Efficient Frontier"**（NCO 首发）
  - 2019, SSRN
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3469961（一手）

- **"The Myth of Diversification: Risk Factors versus Asset Classes"**（用户指定）
  - 发表：*Journal of Portfolio Management*
  - 来源：https://www.proquest.com/openview/c59073200478235524d6aeda3fd9972d/（二手, ProQuest 托管）
  - ⚠️ 未获取全文 abstract，暂记为"存在 + 主题为 risk factors 对 asset classes 的 dominance 讨论"——**信息缺口，待补**

- **"Estimation of Theory-Implied Correlation Matrices"**（TIC, 2019）
  - 来源：https://www.quantresearch.org/Publications.htm（一手）

#### 1.2.4 Causal Factor Investing 系列（2022+，最新战线）

- **"Causal Factor Investing: Can Factor Investing Become Scientific?"**（2022, SSRN 预印 → 2023 Cambridge Element）
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4205613（一手）
- **"Why Has Factor Investing Failed?: The Role of Specification Errors"**（与 Zoonekynd, 2024）
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4697929（一手）
  - 关键宣告（二手转述，一手待补）："specification errors arguably more dangerous to investors than p-hacking"
- **"The Case for Causal Factor Investing"**（与 Lipton, Zoonekynd）
  - 发表：*Journal of Portfolio Management* 51(1), 2024, pp. 146-158
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4774522（一手）
- **"Causality and Factor Investing: A Primer"**（与 Zoonekynd, 2025, CFA Institute Research Foundation）
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5277078（一手）；https://rpc.cfainstitute.org/research/foundation/2025/causality-factor-investing（一手 CFA 出版）
- **"Ranking Empirical Evidence in Finance"**（2023, 独著）
  - 发表：*Journal of Portfolio Management* 49(9), 2023, pp. 10-29
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4425855（一手）
  - 核心：提出金融证据的**hierarchy**——不同研究方法的科学权重不同，最高是"可证伪 causal claim"
- **"Causal Factor Analysis is a Necessary Condition for Investment Efficiency"**（2025, 与 Lipton + Zoonekynd）
  - 发表：*Journal of Portfolio Management* 52(1), 2025, pp. 7-19
- **"Where are the Factors in Factor Investing?"**（2023, *JPM* 49(5): 6-20）

#### 1.2.5 Sharpe Ratio 系列（长跑主线）

- **"How to Use the Sharpe Ratio"**（与 Lipton + Zoonekynd, 2026 *JPM* 52(6): 6-50，最新版）
  - 来源：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5520741（一手）
- **"Confidence and Power of the Sharpe Ratio under Multiple Testing"**（2022, *JPM* 49(1): 39-46）
- **"A Closed-Form Solution for Sharpe Ratio Inference under GARCH Returns"**（2026, 与 Porcu, Zoonekynd, Engle）

#### 1.2.6 Market Microstructure（与 Easley + O'Hara 长期合作）

- **"The Microstructure of the Flash Crash"**（2011, *JPM* 37(2): 118-128）——SSRN 上 Finance 领域最常被读论文之一
- **"Flow Toxicity and Liquidity in a High Frequency World"**（2012, *Review of Financial Studies* 25(5): 1457-1493）——VPIN 首发
- **"The Volume Clock: Insights into the High Frequency Paradigm"**（2012, *JPM* 39(1): 19-29）
- **"Discerning Information From Trade Data"**（2016, *Journal of Financial Economics* 120(2): 269-286）
- **"Microstructure in the Machine Age"**（2021, *Review of Financial Studies* 34(7): 3316-3363, 与 Easley + Zhang）

#### 1.2.7 Course Materials（Cornell ORIE 5256, 高下载量）

10 讲 Lecture 1-10，2018-2019，全部在 SSRN：
- Lecture 1: The Pitfalls of Econometric Analysis（17,787 下载）
- Lecture 2: Financial Applications of ML
- Lecture 3: Data Analysis（13,549 下载）
- Lecture 4: Modelling（10,193 下载）
- Lecture 5-6: Backtesting I & II
- Lecture 7: ML Portfolio Construction
- Lecture 8: Useful Financial Features
- Lecture 9: High-Performance Computing
- Lecture 10: The 7 Reasons Most ML Funds Fail（6,510 下载）
- Numerai's Tournament (2019)
- 来源：https://www.quantresearch.org/Lectures.htm（一手）

---

## 2. 反复出现 ≥3 次的核心主张（即"真信念"）

按出现频次从高到低。每条主张列出**至少 3 个独立来源**作为信念证据。

### C1. 大部分金融实证发现是假的（"Most discoveries in empirical finance are false"）

- 出处 1：*A Data Science Solution to the Multiple-Testing Crisis*（2019, JFDS）—— abstract 原文
- 出处 2：*Pseudo-Mathematics and Financial Charlatanism*（2014, AMS Notices）—— "a large proportion of backtests published in academic journals may be misleading"
- 出处 3：*Causal Factor Investing*（2023, Cambridge）—— "virtually all journal articles ... make associational claims"
- 出处 4：LinkedIn 2022 热帖 7004376644073209856（59 评论）—— "a collection of anecdotal empirical evidence, undermined by p-hacking, backtest overfitting, and reproducibility problems"
- 可信度：**一手高浓度**，跨 12 年稳定

### C2. 金融研究应当是科学（scientific method），不是 alchemy

- 出处 1：*Advances in Financial Machine Learning* 书名副标题 + 出版商宣传 "establishes a new scientific discipline"
- 出处 2：*Causal Factor Investing* 副标题直问 "Can Factor Investing Become Scientific?"
- 出处 3：*Ranking Empirical Evidence in Finance*（2023）—— 建立"证据科学权重等级"
- 出处 4：Lecture 2015 "**Illegitimate Science**: Why Most Empirical Discoveries in Finance Are Likely Wrong, and What Can Be Done About It"（quantresearch.org Lectures）
- 出处 5：2025 讲座 "Financial Machine Learning: An Engineering Problem" —— 把 FML 重定位为"工程问题"
- 可信度：**一手高浓度**，书名/副标题/讲座标题级别的高强度承诺

### C3. Factor Zoo 是 p-hacking 的工业化产物；关联 ≠ 因果

- 出处 1：*Causal Factor Investing*（2023）整本书主论点
- 出处 2：*The Case for Causal Factor Investing*（2024, JPM）
- 出处 3：*Why Has Factor Investing Failed?*（2024, Zoonekynd）—— "specification errors arguably more dangerous than p-hacking"（这一条**进化了论点**：不只是 p-hacking，更本质是 specification error 即因果图错误）
- 出处 4：*Where are the Factors in Factor Investing?*（2023, JPM）
- 出处 5：ADIA Lab 10 万美元 causal inference 悬赏（行为层面证据，一手 LinkedIn）
- 可信度：**一手高浓度**，2022+ 成为首要战线

### C4. Cross-validation 在金融时序里不能直接套 IID 方法

- 出处 1：AFML Ch. 7（Purged K-Fold + Embargo）
- 出处 2：AFML Ch. 12（CPCV）
- 出处 3：ML4AM overfitting 章
- 出处 4：Lecture 1/10 "The Pitfalls of Econometric Analysis"
- 可信度：**一手**，贯穿所有教材和讲座

### C5. Backtest 不是理论，不是研究工具；每个 backtest 必须报 trial 数

- 出处 1："Backtesting while researching is like drink driving"（AFML, 被 reasonabledeviations 标为 "Marcos' Second Law"）
- 出处 2："Every backtest must be reported with all trials involved"（"Marcos' Third Law"）
- 出处 3：*Pseudo-Mathematics* 2014 —— "the number of model configurations used in a backtest is very often not revealed"
- 出处 4：*Deflated Sharpe Ratio* 2014 —— "most important piece of information missing ... is the number of trials attempted"
- 出处 5：ML4AM —— "a backtest is not a theory"
- 可信度：**一手高浓度**，跨 10 年稳定

### C6. ML Funds 失败有系统性原因（非随机）

- 出处 1：*The 10 Reasons Most Machine Learning Funds Fail*（2018, JPM）
- 出处 2：Lecture 10 "The 7 Reasons Most ML Funds Fail"（2018 版）
- 出处 3：2019 Lecture "The 7 Reasons Most Econometric Investments Fail"（**同构论点扩展到传统 econometric 基金**）
- 出处 4：AFML Ch. 1 "The Main Reason Financial Machine Learning Projects Usually Fail"（即 Sisyphus paradigm）
- 可信度：**一手**，主题数字从 7→10 说明他在迭代扩展

### C7. Triple-Barrier + Meta-Labeling 是 ML 金融落地的正确起点

- 出处 1：AFML Ch. 3 原创章节
- 出处 2：ML4AM 再次展开 + 加入 Trend-Scanning
- 出处 3：Lecture 3/10 "Data Analysis"
- 出处 4：Numerai 系列 SSRN
- 可信度：**一手**

### C8. Fractional Differentiation 解决 stationarity-memory tradeoff

- 出处 1：AFML Ch. 5 原创章节
- 出处 2：2021 Springer 论文 "Fractional differentiation and its use in machine learning"（*Int. J. Advances in Engineering Sciences and Applied Mathematics*）
- 出处 3：AFML 内部实证 "across 87 of the most liquid futures worldwide, stationarity was achieved with d < 0.6"
- 可信度：**一手**

### C9. Sisyphus paradigm（个人英雄量化员）→ Meta-Strategy paradigm（生产线化分工）

- 出处 1：AFML Ch. 1（首发）
- 出处 2：2021 Lecture "Escaping The Sisyphean Trap: How Quants Can Achieve Their Full Potential"
- 出处 3：LinkedIn 多次引用
- 可信度：**一手**，是他的组织论观点

---

## 3. 自创术语库（逐一解释 + 首发出处）

| 术语 | 定义（一手简化） | 首发出处 | 可信度 |
|---|---|---|---|
| **Triple-Barrier Method** | 对每笔假想仓位设三条 barrier：上 profit-take / 下 stop-loss / 右 time expiry。label = 最先触发的 barrier 方向（+1/-1/0）。对标 fixed-horizon labeling 的升级——"accounts for changing volatility" | AFML Ch. 3, 2018 | 一手 |
| **Meta-Labeling** | 二级 ML 模型学"主模型信号是否应该下注 + 下多大"。主模型管方向（side），meta 模型管仓位（size，含"不下注"=0）。经典 claimed gain：mean-reversion strategy 准确率从 17% → 63%（Hudson Thames 复现） | AFML Ch. 3, 2018 | 一手 + 二手复现 |
| **Fractional Differentiation** | 对价格时序取实数阶 d∈(0,1) 的差分（而非 0=价格 / 1=return 两档），使序列平稳同时保留最多 memory。基础来自 Hosking (1981)，但他是首次引入金融 ML | AFML Ch. 5, 2018 | 一手应用 + 二手（Hosking 理论源头） |
| **Purged K-Fold CV** | 从训练集移除"label horizon 与测试集 label 重叠"的样本，消除 look-ahead leakage | AFML Ch. 7, 2018 | 一手原创 |
| **Embargo** | Purged KFold 之上再加一个时间 buffer，阻断 serial correlation 造成的信息泄露 | AFML Ch. 7, 2018 | 一手原创 |
| **Combinatorial Purged Cross-Validation (CPCV)** | 把时序切 N 组，每次测 k 组（k<N），所有 C(N,k) 组合跑一遍，得到 path distribution 而非单一 OOS 估计。同时 purge + embargo | AFML Ch. 12, 2018 | 一手原创 |
| **Probability of Backtest Overfitting (PBO)** | 分析框架——衡量"样本内 best strategy 在样本外排名跌到中位数以下"的概率。越高越 overfit | Bailey+Borwein+Prado+Zhu, *J. Computational Finance* 2017 | 一手原创（四人合作） |
| **Deflated Sharpe Ratio (DSR)** | 在 PSR 基础上把基准 SR 替换成"N 次 unskilled trials 的期望最大 SR"，校正 selection bias。公式用 Φ((SR*-SR₀)·√(T-1) / √(1-γ₃·SR₀+(γ₄-1)/4·SR₀²)) | Bailey+Prado, *JPM* 2014 | 一手原创 |
| **Probabilistic Sharpe Ratio (PSR)** | "真实 SR 超过给定阈值的概率"，考虑样本长度 + 前 4 阶矩（skew + kurtosis） | Bailey+Prado, 2012 | 一手原创 |
| **Minimum Track Record Length (MinTRL)** | 给定置信度 + 阈值，确证策略非假所需的最短样本长度。年化 SR=0.95 需约 3 年日收益 | Bailey+Prado, 2012 | 一手原创 |
| **Minimum Backtest Length (MinBTL)** | 给定 N 次 trials，避免 overfitting 所需的最短 backtest 长度 | *Pseudo-Mathematics* 2014 | 一手原创 |
| **False Strategy Theorem** | unskilled strategies 在 N 次试验下期望最大 SR 的解析解：SR₀ = √V[SR] · [(1-γ)Φ⁻¹(1-1/N) + γΦ⁻¹(1-1/(Ne))]，其中 γ≈0.5772（Euler-Mascheroni） | López de Prado + Bailey, *American Mathematical Monthly* 2021 | 一手原创 |
| **Haircut Sharpe Ratio** | ⚠️ **不是他自创**——是 Harvey + Liu (2014, 2015) 提出的。但他长期与 DSR 并列讨论，AFML Ch. 14 做了系统对比：**DSR 数据密集 / HSR 基于 econometrics 分布假设**。属于他纳入讨论体系但非 attribution | Harvey + Liu, 2014-2015 | 二手（Prado 的是 DSR，不是 HSR） |
| **Hierarchical Risk Parity (HRP)** | 用分层聚类替代协方差矩阵求逆的 portfolio 构建法。三大优势：不要求矩阵可逆、对病态矩阵稳健、OOS 方差低于 CLA 即便 CLA 专为最小方差设计 | López de Prado, *JPM* 2016 | 一手原创 |
| **Nested Clustered Optimization (NCO)** | 在 HRP 之上加嵌套：先聚类，每类内部 optimizer 算内权，然后把每类当"单一资产"再 optimizer 算外权。分解 Markowitz 诅咒 | López de Prado, 2019 SSRN 3469961 | 一手原创 |
| **Trend-Scanning Labels** | 不设固定 horizon，在 [t, t+L] 窗口内拟合多个回归，选 t-value 最大那个的斜率方向作为 label。捕捉"最统计显著 horizon 的 trend 方向" | ML4AM, 2020 + Lecture 3/10 | 一手原创 |
| **Sisyphus Paradigm** | 量化员个体英雄主义——一个人从数据清洗到策略部署端到端负责。隐喻 Sisyphus 推石——每个人都在重复别人做过的事，产出不累积。对立面是 Meta-Strategy Paradigm（生产线化专业分工） | AFML Ch. 1, 2018 | 一手原创 |
| **Meta-Strategy Paradigm** | 量化研究生产线：data curators → feature analysts → strategists → backtesters → deployment。类比制造业流水线，每环节专精，防止 overfitting 激励错位 | AFML Ch. 1, 2018 | 一手原创 |
| **Type-A / Type-B Spuriosity** | Type-A = 纯噪声关联 / Type-B = 因果误设导致的伪关联（如遗漏 confounder、调错 collider）。把 spurious correlation 拆成两个本质不同的病 | *Causal Factor Investing* 2023 + 后续 2024-2025 | 一手原创 |
| **Optimal Significance Level (OSL)** | 根据 Type I/II error 成本结构，解析得出投资决策的最优 significance level（非默认 5%） | quantresearch.org Innovations 页 | 一手原创 |
| **Triple Penance Rule** | drawdown duration 与 recovery time 的 serial correlation 关系的封闭解 | quantresearch.org Innovations | 一手原创 |
| **Probability of Divergence (PoD)** | 检测 manager 实际表现与 track record 偏离的概率 | quantresearch.org Innovations | 一手原创 |
| **Theory-Implied Correlation (TIC)** | 从知识图谱（理论先验）推出的相关矩阵，用于 shrink 经验估计 | 2019 SSRN | 一手原创 |
| **Volume-Synchronized PIN (VPIN)** | 用 volume 时钟替代 clock time 计算 Probability of Informed Trading，对 HFT 时代更合适 | Easley+López de Prado+O'Hara, *RFS* 2012 | 一手原创（三人合作） |
| **Kinetic Component Analysis (KCA)** | 用 Kalman Filter + Taylor 展开做时序降噪 | quantresearch.org Innovations | 一手原创 |

### 独创判断的数量级

从 https://www.quantresearch.org/Innovations.htm（他自己维护的创新清单，一手），列出 50+ 条原创方法，分 6 大类：Portfolio Optimization / Machine Learning / Causal Factor Investing / Strategy Selection & Meta-Research / Market Microstructure / Execution & Trading / Portfolio & Risk Management / Operations Research。

⚠️ 注意：**他本人的自报创新清单**是一手，但"他是不是真正原创者"需与学术文献交叉——HRP 的分层聚类思路、fractional differentiation 的 Hosking 源头、causal inference 的 Pearl 源头，都不是他首创，他的贡献是**把通用工具做金融化 + 配套落地**。

---

## 4. 智识谱系（引用的思想源头）

### 4.1 数学/统计基础

- **David H. Bailey**（Lawrence Berkeley Lab）——最密合作者，19 篇合作论文。backtest overfitting 整条主线是二人共创。数值分析背景。
- **Jonathan M. Borwein**（University of Newcastle, Australia, 已故）——experimental mathematics 奠基人，与 Bailey 长期合作。他把 Prado 带入"experimental mathematics 给金融严谨证明"的范式。
- **Jim (Qiji) Zhu**（Western Michigan University）——变分分析、凸优化。*Pseudo-Mathematics* 2014 合作者。
- 来源：https://www.quantresearch.org/Co-authors.htm（一手）

### 4.2 因果推断

- **Judea Pearl**——*Causal Factor Investing*（2023）索引有 "Pearl" 条目。do-calculus、DAG、counterfactual 三件套被系统引入金融。Prado 明确认同 Pearl 的"association 不等于 causation"纲领。
- **Guido Imbens**（Stanford, 2021 Nobel in Economics）——合作者，共同出现在 2026 ADIA Lab Causal Discovery Challenge 论文（*Journal of Financial Data Science*）
- **Miguel Hernán**（Harvard T.H. Chan）——流行病学因果推断权威，同篇 2026 ADIA Lab Challenge 合作者
- 来源：https://www.quantresearch.org/Publications.htm（一手）+ Cambridge 书介绍 + 二手解读

### 4.3 市场微观结构

- **Maureen O'Hara**（Cornell）——market microstructure 标准教科书作者，10 篇合作论文
- **David Easley**（Cornell）——PIN 模型原作者。Prado 的 VPIN 是对 PIN 的 HFT 时代改造
- **Robert Almgren**（NYU Courant + 前 Morgan Stanley）——市场冲击模型奠基人之一
- 来源：Co-authors.htm（一手）

### 4.4 数学金融与 fintech

- **Peter Carr**（NYU Courant, Morgan Stanley, 2022 已故）——衍生品定价
- **Alexander Lipton**（Hebrew University）——近年频繁合作（Private Equity, Sharpe Ratio Inference, HRP 稳定性），定量金融多面手
- **Frank Fabozzi**（EDHEC）——金融教材大 IP，联合编辑 *Asset Management: Tools and Issues* (2020)
- **Robert F. Engle**（NYU Stern, 2003 Nobel）——GARCH 原创者，Prado 2026 合作 GARCH-Sharpe 论文
- **Riccardo Rebonato**（PIMCO）——固收衍生品

### 4.5 明确反对 / 批判的对象

- **Fama-French 因子模型及其后继**：*Causal Factor Investing* 全书攻击的靶子。不是反对 Fama-French 的统计工作，而是反对"把 association 当 causation"的解释层。
- **整个 "factor zoo" 学派**（Harvey-Liu 做过统计，Hou-Xue-Zhang 做过数据库，Feng-Giglio-Xiu 做过 ML 筛选）——Prado 认同他们指出问题，但反对只做 statistical correction 而不触碰 causal structure。
- **Econometrics 正统**：Lecture 1/10 标题就是 "The Pitfalls of Econometric Analysis"。2019 Lecture "The 7 Reasons Most Econometric Investments Fail" 把矛头直接指向 traditional econometric funds。
- **EMH（有效市场假说）**：⚠️ **他没有像 Shiller / Thaler 那样直接点名 EMH 反对**。他的路径不是"市场无效因此可赚钱"而是"市场研究方法错了因此结论错了"。属于 methodologist 而非 anomaly hunter。这是与行为金融学派的关键差异。
  - 可信度：推断，基于大量论文 abstract 未直接攻击 EMH 但攻击 "factor investing 的 associational 做法"

---

## 5. 推演性观点（一手未覆盖但从原则可推断；需明确标注）

⚠️ 以下观点**不是 Prado 原话**，是基于他一手材料中核心主张的**严格推演**。使用时必须标注"推断"。

### P1. 他对 LLM 在金融应用的立场

- 一手证据：2025 *JPM* "Implementing AI Foundation Models in Asset Management"（与 Francesco Fabozzi）——**接受 AI Foundation Models**
- 推断：鉴于他对"机器学习在金融的首要问题是 overfitting + causal misspecification"的长期立场，他对 LLM 金融应用的态度**大概率是"工程层可用，研究层需配合 causal + multiple testing 框架"**。不会像 Taleb 那样全盘否定。
- 可信度：**推断**，一手 confirmative 是 2025 论文标题但未获取全文

### P2. 他对 EMH 的立场

- 一手证据：未找到直接正/反方声明
- 推断：他的工作**隐含弱版 EMH**——承认 edge 存在但极稀有，需极大 N 去证明。他不会像 Shiller 那样用行为偏差论证市场无效，而是用 methodology 论证"你以为的 edge 多半是假的"。
- 可信度：**推断**

### P3. 他对中国 / A 股 / 新兴市场的立场

- 一手证据：未找到直接论述
- 推断：他的 framework 是**市场中立**的——重点是 data 的 signal-to-noise、非平稳性、IID 假设失效。这些问题在新兴市场**更严重**，但他的方法不做区域特化。
- 可信度：**推断**，零一手证据

### P4. 他对 "Low-Frequency Traders in a High-Frequency World: A Survival Guide"（2012 Lecture）的立场

- 一手证据：2012 Lecture 标题存在（quantresearch.org）
- 推断：结合 VPIN、微观结构合作者群（Easley/O'Hara），他**认为 LFT 在 HFT 时代需要使用 volume clock + 毒性监控**。属于 HFT 防御工具集的推广。
- 可信度：**推断**（标题+邻近论文）

---

## 6. 矛盾与立场演化（直接记录不和稀泥）

### M1. 从 "10 Reasons" 到 "7 Reasons"

- 2018 JPM 正式论文："The **10** Reasons Most ML Funds Fail"
- 2017 / 2018 Lecture 10/10 标题："The **7** Reasons Most ML Funds Fail"
- 2019 Lecture："The **7** Reasons Most **Econometric** Investments Fail"（扩展到非 ML）
- **矛盾评估**：不是真矛盾。是他自己把内容从 10 精简到 7（Hudson Thames mlfinlab 也只做 7 条版本）+ 泛化到 econometric 基金。属于**论点进化**而非自相矛盾。

### M2. 从 "Factor investing 有 p-hacking 问题" 到 "Specification errors 比 p-hacking 更危险"

- 2014 *Pseudo-Mathematics*：主攻 backtest overfitting（p-hacking 同族）
- 2018 *10 Reasons*：仍在 overfitting 主线
- 2022 起 *Causal Factor Investing*：**升级论点**—"specification errors arguably more dangerous than p-hacking"
- 2024 *Why Has Factor Investing Failed?*：定论——即便 p-hacking 修复了，specification error 仍会导致系统性亏损
- **立场演化**：他在 **2022 之后把火力从 statistical（selection bias）升级到 structural（causal DAG）**。早期重点是"N 个 trials 的分布校正"，晚期重点是"因果图错了校正再多也没用"。这是实质性的进化。
- 可信度：一手跨期引用均确认

### M3. HRP 的实际效果

- 2016 HRP 首发：Monte Carlo 实验"HRP delivers lower out-of-sample variance than CLA"
- reasonabledeviations 第三方阅读笔记（二手）："HRP (portfolio optimization technique, **author notes limited practical success**)"——这条如果属实，是重要矛盾证据。
- ⚠️ 但**未在一手文本中验证**"limited practical success"的原话。暂记为**第三方解读可能的矛盾点**，待查 AFML Ch. 16 原文。
- 2025 *Risk Magazine* "Overcoming Markowitz's Instability with Hierarchical Risk Parity"（与 Antonov + Lipton）——继续改进 HRP，说明他**承认原版有局限**但仍在这条线上推进。
- 可信度：**部分矛盾待查原文**

### M4. 对 Harvey-Liu 的定位

- 一手（AFML Ch. 14）：把 DSR 和 Haircut SR 并列讨论，对 Harvey-Liu 工作有**技术层面的尊重**
- 同时：他的 DSR 体系是**直接竞争**对 Harvey-Liu 的解决方案
- 评估：不是矛盾，是**同问题两派解法**——Prado 派 data-intensive, Harvey 派 econometric-assumption-driven。

### M5. 对 Judea Pearl 的引用深度

- 一手：*Causal Factor Investing* 索引有 Pearl
- 但：Prado 没有像 Pearl 本人那样做"3 层级因果阶梯"的完整哲学论证
- 评估：**工程采用 + 哲学跟进**的姿态——Prado 是 Pearl 框架在金融的工程落地者，不是 Pearl 哲学的拓展者。

---

## 7. 信息缺口（本调研未能一手覆盖，供下一轮补充）

1. **《AFML》完整 24 章原文**——本次只通过第三方笔记 + SSRN Ch. 1 交叉确认，Ch. 10 / 15 / 20-22 的内部细节未一手读过。Chapter 16 HRP 是否真有 "limited practical success" 自述需查证。
2. **《ML4AM》141 页完整原文**——只拿到摘要 + 7 主题概览 + Cambridge 介绍，Trend-Scanning 的数学定义和 NCO 的伪代码未一手读过。
3. **《Causal Factor Investing》完整原文**——SSRN 预印 PDF 抓取失败（403）；Cambridge 页 429；只有摘要 + ADIA Lab 的 7 步 protocol + 书评。Type-A / Type-B Spuriosity 的严格定义未一手读过。
4. **"10 Reasons" 原文 10 条列表**——PDF binary 抓取失败，GARP 白皮书页只有摘要，Hudson Thames 7 条版不等于原版 10 条。
5. **"Myth of Diversification" 论文全文**——只确认存在（ProQuest）。
6. **最新 2024-2026 立场**：
   - "How to Use the Sharpe Ratio"（2026 JPM，52(6): 6-50，与 Lipton + Zoonekynd）
   - "Ten Applications of Financial Machine Learning"（2025 JPM 52(2): 71-80）
   - "Financial Machine Learning: An Engineering Problem"（2025 lecture + SSRN）
   - 以上三篇摘要未一手提取
7. **他对 Taleb 的立场**（如果存在）——未找到任何一手文字。两人都在尾部风险 / 多重检验领域工作，但 Prado 的 Deflated Sharpe 是 Gaussian 修正为主，Taleb 的 fat tails 是 Gaussian 根本反对——立场应有冲突，但**一手证据零**。
8. **他对 Renaissance / Simons 的立场**——未找到。
9. **LinkedIn long posts 的系统化调研**——他在 LinkedIn 发长帖频繁（单帖 50+ 评论），按本次调研方向"不碰碎片"原则只抓了 2 条作为立场确认。如需更系统可单独开一篇。

---

## 8. 可信度速览表（供 skill 引用时查核）

| 信息类型 | 可信度等级 | 典型来源 |
|---|---|---|
| 著作存在 + 出版年 + ISBN | **一手 A** | quantresearch.org, 出版商页, SSRN |
| 书籍章节结构 | **一手 A**（Ch. 1）→ **二手 B**（其他章） | SSRN Ch. 1 + 第三方笔记交叉 |
| 自创术语定义（AFML Ch. 1-7） | **一手 A** | SSRN Ch. 1 + 多个第三方复现实现一致 |
| 自创术语定义（AFML Ch. 10-23） | **二手 B** | 第三方笔记（reasonabledeviations 等） |
| 核心主张（跨书重复 ≥3 次） | **一手 A** | 多篇论文 abstract + 讲座标题 |
| 智识谱系（合作者名单） | **一手 A** | quantresearch.org/Co-authors.htm |
| 智识谱系（思想来源 Pearl 等） | **一手 A + 二手 B** | Cambridge 书介绍 + 第三方解读 |
| 立场演化（p-hacking → specification error） | **一手 A** | 跨期论文 abstract 直接对比 |
| 本人 vs 他人创新归属 | **一手 A**（他自己的清单）+ **二手 B**（学术谱系校准） | Innovations.htm + 维基 |
| 推演性观点（EMH / LLM / 中国 / Taleb 对比） | **推断 C** | 零一手，基于原则外推 |

---

## 附：关键 URL 速查

- 一手主站（他本人维护）：https://www.quantresearch.org/
  - Vita：https://www.quantresearch.org/Vita.htm
  - Publications：https://www.quantresearch.org/Publications.htm
  - Lectures：https://www.quantresearch.org/Lectures.htm
  - Innovations：https://www.quantresearch.org/Innovations.htm
  - Co-authors：https://www.quantresearch.org/Co-authors.htm
- SSRN 作者页（需合并搜索）：https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=434076
- LinkedIn（一手立场表达）：https://www.linkedin.com/in/lopezdeprado/
- Cornell ORIE：https://www.orie.cornell.edu/faculty-directory/marcos-lopez-de-prado
- True Positive Technologies：https://www.truepositive.com/leadership
- ADIA Lab：https://www.adialab.ae/
- Cambridge Element 系列：https://www.cambridge.org/core/series/elements-in-quantitative-finance
- AMS Notices 2014 原文：https://www.ams.org/notices/201405/rnoti-p458.pdf
- GARP 10 Reasons 白皮书：https://www.garp.org/white-paper/the-10-reasons-most-machine-learning-funds-fail
- CFA Institute Research Foundation（Causality and Factor Investing Primer, 2025）：https://rpc.cfainstitute.org/research/foundation/2025/causality-factor-investing
