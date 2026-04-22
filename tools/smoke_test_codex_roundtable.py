#!/usr/bin/env python3
"""Manual smoke test for the Codex roundtable adapter.

This probe is intentionally heavier than ``check_consistency.py``:

1. Refresh shipped assets via ``./install.sh``
2. Render and install the source-only Codex roundtable adapters into ``$CODEX_HOME``
3. Verify installed adapter path references resolve
4. Run a minimal ``codex exec`` probe and assert the roundtable skill activates
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from install_codex_source_adapters import install_source_only_adapters


ROOT = Path(__file__).resolve().parents[1]

PROMPT = (
    "请触发本机 skill zhuzi-roundtable，但不要执行 roundtable、不要编辑文件、不要调用任何子 agent。"
    "只输出三行：第一行 SKILL_OK 或 SKILL_MISSING；第二行写你会优先读取的 workflow 路径；"
    "第三行写你会优先读取的 verdict schema 路径。"
)


class SmokeFailure(RuntimeError):
    """Raised when the Codex smoke test fails."""


def run_checked(
    cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise SmokeFailure(
            "command failed:\n"
            f"$ {' '.join(cmd)}\n"
            f"exit={result.returncode}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def build_install_env(*, codex_home: Path, claude_dir: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["CODEX_HOME"] = str(codex_home)
    env["CLAUDE_DIR"] = str(claude_dir)
    return env


def refresh_shipped_assets(*, install_env: dict[str, str]) -> None:
    run_checked(["./install.sh"], cwd=ROOT, env=install_env)


def collect_installed_files(*, codex_home: Path) -> list[Path]:
    installed_agent_dir = codex_home / "agents"
    installed_skill_dir = codex_home / "skills" / "zhuzi-roundtable"
    return [
        installed_skill_dir / "SKILL.md",
        installed_agent_dir / "linus-engineer.md",
        installed_agent_dir / "munger-reviewer.md",
        installed_agent_dir / "taleb-reviewer.md",
        installed_agent_dir / "lopezdeprado-reviewer.md",
    ]


def validate_path_references(*, codex_home: Path) -> None:
    patterns = [
        re.compile(r"`(/[^`\n]+\.md)`"),
        re.compile(r"`\./([^`]+)`"),
    ]

    missing: list[tuple[Path, str, Path]] = []
    for file_path in collect_installed_files(codex_home=codex_home):
        text = file_path.read_text(encoding="utf-8")
        for pattern in patterns:
            for match in pattern.finditer(text):
                raw = match.group(0).strip("`")
                if raw.startswith("/"):
                    resolved = Path(raw)
                elif raw.startswith("./"):
                    resolved = ROOT / raw[2:]
                else:
                    continue

                if not resolved.exists():
                    missing.append((file_path, raw, resolved))

    if missing:
        details = "\n".join(
            f"- {path}: {raw} -> {resolved}" for path, raw, resolved in missing
        )
        raise SmokeFailure(f"installed adapter path references missing targets:\n{details}")


def ensure_codex_cli() -> str:
    codex = shutil.which("codex")
    if not codex:
        raise SmokeFailure("`codex` CLI not found in PATH")
    return codex


def run_codex_probe(codex_bin: str, *, codex_home: Path, install_env: dict[str, str]) -> None:
    installed_shared_root = codex_home / "zhuzi"
    expected_workflow = str(installed_shared_root / "workflows" / "roundtable.md")
    expected_schema = str(installed_shared_root / "references" / "verdict-schema.md")

    with tempfile.TemporaryDirectory(prefix="zhuzi-codex-smoke-") as tmp_dir:
        tmp_path = Path(tmp_dir)
        out_file = tmp_path / "last_message.txt"

        result = subprocess.run(
            [
                codex_bin,
                "exec",
                "-C",
                tmp_dir,
                "--skip-git-repo-check",
                "--ignore-rules",
                "--sandbox",
                "read-only",
                "-o",
                str(out_file),
                PROMPT,
            ],
            env=install_env,
            text=True,
            capture_output=True,
            check=False,
            timeout=180,
        )

        last_message = out_file.read_text(encoding="utf-8").strip() if out_file.exists() else ""
        if result.returncode != 0:
            raise SmokeFailure(
                "codex probe failed:\n"
                f"exit={result.returncode}\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}\n"
                f"last_message:\n{last_message}"
            )

        lines = [line.strip() for line in last_message.splitlines() if line.strip()]
        if lines[:3] != ["SKILL_OK", expected_workflow, expected_schema]:
            raise SmokeFailure(
                "unexpected codex probe output:\n"
                f"expected:\nSKILL_OK\n{expected_workflow}\n{expected_schema}\n\n"
                f"got:\n{last_message}\n\n"
                f"stderr:\n{result.stderr}"
            )


def main() -> int:
    try:
        codex_bin = ensure_codex_cli()
        with tempfile.TemporaryDirectory(prefix="zhuzi-codex-install-") as install_dir:
            install_root = Path(install_dir)
            codex_home = install_root / "codex-home"
            claude_dir = install_root / "claude-home"
            install_env = build_install_env(codex_home=codex_home, claude_dir=claude_dir)

            refresh_shipped_assets(install_env=install_env)
            install_source_only_adapters(codex_home, render_concrete=True)
            validate_path_references(codex_home=codex_home)
            run_codex_probe(codex_bin, codex_home=codex_home, install_env=install_env)
    except SmokeFailure as exc:
        print(f"Codex roundtable smoke failed:\n{exc}", file=sys.stderr)
        return 1

    print("Codex roundtable smoke passed.")
    print(f"codex={codex_bin}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
