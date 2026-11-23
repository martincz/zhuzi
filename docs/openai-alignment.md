# 运行时、维护与验证

## 指令设计

根 `AGENTS.md` 采用纯 Markdown 开放格式（无 YAML frontmatter，体积控制在 Antigravity 单规则文件 24 KB 上限以内），定义自主执行权限、不可动摇安全红线、按任务查阅入口与验证闭环：

- **Codex CLI** 与 **Antigravity CLI** 按工作目录向上层级自动发现 `AGENTS.md`。
- **Claude Code CLI** 通过根 `CLAUDE.md` 的 `@AGENTS.md` 导入同一份文件，三端共享单一指令源，避免多份规约漂移。

根文件的 `## Code Review Rules` 仅保留跨全库生效的实质评审不变量（强制路由闭环、子线程真实完成证据、同配置对照归因）；机械格式与路径校验交给 `tools/check_consistency.py` 与单元测试。参考：[AGENTS.md 开放格式](https://agents.md/) · [Codex 指令发现](https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance) · [Claude Code 指令导入](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools) · [仓库评审规则](../AGENTS.md#code-review-rules)。

Skill 遵循开放 [Agent Skills 规范](https://agentskills.io/specification) 与渐进式披露（Progressive Disclosure）原则：

- **精确触发**：`name` 与目录名严格一致（小写连字符，`≤64` 字符）；`description`（UTF-8 `≤1024` 字节）精简声明**何时触发**与**核心职责**，仅在用户点名人物/标签或显式要求开圆桌/短读时激活。常规代码审查、文档解释、UX 评审或产品讨论不触发人物 Skill。
- **渐进加载**：根 `SKILL.md` 只负责核心判断框架、硬边界与引用路由；详细检查清单、反模式库、表达档位及一手调研留在 `references/`，仅在任务确实需要时按需读取。
- **互补分工**：回测与实验议题中，López 审因果与检验纪律，Taleb 审尾部暴露；产品与界面议题中，Jobs 看定位与取舍，Norman 诊交互鸿沟与误操作归因，PG 看真实用户需求与说服力。

## 运行时支持

共享资产（`skills/`、`zhuzi/seats/`、`zhuzi/workflows/`、`zhuzi/manifests/`、`zhuzi/validators/`）保持跨运行时中立，仅使用抽象编排动作 `invoke_seat(seat, message)` 与 `continue_existing_agent(agent_id, message)`。各 CLI 按原生规范接入：

| 运行时 | 指令发现 | Skill 发现位置 | 具名席位与编排映射 |
|---|---|---|---|
| **Claude Code CLI** | `CLAUDE.md`（`@AGENTS.md`） | `~/.claude/skills/<name>/SKILL.md` | 命令 `runtimes/claude/commands/zhuzi/*.md` + 席位 `runtimes/claude/agents/*.md`（评议席禁 `Edit/Write`），映射 `Agent` 与 `SendMessage` |
| **Codex CLI** | 层级 `AGENTS.md` | `~/.agents/skills/<name>/SKILL.md` 或 `.agents/skills/` | 协调 Skill `runtimes/codex/skills/zhuzi-*/SKILL.md` + 原生 `runtimes/codex/agents/*.toml`，映射 `spawn_agent` 与 `send_input` / `followup_task` |
| **Antigravity CLI** | 层级 `AGENTS.md` | 工作区 `.agents/skills/`、`.agents/skills.json`（如 `{"entries":[{"path":"skills"}]}`）、全局 `~/.gemini/config/skills/` 或插件 `skills/`（自动注册同名 `/<skill>` 命令） | 子席位 `.agents/agents/<name>.md` 或插件 `agents/<name>.md`（声明 `subagent: true`、`mainAgent: false` 与显式 `tools`：评议席只读，实施席 `linus-engineer` 含 `edit_file, write_file`），映射 `invoke_subagent` 与 `send_message` |

所有运行时子席均沿用父会话的权限、provider 与沙箱边界；指令层只读声明不替代宿主沙箱。`./install.sh` 开箱安装并离线验收 Claude Code 与 Codex CLI（见 [分发清单](INVENTORY.md)）；在 Antigravity CLI 等环境接入圆桌或短读时，须按原生子席调用与同线程续跑做真实接线验收，席位缺失时如实报告缺口。参见 [正式圆桌流程](../zhuzi/workflows/roundtable.md) 与 [短读流程](../zhuzi/workflows/quick-multi.md)。

## 维护共享资产

- **维护单人物 Skill**：修改对应 `skills/<name>/SKILL.md` 及其 `references/`。保持简短精确的 `description` 触发条件，用正例与常规任务反例排查误触发及跨人物重叠；`references/` 顶层文档须可从 `SKILL.md` 按需路由到达。
- **维护或新增席位**：在 [seats/](../zhuzi/seats/) 定义职责、阶段纪律与越权边界，在 [roundtable-contract.json](../zhuzi/manifests/roundtable-contract.json) 声明 root key、native verdict、路由映射及 `seat_specific` 字段，运行 `python3 -B tools/render_roundtable_contract_docs.py` 刷新生成区块与 JSON Schema。条件路由的 `override` 约束必须同时在 Schema 与 `verdict.py` 中生效。
- **维护原生 Adapter 与分发面**：仅在宿主协议变化时修改 [runtimes/](../runtimes/)，源码保留 `{{ZHUZI_SKILL_ROOT}}` / `{{ZHUZI_SHARED_ROOT}}` 模板占位符与开发态相对回退。增删分发文件同步 [shipped-surface.json](../zhuzi/manifests/shipped-surface.json) 与 [INVENTORY.md](INVENTORY.md)。

## 安装与迁移

使用 Python 3.10+ 与 [开发依赖](../requirements-dev.txt)（Python 3.10 用 `tomli` 解析 TOML，3.11+ 用内置 `tomllib`）。

`./install.sh` 默认安装 Claude Code（默认根 `~/.claude`，可用 `CLAUDE_DIR` 覆盖）与 Codex CLI（默认根 `~/.codex`，可用 `CODEX_HOME` 覆盖；默认技能发现根 `~/.agents/skills`，可用 `CODEX_SKILL_DIR` 覆盖，显式设置 `CODEX_HOME` 时技能默认随该根隔离到 `$CODEX_HOME/skills`）。安装验证一律使用临时隔离目录：

```bash
./install.sh --codex-only --dry-run --json
./install.sh --codex-only
```

第一条只预览，第二条执行带备份与回滚的 Codex 安装迁移：变更资产先暂存校验，待覆盖条目与旧版残留先备份到 `$CODEX_HOME/backups/zhuzi/<timestamp>/` 并写入 `migration.json`；旧 skill 须通过已安装 manifest 与 `name` 归属核验（或内容完全一致）才会迁移，否则中止报错；中途失败自动回滚已触及资产。外部符号链接目标、无关 skill/agent、provider 配置与凭证均不在修改范围内。

## 开发验证

从仓库根目录按改动范围执行对应检查，跑完实现—检查—修复—复验闭环：

```bash
python3 -m pip install -r requirements-dev.txt
python3 -B tools/render_roundtable_contract_docs.py --check
python3 -B tools/check_consistency.py
python3 -B -m unittest discover -s tests -v
python3 -B tools/smoke_test_codex_roundtable.py --offline
```

修改 `roundtable-contract.json` 后先运行 `python3 -B tools/render_roundtable_contract_docs.py` 刷新投影与 JSON Schema。`--offline` 在临时根完成双端隔离安装并校验渲染后的具体路径引用，不发起模型请求。

变更具名席位调用或同线程续跑协议时，在具备本机 Codex CLI 与可用 provider 的环境下运行在线接线探针（会产生模型用量）：

```bash
python3 -B tools/smoke_test_codex_roundtable.py
```

在线探针使用临时隔离安装与只读合成工作区（继承 provider 配置、低推理档位、禁用外部 MCP），核验 `feynman-reviewer`（阶段 1）与 `linus-engineer`（阶段 2）的真实角色线程 ID、成对工具调用、合规 verdict、同一 `linus-engineer` 线程的唤醒续跑新返回以及只读 fixture 零改动。`--trace-dir` 仅保存脱敏事件与会话证据，不复制凭证。

共享校验器 [verdict.py](../zhuzi/validators/verdict.py) 支持 JSON 或 YAML 文件及 `-`（stdin 只读管道），不执行合同中的验证命令：

```bash
python3 -B zhuzi/validators/verdict.py verdict.json --seat feynman-reviewer --phase 1 --truth-count 1
python3 -B zhuzi/validators/verdict.py locked-must-haves.json
python3 -B zhuzi/validators/verdict.py execution.json --seat linus-engineer --phase 4 --truth-count 1 --must-haves locked-must-haves.json
```

## 行为评测

[evals/cases.json](../evals/cases.json) 提供 20 个合成回归场景（覆盖单席短路、盲审无分歧、缺失证据、授权边界、验证跳过/失败与模式隔离）。默认列出题面；加 `--run` 时在隔离环境中对同题对照记录 `plain`（普通回答）、`single`（单 agent 多视角）与 `roundtable`（协调器入口）：

```bash
python3 -B tools/run_behavioral_evals.py --case early-pmf
python3 -B tools/run_behavioral_evals.py --run --case early-pmf --case clear-contract --model "$ZHUZI_EVAL_MODEL" --reasoning-effort medium --repeat 3 --output /tmp/zhuzi-eval.jsonl
```

记录器在临时配置中锁定父会话与全部原生子席的模型及推理档位，校验运行时实际生效配置；缺失或不一致时标记 `comparison_eligible: false` 并返回非零退出码，同时保留原始输出为 `unscored`（评分 rubric 绝不注入模型提示），供盲评后再对照用量、延迟与调用成功率。
