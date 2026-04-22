# Roundtable Seat Registry

> 这是 `/zhuzi:roundtable` 的人读席位权威表。Quick headings、seat/stages/route、seat-specific 机器合同以 `zhuzi/manifests/roundtable-contract.json` 为准；若 `roundtable.md`、README、AGENTS、agent 描述段漂移，以 manifest 与本文件交叉校验结果为准。

## 当前席位

<!-- GENERATED:seat_registry_current_seats:start -->
| 席位 | agent | 职责 | 默认 `stages` | 擅长领域（议题匹配关键词） |
|---|---|---|---|---|
| 风险结构 | `taleb-reviewer` | 尾部风险、fragility、凸性、barbell、skin in the game | `[1]` | 不确定性 / 尾部风险 / 脆弱性 / 凸性 / ruin risk / barbell / 冗余 / 选择权 / 依赖链风险 / skin-in-the-game / 厚尾分布 |
| 决策质量 | `munger-reviewer` | 愚蠢清单、认知偏误、激励结构、能力圈、机会成本 | `[1]` | 投资决策 / 商业判断 / 产品策略 / 组织决策 / 认知偏误审视 / 能力圈边界 / 机会成本 / 安全边际 / 激励结构 / 护城河 / Lollapalooza |
| 证据质量 | `lopezdeprado-reviewer` | 研究诚信、associational vs causal、实验/评估设计、backtest overfitting、DSR/PBO/CPCV | `[1]` | 研究方法论 / 实验设计 / 因果声明 / benchmark / A-B test / eval / data leakage / backtest overfitting / p-hacking / multiple testing / specification error / Deflated Sharpe / Purged K-Fold / CPCV / 研究流程诊断 |
| 解释清晰度 | `feynman-reviewer` | 术语去魅、命名 vs 机制、例子、可验证解释、cargo cult 检测 | `[1]` | spec / API contract / 指标口径 / 时间语义 / 术语定义 / 文档解释 / 命名是否冒充理解 / AI 易误读表述 |
| 代码 | `linus-engineer` | 架构、可行性、review、重构、实施、good taste | `[2]` 或 `[1,2]` | 软件架构 / 数据结构 / API 边界 / 并发 / 性能 / 可靠性 / 代码实施 / 可行性评估 / 重构 / 工程纪律 / 技术选型 / good taste 审视 |
<!-- GENERATED:seat_registry_current_seats:end -->

## 召开纪律

- 语义匹配优先于关键词精确命中。`激励结构` 和 `激励设计` 算同一域。
- Quick 模式下评议席位默认不超过 3 个；超过时优先保留最可能发现 hard blocker 或真实分歧的席位。
- `N >= 1` 合法。`N = 0` 时停止流水线；`N = 1` 时退化为单席位 roundtable。

## 默认 `stages` 规则

<!-- GENERATED:seat_registry_stage_rules:start -->
| 席位 | 策略/投资/商业/组织决策 | 研究/实验/因果评估 | 纯代码实施议题 | 工程决策议题 | 混合议题 |
|---|---|---|---|---|---|
| Taleb | 含不确定性 / 尾部 / 脆弱性 → `[1]` | 仅在评估暴露尾部风险时 `[1]` | 弃权 | 仅在工程方案有系统性脆弱性时 `[1]` | `[1]` |
| Munger | 含判断质量 / 激励 / 能力圈 / 机会成本 → `[1]` | 仅在指标激励或研究者偏误关键时 `[1]` | 弃权 | 弃权 | `[1]` |
| López | evidence claim 关键时 `[1]` | 含实验 / 因果 / benchmark / eval / 回测 → `[1]` | 弃权 | 弃权 | `[1]` |
| Feynman | 含术语定义 / 决策说明 / 口径解释清晰度 → `[1]` | 含指标口径 / 时间语义 / 方法解释 → `[1]` | 仅在 API contract / 命名 / 抽象边界讲不清时 `[1]` | 含接口语义 / 抽象命名 / spec clarity → `[1]` | 议题需要先讲清 contract / 术语 / 验证口径 → `[1]` |
| Linus | 弃权 | 弃权 | `[2]` | `[1,2]` | `[1,2]` |
<!-- GENERATED:seat_registry_stage_rules:end -->

## 补充规则

### López 必召开触发词

<!-- GENERATED:seat_registry_lopez_must_call:start -->
议题含 `研究方法论 / 实验设计 / benchmark / eval / A-B test / 因果声明 / causal claim / data leakage / selection bias / backtest 审视 / 因子诚信 / 过拟合诊断 / trial 披露 / CV 方法 / Sharpe deflation / factor zoo / specification / Sisyphus workflow` 任一关键词时，López 必召开，即使议题不是量化金融。
<!-- GENERATED:seat_registry_lopez_must_call:end -->

### Linus `stages=[1,2]`

<!-- GENERATED:seat_registry_linus_dual_stage:start -->
- 阶段 1：工程视角评议题，关注 good taste、数据结构、anti-pattern，不评判当前 codebase 是否承载得住。
- 阶段 2：可行性 gate，吸收阶段 1 和其他席位结论，评估能否干净落地。
<!-- GENERATED:seat_registry_linus_dual_stage:end -->

## 扩席位维护清单

> 顺序严格：**前置判断 → 判断填字段 → 机械生成文件 → 跑守门**。每步标 **（判断）** 需问用户/查人物素材决定，**（机械）** 可照着现有席位 copy-modify 直接做。A 类思维顾问才走全流程；B 类聊天娱乐（如 `luxun-zawen`）只做 Step 1 后停。

### 前置判断（判断）

- [ ] **A 类 vs B 类**：skill 是否输出可进入决策的结构化判断？是 → A 类，走全流程；只做语言改写 / 娱乐 → B 类，只完成 Step 1 + Step 4 的 skills/INVENTORY/manifest 三处，不建 seat / agent
- [ ] skill 已在 `skills/<family>-<signature>/SKILL.md` 就位（如 `taleb-antifragile`）。命名建议：`<family>` = 人物姓氏 / 代表标签，`<signature>` = 人物核心方法论词（如 `antifragile` / `checklist` / `engineer` / `scientist` / `zawen`），不使用 nuwa 默认的 `-perspective` 后缀

### Step 1（机械）— skill 进仓库

- [ ] 把 nuwa 产物从 `~/.claude/skills/<nuwa-output>/` 移到 `skills/<family>-<signature>/`
- [ ] SKILL.md frontmatter 中 `description` 的 UTF-8 字节数 ≤ 1024（Codex 限制，`check_consistency.py` 会拦）

### Step 2（判断）— 设计席位字段（仅 A 类）

对 A 类必做。以下每项都是**人工决定**，不能自动推。填完后进 Step 3-4：

- [ ] **席位名**：评议型用 `<family>-reviewer`，实施型用 `<family>-engineer`
- [ ] **verdict root key**：通常 `<family>_verdict`；实施型（如 Linus）用 `<family>_feasibility`
- [ ] **native verdict 词汇表**（2-5 词）：反映人物思想核心极性。参考：taleb 的 `fragile/robust/antifragile`、munger 的 `pass/revise/kill`、linus 的 feasibility 系。提示：从 skill 心智模型第 1 条找核心术语
- [ ] **route 映射**：每个 native verdict 映射到 `go` / `go_with_conditions` / `revise_must_haves` / `kill` 之一
- [ ] **seat_specific 必填字段**（3-6 个）：把人物独特方法论翻译成 YAML 槽位。例：taleb 的 `tail_events_breaking_must_haves`、munger 的 `lollapalooza_stack`、lópez 的 `claim_classification`
- [ ] **默认 stages 规则**：这个人物在「策略决策 / 研究评估 / 纯代码实施 / 工程决策 / 混合议题」5 种场景下各弃权 / `[1]` / `[1,2]`，依据是人物真实专长
- [ ] **越权边界**：跟现有 4 席（Linus / Munger / Taleb / López）哪些话题重合？重合点由谁让路？写进 seat contract 的「## 越权边界」
- [ ] **skill/agent 路由护栏**：standalone 场景（`#<family>` / `X 视角`）用 skill，roundtable 场景用 agent。seat contract「## 适用范围」和 agent description 两侧都必须明示

### Step 3（机械）— 生成三个文件

从最接近的现有席位 copy-modify 并替换 family-specific 内容：

- [ ] `zhuzi/seats/<seat>.md` — 评议型参考 `zhuzi/seats/taleb-reviewer.md`，实施型参考 `zhuzi/seats/linus-engineer.md`；手写职责/边界/纪律，保留 `## 输出契约` 生成块 marker
- [ ] `runtimes/claude/agents/<seat>.md` — 参考同人物的 Claude adapter（薄；只装载 skill + seat contract + schema）
- [ ] `runtimes/codex/agents/<seat>.md` — 参考同人物的 Codex adapter（薄；必须含 `{{ZHUZI_SKILL_ROOT}}` / `{{ZHUZI_SHARED_ROOT}}` 模板路径和 `./skills/...` / `./zhuzi/...` 仓库 fallback 两组路径）

### Step 4（机械）— 更新注册表

- [ ] `zhuzi/manifests/roundtable-contract.json` 的 `seats`、stage policy、route、Quick 相关字段与 seat 输出契约补齐
- [ ] 运行 `python3 tools/render_roundtable_contract_docs.py`，刷新本文件、`verdict-schema.md` 与 seat 文件里的 `## 输出契约` 生成段
- [ ] 检查本文件的非生成说明段是否仍成立（例如召开纪律、维护流程、判断/机械边界）
- [ ] `docs/INVENTORY.md` 的 Skills / Agents / Seats 三节加条目，更新每节顶部计数
- [ ] `zhuzi/manifests/shipped-surface.json` 的 `skills` / `agents` / `seats` 三个 family 加条目
- [ ] `tools/check_consistency.py` 会直接读取 manifest 校验 shared seats / adapters / references；确认新字段已被守门覆盖
- [ ] 若引入新 native verdict 或 route 语义，先改 manifest 并 rerender；只有 shared schema 的非生成说明变化时才手改 `zhuzi/references/verdict-schema.md`

### Step 5（机械）— 跑守门

- [ ] `python3 tools/check_consistency.py` 必须 pass
- [ ] 若动了 roundtable surface / shared schema / Codex adapter / 安装路径：`python3 tools/smoke_test_codex_roundtable.py` 必须 pass
