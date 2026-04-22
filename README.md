# zhuzi · 诸子

> **诸子**——取诸子百家之意。每家思想是一种独立的思维操作系统；合起来，是一张可被支持 Skills / Agents / Commands 的 agent runtime 加载、可以**并排坐到同一张圆桌上审议一个议题**的多视角思维网。
>
> An agent-runtime toolkit that turns distinct thinkers into runnable cognitive operating systems — and wires them together into a **roundtable pipeline** where multiple perspectives deliberate on the same question in parallel, each returning a machine-readable verdict under a shared schema.

---

## 项目作用

zhuzi 把"诸子百家"做成一组可运行的 agent 思维席位：每一位人物代表一种稳定的方法论、边界和表达风格。你可以单独调用某一家的视角，也可以把多个席位放到同一张圆桌上，让它们围绕同一个议题各自审议、互相保留分歧，最后交给用户拍板。

这里的"诸子百家"强调保留不同学派的锋利边界：

- Linus 看代码结构、抽象层和 good taste。
- Munger 看愚蠢清单、能力圈、激励结构和 Lollapalooza。
- Taleb 看尾部风险、fragility、skin in the game 和凸性。
- López de Prado 看研究诚信、causal claim、backtest overfitting 和方法论纪律。
- 鲁迅只做杂文式文体改写，不参与决策审议。

圆桌的价值在于把"多视角建议"变成一个可执行流程：先定义议题成功必须满足的 `must_haves`，再让合适席位并行给出结构化 verdict，必要时修订契约，最后综合成可选择、可实施、可验证的决策表。

## 使用方式

| 用法 | 适合场景 | 结果 |
|---|---|---|
| 直接触发单个 skill | 想用某一家的视角审代码、看策略、改文体 | 模型以该人物的思维框架直接回应 |
| Claude：`/zhuzi:roundtable <议题>` | 议题需要多视角审议、存在策略/工程/方法论冲突 | 默认输出议题卡、席位短评和决策表；完整 YAML 可展开 |
| Codex：触发 `zhuzi-roundtable` skill | 同样的多席位审议，但通过 orchestrator skill 驱动 | 共享同一套 workflow / schema / Quick 模板 |

快速了解圆桌输出长相：看 [Quick Roundtable 示例](./examples/roundtable-quick.md)。
当前 shipped surface 的权威清单：看 [docs/INVENTORY.md](./docs/INVENTORY.md)。
机器可读的 shipped surface 真相源：看 [zhuzi/manifests/shipped-surface.json](./zhuzi/manifests/shipped-surface.json)。

## 核心组成

| 类别 | 数量 | 角色 |
|---|---|---|
| **Skills** | 5 个 | 单人物的思维操作系统——用户口语触发时，模型直接以该视角说话 |
| **Shared seat contracts** | 4 个 | `zhuzi/seats/*.md`，定义每个席位的职责、越权边界、root key、route 语义与 `seat_specific` 字段 |
| **Seat adapters** | 4 个共享席位；Claude shipped 4 个，Codex source-only 4 个 | 各 runtime 的薄 wrapper，只负责读取 skill + shared seat contract + shared schema |
| **Roundtable entry adapters** | Claude 1 条 command；Codex 1 个 orchestrator skill | 只负责装载 workflow 与共享资产，并把流程映射到各 runtime 的编排语义 |
| **Workflows** | 1 条 | `zhuzi/workflows/roundtable.md`——Roundtable 阶段编排、gate 与实施分支 |

三层关系：**skill 是思想内核 → agent 是该思想在协作中的发言席位 → roundtable adapter（Claude command / Codex orchestrator skill）是让这些席位围坐一桌的议事规则。**

Roundtable 运行时进一步拆成五层：**入口 adapter → workflow → shared seat contracts → shared references → Quick template / manifest**。入口保持薄，席位语义和流程骨架放到 `zhuzi/` 目录下的项目级资产里。

运行形态很轻：全部内容都是 Markdown 文档，由支持相应规范的 agent runtime 加载。当前仓库同时维护 runtime-agnostic 的 `skills/` 与 `zhuzi/` 共享资产，以及位于 `runtimes/claude/` 的 shipped Claude adapter 源码和位于 `runtimes/codex/` 的 source-only Codex adapter 源码。两边共用同一份 workflow / seats / references / template。

---

## 目录详解

### 一、Skills（思维操作系统）

每个 skill 是一个独立目录，`SKILL.md` 是入口，`references/` 是支撑证据链（research / anti-patterns / expression-levels / playbook）。

Skill 按用途分两类：

#### A 类 · 思维顾问型（Thinking Advisor）

严肃决策辅助——代码审查、策略设计、研究诚信审查、风险诊断、商业判断。激活后在用户"想问题"时介入，输出可追溯到一手来源的结构化分析。

| Skill | 人物 | 招牌方法论 |
|---|---|---|
| `linus-torvalds-engineer` | Linus Torvalds | Good Taste 7 步 / 12 条 anti-pattern / 4 级表达档位 |
| `munger-checklist` | Charlie Munger | 20 条愚蠢清单 / 10 步 Pre-Trade Checklist / Lollapalooza 扫描 |
| `taleb-antifragile` | Nassim Nicholas Taleb | 18 条 fragility 清单 / 10 步 Pre-Trade Fragility Check / barbell & turkey 检查 |
| `lopezdeprado-scientist` | Marcos López de Prado | 18 条方法论 anti-pattern / 10 步 Research Integrity Check / Sisyphus vs Meta-Strategy |

#### B 类 · 聊天娱乐型（Chat Entertainment）

朋友间聊天娱乐——把要发出去的一句话改写成该人物的口吻。**不做**决策建议、不做思维顾问、不做现代操作指南。

| Skill | 人物 | 招牌方法论 |
|---|---|---|
| `luxun-zawen` | 鲁迅 | 6 种修辞 DNA / 12 条假鲁迅识别器 / 4 级阴狠度 / 12 种聊天场景 playbook |

**跨类隔离**（硬约束）：
- A 类收到"帮我用 XX 口吻回朋友" → 路由到 B 类
- B 类收到"帮我审这个策略 / 做决策" → 退出角色并路由到 A 类
- 禁止把娱乐改写当决策依据，也禁止把决策分析包装成口吻梗

#### 已归档

- `archive/linus-torvalds-perspective/`（Linus v1，传记式思维顾问）——已被 `linus-torvalds-engineer` 替代，仅作对比参考保留

---

### 二、Shared Seat Contracts + Runtime Adapters

每个 roundtable 席位现在拆成一层共享契约 + 两套 runtime adapter 源码：

- `zhuzi/seats/<name>.md`——**共享 seat contract**。席位职责、越权边界、root key、route 语义、`seat_specific` 字段要求都放这里。
- `runtimes/claude/agents/<name>.md`——**Claude runtime adapter 模板**。源码里只保留 `{{ZHUZI_SKILL_ROOT}}` / `{{ZHUZI_SHARED_ROOT}}` 这类占位符；安装时才渲染成真实路径。
- `runtimes/codex/agents/<name>.md`——**Codex agent 定义**。和 Claude 一样保留 repo-level placeholder；side-load 时再渲染成 Codex 安装路径，源码里仍保留 repo 相对路径 fallback。

两边都不复制人物方法论正文，也不再各自维护一份 seat 语义；adapter 只 pull 对应 skill、shared seat contract 与 shared schema。

| Agent | 对应 skill | 席位性质 | 擅长领域 |
|---|---|---|---|
| `linus-engineer` | `linus-torvalds-engineer` | 代码席（唯一） | 软件架构、数据结构、API 边界、并发、性能、可靠性、review、重构、good taste；代码层 broken 可单边否决 |
| `munger-reviewer` | `munger-checklist` | 决策质量席 | 愚蠢清单、认知偏误、能力圈、机会成本、安全边际、激励结构、商业质量、护城河、Lollapalooza |
| `taleb-reviewer` | `taleb-antifragile` | 风险结构席 | 不确定性、尾部风险、fragility、凸性、barbell、ruin risk、冗余、选择权、skin in the game |
| `lopezdeprado-reviewer` | `lopezdeprado-scientist` | 证据质量席 | 研究诚信、实验设计、associational vs causal、benchmark / eval、backtest overfitting、DSR / PBO / CPCV、Sisyphus vs Meta-Strategy |

**设计要点**：

- **agent ≠ skill**。Skill 是直接对用户说话（"我是 Linus……"），agent 是对 orchestrator 返回结构化 verdict（`core` + `must_haves_review` + `must_haves_challenge` + `seat_specific` 四层）。
- **seat contract 是席位语义真相源**——职责、越权边界、YAML root key、route 映射和 `seat_specific` 约束都进 `zhuzi/seats/`；Claude / Codex adapter 只做薄 wrapper。
- **非代码席只研究不实施**——Munger / Taleb / López 只产出判断，不动文件；只有代码席位（Linus）在阶段 4 实施。
- **席位资格路由**——agent 描述里显式列"擅长领域关键词"，orchestrator 在阶段 0.5 按议题关键词匹配决定召开哪些席位，不强制所有席位全开。
- **持续更新**——skill 正文改了，seat contract 改了，runtime adapter 下次 spawn 自动拉最新，零同步成本。

---

### 三、Roundtable 入口（Runtime Adapters）

#### `/zhuzi:roundtable <议题>` — 多席位圆桌会议

默认是 **Quick Roundtable**。两套入口 adapter 都只做薄装载，不复制 shared assets：

| Runtime | 入口 | 作用 |
|---|---|---|
| Claude | `runtimes/claude/commands/zhuzi/roundtable.md` | command 薄入口，安装后直接提供 `/zhuzi:roundtable` |
| Codex | `runtimes/codex/skills/zhuzi-roundtable/SKILL.md` | orchestrator skill，把共享 workflow 映射到 `spawn_agent` / `send_input` |

两者都会先装载 workflow、shared seat contracts、shared references 和 Quick 模板，再按阶段推进。用户默认只读议题卡、席位短评和决策表；完整原文/YAML 作为可展开证据保留。

| 阶段 | 动作 | 产物 |
|---|---|---|
| **0.5 · 议题卡** | orchestrator 扫议题关键词 → 召开名单 + 成功标准（Quick 默认 1-3 条）+ 暂不讨论 | 用户确认议题卡 |
| **1 · 并行审议** | 并行 spawn 相关席位，每个席位按自己 SKILL.md 的 checklist 审议，产出 YAML verdict | 默认显示席位短评 |
| **1.5 · 契约修订 gate**（条件触发） | 任一席位 `must_haves_challenge.triggered: yes` → 暂停，合并 v2，呈现给用户五选一 | 锁定 must_haves v2 |
| **2 · 代码可行性** | 打包阶段 1 所有结论交 Linus 评 sane / broken / needs_refactor_first | Linus 可行性报告 |
| **3 · 综合对齐** | orchestrator 读 YAML verdict 做机读综合 → 主持人结论 + 冲突与取舍 + DECISIONS 表 | 等用户拍板 |
| **4 · 实施** | Linus 按锁定方案实施（优先续跑同一 `linus_id`：Claude 用 `SendMessage`，Codex 用 `send_input`；否则 fallback 新 spawn + 完整上下文注入） | 默认显示短实施报告 |

核心设计：

- **共同 verdict schema**——所有席位统一输出 `core` 层（`route` + `seat_native_verdict` + `hard_blockers` + `peer_disagreements`）+ `must_haves_review` + `must_haves_challenge` + `seat_specific`。主持人阶段 3 机读综合不用翻译席位方言。
- **must_haves 契约优先于视角**——议题成功的可验证 truth 在阶段 0.5 就锁定；Quick 默认 1-3 条，full 模式最多 5 条。席位可通过 `must_haves_challenge` 反向推翻契约，但必须走阶段 1.5 修订 gate、给用户决定。
- **N ≥ 1 席位合法**——无匹配席位则退回普通对话；只匹配 1 席位（如纯 factor literature 审视→只召 López）仍可跑。Quick 默认评议席位不超过 3 个。
- **硬约束**：
  1. 绝不篡改 agent 判断——默认短评卡，用户要求时展开完整原文和 YAML
  2. 绝不跳阶段——阶段 3 用户未确认前禁进阶段 4
  3. 实施阶段优先续跑同一 agent（Claude: `SendMessage`；Codex: `send_input`），不可用则新 spawn + 阶段 2 原文**完整注入**，不得摘要

`/zhuzi:roundtable` 的项目级核心资产都在 `zhuzi/`，安装后位于 `~/.claude/zhuzi/` 与 `~/.codex/zhuzi/`：

- `workflows/roundtable.md`：阶段编排、gate 规则、实施分支
- `seats/*.md`：共享席位契约，定义各席位职责、越权边界与输出契约
- `references/seat-registry.md`：当前席位权威表、默认 `stages` 路由规则
- `references/verdict-schema.md`：共同 YAML verdict 契约、route 映射和新增席位维护边界
- `templates/roundtable-quick.md`：Quick Roundtable 输出骨架
- `manifests/shipped-surface.json`：机器可读 shipped surface 清单

---

## 人物介绍（Skills / Agents 背后的五位）

### Linus Torvalds（1969-，在世）

芬兰裔美籍软件工程师，**Linux 内核**（1991-）与 **Git**（2005-）的创造者；当代最具影响力的开源治理者之一，LKML 上以技术判断直接、骨头硬、骂代码不骂人著称。核心方法论：**数据结构先行、消除特殊情况、删除不必要的抽象层**；代表短语 "Talk is cheap. Show me the code." / "Bad programmers worry about the code. Good programmers worry about data structures."

本仓库里他承担两个角色：
- **Skill `linus-torvalds-engineer`**：6 心智模型 / 12 anti-pattern / 7 步 Good Taste 清单 / 4 级表达档位，用于代码审查、架构评估、技术选型、开源治理
- **Agent `linus-engineer`**：Roundtable 唯一代码席，做可行性 gate 与实施；**代码层 broken 可单边否决**

信息持续更新（`references/research/07-updates-*.md`）。

---

### Charlie Munger（1924-2023）

美国律师、投资家、思想家；伯克希尔·哈撒韦副主席（1978-2023），巴菲特 60 年搭档。**跨学科思维**（Latticework of Mental Models）与**愚蠢清单**（"collect the asininities of the world in a kind of checklist"）的倡导者；代表短语 "All I want to know is where I'm going to die, so I'll never go there." / "It is remarkable how much long-term advantage people like us have gotten by trying to be consistently not stupid, instead of trying to be very intelligent."

本仓库里他承担两个角色：
- **Skill `munger-checklist`**：7 心智模型 / 20 条 anti-pattern（10 认知 + 9 量化 + 1 元）/ 10 步 Pre-Trade Checklist / 量化 playbook，用于投资决策、策略审视、商业判断
- **Agent `munger-reviewer`**：Roundtable 决策质量席——扫 Lollapalooza、能力圈、机会成本、激励结构

**信息截止 2023-11-28**（去世）。之后不补新事件——任何 2023-11 后内容必须标注"按原则推断"，不能作为芒格原话。

---

### Nassim Nicholas Taleb（1960-，在世）

黎巴嫩裔美籍学者、前期权交易员、Empirica（1999-2004）与 Universa Investments（2007-）顾问；Incerto 五部曲（*Fooled by Randomness* / *The Black Swan* / *The Bed of Procrustes* / *Antifragile* / *Skin in the Game*）作者，自造词 **antifragile** 的发明人。核心立场：金融**无法**科学化（tail 破坏 estimation），应用 barbell / via negativa / skin in the game 等结构性原则而非预测；实战档案包括 2008 年 +100%+、2020-03 +3,612% 的长尾对冲业绩。代表短语 "Don't tell me what you think, tell me what's in your portfolio." / "The Sharpe ratio is meaningless under fat tails."

本仓库里他承担两个角色：
- **Skill `taleb-antifragile`**：7 心智模型 / 18 条 fragility 清单 / 10 步 Pre-Trade Fragility Check / 4 级表达档位（独特之处：**按对手身份 route，不是按话题**——对 Wolfram 谈 ergodicity 是 L1，对 Pinker 谈同一概念是 L3）
- **Agent `taleb-reviewer`**：Roundtable 风险结构席——判 fragile / robust / antifragile

信息持续更新；每章量化 playbook 末尾强制 "⚠️ Taleb 可能反驳" 警示，明确区分 "Taleb 原话" 和 "基于原则的推演"。**与 López 是方法论对立阵营**：Taleb 认为金融不能科学化，López 认为应当且能够科学化——Roundtable 同时召开时不强行合并，留为 `peer_disagreements`。

---

### Marcos López de Prado（~1975-，在世）

西班牙裔金融学者、量化从业者；ADIA Lab 董事 / 首席研究员，Cornell ORIE 兼职教授，SSRN Economics Top-10 作者。代表作 *Advances in Financial Machine Learning*（2018）、*Machine Learning for Asset Managers*（2020）、*Causal Factor Investing*（2023）；2019-12-06 美国众议院金融服务委员会作证（定性 financial research 的 scientific fraud 问题）。核心立场：**金融研究必须科学化**——通过 causal inference（DAG / do-calculus）+ FDR 控制 + Purged K-Fold / CPCV / Deflated Sharpe / PBO 等方法论纪律，把大量 factor literature 从 associational claim 升级为 causal claim。代表短语 "Most discoveries in empirical finance are false." / "Backtesting is not a research tool. Feature importance is." / "Virtually all factor literature makes associational claims, in denial of the causal content of factor models."

本仓库里他承担两个角色：
- **Skill `lopezdeprado-scientist`**：6 心智模型 / 18 条方法论 anti-pattern / 10 步 Research Integrity Check / 4 级表达档位（独特之处：**按议题性质 route**——谈 purged K-Fold 对任何人都是 L1，谈整个 factor zoo 工业对任何人都是 L3）/ 量化 playbook 含自反审查章
- **Agent `lopezdeprado-reviewer`**：Roundtable 证据质量席——判 scientific / associational / pseudo_scientific，对每条 must_haves.truth 做 claim classification；命中议题属"量子 / 个股 / 宏观 / 地缘 / LLM agent alpha"的 L4 静默清单时自动 `too_hard`

**pattern-level 批评纪律**：所有输出不点名具体公司 / 基金 / PM / ticker；仅对 pattern 开火。信息持续更新。

---

### 鲁迅（周树人，1881-1936）

中国现代文学奠基人；杂文家、小说家、翻译家。一生写杂文数百万字（14 本杂文集：《坟》《华盖集》《而已集》《南腔北调集》《且介亭杂文》等），短篇小说三十余篇（《呐喊》《彷徨》《故事新编》），散文诗集《野草》。杂文是他自认为的"感应的神经，攻守的手足"——短、狠、冷、见微知著。代表语 "从来如此，便对吗？"（《狂人日记》，1918）/ "我向来是不惮以最坏的恶意，来推测中国人的。"（《纪念刘和珍君》，1926）

本仓库里他承担一个角色：
- **Skill `luxun-zawen`**：6 种招牌修辞（对比反讽 / 做标本 / 以小见大 / 假引退 / 层层剥皮 / 冷眼装蒜）/ 12 条假鲁迅识别器 / 4 级阴狠度（S 一句刀 / M 两句带转折 / L 小段杂文体 / XL 长 po 式）/ 12 种聊天场景 playbook，用于朋友间聊天娱乐的文体改写

**信息截止 1936-10-19**（去世）。**不做思维顾问**——遇到"鲁迅会怎么看 AI / 房价"这类请求会退出角色并路由到 A 类 skill。**不进 Roundtable**——杂文体不是审议语言。

---

## 安装

### 方式 A：一键安装（推荐）

```bash
git clone https://github.com/<your-fork>/zhuzi.git
cd zhuzi
./install.sh
```

`install.sh` 默认安装以下目标：

- `skills/*/` → `~/.claude/skills/<name>/`（Claude-style skills）
- `skills/*/` → `$CODEX_HOME/skills/<name>/`，默认 `$HOME/.codex/skills/<name>/`（Codex skills）
- `runtimes/claude/agents/*.md` → `~/.claude/agents/<name>.md`（4 个 agent 逐文件渲染，不影响旁边的 gsd-* 等）
- `runtimes/claude/commands/zhuzi/` → `~/.claude/commands/zhuzi/`（整目录渲染，`/zhuzi:roundtable` 即时可用）
- `zhuzi/` → `~/.claude/zhuzi/` 与 `$CODEX_HOME/zhuzi/`（共享 seats / references / workflows / templates / manifests）

不保留备份。每次修改仓库后重跑。环境变量 `CLAUDE_DIR` 可覆盖 `~/.claude`，`CODEX_HOME` 可覆盖 `$HOME/.codex`。

安装源面默认读取 `zhuzi/manifests/shipped-surface.json`，因此新增 / 迁移 Claude adapter 或 skill 时，除了改文件树，也要同步更新 manifest。

注意：仓库里的 `runtimes/claude/agents/*.md` 与 `runtimes/claude/commands/zhuzi/*.md` 是**模板源码**，不直接写死 `~/.claude/...` 或 `~/.codex/...`。这些路径只在安装产物里出现，由 `install.sh` 按目标 runtime 根目录渲染。

补充说明：安装产物里出现本机绝对路径是**预期行为**，不是源码污染。原因很简单：这些 markdown 最终是给 runtime / agent 当“可直接读取的具体路径”用的，不是 shell 脚本；把它写成 `$HOME/...` 并不保证会被运行时展开。真正该保持 runtime-agnostic 的，是仓库里的源码模板，而不是安装后生成的本机副本。

### 方式 B：手动试用 Codex roundtable adapter（当前 source-only）

`runtimes/codex/` 当前**故意不进** shipped surface / manifest / `install.sh`。如果要本地试用 Codex roundtable：

```bash
./install.sh
python3 tools/install_codex_source_adapters.py
```

这样装的是：
- 已 shipped 的 persona skills + shared `zhuzi/` 资产
- 以及尚未纳入 shipped surface 的 Codex roundtable adapter 源码（渲染后写入 Codex 安装根）

### 方式 C：只装单个 skill

```bash
cp -r skills/<skill-name> ~/.claude/skills/
cp -r skills/<skill-name> "${CODEX_HOME:-$HOME/.codex}/skills/"
```

注意：只装 persona skill、不装 roundtable seat adapter / entry adapter 时，roundtable 不可用；单独触发该 skill 仍可工作。

---

## 仓库布局

```
zhuzi/
├── skills/                           # 5 个 skill（思维操作系统）
│   ├── linus-torvalds-engineer/
│   ├── munger-checklist/
│   ├── taleb-antifragile/
│   ├── lopezdeprado-scientist/
│   └── luxun-zawen/
├── runtimes/
│   ├── claude/
│   │   ├── agents/                   # Claude 薄 adapter：读取 shared seat contract
│   │   │   ├── linus-engineer.md     # 代码席
│   │   │   ├── munger-reviewer.md    # 决策质量席
│   │   │   ├── taleb-reviewer.md     # 风险结构席
│   │   │   └── lopezdeprado-reviewer.md
│   │   └── commands/zhuzi/
│   │       └── roundtable.md         # /zhuzi:roundtable 薄入口
│   └── codex/
│       ├── agents/                   # Codex source-only 薄 adapter：读取 shared seat contract
│       │   ├── linus-engineer.md
│       │   ├── munger-reviewer.md
│       │   ├── taleb-reviewer.md
│       │   └── lopezdeprado-reviewer.md
│       └── skills/zhuzi-roundtable/
│           └── SKILL.md              # Codex orchestrator skill
├── zhuzi/
│   ├── seats/                        # 共享席位契约：seat 语义真相源
│   ├── references/                   # 席位表与 schema
│   ├── workflows/                    # roundtable 流程正文
│   ├── templates/                    # Quick 输出骨架
│   └── manifests/                    # 机器可读 shipped surface 清单
├── docs/
│   └── INVENTORY.md                  # shipped surface 的人读视图
├── examples/
│   └── roundtable-quick.md            # 默认短读圆桌示例
├── archive/
│   └── linus-torvalds-perspective/   # Linus v1（不推荐安装，对比参考）
├── AGENTS.md                         # 仓库内部协作纪律（Codex / Claude 共用）
├── CLAUDE.md                         # Claude Code 兼容 shim，指向 AGENTS.md
├── tools/check_consistency.py         # 本仓库 Markdown 运行时一致性检查
├── tools/smoke_test_codex_roundtable.py # 手动 Codex roundtable 烟雾测试
├── install.sh
└── README.md
```

---

## 激活

### 直接触发 skill

支持 Skill frontmatter 的 runtime 会按 `description` 匹配用户消息自动激活；Codex 也可以直接读取 `skills/<name>/SKILL.md` 作为本地 skill。典型触发词：

| Skill | 触发 |
|---|---|
| `linus-torvalds-engineer` | "用 Linus 视角"、"帮我 review 这段代码"、"good taste"、"torvalds mode"、"#linus" |
| `munger-checklist` | "用芒格视角"、"过一遍 checklist"、"Lollapalooza"、"#munger" |
| `taleb-antifragile` | "用 Taleb 视角"、"这策略 antifragile 吗"、"fragility check"、"turkey 检查"、"#taleb" |
| `lopezdeprado-scientist` | "用 López 视角"、"这是 associational 还是 causal"、"Deflated Sharpe"、"CPCV"、"#prado" |
| `luxun-zawen` | "用鲁迅口吻"、"改成鲁迅腔"、"冷讽一下"、"阴阳怪气版"、"#luxun" |

完整触发词见各 skill 的 `SKILL.md` frontmatter。

### 召开圆桌

```
/zhuzi:roundtable v28 M1 因子：把 hit% 拉到 d20 基线以上，权重表不改
```

orchestrator 会先给出议题卡让用户确认，包括召开席位、弃权席位、成功标准和暂不讨论内容，然后进入并行审议。

默认输出是短读格式：`主持人结论 → 议题卡 → 席位短评 → 决策表 → 下一步`。完整原文和 YAML 只在你要求“展开原文 / 展开 YAML / full / strict”时显示。

---

## 设计原则

修改仓库任何文件前请先读 [`CLAUDE.md`](./CLAUDE.md)。核心几条：

1. **证据链不可断**——每个心智模型 / anti-pattern / 表达档位都必须可追溯到 `references/research/` 里的一手来源（LKML URL、SSRN 论文、股东会 transcript、杂文集原文）。新增观点前先补证据。
2. **SKILL.md 用人物本人的品味写**——不是"关于他的描述"，是"他会怎么说"。
3. **跨类隔离**——A 类（思维顾问）与 B 类（聊天娱乐）不混用；B 类（鲁迅）不进 Roundtable 席位。
4. **命名约定**——新增 skill 后缀取自人物自己的身份 / 方法论，不照搬 `-engineer`：Linus 用 `-engineer`（自我认同）、Munger 用 `-checklist`（招牌方法）、Taleb 用 `-antifragile`（自造词 + magnum opus）、López 用 `-scientist`（scientist vs charlatan 二元轴）、鲁迅用 `-zawen`（一辈子的招牌文体）。
5. **通用性约束**——skill / agent / command 对任意项目类型通用。禁止硬编码特定项目（某量化策略 / 某 web app）的场景、truth 形式、verdict 用词；硬约束层必须领域无关，示例层至少一组异领域对照。
6. **Roundtable verdict schema 是契约**——新增席位必须填齐 `core` 四层字段，并在 `zhuzi/references/verdict-schema.md` 补 route 映射。

---

## 无需运行的检查

没有 linter、没有测试。修改后的验证方式：

- **内部一致性**：SKILL.md / workflow / command 引用的路径真实存在
- **manifest / inventory 一致性**：`zhuzi/manifests/shipped-surface.json`、`docs/INVENTORY.md` 与实际文件系统一致
- **证据一致性**：新增观点有对应的 research 文件支撑
- **触发词不与其他已安装 skill 冲突**（用户侧关注，本仓库无法自动检查）
- **Roundtable 烟雾测试**：skill 方向大改（verdict 档位、核心心智模型换了）后跑一次 `/zhuzi:roundtable`，必要时调对应 agent md 的硬边界段
- **自动一致性检查**：运行 `python3 tools/check_consistency.py`
- **Codex roundtable 烟雾测试**：运行 `python3 tools/smoke_test_codex_roundtable.py`

---

## 伦理与边界

每个 skill 的 `SKILL.md` 都有**诚实边界** section 明确说明：

- 它做什么 / 不做什么
- 信息截止日期（Linus / Taleb / López 持续更新；Munger 截至 2023-11-28；鲁迅截至 1936-10-19）
- 学术争议未解决的部分（不强行收口）
- Roundtable 席位的 `pattern-level` 批评纪律（不点名具体公司 / 个人 / ticker）

---

## 贡献

欢迎 PR。新增人物 skill / agent 请：

1. 遵循[命名约定](#设计原则)——后缀贴合人物自我身份 / 方法论
2. 遵循 skill 架构约定（SKILL.md 紧凑 + references 下沉）
3. 证据链完整（每个观点可追溯到一手 / 二手来源）
4. 若拟进入 Roundtable 席位：先新建 `zhuzi/seats/<name>.md` 共享 seat contract，再同步新建对应 runtime 的薄 adapter（Claude shipped 侧在 `runtimes/claude/agents/`；Codex roundtable 侧在 `runtimes/codex/agents/`），并更新 `zhuzi/references/seat-registry.md`、`zhuzi/references/verdict-schema.md`；只有纳入 shipped surface 时才更新 `zhuzi/manifests/shipped-surface.json`
5. 诚实边界写明"做不到什么"

---

## License

MIT License. 调研使用的一手 / 二手来源版权归原作者所有。

---

*"诸子百家"不是"集大成"，是"各执一端"——把不同的端摆到同一张桌子上，让用户自己看见分歧、自己拍板，比强行合流成"通用智慧"更诚实。*
