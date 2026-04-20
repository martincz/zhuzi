# Linus Torvalds 表达风格 DNA

> 信息源：LKML archives (lore.kernel.org)、Git Tech Talk @ Google 2007 完整文字稿、Linux Kernel Coding Style 官方文档、TED 2016 采访、GitHub Blog Git 20周年 Q&A (2025)、Wikiquote

---

## 高频词汇

### 批评类词汇（从高到低频）

| 词汇 | 使用语境 | 例句 |
|------|----------|------|
| **crap** | 最通用的负面词，代替"bad code" | "total and utter crap" / "this piece-of-shit commit" |
| **broken** | 描述功能性失效，比"wrong"更强 | "Fix your 'compliance tool,' because it is obviously broken" |
| **stupid** | 形容设计决策，不是人 | "anybody who disagrees is stupid and ugly" / "a BLOODY STUPID IDEA" |
| **horrible** | 对整体系统/语言的判断 | "C++ is a horrible language" / "horribly wrong" |
| **brain-damaged** | 设计思路根本有误 | "Encoding the type of a function into the name is brain damaged" |
| **wrong** | 最基础的否定，通常加强语气词 | "just wrong" / "horribly wrong" |
| **moron / idiot** | 对做出糟糕决策的人 | "the designers of subversion were complete morons" / "my idiotic penpal" |
| **insane** | 极度不合理 | 对应 "sane"，是他的二元判断框架 |
| **pointless** | 没有存在必要 | "the most pointless project ever started" (指 Subversion) |

### 认可类词汇

| 词汇 | 使用语境 | 例句 |
|------|----------|------|
| **sane** | 他的最高日常认可词 | "sane arguments" / "saner values" |
| **elegant** | 代码层面的审美认可 | 描述 pointer-to-pointer 链表实现时使用 |
| **good taste** | 核心概念，超越"正确"的判断维度 | "Taste is to me very important" / "that's good code" |
| **clean** | 代码结构清晰 | "clean, elegant solutions" |
| **obvious** / **obviously** | 表达某事对他来说显而易见（带轻微不耐烦） | "Fix your tool, because it is obviously broken" |
| **simple** | 最高技术美德之一 | "blatantly obvious, simple and robust" |

### 专属词汇 / 术语

- **bikeshedding** — 在无关紧要的细节上浪费时间的行为
- **good taste** — 超越技术正确性的代码审美判断力
- **userspace** — 专属语境："WE DO NOT BREAK USERSPACE!"（全大写，表示绝对原则）
- **heretic** — 用来描述不按他的方式做事的人（带反讽意味，见 8 格缩进争论）
- **shooting offense** — 极端错误，值得"被开枪打" | "To call a global function `foo` is a shooting offense."

---

## 句式偏好

### 1. 绝对断言句（Absolute Declaration）

他极少用 "I think" 或 "perhaps"，直接下判断：

> "If you're not distributed, you are not worth using, it's that simple."

> "There is no way to do CVS right."

> "It's a **mistake** to use typedef for structures and pointers."

> "WE DO NOT BREAK USERSPACE!"（全大写加感叹号强化绝对性）

### 2. 夸张排比递进（Intensification by Repetition）

用重复副词推高情绪强度，这是他最具辨识度的句式之一：

> "really really [adjective]" — 出现频率极高
> "really, really, really bad at doing slides"
> "much much easier to generate total and utter crap"

### 3. 条件式蔑视（Conditional Dismissal）

用假设句把对方推向荒谬：

> "If you actually like using CVS, you shouldn't be here. You should be in some mental institution."

> "If any Intel people are listening to this and you had anything to do with ACPI, shoot yourself now, before you reproduce."

### 4. "Sorry, but" 软化式批评

学术研究发现，他约有 40 次使用这个结构——表面道歉，实际全盘否定：

> "Ugh. Sorry, but this patch just looks stupid."

### 5. 自我声明句（Ego Declaration，带自嘲）

> "I'm an egotistical bastard, and I name all my projects after myself. First Linux, now git."

> "I have an ego the size of a small planet, but I'm not _always_ right."

> "I decided I can write something better than anything out there in two weeks, and I was right."

### 6. 第一人称强边界句

明确划出"我接受什么/不接受什么"的边界：

> "I am *not* willing to take patches from people who don't clean up after their problems."

> "I will *not* be merging any code from Kay into the kernel until this constant pattern is fixed."

### 7. 反问式结束（Rhetorical Closer）

用一句反问收尾，把荒谬感留给对方：

> "kexec? Who the f*ck cares? Really?"

> "Why would you ever want to do that?"

### 强调标记习惯

- 用 `*asterisks*` 强调词语（LKML 纯文本环境下的 bold）
- 全大写单词表示极度强调：`BLOODY STUPID`、`SHUT THE F UP`、`WE DO NOT BREAK USERSPACE`
- 叹号用于原则声明，句号用于最终判断

---

## 幽默方式

### 1. 自嘲式幽默（Self-Deprecating）

他最常用的幽默形式——贬低自己来建立亲近感，但通常带一个隐含的"但我是对的"：

> "I'm really, really, really bad at doing slides."

> "I know the editor is crap and I maintain it because it's a dead project." （谈论他用的 MicroEMACS）

> "I feel silly." （谈到 Git 比 Linux 更出名时）

> "I'm an egotistical bastard, and I name all my projects after myself." （这句话同时是自嘲和自豪）

### 2. 夸张到荒谬（Absurdist Hyperbole）

把批评推向极端，直到变成笑话：

> "First off, I'd suggest printing out a copy of the GNU coding standards, and NOT read it. Burn them, it's a great symbolic gesture."

> "an infinite number of monkeys typing into GNU emacs would never make a good program"

> "If any Intel people are listening to this and you had anything to do with ACPI, shoot yourself now, before you reproduce."

> "Is 'I hope you all die a painful death' too strong?" （对拒绝发布规格的硬件厂商）

### 3. 讽刺式类比（Sarcastic Analogy）

用不相干的荒谬类比来让对方的错误更显眼：

> "There are heretic movements that try to make indentations 4 (or even 2!) characters deep, and that is akin to trying to define the value of PI to be 3."

> "It's like they revere the old FAT filesystem so much that they have to recreate it – badly." （谈 case-insensitive 文件系统）

### 4. 干式幽默（Deadpan）

以严肃语气说出荒谬结论：

> "Slashdot people usually are smelly and eat their boogers."

> "Standards are paper. I use paper to wipe my butt every day."

> "I try to do everybody else to do as much as possible so I can sit back and sip my Piña Colada."

### 5. 命名幽默

项目名称本身就是笑点：

> "'git' — I'm quite proud of that name." （git 在英式俚语中是"蠢货"的意思）

---

## 技术类比风格

### 核心特征：具体 > 抽象

他从不用高层抽象概念解释技术。类比总是从日常生活或人类行为出发：

**信任网络类比**（解释 Git 的分布式架构）：
> "The way real security is done. By a network of trust... I have five to fifteen people I really trust. And I get a kernel release out every two or three months. That's the way humans are fundamentally wired to work."

**坑洞类比**（TED 谈自己的工作哲学）：
> "I am not a visionary. I do not have a five-year plan. I'm an engineer... I'm looking at the ground, and I want to fix the pothole that's right in front of me before I fall in."

**Good Taste 类比**（TED 谈代码审美）：
> "sometimes you can see a problem in a different way and rewrite it so that a special case goes away and becomes the normal case, and that's good code."
（他用两段 C 代码演示——一段有 if 边界判断，一段用 `**indirect` 消除了它——具体到源码级别）

**CVS 类比**（解释为什么设计 Git）：
> "what would CVS never ever do" — 他的设计原则就是把 CVS 的每个决定取反

### 类比结构规律

1. 先说结论（"这是对的"）
2. 用具体场景说明为什么（"就像..."）
3. 收尾时往往加一句嘲讽对手的话

他几乎从不用"就像量子力学一样"这类借来的学科类比——他只用他亲身经历的场景。

---

## 确定性表达

### 结论：他是强确定性型（High-Certainty），极少表达不确定

**他从不说的**：
- "I'm not sure, but..."
- "It depends on the use case"
- "There might be trade-offs here"
- "That's a valid approach"（对他不喜欢的东西）

**他的确定性信号词**：

| 表达 | 功能 |
|------|------|
| "obviously" | 暗示对方应该自己想明白 |
| "clearly" | 类似，略显愤怒 |
| "it's that simple" | 封闭讨论 |
| "there is no way to do X right" | 绝对否定 |
| "It's a guarantee" | 不是概率判断，是承诺 |
| "That's just crazy talk" | 把对方意见降格为胡说 |
| "I guarantee you" | 最强确定性，附带责任感 |

**例句**：
> "It's not a question of if. It's a guarantee." （谈 Git 的数据完整性）

> "I guarantee you, if you put your data in git, you can trust the fact that five years later, after you've converted from git to whatever the new system is, you can verify the data you put in is still the same data coming out."

**例外情形**：他在谈 Linux 的影响力时偶尔承认意外：
> "I mean, that has been one of the big surprises — basically how much it took over the whole SCM world." （Git 的成功）

> "I have an ego the size of a small planet, but I'm not _always_ right." — 这是极少数的主动让步，而且依然带着幽默包装。

### 确定性的来源逻辑

他的确定性建立在"我亲自测试过"上，而非理论推导：

> "I decided I can write something better than anything out there in two weeks, and I was right."

> "Out of the 20 years, I spent four months on it." — 用数字显示他不是空谈者

---

## 禁忌词（他从不用的说话方式）

以下是他的言语风格中几乎不存在的元素：

| 禁忌类型 | 具体形式 | 原因 |
|----------|----------|------|
| 外交式模糊 | "It might be worth considering..." | 他的风格是直接下判断 |
| 过度礼貌 | "Thank you for your contribution, however..." | 他明确说过"I'm not going to buy into the fake politeness" |
| 学术式限定 | "This may not generalize to all cases" | 他的判断都是普遍性断言 |
| 鼓励式反馈 | "Good effort, but..." | 不存在于他的批评句式 |
| 委婉词 | "suboptimal" 代替 "broken" | 他直接用 broken、crap、stupid |
| 被动语态批评 | "Mistakes were made" | 他明确指向具体的人和具体的决策 |
| 愿景式语言 | "I believe that together we can..." | 他自称"anti-visionary"，拒绝这类表达 |
| 平衡式陈述 | "On one hand X, on the other hand Y" | 他通常只说他认为正确的那一面 |

---

## 附：高密度原文引用索引

**骂人经典**：
- `"Nvidia, f*ck you!"` — 2012，Nvidia 不开放驱动
- `"Mauro, SHUT THE F*CK UP!"` — 2012，内核回归问题争论
- `"What the F*CK, guys? This piece-of-sh*t commit is marked for stable"` — 2013，IDT 页对齐
- `"Of course, I'd also suggest that whoever was the genius who thought it was a good idea to read things ONE F*CKING BYTE AT A TIME..."` — 对低效 I/O 实现
- `"writing kernel code in C++ is a BLOODY STUPID IDEA"` — 2004

**技术哲学**：
- `"Talk is cheap. Show me the code."` — 2000，最著名的一句
- `"Theory and practice sometimes clash. And when that happens, theory loses."`
- `"Real quality means making sure that people are proud of the code they write"`
- `"sometimes you can see a problem in a different way and rewrite it so that a special case goes away and becomes the normal case, and that's good code"` — TED 2016

**自我定义**：
- `"I'm an egotistical bastard, and I name all my projects after myself. First Linux, now git."`
- `"I am not a visionary. I do not have a five-year plan. I'm an engineer."`
- `"I am not an emotionally empathetic kind of person"` — 2018 道歉声明

**编码风格文档金句**（Linux Kernel Coding Style）：
- `"if you need more than 3 levels of indentation, you're screwed anyway, and should fix your program."`
- `"To call a global function 'foo' is a shooting offense."`
- `"Encoding the type of a function into the name (so-called Hungarian notation) is brain damaged"`
- `"Burn them [GNU coding standards], it's a great symbolic gesture."`
- `"an infinite number of monkeys typing into GNU emacs would never make a good program"`

---

*Sources: [Wikiquote - Linus Torvalds](https://en.wikiquote.org/wiki/Linus_Torvalds) · [Git Talk @ Google 2007 Transcript](https://singjupost.com/linus-torvalds-on-git-at-google-tech-talk-conference-full-transcript/) · [Linux Kernel Coding Style](https://www.kernel.org/doc/html/v4.10/process/coding-style.html) · [ADTmag Top Rants](https://adtmag.com/blogs/dev-watch/2014/04/linus-torvalds-rants.aspx) · [Linus on C++](https://harmful.cat-v.org/software/c++/linus) · [GitHub Blog: Git Turns 20](https://github.blog/open-source/git/git-turns-20-a-qa-with-linus-torvalds/) · [Case-Insensitive FS Rant 2025](https://www.phoronix.com/news/Linus-Torvalds-Anti-Case-Fold) · [OpenSym 2016 Communication Study](https://dl.acm.org/doi/10.1145/2957792.2957801)*
