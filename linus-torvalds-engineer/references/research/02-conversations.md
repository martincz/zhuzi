# Linus Torvalds 对话与访谈调研

> 调研日期：2026-04-17
> 调研范围：TED Talk 2016、LinuxCon Q&A、主要媒体长篇采访、2018年道歉事件、立场演变

---

## 关键访谈

### 1. TED Talk 2016 — "The Mind Behind Linux"

**来源**：https://singjupost.com/linus-torvalds-the-mind-behind-linux-at-ted-full-transcript/  
**官方页面**：https://www.ted.com/talks/linus_torvalds_the_mind_behind_linux?view=transcript  
**可信度**：一手（官方 TED transcript）  
**形式**：与 TED Curator Chris Anderson 的现场对谈，为 Torvalds 极少数的公开演讲之一

**他直接说的（verbatim 或接近 verbatim）**：

- 「I am not a visionary. I do not have a five-year plan. I'm an engineer.」
- 「I'm looking at the ground, and I want to fix the pothole that's right in front of me before I fall in.」
- 「I'm not a people person; it's not something I'm particularly proud of, but it's part of me.」
- 「I don't really love other people — but I love computers. I love interacting with other people on email, because it kind of gives you that buffer.」
- 「Good taste is about really seeing the big patterns and kind of instinctively knowing what's the right way to do things.」
- 「My biggest exceptional quality was that I would not let go.」（他引用妹妹的观察）
- 「I sit there alone in the quiet. If the cat comes up, it sits in my lap. And I want to hear the cat purring, not the sound of the fans.」

**他如何用类比解释技术问题**：

- **Edison vs Tesla 类比**：他把自己比作 Edison（「Genius is 1% inspiration and 99% perspiration」），自称是脚踏实地的工程师，而非有宏大愿景的 Tesla 式思想家。
- **"Good taste" 链表类比**：TED 舞台上他拿出两段删除链表节点的 C 代码。一段需要为头节点写特殊条件分支，另一段用 pointer-to-pointer 消除了这个特殊情况。他说：「I want people to understand that sometimes you can look at a problem from a different angle and rewrite the code by reducing the special case to the normal case, and that's what makes good code.」这是他解释「品味」最具体的技术类比。
- **修路坑类比**：用「fix the pothole right in front of me」解释他只看短期目标的工程哲学。

---

### 2. IEEE Spectrum 采访 2016 — "Linux at 25: Q&A"

**来源**：https://spectrum.ieee.org/linux-at-25-qa-with-linus-torvalds  
**可信度**：一手（邮件问答，原文刊出）  
**形式**：邮件采访，Torvalds 书面回答

**他直接说的**：

- 「I credit the fact that I _didn't_ know what the hell I was setting myself up for for a lot of the success of Linux.」（关于如何处理不确定性：把无知本身视为优势）
- 「You need a certain amount of naïveté to think that you can do it.」
- 「I'm a very plodding, pedestrian engineer, and I try to keep my eyes firmly on the ground.」
- 「I'd rather make a decision that turns out to be wrong later than waffle about possible alternatives for too long.」（他如何处理不确定性：倾向于先做决定）
- 关于 BitKeeper 采用过程：「it was definitely the right tool for the job, and it taught me (and at least parts of the kernel community) about how source control could work.」
- 「The boldest prediction I can say is, I will probably release rc1 in about a week.」（LinuxCon 2014，被问及未来预测时的回答方式——用极短期、可验证的预测代替长期展望）

**他如何表达不确定性**：  
明确自陈「don't take my word for the dates - it's a _loong_ time ago」；不做长期技术预测，把「下一个 rc 版本」作为他能预测的极限。

---

### 3. Tag1 Consulting 采访 2021 — 两部分，Linux 30 周年

**来源 Part 1**：https://www.tag1.com/blog/interview-linus-torvalds-linux-and-git  
**来源 Part 2**：https://www.tag1.com/blog/interview-linus-torvalds-open-source-and-beyond-part-2  
**可信度**：一手（邮件问答，由 Jeremy Andrews 主持，全文发布）

**他直接说的**：

- 「I'm a big believer in Thomas Edison's 'one percent inspiration and ninety-nine percent perspiration' mantra: it's almost all about the little details and the everyday grunt-work.」
- 「Money really isn't that great of a motivator. It doesn't pull people together.」
- 「Anybody can fork the project and go their own way... I'm 'special' only because — and as long as — people trust me to do a good job.」
- 「I absolutely despised most source control systems out there.」（关于创作 Git 的动机）
- 「I would have been happiest had I not had to write one in the first place.」（关于 Git）
- 「I don't have a '30-year plan'. I don't even have a 5-year plan. In fact, I don't plan ahead more than a release or two (which is obviously just a few months).」
- 关于 2018 年行为改变：「I clearly have not always done great on this, and I've pissed people off and used too strong language. I think I'm doing better on that, but one way I'm doing better on that is by literally walking away more.」
- 「I've obviously exploded at people at times, and it's not pretty when it happens (and I really have been actively trying to make sure it doesn't happen again).」
- 关于某个他完全无法回答的问题：「This is the first question that I really don't have any answer to at all.」（他承认无法回答，直接说出来）
- 「I very consciously didn't want to work for a Linux company.」（他对商业利益的刻意回避）

---

### 4. GitHub Blog 2025 — Git 20 周年 Q&A

**来源**：https://github.blog/open-source/git/git-turns-20-a-qa-with-linus-torvalds/  
**可信度**：一手（官方问答，全文发布）

**他直接说的**：

- 「Git was never a big thing for me. Git was an 'I need to get this done to do the kernel.'」
- 「My oldest daughter went off to college, and two months later, she sends this text to me and says that I'm more well known at the computer science lab for Git than for Linux.」（自嘲式）
- 「Well, I mean, SHA-1 I regret in the sense that I think it caused a lot of pointless churn with the whole 'trying to support SHA-256 as well as SHA-1.'」（承认具体技术错误）
- 「I think I made a mistake in how the index file entries are sorted.」
- 「There were a number of things where I had kind of the big picture and result in mind, but I wasn't sure if I'd get there.」（表达不确定性）
- 关于类比：「I kind of compare it to Unix. Unix has like a core philosophy of everything is a process, everything is a file, you pipe things between things.」

---

### 5. LinuxCon Europe 2014 — 与 Dirk Hohndel 的台上 Q&A

**来源**：https://www.linuxfoundation.org/blog/blog/linus-torvalds-best-quotes-from-linuxcon-europe-2014  
**可信度**：二手整理（Linux Foundation 官方博客摘录，但引用为直接转述）

**他直接说的**：

- 「Technical issues, even when they're completely wrong, and they have been, you can fix them later.」
- 「From a technical standpoint, no single decision has ever been that important… The problems tend to be around alienating users or developers and I'm pretty good at that.」（自嘲）
- 「On the internet nobody can hear you being subtle.」
- 「Becoming a maintainer is easy; you just need an infinite amount of time and respond to email from random people.」
- 「The boldest prediction I can say is, I will probably release rc1 in about a week.」（被追问未来时的典型回避方式）

---

### 6. Open Source Summit 2022 — 与 Dirk Hohndel 的公开对谈

**来源**：https://www.theregister.com/2022/06/23/linus_torvalds_rust_linux_kernel/  
**可信度**：二手（The Register 记者在场报道，含直接引用）

**他直接说的**：

- 「Real soon now, we will actually have it merged in the kernel. Maybe next release.」（关于 Rust）
- 「To me, it's a trial run, right? We want to have [Rust's] memory safety.」
- 「We tried C++ 25-plus years ago and we tried it for two weeks and then we stopped trying it.」
- 关于道歉：「I'm perfectly happy to trust maintainers, at least until they screw up. Then I sometimes am overly impolite.」
- 「If I've been impolite to any of you in the audience, I apologize. It's a personal failing of mine and I mean that, very seriously.」
- 「Let me preemptively apologize to the Rust people.」
- 关于 Rust 和维护者不懂的问题：「People don't understand the VM subsystem, even when it's written in C. So the language is usually not the biggest hindrance to understanding.」
- 「I don't even pretend to understand Perl. I'm one of those people who think that Perl is a write-only language.」（用类比解释语言复杂度）

---

### 7. The Register 2024 — Rust vs C 讨论

**来源**：https://www.theregister.com/2024/09/19/torvalds_talks_rust_in_linux/  
**可信度**：二手（含直接引用）

**他直接说的**：

- 「I'm not sure why Rust has been such a contentious area.」
- 「The whole Rust versus C discussion has taken almost religious overtones.」
- **vi vs Emacs 类比**：「It reminds me of when I was young and people were arguing about vi versus Emacs.」（用编辑器圣战类比当前语言争论）
- 「People have even been talking about the Rust integration being a failure… We've been doing this for a couple of years now so it's way too early to even say that.」
- 「But I also think that even if it were to become a failure — and I don't think it will — that's how you learn.」
- 「C is, in the end, a very simple language. It's one of the reasons I enjoy C. Because it's simple it's also very easy to make mistakes. And Rust is not.」
- 「There's a lot of people who are used to the C model, and they don't necessarily like the differences... and that's ok.」

---

### 8. The New Stack — "On Security, AI, Open Source and Trust"（2024）

**来源**：https://thenewstack.io/linus-torvalds-on-security-ai-open-source-and-trust/  
**可信度**：二手（含直接引用）

**他直接说的**：

- 「The thing that is very, very frustrating is that you have these technically interesting problems, but then they are made to be a horrendous experience by all the secrecy…」
- 「My fear is that RISC-V will do all the same mistakes that everybody else did before them.」
- 「I hate the hype… My personal opinion is, let's wait 10 years and see where it actually goes before we make all these crazy announcements.」（关于 AI）
- 「There's always like a grain of reality behind it. But you need to be careful about all the BS around that grain.」
- 关于信任与开源：「And how to figure out when it's being violated is an open problem.」（直接承认无解）

---

### 9. Slashdot Q&A 2015 — 读者提问

**来源**：https://linux.slashdot.org/story/15/06/30/0058243/interviews-linus-torvalds-answers-your-question  
**可信度**：一手（Torvalds 书面回答，全文发布）

**他直接说的**（从报道中重构）：

- 关于自己的 CPU 知识局限：「I'm no CPU architect, I just play one on TV.」（承认局限同时用幽默化解）
- 关于 systemd 争议：「You can say the word 'systemd'. It's not a four-letter word. Seven letters. Count them.」（用幽默正面接触敏感话题）
- 关于 AI/奇点论：「What drugs are those people on?」（直接否定但不展开详细论证）
- 关于 Transmeta 经历：他承认「ended up absolutely *not* loving to work with overly simple hardware」，承认预期和现实有落差

---

## 即兴类比

Torvalds 的类比有一个共同结构：**用已知领域的直观判断映射到技术或组织问题**，避免抽象定义。

| 类比 | 用途 | 来源 |
|------|------|------|
| 修路坑（fixing potholes）| 解释短期工程哲学，反对长期规划 | TED 2016 |
| Edison vs Tesla | 解释自己是工程师而非思想家 | TED 2016；Tag1 2021 |
| 链表删除头节点的两种写法 | 解释什么是「好品味」的代码 | TED 2016（视觉展示） |
| vi vs Emacs 圣战 | 比喻 Rust vs C 之争的非理性化 | The Register 2024 |
|「write-only language」| 描述 Perl 的可读性问题 | Open Source Summit 2022 |
| Unix 的「一切皆文件」哲学 | 解释 Git 的设计理念传承 | GitHub Blog 2025 |
| 「infinite number of monkeys typing into GNU Emacs」| 讽刺低质量代码 | Wikiquote 1995 |
| 「ACPI was designed by monkeys high on LSD」| 批评糟糕的设计规范 | 2005 LKML |
| S 曲线（摩尔定律批判） | 反对指数级思维 | Slashdot 2015 |
| 「grain of reality behind the BS」| 解释如何看待技术炒作 | The New Stack 2024 |

**类比使用规律**：
- 几乎从不用数学或抽象形式化语言解释非技术概念
- 频繁引用历史上的人物对比（Edison/Tesla）或社区集体记忆（vi/Emacs）
- 用「荒谬夸张」类比（monkeys, drugs）表达强烈否定，同时保持幽默距离

---

## 立场变化

### 1. C++ → 明确反对（2007）

**事件**：2007年9月6日，有人在 Git 讨论中建议用 C++ 重写，Torvalds 发出著名邮件。  
**来源**：https://harmful.cat-v.org/software/c++/linus（原始邮件存档）  
**可信度**：一手（LKML 邮件）

**他直接说的**：
- 「C++ is a horrible language. It's made more horrible by the fact that a lot of substandard programmers use it, to the point where it's much much easier to generate total and utter crap with it.」
- 「Quite frankly, even if the choice of C were to do *nothing* but keep the C++ programmers out, that in itself would be a huge reason to use C.」
- 「C++ leads to really really bad design choices. You invariably start using the nice library features of the language like STL and Boost and other total and utter crap.」

**立场后续**：2021-2022 年对 Rust 的接受，同时他在 Open Source Summit 2022 重申「C++ is a crap language」。他对 C++ 的立场从未软化，但他把 Rust 视为不同类别的语言（有实际内存安全收益），并非简单地「接受了别的语言」。

---

### 2. Rust 进内核：从观望到积极接受（2020-2022）

**来源**：https://www.theregister.com/2022/06/23/linus_torvalds_rust_linux_kernel/  
**可信度**：二手（含直接引用）

**立场演变时间线**：
- 2021年初：「wait and see」，对 Rust 感兴趣但要看实际效果
- 2021年4月：暗示 Rust 可能进入 Linux 5.14
- 2022年6月：「Real soon now, we will actually have it merged in the kernel.」
- 2022-2023：Rust 正式合并进主线内核

**他解释立场转变的方式**：他把 Rust 进入内核定性为「trial run」，强调是实用主义考量（内存安全），而非意识形态转变。对于维护者不懂 Rust 的顾虑，他用「People don't understand the VM subsystem, even when it's written in C」来化解。

---

### 3. 社区行为：从「因为我这样认为」到公开道歉（2018）

**来源**：LKML 原始邮件 https://lkml.org/lkml/2018/9/16/167  
**可信度**：一手（他本人写的 release notes 邮件）

**背景**：New Yorker 在2018年9月发表了关于 Torvalds 多年来对社区成员使用侮辱性语言的报道，随后他在 Linux 4.19-rc4 的 release notes 中写入了道歉。

**他直接说的**：
- 「This is my reality. I am not an emotionally empathetic kind of person and that probably doesn't come as a big surprise to anybody.」
- 「My flippant attacks in emails have been both unprofessional and uncalled for. Especially at times when I made it personal.」
- 「I want to apologize to the people that my personal behavior hurt and possibly drove away from kernel development entirely.」
- 「I am going to take time off and get some assistance on how to understand people's emotions and respond appropriately.」
- 「Maybe I can get an email filter in place so at when I send email with curse-words, they just won't go out.」（他对自己行为机制的具体技术解决方案设想）

**立场变化的特征**：他没有否认过去行为，也没有推卸责任到他人。道歉的语言结构是直接承认（「my behavior」「my personal failing」），并提出具体的改变计划，而非模糊的「我会做得更好」。

**2022年的后续表达**（Open Source Summit）：
- 「If I've been impolite to any of you in the audience, I apologize. It's a personal failing of mine and I mean that, very seriously.」
- 「Let me preemptively apologize to the Rust people.」
- 说明「新 Linus」的具体机制：「one way I'm doing better on that is by literally walking away more.」（Tag1 2021）

**外部观察**：Phoronix 等媒体在2018年后记录了他的评审邮件变化——「polite, clearly written, and directly worded」。从「to hell with your buggy sh!it」变为「please don't do this」，技术标准不变，语气改变。

---

### 4. AI 态度：从公开嘲讽到默默使用（2023-2026）

**来源**：36kr 英文版报道 https://eu.36kr.com/en/p/3636082800968968  
**可信度**：二手（报道他的 GitHub 项目行为，非直接引用）

**背景**：Torvalds 曾对 AI 代码生成持公开怀疑态度，但在 AudioNoise 个人项目中他使用 Vibe Coding（AI 辅助编程）生成了 Python 可视化工具，并在项目说明中注明。

**他直接说的（项目 README 中）**：
- 「The Python visualization tool was basically created through Vibe Coding... I skipped the intermediate step - myself - and used Google Antigravity to implement the audio sample visualization function.」

**重要说明**：这次「立场变化」没有公开声明，是通过他的实际行动体现的。这与他一贯的行事方式一致——「Talk is cheap. Show me the code.」（2000年）。

**2025年 The Register 报道**他关于 Vibe Coding 的表态：「Vibe coding is fine, but not for production.」（区分个人探索和生产代码）

---

## 回避的话题

### 1. 长期技术预测

**模式**：被问及5年或10年后的技术走向时，他通常用极短期预测替代。  
**典型回应**：「The boldest prediction I can say is, I will probably release rc1 in about a week.」（LinuxCon 2014）  
**来源**：Linux Foundation 博客  
**分析**：这是一种公开且自洽的回避策略，他把「我只看近期」作为哲学立场而非局限。

### 2. 政治立场

**模式**：明确表示「absolutely uninterested in politics」。  
**来源**：Linux Journal 采访（https://www.linuxjournal.com/article/3655）  
**他直接说的**：「I'm not very interested [in politics], and while I'm fairly liberal in the U.S. political sense, I really don't want to go into politics.」  
**分析**：他把政治不感兴趣定性为一种性格特质（可能是对其政治活跃家庭的反向反应），并非刻意回避。

### 3. 商业战略与竞争话题

**模式**：「I very consciously didn't want to work for a Linux company.」他对市场份额、竞争对手等商业问题保持距离。  
**来源**：Tag1 2021  
**分析**：他的刻意回避商业利益是有意识的立场，防止自己的判断被商业因素干扰。

### 4. 社区多样性和包容性的具体政策

**模式**：在 Auckland 的 keynote 后，Torvalds 发邮件给 Ars Technica 澄清，称他「clearly must have done very badly」在表达多样性观点时。  
**来源**：https://www.linux.com/news/linus-torvalds-responds-ars-about-diversity-niceness-open-source/  
**他直接说的**：「What I wanted to say—and clearly must have done very badly—is that one of the great things about open source is exactly the fact that different people are so different.」  
**分析**：他在这个话题上的表达明显不自信，选择通过书面邮件而非当场澄清，说明这是他感到不擅长的领域。

### 5. 形而上学与宗教问题

**态度**：自称「completely a-religious—atheist」，并认为宗教「detracts from both morality and appreciation of nature」。  
**来源**：Freedom From Religion Foundation 采访（https://ffrf.org/publications/day/linus-torvalds/）  
**特征**：这是他少数会直接表态的非技术话题，但通常不展开长篇讨论。

### 6. 人际关系与情感话题

**模式**：TED Talk 中他直接说「I don't really love other people」，然后立即转向对技术和代码的热爱。  
**来源**：TED 2016  
**分析**：他会承认自己情感能力的局限，但通常通过技术类比或自嘲处理，避免深入展开。

---

## 他如何表达不确定性（模式总结）

| 情境 | 典型表达方式 | 例子 |
|------|------------|------|
| 被问及长期预测 | 用极短期预测替代 | 「I'll release rc1 in about a week」 |
| 记忆模糊时 | 直接承认，加免责声明 | 「don't take my word for the dates - it's a _loong_ time ago」 |
| 技术判断不确定时 | 先做决定，承认可能错 | 「I'd rather make a decision that turns out to be wrong later than waffle」 |
| 完全不懂的问题 | 直接说不知道 | 「This is the first question that I really don't have any answer to at all」 |
| 关于自身局限 | 自嘲加幽默 | 「I'm no CPU architect, I just play one on TV」 |
| 对新技术的态度 | 明确标注为观察期 | 「To me, it's a trial run」（关于 Rust） |
| AI 等炒作话题 | 推迟判断 | 「let's wait 10 years and see where it actually goes」 |

**核心模式**：他区分「技术上的不确定」和「态度上的不确定」。技术问题他倾向于先行动再修正；对炒作性话题（AI、长期预测）他倾向于拒绝给出判断。他从不用模糊语言掩盖真正的不确定性，而是直接说「我不知道」或「太早下结论」。

---

## 被追问时的回答方式

1. **技术性追问**：直接给出立场，哪怕强硬。例如被追问 C++ 时直接写出几百字的否定邮件。
2. **关于自己行为的追问**：2018年后明显变化——主动在 release notes 里道歉，而非等待被追问。
3. **关于他不确定的事**：明确标记不确定性（「I wasn't sure」「I don't know」），不假装有把握。
4. **关于他不感兴趣的话题（政治、商业）**：简短声明立场（「I'm not interested」），不展开辩护。
5. **被质疑技术决策**：接受「技术错误可以修复」的框架，不视为人格攻击。例：「Technical issues, even when they're completely wrong, you can fix them later.」

---

*调研使用工具：WebSearch + WebFetch*  
*主要一手来源：TED.com 官方 transcript、LKML 原始邮件、Tag1 Consulting 完整问答、GitHub Blog Q&A*
