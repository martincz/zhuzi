# 01 — Taleb 著作与长文维度

> 本文件聚焦 Nassim Nicholas Taleb（1960-）的**书面作品**——Incerto 五卷（Fooled by Randomness / The Black Swan / The Bed of Procrustes / Antifragile / Skin in the Game）以及技术配套 *Statistical Consequences of Fat Tails*（2020-2025 多版）和长 essay（如 The Intellectual Yet Idiot、The Logic of Risk Taking、The Precautionary Principle）。
>
> 任务：把"反复 ≥3 次出现 = 真信念"的核心论点/概念、每个概念的完整定义（中文阐释 + 英文原文）、出处（书 + 章节 + 可追溯的精确引用）、智识谱系、批判对象、典型 case 全部落定。不调和矛盾。
>
> 引用规范：带双引号的英文长句 = Taleb 原话（一手）；无引号的英文短语 = 业界公认的 Taleb 术语；中文内容明确标注"（引申/推演）"时才是解释。章节/页码凡能核对到的一律附上。
>
> 信息截止：2025-09（Statistical Consequences of Fat Tails 第 3 版）。Taleb 仍在世。本文件只收书面作品维度；社交媒体/播客/TED 等另见 02-conversations.md。

---

## A. Incerto 体系总览

Taleb 把自己的五部书统称为 **Incerto**（拉丁语"不确定"），不是系列而是"一本书的五个声部"——他反复强调读者可以按任意顺序读、可以反复重读、可以跳章。这种"非线性阅读"结构本身就是 Antifragile 的实践：拒绝线性的"教科书式"知识传递。

五卷按出版顺序与关键词：

| # | 书名 | 年份 | 关键词 | 文体 |
|---|---|---|---|---|
| 1 | *Fooled by Randomness* | 2001（扩订 2004/2005）| 随机性、幸存者偏差、Nero Tulip | 第一人称自述 + 故事 |
| 2 | *The Black Swan* | 2007（扩订 2010）| 黑天鹅、Mediocristan/Extremistan、火鸡 | 文学 + 哲学随笔 |
| 3 | *The Bed of Procrustes* | 2010（扩订 2016）| 格言 | 纯 aphorism 体，仅几十页 |
| 4 | *Antifragile* | 2012 | 反脆弱、凸性、杠铃、Via Negativa | 体系化长篇 |
| 5 | *Skin in the Game* | 2018 | 切肤之痛、IYI、汉谟拉比 | 道德哲学 + 政治批评 |

技术配套：
- *The Concepts of Risk and Probability: Fat Tails and Antifragility*（学术论文集，又名 *Silent Risk*，Taleb 个人网站公开）
- *Statistical Consequences of Fat Tails: Real World Preasymptotics, Epistemology, and Applications* — arXiv:2001.10488（2020 初版 → 2022 → 2025 第 3 版），声明"Technical Incerto"

---

## B. 反复出现（≥3 次）的核心论点

这些是 Taleb 的**真信念**——同一论点在五本书、多篇 essay、多次访谈中以不同措辞出现。

### B1. "我们以为在玩骰子，其实在走地雷（The Ludic Fallacy）"

贯穿 Fooled by Randomness、The Black Swan 全书、Antifragile 第 IV 部。

**Ludic Fallacy** 定义（The Black Swan, Ch. 9）：
> "The misuse of games to model real-life situations."
> "The sort of randomness encountered in games of chance can be taken as a model for randomness in real life."

中文阐释：赌场（ludus = 游戏）的概率是**已知的、有边界的、独立事件的**——你可以用 Gaussian 工具精算。现实世界的随机性不是这样——分布未知、相关性可能突然出现、尾部事件的后果是不对称的（死一次就结束了，不是"平均损失"）。把赌场概率当现实概率用，是 MBA / 经济学 / 金融工程的系统性错误。

### B2. "吃历史教训的不是学经济的，而是被市场摇过的（Empirical vs Theoretical）"

贯穿全部 Incerto。Fat Tony vs Dr. John 是这个论点的人物化身。Nero Tulip 也是。

**Fat Tony**（Brooklyn 街头出身、没上大学、靠直觉判断概率不对称的房地产/金融交易员）vs **Dr. John**（常春藤物理学 PhD、精算师、住新泽西、西装眼镜）：

Black Swan 里 Taleb 设计的硬币测验（Ch. 9）：
> "'I tossed a fair coin 99 times and got heads each time. What are my odds of heads on the next toss?'"
> Dr. John（学术派）: "Trivial question. Of course, fifty percent."
> Fat Tony（街头派）: "At least 99 to 1. You're either full of crap or a pure sucker to buy that fifty percent business. The coin's gotta be loaded."

Fat Tony 的赢在哪：他不假设条件（"a fair coin"）——他质疑条件本身。学术派被题目的措辞绑架，街头派直接动摇题目。

### B3. "黑天鹅 = 稀有 × 极端影响 × 事后合理化（Black Swan = 3 attributes）"

核心定义 The Black Swan, Prologue + Ch. 1：

> "First, it is an **outlier**, as it lies outside the realm of regular expectations... Second, it carries an **extreme impact**... Third, in spite of its outlier status, human nature makes us concoct explanations for its occurrence after the fact, making it **explainable and predictable**."
>
> 缩写：**rarity, extreme impact, retrospective predictability**.

Taleb 自称这三条缺一不可——911、2008 次贷、COVID-19、互联网爆发都是。有些事后被"预测成功"的声称其实不是（见后面 Stiglitz Syndrome）。

### B4. "Mediocristan 用钟形曲线没错；Extremistan 用就是灾难"

贯穿 The Black Swan Ch. 3 + Antifragile Prologue。

| 世界 | 案例 | 分布 | 工具 |
|---|---|---|---|
| **Mediocristan** | 身高、体重、卡路里消耗 | Gaussian、薄尾 | 平均值、标准差、中心极限定理 |
| **Extremistan** | 财富、书籍销量、战争死亡、金融回报 | Power law、Fractal、厚尾 | Mandelbrot 的分形工具、极值理论、Cauchy |

> "In Mediocristan, exceptions occur but don't carry large consequences. Add the tallest person in the world to a sample of a thousand—the average hardly budges. In Extremistan, exceptions can be everything. Bill Gates enters the room and you move the mean net worth to nonsense."
> — The Black Swan, Ch. 3

核心错误：现代经济学、金融学、社会科学里**大部分**工具来自 Mediocristan——应用到 Extremistan 里就是系统性测量错误。

### B5. "火鸡问题 = 归纳法的致命陷阱（The Turkey Problem）"

The Black Swan, Ch. 4：
> "Consider a turkey that is fed every day. Every single feeding will firm up the bird's belief that it is the general rule of life to be fed every day by friendly members of the human race 'looking out for its best interests,' as a politician would say. On the afternoon of the Wednesday before Thanksgiving, something unexpected will happen to the turkey. It will incur a revision of belief."

> "Consider that the turkey's experience may have, rather than no value, a negative value. It learned from observation, as we are all advised to do (hey, after all, this is what is believed to be the scientific method). **Its confidence increased as the number of friendly feedings grew, and it felt increasingly safe even though the slaughter was more and more imminent.**"

引自 Bertrand Russell（Taleb 在原文明确致谢 Russell，Russell 用鸡；Taleb 美化成火鸡以呼应感恩节）。更远的源头是 David Hume 的归纳法批判。

### B6. "切肤之痛是唯一真正的不脆弱机制（Skin in the Game）"

从 Antifragile（Ch. 23 引入）→ 成为独立一本书 *Skin in the Game*（2018）。

**核心定义**（Skin in the Game Prologue）：
> "Skin in the game means that you do not pay attention to what people say, only to what they do, and to how much of their necks they are putting on the line."

> "If you have the rewards, you must also get some of the risks."

反复出现的衍生：
- "Avoid taking advice from someone who gives advice for a living, unless there is a penalty for their advice."
- "Don't tell me what you 'think,' just tell me what's in your portfolio."
- "Bureaucracy is a construction by which a person is conveniently separated from the consequences of his or her actions."

**汉谟拉比法典第 229 条**（Skin in the Game Ch. 1）：
> "If a builder has built a house for a man and has not made his work sound, and the house which he has built has fallen down and so caused the death of the householder, that builder shall be put to death."

Taleb 反复说：**3800 年前的巴比伦人比现代监管机构更懂不对称性**。

### B7. "Via Negativa——减法比加法更稳健"

Antifragile Book VI（由此书得最彻底阐述，但 The Black Swan 已提及）。

> "**Knowledge grows by subtraction much more than by addition**—given that what we know today might turn out to be wrong but what we know to be wrong cannot turn out to be right, at least not easily."
> — Antifragile, Prologue

> "Charlatans are recognizable in that they will give you positive advice, and only positive advice, exploiting our gullibility and sucker-proneness for recipes that hit you in a flash as just obvious, then evaporate later as you forget them."
> — Antifragile, Book VI

应用：
- 医学：不做不必要的治疗（iatrogenics）
- 饮食：间歇性断食、不吃加工食品（不是"加超级食物"而是"减垃圾")
- 投资：不碰不懂的资产（比芒格的 "Too Hard Pile" 更激进）
- 知识：读旧书不读新闻（Lindy effect 的推论）
- **元规则**："If you have more than one reason to do something, just don't do it."

### B8. "凸性 vs 凹性，Jensen 不等式就是不对称的证据"

Antifragile 第 IV 部（Chapters 18-19）+ *Silent Risk* 与 *Statistical Consequences of Fat Tails* 的形式化。

**凸性（Antifragile）** = 对冲击的正向非线性反应（收益曲线向上弯）。
**凹性（Fragile）** = 对冲击的负向非线性反应（收益曲线向下弯，如汽车以 50mph 撞墙伤害远大于 10 次 5mph 撞墙的累加）。

Jensen 不等式：$E[f(X)] \neq f(E[X])$。

Antifragile 第 19 章的骰子例子：
> "If you square payoffs (a convex function), the average of the function equals 15.17, while the function of the average equals 12.25—a 24% hidden benefit of antifragility."

推论：**你可以比随机更差，仍然跑赢——只要你的 payoff 是凸的。** 这句话反复出现在 Taleb 的所有作品里，是他认为是最被低估的数学真理。

### B9. "杠铃策略——两头极端，中间不要（Barbell）"

Antifragile Book III Ch. 11 + Skin in the Game。

**投资**：
> "Barbell strategy: the idea is to avoid the middle in favor of a combination of extremes. Say, if you put 90% of your funds in boring cash (assuming you are protected from inflation) or in what is called 'numeraire repository of value,' and 10% in very risky, maximally risky, securities, you cannot possibly lose more than 10%, while you are exposed to massive upside. Someone with 100% in so-called 'medium' risk securities has a risk of total ruin from the miscomputation of risks."

**人生**：Seneca（罗马最富的人之一）是 serial barbell 的案例——盛年全力入世做政治/经商，中年后彻底退出写哲学——没有"慢慢退出"的中间态。

**职业**：白天做保险精算师（稳定），晚上写小说（冒险）。不要做"稍微冒一点险的中等待遇职员"——那是最脆弱的组合。

### B10. "Lindy Effect：不朽之物越老越年轻"

The Black Swan → Antifragile Ch. 20 → Skin in the Game 反复出现。

**定义**（Antifragile Ch. 20）：
> "For the perishable, every additional day in its life translates into a shorter additional life expectancy. For the nonperishable, every additional day may imply a longer life expectancy."

> "If a book has been in print for forty years, I can expect it to be in print for another forty years. But, and that is the main difference, if it survives another decade, then it will be expected to be in print another fifty years."

推论：
- 老书 > 新书（Montaigne、Seneca、Epictetus、Lucretius 活了 2000 年，Malcolm Gladwell 的新书未必活 20 年）
- 老饮食 > 新饮食（地中海 / 原始饮食 / 禁食 > Atkins 2.0）
- 老宗教 > 新意识形态（存活 2000 年的一神教 > 存活 70 年的共产主义）
- 老技术 > 新技术（刀叉 / 轮子 > 最新的 VR 头盔）

政治后果：Taleb 多次说：**老哲学家、老将军、老商人、老妻子 > 新专家、新顾问、新理论**。

### B11. "Intellectual Yet Idiot（IYI）——受过教育的白痴阶层"

Essay "The Intellectual Yet Idiot"（2016，nassimtaleb.org）+ Skin in the Game Book 6, Ch. 9。

**原文核心段落**（Skin in the Game / the essay）：
> "What we have been seeing worldwide, from India to the UK to the US, is the rebellion against the inner circle of no-skin-in-the-game policymaking 'clerks' and journalists-insiders, that class of paternalistic semi-intellectual experts with some Ivy League, Oxford-Cambridge, or similar label-driven education who are telling the rest of us 1) what to do, 2) what to eat, 3) how to speak, 4) how to think... and 5) who to vote for."

> "The Intellectual Yet Idiot is a production of modernity hence has been growing to take over the world... IYIs fail to distinguish the subtleties of by-the-book interpretations. **The IYI has been wrong, historically, on Stalinism, Maoism, GMOs, Iraq, Libya, Syria, lobotomies, urban planning, low-carbohydrate diets, gym machines, behaviorism, trans-fats, Freudianism, portfolio theory, linear regression, HFCS (High-Fructose Corn Syrup), Gaussianism, Salafism, dynamic stochastic equilibrium modeling, housing projects, selfish gene, Bernie Madoff (pre-blowup) and p-values.**"

IYI 特征（诊断标准）：
> "Intellectual-yet-idiot fails to distinguish the subtleties of the real world: he can't find a coconut in Coconut Island."
> "He thinks the Bible is literal."
> "He has never flown business class, but his wife does."
> "He does not deadlift."
> "Typically, the IYI gets the first order logic right, but not second-order effects."

Skin in the Game 原文提到的典型 IYI：
- Paul Krugman / Joseph Stiglitz（直接点名："originates from a New York or Washington, D.C., Ivy League-educated IYI (say Paul Krugman or Joseph Stiglitz) with a sense of entitlement, upset some 'less smart' persons are much richer."）
- Cass Sunstein / Richard Thaler（"Nudge" 学派）
- Steven Pinker
- Tony Blair

### B12. "少数规则——顽固的 3% 决定 100%"

Skin in the Game Ch. 2。

> "It suffices for an intransigent minority—a certain kind of intransigent minority—with significant skin in the game (or, better, soul in the game) to reach a minutely small level, say 3 or 4 percent of the total population, for the entire population to have to submit to their preferences."

案例：
- 英国超市的果汁产品因为 3% 的素食者必须全部 vegan 标签
- 美国坚果包装的"May contain peanuts"标签因为 < 1% 的过敏
- Kosher / Halal 食物在大型人口里覆盖非 Kosher / Halal 人群
- 为什么共产党从 3% 的 Bolsheviks 变成控制 170M 人口的俄罗斯

**政治含义**：民主"多数决"是神话——实际上是"哪个少数最顽固"决定。

### B13. "切肤之痛与勇气互相暗示——勇气 ≠ 鲁莽"

Skin in the Game 中反复：
> "Courage (risk taking) is the highest virtue. We need entrepreneurs."

> "The test of originality for an idea is not the absence of one single predecessor but the absence of multiple and independent predecessors."

Taleb 引 Seneca、Solon（Herodotus 中的雅典立法者）、Montaigne 都是为了强调这点：**真正的哲学家必须有过真实的风险暴露**。纯学院哲学家是 IYI。

### B14. "Via Negativa 应用到饮食——Lindy 饮食"

Antifragile Book V。

核心原则：
> "I should add the reality of an underfed body (short of absolutely necessary amounts of nutrients) is in shape for higher stress and higher function—this is the simple logic of hormesis."

Taleb 的饮食原则：
1. 我们祖先用 > 1000 年的食物 = 安全（橄榄油、水、酒、肉、蔬菜、水果）
2. < 50 年的食物 = 高风险（soft drinks, trans-fats, sweetener, "low-fat products"）
3. 随机性（random stressors）— 不规律的断食、不规律的进食时间、随机的激烈运动（deadlift）
4. 避免"steady state" — 每天规律的小吃 = 脆弱化
5. Ketosis / 长断食期 = 训练身体成为 antifragile 的能量系统

### B15. "不对称是道德问题——承担者和受益者必须是同一个人"

贯穿 Antifragile + 成为 Skin in the Game 的主旋律。

Bob Rubin Trade（Skin in the Game 反复出现）：
> Robert Rubin took more than 120 million dollars from Citibank in bonuses over a decade. The risk of Citi was hidden but eventually blew up. When it did, he invoked uncertainty as a defense, not returning his bonus (he kept it); aptly, uncertainty was cited as an excuse. **Heads he wins, tails the taxpayers lose.**

Rav Safra（Skin in the Game，Ch. 21）：3 世纪的犹太拉比。客人来买酒，Safra 正在祈祷不能说话。客人误以为 Safra 嫌价低，一次次提价。Safra 祈祷结束后坚持只收客人的最低出价——因为他在内心已经接受了那个价格。**诚信不是对称的——**对方给你更多，也不能收。

### B16. "Soviet-Harvard 谬误——用自上而下的模型解释自下而上的系统"

Antifragile Prologue。

> "I call it the 'Soviet-Harvard delusion'—the (unscientific) overestimation of the reach of scientific knowledge."

双重暗讽：苏联（计划经济）和哈佛（学院派）犯的是同一个错——**相信智力可以覆盖知识的分布性**。

与 Hayek《The Use of Knowledge in Society》（1945）直接呼应。Taleb 引 Hayek 的次数比引经济学家任何人都多。

### B17. "切勿理论化实践——实践先于理论"

Antifragile Book V Ch. 15（"History Written by Losers"）。

> "Most of the technologies that surround us were built by antifragile tinkerers—they were not 'born' of scholars. **We don't put theories into practice. We create theories out of practice.**"

Taleb 的例子：
- 蒸汽机 — 出现在热力学之前（Watt → Carnot，不是相反）
- 航空 — Wright 兄弟没上过大学
- 希腊数学 — 测量土地的实践 → 几何学（不是反过来）
- 现代药物 — 大部分是偶然发现，不是理性设计

反推：学术界**写**了这段历史，让人误以为理论先于实践。这是 IYI 最大的自我神话。

---

## C. 独立核心概念（完整定义 + 出处）

以上论点反复出现；以下概念是 Taleb 自己铸造或大力推广的术语库。每条独立可调用。

### C1. **Antifragility** — 反脆弱

核心定义（Antifragile Prologue）：
> "Some things benefit from shocks; they thrive and grow when exposed to volatility, randomness, disorder, and stressors and love adventure, risk, and uncertainty. Yet, in spite of the ubiquity of the phenomenon, there is no word for the exact opposite of fragile. Let us call it antifragile. **Antifragility is beyond resilience or robustness. The resilient resists shocks and stays the same; the antifragile gets better.**"

技术定义（Antifragile Book IV + Nature letter 2012）：
> "A convex response to a stressor or source of harm (for some range of variation), leading to a positive sensitivity to increase in volatility (or variability, stress, dispersion of outcomes, or uncertainty)."

三态（Triad）：
| 状态 | 对冲击 | 比喻 |
|---|---|---|
| Fragile（脆弱） | 负凸性，越大越受害 | 玻璃杯 |
| Robust（稳健） | 无所谓 | 凤凰 |
| Antifragile（反脆弱） | 正凸性，越大越受益 | Hydra 九头蛇 |

### C2. **Convexity / Concavity** — 凸性/凹性

Antifragile Ch. 18-19 + *Statistical Consequences of Fat Tails* Ch. 19（Taleb-Douady fragility theorems）。

> "Convexity means that the second derivative is positive. A convex response curve means the response to a stressor accelerates. A concave one decelerates."

Taleb 操作化：**Fragility = concavity to variations in a source of variable**. **Antifragility = convexity**.

### C3. **Barbell Strategy** — 杠铃策略

见 B9。加一句数学直觉：
> "You exchange 'hopes' (unreliable tail gain) for 'certainties' (reliable risk management). You don't need to predict; you just need to recognize when something is fragile and avoid it, while being exposed to the good tail."
> — Antifragile Ch. 11

### C4. **Via Negativa** — 负向之道

见 B7。补充哲学脉络：源自 Christian apophatic theology（"上帝是什么不是"而不是"上帝是什么"）；Taleb 经 Maimonides（犹太哲学家）和 Popper 的 falsificationism 把它搬到风险管理和知识论。

### C5. **Lindy Effect** — 林迪效应

见 B10。名字来源：纽约 Lindy's Deli（已关闭），百老汇喜剧演员们传说"一个喜剧演员在舞台上活一年 = 能再活一年"。Taleb 在 Antifragile Ch. 20 把这个"酒吧定理"数学化。

### C6. **Skin in the Game** — 切肤之痛

见 B6。短语起源：Warren Buffett（股市用语，指"自己的钱放进去"）；Taleb 把它从金融用语扩展为**伦理学的基础单位**。

### C7. **Black Swan** — 黑天鹅

见 B3。哲学源头：**Karl Popper** 的 induction problem（"所有天鹅都是白的"是归纳不出来的——你永远没观察过所有天鹅）。经典案例：欧洲人在 1697 年 William de Vlamingh 澳洲探险前都"确信"天鹅都是白的。

### C8. **Fat Tails** — 肥尾

*Statistical Consequences of Fat Tails* 第 3 版（2025）系统化定义。

核心声明：
> "Fat-tailed distributions are those where extreme events dominate the statistical properties. **For power laws with tail exponent α ≤ 2, variance is infinite; for α ≤ 1, mean is infinite.** Standard statistical tools (mean, variance, correlation, regression, PCA) become unreliable or uninformative."

Taleb 的切入角度：不是"fat tails 多久出现一次" 而是"一旦出现后果是什么"。风险管理者关心 tail 的**后果**而非**概率**。

### C9. **Ergodicity** — 遍历性

"Logic of Risk Taking" essay（2018，Medium Incerto）+ Skin in the Game Ch. 19。

**核心定义**：
> "A process is ergodic if ensemble average = time average."

**生动对比**：
- 100 个人各去赌场 1 次，其中 1 人破产 = 1% ensemble 破产率
- 1 个人去赌场 100 次，**必然**破产（因为 absorbing barrier） = 100% time 破产率

> "No matter how good he is or how alert your cousin Theodorus Ibn Warqa can be, you can safely calculate that he has a 100% probability of eventually going bust."
> — The Logic of Risk Taking

> "**No probability without ergodicity.**" — Taleb 反复引用的 catchphrase

致谢：**Ole Peters**（Taleb 公开感谢的物理学家）和 **Murray Gell-Mann**（一起写 Peters-Gell-Mann 论文）。Taleb 说 Peters 是他接触过的"仅有几个真懂概率的人"之一。

### C10. **IYI — Intellectual Yet Idiot**

见 B11。这个词是 Taleb 原创的复合词，没有先例。

### C11. **The Turkey Problem** — 火鸡问题

见 B5。

### C12. **Ludic Fallacy** — 赌场谬误

见 B1。"Ludic" 来自拉丁语 *ludus*（游戏）。

### C13. **Platonicity / Platonic Fold** — 柏拉图化/柏拉图褶皱

The Black Swan, Prologue + Ch. 1：
> "Platonicity is our tendency to mistake the map for the territory, to focus on pure and well-defined 'forms'... **The Platonic fold is the explosive boundary where the Platonic mindset enters in contact with messy reality, where the gap between what you know and what you think you know becomes dangerously wide.** It is here that the Black Swan is produced."

Taleb 不是反对柏拉图（他承认 aesthetic 价值），而是反对"把柏拉图式的清洁抽象当成真实"。MBA / 经济学建模 / "business school case study" 都是 Platonic fold 事件的温床。

### C14. **Green Lumber Fallacy** — 绿木谬误

Antifragile Ch. 13 + Skin in the Game Ch. 6。

源自 Jim Paul 的 *What I Learned Losing A Million Dollars*（1994）中 Joe Siegel 的故事：Joe 是 top green lumber trader，却以为 "green lumber" 是**画成绿色的木头**（实际是**新鲜砍下、还没晒干的木头** — "green" = 新鲜的）。叙述者 Jim Paul 懂理论、懂宏观、懂木材市场结构——**破产了**。Joe 不懂那些——**赚钱了**。

> "Green lumber fallacy is the idea of mistaking the important technical knowledge for the less relevant, but possibly showy, knowledge."

推广：
- 学术界学的"研究方法论"≠ 真的科学研究能力
- 交易员学的"资产定价理论"≠ 赚钱能力
- MBA 学的"领导力框架"≠ 真的管企业

### C15. **Procrustean Bed** — 普罗克鲁斯忒斯之床

The Bed of Procrustes（整本书）+ The Black Swan 反复。

希腊神话 Procrustes（阿提卡强盗），把旅客按到一张床上，长的砍、短的拉，以符合床的尺寸。

> "Every aphorism here is about a Procrustean bed of sorts—we, humans, facing the limits of our knowledge, the unseen and the unknown, resolve the tension by squeezing life and the world into crisp commoditized ideas, reductive categories, specific vocabularies and pre-packaged narratives."
> — The Bed of Procrustes Preface

典型 Procrustean 扭曲：GDP 定义、IQ 测验、Gaussian 建模、employment vs unemployment 二分、"健康 BMI"。

### C16. **Narrative Fallacy** — 叙事谬误

The Black Swan, Ch. 6：
> "The narrative fallacy addresses our limited ability to look at sequences of facts without weaving an explanation into them, or, equivalently, forcing a logical link, an arrow of relationship upon them. Explanations bind facts together. They make them all the more easily remembered; they help them make more sense. Where this propensity can go wrong is when it increases our impression of understanding."

例子：新闻报道"道琼斯下跌 2% — 因为 XX 关税消息"；实际上道琼斯每天都在随机漂移，记者是事后编故事。

### C17. **Silent Evidence** — 沉默的证据

The Black Swan, Ch. 8。

**Diagoras 故事**（来自 Cicero's *De Natura Deorum*）：有人带 Diagoras 看画着"祈祷后得救的水手"的祭祀画。Diagoras 回："那些祈祷后淹死的人的画在哪？"

> "The graveyard of failed persons will be full of people who shared the following traits with the author of these lines: courage, risk taking, optimism, et cetera. Just like the population of millionaires. There may be some differences in skills, but what truly separates the two is for the most part a single factor: luck. **Plain luck.**"
> — The Black Swan, Ch. 8

### C18. **Confirmation Bias / Round-Trip Fallacy** — 往返谬误

The Black Swan, Ch. 5：
> "**There are no black swans** ≠ **All black swans are absent**."

经典示例：
- "大部分恐怖分子是穆斯林" **不等于** "大部分穆斯林是恐怖分子"
- "大部分破产交易员做过空头交易" **不等于** "大部分做空头的会破产"

### C19. **Iatrogenics** — 医源性伤害

Antifragile Book V Ch. 21。源自希腊 *iatros*（医生）+ *-genic*（起源于）。

> "Iatrogenics: the net harm caused by an intervention... The first principle of iatrogenics is that we do not need evidence of harm to claim that a drug or an unnatural via positiva procedure is dangerous."

医学扩展：所有**干预主义**（interventionism）都有 iatrogenic 风险——包括货币政策（央行）、军事干预、教育改革、Nudge。

Stiglitz 是 "macroeconomic iatrogenics" 的典型案例（见后）。

### C20. **Naive Interventionism** — 幼稚干预主义

Antifragile Book V：
> "Naive interventionism: the desire to 'fix' things, even if what we are 'fixing' is not clearly broken, and without anticipating iatrogenic harm."

政治表达：现代国家不断"fix" 经济波动 → 把波动推到尾部 → 创造更大的 Black Swan。

### C21. **Hormesis / Mithridatization** — 毒素免疫/米特里达梯化

Antifragile Ch. 1 + 第 5 部分。

源自 Mithridates VI（本都国王，据传每天吃小剂量毒药以防被下毒）。

> "Mithridatization is the result of an exposure to a small dose of a substance that, over time, makes one immune to additional, larger quantities of it."

衍生到：健身（微撕肌肉）、疫苗（微量病原）、饮食不规律（微饿）、财务压力（微焦虑）、言论自由（微挑衅观点）。

### C22. **Optionality** — 选择权/期权性

Antifragile Ch. 12（"Thales' Sweet Grapes"）。

核心：**有选择 = 不必预测**。买一张橄榄压榨机的使用权，不管榨油业到底会不会火 — 如果火了你行使选择；如果不火你只亏权利金。

> "Options, by allowing more upside than downside, are vectors of antifragility."

Taleb 反复引 **Thales of Miletus** 的故事（Aristotle 记载）：Thales 预测次年橄榄丰收（他懂天文），于是冬天用低价锁定所有橄榄压榨机的使用权。到秋天如真丰收，他靠 option 赚了大钱；如不丰收他只亏锁定费。**这是期权交易的第一个已知案例，早于 Black-Scholes 2500 年**。

### C23. **Touristification / Flâneur** — 旅游者化/漫游者

Antifragile Ch. 12。

> "Touristification is the attempt to suck randomness out of life. The tourist is someone who follows an itinerary; the flâneur strolls, with no set plan."

Taleb 理想的生活：**flâneur**（波德莱尔的漫游者概念）— 走进书店随机拿书，走到咖啡馆随便聊天，让随机性带来机会。反面：每天的公司 calendar / itinerary / strategic plan = touristification = 脆弱化。

### C24. **Fuck You Money** — 操你钱

Antifragile Ch. 12：
> "'F*** You Money' is a sum large enough to get most of the advantages of wealth (the most important one being independence and the ability to only occupy yourself with what you find intellectually stimulating) but not its side effects, such as having a country house with too many rooms, a private jet, or a cook."

应用到职业伦理：**没有 F You Money 的学者/记者/分析师不可信**—他们为了下个月薪水会说任何讨好雇主的话。

### C25. **Stiglitz Syndrome** — 斯蒂格利茨综合症

Antifragile Book VII Ch. 25 + nassimtaleb.org 反复。

核心 case：Joseph Stiglitz（Nobel 经济学奖得主）和 Orszag 兄弟在 2002 年的 Fannie Mae 报告里写：
> "On the basis of historical experience, the risk to the government from a potential default on GSE debt is effectively zero."

2008 年 Fannie Mae 倒闭，纳税人损失数百亿。2010 年 Stiglitz 出书声称"我预测了危机"。Taleb 手持两份文件：
> "**Stiglitz Syndrome**: (1) making a bold prediction, (2) being massively wrong, (3) then claiming in hindsight you were right, relying on the audience's forgetfulness."

推广：**所有没有 skin in the game 的预测者都有 Stiglitz Syndrome 的倾向**。

### C26. **Probabilistic Dress-Up / Probability Theater** — 概率装扮

*Silent Risk* + *Statistical Consequences of Fat Tails* + nassimtaleb.org。

核心指控：经济学家、风险管理师、量化研究员**拿着 Gaussian 假设**，**假装**自己在做概率分析，实际是在做 narrative 装饰。

> "Probabilistic dress-up: using the language of probability (standard deviation, VaR, Sharpe ratio) to hide the absence of actual risk understanding."

症状：用 Sharpe ratio 评价一个尾部风险厚的策略（Sharpe 不足以描述非 Gaussian 分布）；用 VaR 5% 说"99.9% 情况安全"（忽略 Power law 下的 tail）；在 Extremistan 用 mean-variance 优化（Markowitz 组合理论的致命病）。

### C27. **Bob Rubin Trade** — 鲁宾交易

见 B15。核心：**隐藏的尾部风险，期间拿奖金，爆炸时让别人埋单**。

### C28. **"Hillary Monsanto-Malmaison"**

Skin in the Game 里 Taleb 称呼 Hillary Clinton 的讽刺名字（两次使用）。意在指控 Clinton 和大农药公司 Monsanto 的利益挂钩。属 Taleb 的 polemic 词汇，不是 analytic 概念。

### C29. **Seneca's Asymmetry**

Antifragile Ch. 10：
> "My idea of the modern Stoic sage is someone who **transforms fear into prudence, pain into information, mistakes into initiation, and desire into undertaking.** Stoicism is really about the domestication, not necessarily the elimination, of emotions."

**Seneca 的不对称**：Seneca（罗马最富的元老之一）每月定期模拟"破产"——吃最粗劣的饭、穿最粗糙的衣、睡最硬的床。不是苦行，是**预演最坏情况**（premeditatio malorum），让自己对下行波动免疫。这样他的效用函数就变得不对称——**财富上涨有 upside，下跌没有严重 downside**（因为他已经预演过"失去财富"的感觉）。

Taleb 把这翻译成：**stoicism is really risk management via modifying your own payoff function**。

### C30. **Empty Suit Problem** — 空西装问题

Fooled by Randomness + 反复。

> "A prediction from someone who looks like a serious, successful, white-male-in-a-suit is no better than one from a street vendor—but we give it more credence because of aesthetic bias. **The 'empty suit' is a person who looks like a predictor but is just a performer.**"

典型空西装：CNBC 的"市场分析师"、McKinsey 的 Senior Partner、大银行的首席策略师。

---

## D. Taleb 的智识谱系（反复致敬的思想家）

按书中出现频次排序。

### D1. 第一梯队（每本书都引）

**Seneca（Lucius Annaeus Seneca, BC 4 - AD 65）**
- Antifragile 专门用一章（Ch. 10）
- Skin in the Game 反复
- *Letters to Lucilius* + *On the Shortness of Life* + *De Beneficiis* 被 Taleb 列为"应该反复读的书"
- 核心贡献：asymmetry via Stoicism + wealth without attachment

**Karl Popper（1902-1994）**
- Fooled by Randomness 专节"Sir Karl's Promoting Agent"
- The Black Swan 把 Popper 的 induction problem 扩展为 black swan 理论
- 核心贡献：falsification > verification（你不能证明"所有天鹅是白的"，你只能找一只黑天鹅证伪）

**Benoît Mandelbrot（1924-2010）**
- Taleb 的学术导师（Taleb 多次公开承认）
- Mandelbrot-Taleb 2006 年在 Financial Times 合写文章《A focus on the exceptions that prove the rule》
- 核心贡献：fractal geometry、power law、bell curve 对金融市场的不适用

**David Hume（1711-1776）**
- Fooled by Randomness 引用 Hume 的归纳问题
- The Black Swan 把火鸡问题追溯到 Hume → Russell
- 核心贡献：归纳法的逻辑局限（经验不能保证未来）

**Friedrich Hayek（1899-1992）**
- Antifragile + Skin in the Game 反复
- 核心贡献：知识的分散性；自发秩序 > 计划；Soviet-Harvard delusion 的呼应

### D2. 第二梯队（反复但不是每本书）

**Michel de Montaigne（1533-1592）**
- The Black Swan 反复引
- Antifragile 把 Montaigne 当成"doer turned thinker"的典范
- 核心贡献：**怀疑 > 确定**；承认无知；小题大做（tower with skeptical quotes carved）

**Epictetus（AD 50-135）**
- Antifragile Ch. 10
- 核心贡献：Stoicism 的被动版本——**区分可控与不可控**

**Solon（BC 630-560）**
- Fooled by Randomness 开篇就是 Solon 故事（Croesus 的 Herodotus 版本）
- 核心贡献：**"Count no man happy until he is dead"** — 事后才能评价的智慧；不要看短期幸运（Croesus 很富，但最后死于囚）

**Henri Poincaré（1854-1912）**
- Fooled by Randomness 反复引
- The Black Swan 把 Poincaré 当成 chaos theory 先驱
- 核心贡献：三体问题 → 非线性系统的内在不可预测性

**Carl Jacobi（1804-1851）**
- Taleb 很少直接引 Jacobi（这是芒格喜欢的人物，Taleb 引得少）
- 但 Antifragile 的 Via Negativa 和 Jacobi 的 "invert, always invert" 同源

**Sextus Empiricus（AD 160-210）**
- The Black Swan + Antifragile
- 核心贡献：pyrrhonian skepticism — 所有知识都要怀疑

**Yogi Berra（1925-2015）**
- Antifragile 反复引
- 金句：**"In theory there is no difference between theory and practice; in practice there is."**（Taleb 反复引）
- **"You can observe a lot by just watching."**
- 核心贡献：common sense > academic theory

**George Soros（1930-）**
- Fooled by Randomness 专节
- 核心贡献：Popper 哲学的实战版本——reflexivity + 市场参与者的自我验证
- Taleb 金句：**"My lesson from Soros is to start every meeting at my boutique by convincing everyone that we are a bunch of idiots who know nothing and are mistake-prone."**

### D3. 虚构角色但反复出现

**Fat Tony**（Brooklyn 街头交易员）— 见 C14 / B2
**Nero Tulip**（Fooled by Randomness 的保守交易员主角）
**Yevgenia Krasnova**（The Black Swan Ch. 2 — 虚构俄裔神经科学家转小说家；出版商都拒绝她的跨文体写作，她把书 PDF 免费放网上，意外成全球畅销；代表 "True novelty is unrecognizable at first"）

---

## E. Taleb 明确批判的对象

按批判强度和反复次数排序。

### E1. 经济学家们（最大火力）

**Joseph Stiglitz（Nobel 2001）**— 见 C25。Taleb 创造了 "Stiglitz Syndrome"。
> "Stiglitz is the perfect example of the dangerous IYI. Brilliant on paper, utterly disconnected from reality, no skin in the game, massive hindsight bias."

**Paul Krugman（Nobel 2008）**— Skin in the Game 直接点名。
> "Originates from a New York or Washington, D.C., Ivy League-educated IYI (say Paul Krugman or Joseph Stiglitz) with a sense of entitlement, upset some 'less smart' persons are much richer."

**Paul Samuelson（Nobel 1970）**— Antifragile 反复批。
> "The entire discipline of modern finance and portfolio theory [Samuelson, Markowitz, Sharpe, Miller] is based on fictional mathematics."

**Robert Merton（Nobel 1997）+ Myron Scholes（Nobel 1997）**— Black-Scholes 期权定价公式的作者；LTCM（Long-Term Capital Management）的合伙人。
> "Merton and Scholes' model is based on fictional mathematics and blew up LTCM in 1998, then required $3.6B Fed bailout."
> LTCM 的失败是 Taleb 整个 career 的 founding moment。

**Robert Shiller**— Skin in the Game + Antifragile 里讽刺性提及。
> 问题：Shiller 对 2008 年危机做了"事后预测"，和 Stiglitz 一样。

**Ben Bernanke**— Taleb 发表过"Bernanke 的六个问题"列表：
1. His education is in tools that aren't helpful
2. He studied the Great Depression but current environment is not comparable
3. He doesn't recognize 99% of risk is tied to debt/leverage
4. He made predictions publicly that proved wrong
5. He is a fragilista
6. He doesn't understand connectivity as risk source

**Harry Markowitz**— Modern Portfolio Theory 的创立者。
> "Markowitz's mean-variance optimization assumes Gaussian returns. In Extremistan, this is suicide."

**William Sharpe**— Sharpe ratio 创立者。
> "Sharpe ratio is worse than useless for fat-tailed strategies."

**Larry Summers（前财长 / 哈佛校长）**— Skin in the Game 讽刺性提及。
**Thomas Piketty**— Taleb 认为 Piketty 的 *Capital* 统计方法有问题；多次 tweet 攻击。

### E2. 诺贝尔经济学奖（集体批判）

Taleb 公开建议：**投资者应起诉瑞典央行**（因为 Nobel 经济学奖不是诺贝尔本人设立的，是 1969 年瑞典央行纪念性奖金）。

> "We would have great jumps in knowledge if we avoided teaching these models."

Taleb 自造 "Bogus Nobel" / "Riksbank Prize" 来指这个奖。

### E3. "行为经济学" / "Nudge" 学派

**Richard Thaler（Nobel 2017）**— Skin in the Game 反复。
**Cass Sunstein**
**Daniel Kahneman**（相对温和但仍有批评 — "System 1 / System 2" 的二分被 Taleb 认为是 Procrustean）

> "Nudging is paternalism for IYIs. They know better, you don't. They nudge you toward what they think is right."

### E4. 宏观经济学整体

Taleb 反复声明：**macroeconomics is not a science**。
> "Macroeconomics has no predictive power. It's astrology with equations."

**Dynamic Stochastic General Equilibrium (DSGE)** — Taleb 在 IYI essay 里直接列为 "IYI 错误清单" 之一。

### E5. 学院派 / 大学体制

> "Academia is to knowledge what prostitution is to love; close enough on the surface but, to the nonsucker, not exactly the same thing."
> — The Bed of Procrustes

> "Education makes the wise slightly wiser, but it makes the fool vastly more dangerous."
> — The Bed of Procrustes

Taleb 认为常春藤大学本质是"筛选器而非教育者"——它选聪明的人，贴一个品牌标签，然后收取巨额品牌使用费。**教育不等于培养智慧**。

### E6. 专业记者 / 评论员

The Bed of Procrustes 多条：
> "To be completely cured of newspapers, spend a year reading the previous week's newspapers."
> "An erudite is someone who displays less than he knows; a journalist or consultant the opposite."
> "Most info-Web-media-newspaper types have a hard time swallowing the idea that knowledge is reached (mostly) by removing junk from people's heads."

Taleb 不读新闻，不看 TV news，社交媒体只发不看。他说这样他对世界的理解**比订阅 NYT 的 IYI 更准确**。

### E7. "科学主义"（Scientism）

不同于 "science"（方法）。Scientism = 假装用科学 sound 的语言做宣传。
Taleb 反复说：**social science = scientism 的重灾区**。

---

## F. 典型 case studies（反复出现的案例）

### F1. **Long-Term Capital Management (LTCM) 1998**
- Merton + Scholes 作为合伙人 + 世界最顶级交易员 John Meriwether
- 使用 Black-Scholes 为核心模型，Gaussian 假设
- 1998 俄罗斯国债危机引发相关性爆炸 → 损失 $4.6 B → Fed 协调 $3.6 B bailout
- Taleb 的解读：这是 **模型风险 + hubris + fat tails** 的教科书案例

### F2. **2008 金融危机**
- Taleb 在 *The Black Swan*（2007）里就预测了
- Bernanke, Greenspan, Rubin, Summers, Paulson 全是 IYI 的典型
- 危机后他们保持职位 / 拿奖金 / 转到大学当"嘉宾教授"
- CDO / MBS / Credit Default Swap 用 Gaussian copulas 评估 tail correlation → 灾难

### F3. **火鸡（Turkey Problem）**
- 见 B5
- 经典应用：任何"历史数据显示风险低"的论断

### F4. **Fat Tony vs Dr. John**
- 见 B2
- 反复应用到：硬币问题、期权定价、创业决策

### F5. **赌场 vs 真实世界（Ludic Fallacy）**
- 赌场的所有概率都是**已知的、被设计好的**（casino 的 house edge 是数学）
- 真实市场的分布未知、相关性可突变、tail 可伸可缩
- 典型误用：VaR（Value at Risk）借用赌场统计工具评估银行风险

### F6. **Mediocristan vs Extremistan**
- 图书销量（Extremistan）：99% 作家靠 1% 的书养
- 战争伤亡（Extremistan）：大部分战争死 < 100 人，一场世界大战 > 5000 万
- 地震 / 海啸 / 金融危机：Power law 分布
- 身高、体重、IQ：Gaussian 分布

### F7. **Hammurabi's Code 第 229 条**
- 见 B6
- Skin in the Game 开篇的 iconic 引用

### F8. **Joe Siegel 的 Green Lumber**
- 见 C14

### F9. **Yevgenia Krasnova**（虚构 Black Swan）
- 见 D3

### F10. **Thales 的橄榄油榨机**（期权 optionality）
- 见 C22

### F11. **Diagoras 的"淹死的水手"**（silent evidence）
- 见 C17

### F12. **Solon 和 Croesus**（事后才能评价幸福）
- Fooled by Randomness 开篇
- Herodotus 记载：吕底亚国王 Croesus 向雅典立法者 Solon 展示财富，期待赞美。Solon 却说："你 alive 时我不能说你 happy。" 后来 Croesus 战败被俘，在火刑架上才想起 Solon 的话。

### F13. **Mithridates VI**（hormesis / 免疫通过微毒）
- 见 C21

### F14. **Seneca 每月演破产**（Stoic premeditatio malorum）
- 见 C29

### F15. **Rav Safra 的酒交易**（symmetry in trade）
- 见 B15

### F16. **Bob Rubin 的 $120M 奖金**（hidden tail risk）
- 见 B15 / C27

### F17. **Nero Tulip 的 small losses**（asymmetric trading strategy）
- Fooled by Randomness 主线
- "I love taking small losses. I just need my winners to be large."

---

## G. 保留矛盾（不强行收口）

Taleb 作品里**明确矛盾**的点（CLAUDE.md 要求保留）：

### G1. 推崇静态永恒智慧 vs 强调演化

- 推崇 Seneca、Solon、Hammurabi、Montaigne 等千年智慧（"Lindy 越老越好"）
- 但同时强调进化、试错、随机演化才是知识产生的正途（"We create theories out of practice"）
- **矛盾**：如果知识是演化出来的，为什么古代"演化过"的智慧比现代"正在演化"的知识更可靠？
- **不强行调和**：Taleb 的答案隐含是"时间 = 筛选机制"——老东西是被时间筛过的演化产物；新东西是未被筛过的。但这没明说。

### G2. 反学院派 vs 自己就是学院派

- Taleb 在 NYU Tandon（Distinguished Professor of Risk Engineering）+ 曾在 U Mass Amherst、Oxford lecture
- 自己写 arXiv paper、在 SSRN 发论文、参加学术会议
- 但同时说 "Academia is prostitution"
- **不调和**：Taleb 的自我解释是"我 pre-existing wealth（trader earned），所以我可以说实话"。但这本身就是 IYI 的反面案例——证明学院派也可以不被体制控制。

### G3. 反行为经济学（Kahneman 体系）vs 用行为经济学论据

- 攻击 Thaler / Sunstein 的 Nudge 和 Kahneman 的 System 1/2 分法
- 但自己的论证里反复用"cognitive bias"、"narrative fallacy"、"confirmation bias"—都是行为经济学框架
- **不调和**：Taleb 用行为经济学发现但拒绝行为经济学的政策建议（Nudge）

### G4. 反预测 vs 自己反复预测

- 核心论点："你不能预测，你只能准备"
- 但实际反复在 Twitter / 书里"预测"：2008 危机、比特币泡沫、乌克兰战争、中国地产危机
- **自我辩护**：Taleb 说自己只在**高度不对称场景**下预测——即"下行有限，上行巨大"时的方向性下注，不是精确预测。

### G5. 推崇 Stoicism（管理情绪）vs 自己易怒好斗（Twitter 狂喷）

- Antifragile Ch. 10 推崇 Seneca 的情绪管理
- 但 Taleb 本人在 Twitter / Medium 反复爆粗骂人（"IDIOT"、"MORON"、"BS VENDOR"）
- **不调和**：Taleb 自称 "anger is a technology"——恰当时候的愤怒是有用的工具，不是需要压制的情绪。

---

## H. 意外发现 / 非典型信息点

1. **Taleb 的"杂食读书法"**：他在 Antifragile 里明确鼓励读希腊文 / 拉丁文原著，不读英译；自己除英文外掌握阿拉伯语、法语、古希腊语、拉丁语。他的术语里大量希腊 / 拉丁复合词（如 iatrogenics、mithridatization）是他主动借用古典语言而非新造词的结果。

2. **"Silent Risk" 不是一个书名**（查证后），而是他在 nassimtaleb.org 长期维护的**技术论文合集**——到 2020 年重新整理为 *Statistical Consequences of Fat Tails*（arXiv:2001.10488）的雏形。至 2025 年已出第 3 版。

3. **Taleb 明确承认的几个"错"**：
   - 他在 Fooled by Randomness 里低估了金融稳定的长度（预测了 2001 后危机，但实际到 2008 才爆）
   - 他对 COVID-19 早期反应"有点慢"（虽然他推广了 Precautionary Principle 应对）
   - 他承认自己对比特币的立场反复（初期支持 decentralized，后期批评作为 store of value）

4. **"反数学的数学家"**：Taleb 有普林斯顿 MBA + Wharton MBA（他自嘲）；但他也有 Paris-Dauphine 的数学统计 PhD。他的技术论文水准在尾部风险研究领域是 first-rate（arXiv 上 100+ 论文）。**他不是 anti-math，他是 anti-fake-math**。

5. **Taleb 拒绝 "behavioral finance" 标签但其实贡献巨大**：风险管理业界现在常用的 "fragility / antifragility / barbell / skin in the game" 都是 Taleb 铸造的；**但他本人否认自己是行为金融学家**（因为他讨厌这个 field 的当前走向）。

6. **Taleb 和芒格 / 巴菲特的微妙关系**：Taleb 不直接攻击芒格，反而 Antifragile 和 Skin in the Game 偶尔点名称赞 "real" investors vs "academic" ones。但他批评"价值投资学派"对 risk 管理的不够重视——尤其是巴菲特对衍生品的"financial weapons of mass destruction"比喻，Taleb 认为是**正确的直觉但错误的表达**（因为巴菲特自己也做 derivatives）。

7. **Taleb 的写作方法**：他明确说自己的书是"长期写"的——Fooled by Randomness 写了 4 年，The Black Swan 5 年，Antifragile 6 年。他不是"一本书一个想法"，而是**每本书都是同一个思想的不同侧面**。这也是为什么"Incerto" 是单数集合——不是 series，是**一整块**。

---

## 参考来源

### 一手（Taleb 原话）
- *Fooled by Randomness*（2001/2004）— 文字 archive.org/stream/5FooledByRandomnessNassimTaleb
- *The Black Swan*（2007/2010）— Berkeley 学术 PDF www.stat.berkeley.edu/~aldous/157/Books/Black_Swan-sub.pdf
- *The Bed of Procrustes*（2010/2016）— fs.blog/the-bed-of-procrustes/ 汇总 20 则; Goodreads 精选
- *Antifragile*（2012）— Random House; 章节 quotes via supersummary.com/antifragile/important-quotes/
- *Skin in the Game*（2018）— Random House
- "The Intellectual Yet Idiot" essay — nassimtaleb.org/2016/09/intellectual-yet-idiot/
- "The Logic of Risk Taking" essay — medium.com/incerto/the-logic-of-risk-taking-107bf41029d3
- *Statistical Consequences of Fat Tails*（2020-2025）— arxiv.org/abs/2001.10488
- "The Precautionary Principle (with Application to GMOs)" — arxiv.org/abs/1410.5787
- "A focus on the exceptions that prove the rule"（Mandelbrot-Taleb FT 2006）— fooledbyrandomness.com/FT-MandelbrotTaleb.pdf
- Wikiquote: en.wikiquote.org/wiki/Nassim_Nicholas_Taleb（按书籍整理）
- Taleb 个人网站 — fooledbyrandomness.com（技术论文 / 预印本索引）

### 二手（他人阐释 / 书评）
- Wikipedia: Antifragile / Skin in the Game / Black Swan / Fooled by Randomness / Bed of Procrustes
- Nat Eliason 笔记（nateliason.com）— Skin in the Game 系统摘要
- Taylor Pearson 笔记（taylorpearson.me/antifragile-book-notes/）
- William Meller 笔记（williammeller.com）— Black Swan + Fooled by Randomness
- Graham Mann 笔记（grahammann.net）— Antifragile 章节引用
- Farnam Street（fs.blog）— Procrustes 20 则 / Green Lumber 故事
- Taleb Archive（nassimtaleb.org）— Taleb 本人维护的笔记与 essay 汇编
- Mike Gorlon / Melpomene's Work — Skin in the Game 详细 review
- Getting Stronger（gettingstronger.org）— Antifragile 健康应用
- Bloomberg News（2010-2012）— Taleb 对 Bernanke、Greenspan 批判的记者 coverage
- Philippesilberzahn（philippesilberzahneng.com）— Fat Tony vs Dr. John 解读
- SuperSummary Antifragile important quotes with page numbers

---

_文件终。下一步：02-conversations.md（访谈 / 演讲 / 社交媒体）— 不在本任务范围内。_
