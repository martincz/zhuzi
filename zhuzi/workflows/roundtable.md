# Roundtable Workflow

> 这是 `/zhuzi:roundtable` 的权威 workflow。命令入口负责装载，本文件只负责议事流程。
>
> **输出形态由 `templates/roundtable-quick.md` 负责**——本文件不再维护一份排版规则。Quick headings、seat/stages/route、seat-specific 机器合同以 `zhuzi/manifests/roundtable-contract.json` 为准。

## 流水线性质

- 支持 **N 席位召开（N ≥ 2）**——阶段 0.5 扫议题关键词匹配 `seat-registry.md` 的"当前席位"表，只 spawn 有资格的席位。弃权席位不产出 YAML。
- N=0 / N=1 的路由由阶段 0.5 Step 0 处理（详见下文"召开人数路由"）。
- 无代码席位时阶段 2（代码可行性）dispatch 不触发。

## 默认交互契约

圆桌默认走 **Quick Roundtable**：内部保留完整阶段、原文和 YAML，用户界面只展示能帮助决策的短读内容。只有用户显式说"完整圆桌 / strict / full / 展开原文 / 展开 YAML"时，才展示完整席位原文和完整协议细节。

输出形态以 `templates/roundtable-quick.md` 的渲染约定和骨架为准——本 workflow 只描述"什么时候说什么、在哪里 gate"，不重复维护标点、cell 长度、table 形态等排版细节。

**议事侧硬约束**（不在 template 里说的部分）：

- 第一屏先给主持人结论，不先铺流程。
- 阶段 1 评议席位默认期望 3 个（`review_seat_soft_count`）；命中超过时**全部并行 spawn，不砍席**——选席判断本来就在 orchestrator 看 verdict 之前不可执行。命中 ≥ 4 时议题卡末尾加一行 hint「本议题命中 N 席评议（默认期望 3），Quick 短评 table 会变长」让用户知道而已。
- 默认 `must_haves.truths` 1-3 条；只有 full 模式或议题天然很大时才放宽到 5 条。
- agent 原文和 YAML 是机读证据，不是默认阅读材料；默认只在"展开原文 / 调试 / 审计"请求下显示。
- **绝不篡改 agent 判断**：orchestrator 可以默认压缩成短评卡，但不得软化、反向改写、遗漏 hard blocker。

## 内部流水线（严格按阶段推进，外部默认短读）

### 阶段 0.5 — 议题契约定义（orchestrator）

spawn 任何席位**之前**，orchestrator 完成三步。

#### Step 0 · 席位召开判定

扫议题关键词 + `seat-registry.md` 的"当前席位"表与默认 `stages` 规则 → 匹配产出召开名单（**含每席位 `stages` 在哪些阶段出场**）+ 弃权名单 + 理由。**orchestrator 主动决定，不为每次召开单独问用户**（用户在 Step 2 一起确认/override）。

呈现形态按 template 骨架的"议题卡"段；本文件不再重复维护字段排列。

**召开人数路由**：

- **N=0**：无席位匹配。停流水线，建议用户改议题描述或直接和 orchestrator 对话。
- **N=1**：默认**短路退出 roundtable**——roundtable 的存在意义是保留分歧，单席位议事是 cargo cult。orchestrator 给一条引导：「本议题只命中 `<seat>` 一个席位。建议直接用 `<skill-name>` skill（`#<trigger>` 或 `<persona> 视角` 触发），不开圆桌。若坚持要走结构化议事，回复『强制开圆桌』。」用户回复"强制开圆桌"/"force roundtable" 才继续走 Step 1；否则退出。也可改用 `/zhuzi:quick` 多视角短读。
- **N≥2**：进 Step 1。

**议事侧约束**：

- 席位语义匹配 ≠ 关键词精确命中——"激励结构"和"激励设计"算同一域，orchestrator 按语义判断。
- 阶段 1 评议席位默认期望 3 个；语义命中超过 3 个时**全部召开**，不在 spawn 之前砍席（哪个席位会发现 hard blocker 必须 spawn 后才知道）。
- **目标行 = 可交付产出**——议题卡的"目标"必须是本轮结束时可指给别人看的产物（决策表 + 验证信号 / contract 修订锁定 / 参数值锁定 / 议题拆分结果）。禁止以"判断 / 讨论 / 评估 / 决定是否 / 审视"开头——那些是**正在做什么**而不是**做完有什么**。若实在写不出产物，多半议题粒度太粗，拆成两条再开。

`stages` 的默认路由、López / Paul Graham 必召开触发词，以及 Linus `stages=[1,2]` 的双阶段语义都以 `roundtable-contract.json` 为机读真相源，并以 `seat-registry.md` 作为人读解释层。

#### Step 1 · must_haves 定义

基于**召开名单的视角**（不给弃权席位预留 truth），把议题翻译成可验证的成功标准。

**机读合同结构（内部保留，不直接展示给用户）**——阶段 1 spawn 席位时注入 prompt、阶段 4 实施时跑 verify、事后 audit trail 追溯用：

```yaml
must_haves:
  truths:            # Quick 默认 1-3 条；full 模式最多 5 条
    - "<例：v28 M1 在 baseline 上 paired bootstrap walpha Δ 下界 > 0>"
    - "<例：d20 hit% 不回退超 1pp>"
  verify_commands:   # 每条 truth 对应的可机器执行验证命令
    - truth: 1
      cmd: "<observable_metric 示例：python3 tools/bench.py --replay-from <baseline>>"
      pass_criterion: "TBD — 待召开席位审阅"
    - truth: 2
      cmd: "<policy_discipline 示例：grep -E '<pattern>' <file>>"
      pass_criterion: "grep 命中 ≥ 1 条且匹配 '<约定措辞>'"
  out_of_scope:
    - "<例：不动某权重表 / 不改某候选池定义>"
```

**呈现形态**按 template 骨架的"什么算过关"段。本 workflow 只列**议事侧硬约束**：

1. **`truths` 只放可验证主张**，两类合法：
   - **observable_metric**：可观测的量化行为（回测 walpha Δ / API p99 / 内存峰值 / bundle 大小 / 错误率 / bootstrap CI 等）
   - **policy_discipline**：可验证的结构性 / 纪律性事实（某文档新增条款且含指定措辞 / 某接口字段存在且类型正确 / 某配置开关默认值符合约定 等）

   禁放 truths：
   - 实施约束（"只改 N 个文件"）→ 走阶段 3 `DECISIONS.locked`
   - 主观项（"代码写得好看"）
   - 流程要求（"跑通编译"）→ 走 `out_of_scope` 默认项

2. **`truths` 数量默认 1-3 条，硬上限 5 条**——Quick 模式超过 3 条删到最关键；超过 5 条说明议题粒度太粗，拆成两个 roundtable。

3. **`pass_criterion` 按 truth 类型分写**：
   - **observable_metric**：orchestrator 原则上打 `TBD — 待召开席位审阅`，交席位在 `must_haves_review.proposed_criterion` 填具体阈值。
   - **policy_discipline**：orchestrator **必须直接写死**判断标准，**不得 TBD**。
   - 纯技术断言（"py_compile 通过" / "HTTP 200" / "lint 无 error"）按 `policy_discipline` 规则，orchestrator 直接写死。

4. **`out_of_scope`** 直接喂给阶段 3 DECISIONS 表的 `deferred` 段。

5. **无法为某 truth 写出 verify 命令时**，先打 `TBD — 需要召开席位确认指标口径`——缺验证标准比议题失败更严重。

6. **`pass_criterion` 禁"程序正义式"描述**——回答"什么状态算通过"，不是"谁说了算 / 怎么达成一致"。

7. **`truths` 过席位必要性预检**——若某 truth 不需要召开席位专业视角才能评估，就不要塞进 `must_haves.truths`，改入 `DECISIONS.locked` 或 `DECISIONS.discretion`。

**空心词禁用**——"真正有价值" / "合理的" / "更好的" 这类词必须替换成可验证标准（"能量化提升" / "风险降低" / "d20 命中率不回退"）。

**小议题例外**：议题是纯代码整理 / 文案 / 修 bug 时，truths 可简化为最小可验证集（例：改动文件 `py_compile` 通过 + 一条针对性断言通过）。这些属于 `policy_discipline truth`，`pass_criterion` 直接写死。

#### Step 2 · 用户确认

Step 0 的议题卡 + Step 1 的"什么算过关"段**一次性呈现**给用户（按 template 骨架渲染）。YAML 机读合同仍在内部保留，用户要才展示。用户四选一：

- **接受全部** → 进阶段 1
- **override 召开名单**（增/减席位）→ orchestrator 调整召开名单 + 基于新名单重定 must_haves → 重呈现 Step 2
- **override must_haves** → 修 truths / verify_commands / out_of_scope → 重呈现 Step 2
- **叫停议题** → 退出 roundtable

### 阶段 1 — 视角并行审议（dispatch: 召开名单有席位 `stages` 含 `1` 时触发）

**按阶段 0.5 Step 0 产出的召开名单**动态 spawn——在同一条消息内**并行** spawn 所有 `stages` 含 `1` 的被召开席位。

- **召开名单有席位 `stages` 含 `1`** → spawn 所有此类席位；弃权席位和 `stages` 不含 1 的席位**都不 spawn**。
- **无席位 `stages` 含 `1`**（纯实施议题，只召开 Linus 且 `stages=[2]`）→ **跳过本阶段**，直接进阶段 2。

**Linus 在阶段 1 出场时**（`stages=[1,2]`）：spawn prompt 明确他做"工程视角评议题"——good taste / 数据结构合理性 / bikeshedding / premature abstraction / anti-pattern 扫描，**不关心当前 codebase 能否承载**（那是阶段 2 的事）。阶段 2 的 Linus spawn 另起，prompt 明确"吸收阶段 1 所有席位结论 + must_haves → 可行性 gate"。两次 spawn 工作不同，不是重复。

**spawn 结构**——所有阶段 1 席位的 spawn prompt 共享同一骨架。**具体话术**（fragility check / 愚蠢清单 / Research Integrity Audit / 解释清晰度审议 / Maker taste / UI 认知诊断 等）**由各席位 seat contract 的「## 审议动作」承载，本 workflow 不复制维护一份**。

每个被召开席位的 spawn prompt 必含：

1. 议题原文（如有相关回测 / 数据 / 研究上下文一并贴上）
2. 阶段 0.5 must_haves YAML（完整粘贴，不摘要）
3. 执行指令："按你启动时读到的 skill + seat contract 的『## 审议动作』执行评议；对每条 `must_haves.truth` 走完审议动作要求的所有维度；原文结尾必须带 YAML verdict block，格式按 seat contract 的『## 输出契约』。"
4. 通用纪律：与其他席位分歧时写入 `peer_disagreements`，不强行收敛；不替主持人拍板。

**最小示例**（taleb-reviewer；其它席位同构，只换 `subagent_type` 与读取的 seat contract）：

```text
Agent(subagent_type="taleb-reviewer", prompt="""
议题: <议题原文>
<若有相关回测/数据/研究上下文一并贴上>

阶段 0.5 must_haves:
<完整粘贴阶段 0.5 产出的 YAML 块>

请按你启动时读到的 skill + seat contract 的「## 审议动作」执行评议：
- 对每条 must_haves.truth 走完审议动作要求的所有维度
- 与其他席位分歧时写入 peer_disagreements，不强行收敛
- 不替主持人拍板
- 原文结尾必须带 YAML verdict block，格式按 seat contract 的「## 输出契约」
""")
```

agent 返回后，orchestrator **先机读 YAML verdict**，默认按 template 的"席位短评"骨架呈现。结论列译表、信心列判据格式、cell 超长拆 `### <席位名> 展开` 段——全部按 template 渲染约定执行，本 workflow 不再列具体形态。

**议事侧呈现底线**：

- `kill` / `too_hard` / `revise_must_haves` / 代码层 `broken` 必须在短评卡直接露出，不得藏到展开内容里。
- 席位 `native_verdict`（`fragile` / `cargo_cult` / `pseudo_scientific` 等）保留在内部 YAML 和原文里——Quick 短评卡只显示路由中文译。
- 用户说"展开原文 / 展开 YAML / strict / full" → 按席位完整展示原文和 YAML。

### 阶段 1.5 — must_haves 修订 gate（条件触发）

扫描阶段 1 所有席位 verdict block 的 `must_haves_challenge.triggered` 字段：

- **全部 `triggered: no`** → 直接进阶段 2，Linus 拿 must_haves v1。
- **任一 `triggered: yes`** → **暂停，走修订流程**。

#### 修订流程

1. orchestrator 汇总所有 `triggered: yes` 席位的 `proposed_revision`，合并成 must_haves v2（多席位冲突时显式标注差异，不擅自取舍）。

2. 按 template 的"阶段 1.5 修订对照表骨架"呈现 v1 vs v2 给用户。

3. **用户五选一**：
   - **接受 v2** → 锁定新版 must_haves，阶段 2 Linus 拿新版
   - **接受部分**（指定哪些 truth 采纳）→ 锁定混合版
   - **保持 v1** → 阶段 2 进行但显式告知 Linus"非代码评议席位建议修订 must_haves 但用户维持 v1"，Linus 在自己的 verdict 里可选择继续 challenge
   - **重开议题** → 流水线终止，回阶段 0.5 重写议题（见下方"重开议题的子议题候选纪律"）
   - **要求 orchestrator 改写 v2 表达** → 不改实质内容，只做去黑话 / 排版重组 / 人话化，回到五选一

#### 重开议题的子议题候选纪律

orchestrator 若基于席位 `spawn_sub_topic` 字段给子议题候选列表，必须遵守：

- **同粒度分组**——候选要么全是"基建/规范重构"（多周尺度），要么全是"具体审计/规则"（2-5 天尺度）；混放两个尺度按 `### 基建层` / `### 具体动作层` 两节展示。
- **每条标注"预估耗时"**——格式 `预估耗时：<X 天> / <X 周>`，禁止"想清楚再来"等空心时间。

#### 阶段 1.5 议事约束

- **禁止** orchestrator 自行合并 challenge 或无视 challenge 强行推进。这是阶段 1.5 的唯一作用：把"席位推翻刚拍板的契约"这个事件升格成协议内置流程。
- **尊重席位侧已分层的 `proposed_revision`**——直接对应 `revised_truth` / `revised_verify_suggestion` / `spawn_sub_topic` 三字段合并，不重新搅成一团。
- v1 vs v2 对照的呈现形态以 template 为准。

### 阶段 2 — 代码可行性评审（dispatch: 召开名单有席位 `stages` 含 `2` 时触发）

- **召开名单有席位 `stages` 含 `2`**（默认为 `linus-engineer`，`stages=[2]` 或 `stages=[1,2]`）→ 把阶段 1 所有席位原文（如有）打包交该席位，**保留 `linus_id` 以便阶段 4 续跑**。
- **无席位 `stages` 含 `2`**（纯策略讨论）→ 跳过本阶段，直接进阶段 3（综合时标注"本议题无代码落地维度，阶段 2 跳过"）。

若 Linus `stages=[1,2]`，他在阶段 1 已有独立 verdict block（`linus_feasibility` with `phase: 1`）——阶段 2 的 spawn prompt 显式提醒他"你阶段 1 已给出工程视角初判，本阶段吸收所有席位结论做可行性 gate，不要重复阶段 1 的 good taste 论证"。

```text
linus_id = Agent(subagent_type="linus-engineer", prompt="""
议题: <议题原文>

阶段 1 席位原文（按本次实际召开名单逐个粘贴）：

=== <Seat A> ===
<Seat A 原文>

=== <Seat B> ===
<Seat B 原文>

...

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

Linus 返回后默认按 template 的代码席短评骨架呈现。完整原文只在用户要求展开或进入 full 模式时显示。

### 阶段 3 — 综合对齐（orchestrator 主持）

orchestrator 做综合，**优先读每个席位原文末尾的 YAML verdict block**（机读），再补文字表达。

**阅读顺序**：

1. **先扫 `core.route`**——聚合所有席位的路由
2. **读 `seat_native_verdict`**——保留人物 DNA
3. **汇总所有 `core.hard_blockers`**——列成综合 blocker 列表
4. **合并 `must_haves_review`**——同一 truth 多席位 flag 冲突时，取最严的 `proposed_criterion`
5. **读 `seat_specific`**——补充细节（tail_events / anti_patterns / broken_evidence 等）作为人读补充
6. **读 `core.peer_disagreements`**——显式列分歧，不在综合时强行收敛

**默认输出顺序**（具体形态见 template 骨架）：

1. **主持人结论**（必须在第一屏）
2. **席位短评汇总**——每席 1 行；分歧只在 table 的"分歧"列里出一次，文末**不**额外加"明确分歧"段
3. **冲突与取舍**——最多 3 条；没有真实冲突写"无关键分歧"。这段是 orchestrator 综合判断（哪方值得听、为什么），和短评 table 的"分歧"列不重复
4. **做完会怎样**——必填人话段：用户日常工作里会经历什么具体变化、做不到什么。**段末必须以 `**验证信号**：<…>` 收尾**——验证信号缺失 = 愿景式散文，退回重写；写不出就说明议题不可证伪，回阶段 0.5 重定义
5. **DECISIONS 表**——`locked` + `deferred`；`discretion` 默认不渲染（用户说"展开 discretion"才显示）
6. **主持人观察（可选）**——只在能直接帮助用户拍板时才出（结论一致性 / 分歧集中点 / 信心分布）。**禁止**建议"推荐选哪个"——只陈述客观信号，不替用户选
7. **等用户确认**——用户未明示 go 之前，禁止进入阶段 4

full 模式可额外展示完整 YAML、非代码评议表、代码层表、候选方案表；Quick 模式只在用户要求时展开。

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
| 非代码评议席位之间分歧（如 Taleb vs Munger / Taleb vs López / Munger vs López） | 可选：若当前 runtime 支持 `continue_existing_agent(agent_id, message)`，让他们互相 push back 一轮；不支持就由 orchestrator 呈分歧表给用户拍板。典型 Taleb vs López 分歧：Taleb 认为金融不能科学化，López 认为应当科学化——路径相反，不强行合并 |
| Linus 说"代码层 broken" | 回阶段 1 问相关评议席位：是否有等价路径可绕开该 broken 点 |
| 非工程要求 × 代码无法干净落地 | orchestrator + 用户拍板：重构承载 / 降级需求 / 放弃本次改动 |
| Linus 阶段 2 建议与非代码结论矛盾 | orchestrator 明确呈现给用户，不擅自取舍 |

## 硬约束（任何情况不得违反）

1. **绝不篡改 agent 判断**：orchestrator 可以默认压缩成短评卡，但不得软化、反向改写、遗漏 hard blocker；用户要求展开时必须提供完整原文和 YAML。
2. **绝不跳阶段**：阶段 3 用户未确认前不得进阶段 4。
3. **实施阶段优先续跑同一 agent**：runtime 若支持 `continue_existing_agent(agent_id, message)` 就走阶段 4 路径 A；没有则走路径 B（新起同 seat agent + 阶段 2 原文**完整注入**，不得摘要）。
4. **项目纪律由 agent 自己发现**：不在 workflow 里硬编码项目特定规则。Linus 启动时会自动 Read 当前项目的 `AGENTS.md` / `CLAUDE.md`。
5. **输出形态以 template 为准**：本 workflow 不维护排版规则。改 Quick 输出形态请改 `templates/roundtable-quick.md`，不要在本文件加 prose 补丁。
