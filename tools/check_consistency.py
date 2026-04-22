#!/usr/bin/env python3
"""Lightweight consistency checks for the zhuzi Markdown runtime files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "zhuzi" / "manifests" / "shipped-surface.json"

ACTIVE_TEXT_GLOBS = [
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "install.sh",
    "docs/**/*.md",
    "examples/**/*.md",
    "runtimes/**/*.md",
    "zhuzi/**/*.md",
    "skills/*/SKILL.md",
]

CLAUDE_RUNTIME_ROOT = ROOT / "runtimes" / "claude"

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

AGENT_VERDICT_REFERENCE_PATH = "{{ZHUZI_SHARED_ROOT}}/references/verdict-schema.md"
ROUNDTABLE_REFERENCE_PATHS = [
    "{{ZHUZI_SHARED_ROOT}}/references/seat-registry.md",
    "{{ZHUZI_SHARED_ROOT}}/references/verdict-schema.md",
]
ROUNDTABLE_WORKFLOW_PATH = "{{ZHUZI_SHARED_ROOT}}/workflows/roundtable.md"
ROUNDTABLE_TEMPLATE_PATH = "{{ZHUZI_SHARED_ROOT}}/templates/roundtable-quick.md"
AGENT_SKILL_PATH_TEMPLATE = "{{{{ZHUZI_SKILL_ROOT}}}}/{skill_name}/SKILL.md"
ROUNDTABLE_EXECUTION_CONTEXTS = [
    f"@{ROUNDTABLE_WORKFLOW_PATH}",
    f"@{ROUNDTABLE_REFERENCE_PATHS[0]}",
    f"@{ROUNDTABLE_REFERENCE_PATHS[1]}",
    f"@{ROUNDTABLE_TEMPLATE_PATH}",
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

SURFACE_FAMILIES = [
    (
        "Skills",
        "skills",
        lambda: sorted((ROOT / "skills").glob("*/SKILL.md")),
        lambda path: path.parent.name,
    ),
    (
        "Agents",
        "agents",
        lambda: sorted((CLAUDE_RUNTIME_ROOT / "agents").glob("*.md")),
        lambda path: path.stem,
    ),
    (
        "Commands",
        "commands",
        lambda: sorted((CLAUDE_RUNTIME_ROOT / "commands" / "zhuzi").glob("*.md")),
        lambda path: path.stem,
    ),
    (
        "Workflows",
        "workflows",
        lambda: sorted((ROOT / "zhuzi" / "workflows").glob("*.md")),
        lambda path: path.stem,
    ),
    (
        "References",
        "references",
        lambda: sorted((ROOT / "zhuzi" / "references").glob("*.md")),
        lambda path: path.stem,
    ),
    (
        "Templates",
        "templates",
        lambda: sorted((ROOT / "zhuzi" / "templates").glob("*.md")),
        lambda path: path.stem,
    ),
    (
        "Manifests",
        "manifests",
        lambda: sorted((ROOT / "zhuzi" / "manifests").glob("*.json")),
        lambda path: path.stem,
    ),
    (
        "Examples",
        "examples",
        lambda: sorted((ROOT / "examples").glob("*.md")),
        lambda path: path.stem,
    ),
    (
        "Tools",
        "tools",
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


def load_manifest(errors: list[str]) -> dict[str, list[dict[str, str]]] | None:
    if not MANIFEST_PATH.exists():
        add_error(errors, MANIFEST_PATH, 1, "missing shipped surface manifest")
        return None

    try:
        payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_error(errors, MANIFEST_PATH, exc.lineno or 1, f"invalid JSON: {exc.msg}")
        return None

    families = payload.get("families")
    if not isinstance(families, dict):
        add_error(errors, MANIFEST_PATH, 1, "manifest missing top-level families object")
        return None

    return families


def check_banned_snippets(errors: list[str]) -> None:
    for path in iter_files(ACTIVE_TEXT_GLOBS):
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            for snippet in BANNED_SNIPPETS:
                if snippet in line:
                    add_error(errors, path, lineno, f"banned snippet: {snippet}")


def check_agent_skill_paths(errors: list[str]) -> None:
    for agent_file, skill_name in AGENT_SKILLS.items():
        path = CLAUDE_RUNTIME_ROOT / "agents" / agent_file
        text = path.read_text(encoding="utf-8")
        expected = AGENT_SKILL_PATH_TEMPLATE.format(skill_name=skill_name)
        if expected not in text:
            add_error(errors, path, 1, f"missing installed skill path {expected}")


def check_runtime_path_templates(errors: list[str]) -> None:
    template_files = list(CLAUDE_RUNTIME_ROOT.glob("**/*.md"))
    template_files.extend((ROOT / "zhuzi" / "workflows").glob("*.md"))

    banned_runtime_literals = ["~/.claude/", "~/.codex/", "@~/.claude/", "@~/.codex/"]
    for path in template_files:
        text = path.read_text(encoding="utf-8")
        for literal in banned_runtime_literals:
            if literal in text:
                add_error(errors, path, 1, f"runtime template leaked hardcoded path {literal}")


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


def check_roundtable_command_entry(errors: list[str]) -> None:
    path = CLAUDE_RUNTIME_ROOT / "commands" / "zhuzi" / "roundtable.md"
    text = path.read_text(encoding="utf-8")
    for required in [
        "<objective>",
        "<execution_context>",
        "<context>",
        "<process>",
        *ROUNDTABLE_EXECUTION_CONTEXTS,
        "zhuzi/workflows/roundtable.md",
        "zhuzi/templates/roundtable-quick.md",
    ]:
        if required not in text:
            add_error(errors, path, 1, f"roundtable command missing {required}")


def check_roundtable_workflow(errors: list[str]) -> None:
    path = ROOT / "zhuzi" / "workflows" / "roundtable.md"
    if not path.exists():
        add_error(errors, path, 1, "missing roundtable workflow")
        return

    text = path.read_text(encoding="utf-8")
    for required in [
        "## 流水线性质",
        "## 默认交互契约",
        "### Quick 输出模板（默认必须使用）",
        "### 阶段 0.5 — 议题契约定义（orchestrator）",
        "### 阶段 1 — 视角并行审议",
        "### 阶段 1.5 — must_haves 修订 gate（条件触发）",
        "### 阶段 2 — 代码可行性评审",
        "### 阶段 3 — 综合对齐（orchestrator 主持）",
        "### 阶段 4 — 实施",
        "## 冲突裁决规则",
        "## 硬约束（任何情况不得违反）",
        "N 席位召开（N ≥ 1）",
    ]:
        if required not in text:
            add_error(errors, path, 1, f"roundtable workflow missing {required}")


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
        file_agents = {agent.stem for agent in (CLAUDE_RUNTIME_ROOT / "agents").glob("*.md")}
        if table_agents != file_agents:
            add_error(
                errors,
                path,
                1,
                f"seat registry mismatch: table={sorted(table_agents)} files={sorted(file_agents)}",
            )


def check_quick_roundtable_contract(errors: list[str]) -> None:
    template = ROOT / "zhuzi" / "templates" / "roundtable-quick.md"
    if not template.exists():
        add_error(errors, template, 1, "missing Quick Roundtable template")
    else:
        template_text = template.read_text(encoding="utf-8")
        check_required_order(errors, template, template_text, QUICK_OUTPUT_HEADINGS, "quick template")

    example = ROOT / "examples" / "roundtable-quick.md"
    if not example.exists():
        add_error(errors, example, 1, "missing Quick Roundtable example")
    else:
        example_text = example.read_text(encoding="utf-8")
        check_required_order(errors, example, example_text, QUICK_OUTPUT_HEADINGS, "quick example")

    readme = ROOT / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    for required in [
        "./examples/roundtable-quick.md",
        "./docs/INVENTORY.md",
        "./zhuzi/manifests/shipped-surface.json",
        "zhuzi/workflows/roundtable.md",
    ]:
        if required not in readme_text:
            add_error(errors, readme, 1, f"README missing {required}")


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
        path = CLAUDE_RUNTIME_ROOT / "agents" / agent_file
        text = path.read_text(encoding="utf-8")
        if AGENT_VERDICT_REFERENCE_PATH not in text:
            add_error(errors, path, 1, f"missing schema reference {AGENT_VERDICT_REFERENCE_PATH}")
        if root_key not in text:
            add_error(errors, path, 1, f"missing verdict root {root_key}")
        for section in required_sections:
            if section not in text:
                add_error(errors, path, 1, f"missing verdict schema section {section}")


def check_schema_reference(errors: list[str]) -> None:
    path = ROOT / "zhuzi" / "references" / "verdict-schema.md"
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


def check_manifest(errors: list[str], manifest_families: dict[str, list[dict[str, str]]] | None) -> None:
    if manifest_families is None:
        return

    for label, key, finder, namer in SURFACE_FAMILIES:
        entries = manifest_families.get(key)
        if not isinstance(entries, list):
            add_error(errors, MANIFEST_PATH, 1, f"manifest missing family {key}")
            continue

        actual_files = finder()
        actual_by_entry = {namer(path): rel(path) for path in actual_files}
        manifest_by_entry: dict[str, str] = {}
        for index, entry in enumerate(entries, 1):
            if not isinstance(entry, dict):
                add_error(errors, MANIFEST_PATH, 1, f"manifest family {key} entry {index} is not an object")
                continue
            for field in ["entry", "path", "role"]:
                if field not in entry:
                    add_error(errors, MANIFEST_PATH, 1, f"manifest family {key} entry {index} missing {field}")
            entry_name = entry.get("entry")
            entry_path = entry.get("path")
            if isinstance(entry_name, str) and isinstance(entry_path, str):
                manifest_by_entry[entry_name] = entry_path
                target = ROOT / entry_path
                if not target.exists():
                    add_error(errors, MANIFEST_PATH, 1, f"manifest entry {entry_name} points to missing {entry_path}")

        if set(manifest_by_entry) != set(actual_by_entry):
            add_error(
                errors,
                MANIFEST_PATH,
                1,
                f"manifest family {label} mismatch: manifest={sorted(manifest_by_entry)} actual={sorted(actual_by_entry)}",
            )
            continue

        for entry_name, actual_path in actual_by_entry.items():
            if manifest_by_entry.get(entry_name) != actual_path:
                add_error(
                    errors,
                    MANIFEST_PATH,
                    1,
                    f"manifest path mismatch for {entry_name}: manifest={manifest_by_entry.get(entry_name)} actual={actual_path}",
                )


def check_inventory(errors: list[str], manifest_families: dict[str, list[dict[str, str]]] | None) -> None:
    path = ROOT / "docs" / "INVENTORY.md"
    if not path.exists():
        add_error(errors, path, 1, "missing docs/INVENTORY.md")
        return

    text = path.read_text(encoding="utf-8")
    for label, key, _, _ in SURFACE_FAMILIES:
        match = re.search(rf"^## {re.escape(label)} \((\d+) shipped\)", text, re.MULTILINE)
        if not match:
            add_error(errors, path, 1, f"inventory missing section header for {label}")
            continue

        expected_count = len(manifest_families.get(key, [])) if manifest_families else 0
        documented = int(match.group(1))
        if documented != expected_count:
            add_error(
                errors,
                path,
                1,
                f"inventory count mismatch for {label}: documented={documented} actual={expected_count}",
            )

        for entry in manifest_families.get(key, []) if manifest_families else []:
            entry_name = entry.get("entry")
            entry_path = entry.get("path")
            if isinstance(entry_name, str) and f"`{entry_name}`" not in text:
                add_error(errors, path, 1, f"inventory missing entry `{entry_name}`")
            if isinstance(entry_path, str) and f"`{entry_path}`" not in text:
                add_error(errors, path, 1, f"inventory missing path `{entry_path}`")


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
    for required in [
        "CODEX_HOME",
        "$CODEX/skills",
        "$CLAUDE/skills",
        "$CLAUDE/zhuzi",
        "$CODEX/zhuzi",
        "MANIFEST_PATH",
        "manifest_paths",
        "shipped-surface.json",
        "runtimes/claude/agents",
        "runtimes/claude/commands/zhuzi",
        "references/workflows/templates/manifests",
    ]:
        if required not in text:
            add_error(errors, path, 1, f"install.sh missing {required}")


def main() -> int:
    errors: list[str] = []
    manifest_families = load_manifest(errors)

    check_banned_snippets(errors)
    check_agent_skill_paths(errors)
    check_runtime_path_templates(errors)
    check_roundtable_command_entry(errors)
    check_roundtable_workflow(errors)
    check_seat_registry(errors)
    check_quick_roundtable_contract(errors)
    check_commit_guidelines(errors)
    check_agent_verdict_schema(errors)
    check_schema_reference(errors)
    check_manifest(errors, manifest_families)
    check_inventory(errors, manifest_families)
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
