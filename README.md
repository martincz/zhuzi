# zhuzi · 诸子

把人物的方法论提炼为按需加载的独立框架，再用具名席位在同一议题上取得独立判断。默认收敛安装为单一 `skills/zhuzi/` 入口，不污染全局技能目录；圆桌保留真实分歧与可追溯证据，由用户掌握关键取舍与实施授权。

## 使用方式

| 想要的结果 | Claude Code | Codex CLI | Antigravity CLI |
|---|---|---|---|
| 查看推荐模式与人物菜单 | `/zhuzi` | `$zhuzi` | `/zhuzi` |
| 指定单个人物的视角 | `/zhuzi linus 看这段代码` | `$zhuzi linus 看这段代码` | `/zhuzi linus 看这段代码` |
| 并列听几个独立角度（不拍板） | `/zhuzi quick 议题` | `$zhuzi quick 议题` | `/zhuzi quick 议题` |
| 正式审议，产出决策表和验证信号 | `/zhuzi roundtable 议题` | `$zhuzi roundtable 议题` | `/zhuzi roundtable 议题` |
| 按需将高频人物固定为顶层快捷指令 | `./install.sh --pin linus` → `/linus-torvalds-engineer` | 同左 → `$linus-torvalds-engineer` | 同左 |

默认通过显式调用 `/zhuzi` 或 `$zhuzi` 启用（`disable-model-invocation: true` / `allow_implicit_invocation: false`）；泛称「审代码」「讲清楚」「做 UX 审查」绝不自动误触发人物视角或圆桌。

多视角短读（`quick-multi`）并列 2–5 个具名席位的独立短评，不走 `must_haves`、不走 gate、不做综合。正式圆桌（`roundtable`）先定义可验证议题合同，由席位独立盲审后再综合证据与分歧；只命中 1 席时默认引导至对应单人物视角（声明「强制开圆桌」或 `force roundtable` 才继续）。正式圆桌默认按短读骨架呈现，要求「展开原文」或「展开 YAML」时附完整记录。

权威资产见 [总控路由入口](./skills/zhuzi/SKILL.md)、[正式圆桌流程](./zhuzi/workflows/roundtable.md)（`zhuzi/workflows/roundtable.md`）、[短读流程](./zhuzi/workflows/quick-multi.md)、[席位契约目录](./zhuzi/seats/)（`zhuzi/seats/`）、[席位表](./zhuzi/references/seat-registry.md)、[机器合同](./zhuzi/manifests/roundtable-contract.json) 与 [正式圆桌模板](./zhuzi/templates/roundtable-quick.md)。代表性输出见 [正式圆桌示例](./examples/roundtable-quick.md) 和 [短读示例](./examples/quick-multi.md)。

## 内置人物

### 可作为圆桌与短读席位

#### Linus Torvalds · `linus-torvalds-engineer`

子指令别名 `linus` / `torvalds`。从数据结构、接口边界与特殊情况消解审工程品味。代码席 `linus-engineer` 另负责代码可行性审查与获授权实施。

#### Charlie Munger · `munger-checklist`

子指令别名 `munger`。逆向推演失败路径，审能力圈、激励错配、偏误叠加与安全边际。决策质量只读席为 `munger-reviewer`。

#### Nassim Nicholas Taleb · `taleb-antifragile`

子指令别名 `taleb`。审厚尾分布、破产路径、payoff 凸凹性与下行风险承担。风险结构只读席为 `taleb-reviewer`。

#### Marcos López de Prado · `lopezdeprado-scientist`

子指令别名 `lopez` / `prado`。区分关联与因果声明，审查数据泄漏、多重检验与独立验证设计。证据质量只读席为 `lopezdeprado-reviewer`。

#### Richard Feynman · `feynman-explainer`

子指令别名 `feynman`。用可观察机制、正反例与可验证语义拆解术语伪装。解释清晰度只读席为 `feynman-reviewer`。

#### Paul Graham · `paul-graham-perspective`

子指令别名 `pg` / `paul-graham`。从真实用户需求、Maker 视角与超线性回报看创业及职业选择，审 essay 是否生成新想法。创业只读席为 `paul-graham-reviewer`。

#### Don Norman · `don-norman-perspective`

子指令别名 `norman` / `don-norman`。诊断界面可发现性、状态反馈、概念模型与误操作归因（slip vs mistake）。可用性认知诊断只读席为 `don-norman-reviewer`。

### 单人物专用

#### 张雪峰 · `zhangxuefeng-perspective`

子指令别名 `zhangxuefeng`。按普通毕业生就业中位数与真实招聘入口倒推中国高考志愿、专业与考研选择。

#### Elon Musk · `elon-musk-perspective`

子指令别名 `musk` / `elon-musk`。用第一性原理、物理渐近极限、白痴指数与五步算法拆解工程成本与制造流程，并标明治理领域局限。

#### Steve Jobs · `steve-jobs-perspective`

子指令别名 `jobs` / `steve-jobs`。审视一句话产品定位、端到端体验链控制与功能砍削取舍。

#### Donald Trump · `donald-trump-perspective`

子指令别名 `trump`。分析商业谈判筹码、BATNA、品牌叙事与短期危机反击节奏；非政治立场与人身攻击工具，边界见 [Skill](skills/donald-trump-perspective/SKILL.md)。

## 安装、固定与清理

在仓库根目录执行：

```bash
python3 -m pip install -r requirements-dev.txt
./install.sh --dry-run
./install.sh
```

`./install.sh` 默认将全部技能收敛安装为单一 `~/.claude/skills/zhuzi` 与 `~/.agents/skills/zhuzi` 目录（排除 `references/research/` 等研发底稿），并自动备份迁移旧版散落的顶层技能与旧 `commands/zhuzi/`。常用管理选项：

- 仅预览或安装单端：`./install.sh --codex-only [--dry-run] [--json]` · `./install.sh --claude-only [--dry-run] [--json]`
- 固定或取消固定独立顶层快捷 Skill：`./install.sh --pin linus` · `./install.sh --unpin linus`
- 安全卸载已安装诸子资产：`./install.sh --uninstall`

隔离目录、备份回滚与跨 CLI 席位映射见 [运行时、维护与验证](./docs/openai-alignment.md#安装与迁移) 与 [运行时支持](./docs/openai-alignment.md#运行时支持)。公开分发面见 [清单](./docs/INVENTORY.md) 与 [分发 manifest](./zhuzi/manifests/shipped-surface.json)。

## 维护

仓库协作边界、按需读取入口与完成标准见 [AGENTS.md](./AGENTS.md)。检查、接线探针与行为评测命令见 [开发验证](./docs/openai-alignment.md#开发验证)。历史归档见 [archive/](archive/)。

## License

MIT License. 人物研究的一手和二手来源版权归原作者所有。
