# zhuzi · 诸子

> **诸子**——把不同人物的方法论做成可运行的 skill，并把它们接到同一张 roundtable 上。
>
> A runtime-agnostic toolkit for persona skills, roundtable seats, and shared deliberation workflows.

---

## 项目作用

`zhuzi` 不是一个单一人格 prompt 集合，而是一套分层资产：

- **skill**：单人物视角，直接对用户说话
- **agent seat**：roundtable 席位，对 orchestrator 返回结构化 verdict
- **roundtable**：把多个席位放到同一条流程里审议一个议题

它的目标不是把不同学派揉成“通用智慧”，而是把分歧保留下来，并让这些分歧进入一个可执行、可验证、可复盘的协作流程。

## 使用方式

| 用法 | 适合场景 | 结果 |
|---|---|---|
| 直接触发单个 skill | 想用某一人物视角审代码、看研究、改口吻 | 模型以该人物的思维框架直接回应 |
| Claude：`/zhuzi:roundtable <议题>` | 议题需要多视角审议 | 默认输出议题卡、席位短评和决策表 |
| Codex：触发 `zhuzi-roundtable` skill | 同样的多席位审议，但走 Codex orchestrator skill | 共享同一套 workflow / schema / Quick 模板 |

快速了解默认输出长相：看 [Quick Roundtable 示例](./examples/roundtable-quick.md)。  
当前 shipped surface 的人读清单：看 [docs/INVENTORY.md](./docs/INVENTORY.md)。  
机器可读真相源：看 [zhuzi/manifests/shipped-surface.json](./zhuzi/manifests/shipped-surface.json)。

## 核心组成

| 层 | 位置 | 作用 |
|---|---|---|
| Skills | `skills/` | 单人物思维操作系统 |
| Shared seat contracts | `zhuzi/seats/` | 席位职责、越权边界、route 语义、输出契约 |
| Runtime adapters | `runtimes/claude/`、`runtimes/codex/` | 薄 wrapper，负责装载 shared assets |
| Workflow | `zhuzi/workflows/roundtable.md` | roundtable 权威流程 |
| Shared references | `zhuzi/references/` | 席位表、schema、路由规则 |
| Templates / manifests | `zhuzi/templates/`、`zhuzi/manifests/` | Quick 输出骨架与 shipped surface 真相源 |

一句话关系：**skill 是思想内核，agent 是协作席位，roundtable 是议事规则。**

## 内置人物

| Skill | 定位 | Roundtable 角色 |
|---|---|---|
| `linus-torvalds-engineer` | 工程、架构、good taste 思维顾问 | `linus-engineer`，唯一代码席 |
| `munger-checklist` | 决策质量、偏误、激励结构思维顾问 | `munger-reviewer`，决策质量席 |
| `taleb-antifragile` | 尾部风险、fragility、antifragile 思维顾问 | `taleb-reviewer`，风险结构席 |
| `lopezdeprado-scientist` | 研究诚信、causal claim、实验纪律思维顾问 | `lopezdeprado-reviewer`，证据质量席 |
| `luxun-zawen` | 聊天娱乐型文体改写工具 | 不进 roundtable |

更具体的人物正文、触发词和研究支撑都在各自的 `SKILL.md` 与 `references/` 内；README 只保留入口级说明，不重复维护这些细节。

## 安装

### 方式 A：一键安装

```bash
git clone https://github.com/<your-fork>/zhuzi.git
cd zhuzi
./install.sh
```

`install.sh` 会把 shipped surface 安装到 Claude 和 Codex 的默认根目录；具体渲染与拷贝行为以脚本本身和 manifest 为准。

### 方式 B：本地试用 Codex roundtable adapter

`runtimes/codex/` 当前仍是 **source-only adapter**，不进主 shipped surface。要本地试用：

```bash
./install.sh
python3 tools/install_codex_source_adapters.py
```

### 方式 C：只装单个 skill

```bash
cp -r skills/<skill-name> ~/.claude/skills/
cp -r skills/<skill-name> "${CODEX_HOME:-$HOME/.codex}/skills/"
```

这只安装 persona skill，不安装 roundtable 入口和 seat adapter。

## 仓库布局

```text
zhuzi/
├── skills/                     # 单人物 skill
├── runtimes/
│   ├── claude/                 # Claude shipped adapters
│   └── codex/                  # Codex source-only adapters
├── zhuzi/
│   ├── seats/                  # 共享 seat contracts
│   ├── references/             # seat-registry / verdict-schema
│   ├── workflows/              # 权威流程正文
│   ├── templates/              # Quick 输出骨架
│   └── manifests/              # shipped surface 真相源
├── docs/INVENTORY.md           # shipped surface 的人读清单
├── examples/roundtable-quick.md
├── AGENTS.md                   # 仓库协作总规约
├── CLAUDE.md                   # 指向 AGENTS.md 的兼容 shim
├── install.sh
└── tools/
```

如果你要找 roundtable 的权威文件，先看这些路径：

- `zhuzi/workflows/roundtable.md`
- `zhuzi/seats/`
- `zhuzi/references/seat-registry.md`
- `zhuzi/references/verdict-schema.md`

## 激活示例

### 直接触发 skill

```text
用 Linus 视角 review 这段代码
用 Taleb 视角看这个方案 fragile 不 fragile
用鲁迅口吻把这句话改得更损一点
```

完整触发词看各 skill 顶部 frontmatter，不在 README 里重复抄一遍。

### 召开圆桌

```text
/zhuzi:roundtable 这个 API 设计该不该先重构再扩功能
```

默认输出是短读格式：`主持人结论 → 议题卡 → 席位短评 → 决策表 → 下一步`。  
完整原文和 YAML 只在你要求 `展开原文 / 展开 YAML / full / strict` 时展示。

## 协作与验证

仓库级协作纪律统一写在 [AGENTS.md](./AGENTS.md)。`CLAUDE.md` 只是一个兼容 shim，不是另一份规则。

最小验证流程：

```bash
python3 tools/check_consistency.py
```

如果你动了 roundtable surface、shared schema、Codex adapter 或安装路径，再跑：

```bash
python3 tools/smoke_test_codex_roundtable.py
```

## 伦理与边界

每个 skill 都应明确说明：

- 它做什么，不做什么
- 信息截止日期或更新策略
- 哪些结论是原话，哪些只是基于原则的推演
- 在 roundtable 里哪些批评只能打到 pattern，不应下沉为对具体人或具体项目的攻击

这些边界应写在 skill 本体和 shared contract 里，而不是散落在 README 段落里。

## 贡献

欢迎 PR。改动前先分清你碰的是哪一层：

- 人物正文、触发词、anti-pattern、研究支撑：改 `skills/<name>/`
- 席位职责、越权边界、输出 root、seat-specific 字段：改 `zhuzi/seats/*.md`
- 席位表、默认 `stages`、召开纪律：改 `zhuzi/references/seat-registry.md`
- 共同 verdict schema：改 `zhuzi/references/verdict-schema.md`
- Roundtable 流程：先改 `zhuzi/workflows/roundtable.md`
- shipped surface：同步 `docs/INVENTORY.md` 与 `zhuzi/manifests/shipped-surface.json`
- 安装或 side-load 行为：改 `install.sh` 与 `tools/install_codex_source_adapters.py`

如果你要新增人物或新增席位，先把共享真相源补齐，再去写 runtime adapter。不要先写 wrapper，再回头补合同。

## License

MIT License. 调研使用的一手 / 二手来源版权归原作者所有。

---

*"诸子百家"不是为了合流成平均主义，而是为了把分歧摆上桌。*
