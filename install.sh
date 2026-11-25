#!/usr/bin/env bash
# 统一委托 Python 事务安装器完成 Claude Code 与 OpenAI Codex 资产安装、旧散落条目备份迁移、--pin 快捷固定与失败回滚。
# 安装源面与运行期排除项由 zhuzi/manifests/shipped-surface.json 唯一驱动：
#   默认仅向 ~/.claude/skills/zhuzi 与 ~/.agents/skills/zhuzi 安装唯一顶层入口（内含运行期 personas/，剔除 references/research/ 等研发底稿）；
#   具名席位安装至 ~/.claude/agents/*.md 与 ~/.codex/agents/*.toml，共享契约与校验器安装至 ~/.claude/zhuzi 与 ~/.codex/zhuzi。
# 环境变量隔离：CLAUDE_DIR 覆盖 Claude 根；CODEX_HOME 覆盖 Codex 根；CODEX_SKILL_DIR 覆盖 Codex 技能根。

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 -B "$REPO/tools/install_codex_source_adapters.py" "$@"
