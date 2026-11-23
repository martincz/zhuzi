---
description: "召开诸子正式圆桌，由具名席位独立审议议题合同并产出决策表与验证信号。"
argument-hint: "[议题]"
---

# 诸子圆桌 · Claude Code

议题为 `$ARGUMENTS`。

用 Read 读取 `{{ZHUZI_SHARED_ROOT}}/workflows/roundtable.md`，按当前所处阶段按需查阅其中的相对引用。路径中的 `$HOME` 按当前环境展开。

将共享流程中的 `invoke_seat` 映射为 `Agent` 调用同名已发现席位，按运行时容量收集真实完成返回并保留阶段 2 的实现席位 ID；将 `continue_existing_agent` 映射为对同一目标 ID 的 `SendMessage` 唤醒续跑（不可用时按共享流程新起同名席位并完整附带阶段 2 原文）。具名席位缺失时如实报告缺口。
