#!/usr/bin/env python3
"""Lightweight consistency checks for the zhuzi Markdown runtime files."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ACTIVE_TEXT_GLOBS = [
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "install.sh",
    "agents/*.md",
    "commands/**/*.md",
    "skills/*/SKILL.md",
]

AGENT_SKILLS = {
    "linus-engineer.md": "linus-torvalds-engineer",
    "munger-reviewer.md": "munger-checklist",
    "taleb-reviewer.md": "taleb-antifragile",
    "lopezdeprado-reviewer.md": "lopezdeprado-scientist",
}

BANNED_SNIPPETS = [
    "可被 Claude Code 直接加载",
    "/home/martincz",
    "/mnt/g/zhuzi",
    "`/roundtable`",
    "`~/.claude/commands/roundtable.md`",
    "`.claude/commands/roundtable.md`",
    "commands/roundtable.md",
    "三个 agent",
]


def iter_files(patterns: list[str]) -> list[Path]:
    files: list[Path] = []
    for pattern in patterns:
        files.extend(ROOT.glob(pattern))
    return sorted({path for path in files if path.is_file()})


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def add_error(errors: list[str], path: Path, lineno: int, message: str) -> None:
    errors.append(f"{rel(path)}:{lineno}: {message}")


def check_banned_snippets(errors: list[str]) -> None:
    for path in iter_files(ACTIVE_TEXT_GLOBS):
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            for snippet in BANNED_SNIPPETS:
                if snippet in line:
                    add_error(errors, path, lineno, f"banned snippet: {snippet}")


def check_agent_skill_paths(errors: list[str]) -> None:
    for agent_file, skill_name in AGENT_SKILLS.items():
        path = ROOT / "agents" / agent_file
        text = path.read_text(encoding="utf-8")
        expected = f"~/.claude/skills/{skill_name}/SKILL.md"
        if expected not in text:
            add_error(errors, path, 1, f"missing installed skill path {expected}")


def check_roundtable_seats(errors: list[str]) -> None:
    command = ROOT / "commands" / "zhuzi" / "roundtable.md"
    text = command.read_text(encoding="utf-8")
    table_agents = set(re.findall(r"\|\s*(?:策略|代码)\s*\|\s*`([^`]+)`", text))
    file_agents = {path.stem for path in (ROOT / "agents").glob("*.md")}
    if table_agents != file_agents:
        add_error(
            errors,
            command,
            1,
            f"roundtable seat table mismatch: table={sorted(table_agents)} files={sorted(file_agents)}",
        )


def check_skill_reference_links(errors: list[str]) -> None:
    link_pattern = re.compile(r"references/[A-Za-z0-9_./-]+\.md")
    for skill in (ROOT / "skills").glob("*/SKILL.md"):
        text = skill.read_text(encoding="utf-8")
        for match in link_pattern.finditer(text):
            target = skill.parent / match.group(0)
            if not target.exists():
                line = text.count("\n", 0, match.start()) + 1
                add_error(errors, skill, line, f"missing referenced file {match.group(0)}")


def check_codex_install(errors: list[str]) -> None:
    path = ROOT / "install.sh"
    text = path.read_text(encoding="utf-8")
    for required in ["CODEX_HOME", "$CODEX/skills", "$CLAUDE/skills"]:
        if required not in text:
            add_error(errors, path, 1, f"install.sh missing {required}")


def main() -> int:
    errors: list[str] = []
    check_banned_snippets(errors)
    check_agent_skill_paths(errors)
    check_roundtable_seats(errors)
    check_skill_reference_links(errors)
    check_codex_install(errors)

    if errors:
        print("Consistency check failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Consistency check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
