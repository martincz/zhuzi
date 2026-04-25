# Roundtable 示例 · 阶段 1.5 修订 gate 触发

> 展示 roundtable 的核心价值：**席位有权推翻刚刚锁定的 must_haves**。这是让一份"听起来对"的 must_haves 在实施前被卡住的协议机制。

输入：

```text
/zhuzi:roundtable 我在权重搜索里试了 17 种组合，第 12 种回测 walpha +1.8% Sharpe 1.4 显著 vs baseline，建议上线
```

阶段 0.5 用户确认后的 must_haves（v1）：

```yaml
must_haves:
  truths:
    - "组合 12 在 baseline 上 walpha Δ ≥ 1%"
    - "组合 12 Sharpe ≥ 1.0"
    - "p-value < 0.05"
```

---

## 阶段 1 席位短评（截取）

| 席位 | 结论 | 最大风险 | 必须满足 | 分歧 | 信心 |
|---|---|---|---|---|---|
| López | 改 must_haves | 见下方展开 | 见下方展开 | 与 Munger 部分一致 | high · 本席位 core 领域 |
| Munger | 改 must_haves | 见下方展开 | 见下方展开 | 与 López 部分一致 | high · selection bias 是清单第 3 条 |

### López 展开

**最大风险**：
- `selection bias`（试 N 次后挑最好的 1 个，p < 0.05 在 N=17 下几乎必然命中）· 17 次 trial 下，5% 显著性水平的 false positive 率约 58%
- `Deflated Sharpe`（试 N 次后要对观察到的 Sharpe 打折才算真显著）· 未做 deflation 的 Sharpe 1.4 在 N=17 下接近无显著
- `PBO`（probability of backtest overfitting，CSCV 跨验证下方法论是否还有效）· 未披露

**must_haves_challenge.triggered: yes** —— v1 的 truths 把"挑选过的指标"当成"独立指标"，方法论根本错。

### Munger 展开

**最大风险**：
- `selection bias`（清单第 3 条）· 17 选 1 是经典 cherry pick
- `deprival super-reaction`（用户已经爱上"组合 12 看起来真好"）

**must_haves_challenge.triggered: yes** —— v1 没要求披露 trial 数和 selection 程序。

---

## 阶段 1.5 修订对照表

| # | v1（旧） | v2（新） | 来源 | 根因 |
|---|---|---|---|---|
| 1 | walpha Δ ≥ 1% | DSR_lower_bound > 0 + walpha Δ ≥ 1% | López | Sharpe 必须经 trial 数 deflate 才算显著 |
| 2 | Sharpe ≥ 1.0 | PBO < 0.5（CSCV 验证） | López | 单个 backtest Sharpe 不抗 selection；要看 OOS 稳定性 |
| 3 | p-value < 0.05 | walk-forward CV 5 折下 4/5 折 OOS walpha 同向 | López + Munger | p-value 在 17 次 trial 下不是有效证据 |
| 4 | （新增） | 公开披露：本次实验的 trial 数 = 17，选 1 留 16 | López + Munger | 不披露 selection process 的回测不是 evidence |

### Truth 1 展开

**Deflated Sharpe Ratio**（DSR）= 试 N 次后，对观察 Sharpe 打折，得到调整后的"真显著性下界"。

例：N=17 实验中观察 Sharpe 1.4，DSR 下界约为 0.7-0.9（取决于 backtest 长度和实验自相关）。要求 `DSR_lower_bound > 0` 等于"哪怕考虑了 selection，仍有非零超额"。

### Truth 2 展开

**PBO**（Probability of Backtest Overfitting）= 用 CSCV（Combinatorially Symmetric Cross Validation）切分回测，看"在 IS 段排第一的组合在 OOS 段排第几"的分布。PBO < 0.5 = OOS 性能比 random 好。

---

## 用户五选一

- **接受 v2** ✓
- 接受部分（指定哪些 truth 采纳）
- 保持 v1
- 重开议题
- 要求 orchestrator 改写 v2 表达

**用户选择**：接受 v2

---

## 阶段 2 · 用 v2 must_haves 进可行性评审

`linus-engineer` 收到的 must_haves 是 v2 版本——他在阶段 4 实施时跑的 verify_commands 也变了：

```yaml
verify_commands:
  - truth: 1
    cmd: "python3 tools/dsr.py --trials 17 --observed-sharpe 1.4"
    pass_criterion: "DSR_lower_bound > 0"
  - truth: 2
    cmd: "python3 tools/cscv.py --splits 16"
    pass_criterion: "PBO < 0.5"
  - truth: 3
    cmd: "python3 tools/walk_forward.py --folds 5"
    pass_criterion: "OOS walpha 同向 ≥ 4/5"
  - truth: 4
    cmd: "grep -E 'trial_count: 17' EXPERIMENT.md"
    pass_criterion: "披露文件存在且 trial_count == 17"
```

---

## 协议笔记

这个例子的价值在于：**议题进 roundtable 时 must_haves 看起来"科学"（有 walpha 阈值 + Sharpe + p-value），但席位审议后发现整个 must_haves 框架在方法论层就塌了**。如果没有阶段 1.5 修订 gate，议题会带着"挑过的指标"走完阶段 4 的 verify——`grep walpha > 1%` 通过，但实际产品上线后 OOS 失效，是**协议级的错误**。

阶段 1.5 把"席位推翻刚拍板的契约"从临场补 gate 升格成协议内置流程——这是 roundtable 区别于普通"几个 LLM 投票"的关键。
