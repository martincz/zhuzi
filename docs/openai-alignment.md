# 运行时、维护与验证

## 指令与开放规范设计

根 `AGENTS.md` 采用纯 Markdown 开放格式（无 YAML frontmatter，体积控制在 `<200` 行与 24 KB 规则上限以内），定义自主执行权限、不可动摇安全红线、按任务查阅入口与验证闭环：

- **Codex CLI** 与 **Antigravity CLI** 按工作目录向上层级自动发现 `AGENTS.md`。
- **Claude Code CLI** 通过根 `CLAUDE.md` 的 `@AGENTS.md` 导入同一份文件，三端共享单一指令源，避免多份规约漂移。

Skill 严格遵循开放 [Agent Skills 规范](https://agentskills.io/specification) 与渐进式披露（Progressive Disclosure）原则：

- **纯开放源与宿主下沉**：`skills/*/SKILL.md` 仅使用开放标准字段（`name`、`description`），核心适用场景前置并显式声明不适用边界。Codex 专属界面元数据与 `policy.allow_implicit_invocation: false` 统一收敛于侧车 `skills/*/agents/openai.yaml`；Claude 专属 `disable-model-invocation: true` 与 `argument-hint` 下沉至 `runtimes/claude/` 及构建安装管线。
- **单入口收敛与按需 Pin**：默认仅向宿主技能目录安装唯一一个 `skills/zhuzi/` 总入口（内含运行期 `personas/<name>/PERSONA.md`，避免 Codex 递归扫描产生重复顶层条目），支持 `./install.sh --pin <name>` 按需将高频人物固定为顶层独立快捷指令。
- **纯净分发与按章只读**：所有 `SKILL.md` 保持 1 层引用深度（`<500` 行）；超过 100 行的 `references/*.md` 均内置带精确行号区间的顶部目录（TOC）；`references/research/`、`upgrade-notes.md`、`verification-report.md`、`synthesis.md` 等研发底稿仅留在源码仓，运行期安装时严格剔除。

## 运行时支持

共享资产（`skills/`、`zhuzi/seats/`、`zhuzi/workflows/`、`zhuzi/manifests/`、`zhuzi/validators/`）保持跨运行时中立，仅使用抽象编排动作 `invoke_seat(seat, message)` 与 `continue_existing_agent(agent_id, message)`。各 CLI 按原生规范接入：

| 运行时 | 指令发现 | Skill 发现位置 | 具名席位与最小权限映射 |
|---|---|---|---|
| **Claude Code CLI** | `CLAUDE.md`（`@AGENTS.md`） | `~/.claude/skills/zhuzi/SKILL.md`（`disable-model-invocation: true`） | `runtimes/claude/agents/*.md`：6 个评议席仅保留 `Read, Grep, Glob` 并显式 `disallowedTools: Write, Edit, Bash, NotebookEdit` + `maxTurns: 16`；实施席 `linus-engineer` 含 `Edit, Write, Bash` + `maxTurns: 40`。映射 `Agent` 与 `SendMessage` |
| **Codex CLI** | 层级 `AGENTS.md` | `~/.agents/skills/zhuzi/SKILL.md` + `agents/openai.yaml` | `runtimes/codex/agents/*.toml`：全部席位设 `skills.include_instructions = false` 与 `features.request_permissions_tool = false`；6 个评议席设 `features.shell_tool = false`。映射 `spawn_agent` 与 `send_input` / `followup_task` |
| **Antigravity CLI** | 层级 `AGENTS.md` | `.agents/skills/zhuzi/SKILL.md` 或 `~/.gemini/config/skills/zhuzi/SKILL.md` | 子席位映射 `invoke_subagent` 与 `send_message`；评议席只读，实施席 `linus-engineer` 获授权后可修改 |

参见 [正式圆桌流程](../zhuzi/workflows/roundtable.md) 与 [短读流程](../zhuzi/workflows/quick-multi.md)。

## 维护共享资产

- **维护单人物 Skill**：修改对应 `skills/<name>/SKILL.md` 及其 `references/`（一手研究底稿放入 `references/research/`）。超过 100 行的运行期参考文件须保留 `## 目录（按场景只读对应章节）`，所有 `references/*.md` 须从 `SKILL.md` 1 跳直达。
- **维护席位与机器合同**：在 [seats/](../zhuzi/seats/) 定义职责与边界，在 [roundtable-contract.json](../zhuzi/manifests/roundtable-contract.json) 与 [shipped-surface.json](../zhuzi/manifests/shipped-surface.json) 更新配置，运行 `python3 -B tools/render_roundtable_contract_docs.py` 刷新 JSON Schema、契约投影、双端席位 adapter、`agents/openai.yaml` 与 [INVENTORY.md](INVENTORY.md)。

## 安装与迁移

使用 Python 3.10+ 与 [开发依赖](../requirements-dev.txt)。`./install.sh` 委托统一事务安装器完成 Claude Code（默认 `~/.claude`，可用 `CLAUDE_DIR` 覆盖）与 Codex CLI（默认 `~/.codex` + `~/.agents/skills`，可用 `CODEX_HOME` / `CODEX_SKILL_DIR` 覆盖）的原子安装与旧版散落技能迁移：

```bash
./install.sh --dry-run --json
./install.sh
./install.sh --pin linus
./install.sh --unpin linus
./install.sh --uninstall --dry-run
```

变更资产先在临时目录暂存校验，待覆盖条目、历史散落顶层人物技能与旧 `commands/zhuzi/` 先经归属核验并备份至 `<runtime_home>/backups/zhuzi/<timestamp>/`（含 `migration.json`），中途失败自动完整回滚。无关用户技能、自定义 agent、provider 配置与凭证均不在修改范围内。

## 开发验证

从仓库根目录按改动范围执行对应检查，跑完实现—检查—修复—复验闭环：

```bash
python3 -m pip install -r requirements-dev.txt
python3 -B tools/render_roundtable_contract_docs.py --check
python3 -B tools/check_consistency.py
python3 -B -m unittest discover -s tests -v
python3 -B tools/smoke_test_codex_roundtable.py --offline
```

变更具名席位调用或同线程续跑协议时，在具备本机 Codex CLI 与可用 provider 的环境下运行在线接线探针（会产生模型用量）：

```bash
python3 -B tools/smoke_test_codex_roundtable.py
```

共享校验器 [verdict.py](../zhuzi/validators/verdict.py) 支持 JSON 或 YAML 文件及 `-`（stdin 只读管道），不执行合同中的验证命令：

```bash
python3 -B zhuzi/validators/verdict.py verdict.json --seat feynman-reviewer --phase 1 --truth-count 1
python3 -B zhuzi/validators/verdict.py locked-must-haves.json
python3 -B zhuzi/validators/verdict.py execution.json --seat linus-engineer --phase 4 --truth-count 1 --must-haves locked-must-haves.json
```

## 触发与行为评测

- **触发边界评测集**：[evals/trigger_cases.json](../evals/trigger_cases.json) 覆盖全部 13 个 Skill 的自然带噪正例（`should_trigger`）与高混淆日常开发反例（`should_not_trigger`）。
- **行为与红线评测集**：[evals/cases.json](../evals/cases.json) 覆盖全 11 位人物与圆桌协议回归场景，内置不向模型提示泄露的确定性协议机判（`deterministic_checks`）与人工盲评 rubric：

```bash
python3 -B tools/run_behavioral_evals.py --case early-pmf
python3 -B tools/run_behavioral_evals.py --run --case early-pmf --case clear-contract --model "$ZHUZI_EVAL_MODEL" --reasoning-effort medium --repeat 3 --output /tmp/zhuzi-eval.jsonl
```
