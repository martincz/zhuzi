# Quick Multi Template

> `/zhuzi:quick` 的输出骨架。与 roundtable 的 Quick 模板**根本不同**：无议题卡、无 must_haves、无 DECISIONS 表、无验证信号。只有 N 个并列段落和一张压缩对照表。

## 渲染约定（精简）

- **段落标题**：`## <Persona 中文/英文显示名>（<seat-id>）`，不带 emoji 不带角色描述
- **段落内容**：席位返回的散文，≤ 200 字。如果席位返回了 YAML，剥掉。
- **一句话对照表**：从每段散文里**字面**抽出第一句结论，不重写不软化
- **席位顺序**：按召开顺序（语义匹配度高的在前），不按字母不按观点
- **多席位说同一件事**：保留所有段落，**不**合并；对照表里照样并列
- **冲突场景**：A 席 fragile / B 席 keep —— 直接并列，**不**加 orchestrator 仲裁

## 骨架

```markdown
# Quick Multi-Perspective: <议题 ≤ 30 字摘要>

> N 视角短读 · 不做综合 · 拍板请走 `/zhuzi:roundtable`

## <Persona-A>（<seat-id-a>）

<席位返回的散文段落，≤ 200 字>

## <Persona-B>（<seat-id-b>）

<同上>

## <Persona-C>（<seat-id-c>）

<同上>

## 一句话对照

| 席位 | 一句话结论 |
|---|---|
| <Persona-A> | <字面抽取的第一句结论> |
| <Persona-B> | <同上> |
| <Persona-C> | <同上> |

## 下一步建议

- 想拍板（出决策表 + 验证信号）→ `/zhuzi:roundtable <议题>`
- 想深聊某个视角 → 直接调对应 skill（`<persona> 视角` / `#<trigger>`）
```

## 禁用

- 不加"主持人结论"段
- 不加 "DECISIONS 表 / 验证信号 / 议题卡 / must_haves"
- 不加 orchestrator meta 评语段（"三席观点高度一致……"）
- 不加 emoji
