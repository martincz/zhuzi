#!/usr/bin/env bash
# 把 runtimes/claude/ / zhuzi/ / skills/ 下的内容安装到本机 agent runtime 配置目录。
# 源码中的 agent / command 保持 runtime-agnostic 占位符，安装时再渲染成目标 runtime 的真实路径。
# 覆盖安装，不保留备份。每次修改本仓库后需重跑本脚本。
# 覆盖目标：
#   runtimes/claude/agents/*.md     → ~/.claude/agents/<name>.md （逐文件拷贝，不影响旁边的 gsd-*.md）
#   runtimes/claude/commands/zhuzi/ → ~/.claude/commands/zhuzi   （命令入口）
#   zhuzi/                → ~/.claude/zhuzi / ~/.codex/zhuzi    （项目级共享资产，当前含 references/workflows/templates/manifests）
#   skills/<name>/        → ~/.claude/skills/<name>             （Claude-style skills）
#   skills/<name>/        → $CODEX_HOME/skills/<name>           （Codex skills，默认 ~/.codex）
# 环境变量 CLAUDE_DIR 可覆盖 ~/.claude，CODEX_HOME 可覆盖 ~/.codex（测试用）。

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_RUNTIME_SOURCE="$REPO/runtimes/claude"
CLAUDE="${CLAUDE_DIR:-$HOME/.claude}"
CODEX="${CODEX_HOME:-$HOME/.codex}"
CLAUDE_SKILL_ROOT="$CLAUDE/skills"
CLAUDE_SHARED_ROOT="$CLAUDE/zhuzi"

render_template() {
  local src="$1"
  local dst="$2"
  local skill_root="$3"
  local shared_root="$4"

  sed \
    -e "s|{{ZHUZI_SKILL_ROOT}}|$skill_root|g" \
    -e "s|{{ZHUZI_SHARED_ROOT}}|$shared_root|g" \
    "$src" > "$dst"
}

mkdir -p "$CLAUDE/agents" "$CLAUDE/commands" "$CLAUDE/skills" "$CLAUDE/zhuzi"
mkdir -p "$CODEX/skills" "$CODEX/zhuzi"

echo "仓库：$REPO"
echo "Claude 目标：$CLAUDE"
echo "Codex 目标：$CODEX"
echo

echo "[1/4] agents"
for f in "$CLAUDE_RUNTIME_SOURCE"/agents/*.md; do
  [[ -e "$f" ]] || continue
  dst="$CLAUDE/agents/$(basename "$f")"
  rm -rf "$dst"
  render_template "$f" "$dst" "$CLAUDE_SKILL_ROOT" "$CLAUDE_SHARED_ROOT"
  echo "  + $dst"
done

echo
echo "[2/4] commands/zhuzi"
dst="$CLAUDE/commands/zhuzi"
rm -rf "$dst"
mkdir -p "$dst"
for f in "$CLAUDE_RUNTIME_SOURCE"/commands/zhuzi/*.md; do
  [[ -e "$f" ]] || continue
  render_template "$f" "$dst/$(basename "$f")" "$CLAUDE_SKILL_ROOT" "$CLAUDE_SHARED_ROOT"
done
echo "  + $dst"

echo
echo "[3/4] zhuzi runtime assets"
claude_runtime_dst="$CLAUDE/zhuzi"
rm -rf "$claude_runtime_dst"
cp -r "$REPO/zhuzi" "$claude_runtime_dst"
echo "  + $claude_runtime_dst"

codex_runtime_dst="$CODEX/zhuzi"
rm -rf "$codex_runtime_dst"
cp -r "$REPO/zhuzi" "$codex_runtime_dst"
echo "  + $codex_runtime_dst"

echo
echo "[4/4] skills"
for d in "$REPO"/skills/*/; do
  [[ -d "$d" ]] || continue
  name=$(basename "$d")
  dst="$CLAUDE/skills/$name"
  rm -rf "$dst"
  cp -r "$d" "$dst"
  echo "  + $dst"

  codex_dst="$CODEX/skills/$name"
  rm -rf "$codex_dst"
  cp -r "$d" "$codex_dst"
  echo "  + $codex_dst"
done

echo
echo "完成。修改仓库文件后需重跑本脚本。"
