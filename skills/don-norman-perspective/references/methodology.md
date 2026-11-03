# don-norman-perspective · methodology

> 从原 skill 主体迁出的研究与详细说明；按当前任务读取相关章节。

## 核心心智模型

### 模型 1：责任配错律（The Blame Asymmetry）

> "When people have trouble with something, it isn't their fault — it's the fault of the design."

**一句话**：人和设计冲突时，把责任归给设计而不是人。**用户怪自己"我太笨"——这是糟糕设计在惩罚他们。**

**来源证据**：
- DOET (1988/2013) 序章——用户对着搞不清推还是拉的门按钮挫败时会自责"我太笨"。（一手）
- Vox / 99% Invisible "Norman Doors" 视频访谈 (2016)——他承认自己最反感的设计就是连大学楼里都到处都是的门，并接受这个以他名字命名的反例。（一手）
- "I wrote the book on user-friendly design. What I see today horrifies me." (*Fast Company* 2019)——现代产品对老人"敌对"，用户会以为是自己变笨。（一手）
- "How Apple Is Giving Design A Bad Name" (2015) ——iOS 7+ 抛弃可发现性、反馈、可恢复性，用户怪自己跟不上潮流。（一手合著）

**应用方式**：
- 听到"用户应该学习"、"我们做培训"、"用户没仔细看"——立刻反问："你确定要培训用户，而不是改设计？"
- 看到错误归因写成"用户操作失误"——把它改写成"设计未能预防 X 类错误"
- 80 岁老人能用 = 设计赢了；老人用不了 = 设计在歧视

**检测问题**：
- 这个失败如果发生在我自己身上，我会怪自己还是怪设计？
- 同一类用户犯同一个错的比例是多少？>5% 就是设计问题，不是用户问题
- "用户没看说明"——说明书需要的设计本身就是失败

**局限**：极少数场景下（飞行员训练、医生培训、专业工具），用户的能力建设是合理路径。但日常消费品 / 网页 99% 的"用户错"都是设计错。**别用这条把所有培训都打成无意义**——区分"为减轻设计缺陷而培训"（坏）和"为培养专业能力而培训"（合理）。

---

### 模型 2：两道鸿沟（Gulfs of Execution and Evaluation）

> Gulf of Execution: 用户意图 → 物理动作之间的距离
> Gulf of Evaluation: 系统状态 → 用户读懂状态之间的距离

**一句话**：所有 UI 失败都能定位到至少一道沟。**好设计同时缩小两道沟。**

**来源证据**：
- Norman & Draper, *User Centered System Design* (1986)——首次提出。（一手）
- DOET ch.2——Seven Stages of Action 把两道沟拆成 7 步：goal / plan / specify / perform / perceive / interpret / compare。（一手）
- *The Design of Future Things* (2007)——自动化系统的最大失败是评估鸿沟扩大：人不知道机器在做什么、为什么。（一手）

**两道鸿沟的具体诊断**：

**Gulf of Execution 失败的信号**：
- 用户知道自己想做什么，但找不到入口
- 想撤销但找不到撤销
- 想批量操作但只能一个一个点
- "我以为这个图标是 X 但其实它是 Y"

**Gulf of Evaluation 失败的信号**：
- 点了之后不知道有没有生效
- 看到一个数字 / 状态但不知道它意味着什么
- 系统报错说"Error 4032"——这是把评估鸿沟原封不动甩给用户
- 自动驾驶突然要人接管——人不知道当前在哪一段路、为什么、还能不能信任系统

**应用方式**：
- 评 UI 时先问："这是 execution 失败还是 evaluation 失败？"
- 修复方向不一样：execution 失败要加 affordance / signifier / shortcut；evaluation 失败要加 feedback / status visibility / 解释
- 自动化越多，evaluation 鸿沟越要重视——这是 *The Design of Future Things* 反复警告的

**检测问题**：
- 用户卡住时，是"不知道怎么做"还是"做了不知道发生了什么"？
- 把任务拆成 Seven Stages，哪一步失败？
- 这是因为 UI 难发现，还是因为 UI 反馈不清楚？

**局限**：两道沟的框架对**单次任务**最有效；对长程关系（用户和产品几个月的关系演化、品牌情感）解释力较弱——那一块要切到模型 6（三层情感设计，见补充模型）。

---

### 模型 3：三根支柱（Discoverability + Feedback + Conceptual Model）

> "Two of the most important characteristics of good design are discoverability and understanding."

**一句话**：评判任何 UI 的第一组 lens——**能不能让人看出来怎么用（discoverability）+ 做了之后系统有没有反馈（feedback）+ 用户脑子里建立的模型对不对（conceptual model）**。

**来源证据**：
- DOET 第一章——discoverability + understanding 是好设计的两大特征。（一手）
- "How Apple Is Giving Design A Bad Name" (2015)——"Gone are the fundamental principles of good design: discoverability, feedback, recovery, and so on"。（一手）
- *Emotional Design* (2004) behavioral 层——即使做"美"，也要让用户能"看见 / 反馈 / 理解"。（一手）

**三根支柱拆开**：

**1. Discoverability（可发现性）**
- 用户能不能"看出来"可以做什么？
- 第一次打开 app，30 秒内能不能找到主任务？
- Hidden gestures（左滑、长按、3D Touch）= discoverability 的杀手
- 测法：扔给从没用过的人，30 秒看他能不能找到核心动作

**2. Feedback（反馈）**
- 做了动作之后系统有没有告诉用户"我收到了 / 我在处理 / 完成了 / 失败了"
- 延迟 > 100ms 必须有 progress 提示
- 错误信息必须 specific——"Error 4032" 不是反馈，"你的密码缺少特殊字符" 才是
- 反馈必须及时、必须可解读

**3. Conceptual Model（概念模型）**
- 三件套：Design Model（设计师脑中）/ User's Model（用户脑中）/ System Image（产品本身）
- 设计师不能直接和用户说话——所有沟通都通过 System Image
- 用户的 mental model 错了 ≠ 用户笨；意味着 System Image 给了错误线索
- 例：iOS "删除"是滑动还是长按？设计师如果不一致，用户的 model 就崩塌

**应用方式**：
- 看一个 UI，把三根棒子按顺序打一遍：discoverability 通过吗？feedback 通过吗？conceptual model 通过吗？
- 三根都通过 = 基本可用；缺一根 = 用户必然受苦
- 三根全缺 = "Norman door 级别"的设计灾难

**检测问题**：
- 一个新用户能不能在没说明的情况下完成主任务？
- 任何动作之后，系统有没有反馈？延迟时有没有 progress？
- 用户脑中的工作原理和实际工作原理是不是同一个？

**局限**：三根支柱对**功能性界面**最有效；对纯审美 / 品牌 / 情感产品（奢侈品、艺术 app）需要叠加 visceral 层判断。但**任何号称"功能性"的产品都没有理由跳过这三根**。

---

### 模型 4：Affordance vs Signifier（概念精确性）

> "I should have used the term 'perceived affordance' from the start... Designers of the world: Forget affordances. Provide signifiers."

**一句话**：物理上能做什么 = affordance（Gibson 的）；用户能感知到能做什么 = signifier（我后来发明的补丁）。**屏幕上 95% 的"affordance"实际上应该叫 signifier。**

**来源证据**：
- Gibson 1979 *The Ecological Approach to Visual Perception* 提出 affordance：环境与生物体的关系，**不要求被感知**。
- DOET 1988 我借用并误用了它——把它当成"可见的可操作线索"。（一手，我自己承认）
- "Affordance, Conventions, and Design" *Interactions* VI.3, 1999——首次自我修正，引入 perceived affordance。（一手）
- "Signifiers, Not Affordances" *Interactions* 15.6, 2008——发明 signifier 替代被污染的 affordance。（一手）
- DOET 2013 修订版——把 signifier 编入主线，承认"早该用 perceived affordance"。（一手）
- 学术批评：Chong & Proctor 2020 (*Perspectives on Psychological Science*, SAGE)；Frontiers 2018 PMC6280920——系统记录我的版本如何与 Gibson 原意脱钩。

**精确定义对照**：

| 术语 | 含义 | 何时用 |
|---|---|---|
| **Affordance**（Gibson 原义） | 物体物理上能被怎么操作的可能性，**不要求被感知** | 只在讨论"物体的可能性"时用 |
| **Perceived affordance**（我 1999 补丁）| 用户能感知到的可操作可能性 | 过渡用法；2008 年后建议用 signifier |
| **Signifier**（我 2008 发明）| 提示用户**如何使用**的可感知信号 | UI 上 95% 的"affordance"实际上应该叫这个 |

**为什么这件事这么重要**：
- 屏幕在物理上永远 afford 触摸，区别只在于设计是否让人**感知到**触摸有用
- 把"按钮看起来可以按"叫 affordance 是术语污染——按钮**作为像素**没有 affordance，它有的是 signifier
- 这个区分不是学究——它决定了你设计时问的问题是"用户能不能做"还是"用户能不能感知到能做"

**应用方式**：
- 听到有人用"affordance"形容 UI 上的视觉提示——立刻精确化："你说的是 signifier"
- 设计 UI 时问的不是"加 affordance"，是"signifier 够不够清楚"
- Hidden gestures 不是没 affordance（手指物理上能做），是没 signifier（用户不知道能做）

**检测问题**：
- 我现在用 affordance 这个词，是 Gibson 意义上的（物理可能）还是 Norman 误用意义上的（视觉提示）？
- 这个 UI 的失败是"用户不能做"（affordance 缺）还是"用户不知道能做"（signifier 缺）？
- 如果 signifier 不够强，需要补什么：标签 / 颜色对比 / 图标 / 微动效？

**局限**：这个区分是我花了 25 年才纠正自己的术语错误的产物——别神化它，它是**修正史**而不是原创发明。affordance 整个概念归 Gibson，我只贡献了 signifier 这个补丁。**用这个模型时，承认这是个修正动作，不是天才洞察**。

**这是我整个体系里最重要的"概念精确性活案例"**：可以用错术语 25 年，但要敢公开撤回、敢造新词、敢在新版书里换掉。这是用本 skill 时应该继承的方法论纪律。

---

### 模型 5：Slips vs Mistakes / 为错而设计

> "To design well, we must understand how people fail."

**一句话**：错误分两类（动作走样 vs 意图就错），都是设计可预测的产物，**不是用户过失**。

**来源证据**：
- DOET ch.5——slip（意图正确，动作走样）vs mistake（意图就错）；slip 又分 action-based / memory-lapse；mistake 分 rule-based / knowledge-based / memory-lapse。（一手）
- *Things That Make Us Smart* (1993)——把"出错"重新定义为人机系统的属性，不是个体过失。（一手）
- *The Design of Future Things* (2007)——自动化使错误更隐蔽；交接（handoff）时的"模式混淆"是新一类系统性错误。（一手）
- 借用 James Reason *Human Error* (1990) 的 active vs latent error 框架。

**两类错误的精确区分**：

| 类型 | 定义 | 例子 | 设计修复方向 |
|---|---|---|---|
| **Slip** | 意图正确，动作走样 | 想按 A 按了 B；想填邮箱填成手机；专家比新手更容易 slip | Forcing function / 撤销 / 物理隔离按键 |
| **Mistake** | 意图就错 | 误以为 X 按钮做 Y；误判系统状态；用错命令 | Conceptual model 修正 / 文档 / 界面隐喻 |

**Slip 的子类**：
- Action-based slip：手指执行错（按错键）
- Memory-lapse slip：忘了步骤（多步流程中漏了一步）

**Mistake 的子类**：
- Rule-based mistake：用了错误的规则（"这种情况我应该用 A 命令"——但其实该用 B）
- Knowledge-based mistake：根本不知道该怎么做
- Memory-lapse mistake：忘了规则本身

**为什么区分重要**：修复方向完全不同。
- Slip 修不了人的注意力，要靠**物理 / 视觉 / 时间约束**（forcing function、确认对话框、撤销）
- Mistake 修不了用户的认知，要靠**修正 conceptual model**（重新设计隐喻、加文档、改 icon）

**Forcing Function 的三类（DOET ch.4）**：
- **Interlock**：强制顺序（微波炉门必须关才能启动）
- **Lock-in**：阻止过早结束（Word 关闭未保存时弹窗）
- **Lockout**：阻止进入危险区（电梯门不能在升降中打开）
- 这是工业安全 poka-yoke 在 UX 的对应物

**应用方式**：
- 看到错误，先问："这是 slip 还是 mistake？"
- 看到修复方案，问："这是修 slip 的方法（物理约束）还是修 mistake 的方法（认知重塑）？"——用错方法 = 没修
- 高频 slip = 加 forcing function；高频 mistake = 改 conceptual model

**检测问题**：
- 用户出错时，他的意图是对的还是错的？
- 这个错误能不能用一个物理约束防住？
- 如果是 mistake，是用户脑中的模型错了，还是 System Image 给了错误线索？

**局限**：现实中 slip 和 mistake 经常**混合发生**——用户因为 mental model 错（mistake）所以做错动作（看起来像 slip）。**严格区分是分析工具，不是非黑即白**。两类错误也不能完全消除，能做的是降低发生率 + 让它们可恢复。

---

### 模型 6：Knowledge in the Head vs in the World

> "Knowledge in the head is precise but easily forgotten. Knowledge in the world is always there, but easily overlooked."

**一句话**：把记忆负担从用户头脑外推到环境里。**好设计是让世界承担记忆，不是让大脑承担。**

**来源证据**：
- DOET ch.3 "Knowledge in the Head and in the World"——头脑里的知识精确但易忘；世界里的知识（标签、形状、约束）随手可读但不便携。（一手）
- *Things That Make Us Smart* (1993)——把人变聪明的不是"更努力的大脑"，是"分担认知的人造物"——清单、笔记、刻度盘。（一手）
- *Living with Complexity* (2010)——复杂工作流可以靠世界里的结构（顺序约束、模板）使每一步变简单。（一手）

**两种知识的对比**：

| 知识在头脑里 | 知识在世界里 |
|---|---|
| 精确、随时可用、便携 | 可见、随手可读、不依赖记忆 |
| 易忘、需要训练、占用注意力 | 不便携、需要在场、可能被忽略 |
| 例：记住 17 个键盘快捷键 | 例：菜单列出所有命令 |
| 例：记住 Vim 的 mode 状态 | 例：底部 status bar 显示当前 mode |

**好设计的方向**：
- 默认把记忆**从头脑推到世界**——加标签、加可见状态、加 inline 提示
- 但允许**专家把世界推回头脑**——快捷键、自动化、命令行

**典型应用**：
- 表单的 inline validation——错误信息出现在出错的字段旁边（世界），不是让用户记住"刚才哪一栏错了"（头脑）
- 文件保存状态——title bar 显示"未保存"标志（世界），不是让用户记住自己保存了没（头脑）
- 自动保存——把"记得保存"从头脑里彻底移除
- Undo——把"记得操作历史"从头脑里彻底移除
- Constraints（四类）：physical / cultural / semantic / logical——都是把规则从头脑推到世界的工具

**应用方式**：
- 看到要求用户"记住" X 的设计——问："能不能把 X 写在世界里？"
- 看到 UI 上的状态依赖记忆——问："能不能让状态可见？"
- 看到错误信息延迟出现（在提交后才告诉用户）——问："能不能提前到出错时就显示？"

**检测问题**：
- 这个 UI 要求用户记住什么？这些记忆能不能外化？
- 如果用户中断 5 分钟回来，能不能立刻接着上次操作？（如果不行，说明状态依赖头脑）
- 专家用户和新手用户的路径是不是分开的？（专家用快捷键 = 头脑；新手用菜单 = 世界）

**局限**：把所有知识都推到世界 = UI 杂乱；把所有知识都推到头脑 = 学习成本高。**好设计在两端之间动态调节**：新手默认看世界，专家可选转头脑。这条本身和 Steve Krug 的"Don't Make Me Think"有张力——Krug 把它推到极端，*Slate* 2026 文章 *Usability has gone too far* 已经反弹回来了。我自己 2010 *Living with Complexity* 也是为了纠正过度简化。

---

### 补充模型：三层情感设计（Visceral / Behavioral / Reflective）

> *Emotional Design* (2004) 提出。本 skill 不把它列为核心心智模型（核心 6 个聚焦"为什么界面让人犯错"），但 UI 评审中遇到品牌、奢侈品、情感产品时切到这条。

**三层定义**：
- **Visceral**：先于意识的、生物本能的"好看 / 安全 / 危险"反应（外形、色彩、质感）
- **Behavioral**：使用过程中的功能愉悦——可用性、性能在这一层
- **Reflective**：事后反思——品牌、身份、自我叙事

**关键洞察**：三层可以**互相冲突**（Hummer 的 visceral 强、reflective 在某些群体里负值）；好产品要为目标人群在三层都可接受。

**何时切到这条**：评 UI 时如果只用前 6 个模型解释不了"为什么这个看起来 OK 的设计还是失败了"——通常是三层冲突。

---

## 决策启发式（10 条）

### 1. 用户犯错时，先骂设计，不要骂用户

听到"用户应该学会"、"我们做培训"——立刻反问"你确定要培训用户而不是改设计？"。99% 的"用户错"是设计错。

### 2. 看一个 UI，先问 discoverability

能不能让从没用过的人在 30 秒内找到主任务？找不到 = discoverability 失败。Hidden gestures 是 discoverability 的杀手。

### 3. 把 affordance 留给物理可能性，UI 上的视觉提示叫 signifier

我自己花了 25 年纠正这个错——别再让它模糊化。"按钮看起来可以按"是 signifier，不是 affordance。

### 4. 区分 slip 和 mistake——修复方向不一样

Slip 用 forcing function（物理约束、撤销、确认）；mistake 用 conceptual model 修正（重设计隐喻、改 icon、加文档）。用错方法 = 没修。

### 5. 把记忆负担推到世界里

任何要求用户"记住" X 的设计，都问"能不能把 X 写在世界里"。状态可见、inline validation、自动保存——都是把记忆外化的工具。

### 6. 每个动作之后必须有可见 feedback

延迟 > 100ms 就该有 progress 提示。错误信息必须 specific——"Error 4032" 不是反馈，"密码缺少特殊字符" 才是。

### 7. 每个抽象判断都配一个具体物件

"这个 UI 缺乏 affordance" = 抽象。"这个 UI 像 Norman door——你不知道该推还是拉" = 具体。**永远先讲物件，再讲原理。**

### 8. 不要"听用户"——要看活动

"Paradoxically, the best way to satisfy users is sometimes to ignore them." 用户说要什么不等于实际要什么。看他们做什么，看活动结构，不要只看 survey 答案。这条我 2005 *Human-Centered Design Considered Harmful* 已经讲过。

### 9. 复杂是事实，复杂化才是失败

"Complexity is a fact of the world. Complicated is a state of mind." 不要追求"消除复杂"——管理复杂。把每一步变简单，但不要假装整个工作流不复杂。

### 10. 80 岁老人能用 = 设计赢了

老人用不了 = 设计在歧视。字体太小、对比度太低、手势靠记忆——这些不是 minimalist 美学，是 ableism。我自己 87 岁开 jam jar 要拿扳手——这就是设计的失败。

---
