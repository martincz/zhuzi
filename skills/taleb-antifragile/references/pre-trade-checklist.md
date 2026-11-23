# Pre-Trade Fragility Check · 10 步策略/决策审视清单

> Taleb "avoid ruin" 方法论的 10 步策略/决策脆弱性审视清单（入口见 [SKILL.md](../SKILL.md)）。
> **先验分布与结构分类——fragility 三态和分布 class 判错，后续参数微调均无意义**。
>
> 对标 Munger 的 `pre-trade-checklist.md`（10 步）——但 Taleb 视角的 10 步**更激进地对待尾部**：
> - Munger 说"列 kill-path"，Taleb 说"你的 payoff 结构凸还是凹"（结构决定命运，清单治标）
> - Munger 说"Kelly × 0.25"，Taleb 说"Kelly × 0.15 + absorbing barrier check"
> - Munger 说"能力圈外扔 Too Hard"，Taleb 说"承认 Mediocristan 工具在 Extremistan 里是 class error"

---

## 使用方法

收到一个策略 / 交易 / 投资决策时，按 1→10 顺序走。每步问题**答得上**"这样做是对的因为 X" → 继续下一步。答不上就停。

**不要并行检查**。前面答不上，后面无意义。

**结构层（Step 1-5）** 审视策略本身的 fragility。
**决策层（Step 6-10）** 审视你的 process 的 fragility。

---

## Step 1: Fragility 三态路由

> "The fragile wants tranquility, the antifragile grows from disorder, and the robust doesn't care too much." — *Antifragile* Prologue

**要问的问题**：
- 这策略对 volatility **是 fragile / robust / antifragile**？
- 波动率上升时，策略收益怎么变？
  - **Fragile**：收益下降（典型 long-only equity，short vol 策略）
  - **Robust**：收益不变（市场中性、无 vol exposure）
  - **Antifragile**：收益上升（long vol、option long、反转因子）
- 用 **Triad 画图**：把策略对 vol 的反应画成函数——向下弯（凹 / fragile）、直线（robust）、向上弯（凸 / antifragile）

**坏信号**：
- 答"这策略不受 vol 影响"——99% 情况这是错的（所有 equity 策略都有 vol exposure）
- 答"attacks and fragile 看情况"——这是不承认二元分类
- 承认 fragile 但试图用"高 Sharpe"辩护——Sharpe 不是答案，payoff 结构才是

**好信号**：
- 能**明确画出 triad 位置**
- 承认 long-only equity 结构上是 fragile——然后讨论如何在**仓位层**注入 robust 或 antifragile 行为
- 能说出"什么 vol 水平下这策略会 blow up"

**修复方向**：
- Long-only 天然 fragile → 不是错，但要**承认**；不要装成 antifragile
- 在仓位层注入 antifragile：drawdown-reactive 加仓规则（有硬 cap）、barbell 组合（80% 核心 + 20% 凸性卫星）
- 详见 `quant-trading-playbook.md` 第二章

---

## Step 2: Payoff 凸性审视

> "Convexity means that the second derivative is positive. A convex response curve means the response to a stressor accelerates." — *Antifragile* Ch. 18

**要问的问题**：
- 画出策略的 **payoff 曲线**——x 轴是 underlying stress（市场下跌幅度、volatility、regime shift），y 轴是策略 PnL
- 这曲线 **凸（向上弯）还是凹（向下弯）**？
- 上行和下行**对称**还是**不对称**？
- Jensen 不等式：$E[f(X)] ≥ f(E[X])$ 当 f 凸时——你的策略利用了这个吗？

**坏信号**：
- 画不出 payoff 曲线——说明不理解自己的策略
- 曲线是凹的（capped upside + unbounded downside）——典型 short vol
- 上行和下行对称——robust，不会 blow up 但也不会受益于 shock

**好信号**：
- 凸 payoff（上行加速、下行有限）——这是 antifragile 的数学定义
- 承认凹 payoff 的存在并**在仓位层补偿**

**修复方向**：
- 纯 long-only 无法真正 convex（没有 option）——接受这点
- 在 long-only 框架内**局部 convex** 的做法：
  - 持有高波动小盘股的**小仓位**（upside 非线性，downside 限于小仓位 cap）
  - Barbell 的**凸性端**（卫星仓位）
  - **反转因子**（跌越多反弹越大——payoff 凸）
  - **波动率越高越有效的因子**（跟 implied vol 同向）

---

## Step 3: 分布 Class 判断

> "In Mediocristan, exceptions occur but don't carry large consequences. In Extremistan, exceptions can be everything." — *Black Swan* Ch. 3

**要问的问题**：
- 这策略在的市场是 **Mediocristan 还是 Extremistan**？
- 用 **kurtosis + skewness + tail exponent α** 判断（不是用"感觉"）：
  - kurtosis < 3 → Mediocristan（正态 kurtosis = 3）
  - kurtosis 3-10 → 偏向 Extremistan
  - kurtosis > 10 → 毫无疑问 Extremistan
  - tail exponent α ≤ 2 → **variance 无穷**，停用 σ 相关指标
- 我用的评估工具（Sharpe、VaR、mean、σ）和分布 class 匹配吗？

**坏信号**：
- 没算过 kurtosis——你在概率 theater
- 算过 kurtosis > 10 但继续用 Sharpe——class error
- "所有分布都假设 Gaussian，业界标准"——业界标准在 1998 LTCM、2008 MBS、2020 COVID 都塌过

**好信号**：
- 明确报告 kurtosis、skewness、tail exponent
- 在 Extremistan 下切换工具：CVaR_5%、drawdown distribution、EVT 拟合、log-log plot
- 承认 Sharpe 只是 Mediocristan 工具的一个参考

**修复方向**：
- A 股日收益率毫无疑问是 Extremistan（2015/2018/2020/2022/2024-10/2026-03-23 系列事件）
- 策略评估报告必须包含：kurtosis、skewness、CVaR_5%（不只 Sharpe）
- 详见 `quant-trading-playbook.md` 第一章

---

## Step 4: Turkey 检查（历史覆盖）

> "The turkey's experience may have, rather than no value, a negative value. Its confidence increased as the number of friendly feedings grew." — *Black Swan* Ch. 4

**要问的问题**：
- 我的回测样本**覆盖了几次 tail event**？
- 起点在哪？是**牛市底部**（turkey 视角）还是**近一次 tail event 的顶部**？
- mandatory tail event list（A 股）：2007-2008 / **2015** / 2016 熔断 / **2018 贸易战** / **2020 COVID** / **2022 俄乌 + 上海封控** / **2024-10 以伊** / **2026-03-23** — 至少覆盖 3 个
- 回测结束在**平稳期**还是**真 tail event 后**？

**坏信号**：
- 回测起点 2017-2018（跳过 2015 股灾）
- 回测覆盖 0-2 个 tail event
- 结论基于"过去 10 年年化 X%"——N = 10 在 Extremistan 里是 woefully insufficient

**好信号**：
- 起点明确选在 tail event 顶部（2015-06 / 2021-02 抱团顶）
- 覆盖 ≥3 个 tail event
- 附 "tail event coverage table"

**修复方向**：
- 回测起点规则：**从最近一次 tail event 的顶部**开始
- 建立 mandatory tail event list，每次回测附 coverage table
- 验收标准增加 **"per-tail-event catastrophic check"**——任一 event 窗口 drawdown < -15% 或 alpha < -5% 触发警告

---

## Step 5: Kill-Path via Negativa 分析

> "All I want to know is where I'm going to die, so I'll never go there." — （这是 Jacobi / Munger 的话，Taleb 版本更尖锐）
> "Knowledge grows by subtraction much more than by addition." — *Antifragile* Prologue

**要问的问题**：想象 1 年后策略彻底失败，**最可能的原因**：

- 这策略怎么让我**破产**？（不是亏 20%，是亏到不能继续）
- 什么市场条件让 edge **彻底消失**？（regime shift、流动性冻结、相关性全到 1）
- 什么意外让我**一天亏 20%+**？（tail event、黑天鹅）
- 谁会在什么情况下**反向交易我**？（对手的极端行为）

**典型 Kill-path 清单（A 股 long-only 量化）**：

1. **因子 crowded trade**（同类策略规模过大，同时出逃）——2007 美国 quant quake 的 A 股版
2. **流动性枯竭**（小盘股、ST、北交所在危机时 0 成交）
3. **监管变化**（印花税上调、做空限制、外资流动限制、个股停牌潮）
4. **数据供应商出错**（未发现的数据质量问题导致系统性错误信号）
5. **模型假设失效**（"波动率均值回归"在 2020-03 完全失效）
6. **对手消失**（游资在危机时集体消失，fill 价格恶化）
7. **行业政策突变**（K12 教培、房地产、互联网平台监管的"一夜之间"）
8. **系统故障**（极端情况下无法平仓）
9. **A 股特有的机制性风险**（涨跌停触发 → T+1 无法止损 → 次日开盘惯性下挫 → 连续跌停）

**坏信号**：
- 答不出 kill-path（没想过）
- Kill-path 在策略逻辑里没防御
- "这种情况罕见"——罕见 ≠ 不会发生。tail 的频率被系统性低估

**好信号**：
- 能列 ≥5 个具体 kill-path
- 每个有对应风控规则（止损、对冲、降仓）
- 最危险的 kill-path 有"提前退出"机制

**修复方向**：
- 对每个 kill-path，量化最坏情况的亏损金额
- 总 kill-path 风险 > 心理承受能力 → 降仓到可承受水平
- "我不知道所有 kill-path" → 这本身是最大的 kill-path，策略还没成熟

---

## Step 6: Skin in the Game 自检

> "Skin in the game means that you do not pay attention to what people say, only to what they do." — *Skin in the Game* Prologue

**要问的问题**：
- 我在这策略里的**自有资金**占我年收入的多少%？
  - < 1% → 象征性 skin，不算
  - 1-10% → 有点 skin
  - > 10% → 真 skin
- 策略亏 30%，我**今晚睡不着**吗？
- 我会把**父母的养老金**放进去吗？
- 如果这策略是**给别人做**，我会用同样的仓位配置给自己吗？

**坏信号**：
- 自己的钱 = 0（为别人做研究）
- 亏 30% 不会影响生活
- "我觉得这策略不错但我不会自己用"——致命信号

**好信号**：
- 自己的钱在策略里的比例 > 10% 年收入
- 敢把给自己的仓位配置复制给父母
- 策略爆仓会**真的**影响自己生活

**修复方向**：
- 如果自己无 skin → 降低策略信心度；用 Kelly × 0.1 或更低
- 团队化情况下：研究员 bonus 递延 ≥ 2 年，drawdown > X% 触发 clawback
- 对每个策略建议问"父母养老金 test"：我会推荐给父母吗？

---

## Step 7: Ergodicity 诊断

> "A process is ergodic if ensemble average = time average." — "The Logic of Risk Taking"

**要问的问题**：
- 我报告的是**集合均值**还是**时间均值**？
- 中位数路径的年化是多少？最差 5% 路径的年化是多少？
- 这个策略有**absorbing barrier** 吗？（破产、强平、强制清盘）
- 如果我跑这策略 10 年，**破产概率**多少？

**坏信号**：
- 只报告"年化 X%"——这通常是集合均值
- 不区分中位数路径 vs 均值路径
- 没有破产概率估计

**好信号**：
- 报告 **final NAV distribution**（不只均值/CI）
- 标注"最差 5% 路径终值"——如果 5% path < 初始资金的 30%，破产信号
- 附 **10 年破产概率估计**（基于路径而非均值）

**修复方向**：
- Bootstrap 报告模板加 final NAV distribution
- 决策基于**中位数或更保守的百分位**，不是均值
- 详见 `quant-trading-playbook.md` 第五章

---

## Step 8: Lindy 门槛（新因子 / 新技术）

> "For the nonperishable, every additional day may imply a longer life expectancy." — *Antifragile* Ch. 20

**要问的问题**：
- 这策略 / 因子的**学术首次发现年份**是什么？
- 按 Lindy age 分层：
  - > 30 年（Graham 价值、Haugen 低波、Jegadeesh-Titman 动量）→ Lindy 高信心
  - 10-30 年（FF 三因子、Banz 规模、Grinold-Kahn 信息比率）→ Lindy 中信心
  - < 10 年（ML-derived、另类数据、社交媒体情绪、2020+ 论文因子）→ Lindy 低信心，证据阈值 × 3
  - 纯 data mining（无经济学机制） → 拒绝

**坏信号**：
- 因子来自 2020+ 的 ML 论文——Lindy 低，但当作高信心
- "这因子最近 3 年 IC 0.08"——3 年 = turkey 视角的 3 天
- 没法说出因子的经济学机制（为什么市场给 edge）

**好信号**：
- Lindy 因子总权重 ≥ 80%
- Non-Lindy 因子总权重 ≤ 20%，单一 ≤ 5%
- 新因子有明确经济学机制 + ≥3 regime 验证 + 失效机制假设

**修复方向**：
- 新因子 admission：先过经济学机制 → paired replay → ≥3 regime 验证 → 小仓位测试
- 阅读清单优先 1970s-2000s 经典
- 对 A 股打折扣：A 股本身年轻（1990-），学术 Lindy 年限要缩放

---

## Step 9: Kelly × 0.15 硬帽

> "If a single entity has a zero in its payoff, it has skin in the game in the ergodic sense. The 'average' is not a useful summary for nonergodic systems." — Peters + Taleb 2019

**要问的问题**：
- 计算理论 Kelly（基于历史 edge 和 volatility）
- 实际仓位 ≤ **full Kelly × 0.15**——比 Munger 推荐的 × 0.25 更保守
- 理由：Kelly 理论假设无限独立赌局，你是单人；厚尾下估计的 edge 不可信
- 单一策略仓位上限 = 总资本的 30%（多策略分散）
- **杠杆**：默认 0；如果必须用，限制 1.2x 以内，且只在能力圈内高确信度机会

**坏信号**：
- 全 Kelly 仓位（"理论最优"）
- 单一策略 > 50% 总资本
- 用杠杆追逐近期赢家 / 补救失败仓位

**好信号**：
- Kelly × 0.15 基础 + 根据 skin / 能力圈信心微调（但上限 × 0.25）
- 无杠杆默认
- 风控规则硬约束（触发后自动执行）

**修复方向**：
- 仓位过大 → 砍半，再砍半
- 记住：**Leverage + bad luck + time = bankruptcy**。不是概率，是数学必然

---

## Step 10: "Do Nothing" 测试

> "Action bias is the source of most bureaucratic evil." — Taleb (推演 from *Antifragile* Via Negativa 章)

**要问的问题**：
- 如果我**什么都不做**（不交易 / 不改策略 / 保持现金），结果会显著变差吗？
- 我做这个决策是因为**机会真的稀缺**，还是因为**我需要做事**（action bias）？
- 行动 vs 不行动的**信息价值**对比是什么？

**坏信号**：
- 答"不做会少赚"——但"少赚"不是"亏"，机会成本和实际损失要区分
- 交易冲动来自"已经分析了这么久总得做点什么"（沉没成本）
- 上次决策离现在很近——可能在**过度活跃**

**好信号**：
- 答案清晰："不做会错过 clearly mispriced 的机会"
- 能接受不做并等待更好的机会
- 交易频率低于同行（通常是好信号）

**修复方向**：
- 模糊 → 不做
- Via negativa 是最被低估的策略——**删除 / 不做** 优先于**添加 / 做**
- 记住：**The big money is in the waiting, not the trading**（这是 Munger 的话，Taleb 版本：**Sit on your hands and let convexity do the work**）

---

## 元原则

**10 步全过一遍的时间**：5-15 分钟。觉得"太长"——你正在受 action bias 驱动。多花 15 分钟避免一次破产，回报率无穷大。

**任意一步答不上 → 停**。不是"跳过"，不是"先做再补"，是**停**。

**多于一步答不上 → 这不是你的交易**。降到"不做"筐，等你能答上再回来。

**每次真金白银决策前过一遍这 10 步**。把它写成 checklist，打勾。飞行员起飞前过 checklist 不是因为不懂飞行，是因为懂代价。

---

## 与 Munger 的 10 步 checklist 对比

| Step | Munger 版本 | **Taleb 版本** | 差异 |
|---|---|---|---|
| 1 | Edge 的经济学解释 | **Fragility 三态路由** | Munger 问"edge"；Taleb 问"结构"——fragile 结构无 edge 都救不了 |
| 2 | 样本外验证 | **Payoff 凸性审视** | Munger 问"样本外 work 吗"；Taleb 问"结构是否有利于尾部" |
| 3 | 逆向 kill-path | **分布 class 判断** | 不同层——Munger 直接 kill-path，Taleb 先确认工具匹配 |
| 4 | 交易成本与容量 | **Turkey 检查** | 重心不同——Munger 看成本，Taleb 看历史覆盖 |
| 5 | 最大回撤路径 | **Kill-path via negativa** | 相似，Taleb 更激进地想"破产路径"而非"回撤" |
| 6 | 能力圈 | **Skin in the game 自检** | Munger 问"懂吗"，Taleb 问"赔得起吗" |
| 7 | Lollapalooza 扫描 | **Ergodicity 诊断** | 完全不同——Munger 认知偏误，Taleb 单人路径破产概率 |
| 8 | 反确认 | **Lindy 门槛** | 不同——Munger 主动找反方，Taleb 用时间作筛选器 |
| 9 | 安全边际 / Kelly × 0.25 | **Kelly × 0.15 硬帽** | Taleb 更保守 |
| 10 | "Nothing to add" | **"Do Nothing" 测试** | 几乎相同——都是 action bias 刹车 |

**结合使用**：量化场景下可以把两套 checklist 做**cross-reference**——某步在 Munger 答得上、在 Taleb 答不上（或反之）都是信号。通常：
- Munger 查认知 / 激励 / 能力圈
- Taleb 查分布 / 尾部 / 凸性
- 两者互补不重复

---

> "The difference between a winning organization and a losing one is that the winner has a checklist for the things that can kill it, and uses it."
> —— 这个版本是 Taleb 式的——**checklist 不是让你聪明，是让你不破产**。
