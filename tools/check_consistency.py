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
    "docs/**/*.md",
    "examples/**/*.md",
    "agents/*.md",
    "commands/**/*.md",
    "zhuzi/**/*.md",
    "skills/*/SKILL.md",
]

AGENT_SKILLS = {
    "linus-engineer.md": "linus-torvalds-engineer",
    "munger-reviewer.md": "munger-checklist",
    "taleb-reviewer.md": "taleb-antifragile",
    "lopezdeprado-reviewer.md": "lopezdeprado-scientist",
}

AGENT_VERDICT_ROOTS = {
    "linus-engineer.md": "linus_feasibility:",
    "munger-reviewer.md": "munger_verdict:",
    "taleb-reviewer.md": "taleb_verdict:",
    "lopezdeprado-reviewer.md": "lopezdeprado_verdict:",
}

AGENT_VERDICT_REFERENCE_PATH = "~/.claude/zhuzi/references/verdict-schema-v2.md"
ROUNDTABLE_REFERENCE_PATHS = [
    "~/.claude/zhuzi/references/seat-registry.md",
    "~/.claude/zhuzi/references/verdict-schema-v2.md",
]

CODEX_SKILL_DESCRIPTION_BYTES_LIMIT = 1024

QUICK_OUTPUT_HEADINGS = [
    "## 主持人结论",
    "## 议题卡",
    "## 席位短评",
    "## 决策表",
    "## 下一步",
]

BANNED_SNIPPETS = [
    "本仓库不再",
    "不再只是",
    "Skill 集合",
    "它包含三类互相咬合的产物",
    "不是某个单一运行时",
    "席位原文完整呈现",
    "完整呈现给用户",
    "绝不转述 agent 原文",
    "席位 YAML verdict 完整呈现",
    "3-5 条可验证 truth",
    "可被 Claude Code 直接加载",
    "/home/martincz",
    "/mnt/g/zhuzi",
    "`/roundtable`",
    "`~/.claude/commands/roundtable.md`",
    "`.claude/commands/roundtable.md`",
    "commands/roundtable.md",
    "三个 agent",
]

INVENTORY_FAMILIES = [
    (
        "Skills",
        lambda: sorted((ROOT / "skills").glob("*/SKILL.md")),
        lambda path: path.parent.name,
    ),
    (
        "Agents",
        lambda: sorted((ROOT / "agents").glob("*.md")),
        lambda path: path.stem,
    ),
    (
        "Commands",
        lambda: sorted((ROOT / "commands" / "zhuzi").glob("*.md")),
        lambda path: path.stem,
    ),
    (
        "Runtime Assets",
        lambda: sorted((ROOT / "zhuzi" / "references").glob("*.md")),
        lambda path: path.stem,
    ),
    (
        "Examples",
        lambda: sorted((ROOT / "examples").glob("*.md")),
        lambda path: path.stem,
    ),
    (
        "Tools",
        lambda: sorted((ROOT / "tools").glob("*.py")),
        lambda path: path.name,
    ),
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


def check_required_order(
    errors: list[str], path: Path, text: str, required: list[str], label: str
) -> None:
    position = -1
    for snippet in required:
        next_position = text.find(snippet)
        if next_position == -1:
            add_error(errors, path, 1, f"{label} missing {snippet}")
            continue
        if next_position < position:
            add_error(errors, path, 1, f"{label} out of order at {snippet}")
        position = next_position


def check_roundtable_shared_references(errors: list[str]) -> None:
    command = ROOT / "commands" / "zhuzi" / "roundtable.md"
    text = command.read_text(encoding="utf-8")
    for required in ["## 共享契约文件", *ROUNDTABLE_REFERENCE_PATHS]:
        if required not in text:
            add_error(errors, command, 1, f"roundtable missing shared reference {required}")


def check_seat_registry(errors: list[str]) -> None:
    path = ROOT / "zhuzi" / "references" / "seat-registry.md"
    if not path.exists():
        add_error(errors, path, 1, "missing seat registry")
        return

    text = path.read_text(encoding="utf-8")
    for required in ["## 当前席位", "## 默认 `stages` 规则", "## 扩席位维护清单"]:
        if required not in text:
            add_error(errors, path, 1, f"seat registry missing {required}")

    marker = "## 当前席位"
    if marker in text and "## 召开纪律" in text:
        seat_section = text.split(marker, 1)[1].split("## 召开纪律", 1)[0]
        table_agents = set(re.findall(r"^\|\s*[^|]+\s*\|\s*`([^`]+)`", seat_section, re.MULTILINE))
        file_agents = {agent.stem for agent in (ROOT / "agents").glob("*.md")}
        if table_agents != file_agents:
            add_error(
                errors,
                path,
                1,
                f"seat registry mismatch: table={sorted(table_agents)} files={sorted(file_agents)}",
            )


def check_quick_roundtable_contract(errors: list[str]) -> None:
    command = ROOT / "commands" / "zhuzi" / "roundtable.md"
    command_text = command.read_text(encoding="utf-8")
    for required in [
        "## 默认交互契约",
        "### Quick 输出模板（默认必须使用）",
        "Quick Roundtable",
        "locked / deferred / discretion",
    ]:
        if required not in command_text:
            add_error(errors, command, 1, f"quick roundtable contract missing {required}")
    check_required_order(errors, command, command_text, QUICK_OUTPUT_HEADINGS, "quick template")

    example = ROOT / "examples" / "roundtable-quick.md"
    if not example.exists():
        add_error(errors, example, 1, "missing Quick Roundtable example")
        return
    example_text = example.read_text(encoding="utf-8")
    check_required_order(errors, example, example_text, QUICK_OUTPUT_HEADINGS, "quick example")

    readme = ROOT / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    if "./examples/roundtable-quick.md" not in readme_text:
        add_error(errors, readme, 1, "README missing Quick Roundtable example link")


def check_commit_guidelines(errors: list[str]) -> None:
    path = ROOT / "AGENTS.md"
    text = path.read_text(encoding="utf-8")
    for required in [
        "## 提交规范",
        "`feat/fix/refactor/style/chore`",
        "多行格式",
        "单次提交只解决一个问题",
        "除前缀外，提交信息其他内容必须使用中文",
    ]:
        if required not in text:
            add_error(errors, path, 1, f"commit guideline missing {required}")


def check_agent_verdict_schema(errors: list[str]) -> None:
    required_sections = ["core:", "must_haves_review:", "must_haves_challenge:", "seat_specific:"]
    for agent_file, root_key in AGENT_VERDICT_ROOTS.items():
        path = ROOT / "agents" / agent_file
        text = path.read_text(encoding="utf-8")
        if AGENT_VERDICT_REFERENCE_PATH not in text:
            add_error(errors, path, 1, f"missing schema reference {AGENT_VERDICT_REFERENCE_PATH}")
        if root_key not in text:
            add_error(errors, path, 1, f"missing verdict root {root_key}")
        for section in required_sections:
            if section not in text:
                add_error(errors, path, 1, f"missing verdict schema section {section}")


def check_schema_reference(errors: list[str]) -> None:
    path = ROOT / "zhuzi" / "references" / "verdict-schema-v2.md"
    if not path.exists():
        add_error(errors, path, 1, "missing verdict schema reference")
        return

    text = path.read_text(encoding="utf-8")
    for required in [
        "## 层级结构",
        "## `core`",
        "## `must_haves_review`",
        "## `must_haves_challenge`",
        "## route 映射规则",
        "## 阶段 4 例外",
    ]:
        if required not in text:
            add_error(errors, path, 1, f"schema reference missing {required}")


def check_inventory(errors: list[str]) -> None:
    path = ROOT / "docs" / "INVENTORY.md"
    if not path.exists():
        add_error(errors, path, 1, "missing docs/INVENTORY.md")
        return

    text = path.read_text(encoding="utf-8")
    for label, finder, namer in INVENTORY_FAMILIES:
        match = re.search(rf"^## {re.escape(label)} \((\d+) shipped\)", text, re.MULTILINE)
        if not match:
            add_error(errors, path, 1, f"inventory missing section header for {label}")
            continue

        items = finder()
        documented = int(match.group(1))
        if documented != len(items):
            add_error(
                errors,
                path,
                1,
                f"inventory count mismatch for {label}: documented={documented} actual={len(items)}",
            )

        for item in items:
            name = namer(item)
            if f"`{name}`" not in text:
                add_error(errors, path, 1, f"inventory missing entry `{name}`")


def check_skill_reference_links(errors: list[str]) -> None:
    link_pattern = re.compile(r"references/[A-Za-z0-9_./-]+\.md")
    for skill in (ROOT / "skills").glob("*/SKILL.md"):
        text = skill.read_text(encoding="utf-8")
        for match in link_pattern.finditer(text):
            target = skill.parent / match.group(0)
            if not target.exists():
                line = text.count("\n", 0, match.start()) + 1
                add_error(errors, skill, line, f"missing referenced file {match.group(0)}")


def check_skill_description_lengths(errors: list[str]) -> None:
    for skill in (ROOT / "skills").glob("*/SKILL.md"):
        text = skill.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\n(.*?)\n---", text, re.DOTALL)
        if not frontmatter:
            add_error(errors, skill, 1, "missing YAML frontmatter")
            continue

        lines = frontmatter.group(1).splitlines()
        for index, line in enumerate(lines):
            if line != "description: |":
                continue

            description_lines: list[str] = []
            for description_line in lines[index + 1 :]:
                if description_line.startswith("  "):
                    description_lines.append(description_line[2:])
                    continue
                if description_line == "":
                    description_lines.append("")
                    continue
                break

            description = "\n".join(description_lines).rstrip()
            description_bytes = len(description.encode("utf-8"))
            if description_bytes > CODEX_SKILL_DESCRIPTION_BYTES_LIMIT:
                add_error(
                    errors,
                    skill,
                    index + 1,
                    "Codex skill description "
                    f"{description_bytes} bytes exceeds "
                    f"{CODEX_SKILL_DESCRIPTION_BYTES_LIMIT} byte limit",
                )
            break
        else:
            add_error(errors, skill, 1, "missing description block")


def check_codex_install(errors: list[str]) -> None:
    path = ROOT / "install.sh"
    text = path.read_text(encoding="utf-8")
    for required in ["CODEX_HOME", "$CODEX/skills", "$CLAUDE/skills", "$CLAUDE/zhuzi", "$CODEX/zhuzi"]:
        if required not in text:
            add_error(errors, path, 1, f"install.sh missing {required}")


def main() -> int:
    errors: list[str] = []
    check_banned_snippets(errors)
    check_agent_skill_paths(errors)
    check_roundtable_shared_references(errors)
    check_seat_registry(errors)
    check_quick_roundtable_contract(errors)
    check_commit_guidelines(errors)
    check_agent_verdict_schema(errors)
    check_schema_reference(errors)
    check_inventory(errors)
    check_skill_reference_links(errors)
    check_skill_description_lengths(errors)
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
