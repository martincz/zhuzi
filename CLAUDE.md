# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库性质

这是一个 **Claude Code Skill 集合**——没有构建系统、没有测试套件、没有运行时。全部内容都是 Markdown 文档，定义可被 Claude Code 加载的人物/工程视角 skill：

- `linus-torvalds-perspective/`（Linus v1）——传记式思维框架总结
- `linus-torvalds-engineer/`（Linus v2）——v1 的重写，把思维参考升级为"可执行指令集"
- `munger-checklist/`（Munger v2）——Charlie Munger 的 checklist 式清单工具箱，对标 Linus v2 结构，专为量化策略设计 / 投资决策审视。命名取自芒格自己的方法论（"We collect the asininities of the world in a kind of checklist"）——芒格不是工程师，所以不用 `-engineer` 后缀。基线参考 `/mnt/g/nuwa-skill/examples/munger-perspective`（v1，未收入本仓库）
- `luxun-zawen/`（鲁迅杂文改写）——**不同于前两者的新类型：文体改写工具，不是思维顾问**。把日常聊天 / 吐槽 / 反击的一句话改写成鲁迅杂文体。命名取自鲁迅一辈子的招牌文体身份（杂文家），对标 Linus 的 `-engineer`、Munger 的 `-checklist`。6 种招牌修辞 DNA（对比反讽 / 做标本 / 以小见大 / 假引退 / 层层剥皮 / 冷眼装蒜）/ 12 条假鲁迅识别器 / 4 级阴狠度（S 一句刀 / M 两句带转折 / L 小段杂文体 / XL 长 po）/ 12 种聊天场景 playbook。**信息截止 1936-10-19**（鲁迅去世）。

所有 skill 共存、互为补充，由用户触发词决定激活哪一个（见各自 SKILL.md 的 frontmatter `description` 字段）。Linus skill 擅长代码 / 系统工程 / 开源治理决策，Munger skill 擅长金融 / 量化 / 商业判断——量化工程师场景可能同时激活两者。Luxun skill 是**独立的文体改写工具**，和前两者场景不重叠——前两者是"帮你想问题"，luxun 是"帮你改写要发出去的话"。

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

**Luxun 特有**（文体改写类型——架构上对标但语义不同）：
- 没有 `upgrade-notes.md`（没有对应的 v1）
- 没有思维顾问型的"心智模型"——替换为 `references/rhetoric-patterns.md`（6 种修辞 DNA 的详细模板）
- 没有决策路由型的 checklist——替换为 `references/scenario-playbook.md`（12 种聊天场景的套路）
- `references/expression-levels.md` 的档位含义不同：Linus 是"技术严肃性"、Munger 是"判断严厉度"、Luxun 是"**文本长度与修辞密度**"（S/M/L/XL 对应字数 10-25 / 30-60 / 80-150 / 200+）
- `references/research/` 只有 5 个维度文件（01 生平与杂文语境 / 02 修辞 DNA 形成 / 03 招牌手法证据链 / 04 词汇池 / 05 作品清单），比 Linus 的 7 个和 Munger 的 9 个少——因为文体改写不需要"近期动态"维度，鲁迅已于 1936 年去世
- **不做思维顾问任务**（如"鲁迅会怎么看 AI / 房价 / 某社会事件"）——遇到这类请求应退出角色并建议用户改用思维顾问型 skill

## 关键设计原则（修改任何 skill 前必须理解）

1. **v1 和 v2 不是迭代关系，是共存关系**——不要把 v2 的改动回灌 v1，也不要让 v1 过时废弃。对应的 `<skill>/references/upgrade-notes.md` 是两者差异的权威说明。
2. **证据链不可断**——每个心智模型、anti-pattern、表达档位都必须可追溯到 `references/research/` 里的一手来源（LKML URL、TED / 股东会 transcript、访谈原文）。新增观点前先补证据，不补就不加。
3. **SKILL.md 用人物本人的品味写**——Linus：消除特殊情况、数据结构先行、删除不必要的抽象层、用例子替代宣言；Munger：否定句替代肯定句、粗俗精准类比替代抽象原则、承认矛盾不强行收口。对应的 upgrade-notes.md 有明确示范。
4. **表达分级是核心特性**（engineer v2 独有）——Level 1/2/3/4 的词汇、触发条件、例句不能混淆。修改 `references/expression-levels.md` 时保留档位边界。Linus 的档位是"技术严肃性"，Munger 的档位是"判断严厉度"——不要把两者的档位逻辑混用。
5. **量化 playbook 的推演声明**（Munger 独有）——`quant-trading-playbook.md` 明确声明是"基于原则推演"而非 Munger 原话。修改时保留这个声明，不要让它漂移成"Munger 说过 XX"。
6. **中文为主，技术术语保留英文**（如 `bikeshedding`、`good taste`、`Lollapalooza`、`circle of competence`、`regression`）。引用人物原话用英文，不翻译。
7. **文体改写型 skill（Luxun）的特殊规则**——不是思维顾问而是改写工具。不能用它生成"人物观点 / 判断 / 推演"，只能做文本风格转换。每次改写必须能归类到已定义的修辞 DNA（Luxun 是 6 种）——无法归类的改写说明破功。引用人物原话时必须查证出处（Luxun 的所有"鲁迅说过"引用都标注到作品与年份）——误引（把网络梗"我没有说过" / 蜘蛛侠"能力越大责任越大" 当鲁迅原话）是核心 anti-pattern（见 `luxun-zawen/references/anti-patterns.md` 症状 4）。

## 常见修改场景

- **补 Linus 2026-04 之后的新素材**（新 LKML 事件、新访谈）→ 先进 `linus-torvalds-engineer/references/research/07-updates-2024-2026.md`，再决定是否升级到 SKILL.md 的心智模型或 anti-pattern 库。
- **Munger 信息截止 2023-11-28**（去世）→ 不补新事件；只能补**已有但调研没覆盖**的历史材料。任何 2023-11 后的内容应标注为"按原则推断"而非 Munger 原话。
- **调整触发词**→ 改 SKILL.md 顶部 frontmatter 的 `description` 字段；v1 和 v2 的触发词要保持分化（动作词偏 v2，认知词偏 v1，见对应 upgrade-notes.md 最后一节）。
- **新增 anti-pattern**→ 必须同时更新 SKILL.md 的表格和 `references/anti-patterns.md` 的详细条目，两处编号一致。Linus 是 12 条，Munger 是 20 条（10 认知 + 9 量化 + 1 元）。
- **量化 playbook 扩展**（Munger）→ 每次新增"XX 映射到量化"内容时必须检查心智模型 7 个的完整对应——不要漏掉某个模型也不要强行塞入无关映射。
- **补 Luxun 鲁迅未覆盖的聊天场景**（如新的约定场景 / 新的朋友互动模式）→ 加到 `luxun-zawen/references/scenario-playbook.md`，不要改 SKILL.md 主表（主表只列入 12 个核心场景）。如果新场景需要引入新的修辞 DNA（超出 6 种），则必须同时更新：(1) SKILL.md 的修辞索引表、(2) `rhetoric-patterns.md` 详细条目、(3) `research/03-signature-devices.md` 的原文证据链（**至少 5 条精确出处引用**）——三处同步且编号一致。
- **补 Luxun 原文引用**（新发现的鲁迅原话可供 skill 引用）→ 进 `research/04-vocabulary-pool.md` 的"可引用原话"表，**必须精确到作品名 + 年份**。禁止引用无法查证的网络流传句。鲁迅信息**截止 1936-10-19**——不补后续二手评价。
- **命名约定的元原则**：新增人物 skill 时，**后缀要贴合该人物自己的身份 / 方法论**——不要照搬 `-engineer` 当通用后缀。已落地案例：Linus 用 `-engineer`（自我认同），Munger 用 `-checklist`（招牌方法），Luxun 用 `-zawen` / 杂文（一辈子的招牌文体身份）。建议后缀：费曼可能用 `-teacher` 或 `-explainer`，巴菲特可能用 `-letter`（股东信体）。错误样例：把所有新 skill 都叫 `-engineer` 会制造身份错认。

## 无需运行的检查

没有 linter、没有测试。修改后的唯一验证方式是：

- 内部一致性——SKILL.md 引用的 `references/*.md` 路径真实存在
- 证据一致性——新增观点有对应的 research 文件支撑
- 触发词不与其他已安装 skill 冲突（用户侧关注，本仓库无法自动检查）
