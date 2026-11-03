"""Regression checks for routing, coverage, execution evidence and native installs."""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from install_codex_source_adapters import install_source_only_adapters, resolve_skill_root, tomllib
from smoke_test_codex_roundtable import build_install_env, refresh_shipped_assets, session_tool_calls, validate_live_result, validate_path_references, SmokeFailure
from zhuzi.validators.verdict import build_schema, validate_must_haves, validate_verdict
import run_behavioral_evals as behavioral

CONTRACT = json.loads((ROOT / "zhuzi/manifests/roundtable-contract.json").read_text())


def feynman():
    return {"feynman_verdict": {
        "core": {"seat": "feynman", "phase": 1, "route": "go", "seat_native_verdict": "clear",
                 "confidence": "medium", "hard_blockers": [], "peer_disagreements": [],
                 "evidence": [{"claim": "说明与接口一致", "source": "fixture/app.py:add", "kind": "observed"}],
                 "missing_evidence": []},
        "must_haves_review": [{"truth": 1, "flag": "none"}],
        "must_haves_challenge": {"triggered": False, "challenged_truths": [], "fundamental_issue": "", "proposed_revision": []},
        "seat_specific": {"undefined_terms": [], "mechanism_gaps": [], "missing_examples": [],
                          "boundary_gaps": [], "false_analogies": [], "verification_gaps": [],
                          "ai_misread_risk": "low", "diagnosis_level": "n_a"}}}


def execution():
    return {"linus_execution": {"phase": 4, "status": "done", "decisions_honored": True,
        "out_of_scope_touched": False, "verification_attempted": [
            {"truth": 1, "cmd": "python3 check.py", "result": "passed", "evidence": "exit=0; actual=5"}],
        "self_audit": ["已检查变更范围"], "commit_status": "not_committed", "gaps_to_route_back": []}}


def locked():
    return {"truths": ["返回值为 5"], "verify_commands": [
        {"truth": 1, "cmd": "python3 check.py", "pass_criterion": "exit=0 且 actual=5"}]}


class VerdictTests(unittest.TestCase):
    def validate(self, payload, **kwargs):
        return validate_verdict(payload, contract=CONTRACT, seat_name="feynman-reviewer",
                                phase=1, truth_count=1, **kwargs)

    def test_valid_verdict_and_generated_schema(self):
        from jsonschema import Draft202012Validator
        Draft202012Validator.check_schema(build_schema(CONTRACT))
        self.assertEqual(self.validate(feynman()), [])
        self.assertEqual(json.loads((ROOT / "zhuzi/schemas/verdict.schema.json").read_text()), build_schema(CONTRACT))

    def test_shipped_broken_example_is_a_valid_phase_two_verdict(self):
        import re
        import yaml
        example = (ROOT / "examples/roundtable-broken-veto.md").read_text()
        payload = yaml.safe_load(re.search(r"```yaml\n(.*?)\n```", example, re.S).group(1))
        self.assertEqual(validate_verdict(payload, contract=CONTRACT, seat_name="linus-engineer",
                                         phase=2, truth_count=1), [])

    def test_rejects_missing_truth_and_duplicate_review(self):
        for records in ([], [{"truth": 1, "flag": "none"}] * 2, [{"truth": 2, "flag": "none"}]):
            payload = feynman()
            payload["feynman_verdict"]["must_haves_review"] = records
            self.assertTrue(self.validate(payload))

    def test_rejects_false_native_route_and_unresolved_go(self):
        for change in ({"route": "kill"}, {"hard_blockers": ["缺少验证"]}, {"seat": "linus"}, {"phase": 2}):
            payload = feynman()
            payload["feynman_verdict"]["core"].update(change)
            self.assertTrue(self.validate(payload))

    def test_blind_review_cannot_invent_peer_disagreements(self):
        payload = feynman()
        payload["feynman_verdict"]["core"]["peer_disagreements"] = [{"peer": "taleb", "point": "实际分歧"}]
        self.assertTrue(self.validate(payload))
        self.assertEqual(self.validate(payload, peer_context=True), [])

    def test_challenge_requires_revision_and_stops_go(self):
        payload = feynman()
        body = payload["feynman_verdict"]
        body["must_haves_challenge"].update(triggered=True, challenged_truths=[1], fundamental_issue="接口语义未定义")
        self.assertTrue(self.validate(payload))
        body["must_haves_challenge"]["proposed_revision"] = [{"truth_id": 1, "revised_truth": "接口语义明确",
            "revised_verify_suggestion": "补上输入输出例子", "spawn_sub_topic": ""}]
        self.assertTrue(self.validate(payload))
        body["core"].update(route="revise_must_haves", seat_native_verdict="muddy")
        self.assertEqual(self.validate(payload), [])
        body["must_haves_challenge"]["proposed_revision"][0]["truth_id"] = 2
        self.assertTrue(self.validate(payload))

    def test_rejects_missing_evidence_fields_and_invalid_types(self):
        for field, value in (("evidence", [{}]), ("missing_evidence", "unknown"), ("confidence", "certain")):
            payload = feynman()
            payload["feynman_verdict"]["core"][field] = value
            self.assertTrue(self.validate(payload))
        for payload in ([], None, {"invented_root": {}}):
            self.assertTrue(self.validate(payload))

    def test_munger_conditional_route_comes_from_manifest(self):
        payload = feynman()["feynman_verdict"]
        payload["core"].update(seat="munger", seat_native_verdict="keep", route="revise_must_haves")
        payload["seat_specific"] = {"anti_patterns_hit": [], "lollapalooza_stack": [],
            "circle_of_competence": "in", "incentive_map": {}, "opportunity_cost_note": "明确替代项",
            "reverse_kill_path": "在验证前扩大不可逆投入"}
        validate = lambda: validate_verdict({"munger_verdict": payload}, contract=CONTRACT,
            seat_name="munger-reviewer", phase=1, truth_count=1)
        self.assertTrue(validate())
        payload["must_haves_challenge"] = {"triggered": True, "challenged_truths": [1],
            "fundamental_issue": "激励错配", "proposed_revision": [{"truth_id": 1,
            "revised_truth": "明确验证激励", "revised_verify_suggestion": "审查激励结构", "spawn_sub_topic": ""}]}
        self.assertEqual(validate(), [])
        payload["core"]["route"] = "go_with_conditions"
        payload["must_haves_challenge"] = {"triggered": False, "challenged_truths": [],
                                           "fundamental_issue": "", "proposed_revision": []}
        self.assertEqual(validate(), [])

    def test_execution_rejects_failed_skipped_missing_and_out_of_scope(self):
        validate = lambda p: validate_verdict(p, contract=CONTRACT, seat_name="linus-engineer",
            phase=4, truth_count=1, must_haves=locked())
        self.assertEqual(validate(execution()), [])
        for result in ("failed", "skipped"):
            payload = execution()
            payload["linus_execution"]["verification_attempted"][0]["result"] = result
            self.assertTrue(validate(payload))
        for change in ({"verification_attempted": []}, {"out_of_scope_touched": True},
                       {"decisions_honored": False}, {"gaps_to_route_back": ["仍缺测试"]}, {"commit_status": "committed"}):
            payload = execution()
            payload["linus_execution"].update(change)
            self.assertTrue(validate(payload))
        payload = execution()
        payload["linus_execution"]["verification_attempted"][0]["cmd"] = "echo passed"
        self.assertTrue(validate(payload))

    def test_execution_needs_the_actual_complete_locked_contract(self):
        self.assertTrue(validate_verdict(execution(), contract=CONTRACT, seat_name="linus-engineer",
                                         phase=4, truth_count=1))
        incomplete = locked()
        incomplete["truths"].append("另一个未验证的主张")
        self.assertTrue(validate_verdict(execution(), contract=CONTRACT, seat_name="linus-engineer",
                                         phase=4, truth_count=1, must_haves=incomplete))

    def test_locked_criteria_and_commands_cannot_be_tbd(self):
        self.assertEqual(validate_must_haves(locked()), [])
        for value in ("TBD", "", None):
            payload = locked()
            payload["verify_commands"][0]["pass_criterion"] = value
            self.assertTrue(validate_must_haves(payload))
        payload = locked()
        payload["verify_commands"][0]["truth"] = True
        self.assertTrue(validate_must_haves(payload))

    def test_claimed_live_success_without_tool_events_fails(self):
        home = Path("/tmp/fixture")
        linus = feynman()["feynman_verdict"]
        linus["core"].update(seat="linus", phase=2, seat_native_verdict="sane")
        linus["seat_specific"] = {"broken_evidence": [], "must_haves_coverage_detail": [],
            "refactor_prerequisites": [], "risk_notes": [], "out_of_scope_for_strategy": []}
        result = {"skill_loaded": True, "workflow_path": str(home / "zhuzi/workflows/roundtable.md"),
                  "results": [{"seat": "feynman-reviewer", "phase": 1, "verdict_json": json.dumps(feynman())},
                              {"seat": "linus-engineer", "phase": 2, "verdict_json": json.dumps({"linus_feasibility": linus})}],
                  "continuation_agent_id": "claimed-agent", "continuation_message": "CONTINUE_OK"}
        with self.assertRaisesRegex(SmokeFailure, "spawn/continuation"):
            validate_live_result(result, [], codex_home=home)

    def test_only_paired_tool_calls_are_execution_evidence(self):
        with tempfile.TemporaryDirectory(prefix="zhuzi-session-test-") as raw:
            home = Path(raw)
            events = [
                {"type": "response_item", "payload": {"type": "function_call", "name": "collaboration.spawn_agent",
                    "call_id": "finished", "arguments": json.dumps({"agent_type": "linus-engineer"})}},
                {"type": "response_item", "payload": {"type": "function_call_output", "call_id": "finished",
                    "output": json.dumps({"task_name": "/root/linus"})}},
                {"type": "response_item", "payload": {"type": "function_call", "name": "collaboration.spawn_agent",
                    "call_id": "not-executed", "arguments": json.dumps({"agent_type": "feynman-reviewer"})}},
            ]
            (home / "sessions").mkdir()
            (home / "sessions/session.jsonl").write_text("\n".join(json.dumps(e) for e in events))
            calls = session_tool_calls(home)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0]["arguments"]["agent_type"], "linus-engineer")


class EvaluationTests(unittest.TestCase):
    def test_expected_rubric_is_never_leaked_to_models(self):
        case = {"id": "fixture", "prompt": "给定事实", "skills": ["feynman-explainer"],
                "workflow": "roundtable", "rubric": ["SECRET_GRADING_CRITERION"]}
        for mode in ("plain", "single", "roundtable"):
            prompt = behavioral.prompt_for(case, mode)
            self.assertIn("给定事实", prompt)
            self.assertNotIn("SECRET_GRADING_CRITERION", prompt)

    def test_capture_keeps_success_unscored_and_records_usage(self):
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory(prefix="zhuzi-eval-test-") as raw:
            target = Path(raw) / "capture.jsonl"
            def fake_run(cmd, **kwargs):
                if cmd[1:] == ["--version"]:
                    return SimpleNamespace(stdout="codex-fixture", stderr="", returncode=0)
                Path(cmd[cmd.index("-o") + 1]).write_text("actual fixture answer")
                sessions = Path(kwargs["env"]["CODEX_HOME"]) / "sessions"
                sessions.mkdir(parents=True)
                (sessions / "root.jsonl").write_text("\n".join(json.dumps(e) for e in [
                    {"type": "session_meta", "payload": {"id": "root"}},
                    {"type": "event_msg", "payload": {"type": "thread_settings_applied", "thread_id": "root",
                        "thread_settings": {"model": "fixture-model", "reasoning_effort": "medium"}}}]))
                return SimpleNamespace(stdout=json.dumps({"type": "turn.completed", "usage": {"input_tokens": 123}}),
                                       stderr="", returncode=0)
            args = ["eval", "--run", "--case", "early-pmf", "--mode", "plain", "--model", "fixture-model", "--output", str(target)]
            with patch.object(sys, "argv", args), patch.object(behavioral.shutil, "which", return_value="fixture-codex"), \
                 patch.object(behavioral.subprocess, "run", side_effect=fake_run), \
                 patch.object(behavioral, "inherit_provider_config"), patch.object(behavioral, "refresh_shipped_assets"):
                self.assertEqual(behavioral.main(), 0)
            record = json.loads(target.read_text())
            self.assertEqual(record["grading"]["status"], "unscored")
            self.assertIsNone(record["grading"]["scores"])
            self.assertEqual(record["output"], "actual fixture answer")
            self.assertEqual(record["model"], "fixture-model")
            self.assertEqual(record["events"][0]["usage"]["input_tokens"], 123)


class NativeInstallTests(unittest.TestCase):
    def test_custom_roots_native_toml_and_legacy_wrapper_migration(self):
        with tempfile.TemporaryDirectory(prefix="zhuzi-install-test-") as raw:
            root = Path(raw)
            home = root / 'codex space "quote"'
            (home / "agents").mkdir(parents=True)
            (home / "agents/linus-engineer.md").write_text("old zhuzi wrapper")
            other = home / "agents/unrelated.md"
            other.write_text("keep this agent")
            env = build_install_env(codex_home=home, claude_dir=root / "claude space")
            refresh_shipped_assets(install_env=env)
            self.assertEqual(other.read_text(), "keep this agent")
            self.assertFalse((home / "agents/linus-engineer.md").exists())
            other.unlink()  # The standalone smoke fixture intentionally has only zhuzi agents.
            validate_path_references(codex_home=home)
            with patch.dict(os.environ, env):
                install_source_only_adapters(home)
            validate_path_references(codex_home=home)
            for seat in CONTRACT["seats"]:
                agent = tomllib.loads((home / "agents" / f"{seat}.toml").read_text())
                self.assertIn(str(home), agent["developer_instructions"])
                self.assertNotIn("sandbox_mode", agent)
            for skill in json.loads((ROOT / "zhuzi/manifests/shipped-surface.json").read_text())["families"]["skills"]:
                self.assertTrue((home / "skills" / skill["entry"] / "references").is_dir())

    def test_default_discovery_and_explicit_override(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(resolve_skill_root(Path.home() / ".codex"), Path.home() / ".agents/skills")
        with patch.dict(os.environ, {"CODEX_SKILL_DIR": "/tmp/isolated-skills"}):
            self.assertEqual(resolve_skill_root(Path("/tmp/custom-codex")), Path("/tmp/isolated-skills"))


if __name__ == "__main__":
    unittest.main()
