---
name: zhuzi-roundtable
description: "用户明确要求开诸子圆桌（/zhuzi:roundtable），由具名席位审议合同并形成决策。"
metadata:
  short-description: "诸子圆桌 Codex 协调器"
---

# 诸子圆桌 · Codex

读取已安装的正式流程 `{{ZHUZI_SHARED_ROOT}}/workflows/roundtable.md`，按其中的阶段查阅相对链接。
- 在源码仓库开发且未安装时，从 `./zhuzi` 读取同一流程及其引用。

以用户给定的议题为准。用当前的 `spawn_agent` 按名称调用对应席位，传完整任务与模式。依据运行时容量和成功返回调度，保留阶段 2 的线程 ID。用能唤醒同一线程的续跑工具（如 `send_input` 或 `followup_task`），再通过当前运行时取得新一轮的完成结果。续跑不可用时按共享流程交接给新起的同名席位。具名席位缺失时如实报告。

需要确认时沿用已有明确授权。需新增授权时，用当前运行时能等待明确回复的交互方式。席位沿用父会话的沙箱与权限。
