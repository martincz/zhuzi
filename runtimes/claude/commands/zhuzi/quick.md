---
description: "用户要求诸子多视角短读，只并列席位观点供快速阅读。"
argument-hint: "[议题]"
---

# 诸子多视角短读 · Claude Code

议题为 `$ARGUMENTS`。

用 Read 打开 `{{ZHUZI_SHARED_ROOT}}/workflows/quick-multi.md` 并按链接选席和呈现。路径中的 `$HOME` 按当前环境展开。用 `Agent` 调用已发现的同名席位，显式传 `mode: quick-multi`，按运行时容量收集完成返回。席位或能力缺失时说明。
