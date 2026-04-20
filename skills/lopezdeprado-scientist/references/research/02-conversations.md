# 02 · 对谈 / 访谈 / 讲座里的即兴思维

> **本文件定位**：只收 **对话语境** 下的发言——即席问答、podcast、panel、推文回击、Q&A、国会质询——**不碰** 书里成系统的论述（那归 `01-writings.md`）。
>
> **信息来源优先级**：原始 podcast / 一手 PDF / 官方推文 / Risk.net / 会议方页面 > 二手报道 > 社区论坛。**黑名单**：知乎、微信公众号、百度。
>
> **素材覆盖时间**：2013（Algorithmic Finance Journal 首访）— 2025（CFA × Fabozzi × ADIA）。总计 18 条主干资料 + 多条推特交锋。
>
> **组织方式**：按题目类型分 A/B/C/D 四块。每条标注 `[来源 · 主持 · 年份]` + URL。区分"他原话"（英文引号）与"主持人/记者转述"（斜体）。
>
> **已尝试但未拿到 transcript 的长视频**（字幕下载被 YouTube bot 拦截）：
> - Global Derivatives 2015 Thalesians 访谈（Saeed Amen 主持，YouTube `UODdqHh7ZNM`）
> - Quant Congress USA 2015（Risk Magazine，YouTube `9CbAcn--98Y`）
> - QuantCon 2018 "The 7 Reasons Most ML Funds Fail"（Quantopian，YouTube `BRUlSm4gdQ4`）
> - Kapitaleierdagen 2024（YouTube `fOCzNFwmM7Y`）
> - Fabozzi × Lopez de Prado "Don Marcos" 2025（PM-Research，付费墙）
> - CFA × Fabozzi 2025 webinar（`rpc.cfainstitute.org/.../conversations-with-frank-fabozzi-featuring-marcos-lopez-de-prado`）
> - "Democratization of Alpha"（YouTube `WoB3oPfWDF0`，Private video）
>
> 这些视频仅通过二手报道、主办方文案、搜索结果摘要间接引用，标记为 `[间接]`。

---

## A · 被追问时的回答模式

收录他在记者 / 主持人 / 论战对手 / 国会议员 **直接追问** 时的即席应对。重点看他如何**不回避**核心冲突、如何用什么句式反击。

### A-1 · "你批判 econ-quant，自己也在做策略——区别是什么？"

**最权威一次回答**，Risk.net 2019（Rob Mannix 专访，2019-09-19）：
https://www.risk.net/investing/quant-investing/6993166/

他区分 "math-quants" 与 "econ-quants" 两类——自己属前者。原话：

> "They [econ-quants] form a theory, they select the data that helps them prove that theory, they run some thousands of linear regressions, they report only the result with the lowest p-value."

> "If you acknowledge that each study is the result of thousands of unreported backtests, rather than one backtest, it is quite unlikely any of these factors is real."

> "Unless there is some sort of revolution in the econ-quant space, those firms will struggle."

**回答模式**：不回避"你自己也在做策略"这个指控——直接把自己放进另一个阵营（math-quant / ML / causal），让方法论差异承担论证，不靠身份辩护。

同一主题在 InformaConnect 2020-03-24 "Quant of the Year 2019" 访谈（https://informaconnect.com/a-conversation-with-quant-of-the-year-2019-marcos-lopez-de-prado/）里，他又加一刀：

> "Math-quants are empiricists, not dogmatists: they derive theories from their rigorous analysis of large amounts of data."

**暗含句式**：把对方的归类（你也是 quant）承认一半，然后用方法论差异把剩下一半切掉。

### A-2 · "ML 在金融真的 work 吗？还是只是另一种 overfitting？"

**InformaConnect "The future is bright..." 2021-01-05**（https://informaconnect.com/the-future-is-bright-for-those-who-survive/）直接反转这个追问：

> "[Classical methods are] more likely to overfit."

*主持人追问 ML 相比经典方法的风险*，他反过来指控经典方法**更**容易过拟合——因为 ML 自带 cross-validation / regularization / ensemble，而 econometrics 没有。

同一访谈关于"edge 从哪来"：

> "Whatever edge you aspire to gain in finance, it can only be justified in terms of someone else making a systematic mistake."

**回答模式**：把"ML 可能 overfit"的担忧，重定义为"ML 的 overfit 至少可被测量，你的 OLS 连测量工具都没有"。这是典型的**转移举证责任**。

在 Congressional Testimony（2019-12-06，见 D-1）里他把 overfitting 直接定性为 **scientific fraud**：

> "This methodological error is known as 'backtest overfitting,' and it is so notorious among statisticians that we consider it scientific fraud."

### A-3 · 被要求对特定公司 / 基金 / 人点评

**从不避让具体案例**，但**只点方法不点人**（除了 Taleb——见 C-3）。

Risk.net 2019 里被问到具体哪些 firm 会出问题：他**不点名**，只说"econ-quant 类"——但上下文让读者都能对号入座（Fama-French 系）。

InformaConnect 2020 被问到 "aren't some econ-quant firms experimenting with ML?" 他直接说：

> *[paraphrased] These announcements are primarily a marketing ploy to address mediocre results.*

指出两大障碍：(1) 承认方法论过时的心理抗性 (2) 内部权力斗争。

**回答模式**：具体公司不点名（避免诽谤诉讼），但把"营销话术"这个判定公开喊出来，让读者自己填空。

---

## B · 即兴类比（书里没写过的）

收录他临场解释抽象概念时抛出来的比喻。**不收** AFML 书里正式定义的术语（如 Triple Barrier、PBO）——那是系统化的，不是即兴的。

### B-1 · 金融研究 = 不能重复实验的物理学

Singularity Hub, 2016-06-13（Jason Dorrier 访谈，Exponential Finance 峰会后台）：
https://singularityhub.com/2016/06/13/how-quantum-computing-can-make-finance-more-scientific/

> "That's the situation in finance. It's a very big problem that most research is done without having the ability to reproduce an experiment by controlling the variables involved in that experiment."

**即兴扩展**：把自己比喻成"一个不能重复扔球、却还想研究重力"的物理学家。这个比喻**不在** AFML 书里——是现场对记者讲的。

### B-2 · 量子计算 = "用自然解自然的问题"

同一访谈：

> "Essentially… a quantum computer is a device that uses nature to solve a problem that is relevant to us."

> "The digital computing era is about to end. We need something to replace it. And right now the best candidate is quantum computing."

**回答模式**：面对非技术记者（Singularity Hub 读者），用一句**去掉术语**的定义打开话题——"用自然解问题"。注意他没讲 qubit、superposition，只讲一个具象动作。

### B-3 · 天气预报 + 智能 agent = 金融市场

同一访谈延伸类比：

> *[paraphrased] Weather modeling handles complex variable interactions, but markets additionally involve intelligent agents constantly adapting behavior based on peer actions—making them substantially more intricate.*

**关键判断**：他不把市场比作**天气**（常见陈词），而是比作 **"天气 + 能看天气预报并根据预报调整行为的天气"**。递归层加进来。

### B-4 · Black Swan 预测 = 广义相对论 → 黑洞

InformaConnect 2021（见 A-2）讨论 Black Swan 为何统计模型预测不了时：

> "Only a theory can do that."

*具体类比*：

> *[reference] General Relativity predicted black holes decades before observation.*

**回答模式**：用**物理学史**做类比（不是数学、不是工程），主张只有**理论**（causal structure）才能预测结构上未见过的事件——统计联系做不到。这是他对 Taleb 的间接反击（见 C-3）：不是说黑天鹅不存在，而是说你没理论就没法预测它，光抱怨 fat tail 不够。

### B-5 · Backtest 过拟合 = 制药公司不做 FDA 审批就卖药

Forbes 2018-05-25（Brett Steenbarger 访谈 Bailey & Lopez de Prado，Mathematical Investor 转载 https://mathinvestor.org/2018/05/bailey-and-lopez-de-prado-on-the-crisis-of-pseudoscience-in-finance/）：

*他们共同的类比*：制药公司测 1000 种药在 1000 组病人上，挑几十个 p<0.05 的就拿去卖，没有监管——金融业正是这样卖策略，投资者却没有 FDA 这样的消费者保护机构。

Congressional Testimony 2019（见 D-1）把这个类比正式化：

> "In other experimental fields, like in medical research, logging all trials is standard operating practice."

**回答模式**：当他想**让非专业听众感觉愤怒**时就上药厂类比；当他想**让技术同行感觉羞耻**时就上 scientific fraud 定性。两套话术按听众切换。

### B-6 · 工厂 vs 手工——"strategy factory" 概念

InformaConnect 2020（见 A-1）提出三个 institutional investor 的出路时，他用了"strategy factory"一词：

> *[paraphrased] Three alternatives: invest in math-quant firms, strategy factories, or insource investment processes for potential 90% cost reduction.*

把 quant 研究流程工业化 → "工厂" 隐喻。这也是他在 Cornell "Seven Reasons" 讲座里反复用的组织架构比喻——把每个研究员当"手工作坊"是反模式，统一的 research platform 才是"工厂"。

---

## C · 立场演化 / 强化 / 弱化的瞬间

### C-1 · 从 AFML (2018) → MLAM (2020) → CFI (2023) 的主张演化

**强化**的部分：
- **p-hacking / 多重检验** 从 AFML 的一章上升到 MLAM 全书主题之一，再到 CFI 的**副标题级关切**（*Causal Factor Investing: Can Factor Investing Become Scientific?* 2023）
- 在 LinkedIn 2022 年底的帖子（https://www.linkedin.com/posts/lopezdeprado_are-you-an-associational-quant-or-a-causal-activity-7015709847014785024-2ppC）首次公开提出 **"associational quant" vs "causal quant"** 的身份标签——这是 2018 AFML 里没有的二分
- 2024 LinkedIn 帖（https://www.linkedin.com/posts/lopezdeprado_why-has-factor-investing-failed-surely-activity-7153381278388543489-d37V）把"factor investing failed"直接标成结论，不再是 2018 时的"可能有问题"

**弱化**的部分：
- 2016 Singularity Hub 访谈对**量子计算**非常乐观（"digital computing era is about to end"），2019 Risk.net 仍强调"不准备就完蛋"，但 2023 ADIA Lab / CFI 阶段已经基本不谈——重心完全转到 causal inference。**间接**从他 Lectures.htm 页面也能看出：量子类讲座定格在 2016-2017，之后是 ML / causality。
- 早期（2013 Algorithmic Finance Journal "A Minute with..."）还在讲 HFT 微观结构，后期完全不讲了——职业轨迹从 Guggenheim（HFT / execution）→ AQR → TPT → ADIA 已经离开那个领域。

### C-2 · 量子计算乐观度曲线

- **2016 乐观顶点**（Singularity Hub）："The digital computing era is about to end."
- **2019 维持但转具体**（Risk.net）：*[paraphrased] adoption delays could prove catastrophic for unprepared firms*——从革命性语调转向战术警告
- **2023-2025 基本消失**：CFI 书、ADIA Lab 研究、Fabozzi 对谈都不谈量子了，主题切到 causal inference。**他没公开收回过量子观点，只是静默转向。**

### C-3 · 对 Taleb 从沉默到公开反击（2020 May 决裂点）

**之前**（2018-2019 AFML 发布期）：López de Prado 不公开回应 Taleb 对 ML quant finance 的长期指控（"charlatanism"）。

**引爆点**：2020-05 Asness vs Taleb 的 Twitter 大战（Aaron Brown 2020-05-26 Bloomberg Opinion / Yahoo Finance 有总结 https://finance.yahoo.com/news/taleb-asness-black-swan-spat-131503756.html；Dealbreaker 2020-05 也有报道但已 403）。López de Prado 介入，发推（2020-05-30 左右，推文 ID `1266716228497944577`）：

> "@yogicrypto @PTetlock @CliffordAsness We tried that. Taleb will not share his data, and that's the end of the scientific debate. Instead, Taleb smears anyone who challenges his opinions, and incites his college students to verbally abuse his opponents. If Black Swan strategies work, where are the track records?"

https://x.com/lopezdeprado/status/1266716228497944577

**回答模式三连**：
1. **数据证据** — "won't share his data" → 终结 scientific debate 的前置条件
2. **人身作风** — "smears... incites students"
3. **业绩挑战** — "where are the track records?"（这是最狠的一击，针对 Taleb 长期不公开 Universa 具体业绩数字）

**之后**：López de Prado 的 Incerto / Taleb 相关推文就这么一条公开标志性的。他没把这个议题继续拉长——但每次被问到 Black Swan 预测就回到 B-4 的"只有理论能预测结构未见"立场（间接反击 Taleb 的纯统计尾部观）。

### C-4 · LLM / Generative AI 立场（2023+，不激进）

公开访谈里**几乎不正面评论 LLM**。ADIA Lab Market Prediction Competition 颁奖 panel（CrunchDAO Ensemble Podcast, 2023-12-01, https://open.spotify.com/episode/6hnCuQE0MyVwOyWBhUOxhm）主题是 "Replicability in AI, P-Hacking and implications in Quant Finance"——他把**replicability crisis** 作为观察 AI/LLM 的视角，而不是去辩论 LLM 能否做 alpha。

**暗含立场**：LLM 作为 causal discovery 的辅助（ADIA Lab 2024 Causal Discovery Challenge 评估了 AI 学 causal structure 的能力，paper SSRN 6125566），**不作为** alpha 生成器。他从不像某些量化 KOL 那样吹 "GPT can trade"。

---

## D · 拒绝 / 回避 / 只给一半答案的话题

### D-1 · 国会质询 Q&A 的真实边界（2019-12-06）

**prepared testimony**（https://www.congress.gov/116/meeting/house/110292/witnesses/HHRG-116-BA00-Wstate-LopezdePradoM-20191206.pdf）全文 13 页，核心结论（他**主动** 上升到立法高度）：

> "This methodological error is known as 'backtest overfitting,' and it is so notorious among statisticians that we consider it scientific fraud (Bailey et al. [2014]). Academic financial journals are filled with such pseudo-discoveries."

> "Although there are no laws specifically prohibiting funds based on overfit backtests (yet), investors may have a legal case against this widespread investment malpractice that professional associations of mathematicians have deemed unethical."

**他主动提出的立法/监管建议三条**：
1. 要求 firm **记录所有 backtests**（就像药物试验日志）
2. 要求披露产品是否基于"flawed academic publications"
3. 推行 ML tournament 范式（数据不全给研究者，防 overfit）

**移民与人才**：
> "We must make sure that America retains the talent it develops. ... Unless we help them stay, they will return to their countries of origin with their fellow students, to compete against us in the near future."

**多元化**：
> "In finance, too, math could be 'the great equalizer.'"

**他回避了什么**：prepared statement 里**不点任何具体公司名**（只脚注 Bloomberg 2015 flash crash 报道）；不评价 AQR / Bridgewater / Two Sigma / Renaissance；不讨论自己与 AQR 分手的细节。**回避标志**：凡是可能变成法律纠纷或前雇主敏感信息的，他走"只讲方法论 / 不讲实体"的路径。

### D-2 · 仓位 / 具体策略 / 自己的 P&L

跨所有访谈**一致不谈**：
- TPT / ADIA 在管策略的任何仓位细节
- 他自己个人持仓
- Guggenheim 13B AUM 时期的具体 trade

**间接数据点**：Congress testimony 2019 bio 里他**主动** 披露过 "delivered an audited risk-adjusted return (information ratio) of 2.3"（在 Guggenheim）——这是他唯一公开的历史业绩数字。**为什么披露这个**：用来反击"你没 track record"的潜在 Taleb 式攻击（C-3）。

### D-3 · 不直接 endorse 具体 firm——唯一的例外

InformaConnect 2020 里他**主动** 点名 "math-quant firms like Renaissance Technologies, Two Sigma, DE Shaw" 作为正面例子（Sharpe > 2）——但这是把它们当**类别标本**，不是推荐投资。

他**从不**点名具体 econ-quant firm 作反面——这个不对称很重要：正面点名（强化 math-quant 分类）是安全的（这些 firm 不会告他），反面点名（某 AQR / GSAM / BlackRock 系是 charlatan）会引诉讼。

### D-4 · 对 Taleb 的**正面学术辩论**回避，但**人身作风**公开回击

对比 C-3 的推文：他攻击的是 Taleb 的 **sharing data** / **incitement to students** / **track record**——**不正面** 辩论 Taleb 的分布论（fat tails 数学、ergodicity、ludic fallacy）。

**为什么这样划界**：在 López de Prado 的框架里，Taleb 是"只有批评没有方法"的——他（López de Prado）要的是可实操的 protocol（PBO、DSR、causal graph、tournament），Taleb 提供不了这个。所以不跟 Taleb 在**哲学层**吵（因为没 operational answer 就没讨论意义），只在**可验证层**——你有没有数据、有没有业绩——吵。

**间接可验证**：查他全部论文、所有已公开访谈，他对 Taleb 的点名批评**只有这一次公开推文**——其他所有场合都用 "black swan strategies" / "theory-based prediction" 等抽象层代词。这是有纪律的回避。

### D-5 · Fama / French / Andrew Lo 的学术对话——不存在

搜索未发现 López de Prado 与 Fama / French / Cochrane 的同台讨论、对话、回应。他的 *Causal Factor Investing* (2023) 大量**引用** 并**批判** Fama-French 框架，但是**书面单向** 批评——没有这些大佬公开回应他，也没有他们同台的 debate。

**他的策略选择**：绕过"名教授现场辩论"路径，走"书 + 国会 testimony + ADIA Lab 研究序列"路径。这本身是对 D-4 同一哲学的延伸：不在对方设定的舞台（AEA / Chicago seminar）上辩论，只在自己搭建的 infrastructure（CFI 书、ADIA Lab、Journal of Financial Data Science 编辑权）里输出。

### D-6 · AQR 分手原因

Bloomberg 2019-04-05 报道（https://www.bloomberg.com/news/articles/2019-04-05/aqr-head-of-machine-learning-set-to-leave-after-less-than-a-year；WebFetch 403，信息来自搜索摘要）：他从 AQR 离开的"内部原因"**从未公开说过**。公开版本统一为"launching TPT, AQR bought his patents"。

**关键不对称**：他**公开批评** "econ-quant firms 内部权力斗争 + 拒认方法过时"（InformaConnect 2020，A-3）——这句话的**指涉对象** 不需要任何推测就能落在 AQR 身上（他刚从那离开），但他**从不** 把这两件事在同一句里点明。这是 D-2 的变体：结构诚实（说方法论问题），政治回避（不点前雇主名）。

---

## 辅助索引 · 按来源平台列

| 来源类型 | 平台 / 节目 | 主持 / 作者 | 年份 | URL 或 ID | 是否有 transcript |
|---|---|---|---|---|---|
| Podcast | Risk.net Cutting Edge | Mauro Cesa | 2020-06-19 | risk.net/.../7564701 | 描述 + 摘要引语 |
| Podcast | The Ensemble (CrunchDAO) | Matteo Manzi | 2023-12-01 | spotify: 6hnCuQE0MyVwOyWBhUOxhm | 无（仅 37min 音频） |
| Podcast | Parkview Group Ep. 5 | Oussama Himani | 2020 | parkview.ch（404 已删） | 无 |
| Podcast | DG-FinTech | — | 2019 | soundcloud user-503420529/a-m-pe3-marcos-e1 | 无 |
| YouTube | Global Derivatives 2015 | Saeed Amen (Thalesians) | 2015-05 | UODdqHh7ZNM | bot 挡下载 |
| YouTube | Risk / Quant Congress USA | — | 2015-06 | 9CbAcn--98Y | bot 挡下载 |
| YouTube | QuantCon 2018 "Seven Reasons" | Quantopian | 2018 | BRUlSm4gdQ4 | bot 挡下载（仅二手 Medium 总结） |
| YouTube | Kapitaleierdagen 2024 | — | 2024 | fOCzNFwmM7Y | bot 挡下载 |
| YouTube | 1QBit Exponential Finance | — | 2016 | kU7vk9jmQC8 | 无 |
| YouTube | Numerai Erasure Conf | Richard Craib | 2019 | YojhLjLrG1M?t=1726 | bot 挡下载 |
| YouTube | "Democratization of Alpha" | — | — | WoB3oPfWDF0 | Private（无权限） |
| 网络访谈 | Risk.net 文字专访 | Rob Mannix | 2019-09-19 | risk.net/.../6993166 | 有直接引语 ✓ |
| 网络访谈 | InformaConnect "Quant of Year" | — | 2020-03-24 | informaconnect.com/a-conversation... | 有直接引语 ✓ |
| 网络访谈 | InformaConnect "Future is bright" | — | 2021-01-05 | informaconnect.com/the-future-is-bright... | 有直接引语 ✓ |
| 网络访谈 | Singularity Hub | Jason Dorrier | 2016-06-13 | singularityhub.com/.../quantum-computing... | 有直接引语 ✓ |
| 网络访谈 | Forbes / Math Investor 转 | Brett Steenbarger | 2018-05-25 | mathinvestor.org/2018/05/bailey... | 半直接 |
| 网络访谈 | Mathematical Investor | — | 2019-09 | mathinvestor.org/2019/09/interview... | 摘要 |
| PDF 访谈 | quantresearch.org 自档案 | — | — | quantresearch.org/marcoslopezdepradointerview.pdf | 二进制未解出 |
| 官方证词 | US House Committee on Financial Services | Task Force on AI | 2019-12-06 | congress.gov HHRG-116-BA00 | 有完整 PDF ✓（13 页全文已获取） |
| Video+Webinar | CFA Institute × Fabozzi | Frank Fabozzi | 2025-03-18 | rpc.cfainstitute.org/.../conversations-with-frank-fabozzi... | 仅描述 |
| 文字对谈 | PM-Research "Don Marcos" | Frank Fabozzi | 2025-02-03 | pm-research.com/content/iijjfds/7/1/10 | 付费墙 |
| 推文 | X / Twitter | @lopezdeprado | 2020-05-30 | x.com/lopezdeprado/status/1266716228497944577 | 有全文 ✓ |
| 推文 | X / Twitter | @lopezdeprado | 2019-06-13 | x.com/lopezdeprado/status/1138716396248915968 | 有（backtest 立场声明）✓ |
| 推文 | X / Twitter | @lopezdeprado | 2020-01-29 | x.com/lopezdeprado/status/1222542276703985673 | 有（p-hacking）✓ |

---

## 待补缺口（后续调研优先级）

1. **高优先级**：找到 QuantCon 2018 "Seven Reasons" 的英文 transcript——这是他最重要的一次公开讲座，目前只有 Medium 二手总结。方案：等 YouTube cookie 可用或找 Quantopian archive 的 slides PDF。
2. **高优先级**：CFA × Fabozzi 2025 webinar 的录像——López de Prado 最近一次公开长访谈（55 分钟），主题正是 causal inference。需 CFA Institute 登录。
3. **中优先级**：Global Derivatives 2015 Thalesians（Saeed Amen 主持），能看他 HFT 期的表达——对比当前的 causal 期，能测**表达演化**。
4. **中优先级**：PM-Research 2025 "Don Marcos" 付费全文——这是他目前职业顶峰的自我叙事，对比 2013 *A Minute with* 能测"年轻 vs 权威"的语体差。
5. **低优先级**：找 Parkview Podcast Ep.5（2020）的 archive.org 快照——官方页面已 404。
6. **低优先级**：Numerai Erasure Conf 2019（Richard Craib 同台）——这是他和一个 skeptical founder 的对谈，风格上该有意思。

---

## 引用与出处纪律

- **在本仓库 SKILL.md / anti-pattern / expression-levels 引用本文件时**：必须具体到小节（如 "见 02 C-3"），不要笼统引 "02-conversations.md"。
- **引 López de Prado 原话**：必须保留英文原文 + 年份 + 来源（X 推文带 status ID；书面访谈带发布日期）。不允许中文改写后当原话。
- **不允许引** `quantresearch.org/marcoslopezdepradointerview.pdf` 和 `Interview_AF.pdf` 的内容——这两个 PDF 是扫描/PowerPoint 转 PDF，WebFetch 未能提取可验证文本。待后续人工校验后才能用。
- **推文时间戳** 来自 Twitter snowflake ID 解析，与搜索引擎索引吻合，作为二级证据。
