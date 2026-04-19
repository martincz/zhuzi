# zhuzi · 诸子

> **诸子**——取诸子百家之意。每个 skill 是一家思想，合起来是思维工具的**百家争鸣**。
>
> A collection of Claude Code Skills that distill the thinking frameworks of notable figures into runnable cognitive tools — named after *zhūzǐ* ("hundred schools of thought"), where each skill is one school.

---

## 这是什么

这是一个 **Claude Code Skill 集合**——每个 skill 都是一套可激活的 Markdown 规约，把某个历史 / 当代人物的思维框架工程化成 Claude 可以直接运行的"认知操作系统"。

没有构建系统、没有测试套件、没有运行时。全部内容都是 Markdown 文档，由 Claude Code 按 skill 规范加载。

目标不是**角色扮演**（"我是 Linus，我会说 fuck"），而是**思维框架的提炼**：
- 他用什么**心智模型**看世界？
- 他用什么**决策启发式**做判断？
- 他怎么**表达**？
- 他**绝对不会**做什么？
- 什么是这个 skill **做不到的**（诚实边界）？

---

## 已包含的 Skill

| Skill | 人物 | 类型 | 用途 |
|-------|------|------|------|
| `linus-torvalds-perspective` | Linus Torvalds (v1) | 思维顾问（传记式） | 代码 / 系统工程 / 开源治理的思维参考 |
| `linus-torvalds-engineer` | Linus Torvalds (v2) | 工程师级（可执行指令集） | 代码审查、架构设计、技术选型、good taste 7 步清单 |
| `munger-checklist` | Charlie Munger | Checklist 式思维工具 | 量化策略设计、投资决策、商业判断、20 条愚蠢清单 + 10 步 Pre-Trade Checklist |
| `taleb-antifragile` | Nassim Nicholas Taleb | Fragility 审视 / 厚尾风险引擎 | 量化策略尾部风险、反脆弱设计、概率装饰识别、18 条 fragility 清单 + 10 步 Pre-Trade Fragility Check |
| `luxun-zawen` | 鲁迅 | **文体改写工具**（非思维顾问） | 日常聊天 / 吐槽 / 反击的杂文腔改写，6 种修辞 DNA / 12 种场景 playbook |
| `stalin-gensek` | Joseph Stalin | **组织学案例研究**（非智识典范） | 权力结构识别、战略反面对照、历史案例分析——**做历史分析，不做现代操作建议** |

### 命名约定

每个 skill 的**后缀**取自该人物自己的身份 / 方法论，不是通用的 `-engineer`：

- Linus 用 `-engineer`（自我认同）
- Munger 用 `-checklist`（招牌方法："We collect the asininities..."）
- Taleb 用 `-antifragile`（自造概念 + magnum opus 书名——他一辈子工作的核心）
- 鲁迅用 `-zawen`（杂文——一辈子的招牌文体）
- Stalin 用 `-gensek`（Генсек / 总书记——他的权力基础岗位）

新增 skill 时请沿用这个命名元原则（建议后缀例：费曼 `-teacher`、巴菲特 `-letter`、达里奥 `-principles`）。

---

## 安装

### 方式 A：复制到全局 skill 目录

```bash
git clone https://github.com/<your-fork>/zhuzi.git
cp -r zhuzi/<skill-name> ~/.claude/skills/
```

### 方式 B：直接用这个仓库作为工作区

```bash
git clone https://github.com/<your-fork>/zhuzi.git
cd zhuzi
claude
```

Claude Code 会自动识别当前目录下的 skill 目录。

---

## 激活

Claude Code 会按 skill 的 `description` frontmatter 字段匹配用户消息自动激活。也可以用触发词显式激活：

| Skill | 典型触发 |
|-------|---------|
| `linus-torvalds-engineer` | "用 Linus 视角"、"帮我 review 这段代码"、"good taste"、"torvalds mode" |
| `munger-checklist` | "用芒格视角"、"帮我审这个策略"、"过一遍 checklist"、"Lollapalooza" |
| `taleb-antifragile` | "用 Taleb 视角"、"这策略 antifragile 吗"、"fragility check"、"turkey 检查"、"Sharpe 在厚尾下靠谱吗" |
| `luxun-zawen` | "用鲁迅口吻"、"改成鲁迅腔"、"冷讽一下"、"阴阳怪气版" |
| `stalin-gensek` | "用斯大林视角"、"拆解这个权力结构"、"5 管道扫描"、"1937 味" |

完整触发词见各 skill 的 `SKILL.md` frontmatter。

---

## Skill 架构约定

每个 skill 目录遵循 Claude Code 的 Skill 规范：

```
<skill-name>/
├── SKILL.md                      # 入口，顶部 YAML frontmatter 声明 name/description/触发词
└── references/                   # SKILL.md 中链接的详细支撑材料
    ├── research/                 # 一手 / 二手来源调研（按维度编号）
    ├── anti-patterns.md          # 反模式识别库（可运行）
    ├── expression-levels.md      # 分级表达 DNA（可运行）
    ├── mental-models.md          # 心智模型详细版
    └── ...                       # 其他 checklist / playbook（因 skill 而异）
```

### 核心设计原则

1. **SKILL.md 是"激活即用"的主文件**——保持紧凑，细节下沉到 references
2. **证据链不可断**——每个心智模型 / anti-pattern / 表达档位都必须可追溯到 research 文件里的一手来源（LKML URL、访谈 transcript、股东会 / 党代会 / 著作原文）
3. **SKILL.md 用人物本人的品味写**——不是"关于他的描述"，是"他会怎么说"
4. **表达分级**（engineer v2 独有）——Level 1/2/3/4 按场景切档
5. **中文为主，技术术语保留英文**（如 `bikeshedding`、`good taste`、`Lollapalooza`、`Catechism`、`Kremlin`）。引用人物原话用原文（英语 / 俄语 / 古汉语）不翻译
6. **Self-contained 分发**——所有调研文件必须在 skill 目录内（`references/research/`），不依赖外部路径。复制整个 skill 目录就能独立使用

### 特殊类型（非思维顾问型）

- **`luxun-zawen` 是文体改写工具**：不做"鲁迅会怎么看 AI"这类思维顾问任务，只做文本风格转换。遇到思维顾问请求会退出角色并建议用其他 skill
- **`stalin-gensek` 是组织学案例研究**：不是智识典范。skill 拒绝"帮我在公司做清洗"等现代操作请求，自动重写为历史问题。详见 `stalin-gensek/references/ethical-boundary.md`

---

## 如何新增 skill

简化流程：

1. **调研**：收集一手来源（著作 / 访谈 / 决策记录），按维度写入 `<skill>/references/research/01-*.md` 到 `06-*.md`
2. **提炼**：用三重验证（跨域复现 / 生成力 / 排他性）筛选心智模型（3-7 个）、决策启发式、表达 DNA、反模式、诚实边界
3. **构建**：按 SKILL.md 模板（参考 `munger-checklist/SKILL.md` 或 `stalin-gensek/SKILL.md`）写入主文件，细节下沉到 references 子文件
4. **验证**：用已知测试 / 边缘测试 / 风格测试独立验证 skill 质量
5. **精炼**：用 skill-optimizer / skill-creator 双视角评审，应用不冲突改进

本仓库的所有 skill 都是用 [女娲 · Skill 造人术](https://github.com/alchaincyf/nuwa-skill) 流程生成的。

### 常见修改约定

详见 [CLAUDE.md](./CLAUDE.md)。要点：

- **v1 和 v2 共存**（如 `linus-torvalds-perspective` 与 `linus-torvalds-engineer`）——不要把 v2 改动回灌 v1
- **补证据再加观点**：新增 anti-pattern / 心智模型前先进 `references/research/`
- **信息截止点**：
  - Linus：持续更新（`07-updates-*.md`）
  - Munger：2023-11-28 去世后不补新事件
  - Taleb：持续更新（1960- 仍在世，2026-04 截止；每次更新关注 X @nntaleb、新技术论文、新 beefs）
  - 鲁迅：1936-10-19 去世后不补新事件
  - Stalin：1953-03-05 去世后不补新事件

---

## 无需运行的检查

没有 linter、没有测试。修改后的验证方式：

- **内部一致性**：SKILL.md 引用的 `references/*.md` 路径真实存在
- **证据一致性**：新增观点有对应的 research 文件支撑
- **触发词不与其他已安装 skill 冲突**（用户侧关注）

---

## 伦理与边界

每个 skill 都有**诚实边界** section 明确说明：
- 它做什么 / 不做什么
- 信息截止日期
- 学术争议未解决的部分（不强行收口）

特别是 `stalin-gensek`——作为极权历史人物的 skill，带有 6 条 Hard Rules（强制规则）+ E/F/G/H 四类拒答模板 + 假引用黑名单 + 具名活人匿名化护栏。skill 的存在不等于对该人物政权的认同——**理解权力工程学是防止重演的前提**。

---

## 贡献

欢迎 PR。新增 skill 请：

1. 遵循 [命名约定](#命名约定)（后缀贴合人物自我身份 / 方法论）
2. 遵循 [架构约定](#skill-架构约定)（SKILL.md 紧凑 + references 下沉）
3. 证据链完整（每个观点可追溯到一手 / 二手来源）
4. 对争议不强行收口（尤其历史人物 skill）
5. 诚实边界写明"做不到什么"

---

## License

MIT License. 调研使用的一手 / 二手来源版权归原作者所有。

---

*"我们所有人都会按自己的品味去读一个人——skill 的价值不在复制他的原话，而在于让你用他的眼睛看自己的问题。"*
