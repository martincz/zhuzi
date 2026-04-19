# archive/ · 已归档的历史 skill 版本

这里存放已被**新版本替代**的 skill——**不推荐安装到 `~/.claude/skills/`**，仅作为对比参考保留在仓库里。

## 为什么保留

- **对照研究**：新版 SKILL.md 顶部的 "与 v1 的差异" / `upgrade-notes.md` 引用这些文件
- **证据链完整**：v1 的 research 调研是 v2 的基础，不应随 v1 一起丢失
- **命名元原则的历史样本**：v1 的 `-perspective` 后缀、SKILL 结构代表了 zhuzi 早期做法

## 已归档清单

| 归档 skill | 替代者 | 归档日期 | 主要原因 |
|-----------|--------|----------|----------|
| `linus-torvalds-perspective/` | `linus-torvalds-engineer/`（仓库根）| 2026-04-20 | v2 是完整重写：把传记式思维参考升级为"可执行指令集"——Good Taste 7 步清单、12 条 anti-pattern、4 级表达档位、短路决策路由。v1 的使用场景被 v2 完全覆盖。两者的差异权威说明见 `linus-torvalds-engineer/references/upgrade-notes.md` |

## 归档 ≠ 删除

本目录的文件**不应从 git 历史删除**——这是 skill 演化的原始档案。v2 的任何"和 v1 对比"改动如果需要重读 v1，从这里读。

## 不要安装到 `~/.claude/skills/`

如果误装了 v1，会同时激活 v1 和 v2（两者触发词可能冲突，尤其是 "用 Linus 视角" 这类宽泛触发），导致不可预测的行为。**要用就用仓库根的新版**。

---

*归档不是废弃——是对既往工作的尊重，也是对新版的诚实。*
