---
name: zhuzi-quick
description: "用户明确要求诸子多视角短读（/zhuzi:quick、$zhuzi-quick、诸子短读），并行召集多席位各给一段独立短评、不做综合拍板时使用；正式圆桌或单人物视角不触发。"
metadata:
  short-description: "诸子多视角短读 Codex 协调器"
---

# 诸子多视角短读 · Codex

读取已安装的短读流程 `{{ZHUZI_SHARED_ROOT}}/workflows/quick-multi.md`，按其中的相对链接完成选席与平铺呈现。
- 在源码仓库开发且未安装时，从 `./zhuzi` 读取同一流程及其引用。

将 `invoke_seat` 映射为当前运行时的 `spawn_agent` 按名调用对应席位，显式传入 `mode: quick-multi`，按并发容量调度并收集真实完成返回；本模式无续跑、无 gate、不进入实施。具名席位或能力缺失时如实说明。
