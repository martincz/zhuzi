---
description: 圆桌会议模式——薄入口；加载共享契约、workflow 与 Quick 模板后执行多席位审议
argument-hint: [议题/策略/提案/需求描述]
---

# 圆桌会议（Roundtable）

用户开启圆桌会议。**议题**：

$ARGUMENTS

<objective>
执行 `/zhuzi:roundtable` 的完整多席位审议流程。
默认走 Quick Roundtable：对用户只展示主持人结论、议题卡、席位短评、决策表和下一步；完整原文/YAML 仅在用户要求时展开。
</objective>

<claude_command_adapter>
共享 workflow 里的抽象 orchestration 动作用 Claude runtime 这样落地：

- `Agent(subagent_type="X", prompt="Y")`：直接使用 Claude 的 `Agent(...)`
- `continue_existing_agent(agent_id, message)`：若 runtime 支持，就用 `SendMessage(to=agent_id, message="Y")`
- 若 `continue_existing_agent(...)` 不可用，就 fallback 到新的 `Agent(...)`，并完整注入阶段 2 的 Linus 原文
</claude_command_adapter>

<execution_context>
@{{ZHUZI_SHARED_ROOT}}/workflows/roundtable.md
@{{ZHUZI_SHARED_ROOT}}/references/seat-registry.md
@{{ZHUZI_SHARED_ROOT}}/references/verdict-schema.md
@{{ZHUZI_SHARED_ROOT}}/templates/roundtable-quick.md
</execution_context>

<context>
仓库内对应路径：
- `zhuzi/workflows/roundtable.md`
- `zhuzi/references/seat-registry.md`
- `zhuzi/references/verdict-schema.md`
- `zhuzi/templates/roundtable-quick.md`

若 workflow、references、template 与 README、agent 示例段有出入，以本命令装载的执行上下文为准。
</context>

<process>
执行 `@{{ZHUZI_SHARED_ROOT}}/workflows/roundtable.md` end-to-end。
在阶段 3 未收到用户确认前，禁止进入阶段 4。
</process>
