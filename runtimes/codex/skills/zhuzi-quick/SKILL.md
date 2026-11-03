---
name: "zhuzi-quick"
description: |
  诸子轻量多视角短读的 Codex skill。用户明确要求 `/zhuzi:quick`、想"快速听几个角度"、不需要拍板时使用。
  不走 must_haves / gate / verdict schema / 综合。和 zhuzi-roundtable 互补：roundtable 拍板，quick 听角度。
metadata:
  short-description: "诸子多视角短读 Codex 协调器"
---

<codex_skill_adapter>
## A. 触发规则
- 当用户明确要求 `/zhuzi:quick`、"开多视角短读"、"快速听几个角度"或等价表达时激活。
- 用户要求"开圆桌 / roundtable / 拍板"时**不**激活本 skill —— 走 `zhuzi-roundtable`。

## B. 用户确认映射
- **本协议没有 user gate** —— 无需 `request_user_input`。
- 直接 spawn 席位 → 平铺呈现 → 给路径建议。

## C. 抽象 orchestration 动作映射
- `invoke_seat(seat="X", message="Y")` → 用当前运行时的 `spawn_agent` 调用已发现的同名自定义 agent；消息显式传 `mode: quick-multi`。
- 先确认席位与工具可用，按运行时容量并发调度，超出部分排队；不可用时报告缺口，不假装已调用。
- 使用实际可用的等待和结果读取工具收集；运行时提供关闭能力时释放已完成线程。
- **不**保留 agent ID（无续跑）
- **不**调用 `continue_existing_agent`
</codex_skill_adapter>

<objective>
在 Codex 中执行 `/zhuzi:quick` 协议：N 个席位平行说一段话，不综合、不 gate、不拍板。
</objective>

<execution_context>
先确定共享根目录，只能选一个：

- 已安装共享根目录：`{{ZHUZI_SHARED_ROOT}}`
- 仓库开发态 fallback 根目录：`./zhuzi`（仅当直接在本仓库里运行且已安装根目录不可用时才用）

然后从选定根目录读取：
- `workflows/quick-multi.md`
- `references/seat-registry.md`
- `templates/quick-multi.md`
</execution_context>

<context>
共享真相源：
- `zhuzi/workflows/quick-multi.md`
- `zhuzi/references/seat-registry.md`
- `zhuzi/templates/quick-multi.md`

席位匹配规则复用 seat-registry 的"擅长领域"列；本协议**不**用 manifest 的 stage_policy。

硬约束：
- 不走 roundtable 的任何 gate 或 must_haves 流程
- 不输出 verdict YAML
- 不做 orchestrator 综合
- 不进入实施
</context>

<process>
端到端执行 `quick-multi.md`：席位匹配 → 并行 spawn → 平铺呈现 → 路径建议。
把 workflow 里的 `invoke_seat(...)` 翻译为当前 Codex 运行时真实可用的调用。
</process>
