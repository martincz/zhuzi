---
name: "zhuzi-roundtable"
description: |
  诸子圆桌的 Codex 协调层 skill。用户明确要求 `/zhuzi:roundtable`、开圆桌、多席位审议时使用。
  负责装载共享 workflow，并在共同 verdict schema 下调度席位 agent。
metadata:
  short-description: "诸子圆桌 Codex 协调器"
---

<codex_skill_adapter>
## A. 触发规则
- 当用户明确要求启动 zhuzi roundtable、多席位审议、`/zhuzi:roundtable`、`开圆桌` 或等价表达时激活。
- 除非上游上下文已经提供更精确的议题正文，否则把当前用户请求直接视为本次 roundtable 议题。

## B. 用户确认映射
- 需要用户确认时，沿用已有明确授权；缺少授权或出现实质变更时，用普通对话等待用户回复。
- 只有当前运行时提供支持必答确认的交互工具时才使用它；仅用于可选问题的工具不能充当授权 gate。沉默、超时和空回答都不是批准。

## C. 抽象 orchestration 动作映射
- `invoke_seat(seat="X", message="Y")` → 使用当前运行时的 `spawn_agent`，选择已发现的同名自定义 agent 并传入消息。
- 调用前检查命名席位是否可用、并发容量和实际工具参数；不可用时明确报告兼容性缺口，不把普通回答冒充席位运行。
- 保留返回的 agent ID，方便阶段 4 在 runtime 支持时继续复用同一个 `linus_id`
- `continue_existing_agent(agent_id, message)` → 使用当前运行时能唤醒并续跑已有 agent 的工具（如 `send_input` 或 `followup_task`）；只投递消息但不唤醒空闲 agent 的工具不能视为续跑完成。
- 如果 `continue_existing_agent(...)` 不可用，就 fallback 到新的 `spawn_agent`，并完整注入阶段 2 的 Linus 原文
- 使用当前运行时实际提供的等待和结果读取工具收集完整输出；保留阶段 2 的实现席位至实施结束，最后在运行时提供关闭能力时释放它。不要假定固定工具名、参数或必有 `close_agent`。
</codex_skill_adapter>

<objective>
在 Codex 中执行 zhuzi 的 roundtable 协议。默认走 Quick Roundtable：对用户只展示主持人结论、议题卡、席位短评、决策表和下一步；完整原文与 YAML 只在用户要求时展开。
</objective>

<execution_context>
先确定共享根目录，只能选一个：

- 已安装共享根目录：`{{ZHUZI_SHARED_ROOT}}`
- 仓库开发态 fallback 根目录：`./zhuzi`（仅当直接在本仓库里运行且已安装根目录不可用时才用）

然后从选定根目录读取：
- `workflows/roundtable.md`
- `references/seat-registry.md`
- `references/verdict-schema.md`
- `templates/roundtable-quick.md`
- `manifests/roundtable-contract.json`
</execution_context>

<context>
Roundtable 的共享真相源仍然只认：
- `zhuzi/workflows/roundtable.md`
- `zhuzi/references/seat-registry.md`
- `zhuzi/references/verdict-schema.md`
- `zhuzi/templates/roundtable-quick.md`
- `zhuzi/manifests/roundtable-contract.json`

Codex 侧没有 Claude-style slash command。本 skill 充当 Codex 的 roundtable 协调层适配器。

硬约束：
- 阶段 3 未有覆盖当前方案的实施授权前，禁止进入阶段 4
- 阶段 4 优先续跑同一个 `linus_id`；做不到才 fallback 新 spawn + 完整注入阶段 2 原文
- 不复制或改写共享协议；本 skill 只是 Codex 语义适配层
</context>

<process>
在 Codex 中端到端执行已装载的 roundtable workflow。
遵守共享 gate 和硬约束；把 `invoke_seat(...)` / `continue_existing_agent(...)` 翻译为当前运行时真实可用的调用。自定义 agent 的权限、provider、MCP 和 service tier 继承父会话，adapter 不承诺独立沙箱。
</process>
