#!/usr/bin/env python3
"""Render roundtable contract docs from the structured contract manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from zhuzi.validators.verdict import build_schema
ROUNDTABLE_CONTRACT_PATH = ROOT / "zhuzi" / "manifests" / "roundtable-contract.json"

SEAT_REGISTRY_PATH = "zhuzi/references/seat-registry.md"
VERDICT_SCHEMA_PATH = "zhuzi/references/verdict-schema.md"

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


def load_roundtable_contract(path: Path = ROUNDTABLE_CONTRACT_PATH) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"roundtable contract must be a JSON object: {path}")
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


def render_docs(*, check: bool) -> int:
    contract = load_roundtable_contract()
    generated_docs = get_generated_docs(contract)
    stale: list[str] = []
    changed: list[str] = []

    schema_relative = contract["references"]["verdict_json_schema"]
    schema_path = ROOT / schema_relative
    schema_text = json.dumps(build_schema(contract), ensure_ascii=False, indent=2) + "\n"
    if not schema_path.exists() or schema_path.read_text(encoding="utf-8") != schema_text:
        if check:
            stale.append(schema_relative)
        else:
            schema_path.parent.mkdir(parents=True, exist_ok=True)
            schema_path.write_text(schema_text, encoding="utf-8")
            changed.append(schema_relative)

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
            print("Roundtable contract docs are stale:")
            for relative_path in stale:
                print(f"  - {relative_path}")
            print("Run: python3 tools/render_roundtable_contract_docs.py")
            return 1
        print("Roundtable contract docs are up to date.")
        return 0

    if changed:
        print("Updated roundtable contract docs:")
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
        help="fail if generated doc blocks are stale",
    )
    args = parser.parse_args()
    return render_docs(check=args.check)


if __name__ == "__main__":
    sys.exit(main())
