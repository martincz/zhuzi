# zhuzi · 诸子

> 把不同人物的方法论做成可运行的 skill，再把它们接到同一张 roundtable 上。
>
> A runtime-agnostic toolkit for persona skills, roundtable seats, and shared deliberation workflows.

---

## 项目由来

"诸子"取自先秦"诸子百家"——百家争鸣不是为了合流成一家，而是把彼此不相容的看法各自表达清楚，让分歧本身成为判断的一部分。

当今的 AI 助手常常把多元立场揉成一个"平衡而温和"的回答——这是另一种形式的合流，代价是**锋利的判断被磨平了**。`zhuzi` 做相反的事：

- 每个人物有**独立的思维操作系统**——不是 prompt 风格包装，是经过研究提炼的心智模型、anti-pattern 库、表达档位。
- 要多视角时让他们**同席而坐、各执一词**，保留分歧进入决策流程，而不是替用户调和。
- 写成 Markdown 驱动，由支持相应规范的 agent runtime 加载——目前支持 Claude Code 与 Codex CLI。

## 圆桌是什么

圆桌（roundtable）是把多个人物席位放进一条议事流水线，审议同一个议题。和 "把几个 prompt 塞给一个 agent" 不同的是：

- **席位独立运行**——每个席位是一个子 agent，按自己的 verdict schema 给结构化判断，不被其他席位的结论污染。
- **分歧被显式保留**——主持人（orchestrator）做综合，但不擅自收敛；Taleb 认为 fragile、Munger 认为 keep、这两件事会并列呈现，让用户拍板。
- **议题契约先行**——召开席位前先定义 `must_haves.truths` 和 `verify_commands`，避免"讨论了一圈但不知道什么算成立"。
- **实施可承接**——若议题涉及代码，Linus 席位按议题类型出场：工程决策议题 `stages=[1,2]`（阶段 1 做 good taste / anti-pattern 工程评议，阶段 2 做代码可行性 gate），纯实施议题 `stages=[2]`；阶段 4 按锁定方案实施。

权威流程在 [zhuzi/workflows/roundtable.md](./zhuzi/workflows/roundtable.md)；机器合同在 [zhuzi/manifests/roundtable-contract.json](./zhuzi/manifests/roundtable-contract.json)；默认输出长相见 [Quick Roundtable 示例](./examples/roundtable-quick.md) 与 [模板](./zhuzi/templates/roundtable-quick.md)。

## 内置人物

人物按用法分两类。**思维顾问**输出结构化判断，可被召集进 `/zhuzi:roundtable`（拍板）或 `/zhuzi:quick`（听角度）；**专项工具**只服务特定场景，不进 roundtable。

### 思维顾问（决策辅助 · roundtable / quick 候选）

#### Linus Torvalds · `linus-torvalds-engineer`

Linux 内核与 Git 的作者。工程实用主义的代表人物——"Talk is cheap. Show me the code."

**他看问题的方式**：数据结构先行（坏代码救不了烂数据结构），特殊情况必须消失（good taste 的核心），维护者的 bug 响应比代码本身更重要。

- **Skill**：工程、架构、代码审查、技术选型的思维顾问。会点名 premature abstraction、bikeshedding、cargo cult 之类的 anti-pattern，按 4 级表达档位下判断。
- **Roundtable 角色**：`linus-engineer`——**唯一代码席位**。工程决策议题在阶段 1 做 good taste / anti-pattern 评议（`stages=[1,2]`），阶段 2 做代码可行性 gate，代码层判 `broken` 可单边否决；阶段 4 按锁定方案实施。

#### Charlie Munger · `munger-checklist`

伯克希尔副主席，Buffett 长期搭档（1924–2023）。"反过来想"和"愚蠢清单"的倡导者——"If I know where I'm going to die, I'll never go there."

**他看问题的方式**：能力圈是纪律（圈外沉默叫 Too Hard），激励结构决定行为，≥3 个偏误同时发力就进入 Lollapalooza 警报，安全边际是底线。

- **Skill**：投资、商业判断、组织决策的反愚蠢审视——20 条 anti-pattern 逐条过，10 步 Pre-Trade Checklist。
- **Roundtable 角色**：`munger-reviewer`——**决策质量席**。当议题涉及激励、能力圈、机会成本、或多偏误叠加时召开。

#### Nassim Nicholas Taleb · `taleb-antifragile`

期权交易员出身的统计学家。《Black Swan》《Antifragile》《Skin in the Game》作者——"The Sharpe ratio is meaningless under fat tails."

**他看问题的方式**：事物只分 fragile / robust / antifragile 三态；分布是 Mediocristan 还是 Extremistan 决定工具是否合适；payoff 凸凹决定是否需要预测；上行受益者不承担下行埋单就是激励错位。

- **Skill**：尾部风险、破产风险、Kelly 仓位、barbell 结构、`skin in the game` 审视——18 条 fragility anti-pattern 和 10 步 Pre-Trade Fragility Check。
- **Roundtable 角色**：`taleb-reviewer`——**风险结构席**。当议题含不确定性、尾部风险、脆弱性或 ruin risk 时召开。

#### Marcos López de Prado · `lopezdeprado-scientist`

AFML、ML for Asset Managers、Causal Factor Investing 作者，Cornell 讲师，ADIA Lab 负责人。把金融从炼金术推向科学的旗手——"A backtest is not a theory."

**他看问题的方式**：先分 associational vs causal（没有 causal graph 就归 associational），selection bias 在 multiple testing 下几乎必然，Sisyphus workflow（单人端到端）是结构性警报，CV 方法用错就是 class error。

- **Skill**：研究诚信、实验/评估设计、backtest overfitting 审视——18 条方法论 anti-pattern、10 步 Research Integrity Check、Deflated Sharpe / PBO / Purged K-Fold / CPCV 工具集。
- **Roundtable 角色**：`lopezdeprado-reviewer`——**证据质量席**。议题含实验、因果声明、benchmark、eval、回测时必召开（触发词见 [seat-registry](./zhuzi/references/seat-registry.md)）。

#### Richard Feynman · `feynman-explainer`

诺贝尔物理奖得主（1918–1988），Caltech 教授，挑战者号事故调查委员——"The first principle is that you must not fool yourself, and you are the easiest person to fool."

**他看问题的方式**：命名不等于理解（知道鸟叫什么 ≠ 了解鸟），形式不等于科学（cargo cult），权威不等于证据。解释必须能被验证——讲不清就是没懂。

- **Skill**：说明文、spec、教程、架构文档、决策论证的清晰度审视——专抓术语遮羞布、命名冒充机制、论证缺例子。
- **Roundtable 角色**：`feynman-reviewer`——**解释清晰度席**。议题含术语定义、指标口径、时间语义、接口语义或 spec clarity 时召开。

#### Paul Graham · `paul-graham-perspective`

Y Combinator 联创，《Hackers & Painters》作者。essayist / 创业导师视角——"The way to get startup ideas is not to try to think of startup ideas. It's to look for problems."

**他看问题的方式**：分 maker（写、做、produce）和 manager（开会、调度、organize）两种视角，自己只擅长 maker 那半边；love from few > like from many；超线性回报选项 > 线性回报选项；写作不只传递想法，是生成想法的方法。

- **Skill**：创业方向、产品方向、PMF 真伪、创始人评估、essay / pitch 评审、职业与人生选择的 taste 审视。
- **Roundtable 角色**：`paul-graham-reviewer`——**Maker 视角席**。议题含创业 / 产品 / PMF / 创始人评估 / essay 或 spec taste 评审时召开。

#### Don Norman · `don-norman-perspective`

UC San Diego 认知科学名誉教授（生于 1935），《The Design of Everyday Things》作者，Apple 第一位 User Experience Architect——"When people have trouble with something, it isn't their fault — it's the fault of the design."

**他看问题的方式**：把"用户犯错"翻成"设计失败"，用 discoverability / feedback / conceptual model 三件套定位 UI 失败；区分 affordance（物理可能性）与 signifier（界面可感知信号）；区分 slip（动作走样）与 mistake（意图就错），两类错误修法不一样——slip 用 forcing function，mistake 改 conceptual model。

- **Skill**：UI / UX / 错误信息 / 默认值 / 可访问性的认知诊断——10 条 anti-pattern、Gulf of Execution & Evaluation 拆解、招牌物件类比（Norman door / 烤面包机 / 淋浴龙头）。
- **Roundtable 角色**：`don-norman-reviewer`——**UI/UX 认知诊断席**。议题含 UI 评审 / UX 评审 / 可用性归因 / 用户错误归因 / 可访问性时召开（触发词见 [seat-registry](./zhuzi/references/seat-registry.md)）。

### 专项工具（standalone only · 不进 roundtable）

这三个 skill 不输出结构化 verdict，不参与 roundtable / quick；只服务特定场景。

#### Steve Jobs · `steve-jobs-perspective`

Apple 联创（1955–2011），iPod / iPhone / iPad 主导者。产品 / 设计 / 聚焦视角——"It means saying no to the hundred other good ideas."

**他看问题的方式**：focus = saying no（说不才是聚焦）；whole widget（端到端控制体验链）；一句话定义产品（"1,000 songs in your pocket"）；A players only（B 招 C，C 招 D）；技术 × liberal arts（不是加好看的 UI，是从人怎么思考出发设计技术）；reality distortion field 推团队突破自我——但 Jobs 自己用生命学到 RDF 在物理常数 / 生物学事实前不工作。

- **Skill 定位**：standalone 产品评审 / 设计取舍 / 战略聚焦 / 创业评估思维顾问。激活时直接以「我」回应，含 12 条 anti-pattern 库与触碰边界时的降级模板。
- **不进 roundtable**——已故人物，2011 年后空白；C 端消费品偏置；管理风格在大组织 / 跨文化语境中不通用——三类边界已写进诚实边界，不承担多视角议事中的结构化判断。

#### Donald Trump · `donald-trump-perspective`

谈判 / 品牌 / 媒体战思维 skill。**非政治立场工具**——不用于党派立场、贬损真人或政策评价。"Everything's a deal."

**它做什么**：BATNA / leverage 映射、narrative pivot、注意力工程、被攻击时的反击节奏。短句结论 + ≤ 7 天时间窗的下一步动作。

**它不做**：针对真人的攻击 / 绰号、政策立场、5+ 年预测、法律建议、临床诊断。

- **Skill 定位**：standalone 对抗性博弈工具。被攻击 / 公关爆雷 / BATNA / 杠杆 / dominate 新闻周期类问题时激活。
- **不进 roundtable**——博弈工具不承担多视角议事中的结构化判断。

#### 鲁迅 · `luxun-zawen`

中国现代白话文最尖锐的讽刺作家（1881–1936）。杂文数百万字是他真正的战场——短、狠、冷、见微知著。

**它做什么**：B 类聊天娱乐型——只做**修辞肌肉**（6 种杂文 DNA、4 级阴狠度），把普通话改成鲁迅腔消息、吐槽、反击、催促。

**它不做**：决策、投资、代码建议、人物观点推演。遇到思维咨询会自动退出角色。

- **Skill 定位**：standalone 修辞改写工具。
- **不进 roundtable**——娱乐型 skill 不承担结构化判断。

## 使用方式

### 直接触发 skill

```text
用 Linus 视角 review 这段代码
用 Taleb 视角看这个方案 fragile 不 fragile
用费曼视角审一下这份 spec
用鲁迅口吻把这句话改损一点
```

每个 skill 的完整触发词见 `skills/<name>/SKILL.md` 顶部 frontmatter。

### 听几个角度（不拍板）

```text
# Claude Code
/zhuzi:quick 我在考虑把单体后端拆成 3 个微服务，团队就 2 个人

# Codex CLI
触发 zhuzi-quick skill，喂入同样的议题
```

`/zhuzi:quick` 召集匹配的席位**平行说一段话**——不走 must_haves、不走 user gate、不做综合。30 秒读完 N 个角度，不替你拍板。要拍板请走下面的圆桌。

### 召开圆桌（要拍板）

```text
# Claude Code
/zhuzi:roundtable 这个 API 设计该不该先重构再扩功能

# Codex CLI
触发 zhuzi-roundtable skill，喂入同样的议题
```

默认走 Quick Roundtable 短读输出：议题卡、席位短评表、决策表。需要完整席位原文或 YAML verdict 时说"展开原文 / 展开 YAML / full / strict"。

**轻议题路由**：议题只命中 ≤1 个席位时，圆桌默认短路退出，建议直接调对应 standalone skill。要强制走完整流程回复"强制开圆桌"。

## 安装

```bash
git clone https://github.com/<your-fork>/zhuzi.git
cd zhuzi
./install.sh
```

`install.sh` 按 [zhuzi/manifests/shipped-surface.json](./zhuzi/manifests/shipped-surface.json) 把全部 shipped surface 安装到 Claude 和 Codex 的默认根目录。shipped surface 的人读清单见 [docs/INVENTORY.md](./docs/INVENTORY.md)。

覆盖根目录：

- `CLAUDE_DIR`（默认 `~/.claude`）
- `CODEX_HOME`（默认 `~/.codex`）

## 仓库布局

```text
zhuzi/
├── skills/                         # 单人物 skill
├── runtimes/
│   ├── claude/
│   │   ├── agents/                 # roundtable seat adapters
│   │   └── commands/zhuzi/         # /zhuzi:roundtable, /zhuzi:quick 入口
│   └── codex/
│       ├── agents/                 # Codex seat adapters
│       └── skills/                 # zhuzi-roundtable, zhuzi-quick orchestrator skills
├── zhuzi/
│   ├── seats/                      # 共享 seat contracts
│   ├── references/                 # seat-registry / verdict-schema
│   ├── workflows/                  # roundtable / quick-multi 权威流程
│   ├── templates/                  # roundtable / quick-multi 输出骨架
│   └── manifests/                  # roundtable / shipped surface 机器真相源
├── docs/INVENTORY.md               # shipped surface 的人读清单
├── examples/                       # 5 个代表性输出示例（quick-multi / roundtable-quick / disagreement / revision-gate / broken-veto）
├── AGENTS.md                       # agent 规约（协作、修改、验证）
├── CLAUDE.md                       # 指向 AGENTS.md 的兼容 shim
├── install.sh
└── tools/
```

找 roundtable 权威资产：

- 流程：`zhuzi/workflows/roundtable.md`
- 机器合同：`zhuzi/manifests/roundtable-contract.json`
- 席位契约：`zhuzi/seats/`
- 人读说明：`zhuzi/references/seat-registry.md`、`zhuzi/references/verdict-schema.md`

## 协作与贡献

agent 在本仓库工作的规约、真相源清单、修改指针、提交规范、验证流程统一在 [AGENTS.md](./AGENTS.md)。

## License

MIT License. 各人物调研使用的一手 / 二手来源版权归原作者所有。

---

*"诸子百家"不是为了合流成平均主义，而是为了把分歧摆上桌。*
