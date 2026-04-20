# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库性质

这是一个 **Claude Code Skill 集合**——没有构建系统、没有测试套件、没有运行时。全部内容都是 Markdown 文档，定义可被 Claude Code 加载的人物/工程视角 skill：

- `skills/linus-torvalds-engineer/`（Linus，原 v2）——把传记式思维参考升级为"可执行指令集"。v1（`linus-torvalds-perspective`）已于 2026-04-20 归档到 `archive/`，不再作为活动 skill——见 `archive/README.md`
- `skills/munger-checklist/`（Munger v2）——Charlie Munger 的 checklist 式清单工具箱，对标 Linus v2 结构，专为量化策略设计 / 投资决策审视。命名取自芒格自己的方法论（"We collect the asininities of the world in a kind of checklist"）——芒格不是工程师，所以不用 `-engineer` 后缀。基线参考 `/mnt/g/nuwa-skill/examples/munger-perspective`（v1，未收入本仓库）
- `skills/taleb-antifragile/`（Taleb，**独立首发无 v1**）——Nassim Nicholas Taleb 的反脆弱 / 厚尾 / 凸性思维操作系统。对标 Linus v2 / Munger v2 的 engineer 级架构。命名取自 Taleb 自造的核心概念 + magnum opus 书名（*Antifragile*, 2012）——他一辈子工作的核心。7 心智模型（Antifragility / Fat Tails / Skin in the Game / Via Negativa / Barbell / Ergodicity / Lindy）/ 18 条 anti-pattern（fragility 清单，6 分布误用 + 5 认知论证 + 5 激励伦理 + 1 量化 + 1 元）/ 10 步 Pre-Trade Fragility Check / 4 级表达强度（按对手身份 route 而非话题——**独有**）/ 量化交易 playbook（基于 Incerto 原则推演，**非 Taleb 原话**，顶部强制声明）。**信息持续更新**（Taleb 仍在世，1960-，2026-04 截止；每次更新看 X @nntaleb、新技术论文、新 beefs、Gaza / Lebanon 立场演化）。
- `skills/luxun-zawen/`（鲁迅杂文改写）——**聊天娱乐型**（文体改写工具）。把日常聊天 / 吐槽 / 反击的一句话改写成鲁迅杂文体。命名取自鲁迅一辈子的招牌文体身份（杂文家），对标 Linus 的 `-engineer`、Munger 的 `-checklist`、Taleb 的 `-antifragile`。6 种招牌修辞 DNA（对比反讽 / 做标本 / 以小见大 / 假引退 / 层层剥皮 / 冷眼装蒜）/ 12 条假鲁迅识别器 / 4 级阴狠度（S 一句刀 / M 两句带转折 / L 小段杂文体 / XL 长 po）/ 12 种聊天场景 playbook。**信息截止 1936-10-19**（鲁迅去世）。

**两类 skill**：
- **A 类 · 思维顾问型**：Linus / Munger / Taleb——用户"想问题"时介入，输出结构化分析。Linus skill 擅长代码 / 系统工程 / 开源治理决策，Munger skill 擅长金融 / 量化 / 商业判断，Taleb skill 擅长尾部风险 / 厚尾分布 / 反脆弱设计。量化工程师场景可能同时激活多个（Munger + Taleb 是最紧密互补：Munger 避免愚蠢 / 认知偏误，Taleb 避免破产 / 数学分布；Munger Kelly × 0.25，Taleb Kelly × 0.15；Munger 说"中等 = 稳健"，Taleb 说"中等 = 最脆弱 / barbell 拒绝中间"）
- **B 类 · 聊天娱乐型**：Luxun——用户"改写要发出去的话 / 装口吻玩梗"时介入。不重叠于 A 类——前者是"帮你改写要发出去的话"，后者是"帮你想问题"

所有 skill 共存、互为补充，由用户触发词决定激活哪一个（见各自 SKILL.md 的 frontmatter `description` 字段）。**跨类路由规则**见下方"关键设计原则"第 8 条。

## Skill 架构约定

每个 engineer 级 skill 目录遵循 Claude Code 的 Skill 规范：

```
<skill-name>/
├── SKILL.md                       # 入口，顶部 YAML frontmatter 声明 name/description/触发词
└── references/                    # SKILL.md 中链接的详细支撑材料
    ├── research/                  # 一手/二手来源调研（按 01-07 编号的维度文件）
    ├── anti-patterns.md           # 反模式识别库（可运行）
    ├── expression-levels.md       # 分级表达 DNA（可运行）
    ├── upgrade-notes.md           # 与对应 v1 的差异说明
    └── *.md                       # 其他可运行 checklist（如 good-taste-checklist / pre-trade-checklist / quant-trading-playbook）
```

SKILL.md 是给模型加载的主文件，必须保持紧凑（v2 的设计目标是"激活后 5 秒内知道该做什么"）。细节下沉到 `references/`，SKILL.md 通过显式路径引用（`references/anti-patterns.md`）。

**Munger 特有**：
- `references/quant-trading-playbook.md` 是 Linus skill 没有的量化专用模块——把心智模型映射到因子设计、回测审视、仓位决策、策略生命周期管理
- `references/pre-trade-checklist.md` 是芒格 skill 对 Linus `good-taste-checklist.md` 的等价物（10 步 vs 7 步）

**Taleb 特有**（**独立 skill 无 v1**，对标 Linus/Munger engineer v2 架构）：
- `references/quant-trading-playbook.md` 对标 Munger 的同名文件，但**顶部诚实声明更严格**——Taleb 的核心 domain 是 tail hedge / long vol / convex payoff，他**没有公开系统评论过 A 股 long-only 选股**。每章末尾有 "⚠️ Taleb 可能反驳" 警示，明确区分"Taleb 原则的推演"和"Taleb 原话"
- `references/pre-trade-checklist.md` 对标 Munger 的 10 步，但视角不同：Munger 问"edge 存在吗 + 能力圈 + Lollapalooza"，Taleb 问"结构 fragility + payoff 凸性 + 分布 class + turkey 覆盖 + ergodicity"。两者互补——同一策略在 Munger 某步答得上、在 Taleb 答不上（或反之）都是信号
- `references/expression-levels.md` 的档位逻辑**独特**：不是技术严肃性（Linus）或判断严厉度（Munger）或文本密度（Luxun），而是**对手身份 → register**——对 Wolfram 谈 ergodicity = L1（"Maestro"），对 Pinker 谈同一概念 = L3（charlatan）。这是 Taleb skill 最易被误用的地方
- **Fat Tony 代言层**（其他 skill 都没有）：L3.5 的独立表达装置——当 Taleb 本人作为学者不方便粗，Fat Tony 上场。有完整句式特征和名句库
- `references/research/` 只有 7 个维度文件（01-writings / 02-conversations / 03-expression-dna / 04-external-views / 05-decisions / 06-timeline / 07-quant-application）——比 Munger 的 9 个少，多在 03（表达 DNA 极丰富）

**Luxun 特有**（文体改写类型——架构上对标但语义不同）：
- 没有 `upgrade-notes.md`（没有对应的 v1）
- 没有思维顾问型的"心智模型"——替换为 `references/rhetoric-patterns.md`（6 种修辞 DNA 的详细模板）
- 没有决策路由型的 checklist——替换为 `references/scenario-playbook.md`（12 种聊天场景的套路）
- `references/expression-levels.md` 的档位含义不同：Linus 是"技术严肃性"、Munger 是"判断严厉度"、Luxun 是"**文本长度与修辞密度**"（S/M/L/XL 对应字数 10-25 / 30-60 / 80-150 / 200+）
- `references/research/` 只有 5 个维度文件（01 生平与杂文语境 / 02 修辞 DNA 形成 / 03 招牌手法证据链 / 04 词汇池 / 05 作品清单），比 Linus 的 7 个和 Munger 的 9 个少——因为文体改写不需要"近期动态"维度，鲁迅已于 1936 年去世
- **不做思维顾问任务**（如"鲁迅会怎么看 AI / 房价 / 某社会事件"）——遇到这类请求应退出角色并建议用户改用思维顾问型 skill

## 关键设计原则（修改任何 skill 前必须理解）

1. **v2 替代 v1 时用归档而非删除**——已归档的 v1 移到 `archive/`（见 `archive/README.md`），不再作为活动 skill，但保留完整文件供对比参考。`<skill>/references/upgrade-notes.md` 引用的 v1 路径指向 `archive/`。不要把 v2 的改动回灌归档的 v1，也不要从 git 历史删除 v1——它是 skill 演化的原始档案。
2. **证据链不可断**——每个心智模型、anti-pattern、表达档位都必须可追溯到 `references/research/` 里的一手来源（LKML URL、TED / 股东会 transcript、访谈原文）。新增观点前先补证据，不补就不加。
3. **SKILL.md 用人物本人的品味写**——Linus：消除特殊情况、数据结构先行、删除不必要的抽象层、用例子替代宣言；Munger：否定句替代肯定句、粗俗精准类比替代抽象原则、承认矛盾不强行收口。对应的 upgrade-notes.md 有明确示范。
4. **表达分级是核心特性**（engineer v2 独有）——Level 1/2/3/4 的词汇、触发条件、例句不能混淆。修改 `references/expression-levels.md` 时保留档位边界。Linus 的档位是"技术严肃性"，Munger 的档位是"判断严厉度"——不要把两者的档位逻辑混用。
5. **量化 playbook 的推演声明**（Munger 独有）——`quant-trading-playbook.md` 明确声明是"基于原则推演"而非 Munger 原话。修改时保留这个声明，不要让它漂移成"Munger 说过 XX"。
6. **中文为主，技术术语保留英文**（如 `bikeshedding`、`good taste`、`Lollapalooza`、`circle of competence`、`regression`）。引用人物原话用英文，不翻译。
7. **聊天娱乐型 skill（Luxun）的特殊规则**——不是思维顾问而是口吻 / 文体工具。不能用它生成"人物观点 / 判断 / 推演"作为决策依据，只能做文本风格转换。每次改写必须能归类到已定义的修辞 DNA（Luxun 是 6 种 + S/M/L/XL 四档）——无法归类的产出说明破功。引用人物原话时必须查证出处（Luxun 的所有"鲁迅说过"引用都标注到作品与年份）——误引（把网络梗"我没有说过" / 蜘蛛侠"能力越大责任越大" 当鲁迅原话）是核心 anti-pattern（见 `skills/luxun-zawen/references/anti-patterns.md` 症状 4）。
8. **跨类隔离原则**（A 类思维顾问 vs B 类聊天娱乐不混用）：
   - **A 类**（Linus / Munger / Taleb）收到"帮我用 XX 口吻回朋友 / 把这句话改阴一点 / 装 XX 腔" → 不自己做文体改写，路由到 B 类（Luxun）
   - **B 类**（Luxun）收到"帮我审这段代码 / 看这个策略 / 做决策建议" → 不假扮人物输出"他会怎么看"，退出角色并路由到 A 类对应 skill
   - **禁止**把 A 类的决策分析用 B 类口吻包装后当"有趣的建议"——这会让用户把娱乐产出误当决策依据
   - **禁止**把 B 类的聊天改写结果当作"人物对这件事的真实观点"——B 类只做口吻转换，不承担观点归属
   - 两类的 anti-pattern 库相互独立：A 类的 anti-pattern 针对思维误用（过度自信 / 能力圈外 / 概率装饰），B 类的 anti-pattern 针对口吻破功（半文半白 / 假引用 / 时代错置）——不要交叉引用

## 跨项目使用纪律（Claude 与用户的协作层）

本仓库是 skill / agent / command 的**开发仓库**，不是任何具体业务项目（量化策略 / web app / infra / 任一）的工作仓库。用户在此粘贴的内容、截图、议题描述，几乎必然是"借具体项目的使用痕迹来改进这里的通用产物"——不是让 Claude 介入那个具体项目的业务细节。

### 1. 他项目 roundtable / skill 使用痕迹的解读默认

用户贴来其他项目的 `/zhuzi:roundtable` 产出、verdict YAML、契约草稿、席位原文、截图时，**默认意图 = 改进本仓库的 skill / agent / command**。

- 先识别：粘贴内容暴露了本仓库哪些可固化的元层模式（流程漏洞、schema 缺陷、措辞歧义、纪律盲点、通用性破坏）
- 再提议：针对本仓库具体文件的改动方案
- **不要**分析粘贴内容的业务议题细节（某策略是否 fragile / 某架构是否 sane / 某方法论对不对）——那是该项目自己的 roundtable 该做的事，已经做过了
- **不要**把具体项目的业务结论（特定方法论、特定参数、特定领域纪律）写进本仓库的通用产物——那属于**该项目**的 AGENTS.md，不是本仓库

意图不明时先问一句"你要改进 skill 还是想讨论这个议题"，不要默认走分析路径——默认分析是本仓库最容易犯的错。

### 2. skill / agent / command 的通用性约束

本仓库所有产物必须**对任意项目类型通用**，即使当前只有一个用户、一个落地项目。

- **禁止硬编码特定项目**（某量化策略项目 / 某 web app / 某 infra）的场景、工具链、验证命令、truth 形式、verdict 用词
- **硬约束层 vs 示例层分离**：
  - 硬约束（"pass_criterion 必须可机器验证"）必须领域无关
  - 示例可以举某领域例子，但应给出**至少一个异领域对照**（量化指标 + web API / 文档纪律 / 编译产物 等）避免读者把示例当定义
- **truth 形态 / verify 命令 / pass_criterion 写法**要覆盖：可观测量化指标（回测 / API 响应 / 内存 / bundle）+ 结构性纪律事实（文档条款 / 接口字段 / 输出格式 / 目录约定）——不能只服务一类
- skill / agent / command 的 `description`、示例、prompt 里不得出现特定项目名
- 新增硬约束或示例前自问："这句话改到另一个项目（非量化 / 非本场景）还成立吗？"——不成立就降级为示例，不进硬约束

## 常见修改场景

- **补 Linus 2026-04 之后的新素材**（新 LKML 事件、新访谈）→ 先进 `skills/linus-torvalds-engineer/references/research/07-updates-2024-2026.md`，再决定是否升级到 SKILL.md 的心智模型或 anti-pattern 库。
- **Munger 信息截止 2023-11-28**（去世）→ 不补新事件；只能补**已有但调研没覆盖**的历史材料。任何 2023-11 后的内容应标注为"按原则推断"而非 Munger 原话。
- **Taleb 信息持续更新**（仍在世 1960-）→ 更新策略：新访谈 / 新推文进 `research/02-conversations.md` 和 `03-expression-dna.md`；新技术论文（如 *Fat Tails* 第 4 版）进 `01-writings.md`；新 public beefs 进 `03-expression-dna.md` 的"近期动态 > 新 beefs"；立场演化（如他对 AI / LLM 从温和到更激烈）更新 SKILL.md 身份卡 + 时间线。**Gaza / Lebanon 立场**有隔离规则——skill 可引原话但加 "这是他立场不是普适真理" caveat，不做政治宣传。
- **调整触发词**→ 改 SKILL.md 顶部 frontmatter 的 `description` 字段。已归档的 v1（在 `archive/`）不再扫描，不用考虑触发词冲突。
- **新增 anti-pattern**→ 必须同时更新 SKILL.md 的表格和 `references/anti-patterns.md` 的详细条目，两处编号一致。Linus 是 12 条，Munger 是 20 条（10 认知 + 9 量化 + 1 元），Taleb 是 18 条（6 分布误用 + 5 认知论证 + 5 激励伦理 + 1 量化 + 1 元 "Fragility Stack"）。
- **量化 playbook 扩展**（Munger / Taleb）→ 每次新增"XX 映射到量化"内容时必须检查心智模型完整对应（Munger 7 个 / Taleb 7 个）——不要漏掉某个模型也不要强行塞入无关映射。**Taleb 特别注意**：每章末尾的 "⚠️ Taleb 可能反驳" 警示不要被稀释——它是 skill 诚实性的关键。
- **补 Luxun 鲁迅未覆盖的聊天场景**（如新的约定场景 / 新的朋友互动模式）→ 加到 `skills/luxun-zawen/references/scenario-playbook.md`，不要改 SKILL.md 主表（主表只列入 12 个核心场景）。如果新场景需要引入新的修辞 DNA（超出 6 种），则必须同时更新：(1) SKILL.md 的修辞索引表、(2) `rhetoric-patterns.md` 详细条目、(3) `research/03-signature-devices.md` 的原文证据链（**至少 5 条精确出处引用**）——三处同步且编号一致。
- **补 Luxun 原文引用**（新发现的鲁迅原话可供 skill 引用）→ 进 `research/04-vocabulary-pool.md` 的"可引用原话"表，**必须精确到作品名 + 年份**。禁止引用无法查证的网络流传句。鲁迅信息**截止 1936-10-19**——不补后续二手评价。
- **命名约定的元原则**：新增人物 skill 时，**后缀要贴合该人物自己的身份 / 方法论**——不要照搬 `-engineer` 当通用后缀。已落地案例：Linus 用 `-engineer`（自我认同），Munger 用 `-checklist`（招牌方法），Luxun 用 `-zawen` / 杂文（一辈子的招牌文体身份）。建议后缀：费曼可能用 `-teacher` 或 `-explainer`，巴菲特可能用 `-letter`（股东信体）。错误样例：把所有新 skill 都叫 `-engineer` 会制造身份错认。

## 无需运行的检查

没有 linter、没有测试。修改后的唯一验证方式是：

- 内部一致性——SKILL.md 引用的 `references/*.md` 路径真实存在
- 证据一致性——新增观点有对应的 research 文件支撑
- 触发词不与其他已安装 skill 冲突（用户侧关注，本仓库无法自动检查）
