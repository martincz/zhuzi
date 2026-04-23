# Roundtable Workflow

> 这是 `/zhuzi:roundtable` 的权威 workflow。命令入口负责装载，本文件只负责流程本身。Quick headings、seat/stages/route、seat-specific 机器合同以 `zhuzi/manifests/roundtable-contract.json` 为准；人读解释以同时装载的 reference / template 为准。

## 流水线性质

本流水线支持 **N 席位召开（N ≥ 1）**——阶段 0.5 扫议题关键词匹配席位权威表，只 spawn 有资格的席位。弃权席位不产出 YAML。无代码席位时阶段 2（代码可行性）dispatch 不触发；N=1 时流水线退化为单席位审议，这是合法状态不需特殊 exit。

## 默认交互契约

圆桌默认走 **Quick Roundtable**：内部保留完整阶段、原文和 YAML，用户界面只展示能帮助决策的短读内容。只有用户显式说“完整圆桌 / strict / full / 展开原文 / 展开 YAML”时，才展示完整席位原文和完整协议细节。

### Quick 输出模板（默认必须使用）

默认骨架只认同时装载的 `templates/roundtable-quick.md`。
顶级标题名称、顺序和表格骨架都以 template 为准；本 workflow 只定义阅读纪律和阶段语义，不再复制另一份 heading 列表。

**模板纪律**：

- 不新增“背景复述”“完整会议纪要”“逐席位长段落”等默认区块。
- `主持人结论` 必须先出现；不能先展示流程、YAML 或席位原文。
- `席位短评` 每席只占一行；需要长理由时放到 full/strict 展开。
- `决策表` 的分类只用 `locked / deferred / discretion`，避免额外术语。
- **persona 术语首次出现必须带 1 句人话括注**——覆盖议题卡、must_haves truths、席位短评、做完会怎样、DECISIONS 表等所有默认呈现段。例：`Deflated Sharpe`（试了 N 次后要对观察到的 Sharpe 打折才算真显著）、`ergodicity`（单人长期路径和平行宇宙平均是两回事）。用户要完整 persona DNA 时说“展开原文”再呈现无括注版。

**可读性预算**：

- 第一屏先给主持人结论，不先铺流程。
- 默认阶段 1 同时召开的评议席位不超过 3 个；超过时选最相关、分歧价值最高的席位，其他席位弃权并简短说明。
- 默认 `must_haves.truths` 1-3 条；只有 full 模式或议题天然很大时才放宽到 5 条。
- agent 原文和 YAML 是机读证据，不是默认阅读材料；默认只在“展开原文 / 调试 / 审计”请求下显示。

## 内部流水线（严格按阶段推进，外部默认短读）

### 阶段 0.5 — 议题契约定义（orchestrator）

spawn 任何席位**之前**，orchestrator 完成三件事。Quick 模式下不要把内部 YAML 整段甩给用户，而是压缩成一张议题卡；full 模式或用户要求展开时再显示完整结构。

#### Step 0 · 席位召开判定

扫议题关键词 + `seat-registry.md` 的“当前席位”表与默认 `stages` 规则 → 匹配产出召开名单（**含每席位 `stages` 在哪些阶段出场**）+ 弃权名单 + 理由。**orchestrator 主动决定，不为每次召开单独问用户**（用户在 Step 2 一起确认/override）。

默认用户可见格式（**粗体段头 + bullet**，**不用 Markdown table**；table 的 cell 天然挤压，脱 table 后物理上不存在挤压问题）：

```markdown
**目标**：<本轮结束时可指给别人看的产物>

**召开席位**
- `<seat-1>` · <1 句理由>
- `<seat-2>` · <1 句理由>

**弃权席位**
- `<seat-a>` · <1 句理由>

**暂不讨论**
- <out_of_scope-1>
- <out_of_scope-2>
```

**标点硬约定（议题卡 + 什么算过关 + 席位短评全部适用）**：

| 符号 | 专用语义 | 反例（禁止） |
|---|---|---|
| `：` | 粗体标签 → 详情（唯一形式） | 不做 inline 列表分隔 |
| `·` | **仅** `<ID> · <短说明>` 一种用法（席位名单、"关联性 · 例：..."） | 不做标签-详情分隔、不做多项并列 |
| `/` | 紧凑枚举（"A / B / C"） | 不接详情 |
| `+` | 并列累加（"指标 + 阈值"） | 不做分隔 |
| `—` / `——`（破折号） | **不用**——全部退成 `：` | |

**排版硬约束**：

- **议题卡不用 table**——`目标` 用 inline `**目标**：...` 一行搞定；`召开席位 / 弃权席位 / 暂不讨论` 都用 `**粗体段头**` 起段后接 bullet 列表。Bullet 每项独占一行，物理上无法挤压，不需要 `<br>` 规则。
- **目标行 = 可交付产出，不是工作描述**——目标必须是本轮 roundtable 结束时可指给别人看的产物（决策表 + 验证信号 / contract 修订锁定 / 参数值锁定 / 议题拆分结果）。禁止以 "判断" / "讨论" / "评估" / "决定是否" / "审视" 开头——那些是**正在做什么**而不是**做完有什么**。若实在写不出产物，多半议题粒度太粗，拆成两条再开。
- **成功标准独立段**——成功标准作为独立二级 heading 段落 `## 什么算过关`，放在议题卡之后、Step 2 的四选一之前。具体排版规则见 Step 1。

内部仍保留结构化 `seat / stages / reason`，供后续 spawn 使用；用户要求“展开契约”时再显示完整 YAML。

**硬约束**：

- 席位自然语言匹配 ≠ 关键词精确命中——“激励结构”和“激励设计”算同一域，orchestrator 按语义判断。
- N=1 时（只 1 个席位召开）明确告知用户“本议题退化为单席位 roundtable”——这是合法状态，不需额外 exit 路径。
- N=0 时（无席位匹配）停流水线，建议用户改议题描述或用非 roundtable 流程直接和 orchestrator 对话。
- Quick 模式下评议席位默认不超过 3 个；若语义命中超过 3 个，优先保留最能发现 hard blocker 或真实分歧的席位。

`stages` 的默认路由、López 必召开触发词，以及 Linus `stages=[1,2]` 的双阶段语义都以 `roundtable-contract.json` 为机读真相源，并以 `seat-registry.md` 作为人读解释层。本文件只在真正需要的阶段描述里重复其效果，不复制完整席位表。

#### Step 1 · must_haves 定义

基于**召开名单的视角**（不给弃权席位预留 truth），把议题翻译成可验证的成功标准。

**机读合同结构（内部保留，不直接展示给用户）**——阶段 1 spawn 席位时注入 prompt、阶段 4 实施时跑 verify、事后 audit trail 追溯用：

```yaml
must_haves:
  truths:            # Quick 默认 1-3 条；full 模式最多 5 条
    - "<例：v28 M1 在 baseline 上 paired bootstrap walpha Δ 下界 > 0>"
    - "<例：d20 hit% 不回退超 1pp>"
    - "<例：Spearman ρ 与 walpha 方向一致>"
  verify_commands:   # 每条 truth 对应的可机器执行验证命令
    - truth: 1
      cmd: "<observable_metric 示例：python3 tools/bench.py --replay-from <baseline> / curl -w '%{time_total}' <api> / du -b dist/bundle.js>"
      pass_criterion: "TBD — 待召开席位审阅"
    - truth: 2
      cmd: "<policy_discipline 示例：grep -E '<pattern>' <file> / jq '.schema.fields.X.type' <json>>"
      pass_criterion: "grep 命中 ≥ 1 条且匹配 '<约定措辞>' / JSON 字段 X 存在且 type == 'Y'"
  out_of_scope:
    - "<例：不动某权重表 / 不改某候选池定义 / 不触发新基准测试>"
```

**面向用户的呈现规则（议题卡之后独立的 `## 什么算过关` 段的展示形式，不塞进议题卡 table）**：

- **truths 用 "粗体短标签：短陈述 + 子 bullet 详情" 结构**，不是单行长句。粗体标签接 `：` 引出详情（不用破折号 `—`）；候选阈值、并列选项、例子都用子 bullet 分行列出。一条规则若超过 5 行，说明粒度太粗，拆成两条。
- **术语括注必须讲机制，不是中英对照**——给可验证行为的例子，不是换名字。判断标准：把术语换成别的词、例子还成立吗？成立就是解释，不成立就是翻译。例：✓ `**关联性** · 例：X 和 Y 同涨同跌`；✗ `关联性（associational）`——后者只是中英对照，不讲机制。
- **规则正文里不混专业引用**——类似 `按 XX 文档的 YY` 或 `[internal_code_name]` 这种引用要么展开为 1 句人话说明，要么挪到独立 "参考" 行。规则主干只放可直接理解的内容。
- **空心词禁用**——"真正有价值" / "合理的" / "更好的" 这类词必须替换成可验证标准（"能量化提升" / "风险降低" / "d20 命中率不回退"）。
- **不罗列 `type` / `pass_criterion` / `verify_cmd` 字段**——这些是内部字段。
- **out_of_scope** 合并成一段短说明或紧凑列表，不做三栏表。
- **`verify_commands` / `pass_criterion` 默认不展示**——它们服务阶段 4 实施和事后 audit，不服务用户阶段 0.5 拍板。
- 用户说 **"展开 YAML / 展开机读合同 / strict"** 时才显示上面的机读版。

人读压缩版范例（3 条 truths + out_of_scope）：

```text
**什么算过关**

**1. 改进要能量化**：给出目标指标 + 阈值。候选参考：
- `paired bootstrap replay`（抽样比对新旧版本差异显著性）下 `walpha`（加权超额收益）Δ 下界 > 0
- d20 命中率不回退超 1pp

**2. 每条建议声明性质**：三选一——
- **关联性** · 例：看到 X 和 Y 同涨同跌
- **因果性** · 例：做 X 能让 Y 变好
- **可观测指标** · 例：回测跑完 walpha 是 +1.5%

若做过多次权重搜索，披露累计 trial 数，按 `Deflated Sharpe`（试 N 次后对观察 Sharpe 打折才算真显著）算。

**3. 守住能力圈**：三项硬约束不动：
- 收盘后运行
- 基于现有数据源
- 输出固定数量

**暂不涉及**：改变选股数量 / 运行时点 / 额外数据源 / 部署架构 / 权限模型
```

**硬约束（任一违反则 must_haves 段不合格，必须重写）**：

1. **`truths` 只放可验证主张**，两类合法：
   - **observable_metric**：可观测的量化行为（例：回测 walpha Δ / API p99 latency / 内存峰值 / bundle 大小 / 编译耗时 / 错误率 / bootstrap CI）
   - **policy_discipline**：可验证的结构性 / 纪律性事实（例：某文档新增条款且含指定措辞 / 某接口字段存在且类型正确 / 某输出列带约定前缀 / 某目录结构符合规范 / 某配置开关默认值符合约定）

   两类都合法，但以下禁放 truths：
   - 实施约束（“只改 N 个文件”“不引入新依赖”）→ 走阶段 3 `DECISIONS.locked`
   - 主观项（“代码写得好看”“文档清楚”）
   - 流程要求（“跑通编译”“跑通测试”）→ 走 `out_of_scope` 默认项

2. **`truths` 数量默认 1-3 条，硬上限 5 条**——Quick 模式超过 3 条必须删到最关键；full 模式超过 5 条说明议题粒度太粗，必须拆成两个 roundtable 分别开。

3. **`pass_criterion` 按 truth 类型分写**：
   - **observable_metric truth**：orchestrator 原则上打 `TBD — 待召开席位审阅`，交席位在 `must_haves_review.proposed_criterion` 填具体阈值。
   - **policy_discipline truth**：orchestrator **必须直接写死**判断标准，**不得 TBD**。
   - 纯技术断言（“py_compile 通过”“HTTP 200”“lint 无 error”）按 `policy_discipline` 规则，orchestrator 直接写死。

4. **`out_of_scope`** 直接喂给阶段 3 DECISIONS 表的 `deferred` 段。

5. **无法为某 truth 写出 verify 命令时**，先打 `TBD — 需要召开席位确认指标口径`——缺验证标准比议题失败更严重。

6. **`pass_criterion` 禁“程序正义式”描述**——回答“什么状态算通过”，不是“谁说了算 / 怎么达成一致”。

7. **`truths` 过席位必要性预检**——若某 truth 不需要召开席位专业视角才能评估，就不要塞进 `must_haves.truths`，改入 `DECISIONS.locked` 或 `DECISIONS.discretion`。

**小议题例外**：议题是纯代码整理 / 文案 / 修 bug 时，truths 可简化为最小可验证集（例：改动文件 `py_compile` 通过 + 一条针对性断言通过 / lint 无 error + 回归测试 pass）。这些属于 `policy_discipline truth`，`pass_criterion` 直接写死，不硬凑专业指标。

#### Step 2 · 用户确认

Step 0 产出的**议题卡**（框线 table，不含成功标准）+ Step 1 产出的**独立 `## 什么算过关` 段**（粗体标签 + 子 bullet 的人读压缩版）**一次性呈现**给用户。YAML 机读合同仍在内部保留，用户要才展示。用户四选一：

- **接受全部** → 进阶段 1
- **override 召开名单**（增/减席位）→ orchestrator 调整召开名单 + 基于新名单重定 must_haves → 重呈现 Step 2
- **override must_haves** → 修 truths / verify_commands / out_of_scope → 重呈现 Step 2
- **叫停议题** → 退出 roundtable

### 阶段 1 — 视角并行审议（dispatch: 召开名单有席位 `stages` 含 `1` 时触发）

**按阶段 0.5 Step 0 产出的召开名单**动态 spawn——在同一条消息内**并行** spawn 所有 `stages` 含 `1` 的被召开席位。默认按议题召集相关非代码评议席位，**也可能包括代码席位 Linus**（当议题有工程决策维度，Step 0 给他 `stages: [1, 2]`）。

- **召开名单有席位 `stages` 含 `1`** → spawn 所有此类席位；弃权席位和 `stages` 不含 1 的席位**都不 spawn**。
- **无席位 `stages` 含 `1`**（纯实施议题，只召开 Linus 且 `stages=[2]`）→ **跳过本阶段**，直接进阶段 2。
- **阶段 1 席位 N=1** → 只 spawn 该 1 个 agent，阶段 1.5 修订 gate 仍生效。

**Linus 在阶段 1 出场时**（`stages=[1,2]`）：spawn prompt 明确他做“工程视角评议题”——good taste / 数据结构合理性 / bikeshedding / premature abstraction / anti-pattern 扫描，**不关心当前 codebase 能否承载**（那是阶段 2 的事）。阶段 2 的 Linus spawn 另起，prompt 明确“吸收阶段 1 所有席位结论 + must_haves → 可行性 gate”。两次 spawn 工作不同，不是重复。

下面是**非代码评议席位全召开**时的 spawn 模板，实际运行时**按召开名单裁剪**——召开名单不含某席位时，整个对应 Agent block 删去；若 Linus `stages` 含 `1` 也要在此阶段加一个 Linus 的 spawn block（prompt 按“工程视角评议题”写）：

```text
Agent(subagent_type="taleb-reviewer", prompt="""
议题: <议题原文>
<若有相关回测/数据/研究上下文一并贴上>

阶段 0.5 must_haves:
<完整粘贴阶段 0.5 产出的 YAML 块>

请做 fragility check：
- 10 步 Pre-Trade Fragility Check 逐条过
- tail event 下破裂点
- 针对 must_haves 的每条 truth，判断是否 fragile（tail event 下 truth 是否会塌）
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
- 针对 must_haves：truths 和 verify_commands 是否有过拟合 / 指标操纵 / 激励扭曲的隐患
- verdict: keep / kill / too-hard
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
- 针对 must_haves：truths 是否是 associational claim 伪装 causal / 是否缺 causal graph / 是否未披露 trial 数 / 是否用 random K-Fold / 是否激励 p-hacking
- 若发现 truth 本身是 associational / 把 backtest 当 theory / 未披露 trial 数等根本问题 → `must_haves_challenge.triggered: yes`
- verdict: scientific / associational / pseudo_scientific（三态）
- 若 pseudo_scientific 列出命中的 AP-N 编号；若 associational 给出升级 causal 的路径（7 步 Protocol 第几步缺）
- 议题若落在 L4 静默清单（量子 / 个股 / 宏观 / 地缘 / LLM agent alpha）→ `domain_limit_flag` 标注 + `core.route: too_hard`
- 原文结尾必须带 YAML verdict block（见 agent 定义）
- pattern-level 批评纪律不得违反：原文和 YAML 里都不得点名具体公司 / 基金 / PM / ticker
""")
```

agent 返回后，orchestrator **先机读 YAML verdict**，默认只向用户呈现席位短评卡。不得软化、反向改写或掩盖 hard blocker；但也不得把长原文当默认阅读材料。

默认席位短评卡：

| 席位 | 结论 | 最大风险 | 必须满足 | 分歧 | 信心 |
|---|---|---|---|---|---|
| `<seat>` | <路由中文译 · 1 句条件> | 1 句 | 1 句 | 1 句，没有写“无” | <判据 · high/medium/low> |

**信心列打分机制（不允许主观打分，必须按判据给值 + 一句判据来源）**：

| 判据 | 值 | 说明 |
|---|---|---|
| 席位自声明"证据充分 + 能力圈内 + 无 must_haves challenge" | `high` | 格式：`high · 2 席一致` / `high · 本席位 core 领域` |
| 席位 flag 了 `must_haves_review` 或席位间结论分歧 | `medium` | 格式：`medium · 方法论 blocker 未过` / `medium · 与 Linus 有分歧` |
| 席位 `core.domain_limit_flag=true`、`too_hard`、或信息不足 | `low` | 格式：`low · 能力圈外` / `low · 证据不足` |

判据必须写进单元格（`<值> · <判据>` 形式），禁止裸写 `high` / `medium` / `low`。判据冲突时就低不就高。

**结论列译表（Quick 默认只露路由的中文译，不露 `core.route` token 也不露 `native_verdict`）**：

| `core.route` | 中文译 | 用法 |
|---|---|---|
| `go` | 过 | 方案按现状可推进 |
| `go_with_conditions` | 可做 · <1 句条件> | 条件直接拼进译文，例：`可做 · 先定义缓存键和失效规则` |
| `revise_must_haves` | 改 must_haves | 回阶段 1.5 修 |
| `kill` | 停 | 建议不做 |
| `too_hard` | 放弃 · <1 句原因> | 能力圈外或议题粒度太粗 |

席位 `native_verdict`（如 `sane` / `cargo_cult` / `pseudo_scientific` / `fragile`）是 persona DNA，保留在内部 YAML 和原文里，**Quick 短评卡不展示**；用户说 “展开 verdict / 展开原文” 时才列。硬 blocker（`kill` / `too_hard` / `revise_must_haves` / 代码层 `broken`）除外——这些必须在短评卡直接露出，不得藏到展开内容里。

**展开规则**：

- 用户说“展开原文 / 展开 YAML / strict / full” → 按席位完整展示原文和 YAML。
- 有 `kill` / `too_hard` / `revise_must_haves` / 代码层 `broken` → 短评卡里必须直接露出，不得藏到展开内容里。
- 席位原文仍作为内部证据保留，阶段 2/3/4 可引用；默认 UI 只展示短评卡。

### 阶段 1.5 — must_haves 修订 gate（条件触发）

扫描阶段 1 所有席位 verdict block 的 `must_haves_challenge.triggered` 字段：

- **全部 `triggered: no`** → 直接进阶段 2，Linus 拿 must_haves v1。
- **任一 `triggered: yes`** → **暂停，走修订流程**：

1. orchestrator 汇总所有 `triggered: yes` 席位的 `proposed_revision`，合并成 must_haves v2（多席位冲突时显式标注差异，不擅自取舍）。
2. 呈现给用户：
   - v1 vs v2 对照表（按 truth_id）
   - 每条修改的来源席位 + `fundamental_issue`
   - 用户五选一：**接受 v2** / **接受部分**（指定哪些 truth 采纳）/ **保持 v1** / **重开议题** / **要求 orchestrator 改写 v2 表达**
3. 用户选“接受 v2”或“接受部分” → 锁定新版 must_haves，阶段 2 Linus 拿新版。
4. 用户选“保持 v1” → 阶段 2 进行但显式告知 Linus“非代码评议席位建议修订 must_haves 但用户维持 v1”，Linus 在自己的 verdict 里可选择继续 challenge。
5. 用户选“重开议题” → 流水线终止，回阶段 0.5 重写议题。
6. 用户选“要求 orchestrator 改写 v2 表达” → 不改实质内容，只做去黑话 / 排版重组 / 人话化，然后回到五选一。

**禁止** orchestrator 自行合并 challenge / 无视 challenge 强行推进。这是阶段 1.5 的唯一作用：把“席位推翻刚拍板的契约”这个事件从临场补 gate 升格成协议内置流程。

#### 阶段 1.5 产物可读性约束

任一违反则 orchestrator 综合产出不合格，必须重写：

1. **去 persona 黑话**——按模板纪律里的术语括注规则执行；阶段 1.5 产物不得出现首次无括注的 persona 术语。
2. **尊重席位侧已分层的 `proposed_revision`**——直接对应 `revised_truth` / `revised_verify_suggestion` / `spawn_sub_topic` 三字段合并，不得重新搅成一团。
3. **结构复杂度上限**：
   - v2 主张单条 ≤ 50 字。
   - 单条 v2 段不含超过 2 层括号嵌套。
   - “修订来源 + fundamental_issue” 按席位分列展示，禁止用分号挤成一行。
4. **orchestrator 自检**——在 30 秒内能让一个没读 persona 资料的人判断“是否接受 v2”。

### 阶段 2 — 代码可行性评审（dispatch: 召开名单有席位 `stages` 含 `2` 时触发）

- **召开名单有席位 `stages` 含 `2`**（默认为 `linus-engineer`，`stages=[2]` 或 `stages=[1,2]`）→ 把阶段 1 所有席位原文（如有）打包交该席位，**保留 `linus_id` 以便阶段 4 续跑**。
- **无席位 `stages` 含 `2`**（纯策略讨论，无代码落地需求）→ 跳过本阶段，直接进阶段 3（综合时标注“本议题无代码落地维度，阶段 2 跳过”）。

若 Linus `stages=[1,2]`，他在阶段 1 已有独立 verdict block（`linus_feasibility` with `phase: 1`）——阶段 2 的 spawn prompt 应显式提醒他“你阶段 1 已给出工程视角初判，本阶段吸收所有席位结论做可行性 gate，不要重复阶段 1 的 good taste 论证”。

```text
linus_id = Agent(subagent_type="linus-engineer", prompt="""
议题: <议题原文>

阶段 1 席位原文（按本次实际召开名单逐个粘贴；下面只是格式示意，可能包含 Taleb / Munger / López / Linus phase 1 / 未来席位）：

=== <Seat A> ===
<Seat A 原文>

=== <Seat B> ===
<Seat B 原文>

...（继续附上本次阶段 1 所有席位原文）

请做可行性评审（不要动任何文件）：
- 现有架构能否承载
- 有没有更 sane 的切法
- 技术债 / 回归风险
- 是否需要先重构再上新功能
- 按你启动时读到的当前项目 AGENTS.md/CLAUDE.md 的工程纪律判断

不评判策略 alpha。输出：sane / broken 判断 + 具体建议 + 风险提示。
""")
```

Linus 会在启动时自动发现当前项目的 `AGENTS.md` / `CLAUDE.md` 并按项目纪律工作——**不需要在 prompt 里硬编码项目特定规则**。

Linus 返回后默认呈现代码席短评：`sane / broken / needs_refactor_first`、最关键证据、是否能实施、必须先做什么。完整原文只在用户要求展开或进入 full 模式时展示。

### 阶段 3 — 综合对齐（orchestrator 主持）

你（orchestrator）做综合，**优先读每个席位原文末尾的 YAML verdict block**（机读），再补文字表达。

**阅读顺序**：

1. **先扫 `core.route`**——聚合所有席位的路由。
2. **读 `seat_native_verdict`**——保留人物 DNA。
3. **汇总所有 `core.hard_blockers`**——列成综合 blocker 列表。
4. **合并 `must_haves_review`**——同一 truth 多席位 flag 冲突时，取最严的 `proposed_criterion`。
5. **读 `seat_specific`**——补充细节（tail_events / anti_patterns / broken_evidence 等）作为“人读补充”。
6. **读 `core.peer_disagreements`**——显式列分歧，不要在综合时强行收敛。

**默认输出顺序**：

1. **主持人结论**（必须在第一屏）：推荐做什么；是否有 hard blocker；下一步是否值得实施。
2. **席位短评汇总**：只列被召开席位，每席 1 行。
3. **冲突与取舍**：最多 3 条；没有真实冲突就写“无关键分歧”。
4. **做完会怎样**（必填，人话段）：如果按主持人结论落地，用户在日常工作里会经历什么具体变化；做不到什么。用最短可理解的形式——通常 2-5 句散文，若议题本身就是"做完前 vs 做完后"的对比结构，两行表格也合适。判断标准是让没读过完整 verdict 的人 30 秒看懂差异，不是凑够字数或避开某种排版。这段把 agent verdict 翻译成"用户侧感觉到的差异"，不是重复 DECISIONS 里的项目名。**段末必须以一行 `**验证信号**：<…>` 收尾**——明确哪些观测值代表"做到了"、哪些代表"没做到"。验证信号缺失 = 愿景式散文，退回重写；签两句都写不出就说明议题不可证伪，回阶段 0.5 重定义。
5. **DECISIONS 表**：

   | 分类 | 内容 | 来源 |
   |---|---|---|
   | `locked` | D-01 ... D-0N | 阶段 0.5 must_haves（含阶段 1.5 修订后的 v2）+ 阶段 3 用户拍板 |
   | `deferred` | ... | 阶段 0.5 out_of_scope + 用户拍板延后项 |

   `discretion` 档（执行席位自行判断的实施细节）仍在内部 audit trail 保留，但**不进默认 DECISIONS 表**——用户明确说“展开实施细节 / 展开 discretion”时才显示。

6. **等用户确认**：用户未明示 go 之前，禁止进入阶段 4。

full 模式可额外展示非代码评议表、代码层表、候选方案表和完整 YAML；Quick 模式只在用户要求时展开。

### 阶段 4 — 实施

用户确认后，**按运行时条件分支**推进。共享 workflow 只定义抽象 orchestration 动作，不写死 Claude / Codex 的具体调用语法。

- `continue_existing_agent(agent_id, message)`：向已有实现席位续跑，保留阶段 2 的内部状态
- fallback：新起同 seat agent，并完整注入阶段 2 原文与锁定方案

#### 路径 A · 续跑同一实现席位（首选）

orchestrator 在阶段 4 先检查当前 runtime 是否支持 `continue_existing_agent(agent_id, message)`。**如果支持**，优先续跑同一个 `linus_id`。

续跑消息最少包含：

- 方案已锁定：`<细到文件/函数级别>`
- 按阶段 2 的可行性建议实施
- 完成后按当前项目 `AGENTS.md` / `CLAUDE.md` 定义的自审清单执行
- 实施后不要 commit，等用户验证通过

优点：保留 Linus 阶段 2 的完整内部状态 + 对话历史，prompt 最短。

#### 路径 B · 新起同 seat agent + 完整上下文注入（fallback）

**同 agent 续跑不可用**时，改为新起同一个实现席位，并完整注入上下文。

注入内容最少包含：

- 议题原文
- 已锁定方案：`<细到文件/函数级别>`
- 阶段 2 Linus 可行性评审原文
- 非代码评议席位结论摘要
- 完成后按当前项目 `AGENTS.md` / `CLAUDE.md` 自审
- 实施后不要 commit，等用户验证通过

**关键**：阶段 2 Linus 原文必须**完整粘贴**，不得摘要——他需要自己上一轮的具体判断才能延续可行性结论。

#### 路径自动切换

两路径语义等价。入口 adapter 负责把抽象动作翻译成各 runtime 的 primitive；共享 workflow 不再为运行时差异单独改文案。

Linus 返回实施报告后默认给用户短报告：改了什么、验证结果、是否有缺口、是否需要回流圆桌。完整实施原文和 `linus_execution` block 只在用户要求展开时显示。

## 冲突裁决规则

| 冲突类型 | 处理 |
|---|---|
| 非代码评议席位之间分歧（如 Taleb vs Munger / Taleb vs López / Munger vs López） | 可选：若当前 runtime 支持 `continue_existing_agent(agent_id, message)`，让他们互相 push back 一轮；不支持就由 orchestrator 呈分歧表给用户拍板。典型 Taleb vs López 分歧：Taleb 认为金融不能科学化，López 认为应当科学化——路径相反，不强行合并。 |
| Linus 说“代码层 broken” | 回阶段 1 问相关评议席位：是否有等价路径可绕开该 broken 点。 |
| 非工程要求 × 代码无法干净落地 | orchestrator + 用户拍板：重构承载 / 降级需求 / 放弃本次改动。 |
| Linus 阶段 2 建议与非代码结论矛盾 | orchestrator 明确呈现给用户，不擅自取舍。 |

## 硬约束（任何情况不得违反）

1. **绝不篡改 agent 判断**：orchestrator 可以默认压缩成短评卡，但不得软化、反向改写、遗漏 hard blocker；用户要求展开时必须提供完整原文和 YAML。
2. **绝不跳阶段**：阶段 3 用户未确认前不得进阶段 4。
3. **实施阶段优先续跑同一 agent**：runtime 若支持 `continue_existing_agent(agent_id, message)` 就走阶段 4 路径 A；没有则走路径 B（新起同 seat agent + 阶段 2 原文**完整注入**，不得摘要）。
4. **项目纪律由 agent 自己发现**：不在 workflow 里硬编码项目特定规则。Linus 启动时会自动 Read 当前项目的 `AGENTS.md` / `CLAUDE.md`。
