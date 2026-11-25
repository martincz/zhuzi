#!/usr/bin/env python3
"""Isolated dual-runtime installation purity checks and live invocation/continuation probe."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from install_codex_source_adapters import load_manifest_families, tomllib
from render_roundtable_contract_docs import load_roundtable_contract

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from zhuzi.validators.verdict import validate_verdict


class SmokeFailure(RuntimeError):
    pass


def build_install_env(*, codex_home: Path, claude_dir: Path) -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        CODEX_HOME=str(codex_home),
        CLAUDE_DIR=str(claude_dir),
        CODEX_SKILL_DIR=str(codex_home / "skills"),
        PYTHONDONTWRITEBYTECODE="1",
    )
    return env


def refresh_shipped_assets(*, install_env: dict[str, str]) -> None:
    result = subprocess.run(
        ["bash", "install.sh"],
        cwd=ROOT,
        env=install_env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise SmokeFailure(f"isolated installation failed: {result.stderr[-2000:]}")


def validate_rendered_paths(path: Path, install_root: Path, text: str) -> None:
    if "{{ZHUZI_" in text or "`./skills/" in text or "`./zhuzi" in text or "$HOME/" in text:
        raise SmokeFailure(f"unresolved installed adapter path: {path}")
    references = re.findall(r"`(/[^`\n]+\.(?:md|json))`", text)
    if not references:
        raise SmokeFailure(f"installed adapter has no concrete references: {path}")
    root = install_root.resolve()
    for target in references:
        resolved = Path(target).resolve()
        if not resolved.is_file() or not resolved.is_relative_to(root):
            raise SmokeFailure(f"missing or non-isolated reference in {path.name}: {target}")


def validate_installed_skill_bundle(skill_root: Path, *, runtime: str) -> None:
    top_dirs = sorted(p.name for p in skill_root.iterdir() if p.is_dir())
    if top_dirs != ["zhuzi"]:
        raise SmokeFailure(f"{runtime} default install must create only 'zhuzi' under {skill_root}, got {top_dirs}")

    zhuzi_dir = skill_root / "zhuzi"
    skill_mds = [p.relative_to(zhuzi_dir).as_posix() for p in zhuzi_dir.rglob("SKILL.md")]
    if skill_mds != ["SKILL.md"]:
        raise SmokeFailure(f"{runtime} zhuzi bundle must contain exactly one SKILL.md, got {skill_mds}")

    banned_names = {"upgrade-notes.md", "verification-report.md", "synthesis.md"}
    for item in zhuzi_dir.rglob("*"):
        if item.is_dir():
            if item.name in {"research", "sources", "__pycache__"} or not any(item.iterdir()):
                raise SmokeFailure(f"non-runtime or empty directory leaked into {runtime} bundle: {item}")
        elif item.is_file():
            if item.name in banned_names or item.name.endswith((":Zone.Identifier", ".pyc")):
                raise SmokeFailure(f"non-runtime draft leaked into {runtime} bundle: {item}")


def validate_path_references(*, codex_home: Path, claude_dir: Path | None = None) -> None:
    contract = load_roundtable_contract()
    shipped = load_manifest_families()

    codex_skill_root = codex_home / "skills"
    validate_installed_skill_bundle(codex_skill_root, runtime="codex")
    codex_zhuzi_md = codex_skill_root / "zhuzi" / "SKILL.md"
    validate_rendered_paths(codex_zhuzi_md, codex_home, codex_zhuzi_md.read_text(encoding="utf-8"))
    if not (codex_skill_root / "zhuzi" / "agents" / "openai.yaml").is_file():
        raise SmokeFailure("Codex zhuzi skill bundle missing agents/openai.yaml")

    allowed_keys = {"name", "description", "developer_instructions", "features", "skills"}
    for seat in contract["seats"]:
        path = codex_home / "agents" / f"{seat}.toml"
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
        if payload.get("name") != seat or not set(payload).issubset(allowed_keys):
            raise SmokeFailure(f"invalid native agent: {seat}")
        if payload.get("skills", {}).get("include_instructions") is not False:
            raise SmokeFailure(f"Codex agent missing skills.include_instructions=false: {seat}")
        if seat != "linus-engineer" and payload.get("features", {}).get("shell_tool") is not False:
            raise SmokeFailure(f"Codex reviewer seat must disable shell_tool: {seat}")
        validate_rendered_paths(path, codex_home, payload["developer_instructions"])

    if list((codex_home / "agents").glob("*.md")):
        raise SmokeFailure("legacy Markdown agents remain in isolated installation")

    if claude_dir is not None:
        if (claude_dir / "commands" / "zhuzi").exists():
            raise SmokeFailure("legacy .claude/commands/zhuzi remains in Claude installation")
        validate_installed_skill_bundle(claude_dir / "skills", runtime="claude")
        claude_zhuzi_md = claude_dir / "skills" / "zhuzi" / "SKILL.md"
        claude_zhuzi_text = claude_zhuzi_md.read_text(encoding="utf-8")
        if "disable-model-invocation: true" not in claude_zhuzi_text:
            raise SmokeFailure("Claude zhuzi skill missing disable-model-invocation: true")
        validate_rendered_paths(claude_zhuzi_md, claude_dir, claude_zhuzi_text)
        for entry in shipped["agents"]:
            path = claude_dir / "agents" / Path(str(entry["path"])).name
            validate_rendered_paths(path, claude_dir, path.read_text(encoding="utf-8"))


def inherit_provider_config(*, source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for name in ("config.toml", "auth.json"):
        path = source / name
        if path.is_file():
            shutil.copy2(path, target / name)


def probe_overrides(codex_home: Path) -> list[str]:
    """A wiring test needs neither external MCP startup nor expensive reasoning."""
    overrides = ["-c", 'model_reasoning_effort="low"']
    path = codex_home / "config.toml"
    config = tomllib.loads(path.read_text()) if path.exists() else {}
    for name in config.get("mcp_servers", {}):
        overrides.extend(["-c", f"mcp_servers.{name}.enabled=false"])
    return overrides


def event_summary(stdout) -> list[dict]:
    if isinstance(stdout, bytes):
        stdout = stdout.decode(errors="replace")
    events = []
    for line in (stdout or "").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item", {})
        events.append({"event": event.get("type"), "item": item.get("type"), "tool": item.get("tool"), "status": item.get("status")})
    return events[-12:]


def snapshot(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob("*") if p.is_file()}


def _output(value):
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _instant(value):
    from datetime import datetime
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def read_session_evidence(codex_home: Path) -> dict:
    """Read this install's runtime logs and identify each rollout's owner."""
    threads, calls = {}, []
    for path in sorted((codex_home / "sessions").rglob("*.jsonl")):
        records = []
        for line in path.read_text(errors="replace").splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict) and isinstance(record.get("payload"), dict):
                records.append(record)
        meta = next((r["payload"] for r in records if r.get("type") == "session_meta"), {})
        owner = meta.get("id")
        parent = meta.get("parent_thread_id")
        spawn = meta.get("source", {})
        spawn = spawn.get("subagent", {}).get("thread_spawn", {}) if isinstance(spawn, dict) else {}
        thread = {
            "id": owner,
            "parent_id": parent or spawn.get("parent_thread_id"),
            "agent_path": meta.get("agent_path") or spawn.get("agent_path"),
            "agent_role": meta.get("agent_role") or spawn.get("agent_role"),
            "cwd": meta.get("cwd"),
            "messages": [],
            "activities": [],
            "configurations": [],
        }
        pending, outputs, completions, aborted, own_turns = {}, {}, {}, set(), set()
        for r in records:
            v = r["payload"]
            stamp = _instant(r.get("timestamp"))
            if r.get("type") == "response_item":
                call_id = v.get("call_id")
                name = v.get("name", "").split(".")[-1].split("__")[-1]
                if v.get("type") == "function_call" and call_id and name in {"spawn_agent", "send_input", "followup_task", "resume_agent"}:
                    try:
                        arguments = json.loads(v.get("arguments", "{}"))
                    except (ValueError, TypeError):
                        continue
                    if isinstance(arguments, dict):
                        pending[call_id] = {
                            "call_id": call_id,
                            "owner_thread_id": owner,
                            "tool": name,
                            "arguments": arguments,
                            "timestamp": stamp,
                        }
                elif v.get("type") == "function_call_output" and call_id:
                    outputs[call_id] = _output(v.get("output"))
            if r.get("type") != "event_msg":
                continue
            if v.get("type") == "item_completed" and owner and v.get("thread_id") == owner:
                item = v.get("item", {})
                turn = v.get("turn_id")
                if turn:
                    own_turns.add(turn)
                if item.get("type") == "SubAgentActivity":
                    thread["activities"].append({**item, "timestamp": stamp})
                if item.get("type") == "AgentMessage" and item.get("phase") in {"final", "final_answer"}:
                    content = item.get("content", [])
                    message = "".join(
                        part.get("text", "")
                        for part in content
                        if isinstance(part, dict) and part.get("type") in {"Text", "text", "output_text"}
                    )
                    thread["messages"].append({"turn_id": turn, "text": message, "timestamp": stamp})
            if v.get("type") == "thread_settings_applied" and owner and v.get("thread_id") == owner:
                settings = v.get("thread_settings", {})
                thread["configurations"].append(
                    {"model": settings.get("model"), "reasoning_effort": settings.get("reasoning_effort"), "source": "thread_settings_applied"}
                )
            if v.get("type") == "task_complete":
                completions[v.get("turn_id")] = v.get("last_agent_message")
            if v.get("type") in {"turn_aborted", "turn_failed", "task_failed"}:
                aborted.add(v.get("turn_id"))
        for r in records:
            v = r["payload"]
            if r.get("type") == "turn_context" and v.get("turn_id") in own_turns:
                thread["configurations"].append(
                    {"model": v.get("model"), "reasoning_effort": v.get("effort", v.get("model_reasoning_effort")), "source": "turn_context", "turn_id": v.get("turn_id")}
                )
        for message in thread["messages"]:
            turn = message["turn_id"]
            message["completed"] = turn in completions and turn not in aborted and completions[turn] == message["text"]
        calls.extend({**call, "output": outputs[call_id], "status": "returned"} for call_id, call in pending.items() if call_id in outputs)
        if owner:
            if owner in threads:
                raise SmokeFailure(f"duplicate rollout owner: {owner}")
            threads[owner] = thread
    return {"threads": threads, "calls": calls}


def session_tool_calls(codex_home: Path) -> list[dict]:
    return read_session_evidence(codex_home)["calls"]


def _tool_error(call):
    if call.get("status") not in {"completed", "returned", "success"}:
        return "tool did not return successfully"
    value = _output(call.get("output"))
    if not isinstance(value, (str, dict, type(None))):
        return "unsupported tool result"
    if isinstance(value, str) and value.strip():
        return "unstructured tool error or unsupported result"
    if isinstance(value, dict) and (
        value.get("error") is not None
        or value.get("isError")
        or value.get("status") in {"failed", "error", "aborted", "cancelled", "not_found"}
    ):
        return "tool returned an error"
    return None


def _target(arguments):
    values = {arguments[k] for k in ("target", "id", "agent_id") if isinstance(arguments.get(k), str) and arguments[k]}
    return next(iter(values)) if len(values) == 1 else None


def _json_verdict(text):
    text = text.strip()
    fenced = re.fullmatch(r"```(?:json|yaml)?\s*\n(.*?)\n```", text, re.S)
    try:
        return json.loads(fenced.group(1) if fenced else text)
    except (ValueError, TypeError):
        return None


def validate_live_result(result: dict, events: list[dict], *, codex_home: Path, raw_calls: list[dict] | None = None) -> None:
    contract = load_roundtable_contract()
    expected = {"feynman-reviewer": 1, "linus-engineer": 2}
    records = result.get("results", [])
    if {(r.get("seat"), r.get("phase")) for r in records} != set(expected.items()) or len(records) != 2:
        raise SmokeFailure("live probe did not return both requested seats")
    if result.get("skill_loaded") is not True or result.get("workflow_path") != str(codex_home / "zhuzi/workflows/roundtable.md"):
        raise SmokeFailure("live probe did not load isolated orchestrator skill")
    evidence = read_session_evidence(codex_home)
    threads = evidence["threads"]
    roots = [t for t in threads.values() if not t["parent_id"]]
    if len(roots) != 1:
        raise SmokeFailure("missing actual spawn/continuation thread evidence")
    root = roots[0]
    calls = [c for c in evidence["calls"] if c["owner_thread_id"] == root["id"]]
    spawns = [c for c in calls if c["tool"] == "spawn_agent"]
    if len(spawns) != 2:
        raise SmokeFailure("expected exactly two actual native spawn calls")
    bound = {}
    for call in spawns:
        if _tool_error(call):
            raise SmokeFailure("native spawn tool failed")
        seat = call["arguments"].get("agent_type")
        if seat not in expected or seat in bound:
            raise SmokeFailure("spawn agent_type is not the requested native seat")
        output = call["output"]
        if not isinstance(output, dict):
            raise SmokeFailure("spawn did not return a structured agent handle")
        handle = output.get("agent_id") or output.get("task_name")
        children = [
            t
            for t in threads.values()
            if handle and handle in {t["id"], t["agent_path"]} and t["parent_id"] == root["id"] and t["agent_role"] == seat
        ]
        if len(children) != 1:
            raise SmokeFailure("spawn handle does not identify the expected native child thread")
        child = children[0]
        activity = [
            a
            for a in root["activities"]
            if a.get("id") == call["call_id"]
            and a.get("kind") == "started"
            and a.get("agent_thread_id") == child["id"]
            and a.get("status") not in {"failed", "error", "aborted", "cancelled"}
        ]
        if not activity:
            raise SmokeFailure("native child start was not confirmed by the runtime")
        report = next(r for r in records if r["seat"] == seat)
        verdict = json.loads(report["verdict_json"])
        errors = validate_verdict(verdict, contract=contract, seat_name=seat, phase=expected[seat], truth_count=1)
        if errors:
            raise SmokeFailure(f"{seat} invalid verdict: {errors}")
        originals = [
            m
            for m in child["messages"]
            if m["completed"]
            and m["timestamp"] is not None
            and call["timestamp"] is not None
            and m["timestamp"] >= call["timestamp"]
            and json.dumps(_json_verdict(m["text"]), sort_keys=True) == json.dumps(verdict, sort_keys=True)
        ]
        if not originals:
            raise SmokeFailure("reported verdict is not a completed reply from that child")
        bound[seat] = (child, handle, originals[0])
    child, handle, original = bound["linus-engineer"]
    aliases = {child["id"], child["agent_path"], handle}
    reported_id = result.get("continuation_agent_id")
    if not reported_id or reported_id not in aliases:
        raise SmokeFailure("reported continuation handle does not exactly identify Linus")
    for call in calls:
        if call["tool"] not in {"send_input", "followup_task"} or _target(call["arguments"]) not in aliases:
            continue
        if _tool_error(call) or any(h.get("call_id") == call["call_id"] and _tool_error(h) for h in raw_calls or []):
            continue
        interactions = [
            a
            for a in root["activities"]
            if a.get("id") == call["call_id"]
            and a.get("kind") == "interacted"
            and a.get("agent_thread_id") == child["id"]
            and a.get("status") not in {"failed", "error"}
        ]
        if not interactions or call["timestamp"] is None:
            continue
        for reply in child["messages"]:
            if (
                reply["completed"]
                and reply["turn_id"] != original["turn_id"]
                and reply["timestamp"] is not None
                and reply["timestamp"] > call["timestamp"]
                and re.match(r"^CONTINUE_OK(?:\b|[：:])", reply["text"].strip())
                and reply["text"].strip() == result.get("continuation_message", "").strip()
            ):
                return
    raise SmokeFailure("no successful continuation with a completed reply from the same Linus thread")


def run_codex_probe(codex_bin: str, *, codex_home: Path, install_env: dict[str, str], workspace: Path, trace_dir: Path | None = None) -> None:
    (workspace / ".agents").mkdir()
    (workspace / ".agents/skills").symlink_to(codex_home / "skills", target_is_directory=True)
    (workspace / "app.py").write_text('def add(a, b):\n    """返回 a 与 b 的和。"""\n    return a + b\n')
    (workspace / "AGENTS.md").write_text("这是运行时验收 fixture。只读，不修改、不提交；允许调用已安装的具名圆桌席位。\n")
    props = {
        "skill_loaded": {"type": "boolean"},
        "workflow_path": {"type": "string"},
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {"seat": {"type": "string"}, "phase": {"type": "integer"}, "verdict_json": {"type": "string"}},
                "required": ["seat", "phase", "verdict_json"],
            },
        },
        "continuation_agent_id": {"type": "string"},
        "continuation_message": {"type": "string"},
    }
    schema_file = codex_home / "probe-response.schema.json"
    schema_file.write_text(json.dumps({"type": "object", "properties": props, "required": list(props), "additionalProperties": False}))
    output = codex_home / "probe-result.json"
    prompt = """使用 $zhuzi roundtable 做只读接线验收。先读取已安装的 $zhuzi 入口 skill、workflow 和共享 schema。
这是显式授权的测试，不执行完整圆桌决策或实施；本题只验收已指定的两席和续跑，不测试自动选席。
议题：检查当前 app.py 的 add 接口与文档是否一致。
已接受的 must_haves：truths=['add(2,3) 返回 5，文档与行为一致']；verify_commands=[{truth:1,cmd:'python3 -c "import app; assert app.add(2,3)==5"',pass_criterion:'退出码为 0'}]。
调用具名自定义席位 feynman-reviewer（phase 1）与 linus-engineer（phase 2），各传 mode: roundtable、议题、完整合同、对应阶段以及源码路径。按运行时容量调度。
要求席位按共享 schema 返回完整 JSON verdict，含 evidence、missing_evidence；首轮 peer_disagreements 为空。不修改文件。
收到 Linus 后保留他的实际 agent ID，调用当前运行时可唤醒已有 agent 的续跑工具，要求他不改文件、只返回 CONTINUE_OK 并复述自己上轮对 app.py/add 的具体结论。不得用新 agent 代替续跑。
只输出 response schema 指定的 JSON。results 的 verdict_json 是每席实际返回的完整 JSON 字符串，不改写判断。continuation_message 使用续跑原文。工具或席位不可用时如实失败，不伪造调用。"""
    before = snapshot(workspace)
    print("Live smoke: starting two native seats and same-agent continuation (low reasoning; MCP disabled).", flush=True)
    try:
        proc = subprocess.run(
            [
                codex_bin,
                "exec",
                "-C",
                str(workspace),
                "--skip-git-repo-check",
                "--ignore-rules",
                "--sandbox",
                "read-only",
                "--json",
                "--output-schema",
                str(schema_file),
                "-o",
                str(output),
                *probe_overrides(codex_home),
                prompt,
            ],
            env=install_env,
            stdin=subprocess.DEVNULL,
            text=True,
            capture_output=True,
            timeout=360,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        if trace_dir is not None:
            trace_dir.mkdir(parents=True, exist_ok=True)
            stdout = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else exc.stdout or ""
            (trace_dir / "events.jsonl").write_text(stdout)
        raise SmokeFailure(f"live probe timed out after 360 seconds; last events: {event_summary(exc.stdout)}") from exc
    if trace_dir is not None:
        trace_dir.mkdir(parents=True, exist_ok=True)
        (trace_dir / "events.jsonl").write_text(proc.stdout)
        if output.exists():
            shutil.copy2(output, trace_dir / "result.json")
        (trace_dir / "collaboration.json").write_text(json.dumps(session_tool_calls(codex_home), ensure_ascii=False, indent=2))
        (trace_dir / "session-evidence.json").write_text(json.dumps(read_session_evidence(codex_home), ensure_ascii=False, indent=2))
    if snapshot(workspace) != before:
        raise SmokeFailure("live probe modified read-only fixture")
    if proc.returncode or not output.exists():
        failures = []
        for line in proc.stdout.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") in {"error", "turn.failed"}:
                failures.append(event.get("message") or event.get("error", {}).get("message"))
        raise SmokeFailure(f"codex exec failed (exit={proc.returncode}): {failures}; {proc.stderr[-1000:]}")
    events = []
    for line in proc.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    raw_calls = session_tool_calls(codex_home)
    validate_live_result(json.loads(output.read_text()), events, codex_home=codex_home, raw_calls=raw_calls)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="installation/path checks only; no model calls")
    parser.add_argument("--trace-dir", type=Path, help="save model events/results for debugging; never copies provider credentials")
    args = parser.parse_args()
    try:
        source_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        with tempfile.TemporaryDirectory(prefix="zhuzi-smoke-") as raw:
            root = Path(raw)
            codex_home = root / "codex home"
            claude_dir = root / "claude home"
            env = build_install_env(codex_home=codex_home, claude_dir=claude_dir)
            if not args.offline:
                inherit_provider_config(source=source_home, target=codex_home)
            refresh_shipped_assets(install_env=env)
            validate_path_references(codex_home=codex_home, claude_dir=claude_dir)
            if not args.offline:
                codex = shutil.which("codex")
                if not codex:
                    raise SmokeFailure("codex CLI is not installed")
                workspace = root / "fixture"
                workspace.mkdir()
                run_codex_probe(codex, codex_home=codex_home, install_env=env, workspace=workspace, trace_dir=args.trace_dir)
    except (SmokeFailure, ValueError, OSError, ImportError) as exc:
        print(f"Codex roundtable smoke failed: {exc}", file=sys.stderr)
        return 1
    print(
        "Codex roundtable offline smoke passed (installation and paths only)."
        if args.offline
        else "Codex roundtable live smoke passed (skill, two native seats, verdicts, continuation)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
