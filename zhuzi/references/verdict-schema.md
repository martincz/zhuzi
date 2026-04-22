# Shared Verdict Schema

> 这是 `/zhuzi:roundtable` 所有席位共享的 YAML verdict 契约权威源。若 `roundtable.md`、agent 示例段或 README 的说法漂移，以本文件为准。

## 层级结构

所有席位（Taleb / Munger / López / Linus / 未来扩展）在 verdict 阶段统一输出四层：

- `core`
- `must_haves_review`
- `must_haves_challenge`
- `seat_specific`

## `core`

| 字段 | 取值 | 作用 |
|---|---|---|
| `seat` | `taleb` / `munger` / `lopezdeprado` / `linus` / 新席位 | 席位标识 |
| `phase` | `1` / `2` / `4` | 当前阶段 |
| `route` | `go` / `go_with_conditions` / `revise_must_haves` / `kill` / `too_hard` | 主持人机读统一路由空间 |
| `seat_native_verdict` | 各席位原生 verdict | 保留人物 DNA |
| `confidence` | `low` / `medium` / `high` | 信心 |
| `hard_blockers` | `[]` | 转 `go` 的必要条件 |
| `peer_disagreements` | `[{peer, point}]` | 跨席位分歧，主持人阶段 3 直接呈现 |

## `must_haves_review`

统一 flag 空间：

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

- Taleb: `tail_events_breaking_must_haves` / `fragility_checklist_failures` / `skin_in_the_game`
- Munger: `anti_patterns_hit` / `lollapalooza_stack` / `circle_of_competence` / `reverse_kill_path`
- López: `claim_classification` / `causal_graph_missing` / `trial_count_disclosed` / `integrity_checklist_failures` / `anti_pattern_hits` / `workflow_diagnosis` / `domain_limit_flag`
- Linus 阶段 2: `broken_evidence` / `must_haves_coverage_detail` / `refactor_prerequisites` / `risk_notes` / `out_of_scope_for_strategy`

## route 映射规则

| 席位 | native | → `core.route` |
|---|---|---|
| Taleb | `fragile` | `go_with_conditions` / `revise_must_haves` / `kill` |
| Taleb | `robust` / `antifragile` | `go` |
| Munger | `keep` | `go` |
| Munger | `kill` | `kill` |
| Munger | `too_hard` | `too_hard` |
| López | `scientific` | `go` |
| López | `associational` | `go_with_conditions` |
| López | `pseudo_scientific` | `kill` / `revise_must_haves` |
| López | `domain_limit_flag` 非空 | `too_hard` |
| Linus | `sane` | `go` |
| Linus | `broken` | `kill` |
| Linus | `needs_refactor_first` | `revise_must_haves` / `go_with_conditions` |

## 阶段 4 例外

`linus_execution` 是实施验证状态输出，不走共同 verdict schema。它保留自己的字段结构：`status` / `decisions_honored` / `verification_attempted` / `self_audit` / `commit_status` / `gaps_to_route_back`。

## 新增席位维护清单

1. 为需要支持的 runtime 新建对应 agent adapter，并定义 `<seat>_verdict` root key。
2. 在 agent 示例段里填齐 `core` / `must_haves_review` / `must_haves_challenge` / `seat_specific`。
3. 更新 `zhuzi/references/seat-registry.md`。
4. 更新本文件的 route 映射规则和 seat-specific 字段说明。
5. 更新 `docs/INVENTORY.md` 与 `tools/check_consistency.py` 的覆盖面。
