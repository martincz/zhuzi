---
description: 多视角短读——并行 spawn N 个席位说一段话，不走 must_haves / gate / verdict schema，不做综合
argument-hint: [议题/想法/选择]
---

# Quick Multi-Perspective

用户启动多视角短读。**议题**：

$ARGUMENTS

<objective>
执行 `/zhuzi:quick` 协议：召集匹配的席位平行说一段话，**不**走 must_haves、**不**走 user gate、**不**走 verdict schema、**不**做综合。
默认输出：N 个并列段落 + 一张一句话对照表。
</objective>

<claude_command_adapter>
共享 workflow 里的抽象 orchestration 动作用 Claude runtime 这样落地：

- `Agent(subagent_type="X", prompt="Y")`：直接使用 Claude 的 `Agent(...)`，N 个席位**在同一条消息内并行 spawn**
- 席位 prompt **必须**含 `[quick-multi 模式 — 不走 verdict schema]` 标记
- 不需要 `continue_existing_agent` —— 本协议无续跑
</claude_command_adapter>

<execution_context>
@{{ZHUZI_SHARED_ROOT}}/workflows/quick-multi.md
@{{ZHUZI_SHARED_ROOT}}/references/seat-registry.md
@{{ZHUZI_SHARED_ROOT}}/templates/quick-multi.md
</execution_context>

<context>
仓库内对应路径：
- `zhuzi/workflows/quick-multi.md`
- `zhuzi/references/seat-registry.md`
- `zhuzi/templates/quick-multi.md`

席位匹配规则复用 seat-registry 的"擅长领域"列；本协议**不**用 manifest 里的 stage_policy（quick 没有 stages 概念）。
</context>

<process>
执行 `@{{ZHUZI_SHARED_ROOT}}/workflows/quick-multi.md` end-to-end：

1. 扫议题关键词匹配席位
2. N=0 / N=1 时按 workflow 规定退出
3. N≥2 时并行 spawn，全部用轻量 prompt
4. 平铺呈现 + 一句话对照
5. 给下一步路径建议（roundtable / standalone skill）

**禁止**：
- 不走 roundtable 的任何 gate 或 must_haves 流程
- 不在 quick 输出后自动进入实施
- 不做 orchestrator 综合与仲裁
</process>
