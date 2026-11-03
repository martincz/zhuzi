# OpenAI 运行与技能设计对齐

核对日期：2026-11-03。官方文档约束与本项目的设计选择分开维护；后续升级先复核来源，再改实现。

## 官方约束与支持范围

| 内容 | 当前约定 | 本仓库的实现 |
|---|---|---|
| Codex 自定义 agent | 独立 TOML，含 `name`、`description`、`developer_instructions` | `runtimes/codex/agents/*.toml`；不在其中复制人物或 schema |
| 权限 | 自定义 agent 继承父会话权限、provider、MCP；指令不能构成独立只读沙箱 | 在父会话设置权限；席位仍遵守只分析与实施阶段边界 |
| Skill | `SKILL.md` 提供名称、描述与核心步骤，详细材料按需读取 | 人物正文保留操作内核，研究、表达、边界说明迁入对应 references |
| 本地发现 | 用户技能的推荐位置为 `~/.agents/skills`，项目技能为 `.agents/skills` | 默认用户安装使用推荐位置；隔离安装显式指定存储根，并以项目位置供运行时发现 |
| ChatGPT 分发 | 跨 ChatGPT 产品分发使用 plugin；本地 agent 配置不自动变为 ChatGPT 插件能力 | 当前安装器验收 Claude Code 与本地 Codex；尚未发布 ChatGPT plugin，不声称网页端已可使用圆桌 |

来源：[Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)、[Build skills](https://learn.chatgpt.com/docs/build-skills)、[Claude 插件迁移支持范围](https://developers.openai.com/plugins/guides/submit-claude-plugin#review-what-openai-supports)。

入口只映射当前运行时实际存在的能力。工具名、参数、并发容量和续跑方式先探测；缺少命名席位时报告缺口，不把单线程角色扮演报告成真实多席位。需要发布 ChatGPT plugin 时，应单独做 skills 打包与目标环境验收，不能把本地 TOML agent 打包后假设云端会加载。

## 本项目的设计选择

以下是项目自身的判断质量要求，不是 OpenAI 的强制字段：

- 保留 skill / seat / workflow 三层、首轮盲审、真实分歧、修订 gate 与实施授权。
- `mode: quick-multi` 与正式圆桌使用同一席位，但输出合同不同；模式规则先于正式 verdict 的字段要求。
- 缺少证据、观察到反证、超出能力圈分别说明；`untested` 不自动等于需要转向，`manager` 标签不自动证明管理漂移。
- 证据强度与席位一致程度分开。原话、转述、运行话术、框架推演不得混淆；案例中的数字明确是已知事实还是假设。
- JSON Schema、字段类型、条件路由从 manifest 派生。条件路由显式区分 `add` 与 `override`；覆盖约束不能因追加其他允许项而失效。验证器检查格式、覆盖和控制流一致性，不替代事实核实。
- 初次授权仍有效且方案没有实质变化时不重复询问。新增取舍、扩大范围或缺少授权时等待用户，沉默不是接受。

修改入口仍见 `AGENTS.md`。生成文件只通过 renderer 更新。

## 安装与迁移

先安装开发验证依赖：`python3 -m pip install -r requirements-dev.txt`。Python 3.10 使用 tomli；3.11 及以上使用内置 tomllib。

`./install.sh` 默认把人物和协调 skill 放到 `~/.agents/skills`，共享资产和原生 agent 放到 Codex 根。`CODEX_SKILL_DIR` 可单独指定技能存储目录；仅设置 `CODEX_HOME` 时仍以其下的 `skills` 保持隔离，调用方须通过项目 `.agents/skills` 等已支持的位置发现这些技能。测试会建立临时项目链接，无需修改 HOME。

Codex 安装器统一处理人物 skill、协调 skill、原生 agent 和共享资产。先读取旧共享 manifest 确认归属，渲染并暂存全部新资产，再把将覆盖或清理的资产完整备份到 Codex 根下的 `backups/zhuzi/<时间戳-随机标识>/`，同时生成 `migration.json`。新资产校验成功后才移除旧技能副本与同名 Markdown 席位，失败则恢复已触及的资产。备份留在技能和 agent 发现目录之外。

旧技能目录与新目录相同时只覆盖，不把刚更新的技能当旧副本删除；旧条目为符号链接时备份并移除链接，不改其外部目标。新旧目录内容冲突也会保留覆盖前副本。无法确认归属的同名旧技能会在修改前报错；其他技能、其他 agent、provider 配置与凭证不在迁移范围。重复运行且内容未变时，不再覆盖或生成新备份。

只检查或迁移 Codex，可以使用：

```bash
./install.sh --codex-only --dry-run --json
./install.sh --codex-only
```

第一条只预览，不修改安装；第二条执行带备份的迁移。默认 `./install.sh` 仍安装两个 runtime，Claude 侧按原有方式覆盖。这里的路径是安装说明，不写入共享人物或席位合同。

## 可复跑验证

```bash
python3 tools/render_roundtable_contract_docs.py
python3 tools/check_consistency.py
python3 -m unittest discover -s tests -v
python3 tools/smoke_test_codex_roundtable.py --offline
python3 tools/smoke_test_codex_roundtable.py
```

离线 smoke 检查临时安装、TOML 解析和引用路径。在线 smoke 另调用 Feynman 阶段 1、Linus 阶段 2，并续跑同一个 Linus；以实际调用记录、完整 verdict 校验和 fixture 未被修改为依据。

在线验收从本次临时根的 rollout 首个 `session_meta` 确定各线程身份，以原生 `agent_type`、子线程角色、精确句柄及运行时活动事件绑定调用。父模型报告的 verdict 必须与对应子线程完成的原文一致。续跑还须有成功的工具调用、同一子线程中新一轮完成的哨兵回复，并与父模型引用的原文一致。工具错误、父模型自报成功、近似 ID、旧回复或 fork 继承的父线程消息均不能代替证据。日志不足时失败，不降级为字符串匹配。

它只证明接线可用，不代表选席质量或完整决策流程已经验收。运行需要现有 Codex CLI 与可用 provider 配置，会产生模型用量。

接线探针使用继承的模型、低推理档位并禁用无关 MCP 启动，不改变用户配置；这些设置只适用于接线验收。用 `--trace-dir <临时目录>` 可保留事件与返回结果以定位问题，不复制凭证。行为评测保持独立的模型与配置记录，不能用接线探针推断质量收益。

共享验证器可在已安装的共享根下独立运行：

```bash
python3 zhuzi/validators/verdict.py verdict.json --seat feynman-reviewer --phase 1 --truth-count 1
python3 zhuzi/validators/verdict.py locked-must-haves.json
python3 zhuzi/validators/verdict.py execution.json --seat linus-engineer --phase 4 --truth-count 1 --must-haves locked-must-haves.json
```

## 行为评测

`evals/cases.json` 提供 20 个合成回归场景，覆盖证据不足、正例、选择偏差、模式边界、并发、授权和验证失败。它们是起始回归集，不能作为真实任务总体的代表。

```bash
python3 tools/run_behavioral_evals.py
python3 tools/run_behavioral_evals.py --run --case early-pmf --case clear-contract --model <可用的固定模型ID> --reasoning-effort medium --repeat 3 --output /tmp/zhuzi-eval.jsonl
```

同一议题比较普通回答、单 agent 多视角、真实圆桌，保持模型与原始事实一致。`--reasoning-effort` 默认固定为 `medium`，应选择目标模型支持的档位。每次运行使用独立临时配置，同时锁定主持人、子席默认设置和本项目原生角色文件中的模型与推理档位，避免继承用户配置中的不同默认值；不修改用户配置或源码 adapter。

记录包含请求配置与从运行时线程记录读取的有效配置，检查所有实际子线程，而不把 fork 带入的父线程设置当成子席设置。缺少证据或实际配置不一致时，`configuration.status` 标记为未核实或不匹配、`comparison_eligible` 为 false，顶层 `model` 不再伪装成已验证模型，进程返回失败并保留原始结果供排查。

同时记录 CLI 版本、资产/题集摘要、提示摘要、耗时和原始事件（含可用的用量）；评分依据不注入模型输入。配置核对通过不证明模式行为或判断质量通过，输出仍为 `unscored`。正式比较需在隐藏模式标签后，结合人类复核评估有效发现、误判遗漏、证据、协议与可执行性，并单独比较用量与延迟。按实际暴露的失败扩展留出题，避免只优化既有题面。

参考：[Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)。本项目使用本地记录器，不依赖该页面中正在退出的托管 Evals 平台。
