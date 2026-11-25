"""Regression checks for routing, coverage, execution evidence, dual-runtime gates, and native installs."""
from __future__ import annotations

import copy
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
from install_codex_source_adapters import (
    install_claude_assets,
    install_codex_assets,
    install_source_only_adapters,
    resolve_skill_root,
    tomllib,
)
from smoke_test_codex_roundtable import (
    SmokeFailure,
    build_install_env,
    refresh_shipped_assets,
    session_tool_calls,
    validate_live_result,
    validate_path_references,
)
from zhuzi.validators.verdict import build_schema, validate_must_haves, validate_verdict
import run_behavioral_evals as behavioral

CONTRACT = json.loads((ROOT / "zhuzi/manifests/roundtable-contract.json").read_text())


def feynman():
    return {
        "feynman_verdict": {
            "core": {
                "seat": "feynman",
                "phase": 1,
                "route": "go",
                "seat_native_verdict": "clear",
                "confidence": "medium",
                "hard_blockers": [],
                "peer_disagreements": [],
                "evidence": [{"claim": "说明与接口一致", "source": "fixture/app.py:add", "kind": "observed"}],
                "missing_evidence": [],
            },
            "must_haves_review": [{"truth": 1, "flag": "none"}],
            "must_haves_challenge": {"triggered": False, "challenged_truths": [], "fundamental_issue": "", "proposed_revision": []},
            "seat_specific": {
                "undefined_terms": [],
                "mechanism_gaps": [],
                "missing_examples": [],
                "boundary_gaps": [],
                "false_analogies": [],
                "verification_gaps": [],
                "ai_misread_risk": "low",
                "diagnosis_level": "n_a",
            },
        }
    }


def execution():
    return {
        "linus_execution": {
            "phase": 4,
            "status": "done",
            "decisions_honored": True,
            "out_of_scope_touched": False,
            "verification_attempted": [{"truth": 1, "cmd": "python3 check.py", "result": "passed", "evidence": "exit=0; actual=5"}],
            "self_audit": ["已检查变更范围"],
            "commit_status": "not_committed",
            "gaps_to_route_back": [],
        }
    }


def locked():
    return {
        "truths": ["返回值为 5"],
        "verify_commands": [{"truth": 1, "cmd": "python3 check.py", "pass_criterion": "exit=0 且 actual=5"}],
    }


class VerdictTests(unittest.TestCase):
    def validate(self, payload, **kwargs):
        return validate_verdict(payload, contract=CONTRACT, seat_name="feynman-reviewer", phase=1, truth_count=1, **kwargs)

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
        self.assertEqual(validate_verdict(payload, contract=CONTRACT, seat_name="linus-engineer", phase=2, truth_count=1), [])

    def test_cli_reads_verdict_from_stdin(self):
        import yaml

        command = [
            sys.executable,
            "-B",
            str(ROOT / "zhuzi/validators/verdict.py"),
            "-",
            "--seat",
            "feynman-reviewer",
            "--phase",
            "1",
            "--truth-count",
            "1",
        ]
        for payload, expected_exit in ((yaml.safe_dump(feynman()), 0), ("verdict: [", 1)):
            with self.subTest(expected_exit=expected_exit):
                result = subprocess.run(command, input=payload, text=True, capture_output=True)
                self.assertEqual(result.returncode, expected_exit, result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stderr)

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
        body["must_haves_challenge"]["proposed_revision"] = [
            {"truth_id": 1, "revised_truth": "接口语义明确", "revised_verify_suggestion": "补上输入输出例子", "spawn_sub_topic": ""}
        ]
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
        payload["seat_specific"] = {
            "anti_patterns_hit": [],
            "lollapalooza_stack": [],
            "circle_of_competence": "in",
            "incentive_map": {},
            "opportunity_cost_note": "明确替代项",
            "reverse_kill_path": "在验证前扩大不可逆投入",
        }
        validate = lambda: validate_verdict({"munger_verdict": payload}, contract=CONTRACT, seat_name="munger-reviewer", phase=1, truth_count=1)
        self.assertTrue(validate())
        payload["must_haves_challenge"] = {
            "triggered": True,
            "challenged_truths": [1],
            "fundamental_issue": "激励错配",
            "proposed_revision": [{"truth_id": 1, "revised_truth": "明确验证激励", "revised_verify_suggestion": "审查激励结构", "spawn_sub_topic": ""}],
        }
        self.assertEqual(validate(), [])
        payload["core"]["route"] = "go_with_conditions"
        payload["must_haves_challenge"] = {"triggered": False, "challenged_truths": [], "fundamental_issue": "", "proposed_revision": []}
        self.assertEqual(validate(), [])

    def test_execution_rejects_failed_skipped_missing_and_out_of_scope(self):
        validate = lambda p: validate_verdict(p, contract=CONTRACT, seat_name="linus-engineer", phase=4, truth_count=1, must_haves=locked())
        self.assertEqual(validate(execution()), [])
        for result in ("failed", "skipped"):
            payload = execution()
            payload["linus_execution"]["verification_attempted"][0]["result"] = result
            self.assertTrue(validate(payload))
        for change in (
            {"verification_attempted": []},
            {"out_of_scope_touched": True},
            {"decisions_honored": False},
            {"gaps_to_route_back": ["仍缺测试"]},
            {"commit_status": "committed"},
        ):
            payload = execution()
            payload["linus_execution"].update(change)
            self.assertTrue(validate(payload))
        payload = execution()
        payload["linus_execution"]["verification_attempted"][0]["cmd"] = "echo passed"
        self.assertTrue(validate(payload))

    def test_execution_needs_the_actual_complete_locked_contract(self):
        self.assertTrue(validate_verdict(execution(), contract=CONTRACT, seat_name="linus-engineer", phase=4, truth_count=1))
        incomplete = locked()
        incomplete["truths"].append("另一个未验证的主张")
        self.assertTrue(validate_verdict(execution(), contract=CONTRACT, seat_name="linus-engineer", phase=4, truth_count=1, must_haves=incomplete))

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
        linus["seat_specific"] = {
            "broken_evidence": [],
            "must_haves_coverage_detail": [],
            "refactor_prerequisites": [],
            "risk_notes": [],
            "out_of_scope_for_strategy": [],
        }
        result = {
            "skill_loaded": True,
            "workflow_path": str(home / "zhuzi/workflows/roundtable.md"),
            "results": [
                {"seat": "feynman-reviewer", "phase": 1, "verdict_json": json.dumps(feynman())},
                {"seat": "linus-engineer", "phase": 2, "verdict_json": json.dumps({"linus_feasibility": linus})},
            ],
            "continuation_agent_id": "claimed-agent",
            "continuation_message": "CONTINUE_OK",
        }
        with self.assertRaisesRegex(SmokeFailure, "spawn/continuation"):
            validate_live_result(result, [], codex_home=home)

    def test_only_paired_tool_calls_are_execution_evidence(self):
        with tempfile.TemporaryDirectory(prefix="zhuzi-session-test-") as raw:
            home = Path(raw)
            events = [
                {
                    "type": "response_item",
                    "payload": {
                        "type": "function_call",
                        "name": "collaboration.spawn_agent",
                        "call_id": "finished",
                        "arguments": json.dumps({"agent_type": "linus-engineer"}),
                    },
                },
                {
                    "type": "response_item",
                    "payload": {"type": "function_call_output", "call_id": "finished", "output": json.dumps({"task_name": "/root/linus"})},
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "function_call",
                        "name": "collaboration.spawn_agent",
                        "call_id": "not-executed",
                        "arguments": json.dumps({"agent_type": "feynman-reviewer"}),
                    },
                },
            ]
            (home / "sessions").mkdir()
            (home / "sessions/session.jsonl").write_text("\n".join(json.dumps(e) for e in events))
            calls = session_tool_calls(home)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0]["arguments"]["agent_type"], "linus-engineer")


class EvaluationTests(unittest.TestCase):
    def test_expected_rubric_and_deterministic_checks_are_never_leaked_to_models(self):
        case = {
            "id": "fixture",
            "prompt": "给定事实",
            "skills": ["feynman-explainer"],
            "workflow": "quick",
            "deterministic_checks": {"forbid_yaml_fence": True},
            "rubric": ["SECRET_GRADING_CRITERION"],
        }
        for mode in ("plain", "single", "roundtable"):
            prompt = behavioral.prompt_for(case, mode)
            self.assertIn("给定事实", prompt)
            self.assertNotIn("SECRET_GRADING_CRITERION", prompt)
            self.assertNotIn("forbid_yaml_fence", prompt)

        failed = behavioral.evaluate_protocol_checks(case, "```yaml\ncore:\n  route: go\n```")
        self.assertFalse(failed["passed"])
        passed = behavioral.evaluate_protocol_checks(case, "Linus：纯散文短评观点。")
        self.assertTrue(passed["passed"])

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
                (sessions / "root.jsonl").write_text(
                    "\n".join(
                        json.dumps(e)
                        for e in [
                            {"type": "session_meta", "payload": {"id": "root"}},
                            {
                                "type": "event_msg",
                                "payload": {
                                    "type": "thread_settings_applied",
                                    "thread_id": "root",
                                    "thread_settings": {"model": "fixture-model", "reasoning_effort": "medium"},
                                },
                            },
                        ]
                    )
                )
                return SimpleNamespace(stdout=json.dumps({"type": "turn.completed", "usage": {"input_tokens": 123}}), stderr="", returncode=0)

            args = ["eval", "--run", "--case", "early-pmf", "--mode", "plain", "--model", "fixture-model", "--output", str(target)]
            with patch.object(sys, "argv", args), patch.object(behavioral.shutil, "which", return_value="fixture-codex"), patch.object(
                behavioral.subprocess, "run", side_effect=fake_run
            ), patch.object(behavioral, "inherit_provider_config"), patch.object(behavioral, "refresh_shipped_assets"):
                self.assertEqual(behavioral.main(), 0)
            record = json.loads(target.read_text())
            self.assertEqual(record["grading"]["status"], "unscored")
            self.assertIsNone(record["grading"]["scores"])
            self.assertTrue(record["grading"]["protocol_checks"]["passed"])
            self.assertEqual(record["output"], "actual fixture answer")
            self.assertEqual(record["model"], "fixture-model")
            self.assertEqual(record["events"][0]["usage"]["input_tokens"], 123)


class NativeInstallTests(unittest.TestCase):
    def test_single_umbrella_bundle_special_chars_and_runtime_purity(self):
        with tempfile.TemporaryDirectory(prefix="zhuzi-install-test-") as raw:
            root = Path(raw)
            home = root / 'codex & pipe|space "quote"'
            (home / "agents").mkdir(parents=True)
            (home / "agents/linus-engineer.md").write_text("old zhuzi wrapper")
            other = home / "agents/unrelated.md"
            other.write_text("keep this agent")
            claude_dir = root / "claude & pipe|dir"
            (claude_dir / "commands/zhuzi").mkdir(parents=True)
            (claude_dir / "commands/zhuzi/roundtable.md").write_text("legacy claude command")

            env = build_install_env(codex_home=home, claude_dir=claude_dir)
            refresh_shipped_assets(install_env=env)

            self.assertEqual(other.read_text(), "keep this agent")
            self.assertFalse((home / "agents/linus-engineer.md").exists())
            self.assertFalse((claude_dir / "commands/zhuzi").exists())
            other.unlink()

            validate_path_references(codex_home=home, claude_dir=claude_dir)
            with patch.dict(os.environ, env):
                install_source_only_adapters(home)
            validate_path_references(codex_home=home)

            for seat in CONTRACT["seats"]:
                agent = tomllib.loads((home / "agents" / f"{seat}.toml").read_text())
                self.assertIn(str(home), agent["developer_instructions"])
                self.assertNotIn("sandbox_mode", agent)
                self.assertFalse(agent["skills"]["include_instructions"])
                if seat != "linus-engineer":
                    self.assertFalse(agent["features"]["shell_tool"])

            # Only 'zhuzi' exists at top-level, with all 12 personas bundled under zhuzi/personas/ without research drafts
            self.assertEqual([p.name for p in (home / "skills").iterdir() if p.is_dir()], ["zhuzi"])
            self.assertEqual([p.name for p in (claude_dir / "skills").iterdir() if p.is_dir()], ["zhuzi"])
            for skill in json.loads((ROOT / "zhuzi/manifests/shipped-surface.json").read_text())["families"]["skills"]:
                if skill["entry"] == "zhuzi":
                    continue
                persona_dir = home / "skills/zhuzi/personas" / skill["entry"]
                self.assertTrue((persona_dir / "PERSONA.md").is_file())
                self.assertFalse((persona_dir / "SKILL.md").exists())
                self.assertTrue((persona_dir / "references").is_dir())
                self.assertFalse((persona_dir / "references/research").exists())

    def test_pin_unpin_and_uninstall_lifecycle(self):
        with tempfile.TemporaryDirectory(prefix="zhuzi-pin-test-") as raw:
            root = Path(raw)
            codex_home = root / "codex"
            claude_dir = root / "claude"
            env = build_install_env(codex_home=codex_home, claude_dir=claude_dir)

            with patch.dict(os.environ, env):
                install_codex_assets(codex_home, pin=["linus"])
                install_claude_assets(claude_dir, pin=["linus"])

                self.assertTrue((codex_home / "skills/linus-torvalds-engineer/SKILL.md").is_file())
                self.assertTrue((codex_home / "skills/linus-torvalds-engineer/agents/openai.yaml").is_file())
                self.assertFalse((codex_home / "skills/linus-torvalds-engineer/references/research").exists())
                claude_pinned_text = (claude_dir / "skills/linus-torvalds-engineer/SKILL.md").read_text()
                self.assertIn("disable-model-invocation: true", claude_pinned_text)

                # Unpin cleanly removes top-level shortcut while keeping zhuzi umbrella
                install_codex_assets(codex_home, unpin=["linus"])
                install_claude_assets(claude_dir, unpin=["linus"])
                self.assertFalse((codex_home / "skills/linus-torvalds-engineer").exists())
                self.assertFalse((claude_dir / "skills/linus-torvalds-engineer").exists())
                self.assertTrue((codex_home / "skills/zhuzi/SKILL.md").is_file())

                # Uninstall removes zhuzi assets while keeping unrelated files
                (codex_home / "skills/unrelated").mkdir(parents=True)
                (codex_home / "skills/unrelated/SKILL.md").write_text("keep")
                install_codex_assets(codex_home, uninstall=True)
                self.assertFalse((codex_home / "skills/zhuzi").exists())
                self.assertFalse((codex_home / "zhuzi").exists())
                self.assertTrue((codex_home / "skills/unrelated/SKILL.md").is_file())

    def test_default_home_without_env_overrides_renders_concrete_paths(self):
        import site

        with tempfile.TemporaryDirectory(prefix="zhuzi-fakehome-") as raw:
            fake_home = Path(raw)
            clean_env = {k: v for k, v in os.environ.items() if k not in {"CLAUDE_DIR", "CODEX_HOME", "CODEX_SKILL_DIR"}}
            clean_env["HOME"] = str(fake_home)
            clean_env["PYTHONUSERBASE"] = site.getuserbase()
            clean_env["PYTHONDONTWRITEBYTECODE"] = "1"
            res = subprocess.run(["bash", "install.sh"], cwd=ROOT, env=clean_env, text=True, capture_output=True, check=False)
            self.assertEqual(res.returncode, 0, res.stderr)
            claude_agent = (fake_home / ".claude/agents/munger-reviewer.md").read_text()
            self.assertNotIn("$HOME", claude_agent)
            self.assertIn(str(fake_home / ".claude/zhuzi/seats/munger-reviewer.md"), claude_agent)
            self.assertTrue((fake_home / ".agents/skills/zhuzi/SKILL.md").is_file())

    def test_default_discovery_and_explicit_override(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(resolve_skill_root(Path.home() / ".codex"), Path.home() / ".agents/skills")
        with patch.dict(os.environ, {"CODEX_SKILL_DIR": "/tmp/isolated-skills"}):
            self.assertEqual(resolve_skill_root(Path("/tmp/custom-codex")), Path("/tmp/isolated-skills"))


class ConsistencyGuardTests(unittest.TestCase):
    def test_consistency_checks_reject_proprietary_frontmatter_bash_leak_missing_toc_and_2hop_refs(self):
        import check_consistency as consistency

        self.assertEqual(consistency.main(), 0)

        with tempfile.TemporaryDirectory(prefix="zhuzi-consistency-test-") as raw:
            temp_root = Path(raw)
            (temp_root / "AGENTS.md").write_text("---\ntrigger: always_on\n---\n# Bad frontmatter\n", encoding="utf-8")
            (temp_root / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            with patch.object(consistency, "ROOT", temp_root):
                root_errors: list[str] = []
                consistency.check_root_instruction_files(root_errors)
                self.assertTrue(any("YAML frontmatter" in err for err in root_errors), root_errors)

            # 1. Proprietary key + byte overflow + missing sidecar + >100L without TOC + orphan ref
            skill_dir = temp_root / "skills" / "demo-skill"
            (skill_dir / "references").mkdir(parents=True)
            bloated_desc = "测" * 400
            (skill_dir / "SKILL.md").write_text(
                f'---\nname: demo-skill\ndescription: "{bloated_desc}"\ndisable-model-invocation: true\n---\n\n# Demo\n\nSee [m](references/methodology.md).\n',
                encoding="utf-8",
            )
            (skill_dir / "references" / "methodology.md").write_text("# M\n" + "\n".join(f"line {i}" for i in range(120)), encoding="utf-8")
            (skill_dir / "references" / "orphan.md").write_text("# Orphan\n", encoding="utf-8")
            with patch.object(consistency, "ROOT", temp_root):
                meta_errors: list[str] = []
                consistency.check_skill_metadata(meta_errors, {"skills": []})
                self.assertTrue(any("1024 UTF-8 bytes" in err for err in meta_errors), meta_errors)
                self.assertTrue(any("non-portable" in err for err in meta_errors), meta_errors)
                self.assertTrue(any("agents/openai.yaml" in err for err in meta_errors), meta_errors)

                ref_errors: list[str] = []
                consistency.check_skill_progressive_references(ref_errors)
                self.assertTrue(any("orphan.md" in err for err in ref_errors), ref_errors)
                self.assertTrue(any("## 目录" in err for err in ref_errors), ref_errors)

            # 2. Reviewer subagent leaking Bash tool in Claude adapter
            claude_agents = temp_root / "runtimes" / "claude" / "agents"
            claude_agents.mkdir(parents=True)
            (claude_agents / "feynman-reviewer.md").write_text(
                '---\nname: feynman-reviewer\ndescription: "bad"\ntools: Read, Bash, Grep\nmaxTurns: 16\n---\nBody\n',
                encoding="utf-8",
            )
            fake_contract = {"seats": {"feynman-reviewer": {"skill": "feynman-explainer"}}}
            with patch.object(consistency, "ROOT", temp_root), patch.object(consistency, "CLAUDE_RUNTIME_ROOT", temp_root / "runtimes" / "claude"):
                agent_errors: list[str] = []
                consistency.check_claude_agent_adapters(agent_errors, fake_contract)
                self.assertTrue(any("Bash" in err for err in agent_errors), agent_errors)

            # 3. Shared workflow leaking runtime primitive
            wf_dir = temp_root / "zhuzi" / "workflows"
            wf_dir.mkdir(parents=True)
            (wf_dir / "roundtable.md").write_text("# Bad\ninvoke_subagent(TypeName='linus-engineer')\n", encoding="utf-8")
            (wf_dir / "quick-multi.md").write_text("# Quick\n", encoding="utf-8")
            with patch.object(consistency, "ROOT", temp_root), patch.object(
                consistency, "CLAUDE_RUNTIME_ROOT", temp_root / "runtimes" / "claude"
            ):
                wf_errors: list[str] = []
                consistency.check_workflow_adapters(wf_errors)
                self.assertTrue(any("invoke_subagent(" in err for err in wf_errors), wf_errors)


if __name__ == "__main__":
    unittest.main()
