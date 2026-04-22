# AGENTS.md

This file provides guidance to agent runtimes (Codex, Claude Code, and compatible tools) when working with code in this repository.

## 仓库性质

`zhuzi` 是一个围绕 **skill + agent + roundtable** 三层模型构建的开发仓库。全部资产都是 Markdown 驱动，由支持相应规范的 agent runtime 加载。

- `skills/`：用户直接触发的人物 skill
- `zhuzi/seats/` + `runtimes/*/agents/`：roundtable 席位契约与 runtime adapter
- `zhuzi/workflows/roundtable.md` + `runtimes/*` 入口：圆桌编排规则

修改前先分清三层边界：

- **skill** 是思想内核，直接对用户说话
- **agent** 是协作席位，对 orchestrator 返回结构化 verdict
- **roundtable adapter** 是入口和议事规则，不承载人物正文

若摘要性描述有漂移，以下列文件为准：

- `README.md`：仓库概览、目录结构、安装方式
- `zhuzi/workflows/roundtable.md`：Roundtable 权威流程与 gate 规则
- `zhuzi/manifests/roundtable-contract.json`：Quick headings、seat/stages/route、seat_specific 机器合同
- `zhuzi/references/seat-registry.md`：当前席位、默认 `stages`、召开纪律
- `zhuzi/references/verdict-schema.md`：共同 YAML verdict 契约
- `zhuzi/templates/roundtable-quick.md`：Quick Roundtable 默认骨架
- `docs/INVENTORY.md` + `zhuzi/manifests/shipped-surface.json`：shipped surface 真相源
- `install.sh` + `tools/install_codex_source_adapters.py`：安装、渲染、side-load 行为

## 提交规范

- 提交信息遵循 `feat/fix/refactor/style/chore` 前缀风格。
- 多行格式：首行摘要，后续用 `- ` 列出 1-3 条关键改动。
- 单次提交只解决一个问题。
- 除前缀外，提交信息其他内容必须使用中文。

示例：

```text
chore: 固化圆桌短读输出模板

- 新增 Quick Roundtable 示例
- 扩展一致性检查覆盖默认输出骨架
```

## 关键设计原则

1. **共享真相源优先**  
   席位职责、越权边界放在 `zhuzi/seats/`；Quick headings、seat/stages/route、`seat_specific` 机器合同放在 `zhuzi/manifests/roundtable-contract.json`；人读解释放在 `zhuzi/references/`。不要在 Claude/Codex adapter 里再各写一份。

2. **adapter 保持薄**  
   runtime adapter 只负责装载对应 skill、seat contract、shared schema 和 workflow，不复制人物正文，不内嵌大段 schema，不承载维护手册。

3. **runtime-agnostic 文案与路径**  
   共享资产和总规约不写死单一 runtime，不写死机器绝对路径。源码模板允许 placeholder 和仓库 fallback；安装后的产物应收敛到 installed root。

4. **skill / agent 路由护栏必须明确**  
   用户说“用 Linus 视角”这类 standalone 场景，应激活 skill；只有 roundtable 协作场景才调用 agent。新增人物或席位时，必须同时检查两侧触发词是否撞车。

5. **A 类思维顾问与 B 类聊天娱乐隔离**  
   思维顾问型 skill 不做口吻玩梗；聊天娱乐型 skill 不做决策建议。不要把娱乐改写伪装成严肃判断。

6. **能力边界按人物真实专长写，不按当前示例收窄**  
   席位和 skill 的职责应覆盖该人物真实擅长领域，不要被当前量化案例、现有示例或一时的落地项目绑死。

7. **证据链不可断**  
   新增人物观点、anti-pattern、表达档位或方法论约束前，先补对应 research / 来源。没有证据，不进主合同。

8. **硬约束与示例分离**  
   能跨项目成立的内容才进合同；项目、领域、工具链相关内容只作示例，不得冒充通用规则。

9. **Roundtable 共同契约不得私改方言**  
   `core`、`must_haves_review`、`must_haves_challenge`、`seat_specific` 的分层语义以 shared schema 为准。新增席位或 verdict 语义时，先补 shared schema，再改 adapter。

## 跨项目使用纪律

本仓库是 skill / agent / roundtable 资产的开发仓库，不是具体业务项目的工作仓库。

- 用户贴来别的项目里的 verdict、截图、圆桌输出或契约草稿时，默认意图是**改进本仓库的通用产物**。
- 不要把别的项目的业务结论、参数口径、领域纪律写进这里的通用文档。
- 如果用户意图不明，先分清他是要改本仓库，还是要讨论那个具体议题本身。
- 所有总规约都应尽量保持跨项目成立；量化、Web、文档、编译产物等示例只能帮助理解，不能替代定义。

## 修改指针

- 改人物正文、触发词、研究引用、anti-pattern：去对应 `skills/<name>/`
- 改席位职责、越权边界、输出 root、seat-specific 字段：去 `zhuzi/seats/*.md`
- 改 Roundtable 机器合同（Quick headings、seat/stages/route、seat-specific 注册）：去 `zhuzi/manifests/roundtable-contract.json`
- 改当前席位、默认 `stages`、召开纪律：去 `zhuzi/references/seat-registry.md`
- 改共同 verdict schema：去 `zhuzi/references/verdict-schema.md`
- 改 Roundtable 阶段、gate、Quick 行为：先改 `zhuzi/workflows/roundtable.md`，再看是否需要改入口 adapter
- 改 shipped surface：同步 `docs/INVENTORY.md` 与 `zhuzi/manifests/shipped-surface.json`
- 改安装或路径渲染：去 `install.sh` 与 `tools/install_codex_source_adapters.py`

## 无需运行的检查

修改后的最小验证：

- 运行 `python3 tools/check_consistency.py`
- 若动了 roundtable surface、shared schema、Codex adapter 或安装路径，再跑 `python3 tools/smoke_test_codex_roundtable.py`

额外自查：

- 路径真实存在
- 没有把机器专属路径写进 active 文档
- 没有把某个项目的业务纪律泄漏进通用合同
- adapter、workflow、registry、schema、inventory、manifest 之间没有重复维护同一份真相
