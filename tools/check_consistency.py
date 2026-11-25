#!/usr/bin/env python3
"""Check shared contracts, open Agent Skills compliance, dual-runtime adapters, and eval coverage."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from render_roundtable_contract_docs import (
    STATIC_GENERATED_DOCS,
    build_full_rendered_files,
    get_generated_docs,
    render_doc_text,
)


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
AGENT_PERSONA_PATH_TEMPLATE = "{{{{ZHUZI_SKILL_ROOT}}}}/{skill_name}/PERSONA.md"

SKILL_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MARKDOWN_LINK = re.compile(r"\]\(\s*(?:<([^>\n]+)>|([^\s)]+))")

OPEN_AGENTSKILLS_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
SKILL_MAX_LINES = 500
SKILL_DESCRIPTION_MAX_BYTES = 1024
SKILL_DESCRIPTION_CONCISE_BYTES = 360
OPENAI_SHORT_DESC_MAX_CHARS = 64
AGENTS_RULE_MAX_BYTES = 24000
AGENTS_RULE_MAX_LINES = 200
TOC_REQUIRED_MIN_LINES = 100

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
    "/zhuzi:roundtable",
    "/zhuzi:quick",
    "$zhuzi-roundtable",
    "$zhuzi-quick",
    "luxun-zawen",
]

SURFACE_FAMILIES = [
    (
        "Skills",
        "skills",
        lambda: sorted((ROOT / "skills").glob("*/SKILL.md")),
        lambda path: path.parent.name,
    ),
    (
        "OpenAI Sidecars",
        "openai_sidecars",
        lambda: sorted((ROOT / "skills").glob("*/agents/openai.yaml")),
        lambda path: path.parents[1].name,
    ),
    (
        "Claude Skills",
        "claude_skills",
        lambda: sorted((CLAUDE_RUNTIME_ROOT / "skills").glob("*/SKILL.md")),
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
        "Schemas",
        "schemas",
        lambda: sorted((ROOT / "zhuzi" / "schemas").glob("*.json")),
        lambda path: path.stem,
    ),
    (
        "Validators",
        "validators",
        lambda: sorted((ROOT / "zhuzi" / "validators").glob("*.py")),
        lambda path: path.stem,
    ),
    (
        "Evals",
        "evals",
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
    return sorted({path for path in files if path.is_file() and not path.name.endswith(":Zone.Identifier")})


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def add_error(errors: list[str], path: Path, lineno: int, message: str) -> None:
    errors.append(f"{rel(path)}:{lineno}: {message}")


def load_surface(errors: list[str]) -> dict[str, object] | None:
    if not MANIFEST_PATH.exists():
        add_error(errors, MANIFEST_PATH, 1, "missing shipped surface manifest")
        return None

    try:
        payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_error(errors, MANIFEST_PATH, exc.lineno or 1, f"invalid JSON: {exc.msg}")
        return None

    if not isinstance(payload, dict) or not isinstance(payload.get("families"), dict):
        add_error(errors, MANIFEST_PATH, 1, "manifest missing top-level families object")
        return None

    return payload


def load_roundtable_contract(errors: list[str]) -> dict[str, object] | None:
    if not ROUNDTABLE_CONTRACT_PATH.exists():
        add_error(errors, ROUNDTABLE_CONTRACT_PATH, 1, "missing roundtable contract manifest")
        return None

    try:
        payload = json.loads(ROUNDTABLE_CONTRACT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_error(errors, ROUNDTABLE_CONTRACT_PATH, exc.lineno or 1, f"invalid JSON: {exc.msg}")
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
        for field in [
            "skill",
            "agent",
            "persona",
            "adapter",
            "generated_block",
            "registry_summary",
            "registry_stage_row",
            "output_contract",
            "required_contract_snippets",
        ]:
            if field not in config:
                add_error(errors, ROUNDTABLE_CONTRACT_PATH, 1, f"seat contract {seat_name} missing {field}")

    return payload


def iter_roundtable_seats(roundtable_contract: dict[str, object] | None) -> list[tuple[str, dict[str, object]]]:
    if not roundtable_contract:
        return []
    seats = roundtable_contract.get("seats")
    if not isinstance(seats, dict):
        return []
    return [(k, v) for k, v in seats.items() if isinstance(k, str) and isinstance(v, dict)]


def resolve_generated_docs(
    errors: list[str],
    roundtable_contract: dict[str, object] | None,
) -> dict[str, list[str]]:
    if roundtable_contract is None:
        return {k: list(v) for k, v in STATIC_GENERATED_DOCS.items()}
    try:
        return get_generated_docs(roundtable_contract)
    except ValueError as exc:
        add_error(errors, ROUNDTABLE_CONTRACT_PATH, 1, str(exc))
        return {k: list(v) for k, v in STATIC_GENERATED_DOCS.items()}


def check_banned_snippets(errors: list[str]) -> None:
    for path in iter_files(ACTIVE_TEXT_GLOBS):
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            for snippet in BANNED_SNIPPETS:
                if snippet in line:
                    add_error(errors, path, lineno, f"banned snippet: {snippet}")


def read_frontmatter(errors: list[str], path: Path, text: str) -> dict | None:
    header = re.match(r"\A---\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.DOTALL)
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
    if (CLAUDE_RUNTIME_ROOT / "commands").exists():
        add_error(
            errors,
            CLAUDE_RUNTIME_ROOT / "commands",
            1,
            "legacy .claude/commands directory must be migrated to runtimes/claude/skills/",
        )

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
            if "skills" in fields:
                add_error(errors, path, 1, "Claude seat must not preload full skills via frontmatter skills field")
            max_turns = fields.get("maxTurns")
            if not isinstance(max_turns, int) or max_turns < 1 or max_turns > 60:
                add_error(errors, path, 1, "Claude seat requires a bounded integer maxTurns (1..60)")

            raw_tools = fields.get("tools")
            tools = {name.strip() for name in raw_tools.split(",")} if isinstance(raw_tools, str) else set()
            raw_disallowed = fields.get("disallowedTools")
            disallowed = (
                {name.strip() for name in raw_disallowed.split(",")}
                if isinstance(raw_disallowed, str)
                else set()
            )
            if "Read" not in tools:
                add_error(errors, path, 1, "Claude seat requires an explicit tool list with Read")
            elif seat_name != "linus-engineer":
                if tools & {"Write", "Edit", "Bash", "NotebookEdit"}:
                    add_error(errors, path, 1, "analysis seats cannot declare Write, Edit, or Bash tools")
                if not {"Write", "Edit", "Bash"}.issubset(disallowed):
                    add_error(errors, path, 1, "analysis seats must explicitly disallow Write, Edit, and Bash")

        skill_name = config.get("skill")
        if not isinstance(skill_name, str):
            add_error(errors, ROUNDTABLE_CONTRACT_PATH, 1, f"seat contract {seat_name} missing string skill")
            continue

        expected_persona = AGENT_PERSONA_PATH_TEMPLATE.format(skill_name=skill_name)
        expected_seat = AGENT_SEAT_REFERENCE_PATH_TEMPLATE.format(seat_file=f"{seat_name}.md")
        for required in [expected_persona, expected_seat, AGENT_VERDICT_REFERENCE_PATH]:
            if required not in text:
                add_error(errors, path, 1, f"missing Claude agent reference {required}")
        for banned in ADAPTER_INLINE_SCHEMA_SNIPPETS:
            if banned in text:
                add_error(errors, path, 1, f"Claude agent should not inline shared schema snippet {banned}")


def check_codex_agent_adapters(errors: list[str], roundtable_contract: dict[str, object] | None) -> None:
    if (CODEX_RUNTIME_ROOT / "skills").exists():
        add_error(
            errors,
            CODEX_RUNTIME_ROOT / "skills",
            1,
            "separate runtimes/codex/skills directory must be consolidated into skills/zhuzi/",
        )

    agent_dir = CODEX_RUNTIME_ROOT / "agents"
    expected = {f"{name}.toml" for name, _ in iter_roundtable_seats(roundtable_contract)}
    if {p.name for p in agent_dir.glob("*.toml")} != expected or list(agent_dir.glob("*.md")):
        add_error(errors, agent_dir, 1, "Codex agents must match the manifest as native TOML files")

    allowed_top_keys = {"name", "description", "developer_instructions", "features", "skills"}
    for seat_name, config in iter_roundtable_seats(roundtable_contract):
        path = agent_dir / f"{seat_name}.toml"
        if not path.exists():
            continue
        try:
            payload = tomllib.loads(path.read_text(encoding="utf-8"))
        except (ValueError, tomllib.TOMLDecodeError) as exc:
            add_error(errors, path, 1, f"invalid native agent: {exc}")
            continue
        if not set(payload).issubset(allowed_top_keys) or not {"name", "description", "developer_instructions"}.issubset(payload):
            add_error(errors, path, 1, f"unexpected Codex agent keys: {sorted(payload)}")
        if "sandbox_mode" in payload:
            add_error(errors, path, 1, "custom agent TOML cannot override session sandbox_mode")

        description = payload.get("description")
        if payload.get("name") != seat_name or not isinstance(description, str) or not description.strip():
            add_error(errors, path, 1, "invalid native agent identity")

        features = payload.get("features")
        skills_cfg = payload.get("skills")
        if not isinstance(skills_cfg, dict) or skills_cfg.get("include_instructions") is not False:
            add_error(errors, path, 1, "Codex seat must set skills.include_instructions = false")
        if not isinstance(features, dict) or features.get("request_permissions_tool") is not False:
            add_error(errors, path, 1, "Codex seat must set features.request_permissions_tool = false")
        if seat_name != "linus-engineer" and (not isinstance(features, dict) or features.get("shell_tool") is not False):
            add_error(errors, path, 1, "Codex read-only seat must set features.shell_tool = false")

        instructions = payload.get("developer_instructions")
        if not isinstance(instructions, str) or not instructions.strip():
            add_error(errors, path, 1, "missing native agent instructions")
            continue
        skill_name = str(config["skill"])
        for required in [
            AGENT_PERSONA_PATH_TEMPLATE.format(skill_name=skill_name),
            AGENT_SEAT_REFERENCE_PATH_TEMPLATE.format(seat_file=f"{seat_name}.md"),
            AGENT_VERDICT_REFERENCE_PATH,
            f"./skills/{skill_name}/SKILL.md",
            f"./zhuzi/seats/{seat_name}.md",
        ]:
            if required not in instructions:
                add_error(errors, path, 1, f"missing shared asset reference {required}")
        for banned in ADAPTER_INLINE_SCHEMA_SNIPPETS:
            if banned in instructions:
                add_error(errors, path, 1, f"native agent inlines shared schema: {banned}")


def check_runtime_path_templates(errors: list[str]) -> None:
    template_files = list((ROOT / "runtimes").glob("**/*.md"))
    template_files.extend((ROOT / "runtimes").glob("**/*.toml"))
    template_files.extend((ROOT / "zhuzi" / "workflows").glob("*.md"))
    template_files.extend((ROOT / "zhuzi" / "seats").glob("*.md"))
    template_files.append(ROOT / "skills" / "zhuzi" / "SKILL.md")

    banned_runtime_literals = [
        "~/.claude/",
        "~/.codex/",
        "@~/.claude/",
        "@~/.codex/",
        "$HOME/.claude/",
        "$HOME/.codex/",
    ]
    for path in template_files:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for literal in banned_runtime_literals:
            if literal in text:
                add_error(errors, path, 1, f"runtime template leaked hardcoded path {literal}")


def check_workflow_adapters(errors: list[str]) -> None:
    runtime_primitives = (
        "Agent(",
        "SendMessage(",
        "spawn_agent(",
        "wait_agent(",
        "followup_task(",
        "send_input(",
        "invoke_subagent(",
        "send_message(",
    )
    for workflow in ("roundtable", "quick-multi"):
        shared_file = f"workflows/{workflow}.md"
        path = ROOT / "zhuzi" / shared_file
        if not path.is_file():
            add_error(errors, path, 1, "missing shared workflow")
            continue
        text = path.read_text(encoding="utf-8")
        for primitive in runtime_primitives:
            if primitive in text:
                add_error(errors, path, 1, f"shared workflow leaked runtime-specific primitive {primitive}")
        if workflow == "roundtable":
            for snippet in (
                "## 阶段 0.5",
                "## 阶段 1",
                "## 阶段 1.5",
                "## 阶段 2",
                "## 阶段 3",
                "## 阶段 4",
                "invoke_seat",
                "continue_existing_agent",
                "not_committed",
            ):
                if snippet not in text:
                    add_error(errors, path, 1, f"roundtable workflow missing core contract snippet {snippet}")

    for adapter in (
        ROOT / "skills" / "zhuzi" / "SKILL.md",
        CLAUDE_RUNTIME_ROOT / "skills" / "zhuzi" / "SKILL.md",
    ):
        if not adapter.is_file():
            add_error(errors, adapter, 1, "missing unified zhuzi workflow skill adapter")
            continue
        body = adapter.read_text(encoding="utf-8")
        for shared_file in ("workflows/roundtable.md", "workflows/quick-multi.md"):
            if f"{{{{ZHUZI_SHARED_ROOT}}}}/{shared_file}" not in body:
                add_error(errors, adapter, 1, f"missing shared workflow reference {shared_file}")
        if "`./zhuzi/workflows/roundtable.md`" not in body:
            add_error(errors, adapter, 1, "missing repository fallback in zhuzi router")
        if adapter.is_relative_to(CLAUDE_RUNTIME_ROOT):
            fields = read_frontmatter(errors, adapter, body)
            if fields is not None:
                if fields.get("disable-model-invocation") is not True:
                    add_error(errors, adapter, 1, "Claude zhuzi skill must set disable-model-invocation: true")
                if not fields.get("argument-hint"):
                    add_error(errors, adapter, 1, "Claude zhuzi skill requires argument-hint")


def check_root_instruction_files(errors: list[str]) -> None:
    agents_md = ROOT / "AGENTS.md"
    if not agents_md.is_file():
        add_error(errors, agents_md, 1, "missing root AGENTS.md")
    else:
        raw = agents_md.read_bytes()
        text = raw.decode("utf-8")
        if text.startswith("---\n") or text.startswith("---\r\n"):
            add_error(errors, agents_md, 1, "standalone AGENTS.md must not declare YAML frontmatter")
        if len(raw) > AGENTS_RULE_MAX_BYTES:
            add_error(errors, agents_md, 1, f"AGENTS.md exceeds {AGENTS_RULE_MAX_BYTES}-byte rule cap")
        if len(text.splitlines()) > AGENTS_RULE_MAX_LINES:
            add_error(errors, agents_md, 1, f"AGENTS.md exceeds {AGENTS_RULE_MAX_LINES}-line conciseness cap")
        for required in ("## Code Review Rules", "## 提交规范", "`feat/fix/refactor/style/chore/docs`"):
            if required not in text:
                add_error(errors, agents_md, 1, f"AGENTS.md missing {required}")

    claude_md = ROOT / "CLAUDE.md"
    if not claude_md.is_file() or claude_md.read_text(encoding="utf-8").strip() != "@AGENTS.md":
        add_error(errors, claude_md, 1, "CLAUDE.md must remain a thin @AGENTS.md shim")


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


def check_full_ssot_rendered_outputs(
    errors: list[str],
    roundtable_contract: dict[str, object] | None,
    surface: dict[str, object] | None,
) -> None:
    if roundtable_contract is None or surface is None:
        return
    try:
        expected_map = build_full_rendered_files(roundtable_contract, surface)
    except (ValueError, KeyError) as exc:
        add_error(errors, ROUNDTABLE_CONTRACT_PATH, 1, f"failed to build SSOT outputs: {exc}")
        return
    for relative_path, expected_text in expected_map.items():
        target = ROOT / relative_path
        if not target.is_file() or target.read_text(encoding="utf-8") != expected_text:
            add_error(
                errors,
                target,
                1,
                "derived SSOT file is missing or stale; run `python3 tools/render_roundtable_contract_docs.py`",
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

    for example_name in ("roundtable-quick.md", "roundtable-disagreement.md"):
        example = ROOT / "examples" / example_name
        if not example.exists():
            add_error(errors, example, 1, f"missing {example_name} example")
        elif extract_markdown_headings(example.read_text(encoding="utf-8"), level=2) != expected_headings:
            add_error(errors, example, 1, f"{example_name} headings differ from the manifest order")

    rev_example = ROOT / "examples" / "roundtable-revision-gate.md"
    if not rev_example.is_file() or "## 阶段 1.5 · 修订对照" not in rev_example.read_text(encoding="utf-8"):
        add_error(errors, rev_example, 1, "revision-gate example missing stage 1.5 comparison section")

    quick_example = ROOT / "examples" / "quick-multi.md"
    max_chars = int((roundtable_contract or {}).get("modes", {}).get("quick-multi", {}).get("max_characters", 200))  # type: ignore[union-attr]
    if not quick_example.is_file():
        add_error(errors, quick_example, 1, "missing quick-multi example")
    else:
        q_text = quick_example.read_text(encoding="utf-8")
        if "## 一句话对照" not in q_text or "```yaml" in q_text:
            add_error(errors, quick_example, 1, "quick-multi example must include comparison table and no YAML blocks")
        sections = re.split(r"^## ", q_text, flags=re.MULTILINE)[1:]
        for sec in sections:
            lines = sec.strip().splitlines()
            heading = lines[0]
            if heading.startswith("一句话对照"):
                continue
            body = "".join(line.strip() for line in lines[1:] if line.strip())
            if len(body) > max_chars:
                add_error(errors, quick_example, 1, f"quick-multi seat {heading!r} exceeds {max_chars} chars ({len(body)})")

    readme = ROOT / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    for required in [
        "./skills/zhuzi/SKILL.md",
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


def check_manifest(errors: list[str], manifest_families: dict[str, list[dict[str, object]]] | None) -> None:
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


def check_inventory(errors: list[str], manifest_families: dict[str, list[dict[str, object]]] | None) -> None:
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


def check_install_scripts(errors: list[str]) -> None:
    sh_path = ROOT / "install.sh"
    if not os.access(sh_path, os.X_OK):
        add_error(errors, sh_path, 1, "install.sh must be executable (chmod +x)")
    sh_text = sh_path.read_text(encoding="utf-8")
    if "tools/install_codex_source_adapters.py" not in sh_text or "sed " in sh_text:
        add_error(errors, sh_path, 1, "install.sh must delegate to tools/install_codex_source_adapters.py without fragile sed")

    py_path = ROOT / "tools" / "install_codex_source_adapters.py"
    if not py_path.exists():
        add_error(errors, py_path, 1, "missing dual-runtime installer")
        return
    py_text = py_path.read_text(encoding="utf-8")
    for required in [
        "MANIFEST_PATH",
        "load_manifest_families",
        "collapse_repo_fallbacks",
        "render_text",
        "install_codex_assets",
        "install_claude_assets",
        "migration_candidates",
        "apply_install",
        "resolve_skill_root",
        "serialize_agent_toml",
        "--pin",
        "--unpin",
        "--uninstall",
    ]:
        if required not in py_text:
            add_error(errors, py_path, 1, f"installer missing {required}")


def iter_skill_entrypoints() -> list[Path]:
    return sorted(path for path in (ROOT / "skills").glob("*/SKILL.md") if path.is_file())


def check_skill_metadata(errors: list[str], manifest_families: dict[str, list[dict[str, object]]] | None) -> None:
    seen: set[str] = set()
    skills_meta = {
        str(item["entry"]): item
        for item in (manifest_families or {}).get("skills", [])
        if isinstance(item, dict) and isinstance(item.get("entry"), str)
    }

    for path in iter_skill_entrypoints():
        text = path.read_text(encoding="utf-8")
        line_count = len(text.splitlines())
        if line_count > SKILL_MAX_LINES:
            add_error(errors, path, 1, f"SKILL.md exceeds {SKILL_MAX_LINES}-line upper limit ({line_count})")

        fields = read_frontmatter(errors, path, text)
        if fields is None:
            continue

        non_portable = set(fields) - OPEN_AGENTSKILLS_KEYS
        if non_portable:
            add_error(
                errors,
                path,
                1,
                f"shared SKILL.md contains non-portable host frontmatter keys: {sorted(non_portable)}",
            )

        name = fields.get("name")
        if name != path.parent.name or not SKILL_NAME.fullmatch(path.parent.name) or len(path.parent.name) > 64:
            add_error(errors, path, 1, "skill name must match the skill folder and Agent Skills naming rules")
        elif name in seen:
            add_error(errors, path, 1, f"duplicate installed skill name {name}")
        else:
            seen.add(name)

        description = fields.get("description")
        if not isinstance(description, str) or not description.strip():
            add_error(errors, path, 1, "skill description must be a non-empty string")
        else:
            desc_bytes = len(description.strip().encode("utf-8"))
            if desc_bytes > SKILL_DESCRIPTION_MAX_BYTES:
                add_error(errors, path, 1, f"skill description exceeds {SKILL_DESCRIPTION_MAX_BYTES} UTF-8 bytes ({desc_bytes})")
            elif desc_bytes > SKILL_DESCRIPTION_CONCISE_BYTES:
                add_error(errors, path, 1, f"skill description exceeds concise trigger budget of {SKILL_DESCRIPTION_CONCISE_BYTES} UTF-8 bytes ({desc_bytes})")
            if "不触发" not in description:
                add_error(errors, path, 1, "skill description must explicitly declare negative non-trigger boundaries")

        metadata = fields.get("metadata", {})
        if not isinstance(metadata, dict) or any(
            not isinstance(key, str) or not isinstance(value, str) for key, value in metadata.items()
        ):
            add_error(errors, path, 1, "skill metadata must map strings to strings")

        # Validate paired agents/openai.yaml sidecar
        sidecar = path.parent / "agents" / "openai.yaml"
        if not sidecar.is_file():
            add_error(errors, path, 1, "missing Codex sidecar agents/openai.yaml")
            continue
        try:
            sidecar_data = yaml.safe_load(sidecar.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            add_error(errors, sidecar, 1, f"invalid YAML in agents/openai.yaml: {exc}")
            continue
        if not isinstance(sidecar_data, dict):
            add_error(errors, sidecar, 1, "agents/openai.yaml must be a mapping")
            continue
        iface = sidecar_data.get("interface")
        policy = sidecar_data.get("policy")
        if not isinstance(iface, dict) or not iface.get("display_name") or not iface.get("short_description"):
            add_error(errors, sidecar, 1, "agents/openai.yaml requires interface.display_name and interface.short_description")
        elif len(str(iface["short_description"])) > OPENAI_SHORT_DESC_MAX_CHARS:
            add_error(errors, sidecar, 1, f"interface.short_description exceeds {OPENAI_SHORT_DESC_MAX_CHARS} chars")
        if not isinstance(policy, dict) or not isinstance(policy.get("allow_implicit_invocation"), bool):
            add_error(errors, sidecar, 1, "agents/openai.yaml requires boolean policy.allow_implicit_invocation")
        elif isinstance(name, str) and name in skills_meta:
            expected_implicit = bool(skills_meta[name].get("implicit_invocation", False))
            if policy["allow_implicit_invocation"] != expected_implicit:
                add_error(errors, sidecar, 1, "allow_implicit_invocation differs from shipped-surface.json policy")


def check_skill_progressive_references(errors: list[str]) -> None:
    banned_ref_filenames = {"upgrade-notes.md", "verification-report.md", "synthesis.md"}

    for skill_dir in sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir()):
        for d in sorted(skill_dir.rglob("*")):
            if d.is_dir() and not any(d.iterdir()):
                add_error(errors, d, 1, "empty directory inside skill package")
            if d.is_file() and d.name.endswith(":Zone.Identifier"):
                add_error(errors, d, 1, "WSL Zone.Identifier artifact inside skill package")

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        ref_dir = skill_dir / "references"
        expected_top_refs = {path.resolve() for path in ref_dir.glob("*.md") if path.is_file()} if ref_dir.is_dir() else set()
        direct_linked_refs: set[Path] = set()

        for line_no, line in enumerate(skill_md.read_text(encoding="utf-8").splitlines(), 1):
            for match in MARKDOWN_LINK.finditer(line):
                target = urlsplit(match.group(1) or match.group(2))
                if target.scheme or target.netloc or not target.path:
                    continue
                raw_rel = unquote(target.path)
                # Ignore repo-fallback lines like `../<入口名>/SKILL.md` which are in backticks, not markdown links
                resolved = (skill_md.parent / raw_rel).resolve()
                rel_parts = Path(raw_rel).parts
                if len(rel_parts) != 2 or rel_parts[0] != "references" or not raw_rel.endswith(".md"):
                    add_error(errors, skill_md, line_no, f"SKILL.md reference must stay 1 level deep under references/*.md: {raw_rel}")
                    continue
                if resolved.is_file():
                    direct_linked_refs.add(resolved)

        for unlinked in sorted(expected_top_refs - direct_linked_refs):
            add_error(errors, skill_md, 1, f"top-level reference not directly linked in 1 hop from SKILL.md: {rel(unlinked)}")

        for ref_file in sorted(expected_top_refs):
            if ref_file.name in banned_ref_filenames:
                add_error(errors, ref_file, 1, f"non-runtime historical draft {ref_file.name} must live under references/research/")
            ref_text = ref_file.read_text(encoding="utf-8")
            ref_lines = ref_text.splitlines()
            if "历史设计或评估记录" in ref_text:
                add_error(errors, ref_file, 1, "historical build/eval record leaked into runtime references/")
            if len(ref_lines) > TOC_REQUIRED_MIN_LINES and "## 目录" not in "\n".join(ref_lines[:40]):
                add_error(errors, ref_file, 1, f"reference file >{TOC_REQUIRED_MIN_LINES} lines missing top `## 目录`")
            for line_no, line in enumerate(ref_lines, 1):
                for match in MARKDOWN_LINK.finditer(line):
                    target = urlsplit(match.group(1) or match.group(2))
                    if target.scheme or target.netloc or not target.path:
                        continue
                    raw_rel = unquote(target.path)
                    if "research/" in raw_rel or "sources/" in raw_rel:
                        add_error(errors, ref_file, line_no, f"runtime reference must not link to research drafts: {raw_rel}")


def check_markdown_links(errors: list[str]) -> None:
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
    manifest_families: dict[str, list[dict[str, object]]] | None,
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
        if not isinstance(entry, dict) or entry.get("default_install", False):
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


def check_eval_suites(
    errors: list[str],
    manifest_families: dict[str, list[dict[str, object]]] | None,
) -> None:
    if manifest_families is None:
        return
    all_skill_names = {
        str(item["entry"])
        for item in manifest_families.get("skills", [])
        if isinstance(item, dict) and isinstance(item.get("entry"), str)
    }
    persona_skill_names = all_skill_names - {"zhuzi"}

    cases_path = ROOT / "evals" / "cases.json"
    if not cases_path.is_file():
        add_error(errors, cases_path, 1, "missing evals/cases.json")
    else:
        cases_data = json.loads(cases_path.read_text(encoding="utf-8"))
        covered_personas: set[str] = set()
        for case in cases_data.get("cases", []):
            for sk in case.get("skills", []):
                covered_personas.add(str(sk))
        missing_personas = sorted(persona_skill_names - covered_personas)
        if missing_personas:
            add_error(errors, cases_path, 1, f"evals/cases.json missing persona coverage for: {missing_personas}")

    trigger_path = ROOT / "evals" / "trigger_cases.json"
    if not trigger_path.is_file():
        add_error(errors, trigger_path, 1, "missing evals/trigger_cases.json")
        return
    trigger_data = json.loads(trigger_path.read_text(encoding="utf-8"))
    suites = trigger_data.get("skills", {})
    if not isinstance(suites, dict):
        add_error(errors, trigger_path, 1, "trigger_cases.json missing skills mapping")
        return
    if set(suites) != all_skill_names:
        add_error(
            errors,
            trigger_path,
            1,
            f"trigger_cases.json skill coverage mismatch: expected={sorted(all_skill_names)} actual={sorted(suites)}",
        )
    for sk_name, spec in suites.items():
        pos = spec.get("should_trigger", []) if isinstance(spec, dict) else []
        neg = spec.get("should_not_trigger", []) if isinstance(spec, dict) else []
        if len(pos) < 2 or len(neg) < 2:
            add_error(
                errors,
                trigger_path,
                1,
                f"trigger_cases.json entry {sk_name} requires >=2 should_trigger and >=2 should_not_trigger queries",
            )


def main() -> int:
    errors: list[str] = []
    surface = load_surface(errors)
    manifest_families = surface.get("families") if isinstance(surface, dict) else None  # type: ignore[assignment]
    roundtable_contract = load_roundtable_contract(errors)
    generated_docs = resolve_generated_docs(errors, roundtable_contract)

    check_banned_snippets(errors)
    check_root_instruction_files(errors)
    check_claude_agent_adapters(errors, roundtable_contract)
    check_codex_agent_adapters(errors, roundtable_contract)
    check_runtime_path_templates(errors)
    check_workflow_adapters(errors)
    check_full_ssot_rendered_outputs(errors, roundtable_contract, surface)
    check_seat_registry(errors, roundtable_contract, generated_docs)
    check_shared_seat_contracts(errors, roundtable_contract, generated_docs)
    check_quick_roundtable_contract(errors, roundtable_contract)
    check_readme_persona_coverage(errors, manifest_families)
    check_schema_reference(errors, roundtable_contract, generated_docs)
    check_manifest(errors, manifest_families)
    check_inventory(errors, manifest_families)
    check_skill_metadata(errors, manifest_families)
    check_skill_progressive_references(errors)
    check_markdown_links(errors)
    check_install_scripts(errors)
    check_eval_suites(errors, manifest_families)

    if errors:
        print("Consistency check failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Consistency check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
