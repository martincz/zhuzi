# AGENTS.md

## 自主权与安全红线

- **本地自主执行**：在用户授权范围内，直接完成代码与文档修改、生成物渲染、一致性校验、单元测试、隔离目录安装排错与失败修复，可逆的常规工程选择自行决定，无需逐步请示。仅在存在不可逆取舍、实质范围扩大或缺少必要授权时向用户确认。
- **环境与数据红线**：保留工作区无关改动与既有数据，不擅自回退他人工作或执行破坏性清理。安装与迁移验证必须使用临时隔离目录（覆盖 `CLAUDE_DIR` / `CODEX_HOME` / `CODEX_SKILL_DIR`）；写入实机用户目录、生产/共享环境，或执行提交、发布、推送，均须有覆盖该操作的明确授权。遵守运行时沙箱与权限边界，严禁在日志、示例或仓库文件中复制、打印或泄露凭证与未授权私有数据。
- **只读边界**：只读分析、审计或评议任务仅做检查与报告，不写入、生成或修改文件。

## 按任务查阅

按当前任务类型或改动目录按需读取对应入口，不预先全量加载仓库文档或研究材料：

| 任务类型 | 按需读取与修改入口 |
|---|---|
| 统一入口与单人物方法 | 总控路由见 [skills/zhuzi/SKILL.md](skills/zhuzi/SKILL.md)，单人物内核见 [skills/](skills/) 下 `<name>/SKILL.md`，仅按目标章节只读 `references/` 子文档。新增人物判断、反模式或方法论约束须有一手来源依据。 |
| 正式圆桌与多视角短读 | 编排流程见 [zhuzi/workflows/](zhuzi/workflows/)，席位职责与读写边界见 [zhuzi/seats/](zhuzi/seats/)，输出骨架见 [zhuzi/templates/](zhuzi/templates/)。 |
| 机器合同、Schema 与校验 | [roundtable-contract.json](zhuzi/manifests/roundtable-contract.json) 与 [shipped-surface.json](zhuzi/manifests/shipped-surface.json) 为唯一真相源，[verdict.py](zhuzi/validators/verdict.py) 执行跨字段与覆盖率校验。修改清单后运行 [render_roundtable_contract_docs.py](tools/render_roundtable_contract_docs.py) 更新生成物。 |
| 运行时适配、安装与分发 | [runtimes/](runtimes/)、[install.sh](install.sh)、[install_codex_source_adapters.py](tools/install_codex_source_adapters.py)。分发清单同步至 [INVENTORY.md](docs/INVENTORY.md)；跨 CLI 规范与评测见 [openai-alignment.md](docs/openai-alignment.md)。 |

## 架构与口径不变量

- **纯开放共享源与下沉薄 Adapter**：根 `skills/*/SKILL.md` 严守 `agentskills.io` 开放规范（不混入单一宿主私有字段），Codex 侧车统一由 `agents/openai.yaml` 承载，Claude 控制项与席位工具白名单收敛在 `runtimes/claude/`。默认仅安装单一顶层 `skills/zhuzi/` 目录（内含各人物运行期 `personas/`，排除 `references/research/` 等研发底稿，支持 `--pin` 按需固定高频独立入口）。`CLAUDE.md` 仅保留 `@AGENTS.md`。
- **生成物与机器合同口径**：严禁手改 `<!-- GENERATED:... -->` 区块、`zhuzi/schemas/verdict.schema.json`、双端席位 adapter、`agents/openai.yaml` 与 `docs/INVENTORY.md`。正式圆桌 verdict 四层结构（`core` / `must_haves_review` / `must_haves_challenge` / `seat_specific`）、`truths` 逐条全覆盖、首轮盲审 `peer_disagreements: []`、阶段 4 `commit_status: not_committed` 及条件路由 `override` 不可被 `add` 放宽等不变量不得弱化。
- **路由与权限隔离**：总控入口与人物视角默认关闭隐式自动触发（常规开发/文档/UX 请求不自动触发人物或圆桌）；评议席位（`*-reviewer`）锁死只读工具集，仅实施席 `linus-engineer` 在阶段 4 锁定授权范围内可修改代码与运行验证。

## 验证与完成标准

修改任务须完成 **实现 → 运行对应检查 → 核对输出 → 修复失败 → 重新验证通过** 闭环后方可结束：

```bash
python3 -B tools/render_roundtable_contract_docs.py --check  # 改清单先去掉 --check 重渲染
python3 -B tools/check_consistency.py
python3 -B -m unittest discover -s tests -v
python3 -B tools/smoke_test_codex_roundtable.py --offline
```

协议或校验逻辑变更须覆盖有效、无效与边界用例。涉及具名席位真实调用或同线程续跑时，按 [开发验证](docs/openai-alignment.md#开发验证) 执行在线探针。离线结构校验、在线调用证据与判断质量分别报告；未运行或受环境阻塞的检查如实说明，不得报为通过。

## Code Review Rules

- 核对强制路由在 JSON Schema 与 `verdict.py` 验证链上同时生效；命中 `override` 条件时，`add` 规则不得放宽允许范围，条件冲突须 fail-closed。
- 核对异步席位的真实具名调用、成功状态与目标子线程的新完成返回；父会话自报或仅有调用记录不足以证明完成。
- 对比判断质量、用量或延迟时，核对主持人与各子席的有效模型和推理档位；有意混用须注明，配置未知或不一致的运行不得用于同配置归因。

## 提交规范

提交使用 `feat/fix/refactor/style/chore/docs` 前缀。单次提交聚焦单一问题，首行中文摘要后空一行，用 1–3 条 `- ` 列出中文关键改动。
