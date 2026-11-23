#!/usr/bin/env python3
"""Check shared contracts, distribution paths, and instruction metadata."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from render_roundtable_contract_docs import STATIC_GENERATED_DOCS, build_schema, get_generated_docs, render_doc_text


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "zhuzi" / "manifests" / "shipped-surface.json"
ROUNDTABLE_CONTRACT_PATH = ROOT / "zhuzi" / "manifests" / "roundtable-contract.json"

ACTIVE_TEXT_GLOBS = [
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "install.sh",
    "docs/**/*.md",
    "examples/**/*.md",
    "runtimes/**/*.md",
    "runtimes/**/*.toml",
    "zhuzi/**/*.md",
    "skills/*/SKILL.md",
]

CLAUDE_RUNTIME_ROOT = ROOT / "runtimes" / "claude"
CODEX_RUNTIME_ROOT = ROOT / "runtimes" / "codex"
AGENT_VERDICT_REFERENCE_PATH = "{{ZHUZI_SHARED_ROOT}}/references/verdict-schema.md"
AGENT_SEAT_REFERENCE_PATH_TEMPLATE = "{{{{ZHUZI_SHARED_ROOT}}}}/seats/{seat_file}"
AGENT_SKILL_PATH_TEMPLATE = "{{{{ZHUZI_SKILL_ROOT}}}}/{skill_name}/SKILL.md"
WORKFLOW_ENTRIES = {"roundtable": "roundtable", "quick": "quick-multi"}
SKILL_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MARKDOWN_LINK = re.compile(r"\]\(\s*(?:<([^>\n]+)>|([^\s)]+))")

ADAPTER_INLINE_SCHEMA_SNIPPETS = [
    "must_haves_review:",
    "must_haves_challenge:",
    "seat_specific:",
    "Filled-in 示例",
]

BANNED_SNIPPETS = [
    "/home/martincz",
    "/mnt/g/zhuzi",
    "`/roundtable`",
    "`~/.claude/commands/roundtable.md`",
    "`.claude/commands/roundtable.md`",
    "commands/roundtable.md",
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
        "Codex Agents",
        "codex_agents",
        lambda: sorted((CODEX_RUNTIME_ROOT / "agents").glob("*.toml")),
        lambda path: path.stem,
    ),
    (
        "Codex Skills",
        "codex_skills",
        lambda: sorted((CODEX_RUNTIME_ROOT / "skills").glob("*/SKILL.md")),
        lambda path: path.parent.name,
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
        "Seats",
        "seats",
        lambda: sorted((ROOT / "zhuzi" / "seats").glob("*.md")),
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
        "Schemas", "schemas",
        lambda: sorted((ROOT / "zhuzi" / "schemas").glob("*.json")),
        lambda path: path.stem,
    ),
    (
        "Validators", "validators",
        lambda: sorted((ROOT / "zhuzi" / "validators").glob("*.py")),
        lambda path: path.stem,
    ),
    (
        "Evals", "evals",
        lambda: sorted((ROOT / "evals").glob("*.json")),
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


def load_roundtable_contract(errors: list[str]) -> dict[str, object] | None:
    if not ROUNDTABLE_CONTRACT_PATH.exists():
        add_error(errors, ROUNDTABLE_CONTRACT_PATH, 1, "missing roundtable contract manifest")
        return None

    try:
        payload = json.loads(ROUNDTABLE_CONTRACT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_error(  # pragma: no cover - exercised through runtime validation
            errors,
            ROUNDTABLE_CONTRACT_PATH,
            exc.lineno or 1,
            f"invalid JSON: {exc.msg}",
        )
        return None

    if not isinstance(payload, dict):
        add_error(errors, ROUNDTABLE_CONTRACT_PATH, 1, "roundtable contract must be a JSON object")
        return None

    for key in ["references", "quick_output", "dispatch_rules", "verdict_schema", "seats"]:
        if key not in payload:
            add_error(errors, ROUNDTABLE_CONTRACT_PATH, 1, f"roundtable contract missing {key}")

    seats = payload.get("seats")
    if not isinstance(seats, dict) or not seats:
        add_error(errors, ROUNDTABLE_CONTRACT_PATH, 1, "roundtable contract seats must be a non-empty object")
        return None

    for seat_name, config in seats.items():
        if not isinstance(config, dict):
            add_error(errors, ROUNDTABLE_CONTRACT_PATH, 1, f"seat contract {seat_name} must be an object")
            continue
        for field in ["skill", "agent", "persona", "generated_block", "registry_summary", "registry_stage_row", "output_contract", "required_contract_snippets"]:
            if field not in config:
                add_error(errors, ROUNDTABLE_CONTRACT_PATH, 1, f"seat contract {seat_name} missing {field}")

    return payload


def iter_roundtable_seats(roundtable_contract: dict[str, object] | None) -> list[tuple[str, dict[str, object]]]:
    if not roundtable_contract:
        return []
    seats = roundtable_contract.get("seats")
    if not isinstance(seats, dict):
        return []

    result: list[tuple[str, dict[str, object]]] = []
    for seat_name, config in seats.items():
        if isinstance(seat_name, str) and isinstance(config, dict):
            result.append((seat_name, config))
    return result


def resolve_generated_docs(
    errors: list[str],
    roundtable_contract: dict[str, object] | None,
) -> dict[str, list[str]]:
    if roundtable_contract is None:
        return {
            relative_path: list(block_names)
            for relative_path, block_names in STATIC_GENERATED_DOCS.items()
        }

    try:
        return get_generated_docs(roundtable_contract)
    except ValueError as exc:
        add_error(errors, ROUNDTABLE_CONTRACT_PATH, 1, str(exc))
        return {
            relative_path: list(block_names)
            for relative_path, block_names in STATIC_GENERATED_DOCS.items()
        }


def check_banned_snippets(errors: list[str]) -> None:
    for path in iter_files(ACTIVE_TEXT_GLOBS):
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            for snippet in BANNED_SNIPPETS:
                if snippet in line:
                    add_error(errors, path, lineno, f"banned snippet: {snippet}")


def read_frontmatter(errors: list[str], path: Path, text: str) -> dict | None:
    header = re.match(r"\A---\n(.*?)\n---[ \t]*(?:\n|$)", text, re.DOTALL)
    if not header:
        add_error(errors, path, 1, "missing YAML frontmatter")
        return None
    try:
        fields = yaml.safe_load(header.group(1))
    except yaml.YAMLError as exc:
        add_error(errors, path, 1, f"invalid YAML frontmatter: {exc}")
        return None
    if not isinstance(fields, dict):
        add_error(errors, path, 1, "YAML frontmatter must be a mapping")
        return None
    if not text[header.end():].strip():
        add_error(errors, path, 1, "missing instructions after frontmatter")
    return fields


def check_claude_agent_adapters(errors: list[str], roundtable_contract: dict[str, object] | None) -> None:
    actual_files = {path.name for path in (CLAUDE_RUNTIME_ROOT / "agents").glob("*.md")}
    expected_files = {f"{seat_name}.md" for seat_name, _ in iter_roundtable_seats(roundtable_contract)}
    if actual_files != expected_files:
        add_error(
            errors,
            CLAUDE_RUNTIME_ROOT / "agents",
            1,
            f"Claude agent set mismatch: expected={sorted(expected_files)} actual={sorted(actual_files)}",
        )

    for seat_name, config in iter_roundtable_seats(roundtable_contract):
        path = CLAUDE_RUNTIME_ROOT / "agents" / f"{seat_name}.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        fields = read_frontmatter(errors, path, text)
        if fields is not None:
            description = fields.get("description")
            if fields.get("name") != seat_name or not isinstance(description, str) or not description.strip():
                add_error(errors, path, 1, "invalid Claude agent identity or description")
            raw_tools = fields.get("tools")
            tools = {name.strip() for name in raw_tools.split(",")} if isinstance(raw_tools, str) else set()
            if "Read" not in tools:
                add_error(errors, path, 1, "Claude seat requires an explicit tool list with Read")
            elif seat_name != "linus-engineer" and tools & {"Write", "Edit"}:
                add_error(errors, path, 1, "analysis seats cannot declare edit tools")
        skill_name = config.get("skill")
        if not isinstance(skill_name, str):
            add_error(errors, ROUNDTABLE_CONTRACT_PATH, 1, f"seat contract {seat_name} missing string skill")
            continue

        expected_skill = AGENT_SKILL_PATH_TEMPLATE.format(skill_name=skill_name)
        expected_seat = AGENT_SEAT_REFERENCE_PATH_TEMPLATE.format(seat_file=f"{seat_name}.md")
        for required in [expected_skill, expected_seat, AGENT_VERDICT_REFERENCE_PATH]:
            if required not in text:
                add_error(errors, path, 1, f"missing Claude agent reference {required}")
        for banned in ADAPTER_INLINE_SCHEMA_SNIPPETS:
            if banned in text:
                add_error(errors, path, 1, f"Claude agent should not inline shared schema snippet {banned}")


def check_runtime_path_templates(errors: list[str]) -> None:
    template_files = list((ROOT / "runtimes").glob("**/*.md"))
    template_files.extend((ROOT / "runtimes").glob("**/*.toml"))
    template_files.extend((ROOT / "zhuzi" / "workflows").glob("*.md"))
    template_files.extend((ROOT / "zhuzi" / "seats").glob("*.md"))

    banned_runtime_literals = [
        "~/.claude/",
        "~/.codex/",
        "@~/.claude/",
        "@~/.codex/",
        "$HOME/.claude/",
        "$HOME/.codex/",
    ]
    for path in template_files:
        text = path.read_text(encoding="utf-8")
        for literal in banned_runtime_literals:
            if literal in text:
                add_error(errors, path, 1, f"runtime template leaked hardcoded path {literal}")


def check_workflow_adapters(errors: list[str]) -> None:
    for entry, workflow in WORKFLOW_ENTRIES.items():
        shared_file = f"workflows/{workflow}.md"
        path = ROOT / "zhuzi" / shared_file
        if not path.is_file():
            add_error(errors, path, 1, "missing shared workflow")
            continue
        text = path.read_text(encoding="utf-8")
        for primitive in ("Agent(", "SendMessage(", "spawn_agent(", "wait_agent(", "followup_task(", "send_input("):
            if primitive in text:
                add_error(errors, path, 1, f"shared workflow leaked runtime-specific primitive {primitive}")

        for adapter in (CLAUDE_RUNTIME_ROOT / f"commands/zhuzi/{entry}.md",
                        CODEX_RUNTIME_ROOT / f"skills/zhuzi-{entry}/SKILL.md"):
            if not adapter.is_file():
                add_error(errors, adapter, 1, "missing workflow adapter")
                continue
            body = adapter.read_text(encoding="utf-8")
            if f"{{{{ZHUZI_SHARED_ROOT}}}}/{shared_file}" not in body:
                add_error(errors, adapter, 1, f"missing shared workflow reference {shared_file}")
            if adapter.is_relative_to(CLAUDE_RUNTIME_ROOT):
                fields = read_frontmatter(errors, adapter, body)
                if fields is not None and (not fields.get("description") or "$ARGUMENTS" not in body):
                    add_error(errors, adapter, 1, "command needs a description and argument placeholder")
            elif "`./zhuzi`" not in body:
                add_error(errors, adapter, 1, "missing repository fallback")


def extract_markdown_headings(text: str, *, level: int) -> list[str]:
    prefix = "#" * level
    return re.findall(rf"^{re.escape(prefix)} .+$", text, re.MULTILINE)


def check_generated_roundtable_doc(
    errors: list[str],
    *,
    relative_path: str,
    roundtable_contract: dict[str, object] | None,
) -> None:
    path = ROOT / relative_path
    if not path.exists():
        add_error(errors, path, 1, "missing generated roundtable doc")
        return

    if roundtable_contract is None:
        return

    current_text = path.read_text(encoding="utf-8")
    try:
        rendered_text = render_doc_text(relative_path, current_text, roundtable_contract)
    except ValueError as exc:
        add_error(errors, path, 1, str(exc))
        return

    if current_text != rendered_text:
        add_error(
            errors,
            path,
            1,
            "generated blocks are stale; run `python3 tools/render_roundtable_contract_docs.py`",
        )


def check_seat_registry(
    errors: list[str],
    roundtable_contract: dict[str, object] | None,
    generated_docs: dict[str, list[str]],
) -> None:
    path = ROOT / "zhuzi" / "references" / "seat-registry.md"
    if not path.exists():
        add_error(errors, path, 1, "missing seat registry")
        return

    text = path.read_text(encoding="utf-8")
    for block_name in generated_docs.get("zhuzi/references/seat-registry.md", []):
        if f"<!-- GENERATED:{block_name}:start -->" not in text or f"<!-- GENERATED:{block_name}:end -->" not in text:
            add_error(errors, path, 1, f"seat registry missing generated block markers for {block_name}")
    check_generated_roundtable_doc(
        errors,
        relative_path="zhuzi/references/seat-registry.md",
        roundtable_contract=roundtable_contract,
    )


def check_shared_seat_contracts(
    errors: list[str],
    roundtable_contract: dict[str, object] | None,
    generated_docs: dict[str, list[str]],
) -> None:
    seat_dir = ROOT / "zhuzi" / "seats"
    if not seat_dir.exists():
        add_error(errors, seat_dir, 1, "missing shared seats directory")
        return

    actual_files = {path.name for path in seat_dir.glob("*.md")}
    expected_files = {f"{seat_name}.md" for seat_name, _ in iter_roundtable_seats(roundtable_contract)}
    if actual_files != expected_files:
        add_error(
            errors,
            seat_dir,
            1,
            f"shared seat set mismatch: expected={sorted(expected_files)} actual={sorted(actual_files)}",
        )

    for seat_name, config in iter_roundtable_seats(roundtable_contract):
        path = seat_dir / f"{seat_name}.md"
        if not path.exists():
            add_error(errors, path, 1, "missing shared seat contract")
            continue

        text = path.read_text(encoding="utf-8")
        relative_path = rel(path)
        required_snippets = config.get("required_contract_snippets")
        if not isinstance(required_snippets, list):
            add_error(errors, ROUNDTABLE_CONTRACT_PATH, 1, f"seat contract {seat_name} missing required_contract_snippets list")
            continue
        for required in ["## 适用范围", "## 职责", "## 越权边界", "## 输出契约", "## 输出底线", *required_snippets]:
            if required not in text:
                add_error(errors, path, 1, f"shared seat contract missing {required}")

        for block_name in generated_docs.get(relative_path, []):
            if f"<!-- GENERATED:{block_name}:start -->" not in text or f"<!-- GENERATED:{block_name}:end -->" not in text:
                add_error(errors, path, 1, f"shared seat contract missing generated block markers for {block_name}")

        if relative_path in generated_docs:
            check_generated_roundtable_doc(
                errors,
                relative_path=relative_path,
                roundtable_contract=roundtable_contract,
            )


def check_quick_roundtable_contract(errors: list[str], roundtable_contract: dict[str, object] | None) -> None:
    template = ROOT / "zhuzi" / "templates" / "roundtable-quick.md"
    expected_headings: list[str] = []
    quick_output = roundtable_contract.get("quick_output") if isinstance(roundtable_contract, dict) else None
    if isinstance(quick_output, dict):
        headings = quick_output.get("headings")
        if isinstance(headings, list):
            expected_headings = [heading for heading in headings if isinstance(heading, str)]

    if not template.exists():
        add_error(errors, template, 1, "missing Quick Roundtable template")
    else:
        template_text = template.read_text(encoding="utf-8")
        skeleton = re.search(r"^```markdown\n(.*?)^```$", template_text, re.MULTILINE | re.DOTALL)
        if not skeleton or extract_markdown_headings(skeleton.group(1), level=2) != expected_headings:
            add_error(errors, template, 1, "Quick template headings differ from the manifest order")
        for category in (quick_output or {}).get("decision_categories", []):
            if not isinstance(category, str):
                continue
            if (
                f"| {category} |" not in template_text
                and f"| `{category}` |" not in template_text
                and f"`{category}`" not in template_text
            ):
                add_error(errors, template, 1, f"quick template missing decision category {category}")

    example = ROOT / "examples" / "roundtable-quick.md"
    if not example.exists():
        add_error(errors, example, 1, "missing Quick Roundtable example")
    else:
        example_text = example.read_text(encoding="utf-8")
        if extract_markdown_headings(example_text, level=2) != expected_headings:
            add_error(errors, example, 1, "Quick example headings differ from the manifest order")

    readme = ROOT / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    for required in [
        "./examples/roundtable-quick.md",
        "./zhuzi/templates/roundtable-quick.md",
        "./docs/INVENTORY.md",
        "./zhuzi/manifests/shipped-surface.json",
        "./zhuzi/manifests/roundtable-contract.json",
        "zhuzi/workflows/roundtable.md",
        "zhuzi/seats/",
    ]:
        if required not in readme_text:
            add_error(errors, readme, 1, f"README missing {required}")


def check_codex_agent_adapters(errors: list[str], roundtable_contract: dict[str, object] | None) -> None:
    agent_dir = CODEX_RUNTIME_ROOT / "agents"
    expected = {f"{name}.toml" for name, _ in iter_roundtable_seats(roundtable_contract)}
    if {p.name for p in agent_dir.glob("*.toml")} != expected or list(agent_dir.glob("*.md")):
        add_error(errors, agent_dir, 1, "Codex agents must match the manifest as native TOML files")
    for seat_name, config in iter_roundtable_seats(roundtable_contract):
        path = agent_dir / f"{seat_name}.toml"
        if not path.exists():
            continue
        try:
            payload = tomllib.loads(path.read_text(encoding="utf-8"))
        except (ValueError, tomllib.TOMLDecodeError) as exc:
            add_error(errors, path, 1, f"invalid native agent: {exc}")
            continue
        if set(payload) != {"name", "description", "developer_instructions"}:
            add_error(errors, path, 1, "thin agent must contain only name, description and developer_instructions")
        description = payload.get("description")
        if payload.get("name") != seat_name or not isinstance(description, str) or not description.strip():
            add_error(errors, path, 1, "invalid native agent identity")
        instructions = payload.get("developer_instructions")
        if not isinstance(instructions, str) or not instructions.strip():
            add_error(errors, path, 1, "missing native agent instructions")
            continue
        skill_name = config["skill"]
        for required in [AGENT_SKILL_PATH_TEMPLATE.format(skill_name=skill_name),
                         AGENT_SEAT_REFERENCE_PATH_TEMPLATE.format(seat_file=f"{seat_name}.md"),
                         AGENT_VERDICT_REFERENCE_PATH, f"./skills/{skill_name}/SKILL.md",
                         f"./zhuzi/seats/{seat_name}.md"]:
            if required not in instructions:
                add_error(errors, path, 1, f"missing shared asset reference {required}")
        for banned in ADAPTER_INLINE_SCHEMA_SNIPPETS:
            if banned in instructions:
                add_error(errors, path, 1, f"native agent inlines shared schema: {banned}")


def check_schema_reference(
    errors: list[str],
    roundtable_contract: dict[str, object] | None,
    generated_docs: dict[str, list[str]],
) -> None:
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
    for block_name in generated_docs.get("zhuzi/references/verdict-schema.md", []):
        if f"<!-- GENERATED:{block_name}:start -->" not in text or f"<!-- GENERATED:{block_name}:end -->" not in text:
            add_error(errors, path, 1, f"schema reference missing generated block markers for {block_name}")
    check_generated_roundtable_doc(
        errors,
        relative_path="zhuzi/references/verdict-schema.md",
        roundtable_contract=roundtable_contract,
    )


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
            entry_role = entry.get("role")
            if isinstance(entry_name, str) and f"`{entry_name}`" not in text:
                add_error(errors, path, 1, f"inventory missing entry `{entry_name}`")
            if isinstance(entry_path, str) and f"`{entry_path}`" not in text:
                add_error(errors, path, 1, f"inventory missing path `{entry_path}`")
            if (
                isinstance(entry_name, str)
                and isinstance(entry_path, str)
                and isinstance(entry_role, str)
            ):
                row_pattern = re.compile(
                    rf"^\|\s*`{re.escape(entry_name)}`\s*\|\s*`{re.escape(entry_path)}`\s*\|\s*(.+?)\s*\|\s*$",
                    re.MULTILINE,
                )
                row_match = row_pattern.search(text)
                if row_match is None:
                    add_error(
                        errors,
                        path,
                        1,
                        f"inventory missing row for `{entry_name}` with path `{entry_path}`",
                    )
                elif row_match.group(1) != entry_role:
                    add_error(
                        errors,
                        path,
                        1,
                        f"inventory role mismatch for `{entry_name}`: inventory={row_match.group(1)!r} manifest={entry_role!r}",
                    )


def check_codex_install(errors: list[str]) -> None:
    path = ROOT / "install.sh"
    text = path.read_text(encoding="utf-8")
    for required in [
        "CODEX_HOME",
        "CLAUDE_RENDER_ROOT",
        "$CODEX_SKILLS",
        "$CLAUDE/skills",
        "$CLAUDE/zhuzi",
        "--codex-only",
        "MANIFEST_PATH",
        "manifest_paths",
        "shipped-surface.json",
        "runtimes/claude/agents",
        "runtimes/claude/commands/zhuzi",
        "seats/references/workflows/templates/manifests",
        "tools/install_codex_source_adapters.py",
        "[5/5] codex roundtable adapter",
    ]:
        if required not in text:
            add_error(errors, path, 1, f"install.sh missing {required}")


def check_codex_source_installer(errors: list[str]) -> None:
    path = ROOT / "tools" / "install_codex_source_adapters.py"
    if not path.exists():
        add_error(errors, path, 1, "missing Codex source adapter installer")
        return

    text = path.read_text(encoding="utf-8")
    for required in [
        "MANIFEST_PATH",
        "load_manifest_families",
        "manifest_family_paths",
        "collapse_repo_fallbacks",
        "render_text",
        "install_source_only_adapters",
        "install_codex_assets",
        "migration_candidates",
        "previous_skill_names",
        "apply_install",
        "resolve_skill_root",
        "tomllib.loads",
        "{{ZHUZI_SKILL_ROOT}}",
        "{{ZHUZI_SHARED_ROOT}}",
        "codex_agents",
        "codex_skills",
    ]:
        if required not in text:
            add_error(errors, path, 1, f"Codex source installer missing {required}")


def iter_skill_entrypoints() -> list[Path]:
    files = list((ROOT / "skills").glob("*/SKILL.md"))
    files.extend((CODEX_RUNTIME_ROOT / "skills").glob("*/SKILL.md"))
    return sorted({path for path in files if path.is_file()})


def check_skill_metadata(errors: list[str]) -> None:
    seen: set[str] = set()
    for path in iter_skill_entrypoints():
        fields = read_frontmatter(errors, path, path.read_text(encoding="utf-8"))
        if fields is None:
            continue
        name = fields.get("name")
        if name != path.parent.name or not SKILL_NAME.fullmatch(path.parent.name) or len(path.parent.name) > 64:
            add_error(errors, path, 1, "skill name must match the skill folder and Agent Skills naming rules")
        elif name in seen:
            add_error(errors, path, 1, f"duplicate installed skill name {name}")
        else:
            seen.add(name)

        description = fields.get("description")
        if not isinstance(description, str) or not 0 < len(description.strip()) <= 1024:
            add_error(errors, path, 1, "skill description must be a non-empty string of at most 1024 characters")
        metadata = fields.get("metadata", {})
        if not isinstance(metadata, dict) or any(
            not isinstance(key, str) or not isinstance(value, str) for key, value in metadata.items()
        ):
            add_error(errors, path, 1, "skill metadata must map strings to strings")


def check_markdown_links(errors: list[str]) -> None:
    # Check repository-relative links without fetching external research sources.
    for path in iter_files([*ACTIVE_TEXT_GLOBS, "skills/**/*.md", "archive/**/*.md"]):
        if path.suffix != ".md":
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for match in MARKDOWN_LINK.finditer(line):
                target = urlsplit(match.group(1) or match.group(2))
                if target.scheme or target.netloc or not target.path:
                    continue
                if not (path.parent / unquote(target.path)).exists():
                    add_error(errors, path, line_number, f"missing linked path {target.path}")


def check_readme_persona_coverage(
    errors: list[str],
    manifest_families: dict[str, list[dict[str, str]]] | None,
) -> None:
    if manifest_families is None:
        return
    skills = manifest_families.get("skills")
    if not isinstance(skills, list):
        return

    readme = ROOT / "README.md"
    if not readme.exists():
        add_error(errors, readme, 1, "missing README.md")
        return

    text = readme.read_text(encoding="utf-8")
    persona_pattern = re.compile(r"^####\s+.+?·\s+`([^`]+)`\s*$", re.MULTILINE)
    documented = {match.group(1) for match in persona_pattern.finditer(text)}

    for entry in skills:
        if not isinstance(entry, dict):
            continue
        entry_name = entry.get("entry")
        if isinstance(entry_name, str) and entry_name not in documented:
            add_error(
                errors,
                readme,
                1,
                f"README missing skill section for `{entry_name}` "
                f"(expected an `#### <Name> · `{entry_name}`` heading)",
            )


def main() -> int:
    errors: list[str] = []
    manifest_families = load_manifest(errors)
    roundtable_contract = load_roundtable_contract(errors)
    generated_docs = resolve_generated_docs(errors, roundtable_contract)

    check_banned_snippets(errors)
    check_claude_agent_adapters(errors, roundtable_contract)
    check_runtime_path_templates(errors)
    check_workflow_adapters(errors)
    check_seat_registry(errors, roundtable_contract, generated_docs)
    check_shared_seat_contracts(errors, roundtable_contract, generated_docs)
    check_quick_roundtable_contract(errors, roundtable_contract)
    check_readme_persona_coverage(errors, manifest_families)
    check_codex_agent_adapters(errors, roundtable_contract)
    check_schema_reference(errors, roundtable_contract, generated_docs)
    check_manifest(errors, manifest_families)
    check_inventory(errors, manifest_families)
    check_skill_metadata(errors)
    check_markdown_links(errors)
    check_codex_install(errors)
    check_codex_source_installer(errors)

    if errors:
        print("Consistency check failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Consistency check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
