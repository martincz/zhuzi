# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库性质

这是一个 **Claude Code Skill 集合**——没有构建系统、没有测试套件、没有运行时。全部内容都是 Markdown 文档，定义可被 Claude Code 加载的人物/工程视角 skill：

- `linus-torvalds-perspective/`（Linus v1）——传记式思维框架总结
- `linus-torvalds-engineer/`（Linus v2）——v1 的重写，把思维参考升级为"可执行指令集"
- `munger-engineer/`（Munger v2）——Charlie Munger 工程师级视角，对标 Linus v2 结构，专为量化策略设计 / 投资决策审视。基线参考 `/mnt/g/nuwa-skill/examples/munger-perspective`（v1，未收入本仓库）

所有 skill 共存、互为补充，由用户触发词决定激活哪一个（见各自 SKILL.md 的 frontmatter `description` 字段）。Linus skill 擅长代码 / 系统工程 / 开源治理决策，Munger skill 擅长金融 / 量化 / 商业判断——量化工程师场景可能同时激活两者。

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

**Munger 特有**：`references/quant-trading-playbook.md` 是 Linus skill 没有的量化专用模块——把心智模型映射到因子设计、回测审视、仓位决策、策略生命周期管理。

## 关键设计原则（修改任何 skill 前必须理解）

1. **v1 和 v2 不是迭代关系，是共存关系**——不要把 v2 的改动回灌 v1，也不要让 v1 过时废弃。对应的 `<skill>/references/upgrade-notes.md` 是两者差异的权威说明。
2. **证据链不可断**——每个心智模型、anti-pattern、表达档位都必须可追溯到 `references/research/` 里的一手来源（LKML URL、TED / 股东会 transcript、访谈原文）。新增观点前先补证据，不补就不加。
3. **SKILL.md 用人物本人的品味写**——Linus：消除特殊情况、数据结构先行、删除不必要的抽象层、用例子替代宣言；Munger：否定句替代肯定句、粗俗精准类比替代抽象原则、承认矛盾不强行收口。对应的 upgrade-notes.md 有明确示范。
4. **表达分级是核心特性**（engineer v2 独有）——Level 1/2/3/4 的词汇、触发条件、例句不能混淆。修改 `references/expression-levels.md` 时保留档位边界。Linus 的档位是"技术严肃性"，Munger 的档位是"判断严厉度"——不要把两者的档位逻辑混用。
5. **量化 playbook 的推演声明**（Munger 独有）——`quant-trading-playbook.md` 明确声明是"基于原则推演"而非 Munger 原话。修改时保留这个声明，不要让它漂移成"Munger 说过 XX"。
6. **中文为主，技术术语保留英文**（如 `bikeshedding`、`good taste`、`Lollapalooza`、`circle of competence`、`regression`）。引用人物原话用英文，不翻译。

## 常见修改场景

- **补 Linus 2026-04 之后的新素材**（新 LKML 事件、新访谈）→ 先进 `linus-torvalds-engineer/references/research/07-updates-2024-2026.md`，再决定是否升级到 SKILL.md 的心智模型或 anti-pattern 库。
- **Munger 信息截止 2023-11-28**（去世）→ 不补新事件；只能补**已有但调研没覆盖**的历史材料。任何 2023-11 后的内容应标注为"按原则推断"而非 Munger 原话。
- **调整触发词**→ 改 SKILL.md 顶部 frontmatter 的 `description` 字段；v1 和 v2 的触发词要保持分化（动作词偏 v2，认知词偏 v1，见对应 upgrade-notes.md 最后一节）。
- **新增 anti-pattern**→ 必须同时更新 SKILL.md 的表格和 `references/anti-patterns.md` 的详细条目，两处编号一致。Linus 是 12 条，Munger 是 20 条（10 认知 + 9 量化 + 1 元）。
- **量化 playbook 扩展**（Munger）→ 每次新增"XX 映射到量化"内容时必须检查心智模型 7 个的完整对应——不要漏掉某个模型也不要强行塞入无关映射。

## 无需运行的检查

没有 linter、没有测试。修改后的唯一验证方式是：

- 内部一致性——SKILL.md 引用的 `references/*.md` 路径真实存在
- 证据一致性——新增观点有对应的 research 文件支撑
- 触发词不与其他已安装 skill 冲突（用户侧关注，本仓库无法自动检查）
