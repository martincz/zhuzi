#!/usr/bin/env bash
# 把 agents/ 和 commands/ 下的文件安装到 Claude Code 的 ~/.claude/。
# 覆盖安装，不保留备份。每次修改本仓库后需重跑本脚本。
# 覆盖目标：
#   agents/*.md           → ~/.claude/agents/<name>.md          （逐文件拷贝，不影响旁边的 gsd-*.md）
#   commands/zhuzi/       → ~/.claude/commands/zhuzi            （整目录同步）
# 环境变量 CLAUDE_DIR 可覆盖 ~/.claude（测试用）。

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE="${CLAUDE_DIR:-$HOME/.claude}"

mkdir -p "$CLAUDE/agents" "$CLAUDE/commands"

echo "仓库：$REPO"
echo "目标：$CLAUDE"
echo

echo "[1/2] agents"
for f in "$REPO"/agents/*.md; do
  [[ -e "$f" ]] || continue
  dst="$CLAUDE/agents/$(basename "$f")"
  rm -rf "$dst"
  cp "$f" "$dst"
  echo "  + $dst"
done

echo
echo "[2/2] commands/zhuzi"
dst="$CLAUDE/commands/zhuzi"
rm -rf "$dst"
cp -r "$REPO/commands/zhuzi" "$dst"
echo "  + $dst"

echo
echo "完成。修改仓库文件后需重跑本脚本。"
