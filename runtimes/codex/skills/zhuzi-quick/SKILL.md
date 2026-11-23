---
name: zhuzi-quick
description: "用户要求诸子多视角短读（/zhuzi:quick），只并列席位观点供快速阅读。"
metadata:
  short-description: "诸子多视角短读 Codex 协调器"
---

# 诸子多视角短读 · Codex

读取已安装的短读流程 `{{ZHUZI_SHARED_ROOT}}/workflows/quick-multi.md`，按其中的链接选席和呈现。
- 在源码仓库开发且未安装时，从 `./zhuzi` 读取同一流程及其引用。

用当前运行时的 `spawn_agent` 调用同名席位，按容量调度并收集实际完成的返回。席位或能力缺失时说明。使用共享流程规定的 `mode: quick-multi`。
