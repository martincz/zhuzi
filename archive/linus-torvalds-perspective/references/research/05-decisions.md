# Linus Torvalds 重大决策调研

> 信息来源：LKML archives、GitHub 官方公告、Linux Foundation 声明、The Register、Phoronix、LWN.net、Wikipedia、The New Yorker

---

## 创始决策

### D-01：1991年创建 Linux（为何没选 Minix / GNU Hurd）

**背景**
1991年，21岁的 Linus Torvalds 在赫尔辛基大学攻读计算机科学，刚买了一台配备 Intel 386 处理器的 PC。他在课程中使用 MINIX（Andrew Tanenbaum 为教学目的开发的类 Unix 系统），但对其限制深感不满。

**决策内容**
1991年8月25日，Torvalds 在 `comp.os.minix` 新闻组发出历史性公告：
> "I'm doing a (free) operating system (just a hobby, won't be big and professional like gnu) for 386(486) AT clones."

**决策逻辑**

| 为何放弃 Minix | 为何放弃 GNU Hurd |
|---|---|
| Minix 是16位设计，386的32位特性无法充分利用 | Hurd 从1990年开始开发，但进展极慢、长期未完成 |
| 源代码虽然可查，但修改和再发布受许可证限制 | Torvalds 事后承认：如果当时 Hurd 或 386BSD 可用，他可能不会写 Linux |
| 商业 AT&T Unix 价格高昂，学生无力负担 | Hurd 微内核设计理念复杂，远水解不了近渴 |
| 个人动机：想探索386处理器能力，学习OS原理 | — |

Torvalds 的动机更接近工程师的"工具驱动"：他需要一个能在386上运行的、可自由修改的系统，而现实中没有这样的选项存在。

**后续影响**
- Linux 在发布后数月内吸引了全球开发者贡献代码，1994年发布1.0版
- 成为世界上使用最广泛的操作系统内核（超过90%的服务器、Android、嵌入式设备）
- Tanenbaum 曾公开批评 Linux 的单体内核设计是"过时的"（1992年"Tanenbaum-Torvalds 辩论"），Torvalds 回击坚持实用主义

**言行一致性**
✅ **一致**：Torvalds 始终把个人好奇心和实际可用性放在第一位，这与他此后30年"工程实用主义"的风格完全吻合。

---

### D-02：选择 GPL v2 协议（而非其他许可证）

**背景**
Linux 0.01（1991年9月）使用的是 Torvalds 自己写的许可证，明确禁止商业发行。他事后承认这个限制"太过严格，阻碍了一些完全合法的用途"。

**决策内容**
1992年，Linux 0.99 切换至 GPL v2。此后 Torvalds 多次强调这是他"做过的最正确的决定"。

**决策逻辑**
- GCC 编译器（Linux 的构建基础）本身是 GPLv2，Torvalds 想表达对 GNU 工具的感激
- GPLv2 的"copyleft"条款确保所有改进必须回馈社区——这是他核心关切：防止私有化分叉
- Torvalds 明确表态：他认可 GPL 是工程选择，而非像 RMS 那样的道德立场

**2007年 GPLv3 决策：拒绝升级**

当 FSF 发布 GPLv3 时，Torvalds 明确拒绝升级，理由：
1. **Tivoization 条款**：GPLv3 禁止硬件厂商用硬件锁阻止用户运行修改版软件，Torvalds 认为只要源代码开放，硬件厂商有权保护自己的设备
2. **主权原则**："我不想在协议这么重要的事情上受制于别人"
3. Torvalds 与 FSF / Richard Stallman 关系紧张，明确区分"我认可 GPL 作为工程工具，但我不是软件自由的道德传教士"

**后续影响**
- Linux 至今维持 GPLv2-only，是开源世界最大的 GPLv2 代码库之一
- 引发长期争议：GPLv3 支持者（FSF）批评 Linux 实际上允许 Tivoization
- Android 采用 Linux 内核但加了自己的用户空间，间接利用了 Torvalds 的立场

**言行一致性**
✅ **一致**：Torvalds 的 GPLv2 立场从1992年到今天没有动摇，且有清晰的工程逻辑支撑，体现"独立判断、抵制外部压力"的一贯模式。

---

## 技术决策

### D-03：创建 Git（2005年，BitKeeper 事件后）

**背景**
2002–2005年，Linux 内核开发使用 BitKeeper（Larry McVoy 的商业 DVCS），BitMover 提供免费许可证，但附加条件：Linux 开发者不得参与开发竞争性的版本控制系统。

2005年4月，Andrew Tridgell 尝试逆向工程 BitKeeper 协议以创建开源替代品。BitMover 以违反协议为由吊销了 Linux 项目的免费许可证。

**决策内容**
Torvalds 在失去 BitKeeper 访问权的数天内启动 Git 开发：
- 2005年4月3日：开始开发
- 4月6日：公开宣布项目
- 4月7日：Git 实现自我托管（用 Git 管理 Git 的源代码）
- 4月29日：Linux 内核切换至 Git
- 7月26日：Torvalds 将维护权移交 Junio Hamano
- 12月21日：Git 1.0 发布

**决策逻辑**
Torvalds 对当时现有开源 VCS（CVS、Subversion）的批评极为直接：它们无法满足分布式大规模协作的需求。他设定了三个不可妥协的设计目标：
1. 速度（CVS/SVN 太慢）
2. 去中心化（没有单一权威仓库）
3. 数据完整性（SHA-1 内容寻址）

**后续影响**
- Git 成为全球使用最广泛的版本控制系统，GitHub 于2008年建立在其上
- Torvalds 在2025年 GitHub 20周年访谈中回顾："Git 比 Linux 对计算机科学的影响更大，因为每个人每天都在用"
- 展示了 Torvalds "愤怒驱动的高效创造力"：10天内完成核心原型

**言行一致性**
✅ **一致**：Torvalds 声称需要"能解决实际问题的工具"，Git 从第一天起就是为内核开发的真实需求而生，且快速将维护权移交他人——符合他"做完就脱手"的模式。

---

### D-04：内核合并决策标准

**背景**
Linux 内核每个开发周期（约8周）接受数千个补丁。Torvalds 是最终合并权威，但实际上只直接审查约1.3%的补丁，其余通过子系统维护者的"信任链"流入。

**决策逻辑（Torvalds 明确表达的标准）**

| 接受标准 | 拒绝原因 |
|---|---|
| 补丁有活跃、负责任的维护者 | 维护者已知忽视 bug 报告（如 Kay Sievers 事件） |
| 无回归（regression-free）是核心红线 | 引入回归的补丁极大概率被 revert |
| 代码解释清晰，merge 逻辑可陈述 | "如果你解释不了这个 merge 为什么存在，就别做" |
| 合并窗口（约两周）内提交 | 窗口关闭后提交新功能会被拒，附加训斥 |
| 架构专属代码在对应子目录 | 通用头文件里加架构特定代码会被直接拒 |

**典型案例**
- **2007年 CFS 调度器**：Torvalds 选择 Ingo Molnár 的 CFS 而非 Con Kolivas 的 SD，核心原因：Ingo 有持续维护的记录，Con 则在争议后退出了内核开发
- **2014年 Kay Sievers 禁令**：Torvalds 明确拒绝合并任何 Kay Sievers 维护的补丁，理由是其"不关心他代码中的 bug"
- **2025年 RISC-V 补丁**：Torvalds 称部分 RISC-V 补丁为"garbage"，拒绝在合并窗口末期接受迟交的变更

**言行一致性**
⚠️ **部分一致**：技术标准一致性高，但执行方式（公开羞辱 vs 私下反馈）在2018年前后有明显差异，且2025年 RISC-V 事件表明激烈措辞并未完全消失。

---

### D-05：对 Rust 进入内核的态度演变

**背景**
Rust 是以内存安全为核心设计目标的系统编程语言，2020年起社区开始推动将其引入 Linux 内核，作为 C 的补充（而非替代）。

**态度演变时间线**

| 时间 | 立场 | 关键引言/事件 |
|---|---|---|
| 2021年3月 | 观望 | "处于 wait-and-see 阵营，不推也不反对" |
| 2021年4月 | 轻度支持 | 暗示 Rust 可能进入 5.14（最终未兑现） |
| 2022年6月 | 正式支持 | Linux Foundation Open Source Summit 宣布"很快会合并" |
| 2022年10月 | 落地 | Linux 6.1 合并 Rust 基础设施支持 |
| 2023–2024 | 施压推进 | 对 Rust 采用缓慢表示失望；批评老内核开发者不愿学 Rust |
| 2025年2月 | 仲裁冲突 | Hector Martin（Asahi Linux）呼吁 Torvalds"出来说话"解决 Rust vs C 驱动僵局，Torvalds 回应："也许问题出在你身上"，并批评"社交媒体围攻"策略 |

**决策逻辑**
- 支持 Rust 的工程理由：内存安全错误是内核漏洞的主要来源，Rust 的类型系统可以在编译期消除一大类 bug
- 拒绝冒进的理由：内核现有 C 代码量巨大，全面切换不现实；强制现有维护者学 Rust 会损失宝贵人才
- 对"Rust 传道者"态度：Torvalds 明确反对以"宗教热情"推进 Rust，要求技术落地而非理念争论

**后续影响**
- 2025年 Rust 在内核中的覆盖率依然较低，主要用于新驱动
- 2025年2月，Hector Martin（Apple Silicon 移植负责人）因 Rust 冲突宣布辞去 Asahi Linux 首席开发职位，引发社区对 Torvalds 领导力的批评

**言行一致性**
⚠️ **矛盾点**：Torvalds 支持 Rust 进入内核，但在仲裁 Rust vs C 文化冲突时的处理方式（拒绝主动调解，将责任推给 Rust 方）与他声称的"欢迎 Rust"存在张力。Hacker News 评论称"这是 Torvalds 领导力罕见的失败案例"。

---

## 社区决策

### D-06：与 Nvidia 的公开冲突（2012年"中指事件"）

**背景**
Nvidia 长期拒绝为 Linux 提供开源驱动或内核 DRM 接口支持，依赖自己维护的闭源驱动，导致：
1. 内核 ABI 变更时 Nvidia 驱动经常失效
2. Linux 用户体验大幅落后于 Windows
3. Nvidia 拒绝向内核开发者提供必要的技术文档

**决策内容**
2012年6月，在芬兰阿尔托创业中心（Aalto Center for Entrepreneurship）的公开问答中，面对关于 Nvidia Linux 支持的提问，Torvalds 直接面对摄像机竖起中指，并说：

> "So NVIDIA, fuck you!"

随后补充称 Nvidia 是"我们打过交道的最糟糕的公司"（"the single worst company we have ever dealt with"）。

**决策逻辑**
这不是一时冲动，而是多年积累的爆发。Torvalds 的逻辑：
- 公开羞辱是推动封闭厂商做出改变的有效手段（他此前对其他公司也用过类似策略）
- Nvidia 的封闭行为实质上是"绑架"了 Linux 用户——用闭源驱动锁定用户，但又拒绝配合内核维护

**Nvidia 回应**
Nvidia 官方回应措辞谨慎，声称"持续在改善 Linux 支持"，但未承认具体问题，短期内无实质变化。

**后续影响（长弧）**
- 2022年，Nvidia 宣布开源其 GPU 内核驱动模块（Open GPU Kernel Modules）
- Torvalds 在2024年访谈中承认 Nvidia 在此后"学到了很多"，现在认为 Nvidia 在 Linux 支持上做得"相当好"（"really good work"）
- AI/GPU 计算需求的爆炸性增长（CUDA、深度学习）是 Nvidia 改变态度的核心驱动力

**言行一致性**
✅ **有效果，但方式有争议**：羞辱策略最终收到了成效（12年后），但同期 Torvalds 对自己2018年后承诺减少攻击性言行——这与2012年事件形成对比，说明他的行为改变是渐进且不彻底的。

---

### D-07：对 systemd/Poettering 争议的处理

**背景**
2010年代，Lennart Poettering 开发的 systemd 逐渐取代传统 SysV init，成为大多数 Linux 发行版的默认初始化系统。围绕 systemd 的争议极为激烈：
- 支持者：统一接口、加速启动、更好的依赖管理
- 反对者：功能蔓延、违反 Unix 哲学、代码质量问题

**决策内容**
Torvalds 自己在 systemd 争议中保持了罕见的克制，多次表态"对 systemd 没有强烈意见"，认为这是发行版层面的决策，与内核无关。

然而，2014年他对 systemd 联合开发者 **Kay Sievers** 采取了直接行动：明确拒绝合并任何 Kay Sievers 提交的补丁，原因是 Sievers 被认为对用户报告的 bug 漠然处之，且 systemd 代码曾导致内核崩溃而 Sievers 拒绝承认问题。

**Poettering 的反击**
Poettering 在2014年公开撰文批评 Torvalds，称其"骂人的管理风格不是有效的社区管理方式"，并指控 Torvalds 曾说开发者应该"被追溯性堕胎"（retroactively aborted）等极端言论。Poettering 称开源社区是"相当病态的地方"，并将矛头指向 Torvalds 树立的文化榜样。

**决策逻辑**
- Torvalds 将 systemd 本身（架构层面的争议）与 Kay Sievers 的维护态度（工程责任问题）明确分开处理
- 他对系统设计争议保持中立，但对"维护者不修 bug"这个问题上绝不妥协

**后续影响**
- Kay Sievers 在2015年左右逐渐减少了直接向内核提交补丁的行为
- Poettering 后来加入微软（2022年），持续维护 systemd
- 这一事件成为2018年改革讨论中被引用的具体案例之一

**言行一致性**
⚠️ **技术标准一致，态度表达矛盾**：Torvalds 在技术判断上（拒绝不负责任的维护者）是一贯的，但他自身言行（包括他说的"retroactively aborted"等言论）恰恰是他批评社区文化的症结所在。

---

### D-08：2018年休假与道歉——背景、触发点、实际变化

**背景**
多年来，Torvalds 在 LKML 上的攻击性言论引发持续批评，具体案例包括：
- 对 Red Hat 工程师 Mauro Carvalho Chehab："SHUT THE F**K UP！"（因补丁破坏内核）
- 对 Intel 工程师："COMPLETE AND UTTER GARBAGE"（针对 Spectre 漏洞修复代码）
- 多次使用"retroactively aborted"等人身攻击

**触发点**
2018年9月，《纽约客》记者就"Torvalds 的粗暴行为阻碍女性参与 Linux 内核开发"向其发出采访问题。在回应过程中，Torvalds 选择主动在内核邮件列表公开道歉并宣布休假，而非等待文章发表。

**道歉内容**
2018年9月16日，Torvalds 在 LKML 发文：
> "I am truly sorry for some of my past behavior... I need to change some of my behavior, and I want to apologize to the people that my personal behavior hurt and possibly drove away from kernel development entirely."
> 
> "I am going to take time off and get some assistance on how to understand people's emotions and respond appropriately."

同时，内核社区引入了基于 Contributor Covenant 的新行为准则（Code of Conduct），取代2015年的简短版"Code of Conflict"。

**休假时长**：约四周（2018年9月16日 → 10月22日返回）

**实际行为变化的证据**

| 维度 | 变化前 | 变化后 |
|---|---|---|
| 邮件基调 | 频繁出现人身攻击、粗口 | 返回初期以简短"pulled"回复为主，技术批评措辞更克制 |
| 公开言论 | 直接羞辱个人 | 更多指向代码问题而非个人 |
| 2019–2025 | — | 仍有激烈措辞（如2024年对 Google 贡献者的公开批评；2025年 RISC-V "garbage"事件）但减少了明显人身攻击 |

**事后反思**
- 观察者普遍认为 Torvalds 的改变是真实的但不彻底：在低风险场景（常规合并）明显温和，但在他认为原则性的技术争议中仍会爆发
- Torvalds 本人从未声称自己已经"改好了"，只说"正在努力改变"
- 有分析认为 CoC 的引入实质改变了内核社区的整体氛围，即使 Torvalds 个人改变有限

**言行一致性**
⚠️ **部分一致**：Torvalds 承诺改变并有实际行动（休假、引入 CoC），但2024–2025年的案例表明改变是方向性的而非根本性的。他的自我描述（"lifelong struggle"）实际上是对不完全改变的预先声明。

---

## 言行分析

### 一致性总表

| 决策/事件 | 核心承诺/立场 | 实际执行 | 一致性评级 |
|---|---|---|---|
| 创建 Linux | 出于工程需要，追求实用可用 | 项目完全按照"解决真实问题"路径演进 | ✅ 高度一致 |
| GPLv2 选择 | "工程选择，而非道德传教" | 30+年未妥协，拒绝 GPLv3 的道德压力 | ✅ 高度一致 |
| 创建 Git | 需要解决实际版本控制问题 | 10天完成原型，快速移交维护——工具主义 | ✅ 高度一致 |
| 合并标准 | "维护者可靠性 + 无回归" | 长期执行，但2025年仍有激烈拒绝措辞 | ✅ 标准一致，执行方式有争议 |
| Nvidia 对抗 | 公开羞辱推动封闭厂商改变 | 12年后 Nvidia 开源驱动，效果实现 | ✅ 目标一致，代价是形象损耗 |
| systemd 争议 | 内核层面中立，维护者责任绝不妥协 | 拒绝 Kay Sievers，但不干涉发行版 systemd 决策 | ✅ 逻辑一致 |
| 2018年道歉 | "我需要改变行为" | 改变是真实的但不彻底，激烈措辞未完全消失 | ⚠️ 部分一致 |
| Rust 支持 | "支持 Rust 进入内核" | 合并基础设施，但仲裁社区冲突时偏向 C 文化 | ⚠️ 存在张力 |

### 核心模式分析

**模式一：工程实用主义压倒意识形态**
Torvalds 的每一个重大决策都能找到具体的工程理由。他拒绝 GPLv3 是因为 Tivoization 条款干扰他认为合理的硬件设计权；他接受 Rust 是因为内存安全有实际价值；他创建 Git 是因为现有工具不够好。当"原则"与"工程实效"冲突时，工程实效通常获胜。

**模式二：维护者信任制度是核心机制**
Torvalds 最重要的技术判断不是评估某段代码，而是评估某个人。CFS vs SD 调度器之争（选 Ingo 因为他可靠）、拒绝 Kay Sievers（因为他不修 bug）——都是对人的判断，而非代码的判断。这个机制在内核规模增长后变得更加核心，因为 Torvalds 物理上无法审查所有代码。

**模式三：愤怒是工具，而非失控**
Torvalds 的公开爆发（Nvidia 事件、LKML 骂人）在他看来是有目的的：推动改变、划定边界、快速过滤不合格的参与者。问题在于这个"工具"造成了真实的人员流失——女性开发者比例长期偏低，部分有能力的开发者在遭受公开羞辱后退出了内核社区。

**模式四：公开表态 → 私下执行，落差存在**
2018年道歉是公开且诚恳的，但Torvalds 在2025年仍被记者记录到使用"garbage"等攻击性标签。他对"行为改变"的定义可能比外部观察者期待的更窄：他减少了"人身攻击"，但保留了"激烈的技术批判"。

**最关键的言行不一致案例**
Torvalds 批评 systemd 社区和 Poettering 树立了"坏榜样"、制造了"不欢迎的氛围"——但 Poettering 对 Torvalds 的具体指控（"retroactively aborted"等言论）正好说明 Torvalds 自己是这种文化氛围最重要的来源。他批评别人造成的问题，部分上是他自己造成的。这是最清晰的言行矛盾案例。

---

## 信息来源

- [History of Linux - Wikipedia](https://en.wikipedia.org/wiki/History_of_Linux)
- [Git turns 20: A Q&A with Linus Torvalds - GitHub Blog](https://github.blog/open-source/git/git-turns-20-a-qa-with-linus-torvalds/)
- [BitKeeper, Linux, and licensing disputes: How Linus wrote Git in 14 days - Graphite](https://graphite.com/blog/bitkeeper-linux-story-of-git-creation)
- [Linus Torvalds says GPL was defining factor in Linux's success - CIO](https://www.cio.com/article/238985/linus-torvalds-says-gpl-was-defining-factor-in-linuxs-success.html)
- [Celebrating 30 years of the Linux kernel and the GPLv2 - Red Hat](https://www.redhat.com/en/blog/celebrating-30-years-linux-kernel-and-gplv2)
- [Linus Torvalds Calls NVIDIA The Worst Company Ever - Phoronix](https://www.phoronix.com/news/MTEyMTc)
- [12 years after publicly telling Nvidia "Fuck you" - ResetEra](https://www.resetera.com/threads/12-years-after-publicly-telling-nvidia-fuck-you-linus-torvalds-now-considers-them-to-be-doing-really-good-work-on-linux.963084/)
- [Linux kernel's Torvalds: 'I am truly sorry' - The Register](https://www.theregister.com/2018/09/17/linus_torvalds_linux_apology_break/)
- [After Years of Abusive E-mails, the Creator of Linux Steps Aside - LWN.net](https://lwn.net/Articles/765674/)
- [Linux systemd dev says open source is 'SICK' - The Register](https://www.theregister.com/2014/10/06/poettering_says_linux_kernel_community_is_hostil/)
- [Linus Torvalds says Rust is coming to the Linux kernel - The Register](https://www.theregister.com/2022/06/23/linus_torvalds_rust_linux_kernel/)
- [Torvalds weighs in on 'nasty' Rust vs C for Linux debate - The Register](https://www.theregister.com/2024/09/19/torvalds_talks_rust_in_linux/)
- ['Maybe the problem is you' - FreeBSD Forums / The Register](https://forums.freebsd.org/threads/maybe-the-problem-is-you-linus-torvalds-wades-into-linux-kernel-rust-driver-drama.96732/)
- [Rust Drama, Russian Kernel Maintainers & Other Top Linux Kernel Happenings Of 2024 - Phoronix](https://www.phoronix.com/news/Top-Linux-Kernel-News-2024)
- [Submitting patches: the essential guide - Linux Kernel Documentation](https://docs.kernel.org/process/submitting-patches.html)
- [Linux Creator Torvalds Says Rust Adoption in Kernel Lags Expectations - Slashdot](https://linux.slashdot.org/story/24/08/23/1857221/linux-creator-torvalds-says-rust-adoption-in-kernel-lags-expectations)
