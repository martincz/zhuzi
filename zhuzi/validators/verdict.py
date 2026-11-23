#!/usr/bin/env python3
"""Build and validate verdict contracts from the single roundtable manifest."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path


SHARED_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = SHARED_ROOT / "manifests" / "roundtable-contract.json"


def object_schema(properties: dict, required: list[str] | None = None) -> dict:
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else required,
            "additionalProperties": False}


def route_condition(rule: dict) -> dict:
    if rule.get("mode") not in {"add", "override"}:
        raise ValueError("conditional route requires mode add or override")
    when = rule["when"]
    if "equals" in when:
        condition = {"const": when["equals"]}
    elif "enum" in when:
        condition = {"enum": when["enum"]}
    else:
        raise ValueError("conditional route requires equals or enum")
    for key in reversed(when["path"].split(".")):
        condition = {"type": "object", "required": [key], "properties": {key: condition}}
    return condition


def allowed_routes(seat: dict, body: dict) -> set[str]:
    allowed = set(seat["native_verdict_routes"][body["core"]["seat_native_verdict"]])
    overrides = []
    for rule in seat.get("conditional_routes", []):
        route_condition(rule)  # Reject unknown operations even on an inactive condition.
        when = rule["when"]
        value = _lookup(body, when["path"])
        matched = value == when["equals"] if "equals" in when else value in when["enum"]
        if matched:
            if rule["mode"] == "override":
                overrides.append({rule["route"]})
            else:
                allowed.add(rule["route"])
    # Conflicting mandatory conditions fail closed; later additions cannot relax them.
    return set.intersection(*overrides) if overrides else allowed


def build_schema(contract: dict) -> dict:
    """Render Draft 2020-12; field names, types and routes come from the manifest."""
    variants = []
    common = contract["verdict_schema"]
    review_item = copy.deepcopy(common["review_item"])
    review_item["properties"]["flag"]["enum"] = common["review_flags"]
    for seat_name, seat in contract["seats"].items():
        for section in seat["output_contract"]["sections"]:
            root = section["root_key"]
            if section.get("schema_mode") == "phase_4_exception":
                body = object_schema(section["field_schemas"])
            else:
                phase = int(section["phase"])
                core = object_schema({
                    "seat": {"const": seat["core_seat"]}, "phase": {"const": phase},
                    "route": {"enum": common["route_space"]},
                    "seat_native_verdict": {"enum": list(seat["native_verdict_routes"])},
                    **common["core_fields"],
                })
                body = object_schema({
                    "core": core,
                    "must_haves_review": {"type": "array", "items": review_item},
                    "must_haves_challenge": common["challenge"],
                    "seat_specific": object_schema(section["field_schemas"]),
                })
                conditions = []
                for rule in seat.get("conditional_routes", []):
                    condition = route_condition(rule)
                    if rule["mode"] == "override":
                        conditions.append({"if": condition, "then": {"properties": {
                            "core": {"properties": {"route": {"const": rule["route"]}}}}}})
                if conditions:
                    body["allOf"] = conditions
            variants.append(object_schema({root: body}))
    return {"$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "zhuzi roundtable verdict", "oneOf": variants}


def _lookup(value: dict, path: str):
    for key in path.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def validate_verdict(payload, *, contract: dict, seat_name: str, phase: int,
                     truth_count: int, must_haves: dict | None = None,
                     peer_context: bool = False) -> list[str]:
    """Validate shape plus cross-field/coverage invariants; never repair a verdict."""
    from jsonschema import Draft202012Validator

    if truth_count < 1:
        return ["truth_count must be positive"]
    seat = contract["seats"].get(seat_name)
    if seat is None:
        return [f"unknown seat: {seat_name}"]
    sections = [s for s in seat["output_contract"]["sections"]
                if int(s.get("phase", 4 if s.get("schema_mode") == "phase_4_exception" else -1)) == phase]
    if not sections:
        return [f"seat {seat_name} does not support phase {phase}"]
    section = sections[0]
    schema = build_schema(contract)
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    if errors:
        # The manifest-derived union covers all seats. Keep useful leaf errors
        # from this seat's variant rather than flooding logs with other seats.
        expected_root = section["root_key"]
        variant = next(v for v in schema["oneOf"]
                       if expected_root in v["properties"] and
                       (phase == 4 or v["properties"][expected_root].get("properties", {}).get("core", {}).get("properties", {}).get("phase", {}).get("const") == phase))
        return [f"{'/'.join(map(str, e.absolute_path)) or '$'}: {e.message}"
                for e in Draft202012Validator(variant).iter_errors(payload)] or ["verdict does not match the manifest schema"]
    root = section["root_key"]
    if root not in payload:
        return [f"expected root {root}"]
    body = payload[root]
    expected = set(range(1, truth_count + 1))
    if phase == 4:
        if must_haves is None:
            return ["phase 4 validation requires the locked must_haves"]
        locked_errors = validate_must_haves(must_haves)
        if locked_errors or len(must_haves["truths"]) != truth_count:
            return ["invalid or mismatched locked must_haves", *locked_errors]
        attempts = body["verification_attempted"]
        ids = [item["truth"] for item in attempts]
        if set(ids) != expected:
            errors.append("verification_attempted must cover every truth without unknown IDs")
        if body["status"] == "done":
            if not body["decisions_honored"] or body["out_of_scope_touched"]:
                errors.append("done requires honored decisions and no out-of-scope changes")
            if any(item["result"] != "passed" for item in attempts) or body["gaps_to_route_back"]:
                errors.append("done requires all verifications passed and no unresolved gaps")
        if must_haves is not None:
            commands = {(v["truth"], v["cmd"]) for v in must_haves["verify_commands"]}
            attempted = {(v["truth"], v["cmd"]) for v in attempts}
            if commands != attempted:
                errors.append("verification commands differ from the locked must_haves")
        return errors

    core = body["core"]
    if core["seat"] != seat["core_seat"] or core["phase"] != phase:
        errors.append("verdict seat/phase does not match the dispatched request")
    allowed = allowed_routes(seat, body)
    if core["route"] not in allowed:
        errors.append("route contradicts native verdict or its conditional mapping")
    ids = [item["truth"] for item in body["must_haves_review"]]
    if set(ids) != expected or len(ids) != truth_count:
        errors.append("must_haves_review must cover each truth exactly once")
    challenge = body["must_haves_challenge"]
    challenged = set(challenge["challenged_truths"])
    revisions = {r["truth_id"] for r in challenge["proposed_revision"]}
    if not challenged <= expected or not revisions <= expected:
        errors.append("challenge references an unknown truth")
    if challenge["triggered"]:
        if not challenged or not challenge["fundamental_issue"].strip() or revisions != challenged:
            errors.append("triggered challenge requires an issue and a revision for each challenged truth")
        if core["route"] not in {"revise_must_haves", "kill", "too_hard"}:
            errors.append("unresolved challenge cannot route to go or go_with_conditions")
    elif challenged or challenge["proposed_revision"]:
        errors.append("inactive challenge cannot contain challenged truths or revisions")
    if core["route"] == "revise_must_haves" and not challenge["triggered"]:
        errors.append("revise_must_haves requires a triggered challenge")
    if core["route"] == "go" and core["hard_blockers"]:
        errors.append("go cannot contain unresolved hard blockers")
    if core["peer_disagreements"] and phase == 1 and not peer_context:
        errors.append("blind first-round verdict cannot claim observed peer disagreements")
    return errors


def validate_must_haves(payload) -> list[str]:
    """Block implementation when commands or pass criteria are still unresolved."""
    if not isinstance(payload, dict):
        return ["must_haves must be an object"]
    truths = payload.get("truths")
    if not isinstance(truths, list) or not 1 <= len(truths) <= 5 or any(not isinstance(t, str) or not t.strip() for t in truths):
        return ["must_haves requires 1-5 non-empty truths"]
    commands = payload.get("verify_commands")
    if not isinstance(commands, list) or not commands:
        return ["verify_commands must be a non-empty array"]
    errors = []
    ids = []
    for item in commands:
        if not isinstance(item, dict) or type(item.get("truth")) is not int:
            errors.append("verification command requires an integer truth ID")
            continue
        ids.append(item["truth"])
        for field in ("cmd", "pass_criterion"):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip() or any(token in value.upper() for token in ("TBD", "TODO", "待定", "待确认")):
                errors.append(f"truth {item['truth']}: unresolved {field}")
    if set(ids) != set(range(1, len(truths) + 1)):
        errors.append("verify_commands must cover all truths without unknown IDs")
    return errors


def load_payload(path: Path):
    text = sys.stdin.read() if path == Path("-") else path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        import yaml

        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ValueError("input is not valid JSON or YAML") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="JSON or YAML input file, or - for stdin")
    parser.add_argument("--seat")
    parser.add_argument("--phase", type=int, choices=(1, 2, 4), default=1)
    parser.add_argument("--truth-count", type=int)
    parser.add_argument("--must-haves", type=Path)
    parser.add_argument("--peer-context", action="store_true", help="only when actual peer verdicts were supplied for a follow-up review")
    args = parser.parse_args()
    if args.file == args.must_haves == Path("-"):
        parser.error("verdict and locked must_haves cannot both read from stdin")
    try:
        payload = load_payload(args.file)
        if args.seat:
            if args.truth_count is None:
                parser.error("--seat requires --truth-count")
            locked = load_payload(args.must_haves) if args.must_haves else None
            if isinstance(locked, dict):
                locked = locked.get("must_haves", locked)
            errors = validate_verdict(payload, contract=json.loads(MANIFEST.read_text()),
                                      seat_name=args.seat, phase=args.phase,
                                      truth_count=args.truth_count, must_haves=locked,
                                      peer_context=args.peer_context)
        else:
            errors = validate_must_haves(payload.get("must_haves", payload) if isinstance(payload, dict) else payload)
    except (ValueError, KeyError, OSError, ImportError) as exc:
        print(f"Validation failed: {exc}")
        return 1
    if errors:
        print("Validation failed:\n" + "\n".join(f"- {e}" for e in errors))
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
