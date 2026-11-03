# Quick Multi-Perspective Workflow

> 这是 `/zhuzi:quick` 的权威 workflow。**轻量多视角短读**——召集 N 个席位平行出短观点，不走 must_haves、不走 gate、不走 verdict schema、不做综合。
>
> 服务场景：用户想"快速听几个角度"，不想拍板、不想走 5 阶段流水线。
>
> 不能替代 roundtable：要保留分歧并落到决策表，仍然走 `/zhuzi:roundtable`。

## 与 roundtable 的边界

| 维度 | `/zhuzi:quick` | `/zhuzi:roundtable` |
|---|---|---|
| 目的 | 听角度 | 拍板 |
| 输出 | 平铺段落 | 决策表 + 验证信号 |
| 用户 gate | 无 | 阶段 0.5 / 阶段 1.5 / 阶段 3 |
| verdict schema | 不用 | 必填 4 层 |
| must_haves | 不定义 | 必定义 |
| 席位数 | N=2..5 | N≥2（默认期望 3）|
| N=1 行为 | 直接退出建议调 standalone skill | 同左（默认短路） |

## 流程

### Step 1 · 席位匹配

扫议题关键词，按 `seat-registry.md` 的"擅长领域"列匹配。

- **N=0**：停。建议改议题或直接和 orchestrator 对话。
- **N=1**：停。建议直接调对应 standalone skill（`<persona> 视角` / `#<trigger>`）。
- **N=2..5**：进 Step 2。
- **N>5**：保留前 5 个最相关；超出的弃权一句话说明。

### Step 2 · 并行 spawn

在运行时并发容量内 spawn 全部匹配席位，超出的排队。每个席位的 prompt 极简：

```text
invoke_seat(seat="<seat>", message="""
mode: quick-multi
[quick-multi 模式 — 不走 verdict schema]

议题：<议题原文>

请用你的视角给一段短观点（≤ 200 字）：
- 这个议题在你的视角下，最关键的 1-2 点是什么
- 用人物本来的判断词（fragile / kill / cargo cult / broken / 等）下结论
- 不输出 YAML，不做 must_haves 分析，不做综合
- 不要替主持人拍板

格式：纯散文一段，开头一句结论，后面给理由。
""")
```

**席位侧约束**：

- 席位 agent 收到 `[quick-multi 模式]` 标记时**不输出 verdict YAML**——这是和 roundtable 的关键差异。若仍返回 YAML，要求该席按 Quick 模式重新给出短观点；重试仍失败则标记该席协议失败，不靠剥掉 YAML 伪装成模式已正确执行。
- 席位仍按自己的人物 DNA 说话（Linus 仍然 sane/broken，Taleb 仍然 fragile/robust），但只做一段话级别的判断。

### Step 3 · 平铺呈现

按 `templates/quick-multi.md` 输出。骨架：

```markdown
# Quick Multi-Perspective: <议题摘要>

> N 视角短读 · 不做综合 · 拍板请走 `/zhuzi:roundtable`

## <Persona-A>（<seat-id>）

<席位返回的段落 ≤ 200 字>

## <Persona-B>（<seat-id>）

<同上>

...

## 一句话对照

| 席位 | 一句话结论 |
|---|---|
| <Persona-A> | <从段落里压出 1 句结论> |
| <Persona-B> | <同上> |

## 下一步建议

- 想拍板 → `/zhuzi:roundtable <议题>`
- 想深聊某个角度 → 直接调对应 skill（`<persona> 视角`）
```

## orchestrator 纪律

- **不做综合**：哪个对哪个错由用户判断。orchestrator 不写"主持人结论"，不下"哪个席位更可信"的 meta 评语。
- **不强求席位间对齐**：A 席说 fragile / B 席说 keep 直接并列即可，不要尝试调和。
- **一句话对照表是"压缩"不是"评判"**：把每席段落里那一句结论**字面**抽出来，不重写，不软化。
- **不延伸进 roundtable**：用户没说"开圆桌"前不得自动升级。Step 3 末尾可以给路径建议（`/zhuzi:roundtable`），但仅作为 affordance。

## 不做的事（防止协议蔓延）

- 不定义 must_haves、不要 verify_commands、不写 DECISIONS 表
- 不做阶段 1.5 修订 gate
- 不做用户多选确认（quick 模式下用户只读不拍板）
- 不调用 Linus 的实施能力（`/zhuzi:quick` 永远不进实施阶段）

如果用户在 `/zhuzi:quick` 输出后说"按 X 席的建议改一下代码"——orchestrator 提示走 `/zhuzi:roundtable` 或直接对话调用 Linus skill，**不**在 quick 协议内动文件。
