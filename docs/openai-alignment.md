# 运行时、维护与验证

## 指令设计

根 `AGENTS.md` 使用开放 Markdown 格式，提供维护本仓库所需的授权边界、资产入口和完成标准。Codex 按工作目录与项目层级发现指令。Claude Code 通过根 `CLAUDE.md` 的 `@AGENTS.md` 导入同一份文件，兼容尚不直接发现 `AGENTS.md` 的版本。[AGENTS.md 开放格式](https://agents.md/) · [Codex 指令发现说明](https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance) · [Claude Code 指令导入](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools)

根文件的 `## Code Review Rules` 保留适用于全库的评审规则。只影响某个目录的规则放到对应范围。评审规则写清应指出的实际问题、兼容条件或例外，格式和其它机械检查交给校验脚本与测试。项目自行定义授权和协议边界，运行时配置负责执行权限。[OpenAI 评审指导](https://learn.chatgpt.com/docs/third-party/github#customize-what-codex-reviews) · [仓库评审规则](../AGENTS.md#code-review-rules)

Skill 通过 `name` 和 `description` 发现。入口保留判断方法、边界和按需引用。指定单人物、听几席短评、正式审议按用户意图触发。普通的「审架构」或「讲清楚」无需加载人物。回测议题中，López 关注证据，Taleb 关注尾部暴露。产品议题中，Jobs 看取舍，Norman 看交互失败，PG 看实际需求和说服力。具体指令按任务与阶段提供，在授权范围内自主完成并验证结果。[Agent Skills 规范](https://agentskills.io/specification) · [Skill 渐进加载](https://learn.chatgpt.com/docs/build-skills#how-chatgpt-and-codex-use-skills) · [GPT-6.2 任务完成指南](https://developers.openai.com/api/docs/guides/latest-model#task-completion)

## 运行时支持

安装器提供 Codex CLI 和 Claude Code 的原生入口。Codex 的席位使用独立 TOML，Claude Code 使用 Markdown 席位与命令。两端共用人物 Skill、席位契约和议事流程。Codex 子席沿用父会话的权限、provider 和 MCP。需要强制只读时，在父会话使用适当的权限配置或沙箱。[分发清单](INVENTORY.md) · [Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents) · [Claude Code Skills](https://code.claude.com/docs/en/skills)

其他支持 Agent Skills 的工具可按各自的发现方式接入单人物 Skill。接入短读或正式圆桌还需适配具名席位调用、等待和读取实际结果。实施席位的续跑及回退遵循共享流程。新增运行时按其原生入口做验收。[正式圆桌流程](../zhuzi/workflows/roundtable.md) · [短读流程](../zhuzi/workflows/quick-multi.md)

## 维护共享资产

- 单人物维护其 `SKILL.md` 与相关引用。按独立职责判断是否还需要协作席位。沿用既有名称和别名，新增触发用实际正例和容易误触发的反例核对。
- 新增席位时定义擅长领域、阶段、越权边界、native verdict、路由及证据字段。职责写在 [seats/](../zhuzi/seats/)，字段和路由写进 [roundtable-contract.json](../zhuzi/manifests/roundtable-contract.json)，统一生成投影。条件路由的覆盖限制必须同时在 Schema 和验证器中生效。
- 只在需要时改 [runtimes/](../runtimes/) 的原生入口。保留模板路径，使用安装后实际根验证。新增分发项同步 [shipped-surface.json](../zhuzi/manifests/shipped-surface.json) 和 [INVENTORY.md](INVENTORY.md)，包括两端适配器。
- 维护者在仓库根目录运行生成器和相关检查。样例须明确假设与观察。生产或具体项目的阈值以其自身合同为准。

## 安装与迁移

使用 Python 3.10+ 和 [开发依赖](../requirements-dev.txt)。Python 3.10 由 tomli 解析原生 agent，3.11 及以上用内置 tomllib。

`./install.sh` 安装两个运行时。Claude 默认根为 `~/.claude`，可设 `CLAUDE_DIR`。默认渲染符号路径，adapter 按当前 `$HOME` 展开。Claude 对本项目的目标命令、同名 agent、skill 和共享目录做覆盖安装。Codex 默认把共享资产和 agent 放到 `~/.codex`，把 skill 放到发现目录 `~/.agents/skills`。

`CODEX_HOME` 可指定 Codex 根，显式指定时 skill 存储默认随之移到该根下的 `skills/`。用 `CODEX_SKILL_DIR` 可单独指定技能存储。自定义存储需用支持的发现位置接入，例如临时项目的 `.agents/skills` 链接。安装验证时使用隔离目录。

```bash
./install.sh --codex-only --dry-run --json
./install.sh --codex-only
```

第一条只预览，第二条执行 Codex 安装与迁移。变更资产先暂存。已有目标和拟迁移条目先备份并校验，记录在 Codex 根下的 `backups/zhuzi/` 和 `migration.json`。新资产校验成功后清理旧条目。旧 skill 需匹配已安装清单与标识，或与待安装内容一致，否则停止。迁移失败恢复已触及资产。符号链接保全外部目标，未变资产不反复覆盖。无关资产、provider 配置与凭证在迁移范围之外。

## 开发验证

从仓库根目录执行。选择与改动范围对应的检查。

```bash
python3 -m pip install -r requirements-dev.txt
python3 -B tools/render_roundtable_contract_docs.py --check
python3 -B tools/check_consistency.py
python3 -B -m unittest discover -s tests -v
python3 -B tools/smoke_test_codex_roundtable.py --offline
```

修改机器合同后，先运行 `python3 -B tools/render_roundtable_contract_docs.py` 更新生成物。离线 smoke 在临时根安装两端资产并核对入口引用，无模型请求。机器合同测试覆盖结构、跨字段、路由和实施验证，内容事实仍需核实。

变更具名调用或续跑时，对 Codex 额外执行在线接线探针。需要本机 Codex CLI 和可用 provider 配置，产生模型用量。

```bash
python3 -B tools/smoke_test_codex_roundtable.py
```

探针使用隔离安装和只读合成工作区，调用 Feynman 阶段 1 与 Linus 阶段 2 并续跑同一 Linus。继承 provider 配置，使用低推理档位并禁用 MCP。结果核对真实的角色与线程 ID、成功调用、每席完成原文、同一实现席的新一轮返回及 fixture 未被改动。用 `--trace-dir` 保存调试事件时使用临时目录。调试文件不复制凭证。接线检查只覆盖探针路径，不能推断其它运行时或判断质量。

共享 [verdict 校验器](../zhuzi/validators/verdict.py) 支持 JSON 或 YAML。下面用本地捕获文件演示，不执行合同中的命令。只读场景可用 `-` 从 stdin 输入。

```bash
python3 -B zhuzi/validators/verdict.py verdict.json --seat feynman-reviewer --phase 1 --truth-count 1
python3 -B zhuzi/validators/verdict.py locked-must-haves.json
python3 -B zhuzi/validators/verdict.py execution.json --seat linus-engineer --phase 4 --truth-count 1 --must-haves locked-must-haves.json
```

## 行为评测

[evals/cases.json](../evals/cases.json) 是合成回归题集，包含参与者边界、缺失证据、授权、验证及模式差异。先列题。运行时在新路径保存 JSONL，并将 `ZHUZI_EVAL_MODEL` 设为 provider 支持的模型 ID，选择该模型支持的推理档位。

```bash
python3 -B tools/run_behavioral_evals.py --case early-pmf
python3 -B tools/run_behavioral_evals.py --run --case early-pmf --case clear-contract --model "$ZHUZI_EVAL_MODEL" --reasoning-effort medium --repeat 3 --output /tmp/zhuzi-eval.jsonl
```

记录器对同题比较普通回答、单 agent 多视角和圆桌协调入口。主持人与子席在临时配置中固定模型和推理档位，记录有效设置、CLI 版本、题集和资产摘要、提示摘要、原始事件与耗时。设置缺失或不一致时标记 `comparison_eligible: false`，返回失败并保留运行结果。

题集的评分依据不进入模型提示。记录原始输出为 `unscored`。在共同条件下盲评发现、错误、证据和可执行性，再单独比较用量、延迟与调用成功率。保留未参与提示修订的题面，并明确线上接线与判断质量各自的覆盖范围。参见 [OpenAI 评测指南](https://developers.openai.com/api/docs/guides/evaluation-best-practices)。
