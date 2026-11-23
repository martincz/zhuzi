# AGENTS.md

## 自主权与安全红线

- **本地自主执行**：在用户授权范围内，直接完成代码与文档修改、生成物渲染、一致性校验、单元测试、隔离目录安装排错与失败修复，可逆的常规工程选择自行决定，无需逐步请示。仅在存在不可逆取舍、实质范围扩大或缺少必要授权时向用户确认。
- **环境与数据红线**：保留工作区无关改动与既有数据，不擅自回退他人工作或执行破坏性清理。安装与迁移验证必须使用临时隔离目录（覆盖 `CLAUDE_DIR` / `CODEX_HOME` / `CODEX_SKILL_DIR`）；写入实机用户目录、生产/共享环境，或执行提交、发布、推送，均须有覆盖该操作的明确授权。遵守运行时沙箱与权限边界，严禁在日志、示例或仓库文件中复制、打印或泄露凭证与未授权私有数据。
- **只读边界**：只读分析、审计或评议任务仅做检查与报告，不写入、生成或修改文件。

## 按任务查阅

按当前任务类型或改动目录按需读取对应入口，不预先全量加载仓库文档或研究材料：

| 任务类型 | 按需读取与修改入口 |
|---|---|
| 单人物方法、触发与边界 | 对应 [skills/](skills/) 下 `<name>/SKILL.md`，仅在任务需要时选读其 `references/` 子文档。新增人物判断、反模式或方法论约束须有一手来源依据。 |
| 正式圆桌与多视角短读 | 编排流程见 [zhuzi/workflows/](zhuzi/workflows/)，席位职责与读写边界见 [zhuzi/seats/](zhuzi/seats/)，输出骨架见 [zhuzi/templates/](zhuzi/templates/)。 |
| 机器合同、Schema 与校验 | [roundtable-contract.json](zhuzi/manifests/roundtable-contract.json) 为路由、字段与类型的唯一真相源，[verdict.py](zhuzi/validators/verdict.py) 执行跨字段与覆盖率校验。修改合同后运行 renderer 更新生成物。 |
| 运行时适配、安装与分发 | [runtimes/](runtimes/)、[install.sh](install.sh)、[install_codex_source_adapters.py](tools/install_codex_source_adapters.py)。分发面以 [shipped-surface.json](zhuzi/manifests/shipped-surface.json) 为准并同步 [INVENTORY.md](docs/INVENTORY.md)；跨 CLI 规范与评测见 [openai-alignment.md](docs/openai-alignment.md)。 |

## 架构与口径不变量

- **共享源与薄 Adapter**：人物内核留在 `skills/`，席位契约留在 `zhuzi/seats/`，议事编排留在 `zhuzi/workflows/`。共享资产保持跨运行时（兼容 Codex CLI、Antigravity CLI、Claude Code CLI），严禁硬编码机器专属路径或绑定单一运行时工具原语。`runtimes/` 仅装载共享资产并映射宿主能力，不内联复制人物正文或 verdict schema。`CLAUDE.md` 仅保留 `@AGENTS.md`。
- **生成物与机器合同口径**：严禁手改 `<!-- GENERATED:... -->` 区块与 `zhuzi/schemas/verdict.schema.json`。正式圆桌 verdict 四层结构（`core` / `must_haves_review` / `must_haves_challenge` / `seat_specific`）、`truths` 逐条全覆盖、首轮盲审 `peer_disagreements: []`、阶段 4 `commit_status: not_committed` 及条件路由 `override` 不可被 `add` 放宽等不变量不得弱化。业务项目参数留在对应项目或 `examples/`。
- **路由隔离**：单人物咨询仅触发对应 `skills/<name>`（常规开发/文档/UX 请求不触发人物 skill）；多席位审议才由圆桌或短读协调器按名调用具名席位。

## 验证与完成标准

修改任务须完成 **实现 → 运行对应检查 → 核对输出 → 修复失败 → 重新验证通过** 闭环后方可结束：

```bash
python3 -B tools/render_roundtable_contract_docs.py --check  # 改机器合同先去掉 --check 重渲染
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
