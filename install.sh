#!/usr/bin/env bash
# 把 agents/ / commands/ / skills/ 下的内容安装到 Claude Code 的 ~/.claude/。
# 覆盖安装，不保留备份。每次修改本仓库后需重跑本脚本。
# 覆盖目标：
#   agents/*.md           → ~/.claude/agents/<name>.md          （逐文件拷贝，不影响旁边的 gsd-*.md）
#   commands/zhuzi/       → ~/.claude/commands/zhuzi            （整目录同步）
#   skills/<name>/        → ~/.claude/skills/<name>             （逐 skill 目录同步，只动本仓库管理的 skill）
# 环境变量 CLAUDE_DIR 可覆盖 ~/.claude（测试用）。

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE="${CLAUDE_DIR:-$HOME/.claude}"

mkdir -p "$CLAUDE/agents" "$CLAUDE/commands" "$CLAUDE/skills"

echo "仓库：$REPO"
echo "目标：$CLAUDE"
echo

echo "[1/3] agents"
for f in "$REPO"/agents/*.md; do
  [[ -e "$f" ]] || continue
  dst="$CLAUDE/agents/$(basename "$f")"
  rm -rf "$dst"
  cp "$f" "$dst"
  echo "  + $dst"
done

echo
echo "[2/3] commands/zhuzi"
dst="$CLAUDE/commands/zhuzi"
rm -rf "$dst"
cp -r "$REPO/commands/zhuzi" "$dst"
echo "  + $dst"

echo
echo "[3/3] skills"
for d in "$REPO"/skills/*/; do
  [[ -d "$d" ]] || continue
  name=$(basename "$d")
  dst="$CLAUDE/skills/$name"
  rm -rf "$dst"
  cp -r "$d" "$dst"
  echo "  + $dst"
done

echo
echo "完成。修改仓库文件后需重跑本脚本。"
