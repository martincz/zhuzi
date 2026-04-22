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
CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
HOME = Path.home()

INSTALLED_AGENT_DIR = CODEX_HOME / "agents"
INSTALLED_SKILL_DIR = CODEX_HOME / "skills" / "zhuzi-roundtable"
INSTALLED_SHARED_ROOT = CODEX_HOME / "zhuzi"

PROMPT = (
    "请触发本机 skill zhuzi-roundtable，但不要执行 roundtable、不要编辑文件、不要调用任何子 agent。"
    "只输出三行：第一行 SKILL_OK 或 SKILL_MISSING；第二行写你会优先读取的 workflow 路径；"
    "第三行写你会优先读取的 verdict schema 路径。"
)


class SmokeFailure(RuntimeError):
    """Raised when the Codex smoke test fails."""


def run_checked(cmd: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=cwd,
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


def refresh_shipped_assets() -> None:
    run_checked(["./install.sh"], cwd=ROOT)


def collect_installed_files() -> list[Path]:
    return [
        INSTALLED_SKILL_DIR / "SKILL.md",
        INSTALLED_AGENT_DIR / "linus-engineer.md",
        INSTALLED_AGENT_DIR / "munger-reviewer.md",
        INSTALLED_AGENT_DIR / "taleb-reviewer.md",
        INSTALLED_AGENT_DIR / "lopezdeprado-reviewer.md",
    ]


def validate_path_references() -> None:
    patterns = [
        re.compile(r"`(/[^`\n]+\.md)`"),
        re.compile(r"`\./([^`]+)`"),
    ]

    missing: list[tuple[Path, str, Path]] = []
    for file_path in collect_installed_files():
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


def run_codex_probe(codex_bin: str) -> None:
    expected_workflow = str(INSTALLED_SHARED_ROOT / "workflows" / "roundtable.md")
    expected_schema = str(INSTALLED_SHARED_ROOT / "references" / "verdict-schema.md")

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
        refresh_shipped_assets()
        install_source_only_adapters(CODEX_HOME)
        validate_path_references()
        run_codex_probe(codex_bin)
    except SmokeFailure as exc:
        print(f"Codex roundtable smoke failed:\n{exc}", file=sys.stderr)
        return 1

    print("Codex roundtable smoke passed.")
    print(f"codex={codex_bin}")
    print(f"workflow={INSTALLED_SHARED_ROOT / 'workflows' / 'roundtable.md'}")
    print(f"schema={INSTALLED_SHARED_ROOT / 'references' / 'verdict-schema.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
