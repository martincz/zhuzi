# Shared Verdict Schema

> 这是 `/zhuzi:roundtable` 所有席位共享的 YAML verdict 契约人读权威源。route 映射、seat-specific 注册和 Quick/seat/stages 机器合同以 `zhuzi/manifests/roundtable-contract.json` 为准；若 `roundtable.md`、agent 示例段或 README 漂移，以 manifest 与本文件交叉校验结果为准。

## 层级结构

所有席位（Taleb / Munger / López / Linus / 未来扩展）在 verdict 阶段统一输出四层：

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
| `phase` | `1` / `2` / `4` | 当前阶段 |
| `route` | `go` / `go_with_conditions` / `revise_must_haves` / `kill` / `too_hard` | 主持人机读统一路由空间 |
| `seat_native_verdict` | 各席位原生 verdict | 保留人物 DNA |
| `confidence` | `low` / `medium` / `high` | 信心 |
| `hard_blockers` | `[]` | 转 `go` 的必要条件 |
| `peer_disagreements` | `[{peer, point}]` | 跨席位分歧，主持人阶段 3 直接呈现 |
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

每条 `must_haves.truth` 都必须单独给一条 review 记录。即使 `flag: none` 也不得省略该 truth。

## `must_haves_challenge`

```yaml
must_haves_challenge:
  triggered: yes | no
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

任一席位 `triggered: yes`，阶段 1.5 must_haves 修订 gate 必触发。orchestrator 不得忽略。

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

本表只列 native verdict → route 的通用映射。特殊条件 route（例：López `domain_limit_flag` 非空 → `too_hard`）由各席位在自己的 `## 输出契约` 段定义，不收入此表。

<!-- GENERATED:verdict_schema_route_rules:start -->
| 席位 | native | → `core.route` |
|---|---|---|
| Taleb | `fragile` | `go_with_conditions` / `revise_must_haves` / `kill` |
| Taleb | `robust` | `go` |
| Taleb | `antifragile` | `go` |
| Munger | `keep` | `go` |
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

## 新增席位维护清单

1. 先新建共享 seat contract：`zhuzi/seats/<name>-reviewer.md`（或 `-engineer.md`），手写职责、越权边界与纪律，并保留 `## 输出契约` 生成块 marker。
2. 更新 `zhuzi/manifests/roundtable-contract.json`，把 root key、native verdict、route 映射、seat-specific 注册、Quick/stages 与 seat 输出契约机器合同补齐。
3. 运行 `python3 tools/render_roundtable_contract_docs.py`，刷新本文件、`seat-registry.md` 与 seat 文件里的 `## 输出契约` 生成段。
4. 再让 runtime adapter 只引用 skill + shared seat contract + shared schema，不在 wrapper 里复制完整 schema 示例。
5. 更新 `docs/INVENTORY.md` 与 `zhuzi/manifests/shipped-surface.json`；`tools/check_consistency.py` 与 smoke test 已从 manifest / 文件树动态派生，扩席位时不应再手改脚本。
