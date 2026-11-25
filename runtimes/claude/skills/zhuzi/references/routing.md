# 诸子路由菜单与选型指引

当用户无参数调用 `$zhuzi` / `/zhuzi` 或询问不知该选哪种模式时读取本文件，给出 2–3 条针对性调用建议并展示简明菜单，**不自动执行任何子指令**。

## 1. 先选协作粒度

| 你的目标 | 推荐调用方式（Codex / Claude Code） | 特点 |
|---|---|---|
| **已有可验证决策或代码方案，需形成决策表与过关标准** | `$zhuzi roundtable <议题>` / `/zhuzi roundtable <议题>` | 具名席位盲审 `must_haves` 合同，保留分歧与硬阻断，可选进入获授权实施 |
| **只想快速并列听 2–5 个不同维度的独立短评** | `$zhuzi quick <议题>` / `/zhuzi quick <议题>` | 每席 ≤200 字纯散文观点，无 YAML、无 gate、不做综合仲裁、绝不改文件 |
| **明确想借某一位人物的思维工具深挖单点问题** | `$zhuzi <人物别名> <问题>` / `/zhuzi <人物别名> <问题>` | 单线程加载对应人物核心框架与按需参考章节，轻量低开销 |

## 2. 易混人物视角互补速查

- **回测、实验与风险议题**：
  - 查因果声明、数据泄漏、多重检验与研究工作流 → `lopez`（`lopezdeprado-scientist`）
  - 查单次归零破产路径、厚尾暴露与上下行不对称 → `taleb`（`taleb-antifragile`）
  - 查商业激励扭曲、能力圈与认知偏误叠加 → `munger`（`munger-checklist`）
- **产品、界面与创业议题**：
  - 查一句话聚焦定位与功能砍削取舍 → `jobs`（`steve-jobs-perspective`）
  - 查用户看不懂/点错的执行与评估鸿沟及无障碍阻断 → `norman`（`don-norman-perspective`）
  - 查早期真实用户痛点、PMF 真伪与文章说服力 → `pg`（`paul-graham-perspective`）
- **代码、架构与工程规格议题**：
  - 查数据结构设计、消除 `if` 特判与向后兼容 → `linus`（`linus-torvalds-engineer`）
  - 查规格文档是否用黑话/命名冒充可验证机制 → `feynman`（`feynman-explainer`）
  - 查物理极限成本、原材料白痴指数与流程删减 → `musk`（`elon-musk-perspective`）
- **特定场景专用工具（不参与多席圆桌）**：
  - 商业谈判筹码与 BATNA 底牌 → `trump`（`donald-trump-perspective`）
  - 中国本土高考志愿/专业/考研就业中位数倒推 → `zhangxuefeng`（`zhangxuefeng-perspective`）
