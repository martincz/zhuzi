# Roundtable 示例 · Linus 阶段 2 broken 单边否决

> 展示 roundtable 的核心价值：**代码层 broken 可以单边否决**——非代码评议席位说 keep 也不能压过工程层的"现在做就是 premature abstraction"。

输入：

```text
/zhuzi:roundtable 在现有的 cron + 单进程 service 里加 distributed lock，让多机部署时跨机器互斥
```

阶段 0.5 用户确认后的 must_haves（v1）：

```yaml
must_haves:
  truths:
    - "多机部署时 cron job 不会被同一时间在两台机器上同时跑"
    - "lock 获取失败时进程优雅退出，不留半成品状态"
  out_of_scope:
    - "不重写 cron 调度框架"
    - "不引入 K8s leader election"
```

---

## 阶段 1 席位短评

| 席位 | 结论 | 最大风险 | 必须满足 | 分歧 | 信心 |
|---|---|---|---|---|---|
| Munger | 过 | 多机互斥语义对，激励一致 | 失败模式声明清楚 | 与 Linus 阶段 2 有分歧 | medium · 与 Linus 有分歧 |

阶段 1 没有 must_haves_challenge 触发，进阶段 2。

---

## 阶段 2 · Linus 可行性评审

```yaml
linus_feasibility:
  core:
    seat: linus
    phase: 2
    seat_native_verdict: broken
    route: kill
    confidence: high
    hard_blockers:
      - "当前部署只有 1 个 replica（Dockerfile 第 23 行 + docker-compose.yml service.deploy.replicas: 1）"
      - "议题假设的'多机部署'还不存在"
  must_haves_review:
    - truth: 1
      flag: coverage_gap
      note: "多机互斥的前提（多机部署）不存在"
    - truth: 2
      flag: none
  must_haves_challenge:
    triggered: no
    note: "不是 must_haves 写错了——是议题本身解决了不存在的问题"
  seat_specific:
    broken_evidence:
      - file: "Dockerfile"
        symbol: "single replica"
        reason: "部署声明只有 1 个 replica，没有多机场景"
      - file: "docker-compose.yml"
        symbol: "service.deploy.replicas: 1"
        reason: "同上"
      - file: "deploy/staging.yaml"
        symbol: "service.replicas: 1"
        reason: "staging 同样只有 1 个 replica"
    must_haves_coverage_detail:
      - "truth 1 的前提'多机部署'在当前 codebase 里**不**成立——这不是 must_haves 的问题，是议题前提的问题"
    refactor_prerequisites:
      - "如果未来真有多机部署需求，先决定是用 K8s leader election / Redis-based lock / Postgres advisory lock，再写 distributed lock；不是反过来"
    risk_notes:
      - "现在加 distributed lock 是 premature abstraction（anti-pattern #3）——为不存在的需求加抽象层"
      - "lock 实现一旦写下，未来真做多机部署时 99% 概率不匹配实际的部署平台（K8s vs ECS vs systemd），要重写"
    out_of_scope_for_strategy:
      - "本次不评判'是否需要多机部署'——这是产品决策不是工程决策"
```

---

## 阶段 3 · 综合（Linus 单边否决路径）

## 主持人结论

**议题被代码席单边否决**：当前 codebase 没有多机部署，distributed lock 解决的是不存在的问题。Munger 阶段 1 给"过"是基于"假设需求成立"的判断；Linus 阶段 2 拿到具体 codebase 看到部署只有 1 个 replica，触发代码层 `broken` 否决——这是 Linus 在 roundtable 里的单边权。**建议**：先确认是否真有多机部署需求；有 → 重开议题选具体平台；没有 → 不做。

## 席位短评

| 席位 | 结论 | 最大风险 | 必须满足 | 分歧 | 信心 |
|---|---|---|---|---|---|
| Munger | 过 | 假设的多机互斥语义对 | 失败模式声明清楚 | Linus 否决 | medium · 与 Linus 有分歧 |
| Linus | 停 | premature abstraction · 当前部署只有 1 replica | 先决定多机部署平台再谈 lock | 否决 Munger 的"过" | high · 代码席核心领域 |

## 冲突与取舍

非代码席位（Munger）基于议题假设给"过"——这是合理的；代码席位（Linus）基于 codebase 实际状态给"停"——这是 roundtable 设计的代码层单边权。两者不冲突，是不同 frame：Munger 看"如果这个事情值得做"，Linus 看"这个事情现在做不做得了"。**Linus 的否决在 roundtable 协议中具有最终效力**——议题被 kill。

## 做完会怎样

如果接受 Linus 的否决：什么都不做，省下 1-2 周开发 + 维护负担。如果用户说"我就是要先把这个做了，多机部署是 6 个月后的计划"——那议题应该重写为"为 6 个月后的多机部署做选型调研"，不是现在写一个不知道部署在哪里的 distributed lock。

**验证信号**：6 个月后真要上多机部署时，看现在写的 lock 实现是否还能用——99% 概率不能用（不匹配最终选定的部署平台）。这就是 broken 的具体含义。

## 决策表

| 分类 | 内容 | 下一步 |
|---|---|---|
| `locked` | 不做 distributed lock | 关闭议题 |
| `deferred` | 多机部署平台选型（K8s / ECS / systemd 各家的 lock 原语） | 6 个月内若真有部署需求时另开议题 |

## 下一步

议题被 Linus 单边否决，等待用户确认关闭议题。要展开 Linus 完整 broken_evidence 或 Munger 原文，说"展开原文"。

---

## 协议笔记

这个例子的价值在于：

1. **Munger 阶段 1 的判断没有错**——假设议题前提成立，多机互斥确实是合理需求；
2. **Linus 阶段 2 拿到 codebase 才发现议题前提不成立**——这是为什么阶段 2 必须读当前项目纪律和具体 codebase；
3. **broken 的单边否决权防止了一个常见 anti-pattern**——非代码评议席位看议题描述觉得合理，但实际 codebase 里这个改动是 premature abstraction。如果没有阶段 2，roundtable 会让议题进阶段 4 实施，写出一个 6 个月后必然废弃的 distributed lock。

`linus_feasibility.core.route = kill` + `seat_native_verdict = broken` 在 Quick 短评卡里强制露出，**不能藏到展开内容里**——这是 workflow 阶段 1 议事侧呈现底线的具体应用。
