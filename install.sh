#!/usr/bin/env bash
# 把 runtimes/claude/ / zhuzi/ / skills/ 下的内容安装到本机 agent runtime 配置目录。
# 源码中的 agent / command 保持 runtime-agnostic 占位符。
# 默认安装时渲染成 $HOME-rooted symbolic path；若显式设置 CLAUDE_DIR / CODEX_HOME，则改渲染为对应 concrete override path。
# 安装源面由 zhuzi/manifests/shipped-surface.json 驱动，避免 install.sh 再手写一套 shipped surface。
# 覆盖安装，不保留备份。每次修改本仓库后需重跑本脚本。
# 覆盖目标：
#   runtimes/claude/agents/*.md     → ~/.claude/agents/<name>.md （逐文件拷贝，不影响旁边的 gsd-*.md）
#   runtimes/claude/commands/zhuzi/ → ~/.claude/commands/zhuzi   （命令入口）
#   zhuzi/                → ~/.claude/zhuzi / ~/.codex/zhuzi    （项目级共享资产，当前含 seats/references/workflows/templates/manifests）
#   skills/<name>/        → ~/.claude/skills/<name>             （Claude-style skills）
#   skills/<name>/        → $CODEX_HOME/skills/<name>           （Codex skills，默认 ~/.codex）
# 环境变量 CLAUDE_DIR 可覆盖 ~/.claude，CODEX_HOME 可覆盖 ~/.codex（测试用）。

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST_PATH="$REPO/zhuzi/manifests/shipped-surface.json"
CLAUDE="${CLAUDE_DIR:-$HOME/.claude}"
CODEX="${CODEX_HOME:-$HOME/.codex}"

render_root_literal() {
  local override_name="$1"
  local concrete_root="$2"
  local symbolic_root="$3"

  if [[ -n "${!override_name:-}" ]]; then
    printf '%s' "$concrete_root"
  else
    printf '%s' "$symbolic_root"
  fi
}

CLAUDE_RENDER_ROOT="$(render_root_literal CLAUDE_DIR "$CLAUDE" '$HOME/.claude')"
CLAUDE_SKILL_ROOT="$CLAUDE_RENDER_ROOT/skills"
CLAUDE_SHARED_ROOT="$CLAUDE_RENDER_ROOT/zhuzi"

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

manifest_paths() {
  local family="$1"

  python3 - "$MANIFEST_PATH" "$family" <<'PY'
import json
import sys
from pathlib import Path

manifest_path = Path(sys.argv[1])
family = sys.argv[2]
payload = json.loads(manifest_path.read_text(encoding="utf-8"))

for entry in payload.get("families", {}).get(family, []):
    path = entry.get("path")
    if isinstance(path, str):
        print(path)
PY
}

mkdir -p "$CLAUDE/agents" "$CLAUDE/commands" "$CLAUDE/skills" "$CLAUDE/zhuzi"
mkdir -p "$CODEX/skills" "$CODEX/zhuzi"

echo "仓库：$REPO"
echo "Claude 目标：$CLAUDE"
echo "Codex 目标：$CODEX"
echo

echo "[1/5] agents"
while IFS= read -r rel; do
  [[ -n "$rel" ]] || continue
  src="$REPO/$rel"
  dst="$CLAUDE/agents/$(basename "$src")"
  rm -rf "$dst"
  render_template "$src" "$dst" "$CLAUDE_SKILL_ROOT" "$CLAUDE_SHARED_ROOT"
  echo "  + $dst"
done < <(manifest_paths "agents")

echo
echo "[2/5] commands/zhuzi"
dst="$CLAUDE/commands/zhuzi"
rm -rf "$dst"
mkdir -p "$dst"
while IFS= read -r rel; do
  [[ -n "$rel" ]] || continue
  src="$REPO/$rel"
  render_template "$src" "$dst/$(basename "$src")" "$CLAUDE_SKILL_ROOT" "$CLAUDE_SHARED_ROOT"
done < <(manifest_paths "commands")
echo "  + $dst"

echo
echo "[3/5] zhuzi runtime assets"
claude_runtime_dst="$CLAUDE/zhuzi"
rm -rf "$claude_runtime_dst"
cp -r "$REPO/zhuzi" "$claude_runtime_dst"
echo "  + $claude_runtime_dst"

codex_runtime_dst="$CODEX/zhuzi"
rm -rf "$codex_runtime_dst"
cp -r "$REPO/zhuzi" "$codex_runtime_dst"
echo "  + $codex_runtime_dst"

echo
echo "[4/5] skills"
while IFS= read -r rel; do
  [[ -n "$rel" ]] || continue
  src_dir="$REPO/$(dirname "$rel")"
  name=$(basename "$src_dir")
  dst="$CLAUDE/skills/$name"
  rm -rf "$dst"
  cp -r "$src_dir" "$dst"
  echo "  + $dst"

  codex_dst="$CODEX/skills/$name"
  rm -rf "$codex_dst"
  cp -r "$src_dir" "$codex_dst"
  echo "  + $codex_dst"
done < <(manifest_paths "skills")

echo
echo "[5/5] codex roundtable adapter"
python3 "$REPO/tools/install_codex_source_adapters.py"

echo
echo "完成。修改仓库文件后需重跑本脚本。"
