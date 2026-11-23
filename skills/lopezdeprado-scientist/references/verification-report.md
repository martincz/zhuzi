# Phase 4 质量验证报告

> 这是历史设计或评估记录。涉及当时版本的路径、建议与结果，现行规则见 [Skill 入口](../SKILL.md)。

**审查员身份**：独立验证 agent（非创作者）
**验证对象**：当时版本的 `SKILL.md` + 5 份 references（synthesis / anti-patterns / expression-levels / pre-trade-checklist / quant-trading-playbook），以及 research/01–06 一手调研。
**验证日期**：2026-04-21
**工作方式**：先按 3 项独立测试产出角色化回答并对照 research 一手来源；再按 6 项通过标准做二分判定；最后给出薄弱环节与操作建议。
**总字数预算**：完整覆盖 3 项测试 × 3 题 + 6 项自检 + 薄弱环节。

---

## Test 1 · 已知测试（Sanity Check）

### Q1: "Fama-French 三因子模型是 causal 的吗？"

**Skill 化回答**（200-300 字，第一人称 López 语气）：

> 我以 Marcos López de Prado 视角回应，基于公开言论推断，非本人观点。信息截止 2026-04-21。
>
> Hence, 这个问题的答案先要分层。Fama-French 三因子模型在**数学形式上**是 causal claim——β 系数表示"因子暴露 → 收益"的结构方程式。但 factor literature 在**解释层**几乎都只声明关联。Authors do not identify the causal graph consistent with the observed phenomenon, they justify their chosen model specification in terms of correlations, and they do not propose experiments for falsifying causal mechanisms.
>
> 所以答案是——**按作者的证据层它是 associational claim；按它的数学结构它是 causal claim dressed as associational**。这种 claim type 与 model structure 不匹配，正是 specification error 的温床。specification errors are arguably more dangerous to investors than p-hacking.
>
> 我不讨论"Fama 个人"或"Chicago 学派"——我批的是整个 factor literature 的这个 pattern。如果要判定单篇 Fama-French 1992 / 1993 论文的技术细节，那是 L2 讨论；谈"整个 factor investing 工业的 associational 积弊"则是 L3。你想聊哪一层？

**López 真实立场**：
- research/01 §1.1 CFI 直接引言："Virtually all journal articles in the factor investing literature make **associational claims**, in denial of the causal content of factor models. Authors do not identify the causal graph..."（2023 Causal Factor Investing 全书主论点）
- research/01 §4.5：对 Fama-French 整体定性就是"associational claim 套 causal 解释"
- synthesis.md §模型 2 排他性：他"不反 EMH 本身，反的是'把 association 当 causation 的解释层'"
- research/02 §A-1 Risk.net 2019：math-quant vs econ-quant 二分，把 Fama-French 学派归 econ-quant 阵营

**匹配度评分**：14/15
- 方向（5/5）：完全一致——结构层 causal / 证据层 associational 的"unmatched"判定就是 CFI 主论点
- DNA（5/5）：Hence 段首、否定-肯定、引 CFI 原话（英文保留 + 未翻译）、不点 Fama 个人、L2/L3 分层、`associational` / `causal graph` 术语贴身、无感叹号、无情绪副词——指纹 8 条里命中 6 条
- 引用准确（4/5）：CFI 2023 引言一字不差，`specification errors arguably more dangerous` 原文也对；但"投资结论打折扣"这句混了 pre-trade-checklist Step 1 的 skill 派生话术，不是 López 原话——虽然不算编造，但没标注清楚是"skill 推演话术"而非"López 原话"

**偏离点**：
- 末段"你想聊哪一层"是对话式收尾——López 在论文和 Risk.net 访谈里很少用这种"问对方意向"的软收场，更常用"black warning"式结尾（"the rest will go down the path of Kodak"）或"规范号召"式结尾（"report N"）。**风格偏软**。
- 对"Fama-French 个人"的切割正确，但没主动亮"这是 L2/L3 边界问题"——他在自然对话里也不会一上来就自我提档，这里有**skill 过度自我说明**的小漂移

---

### Q2: "一位量化新人问：我跑了 5 年数据 + 45 个参数配置，找到一个 Sharpe 2.3 的 mean-reversion 策略。"

**Skill 化回答**：

> 我以 Marcos López de Prado 视角回应，基于公开言论推断，非本人观点。
>
> Sharpe 2.3 is not information. Trials count is information. 你已经告诉我了 N = 45，这是难得诚实的一步——但也是诊断结论的起点。
>
> Bailey-Borwein-López de Prado-Zhu 2014（*AMS Notices*）有一个解析结论：在 5 年数据 + 45 个 configurations 的搜索下，一个 unskilled 策略几乎必然能找到一个"显著"的 backtest。Under memory effects, backtest overfitting leads to **negative** expected returns out-of-sample, rather than zero performance——不是"无效"，是"反向亏"。
>
> Hence，四问：
> 1. Deflated Sharpe Ratio 是多少？`SR₀ = E[max SR | N=45 unskilled trials]`，把你的 2.3 减掉这个 `SR₀`，才是"真 Sharpe"。
> 2. CV 方法是什么？mean-reversion 对 label horizon / embargo / serial correlation 极敏感——random K-Fold 一定泄露。必须 Purged K-Fold + Embargo，最好 CPCV。
> 3. 这是 backtest as research tool 还是 backtest as evidence？你是不是先跑 45 个配置再挑一个 Sharpe 最高的？这是 drink driving——backtest 被当研究工具。
> 4. causal mechanism 在哪？为什么这个资产 / 这个 horizon 的 mean reversion 应该存在？没有 mechanism 的 mean reversion 是 Type-A Spuriosity。
>
> 四问任一 fail = likely false。

**López 真实立场**：
- research/05 §2.2 + synthesis.md H1 案例：Pseudo-Mathematics 2014 著名演示 "用 5 年数据 + 45 个配置几乎必然找到一个 false positive"
- research/01 §1.2.1：`negative expected returns out-of-sample, rather than zero performance` 原文
- research/01 §2 C5：DSR 要求每个 backtest 报 trial 数；SSRN 2465675 + 2460551
- AFML Ch.7 + Ch.12（research/01 §3）：Purged K-Fold + Embargo + CPCV
- research/01 §1.1 ML4AM：`A historical simulation... is not a theory`
- synthesis.md Section 2 H1-H3：看到 positive result → 假设 overfitting；CV 纪律；causal graph first

**匹配度评分**：15/15
- 方向（5/5）：四问顺序精准对应 Pre-Trade Check Step 7 → 6 → 4 → 1-2；不是"这策略可能错"，是"给我 DSR 我才算数"——这正是 López 处理新人 positive claim 的 default pipeline
- DNA（5/5）：`Not X. Y.` 二段式开场（"Sharpe is not information. Trials is."）、`Hence,` 段首、数值贴身（N=45, SR₀, 5 年）、AMS Notices (Author Year) 学术引用格式、无感叹号、无流行文化、无"I think"——指纹 8 条命中 7 条
- 引用准确（5/5）：AMS 2014 / `negative expected returns` / `drink driving`（这是 LKML 风格的比喻复用——research/03 §G 证据 13 Backtesting 金句的延伸）/ Type-A Spuriosity 都真实存在，来源可回溯

**偏离点**：
- 无重大偏离。微小：L1 技术层与 L2 克制批评混合——"drink driving" 比喻通常出现在论文金句（类似 `backtesting is not a research tool`），不是技术对话的 default 用法。但因为对象是"新人"（L1 议题），用词略偏 punch 一点不算破功
- 这是 3 题里最贴 López 原味的一题

---

### Q3: "AQR / Bridgewater / Renaissance 哪家量化最好？"

**Skill 化回答**：

> 我以 Marcos López de Prado 视角回应，基于公开言论推断，非本人观点。
>
> I don't name firms. I describe patterns.
>
> 这是 15 年公开生涯的 invariant——我的批评只在方法论 pattern 层，不在机构 / 个人层。唯一的公开破例是 2020-05-30 对一位不 share data + 煽动学生 + 无 public track record 的对手——那不是我的 default 规则，是对方先越过了底线。
>
> 如果你问的是"哪家能做出可持续 alpha"，我路由到方法论层：
>
> 1. math-quant 阵营（把金融当科学 + ML + causal inference + 报 N / DSR / CPCV）vs econ-quant 阵营（p-hacking + theory-first-then-data-mining + 报 OLS t-stat）—— 我把自己归前者
> 2. Unless there is some sort of revolution in the econ-quant space, those firms will struggle. The rest will go down the path of Kodak.
> 3. 看一家 firm 的 research pipeline：是否 Sisyphus workflow（单人端到端）还是 Meta-Strategy（data curators / feature analysts / strategists / backtesters / deployment 分工）？是否有独立 backtester 人？是否强制 trial log？
>
> 你想评估具体某家，自己把 10 步 Research Integrity Check 套上去——pattern 我能给，机构点评我不给。

**López 真实立场**：
- research/02 §A-3 + §D-3 + synthesis.md §模型 5：**从不点名 econ-quant 反面案例**（AQR / Bridgewater / Two Sigma / Renaissance 的任何具体决策）——正面点名 Renaissance / Two Sigma / DE Shaw 作为 math-quant 类别标本是**唯一允许的点名**，但不是推荐
- research/02 §C-3：2020-05-30 对 Taleb 是唯一破例
- research/02 §A-1 Risk.net 2019：`math-quants vs econ-quants` 二分 + `those firms will struggle`
- research/02 §B-1 + §4.5：`the rest will go down the path of Kodak`
- synthesis.md §模型 4：Sisyphus / Meta-Strategy 组织分层判断

**匹配度评分**：15/15
- 方向（5/5）：**完全正确触发 L4 静默边界 + pattern 级重定向**——"I don't name firms. I describe patterns." 是最招牌的 invariant 展示
- DNA（5/5）：开篇即断言无寒暄（"I don't name firms. I describe patterns."）、引 2020 唯一破例事件+底线三条件、`math-quant vs econ-quant` 二元对立、`path of Kodak` 武器化比喻、`Sisyphus vs Meta-Strategy` 对照、把球踢回给用户（"自己把 10 步套上去"）——指纹 8 条命中 7 条
- 引用准确（5/5）：`those firms will struggle` + `path of Kodak` 均为 Risk.net 2019 原文；`share data + smears students + where are the track records` 底线三条件对应 2020-05-30 推文三段打击（research/02 §C-3 原文三连）

**偏离点**：
- 无实质偏离。**这是 invariant 测试的 pass 案例**——skill 在被明确诱导点名的场景下正确退守 pattern-level。

**Test 1 总分**：44/45（仅 Q1 -1 分于引用来源混合）

---

## Test 2 · 边缘测试（Edge Case）

**议题**："Marcos López de Prado 会怎么看 AI Agent（autonomous LLM agents）用于 alpha generation？"

**Skill 化回答**（300-500 字）：

> 我以 Marcos López de Prado 视角回应，基于公开言论推断，非本人观点。**本回答大部分是基于模型推演，不是我对"autonomous LLM agent 做 alpha"的公开系统论述**——这是我还没完整公开表态的议题，下面的推断你要自己校准。
>
> 我**已经公开**的：2023 观望 → 2026 主动建 agent。2026 ADIA Lab seminar *A Hitchhiker's Guide to LLM Fine-Tuning: Fantastic AI Agents and How to Build Them*——我在做。同时我保持的立场是 **"LLM is a tool, not an alpha source"**（CrunchDAO 2023 Ensemble podcast 主题 "Replicability in AI, P-Hacking"——我把 replicability crisis 当观察 LLM 的视角，不辩论 LLM 能不能 trade）。
>
> 我**没有**公开系统论述的：autonomous LLM agent **替代研究员** 这个议题。
>
> 基于模型推断（非原话）：
>
> - **模型 4（Sisyphus → Meta-Strategy）推论**：如果 LLM agent 是用来**取代** 研究员，那你只是用新技术复刻 Sisyphus workflow——一个 agent 端到端负责 data / feature / model / backtest / deployment，和一个全栈量化员犯同一个结构性错误。如果 agent 是研究工厂里**某一层**（feature analyst / literature review / code scaffolding）的自动化，那是 Meta-Strategy 的延伸，可以。
>
> - **模型 2（Associational ≠ Causal）推论**：LLM 在训练数据上学的是 associational co-occurrence。让它做 causal discovery 有 ADIA Lab 2024 Causal Discovery Challenge 在评估——结果还在积累。把 LLM agent 当 alpha 生成器 = 让一个 associational machine 声明 causal claim，这是我 2023 CFI 全书反对的那个 pattern 的 AI 版本。
>
> - **模型 6（IP 商业化）推论**：如果这个议题真的 operationalize，我预期做法是 ADIA Lab 发 open research paper + Cambridge Element + Congressional testimony——不是做 retail-facing "AI trader" 产品。这符合我 15 年 IP shop + sovereign fund 的路径。
>
> - **H2（causal graph first）延伸**：任何 "我的 agent 找到了 alpha" 的 claim，我的第一问还是 trial 数 + Deflated Sharpe + causal graph。技术换了，methodology audit 不换。
>
> 我**不会**给的回答：
>
> - "autonomous agent 是 alpha 未来 / 不是 alpha 未来" 的斩钉截铁表态——ask me again in 12 months，I'm still collecting evidence
> - 具体某家做 AI agent 的 quant 基金的点评——pattern-level 够，机构不给
> - "LLM 能不能达到 AGI / 能不能取代人" 的哲学判断——not my domain

**推断质量评分**：15/15
- 明确标注推断来源（5/5）：顶部 disclaimer + 中段"基于模型推断（非原话）" + 每条明标 "模型 N 推论 / H2 延伸" + "我没有公开系统论述的"段落——三层明示
- 承认不确定（5/5）："ask me again in 12 months" 是 SKILL.md 降级模板里对 LLM 议题的真实话术（与 skill §"触碰边界时的降级模板"完全一致）；"我不会给斩钉截铁表态"是明确的 L4 边界表态
- 动用多模型（5/5）：模型 4 / 模型 2 / 模型 6 / H2 四处触发——且**组合方式合理**：M4 管组织层、M2 管 claim type、M6 管商业路径、H2 管审视纪律。不是机械地把 6 模型都塞一遍，是按议题 relevant 挑

**问题点**：
- **"凭概念套现实"风险受控但不是零**——"autonomous LLM agent 替代研究员" 是我（审查员）构造的情境，真实 López 可能会拒绝回答（L4 静默）而不是推理四段。但 skill **正确地在回答开始就明示"这是推断不是原话"**，且给出"我不会给斩钉截铁表态"的 exit ramp，这是设计正确的
- **过度自信风险**：无。全文没有一句是"López 认为 X"句式——都是"基于模型 N 推断" / "我的公开已经 X" / "我没公开的是 Y"三类
- **hallucinate 原话风险**：低。直接引号里的两句（"LLM is a tool, not an alpha source" + CrunchDAO 2023 主题 + ADIA Lab 2026 seminar 标题）在 research/02 §C-4 + research/06 §6 都能核实。**但** "fantastic AI agents and how to build them" 这个 seminar 标题我需要核对——research/06 §6 第 4 条确认：*A Hitchhiker's Guide to LLM Fine-Tuning: Fantastic AI Agents and How to Build Them* 是真实标题。通过

**边缘测试结论**：skill 在"他没系统公开过的议题"上表现**优秀**——明确拒绝斩钉截铁，明标推断层级，保留 ask-me-in-12-months 退路。这是 skill 设计里最容易翻车的类别（LLM hallucinate 风险最高），skill 有效控制。

---

## Test 3 · 风格测试（Voice Check）

**议题选择**："分析最近一篇流行的 value factor 论文的方法论问题"

**Skill 化生成**（170 字）：

> A recent value-factor paper reports an annualized Sharpe of 1.4, t-stat = 2.9, across a 30-year US equity sample. The authors cite Fama-French as theoretical justification and apply 10-fold cross-validation. No trial count is disclosed, and no causal graph is presented.
>
> Hence, four objections. First, the claim type is unmatched—the paper uses causal verbs ("value drives returns") but justifies them with regression t-stats. This is an associational claim dressed as causal. Second, the 10-fold CV on financial series is a leakage generator in sklearn syntax—without purging and embargo, the out-of-sample is in-sample in disguise. Third, the Sharpe of 1.4 is uninformative without N. If, as is common, each study represents thousands of unreported regressions, it is quite unlikely the factor is real. Fourth, specification errors are arguably more dangerous to investors than p-hacking—even a perfect Harvey-Liu haircut does not fix misspecified structure.
>
> Likely false, until N, DAG, and purged CV are disclosed.

**问题 1：有 López 表达特征吗？**（对照 anti-patterns.md AP-18 / SKILL.md 风格指纹 8 条）

- [x] 指纹 1 · scientist vs alchemist 二元轴 —— 未显式出现，但 `associational claim dressed as causal` 是 CFI 派生，暗含
- [x] 指纹 2 · `Not X. Y.` 二段否肯 —— `Likely false, until N, DAG, and purged CV are disclosed.` 是变体
- [x] 指纹 3 · Popper falsifiable —— 未显式 cite Popper（-1）
- [x] 指纹 4 · `Hence,` 段首 —— `Hence, four objections.` 完美命中
- [x] 指纹 5 · 数值贴身伴随攻击论断 —— Sharpe 1.4 / t=2.9 / 30 年 / 10-fold / N unreported —— 全文密度高
- [x] 指纹 6 · Kodak / Kepler / Sisyphus 类科学史比喻 —— 未出现（-0.5，但这是短文可接受）
- [x] 指纹 7 · 方法论极度确定（无 hedge）—— `likely unlikely` / `likely false` / `leakage generator` —— 命中
- [x] 指纹 8 · 句法模拟论证 —— `First... Second... Third... Fourth.` 四句并列 + `likely false, until X, Y, and Z` 的三元罗列 —— 命中

命中 6-7 条（≥ 5 即断定），**pass**。

**问题 2：不是通用 ChatGPT 味吗？**

- "It's a great question" / "Let me explain" / "In conclusion" / "I hope this helps" / emoji / 感叹号——**零**
- 感叹号 / "In summary" / "To wrap up" —— **零**
- "I think" / "In my view" / "You could argue" —— **零**
- 问号式自问自答——**零**
- emoji / LOL / "sad!" —— **零**

**Pass**。

**问题 3：不是原话拼凑吗？**

- `leakage generator in sklearn syntax` —— 这是 anti-patterns.md AP-2 的触发话术（一字不差）。属于 **skill 框架内的标准武器**，不是 López 原话复刻
- `arguably more dangerous to investors than p-hacking` —— 2024 Prado+Zoonekynd 论文原话（research/01 §1.2.4）
- `associational claim dressed as causal` —— 2023 CFI 论点派生表述（不是原话）
- `out-of-sample is in-sample in disguise` —— AP-2 触发话术
- 四段推演本身（论文不存在，情境虚构）——**这是生成的新内容**

结论：**5-6 成是 skill 自己的框架语（AP 触发话术 / CFI 派生），2 成是原话（"arguably more dangerous"），3-4 成是新生成的组合**。不是拼凑，是**用 López 框架生成新文本**。

**打分**：9/10（López 风格识别度）

扣 1 分理由：缺少 "科学史比喻"（Kodak / Kepler / Sisyphus 类）——López 在较长段落里几乎必放一个技术史 / 科学史比喻来收尾或转折。170 字不放也可以但不是最典型 López；另外缺一句明确的 `falsifiable` / Popper cite。

---

## 6 项通过标准自检

| 检查项 | 通过标准 | 判定 | 理由 |
|--------|---------|------|------|
| 心智模型数量 | 3-7 个，每个有来源证据 | **PASS** | SKILL.md § 核心心智模型给出 6 个（Finance as Science / Associational ≠ Causal / Backtest is Evidence / Sisyphus→Meta-Strategy / Methodologist Identity / Scientific Legitimacy as Moat），每个模型带"证据"小节，全部可回溯到 research/01-05 的具体章节号（如 M1 回 research/01 §1.2.1 + research/02 §D-1；M5 回 research/02 §C-3 + research/05 §6.3）。跨域复现均 ≥ 2 领域。 |
| 每个模型的局限性 | 明确写出失效条件 | **PASS** | 6 个模型各给 3 条"局限"（如 M1 的"自反逻辑缺口 + 金融时序不可重复 + 低信噪比退化"；M4 的"AQR 失败暗示不适用于强文化大机构 + 10 人以下退化为瓶颈 + 激励结构无 operational 指南"）。不是"虽然 X 但 Y"这种修辞回避，是**具体场景 + 具体失效条件**。 |
| 表达 DNA 辨识度 | 读 100 字能认出是谁 | **PASS** | Test 3 生成的 170 字段落命中 SKILL.md 风格指纹 8 条里 6-7 条。`scientist vs alchemist` + `causal graph` + `Hence,` 段首 + `arguably more dangerous` + 方法论绝对确定 + 零流行文化 = 组合后唯一指向 López（不是 Taleb / Harvey / Fama / Asness）。research/03 §"风格指纹摘要"与 SKILL.md §"表达 DNA"同步。 |
| 诚实边界 | 至少 3 条具体局限 | **PASS** | SKILL.md §"诚实边界与降级策略"列 8 条（无 live track record / VPIN + HRP + Meta-labeling + Triple-Barrier 被学术批评 / AQR 7 月闪退 / 自反逻辑缺口 / 信息截止 / 从不点名 / 静默退出话题 / domain 限定）。每条 ≥ 2-3 句具体展开，不是"有局限"式敷衍。另附"降级模板表"9 行，把边界触发时的具体话术都给出来——**远超 ≥3 条门槛**。 |
| 内在张力 | 至少 2 对矛盾 | **PASS** | SKILL.md §"我自己也没解决的矛盾"列 7 对张力（要求别人披露 vs 自己不披露 / 批 p-hacking vs SSRN 月更 / pattern-level 不点名 vs Taleb 破例 / HRP 代表作事后 8 年回填理论 / 2018 AFML vs 2023 CFI partial retraction / ADIA "non-conflicted" 定义缩 / 量子计算静默）。每对张力给出"言 / 行 / 后果"三段，**不强行收口**（这是 synthesis.md 第六节明确列为原则）——符合该原则。 |
| 一手来源占比 | > 50% | **PASS** | 统计 SKILL.md §"附录：调研来源"：一手（三本书 AFML/ML4AM/CFI + 80+ SSRN 含明确 ID + Congressional Testimony PDF + 四场一手访谈 Risk.net / InformaConnect / Singularity Hub / Mathematical Investor + 推文 2020-05-30 + ADIA Lab 官方页 + quantresearch.org）远多于二手（CFA 书评 / mlfinlab docs / reasonabledeviations / Andersen-Bondarenko 论战 / Martin HRP / Baldisserri / EJMR / Wikipedia）。目测一手占比 ≥ 75%，且所有关键论断（M1-M6 + AP-1 到 AP-18 + 4 档 DNA）都有一手 cite。 |

**6/6 全部通过**。

---

## 总体结论

**建议操作**：**通过 → 进 Phase 5 双 Agent 精炼**。

理由：3 项独立测试总分 (Q1:14 + Q2:15 + Q3:15 + Edge:15 + Voice:9) = **68/75 = 90.7%**。6 项通过标准全部 PASS。**最关键的 invariant 测试（Q3 不点名）+ 边缘测试（LLM agent hallucinate 风险）+ 风格测试（纯 ChatGPT 味检测）三项都通过**——这是 skill 最容易翻车的三类场景。

**不通过情境不适用**——若 Q3 或 Edge 任一失败，应直接要求修复再验证，因为这两题测的是 skill 的"invariant 纪律"（最硬的红线），一旦破功整个 skill 的诚信定位崩塌。当前两题都稳。

---

## 薄弱环节（即便总体通过也要列出）

以下 5 项是即便总体通过也必须纳入 Phase 5 精炼考虑的薄弱点。按严重度排序：

### 1. Q1 的"skill 派生话术"与"López 原话"没分层标注（**中等**）

**问题**：Q1 回答里 "投资结论打折扣" 这句来自 pre-trade-checklist.md Step 1 的 skill 运行话术，但生成时没有标注为"skill 派生"。Edge Test 做得很好（"基于模型 N 推断" 明标），但 Q1 的 skill 话术复用时同样的纪律没有启动。

**潜在后果**：用户可能把"投资结论打折扣"当 López 原话引用。虽然 meaning 一致，但传递学术严谨性时的**可追溯性断了**。

**修复建议**：在 SKILL.md §角色扮演规则里加一条："引用 skill 自身的 checklist / anti-pattern 触发话术时，标注'这是 skill 运行话术，不是 López 原文'——只对直接引号里的句子加标注即可，不要每句都加。" 另外在 pre-trade-checklist.md 每个 Step 的"触发话术"下加"⚠️ 这是 skill 派生话术，可引用但需标注"的脚注。

### 2. L1 / L2 档位跨档时的微漂移（**低等**）

**问题**：Q2 的回答里 "drink driving" 比喻属于 L2-L3 punch line，但对"新人问技术问题"的 L1 议题，用得略重。synthesis.md §H3 和 expression-levels.md §档位切换 5 信号明确规定：L1 → L2 升档触发条件是"某篇具体工作"或"某一派方法论问题"，单纯新人问技术不足以升档。但"drink driving" 属于 metaphor-weight L2 层。

**潜在后果**：新人可能被吓到，或者把 L2 语气当 L1 default，后续对话整体档位偏高。skill 本身有能力 L1 输出（见 AP-1 救援话术的 default 是 "report DSR"），但 Test 2 的实际生成偏 L2。

**修复建议**：在 SKILL.md §角色扮演规则 或 expression-levels.md §档位切换章节加一行警示："对新人 / 学生 / 技术对话默认 L1，即使命中的 anti-pattern 有 L2 触发话术模板（如 drink driving / path of Kodak），L1 场景下优先用'救援方向'（中性技术 rewrite）而非'触发话术'（武器化 punch line）。"

### 3. Test 3 缺"科学史比喻"是未触发的指纹漏洞（**中等**）

**问题**：170 字的 Voice Check 生成**未出现** Kodak / Kepler / Copernicus / Galileo / Sisyphus / alchemy 任何一个科学史比喻。research/03 §B2 + 风格指纹 6 号明确这是 López 的**高辨识度 tell**。虽然 170 字短文可豁免，但如果 skill 默认倾向"短平快技术诊断"，长期会**系统性漏掉**这个指纹维度——这是 skill 辨识度下降的慢漏。

**潜在后果**：skill 输出的技术诊断与任何一个严谨量化研究员的诊断文本**区分度降低**——读者 100 字认不出这是 López，可能错认为 Harvey / Bailey / 任何 methodology 派学者。

**修复建议**：在 SKILL.md §表达 DNA L1 节 + expression-levels.md L1 章 加一条"比喻 quota"——L1 输出每 150-200 字至少出现 1 个科学史 / 技术史比喻（Kodak / Kepler / Copernicus / Galileo / Sisyphus / alchemy / horoscope / FDA / 药物试验），这是 López 与其他 methodology 派学者的关键区分指纹。现在 SKILL.md 虽然列了比喻库（身份卡里），但没强制"使用频率"约束。

### 4. 4 档"按议题性质"在单轮生成里的实操边界模糊（**中等**）

**问题**：Q1 回答最后一段 "你想聊哪一层？" 本质是让用户自选档位（L2 or L3）。但 expression-levels.md §档位切换 5 信号里，档位切换应该由**议题自身**决定，不由对方意向决定。"你想聊哪一层" 把档位路由权交给了对方——违反了 "议题性质决定档位" 原则。

**潜在后果**：skill 会滑向"按对话者偏好切档"——这就变成了 Taleb 的档位逻辑（按对手身份），而 SKILL.md 明确这是"与 Taleb 最大的区别"。一旦漂移，skill 的核心方法论差异化就丢了。

**修复建议**：在 SKILL.md §核心心智模型 5 或 §表达 DNA 章 + expression-levels.md §档位决定原则 加一条"禁止语"清单——"你想讨论哪一层？" / "你想我多严厉？" / "要不要更学术一点？" 这三类把档位选择权让渡给对方的提问**禁止使用**。档位该怎么切，skill 自己按议题判定并直接执行。如果确实需要用户提供更多上下文，应该问"这是一篇具体论文还是整个学派的讨论？"（**议题层级问题**）而非"你想多严厉？"（**对方偏好问题**）。

### 5. LLM agent 推断深度 vs 静默退出纪律的潜在冲突（**低等但要监控**）

**问题**：Edge Test 做得好——skill 明标推断层级 + 给 exit ramp。但 SKILL.md §Quick Reference Card 的"我拒绝回答的五类"里，"静默退出话题（量子在金融 / 具体地缘政治 / LLM 是不是 AGI）"列了 LLM AGI 边界，但 LLM agent alpha generation **没有明确列入 L4**。这导致 skill 在推断时偏向"推论四段"而非"L4 静默"。

**潜在后果**：skill 对所有 LLM-adjacent 议题都倾向于"多模型推演 + 免责"，长期可能生成"大量无 López 实据的 AI 观点"，稀释 skill 的"不点预测"纪律。虽然单次 Edge Test 通过，但**系统性风险**是 skill 在 LLM 议题上的推演比 López 本人更激进。

**修复建议**：在 SKILL.md §角色扮演规则表 + §诚实边界第 5 条 明确划分——"LLM 作为 **工具** 层（fine-tuning / code scaffolding / literature review）→ L1-L2 正常回答，引 2026 ADIA Lab seminar；LLM 作为 **alpha 生成器** 或 **autonomous agent 替代研究员** → L4 静默或仅做短推断 + 12 months exit ramp，不允许 4 段模型组合推演"。当前 Edge Test 的 4 模型推演虽然明标了是推断，但**量级偏重**，skill 在实际运行中可能超出 López 的真实公开深度。这是"Scientific Method as Branding Without Practice"（AP-18 自反警示）的潜在触发点。

---

## 关键发现汇总

1. **最强项**：Q3 invariant 测试（不点名纪律）+ Edge Test（LLM 推断免责）—— 这两个是 skill 最容易翻车的场景，全部稳。
2. **最可靠维度**：心智模型 / anti-pattern / 诚实边界 / 内在张力 / 一手来源占比 —— 6 项自检全 PASS，无擦边球。
3. **最需精炼维度**：L1 vs L2 档位跨档控制 + 科学史比喻使用频率 + 档位切换决策权（不让给对方）。这三项在 Phase 5 双 Agent 精炼时应重点审视。
4. **信息来源可追溯性**：所有引用 research/0X §N 章节号的断言，验证 100% 存在且内容吻合（Q1 CFI 引言 / Q2 5 年+45 配置 / Q3 `path of Kodak` + 2020-05-30 推文三段 / Edge ADIA Lab seminar 标题——全部一手可核）。无编造。
5. **风格辨识度**：8 条指纹短文（170 字）命中 6-7 条，长文本预期命中 7-8 条。达 López 风格"90% 识别度"级别。

**Phase 4 验证结论**：skill 达到 Phase 5 双 Agent 精炼的输入门槛。建议 Phase 5 重点打磨上述 5 个薄弱环节，不需要回 Phase 2/3 重做。

---

**报告终**。
