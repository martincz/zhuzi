#!/usr/bin/env python3
"""Render contract docs, JSON Schema, dual-runtime adapters, sidecars, and inventory from SSOT manifests."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:  # Python 3.10
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from zhuzi.validators.verdict import build_schema

ROUNDTABLE_CONTRACT_PATH = ROOT / "zhuzi" / "manifests" / "roundtable-contract.json"
SHIPPED_SURFACE_PATH = ROOT / "zhuzi" / "manifests" / "shipped-surface.json"

SEAT_REGISTRY_PATH = "zhuzi/references/seat-registry.md"
VERDICT_SCHEMA_PATH = "zhuzi/references/verdict-schema.md"
INVENTORY_PATH = "docs/INVENTORY.md"

STATIC_GENERATED_DOCS = {
    SEAT_REGISTRY_PATH: [
        "seat_registry_current_seats",
        "seat_registry_stage_rules",
        "seat_registry_lopez_must_call",
        "seat_registry_linus_dual_stage",
    ],
    VERDICT_SCHEMA_PATH: [
        "verdict_schema_modes",
        "verdict_schema_layers",
        "verdict_schema_core_table",
        "verdict_schema_review_flags",
        "verdict_schema_seat_specific",
        "verdict_schema_route_rules",
        "verdict_schema_phase_4_exception",
    ],
}

INVENTORY_FAMILY_ORDER = [
    ("Skills", "skills"),
    ("OpenAI Sidecars", "openai_sidecars"),
    ("Claude Skills", "claude_skills"),
    ("Agents", "agents"),
    ("Codex Agents", "codex_agents"),
    ("Workflows", "workflows"),
    ("Seats", "seats"),
    ("References", "references"),
    ("Templates", "templates"),
    ("Manifests", "manifests"),
    ("Examples", "examples"),
    ("Tools", "tools"),
    ("Schemas", "schemas"),
    ("Validators", "validators"),
    ("Evals", "evals"),
]


def load_roundtable_contract(path: Path = ROUNDTABLE_CONTRACT_PATH) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"roundtable contract must be a JSON object: {path}")
    return payload


def load_shipped_surface(path: Path = SHIPPED_SURFACE_PATH) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"shipped surface manifest must be a JSON object: {path}")
    return payload


def iter_seats(contract: dict[str, object]) -> list[tuple[str, dict[str, object]]]:
    seats = contract.get("seats")
    if not isinstance(seats, dict):
        raise ValueError("roundtable contract missing seats object")

    result: list[tuple[str, dict[str, object]]] = []
    for seat_name, config in seats.items():
        if not isinstance(seat_name, str) or not isinstance(config, dict):
            raise ValueError("roundtable contract seats must map string names to objects")
        result.append((seat_name, config))
    return result


def get_seat_config(contract: dict[str, object], seat_name: str) -> dict[str, object]:
    seats = contract.get("seats")
    if not isinstance(seats, dict):
        raise ValueError("roundtable contract missing seats object")

    config = seats.get(seat_name)
    if not isinstance(config, dict):
        raise ValueError(f"roundtable contract missing seat config: {seat_name}")
    return config


def get_seat_relative_path(seat_name: str) -> str:
    return f"zhuzi/seats/{seat_name}.md"


def expect_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty string")
    return value


def expect_string_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{label} must be a non-empty string list")
    return [str(item) for item in value]


def get_seat_generated_block(config: dict[str, object], *, seat_name: str) -> str:
    return expect_string(config.get("generated_block"), f"{seat_name}.generated_block")


def get_generated_docs(contract: dict[str, object]) -> dict[str, list[str]]:
    generated_docs = {
        relative_path: list(block_names)
        for relative_path, block_names in STATIC_GENERATED_DOCS.items()
    }
    for seat_name, config in iter_seats(contract):
        relative_path = get_seat_relative_path(seat_name)
        if relative_path in generated_docs:
            raise ValueError(f"duplicate generated doc path: {relative_path}")
        generated_docs[relative_path] = [get_seat_generated_block(config, seat_name=seat_name)]
    return generated_docs


def render_markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def markdownize_literals(value: str) -> str:
    return re.sub(r"\b[A-Za-z0-9_.-]+\b", lambda match: f"`{match.group(0)}`", value)


def markdownize_stage_markers(value: str) -> str:
    if "`[" in value:
        return value
    return re.sub(r"\[[0-9,]+\]", lambda match: f"`{match.group(0)}`", value)


def render_seat_registry_current_seats(contract: dict[str, object]) -> str:
    headers = ["席位", "agent", "职责", "默认 `stages`", "擅长领域（议题匹配关键词）"]
    rows: list[list[str]] = []
    for seat_name, config in iter_seats(contract):
        summary = config.get("registry_summary")
        if not isinstance(summary, dict):
            raise ValueError(f"{seat_name} missing registry_summary")
        rows.append(
            [
                str(summary.get("seat", "")),
                f"`{seat_name}`",
                str(summary.get("role", "")),
                markdownize_stage_markers(str(summary.get("default_stages", ""))),
                str(summary.get("domains", "")),
            ]
        )
    return render_markdown_table(headers, rows)


def render_seat_registry_stage_rules(contract: dict[str, object]) -> str:
    headers = ["席位", "策略/投资/商业/组织决策", "研究/实验/因果评估", "纯代码实施议题", "工程决策议题", "混合议题"]
    rows: list[list[str]] = []
    for _, config in iter_seats(contract):
        registry_stage_row = config.get("registry_stage_row")
        if not isinstance(registry_stage_row, dict):
            raise ValueError("seat missing registry_stage_row")
        rows.append(
            [
                str(registry_stage_row.get("seat", "")),
                markdownize_stage_markers(str(registry_stage_row.get("strategy_business_org", ""))),
                markdownize_stage_markers(str(registry_stage_row.get("research_eval", ""))),
                markdownize_stage_markers(str(registry_stage_row.get("pure_code_implementation", ""))),
                markdownize_stage_markers(str(registry_stage_row.get("engineering_decision", ""))),
                markdownize_stage_markers(str(registry_stage_row.get("hybrid", ""))),
            ]
        )
    return render_markdown_table(headers, rows)


def render_seat_registry_lopez_must_call(contract: dict[str, object]) -> str:
    entries: list[str] = []
    for seat_name, config in iter_seats(contract):
        dispatch = config.get("dispatch")
        if not isinstance(dispatch, dict):
            continue
        keywords = dispatch.get("must_call_keywords")
        if not isinstance(keywords, list) or not keywords:
            continue
        persona = expect_string(config.get("persona"), f"{seat_name}.persona")
        joined = " / ".join(str(keyword) for keyword in keywords)
        line = f"议题实质涉及 `{joined}` 所指的领域时，{persona} 必召开"
        note = dispatch.get("must_call_note")
        if isinstance(note, str) and note:
            line += f"，{note}"
        entries.append(line + "。")
    return "\n\n".join(entries)


def render_seat_registry_linus_dual_stage(contract: dict[str, object]) -> str:
    lines: list[str] = []
    for _, config in iter_seats(contract):
        dispatch = config.get("dispatch")
        if not isinstance(dispatch, dict):
            continue
        hints = dispatch.get("stage_hints")
        if not isinstance(hints, list) or not hints:
            continue
        lines.extend(f"- {hint}" for hint in hints)
    return "\n".join(lines)


def render_verdict_schema_layers(contract: dict[str, object]) -> str:
    verdict_schema = contract.get("verdict_schema")
    if not isinstance(verdict_schema, dict):
        raise ValueError("roundtable contract missing verdict_schema")
    layers = verdict_schema.get("layers")
    if not isinstance(layers, list):
        raise ValueError("roundtable contract missing verdict_schema.layers")
    return "\n".join(f"- `{layer}`" for layer in layers)


def render_verdict_schema_modes(contract: dict[str, object]) -> str:
    quick = contract["modes"]["quick-multi"]
    return (
        "- `roundtable`：按下述正式输出契约返回 verdict；实施另受阶段与用户授权约束。\n"
        f"- `quick-multi`：只返回不超过 {quick['max_characters']} 字的观点，不输出 verdict/YAML，不做 must_haves 审议，不实施。\n"
        "- 模式由主持人显式传入；Quick 的无 verdict 规则优先于正式模式的四层必填规则。"
    )


def render_verdict_schema_core_table(contract: dict[str, object]) -> str:
    verdict_schema = contract.get("verdict_schema")
    if not isinstance(verdict_schema, dict):
        raise ValueError("roundtable contract missing verdict_schema")

    route_space = verdict_schema.get("route_space")
    if not isinstance(route_space, list):
        raise ValueError("roundtable contract missing verdict_schema.route_space")

    core_seats: list[str] = []
    phases: set[int] = set()
    for _, config in iter_seats(contract):
        core_seat = config.get("core_seat")
        if isinstance(core_seat, str):
            core_seats.append(core_seat)
        for section in config["output_contract"]["sections"]:
            if section.get("schema_mode") != "phase_4_exception":
                phases.add(int(section["phase"]))
    seat_value = markdownize_literals(" / ".join([*core_seats, "新席位"]))
    route_value = markdownize_literals(" / ".join(str(route) for route in route_space))

    headers = ["字段", "取值", "作用"]
    rows = [
        ["`seat`", seat_value, "席位标识"],
        ["`phase`", " / ".join(f"`{phase}`" for phase in sorted(phases)), "评议阶段"],
        ["`route`", route_value, "主持人机读统一路由空间"],
        ["`seat_native_verdict`", "各席位原生 verdict", "保留人物 DNA"],
    ]
    for name, definition in verdict_schema["core_fields"].items():
        values = " / ".join(f"`{v}`" for v in definition.get("enum", [])) or f"`{definition['type']}`"
        rows.append([f"`{name}`", values, definition.get("description", name)])
    return render_markdown_table(headers, rows)


def render_verdict_schema_review_flags(contract: dict[str, object]) -> str:
    verdict_schema = contract.get("verdict_schema")
    if not isinstance(verdict_schema, dict):
        raise ValueError("roundtable contract missing verdict_schema")
    review_flags = verdict_schema.get("review_flags")
    if not isinstance(review_flags, list):
        raise ValueError("roundtable contract missing verdict_schema.review_flags")
    return "\n".join(f"- `{flag}`" for flag in review_flags)


def render_verdict_schema_seat_specific(contract: dict[str, object]) -> str:
    lines: list[str] = []
    for seat_name, config in iter_seats(contract):
        persona = expect_string(config.get("persona"), f"{seat_name}.persona")
        sections = config.get("output_contract", {}).get("sections")
        if not isinstance(sections, list) or not sections:
            raise ValueError(f"{seat_name}.output_contract.sections must be a non-empty list")
        for section in sections:
            if not isinstance(section, dict):
                continue
            if section.get("schema_mode") == "phase_4_exception":
                continue
            fields = expect_string_list(
                list(section.get("field_schemas", {})),
                f"{seat_name}.output_contract.sections[*].field_schemas",
            )
            heading = section.get("heading")
            label = (
                f"{persona} {heading}"
                if isinstance(heading, str) and heading
                else persona
            )
            joined = " / ".join(f"`{field}`" for field in fields)
            lines.append(f"- {label}: {joined}")
    return "\n".join(lines)


def render_verdict_schema_route_rules(contract: dict[str, object]) -> str:
    headers = ["席位", "native", "→ `core.route`"]
    rows: list[list[str]] = []
    for seat_name, config in iter_seats(contract):
        persona_label = expect_string(config.get("persona"), f"{seat_name}.persona")

        native_verdict_routes = config.get("native_verdict_routes")
        if not isinstance(native_verdict_routes, dict) or not native_verdict_routes:
            raise ValueError(f"{seat_name}.native_verdict_routes must be a non-empty object")

        for native, route_list in native_verdict_routes.items():
            native_key = expect_string(native, f"{seat_name}.native_verdict")
            routes = expect_string_list(route_list, f"{seat_name}.native_verdict_routes.{native_key}")
            rows.append(
                [
                    persona_label,
                    f"`{native_key}`",
                    " / ".join(f"`{route}`" for route in routes),
                ]
            )
    return render_markdown_table(headers, rows)


def render_verdict_schema_phase_4_exception(contract: dict[str, object]) -> str:
    sections = [section for _, seat in iter_seats(contract)
                for section in seat["output_contract"]["sections"]
                if section.get("schema_mode") == "phase_4_exception"]
    if len(sections) != 1:
        raise ValueError("expected one execution exception contract")
    section = sections[0]
    joined = " / ".join(f"`{field}`" for field in section["field_schemas"])
    return f"`{section['root_key']}` 是实施验证状态输出，不走共同 verdict schema。它保留自己的字段结构：{joined}。"


def render_route_targets(routes: list[str]) -> str:
    return " / ".join(f"`{route}`" for route in routes)


def render_shared_output_contract_section(
    seat_name: str,
    config: dict[str, object],
    section: dict[str, object],
) -> str:
    root_key = expect_string(section.get("root_key"), f"{seat_name}.output_contract.root_key")
    phase = expect_string(section.get("phase"), f"{seat_name}.output_contract.phase")
    core_seat = expect_string(config.get("core_seat"), f"{seat_name}.core_seat")

    native_verdict_routes = config.get("native_verdict_routes")
    if not isinstance(native_verdict_routes, dict) or not native_verdict_routes:
        raise ValueError(f"{seat_name}.native_verdict_routes must be a non-empty object")

    verdict_order = section.get("native_verdicts")
    if verdict_order is None:
        ordered_verdicts = [expect_string(key, f"{seat_name}.native_verdict") for key in native_verdict_routes]
    else:
        ordered_verdicts = expect_string_list(verdict_order, f"{seat_name}.output_contract.native_verdicts")

    lines: list[str] = []
    heading = section.get("heading")
    if isinstance(heading, str) and heading:
        lines.extend([f"### {heading}", ""])

    lines.append(f"- YAML root key：`{root_key}`")
    lines.append(f"- `core.seat`: `{core_seat}`")
    lines.append(f"- `core.phase`: `{phase}`")
    lines.append("- `core.seat_native_verdict`: " + " / ".join(f"`{verdict}`" for verdict in ordered_verdicts))
    lines.append("- route 映射：")

    for verdict in ordered_verdicts:
        routes = native_verdict_routes.get(verdict)
        lines.append(f"  - `{verdict}` → {render_route_targets(expect_string_list(routes, f'{seat_name}.native_verdict_routes.{verdict}'))}")

    for rule in config.get("conditional_routes", []):
        mode = rule.get("mode")
        if mode not in {"add", "override"}:
            raise ValueError(f"{seat_name}: conditional route requires add or override mode")
        when = rule["when"]
        condition = f"`{when['path']}` " + (f"= `{json.dumps(when['equals'], ensure_ascii=False)}`" if "equals" in when else "∈ {" + ", ".join(f"`{v}`" for v in when["enum"]) + "}")
        action = "覆盖原生映射，仅允许" if mode == "override" else "在原生映射上追加允许"
        lines.append(f"  - {condition} 时，{action} `{rule['route']}`（`{mode}`）")

    extra_route_lines = section.get("extra_route_lines")
    if extra_route_lines is not None:
        for route_line in expect_string_list(extra_route_lines, f"{seat_name}.output_contract.extra_route_lines"):
            lines.append(f"  - {route_line}")

    for note_key in ["must_haves_review_note", "must_haves_challenge_note"]:
        note = section.get(note_key)
        if note is not None:
            lines.append(f"- {expect_string(note, f'{seat_name}.output_contract.{note_key}')}")

    fields = expect_string_list(
        list(section.get("field_schemas", {})),
        f"{seat_name}.output_contract.sections[*].field_schemas",
    )
    lines.append("- `seat_specific` 必填字段：")
    for field in fields:
        lines.append(f"  - `{field}`")

    field_rules = section.get("field_rules")
    if field_rules is not None:
        for field_rule in expect_string_list(field_rules, f"{seat_name}.output_contract.field_rules"):
            lines.append(f"- {field_rule}")

    return "\n".join(lines)


def render_exception_output_contract_section(
    seat_name: str,
    config: dict[str, object],
    section: dict[str, object],
) -> str:
    root_key = expect_string(section.get("root_key"), f"{seat_name}.output_contract.root_key")
    fields = expect_string_list(
        list(section.get("field_schemas", {})),
        f"{seat_name}.output_contract.sections[*].field_schemas",
    )

    lines: list[str] = []
    heading = section.get("heading")
    if isinstance(heading, str) and heading:
        lines.extend([f"### {heading}", ""])

    lines.append(f"- YAML root key：`{root_key}`")
    intro_note = section.get("intro_note")
    if intro_note is not None:
        lines.append(f"- {expect_string(intro_note, f'{seat_name}.output_contract.intro_note')}")

    field_list_label = expect_string(
        section.get("field_list_label", "必填字段"),
        f"{seat_name}.output_contract.field_list_label",
    )
    lines.append(f"- {field_list_label}：")
    for field in fields:
        lines.append(f"  - `{field}`")

    field_rules = section.get("field_rules")
    if field_rules is not None:
        for field_rule in expect_string_list(field_rules, f"{seat_name}.output_contract.field_rules"):
            lines.append(f"- {field_rule}")

    return "\n".join(lines)


def render_seat_output_contract(contract: dict[str, object], seat_name: str) -> str:
    config = get_seat_config(contract, seat_name)
    output_contract = config.get("output_contract")
    if not isinstance(output_contract, dict):
        raise ValueError(f"{seat_name}.output_contract must be an object")

    shared_intro = expect_string(output_contract.get("shared_intro"), f"{seat_name}.output_contract.shared_intro")
    sections = output_contract.get("sections")
    if not isinstance(sections, list) or not sections:
        raise ValueError(f"{seat_name}.output_contract.sections must be a non-empty list")

    blocks = [render_verdict_schema_modes(contract), shared_intro]
    for section in sections:
        if not isinstance(section, dict):
            raise ValueError(f"{seat_name}.output_contract.sections must contain objects")
        schema_mode = section.get("schema_mode", "shared")
        if schema_mode == "shared":
            blocks.append(render_shared_output_contract_section(seat_name, config, section))
            continue
        if schema_mode == "phase_4_exception":
            blocks.append(render_exception_output_contract_section(seat_name, config, section))
            continue
        raise ValueError(f"{seat_name}.output_contract has unsupported schema_mode {schema_mode}")

    return "\n\n".join(blocks)


STATIC_BLOCK_RENDERERS = {
    "verdict_schema_modes": render_verdict_schema_modes,
    "seat_registry_current_seats": render_seat_registry_current_seats,
    "seat_registry_stage_rules": render_seat_registry_stage_rules,
    "seat_registry_lopez_must_call": render_seat_registry_lopez_must_call,
    "seat_registry_linus_dual_stage": render_seat_registry_linus_dual_stage,
    "verdict_schema_layers": render_verdict_schema_layers,
    "verdict_schema_core_table": render_verdict_schema_core_table,
    "verdict_schema_review_flags": render_verdict_schema_review_flags,
    "verdict_schema_seat_specific": render_verdict_schema_seat_specific,
    "verdict_schema_route_rules": render_verdict_schema_route_rules,
    "verdict_schema_phase_4_exception": render_verdict_schema_phase_4_exception,
}


def get_block_renderers(contract: dict[str, object]) -> dict[str, object]:
    renderers = dict(STATIC_BLOCK_RENDERERS)
    for seat_name, config in iter_seats(contract):
        block_name = get_seat_generated_block(config, seat_name=seat_name)
        if block_name in renderers:
            raise ValueError(f"duplicate generated block name: {block_name}")
        renderers[block_name] = (
            lambda current_contract, seat_name=seat_name: render_seat_output_contract(current_contract, seat_name)
        )
    return renderers


def replace_generated_block(text: str, block_name: str, body: str) -> str:
    start = f"<!-- GENERATED:{block_name}:start -->"
    end = f"<!-- GENERATED:{block_name}:end -->"
    pattern = re.compile(
        rf"{re.escape(start)}\n.*?\n{re.escape(end)}",
        re.DOTALL,
    )
    replacement = f"{start}\n{body.rstrip()}\n{end}"
    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise ValueError(f"missing generated block markers for {block_name}")
    return updated


def render_doc_text(relative_path: str, text: str, contract: dict[str, object]) -> str:
    block_names = get_generated_docs(contract).get(relative_path)
    if block_names is None:
        raise ValueError(f"unsupported generated doc: {relative_path}")

    block_renderers = get_block_renderers(contract)
    rendered = text
    for block_name in block_names:
        renderer = block_renderers.get(block_name)
        if renderer is None:
            raise ValueError(f"missing renderer for generated block: {block_name}")
        rendered = replace_generated_block(rendered, block_name, renderer(contract))
    return rendered


def format_toml_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ", ".join(format_toml_scalar(item) for item in value) + "]"
    raise TypeError(f"unsupported TOML scalar value: {value!r}")


def serialize_agent_toml(payload: dict[str, object]) -> str:
    """Serialize custom agent TOML with top-level scalars first, then [section] tables."""
    scalar_lines: list[str] = []
    table_blocks: list[str] = []

    for key, value in payload.items():
        if isinstance(value, dict):
            lines = [f"[{key}]"]
            for sub_key, sub_val in value.items():
                lines.append(f"{sub_key} = {format_toml_scalar(sub_val)}")
            table_blocks.append("\n".join(lines))
        elif key == "developer_instructions" and isinstance(value, str) and "'''" not in value and "\n" in value:
            body = value if value.endswith("\n") else value + "\n"
            scalar_lines.append(f"{key} = '''\n{body}'''")
        else:
            scalar_lines.append(f"{key} = {format_toml_scalar(value)}")

    sections = ["\n".join(scalar_lines)]
    sections.extend(table_blocks)
    rendered = "\n\n".join(section for section in sections if section) + "\n"
    tomllib.loads(rendered)
    return rendered


def render_claude_seat_adapter(seat_name: str, config: dict[str, object]) -> str:
    skill_name = expect_string(config.get("skill"), f"{seat_name}.skill")
    adapter = config.get("adapter")
    if not isinstance(adapter, dict):
        raise ValueError(f"{seat_name} missing adapter metadata")
    description = expect_string(adapter.get("description"), f"{seat_name}.adapter.description")
    color = expect_string(adapter.get("color"), f"{seat_name}.adapter.color")
    mode = expect_string(adapter.get("mode"), f"{seat_name}.adapter.mode")

    if mode == "implementation":
        tools_line = "tools: Read, Edit, Write, Bash, Grep, Glob"
        extra_guard_lines = ["maxTurns: 40"]
        action_clause = "按请求传入的 `mode` 与阶段执行（短读与阶段 1/2 全程只读；仅阶段 4 在锁定授权范围内实施与验证）"
    elif mode == "readonly":
        tools_line = "tools: Read, Grep, Glob"
        extra_guard_lines = [
            "disallowedTools: Write, Edit, Bash, NotebookEdit",
            "maxTurns: 16",
        ]
        action_clause = "按请求传入的 `mode` 执行严格只读评议（严禁修改文件或执行外部命令）"
    else:
        raise ValueError(f"{seat_name}.adapter.mode must be 'readonly' or 'implementation'")

    header_lines = [
        "---",
        f"name: {seat_name}",
        f"description: {json.dumps(description, ensure_ascii=False)}",
        tools_line,
        *extra_guard_lines,
        f"color: {color}",
        "---",
    ]
    body_lines = [
        f"用 Read 读取 `{{{{ZHUZI_SHARED_ROOT}}}}/seats/{seat_name}.md` 与 `{{{{ZHUZI_SKILL_ROOT}}}}/{skill_name}/PERSONA.md`，{action_clause}。仅当 `mode: roundtable` 需返回正式 verdict 时，再读 `{{{{ZHUZI_SHARED_ROOT}}}}/references/verdict-schema.md`。",
        f"- 源码开发且未安装时，改读 `./zhuzi/seats/{seat_name}.md` 与 `./skills/{skill_name}/SKILL.md`，正式输出查 `./zhuzi/references/verdict-schema.md`。",
    ]
    return "\n".join(header_lines) + "\n\n" + "\n".join(body_lines) + "\n"


def render_codex_seat_adapter(seat_name: str, config: dict[str, object]) -> str:
    skill_name = expect_string(config.get("skill"), f"{seat_name}.skill")
    adapter = config.get("adapter")
    if not isinstance(adapter, dict):
        raise ValueError(f"{seat_name} missing adapter metadata")
    description = expect_string(adapter.get("description"), f"{seat_name}.adapter.description")
    mode = expect_string(adapter.get("mode"), f"{seat_name}.adapter.mode")

    if mode == "implementation":
        action_clause = "按请求传入的 `mode` 与阶段执行（短读与阶段 1/2 全程只读；仅阶段 4 在锁定授权范围内实施与验证）"
        features: dict[str, object] = {"request_permissions_tool": False}
    elif mode == "readonly":
        action_clause = "按请求传入的 `mode` 执行严格只读评议（严禁修改文件或执行外部命令）"
        features = {"shell_tool": False, "request_permissions_tool": False}
    else:
        raise ValueError(f"{seat_name}.adapter.mode must be 'readonly' or 'implementation'")

    instructions = (
        f"读取 `{{{{ZHUZI_SHARED_ROOT}}}}/seats/{seat_name}.md` 与 `{{{{ZHUZI_SKILL_ROOT}}}}/{skill_name}/PERSONA.md`，{action_clause}。\n"
        f"仅当 `mode: roundtable` 需返回正式 verdict 时，再查 `{{{{ZHUZI_SHARED_ROOT}}}}/references/verdict-schema.md`。\n"
        f"- 源码开发且未安装时，改读 `./zhuzi/seats/{seat_name}.md` 与 `./skills/{skill_name}/SKILL.md`，正式输出查 `./zhuzi/references/verdict-schema.md`。\n"
    )
    payload: dict[str, object] = {
        "name": seat_name,
        "description": description,
        "developer_instructions": instructions,
        "features": features,
        "skills": {"include_instructions": False},
    }
    return serialize_agent_toml(payload)


def render_openai_sidecar(skill_entry: dict[str, object]) -> str:
    entry_name = expect_string(skill_entry.get("entry"), "skills[].entry")
    openai_meta = skill_entry.get("openai")
    if not isinstance(openai_meta, dict):
        raise ValueError(f"skill {entry_name} missing openai sidecar config")
    display_name = expect_string(openai_meta.get("display_name"), f"{entry_name}.openai.display_name")
    short_desc = expect_string(openai_meta.get("short_description"), f"{entry_name}.openai.short_description")
    default_prompt = expect_string(openai_meta.get("default_prompt"), f"{entry_name}.openai.default_prompt")
    implicit = bool(skill_entry.get("implicit_invocation", False))

    lines = [
        "interface:",
        f"  display_name: {json.dumps(display_name, ensure_ascii=False)}",
        f"  short_description: {json.dumps(short_desc, ensure_ascii=False)}",
        f"  default_prompt: {json.dumps(default_prompt, ensure_ascii=False)}",
        "",
        "policy:",
        f"  allow_implicit_invocation: {'true' if implicit else 'false'}",
        "",
    ]
    return "\n".join(lines)


def render_claude_skill_overlay(source_skill_md: str, skill_entry: dict[str, object]) -> str:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---[ \t]*\r?\n", source_skill_md, re.DOTALL)
    if not match:
        raise ValueError("source SKILL.md missing YAML frontmatter")
    fm_body = match.group(1).rstrip()
    rest = source_skill_md[match.end():]
    extra_lines: list[str] = []
    arg_hint = skill_entry.get("claude_argument_hint")
    if isinstance(arg_hint, str) and arg_hint:
        extra_lines.append(f"argument-hint: {json.dumps(arg_hint, ensure_ascii=False)}")
    if not bool(skill_entry.get("implicit_invocation", False)):
        extra_lines.append("disable-model-invocation: true")
    merged_fm = "\n".join([fm_body, *extra_lines])
    return f"---\n{merged_fm}\n---\n{rest}"


def render_inventory_markdown(surface: dict[str, object]) -> str:
    families = surface.get("families")
    if not isinstance(families, dict):
        raise ValueError("shipped surface missing families object")

    blocks = [
        "# zhuzi Shipped Surface Inventory",
        "",
        "> 人读清单由 `tools/render_roundtable_contract_docs.py` 从 `zhuzi/manifests/shipped-surface.json` 确定性生成；机器合同另见 `zhuzi/manifests/roundtable-contract.json`。",
    ]
    for label, key in INVENTORY_FAMILY_ORDER:
        entries = families.get(key, [])
        if not isinstance(entries, list):
            raise ValueError(f"shipped surface family {key} must be a list")
        blocks.append("")
        blocks.append(f"## {label} ({len(entries)} shipped)")
        blocks.append("")
        rows = [
            [
                f"`{expect_string(item.get('entry'), f'{key}[].entry')}`",
                f"`{expect_string(item.get('path'), f'{key}[].path')}`",
                expect_string(item.get("role"), f"{key}[].role"),
            ]
            for item in entries
            if isinstance(item, dict)
        ]
        blocks.append(render_markdown_table(["Entry", "Path", "Role"], rows))
    return "\n".join(blocks) + "\n"


def build_full_rendered_files(
    contract: dict[str, object],
    surface: dict[str, object],
) -> dict[str, str]:
    rendered_files: dict[str, str] = {}

    schema_relative = expect_string(
        contract["references"]["verdict_json_schema"],
        "references.verdict_json_schema",
    )
    rendered_files[schema_relative] = json.dumps(build_schema(contract), ensure_ascii=False, indent=2) + "\n"

    for seat_name, config in iter_seats(contract):
        rendered_files[f"runtimes/claude/agents/{seat_name}.md"] = render_claude_seat_adapter(seat_name, config)
        rendered_files[f"runtimes/codex/agents/{seat_name}.toml"] = render_codex_seat_adapter(seat_name, config)

    families = surface.get("families", {})
    if not isinstance(families, dict):
        raise ValueError("shipped surface missing families")
    skills_list = families.get("skills", [])
    if not isinstance(skills_list, list):
        raise ValueError("shipped surface skills must be a list")

    skills_by_entry: dict[str, dict[str, object]] = {}
    for item in skills_list:
        if isinstance(item, dict):
            entry_name = expect_string(item.get("entry"), "skills[].entry")
            skills_by_entry[entry_name] = item
            rendered_files[f"skills/{entry_name}/agents/openai.yaml"] = render_openai_sidecar(item)

    zhuzi_entry = skills_by_entry.get("zhuzi")
    if zhuzi_entry is None:
        raise ValueError("shipped surface skills missing zhuzi umbrella entry")
    zhuzi_source = (ROOT / "skills" / "zhuzi" / "SKILL.md").read_text(encoding="utf-8")
    rendered_files["runtimes/claude/skills/zhuzi/SKILL.md"] = render_claude_skill_overlay(zhuzi_source, zhuzi_entry)
    rendered_files["runtimes/claude/skills/zhuzi/references/routing.md"] = (
        ROOT / "skills" / "zhuzi" / "references" / "routing.md"
    ).read_text(encoding="utf-8")

    rendered_files[INVENTORY_PATH] = render_inventory_markdown(surface)
    return rendered_files


def render_docs(*, check: bool) -> int:
    contract = load_roundtable_contract()
    surface = load_shipped_surface()
    generated_docs = get_generated_docs(contract)
    stale: list[str] = []
    changed: list[str] = []

    for relative_path, expected_text in build_full_rendered_files(contract, surface).items():
        path = ROOT / relative_path
        if not path.exists() or path.read_text(encoding="utf-8") != expected_text:
            if check:
                stale.append(relative_path)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(expected_text, encoding="utf-8")
                changed.append(relative_path)

    for relative_path in generated_docs:
        path = ROOT / relative_path
        current_text = path.read_text(encoding="utf-8")
        rendered_text = render_doc_text(relative_path, current_text, contract)
        if current_text == rendered_text:
            continue
        if check:
            stale.append(relative_path)
            continue
        path.write_text(rendered_text, encoding="utf-8")
        changed.append(relative_path)

    if check:
        if stale:
            print("Roundtable contract & adapter outputs are stale:")
            for relative_path in stale:
                print(f"  - {relative_path}")
            print("Run: python3 tools/render_roundtable_contract_docs.py")
            return 1
        print("Roundtable contract docs are up to date.")
        return 0

    if changed:
        print("Updated roundtable contract & adapter outputs:")
        for relative_path in changed:
            print(f"  + {relative_path}")
    else:
        print("Roundtable contract docs already up to date.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if generated doc blocks or adapters are stale",
    )
    args = parser.parse_args()
    return render_docs(check=args.check)


if __name__ == "__main__":
    sys.exit(main())
