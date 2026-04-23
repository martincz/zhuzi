# AGENTS.md

本文件给 agent runtime（Codex, Claude Code 及兼容工具）在本仓库工作时用。规约优先于任何 runtime 默认行为；与其他文档冲突时以本文件及下面列出的真相源为准。

## 仓库性质

`zhuzi` 围绕 **skill + agent + roundtable** 三层模型组织，全部资产 Markdown 驱动。修改前先分清自己在碰哪一层：

- **skill**（`skills/`）——单人物思维内核，直接对用户说话。
- **agent / seat**（`zhuzi/seats/` + `runtimes/*/agents/`）——roundtable 席位契约与 runtime adapter，对 orchestrator 返回结构化 verdict。
- **roundtable**（`zhuzi/workflows/` + `runtimes/*` 入口）——议事编排与 gate 规则，不承载人物正文。

## 真相源与修改指针

按资产层列出权威文件 + 改动入口。任何说明、示例、摘要与下列文件冲突时，以下列文件为准。

| 资产层 | 权威文件 | 改动入口 |
|---|---|---|
| 人物正文、触发词、anti-pattern、研究支撑 | `skills/<name>/SKILL.md` 及其 `references/` | 直接改对应 skill 目录 |
| 席位职责、越权边界、启动/阶段纪律 | `zhuzi/seats/<seat>.md` | 改 seat contract；保留 `## 输出契约` 生成块 marker |
| Roundtable 机器合同（Quick headings、seat/stages/route、seat-specific 字段、seat 输出契约机器段） | `zhuzi/manifests/roundtable-contract.json` | 改 manifest，然后 `python3 tools/render_roundtable_contract_docs.py` |
| Roundtable reference（seat-registry、verdict-schema）及 seat 输出契约投影段 | `zhuzi/references/*.md`、`zhuzi/seats/*.md` 的生成块 | 只改非生成说明段；生成块由 manifest 渲染 |
| Roundtable 流程、阶段、gate、Quick 行为 | `zhuzi/workflows/roundtable.md` | 先改 workflow，再看是否需要同步 runtime 入口 adapter |
| Quick Roundtable 输出骨架 | `zhuzi/templates/roundtable-quick.md` | 先改 template，再看是否同步示例 |
| Shipped surface（人读 + 机读） | `docs/INVENTORY.md` + `zhuzi/manifests/shipped-surface.json` | 两处同步 |
| 安装、渲染、side-load 行为 | `install.sh` + `tools/install_codex_source_adapters.py` | 改脚本；行为以脚本本身为准 |

## 硬约束

以下是**跨项目、跨 runtime 都成立**的规则。违反任一条属于 roundtable/agent 层的 regression，应当回滚或补齐。

1. **共享真相源优先**——同一份事实只能维护在一处。Claude 和 Codex adapter 都只装载共享资产，不复制人物正文、不内嵌 schema 副本、不自写另一份 seat 语义。
2. **Adapter 保持薄**——runtime adapter 的作用是装载 skill + seat contract + shared schema。不写维护手册、不塞生成块、不改写席位职责。
3. **Runtime-agnostic 的文案与路径**——共享资产不绑定单一 runtime、不写死机器绝对路径。源码模板允许 placeholder 和仓库 fallback；安装产物应收敛到 installed root。
4. **Skill / agent 路由护栏**——standalone 思维顾问场景激活 skill；协作席位场景才调用 agent。新增人物或席位时，skill frontmatter 触发词与 agent description 必须两侧校对不撞车。
5. **共同 verdict 契约不得私改方言**——`core` / `must_haves_review` / `must_haves_challenge` / `seat_specific` 的分层语义以 shared schema 为准。新增 native verdict 或 route 语义要先补 shared schema 与 manifest，再改 adapter。
6. **硬约束与示例分离**——能跨项目成立的纪律才进合同；某个项目、领域或工具链的业务结论只作示例，不得冒充通用规则。
7. **证据链不可断**——新增人物观点、anti-pattern、表达档位或方法论约束前，先补对应研究 / 一手来源。没有证据，不进主合同。

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

## 验证流程

修改后的最小验证：

```bash
python3 tools/render_roundtable_contract_docs.py
python3 tools/check_consistency.py
```

改动涉及 roundtable surface、shared schema、Codex adapter 或安装路径时，再跑：

```bash
python3 tools/smoke_test_codex_roundtable.py
```

额外自查：

- 引用的路径真实存在且是当前权威路径
- 没有把机器专属绝对路径写进 active 文档
- 没有把某个项目的业务纪律泄漏进通用合同
- adapter、workflow、registry、schema、inventory、manifest 之间没有重复维护同一份真相

## 反模式

agent 在本仓库工作时不得做的事：

- 把人物正文复制到 adapter 里（应只引用 skill 路径）
- 在 adapter 内嵌 YAML schema 片段或维护手册（应引用 shared schema）
- 添加只对单一 runtime 有效的路径、指令或命名（应保留 runtime-agnostic 占位符）
- 在通用规约中写死某个业务项目的参数、口径或纪律（应收敛到示例或具体项目的文档）
- 新增 seat / native verdict / route 语义时跳过 manifest 直接改 reference 或 adapter（应先改 manifest 再渲染）
- 手改 `<!-- GENERATED: ... -->` 区块内容（应改 manifest 后重新渲染）
