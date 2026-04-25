# Quick Multi-Perspective 示例

输入：

```text
/zhuzi:quick 我在考虑把现在的单体后端拆成 3 个微服务，团队就 2 个人。
```

默认输出形态：

---

# Quick Multi-Perspective: 2 人团队拆 3 个微服务

> 3 视角短读 · 不做综合 · 拍板请走 `/zhuzi:roundtable`

## Linus（linus-engineer）

Broken。两个人维护三个服务的部署、监控、版本依赖、跨服务调试，等于把一个会出 bug 的进程内调用换成三个会出 bug 的网络调用——你没有解决问题，只是把它搬到更难调试的地方。微服务在团队大到单仓库 merge 冲突无法承受时才有意义；2 人团队的 merge 冲突是 0。先问的是"现在哪个具体痛点拆了能消失"，而不是"是不是该拆了"。

## Munger（munger-reviewer）

Reverse it。如果三年后你回头看，最容易后悔的不是"没拆早一点"，而是"拆早了但人手不够维护"。机会成本是显性的：维护跨服务调用的时间从产品迭代里扣。激励层面要警惕——简历驱动的架构选型是常见 Lollapalooza（社交认同 + 跟风 + 自利）。能力圈检查：你们维护过分布式追踪和跨服务事务吗？没有就是圈外。

## Taleb（taleb-reviewer）

Fragile。单体出问题你看一份日志；3 个微服务出问题你看 3 份日志加一张调用图，failure mode 从加法变成乘法。2 人团队对每个服务的关注度被稀释到 1/3，bus factor 从 2 变成"每个服务 0.67 个人"——任意一人请假，至少一个服务进半失明。如果一定要拆，先做 barbell：核心稳态留单体，边缘高变异区出一个独立服务做实验，不要三刀切。

## 一句话对照

| 席位 | 一句话结论 |
|---|---|
| Linus | Broken——你只是把进程内 bug 搬到网络上，没有解决任何问题 |
| Munger | Reverse it——3 年后最容易后悔的是拆早了，不是拆晚了 |
| Taleb | Fragile——failure mode 从加法变乘法，bus factor 从 2 变 0.67 |

## 下一步建议

- 想拍板（出决策表 + 验证信号）→ `/zhuzi:roundtable 我在考虑把现在的单体后端拆成 3 个微服务，团队就 2 个人`
- 想深聊某个视角 → `用 Linus 视角看这个` / `用 Taleb 视角分析 fragility` / `#munger`
