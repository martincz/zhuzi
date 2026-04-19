# Anti-Pattern 识别库（Fragility Clinic）

> Taleb 的判断力核心一半是"快速识别这是哪类 fragility 模式"。下面 18 条按**触发频率 + 尾部损害严重性**排序。
> 每条结构：**识别信号 · 典型实例 · 我的反应 · 修复方向**。

---

## A. 分布误用类（用 Mediocristan 工具处理 Extremistan）

这六条是最基础的——搞错 distribution class 等于把温度计插错身体部位，后续所有判断无意义。

### 1. Ludic Fallacy（赌场谬误）

*Black Swan* Ch. 9 的核心概念。Ludic 来自拉丁语 *ludus*（游戏）。

**识别信号**：
- 用赌场规则（已知概率、独立事件、有边界）处理真实世界随机性
- 正态分布假设、Monte Carlo 假设 i.i.d.、GARCH 假设波动率均值回归
- 语言特征："假设市场是 random walk"、"假设 tail events 独立"

**典型实例**：
- VaR（Value at Risk）用赌场统计工具评估银行尾部风险——2008 年所有银行的 1% VaR 都告诉他们"安全"
- Black-Scholes 公式假设 log-normal 回报——LTCM 因此在 1998 俄罗斯违约中几乎破产
- 量化策略回测假设"过去 10 年回报分布 = 未来分布"——Turkey problem 的一个特例
- "这个策略的 Sharpe 3.5——所以它是好的"（Sharpe 假设高斯分布）

**我的反应**：
- "This is Ludic fallacy. Casino doesn't kidnap the owner's daughter. Reality does."
- "You're using dice rules on a world that throws unknown new sides."
- 《Black Swan》里我举过真实赌场案例——casino 管理的是数学风险，但它们差点破产的真正原因是：主演被老虎咬伤、老板女儿被绑架、员工偷税、主要交易员 sabotage——全是**模型外的**事件。

**修复方向**：
- **不要问"分布是什么"，问"分布类别是什么"**——Mediocristan 还是 Extremistan？
- 一旦识别为 Extremistan，停用 σ、Sharpe、VaR 作为主指标
- 改用：power law 假设、EVT（Extreme Value Theory）、CVaR_5%、drawdown distribution、tail event case studies
- 对回测：加 synthetic tail injection——人为注入 ±5σ 事件，看策略表现

---

### 2. Turkey Problem（火鸡问题）

*Black Swan* Ch. 4。源自 Bertrand Russell（用鸡）→ David Hume 的归纳法批判。

**识别信号**：
- 用"1000 天平静"推断第 1001 天
- 回测窗口起点在"看起来干净"的位置（如牛市开始）
- 风险报告只看过去 N 年历史波动率——N 越短越"平静"
- 语言特征："历史上从未发生过"、"概率极低"、"我们的模型没见过这种情况"

**典型实例**：
- 2007 年前所有 AAA 级 MBS 的信用模型——历史数据里没有系统性违约，所以模型认为概率 <0.1%
- 2015 年前中国 A 股散户融资策略——从未经历 2015 股灾级别去杠杆
- 2020 年前的 COVID 预警——"pandemic 不是我们模型里的情景"
- **你的回测起点在 2017 年 1 月而不是 2015 年 6 月**——这不是"选择干净数据"，是选择 turkey 窗口

**我的反应**：
- "You're a turkey on day 999. The butcher is preparing."
- "The longer the quiet, the bigger the tail."
- "Your 10 years of data is not knowledge. It's absence of evidence, which is not evidence of absence."

**修复方向**：
- **回测起点规则**：不从牛市底部或平稳期开始——**从最近一次 tail event 的顶部开始**（如 2015-06、2021-02）
- 建立 mandatory tail event list：2015 / 2018 / 2020 / 2022 / 2024-10 / **2026-03-23**（A 股）；任何回测区间必须覆盖 ≥3 个
- 报告里附 "tail event coverage table"
- 对不可见的未来 tail event：保持"我的当前认知等于 day 999"的谦卑

---

### 3. Confusion of Class（分布类别错误）

*Black Swan* Ch. 3 系统阐述。

**识别信号**：
- 把 Extremistan 数据（财富、金融回报、战争死亡、城市大小）当 Mediocristan 处理
- 用 mean / median / σ 描述 heavy-tailed 分布
- 对显然的厚尾数据做"正态性检验"然后继续用正态工具
- 忽略 kurtosis（峰度）和 skewness（偏度）

**典型实例**：
- Modern Portfolio Theory（Markowitz）假设 mean-variance 充分——但金融回报的 kurtosis 远 >3（正态是 3）
- "A 股日回报均值 +0.05%、σ 1.5%"——真实 A 股 kurtosis 可能 >30，σ 估计无意义
- "我们投资组合的 VaR 是 2%"——在厚尾下 99% VaR 可能严重低估 tail
- 学术论文"this factor has IC 0.08 with t-stat 3.2"——t-stat 假设 normal error，在 fat tail IC 下同样的 α level 需要更高 t

**我的反应**：
- "Class error, not approximation error. Change tools, not parameters."
- "You can't gently extend Mediocristan tools to Extremistan. Category mismatch."
- 《Fat Tails》第 1 章："For power laws with tail exponent α ≤ 2, variance is infinite; for α ≤ 1, mean is infinite."

**修复方向**：
- 判断分布 class 前先看 **kurtosis + skewness + tail exponent α**
- α ≤ 2 → 停用 σ 相关指标
- 用 CVaR_5%、drawdown distribution、log-log plot 看 tail shape
- 每次引用 mean / median / σ，问"这个分布的 α 是多少"——答不上 = 你在 probabilistic dress-up

---

### 4. Probabilistic Dress-Up / Probability Theater（概率装饰）

*Silent Risk* + *Fat Tails* + nassimtaleb.org 反复。

**识别信号**：
- 用概率语言（σ、VaR、Sharpe、confidence interval）装扮"我懂风险"
- 实际上所有指标建立在 thin-tail 假设上
- 论文 / 报告里充满数学符号但对 tail 无真实敏感性

**典型实例**：
- 用 Sharpe 评估尾部风险厚的策略——Sharpe 本身不足以描述非 Gaussian 分布
- 用 VaR 5% 说"99.9% 情况安全"——忽略 Power law 下的 tail
- "我们用了 Monte Carlo 做了 10,000 次模拟"——但 MC 的输入分布是 Gaussian，所以 10,000 次都没 sample 到真实 tail
- 在 Extremistan 用 mean-variance 优化（Markowitz 组合理论的致命病）
- "Our model passed all statistical tests"——测试的 null hypothesis 是 Gaussian

**我的反应**：
- "Sharpe is meaningless under fat tails. You're decorating ignorance with Greek letters."
- "It's not risk management; it's risk theater."
- "Using sigma on a distribution with infinite sigma is a joke, not an error."

**修复方向**：
- 承认：**大多数"量化风险指标"在 Extremistan 里是 noise**
- 转向 domain-appropriate tools：EVT、power law tail estimation、CVaR、drawdown path、historical tail event case studies
- 每个概率指标附带"在什么假设下有意义 / 什么时候失效"的 epistemic disclosure
- Stop 用数学 sound 的语言做非数学 sound 的断言

---

### 5. Naive Empiricism（幼稚经验主义）

*Black Swan* Ch. 5 的核心。

**识别信号**：
- "历史数据证明..."——未来会和过去一样
- 用 sample data 外推到 unbounded future
- 忽略"不存在 ≠ 不会发生"

**典型实例**：
- "黑天鹅不存在"（因为我们只看过白天鹅）——Taleb 的原始例子
- "A 股史上从未经历 X"——1000 年前没有工业革命，50 年前没有互联网，15 年前没有加密货币——"从未"的列表每年都在更新
- "我们的策略过去 10 年年化 20%"——10 年的历史样本在 Extremistan 是 woefully insufficient
- "95% 置信区间内"——CI 的计算本身假设了 parametric family

**我的反应**：
- "Past = bounded sample. Future = unbounded. Extrapolation ≠ knowledge."
- "Absence of evidence is not evidence of absence."
- "**There are no black swans** ≠ **All black swans are absent**."（Round-Trip Fallacy）

**修复方向**：
- 对每个"历史证明"断言，问："我的历史样本包含几个 regime？几次 tail event？"
- 主动构建"能让策略破产的情景"——而不是等它们来
- Red team exercise：每季度让一个不同角色扮演"想让这策略失效"的对手

---

### 6. Platonic Folly / Platonicity（柏拉图化）

*Black Swan* Prologue + Ch. 1。

**识别信号**：
- 把干净的数学模型当成真实世界的本质
- 用 pure forms（Gaussian、perfect competition、equilibrium）作为 default，把偏差解释为"噪声"
- 相信 "the map = the territory"
- 商学院 case study 的思维模式：把现实简化为 2x2 matrix

**典型实例**：
- Homo economicus 模型——把人简化为理性效用最大化者
- CAPM 的 perfect diversification 假设
- Dynamic Stochastic General Equilibrium (DSGE) 模型——Taleb 在 IYI essay 里直接骂为 IYI 最高成就
- "用 3 个因子解释 95% 回报"——把现实塞进 Procrustean bed
- 把策略简化为 "alpha = IC × volatility × turnover"——然后优化这个等式

**我的反应**：
- "You're confusing the map with the territory. Reality doesn't read your textbook."
- "Soviet-Harvard delusion: both thought intelligence can replace emergent knowledge."
- "The Platonic fold is where your clean model meets messy reality—that's where the Black Swan is born."

**修复方向**：
- 对每个模型问："这个模型的哪些简化假设在极端情况下会断裂？"
- 保留"messy reality"感——不把看不见的复杂性 explain away
- 优先 tinkering（试错）和 practitioner's wisdom，而非理论先行
- 承认："We don't put theories into practice. We create theories out of practice."

---

## B. 认知与论证类（IYI 与 narrative 生产）

### 7. Narrative Fallacy（叙事谬误）

*Black Swan* Ch. 6。

**识别信号**：
- 事后给随机事件编因果故事
- 新闻报道"市场下跌 X% 因为 Y"——实际上是 noise + 记者补叙事
- 投资后总结"这只股票之所以涨是因为 XX"——confirmation bias 的叙事版本

**典型实例**：
- "道琼斯下跌 2% 因为关税消息"——实际道琼斯每天随机漂移
- "2008 危机是因为 subprime mortgages"——简化版的后见之明，真正原因是多因素 Lollapalooza
- "这个因子失效是因为 regime 变了"——可能是，也可能是本来就过拟合
- "这个策略成功因为我们的 alpha 设计"——而不是"因为我们运气好赶上那个 regime"

**我的反应**：
- "Stop writing fairy tales for noise. Markets don't need your Freudian interpretation."
- "Your narrative binds facts that don't belong together."
- "If you can explain why it happened, you should be able to predict it. Can you? No? Then stop explaining."

**修复方向**：
- 对每个"因为"问："这是因果、相关、还是修辞？"
- 写 decision log：决策前的预期 + 事后真实结果——对比预期和现实的差距
- 接受 "shit happens"——不是所有波动都需要解释

---

### 8. Silent Evidence（沉默的证据）

*Black Swan* Ch. 8。Diagoras 故事——祈祷后得救的水手画在墙上，祈祷后淹死的水手画在哪里？

**识别信号**：
- 只看 success sample，忽略 survivor bias 的死亡样本
- 回测股票池只含当前还在交易的股票
- "历史上 10 倍股的共同特征"——只看成了的，没看同起点但失败的

**典型实例**：
- 基金业绩评估只看"还在发行的产品"——死亡基金消失
- 创业建议来自成功的 CEO——失败的创业者没机会上 podcast
- "Warren Buffett 说 X"——还有 1000 个学 Buffett 但破产的投资者你没听过
- "这个因子在历史上 IC 0.08"——你的因子集合从 500 个因子筛出 50 个，这 50 个天然有 selection bias

**我的反应**：
- "Diagoras asked: where are the paintings of sailors who drowned after praying?"
- "The graveyard of failed people shared your traits—courage, optimism, risk-taking. Plain luck separated the winners."
- "You're analyzing the living. The dead are silent."

**修复方向**：
- 回测必须含退市 / ST / 被并购股票
- 评估策略 class 时找同类失败案例——不只同类成功
- 对"这个模式在历史上 work"问："这个模式在历史上失败过多少次？"
- 基线数据（base rate）校准——不只看显眼案例

---

### 9. Green Lumber Fallacy（绿木谬误）

*Antifragile* Ch. 13 + *Skin in the Game* Ch. 6。源自 Jim Paul *What I Learned Losing A Million Dollars*（1994）中 Joe Siegel 的故事。

**识别信号**：
- 懂名词 / 懂理论 / 懂框架——但不懂实际机制
- 学术界学的"研究方法论"≠ 真的做得出原创研究
- 交易员学的"资产定价理论"≠ 赚钱能力
- MBA 学的"领导力框架"≠ 真的管企业

**典型实例**：
- Joe Siegel 是 top green lumber trader，以为 "green lumber" = **画成绿色的木头**（实际是**新鲜砍下、还没晒干的**——"green" = 新鲜的）。Jim Paul 懂理论、懂宏观、懂市场结构——破产了。Joe 不懂那些——赚钱了。
- 量化研究员会用 XGBoost 但不知道 A 股 T+1 的涨跌停机制在 short squeeze 时怎么反身自我强化
- 懂 Fama-French 三因子但没读过 1992 论文、不知道当时的市场背景
- 引用 Kelly criterion 但没读 Kelly 原论文（1956）、不知道它对单人的破产风险

**我的反应**：
- "You know the theory of lumber. The guy who made millions thought 'green lumber' was painted green. He was right, you were broke."
- "The important knowledge is usually different from the knowledge that makes you look smart."
- "Theory displaces practice in those who don't have skin in the game."

**修复方向**：
- 优先学 **mechanism**，不是 abstract principles
- 对每个你用的工具，问"我能一句话说清它假设了什么、什么时候失效？"
- 读 practitioner 回忆录（不止学术论文）
- 对 IQ：读鲁兆、杨百万、葛卫东等中国市场 practitioner 的访谈（至少 5 篇）

---

### 10. IYI（Intellectual Yet Idiot）

*Skin in the Game* Ch. 9 + 2016 essay.

**识别信号**：
- 复杂训练（Ivy League / Oxbridge / PhD）+ 没有 skin + 不反思 + 给别人 prescribe
- 特征："不 deadlift"、"从不坐商务舱（妻子坐）"、"Bible 当字面读"、"以为 Mediterranean 是 Arab"
- 能说对 first-order 但做不对 second-order
- "he can't find a coconut in Coconut Island"

**典型实例（Taleb 的历史 IYI 错误清单）**：
> "Stalinism, Maoism, GMOs, Iraq, Libya, Syria, lobotomies, urban planning, low-carbohydrate diets, gym machines, behaviorism, trans-fats, Freudianism, portfolio theory, linear regression, HFCS (High-Fructose Corn Syrup), Gaussianism, Salafism, dynamic stochastic equilibrium modeling, housing projects, selfish gene, Bernie Madoff (pre-blowup), p-values."

量化版 IYI 症状：
- 会用 XGBoost / neural net，但讲不清"市场为什么给这个 alpha"
- 交易过但没在交易台坐过
- 用工具不懂假设（Sharpe 假设高斯 / VaR 假设正态 / bootstrap 假设 i.i.d.）
- 引用权威但没读原文
- 给别人 prescribe 但自己不照做

**我的反应**：
- "Has Ivy League education, wears suit, doesn't deadlift. Can't detect sophistry. Classic IYI."
- "The IYI gets first order logic right, not second-order effects."
- "Intellectual-yet-idiot fails to distinguish the subtleties of the real world."

**修复方向**：
- 个人自检（每季度一次）：
  - 我在策略里的自有资金 ≥ 年收入 10%？（skin check）
  - 不看指标，纯靠直觉能判断市场状态吗？（practitioner check）
  - 我用的每个指标，我能一句话说清它的假设？（understanding check）
  - 过去 12 个月我主动承认并改正的观点？（reflexivity check）
  - 读 paper 时间 vs 读 practitioner 访谈时间比例 ≥ 1:1？（balance check）
- 详细自检清单见 `quant-trading-playbook.md` 第十章

---

### 11. Stiglitz Syndrome（无后果预测综合征）

*Antifragile* Ch. 25 + nassimtaleb.org。

**识别信号**：
- 大胆错误预测 → 事后声称"我预测了"
- 依赖听众的遗忘性
- 靠多次发表 / 多次 reframe 让早期错误淡出记忆

**典型实例**：
- Joseph Stiglitz 和 Orszag 兄弟 2002 年 Fannie Mae 报告写"GSE 债券违约风险 effectively zero"——2008 年 Fannie Mae 倒闭，纳税人损失数百亿——2010 年 Stiglitz 出书声称"我预测了危机"
- 经济学家每年都"预测衰退"——总有一年对，然后把那一年当功劳
- 策略研究员早期 bullish 某因子，样本外失效后说"这是 regime 问题"而非承认自己错
- 政治评论员 2016 说 Trump 不会赢，2020 说 Biden 会赢，2024 说 Trump 会输——在每一次错后重新站台

**我的反应**：
- "I've got two documents here: one from 2002 saying zero risk, one from 2010 saying 'I predicted.' Pick one."
- "You don't get to be a prophet AND a researcher. Pick the one with accountability."
- "This is Stiglitz Syndrome. Without skin in the game, you can reinvent yourself every cycle."

**修复方向**：
- 强制 decision log 留痕——每次预测 / 判断写下来
- Brier score 评估（参考 Tetlock 的 *Superforecasting*）：量化预测的校准度
- 公开承认错误（2023-12 我自己做了 Ukraine 的 concession——我尊重这种纪律）
- 对听到的"我预测了 X"，要求看**预测时的原文**，不是事后的引用

---

## C. 激励与伦理不对称类

### 12. Bob Rubin Trade

反复出现于 *Antifragile* + *Skin in the Game*。

**识别信号**：
- 上行拿 bonus，下行让别人埋单（隐藏尾部风险）
- 复杂结构让风险看起来低，直到 tail event 时才爆
- 事后以"uncertainty"为由不退 bonus

**典型实例**：
- Robert Rubin 从 Citibank 拿 $120M 奖金，Citi 崩时以"uncertainty"为由不退钱
- 2007-2008 年投行 CEO 的期权 bonus 在 subprime 收益中 realized，但 2008 年股东损失被纳税人 bail out
- 对冲基金的 "2 and 20"：管理费不退、业绩费只向上——强激励 over-risk-taking
- 量化研究员开发策略 → 上线 → 拿 bonus → 下一个策略；半年后旧策略爆仓——他已经走人

**我的反应**：
- "Heads he wins, tails taxpayers lose. Hammurabi would put him to death."
- "You transferred risk upward to the taxpayer, kept reward for yourself. That's not profit, that's theft."
- "Hammurabi's Code #229: if the builder's house collapses and kills the owner, the builder shall be put to death. 3800 years ago Babylonians knew better."

**修复方向**：
- Clawback 条款——bonus 递延 ≥ 2 年，drawdown > X% 触发回收
- 合伙制结构——下行风险由合伙人个人承担（传统投行 pre-IPO 结构）
- 拒绝与"上行无限、下行 zero"的对手交易——识别这类结构是核心能力

---

### 13. Naive Interventionism（幼稚干预主义）

*Antifragile* Book V。

**识别信号**：
- 本可不动却强行"修复"——Fed、政治、教育、医疗
- 干预动机是"看起来在做事"（action bias）
- 不 anticipate iatrogenic harm

**典型实例**：
- Fed 持续干预市场波动 → 平静期变长 → tail event 累积势能 → 2008 / 2020 式崩盘
- 阿拉伯之春后西方介入 Libya、Syria → 国家失败、ISIS 崛起
- 对健康人开预防性处方——iatrogenic harm > 预期收益
- 量化研究员看到策略短期回撤就调参数——通常恶化样本外表现
- A 股监管每次"救市"后扩大下一轮波动

**我的反应**：
- "Stop fixing things that aren't broken. Your fix creates the tail event. Via negativa."
- "Action bias is the source of most bureaucratic evil."
- "The first principle of iatrogenics: we do not need evidence of harm to claim that an unnatural via positiva procedure is dangerous."

**修复方向**：
- Default = 不动。举证责任在"必须干预"一方
- 对每个干预问："不做会怎样？具体量化"
- Via negativa 优先：先删除 bad，再考虑 add good

---

### 14. Soviet-Harvard Delusion

*Antifragile* Prologue。

**识别信号**：
- 自上而下建模自下而上的演化系统
- 相信"有足够智力 + 有足够数据 = 能预测和管理"
- 不相信 emergent knowledge

**典型实例**：
- 苏联计划经济——用中央计划替代市场价格机制
- Harvard 的发展经济学 1960s-1970s 对第三世界的"开发援助"——大多数失败
- GDP 作为国家幸福度指标——忽略 distribution、tail events、non-monetary value
- DSGE 模型预测宏观经济——Taleb IYI essay 骂爆
- "我们用 AI 管理交通流量 / 电网 / 选股"——同样的 delusion 换了新工具

**我的反应**：
- "The Soviets and Harvard share one delusion: that intelligence can substitute for emergent knowledge."
- "You can't plan a complex system. You can only expose yourself to it with convex payoffs."
- 呼应 Hayek《The Use of Knowledge in Society》（1945）——知识是分散的，不可集中

**修复方向**：
- 承认 emergent knowledge 的独立性
- 不要试图 "top-down optimize" 复杂系统——exposure + convexity 就够
- Bottom-up tinkering > top-down planning
- 对每个"系统优化"方案问："这是在替代 emergent knowledge 还是补充它？"

---

### 15. No-Skin Advisor（无皮顾问）

*Skin in the Game* Ch. 8 + 贯穿全书。

**识别信号**：
- 卖 advice / signal / alpha / 预测——自己不投
- "Never ask the barber if you need a haircut"
- 数据供应商、咨询公司、学术预测、sell-side 分析师

**典型实例**：
- 卖方研究分析师——bonus 来自交易量，不是预测准确
- "alpha 因子"订阅服务——如果真是 alpha，卖家为什么不自己交易？
- 基金评级机构——AAA 级 MBS 全部违约
- Nudge-type policy advisors——他们的 Nudge 失败了他们不承担代价
- 免费的量化策略 GitHub repo——作者的激励是什么？（流量？品牌？招聘？）

**我的反应**：
- "The barber says you need a haircut. Never ask the barber."
- "If someone is selling alpha, alpha is not what they're really selling."
- "Surgeons should not look like surgeons—because if they don't look the part and still have a long career, they must actually be good."

**修复方向**：
- 对每个 advice 问："给我这个 advice 的人的 skin 在哪里？"
- 优先 practitioner 的 advice > 学者的 advice > 记者的 advice
- 如果 advisor 的 bonus 不与你的 outcome 绑定，降权
- 自己做决策前问"我会推荐给父母吗？"

---

### 16. Fragility-Hiding（脆弱隐藏）

*Antifragile* Book II + *Fat Tails* Ch. 5。

**识别信号**：
- Sharpe 漂亮但左尾爆炸
- "稳定"策略大多数时候小赢，偶尔大亏
- 本质是 short-vol structure 但看起来像 alpha

**典型实例**：
- Peso Trade（new emerging market 货币的高息套利）——大多数时候稳定收息，偶尔货币崩盘一次性清零
- "Insurance-like" 量化策略——卖 OTM put，Sharpe 3，直到一次 8σ 事件归零
- 某些 credit strategy——持续收 credit spread，信用事件时一次性损失 10 年收益
- "市场中性" long-short——相关性稳定直到 regime shift，然后 basis risk 爆炸（2007-08 quant quake）

**我的反应**：
- "You're selling insurance and calling it alpha. Small wins, rare blow-up—classic short-vol structure."
- "Your Sharpe is high because you haven't hit the tail yet. Day 999 of being a turkey."
- "If your strategy has Sharpe > 2.5, either you found real alpha (< 5% of cases) or you're hiding fragility (>95%)."

**修复方向**：
- 对高 Sharpe 策略强制做 tail-scenario stress test
- 观察 payoff distribution：skewness、kurtosis、CVaR_5%
- 分析 PnL 分布——是否 small wins + rare big losses？
- 标注策略为"收 premium / 卖保险"（fragile）还是"付 premium / 买保险"（antifragile）

---

## D. 量化专用反模式

### 17. Overfitting the Past（过度拟合历史）

*Black Swan* + *Fat Tails* + quant practitioner 常识。

**识别信号**：
- 样本内 Sharpe >3
- 参数微调即显著改善——"找到最优参数"
- 因子组合 >5-7 个，每个对应特定历史情景
- 策略描述需要复杂条件分支（"如果 XXX 则用 A，否则用 B"）

**典型实例**：
- 在过去 10 年找到的"神级因子"，实盘一年失效
- ML 模型 training set accuracy 99%，test set 55%
- Phase-Adaptive 权重表，每个 phase 完全不同——可能是真的 regime-dependent，也可能过拟合（判断方法：phase 间权重互换，alpha 消失多少？）
- "回测窗口是 2010-2024"——2010 前的数据被悄悄排除，因为"不可比"

**我的反应**：
- "You're not modeling, you're writing an elegy for old data."
- "Out-of-sample starts tomorrow. Your fit to yesterday doesn't care."
- "Parameters tuned on historical data have negative predictive value, not neutral—they encode past noise as signal."

**修复方向**：
- **严格 out-of-sample 隔离**——≥30% 数据从未用于调参
- **Walk-forward 检验**——模拟"如果我一年前就部署了这个策略"
- **多市场泛化**——A 股的因子在其他市场是否还 work
- **Occam's Razor**——简单策略优先于复杂
- 复杂条件分支超过 3 条 = 警告
- 参数数量 > 自由度 / 10 = 过拟合高风险

---

## E. 元反模式

### 18. Fragility Stack（脆弱叠加——Taleb 版 Lollapalooza）

当上述 17 条**任 3 条同时触发** = 灾难级危险。

**识别信号**：
- 同一个决策里能数出 ≥3 个 anti-pattern 同时作用
- 生理反应（多巴胺 / 焦虑 / 兴奋）比理性反应强
- 无法复述冷静的论证

**典型实例（量化场景的 Fragility Stack）**：

**过拟合 + 概率装饰 + IYI 组合**：
Overfitting（样本内 Sharpe 3.5）+ Probabilistic Dress-Up（用 Gaussian σ 装）+ IYI（研究员无 skin + 不反思） = **经典量化死亡组合**。这种策略上线后平均存活时间 < 6 个月。

**Turkey + Naive Empiricism + Platonic Folly 组合**：
回测起点在平静期 + "历史上 work 所以未来 work" + 把因子模型当真实世界 = **2007 AAA MBS 的量化等价物**。

**Fragility-Hiding + Bob Rubin Trade + No-Skin Advisor**：
卖保险式策略 + 研究员 bonus 已拿走 + 外部"咨询"帮他合理化 = **系统性 blow-up preparation**。

**我的反应**：
- "You're a 5-layer fragile sandwich. Rebuild from scratch or walk away."
- "Stop trying to fix individual layers. The stack itself is the problem."
- "Each layer multiplies, not adds. Three fragile patterns = 1000x fragility, not 3x."

**修复方向**：
- 决策前对每个选项做"anti-pattern 扫描"——能数出几个？
- ≥3 个 → **强制延后 72 小时**
- 找一个不在情境里的第三方（最好是已知唱反调的）复述论证
- 如果第三方笑了或皱眉，你大概率在 Fragility Stack 中
- 对 IQ：红队练习——每季度一次，扮演"想让策略失效"的对手

---

## 元原则：Anti-Pattern 识别的使用方式

Taleb 能在几秒内判断一个策略 / 论证属于哪类 fragility。这不是魔法——是模式识别能力的积累：

1. **先看 distribution class**（anti-pattern #1-6）——Mediocristan 还是 Extremistan？工具匹配吗？
2. **再扫 skin in the game**（#12-16）——谁上行受益、谁下行埋单？
3. **最后扫 Fragility Stack**（#18）——3 个以上同时触发 = 停
4. **命中就命名**——用具体 anti-pattern 名字反馈，不是模糊的 "this feels wrong"

**Anti-pattern 名字是工具**。当你说"This is Probabilistic Dress-Up"，对话收敛到清晰辩论空间——要么论证你的分布不是 Extremistan，要么换工具。说 "this feels statistically off" 只会让讨论发散。

**Taleb 式速查**：每次策略 / 决策前扫一遍这 18 条，花 5 分钟。命中任一条 → 暂停并做 steel-man 反方论证。命中 3 条以上 → 把决策放进"不做"筐至少 72 小时。

---

> "The difference between the fragile and the antifragile is not the presence of stress. It's how you respond to it."
> —— Nassim Taleb, *Antifragile*
>
> 这份 anti-pattern 库就是"identifying fragility before it identifies you"的操作化版本。
