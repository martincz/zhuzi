---
description: 圆桌会议模式——多席位协作审议（策略席 + 代码席）。席位可扩，流水线通用。
argument-hint: [议题/策略/提案/需求描述]
---

# 圆桌会议（Roundtable）

用户开启圆桌会议。**议题**：

$ARGUMENTS

---

## 当前席位

| 席位 | agent | 职责 | 域 |
|---|---|---|---|
| 策略 | `taleb-reviewer` | 尾部风险、fragility、barbell、skin in the game | 策略层 |
| 策略 | `munger-reviewer` | 愚蠢清单、认知偏误、激励结构、能力圈 | 策略层 |
| 代码 | `linus-engineer` | 架构、可行性、review、重构、实施、good taste | 代码域全权 |

**扩席位**：新建 `~/.claude/agents/<name>.md`（或项目级覆盖放 `.claude/agents/`），在本文件"当前席位"表 + 阶段 1 的 spawn 列表加一行即可。不拆新 command——圆桌会议本就是开放席位的隐喻。

---

## 流水线（严格按阶段推进，禁止跳阶段）

### 阶段 0.5 — 议题 must_haves 定义（主 Claude）

spawn 任何席位**之前**，主 Claude 先把议题翻译成可验证的成功标准，输出如下段（原文呈现给用户，让用户在讨论开始前就能叫停/修正）：

```yaml
must_haves:
  truths:            # 3-5 条 observable outcome，议题成功时必须全部成立
    - "<例：v28 M1 在 baseline 上 paired bootstrap walpha Δ 下界 > 0>"
    - "<例：d20 hit% 不回退超 1pp>"
    - "<例：Spearman ρ 与 walpha 方向一致>"
  verify_commands:   # 每条 truth 对应的可机器执行验证命令
    - truth: 1
      cmd: "python3 tools/historical_selection_eval.py --replay-from <baseline> --overrides <overrides>"
      pass_criterion: "TBD — 待策略席审阅"       # 主 Claude 不拍阈值，打 TBD 让策略席在 verdict block 里填
    - truth: 2
      cmd: "<...>"
      pass_criterion: "TBD — 待策略席审阅"
  out_of_scope:      # 明示本议题不覆盖什么，避免席位/Linus 跑偏
    - "<例：不动 PHASE_FUND 权重>"
    - "<例：不改候选池定义>"
```

**硬约束（任一违反则 must_haves 段不合格，必须重写）：**

1. **`truths` 只放 observable outcome**——成功时必须成立的**可观测行为**（IQ 典型 = 回测指标 / bootstrap CI / replay 产出）。
   - ❌ 不放实施约束（"只改 2 个文件"、"不引入新依赖"）→ 这些走阶段 3 DECISIONS.locked
   - ❌ 不放主观项（"代码写得好看"、"文档清楚"）
   - ❌ 不放流程要求（"跑通 py_compile"走 out_of_scope 默认项，不是 truth）

2. **`truths` 数量 3-5 条硬上限**——超过 5 条说明议题粒度太粗，必须拆成两个 roundtable 分别开。

3. **`verify_commands.pass_criterion` 主 Claude 原则上打 `TBD`**——阈值（"CI 下界 > 0.3pp"、"hit% 不跌超 1pp"）是策略判断，交策略席在 verdict block 的 `must_haves_sanity`（Taleb）/ `must_haves_integrity`（Munger）里填具体建议。
   - 例外：truth 是纯技术断言（"py_compile 通过"、"接口返回 200"）时主 Claude 可直接写死 pass_criterion。

4. **`out_of_scope`** 直接喂给阶段 3 DECISIONS 表的 `deferred` 段。

5. **无法为某 truth 写出 verify 命令时**，先打 `TBD — 需要策略席确认指标口径`——缺验证标准比议题失败更严重。

**小议题例外**：议题是纯代码整理/文案/修 bug 时 truths 可以简化成 "改动过的文件 `py_compile` 通过 + `<针对性最小测试>` 通过"，不要硬凑回测指标。

### 阶段 1 — 策略并行审议

同一条消息内**并行** spawn 所有策略席位（多个 Agent tool call 并列写）：

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
```

两个 agent 返回后：**原文完整呈现给用户，不得转述或软化**。

### 阶段 2 — 代码可行性评审

把阶段 1 的所有策略席原文打包交 Linus，**保留 `linus_id` 以便阶段 4 续跑**：

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

你（主 Claude）做综合，**优先读每个席位原文末尾的 YAML verdict block**（机读），再补文字表达。输出：

1. **策略层**：所有策略席的一致点 vs 分歧点（表格，verdict / blocker / key concern 三列）
2. **代码层**：Linus 的 sane/broken 判断 + 可行性建议
3. **最终方案候选表**：列 2-3 个可行路径 + 权衡 + 推荐项
4. **DECISIONS 表**（用户拍板时同步定下，阶段 4 的输入）：

   | 分类 | 内容 | 来源 |
   |---|---|---|
   | `locked`（必须实施，Linus 不得越过） | D-01 ... D-0N | 阶段 0.5 must_haves + 阶段 3 用户拍板 |
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
| 策略席之间分歧（如 Taleb vs Munger） | 可选：SendMessage 让他们互相 push back 一轮；或主 Claude 呈分歧表给用户拍板 |
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
