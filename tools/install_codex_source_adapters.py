#!/usr/bin/env python3
"""Install Codex assets with verified backups, legacy migration and rollback.

Called by ``install.sh`` as part of the default shipped-surface install so
Codex skills, agents and shared assets are handled together. The shell installer
must not overwrite the previous Codex manifest before ownership is inspected.

Native agents use TOML. Fresh user installs discover skills in ``~/.agents/skills``.
Explicit install roots stay isolated; installed references always resolve to that root.
Only current manifest entries can be replaced or migrated; other packages and
provider/auth configuration are outside the installation plan.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

try:
    import tomllib
except ImportError:  # Python 3.10
    try:
        import tomli as tomllib
    except ImportError as exc:
        raise SystemExit("Python < 3.11 needs tomli; install requirements-dev.txt first") from exc


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "zhuzi" / "manifests" / "shipped-surface.json"
CODEX_AGENT_FAMILY = "codex_agents"
CODEX_SKILL_FAMILY = "codex_skills"


def render_text(text: str, *, skill_root: Path, shared_root: Path) -> str:
    return (
        text.replace("{{ZHUZI_SKILL_ROOT}}", str(skill_root))
        .replace("{{ZHUZI_SHARED_ROOT}}", str(shared_root))
    )


def collapse_repo_fallbacks(text: str) -> str:
    # Source adapters put repository fallbacks on their own line.
    return "\n".join(
        line for line in text.splitlines() if "`./skills" not in line and "`./zhuzi" not in line
    ) + "\n"


def render_file(src: Path, dst: Path, *, skill_root: Path, shared_root: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding="utf-8")
    # Decode TOML before inserting paths: quotes or backslashes in an install root
    # must remain instruction text rather than changing TOML syntax.
    if src.suffix == ".toml":
        payload = tomllib.loads(text)
        payload["developer_instructions"] = collapse_repo_fallbacks(
            render_text(payload["developer_instructions"], skill_root=skill_root, shared_root=shared_root)
        )
        rendered = "\n".join(f"{key} = {json.dumps(value, ensure_ascii=False)}" for key, value in payload.items()) + "\n"
        tomllib.loads(rendered)
    else:
        rendered = collapse_repo_fallbacks(render_text(text, skill_root=skill_root, shared_root=shared_root))
    dst.write_text(rendered, encoding="utf-8")


def copy_tree_with_render(src: Path, dst: Path, *, skill_root: Path, shared_root: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)

    for path in src.rglob("*"):
        target = dst / path.relative_to(src)
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if path.suffix == ".md":
            render_file(path, target, skill_root=skill_root, shared_root=shared_root)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def load_manifest_families() -> dict[str, list[dict[str, str]]]:
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    families = payload.get("families")
    if not isinstance(families, dict):
        raise ValueError(f"invalid manifest families object: {MANIFEST_PATH}")
    return families


def manifest_family_paths(
    families: dict[str, list[dict[str, str]]], family: str
) -> list[Path]:
    entries = families.get(family)
    if not isinstance(entries, list):
        raise ValueError(f"manifest missing family {family}: {MANIFEST_PATH}")

    resolved: list[Path] = []
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            raise ValueError(f"manifest family {family} entry {index} is not an object")

        raw_path = entry.get("path")
        if not isinstance(raw_path, str):
            raise ValueError(f"manifest family {family} entry {index} missing path")

        resolved_path = ROOT / raw_path
        if not resolved_path.exists():
            raise FileNotFoundError(
                f"manifest family {family} entry {index} points to missing path: {raw_path}"
            )
        resolved.append(resolved_path)

    return resolved


def resolve_skill_root(codex_home: Path) -> Path:
    override = os.environ.get("CODEX_SKILL_DIR")
    if override:
        return Path(override).expanduser().resolve()
    if os.environ.get("CODEX_HOME") or codex_home.resolve() != (Path.home() / ".codex").resolve():
        return codex_home.resolve() / "skills"
    return Path.home() / ".agents" / "skills"


def exists(path: Path) -> bool:
    return os.path.lexists(path)


def remove_entry(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def copy_entry(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_symlink():
        dst.symlink_to(os.readlink(src), target_is_directory=src.is_dir())
    elif src.is_dir():
        shutil.copytree(src, dst, symlinks=True)
    else:
        shutil.copy2(src, dst)


def entry_digest(path: Path) -> str | None:
    """Compare content, modes and links, without following links outside an asset."""
    if not exists(path):
        return None
    digest = hashlib.sha256()
    def visit(item: Path, relative: str) -> None:
        digest.update(relative.encode())
        if item.is_symlink():
            digest.update(b"link" + os.fsencode(os.readlink(item)))
        elif item.is_dir():
            digest.update(f"dir:{item.stat().st_mode & 0o777}".encode())
            for child in sorted(item.iterdir()):
                visit(child, relative + "/" + child.name)
        else:
            digest.update(f"file:{item.stat().st_mode & 0o777}".encode())
            with item.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    visit(path, "")
    return digest.hexdigest()


def previous_skill_names(codex_home: Path) -> set[str]:
    manifest = codex_home / "zhuzi/manifests/shipped-surface.json"
    if not manifest.is_file():
        return set()
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    families = payload.get("families")
    if not isinstance(families, dict):
        raise ValueError("installed shipped-surface manifest is invalid; nothing was migrated")
    names = set()
    for family in ("skills", CODEX_SKILL_FAMILY):
        for entry in families.get(family, []):
            name, raw = entry.get("entry", ""), entry.get("path", "")
            path = Path(raw)
            if (re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", name)
                    and not path.is_absolute() and ".." not in path.parts
                    and len(path.parts) >= 2 and path.parts[-2:] == (name, "SKILL.md")):
                names.add(name)
    return names


def skill_identity(path: Path) -> str | None:
    entry = path / "SKILL.md"
    if not entry.is_file():
        return None
    text = entry.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    frontmatter = text.split("---", 2)[1]
    match = re.search(r"^name:\s*(.+?)\s*$", frontmatter, re.MULTILINE)
    return match.group(1).strip("\"'") if match else None


def stage_assets(codex_home: Path, skill_root: Path, stage: Path) -> tuple[dict[Path, Path], list[Path]]:
    families = load_manifest_families()
    targets: dict[Path, Path] = {}
    for entry in manifest_family_paths(families, "skills"):
        src, dst = entry.parent, stage / "skills" / entry.parent.name
        shutil.copytree(src, dst, symlinks=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        targets[skill_root / src.name] = dst
    for entry in manifest_family_paths(families, CODEX_SKILL_FAMILY):
        src, dst = entry.parent, stage / "skills" / entry.parent.name
        copy_tree_with_render(src, dst, skill_root=skill_root, shared_root=codex_home / "zhuzi")
        targets[skill_root / src.name] = dst
    wrappers = []
    for src in manifest_family_paths(families, CODEX_AGENT_FAMILY):
        if src.suffix != ".toml":
            raise ValueError(f"Codex agent manifest entry must be TOML: {src}")
        dst = stage / "agents" / src.name
        render_file(src, dst, skill_root=skill_root, shared_root=codex_home / "zhuzi")
        targets[codex_home / "agents" / src.name] = dst
        wrappers.append(codex_home / "agents" / f"{src.stem}.md")
    shared = stage / "shared"
    shutil.copytree(ROOT / "zhuzi", shared, symlinks=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    targets[codex_home / "zhuzi"] = shared
    return targets, wrappers


def migration_candidates(codex_home: Path, skill_root: Path, targets: dict[Path, Path], wrappers: list[Path]) -> list[Path]:
    old_root = codex_home / "skills"
    owned = previous_skill_names(codex_home)
    legacy = [p for p in wrappers if exists(p)]
    if old_root.resolve() != skill_root.resolve():
        for target, staged in targets.items():
            if target.parent != skill_root:
                continue
            old = old_root / target.name
            if not exists(old):
                continue
            verified_owner = target.name in owned and skill_identity(old) == target.name
            if not verified_owner and entry_digest(old) != entry_digest(staged):
                raise ValueError(f"cannot confirm ownership of legacy skill {old}; installation left untouched")
            legacy.append(old)
    paths = list(targets) + legacy
    for index, path in enumerate(paths):
        if path == ROOT or ROOT in path.parents or path in ROOT.parents:
            raise ValueError(f"install destination overlaps repository source: {path}")
        for other in paths[index + 1:]:
            if path == other or path in other.parents or other in path.parents:
                raise ValueError(f"overlapping install/migration destinations: {path}, {other}")
    return legacy


def replace_entry(src: Path, dst: Path) -> None:
    """Prepare on the destination filesystem, then publish; backups precede this."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".zhuzi-stage-", dir=dst.parent) as raw:
        prepared = Path(raw) / "asset"
        copy_entry(src, prepared)
        remove_entry(dst)
        os.replace(prepared, dst)


def apply_install(targets: dict[Path, Path], legacy: list[Path], codex_home: Path, skill_root: Path) -> dict:
    changed = {dst: src for dst, src in targets.items() if entry_digest(dst) != entry_digest(src)}
    report = {"codex_home": str(codex_home), "skill_root": str(skill_root),
              "updated": [str(p) for p in changed], "migrated": [str(p) for p in legacy], "backup": None}
    if not changed and not legacy:
        return report
    backup_parent = codex_home / "backups/zhuzi"
    backup_parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-")
    backup = Path(tempfile.mkdtemp(prefix=stamp, dir=backup_parent))
    report["backup"] = str(backup)
    records = {}
    for index, path in enumerate([*changed, *legacy]):
        saved = backup / "assets" / f"{index:03d}-{path.name}"
        before = entry_digest(path)
        if exists(path):
            copy_entry(path, saved)
            if entry_digest(saved) != before:
                raise OSError(f"backup verification failed: {path}")
        records[path] = {"path": str(path), "backup": str(saved.relative_to(backup)) if before else None,
                         "before_sha256": before}
    journal = {**report, "status": "backed_up", "entries": list(records.values())}
    journal_path = backup / "migration.json"
    def save() -> None:
        journal_path.write_text(json.dumps(journal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    save()
    touched = []
    try:
        for path, staged in changed.items():
            if entry_digest(path) != records[path]["before_sha256"]:
                raise OSError(f"asset changed during migration: {path}")
            touched.append(path)
            replace_entry(staged, path)
        for path, staged in targets.items():
            if entry_digest(path) != entry_digest(staged):
                raise OSError(f"installed asset differs from staging: {path}")
        for path in legacy:
            if entry_digest(path) != records[path]["before_sha256"]:
                raise OSError(f"legacy asset changed during migration: {path}")
            touched.append(path)
            remove_entry(path)
        for path, staged in targets.items():
            if entry_digest(path) != entry_digest(staged):
                raise OSError(f"post-migration verification failed: {path}")
        journal["status"] = "complete"
        save()
    except BaseException:
        rollback_errors = []
        for path in reversed(touched):
            try:
                remove_entry(path)
                record = records[path]
                if record["backup"]:
                    copy_entry(backup / record["backup"], path)
                if entry_digest(path) != record["before_sha256"]:
                    raise OSError("restored content differs from backup")
            except OSError as exc:
                rollback_errors.append(f"{path}: {exc}")
        journal.update(status="rollback_failed" if rollback_errors else "rolled_back", rollback_errors=rollback_errors)
        save()
        if rollback_errors:
            raise RuntimeError(f"rollback incomplete; preserved backup: {backup}; {rollback_errors}")
        raise
    return report


def install_codex_assets(codex_home: Path, *, dry_run: bool = False) -> dict:
    codex_home = codex_home.expanduser().resolve()
    skill_root = resolve_skill_root(codex_home).resolve()
    with tempfile.TemporaryDirectory(prefix="zhuzi-install-stage-") as raw:
        targets, wrappers = stage_assets(codex_home, skill_root, Path(raw))
        if dry_run:
            legacy = migration_candidates(codex_home, skill_root, targets, wrappers)
            return {"codex_home": str(codex_home), "skill_root": str(skill_root), "dry_run": True,
                    "updated": [str(p) for p, src in targets.items() if entry_digest(p) != entry_digest(src)],
                    "migrated": [str(p) for p in legacy], "backup": None}
        import fcntl
        codex_home.mkdir(parents=True, exist_ok=True)
        with (codex_home / ".zhuzi-install.lock").open("a") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise RuntimeError("another zhuzi installation is running") from exc
            legacy = migration_candidates(codex_home, skill_root, targets, wrappers)
            return apply_install(targets, legacy, codex_home, skill_root)


def install_source_only_adapters(codex_home: Path, *, render_concrete: bool | None = None) -> list[Path]:
    # Retain the original callable for older local automation.
    result = install_codex_assets(codex_home)
    return [Path(path) for path in result["updated"]]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-skill-root", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true", help="machine-readable migration report")
    args = parser.parse_args()
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    if args.print_skill_root:
        print(resolve_skill_root(codex_home))
        return 0
    try:
        result = install_codex_assets(codex_home, dry_run=args.dry_run)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Codex installation failed: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for path in result["updated"]:
            print(f"  + {path}")
        for path in result["migrated"]:
            print(f"  - migrated legacy entry: {path}")
        if result["backup"]:
            print(f"  backup: {result['backup']}")
        print("Codex migration preview only." if args.dry_run else "Codex installation complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
