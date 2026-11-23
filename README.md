# zhuzi · 诸子

把人物的方法论做成可独立使用的 skill，再用具名席位取得同一议题的不同判断。圆桌保留分歧和证据，用户掌握取舍与实施授权。

## 使用方式

| 想要的结果 | Claude Code | Codex CLI |
|---|---|---|
| 一个指定人物的视角 | 例如「用 Linus 视角看这段代码」 | 同左，也可以直接用 `$linus-torvalds-engineer` |
| 并列听几个角度 | `/zhuzi:quick 议题` | `$zhuzi-quick 议题` |
| 正式审议，产出决策表和验证信号 | `/zhuzi:roundtable 议题` | `$zhuzi-roundtable 议题` |

单人物请求由对应 skill 处理。泛称「审代码」「讲清楚」「做 UX 审查」无需调用人物 skill。人物视角和常用别名见各入口的 `description`。

多视角短读并列 2–5 个具名席位的观点。正式圆桌先确定议题合同，由席位独立审议，再综合证据与冲突。只匹配一席时默认引导到对应的单人物 skill，正式圆桌可用「强制开圆桌」继续。正式圆桌默认使用短读呈现，要求「展开原文」或「展开 YAML」可查看完整证据。

参见 [正式流程](./zhuzi/workflows/roundtable.md)、[短读流程](./zhuzi/workflows/quick-multi.md)、[席位表](./zhuzi/references/seat-registry.md)、[机器合同](./zhuzi/manifests/roundtable-contract.json) 和 [正式圆桌模板](./zhuzi/templates/roundtable-quick.md)。输出示例见 [正式圆桌](./examples/roundtable-quick.md) 和 [短读](./examples/quick-multi.md)。

## 内置人物

### 可作为圆桌和短读席位

#### Linus Torvalds · `linus-torvalds-engineer`

从数据结构、接口和调用者审工程品味。代码席 `linus-engineer` 另负责可行性审查与获授权实施。

#### Charlie Munger · `munger-checklist`

逆推失败路径，审能力圈、激励、偏误和安全边际。决策质量席为 `munger-reviewer`。

#### Nassim Nicholas Taleb · `taleb-antifragile`

审厚尾、破产路径、收益凸凹性与风险承担。风险结构席为 `taleb-reviewer`。

#### Marcos López de Prado · `lopezdeprado-scientist`

区分关联与因果，检查泄漏、多重检验与独立验证。证据质量席为 `lopezdeprado-reviewer`。

#### Richard Feynman · `feynman-explainer`

用可观察机制、例子和反例拆开术语伪装。解释清晰度席为 `feynman-reviewer`。

#### Paul Graham · `paul-graham-perspective`

从实际用户、产品需求与 Maker 角色看创业，审 essay 是否推进了想法。创业席为 `paul-graham-reviewer`。

#### Don Norman · `don-norman-perspective`

诊断界面如何引导用户行动、反馈状态或诱发错误。可用性认知诊断席为 `don-norman-reviewer`。

### 单人物专用

#### 张雪峰 · `zhangxuefeng-perspective`

按专业和岗位的真实机会倒推中国志愿、考研与学校选择。

#### Elon Musk · `elon-musk-perspective`

拆工程成本、物理极限、供应链和制造流程，说明结论的适用条件。

#### Steve Jobs · `steve-jobs-perspective`

看产品定位、体验链条与应该舍弃的功能。

#### Donald Trump · `donald-trump-perspective`

分析商业谈判筹码、品牌叙事与危机公关。能力及使用边界见 [Skill](skills/donald-trump-perspective/SKILL.md)。

#### 鲁迅 · `luxun-zawen`

把给定文字改成白话杂文式冷讽，保留原意与受众关系。

## 安装

在仓库根目录执行。

```bash
python3 -m pip install -r requirements-dev.txt
./install.sh
```

默认安装 Claude Code 和 Codex CLI。只预览或升级 Codex 可分别使用 `./install.sh --codex-only --dry-run --json` 和 `./install.sh --codex-only`。覆盖根、备份、权限和安装边界见 [安装与迁移](./docs/openai-alignment.md#安装与迁移)。其它工具的接入条件见 [运行时支持](./docs/openai-alignment.md#运行时支持)。公开分发面见 [清单](./docs/INVENTORY.md) 与 [分发 manifest](./zhuzi/manifests/shipped-surface.json)。

## 维护

[AGENTS.md](./AGENTS.md) 提供任务路由、边界和完成标准。`skills/` 存人物入口和研究，`zhuzi/seats/` 存席位契约，`zhuzi/workflows/` 存共享流程，`runtimes/` 存原生入口与适配器。[开发验证](./docs/openai-alignment.md#开发验证) 列出检查、接线验收和评测命令。[archive/](archive/) 保留历史版本。

## License

MIT License. 人物研究的一手和二手来源版权归原作者所有。
