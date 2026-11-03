# Roundtable 示例 · 代码层 broken 否决

> 以下为文档内的假设 fixture，不是本仓库存在的后台服务。只展示相关代码席阶段，不冒充完整召开记录。

输入：

```text
/zhuzi:roundtable worker.py 用共享锁防止同一任务同时执行；锁租期 30 秒，任务可运行 90 秒，无续期。该方案能否保证互斥？
```

本例提供的 worker.py 行为：实例 A 在 t=0 获锁开始任务，租期在 t=30 结束；实例 B 可在 t=31 获锁并开始相同任务，而 A 直到 t=90 才结束。

锁定的 truth：同一任务的执行临界区不重叠。

## 阶段 2 · Linus verdict

```yaml
linus_feasibility:
  core:
    seat: linus
    phase: 2
    seat_native_verdict: broken
    route: kill
    confidence: high
    hard_blockers:
      - "30 秒租期短于 90 秒任务，过期后第二实例可进入临界区"
    peer_disagreements: []
    evidence:
      - claim: "t=31 到 t=90 可重叠执行"
        source: "本例提供的 worker.py 行为与时间线"
        kind: provided
    missing_evidence: []
  must_haves_review:
    - truth: 1
      flag: coverage_gap
      note: "现有租期行为不满足互斥"
  must_haves_challenge:
    triggered: false
    challenged_truths: []
    fundamental_issue: ""
    proposed_revision: []
  seat_specific:
    broken_evidence:
      - file: worker.py
        symbol: run_with_lock
        reason: "给定时间线允许锁过期后重复执行"
    must_haves_coverage_detail:
      - "truth 1 不成立，需修正实现后重验"
    refactor_prerequisites: []
    risk_notes:
      - "仅加长租期不能证明所有故障情况下都互斥，替代实现须按明确的故障模型验证"
    out_of_scope_for_strategy: []
```

## 主持人处理

否决当前实现。这里的 broken 有可复核的重叠执行证据，不依赖“我们现在只部署了一个实例”或“这看起来像过早抽象”等品味判断。

把否决与证据保留在短评中，回到相关席位检查是否有满足同一 truth 的等价路径。用户可以选择修正实现、明确降低保证范围或放弃；主持人不把工程否决扩展成其他领域的最终裁决。

**验证信号**：替代实现按明确的租约、任务时长和故障条件验证临界区不重叠。本例没有提供或运行替代实现，所以不报告验证通过。
