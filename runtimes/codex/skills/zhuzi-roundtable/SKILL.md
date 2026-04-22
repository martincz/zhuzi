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
- workflow 里凡是要求用户接受 / override / 停止的步骤，有 `request_user_input` 就用它。
- 如果 `request_user_input` 不可用，就退回纯文本编号列表并等待用户回复。
- 不要因为 runtime 缺少更丰富的交互 UI，就跳过阶段 0.5 或阶段 1.5 的用户 gate。

## C. Agent() / SendMessage 映射
- `Agent(subagent_type="X", prompt="Y")` → `spawn_agent(agent_type="X", message="Y")`
- 保留返回的 agent ID，方便阶段 4 在 runtime 支持时继续复用同一个 `linus_id`。
- Claude `SendMessage(to=linus_id, "...")` → Codex `send_input(target=linus_id, message="...")`
- 如果同一 agent 续跑不可用，就 fallback 到新的 `spawn_agent`，并完整注入阶段 2 的 Linus 原文。
- 用 `wait_agent(...)` 收集席位输出，整合完成后再 `close_agent(...)`。
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
</execution_context>

<context>
Roundtable 的共享真相源仍然只认：
- `zhuzi/workflows/roundtable.md`
- `zhuzi/references/seat-registry.md`
- `zhuzi/references/verdict-schema.md`
- `zhuzi/templates/roundtable-quick.md`

Codex 侧没有 Claude-style slash command。本 skill 充当 Codex 的 roundtable 协调层适配器。

硬约束：
- 阶段 3 未获用户确认前，禁止进入阶段 4
- 阶段 4 优先续跑同一个 `linus_id`；做不到才 fallback 新 spawn + 完整注入阶段 2 原文
- 不复制或改写共享协议；本 skill 只是 Codex 语义适配层
</context>

<process>
在 Codex 中端到端执行已装载的 roundtable workflow。
遵守所有共享 gate 和硬约束；凡 workflow 里出现 Claude 风格 orchestration primitive 时，都按上面的 Codex adapter 映射去翻译执行。
</process>
