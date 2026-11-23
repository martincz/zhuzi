# AGENTS.md

## 工作边界

- 在用户授权范围内自主完成本地修改、测试、排错与复验。保留已有改动和数据。可逆的常规选择自行处理，关键取舍、实质范围变化或缺少必要授权时再询问。
- 安装验证使用临时根。实机安装、生产或共享环境写入、破坏性清理、发布和推送须有覆盖该操作的授权。遵守运行时权限与沙箱，保护凭证和未授权数据。
- 只读任务只做检查与报告。修改任务以可用结果为准，运行相关检查，修复本轮可解决的失败并复验，交代证据与剩余限制。

## 按任务查阅

| 任务 | 查阅和修改入口 |
|---|---|
| 单人物方法、触发与表达 | 对应的 [skills/](skills/) 下 `SKILL.md`，再按议题选读其 references。新增人物判断、反模式或方法论约束须有一手依据。 |
| 正式圆桌或多视角短读 | [zhuzi/workflows/](zhuzi/workflows/) 中相应流程。席位职责和读写边界在 [zhuzi/seats/](zhuzi/seats/)，输出呈现在 [zhuzi/templates/](zhuzi/templates/)。 |
| 机器合同和验证 | [roundtable-contract.json](zhuzi/manifests/roundtable-contract.json) 定义路由、字段与类型，[verdict.py](zhuzi/validators/verdict.py) 执行跨字段校验。合同改动后通过 renderer 更新生成区块与 JSON Schema。 |
| 运行时、安装与分发 | [runtimes/](runtimes/)、[install.sh](install.sh)、[Codex 安装器](tools/install_codex_source_adapters.py)。分发面以 [shipped-surface.json](zhuzi/manifests/shipped-surface.json) 为准，同步 [INVENTORY.md](docs/INVENTORY.md)。 |

共享资产保持跨运行时、无机器专属路径。Adapter 只装载共享资产和映射运行时能力。单人物视角用 skill，协作审议才调具名席位。项目参数与业务结论留在对应项目或示例中。

规范依据见 [指令设计](docs/openai-alignment.md#指令设计)。按 [开发验证](docs/openai-alignment.md#开发验证) 选择检查。行为或协议变更验证有效、无效和边界组合。安装和 adapter 先做隔离 smoke，涉及实际调用或续跑时做在线验收。外部调用证据与判断质量分别报告。

## Code Review Rules

- 核对强制路由在 Schema 和验证链上都生效。命中覆盖条件时，追加路由不得放宽允许范围。
- 核对席位的实际调用、成功状态和精确目标子线程的新返回。完成须有运行时记录与原始结果。
- 对比判断质量、用量或延迟时，核对主持人与各席位的有效模型和推理档位。有意混用时注明，配置未知或不一致的结果不得用于同配置归因。

## 提交规范

提交使用 `feat/fix/refactor/style/chore/docs` 前缀。单次聚焦一个问题，中文摘要后用 1–3 条 `- ` 列出关键改动，条目也用中文。
