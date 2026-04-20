# Linus Torvalds 完整时间线

> 信息截止日期：2026年4月17日  
> 主要来源：Wikipedia、The Register、Phoronix、LWN.net、LKML

---

## 关键时间线

| 年份 | 事件 | 思维影响 |
|------|------|----------|
| **1969** | 12月28日出生于芬兰赫尔辛基，祖父是记者/诗人 Ole Torvalds，外祖父是统计学家 Leo Törnqvist | 书香家庭，数学与文字并重的环境 |
| **1980** | 约10岁，在外祖父的 Commodore VIC-20 上开始自学编程 | 早期独立自学者，无导师引导，纯靠兴趣驱动 |
| **1988** | 进入赫尔辛基大学计算机系 | 正式系统学习操作系统理论 |
| **1989** | 入伍芬兰海军 Nyland Brigade，服11个月军官训练役 | 中断学业，磨砺纪律性 |
| **1990** | 复学，首次接触 Unix（DEC MicroVAX/ULTRIX），购买 Tanenbaum 的《操作系统设计与实现》 | 对 MINIX 的局限性产生强烈不满，种下"自己写OS"的念头 |
| **1991年1月** | 购入 Intel 80386 PC，拿到 MINIX 副本，开始动手 | 从消费者转变为创造者的关键节点 |
| **1991年8月25日** | 在 comp.os.minix 发布历史性帖子："我在做一个（免费的）操作系统……只是一个爱好，不会像 GNU 那么大那么专业" | 低调发布，完全没有预见到未来的规模 |
| **1991年9月** | Linux 0.01 通过 FTP 公开，仅支持 Intel 386，约1万行代码 | 开放源码从第一天就是核心选择 |
| **1992** | 将 Linux 许可证从私有改为 GPL（GNU General Public License） | 理解到 GPL 的"病毒性"对内核传播的战略价值 |
| **1993** | 内核代码突破10万行，发行版 Slackware、Debian 相继出现 | 社区生态开始脱离个人掌控，进入分布式维护模式 |
| **1994年3月** | **Linux 1.0.0 发布**，17万行代码，支持多文件系统、IPv4、多架构 | 从"玩具"到"可用系统"的心理转变 |
| **1996年6月** | **Linux 2.0 发布**，支持 SMP（多处理器），大规模商业部署开始 | 认识到企业级需求与个人爱好项目的张力 |
| **1996年底** | 访问 Transmeta 公司（加州圣克拉拉），决定接受 offer | 首次走向商业化，离开芬兰 |
| **1997年2月** | 加入 Transmeta，主要工作是 x86 代码变形与低功耗 CPU 研发，兼顾 Linux 开发 | 在商业环境中保持开源项目的双线并行 |
| **1999年** | 获得美国永久居留权，随后入籍 | 从芬兰人变为芬兰裔美国人 |
| **2003年6月** | 离开 Transmeta，加入 **OSDL（Open Source Development Labs）**，首次以 Linux 为全职工作 | Linux 基金会薪水的核心逻辑：让内核维护者不依赖商业雇主 |
| **2004年6月** | 举家迁居俄勒冈州 Dunthorpe，靠近 OSDL 总部（Beaverton） | 稳定生活节奏，远离硅谷喧嚣 |
| **2005年4月3日** | **创建 Git**，起因是 BitKeeper 撤销对内核项目的免费授权，Torvalds 用两周时间写出 Git 初版 | 愤怒驱动的创造；"工具应该服务于开发流程，而不是反过来" |
| **2007年** | OSDL 与 Free Standards Group 合并为 **Linux Foundation**，Torvalds 随之转移 | 机构化支撑开源，减少个人财务风险 |
| **2011年** | **Linux 3.0 发布**（版本号重置），纯符号性，无重大架构变化 | Torvalds 明确表示版本号只是数字，不代表"革命" |
| **2015年** | **Linux 4.0 发布**，引入 live kernel patching（kpatch/livepatch） | 运维友好性开始进入内核核心目标 |
| **2015年** | 在接受媒体采访时说："我不是好人，我不关心你，我关心技术和内核" | 这是2018年道歉前最典型的"Torvalds风格"自画像 |
| **2018年9月** | **发表公开道歉信，宣布短暂休假**。原话："我的言语攻击是不专业和不必要的……我需要学习理解他人情绪并作出适当回应" | 最重要的思维转折点（详见下节） |
| **2018年9月** | Linux 内核采用 **Contributor Covenant 行为准则（CoC）** | 机构化约束个人行为，承认"文化即制度" |
| **2019年3月** | **Linux 5.0 发布**，增强性能与安全特性 | 持续演进，无戏剧性 |
| **2022年10月** | **Rust 语言被正式合并进 Linux 内核**（作为实验性支持），允许用 Rust 编写内核驱动 | Torvalds 的态度：开放但不强迫，"如果有人能用 Rust 写出好代码，我不会拒绝" |
| **2023年** | **Linux 6.x 系列持续迭代**（6.1、6.2、6.3……），6.1 成为 LTS 版本 | 稳定的双月发布节奏已成惯例 |
| **2024年8月** | Torvalds 在 Open Source Summit 表示 Rust 进内核"比预期慢"，部分原因是老内核开发者不愿学新语言 | 现实主义校准期望值 |
| **2024年10月** | Greg Kroah-Hartman 移除多名俄罗斯籍维护者。Torvalds 公开支持："这不会被回滚。如果你还没听说过俄罗斯制裁，你应该读读新闻。" | 地缘政治进入开源治理，Torvalds 明确表态不回避 |
| **2025年2月** | Hector Martin 因 Rust 合入内核的争议辞去 Asahi Linux 维护者职位。Torvalds 回应 Christoph Hellwig 的指控，澄清相关 PR 完全未触碰其维护代码 | 内核 Rust 集成争议公开化，Torvalds 直接介入调停 |
| **2025年2月** | LKML 发帖：Rust 内核政策讨论（lkml.org/lkml/2025/2/20/2066），Torvalds 确认 Rust 代码合入不凌驾于维护者反对之上 | 治理原则：共识优先，技术选型不强制 |
| **2025年11月** | 在首尔 Open Source Summit 表示 Rust "真正成为内核的一部分，不再只是实验性的" | 态度从观望转为正式认可 |
| **2026年1月** | **AI Slop 争论**：Torvalds 在 LKML 明确表态，写文档规范 AI 生成代码"没有意义"，因为"那些制造 AI slop 的人不会按规范标注" | 务实主义：规则只约束守规则的人 |
| **2026年1月** | Torvalds 在个人项目 AudioNoise（吉他效果器实验）中亲自使用 AI vibe coding 写了 Python 可视化工具 | 言行一致：个人玩具项目可以，生产内核代码不行 |
| **2026年2月8日** | 宣布 Linux 6.19 是最后的 6.x，**下一版本为 Linux 7.0**。原话："手指脚趾快数不过来了，所以下一个内核叫 7.0" | 版本号升级纯属个人喜好，无技术含义 |
| **2026年4月12日** | **Linux 7.0 正式发布**。Rust 支持从"实验性"升级为"正式支持"，同时包含 ARM/RISC-V/Loongson 改进、KVM AMD EPYC 5 支持、Self-healing XFS | 里程碑版本，标志 Rust 在内核中完成从实验到生产的跃迁 |

---

## 思维转折点

### 转折一：1991年——从用户到创造者

购入 386 PC 的动机最初只是"想用一个好操作系统"。MINIX 的授权限制（Tanenbaum 不允许修改分发）逼着 Torvalds 自己动手。这种"因不满而创造"的模式后来在 Git 上重演。

**核心心理**：看到工具的局限性时，第一反应是重写，而不是妥协。

---

### 转折二：1992年——选择 GPL，理解"病毒性"的力量

早期 Linux 0.01 使用私有许可证（禁止商业使用）。切换到 GPL 后，任何基于 Linux 的修改必须回流开源。Torvalds 后来承认，当时并不完全理解 GPL 的全部含义，但这个决定是 Linux 生态能够爆炸式增长的制度基础。

**核心心理**：开放不只是道德选择，是扩散策略。

---

### 转折三：2005年——Git的创造，愤怒的生产力

BitKeeper 撤销免费授权后，Torvalds 在两周内写出 Git 初版。他事后说，如果当时有任何现成工具能满足需求，他不会动手。Git 的设计哲学（分布式、每个节点都是完整仓库）直接反映了他对内核开发模式的理解。

**核心心理**：工具必须服从工作流，而不是反过来。强迫症级别的性能执念（Git 的速度设计）。

---

### 转折四：2018年——道歉与情感觉醒

这是 Torvalds 公开形象最大的一次转变。他在邮件中写道：

> "我的行为方式，包括几十年来对待其他人时缺乏同理心，是我需要处理的问题。我会花时间理解他人情绪，并学会更恰当地回应。"

背景：多年来他在 LKML 的语言风格极为强硬（"你的代码是垃圾"、"这是最愚蠢的想法"），这种风格在 GitHub 时代开始受到越来越大的社区压力。

**转变结果**：回归后，语气明显软化。但他明确表示这不是性格的彻底改变——他仍然直接、不回避批评，只是去除了人身攻击的成分。CoC 的引入同步提供了制度约束。

**核心心理**：承认情绪智力是可以学习的技能，而非固有品质。

---

### 转折五：2022-2025年——从怀疑到接受 Rust

Torvalds 最初对 Rust 进内核持谨慎态度，担心引入语言复杂性和社区分裂。随着实际 Rust 代码（尤其是驱动层）的积累，他的态度逐渐从"可以实验"转为"真正成为内核一部分"。Linux 7.0 中 Rust 完成正式化是这个转变的终点。

**核心心理**：证据优先。态度跟着代码质量走，不跟着意识形态走。

---

## 最新动态（2024-2026）

> 信息截止日期：**2026年4月17日**

### Linux 内核版本状态

- **Linux 7.0**：2026年4月12日正式发布，当前最新稳定版
- Rust 支持从实验性升级为正式支持（Linux 7.0 的标志性里程碑）
- 发布节奏维持双月周期，Torvalds 亲自主持 merge window 和 RC 公告

### LKML 重要表态

**Rust 政策（2025年2月）**
- Hector Martin 辞职风波后，Torvalds 在 LKML 明确：Rust 代码合入遵循共识原则，不会强行凌驾维护者反对
- 对 Christoph Hellwig 的指控逐条反驳，风格直接但有据可查
- 最终立场：Rust 是被欢迎的，但集成路径必须尊重子系统维护者

**俄罗斯维护者移除（2024年10月）**
- 支持 Greg Kroah-Hartman 的移除决定，原因是美国 OFAC 制裁合规要求
- 原话："我是芬兰人。你以为我会支持俄罗斯侵略？"

**AI Slop 讨论（2026年1月）**
- 明确反对通过文档规范来解决 AI 生成低质量代码的问题
- 论点：愿意遵守规范的人本就不是问题所在
- 内核项目后来确立"Assisted-by"标签制度：允许使用 AI，人类提交者承担完全责任

### 对 AI/LLM 的态度

Torvalds 的立场是务实二元论：

| 场景 | 态度 |
|------|------|
| 内核生产代码 | 高度审慎，AI 生成代码需经严格人工 review，错误由提交者负责 |
| 个人玩具项目 | 接受。他本人用 vibe coding 为 AudioNoise 写了 Python 可视化脚本 |
| AI 整体评价 | "90% 是炒作"（2024年），但承认工具"在进步" |
| AI 对编程未来 | 认为 AI 适合降低入门门槛，让普通人能驱动计算机完成任务；但对内核级系统编程持保留 |

### 对 Rust 进内核的最新评价

- 2025年11月首尔 Open Source Summit：**"Rust 真正成为内核的一部分，不再只是实验性的"**
- 承认进展比预期慢，原因是老一代内核开发者不熟悉 Rust
- Linux 7.0（2026年4月）将 Rust 正式化，完成了这个判断的落地

### 当前技术关注方向

1. **内核安全性**：持续强调内核代码质量高于新功能堆砌
2. **Rust 集成深化**：驱动层之外的子系统逐步引入 Rust
3. **AI 治理**：如何在开源社区建立人类责任机制，而非 AI 准入审查
4. **硬件多元化**：ARM、RISC-V、Loongson 架构支持（7.0 中有具体进展）
5. **个人项目**：AudioNoise（数字吉他效果器实验），他自称这是"纯粹的乐趣"

### 生活状态

- 继续居住在俄勒冈州，保持低调
- 全职受雇于 Linux Foundation，工作即是维护内核
- 公开露面主要在 Linux Foundation 的年度峰会（Open Source Summit 系列）
- 无社交媒体账号，信息输出集中在 LKML

---

*来源：[Wikipedia - Linus Torvalds](https://en.wikipedia.org/wiki/Linus_Torvalds) · [The Register - Linux 7.0](https://www.theregister.com/2026/04/13/linux_kernel_7_releaseed/) · [Phoronix - AI Slop](https://www.phoronix.com/news/Torvalds-Linux-Kernel-AI-Slop) · [LKML - Rust Policy 2025](https://lkml.org/lkml/2025/2/20/2066) · [The Register - Russian Maintainers](https://www.theregister.com/2024/10/23/linus_torvalds_affirms_expulsion_of) · [The Register - Rust Debate](https://www.theregister.com/2024/09/19/torvalds_talks_rust_in_linux/) · [Tom's Hardware - AI Code Policy](https://www.tomshardware.com/software/linux/linux-lays-down-the-law-on-ai-generated-code-yes-to-copilot-no-to-ai-slop-and-humans-take-the-fall-for-mistakes-after-months-of-fierce-debate-torvalds-and-maintainers-come-to-an-agreement)*
