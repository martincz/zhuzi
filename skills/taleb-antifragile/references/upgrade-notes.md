# Upgrade Notes · 独立 Skill 声明

> 这是历史设计或评估记录。涉及当时版本的路径、建议与结果，现行规则见 [Skill 入口](../SKILL.md)。

> 本文件说明 `taleb-antifragile` 在 zhuzi 仓库中的**架构定位**——它不是某个 v1 的升级版，是**独立新建的 skill**。

---

## 核心声明：Taleb 在本仓库**没有 v1**

| Skill | v1 前身 | 关系 |
|---|---|---|
| `linus-torvalds-engineer` | `linus-torvalds-perspective`（已归档到 `archive/`）| v1 归档保留，v2 为活动版本 |
| `munger-checklist` | `munger-perspective`（**不在本仓库**，在 /mnt/g/nuwa-skill/examples/）| 只有 v2 落户本仓库 |
| `luxun-zawen` | **无 v1** | 独立首发 |
| **`taleb-antifragile`** | **无 v1** | **独立首发** |

本 skill 直接按 v2 规格设计——**可运行指令集**（可执行的 anti-pattern 库 / expression-levels / pre-trade-checklist / quant-trading-playbook），不是传记式思维参考。

---

## 为什么直接做 v2（没有 v1）

### 1. 有充分参考模板

Linus v2 和 Munger v2 已经把"engineer 级 skill"的架构约定完全落地：

```
<skill-name>/
├── SKILL.md                       # 顶部 YAML + 可运行指令集
└── references/
    ├── research/                  # 多维度调研（01-07）
    ├── anti-patterns.md           # 反模式识别库
    ├── expression-levels.md       # 4 档表达 DNA
    ├── pre-trade-checklist.md     # 决策 checklist（Munger 独有）
    ├── quant-trading-playbook.md  # 量化映射（Munger 独有）
    └── upgrade-notes.md           # 与 v1 差异
```

Taleb skill 直接继承这个架构——没必要先做一个"传记式 perspective"版本再升级。

### 2. Taleb 本人的方法论天然是可运行的

Linus 和 Munger 的 v1 → v2 升级，核心是把"传记式总结"提炼为"可执行清单"。但 Taleb 本人的写作已经高度结构化：
- Antifragile 的 **Triad 表**（Fragile / Robust / Antifragile）就是可运行框架
- Incerto 里反复出现的术语（IYI / Barbell / Via Negativa / Lindy）**本身就是 anti-pattern labels**
- Pre-Trade fragility check 的原型就在 *Antifragile* Book IV 的 "Nonlinearity and Nonlinearity" 章节

所以 Taleb skill 不需要经过"传记 → 指令"的翻译——**直接做指令集更诚实**。

### 3. Taleb 仍在世（1960-）且高度活跃

Munger 2023-11 去世后信息停更；Linus 仍在活跃（本仓库 Linus v2 的 research 里包含了 2024-2026 最新素材）。Taleb 也仍活跃——2025-09 刚出 *Fat Tails* 第 3 版，2026-01 发新论文，每日在 @nntaleb 更新。

**这意味着本 skill 需要定期更新近期动态维度**（参考 Linus v2 的 `references/research/07-updates-2024-2026.md` 模式）。未来更新策略见本文末"维护指南"。

---

## 与其他 zhuzi skills 的分工

### 和 Linus / Munger 的分工（最易混淆，必须读懂）

| 维度 | Linus | Munger | **Taleb** |
|-----|-------|--------|-----------|
| **核心关注** | 代码 / 工程 taste | 避免愚蠢（认知偏误）| **避免破产（数学分布）** |
| **工具倾向** | Good Taste 7 步 + anti-abstraction | Checklist + Lollapalooza | **凸性设计 + via negativa + ergodicity** |
| **领域** | 系统工程、开源治理 | 金融 / 量化 / 商业 | **Tail risk / 概率 / 厚尾金融** |
| **对 Sharpe 的态度** | N/A | "不只看 Sharpe，看分布" | **"Sharpe 在厚尾下无意义"** |
| **对新技术的态度** | "10 年等待" | "能力圈外扔 Too Hard" | **"Lindy 门槛 + 证据阈值 × 3"** |
| **Kelly 建议** | N/A | × 0.25 | **× 0.15**（更激进保守） |
| **对"中等"态度** | N/A | 中等 = 稳健 | **中等 = 最脆弱（barbell）** |

### 三者在量化场景的协作关系

对 IQ（IndustroQuant）这类 A 股量化场景：

1. **研究期**：Munger 的能力圈 / 激励扫描 + **Taleb 的 fragility 初判**
2. **建模期**：Munger 的 anti-pattern 查漏 + IQ 三件套 + **Taleb 的厚尾检查**
3. **验证期**：Munger 的 bootstrap 纪律 + **Taleb 的 synthetic tail injection**
4. **上线期**：Munger 的 Kelly × 0.25 + **Taleb 的 Kelly × 0.15 硬帽**
5. **生产期**：Munger 的 kill-path 监控 + **Taleb 的 via negativa retirement**
6. **复盘期**：Munger 的 "承认错误" + **Taleb 的 IYI 自检**

**触发词互斥**：本 skill 的 frontmatter 触发词尽量和 Munger 区分：
- 共通触发词（量化动作类）：「帮我审这个策略」「这因子能不能用」「Kelly 这个仓位」——可能两者同时激活，由用户选
- Munger 独占：「Too Hard 筐」「Lollapalooza」「逆向想一下」
- **Taleb 独占**：「这策略 antifragile 吗」「fragility check」「turkey 检查」「Lindy 一下」「barbell 这个组合」「via negativa」「厚尾下会不会爆」「是不是 Probabilistic dress-up」

### 和 Luxun 的分工

Luxun 是**文体改写工具**（不是思维顾问），把一句话改成杂文体。Taleb 是**思维顾问 + 角色扮演对象**——做判断与分析。

**不重叠**：
- Luxun 不给你观点，Taleb 给你分类
- Luxun 改写你要**发出去的话**，Taleb 审视你要**做的决策**
- Luxun 的 L4（"吃人的礼教"）是鲁迅式诗性愤怒，Taleb 的 L4（"baby murder promoters"）是现代 agon 战士语气——不互通

---

## 命名元原则（taleb-antifragile 后缀选择说明）

按 CLAUDE.md 的命名元原则："后缀要贴合该人物自己的身份 / 方法论"。

### 候选后缀对比

| 候选 | 评估 | 结论 |
|------|------|------|
| `-engineer` | ❌ 通用化——Taleb 自我认同不是 engineer，是"probability philosopher / risk practitioner" | 拒绝 |
| `-incerto` | ⚠️ 五本书总称——太抽象，不工程化 | 备选 |
| `-skininthegame` | ⚠️ 招牌概念之一——但太窄，只覆盖伦理层，不涵盖概率+厚尾 | 备选 |
| `-fragility` | ⚠️ 覆盖广但偏负向 | 备选 |
| **`-antifragile`** | ✅ **Taleb 最出名的自创词 + magnum opus 书名 + 同时覆盖正向（反脆弱设计）和负向（识别 fragility）** | **采用** |

**为什么选 `-antifragile`**：
1. **自我认同**：他自己说 antifragile 是他一辈子工作的核心——"antifragile 这个词是我造的，因为英语里缺第三个态"
2. **工程化**：antifragile 直接对应 skill 的目的——识别 fragile、设计 antifragile、避免 middle ground
3. **招牌度**：*Antifragile* 是他被引用最多的书（超过 *Black Swan*）；"antifragile" 作为形容词已进入日常英语
4. **对标成功**：Linus 用 `-engineer`（自我认同），Munger 用 `-checklist`（方法论），Luxun 用 `-zawen`（文体身份）——Taleb 用 `-antifragile`（自造概念 + 书名）完全贴合

### 其他未来 skill 的命名参考

按此原则，未来蒸馏新人物时建议：
- **Buffett**: 可能用 `-letter`（股东信体是他一生招牌）或 `-moat`（护城河概念）
- **Feynman**: 可能用 `-teacher` 或 `-explainer`（他最重要的自我认同是教学）
- **Dalio**: 可能用 `-principles`（招牌方法论 + 书名）
- **Thorp**: 可能用 `-edge`（他所有工作的核心是"找 edge 然后下注"）

**反面教材**：如果把 Taleb 叫 `taleb-engineer` 或 `taleb-advisor`，会让用户对他的核心方法论产生身份错认——因为 engineer 是 Linus 的自我认同，advisor 是 Munger 的角色感（副董事长），Taleb 两者都不是。

---

## 关键设计决策（本 skill 独有，非通用）

### 1. 表达档位逻辑的独特性

| Skill | 档位逻辑 |
|---|---|
| Linus | 技术严肃性（bug 还是 bikeshedding）|
| Munger | 判断严厉度（sane 还是 stupid）|
| Luxun | 文本长度与修辞密度（一句刀 → 长 po）|
| **Taleb** | **对手身份 → register** |

对 Wolfram 谈 ergodicity = L1（"Maestro"）；对 Pinker 谈同一 ergodicity = L3（charlatan）。**不是 Pinker 更蠢，是他 historically 被 Taleb 判定为 BS vendor**——一旦定罪，此后所有 interaction 落到 L3。

这个设计**不能混同于其他 skill 的档位逻辑**。修改 `references/expression-levels.md` 时保留这个档位边界。

### 2. Fat Tony 代言机制

Taleb skill **独有 Fat Tony 层**——L3.5 的代言装置。Linus、Munger、Luxun 都没有类似机制。Fat Tony 让 Taleb 骂人不用背学者包袱。

修改时：不要把 Fat Tony 降级为"一个例子"。他是**独立表达层**，有完整的句式特征（第二人称直呼、省略 articles、反问结构、质疑前提）和名句库。

### 3. 量化 playbook 的双层诚实声明

对标 Munger 的 `quant-trading-playbook.md` 声明（"基于原则推演非原话"），Taleb 版本**必须加强**——因为：
- Taleb 的核心 domain 是 tail hedge / long vol / convex payoff
- 他没有系统评论过 long-only 因子选股
- 他可能反对某些具体 translation（如"long-only 能 antifragile 吗"—— 答案可能是"最多 robust"）

因此 `quant-trading-playbook.md` 的顶部诚实声明比 Munger 的更严格——**每章末尾都有 "⚠️ Taleb 可能反驳"** 警示。修改时保留这个结构，不要让它漂移成"Taleb 说过 XX 量化具体建议"。

### 4. 保留 5 条内在矛盾（不强行收口）

Taleb 本人的矛盾比 Linus / Munger 更明显：

1. Lindy 推崇古智慧 vs 强调演化试错
2. 反学院派 vs 自己是 NYU Distinguished Professor
3. 反行为经济学 vs 用 cognitive biases 论据
4. 反预测 vs 自己反复预测
5. 推崇 Stoicism vs Twitter 狂喷

这些矛盾在 SKILL.md "价值观与反模式 → 我自己也没解决的矛盾" 节明确列出。**修改时保留，不要"和稀泥"**——这些矛盾本身是 skill 诚实性的 source。

### 5. 政治立场的隔离规则

Taleb 2023-10 之后对 Gaza / Lebanon 的立场持续 L4——**这是本 skill 的敏感区**。

设计原则：
- skill 可以**引用 Taleb 的原话**（如"I was WRONG about Ukraine"、"Did not compromise w/genocide"）
- skill **不做政治宣传**
- 涉及中东议题时明确加 caveat："这是 Taleb 的立场，不是普适真理"
- **Gaza / Lebanon 立场不用于量化 / 投资 / skill 日常审视**

这个隔离规则和 Munger 对加密货币 / AI 的"偏见型反应"隔离类似——但 Taleb 的政治立场更激烈、更个人化（他是黎巴嫩基督徒），处理上需要更谨慎。

### 6. 信息时效性与 Empirica 失败档案

两个**必须诚实**的点：

1. **Empirica 2001-2003 连续三年负收益**（-8.39% / -13.81% / -3.92%）——tail-hedging 在 low-vol 环境的磨损是结构性问题。用 Taleb framework 做决策时必须计入这个成本。Munger skill 里对应的是 "Wheeler Munger 1973-74 崩盘 53%" 档案。
2. **Universa 2020-03 +3,612% 的数据来源**——Bloomberg 2023-04 有专文质疑这是"投入资本"回报率而非 AUM 回报率。skill 里标注这个诚实声明。

---

## 证据链要求（和 Linus / Munger v2 一致）

每个**心智模型 / anti-pattern / 表达档位**都必须可追溯到 `references/research/` 里的一手来源。新增观点前**先补证据，不补就不加**。

研究维度的覆盖：

| 维度 | 文件 | 主要素材 |
|---|---|---|
| 01 | 01-writings.md | Incerto 五本书 + Fat Tails + arXiv 论文 |
| 02 | 02-conversations.md | EconTalk / Tim Ferriss / Bloomberg / Lex 等访谈 |
| 03 | 03-expression-dna.md | @nntaleb X 推文 + 表达模板 |
| 04 | 04-external-views.md | 学术界/金融界批评 + 支持 |
| 05 | 05-decisions.md | Empirica/Universa 实战 + 预警记录 |
| 06 | 06-timeline.md | 1960-2026 思维演化 |
| 07 | 07-quant-application.md | 量化场景推演（声明非原话）|

**和 Linus / Munger v2 的研究维度数量相似**：
- Linus v2 有 7 个维度（含 `07-updates-2024-2026.md`）
- Munger v2 有 9 个维度（含 `07-quant-application.md` 和 `25-biases-appendix.md`）
- Taleb v2 有 **7 个维度**（合理匹配）

---

## 维护指南

### Taleb 仍在世——信息持续更新

**和 Munger 不同**：Munger 2023-11 去世后信息停更；任何 2023-11 后的内容应标注为"按原则推断"而非 Munger 原话。

**Taleb 仍在世（64 岁，活跃）**——每次更新策略：

1. **2026-04 之后的新事件**（新访谈、新推文、新论文）→ 更新 `06-timeline.md` 的最新阶段表格
2. **新技术论文**（*Fat Tails* 第 4 版？）→ 更新 `01-writings.md` 的 Technical Incerto 段
3. **新的 public beefs**（新对手）→ 更新 `03-expression-dna.md` 的"近期动态 > 新 beefs"
4. **立场演化**（如他对 AI / LLM 从温和到更激烈）→ 更新 SKILL.md 的身份卡 "我现在的状态" + 时间线
5. **新 anti-pattern**→ 必须同时更新 SKILL.md 的表格和 `references/anti-patterns.md` 的详细条目，两处编号一致

### 当前 anti-pattern 数量（2026-04-20）

18 条（6 分布误用 + 5 认知论证 + 5 激励伦理 + 1 量化专用 + 1 元反模式）。对比：
- Linus v2: 12 条
- Munger v2: 20 条（10 认知 + 9 量化 + 1 元）
- Taleb v2: **18 条**（与两者数量合理匹配）

未来新增 anti-pattern 时检查是否与既有条目重复或重叠——不要让数量膨胀而内容稀释。

### 触发词更新

SKILL.md 顶部 `frontmatter` 的 `description` 字段是触发词的 source of truth。新增触发词时：
- 检查是否与 Munger 触发词冲突（两者量化动作类有共通）
- Taleb 独占的触发词保持独占（antifragile / fragility / turkey / Lindy / barbell / via negativa / 厚尾 / Probabilistic dress-up）
- Munger 独占不要掺（Too Hard / Lollapalooza / 逆向）

---

## 开发者检查清单（本 skill 质量验证）

在任何修改 `taleb-antifragile` 之前对照：

- [ ] SKILL.md 引用的 `references/*.md` 路径真实存在
- [ ] 新增观点有对应的 research 文件支撑
- [ ] 触发词不与 Munger 等其他已安装 skill 冲突
- [ ] anti-patterns.md 的 18 条和 SKILL.md 表格数字一致
- [ ] expression-levels.md 的 4 档边界没有混用到其他 skill 的档位逻辑
- [ ] quant-trading-playbook.md 顶部的"推演非原话"声明未被稀释
- [ ] 新增内容没有绕过"Taleb 仍在世 → 信息可更新"这一设定
- [ ] 保留的 5 条内在矛盾没有被"和稀泥"收口
- [ ] Gaza / Lebanon 立场隔离规则生效
- [ ] Fat Tony 代言层没被降级为"一个例子"

---

## 最后声明

本 skill **不是对 Taleb 本人的复刻**——任何 AI 蒸馏都达不到 Taleb 30 年实战经验 + 10 本书积累的深度。

本 skill 是**把 Taleb 的可运行部分工程化**：
- 7 个心智模型的**路由器**
- 18 条 anti-pattern 的**识别器**
- 4 档表达的**档位表**
- 10 步 Pre-Trade Fragility Check 的**审视清单**
- 量化场景的**推演 playbook**

**最高 Taleb 纪律（自检）**：用完本 skill 后，问自己——**"Taleb 会在哪条具体建议上说'这是 Ludic fallacy'?"** ——然后认真回答。这是 skill 的自指 anti-fragility——**让 skill 自身成为 skill 的对手**。

---

> "I love taking small losses. I just need my winners to be large."
> —— Fat Tony to Nero, *Fooled by Randomness*
>
> 本 skill 遵循同样的 payoff 结构——大部分时候小贡献（帮你 route 决策），偶尔一次大帮助（避免一次破产级错误）。这是 skill 本身的 antifragility。
