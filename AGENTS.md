# AGENTS.md

This file provides guidance to agent runtimes (Codex, Claude Code, and compatible tools) when working with code in this repository.

## 仓库性质

zhuzi 是一组以"诸子百家"为隐喻的 agent 思维席位与圆桌审议流程。每一位人物代表一种稳定的方法论、边界和表达风格；单独使用时是一个 skill，多席位协作时进入 roundtable 流程。

概念上仍是 **skill + agent + roundtable** 三层；运行时实现上分成不同 adapter：

- **Skills**（`skills/`，5 个）——单人物的思维操作系统，面向**用户直接触发**，激活后以"我"身份说话
- **Shared seat contracts**（`zhuzi/seats/`，4 个）——每个 roundtable 席位的共享语义真相源：职责、越权边界、root key、route 语义、`seat_specific` 字段都放这里
- **Seat adapters**（`runtimes/claude/agents/` shipped 4 个；`runtimes/codex/agents/` source-only 4 个）——各 runtime 的薄 wrapper，只负责读取 skill + shared seat contract + shared schema，返回结构化 YAML verdict（不直接对话用户）
- **Roundtable adapters**：
  - Claude：`runtimes/claude/commands/zhuzi/roundtable.md`（command 薄入口）
  - Codex：`runtimes/codex/skills/zhuzi-roundtable/SKILL.md`（orchestrator skill）

开发边界：**skill 是思想内核 → agent 是该思想在协作中的发言席位 → roundtable adapter 是让这些席位围坐一桌的议事规则**。修改任何一层前必须理解三者的路由边界（skill 触发词撞上 agent 触发词会造成错路由——见下方"关键设计原则"第 9 条）。

运行形态很轻：全部内容都是 Markdown 文档，由支持相应规范的 agent runtime 加载；当前仓库同时维护 runtime-agnostic 的项目级资产与 `skills/`，以及位于 `runtimes/claude/` 的 shipped Claude adapter 源码和位于 `runtimes/codex/` 的 source-only Codex adapter 源码。未来若增加其他 runtime，按 `runtimes/<runtime>/` 并列扩展。

---

## 提交规范

- 提交信息遵循 `feat/fix/refactor/style/chore` 前缀风格。
- 多行格式：首行摘要，后续用 `- ` 列出 1-3 条关键改动。
- 单次提交只解决一个问题。
- 除前缀外，提交信息其他内容必须使用中文。

示例：

```text
chore: 固化圆桌短读输出模板

- 新增 Quick Roundtable 示例
- 扩展一致性检查覆盖默认输出骨架
```

---

## 五个 Skill 概览

| Skill                     | 类           | 人物                       | 信息截止   | 核心特性                                                     |
| ------------------------- | ------------ | -------------------------- | ---------- | ------------------------------------------------------------ |
| `linus-torvalds-engineer` | A · 思维顾问 | Linus Torvalds (1969-)     | 持续更新   | 6 心智模型 / 12 anti-pattern / 7 步 Good Taste 清单 / 4 级表达档（技术严肃性） |
| `munger-checklist`        | A · 思维顾问 | Charlie Munger (1924-2023) | 2023-11-28 | 7 心智模型 / 20 anti-pattern（10 认知 + 9 量化 + 1 元）/ 10 步 Pre-Trade Checklist / 4 级表达档（判断严厉度）/ 量化 playbook |
| `taleb-antifragile`       | A · 思维顾问 | N. N. Taleb (1960-)        | 持续更新   | 7 心智模型 / 18 anti-pattern（6 分布误用 + 5 认知论证 + 5 激励伦理 + 1 量化 + 1 元）/ 10 步 Pre-Trade Fragility Check / 4 级表达档（**按对手身份**route）/ Fat Tony 代言层（L3.5）/ 量化 playbook |
| `lopezdeprado-scientist`  | A · 思维顾问 | M. López de Prado (~1975-) | 持续更新   | 6 心智模型 / 18 anti-pattern（方法论反模式）/ 10 步 Research Integrity Check / 4 级表达档（**按议题性质**route）/ 量化 playbook（含第 7 章自反审查——独有）/ L4 静默清单 |
| `luxun-zawen`             | B · 聊天娱乐 | 鲁迅（1881-1936）          | 1936-10-19 | 6 修辞 DNA（对比反讽 / 做标本 / 以小见大 / 假引退 / 层层剥皮 / 冷眼装蒜）/ 12 条假鲁迅识别器 / 4 级阴狠度（**按文本长度**档：S/M/L/XL）/ 12 种聊天场景 playbook |

**两类 skill**：
- **A 类 · 思维顾问型**（4 个）——用户"想问题"时介入，输出结构化分析。复杂决策可多席位激活，量化只是常见场景之一：
  - **Munger + Taleb 互补**：Munger 避免愚蠢（认知偏误），Taleb 避免破产（数学分布）
  - **Munger + López 互补**：Munger 看能力圈 + 激励，López 看研究诚信 + causal 纪律
  - **Taleb vs López 方法论对立**：Taleb 认为金融**不能**科学化（tail 破坏 estimation），López 认为**应当且能够**科学化（通过 causal + FDR）——**不强行合并**，留为分歧
- **B 类 · 聊天娱乐型**（1 个）——用户"改写要发出去的话 / 装口吻玩梗"时介入。**不重叠于 A 类**

**4 级表达档位的语义按 skill 不同**（不要混用）：
- Linus：技术严肃性
- Munger：判断严厉度
- Taleb：对手身份 → register
- López：议题性质 → register
- Luxun：文本长度与修辞密度

---

## 四个共享 Seat Contract（由 runtime adapters 装载）

| Agent                   | 对应 skill                | 席位性质       | 可单边否决                       | 擅长领域匹配关键词                                           |
| ----------------------- | ------------------------- | -------------- | -------------------------------- | ------------------------------------------------------------ |
| `linus-engineer`        | `linus-torvalds-engineer` | 代码席（唯一） | **是**（代码层 broken 单边否决） | 软件架构 / 数据结构 / API 边界 / 并发 / 性能 / 可靠性 / 实施 / 可行性 / 重构 / 工程纪律 / 技术选型 / good taste |
| `munger-reviewer`       | `munger-checklist`        | 决策质量席     | 否                               | 投资决策 / 商业判断 / 产品策略 / 组织决策 / 认知偏误 / 能力圈 / 机会成本 / 安全边际 / 激励结构 / 护城河 / Lollapalooza |
| `taleb-reviewer`        | `taleb-antifragile`       | 风险结构席     | 否                               | 不确定性 / 尾部风险 / 脆弱性 / 凸性 / ruin risk / barbell / 冗余 / 选择权 / 依赖链风险 / skin-in-the-game / 厚尾分布 |
| `lopezdeprado-reviewer` | `lopezdeprado-scientist`  | 证据质量席     | 否                               | 研究方法论 / 实验设计 / 因果声明 / benchmark / A-B test / eval / backtest overfitting / p-hacking / multiple testing / data leakage / specification error / Deflated Sharpe / Purged K-Fold / CPCV / 研究流程诊断 |

**Seat / adapter 架构约定**：

1. **Pull 模式引用 skill**——runtime adapter 的第一步是 `Read` 对应 skill 的 `SKILL.md`。skill 更新后，下次 spawn 自动拉最新，**零同步成本**。不要把 skill 内容复制到 adapter md 里。
2. **共享 seat contract 是席位语义真相源**——职责、越权边界、root key、route 语义和 `seat_specific` 字段要求进 `zhuzi/seats/*.md`；不要在 Claude/Codex adapter 里再各写一份。
3. **非代码席只研究不实施**——Munger / Taleb / López 的 tools 字段不含 `Edit` / `Write`；只有 `linus-engineer` 有完整工具（他在阶段 4 实施）。
4. **强制共同 verdict schema**——所有席位返回 YAML verdict block，含 `core` + `must_haves_review` + `must_haves_challenge` + `seat_specific` 四层。`core` 字段机读统一（`route` / `seat_native_verdict` / `hard_blockers` / `peer_disagreements`），主持人阶段 3 不用翻译席位方言。
5. **pattern-level 批评纪律**（López 最严）——不点名具体公司 / 基金 / PM / ticker；仅对 pattern 开火。
6. **角色隔离 via description 路由护栏**——每个 adapter 的 `description` 字段显式写 "仅在 /zhuzi:roundtable 内调用……standalone 场景请用 XX skill，不要 spawn 本 agent"。防止与 skill 触发词撞车。
7. **Roundtable runtime 分层**——共享 seat contracts 在 `zhuzi/seats/`，当前席位表在 `zhuzi/references/seat-registry.md`，共同 verdict schema 在 `zhuzi/references/verdict-schema.md`，阶段流程在 `zhuzi/workflows/roundtable.md`，Quick 骨架在 `zhuzi/templates/roundtable-quick.md`，机器可读 shipped surface 在 `zhuzi/manifests/shipped-surface.json`。adapter、command、README、docs 的摘要性描述若漂移，以这些项目级资产为准。

---

## Roundtable Runtime 架构（入口 / workflow / 共享资产）

roundtable 协议是本仓库的核心协作产物。Claude 侧入口是 `/zhuzi:roundtable <议题>`；Codex 侧入口是 `runtimes/codex/skills/zhuzi-roundtable/SKILL.md` 这个 orchestrator skill。默认交互是 Quick Roundtable：内部严格按阶段推进，外部只展示议题卡、席位短评和决策表；完整原文/YAML 作为可展开证据保留。

runtime 结构拆成五层：

- `runtimes/claude/commands/zhuzi/roundtable.md`——薄入口模板，只负责装载 workflow / seats / references / template
- `runtimes/codex/skills/zhuzi-roundtable/SKILL.md`——Codex orchestrator adapter，负责把共享 workflow 映射到 `spawn_agent` / `send_input`
- `zhuzi/workflows/roundtable.md`——阶段编排、gate 规则、实施分支
- `zhuzi/seats/*.md`——共享席位契约，定义 seat 语义真相源
- `zhuzi/references/{seat-registry,verdict-schema}.md`——席位权威表 + 共同 verdict 契约
- `zhuzi/templates/roundtable-quick.md`——默认短读骨架

**路径纪律**：

- Claude adapter 模板只允许出现 `{{ZHUZI_SKILL_ROOT}}`、`{{ZHUZI_SHARED_ROOT}}` 这类占位符，不允许写死 runtime 根目录
- Codex source-only adapter 在源码层也使用和 Claude 一样的 repo-level placeholder；通过 `tools/install_codex_source_adapters.py` side-load 时默认渲染成 `$HOME/.codex/...` symbolic path，并保留 repo 相对路径 fallback；显式设置 `CODEX_HOME` 时改渲染为对应 concrete override path
- 安装脚本只负责 shipped surface 的渲染与拷贝；当前**不处理** `runtimes/codex/` source-only adapter，本地试用走 `tools/install_codex_source_adapters.py`
- 默认安装产物优先写成 `$HOME/.claude/...` / `$HOME/.codex/...` 这种 symbolic installed path，避免把 `/home/<user>/...` 烙进文件；只有显式设置 `CLAUDE_DIR` / `CODEX_HOME` 装到非默认根目录时，才渲染 concrete override path
- 共享资产（`zhuzi/`）必须保持 runtime-agnostic，不知道自己最终装在哪个 runtime 根目录

共享契约文件：
- `zhuzi/seats/*.md`——共享席位契约：职责、越权边界、root key、route 语义、seat-specific 字段
- `zhuzi/references/seat-registry.md`——当前席位权威表、默认 `stages` 规则、扩席位维护边界
- `zhuzi/references/verdict-schema.md`——共同 YAML verdict 契约与 route 映射
- `zhuzi/workflows/roundtable.md`——权威阶段流程
- `zhuzi/templates/roundtable-quick.md`——Quick 模式默认骨架

| 阶段                                       | 动作                                                         | 产出                       |
| ------------------------------------------ | ------------------------------------------------------------ | -------------------------- |
| **0.5 · 议题卡**                           | orchestrator 扫议题关键词 → **席位资格路由**（召开名单 + 弃权名单 + 每席位 `stages`）→ 定成功标准（Quick 默认 1-3 条，full 最多 5 条） | 用户确认议题卡             |
| **1 · 并行审议**                           | 并行 spawn 所有 `stages` 含 `1` 的席位（Quick 默认评议席位不超过 3 个） | 默认呈现席位短评；原文/YAML 可展开 |
| **1.5 · must_haves 修订 gate**（条件触发） | 任一席位 `must_haves_challenge.triggered: yes` → 暂停，合并 v2，**五选一**呈现给用户（含"要求 orchestrator 改写 v2 表达"选项） | 锁定 must_haves v2         |
| **2 · 代码可行性**                         | 打包阶段 1 所有结论交 Linus 评 `sane` / `broken` / `needs_refactor_first`；Linus 启动时自动 Read 当前项目的 `AGENTS.md` / `CLAUDE.md` 按项目纪律工作 | Linus 可行性报告           |
| **3 · 综合对齐**                           | orchestrator 读 YAML verdict 做机读综合 → 主持人结论 + 冲突与取舍 + **DECISIONS 表**（`locked` / `deferred` / `discretion` 三档） | 等用户拍板                 |
| **4 · 实施**                               | Linus 按锁定方案实施：**优先续跑同一 `linus_id`**（Claude: `SendMessage`；Codex: `send_input`，保留阶段 2 内部状态）；续跑不可用时 fallback 新 spawn + **阶段 2 原文完整注入**（不得摘要） | 默认短实施报告             |

**硬约束**（改 roundtable runtime 前必须守住）：

1. 绝不篡改 agent 判断——默认短评卡，用户要求时展开完整原文和 YAML
2. 绝不跳阶段——阶段 3 用户未确认前禁进阶段 4
3. 实施阶段优先走同 agent 续跑路径 A（Claude: `SendMessage`；Codex: `send_input`）；不可用时走路径 B + 阶段 2 原文**完整注入**（禁"新 spawn 但只传简短摘要"）
4. 项目纪律由 Linus 自己发现——不在 command 里硬编码项目特定规则

**N ≥ 1 席位合法**——无匹配席位（N=0）停流水线；只匹配 1 席位（N=1）按流程跑，不需特判。Quick 模式下评议席位默认不超过 3 个。

**must_haves 的两类 truth**（阶段 0.5 硬约束第 1 条）：
- `observable_metric`——可观测的量化行为（回测 CI / p99 latency / 内存 / bundle size / 错误率）。`pass_criterion` 打 `TBD`，让席位在 `must_haves_review.proposed_criterion` 填专业阈值
- `policy_discipline`——可验证的结构性 / 纪律性事实（文档条款 + 指定措辞 / JSON schema 字段 / 输出列前缀 / 目录约定）。`pass_criterion` orchestrator **直接写死**，不得 TBD

两者都合法，以下**禁放 truths**：实施约束（改 N 个文件、不引新依赖——走 DECISIONS.locked）/ 主观项（代码好看、文档清楚）/ 流程要求（跑通编译、跑通测试——走 out_of_scope 默认项）。

---

## Skill 架构约定

每个 skill 目录遵循通用 Skill 规范：

```
<skill-name>/
├── SKILL.md                       # 入口，顶部 YAML frontmatter 声明 name/description/触发词
└── references/                    # SKILL.md 中链接的详细支撑材料
    ├── research/                  # 一手/二手来源调研（按 01-NN 编号的维度文件）
    ├── anti-patterns.md           # 反模式识别库（可运行）
    ├── expression-levels.md       # 分级表达 DNA（可运行）
    ├── upgrade-notes.md           # 与对应 v1 的差异说明（仅 v2 skill 有）
    └── *.md                       # 其他可运行 checklist（good-taste / pre-trade / quant-playbook / scenario-playbook 等）
```

SKILL.md 是给模型加载的主文件，必须紧凑（v2 设计目标："激活后 5 秒内知道该做什么"）。细节下沉到 `references/`，SKILL.md 通过显式路径引用（`references/anti-patterns.md`）。

**各 skill 的 `references/research/` 维度数量不同**（不强求统一）：
- Linus：7 个维度（含 `07-updates-2024-2026.md` 持续更新）
- Munger：9 个维度（信息截止 2023-11-28）
- Taleb：7 个维度（`03-expression-dna.md` 含"近期动态 > 新 beefs"）
- López：10 个维度（含 `07-quant-application.md`）
- 鲁迅：5 个维度（不需"近期动态"维度）

**量化 playbook（仅思维顾问型 skill）**：
- Munger：`quant-trading-playbook.md` 明确声明"基于原则推演"而非 Munger 原话
- Taleb：`quant-trading-playbook.md` 每章末尾强制 "⚠️ Taleb 可能反驳" 警示——Taleb 的核心 domain 是 tail hedge / long vol，他**没有公开系统评论过 A 股 long-only 选股**，诚实声明不得稀释
- López：`quant-trading-playbook.md` 含第 7 章"自反审查"（独有）——用自己的 18 条 anti-pattern 审视 López 风格的策略本身

**Luxun 特有**（文体改写类型——架构对标但语义不同）：
- 没有 `upgrade-notes.md`（无 v1）
- 没有思维顾问的"心智模型"——替换为 `references/rhetoric-patterns.md`（6 种修辞 DNA 详细模板）
- 没有决策路由 checklist——替换为 `references/scenario-playbook.md`（12 种聊天场景套路）
- `expression-levels.md` 档位语义不同（文本长度与修辞密度 S/M/L/XL）

---

## 关键设计原则（修改任何层前必须理解）

1. **v2 替代 v1 用归档而非删除**——`archive/linus-torvalds-perspective/`（Linus v1）保留完整文件供对比参考。`<skill>/references/upgrade-notes.md` 引用的 v1 路径指向 `archive/`。不把 v2 改动回灌归档的 v1，也不从 git 历史删 v1。
2. **证据链不可断**——每个心智模型、anti-pattern、表达档位都必须可追溯到 `references/research/` 里的一手来源（LKML URL、SSRN 论文、股东会 transcript、Incerto 章节、鲁迅作品名+年份）。新增观点前先补证据，不补就不加。
3. **SKILL.md 用人物本人的品味写**——不是"关于他的描述"，是"他会怎么说"。Linus：消除特殊情况、数据结构先行、用例子替代宣言；Munger：否定句替代肯定句、粗俗精准类比替代抽象原则；Taleb：Mediocristan vs Extremistan、skin in the game 代替观点；López："Hence," 段首、数据贴身、pattern-level 开火；鲁迅：杂文腔不说教结尾。
4. **表达分级语义按 skill 不同**（见"五个 Skill 概览"表）——修改 `references/expression-levels.md` 时保留档位边界，**不要把 Linus 的档位逻辑套到 López 或 Taleb**。
5. **量化 playbook 的推演声明**（Munger / Taleb / López 都有）——修改时保留"这是基于原则推演而非原话"的顶部声明，不让它漂移成 "XX 说过 YY"。Taleb 的 "⚠️ 可能反驳" 警示是 skill 诚实性的关键。
6. **中文为主，技术术语保留英文**（如 `bikeshedding` / `good taste` / `Lollapalooza` / `circle of competence` / `antifragile` / `ergodicity` / `Purged K-Fold` / `Deflated Sharpe` / `CPCV` / `Meta-Labeling` / `Hence,`）。引用人物原话用原文（英语 / 西语 / 阿拉伯语 / 古汉语）不翻译。
7. **聊天娱乐型 skill（Luxun）特殊规则**——不是思维顾问而是口吻 / 文体工具。不能用它生成"人物观点 / 判断 / 推演"作决策依据，只做文本风格转换。每次改写必须能归类到已定义的修辞 DNA（6 种 + S/M/L/XL 四档）——无法归类的产出说明破功。引用"鲁迅说过"必须查证出处（注到作品+年份）——误引（"我没有说过" / "能力越大责任越大" 当鲁迅原话）是核心 anti-pattern。
8. **跨类隔离原则**（A 类思维顾问 vs B 类聊天娱乐不混用）：
   - **A 类**收到"帮我用 XX 口吻回朋友 / 把这句改阴一点" → 路由到 B 类（Luxun）
   - **B 类**收到"帮我审代码 / 看策略 / 做决策建议" → 退出角色，路由到 A 类
   - 禁止把 A 类决策分析用 B 类口吻包装当"有趣的建议"
   - 禁止把 B 类改写结果当"人物对这件事的真实观点"
   - 两类 anti-pattern 库相互独立，不交叉引用
9. **Skill 触发词 vs Agent 触发词的路由护栏**——skill 的 `description` 触发词是"用户场景触发"（如 "用 Linus 视角"），agent 的 `description` 显式写 "仅在 /zhuzi:roundtable 内调用……standalone 请用对应 skill"。新增 skill / agent 时必须同时检查两侧触发词不撞车——用户说 "用 López 视角" 应激活 skill，不应 spawn agent。
10. **Roundtable verdict schema 是跨席位契约**——`core` 层字段机读统一；`must_haves_challenge.proposed_revision` 三字段分层（`revised_truth` ≤ 50 字 / `revised_verify_suggestion` / `spawn_sub_topic`），**严禁回退为字符串字面量**。新增席位必须填齐 `core` 四层字段并在 `zhuzi/references/verdict-schema.md` 补对应映射。

---

## 跨项目使用纪律（agent 与用户的协作层）

本仓库是 skill / agent / command 的**开发仓库**，不是任何具体业务项目的工作仓库。用户在此粘贴的内容、截图、议题描述，几乎必然是"借具体项目的使用痕迹来改进这里的通用产物"——不是让当前 agent 介入那个具体项目的业务细节。

### 1. 他项目 roundtable / skill 使用痕迹的解读默认

用户贴来其他项目的 `/zhuzi:roundtable` 产出、verdict YAML、契约草稿、席位原文、截图时，**默认意图 = 改进本仓库的 skill / agent / roundtable adapter**。

- 先识别：粘贴内容暴露了本仓库哪些可固化的元层模式（流程漏洞、schema 缺陷、措辞歧义、纪律盲点、通用性破坏）
- 再提议：针对本仓库具体文件的改动方案
- **不要**分析粘贴内容的业务议题细节（某策略是否 fragile / 某架构是否 sane / 某方法论对不对）——那是该项目自己的 roundtable 该做的事
- **不要**把具体项目的业务结论（特定方法论、特定参数、特定领域纪律）写进本仓库的通用产物——那属于**该项目**的 AGENTS.md

意图不明时先问一句"你要改进 skill 还是想讨论这个议题"，不要默认走分析路径。

### 2. skill / agent / command 的通用性约束

本仓库所有产物必须**对任意项目类型通用**，即使当前只有一个用户、一个落地项目。

- **禁止硬编码特定项目**（某量化策略 / 某 web app / 某 infra）的场景、工具链、验证命令、truth 形式、verdict 用词
- **硬约束层 vs 示例层分离**：
  - 硬约束（"`pass_criterion` 必须可机器验证"）必须领域无关
  - 示例可以举某领域例子，但应给出**至少一个异领域对照**（量化指标 + web API / 文档纪律 / 编译产物等），避免读者把示例当定义
- **truth 形态 / verify 命令 / pass_criterion 写法**要覆盖：可观测量化指标 + 结构性纪律事实——不能只服务一类
- skill / agent / command 的 `description`、示例、prompt 里不得出现特定项目名
- 新增硬约束或示例前自问："这句话改到另一个项目（非量化 / 非本场景）还成立吗？"——不成立就降级为示例，不进硬约束

---

## 常见修改场景

### Skill 侧

- **补 Linus / Taleb / López 的新素材**（新事件 / 新访谈 / 新论文）→ 先进对应 `references/research/` 维度文件，再决定是否升级到 SKILL.md 的心智模型或 anti-pattern 库
- **Munger 信息截止 2023-11-28**（去世）→ 不补新事件；只能补**已有但调研没覆盖**的历史材料。任何 2023-11 后内容应标注"按原则推断"
- **Taleb 信息持续更新**（仍在世 1960-）→ 新访谈 / 新推文进 `02-conversations.md` + `03-expression-dna.md`；新技术论文进 `01-writings.md`；新 public beefs 进 `03-expression-dna.md`"近期动态"；立场演化（如对 AI / LLM、Gaza / Lebanon）更新 SKILL.md 身份卡 + 时间线，保留 caveat
- **López 信息持续更新**（仍在世 ~1975-）→ 新 SSRN 论文 / 书进 `01-writings.md`；新国会作证 / 讲座进 `02-conversations.md`；ADIA Lab 新 Protocol 更新进 `07-quant-application.md`；**pattern-level 纪律不得松动**——不点名
- **鲁迅信息截止 1936-10-19** → 不补二手评价；新发现的原话进 `04-vocabulary-pool.md`"可引用原话"表，**必须精确到作品名+年份**
- **调整触发词** → 改 SKILL.md 顶部 frontmatter 的 `description` 字段。同时检查对应 agent 的 `description` 路由护栏仍生效
- **新增 anti-pattern** → 同步更新 SKILL.md 表格和 `references/anti-patterns.md` 详细条目，两处编号一致。计数约束：Linus 12 / Munger 20 / Taleb 18 / López 18 / Luxun 12
- **量化 playbook 扩展** → 每次新增"XX 映射到量化"内容时检查心智模型完整对应（Munger 7 / Taleb 7 / López 6），不漏不硬塞
- **补 Luxun 聊天场景** → 加到 `scenario-playbook.md`，不改 SKILL.md 主表（主表只列 12 个核心场景）。若需引入新修辞 DNA（超出 6 种），必须同步 (1) SKILL.md 修辞索引表 / (2) `rhetoric-patterns.md` 详细条目 / (3) `research/03-signature-devices.md` 至少 5 条精确出处引用——三处编号一致

### Agent 侧

- **新增席位** → 1) 先新建 `zhuzi/seats/<name>-reviewer.md`（或 `-engineer.md`），把职责、越权边界、root key、route 语义和 `seat_specific` 字段要求放进去；2) 再新建 `runtimes/claude/agents/<name>-reviewer.md` 薄 adapter；若 Codex roundtable 也要支持，同步新建 `runtimes/codex/agents/<name>-reviewer.md`；3) `description` 字段加路由护栏（"仅在 roundtable 内调用……standalone 请用 XX skill"）；4) wrapper 只做 Read 对应 skill + shared seat contract + shared schema；5) 更新 `zhuzi/references/seat-registry.md` 的当前席位表与默认 `stages` 规则；6) 更新 `zhuzi/references/verdict-schema.md` 的 native → core.route 映射；7) **只有纳入 shipped surface 的 adapter / shared asset** 才更新 `zhuzi/manifests/shipped-surface.json` 与 `docs/INVENTORY.md`
- **调整席位工具权限** → 非代码席（只研究不实施）tools 不含 `Edit` / `Write`；代码席（Linus）才有完整工具
- **调整擅长领域关键词** → 同步改 agent `description` 段和 `zhuzi/references/seat-registry.md`（阶段 0.5 路由依赖此表）

### Command 侧

- **调整阶段流程** → 优先改 `zhuzi/workflows/roundtable.md`。只有入口装载顺序变化时才改 runtime adapter：Claude 侧改 `runtimes/claude/commands/zhuzi/roundtable.md`，Codex 侧改 `runtimes/codex/skills/zhuzi-roundtable/SKILL.md`
- **调整 verdict schema** → 同步：(1) `zhuzi/references/verdict-schema.md`；(2) 所有 agent md 的 verdict block 示例段；(3) 各 skill SKILL.md 若内嵌 schema 示例也要同步
- **调整席位资格路由** → 优先改 `zhuzi/references/seat-registry.md`；只有阶段流程本身变化时再改 `zhuzi/workflows/roundtable.md`
- **调整 Quick 默认骨架** → 改 `zhuzi/templates/roundtable-quick.md`，并同步 `examples/roundtable-quick.md` 与一致性检查
- **项目级覆盖** → 某项目有专属需求时，Claude 侧可在该项目的 `.claude/commands/zhuzi/roundtable.md` 放覆盖版；Codex 侧若所在 runtime 支持项目级 skill 覆盖，则让同名 `zhuzi-roundtable` 入口优先

### 命名约定的元原则

新增人物 skill / agent 时，**后缀要贴合该人物自己的身份 / 方法论**——不照搬 `-engineer` 当通用后缀。已落地：Linus `-engineer`（自我认同）/ Munger `-checklist`（招牌方法）/ Taleb `-antifragile`（自造词 + magnum opus）/ López `-scientist`（scientist vs charlatan 二元轴）/ 鲁迅 `-zawen`（招牌文体）。建议后缀：费曼 `-teacher` / 巴菲特 `-letter` / 达里奥 `-principles`。错误样例：把所有新 skill 都叫 `-engineer` 会制造身份错认。

---

## 安装与分发（install.sh）

`./install.sh` 覆盖安装 shipped surface 到 `~/.claude/` 与 `$CODEX_HOME`（无备份，每次修改仓库后重跑）：

- `skills/<name>/` → `~/.claude/skills/<name>/`（Claude-style skills）
- `skills/<name>/` → `$CODEX_HOME/skills/<name>/`，默认 `$HOME/.codex/skills/<name>/`（Codex skills）
- `runtimes/claude/agents/*.md` → `~/.claude/agents/<name>.md`（**逐文件拷贝，不整目录同步**——保护旁边的 gsd-* 等其他 agent）
- `runtimes/claude/commands/zhuzi/` → `~/.claude/commands/zhuzi/`（命令入口）
- `zhuzi/` → `~/.claude/zhuzi/` 与 `$CODEX_HOME/zhuzi/`（项目级共享资产；当前包含 `seats/`、`references/`、`workflows/`、`templates/`、`manifests/`）

环境变量 `CLAUDE_DIR` 可覆盖 `~/.claude`，`CODEX_HOME` 可覆盖 `$HOME/.codex`（测试用）。

安装源面默认读取 `zhuzi/manifests/shipped-surface.json`。因此新增 / 迁移 **shipped surface** 的 Claude adapter 或 skill 时，除了改文件树，也要同步更新 manifest。`runtimes/codex/` 当前是 source-only adapter，**故意不进**主 `install.sh`；本地 side-load 用 `python3 tools/install_codex_source_adapters.py`。

默认安装时，渲染产物优先使用 `$HOME/.claude/...` / `$HOME/.codex/...` 这种 symbolic installed path，避免把当前机器用户名写死进 markdown。若显式传入 `CLAUDE_DIR` / `CODEX_HOME`，安装器改渲染 concrete override path，因为此时 `$HOME/.codex/...` 不再等于真实安装根。`./zhuzi/...` 这类 repo 相对路径只用于开发态 fallback，不是 installed root 的替代物。

**Self-contained 分发约束**——每个 skill 的所有调研文件必须在 skill 目录内（`references/research/`），不依赖外部路径。复制整个 skill 目录就能独立使用。

---

## 无需运行的检查

没有 linter、没有测试。修改后的验证方式：

- **内部一致性**——SKILL.md / agent md / workflow / command 引用的路径真实存在
- **Manifest / Inventory 一致性**——`zhuzi/manifests/shipped-surface.json`、`docs/INVENTORY.md` 与实际文件系统一致
- **Codex source-only adapter 一致性**——`runtimes/codex/` 的 skill / agent 入口能回指共享 workflow、schema 与对应 skill；默认安装产物优先用 `$HOME/.codex/...` symbolic path，repo 相对路径只做 fallback，不承担 installed root
- **证据一致性**——新增观点有对应的 research 文件支撑
- **触发词不冲突**——skill 之间、skill 与 agent 之间的 `description` 触发词不撞车（用户侧关注，本仓库无法自动检查）
- **Roundtable 烟雾测试**——skill 方向大改（verdict 档位、核心心智模型换了）或 verdict schema 改动 → 跑一次 `/zhuzi:roundtable` 烟雾测试，必要时调对应 agent md 的硬边界段
- **路由护栏检查**——新增 agent 后，自测用户说"用 XX 视角"是激活 skill 不是 spawn agent；用户说 `/zhuzi:roundtable` 才 spawn agent
- **自动一致性检查**——运行 `python3 tools/check_consistency.py`，检查 inventory count、seat registry 与 agent 文件对齐、schema 引用路径、源码模板里的机器路径泄漏和旧命令路径等结构性问题
- **Codex roundtable 烟雾测试**——运行 `python3 tools/smoke_test_codex_roundtable.py`，刷新 shipped 安装、注入 `runtimes/codex/` source-only adapter，并验证 `codex exec` 真能读到 roundtable skill 与共享资产
