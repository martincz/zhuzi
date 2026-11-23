# Roundtable Seat Registry

从 [机器合同](../manifests/roundtable-contract.json) 生成的席位领域和阶段说明。按议题实质匹配。短读取擅长领域，正式圆桌另用阶段和必召开规则。

## 当前席位

<!-- GENERATED:seat_registry_current_seats:start -->
| 席位 | agent | 职责 | 默认 `stages` | 擅长领域（议题匹配关键词） |
|---|---|---|---|---|
| 风险结构 | `taleb-reviewer` | 尾部风险、fragility、凸性、barbell、skin in the game | `[1]` | 不确定性 / 尾部风险 / 脆弱性 / 凸性 / ruin risk / barbell / 冗余 / 选择权 / 依赖链风险 / skin-in-the-game / 厚尾分布 |
| 决策质量 | `munger-reviewer` | 愚蠢清单、认知偏误、激励结构、能力圈、机会成本 | `[1]` | 投资决策 / 商业判断 / 产品策略 / 组织决策 / 认知偏误审视 / 能力圈边界 / 机会成本 / 安全边际 / 激励结构 / 护城河 / Lollapalooza |
| 证据质量 | `lopezdeprado-reviewer` | 研究诚信、associational vs causal、实验/评估设计、backtest overfitting、DSR/PBO/CPCV | `[1]` | 研究方法论 / 实验设计 / 因果声明 / benchmark / A-B test / eval / data leakage / backtest overfitting / p-hacking / multiple testing / specification error / Deflated Sharpe / Purged K-Fold / CPCV / 研究流程诊断 |
| 解释清晰度 | `feynman-reviewer` | 术语去魅、命名 vs 机制、例子、可验证解释、cargo cult 检测 | `[1]` | spec / API contract / 指标口径 / 时间语义 / 术语定义 / 文档解释 / 命名是否冒充理解 / AI 易误读表述 |
| Maker 视角 | `paul-graham-reviewer` | 创业 / 产品 taste、PMF 真伪、maker vs manager 判断、essay / pitch 评审、Founder Mode 检测 | `[1]` | 创业决策 / 产品方向 / PMF / 创始人评估 / essay 或 pitch 评审 / 职业与人生选择 / Founder Mode vs Manager Mode 组织问题 |
| UI/UX 认知诊断 | `don-norman-reviewer` | discoverability / feedback / conceptual model 三件套审查、affordance vs signifier、slip vs mistake、可访问性 | `[1]` | UI 评审 / UX 评审 / 用户体验 / 产品界面 / discoverability / affordance / signifier / mapping / feedback / conceptual model / mental model / Gulf of Execution / Gulf of Evaluation / slip vs mistake / Norman door / 可访问性 / 无障碍设计 / dark patterns / 自动化交接界面 |
| 代码 | `linus-engineer` | 架构、可行性、review、重构、实施、good taste | `[2]` 或 `[1,2]` | 软件架构 / 数据结构 / API 边界 / 并发 / 性能 / 可靠性 / 代码实施 / 可行性评估 / 重构 / 工程纪律 / 技术选型 / good taste 审视 |
<!-- GENERATED:seat_registry_current_seats:end -->

## 默认 `stages` 规则

<!-- GENERATED:seat_registry_stage_rules:start -->
| 席位 | 策略/投资/商业/组织决策 | 研究/实验/因果评估 | 纯代码实施议题 | 工程决策议题 | 混合议题 |
|---|---|---|---|---|---|
| Taleb | 含不确定性 / 尾部 / 脆弱性 → `[1]` | 仅在评估暴露尾部风险时 `[1]` | 弃权 | 仅在工程方案有系统性脆弱性时 `[1]` | `[1]` |
| Munger | 含判断质量 / 激励 / 能力圈 / 机会成本 → `[1]` | 仅在指标激励或研究者偏误关键时 `[1]` | 弃权 | 弃权 | `[1]` |
| López | evidence claim 关键时 `[1]` | 含实验 / 因果 / benchmark / eval / 回测 → `[1]` | 弃权 | 弃权 | `[1]` |
| Feynman | 决策论证怀疑是口号 / 名词遮蔽机制 / 权威代替证据 → `[1]` | 指标或口径怀疑是 cargo cult 或 AI 易误读 → `[1]` | 仅在命名冒充机制 / 接口语义被黑话遮蔽时 `[1]` | spec 含未定义术语 / 虚假简化 / 类比根未解释 → `[1]` | 议题存在未验证主张伪装成 contract 的风险 → `[1]` |
| Paul Graham | 含创业 / 产品 / 创始人 / PMF / Founder Mode → `[1]` | off（研究诚信让给 López） | off（代码让给 Linus） | 含产品方向 / maker-manager / spec 或 ADR 的 taste 与说服力判断 → `[1]` | 议题含创业 / 产品 / essay / spec 评审或说服力维度 → `[1]` |
| Norman | 含产品界面 / 用户体验 / UI 评审 / 可用性归因争议 → `[1]` | 评估口径含用户界面 / 用户测试时 `[1]` | off（纯后端不评，UI 代码归 hybrid） | 含 UI / CLI / API surface / 错误信息 / 默认值 → `[1]` | 议题含 UI / UX / 可访问性 / 用户错误归因 → `[1]` |
| Linus | 弃权 | 弃权 | `[2]` | `[1,2]` | `[1,2]` |
<!-- GENERATED:seat_registry_stage_rules:end -->

## 补充规则

### 正式圆桌必召开领域

<!-- GENERATED:seat_registry_lopez_must_call:start -->
议题实质涉及 `研究方法论 / 实验设计 / benchmark / eval / A-B test / 因果声明 / causal claim / data leakage / selection bias / backtest 审视 / 因子诚信 / 过拟合诊断 / trial 披露 / CV 方法 / Sharpe deflation / factor zoo / specification / Sisyphus workflow` 所指的领域时，López 必召开，即使议题不是量化金融。

议题实质涉及 `创业方向 / 产品方向 / PMF / product-market fit / 创始人评估 / founder 靠谱吗 / pitch 评审 / pitch deck / essay 评审 / essay 写作 / 写作 taste / spec taste / ADR taste / 说服力评审 / Founder Mode / Manager Mode / default alive / default dead / Stay Upwind / Keep Identity Small / superlinear returns / maker 还是 manager` 所指的领域时，Paul Graham 必召开，触发创业 taste / essay 评审场景时必召开，和 Munger（偏误 / 激励）、Taleb（尾部风险）形成互补分工。

议题实质涉及 `UI 评审 / UX 评审 / design review / 可用性问题 / 为什么用户犯错 / discoverability / affordance / signifier / mapping / feedback 设计 / conceptual model / mental model / Gulf of Execution / Gulf of Evaluation / slip 还是 mistake / Norman door / 用户体验 / 产品界面 / 可访问性 / 无障碍设计 / dark pattern / 错误信息设计 / default value / 用户操作失误 / 用户没培训好` 所指的领域时，Norman 必召开，触发 UI/UX 评议或可用性归因争议时必召开，与 Linus（代码品味）、Feynman（spec 清晰度）、Paul Graham（产品 taste）形成互补分工。
<!-- GENERATED:seat_registry_lopez_must_call:end -->

### Linus `stages=[1,2]`

<!-- GENERATED:seat_registry_linus_dual_stage:start -->
- 阶段 1：工程视角评议题，关注 good taste、数据结构、anti-pattern，不评判当前 codebase 是否承载得住。
- 阶段 2：可行性 gate，吸收阶段 1 和其他席位结论，评估能否干净落地。
<!-- GENERATED:seat_registry_linus_dual_stage:end -->
