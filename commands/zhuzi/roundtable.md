---
description: 圆桌会议模式——多席位协作审议（策略席 + 代码席）。席位可扩，流水线通用。
argument-hint: [议题/策略/提案/需求描述]
---

# 圆桌会议（Roundtable）

用户开启圆桌会议。**议题**：

$ARGUMENTS

---

## 流水线性质

本流水线支持 **N 席位召开（N ≥ 1）**——阶段 0.5 扫议题关键词匹配"擅长领域"列，只 spawn 有资格的席位。弃权席位不产出 YAML。无代码席位时阶段 2（代码可行性）dispatch 不触发；N=1 时流水线退化为单席位审议，这是合法状态不需特殊 exit。

## 当前席位

| 席位 | agent | 职责 | 擅长领域（议题匹配关键词） |
|---|---|---|---|
| 策略 | `taleb-reviewer` | 尾部风险、fragility、barbell、skin in the game | 量化策略 / 尾部风险 / 投资决策 / 仓位管理 / 激励结构 / skin-in-the-game / 厚尾分布 |
| 策略 | `munger-reviewer` | 愚蠢清单、认知偏误、激励结构、能力圈 | 投资决策 / 商业判断 / 认知偏误审视 / 能力圈边界 / 策略审视 / 激励结构 / Lollapalooza |
| 策略 | `lopezdeprado-reviewer` | 研究诚信、associational vs causal、backtest overfitting、DSR/PBO/CPCV、Sisyphus vs Meta-Strategy workflow | 量化研究方法论 / backtest overfitting / p-hacking / multiple testing / causal factor / specification error / Deflated Sharpe / Purged K-Fold / CPCV / Meta-Labeling / Fractional Differentiation / 研究流程诊断 / factor zoo 审视 |
| 代码 | `linus-engineer` | 架构、可行性、review、重构、实施、good taste | 代码架构 / 代码实施 / 可行性评估 / 重构 / 工程纪律 / 技术选型 / good taste 审视 |

**扩席位**：新建 `~/.claude/agents/<name>.md`，在本表加一行（填齐"擅长领域"关键词），并在阶段 1 spawn 模板按需加对应 block。不拆新 command——圆桌会议本就是开放席位的隐喻。

---

## 流水线（严格按阶段推进，禁止跳阶段）

### 阶段 0.5 — 议题契约定义（主 Claude）

spawn 任何席位**之前**，主 Claude 完成三件事，一次性呈现给用户。

#### Step 0 · 席位召开判定

扫议题关键词 + 上方"当前席位"表的"擅长领域"列 → 匹配产出召开名单（**含每席位 `stages` 在哪些阶段出场**）+ 弃权名单 + 理由。**主 Claude 主动决定，不为每次召开单独问用户**（用户在 Step 2 一起确认/override）。

输出格式：

```yaml
召开:
  - seat: <agent名>
    stages: [1]          # 该席位在哪些阶段 spawn；默认规则见下方表
    reason: "<议题命中该席位的哪些擅长领域，以及为何是这些 stages>"
弃权:
  - seat: <agent名>
    reason: "<为何不召开：议题不在此席位擅长领域；给出具体匹配失败的词>"
```

**硬约束**：
- 席位自然语言匹配 ≠ 关键词精确命中——"激励结构"和"激励设计"算同一域，主 Claude 按语义判断
- N=1 时（只 1 个席位召开）明确告知用户"本议题退化为单席位 roundtable"——这是合法状态，不需额外 exit 路径
- N=0 时（无席位匹配）停流水线，建议用户改议题描述或用非 roundtable 流程直接和主 Claude 对话

**`stages` 字段默认规则**（议题类型 → 每席位 stages 推荐值）：

| 席位 | 纯量化策略议题 | 纯代码实施议题（补选项/修 bug） | 工程决策议题（架构/选型/good taste） | 混合议题（量化策略 + 大改架构） |
|---|---|---|---|---|
| Taleb | `[1]` | 弃权 | 弃权 | `[1]` |
| Munger | `[1]` | 弃权 | 弃权 | `[1]` |
| López | `[1]` | 弃权 | 弃权 | `[1]` |
| Linus | 弃权 | `[2]` | `[1, 2]` | `[1, 2]` |

**López 席位额外召开规则**（在上表基础上细化）：议题中含"研究方法论 / backtest 审视 / 因子诚信 / causal claim / 过拟合诊断 / trial 披露 / CV 方法 / Sharpe deflation / factor zoo / specification / Sisyphus workflow"任一关键词时**必召开**，即使未命中 Taleb/Munger 的尾部 / 偏误触发词。**López 与 Taleb/Munger 高度互补但不重复**——三席可同时召开，也可单独 López 召开（例：议题是"审这篇 factor literature 的方法论"——Taleb 弃权 / Munger 弃权 / López 独呈）。

**判断"工程决策维度"的关键词**：架构 / 重构 / 技术选型 / 设计选择 / good taste / 数据结构 / 模块划分 / API 设计 / 工程规范。议题描述中含这类词 → Linus `stages` 含 `1`。

**Linus `stages=[1,2]` 时**：阶段 1 和阶段 2 分别 spawn 两次——阶段 1 做"工程视角评议题"（good taste / 数据结构合理性 / anti-pattern 扫描，**不关心当前 codebase 能否承载**），阶段 2 做"可行性 gate"（吸收阶段 1 结论 + 其他席位意见 + must_haves → 能否干净落地）。两次 spawn 的 prompt 内容不同，不是重复。阶段 1 Linus 输出沿用 `linus_feasibility` schema 但 `phase: 1`，`seat_specific.broken_evidence` 和 `must_haves_coverage_detail` 留空（那是阶段 2 才填的字段），重点填 `risk_notes`（工程视角对议题本身的 risk，不是对当前 codebase 的风险）。

#### Step 1 · must_haves 定义

基于**召开名单的视角**（不给弃权席位预留 truth），把议题翻译成可验证的成功标准：

```yaml
must_haves:
  truths:            # 3-5 条 observable outcome，议题成功时必须全部成立
    - "<例：v28 M1 在 baseline 上 paired bootstrap walpha Δ 下界 > 0>"
    - "<例：d20 hit% 不回退超 1pp>"
    - "<例：Spearman ρ 与 walpha 方向一致>"
  verify_commands:   # 每条 truth 对应的可机器执行验证命令
    - truth: 1
      cmd: "<observable_metric 示例：python3 tools/bench.py --replay-from <baseline> / curl -w '%{time_total}' <api> / du -b dist/bundle.js>"
      pass_criterion: "TBD — 待召开席位审阅"       # observable_metric：主 Claude 打 TBD，席位在 must_haves_review.proposed_criterion 填阈值
    - truth: 2
      cmd: "<policy_discipline 示例：grep -E '<pattern>' <file> / jq '.schema.fields.X.type' <json>>"
      pass_criterion: "grep 命中 ≥ 1 条且匹配 '<约定措辞>' / JSON 字段 X 存在且 type == 'Y'"   # policy_discipline：主 Claude 直接写死判断标准，不得 TBD
  out_of_scope:      # 明示本议题不覆盖什么，避免席位/Linus 跑偏
    - "<例：不动某权重表 / 不改某候选池定义 / 不触发新基准测试>"
```

**硬约束（任一违反则 must_haves 段不合格，必须重写）：**

1. **`truths` 只放可验证主张**，两类合法：
   - **observable_metric**：可观测的量化行为（例：回测 walpha Δ / API p99 latency / 内存峰值 / bundle 大小 / 编译耗时 / 错误率 / bootstrap CI）
   - **policy_discipline**：可验证的结构性 / 纪律性事实（例：某文档新增条款且含指定措辞 / 某接口字段存在且类型正确 / 某输出列带约定前缀 / 某目录结构符合规范 / 某配置开关默认值符合约定）

   两类都合法，但以下禁放 truths：
   - ❌ 实施约束（"只改 N 个文件"、"不引入新依赖"）→ 走阶段 3 DECISIONS.locked
   - ❌ 主观项（"代码写得好看"、"文档清楚"）
   - ❌ 流程要求（"跑通编译"、"跑通测试"）→ 走 out_of_scope 默认项

2. **`truths` 数量 3-5 条硬上限**——超过 5 条说明议题粒度太粗，必须拆成两个 roundtable 分别开。

3. **`pass_criterion` 按 truth 类型分写**：
   - **observable_metric truth**：主 Claude 原则上打 `TBD — 待召开席位审阅`，交席位在 `must_haves_review.proposed_criterion` 填具体阈值（如 "CI 下界 > 0.3pp"、"p99 < 200ms"、"bundle < 500KB"）。阈值是**专业判断**，应由席位给。
   - **policy_discipline truth**：主 Claude **必须直接写死**判断标准，**不得 TBD**——这类 truth 的通过条件本身就是契约内容（如 "grep 命中 ≥ 1 条且含 '禁' / '不得' 之一"、"JSON schema 含字段 X 且类型 Y"、"输出列名前缀为 `POSTMORTEM_`"），不是席位专业阈值。席位可在 `must_haves_challenge` 推翻整条，但不能被动等 orchestrator "留白让席位填"。
   - 纯技术断言（"py_compile 通过"、"HTTP 200"、"lint 无 error"）按 policy_discipline 规则，主 Claude 直接写死。

4. **`out_of_scope`** 直接喂给阶段 3 DECISIONS 表的 `deferred` 段。

5. **无法为某 truth 写出 verify 命令时**，先打 `TBD — 需要召开席位确认指标口径`——缺验证标准比议题失败更严重。

6. **`pass_criterion` 禁"程序正义式"描述**——pass_criterion 回答"什么状态算通过"，不是"谁说了算 / 怎么达成一致"。以下写法禁用：
   - ❌ "由 X 席位 endorse"
   - ❌ "所有席位共同确认"
   - ❌ "讨论后达成一致"
   - ✅ 必须含：判断维度 + 存在性条件 / 阈值 / 结构约束（可被 grep / diff / 数值比较 / schema 检验之一验证）

7. **`truths` 过席位必要性预检**——每条 truth 写完后，orchestrator 自问："此 truth 是否必须召开席位的专业视角才能评估？"
   - 若答案是"orchestrator 或代码席自己能判"（如文档记账 / 目录结构 / 单纯 grep 验证 / 记忆同步 / 配置项存在性）→ **不进 `must_haves.truths`**，改入 `DECISIONS.locked`（强制实施项）或 `DECISIONS.discretion`（实施时判断）
   - `must_haves.truths` 只放真正需要席位**专业视角**才能评估的主张（例：尾部风险覆盖度 / 认知偏误叠加 / 激励错位 / 架构 good taste / 跨模块耦合影响 / 分类设计合理性 / 可观测指标的合理阈值）
   - 作用：席位带宽聚焦在"非席位不可判"的主张上，不被记账类 truth 稀释；verdict 焦点不失真

**小议题例外**：议题是纯代码整理 / 文案 / 修 bug 时，truths 可简化为最小可验证集（例：改动文件 `py_compile` 通过 + 一条针对性断言通过 / lint 无 error + 回归测试 pass）。这些属于 policy_discipline truth，pass_criterion 直接写死，不硬凑专业指标。

#### Step 2 · 用户确认

Step 0（召开/弃权名单）+ Step 1（must_haves）**一次性呈现**给用户。用户四选一：

- **接受全部** → 进阶段 1
- **override 召开名单**（增/减席位）→ 主 Claude 调整召开名单 + 基于新名单重定 must_haves → 重呈现 Step 2
- **override must_haves** → 修 truths/verify_commands/out_of_scope → 重呈现 Step 2
- **叫停议题** → 退出 roundtable

### 阶段 1 — 视角并行审议（dispatch: 召开名单有席位 `stages` 含 `1` 时触发）

**按阶段 0.5 Step 0 产出的召开名单**动态 spawn——在同一条消息内**并行** spawn 所有 `stages` 含 `1` 的被召开席位。默认包括所有策略席位（Taleb / Munger），**也可能包括代码席位 Linus**（当议题有工程决策维度，Step 0 给他 `stages: [1, 2]`）。

- **召开名单有席位 `stages` 含 `1`** → spawn 所有此类席位（多个 Agent tool call 并列写）；弃权席位和 `stages` 不含 1 的席位**都不 spawn**
- **无席位 `stages` 含 `1`**（纯实施议题，只召开 Linus 且 `stages=[2]`）→ **跳过本阶段**，直接进阶段 2
- **阶段 1 席位 N=1** → 只 spawn 该 1 个 agent，阶段 1.5 修订 gate 仍生效

**Linus 在阶段 1 出场时**（`stages=[1,2]`）：spawn prompt 明确他做"工程视角评议题"——good taste / 数据结构合理性 / bikeshedding / premature abstraction / anti-pattern 扫描，**不关心当前 codebase 能否承载**（那是阶段 2 的事）。阶段 2 的 Linus spawn 另起，prompt 明确"吸收阶段 1 所有席位结论 + must_haves → 可行性 gate"。两次 spawn 工作不同，不是重复。

下面是**策略席位全召开**时的 spawn 模板，实际运行时**按召开名单裁剪**——召开名单不含某席位时，整个对应 Agent block 删去；若 Linus `stages` 含 `1` 也要在此阶段加一个 Linus 的 spawn block（prompt 按"工程视角评议题"写）：

```
Agent(subagent_type="taleb-reviewer", prompt="""
议题: <议题原文>
<若有相关回测/数据/研究上下文一并贴上>

阶段 0.5 must_haves:
<完整粘贴阶段 0.5 产出的 YAML 块>

请做 fragility check：
- 10 步 Pre-Trade Fragility Check 逐条过
- tail event 下破裂点
- **针对 must_haves 的每条 truth，判断是否 fragile（tail event 下 truth 是否会塌）**
- route verdict: fragile / robust / antifragile
- 原文结尾必须带 YAML verdict block（见 agent 定义）
""")

Agent(subagent_type="munger-reviewer", prompt="""
议题: <议题原文>
<同上数据>

阶段 0.5 must_haves:
<完整粘贴阶段 0.5 产出的 YAML 块>

请做愚蠢清单扫描：
- 20 条 anti-pattern 逐条过
- Lollapalooza 扫描（多偏误叠加）
- **针对 must_haves：truths 和 verify_commands 是否有过拟合/指标操纵/激励扭曲的隐患**
- verdict: keep / kill / too-hard筐
- 若 kill 指明违反第几条
- 原文结尾必须带 YAML verdict block（见 agent 定义）
""")

Agent(subagent_type="lopezdeprado-reviewer", prompt="""
议题: <议题原文>
<同上数据>

阶段 0.5 must_haves:
<完整粘贴阶段 0.5 产出的 YAML 块>

请做 Research Integrity Audit：
- 10 步 Pre-Trade Research Integrity Check 逐条过
- 对每条 must_haves.truth 做 claim classification（associational / causal / observable_metric / policy_discipline / untestable）
- 18 条方法论 anti-pattern 扫描，命中的给 AP-N 编号
- **针对 must_haves：truths 是否是 associational claim 伪装 causal / 是否缺 causal graph / 是否未披露 trial 数 / 是否用 random K-Fold / 是否激励 p-hacking**
- 若发现 truth 本身是 associational / 把 backtest 当 theory / 未披露 trial 数等根本问题 → `must_haves_challenge.triggered: yes`
- verdict: scientific / associational / pseudo_scientific（三态）
- 若 pseudo_scientific 列出命中的 AP-N 编号；若 associational 给出升级 causal 的路径（7 步 Protocol 第几步缺）
- 议题若落在 L4 静默清单（量子 / 个股 / 宏观 / 地缘 / LLM agent alpha）→ `domain_limit_flag` 标注 + `core.route: too_hard`
- 原文结尾必须带 YAML verdict block（见 agent 定义）
- **pattern-level 批评纪律不得违反**：原文和 YAML 里都不得点名具体公司 / 基金 / PM / ticker
""")
```

三个 agent 返回后：**原文完整呈现给用户，不得转述或软化**。

### 阶段 1.5 — must_haves 修订 gate（条件触发）

扫描阶段 1 所有席位 verdict block 的 `must_haves_challenge.triggered` 字段：

- **全部 `triggered: no`** → 直接进阶段 2，Linus 拿 must_haves v1
- **任一 `triggered: yes`** → **暂停，走修订流程**：

1. 主 Claude 汇总所有 `triggered: yes` 席位的 `proposed_revision`，合并成 must_haves v2（多席位冲突时显式标注差异，不擅自取舍）
2. 呈现给用户：
   - v1 vs v2 对照表（按 truth_id）
   - 每条修改的来源席位 + `fundamental_issue`
   - 用户四选一：**接受 v2** / **接受部分**（指定哪些 truth 采纳）/ **保持 v1** / **重开议题**
3. 用户选"接受 v2"或"接受部分" → 锁定新版 must_haves，阶段 2 Linus 拿新版
4. 用户选"保持 v1" → 阶段 2 进行但显式告知 Linus"策略席建议修订 must_haves 但用户维持 v1"，Linus 在自己的 verdict 里可选择继续 challenge
5. 用户选"重开议题" → 流水线终止，回阶段 0.5 重写议题

**禁止**主 Claude 自行合并 challenge / 无视 challenge 强行推进。这是阶段 1.5 的唯一作用：把"席位推翻刚拍板的契约"这个事件从临场补 gate 升格成协议内置流程（见附录"共同 verdict schema（v2）"的 `must_haves_challenge` 字段）。

#### 阶段 1.5 产物可读性约束

任一违反则 orchestrator 综合产出不合格，必须重写。

1. **去 persona 黑话**——席位专业方言（如 Goodhart / Doubt-Avoidance / metric_gaming / premature abstraction / bikeshedding / Lollapalooza / antifragile / fragility / Turkey / skin in the game / good taste）在 v2 对照表**首次出现时必须带 1 句通俗解释**（"指 X"）。席位原文已在阶段 1 完整呈现——对照表是**决策辅助**不是黑话复读。用户判断"是否同意修订"，不是"是否听懂席位方言"。

2. **尊重席位侧已分层的 `proposed_revision`**——席位 `must_haves_challenge.proposed_revision` 已按 `revised_truth` / `revised_verify_suggestion` / `spawn_sub_topic` 三字段分层（见附录）。orchestrator 合并多席位 v2 时**直接对应字段合并**，不得再次展开或重新混合：
   - 多席位对同一 truth 的 `revised_truth` 合并成一条（矛盾时显式标注"A 席位主张 X / B 席位主张 Y"），合并结果仍保持 ≤ 50 字
   - `revised_verify_suggestion` 合并成对应 truth 的 pass_criterion 建议（按阶段 0.5 硬约束第 3 条按 truth 类型分写）
   - `spawn_sub_topic` 收集到"衍生议题"段——**不进 v2 主 truth**，作为阶段 3 `DECISIONS.deferred` 或建议另开 roundtable

3. **结构复杂度上限**：
   - v2 主张单条 ≤ 50 字（席位侧已约束 `revised_truth ≤ 50 字`，orchestrator 合并时不得膨胀）
   - 单条 v2 段不含超过 2 层括号嵌套
   - "修订来源 + fundamental_issue" 按席位分列展示（每席位独立一行），禁止用"；"挤在一行

4. **用户决策选项扩成五选一**（原 4 + 新 1）：
   - 1. 接受 v2 / 2. 接受部分 / 3. 保持 v1 / 4. 重开议题 / **5. 要求 orchestrator 改写 v2 表达**（不改实质内容，只做去黑话 / 排版重组 / 人话化）
   - 第 5 选项是"可读性回炉"——避免用户在"看不懂 v2"和"叫停议题"之间被迫二选一

5. **orchestrator 自检**（产出前通读一遍）：
   - 自问："如果我完全没读过席位 persona 的 SKILL.md / references，这段 v2 我能在 30 秒内判断是否接受吗？"
   - 自问："v2 每条主句有没有超过 50 字？有没有括号嵌套 3 层？"
   - 任一答案否 / 超限 → 重写，不得呈交用户

### 阶段 2 — 代码可行性评审（dispatch: 召开名单有席位 `stages` 含 `2` 时触发）

- **召开名单有席位 `stages` 含 `2`**（默认为 `linus-engineer`，`stages=[2]` 或 `stages=[1,2]`）→ 把阶段 1 所有席位原文（如有）打包交该席位，**保留 `linus_id` 以便阶段 4 续跑**：
- **无席位 `stages` 含 `2`**（纯策略讨论，无代码落地需求）→ 跳过本阶段，直接进阶段 3（综合时标注"本议题无代码落地维度，阶段 2 跳过"）

若 Linus `stages=[1,2]`，他在阶段 1 已有独立 verdict block（`linus_feasibility` with `phase: 1`）——阶段 2 的 spawn prompt 应显式提醒他"你阶段 1 已给出工程视角初判，本阶段吸收所有席位结论做可行性 gate，不要重复阶段 1 的 good taste 论证"。

```
linus_id = Agent(subagent_type="linus-engineer", prompt="""
议题: <议题原文>

策略层结论：

=== Taleb ===
<Taleb 原文>

=== Munger ===
<Munger 原文>

请做**可行性评审**（不要动任何文件）：
- 现有架构能否承载
- 有没有更 sane 的切法
- 技术债 / 回归风险
- 是否需要先重构再上新功能
- 按你启动时读到的当前项目 AGENTS.md/CLAUDE.md 的工程纪律判断

不评判策略 alpha。输出：sane/broken 判断 + 具体建议 + 风险提示。
""")
```

Linus 会在启动时自动发现当前项目的 `AGENTS.md` / `CLAUDE.md` 并按项目纪律工作——**不需要在 prompt 里硬编码项目特定规则**。

Linus 返回后：**原文完整呈现给用户**。

### 阶段 3 — 综合对齐（主 Claude 主持）

你（主 Claude）做综合，**优先读每个席位原文末尾的 YAML verdict block**（机读），再补文字表达。

**阅读顺序**（所有席位共用 `core` / `must_haves_review` / `must_haves_challenge` / `seat_specific` 四层结构，详见文末附录"共同 verdict schema（v2）"）：

1. **先扫 `core.route`**——聚合所有席位的路由（阶段 1.5 已处理过 challenge，这里主要看 `go` / `go_with_conditions` / `kill` / `too_hard` 分布）
2. **读 `seat_native_verdict`**——角色表达风格（综合表同时列 native 和 route）
3. **汇总所有 `core.hard_blockers`**——列成综合 blocker 列表
4. **合并 `must_haves_review`**——同一 truth 多席位 flag 冲突时，取最严的 `proposed_criterion`
5. **读 `seat_specific`**——补充细节（tail_events / anti_patterns / broken_evidence 等）作为"人读补充"
6. **读 `core.peer_disagreements`**——显式列分歧，不要在综合时强行收敛

**输出**：

1. **策略层综合表**（若召开名单含策略席位）：列 `seat / core.route / seat_native_verdict / hard_blockers / key concern`——仅列被召开席位，弃权席位不出现
2. **代码层**（若召开名单含 `linus-engineer` 且阶段 2 已执行）：Linus 的 `core.route` + `seat_native_verdict`（sane / broken / needs_refactor_first）+ 可行性建议；broken 时列 `seat_specific.broken_evidence` 的 file/symbol。若阶段 2 跳过（召开名单无 Linus）→ 本节改写为"本议题无代码落地维度，阶段 2 跳过"
3. **最终方案候选表**：列 2-3 个可行路径 + 权衡 + 推荐项
4. **DECISIONS 表**（用户拍板时同步定下，阶段 4 的输入）：

   | 分类 | 内容 | 来源 |
   |---|---|---|
   | `locked`（必须实施，Linus 不得越过） | D-01 ... D-0N | 阶段 0.5 must_haves（含阶段 1.5 修订后的 v2）+ 阶段 3 用户拍板 |
   | `deferred`（本议题明确不做） | ... | 阶段 0.5 out_of_scope + 用户拍板延后项 |
   | `discretion`（Linus 可自行判断的区域） | ... | 未被 locked/deferred 覆盖的实现细节 |

5. **等用户确认**：用户未明示 go 之前，禁止进入阶段 4

### 阶段 4 — 实施

用户确认后，**按运行时条件分支**推进——优先尝试 SendMessage 续跑，不可用则 fallback 到新 spawn + 完整上下文注入。

#### 路径 A · SendMessage 续跑（首选）

主 Claude 在阶段 4 先检查自己的 tool schema 是否包含 `SendMessage` 工具。**如果有**，用它续跑同一个 `linus_id`：

```
SendMessage(to=linus_id, """
方案已锁定：<细到文件/函数级别>

按你阶段 2 的可行性建议实施。完成后按当前项目 AGENTS.md/CLAUDE.md 定义的自审清单执行。
实施后不要 commit——等用户验证通过。
""")
```

优点：保留 Linus 阶段 2 的完整内部状态 + 对话历史，prompt 最短。

#### 路径 B · 新 spawn + 完整上下文注入（fallback）

**SendMessage 不可用**时（当前 Claude Code 版本存在 bug [#42737](https://github.com/anthropics/claude-code/issues/42737)，普通 session 该 tool 未暴露），走新 spawn：

```
Agent(subagent_type="linus-engineer", prompt="""
议题：<议题原文>
方案已锁定：<细到文件/函数级别>

=== 你在阶段 2 的可行性评审原文（作为自己上一轮判断对待）===
<完整粘贴阶段 2 Linus 输出，不要摘要>

=== 策略席位结论摘要 ===
Taleb verdict: <fragile/robust/antifragile + 关键理由>
Munger verdict: <keep/kill/too-hard + 关键理由>

按上述锁定方案实施。完成后按当前项目 AGENTS.md/CLAUDE.md 自审。
实施后不要 commit——等用户验证通过。
""")
```

**关键**：阶段 2 Linus 原文必须**完整粘贴**，不得摘要——他需要自己上一轮的具体判断才能延续可行性结论。

#### 路径自动切换

两路径语义等价。官方修复 SendMessage 后主 Claude 自动走路径 A，**本 command 无需改动**。

Linus 返回实施报告后：**原文完整呈现给用户**。

---

## 冲突裁决规则

| 冲突类型 | 处理 |
|---|---|
| 策略席之间分歧（如 Taleb vs Munger / Taleb vs López / Munger vs López） | 可选：SendMessage 让他们互相 push back 一轮；或主 Claude 呈分歧表给用户拍板。**典型 Taleb vs López 分歧**：Taleb 认为金融不能科学化（换分布 class），López 认为应当科学化（Gaussian 工具内 + FDR + causal 修正）——路径相反，不强行合并 |
| Linus 说"代码层 broken" | 回阶段 1 问策略席：是否有等价路径可绕开该 broken 点 |
| 策略必须 × 代码无法干净落地 | 主 Claude + 用户拍板：重构承载 / 降级策略 / 放弃本次改动 |
| Linus 阶段 2 建议与策略结论矛盾 | 主 Claude 明确呈现给用户，不擅自取舍 |

---

## 硬约束（任何情况不得违反）

1. **绝不转述 agent 原文**：各席位的判断是职业发言，转述会失真，必须完整呈现。
2. **绝不跳阶段**：阶段 3 用户未确认前不得进阶段 4。
3. **实施阶段优先 SendMessage 续跑**：tool schema 里有 `SendMessage` 就走阶段 4 路径 A；没有则走路径 B（新 spawn + 阶段 2 原文**完整注入**，不得摘要）。禁止"新 spawn 但只传简短摘要"这种懒做法。
4. **项目纪律由 agent 自己发现**：不在 command 里硬编码项目特定规则。Linus 启动时会自动 Read 当前项目的 AGENTS.md/CLAUDE.md。

---

## 文件布局

| 资源 | 路径 | 说明 |
|---|---|---|
| 三个 agent 定义 | `~/.claude/agents/{taleb,munger,linus}-*.md` | 全局，跨项目可用 |
| 本 command | `~/.claude/commands/roundtable.md` | 全局 |
| persona skill 原文 | `~/.claude/skills/{taleb-antifragile,munger-checklist,linus-torvalds-engineer}/SKILL.md` | agent body 引用，skill 更新自动生效 |
| 项目特定规则 | `<项目根>/AGENTS.md` 或 `<项目根>/CLAUDE.md` | Linus 运行时自动读取 |

### skill 更新后的同步

- skill 正文改了 → **零同步**，agent 下次 spawn 自动拉最新
- skill 路径/文件名改了 → 改对应 agent md 里的引用路径（1 行）
- 新增/调整席位 → 新建 agent md + 更新本 command 的席位表和阶段 1 spawn 列表
- skill 方向大改（verdict 档位、核心心智模型换了）→ 跑一次 `/roundtable` 烟雾测试，必要时调 agent md 的硬边界段

### 项目级覆盖

某项目有专属需求（比如定制的流水线阶段、特殊席位）时，在该项目的 `.claude/commands/roundtable.md` 放一份覆盖全局版。Claude Code 同名时项目级优先。日常不需要，有需求再加。

### SendMessage 续跑能力（自适应）

- 当前 Claude Code 存在 bug：SendMessage 工具被错误锁在 agent teams 功能后，普通 session 未暴露（[#42737](https://github.com/anthropics/claude-code/issues/42737)）
- 阶段 4 已写成**条件分支**：主 Claude 运行时检查 tool schema，有 SendMessage 走路径 A 续跑，无则走路径 B 新 spawn + 阶段 2 原文注入
- 官方修复后**无需改本文件**，主 Claude 自动切到路径 A
- 两路径语义等价：路径 A 保留 agent 内部对话状态更高效，路径 B 信息完整但每次重建 agent

---

## 附录 · 共同 verdict schema（v2）

所有席位（Taleb / Munger / Linus / 未来扩展）的 verdict block 遵守三层结构 —— `core` + `must_haves_review` + `must_haves_challenge` + `seat_specific`（选填）。设计目的：主持人阶段 3 机读统一（不用翻译三套方言），同时保留各席位人格 DNA。

### core（强制，主持人机读综合用）

| 字段 | 取值 | 作用 |
|---|---|---|
| `seat` | taleb / munger / linus / 新席位 | 标识 |
| `phase` | 1 / 2 / 4 | 阶段 |
| `route` | `go` / `go_with_conditions` / `revise_must_haves` / `kill` / `too_hard` | **统一路由空间**，阶段 3 机读 |
| `seat_native_verdict` | Taleb: fragile/robust/antifragile；Munger: keep/kill/too_hard；Linus 阶段 2: sane/broken/needs_refactor_first | 保留人格 DNA |
| `confidence` | low / medium / high | 信心 |
| `hard_blockers` | `[]` | 转 go 的必要条件（合并原 blockers / kill reasons / broken evidence） |
| `peer_disagreements` | `[{peer, point}]` | 跨席位分歧（合并原 push_back_on_X） |

### must_haves_review（强制，点状审视每条 truth）

统一 flag 空间：`none` / `threshold_issue` / `method_issue` / `overfitting_risk` / `metric_gaming` / `coverage_gap` / `lookahead_unchecked` / `multiple_testing` / `incentive_mismatch` / `other`。

席位对 `must_haves.truths` 的每条给出 flag + `proposed_criterion`（非 none 时必填）。主持人阶段 3 合并成 `pass_criterion` 建议 —— 同一 truth 多席位冲突时取最严。

### must_haves_challenge（A1 逃生口）

```yaml
must_haves_challenge:
  triggered: yes | no
  challenged_truths: [1, 3]
  fundamental_issue: "<为何 must_haves 框架从根本跑偏，不是单条阈值问题>"
  proposed_revision:                        # list of struct，每 challenged truth 一条；三字段强制分层
    - truth_id: 1
      revised_truth: "<修订后的主张本身，≤ 50 字；禁混实施路径 / 验证命令 / 衍生议题>"
      revised_verify_suggestion: "<如何验证此主张；无则空字符串 '' 让 orchestrator 后定>"
      spawn_sub_topic: "<建议拆出的新子议题；无则空字符串 ''>"
```

**`proposed_revision` 三字段分层规则**（席位侧源头保证阶段 1.5 产物可读）：

- `revised_truth`：只放修订后的主张本身——"改为什么"。硬上限 ≤ 50 字、不超过 2 层括号嵌套。禁混：具体文件路径 / grep 命令 / 数值阈值 / 新子议题 / 触发条件。
- `revised_verify_suggestion`：修订后主张的验证建议——"怎么验证"。具体文件路径 / grep / 阈值放这里。
- `spawn_sub_topic`：修订触发的新子议题——"需要另开议题的部分"。无则空字符串 `""`。

席位若不分层（把所有内容塞进 `revised_truth`），orchestrator 阶段 1.5 综合时会被迫展开给用户看——这是触发"说的不是人话"事件的源头。从席位侧保证分层，阶段 1.5 才能干净做合并 + 去黑话。**严禁回退为字符串字面量**（旧 schema 的 `proposed_revision: | <多行文本>` 禁用）。

**任一席位 `triggered: yes` → 阶段 1.5 must_haves 修订 gate 强制触发**（见上文阶段 1.5）。orchestrator 不得忽略，也不得自行合并。

`must_haves_review` vs `must_haves_challenge` 区分：前者是点状阈值/方法修订（"改 99%CI"），后者是根本框架推翻（"hit% 做主目标本身就是 Jensen 陷阱 / Goodhart metric"）。两者可并存。

### seat_specific（选填，保留席位 DNA）

各席位自由定义，主持人阶段 3 作为"人读补充"：

- **Taleb**: `tail_events_breaking_must_haves` / `fragility_checklist_failures` / `skin_in_the_game`
- **Munger**: `anti_patterns_hit` / `lollapalooza_stack` / `circle_of_competence` / `reverse_kill_path`
- **López**: `claim_classification` / `causal_graph_missing` / `trial_count_disclosed` / `integrity_checklist_failures` / `anti_pattern_hits` / `workflow_diagnosis` / `domain_limit_flag`
- **Linus 阶段 2**: `broken_evidence` / `must_haves_coverage_detail` / `refactor_prerequisites` / `risk_notes` / `out_of_scope_for_strategy`

### route 映射规则（各席位 native → core.route）

| 席位 | native | → `core.route` |
|---|---|---|
| Taleb | fragile | `go_with_conditions` / `revise_must_haves` / `kill` |
| Taleb | robust / antifragile | `go` |
| Munger | keep | `go` |
| Munger | kill | `kill` |
| Munger | too_hard | `too_hard` |
| Munger | （对 must_haves 框架本身不满） | `revise_must_haves` |
| López | scientific | `go` |
| López | associational | `go_with_conditions`（hard_blockers 列"必须补 causal graph + do-calculus adjustment"） |
| López | pseudo_scientific | `kill`（命中 AP-1/2/4/7/10/16 等核心 anti-pattern 且不可救）/ `revise_must_haves`（must_haves 本身是 associational 伪装 causal，同时触发 challenge） |
| López | （domain_limit_flag 非 none） | `too_hard`（议题属 L4 静默清单 / 非方法论 domain） |
| Linus | sane | `go` |
| Linus | broken | `kill`（单边否决） |
| Linus | needs_refactor_first | `revise_must_haves` / `go_with_conditions` |

### 新增席位时的步骤

1. 新建 `~/.claude/agents/<name>-reviewer.md`（或 `-engineer.md`，后缀按席位身份选——Linus `-engineer`、Munger `-checklist`、Buffett 可能 `-letter`）
2. verdict block root key 用 `<seat>_verdict`（如 `buffett_verdict`）
3. `core` 段字段齐全 + `must_haves_review` + `must_haves_challenge` 强制
4. `seat_specific` 自定义字段
5. 在本文件"当前席位"表 + 阶段 1 spawn 列表加一行
6. 在本附录"route 映射规则"表加对应席位的 native → core.route 映射

### 阶段 4 例外

Linus 阶段 4 的 `linus_execution` block **不走**共同 verdict schema —— 它是实施验证状态输出，不是 verdict。保留原 `status` / `decisions_honored` / `verification_attempted` / `self_audit` / `commit_status` / `gaps_to_route_back` 字段结构。
