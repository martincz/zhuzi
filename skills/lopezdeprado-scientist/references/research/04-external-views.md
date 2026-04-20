# 04 · 外部世界如何看待 Marcos López de Prado

> **调研范围**：支持者、批评者、中立观察三类视角。信息源优先级：X / Hacker News / Reddit / Amazon / SSRN reply papers / 期刊书评 / EJMR / 量化博客。**黑名单**：知乎、微信公众号、百度。
>
> **重要前置声明**：López de Prado 是**高产、有争议、已获多项行业奖项**的人物。他自我定位是"把金融从炼金术推向科学"的旗手，这个定位在学术界、业界、工程师三类人群中评价差距极大。本文件刻意不稀释批评、不稀释赞扬——让张力保留原状。
>
> **信息截止**：2026-04。
>
> **一个 Taleb 相关的重要诚实声明**：本次调研**未能找到 Nassim Taleb 公开点名 López de Prado 的直接证据**（X 上的推文、访谈、论文均无）。Taleb 骂 ML quant finance / factor investing 是 charlatanism 的言论很多，但目标通常是 Ron Ross、Andrew Lo、Cliff Asness、"financial economists" 整体——不是 López。两人的"交锋"是间接的、结构性的，而非公开互撕。下文相关章节会明确区分"Taleb 对 ML quant 整体的批评（可作为 López 的结构性批评者视角）"与"Taleb 点名 López（未找到证据）"。

---

## 一、支持者视角

### 1.1 学术合作者阵营

#### **David H. Bailey（LBNL / UC Davis 数学家）**
- **关系**：López de Prado 长期合作者。两人合著《Pseudo-Mathematics and Financial Charlatanism》(2014, AMS Notices)、《The Probability of Backtest Overfitting》(2015)、《The Deflated Sharpe Ratio》(2014) 三篇奠基性论文。
- **发声平台**：Mathematical Investor 博客 (mathinvestor.org)
- **年份**：2020-10
- **观点**：Bailey 在博客中**完全复读 López 的立场**——"backtest overfitting and other forms of statistical error" 是 "bane of the finance world"；ML 不是 "plug-and-play" 而是 "requires considerable insight and care"。Bailey 的独立发声与 López 本人发声**高度同构**——这是**信号**：Bailey 不是独立第三方验证者，而是合作者-倡导者。
- **URL**：<https://mathinvestor.org/2020/10/lopez-de-prado-on-machine-learning-in-finance/>
- **批评者视角下的解读**：Bailey 的背书不能作为"外部独立验证"——两人共享研究议程与论文署名，近乎一个学派。

#### **Alex Lipton（前美林 / ADIA Lab / Khalifa University 数学物理学家）**
- **关系**：2024 年起与 López 合著 *Causal Factor Investing* 核心论文 *The Case for Causal Factor Investing* (SSRN 4774522, 2024-03) 与 *Causal Factor Analysis is a Necessary Condition for Investment Efficiency* (SSRN 5131050, 2025-02)。
- **地位**：Lipton 是前卫最受尊重的 quant 之一（前 Bank of America Merrill Lynch 量化分析全球负责人），这个合作**实质性拔高了 López 的学术合法性**——不再是"搞 ML 的工程师型 quant"，而是"与顶级数学金融学者联名的研究者"。
- **URL**：<https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4774522>

### 1.2 实现者 / 开源社区阵营

#### **Hudson & Thames（mlfinlab 维护团队）**
- **平台**：hudsonthames.org 博客 + GitHub mlfinlab 包
- **关系**：他们把自己定位为 López 理论的 **"实现者" (implementers)**——"we could not find a cogent implementation of these ideas in the public domain"，所以把 *Advances in Financial Machine Learning* 整本翻译成 Python 库。
- **态度**：**完全正面、毫无批评**。官方发言里没有任何一条对 López 方法论的质疑。López 本人转推过他们的研究并点赞他们的推文，形成师徒-门徒式的互捧关系。
- **一个间接的信号**：他们的 GitHub issue #295 记录了一个重要 bug——"PurgedKFold: training events can overlap with testing events"，这是对 López 原始算法描述不清的**间接批评**（实现者必须打补丁才能工作），但 Hudson & Thames 从不公开点名这是 López 的问题，而是作为技术 bug 处理。
- **URL**：
  - <https://hudsonthames.org/a-laboratory-for-machine-learning-in-finance/>
  - <https://github.com/hudson-and-thames/mlfinlab/issues/295>
- **emoen 的 GitHub 实现库**也**独立发现一个 bug**："In chapter 4 of *Machine Learning for Asset Managers*, there is a bug in the implementation of the Optimal Number of Clusters (ONC) algorithm in the book."—— <https://github.com/emoen/Machine-Learning-for-Asset-Managers>（这是实现社区对代码质量的第二个独立负面信号）

#### **Numerai 社区 / Richard Craib**
- **关系**：López 是 Numerai 的科学顾问。他多次公开推广 Numerai 的"众包对冲基金 / tournament 式量化研究"模式。
- **Numerai 官方态度**：Numerai CEO Richard Craib 把 López 当核心理论支持者。López 在 SSRN 发布过 "Advances in Financial Machine Learning: Numerai's Tournament" seminar slides (SSRN 3478927)。
- **URL**：<https://forum.numer.ai/t/how-to-solve-the-numerai-tournament-lecture-by-marcos-lopez-de-prado/3982>

#### **Ernie Chan（PredictNow.ai 创始人、*Quantitative Trading* 作者）**
- **关系**：同为 quant educator，风格截然不同（Chan 偏实操、小规模自营；López 偏学术、大机构）。
- **态度**：**间接正面**。Chan 在 LinkedIn 与博客中提及 "Lopez de Prado (head of machine learning at AQR)" 作为领域权威。Chan 特别强调 **metalabeling** 是 "key to successfully applying AI/ML to finance"——这是 López 的原创概念，Chan 公开引用并采纳。
- **平台**：LinkedIn / Medium (PredictNow.ai)
- **URL**：<https://predictnow-ai.medium.com/the-most-overlooked-aspect-of-algorithmic-trading-6b82bc8aaac4>

### 1.3 业界奖项与机构背书

- **Journal of Portfolio Management Quant of the Year 2019** (授予 López)
- **Risk.net Buy-Side Quant of the Year 2021** (与 Alex Lipton 共享)
- **Bernstein Fabozzi / Jacobs Levy "Outstanding Article" Award 2024** (JPM)
- **Spain Royal Order of Civil Merit, Officer's Cross 2024-11** (由 Felipe VI 亲授)
- **ADIA Lab 创始董事成员 + ADIA Global Head of Quantitative R&D**（ADIA 是全球最大主权财富基金之一，AUM 千亿美元级别）
- **Cornell Professor of Practice, College of Engineering**（2015 至今）
- **URL**：
  - <https://www.adialab.ae/bios/professor-marcos-lopez-de-prado>
  - <https://www.ku.ac.ae/spain-honors-khalifa-university-professor-and-adia-lab-scientist-marcos-lopez-de-prado-with-knighthood>

---

## 二、批评者视角

### 2.1 结构性批评者（ML 量化金融整体反对派）—— Taleb 路径

#### **Nassim Nicholas Taleb**
- **⚠️ 诚实声明**：**本次调研未找到 Taleb 公开点名 López de Prado 的直接 X / 访谈 / 论文证据**。Taleb 骂 ML quant / factor investing 是 "pseudoscience" / "IYI" / "charlatanism" 的言论非常多，但点名对象通常是 Andrew Lo、Cliff Asness、Ron Ross、"financial economists" 整体——**不是 López**。两人的冲突是**结构性的、立场对立的**（Taleb 否认金融可以科学化 / López 自认为是把金融科学化的旗手），但**不是公开互撕**。
- **Taleb 对 ML quant 整体的批评**（可作为 López 的结构性反对者视角参考）：
  - "Financial economists were destroying knowledge as we had a far more sophisticated option trading heuristics (that deal with fat tails) before the standardized bad Gaussian statistics of Black Scholes." —— Taleb on X, 2018
  - Taleb 认为正态分布假设是 "a great intellectual fraud"，"there is no fat tailed distribution in which the mean can be properly estimated directly from the sample mean, unless we have orders of magnitude more data than we do"（*Statistical Consequences of Fat Tails*, 2020-2025）
  - Taleb 骂 risk parity 是 "pseudotheoretical and pseudoacademic smoke"——这是**对 Hierarchical Risk Parity (López 的招牌方法之一) 的间接攻击**，因为 HRP 本质是风险平价的层次聚类版本。
  - Taleb 的"IYI (Intellectual Yet Idiot)"标签（*Skin in the Game*, 2018）与 López 的"有大量 SSRN 论文、两个 PhD、顶级机构职位、却推销数学化方法论"画像高度匹配——但 **Taleb 从未点名**。
- **Goodreads 上的一个侧面观察**：评论者 "Terran M." 对 López 的书写了 "a hint of Taleb-style arrogance, wanting to be recognized for being the smartest person in the room"——**讽刺之处**：这里是说 López **模仿 Taleb 的傲慢文风**，不是 Taleb 骂 López。
- **URL**：
  - <https://x.com/nntaleb/status/995999029304623104>
  - <https://arxiv.org/abs/2001.10488>
- **给读者的判断**：要把 Taleb 作为"López 的批评者"引用，必须诚实说明**这是结构性对立，不是公开点名**。任何"Taleb 骂 López 是 charlatan"的声称目前**查无实据**，应当视为误传。

#### **Scott Locklin（Locklin on Science 博客，前 quant）**
- **关系**：写过知名博文 *Nassim Taleb: clown of quantitative finance* (2009)——他是**同时骂 Taleb 和 ML quant 两派**的少数派。
- **对 López 的直接评论**：**未找到**。但 Locklin 的整体立场（"Mountebanks... sell their wares by making the regular jamoke reading his books and essays feel fiendishly intelligent"）对 López 有**高概率的适用性**——Locklin 是会骂 López 的类型，只是公开言论没覆盖到。
- **URL**：<https://scottlocklin.wordpress.com/2009/07/17/nassim-taleb-clown-of-quantitative-finance/>

### 2.2 学术方法论批评者

#### **Torben G. Andersen（Northwestern）+ Oleg Bondarenko（UIC）—— VPIN 论战**
- **平台**：*Journal of Financial Markets*, 2014
- **论文**：
  - *VPIN and the Flash Crash* (2014, JFM 17: 1-46)
  - *Reflecting on the VPIN Dispute* (2014, JFM 17: 53-64)
- **批评要点**（直接针对 López 与 Easley / O'Hara 合作的 VPIN 工作）：
  1. "VPIN is a poor predictor of short-run volatility"
  2. "It did not reach an all-time high prior to, but rather after, the Flash Crash"——直接否定 López 等 2011 JPM 论文 *The Microstructure of the "Flash Crash"* 的核心实证主张
  3. "Its predictive content is due primarily to a mechanical relation with the underlying trading intensity"——指出 VPIN 没有独立信息内容，只是交易强度的代理变量
  4. "Using more standard [trade] classification techniques, VPIN behaves in the exact opposite manner of what is portrayed in the original work"——换标准方法结论反转
- **López 等人的回应** (*VPIN and the Flash Crash: A Comment*, SSRN 2062450, 2012)：声称 Andersen-Bondarenko "attack a methodology we do not advocate, an analysis we never performed, and conclusions we did not draw"——标准的学术 "你误解了我" 防御。
- **Andersen-Bondarenko 的 rejoinder** (*Reflecting on the VPIN Dispute*) 维持原批评。
- **EJMR 圈里的定性**：*"The VPIN papers of O'Hara and Co. have been (IMHO) convincingly shown to be garbage by Andersen"*（Economics Job Market Rumors 帖子, 日期约 2014-2015）——这是**学院派匿名量化人员对 VPIN 的流行判词**。
- **URL**：
  - <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1881731>
  - <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2305905>
  - <https://www.econjobrumors.com/topic/empirical-finance-papers-that-have-been-proven-wrong>（帖子 #6）

#### **Campbell R. Harvey（Duke / NBER / Man Group）—— 方法论竞争**
- **地位**：全球最被引用的 multiple testing / p-hacking 批评者之一。Harvey 与 Liu 的 *Evaluating Trading Strategies* (JPM, 2014) 与 López-Bailey 的 DSR (2014) 几乎同期。
- **与 López 的关系**：**不是公开互怼，而是同议题竞争者**。两人研究同一问题（backtest overfitting / multiple testing），但方法论不同：
  - Harvey 的路线：econometrics / Sharpe ratio 的 multiple testing 修正（haircut）
  - López 的路线：data science / PBO / DSR / CPCV（非参数、基于 combinatorics）
- **López 对 Harvey 的定性**（Risk.net 2019 采访）："Even Harvey's assumptions were generous... if each study represents thousands of unreported backtests rather than one backtest, it is quite unlikely any of these factors is real"——López **间接说 Harvey 太保守**。
- **Harvey 对 López 的公开回应**：**本次调研未找到 Harvey 直接点名 López 的批评**。但 Harvey 的 *Presidential Address: The Scientific Outlook in Financial Economics* (Journal of Finance, 2017) 给出的解决方案是"提高 t-stat 门槛到 3.0"——这是 econometric 路线，与 López 的数据科学路线是**平行而非合作**的关系。
- **给读者的判断**：Harvey 与 López 是 **"竞争的盟友"**——都同意"大部分 published 因子是假的"，但一个走经济学一个走数据科学；**López 认为 Harvey 不够激进**，Harvey 在公开场合没有回骂。
- **URL**：
  - <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2893930>（Harvey Presidential Address）
  - <https://www.risk.net/investing/quant-investing/6993166/some-quant-shops-doomed-to-struggle-lopez-de-prado>（López 评 Harvey）

#### **Cliff Asness（AQR 创始人 CIO）—— 前雇主的 cool 态度**
- **关键历史**：López 2018-09 加入 AQR 任 Head of Machine Learning，**2019-04 离开**——**不到 7 个月**。AQR 买下 López 部分 IP 与 ML 专利申请。接任者是 Yale 金融学教授 Bryan Kelly（明确是学院派金融经济学家，不是 López 的"math-quant" 阵营）。这个接任选择本身就是**对 López 方法论的间接否定**。
- **Asness 的公开立场**：
  - 2017-11 在 Evidence-Based Investing Conference："**Machine learning worries me. We've been handed a H-bomb instead of an A-bomb.**" (Risk.net)
  - 2016-10 对 Bloomberg："**Machine learning won't replace stock-pickers.**"
  - Asness 另有博文 *It's Not Data Mining — Not Even Close* 力挺传统 factor investing，间接回击 López 派对 "factor zoo" 的批评。
- **重要转折**：2025-04 Bloomberg 报道 *AQR Bets on Machine Learning as Asness Becomes AI Believer*——Asness 态度**明显软化**，AQR 转向拥抱 ML。但**拥抱 ML 的旗手是 Bryan Kelly，不是 López**——这进一步说明 AQR 对 López 本人的不感冒延续至今。
- **URL**：
  - <https://www.risk.net/asset-management/5352806/aqrs-cliff-asness-machine-learning-worries-me>
  - <https://www.bloomberg.com/news/articles/2025-04-23/aqr-bets-on-machine-learning-as-cliff-asness-becomes-ai-believer>
  - <https://www.bloomberg.com/news/articles/2019-04-05/aqr-head-of-machine-learning-set-to-leave-after-less-than-a-year>

### 2.3 工程师 / 实操派批评者

#### **Amazon 差评（2018-2021 抽样）**
- **关键差评原话**（多个 Amazon 区域站点均可见）：
  > "While I like a lot of Lopez-Prado's (LP) thinking, **this book is disappointing. Too many self-references, very unclear Python code, and poor explanation of the main ideas.** As a pedagogical experiment it failed fast... Perhaps it serves well as a guide book to the author published paper—but for that I think his website and slides is a MUCH better option."
  > ——评论者**最终表示退货**
- **主要工程师抱怨**：
  1. **Self-references 过多**——López 反复引用自己过去的 SSRN 论文
  2. **Python 代码质量差**——"very unclear"、"poor formatting"
  3. **Synthetic data only**——示例全是合成数据，无真实市场验证
  4. **教学失败**——"failed fast as a pedagogical experiment"
- **URL**：<https://www.amazon.com/Advances-Financial-Machine-Learning-Marcos/dp/1119482089>

#### **Goodreads 中评 (3-4 星)**
- **Mike**：*"Tends to dress simple ideas in unnecessarily complex notation"* + *"Lacks rigorous proofs — arguments are largely intuitive and hand-wavy."*
- **Kyle** (即使给高分)：*"The mathematical notation is more reminiscent of the explicit verbosity of C++ than that of python."*
- **David**：*"Some of the code examples are of poor quality and the text itself is poorly formatted."*
- **Thiago Marzagão**：*The author "conflates data and strategy," introducing problems like leakage that wouldn't exist otherwise.*
- **Fos4242**：*"Quite a lot of pages spent talking about proper backtesting... is more quant trading 101 and less 'advances'."* —— 指 AFML 的"进阶"名不副实
- **Terran M.**：*"A hint of Taleb-style arrogance, wanting to be recognized for being the smartest person in the room."*
- **Max Bolingbroke**：*"Read his free paper on hierarchical risk parity (SSRN 2708678) instead."* —— **直接建议读者跳过整本书**
- **URL**：<https://www.goodreads.com/book/show/36742444>

#### **Robert Carver（AHL 前 PM，*Systematic Trading* 作者，riskyfinance.com）**
- **书评原话**：
  - "Machine learning has been badly used by many practitioners who have mostly repeated the overfitting mistakes of classical statistical learning."——**这是对 ML quant 整体的话**，间接适用于 López 派
  - **对读者的警告**："prospective traders seeking easy path to untold riches will find themselves heavily disheartened"
  - **结论**："Recommended for trained specialists... Such teams will find his book an invaluable reference guide"——**条件式推荐**，明确说这不是给散户/小团队的书
- **URL**：<https://riskyfinance.com/2018/08/advances-in-financial-machine-learning/>

#### **Robert Andrew Martin（Reasonable Deviations 博客，PyPortfolioOpt 作者）**
- **关键实操批评**：
  - 关于 **Hierarchical Risk Parity (HRP)**：*"I have found in practice that HRP portfolios don't seem to be the panacea that Lopez de Prado implies they may be, but nevertheless it is a good technique to have in the toolbox."* —— 这是**有数据支撑的一线实操否定**（Martin 是 PyPortfolioOpt 作者，HRP 是他库里实现的方法之一）
  - 关于 Chapter 10：直接引 López 原话 "terse and highly mathematical"——意味着**连作者都承认写得难读**
  - 关于高性能计算章节：*"not very applicable to small players"*——**预设读者是大机构**
- **URL**：<https://reasonabledeviations.com/notes/adv_fin_ml/>

#### **Francesco Baldisserri（QuantConnect forum）—— Meta-labeling 实测反例**
- **批评标题**：*Why Meta-Labeling Is Not a Silver Bullet*
- **三大技术论证**：
  1. **No information advantage**："To improve the performance of the main ML model the meta model should be able, somehow, to extract more information from the existing features than the main model does"——meta 模型看同样的特征，不应该有额外信息
  2. **Infinite regress problem**："If cascading a meta-model after a main one was actually able to improve the overall trading performance then there is no reason to stop there"
  3. **Position sizing 同样难**："Having a meta model correctly sizing the trades, or signals, is as difficult as having a model generating the right signals"
- **实证结果**：Baldisserri 跑 grid search，"meta-labeling didn't improve average Sharpe ratios compared to single end-to-end models"
- **Baldisserri 的让步**：meta-labeling **只对 discretionary 策略有用**，对 end-to-end ML 模型无用——这是对 López 框架的**领域限缩式否定**。
- **URL**：<https://www.quantconnect.com/forum/discussion/14706/why-meta-labeling-is-not-a-silver-bullet/>

#### **Label concurrency 问题（MQL5 / Medium 工程师社区）**
- **Triple-barrier method 的隐藏问题**（多位工程师独立指出）：
  - "When barriers are applied to financial data, the resulting labels often overlap in time. Multiple observations may be 'active' simultaneously... creating temporal dependencies that violate the fundamental assumption of most machine learning algorithms: that training samples are IID."
  - "The threshold level is usually static and stock returns are known to be heteroskedastic; the volatility changes over time and a fixed threshold value fails to account for this."
  - 一项实测对比："Triple Barrier delivered modest improvements in returns and drawdown control, but risk-adjusted metrics remained weak and offered some stability but not a decisive edge."
- **URL**：<https://www.mql5.com/en/articles/19850>

### 2.4 EJMR 学术圈的匿名负面视角

**Economics Job Market Rumors**（学院派经济学家 / 金融博士生匿名论坛）对 López 的评价**集中在以下几点**：

1. **方法论自相矛盾**：
   > *"This guy thinks he is the first to discover problems with multiple testing and data mining, yet he actively pushes ML methods into finance."*
   > 含义：López 一面骂大家 p-hack，一面自己搞 ML + 100+ SSRN 论文，是 meta-level 的 p-hack。

2. **SSRN 下载数据异常**：
   > *"Papers with a handful of citations have 10k downloads. Amazing!... A semi-technical boring title can never reach 500 downloads even if it is written by Fama."*
   > 暗示 SSRN 下载可能被人为刷高。

3. **AQR 短命任职**：
   > *"Ah yeah, he 'left' AQR, because his stint there was such a big success... *rolls eyes*"* 
   > *"Left after 7 months. Replaced by Bryan Kelly... An even bigger joke than De Prado."*——对 AQR 选择**双重嘲讽**

4. **对 ML 在金融中有效性的整体质疑**：
   > *"what a joke. I always said this stuff doesn't work in finance."*
   > *"The ML/DL stuff only works for specific applications. Finance data is nasty."*

5. **对 SSRN 出版物的"卖东西"质疑**：
   > *"Someone's trying to sell something."*——暗示 López 的高产 SSRN 流水是**商业化推广**而非学术贡献

6. **VPIN 工作被点名**：见 2.2 节 Andersen-Bondarenko

- **URL**：
  - <https://www.econjobrumors.com/topic/marcos-lopez-de-prado-to-aqr>
  - <https://www.econjobrumors.com/topic/the-master-of-robots-has-left-aqr-now-hes-coming-for-wall-street>
  - <https://www.econjobrumors.com/topic/empirical-finance-papers-that-have-been-proven-wrong>
  - <https://www.econjobrumors.com/topic/bryan-kelly-is-leading-the-machine-learning-group-at-aqr>

⚠️ **关于 EJMR 的诚实声明**：EJMR 是匿名论坛，评论真实性与出处无法核验，也有大量人身攻击。**作为学术圈"气氛"的证据有参考价值，作为具体事实断言不应直接引用**。本文件列出是为了呈现"学院派对 López 气氛冷淡"的群像，不是背书每条具体指控。

---

## 三、中立观察 / 矛盾信号

### 3.1 期刊书评（学术界中立专业评价）

#### **Mark S. Rzepczynski, PhD（CFA Institute Enterprising Investor, 2021-04）**
- **评 *Machine Learning for Asset Managers***
- **中立关键词**：
  - **批评**："does not fully answer this big question or serve as a foundational text on the subject"
  - **代码问题**："Code snippets are useful for readers who want to use this research, but at times, the integration of code and text in this book can be confusing."
  - **表扬**："López de Prado has practical insights that most technical writers lack."
- **综合判词**：非初学者用书，targeting "quantitative analysts who want to read about new techniques and to access Python code that will jumpstart their implementation"——**工具书定位，非领域奠基**
- **URL**：<https://rpc.cfainstitute.org/blogs/enterprising-investor/2021/book-review-machine-learning-for-asset-managers>

#### **Quantitative Finance 期刊书评 (Vol 20, No 2, 2020)**
- **综合判词**：*"a research manual for teams, not for individuals"*（引用 López 自述）、"rigorous mathematical presentation and compact code snippets that profit from the rigorous mathematical education and in-depth quantitative finance experience of the reader"
- **隐含前提**：**读者门槛高**——既要数学背景又要金融经验，这是对普通量化工程师的**劝退信号**
- **URL**：<https://www.tandfonline.com/doi/abs/10.1080/14697688.2019.1703030>

### 3.2 生涯路径的矛盾信号

**López 的职业路径本身暗藏故事**：

| 时间 | 事件 | 外部解读 |
|------|------|---------|
| 2011-2018 | Guggenheim QIS 团队负责人，管理 $13B 债券 ML 策略 | 业内公认最成功时期 |
| 2018-09 | 加入 AQR 任 Head of ML，与 Guggenheim 打 IP 所有权官司，庭外和解获得 IP 所有权 | 出来单干的动机 |
| 2019-04 | **离开 AQR，不到 7 个月** | **关键信号**——AQR 为什么容不下他？他为什么不待了？ |
| 2019- | 创办 True Positive Technologies (TPT)，独立 IP 公司 | 自营路线 |
| 2019-2023 | Cornell Professor of Practice + Risk.net Quant of Year 2021 | 学术头衔积累 |
| 2023- | ADIA Lab 创始董事成员 + ADIA Global Head of Quantitative R&D | **被主权财富基金收编**——从独立派变体制派 |

- **外部观察者的解读**：从 Guggenheim → AQR (7 个月) → TPT → ADIA 的轨迹，暗示 **López 不适合在成熟 quant 机构内做 middle management**，更适合作为"首席科学家 / 布道者"角色。他的方法论能在 ADIA（白纸一张的新 lab）落地，但在 AQR（有强势既有文化）落不了地。
- **URL**：
  - <https://www.chicagobusiness.com/finance-banking/former-guggenheim-quant-joins-226-billion-money-manager-aqr>
  - <https://warrenenskat.com/aqr-hires-star-head-of-ml-from-guggenheim-after-lawsuit-and-team-spin-out/>
  - <https://www.bloomberg.com/news/articles/2019-04-05/aqr-head-of-machine-learning-set-to-leave-after-less-than-a-year>

### 3.3 方法论采用率的中立观察

**López 推广的方法论在业界的实际落地情况**：

| 方法 | 采用情况 | 来源 |
|------|---------|------|
| **PBO (Probability of Backtest Overfitting)** | 学术论文偶见引用，业界不广泛 | SSRN 引用统计 |
| **DSR (Deflated Sharpe Ratio)** | Wikipedia 有独立条目、pypbo 等 Python 实现，但主流回测平台（QuantConnect / Quantopian 归档）未默认集成 | <https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio> |
| **CPCV (Combinatorial Purged CV)** | Hudson & Thames mlfinlab 实现；业界批评"computationally expensive as the quantity of parameters grows" | <https://towardsai.net/p/l/the-combinatorial-purged-cross-validation-method> |
| **HRP (Hierarchical Risk Parity)** | PyPortfolioOpt、Riskfolio-Lib 等开源库集成；实操者（如 Martin）报告 "not a panacea" | <https://reasonabledeviations.com/notes/adv_fin_ml/> |
| **Triple-Barrier + Meta-labeling** | mlfinlab 实现；QuantConnect 独立研究者结论 "not a silver bullet" | <https://www.quantconnect.com/forum/discussion/14706/why-meta-labeling-is-not-a-silver-bullet/> |
| **Causal Factor Investing** | 2023 新书，采用率未成型；CFA Institute 出版 primer | <https://rpc.cfainstitute.org/sites/default/files/docs/research-reports/rf_lopezdeprado_causalityprimer_online.pdf> |

**中立判断**：López 的方法论**有影响力但未成为行业标准**——HRP 是最成功的（进入开源投资组合优化库），其他方法仍在"有人用、有人批"状态。与 Fama-French 3/5 因子模型、Markowitz MVO 这种行业共识级的方法论相比差距明显。

---

## 四、共识 vs 分歧总结

### 4.1 学界 / 业界 / 工程师三方评价对比

| 维度 | 学界（金融经济学家） | 业界（大机构 quant / PM） | 工程师（开源社区 / 实操） |
|------|-------------------|------------------------|-----------------------|
| **对 López 身份定位** | "有争议的跨界者"——不完全是经济学家，也不完全是 ML 研究者 | "高产顾问 / 可雇的首席科学家"——ADIA 雇得起他 | "权威作者 / 可学习对象"——但代码和示例需要大量补工作 |
| **对 backtest overfitting 批评** | **一致认同**（Harvey 派与 López 派方法论不同但结论同向） | **普遍认同**但感到是 "quant 101" 级别的提醒（Fos4242 评语） | **完全认同**并积极实现（Hudson & Thames、pypbo） |
| **对 HRP 方法** | **较认可**（引用率高） | **谨慎使用**（Martin："not a panacea") | **集成入开源库但有保留** |
| **对 Meta-labeling / Triple-Barrier** | 引用但不主流 | 少数使用 | **批评较多**——label concurrency、infinite regress、no silver bullet |
| **对 VPIN** | **强烈分歧**——Andersen-Bondarenko 派认为"garbage"；Easley-O'Hara-López 派坚持 | 基本不用 | 基本不实现 |
| **对 Causal Factor Investing (2023-2025)** | **尚无定论**——与 Pearl 的 do-calculus 能否落地金融未决；Cam Harvey 阵营未公开回应 | 观望 | 几乎无开源实现 |
| **对 López 本人职业轨迹** | EJMR 冷嘲（"left AQR 7 months") | 认可 ADIA 头衔 | 中立 |
| **对代码质量** | 不关心 | 不关心 | **负面为主**——不清晰、synthetic-only、多个 bug |
| **对"金融是科学"的宣言** | **反对居多**（Fama 派、Cochrane 派、Taleb 路线） | **中性**（业界不在乎本体论） | **中性**（工程师不参与哲学辩论） |

### 4.2 三方的最大共识

1. **"大部分 published factor 是假的"**——Harvey、López、Taleb、Asness、Cochrane 所有人都同意（但解决方案分歧极大）
2. **"ML 在金融中容易 overfit"**——无人反对
3. **"López 是多产的、有影响力的"**——批评者也承认他高产，只是质疑质量
4. **"Backtesting 本身需要方法论改革"**——共识

### 4.3 三方的最大分歧

1. **"金融能否变成科学"** — López 答是 / Taleb 答否 / Fama 答"已经是" / Asness 答"不该太理想化"
2. **"Causal inference 能否应用于金融"** — López 答是（新书整本论证）/ 大部分学术界持怀疑（数据量不够、工具不成熟）/ 业界观望
3. **"数据科学 vs 计量经济学，哪个是正解"** — López 答数据科学（"math-quants will thrive, econ-quants will struggle") / Asness 答计量经济学 + 少量 ML / Harvey 答改造计量经济学
4. **"López 的 100+ SSRN 论文是学术贡献还是商业化？"** — 支持者答贡献 / EJMR 答卖东西 / 中立观察者答"兼而有之"
5. **"他的工程师实操 usefulness"** — Hudson & Thames 答高 / Amazon 差评答低 / Martin 答"要挑着用"

### 4.4 对 skill 设计者的元层提示

**给 Claude 使用本 skill 时的诚实披露清单**：

1. López 的身份是 **"自我定位为科学旗手、被业界奖项认可、但方法论有技术争议"**——不是"公认大师"也不是"江湖骗子"
2. 引用他的方法（PBO / DSR / CPCV / HRP / Meta-labeling）时，应**同时披露主要的批评点**（如"Martin 报告 HRP 不是万能"、"Baldisserri 报告 meta-labeling 无 ML 优势"）
3. 不要制造"Taleb 和 López 的公开互撕"——**这个互撕不存在**，只存在结构性对立
4. 不要把 "López 骂 factor investing" 等价于 "他否定所有量化研究"——他是**竞争性替代**（用 causal / ML 替代 associational），不是否定
5. 他的"金融科学化"宣言在学术哲学上**争议极大**（Cochrane、Fama 派很可能不认同），skill 引用时应把这看成**一个立场，不是共识**

---

## 五、信息源完整索引

### 5.1 期刊 / 学术
- *Advances in Financial Machine Learning* book review: Financial Markets and Portfolio Management (Springer, 2019) — <https://link.springer.com/article/10.1007/s11408-019-00341-4>
- *Quantitative Finance* book review (Vol 20 No 2, 2020) — <https://www.tandfonline.com/doi/abs/10.1080/14697688.2019.1703030>
- Andersen & Bondarenko *VPIN and the Flash Crash* (JFM, 2014) — <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1881731>
- Andersen & Bondarenko *Reflecting on the VPIN Dispute* (JFM, 2014) — <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2305905>
- Easley, López, O'Hara *VPIN and the Flash Crash: A Comment* — <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2062450>
- Harvey *Presidential Address: The Scientific Outlook in Financial Economics* (Journal of Finance, 2017) — <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2893930>

### 5.2 博客 / Substack / 独立评论
- Reasonable Deviations (Robert Andrew Martin) — <https://reasonabledeviations.com/notes/adv_fin_ml/>
- Risky Finance (Robert Carver) — <https://riskyfinance.com/2018/08/advances-in-financial-machine-learning/>
- Mathematical Investor (David H. Bailey) — <https://mathinvestor.org/2020/10/lopez-de-prado-on-machine-learning-in-finance/>
- Scott Locklin 博客 — <https://scottlocklin.wordpress.com/2009/07/17/nassim-taleb-clown-of-quantitative-finance/>
- CFA Institute Enterprising Investor (Rzepczynski) — <https://rpc.cfainstitute.org/blogs/enterprising-investor/2021/book-review-machine-learning-for-asset-managers>
- Investment Ecosystem — <https://investmentecosystem.com/2023/02/13/causal-factor-investing-created-value-attribution-and-numbers-that-lie/>

### 5.3 论坛 / 社区
- Goodreads book page (AFML) — <https://www.goodreads.com/book/show/36742444>
- Amazon AFML book page — <https://www.amazon.com/Advances-Financial-Machine-Learning-Marcos/dp/1119482089>
- Hacker News AFML Python package thread — <https://news.ycombinator.com/item?id=20871769>
- EJMR (marcos-lopez-de-prado-to-aqr) — <https://www.econjobrumors.com/topic/marcos-lopez-de-prado-to-aqr>
- EJMR (master of robots leaves AQR) — <https://www.econjobrumors.com/topic/the-master-of-robots-has-left-aqr-now-hes-coming-for-wall-street>
- EJMR (empirical finance papers proven wrong) — <https://www.econjobrumors.com/topic/empirical-finance-papers-that-have-been-proven-wrong>
- EJMR (Bryan Kelly leading AQR ML) — <https://www.econjobrumors.com/topic/bryan-kelly-is-leading-the-machine-learning-group-at-aqr>
- QuantConnect forum (Meta-labeling 批评) — <https://www.quantconnect.com/forum/discussion/14706/why-meta-labeling-is-not-a-silver-bullet/>

### 5.4 开源实现 / GitHub
- Hudson & Thames mlfinlab — <https://github.com/hudson-and-thames/mlfinlab>
- mlfinlab Issue #295 (PurgedKFold bug) — <https://github.com/hudson-and-thames/mlfinlab/issues/295>
- emoen Machine-Learning-for-Asset-Managers (ONC bug) — <https://github.com/emoen/Machine-Learning-for-Asset-Managers>
- pypbo — <https://github.com/esvhd/pypbo>

### 5.5 行业新闻 / 采访
- Bloomberg AQR departures (2019-04) — <https://www.bloomberg.com/news/articles/2019-04-05/aqr-head-of-machine-learning-set-to-leave-after-less-than-a-year>
- Bloomberg AQR becomes AI believer (2025-04) — <https://www.bloomberg.com/news/articles/2025-04-23/aqr-bets-on-machine-learning-as-cliff-asness-becomes-ai-believer>
- Risk.net Asness "ML worries me" (2017) — <https://www.risk.net/asset-management/5352806/aqrs-cliff-asness-machine-learning-worries-me>
- Risk.net "Some quant shops doomed" (2019) — <https://www.risk.net/investing/quant-investing/6993166/some-quant-shops-doomed-to-struggle-lopez-de-prado>
- Warren Enskat Group AQR lawsuit article — <https://warrenenskat.com/aqr-hires-star-head-of-ml-from-guggenheim-after-lawsuit-and-team-spin-out/>

### 5.6 Taleb 侧（结构性批评视角，非点名）
- Taleb X on Gaussian fraud — <https://x.com/nntaleb/status/995999029304623104>
- Taleb *Statistical Consequences of Fat Tails* — <https://arxiv.org/abs/2001.10488>

### 5.7 López 本人 / 机构
- López X/Twitter — <https://twitter.com/lopezdeprado>
- Quant Research (López 个人站) — <https://www.quantresearch.org/>
- Cornell profile — <https://www.orie.cornell.edu/faculty-directory/marcos-lopez-de-prado>
- ADIA Lab profile — <https://www.adialab.ae/bios/professor-marcos-lopez-de-prado>
- True Positive Technologies — <https://www.truepositive.com/leadership>

---

**文件终结时间**：2026-04-21。**下次更新触发条件**：
1. Taleb 或 Cam Harvey 公开点名 López（目前**未发生**）
2. *Causal Factor Investing* (2023) 收到主要学术期刊的独立书评
3. López 本人职业路径变动（离开 ADIA、新书等）
4. 业界出现"López 方法论失败 / 成功"的实证大样本研究
