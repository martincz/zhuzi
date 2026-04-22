#!/usr/bin/env python3
"""Render and install the Codex roundtable adapters.

Called by ``install.sh`` as part of the default shipped-surface install so
Codex agents and the ``zhuzi-roundtable`` skill land alongside the Claude
assets. Can also be run standalone if only the Codex side needs refreshing.

Default installs render ``$HOME/.codex/...`` symbolic paths.
Explicit ``CODEX_HOME`` overrides render concrete paths so alternate roots stay valid.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "zhuzi" / "manifests" / "shipped-surface.json"
CODEX_AGENT_FAMILY = "codex_agents"
CODEX_SKILL_FAMILY = "codex_skills"


def render_text(text: str, *, skill_root: Path, shared_root: Path) -> str:
    return (
        text.replace("{{ZHUZI_SKILL_ROOT}}", str(skill_root))
        .replace("{{ZHUZI_SHARED_ROOT}}", str(shared_root))
    )


def render_root_literal(concrete_root: Path, *, symbolic_root: str, render_concrete: bool) -> str:
    return str(concrete_root) if render_concrete else symbolic_root


def collapse_repo_fallbacks(text: str) -> str:
    lines = text.splitlines()
    collapsed: list[str] = []

    for line in lines:
        if "`./skills" in line or "`./zhuzi" in line:
            continue
        collapsed.append(line)

    return (
        "\n".join(collapsed)
        .replace(
            "Read the first existing path in each group before doing anything else:",
            "Read these installed paths before doing anything else:",
        )
        .replace(
            "Read the first existing path in each group before proceeding:",
            "Read these installed paths before proceeding:",
        )
        .replace(
            "先确定共享根目录，只能选一个：",
            "使用以下已安装共享根目录：",
        )
        .replace(
            "- 已安装共享根目录：`",
            "- `",
        )
        .replace(
            "然后从选定根目录读取：",
            "然后从该已安装根目录读取：",
        )
        + "\n"
    )


def render_file(src: Path, dst: Path, *, skill_root: Path, shared_root: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding="utf-8")
    dst.write_text(
        collapse_repo_fallbacks(
            render_text(text, skill_root=skill_root, shared_root=shared_root)
        ),
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


def load_manifest_families() -> dict[str, list[dict[str, str]]]:
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    families = payload.get("families")
    if not isinstance(families, dict):
        raise ValueError(f"invalid manifest families object: {MANIFEST_PATH}")
    return families


def manifest_family_paths(
    families: dict[str, list[dict[str, str]]], family: str
) -> list[Path]:
    entries = families.get(family)
    if not isinstance(entries, list):
        raise ValueError(f"manifest missing family {family}: {MANIFEST_PATH}")

    resolved: list[Path] = []
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            raise ValueError(f"manifest family {family} entry {index} is not an object")

        raw_path = entry.get("path")
        if not isinstance(raw_path, str):
            raise ValueError(f"manifest family {family} entry {index} missing path")

        resolved_path = ROOT / raw_path
        if not resolved_path.exists():
            raise FileNotFoundError(
                f"manifest family {family} entry {index} points to missing path: {raw_path}"
            )
        resolved.append(resolved_path)

    return resolved


def install_source_only_adapters(codex_home: Path, *, render_concrete: bool | None = None) -> list[Path]:
    if render_concrete is None:
        render_concrete = os.environ.get("CODEX_HOME") is not None

    families = load_manifest_families()
    installed_agent_dir = codex_home / "agents"
    installed_skill_root = codex_home / "skills"
    installed_shared_root = codex_home / "zhuzi"
    rendered_skill_root = Path(
        render_root_literal(
            installed_skill_root,
            symbolic_root="$HOME/.codex/skills",
            render_concrete=render_concrete,
        )
    )
    rendered_shared_root = Path(
        render_root_literal(
            installed_shared_root,
            symbolic_root="$HOME/.codex/zhuzi",
            render_concrete=render_concrete,
        )
    )

    installed_agent_dir.mkdir(parents=True, exist_ok=True)

    installed_paths: list[Path] = []

    for agent in manifest_family_paths(families, CODEX_AGENT_FAMILY):
        if agent.suffix != ".md":
            raise ValueError(f"Codex agent manifest entry must be a markdown file: {agent}")
        dst = installed_agent_dir / agent.name
        render_file(
            agent,
            dst,
            skill_root=rendered_skill_root,
            shared_root=rendered_shared_root,
        )
        installed_paths.append(dst)

    installed_skill_dirs: dict[str, Path] = {}
    for skill_entry in manifest_family_paths(families, CODEX_SKILL_FAMILY):
        installed_skill_dirs[skill_entry.parent.name] = skill_entry.parent

    for skill_dir in installed_skill_dirs.values():
        installed_skill_dir = installed_skill_root / skill_dir.name
        copy_tree_with_render(
            skill_dir,
            installed_skill_dir,
            skill_root=rendered_skill_root,
            shared_root=rendered_shared_root,
        )
        installed_paths.append(installed_skill_dir)

    return installed_paths


def main() -> int:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    for path in install_source_only_adapters(codex_home):
        print(f"  + {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
