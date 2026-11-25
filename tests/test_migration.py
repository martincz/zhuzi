"""Legacy-directory migration must preserve unrelated data, clean scattered skills, and recover from failures."""
from __future__ import annotations

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
import install_codex_source_adapters as installer


def seed(root: Path, *, symlink: bool = False, crlf: bool = False):
    home, skills = root / "codex", root / "agents/skills"
    old = home / "skills"
    old.mkdir(parents=True)
    source_manifest = json.loads(installer.MANIFEST_PATH.read_text())
    previous = {
        "families": {
            "skills": [next(e for e in source_manifest["families"]["skills"] if e["entry"] == "linus-torvalds-engineer")],
            "codex_skills": [{"entry": "zhuzi-quick", "path": "runtimes/codex/skills/zhuzi-quick/SKILL.md", "role": "legacy"}],
        }
    }
    (home / "zhuzi/manifests").mkdir(parents=True)
    (home / "zhuzi/manifests/shipped-surface.json").write_text(json.dumps(previous))
    (home / "zhuzi/old-contract.txt").write_text("old installed shared assets")
    nl = "\r\n" if crlf else "\n"
    for name in ("linus-torvalds-engineer", "zhuzi-quick"):
        dst = root / "external" / name if symlink else old / name
        dst.mkdir(parents=True)
        (dst / "SKILL.md").write_text(f'---{nl}name: "{name}"{nl}---{nl}old installed skill{nl}')
        (dst / "local-notes.txt").write_text("preserve my local additions in the backup")
        if symlink:
            (old / name).symlink_to(dst, target_is_directory=True)
    (home / "agents").mkdir()
    (home / "agents/linus-engineer.md").write_text("legacy zhuzi adapter")
    (home / "agents/other-agent.md").write_text("do not touch")
    (old / "other-skill").mkdir()
    (old / "other-skill/SKILL.md").write_text("unrelated user skill")
    (home / "config.toml").write_text('model = "unchanged"\n')
    (home / "auth.json").write_text('{"fixture": "unchanged"}')
    env = {
        "CODEX_HOME": str(home),
        "CODEX_SKILL_DIR": str(skills),
        "CLAUDE_DIR": str(root / "claude"),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    return home, skills, env


def snapshot_unrelated(home: Path):
    paths = [home / "config.toml", home / "auth.json", home / "agents/other-agent.md", home / "skills/other-skill"]
    return {p: installer.entry_digest(p) for p in paths}


class MigrationTests(unittest.TestCase):
    def test_cli_preview_then_migration_backup_and_idempotent_rerun(self):
        with tempfile.TemporaryDirectory(prefix="zhuzi-migrate-test-") as raw:
            root = Path(raw)
            home, skills, overrides = seed(root)
            # Scattered copy in current skill_root from v2 flat install must also be archived & consolidated into zhuzi/
            conflict = skills / "linus-torvalds-engineer"
            conflict.mkdir(parents=True)
            (conflict / "SKILL.md").write_text("locally modified destination copy")
            unrelated_top = skills / "impeccable"
            unrelated_top.mkdir(parents=True)
            (unrelated_top / "SKILL.md").write_text("---\nname: impeccable\n---\nkeep untouched\n")

            untouched = snapshot_unrelated(home)
            before = installer.entry_digest(home)
            env = {**os.environ, **overrides}
            cmd = ["bash", "install.sh", "--codex-only", "--json"]
            preview = subprocess.run([*cmd, "--dry-run"], cwd=ROOT, env=env, text=True, capture_output=True, check=True)
            self.assertEqual(len(json.loads(preview.stdout)["migrated"]), 4)
            self.assertEqual(installer.entry_digest(home), before)
            self.assertFalse((root / "claude").exists())

            result = json.loads(subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True, check=True).stdout)
            backup = Path(result["backup"])
            journal = json.loads((backup / "migration.json").read_text())
            self.assertEqual(journal["status"], "complete")
            self.assertFalse((home / "skills/linus-torvalds-engineer").exists())
            self.assertFalse((home / "skills/zhuzi-quick").exists())
            self.assertFalse((skills / "linus-torvalds-engineer").exists())
            self.assertFalse((home / "agents/linus-engineer.md").exists())
            self.assertTrue((skills / "zhuzi/SKILL.md").is_file())
            self.assertTrue((skills / "impeccable/SKILL.md").is_file())
            self.assertEqual(snapshot_unrelated(home), untouched)

            records = {e["path"]: e for e in journal["entries"]}
            saved_old = backup / records[str(home / "skills/linus-torvalds-engineer")]["backup"]
            self.assertTrue((saved_old / "local-notes.txt").is_file())
            saved_conflict = backup / records[str(conflict)]["backup"]
            self.assertEqual((saved_conflict / "SKILL.md").read_text(), "locally modified destination copy")
            self.assertTrue((backup / records[str(home / "zhuzi")]["backup"] / "old-contract.txt").exists())

            count = len(list((home / "backups/zhuzi").iterdir()))
            repeat = json.loads(subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True, check=True).stdout)
            self.assertEqual(repeat["updated"], [])
            self.assertEqual(repeat["migrated"], [])
            self.assertIsNone(repeat["backup"])
            self.assertEqual(len(list((home / "backups/zhuzi").iterdir())), count)

    def test_crlf_legacy_skill_ownership_is_recognized_and_migrated(self):
        with tempfile.TemporaryDirectory(prefix="zhuzi-crlf-test-") as raw:
            home, skills, env = seed(Path(raw), crlf=True)
            self.assertEqual(installer.skill_identity(home / "skills/linus-torvalds-engineer"), "linus-torvalds-engineer")
            with patch.dict(os.environ, env):
                result = installer.install_codex_assets(home)
            self.assertFalse((home / "skills/linus-torvalds-engineer").exists())
            self.assertTrue((skills / "zhuzi/SKILL.md").is_file())
            self.assertIsNotNone(result["backup"])

    def test_claude_legacy_commands_and_scattered_skills_migrate_cleanly(self):
        with tempfile.TemporaryDirectory(prefix="zhuzi-claude-mig-") as raw:
            root = Path(raw)
            claude_dir = root / "claude"
            (claude_dir / "commands/zhuzi").mkdir(parents=True)
            (claude_dir / "commands/zhuzi/roundtable.md").write_text("legacy command")
            (claude_dir / "skills/munger-checklist").mkdir(parents=True)
            (claude_dir / "skills/munger-checklist/SKILL.md").write_text("---\nname: munger-checklist\n---\nold flat skill\n")
            (claude_dir / "skills/custom-user-skill").mkdir(parents=True)
            (claude_dir / "skills/custom-user-skill/SKILL.md").write_text("---\nname: custom-user-skill\n---\nkeep\n")

            res = installer.install_claude_assets(claude_dir)
            self.assertFalse((claude_dir / "commands/zhuzi").exists())
            self.assertFalse((claude_dir / "skills/munger-checklist").exists())
            self.assertTrue((claude_dir / "skills/zhuzi/SKILL.md").is_file())
            self.assertTrue((claude_dir / "skills/custom-user-skill/SKILL.md").is_file())
            self.assertIsNotNone(res["backup"])

    def test_failed_install_rolls_back_already_replaced_assets(self):
        with tempfile.TemporaryDirectory(prefix="zhuzi-rollback-test-") as raw:
            home, skills, env = seed(Path(raw))
            original_shared = installer.entry_digest(home / "zhuzi")
            old = installer.entry_digest(home / "skills/linus-torvalds-engineer")
            unrelated = snapshot_unrelated(home)
            real_replace = installer.replace_entry
            calls = 0

            def fail_second(src, dst):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected copy failure")
                real_replace(src, dst)

            with patch.dict(os.environ, env), patch.object(installer, "replace_entry", side_effect=fail_second):
                with self.assertRaisesRegex(OSError, "injected"):
                    installer.install_codex_assets(home)
            self.assertEqual(installer.entry_digest(home / "zhuzi"), original_shared)
            self.assertEqual(installer.entry_digest(home / "skills/linus-torvalds-engineer"), old)
            self.assertEqual(snapshot_unrelated(home), unrelated)
            self.assertFalse((skills / "zhuzi").exists())
            journal = next((home / "backups/zhuzi").glob("*/migration.json"))
            self.assertEqual(json.loads(journal.read_text())["status"], "rolled_back")

    def test_cleanup_failure_restores_legacy_entries_and_shared_manifest(self):
        with tempfile.TemporaryDirectory(prefix="zhuzi-cleanup-test-") as raw:
            home, skills, env = seed(Path(raw))
            before = {
                p: installer.entry_digest(p)
                for p in (home / "zhuzi", home / "skills/linus-torvalds-engineer", home / "skills/zhuzi-quick", home / "agents/linus-engineer.md")
            }
            failing = home / "skills/zhuzi-quick"
            real_remove = installer.remove_entry
            failed = False

            def fail_once(path):
                nonlocal failed
                if path == failing and not failed:
                    failed = True
                    raise OSError("injected cleanup failure")
                return real_remove(path)

            with patch.dict(os.environ, env), patch.object(installer, "remove_entry", side_effect=fail_once):
                with self.assertRaisesRegex(OSError, "injected cleanup"):
                    installer.install_codex_assets(home)
            self.assertEqual({p: installer.entry_digest(p) for p in before}, before)
            self.assertFalse((skills / "zhuzi").exists())

    def test_symlink_migration_preserves_external_targets_and_links_in_backup(self):
        with tempfile.TemporaryDirectory(prefix="zhuzi-links-test-") as raw:
            root = Path(raw)
            home, skills, env = seed(root, symlink=True)
            external = installer.entry_digest(root / "external")
            with patch.dict(os.environ, env):
                result = installer.install_codex_assets(home)
            self.assertEqual(installer.entry_digest(root / "external"), external)
            self.assertFalse(os.path.lexists(home / "skills/linus-torvalds-engineer"))
            journal = json.loads((Path(result["backup"]) / "migration.json").read_text())
            record = next(e for e in journal["entries"] if e["path"] == str(home / "skills/linus-torvalds-engineer"))
            self.assertTrue((Path(result["backup"]) / record["backup"]).is_symlink())
            self.assertFalse((skills / "zhuzi").is_symlink())

    def test_unknown_legacy_ownership_aborts_without_changing_assets(self):
        with tempfile.TemporaryDirectory(prefix="zhuzi-unknown-test-") as raw:
            home, skills, env = seed(Path(raw))
            (home / "zhuzi/manifests/shipped-surface.json").write_text('{"families": {}}')
            before = installer.entry_digest(home / "skills")
            with patch.dict(os.environ, env):
                with self.assertRaisesRegex(ValueError, "cannot confirm ownership"):
                    installer.install_codex_assets(home)
            self.assertEqual(installer.entry_digest(home / "skills"), before)
            self.assertFalse(skills.exists())
            self.assertFalse((home / "backups").exists())

    def test_same_skill_root_consolidates_into_zhuzi_without_touching_unrelated_skills(self):
        with tempfile.TemporaryDirectory(prefix="zhuzi-same-root-test-") as raw:
            home, skills, env = seed(Path(raw))
            env["CODEX_SKILL_DIR"] = str(home / "skills")
            with patch.dict(os.environ, env):
                result = installer.install_codex_assets(home)
            self.assertIn(str(home / "agents/linus-engineer.md"), result["migrated"])
            self.assertFalse((home / "skills/linus-torvalds-engineer").exists())
            self.assertTrue((home / "skills/zhuzi/SKILL.md").is_file())
            self.assertTrue((home / "skills/other-skill/SKILL.md").exists())

    def test_overlapping_destinations_are_rejected(self):
        with tempfile.TemporaryDirectory(prefix="zhuzi-overlap-test-") as raw:
            home, skills, env = seed(Path(raw))
            env["CODEX_SKILL_DIR"] = str(home / "zhuzi/skills")
            with patch.dict(os.environ, env):
                with self.assertRaisesRegex(ValueError, "overlapping"):
                    installer.install_codex_assets(home)
            self.assertFalse((home / "zhuzi/skills").exists())


if __name__ == "__main__":
    unittest.main()
