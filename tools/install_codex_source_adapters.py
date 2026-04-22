#!/usr/bin/env python3
"""Render and install the source-only Codex roundtable adapters."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ONLY_AGENT_REL = "runtimes/codex/agents"
SOURCE_ONLY_SKILL_REL = "runtimes/codex/skills/zhuzi-roundtable"
SOURCE_ONLY_AGENT_DIR = ROOT / SOURCE_ONLY_AGENT_REL
SOURCE_ONLY_SKILL_DIR = ROOT / SOURCE_ONLY_SKILL_REL


def render_text(text: str, *, skill_root: Path, shared_root: Path) -> str:
    return (
        text.replace("{{ZHUZI_SKILL_ROOT}}", str(skill_root))
        .replace("{{ZHUZI_SHARED_ROOT}}", str(shared_root))
    )


def render_file(src: Path, dst: Path, *, skill_root: Path, shared_root: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding="utf-8")
    dst.write_text(
        render_text(text, skill_root=skill_root, shared_root=shared_root),
        encoding="utf-8",
    )


def copy_tree_with_render(src: Path, dst: Path, *, skill_root: Path, shared_root: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)

    for path in src.rglob("*"):
        target = dst / path.relative_to(src)
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if path.suffix == ".md":
            render_file(path, target, skill_root=skill_root, shared_root=shared_root)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def install_source_only_adapters(codex_home: Path) -> None:
    installed_agent_dir = codex_home / "agents"
    installed_skill_dir = codex_home / "skills" / "zhuzi-roundtable"
    installed_skill_root = codex_home / "skills"
    installed_shared_root = codex_home / "zhuzi"

    installed_agent_dir.mkdir(parents=True, exist_ok=True)

    for agent in SOURCE_ONLY_AGENT_DIR.glob("*.md"):
        render_file(
            agent,
            installed_agent_dir / agent.name,
            skill_root=installed_skill_root,
            shared_root=installed_shared_root,
        )

    copy_tree_with_render(
        SOURCE_ONLY_SKILL_DIR,
        installed_skill_dir,
        skill_root=installed_skill_root,
        shared_root=installed_shared_root,
    )


def main() -> int:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    install_source_only_adapters(codex_home)
    print(f"Codex source-only adapters installed to {codex_home}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
