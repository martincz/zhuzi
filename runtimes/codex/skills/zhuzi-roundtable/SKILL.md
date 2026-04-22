---
name: "zhuzi-roundtable"
description: |
  Codex orchestrator for zhuzi roundtable. Use when the user explicitly asks to open a zhuzi roundtable, multi-seat deliberation, `/zhuzi:roundtable`, `开圆桌`, or `roundtable 审议`.
  Loads the shared workflow and dispatches seat agents under the common verdict schema.
metadata:
  short-description: "Codex orchestrator for zhuzi roundtable"
---

<codex_skill_adapter>
## A. Skill Invocation
- Activate when the user explicitly asks to start zhuzi roundtable, multi-seat deliberation, `/zhuzi:roundtable`, `开圆桌`, or equivalent phrasing.
- Treat the current user request as the roundtable topic unless upstream context already provides a more precise议题正文.

## B. User Confirmation Mapping
- Workflow steps that ask the user to accept / override / stop should use `request_user_input` when available.
- If `request_user_input` is unavailable, present a plain-text numbered list and wait for a text reply.
- Do not skip the stage 0.5 or stage 1.5 user gates just because the runtime lacks a richer UI.

## C. Agent() / SendMessage Mapping
- `Agent(subagent_type="X", prompt="Y")` → `spawn_agent(agent_type="X", message="Y")`
- Keep returned agent IDs so stage 4 can continue the same `linus_id` when the runtime allows it.
- Claude `SendMessage(to=linus_id, "...")` → Codex `send_input(target=linus_id, message="...")`
- If same-agent continuation is unavailable, fall back to a new `spawn_agent` and inject the full phase-2 Linus output verbatim.
- Collect final seat outputs with `wait_agent(...)`, then `close_agent(...)` after integration.
</codex_skill_adapter>

<objective>
在 Codex 中执行 zhuzi 的 roundtable 协议。默认走 Quick Roundtable：对用户只展示主持人结论、议题卡、席位短评、决策表和下一步；完整原文与 YAML 只在用户要求时展开。
</objective>

<execution_context>
Read the first existing path in each group before proceeding:

Shared workflow:
- `{{ZHUZI_SHARED_ROOT}}/workflows/roundtable.md`
- `./zhuzi/workflows/roundtable.md`

Shared references:
- `{{ZHUZI_SHARED_ROOT}}/references/seat-registry.md`
- `./zhuzi/references/seat-registry.md`
- `{{ZHUZI_SHARED_ROOT}}/references/verdict-schema.md`
- `./zhuzi/references/verdict-schema.md`

Quick template:
- `{{ZHUZI_SHARED_ROOT}}/templates/roundtable-quick.md`
- `./zhuzi/templates/roundtable-quick.md`
</execution_context>

<context>
Roundtable 的共享真相源仍然只认：
- `zhuzi/workflows/roundtable.md`
- `zhuzi/references/seat-registry.md`
- `zhuzi/references/verdict-schema.md`
- `zhuzi/templates/roundtable-quick.md`

Codex 侧没有 Claude-style slash command。本 skill 充当 Codex 的 roundtable orchestrator adapter。

硬约束：
- 阶段 3 未获用户确认前，禁止进入阶段 4
- 阶段 4 优先续跑同一个 `linus_id`；做不到才 fallback 新 spawn + 完整注入阶段 2 原文
- 不复制或改写共享协议；本 skill 只是 Codex 语义适配层
</context>

<process>
Execute the loaded roundtable workflow end-to-end in Codex.
Honor all shared gates and hard constraints, but translate Claude-style orchestration primitives through the Codex adapter mapping above whenever the workflow uses them.
</process>
