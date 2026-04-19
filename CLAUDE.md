# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库性质

这是一个 **Claude Code Skill 集合**——没有构建系统、没有测试套件、没有运行时。全部内容都是 Markdown 文档，定义两个可被 Claude Code 加载的 skill：

- `linus-torvalds-perspective/`（v1）——传记式思维框架总结
- `linus-torvalds-engineer/`（v2）——v1 的重写，目标是把思维参考升级为"可执行指令集"

两个 skill 共存、互为补充，由用户触发词决定激活哪一个（见各自 SKILL.md 的 frontmatter `description` 字段）。

## Skill 架构约定

每个 skill 目录遵循 Claude Code 的 Skill 规范：

```
<skill-name>/
├── SKILL.md                  # 入口，顶部 YAML frontmatter 声明 name/description/触发词
└── references/               # SKILL.md 中链接的详细支撑材料
    ├── research/             # 一手/二手来源调研（LKML 邮件、访谈、时间线等）
    └── *.md                  # 可运行 checklist（如 good-taste-checklist.md、anti-patterns.md）
```

SKILL.md 是给模型加载的主文件，必须保持紧凑（v2 的设计目标是"激活后 5 秒内知道该做什么"）。细节下沉到 `references/`，SKILL.md 通过显式路径引用（`references/anti-patterns.md`）。

## 关键设计原则（修改任何 skill 前必须理解）

1. **v1 和 v2 不是迭代关系，是共存关系**——不要把 v2 的改动回灌 v1，也不要让 v1 过时废弃。`linus-torvalds-engineer/references/upgrade-notes.md` 是两者差异的权威说明。
2. **证据链不可断**——每个心智模型、anti-pattern、表达档位都必须可追溯到 `references/research/` 里的一手来源（LKML URL、TED transcript、访谈原文）。新增观点前先补证据，不补就不加。
3. **SKILL.md 用 Linus 自己的品味写**——消除特殊情况、数据结构先行、删除不必要的抽象层、用例子替代宣言。v2 的 upgrade-notes.md 有明确示范。
4. **表达分级是核心特性**（v2 独有）——Level 1/2/3/4 的词汇、触发条件、例句不能混淆。修改 `references/expression-levels.md` 时保留档位边界。
5. **中文为主，技术术语保留英文**（如 `bikeshedding`、`good taste`、`regression`）。引用 Linus 原话用英文，不翻译。

## 常见修改场景

- **补 2026-04 之后的新素材**（新 LKML 事件、新访谈）→ 先进 `linus-torvalds-engineer/references/research/07-updates-2024-2026.md`，再决定是否升级到 SKILL.md 的心智模型或 anti-pattern 库。
- **调整触发词**→ 改 SKILL.md 顶部 frontmatter 的 `description` 字段；v1 和 v2 的触发词要保持分化（动作词偏 v2，认知词偏 v1，见 upgrade-notes.md 最后一节）。
- **新增 anti-pattern**→ 必须同时更新 SKILL.md 的 12 条表格和 `references/anti-patterns.md` 的详细条目，两处编号一致。

## 无需运行的检查

没有 linter、没有测试。修改后的唯一验证方式是：

- 内部一致性——SKILL.md 引用的 `references/*.md` 路径真实存在
- 证据一致性——新增观点有对应的 research 文件支撑
- 触发词不与其他已安装 skill 冲突（用户侧关注，本仓库无法自动检查）
