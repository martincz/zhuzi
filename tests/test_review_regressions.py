"""Adversarial regressions for mandatory routing, continuation proof and eval settings."""
from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from test_contracts import CONTRACT, feynman
from zhuzi.validators.verdict import build_schema
import smoke_test_codex_roundtable as smoke
import run_behavioral_evals as behavioral


def lopez(flag, route="go"):
    body = feynman()["feynman_verdict"]
    body["core"].update(seat="lopezdeprado", seat_native_verdict="scientific", route=route)
    body["seat_specific"] = {"claim_classification": [], "causal_graph_missing": False,
        "trial_count_disclosed": "yes", "integrity_checklist_failures": [], "anti_pattern_hits": [],
        "workflow_diagnosis": "unclear", "domain_limit_flag": flag}
    return {"lopezdeprado_verdict": body}


def event(payload, second=1, kind="event_msg"):
    return {"type": kind, "timestamp": f"2026-11-03T00:00:{second:02d}.000Z", "payload": payload}


def final(thread, turn, text, second):
    return [event({"type": "item_completed", "thread_id": thread, "turn_id": turn,
                   "item": {"type": "AgentMessage", "phase": "final_answer",
                            "content": [{"type": "Text", "text": text}]}}, second),
            event({"type": "task_complete", "turn_id": turn, "last_agent_message": text}, second)]


def write_log(home, name, records):
    path = home / "sessions" / f"{name}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in records))


def smoke_fixture(home, *, continuation_output="", continuation_status="completed",
                  child_reply=True, child_role="linus-engineer", actual_handle="/root/linus"):
    linus = feynman()["feynman_verdict"]
    linus["core"].update(seat="linus", phase=2, seat_native_verdict="sane")
    linus["seat_specific"] = {"broken_evidence": [], "must_haves_coverage_detail": [],
        "refactor_prerequisites": [], "risk_notes": [], "out_of_scope_for_strategy": []}
    verdicts = {"feynman-reviewer": feynman(), "linus-engineer": {"linus_feasibility": linus}}
    result = {"skill_loaded": True, "workflow_path": str(home / "zhuzi/workflows/roundtable.md"),
              "results": [{"seat": seat, "phase": phase, "verdict_json": json.dumps(verdicts[seat])}
                          for seat, phase in (("feynman-reviewer", 1), ("linus-engineer", 2))],
              "continuation_agent_id": "/root/linus", "continuation_message": "CONTINUE_OK: actual reply"}
    root_meta = {"id": "root", "cwd": "/fixture", "source": "exec"}
    root = [event(root_meta, kind="session_meta")]
    calls = []
    for call_id, tool, args, output, target, second, status in [
        ("sf", "spawn_agent", {"agent_type": "feynman-reviewer"}, json.dumps({"task_name": "/root/feynman"}), "fey", 1, "completed"),
        ("sl", "spawn_agent", {"agent_type": child_role, "message": "linus-engineer"}, json.dumps({"task_name": actual_handle}), "linus", 2, "completed"),
        ("cl", "followup_task", {"target": "/root/linus", "message": "return CONTINUE_OK"}, continuation_output, "linus", 5, continuation_status),
    ]:
        root.extend([event({"type": "function_call", "name": f"collaboration.{tool}", "call_id": call_id, "arguments": json.dumps(args)}, second, "response_item"),
                     event({"type": "function_call_output", "call_id": call_id, "output": output}, second, "response_item")])
        root.append(event({"type": "item_completed", "thread_id": "root", "turn_id": "rt",
            "item": {"type": "SubAgentActivity", "id": call_id, "kind": "started" if tool == "spawn_agent" else "interacted",
                     "agent_thread_id": target, "agent_path": "/root/feynman" if target == "fey" else actual_handle}}, second))
        calls.append({"call_id": call_id, "owner_thread_id": "root", "tool": tool,
                      "arguments": args, "output": output, "status": status})
    write_log(home, "root", root)
    for thread, role, handle, second in [("fey", "feynman-reviewer", "/root/feynman", 3), ("linus", child_role, actual_handle, 4)]:
        records = [event({"id": thread, "parent_thread_id": "root", "agent_role": role, "agent_path": handle, "cwd": "/fixture"}, kind="session_meta")]
        records += final(thread, f"{thread}-initial", json.dumps(verdicts["feynman-reviewer" if thread == "fey" else "linus-engineer"]), second)
        if thread == "linus" and child_reply:
            records += final(thread, "linus-continued", result["continuation_message"], 6)
        write_log(home, thread, records)
    return result, calls


class MandatoryRouteTests(unittest.TestCase):
    def test_out_of_domain_and_silence_cannot_approve(self):
        for flag in ("out_of_domain", "L4_silence"):
            for route in CONTRACT["verdict_schema"]["route_space"]:
                with self.subTest(flag=flag, route=route):
                    errors = smoke.validate_verdict(lopez(flag, route), contract=CONTRACT,
                        seat_name="lopezdeprado-reviewer", phase=1, truth_count=1)
                    self.assertEqual(not errors, route == "too_hard")

    def test_in_domain_native_route_remains_available(self):
        self.assertEqual(smoke.validate_verdict(lopez("none"), contract=CONTRACT,
                         seat_name="lopezdeprado-reviewer", phase=1, truth_count=1), [])

    def test_override_cannot_be_relaxed_by_a_later_addition(self):
        from zhuzi.validators.verdict import allowed_routes
        seat = copy.deepcopy(CONTRACT["seats"]["lopezdeprado-reviewer"])
        extra = copy.deepcopy(seat["conditional_routes"][0])
        extra.update(mode="add", route="go")
        seat["conditional_routes"].append(extra)
        self.assertEqual(allowed_routes(seat, lopez("out_of_domain")["lopezdeprado_verdict"]), {"too_hard"})

    def test_generated_schema_also_enforces_mandatory_route(self):
        from jsonschema import Draft202012Validator
        validator = Draft202012Validator(build_schema(CONTRACT))
        self.assertFalse(validator.is_valid(lopez("out_of_domain", "go")))
        self.assertTrue(validator.is_valid(lopez("out_of_domain", "too_hard")))


class ContinuationEvidenceTests(unittest.TestCase):
    def test_real_same_thread_reply_passes(self):
        with tempfile.TemporaryDirectory() as raw:
            home = Path(raw)
            result, calls = smoke_fixture(home)
            smoke.validate_live_result(result, [], codex_home=home, raw_calls=calls)

    def test_tool_failure_cannot_be_overridden_by_parent_report(self):
        for output in ("Error: no such agent", "agent not found", json.dumps({"status": "failed", "error": "agent not found"})):
            with self.subTest(output=output), tempfile.TemporaryDirectory() as raw:
                home = Path(raw)
                result, calls = smoke_fixture(home, continuation_output=output, continuation_status="failed")
                with self.assertRaises(smoke.SmokeFailure):
                    smoke.validate_live_result(result, [], codex_home=home, raw_calls=calls)

    def test_failed_status_cannot_be_overridden_by_a_successful_parent_report(self):
        with tempfile.TemporaryDirectory() as raw:
            home = Path(raw)
            result, calls = smoke_fixture(home, continuation_status="failed")
            with self.assertRaises(smoke.SmokeFailure):
                smoke.validate_live_result(result, [], codex_home=home, raw_calls=calls)

    def test_parent_sentinel_without_child_reply_fails(self):
        with tempfile.TemporaryDirectory() as raw:
            home = Path(raw)
            result, calls = smoke_fixture(home, child_reply=False)
            with self.assertRaises(smoke.SmokeFailure):
                smoke.validate_live_result(result, [], codex_home=home, raw_calls=calls)

    def test_default_agent_mentioning_seat_is_not_that_seat(self):
        with tempfile.TemporaryDirectory() as raw:
            home = Path(raw)
            result, calls = smoke_fixture(home, child_role="default")
            with self.assertRaises(smoke.SmokeFailure):
                smoke.validate_live_result(result, [], codex_home=home, raw_calls=calls)

    def test_partial_handle_match_fails(self):
        with tempfile.TemporaryDirectory() as raw:
            home = Path(raw)
            result, calls = smoke_fixture(home, actual_handle="/root/linus-extra")
            with self.assertRaises(smoke.SmokeFailure):
                smoke.validate_live_result(result, [], codex_home=home, raw_calls=calls)

    def test_inherited_parent_final_cannot_substitute_for_child_reply(self):
        with tempfile.TemporaryDirectory() as raw:
            home = Path(raw)
            result, calls = smoke_fixture(home, child_reply=False)
            with (home / "sessions/linus.jsonl").open("a") as stream:
                for record in final("root", "rt", result["continuation_message"], 6):
                    stream.write("\n" + json.dumps(record))
            with self.assertRaises(smoke.SmokeFailure):
                smoke.validate_live_result(result, [], codex_home=home, raw_calls=calls)

    def test_stale_or_wrong_thread_sentinel_cannot_prove_continuation(self):
        for owner, second in (("linus", 4), ("fey", 6)):
            with self.subTest(owner=owner, second=second), tempfile.TemporaryDirectory() as raw:
                home = Path(raw)
                result, calls = smoke_fixture(home, child_reply=False)
                with (home / f"sessions/{owner}.jsonl").open("a") as stream:
                    for record in final(owner, f"{owner}-unrelated", result["continuation_message"], second):
                        stream.write("\n" + json.dumps(record))
                with self.assertRaises(smoke.SmokeFailure):
                    smoke.validate_live_result(result, [], codex_home=home, raw_calls=calls)

    def test_parent_cannot_replace_the_actual_verdict(self):
        with tempfile.TemporaryDirectory() as raw:
            home = Path(raw)
            result, calls = smoke_fixture(home)
            verdict = json.loads(result["results"][0]["verdict_json"])
            verdict["feynman_verdict"]["core"]["confidence"] = "low"
            result["results"][0]["verdict_json"] = json.dumps(verdict)
            with self.assertRaises(smoke.SmokeFailure):
                smoke.validate_live_result(result, [], codex_home=home, raw_calls=calls)


class EvaluationConfigurationTests(unittest.TestCase):
    def test_successful_process_without_config_evidence_is_not_comparable(self):
        with tempfile.TemporaryDirectory() as raw:
            output = Path(raw) / "capture.jsonl"
            def run(cmd, **kwargs):
                if cmd[1:] == ["--version"]:
                    return SimpleNamespace(stdout="fixture-cli", stderr="", returncode=0)
                Path(cmd[cmd.index("-o") + 1]).write_text("retained answer")
                return SimpleNamespace(stdout='{"type":"turn.completed"}', stderr="", returncode=0)
            args = ["eval", "--run", "--case", "early-pmf", "--mode", "plain", "--model", "fixture-model", "--output", str(output)]
            with patch.object(sys, "argv", args), patch.object(behavioral.shutil, "which", return_value="fixture-codex"), \
                 patch.object(behavioral.subprocess, "run", side_effect=run), \
                 patch.object(behavioral, "inherit_provider_config"), patch.object(behavioral, "refresh_shipped_assets"):
                self.assertEqual(behavioral.main(), 1)
            record = json.loads(output.read_text())
            self.assertFalse(record["comparison_eligible"])
            self.assertIsNone(record["model"])
            self.assertEqual(record["configuration"]["status"], "unverified")
            self.assertEqual(record["output"], "retained answer")
            self.assertEqual(record["grading"]["status"], "unscored")

    def test_inherited_child_defaults_are_overridden_and_effective_settings_recorded(self):
        with tempfile.TemporaryDirectory() as raw:
            source = Path(raw) / "profile"
            source.mkdir()
            (source / "config.toml").write_text('[agents]\ndefault_subagent_model = "other-model"\ndefault_subagent_reasoning_effort = "max"\n')
            output = Path(raw) / "capture.jsonl"
            observed_commands = []
            def install(*, install_env):
                directory = Path(install_env["CODEX_HOME"]) / "agents"
                directory.mkdir()
                (directory / "feynman.toml").write_text('name = "feynman-reviewer"\ndescription = "fixture"\ndeveloper_instructions = "fixture"\nmodel = "role-model"\nmodel_reasoning_effort = "high"\n')
            def run(cmd, **kwargs):
                if cmd[1:] == ["--version"]:
                    return SimpleNamespace(stdout="fixture-cli", stderr="", returncode=0)
                observed_commands.append(cmd)
                home = Path(kwargs["env"]["CODEX_HOME"])
                role = smoke.tomllib.loads((home / "agents/feynman.toml").read_text())
                self.assertEqual((role["model"], role["model_reasoning_effort"]), ("fixture-model", "medium"))
                for identifier, parent, role in (("root", None, None), ("child", "root", "feynman-reviewer")):
                    write_log(home, identifier, [event({"id": identifier, "parent_thread_id": parent, "agent_role": role}, kind="session_meta"),
                        event({"type": "thread_settings_applied", "thread_id": identifier, "thread_settings": {"model": "fixture-model", "reasoning_effort": "medium"}})])
                Path(cmd[cmd.index("-o") + 1]).write_text("fixture answer")
                return SimpleNamespace(stdout='{"type":"turn.completed"}', stderr="", returncode=0)
            args = ["eval", "--run", "--case", "early-pmf", "--mode", "roundtable", "--model", "fixture-model", "--output", str(output)]
            with patch.dict(os.environ, {"CODEX_HOME": str(source)}), patch.object(sys, "argv", args), \
                 patch.object(behavioral.shutil, "which", return_value="fixture-codex"), \
                 patch.object(behavioral.subprocess, "run", side_effect=run), \
                 patch.object(behavioral, "refresh_shipped_assets", side_effect=install):
                self.assertEqual(behavioral.main(), 0)
            cmd = observed_commands[0]
            settings = [cmd[i + 1] for i, value in enumerate(cmd[:-1]) if value == "-c"]
            self.assertIn('agents.default_subagent_model="fixture-model"', settings)
            self.assertIn('agents.default_subagent_reasoning_effort="medium"', settings)
            self.assertIn('model_reasoning_effort="medium"', settings)
            record = json.loads(output.read_text())
            self.assertEqual(record["configuration"]["status"], "verified")
            self.assertEqual({v["model"] for v in record["configuration"]["observed"]}, {"fixture-model"})
            self.assertEqual({v["reasoning_effort"] for v in record["configuration"]["observed"]}, {"medium"})
            self.assertIn('default_subagent_model = "other-model"', (source / "config.toml").read_text())

    def test_effective_mismatch_and_missing_records_are_not_comparable(self):
        for child_model, child_effort, expected in (("other-model", "medium", "mismatch"),
                                                  ("fixture-model", "max", "mismatch"),
                                                  (None, None, "unverified")):
            with self.subTest(model=child_model, effort=child_effort), tempfile.TemporaryDirectory() as raw:
                home = Path(raw)
                for identifier, parent, model, effort in (("root", None, "fixture-model", "medium"),
                                                         ("child", "root", child_model, child_effort)):
                    write_log(home, identifier, [event({"id": identifier, "parent_thread_id": parent}, kind="session_meta"),
                        event({"type": "thread_settings_applied", "thread_id": identifier,
                               "thread_settings": {"model": model, "reasoning_effort": effort}})])
                result = behavioral.effective_configuration(home, "fixture-model", "medium")
                self.assertEqual(result["status"], expected)
                self.assertTrue(result["issues"])

    def test_spawned_child_without_a_configuration_record_is_unverified(self):
        with tempfile.TemporaryDirectory() as raw:
            home = Path(raw)
            write_log(home, "root", [event({"id": "root"}, kind="session_meta"),
                event({"type": "thread_settings_applied", "thread_id": "root",
                       "thread_settings": {"model": "fixture-model", "reasoning_effort": "medium"}}),
                event({"type": "item_completed", "thread_id": "root", "turn_id": "rt",
                       "item": {"type": "SubAgentActivity", "kind": "started", "agent_thread_id": "missing-child"}})])
            result = behavioral.effective_configuration(home, "fixture-model", "medium")
            self.assertEqual(result["status"], "unverified")
