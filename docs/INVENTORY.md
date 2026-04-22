# zhuzi Shipped Surface Inventory

> 这是 `zhuzi` 当前 shipped surface 的人读视图。机器可读真相源在 `zhuzi/manifests/shipped-surface.json`；若 README、AGENTS、agent 示例段与文件系统出现漂移，以 manifest、本文件和仓库树交叉校验结果为准。
>
> 注意：`runtimes/codex/` 当前是 source-only adapter 源码，尚未接入 shipped surface / manifest / install，因此**故意不计入**本清单。

## Skills (5 shipped)

| Entry | Path | Role |
|---|---|---|
| `linus-torvalds-engineer` | `skills/linus-torvalds-engineer/SKILL.md` | 代码、架构、good taste 思维顾问 |
| `munger-checklist` | `skills/munger-checklist/SKILL.md` | 决策质量、偏误、激励结构思维顾问 |
| `taleb-antifragile` | `skills/taleb-antifragile/SKILL.md` | fragility、tail risk、antifragile 思维顾问 |
| `lopezdeprado-scientist` | `skills/lopezdeprado-scientist/SKILL.md` | 研究诚信、causal claim、实验纪律思维顾问 |
| `luxun-zawen` | `skills/luxun-zawen/SKILL.md` | 杂文口吻与修辞改写工具 |

## Agents (4 shipped)

| Entry | Path | Role |
|---|---|---|
| `linus-engineer` | `runtimes/claude/agents/linus-engineer.md` | roundtable 代码席，负责工程可行性与实施 |
| `munger-reviewer` | `runtimes/claude/agents/munger-reviewer.md` | roundtable 决策质量席 |
| `taleb-reviewer` | `runtimes/claude/agents/taleb-reviewer.md` | roundtable 风险结构席 |
| `lopezdeprado-reviewer` | `runtimes/claude/agents/lopezdeprado-reviewer.md` | roundtable 证据质量席 |

## Commands (1 shipped)

| Entry | Path | Role |
|---|---|---|
| `roundtable` | `runtimes/claude/commands/zhuzi/roundtable.md` | Claude 薄入口，负责装载 roundtable workflow 与共享资产 |

## Workflows (1 shipped)

| Entry | Path | Role |
|---|---|---|
| `roundtable` | `zhuzi/workflows/roundtable.md` | Roundtable 阶段编排、gate 规则与实施分支 |

## Seats (4 shipped)

| Entry | Path | Role |
|---|---|---|
| `linus-engineer` | `zhuzi/seats/linus-engineer.md` | 共享 Linus 代码席契约，定义职责、阶段纪律与输出契约 |
| `munger-reviewer` | `zhuzi/seats/munger-reviewer.md` | 共享 Munger 决策质量席契约，定义边界、route 与 seat-specific 字段 |
| `taleb-reviewer` | `zhuzi/seats/taleb-reviewer.md` | 共享 Taleb 风险结构席契约，定义 fragility 审议与输出契约 |
| `lopezdeprado-reviewer` | `zhuzi/seats/lopezdeprado-reviewer.md` | 共享 López 证据质量席契约，定义方法论边界与输出契约 |

## References (2 shipped)

| Entry | Path | Role |
|---|---|---|
| `seat-registry` | `zhuzi/references/seat-registry.md` | 当前席位权威表、默认 `stages` 规则、扩席位维护边界 |
| `verdict-schema` | `zhuzi/references/verdict-schema.md` | roundtable 共同 YAML verdict 契约与 route 映射 |

## Templates (1 shipped)

| Entry | Path | Role |
|---|---|---|
| `roundtable-quick` | `zhuzi/templates/roundtable-quick.md` | Quick Roundtable 输出骨架 |

## Manifests (1 shipped)

| Entry | Path | Role |
|---|---|---|
| `shipped-surface` | `zhuzi/manifests/shipped-surface.json` | 机器可读 shipped surface 真相源 |

## Examples (1 shipped)

| Entry | Path | Role |
|---|---|---|
| `roundtable-quick` | `examples/roundtable-quick.md` | 默认短读圆桌输出示例 |

## Tools (3 shipped)

| Entry | Path | Role |
|---|---|---|
| `check_consistency.py` | `tools/check_consistency.py` | 结构一致性检查，覆盖 manifest、inventory、shared seats、runtime adapter 路径与 schema 引用 |
| `install_codex_source_adapters.py` | `tools/install_codex_source_adapters.py` | 渲染并 side-load Codex source-only roundtable adapters 到 Codex 安装根 |
| `smoke_test_codex_roundtable.py` | `tools/smoke_test_codex_roundtable.py` | 手动 Codex roundtable 烟雾测试：刷新安装、注入 source-only adapter、验证 skill 激活 |
