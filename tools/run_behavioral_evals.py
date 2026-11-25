#!/usr/bin/env python3
"""Record comparable Codex runs with deterministic protocol pre-checks; human rubric scores stay unscored until reviewed."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from install_codex_source_adapters import serialize_agent_toml, tomllib
from smoke_test_codex_roundtable import (
    SmokeFailure,
    build_install_env,
    inherit_provider_config,
    read_session_evidence,
    refresh_shipped_assets,
)

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "evals/cases.json"


def prompt_for(case: dict, mode: str) -> str:
    common = "本次只回答和分析，不实施、不修改文件、不提交。事实仅限题目给出的材料，缺少资料时说明。\n"
    if mode == "plain":
        instruction = "直接回答本题；不加载 zhuzi skill，不调用子 agent。\n"
    elif mode == "single":
        instruction = "由一个 agent 使用以下人物方法论独立分析，不调用子 agent：" + ", ".join(case["skills"]) + "。\n"
    else:
        subcmd = "quick" if case["workflow"] == "quick" else "roundtable"
        instruction = f"使用 $zhuzi {subcmd}。按协议选席；具名席位不可用时如实报告。已有授权仅限只读评议，须用户取舍时停在该处，不能假定追加批准。\n"
    # Expected answers, rubrics, and deterministic_checks are deliberately excluded from model inputs.
    return common + instruction + "\n用户请求：\n" + case["prompt"]


def evaluate_protocol_checks(case: dict, output: str, evidence: dict | None = None) -> dict[str, object]:
    checks = case.get("deterministic_checks")
    if not isinstance(checks, dict) or not checks:
        return {"passed": True, "failures": []}
    failures: list[str] = []
    if checks.get("forbid_yaml_fence") and re.search(r"```(?:yaml|yml)\b", output, re.I):
        failures.append("output contains forbidden YAML code fence in quick mode")
    max_spawns = checks.get("max_spawned_seats")
    if isinstance(max_spawns, int) and isinstance(evidence, dict):
        spawns = [c for c in evidence.get("calls", []) if c.get("tool") == "spawn_agent"]
        if len(spawns) > max_spawns:
            failures.append(f"spawned {len(spawns)} seats > allowed {max_spawns}")
    return {"passed": not failures, "failures": failures}


def asset_digest() -> str:
    digest = hashlib.sha256()
    files = [
        p
        for name in ("skills", "runtimes", "zhuzi")
        for p in (ROOT / name).rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and not p.name.endswith(":Zone.Identifier")
    ]
    for path in sorted(files):
        digest.update(str(path.relative_to(ROOT)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def pin_agent_configuration(home: Path, model: str, effort: str) -> list[str]:
    """Pin only temporary native roles; role settings override explicit spawn values."""
    roles = []
    for path in sorted((home / "agents").glob("*.toml")):
        payload = tomllib.loads(path.read_text())
        ordered: dict[str, object] = {}
        for k, v in payload.items():
            if not isinstance(v, dict):
                ordered[k] = v
        ordered["model"] = model
        ordered["model_reasoning_effort"] = effort
        for k, v in payload.items():
            if isinstance(v, dict):
                ordered[k] = v
        rendered = serialize_agent_toml(ordered)
        path.write_text(rendered)
        roles.append(str(ordered["name"]))
    return roles


def evaluation_overrides(model: str, effort: str) -> list[str]:
    return [
        "-c",
        f"model_reasoning_effort={json.dumps(effort)}",
        "-c",
        f"agents.default_subagent_model={json.dumps(model)}",
        "-c",
        f"agents.default_subagent_reasoning_effort={json.dumps(effort)}",
    ]


def effective_configuration(home: Path, model: str, effort: str) -> dict:
    try:
        evidence = read_session_evidence(home)
    except SmokeFailure as exc:
        return {
            "requested": {"model": model, "reasoning_effort": effort},
            "observed": [],
            "status": "unverified",
            "issues": [str(exc)],
        }
    threads = evidence["threads"]
    observed, issues, mismatch = [], [], False
    if len([t for t in threads.values() if not t["parent_id"]]) != 1:
        issues.append("expected one recorded orchestrator thread")
    for thread in threads.values():
        if not thread["configurations"]:
            issues.append(f"missing effective settings for thread {thread['id']}")
        for settings in thread["configurations"]:
            observed.append({"thread_id": thread["id"], "agent_role": thread["agent_role"], **settings})
            if not settings["model"] or not settings["reasoning_effort"]:
                issues.append(f"incomplete effective settings for thread {thread['id']}")
            elif (settings["model"], settings["reasoning_effort"]) != (model, effort):
                mismatch = True
                issues.append(f"effective model/effort mismatch in thread {thread['id']}")
        for activity in thread["activities"]:
            if activity.get("kind") == "started" and activity.get("agent_thread_id") not in threads:
                issues.append("spawned child has no local effective-configuration record")
    return {
        "requested": {"model": model, "reasoning_effort": effort},
        "observed": observed,
        "status": "mismatch" if mismatch else "unverified" if issues else "verified",
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append", default=[], help="case ID; repeat to select more")
    parser.add_argument("--mode", action="append", choices=("plain", "single", "roundtable"))
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--run", action="store_true", help="invoke the model; otherwise only list selected cases")
    parser.add_argument("--model", help="explicit available model ID, required for comparable model runs")
    parser.add_argument("--reasoning-effort", default="medium", help="fixed effort for parent and native seats; must be supported by the selected model")
    parser.add_argument("--output", type=Path, help="JSONL capture path, required with --run")
    args = parser.parse_args()
    data = json.loads(DATASET.read_text())
    known = {c["id"]: c for c in data["cases"]}
    if any(i not in known for i in args.case) or args.repeat < 1:
        parser.error("unknown case ID or non-positive repeat")
    cases = [known[i] for i in args.case] if args.case else list(known.values())
    if not args.run:
        for case in cases:
            print(f"{case['id']}\t{case['prompt']}")
        return 0
    if not args.model or not args.output or not args.case:
        parser.error("--run requires --model, --output and explicit --case selections")
    codex = shutil.which("codex")
    if not codex:
        parser.error("codex CLI is not installed")
    version = subprocess.run([codex, "--version"], capture_output=True, text=True, check=True).stdout.strip()
    source = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    dataset_hash = hashlib.sha256(DATASET.read_bytes()).hexdigest()
    assets = asset_digest()
    failed = False
    with args.output.open("x", encoding="utf-8") as capture, tempfile.TemporaryDirectory(prefix="zhuzi-eval-") as raw:
        root = Path(raw)
        for case in cases:
            for repeat in range(args.repeat):
                for mode in args.mode or ("plain", "single", "roundtable"):
                    run_root = root / f"{case['id']}-{repeat}-{mode}"
                    home = run_root / "codex-home"
                    home.mkdir(parents=True)
                    env = build_install_env(codex_home=home, claude_dir=run_root / "claude-home")
                    inherit_provider_config(source=source, target=home)
                    refresh_shipped_assets(install_env=env)
                    pinned = pin_agent_configuration(home, args.model, args.reasoning_effort)
                    workspace = run_root / "workspace"
                    (workspace / ".agents").mkdir(parents=True)
                    (workspace / ".agents/skills").symlink_to(home / "skills", target_is_directory=True)
                    output = root / "last-output.txt"
                    output.unlink(missing_ok=True)
                    prompt = prompt_for(case, mode)
                    started = time.monotonic()
                    try:
                        result = subprocess.run(
                            [
                                codex,
                                "exec",
                                "-C",
                                str(workspace),
                                "--skip-git-repo-check",
                                "--ignore-rules",
                                "--sandbox",
                                "read-only",
                                "--json",
                                "--model",
                                args.model,
                                "-o",
                                str(output),
                                *evaluation_overrides(args.model, args.reasoning_effort),
                                prompt,
                            ],
                            env=env,
                            stdin=subprocess.DEVNULL,
                            text=True,
                            capture_output=True,
                            timeout=420,
                            check=False,
                        )
                        events = []
                        for line in result.stdout.splitlines():
                            try:
                                events.append(json.loads(line))
                            except json.JSONDecodeError:
                                continue
                        error = result.stderr[-2000:] if result.returncode else ""
                        code = result.returncode
                    except subprocess.TimeoutExpired:
                        events, error, code = [], "timeout after 420 seconds", -1
                    configuration = effective_configuration(home, args.model, args.reasoning_effort)
                    configuration["pinned_native_roles"] = pinned
                    raw_output = output.read_text() if output.exists() else ""
                    session_ev = None
                    try:
                        session_ev = read_session_evidence(home)
                    except SmokeFailure:
                        session_ev = None
                    protocol_checks = evaluate_protocol_checks(case, raw_output, session_ev) if mode == "roundtable" else {"passed": True, "failures": []}
                    eligible = code == 0 and configuration["status"] == "verified"
                    record = {
                        "case": case["id"],
                        "mode": mode,
                        "repeat": repeat,
                        "model": args.model if eligible else None,
                        "reasoning_effort": args.reasoning_effort if eligible else None,
                        "configuration": configuration,
                        "comparison_eligible": eligible,
                        "codex_version": version,
                        "dataset_sha256": dataset_hash,
                        "assets_sha256": assets,
                        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                        "elapsed_seconds": round(time.monotonic() - started, 3),
                        "exit_code": code,
                        "output": raw_output,
                        "events": events,
                        "error": error,
                        "grading": {
                            "status": "unscored",
                            "rubric": case["rubric"],
                            "protocol_checks": protocol_checks,
                            "scores": None,
                            "reviewer": None,
                        },
                    }
                    capture.write(json.dumps(record, ensure_ascii=False) + "\n")
                    capture.flush()
                    failed |= not eligible or not protocol_checks["passed"]
                    print(f"{case['id']} {mode} #{repeat + 1}: exit={code}; config={configuration['status']}; unscored", flush=True)
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
