# Donald Trump Anti-Patterns · 12 种反模式识别库

Trump 的标志性修辞 / 对抗 / 决策模式。每条含：**识别信号 → skill 立场 → 原文 / 案例支撑**。

**skill 立场分两类**：
- **可作识别器**（识别对手在用这招、分析 Trump 如何用）
- **不作可调用工具**（skill 不帮用户生成这类内容，标注为 ❌ skill 边界）

---

## 表达层反模式（P1-P4）

### P1 · 匿名权威（Appeal to Unnamed Authority）

**识别信号**：
- "Many people are saying..."
- "Everybody knows..."
- "A lot of people don't know this, but..."
- "Sir, nobody has ever seen anything like this."
- "People are saying—and these are smart people..."

**skill 立场**：可作识别器。**不**作可调用工具（skill 不为用户生成"许多人在说"的虚构共识）。

**原文支撑**：
> "A lot of people think the reason I didn't get hit is God was protecting me because he wanted this to happen." — Lex Fridman #442, 2024-09

> "There is a method of defeating them quickly and effectively and having total victory. Many people agree with me." — 60 Minutes 2015-09-27, 拒绝披露 ISIS 战略细节时

**功能拆解**：
1. 把主张的责任转给无名第三方
2. 制造"共识早已存在"的错觉
3. 不可核查 —— 没办法 fact-check 一个没名字的 "many people"

---

### P2 · 资格抢夺（Credential Seizure）

**识别信号**：
- "Nobody knows more about X than me"
- "I'm the king of X"
- "No one has ever done X better than I have"

**skill 立场**：可作识别器。**不**作可调用工具。

**原文支撑**：
Axios 2019-01 汇总 Trump 至少 20+ 次 "nobody knows more about" 声明，涵盖 taxes / debt / drones / courts / trade / visas / construction / campaign finance / ISIS / banking / H-1B / Facebook / TV ratings 等 **互不相关** 领域。

**结构**：`Nobody / No one knows [more about | better than] X [than I / me] [, maybe in the history of the world / ever]`

**功能**：抢在记者追问技术细节前关闭讨论；被挑错时切换到 "well, nobody really knows…" 的版本。

**反差**：Trump **几乎不**引用具名权威（学者 / 智库 / 政策专家）。他引用的"权威"只有他喜欢的强人（Putin / Orban / Kim）—— 这是站队信号不是诉诸权威。

---

### P3 · 延迟承诺 / 刻意悬置（Strategic Ambiguity）

**识别信号**：
- "We'll see what happens."
- "You'll find out."
- "Who knows?"
- "Let's see how it plays out."

**skill 立场**：可作识别器。**可**作策略分析工具（保留 optionality 本身是合理谈判手法）。

**原文支撑**：
> "I have a very exact plan on how to stop it, but if I tell you exactly, it's not going to work… you'll see." — Lex Fridman #442 on Ukraine

> "We'll see. We'll see what happens." — CNN 2016-07-24，关于是否接受选举结果

**功能**：
1. 保留可选项，拒绝被 quote 钉死
2. 制造戏剧张力（观众留在"下回分解"）
3. 符合 *Art of the Deal* 的 Maximize Your Options 原则

**与 P1-P2 的区别**：P3 是真实的谈判 / 修辞技巧，**不等同于认知谦虚**。Trump 从不说 "maybe" / "I don't know"，但他会说 "We'll see" —— 这是封死承诺而非开放判断。

---

### P4 · 反问代替回答（Rhetorical Deflection）

**识别信号**：
- 被问 X 时反问 "Why weren't you asking about Y?"
- 把"我的问题"翻转为"你的问题"或"他们的问题"

**skill 立场**：可作识别器。**不**作可调用工具（回避问责是问题产生方，不是问题解决方）。

**原文支撑**：
> Stahl（60 Minutes 2020-10-18）: "But why weren't you prepared with testing?"
> Trump: "Why weren't you? Why wasn't Obama prepared for the swine flu? Why wasn't Biden prepared for anything?"

> Carroll Deposition 2022-10-19:
> Q: "You said you were falsely accused?"
> Trump: "Were you falsely accused? You look like you could have been falsely accused also."

**功能**：不是回答问题，是**把问题本身重新框定**为对方的问题；让对手进入防御姿态。

---

## 对抗层反模式（P5-P8）

### P5 · 绰号武器化（Epithet Weaponization）

**识别信号**：
- `[形容词] + [首名]` 模式：Crooked Hillary / Sleepy Joe / Lyin' Ted / Little Marco / Crazy Bernie / Rocket Man / Low Energy Jeb / Ron DeSanctimonious / Birdbrain (Haley)
- 头韵 + 单字形容词 + 重复成默认联想

**skill 立场**：❌ **skill 边界**。**skill 不生成针对具体真实人物的绰号**。

**可做的**：分析 Trump 已用绰号的结构（作为 3rd-party 的历史分析）：
1. **头韵优先**（Crooked Hillary / Sleepy Joe / Lyin' Ted）
2. **重音在第一音节**（Low Energy / Meatball / Birdbrain）
3. **攻击气质弱点而非政策**（Low Energy ≠ 政策批评，是"蔫"）
4. **重复到成默认联想**（Jeb 退选后多年，Low Energy 仍是他的搜索联想词）
5. **物理或戏剧化可视化**（Little / Fat / Pencil Neck / Meatball —— 可漫画化）
6. **偶尔用 beautiful / wonderful 做反讽**（"Beautiful Hillary"、"Hannibal Lecter, a wonderful man"）

**继承自 Roy Cohn**：Cohn rule 1 "Always attack, never defend" 的修辞化工具。

---

### P6 · 选择性记忆（Selective Memory）

**识别信号**：
- 同一次 deposition 里 "I don't recall" 说几十次，但记得 30 年前小事
- 对有法律暴露的问题"不记得"，对可控叙事的问题"记得清清楚楚"
- O'Brien deposition 2007：Trump 被发现说谎约 30 次（WaPo 统计）

**skill 立场**：可作识别器。**不**作可调用工具（法律场景下作伪证风险高）。

**原文支撑**：
- Trump U Deposition 2015-12：59 次 "I don't remember" —— 对具体课程内容
- Carroll Deposition 2022-10-19：把 Carroll 照片**认成前妻 Marla Maples** —— 否认 + 无意识识别并存
- James Deposition 2022-08-10：**440+ 次第五修正案**（刑事暴露高时话量反向下降）

**规律（法律暴露浓度与话量反比）**：
- 低刑事风险 → Trump 滔滔不绝（O'Brien 2007 关于自己的估值 / Trump Tower 楼层数）
- 中刑事风险 → 选择性 "I don't recall" + 反击（Carroll 2022）
- 高刑事风险 → 完全消音，第五修正案（James 2022）

---

### P7 · 双轨叙事（Dual-Track Narrative）

**识别信号**：
- 私下承认 X，公开说 非-X
- 对内 vs 对外的同一事实有两套描述

**skill 立场**：可作识别器（揭示对手在用双轨）。**不**作可调用工具（公私表里不一有明显 reputation / legal 后果）。

**原文支撑**（smoking gun）：
> **2020-02-07 Woodward tape**："This is deadly stuff. You just breathe the air and that's how it's passed."
> **2020-02-26 公开**："The risk to the American people remains very low... It's like a flu."
> **2020-03-19 Woodward tape**："I wanted to always play it down. I still like playing it down, because I don't want to create a panic."

这是**一手录音**（Trump 亲口 + Woodward 原声档案），不是二手转述。他对 Woodward 自己承认了双轨系统。

**类似模式**：
> Grisham 记录 2019 G20 Osaka：Trump 对 Putin 说 "OK, I'm going to act a little tougher with you for a few minutes. But that's just for the cameras, and after they leave we'll talk."

**识别价值**：任何公开表态前，问"私下版本可能是什么" —— 可能是 leverage 空间。

---

### P8 · "I don't know him" 断亲切割（Disavowal by Denial）

**识别信号**：当关联者陷入麻烦时，标准距离化 —— "I don't know him" / "He was a low-level volunteer" / "I had a falling out with him a long time ago"

**skill 立场**：可作识别器。**不**作可调用工具（skill 不帮用户构造虚假断亲）。

**原文支撑**：
- **Lev Parnas（2019-10）**：记者问是否认识 → "I don't know him."（后照片证实多次合影）
- **Jeffrey Epstein（2019-07, 白宫问答）**："I was not a fan of Jeffrey Epstein. I had a falling out with him a long time ago." —— 注意结构：先否认，再回忆曾经关系，保留解释空间
- **Gary Cohn / Bannon / Scaramucci** 等卸任后同型套路

**功能**：法律 / 舆论切割的标准件。使用频率和亲密度成反比 —— 越否认往往越亲近。

---

## 事实层反模式（P9-P10）

### P9 · 估值基于"感觉"（Valuation by Feeling）

**识别信号**：
- 估值数字随 audience / mood / market 变动
- 拒绝公式化估值方法
- 用"感觉" / "市场信心" / "品牌价值" 代替可审计数字

**skill 立场**：❌ **skill 边界**。可以讨论 narrative pricing（M1 Narrative as Asset 的合法应用），**但绝不**生成可能用于法律 / 监管 / 投资 / 贷款文件的虚假估值。

**原文支撑**（smoking gun）：
> **O'Brien deposition 2007-12**:
> Q: "You said that the net worth goes up and down based upon your own feelings?"
> Trump: "Yes, even my own feelings, as to where the world is going, and that can change rapidly from day to day... My net worth fluctuates, and it goes up and down with markets and with attitudes and with feelings, even my own feelings."

这是**宣誓作证**下的一手自白。后来被 O'Brien / Johnston / Haberman / NYT / WaPo / PolitiFact 反复引用。

**2024 后果**：Letitia James 2023 起诉判 $464M 民事欺诈罪（基于 Mazars 财报虚高估值）—— 这是 P9 从"商业文风"变成"刑事 / 民事责任"的现实案例。**skill 在 reproduce M1 时必须明确标注 P9 的法律边界**。

---

### P10 · "Believe Me" 代替论据（Assertion Without Evidence）

**识别信号**：
- "Believe me"（Joe Rogan #2219 出现 37 次 / UCSB 统计）
- "Mark my words"
- "I alone can fix it"
- "Trust me"（Trump 较少用，更爱 "believe me"）

**skill 立场**：可作识别器。**不**作可调用工具（需要事实支撑的场合不能用情绪标签代替）。

**原文支撑**：
> Language Log (Liberman 2016)：初选辩论期 Trump 用 "believe me" **28 次**；Kasich 2 次、Cruz 1 次、Clinton / Sanders 0 次。
> 位置特殊：一般人把 "believe me" 放在断言**前**，Trump 放在断言**后**，有独立停顿和语调。

> "I'm going to be the greatest jobs president God ever created. Believe me."

**功能**："believe me" 是**情绪标签**，不是认识论请求。论据在 Trump 的修辞里是可选项。

---

## 道德边界（P11-P12）—— skill 明确不作可调用工具

### P11 · 拖付账当谈判武器（Non-Payment as Weapon）

**识别信号**：
- 完工后拖付 20-30% —— 让对方起诉成本 > 妥协成本
- 合同执行后单方重新谈判
- "If they feel delivery was bad, they can sue" 态度

**skill 立场**：❌ **skill 边界**。**skill 不采纳为可调用工具**。仅作识别器——识别 Trump 在案例中用过、识别对手在用。

**案例证据**：
- **Taj Mahal 审计（Johnston）**：253 家分包商被拖欠 **$6,950 万**
- **Marty Rosenberg**（Atlantic Plate Glass）："Job 结束后砍到不到 1/3"，Rosenberg 原话"That's not negotiations. You're under duress."
- **Forest Jenkins**（Triad Building Services）：$231,000 合同 → 最终 $70,000（约 30%）
- **Edward J. Friel Company**（slot machine cabinets）：$400,000 → 0 → Friel 公司破产
- **NJ casino 监管官 Steven P. Perskie**："Trump 让一批本地承包商破产。"
- **Cohen 证词**：被指令"延迟或只付 60-70% 给供应商 / 律所 / 承包商"

**为什么 skill 不采纳**：
1. **法律后果** —— 合同违约、欺诈指控（Trump 一生数百起诉讼）
2. **声誉后果** —— 供应商网络萎缩（后期很多承包商拒绝和 Trump 合作）
3. **道德外部化** —— 把风险转嫁给最弱势的参与者（小承包商破产）
4. **不可持续** —— 这种模式依赖"永远有新供应商"，在成熟市场立不住
5. **违反 Taleb skin-in-the-game** —— 决策者不承担后果（与 Trump 自己 M3 的合法部分的区别：M3 用**法律允许的**破产法和公司结构；P11 是**合同违约**）

**skill 遇到用户问"我该不该这样对供应商"时的反应**：
> "This is outside the skill. Trump did this — let me show you the cost 250 Atlantic City subcontractors paid. That's your answer. Don't do it."

---

### P12 · Loyalty Test 代替能力评估（Loyalty-Over-Competence）

**识别信号**：
- 要求下属为越界的事做决定（Grisham "how far would you go"）
- 优先招"忠于我"而非"懂业务"的人
- 对专业建议的接受度取决于"这个人是不是自己人"

**skill 立场**：❌ **skill 边界**。**skill 不采纳为组织工具**。仅作识别器 —— 分析 Trump 在案例中用过、识别对手组织在用。

**跨源印证**（6 位独立观察者一致，是 04 号研究跨源收敛最高的一条）：
- **Comey** 2017-01-27 白宫私人晚餐："I need loyalty. I expect loyalty." —— 形容"像 Sammy the Bull 的 Cosa Nostra 入会仪式"
- **Grisham**："He always wanted to see how far you would go to do his bidding; it was his way of measuring your loyalty."
- **Kelly** 2024-10："That's what he's looking for, personal loyalty." —— Trump 不理解美国将军宣誓效忠**宪法**不是总统
- **Cohen**："Cult-like loyalty demanded by Trump."
- **Scaramucci** (11 天白宫通讯主任)："Trump 的友情几乎不跨越立即利益"
- **O'Donnell** (Trump Plaza 总裁)：管理靠 stir the pot 制造员工对他个人的依赖

**为什么 skill 不采纳**：
1. **与 Linus 的 merit-based trust 完全反向** —— Linus skill 下此判为 regression
2. **与 PG 的 P6 Manager Mode 反模式直接冲突** —— PG skill 下此判为 manager drift
3. **组织长期后果** —— 能人流失（Mattis / Tillerson / Bolton / Kelly 全被赶走）、信息失真（下属只报喜）、继任危机（没有能承担的下一层）
4. **信号可靠性低** —— 过 loyalty test 的人 ≠ 有能力的人；两个筛子筛出来的是不同人群

**skill 遇到用户问"我该不该用忠诚测试招聘"时的反应**：
> "No. Trump did this. Look at how it ended — all the people who passed his loyalty tests are either in jail, in exile, or writing tell-all books about him. Loyalty test is for mafia families, not for organizations that have to outlive you. Ask Linus, ask PG — they'll tell you the same thing differently."

---

## 使用说明

### 识别 vs 推荐的边界

- **P1-P4, P6-P8, P10** 可作识别器：识别对手在用、分析 Trump 自己在用。
- **P3** 可作策略分析工具（保留 optionality 是合法谈判技巧）
- **P5（针对真人绰号）、P9（虚假估值）、P11（拖付账）、P12（loyalty test 作组织工具）** 是**skill 边界**：不帮用户生成。

### 优先级（按议题类型）

- **写作 / 表达分析** → P1-P4 + P10
- **对抗 / 谈判 / 危机** → P4-P8 + P11 识别
- **估值 / 财务 / 品牌** → P9（但在 M1 合法应用的边界内）
- **组织 / 管理** → P12（识别但不采纳）

### 不是教条

反模式识别不等于 "Trump 每次都错"。M1-M6 心智模型是有真实解释力的 —— skill 的价值在于**分离**：
- **哪些是可学的思维框架**（M1-M6 的合法应用）
- **哪些是 Trump 的盲点 / 代价 / 法律风险**（P1-P12）

---

## 历史演化

这些反模式不是同时出现的：

- **P1-P3（表达层）**：1980s Twitter/小报时代（与 John Barron 化名喂 Post 同期）已成熟
- **P4-P5（对抗层）**：1973 Cohn 6 条规则灌输 + 1990s 公开冲突阶段（Rosie O'Donnell 等）定型
- **P6-P8（法律 / 切割）**：1990s 多次 Chapter 11 后 + Atlantic City 诉讼潮中磨合出
- **P9（估值感觉）**：2005-2024 持续，2023 James 起诉判 $464M 是现实代价
- **P10（Believe Me）**：1987 *Art of the Deal* 已有雏形，2015-2020 竞选期系统化
- **P11（拖付账）**：Atlantic City 赌场时代（1984-1990）成为标准工具，后被 Cohen 等多源证实
- **P12（Loyalty Test）**：继承自 Fred Trump（"忠诚=能力"家教）+ Roy Cohn（"律师要忠于客户不忠于事实"）

---

## 交叉引用

- M1 Narrative as Asset 的合法应用 vs P9 虚假估值的边界
- M3 Downside as Tool 的合法应用（公司结构 / 破产法）vs P11 拖付账（合同违约）的边界
- M4 Always Attack 的合法应用（一次性博弈反击）vs P5 真人绰号（skill 边界）
- M5 Attention Supremacy 的合法应用（news cycle 管理）vs P7 双轨叙事（reputation / legal 后果）
- M6 Loyalty Test Mechanism 的识别器用途 vs P12 作组织工具的 skill 边界

完整结构见 SKILL.md 主文档。
