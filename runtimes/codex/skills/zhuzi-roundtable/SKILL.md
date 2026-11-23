---
name: zhuzi-roundtable
description: "用户明确要求召开诸子圆桌（/zhuzi:roundtable、$zhuzi-roundtable、开圆桌），调度多席位独立审议议题合同并输出决策表时使用；单人物视角或短读不触发。"
metadata:
  short-description: "诸子圆桌 Codex 协调器"
---

# 诸子圆桌 · Codex

读取已安装的正式流程 `{{ZHUZI_SHARED_ROOT}}/workflows/roundtable.md`，按当前阶段按需查阅其中的相对链接。
- 在源码仓库开发且未安装时，从 `./zhuzi` 读取同一流程及其引用。

以用户给定的议题为准。将 `invoke_seat` 映射为当前运行时的 `spawn_agent` 按名调用对应席位，传入完整任务与 `mode: roundtable`，按并发容量调度并收集真实完成返回，保留阶段 2 的 `linus_id`。将 `continue_existing_agent` 映射为能唤醒同一线程的续跑工具（如 `send_input` 或 `followup_task`）并等待新一轮完成返回；不可用时按共享流程新起同名席位并完整附带阶段 2 原文。具名席位缺失时如实报告缺口。

沿用当前方案已有的明确授权；需新增授权或实质变更确认时，使用能等待用户明确回复的对话交互。子席位沿用父会话的沙箱与权限。
