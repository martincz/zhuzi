# zhuzi Shipped Surface Inventory

> 人读清单由 `tools/render_roundtable_contract_docs.py` 从 `zhuzi/manifests/shipped-surface.json` 确定性生成；机器合同另见 `zhuzi/manifests/roundtable-contract.json`。

## Skills (12 shipped)

| Entry | Path | Role |
|---|---|---|
| `zhuzi` | `skills/zhuzi/SKILL.md` | 统一总控入口 Skill（调度正式圆桌、多视角短读与 11 位人物视角，默认唯一顶层安装项） |
| `linus-torvalds-engineer` | `skills/linus-torvalds-engineer/SKILL.md` | 代码、架构、good taste 思维顾问（支持 $zhuzi linus 调用或 --pin 独立固定） |
| `munger-checklist` | `skills/munger-checklist/SKILL.md` | 决策质量、偏误、激励结构思维顾问（支持 $zhuzi munger 调用或 --pin 独立固定） |
| `taleb-antifragile` | `skills/taleb-antifragile/SKILL.md` | fragility、tail risk、antifragile 思维顾问（支持 $zhuzi taleb 调用或 --pin 独立固定） |
| `lopezdeprado-scientist` | `skills/lopezdeprado-scientist/SKILL.md` | 研究诚信、causal claim、实验纪律思维顾问（支持 $zhuzi lopez 调用或 --pin 独立固定） |
| `feynman-explainer` | `skills/feynman-explainer/SKILL.md` | 解释清晰度、cargo cult 检测、概念理解思维顾问（支持 $zhuzi feynman 调用或 --pin 独立固定） |
| `paul-graham-perspective` | `skills/paul-graham-perspective/SKILL.md` | essay 写作、创业评估、人生选择思维顾问（支持 $zhuzi pg 调用或 --pin 独立固定） |
| `donald-trump-perspective` | `skills/donald-trump-perspective/SKILL.md` | 谈判、品牌、媒体战、对抗性博弈思维顾问（非政治立场工具，支持 $zhuzi trump 调用或 --pin 独立固定） |
| `don-norman-perspective` | `skills/don-norman-perspective/SKILL.md` | UI/UX 失败的认知诊断思维顾问（支持 $zhuzi norman 调用或 --pin 独立固定） |
| `steve-jobs-perspective` | `skills/steve-jobs-perspective/SKILL.md` | 产品 / 设计 / 聚焦 / 极致体验思维顾问（支持 $zhuzi jobs 调用或 --pin 独立固定） |
| `elon-musk-perspective` | `skills/elon-musk-perspective/SKILL.md` | 工程实用主义 / 第一性原理 / 渐近极限 / 五步算法思维顾问（支持 $zhuzi musk 调用或 --pin 独立固定） |
| `zhangxuefeng-perspective` | `skills/zhangxuefeng-perspective/SKILL.md` | 教育实用主义 / 高考志愿 / 就业倒推思维顾问（支持 $zhuzi zhangxuefeng 调用或 --pin 独立固定） |

## OpenAI Sidecars (12 shipped)

| Entry | Path | Role |
|---|---|---|
| `zhuzi` | `skills/zhuzi/agents/openai.yaml` | Codex 诸子总控入口 UI 元数据与显式调用策略（allow_implicit_invocation: false） |
| `linus-torvalds-engineer` | `skills/linus-torvalds-engineer/agents/openai.yaml` | Codex Linus 工程顾问侧车元数据与显式调用策略 |
| `munger-checklist` | `skills/munger-checklist/agents/openai.yaml` | Codex Munger 决策顾问侧车元数据与显式调用策略 |
| `taleb-antifragile` | `skills/taleb-antifragile/agents/openai.yaml` | Codex Taleb 反脆弱顾问侧车元数据与显式调用策略 |
| `lopezdeprado-scientist` | `skills/lopezdeprado-scientist/agents/openai.yaml` | Codex López 研究诚信顾问侧车元数据与显式调用策略 |
| `feynman-explainer` | `skills/feynman-explainer/agents/openai.yaml` | Codex Feynman 解释顾问侧车元数据与显式调用策略 |
| `paul-graham-perspective` | `skills/paul-graham-perspective/agents/openai.yaml` | Codex Paul Graham 创业与写作顾问侧车元数据与显式调用策略 |
| `donald-trump-perspective` | `skills/donald-trump-perspective/agents/openai.yaml` | Codex Trump 商业谈判顾问侧车元数据与显式调用策略 |
| `don-norman-perspective` | `skills/don-norman-perspective/agents/openai.yaml` | Codex Don Norman 可用性顾问侧车元数据与显式调用策略 |
| `steve-jobs-perspective` | `skills/steve-jobs-perspective/agents/openai.yaml` | Codex Steve Jobs 产品聚焦顾问侧车元数据与显式调用策略 |
| `elon-musk-perspective` | `skills/elon-musk-perspective/agents/openai.yaml` | Codex Elon Musk 工程拆解顾问侧车元数据与显式调用策略 |
| `zhangxuefeng-perspective` | `skills/zhangxuefeng-perspective/agents/openai.yaml` | Codex 张雪峰升学就业顾问侧车元数据与显式调用策略 |

## Claude Skills (1 shipped)

| Entry | Path | Role |
|---|---|---|
| `zhuzi` | `runtimes/claude/skills/zhuzi/SKILL.md` | Claude 统一总入口 Skill（迁自旧 commands/zhuzi/，含 disable-model-invocation: true 与参数提示） |

## Agents (7 shipped)

| Entry | Path | Role |
|---|---|---|
| `linus-engineer` | `runtimes/claude/agents/linus-engineer.md` | roundtable 代码席，负责工程可行性与获授权实施（maxTurns: 40） |
| `munger-reviewer` | `runtimes/claude/agents/munger-reviewer.md` | roundtable 决策质量只读席（禁 Write/Edit/Bash） |
| `taleb-reviewer` | `runtimes/claude/agents/taleb-reviewer.md` | roundtable 风险结构只读席（禁 Write/Edit/Bash） |
| `lopezdeprado-reviewer` | `runtimes/claude/agents/lopezdeprado-reviewer.md` | roundtable 证据质量只读席（禁 Write/Edit/Bash） |
| `feynman-reviewer` | `runtimes/claude/agents/feynman-reviewer.md` | roundtable 解释清晰度只读席（禁 Write/Edit/Bash） |
| `paul-graham-reviewer` | `runtimes/claude/agents/paul-graham-reviewer.md` | roundtable Maker 视角只读席（禁 Write/Edit/Bash） |
| `don-norman-reviewer` | `runtimes/claude/agents/don-norman-reviewer.md` | roundtable UI/UX 认知诊断只读席（禁 Write/Edit/Bash） |

## Codex Agents (7 shipped)

| Entry | Path | Role |
|---|---|---|
| `linus-engineer` | `runtimes/codex/agents/linus-engineer.toml` | Codex roundtable 代码席 adapter（禁提权与自动技能注入） |
| `munger-reviewer` | `runtimes/codex/agents/munger-reviewer.toml` | Codex roundtable 决策质量只读席 adapter（禁 shell_tool 与自动技能注入） |
| `taleb-reviewer` | `runtimes/codex/agents/taleb-reviewer.toml` | Codex roundtable 风险结构只读席 adapter（禁 shell_tool 与自动技能注入） |
| `lopezdeprado-reviewer` | `runtimes/codex/agents/lopezdeprado-reviewer.toml` | Codex roundtable 证据质量只读席 adapter（禁 shell_tool 与自动技能注入） |
| `feynman-reviewer` | `runtimes/codex/agents/feynman-reviewer.toml` | Codex roundtable 解释清晰度只读席 adapter（禁 shell_tool 与自动技能注入） |
| `paul-graham-reviewer` | `runtimes/codex/agents/paul-graham-reviewer.toml` | Codex roundtable Maker 视角只读席 adapter（禁 shell_tool 与自动技能注入） |
| `don-norman-reviewer` | `runtimes/codex/agents/don-norman-reviewer.toml` | Codex roundtable UI/UX 认知诊断只读席 adapter（禁 shell_tool 与自动技能注入） |

## Workflows (2 shipped)

| Entry | Path | Role |
|---|---|---|
| `roundtable` | `zhuzi/workflows/roundtable.md` | Roundtable 阶段编排、gate 规则与实施分支 |
| `quick-multi` | `zhuzi/workflows/quick-multi.md` | 多视角短读流程：N 席位平行说一段话，不走 must_haves / gate / verdict schema |

## Seats (7 shipped)

| Entry | Path | Role |
|---|---|---|
| `linus-engineer` | `zhuzi/seats/linus-engineer.md` | 共享 Linus 代码席契约，定义职责、阶段纪律与输出契约 |
| `munger-reviewer` | `zhuzi/seats/munger-reviewer.md` | 共享 Munger 决策质量席契约，定义边界、route 与 seat-specific 字段 |
| `taleb-reviewer` | `zhuzi/seats/taleb-reviewer.md` | 共享 Taleb 风险结构席契约，定义 fragility 审议与输出契约 |
| `lopezdeprado-reviewer` | `zhuzi/seats/lopezdeprado-reviewer.md` | 共享 López 证据质量席契约，定义方法论边界与输出契约 |
| `feynman-reviewer` | `zhuzi/seats/feynman-reviewer.md` | 共享 Feynman 解释清晰度席契约，定义清晰度审议与输出契约 |
| `paul-graham-reviewer` | `zhuzi/seats/paul-graham-reviewer.md` | 共享 Paul Graham Maker 视角席契约，定义 taste 审议与输出契约 |
| `don-norman-reviewer` | `zhuzi/seats/don-norman-reviewer.md` | 共享 Don Norman UI/UX 认知诊断席契约，定义 UI 评审纪律与输出契约 |

## References (2 shipped)

| Entry | Path | Role |
|---|---|---|
| `seat-registry` | `zhuzi/references/seat-registry.md` | 席位领域、默认阶段与必召开规则的生成说明 |
| `verdict-schema` | `zhuzi/references/verdict-schema.md` | roundtable 共同 YAML verdict 契约与 route 映射 |

## Templates (2 shipped)

| Entry | Path | Role |
|---|---|---|
| `roundtable-quick` | `zhuzi/templates/roundtable-quick.md` | Quick Roundtable 输出骨架与渲染约定（输出形态真相源） |
| `quick-multi` | `zhuzi/templates/quick-multi.md` | 多视角短读输出骨架 |

## Manifests (2 shipped)

| Entry | Path | Role |
|---|---|---|
| `roundtable-contract` | `zhuzi/manifests/roundtable-contract.json` | roundtable 机器执行合同，覆盖 Quick headings、seat/stages/route、seat-specific 字段与双端 adapter 策略 |
| `shipped-surface` | `zhuzi/manifests/shipped-surface.json` | 机器可读 shipped surface 与运行期排除清单真相源 |

## Examples (5 shipped)

| Entry | Path | Role |
|---|---|---|
| `roundtable-quick` | `examples/roundtable-quick.md` | 默认短读圆桌输出示例 |
| `roundtable-disagreement` | `examples/roundtable-disagreement.md` | 多席位真分歧示例（Munger vs Taleb 路径相反，不强行收敛） |
| `roundtable-revision-gate` | `examples/roundtable-revision-gate.md` | 阶段 1.5 修订 gate 触发示例（席位推翻刚拍板的 must_haves） |
| `roundtable-broken-veto` | `examples/roundtable-broken-veto.md` | Linus 阶段 2 broken 单边否决示例 |
| `quick-multi` | `examples/quick-multi.md` | 多视角短读输出示例 |

## Tools (5 shipped)

| Entry | Path | Role |
|---|---|---|
| `check_consistency.py` | `tools/check_consistency.py` | 检查合同投影、分发清单、Skill 元数据、openai.yaml 侧车、引用深度与只读权限边界 |
| `install_codex_source_adapters.py` | `tools/install_codex_source_adapters.py` | 双端统一事务安装器（单目录 zhuzi 安装、--pin/--unpin 快捷固定、旧散落条目归属迁移、备份回滚与卸载） |
| `render_roundtable_contract_docs.py` | `tools/render_roundtable_contract_docs.py` | 从机器清单确定性渲染契约文档、JSON Schema、双端席位 adapter、openai.yaml 侧车与 INVENTORY.md |
| `smoke_test_codex_roundtable.py` | `tools/smoke_test_codex_roundtable.py` | 双端隔离安装、运行期纯净度校验与在线两席实际 verdict 及同线程续跑探针 |
| `run_behavioral_evals.py` | `tools/run_behavioral_evals.py` | 记录普通回答、单 agent 多视角与真实圆桌的可比较模型运行及确定性协议预筛 |

## Schemas (1 shipped)

| Entry | Path | Role |
|---|---|---|
| `verdict.schema` | `zhuzi/schemas/verdict.schema.json` | 从 manifest 生成的正式圆桌 JSON Schema |

## Validators (1 shipped)

| Entry | Path | Role |
|---|---|---|
| `verdict` | `zhuzi/validators/verdict.py` | 校验 verdict、truth 覆盖、条件路由与实施验证记录 |

## Evals (2 shipped)

| Entry | Path | Role |
|---|---|---|
| `cases` | `evals/cases.json` | 合成行为与安全红线回归场景（覆盖全 11 位人物与圆桌协议）及确定性协议断言 |
| `trigger_cases` | `evals/trigger_cases.json` | 全量 Skill 路由触发评测集（should-trigger 带噪正例与 should-not-trigger 日常编码混淆反例） |
