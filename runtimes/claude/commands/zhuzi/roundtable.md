---
description: "用户明确要求开诸子圆桌，由具名席位审议合同并形成决策。"
argument-hint: "[议题]"
---

# 诸子圆桌 · Claude Code

议题为 `$ARGUMENTS`。

用 Read 打开 `{{ZHUZI_SHARED_ROOT}}/workflows/roundtable.md`，按其中的阶段查阅相对链接。路径中的 `$HOME` 按当前环境展开。

用 `Agent` 调用已发现的同名席位，按运行时容量收集完成返回。续跑时使用当前可用的 `SendMessage`，以阶段 2 的实际 ID 为目标并等到新返回。续跑不可用时按共享流程交接给新起的同名席位。具名席位缺失时如实报告。
