# Shared Verdict Schema

正式圆桌的输出说明，由 [机器合同](../manifests/roundtable-contract.json) 定义字段和路由。

## 输出模式

<!-- GENERATED:verdict_schema_modes:start -->
- `roundtable`：按下述正式输出契约返回 verdict；实施另受阶段与用户授权约束。
- `quick-multi`：只返回不超过 200 字的观点，不输出 verdict/YAML，不做 must_haves 审议，不实施。
- 模式由主持人显式传入；Quick 的无 verdict 规则优先于正式模式的四层必填规则。
<!-- GENERATED:verdict_schema_modes:end -->

## 层级结构

正式评议的 verdict 包含四层。

<!-- GENERATED:verdict_schema_layers:start -->
- `core`
- `must_haves_review`
- `must_haves_challenge`
- `seat_specific`
<!-- GENERATED:verdict_schema_layers:end -->

## `core`

<!-- GENERATED:verdict_schema_core_table:start -->
| 字段 | 取值 | 作用 |
|---|---|---|
| `seat` | `taleb` / `munger` / `lopezdeprado` / `feynman` / `paul_graham` / `norman` / `linus` / 新席位 | 席位标识 |
| `phase` | `1` / `2` | 评议阶段 |
| `route` | `go` / `go_with_conditions` / `revise_must_haves` / `kill` / `too_hard` | 主持人机读统一路由空间 |
| `seat_native_verdict` | 各席位原生 verdict | 保留人物 DNA |
| `confidence` | `low` / `medium` / `high` | 证据支持程度，与席位是否一致分开 |
| `hard_blockers` | `array` | 转 go 前必须解决的条件 |
| `peer_disagreements` | `array` | 见过对方原文后记录的分歧；盲审首轮为空 |
| `evidence` | `array` | 每项含 claim/source/kind 的可追溯依据 |
| `missing_evidence` | `array` | 尚缺的关键资料或未核实的前提 |
<!-- GENERATED:verdict_schema_core_table:end -->

## `must_haves_review`

统一 flag 空间：

<!-- GENERATED:verdict_schema_review_flags:start -->
- `none`
- `threshold_issue`
- `method_issue`
- `overfitting_risk`
- `metric_gaming`
- `coverage_gap`
- `lookahead_unchecked`
- `multiple_testing`
- `incentive_mismatch`
- `other`
<!-- GENERATED:verdict_schema_review_flags:end -->

每条 `must_haves.truths` 都必须单独给一条 review 记录。即使 `flag: none` 也不得省略该 truth。

## `must_haves_challenge`

```yaml
must_haves_challenge:
  triggered: true
  challenged_truths: [1, 3]
  fundamental_issue: "<为何 must_haves 框架从根本跑偏>"
  proposed_revision:
    - truth_id: 1
      revised_truth: "<修订后的主张本身，≤ 50 字>"
      revised_verify_suggestion: "<如何验证此主张；无则空字符串 ''>"
      spawn_sub_topic: "<建议拆出的新子议题；无则空字符串 ''>"
```

### `proposed_revision` 三字段分层规则

- `revised_truth` 只放主张本身，禁混实现路径、文件路径、grep 命令、阈值或衍生议题。
- `revised_verify_suggestion` 只放验证建议。
- `spawn_sub_topic` 只放拆分出去的新议题。
- 严禁回退成旧式字符串字面量 `proposed_revision: | ...`。

任一席位 `triggered: true`，修订 gate 必触发，包括阶段 2 再次提出的 challenge。orchestrator 不得忽略。

## 证据与机读验证

`core.evidence` 每项含 `claim`、`source`、`kind`。`kind` 分 `provided`（议题材料）、`observed`（实际工具观察）、`primary_source`（核对过的一手来源）、`inference`（框架推演）；推演不得伪装成已观察事实。`missing_evidence` 明列仍缺的关键资料，不能用人格化语气补齐。

信心说明证据质量和适用边界；席位是否一致单独呈现。独立线程保证上下文隔离，不保证统计独立。首轮没有其他席位原文时，`peer_disagreements` 必须为空；主持人基于实际返回值记录分歧，后续有对方原文的复议才填写该字段。

[JSON Schema](../schemas/verdict.schema.json) 由 manifest 生成。JSON 对象和 YAML 均可用于机读 verdict；布尔值写 `true` / `false`，字符串枚举 `yes` / `no` 在 YAML 中须加引号。

用共享根下的 [校验器](../validators/verdict.py) 检查席位、阶段、类型、覆盖和路由。正式评议调用 `python3 -B validators/verdict.py <file> --seat <seat-id> --phase <1|2> --truth-count <N>`。可直接传文件或用 `-` 从 stdin 读取。复议确实收到他席原文时可传 `--peer-context`。

实施前用同一脚本校验锁定 must_haves，省略 `--seat`。校验实施报告时传 `--seat linus-engineer --phase 4 --truth-count <N> --must-haves <locked-file>`。校验器核对结构和控制流，需要另查真实命令与结果。

## `seat_specific`

各席位保留自己的附加字段：

<!-- GENERATED:verdict_schema_seat_specific:start -->
- Taleb: `tail_events_breaking_must_haves` / `fragility_checklist_failures` / `distribution_class` / `payoff_convexity` / `skin_in_the_game`
- Munger: `anti_patterns_hit` / `lollapalooza_stack` / `circle_of_competence` / `incentive_map` / `opportunity_cost_note` / `reverse_kill_path`
- López: `claim_classification` / `causal_graph_missing` / `trial_count_disclosed` / `integrity_checklist_failures` / `anti_pattern_hits` / `workflow_diagnosis` / `domain_limit_flag`
- Feynman: `undefined_terms` / `mechanism_gaps` / `missing_examples` / `boundary_gaps` / `false_analogies` / `verification_gaps` / `ai_misread_risk` / `diagnosis_level`
- Paul Graham: `founder_type` / `pmf_signal` / `taste_verdict` / `identity_risk` / `superlinear_score` / `anti_patterns_hit` / `out_of_circle_flags`
- Norman: `gulf_diagnosis` / `three_pillars_failures` / `slip_vs_mistake_classification` / `signifier_vs_affordance_misuse` / `accessibility_blockers` / `iconic_object_analogy` / `anti_patterns_hit` / `out_of_circle_flags`
- Linus 阶段 1: `data_structure_risks` / `special_case_pressure` / `anti_patterns_hit` / `interface_risks` / `out_of_scope_for_strategy`
- Linus 阶段 2: `broken_evidence` / `must_haves_coverage_detail` / `refactor_prerequisites` / `risk_notes` / `out_of_scope_for_strategy`
<!-- GENERATED:verdict_schema_seat_specific:end -->

## route 映射规则

本表只列 native verdict → route 的通用映射。条件路由由 manifest 的 `conditional_routes` 声明并投影到席位输出契约：`mode: add` 追加可选路由，`mode: override` 命中时替代原生允许范围。覆盖条件不能被之后的追加规则放宽；多个覆盖条件冲突时拒绝放行。JSON Schema 同步强制覆盖条件，完整路由与跨字段校验由共享校验器执行。

<!-- GENERATED:verdict_schema_route_rules:start -->
| 席位 | native | → `core.route` |
|---|---|---|
| Taleb | `fragile` | `go_with_conditions` / `revise_must_haves` / `kill` |
| Taleb | `robust` | `go` |
| Taleb | `antifragile` | `go` |
| Munger | `keep` | `go` / `go_with_conditions` |
| Munger | `kill` | `kill` |
| Munger | `too_hard` | `too_hard` |
| López | `scientific` | `go` |
| López | `associational` | `go_with_conditions` |
| López | `pseudo_scientific` | `kill` / `revise_must_haves` |
| Feynman | `clear` | `go` |
| Feynman | `muddy` | `go_with_conditions` / `revise_must_haves` |
| Feynman | `cargo_cult` | `revise_must_haves` / `kill` |
| Paul Graham | `sane` | `go` |
| Paul Graham | `needs_pivot` | `go_with_conditions` / `revise_must_haves` |
| Paul Graham | `manager_drift` | `revise_must_haves` / `kill` |
| Paul Graham | `not_my_circle` | `too_hard` |
| Norman | `usable` | `go` |
| Norman | `confused_users` | `go_with_conditions` / `revise_must_haves` |
| Norman | `blames_users` | `revise_must_haves` / `kill` |
| Norman | `not_my_circle` | `too_hard` |
| Linus | `sane` | `go` |
| Linus | `broken` | `kill` |
| Linus | `needs_refactor_first` | `revise_must_haves` / `go_with_conditions` |
<!-- GENERATED:verdict_schema_route_rules:end -->

## 阶段 4 例外

<!-- GENERATED:verdict_schema_phase_4_exception:start -->
`linus_execution` 是实施验证状态输出，不走共同 verdict schema。它保留自己的字段结构：`phase` / `status` / `decisions_honored` / `out_of_scope_touched` / `verification_attempted` / `self_audit` / `commit_status` / `gaps_to_route_back`。
<!-- GENERATED:verdict_schema_phase_4_exception:end -->
