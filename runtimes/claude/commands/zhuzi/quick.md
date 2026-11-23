---
description: "运行诸子多视角短读，并行召集具名席位各给一段独立观点，不做综合拍板。"
argument-hint: "[议题]"
---

# 诸子多视角短读 · Claude Code

议题为 `$ARGUMENTS`。

用 Read 读取 `{{ZHUZI_SHARED_ROOT}}/workflows/quick-multi.md`，按其相对链接完成选席与平铺呈现。路径中的 `$HOME` 按当前环境展开。将 `invoke_seat` 映射为 `Agent` 调用已发现的同名席位，显式传入 `mode: quick-multi`，按运行时容量收集真实完成返回；席位或能力缺失时如实说明。
