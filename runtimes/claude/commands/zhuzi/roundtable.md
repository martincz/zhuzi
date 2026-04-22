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
