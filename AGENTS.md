# AGENTS.md

本文件约定 agent 在本仓库及其子目录中的工作方式，遵循运行时的指令优先级和用户授权。更具体的目录说明按运行时的发现规则适用；本文不提升工具权限，也不声明覆盖系统、开发者或用户指令。

## 工作范围

- 按用户当前目标修改仓库，保留无关的已有改动，不回退他人的工作。
- 安装验证默认使用临时目录。实机安装、发布或推送只在任务授权范围内执行；已有明确授权直接沿用，范围发生实质变化时再确认。
- `CLAUDE.md` 仅作加载本文件的兼容入口，不另写一份工作规约。个人工具偏好放在运行时的全局配置中。

## 仓库性质

`zhuzi` 围绕 **skill + agent + roundtable** 三层模型组织。人物知识和议事说明用 Markdown，机器合同用 JSON，Codex 原生 adapter 用 TOML，安装与校验工具用 Python / Bash。修改前先分清自己在碰哪一层：

- **skill**（`skills/`）——单人物思维内核，直接对用户说话。
- **agent / seat**（`zhuzi/seats/` + `runtimes/*/agents/`）——协作席位契约与 runtime adapter，按当前议事模式向 orchestrator 回报。
- **roundtable**（`zhuzi/workflows/` + `runtimes/*` 入口）——议事编排与 gate 规则，不承载人物正文。

## 真相源与修改指针

按本次任务读取相关资产，不要求全量装载。说明、示例与摘要发生冲突时，以对应层的权威源为准；人读清单和生成投影不另创机读规则。

| 资产层 | 权威文件 | 改动入口 |
|---|---|---|
| 人物正文、触发词、anti-pattern、研究支撑 | `skills/<name>/SKILL.md` 及其 `references/` | 直接改对应 skill 目录 |
| 席位职责、越权边界、启动/阶段纪律 | `zhuzi/seats/<seat>.md` | 改 seat contract；保留 `## 输出契约` 生成块 marker |
| 席位注册、阶段路由、verdict 字段与类型 | `zhuzi/manifests/roundtable-contract.json` | 改 manifest，再运行 `python3 tools/render_roundtable_contract_docs.py` |
| 可执行 verdict 校验 | `zhuzi/validators/verdict.py` | 改执行逻辑；字段和路由仍从 manifest 派生，不内嵌第二份定义 |
| JSON Schema 投影 | `zhuzi/schemas/verdict.schema.json` | 只由 manifest 渲染，不手改 |
| Roundtable reference（seat-registry、verdict-schema）及 seat 输出契约投影段 | `zhuzi/references/*.md`、`zhuzi/seats/*.md` 的生成块 | 只改非生成说明段；生成块由 manifest 渲染 |
| Roundtable 流程、阶段、gate、Quick 行为 | `zhuzi/workflows/roundtable.md` | 先改 workflow，再看是否需要同步 runtime 入口 adapter |
| 输出骨架与渲染约定 | `zhuzi/templates/*.md` | 改对应 template，并检查示例 |
| 安装与分发清单 | `zhuzi/manifests/shipped-surface.json` | 同步 `docs/INVENTORY.md` 人读清单 |
| 安装、渲染、side-load 行为 | `install.sh` + `tools/install_codex_source_adapters.py` | 改脚本；行为以脚本本身为准 |

## 核心约束

以下约束适用于本项目资产及其修改，不扩展为其他项目的工作规约。

1. **共享源与薄 adapter**——人物正文留在 skill，席位职责留在 seat contract，议事流程留在 workflow。Adapter 只装载共享资产并映射运行时能力，不复制人物、schema 或另写席位语义。
2. **共享与适配边界**——共享资产不绑定单一 runtime，不写机器专属绝对路径；适配层使用对应 runtime 的原生格式和调用。源码模板可含 placeholder 与仓库 fallback，安装产物指向实际安装根。
3. **Skill / agent 路由**——standalone 思维顾问场景用 skill，协作席位场景才调用 agent。新增人物或席位时，校对 skill 触发说明与 agent description，避免误路由。
4. **共同契约与生成物**——正式 verdict 保持 `core` / `must_haves_review` / `must_haves_challenge` / `seat_specific` 的共享语义；其他模式遵循其共享模式规则。机器字段、native verdict 或 route 变更先改 manifest、重新渲染，再同步 adapter。禁止手改 `<!-- GENERATED: ... -->` 区块和生成的 JSON Schema。
5. **研究与示例边界**——新增人物观点、anti-pattern、表达档位或方法论约束前，先补研究依据与一手来源。具体项目的参数和业务结论留在示例或该项目文档，不写成通用合同。

## 环境与验证

命令均从仓库根目录执行。依赖入口为 `requirements-dev.txt`，优先使用已有或隔离的 Python 环境；需要安装时运行 `python3 -m pip install -r requirements-dev.txt`。

按变更范围选择检查，不因轻微文案修改运行完整模型评测：

| 任务或变更 | 验证要求 |
|---|---|
| 只读分析与审查 | 按需运行生成物 `--check` 和一致性检查；不生成或修复文件 |
| 文档、人物材料、工作约定 | 检查引用与一致性；行为要求有变化时增加对应验证 |
| Manifest、席位合同、议事流程、校验逻辑 | Manifest 变更后重新渲染；运行一致性与相关单元测试，覆盖有效、无效和边界情况 |
| 安装逻辑、原生 adapter、席位生命周期 | 在临时根做安装与离线 smoke；影响实际席位调用或续跑时再做在线验收 |

常用检查命令：

```bash
python3 -B tools/render_roundtable_contract_docs.py --check
python3 -B tools/check_consistency.py
python3 -B -m unittest discover -s tests -v
python3 -B tools/smoke_test_codex_roundtable.py --offline
python3 -B tools/smoke_test_codex_roundtable.py  # 在线调用模型，产生用量
```

验证报告分别说明结构一致性、协议校验、实际调用与判断质量的覆盖范围。离线 smoke 不替代在线验收，调用成功不证明判断质量；检查未运行、被环境阻塞或仍有已知缺口时明确列出，不报告为通过。支持范围及评测细节见 `docs/openai-alignment.md`。

## Code Review Rules

- **合同约束确实生效**：检查机器合同中的强制限制是否在执行链路中得到执行；条件路由的追加与覆盖语义应明确，不能把强制限制降级成可选条件，并用有效与无效组合验证。
- **完成状态有实际证据**：异步席位调用核对精确目标、成功状态和目标子线程的实际返回；父模型自报、字符串包含或只有调用记录都不足以证明完成。
- **对照条件可核实**：质量、用量和延迟比较应核对主持人与子席的有效模型及推理配置；有意混合模型的实验须明确标注，不能按同配置比较归因。格式与其他机械检查交给工具；评审指导不替代测试。

## 提交规范

- 提交信息遵循 `feat/fix/refactor/style/chore/docs` 前缀风格。
- 多行格式：首行摘要，后续用 `- ` 列出 1-3 条关键改动。
- 单次提交只解决一个问题。
- 除前缀外，提交信息其他内容必须使用中文。

格式示例：

```text
chore: 固化圆桌短读输出模板

- 新增 Quick Roundtable 示例
- 扩展一致性检查覆盖默认输出骨架
```

格式与加载规则参考 [AGENTS.md](https://agents.md/) 和 [OpenAI 指令发现说明](https://learn.chatgpt.com/docs/agent-configuration/agents-md)；评审规则的写法参考 [OpenAI 评审指导](https://learn.chatgpt.com/docs/third-party/github#customize-what-codex-reviews)。本仓库的架构、授权边界与验收约定由项目维护，不作为官方通用要求。
