# Roundtable Workflow

正式圆桌通过具名席位对同一议题合同进行独立盲审，保留真实分歧与可追溯证据，产出决策表与验证信号。默认按 [Quick Roundtable 模板](../templates/roundtable-quick.md) 呈现；用户要求「展开原文」或「展开 YAML」时提供完整席位原文与机读 verdict。

## 阶段 0.5 · 议题、选席与审议合同

按 [席位表](../references/seat-registry.md) 的领域、默认阶段及必召开规则做语义匹配，记录召开席位、各自 `stages` 与弃权理由；精确分派参数以 [机器合同](../manifests/roundtable-contract.json) 的 `dispatch_rules` 与席位配置为准：

- 命中 `0` 席：说明原因并结束。
- 仅命中 `1` 席：默认短路退出并引导至对应单人物 Skill；仅在用户明确要求「强制开圆桌」或 `force roundtable` 时继续。
- 命中 `≥2` 席：全部纳入审议（`review_seat_soft_count = 3` 仅为软提示，不裁减命中席位；超出运行时并发上限时排队执行）。

将议题收敛为可验证的 `must_haves`（通常 1–3 条 `truths`，最多 5 条）。指标主张写明数据、比较口径与候选阈值；结构或纪律主张写明可观察通过条件。待评议席补齐的阈值或命令可暂标 `TBD`，但在进入阶段 4 实施前必须全部锁定。本轮不做的事项写入 `out_of_scope`：

```yaml
must_haves:
  truths:
    - "候选在锁定比较口径下满足延迟目标"
  verify_commands:
    - truth: 1
      cmd: "TBD — 待确认项目验证入口"
      pass_criterion: "TBD — 待定指标阈值"
  out_of_scope:
    - "API 路由重写"
```

一次性呈现议题卡、席位安排与过关标准。若用户已对本议题与范围给出明确授权（或委托在给定边界内定稿），直接进入阶段 1，不重复询问；若席位范围、核心标准或边界待定，则等待用户确认、改写或叫停。审议授权不自动构成代码实施授权。

## 阶段 1 · 独立评议

对所有 `stages` 含 `1` 的席位，在运行时并发容量内通过 `invoke_seat(seat, message)` 并行调用。每席在独立上下文接收相同议题、获授权材料、完整 `must_haves` 以及 `mode: roundtable`、`phase: 1`。首轮严格隔离其他席位结论与主持人预判，`peer_disagreements` 必须为空数组 `[]`。Linus 若参与阶段 1，仅评议数据结构、接口切法与特殊情况压力，不提前代替阶段 2 做当前代码库承载评估。

收到各席真实返回后，按 [verdict 字段说明](../references/verdict-schema.md) 运行 [校验器](../validators/verdict.py) 核对席位、阶段、`truths` 全覆盖、路由映射与 challenge 一致性。瞬时调用失败按原席位重试；仅格式不合规时请原席位在不改判断的前提下修正结构；仍无法取得有效 verdict 时如实标明缺口并暂停后续依赖阶段。

## 阶段 1.5 · 修订 gate

任一有效 verdict 的 `must_haves_challenge.triggered` 为 `true` 时暂停推进。汇总各席提出的 `revised_truth`、`revised_verify_suggestion` 与 `spawn_sub_topic`，按模板展示新旧对照表，明确标出不兼容主张及来源席位。

由用户决定接受新版、部分采纳、维持原版或重开议题；维持原版时保留争议进入阶段 2。若重审后对同一问题无新证据而重复触发相同异议，直接呈现未解取舍交用户拍板，避免死循环。

## 阶段 2 · 代码可行性

若有 `stages` 含 `2` 的席位（`linus-engineer`），调用该席位执行阶段 2（传入 `mode: roundtable`、`phase: 2`、当前确认版完整 `must_haves` 及阶段 1 各席实际返回原文），并保留该调用返回的线程 ID（`linus_id`）供阶段 4 续跑。该席位按 [Linus 契约](../seats/linus-engineer.md) 对照当前代码库核查承载路径、先行重构条件与回归风险。

运行校验器验证阶段 2 verdict：
- 若触发 `must_haves_challenge.triggered: true`：回阶段 1.5 对齐修订后重跑阶段 2。
- 若判定代码层 `broken`（`route: kill`，须附具体 `file / symbol / reason`）：单边阻止当前方案进入实施；可请相关评议席审视等价替代路径，由用户选择先重构承载、降级需求或放弃。
- 无阶段 2 席位时直接进入阶段 3。

## 阶段 3 · 决策与授权

按 [Quick Roundtable 模板](../templates/roundtable-quick.md) 呈现主持人结论、议题卡、席位短评、预期变化、决策表与下一步：
- `kill`、`too_hard`、`revise_must_haves`、代码层 `broken` 及所有 `hard_blockers` 必须直接展示，严禁软化或遗漏。
- 证据信心与席位共识分开呈现；若运行时支持 `continue_existing_agent(agent_id, message)`，可在向原席位提供对方原文后做一轮复议（校验时传 `--peer-context`），真实分歧并列保留，不强行折中。同指标同方法的可比阈值取更严格者并注明来源；不可比口径与重大取舍交用户拍板。
- 将决策归入 `DECISIONS.locked`、`deferred`、`discretion`。

若需进入阶段 4 实施，须先消除所有 `TBD` / 待定项，运行 `verdict.py`（不传 `--seat`）校验锁定版 `must_haves`，核对验证命令副作用在授权边界内，并解决全部阻断条件。当前锁定方案已有明确实施授权且范围未发生实质变化时，直接进入阶段 4；缺少实施授权、范围扩大或取舍变更时等待用户明确批准（沉默、空回复或超时均不视为批准）。

## 阶段 4 · 实施与复验

优先通过 `continue_existing_agent(linus_id, message)` 唤醒并续跑阶段 2 的同一实现席位，传入议题、锁定决策与完整锁定版 `must_haves`；仅当运行时不支持同线程续跑时，用 `invoke_seat("linus-engineer", message)` 新起同名席位，并**完整附带阶段 2 原文（严禁摘要）**与相关席位结论。核对目标线程 ID 与新一轮完成返回。

实现席位在锁定范围内自主完成闭环：**修改代码 → 逐条执行 `must_haves.verify_commands` 及项目自审检查 → 定位并修复本轮可解决的失败 → 重新运行验证确认结果**，随后返回 `linus_execution`（保持 `commit_status: not_committed`）。主持人核对变更范围与真实命令输出，并用 `--seat linus-engineer --phase 4 --truth-count <N> --must-haves <locked-file>` 校验 `linus_execution`。任一验证失败、跳过、越界改动或缺少可观察证据均不得报 `done`，须写入 `gaps_to_route_back` 回流处理。

## 运行纪律

- **权限与安全红线**：阶段 1–3 全程只读；阶段 4 严格限制在用户已授权的锁定范围内，保留工作区无关改动。向席位、验证命令和日志传递材料时遵循最小必要原则，严禁泄露凭证与未授权私有数据。
- **真实调用与原文保全**：以真实具名席位调用及对应子线程完成返回为准；运行时缺少具名席位或续跑能力时如实报告缺口，不以单线程角色扮演冒充多席审议。会话压缩前保留可访问的席位原文与验证证据，无法恢复时如实注明。
