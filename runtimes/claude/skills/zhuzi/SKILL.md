---
name: zhuzi
description: "统一调度诸子正式圆桌（roundtable）、多视角短读（quick）与 11 位人物思维视角；仅在显式调用 $zhuzi 或 /zhuzi 时启用，常规编码、审查与问答不触发。"
argument-hint: "[roundtable|quick|<人物>] [议题]"
disable-model-invocation: true
---

# 诸子 · 统一调度入口

通过单一入口调度多席位独立审议（正式圆桌 / 多视角短读）或调用指定人物的独立判断框架。

## 路由规则

1. **无参数或询问用法**（如仅输入 `$zhuzi` / `/zhuzi`）：读取 [路由菜单与选型指引](references/routing.md)，结合当前上下文展示推荐子指令与人物表，**绝不自动启动圆桌或修改文件**。
2. **正式圆桌**：参数以 `roundtable` 或 `圆桌` 开头时，将其余参数作为议题，读取已安装共享流程 `{{ZHUZI_SHARED_ROOT}}/workflows/roundtable.md` 并按当前阶段按需查阅其中的相对引用。
   - 在源码仓库开发且未安装时，从 `./zhuzi/workflows/roundtable.md` 读取同一流程及其引用。
   - 将抽象动作 `invoke_seat` 映射为当前宿主的具名子代理调用（Codex: `spawn_agent`；Claude Code: `Agent`；Antigravity: `invoke_subagent`），传入完整任务与 `mode: roundtable`，按并发容量调度并收集真实子线程完成返回，保留阶段 2 的 `linus_id`。
   - 将 `continue_existing_agent` 映射为唤醒同一子线程的续跑工具（Codex: `send_input` / `followup_task`；Claude Code: `SendMessage`；Antigravity: `send_message`）并核对新一轮完成返回；不可用时按共享流程新起同名席位并完整附带阶段 2 原文。具名席位缺失时如实报告缺口。
3. **多视角短读**：参数以 `quick` 或 `短读` 开头时，将其余参数作为议题，读取 `{{ZHUZI_SHARED_ROOT}}/workflows/quick-multi.md`（源码未安装回退 `./zhuzi/workflows/quick-multi.md`），并行调用具名席位并显式传入 `mode: quick-multi`；本模式无续跑、无 gate、不输出 YAML verdict、绝不进入实施。
4. **指定单人物视角**：参数匹配下表任一人物别名或完整名时，读取 `{{ZHUZI_SKILL_ROOT}}/<入口名>/PERSONA.md`（源码未安装回退 `../<入口名>/SKILL.md`），再按其末尾「按需读取」仅加载当前任务对应的 1 层参考章节：

| 子指令别名 | 入口名（`<入口名>`） | 适用核心场景 |
|---|---|---|
| `linus` / `torvalds` | `linus-torvalds-engineer` | 数据结构先行、消除特判、接口兼容与代码品味审查 |
| `munger` | `munger-checklist` | 逆向失败推演、能力圈、激励错配与偏误共振商业决策 |
| `taleb` | `taleb-antifragile` | 破产吸收壁、厚尾分布、遍历性与收益凸凹性风险诊断 |
| `lopez` / `prado` | `lopezdeprado-scientist` | 因果图识别、时序数据泄漏与多重检验研究诚信审计 |
| `feynman` | `feynman-explainer` | 去行话机制、正反实例与可观察语义拆解规格说明 |
| `pg` / `paul-graham` | `paul-graham-perspective` | 真实痛点、小众深爱（PMF）、Maker 视角与文章新意评审 |
| `norman` / `don-norman` | `don-norman-perspective` | 执行/评估两道鸿沟、可发现性与操作失误（slip/mistake）诊断 |
| `jobs` / `steve-jobs` | `steve-jobs-perspective` | 一句话产品定位、端到端体验掌控与次要功能砍削 |
| `musk` / `elon-musk` | `elon-musk-perspective` | 物理渐近极限、原材料白痴指数与五步删减工程拆解 |
| `trump` | `donald-trump-perspective` | 交易筹码、BATNA 退出底牌、稀缺叙事与短期危机应对 |
| `zhangxuefeng` | `zhangxuefeng-perspective` | 按普通毕业生就业中位数与真实校招倒推中国升学志愿 |

## 授权与快捷固定（Pin）

- **权限边界**：审议与单人物分析默认严格只读；正式圆桌阶段 4 实施须基于用户对当前锁定方案的明确授权，子席位沿用父会话沙箱与权限。
- **固定高频独立入口**：若希望将某个高频人物单独暴露为顶层 `$<入口名>` / `/<入口名>` 快捷指令，可在诸子仓库运行 `./install.sh --pin <别名或入口名>`（取消固定用 `./install.sh --unpin <别名或入口名>`）。
