#!/usr/bin/env python3
"""Transactional dual-runtime installer for zhuzi (Claude Code + OpenAI Codex).

Installs a single clean ``zhuzi/`` umbrella skill directory by default (bundling
runtime persona guides under ``zhuzi/personas/<name>/PERSONA.md`` while excluding
``references/research/`` and historical build drafts), renders concrete paths for
all 7 subagent seats, supports ``--pin`` / ``--unpin`` for standalone top-level
skill shortcuts, and migrates legacy scattered skill directories with verified
SHA-256 backups and automatic rollback.
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
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from render_roundtable_contract_docs import render_claude_skill_overlay, serialize_agent_toml

MANIFEST_PATH = ROOT / "zhuzi" / "manifests" / "shipped-surface.json"
CODEX_AGENT_FAMILY = "codex_agents"
CLAUDE_AGENT_FAMILY = "agents"
CLAUDE_SKILL_FAMILY = "claude_skills"
SKILL_NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", re.DOTALL)

KNOWN_RETIRED_SKILLS = {
    "zhuzi-roundtable",
    "zhuzi-quick",
    "linus-torvalds-perspective",
    "munger-perspective",
    "luxun-zawen",
}


def render_text(text: str, *, skill_root: Path, shared_root: Path) -> str:
    return (
        text.replace("{{ZHUZI_SKILL_ROOT}}", str(skill_root))
        .replace("{{ZHUZI_SHARED_ROOT}}", str(shared_root))
    )


def collapse_repo_fallbacks(text: str) -> str:
    return "\n".join(
        line
        for line in text.splitlines()
        if "`./skills" not in line and "`./zhuzi" not in line and "`../" not in line
    ) + "\n"


def strip_frontmatter(text: str) -> str:
    match = FRONTMATTER_RE.match(text)
    return text[match.end():].lstrip("\r\n") if match else text


def render_file(src: Path, dst: Path, *, skill_root: Path, shared_root: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding="utf-8")
    if src.suffix == ".toml":
        payload = tomllib.loads(text)
        payload["developer_instructions"] = collapse_repo_fallbacks(
            render_text(payload["developer_instructions"], skill_root=skill_root, shared_root=shared_root)
        )
        rendered = serialize_agent_toml(payload)
    else:
        rendered = collapse_repo_fallbacks(render_text(text, skill_root=skill_root, shared_root=shared_root))
    dst.write_text(rendered, encoding="utf-8")


def load_surface_payload() -> dict[str, object]:
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"invalid manifest object: {MANIFEST_PATH}")
    return payload


def load_manifest_families() -> dict[str, list[dict[str, object]]]:
    payload = load_surface_payload()
    families = payload.get("families")
    if not isinstance(families, dict):
        raise ValueError(f"invalid manifest families object: {MANIFEST_PATH}")
    return families


def load_runtime_exclusions() -> tuple[set[str], set[str], tuple[str, ...]]:
    payload = load_surface_payload()
    raw = payload.get("runtime_exclusions", {})
    if not isinstance(raw, dict):
        return {"references/research", "references/sources"}, set(), (":Zone.Identifier", ".pyc")
    subdirs = {str(x).strip("/") for x in raw.get("skill_subdirs", [])}
    filenames = {str(x) for x in raw.get("filenames", [])}
    suffixes = tuple(str(x) for x in raw.get("suffixes", []))
    return subdirs, filenames, suffixes


def manifest_family_paths(
    families: dict[str, list[dict[str, object]]], family: str
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


def resolve_skill_entry_name(name_or_alias: str, families: dict[str, list[dict[str, object]]]) -> str:
    target = name_or_alias.strip().lower()
    for item in families.get("skills", []):
        if not isinstance(item, dict):
            continue
        entry = item.get("entry")
        aliases = item.get("aliases", [])
        if entry == target or (isinstance(aliases, list) and target in aliases):
            if entry == "zhuzi":
                raise ValueError("umbrella skill 'zhuzi' is always installed by default and does not need --pin")
            return str(entry)
    raise ValueError(f"unknown zhuzi skill or alias: {name_or_alias!r}")


def resolve_skill_root(codex_home: Path) -> Path:
    override = os.environ.get("CODEX_SKILL_DIR")
    if override:
        return Path(override).expanduser().resolve()
    if os.environ.get("CODEX_HOME") or codex_home.resolve() != (Path.home() / ".codex").resolve():
        return codex_home.resolve() / "skills"
    return Path.home() / ".agents" / "skills"


def resolve_claude_dir(claude_dir: Path | None = None) -> Path:
    if claude_dir is not None:
        return claude_dir.expanduser().resolve()
    override = os.environ.get("CLAUDE_DIR")
    if override:
        return Path(override).expanduser().resolve()
    return (Path.home() / ".claude").resolve()


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


def is_excluded_skill_relpath(
    rel_posix: str,
    *,
    excluded_subdirs: set[str],
    excluded_filenames: set[str],
    excluded_suffixes: tuple[str, ...],
) -> bool:
    parts = rel_posix.split("/")
    if "__pycache__" in parts:
        return True
    filename = parts[-1]
    if filename in excluded_filenames or any(filename.endswith(sfx) for sfx in excluded_suffixes):
        return True
    for sub in excluded_subdirs:
        if rel_posix == sub or rel_posix.startswith(sub + "/"):
            return True
    return False


def copy_filtered_skill_refs(src_skill_dir: Path, dst_dir: Path) -> None:
    excluded_subdirs, excluded_filenames, excluded_suffixes = load_runtime_exclusions()
    ref_root = src_skill_dir / "references"
    if not ref_root.is_dir():
        return
    for item in sorted(ref_root.rglob("*")):
        if not item.is_file():
            continue
        rel_posix = item.relative_to(src_skill_dir).as_posix()
        if is_excluded_skill_relpath(
            rel_posix,
            excluded_subdirs=excluded_subdirs,
            excluded_filenames=excluded_filenames,
            excluded_suffixes=excluded_suffixes,
        ):
            continue
        out = dst_dir / rel_posix
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, out)


def copy_clean_shared_zhuzi(dst_shared: Path) -> None:
    _, _, excluded_suffixes = load_runtime_exclusions()
    src_shared = ROOT / "zhuzi"
    for item in sorted(src_shared.rglob("*")):
        if not item.is_file():
            continue
        rel_parts = item.relative_to(src_shared).parts
        if "__pycache__" in rel_parts or any(item.name.endswith(sfx) for sfx in excluded_suffixes):
            continue
        out = dst_shared / item.relative_to(src_shared)
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, out)


def read_pinned_skills(runtime_home: Path, families: dict[str, list[dict[str, object]]]) -> set[str]:
    pin_file = runtime_home / "pinned-skills.json"
    if not pin_file.is_file():
        return set()
    try:
        data = json.loads(pin_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()
    valid = {
        str(item["entry"])
        for item in families.get("skills", [])
        if isinstance(item, dict) and not item.get("default_install", False)
    }
    raw_list = data.get("pinned", []) if isinstance(data, dict) else []
    return {str(name) for name in raw_list if isinstance(name, str) and str(name) in valid}


def compute_desired_pins(
    runtime_home: Path,
    families: dict[str, list[dict[str, object]]],
    *,
    pin: list[str] | None = None,
    unpin: list[str] | None = None,
) -> set[str]:
    desired = read_pinned_skills(runtime_home, families)
    for item in pin or []:
        desired.add(resolve_skill_entry_name(item, families))
    for item in unpin or []:
        desired.discard(resolve_skill_entry_name(item, families))
    return desired


def previous_skill_names(runtime_home: Path) -> set[str]:
    manifest = runtime_home / "zhuzi" / "manifests" / "shipped-surface.json"
    if not manifest.is_file():
        return set()
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    families = payload.get("families")
    if not isinstance(families, dict):
        raise ValueError("installed shipped-surface manifest is invalid; nothing was migrated")
    names: set[str] = set()
    for family in ("skills", "codex_skills", "claude_skills"):
        for entry in families.get(family, []):
            if not isinstance(entry, dict):
                continue
            name = entry.get("entry", "")
            raw = entry.get("path", "")
            if not isinstance(name, str) or not isinstance(raw, str):
                continue
            path = Path(raw)
            if (
                SKILL_NAME_RE.fullmatch(name)
                and len(name) <= 64
                and not path.is_absolute()
                and ".." not in path.parts
                and len(path.parts) >= 2
                and path.parts[-2:] == (name, "SKILL.md")
            ):
                names.add(name)
    return names


def skill_identity(path: Path) -> str | None:
    entry = path / "SKILL.md"
    if not entry.is_file():
        return None
    text = entry.read_text(encoding="utf-8", errors="replace")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    name_match = re.search(r"^name:\s*(.+?)\s*$", match.group(1), re.MULTILINE)
    if not name_match:
        return None
    candidate = name_match.group(1).strip().strip("\"'")
    return candidate if SKILL_NAME_RE.fullmatch(candidate) and len(candidate) <= 64 else None


def build_umbrella_zhuzi_dir(
    stage_zhuzi: Path,
    *,
    runtime: str,
    persona_install_root: Path,
    shared_install_root: Path,
    families: dict[str, list[dict[str, object]]],
) -> None:
    stage_zhuzi.mkdir(parents=True, exist_ok=True)
    if runtime == "claude":
        umbrella_src = ROOT / "runtimes" / "claude" / "skills" / "zhuzi" / "SKILL.md"
    else:
        umbrella_src = ROOT / "skills" / "zhuzi" / "SKILL.md"

    render_file(
        umbrella_src,
        stage_zhuzi / "SKILL.md",
        skill_root=persona_install_root,
        shared_root=shared_install_root,
    )
    copy_filtered_skill_refs(ROOT / "skills" / "zhuzi", stage_zhuzi)
    if runtime == "codex":
        sidecar_src = ROOT / "skills" / "zhuzi" / "agents" / "openai.yaml"
        sidecar_dst = stage_zhuzi / "agents" / "openai.yaml"
        sidecar_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(sidecar_src, sidecar_dst)

    for item in families.get("skills", []):
        if not isinstance(item, dict) or item.get("default_install", False):
            continue
        entry = str(item["entry"])
        src_dir = ROOT / "skills" / entry
        persona_dst = stage_zhuzi / "personas" / entry
        persona_dst.mkdir(parents=True, exist_ok=True)
        persona_body = strip_frontmatter((src_dir / "SKILL.md").read_text(encoding="utf-8"))
        (persona_dst / "PERSONA.md").write_text(persona_body, encoding="utf-8")
        copy_filtered_skill_refs(src_dir, persona_dst)


def build_pinned_skill_dir(
    stage_skill_dst: Path,
    *,
    skill_entry: dict[str, object],
    runtime: str,
) -> None:
    entry = str(skill_entry["entry"])
    src_dir = ROOT / "skills" / entry
    stage_skill_dst.mkdir(parents=True, exist_ok=True)
    raw_skill_md = (src_dir / "SKILL.md").read_text(encoding="utf-8")
    if runtime == "claude":
        rendered_md = render_claude_skill_overlay(raw_skill_md, skill_entry)
        (stage_skill_dst / "SKILL.md").write_text(rendered_md, encoding="utf-8")
    else:
        (stage_skill_dst / "SKILL.md").write_text(raw_skill_md, encoding="utf-8")
        sidecar_src = src_dir / "agents" / "openai.yaml"
        if sidecar_src.is_file():
            sidecar_dst = stage_skill_dst / "agents" / "openai.yaml"
            sidecar_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(sidecar_src, sidecar_dst)
    copy_filtered_skill_refs(src_dir, stage_skill_dst)


def stage_codex_assets(
    codex_home: Path,
    skill_root: Path,
    stage: Path,
    *,
    desired_pins: set[str],
) -> tuple[dict[Path, Path], list[Path]]:
    families = load_manifest_families()
    targets: dict[Path, Path] = {}
    persona_root = skill_root / "zhuzi" / "personas"
    shared_root = codex_home / "zhuzi"

    umbrella_stage = stage / "skills" / "zhuzi"
    build_umbrella_zhuzi_dir(
        umbrella_stage,
        runtime="codex",
        persona_install_root=persona_root,
        shared_install_root=shared_root,
        families=families,
    )
    targets[skill_root / "zhuzi"] = umbrella_stage

    skills_by_entry = {str(s["entry"]): s for s in families.get("skills", []) if isinstance(s, dict)}
    for pinned_name in sorted(desired_pins):
        pin_stage = stage / "skills" / pinned_name
        build_pinned_skill_dir(pin_stage, skill_entry=skills_by_entry[pinned_name], runtime="codex")
        targets[skill_root / pinned_name] = pin_stage

    if desired_pins or (codex_home / "pinned-skills.json").exists():
        pin_meta = stage / "pinned-skills.json"
        pin_meta.write_text(
            json.dumps({"pinned": sorted(desired_pins)}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        targets[codex_home / "pinned-skills.json"] = pin_meta

    wrappers: list[Path] = []
    for src in manifest_family_paths(families, CODEX_AGENT_FAMILY):
        if src.suffix != ".toml":
            raise ValueError(f"Codex agent manifest entry must be TOML: {src}")
        dst = stage / "agents" / src.name
        render_file(src, dst, skill_root=persona_root, shared_root=shared_root)
        targets[codex_home / "agents" / src.name] = dst
        wrappers.append(codex_home / "agents" / f"{src.stem}.md")

    shared_stage = stage / "shared"
    copy_clean_shared_zhuzi(shared_stage)
    targets[shared_root] = shared_stage
    return targets, wrappers


def stage_claude_assets(
    claude_dir: Path,
    stage: Path,
    *,
    desired_pins: set[str],
) -> tuple[dict[Path, Path], list[Path]]:
    families = load_manifest_families()
    targets: dict[Path, Path] = {}
    skill_root = claude_dir / "skills"
    persona_root = skill_root / "zhuzi" / "personas"
    shared_root = claude_dir / "zhuzi"

    umbrella_stage = stage / "skills" / "zhuzi"
    build_umbrella_zhuzi_dir(
        umbrella_stage,
        runtime="claude",
        persona_install_root=persona_root,
        shared_install_root=shared_root,
        families=families,
    )
    targets[skill_root / "zhuzi"] = umbrella_stage

    skills_by_entry = {str(s["entry"]): s for s in families.get("skills", []) if isinstance(s, dict)}
    for pinned_name in sorted(desired_pins):
        pin_stage = stage / "skills" / pinned_name
        build_pinned_skill_dir(pin_stage, skill_entry=skills_by_entry[pinned_name], runtime="claude")
        targets[skill_root / pinned_name] = pin_stage

    if desired_pins or (claude_dir / "pinned-skills.json").exists():
        pin_meta = stage / "pinned-skills.json"
        pin_meta.write_text(
            json.dumps({"pinned": sorted(desired_pins)}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        targets[claude_dir / "pinned-skills.json"] = pin_meta

    for src in manifest_family_paths(families, CLAUDE_AGENT_FAMILY):
        dst = stage / "agents" / src.name
        render_file(src, dst, skill_root=persona_root, shared_root=shared_root)
        targets[claude_dir / "agents" / src.name] = dst

    shared_stage = stage / "shared"
    copy_clean_shared_zhuzi(shared_stage)
    targets[shared_root] = shared_stage

    legacy_Namespace_dirs = [claude_dir / "commands" / "zhuzi"]
    return targets, legacy_Namespace_dirs


def source_skill_digest_cache(families: dict[str, list[dict[str, object]]]) -> dict[str, set[str]]:
    digests: dict[str, set[str]] = {}
    with tempfile.TemporaryDirectory(prefix="zhuzi-src-digest-") as raw:
        tmp = Path(raw)
        for item in families.get("skills", []):
            if not isinstance(item, dict):
                continue
            entry = str(item["entry"])
            src = ROOT / "skills" / entry
            d_raw = entry_digest(src)
            s_set = {d_raw} if d_raw else set()
            for rt in ("codex", "claude"):
                p_dir = tmp / rt / entry
                build_pinned_skill_dir(p_dir, skill_entry=item, runtime=rt)
                d_pin = entry_digest(p_dir)
                if d_pin:
                    s_set.add(d_pin)
            digests[entry] = s_set
    return digests


def migration_candidates(
    runtime_home: Path,
    skill_root: Path,
    targets: dict[Path, Path],
    extra_legacy_paths: list[Path],
    *,
    desired_pins: set[str],
) -> list[Path]:
    families = load_manifest_families()
    known_skill_names = {
        str(item["entry"])
        for item in families.get("skills", [])
        if isinstance(item, dict) and not item.get("default_install", False)
    } | KNOWN_RETIRED_SKILLS

    has_installed_manifest = (runtime_home / "zhuzi" / "manifests" / "shipped-surface.json").is_file()
    owned = previous_skill_names(runtime_home) | read_pinned_skills(runtime_home, families)
    known_digests = source_skill_digest_cache(families)

    legacy: list[Path] = [p for p in extra_legacy_paths if exists(p)]
    seen_legacy = {p.resolve() if not p.is_symlink() else p for p in legacy}

    # 1. Check deprecated $CODEX_HOME/skills when distinct from skill_root
    old_root = runtime_home / "skills"
    if old_root.resolve() != skill_root.resolve() and old_root.is_dir():
        for name in sorted(known_skill_names | {"zhuzi"}):
            old = old_root / name
            if not exists(old) or old in targets:
                continue
            verified_owner = name in owned and skill_identity(old) == name
            digest_matches = entry_digest(old) in known_digests.get(name, set())
            if not verified_owner and not digest_matches:
                raise ValueError(f"cannot confirm ownership of legacy skill {old}; installation left untouched")
            legacy.append(old)
            seen_legacy.add(old)

    # 2. Check scattered top-level zhuzi skills in skill_root that are not currently pinned
    if skill_root.is_dir():
        for name in sorted(known_skill_names - desired_pins):
            cand = skill_root / name
            if not exists(cand) or cand in targets or cand in seen_legacy:
                continue
            ident = skill_identity(cand)
            digest_matches = entry_digest(cand) in known_digests.get(name, set())
            if name in owned and (ident == name or ident is None):
                legacy.append(cand)
            elif not has_installed_manifest and ident == name:
                legacy.append(cand)
            elif digest_matches:
                legacy.append(cand)
            else:
                raise ValueError(f"cannot confirm ownership of legacy skill {cand}; installation left untouched")

    paths = list(targets) + legacy
    for index, path in enumerate(paths):
        if path == ROOT or ROOT in path.parents or path in ROOT.parents:
            raise ValueError(f"install destination overlaps repository source: {path}")
        for other in paths[index + 1:]:
            if path == other or path in other.parents or other in path.parents:
                raise ValueError(f"overlapping install/migration destinations: {path}, {other}")
    return legacy


def uninstall_candidates(runtime_home: Path, skill_root: Path, *, runtime: str) -> list[Path]:
    families = load_manifest_families()
    owned = previous_skill_names(runtime_home) | read_pinned_skills(runtime_home, families) | {"zhuzi"}
    candidates: list[Path] = []
    for skill_name in sorted(owned | KNOWN_RETIRED_SKILLS):
        cand = skill_root / skill_name
        if exists(cand) and (skill_name in owned or skill_identity(cand) == skill_name):
            candidates.append(cand)
    agent_family = CLAUDE_AGENT_FAMILY if runtime == "claude" else CODEX_AGENT_FAMILY
    for src in manifest_family_paths(families, agent_family):
        agent_dst = runtime_home / "agents" / src.name
        if exists(agent_dst):
            candidates.append(agent_dst)
    if runtime == "claude" and exists(runtime_home / "commands" / "zhuzi"):
        candidates.append(runtime_home / "commands" / "zhuzi")
    for meta in (runtime_home / "pinned-skills.json", runtime_home / "zhuzi"):
        if exists(meta):
            candidates.append(meta)
    return candidates


def replace_entry(src: Path, dst: Path) -> None:
    """Prepare on the destination filesystem, then publish; backups precede this."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".zhuzi-stage-", dir=dst.parent) as raw:
        prepared = Path(raw) / "asset"
        copy_entry(src, prepared)
        remove_entry(dst)
        os.replace(prepared, dst)


def apply_install(
    targets: dict[Path, Path],
    legacy: list[Path],
    runtime_home: Path,
    skill_root: Path,
    *,
    home_key: str = "codex_home",
) -> dict[str, object]:
    changed = {dst: src for dst, src in targets.items() if entry_digest(dst) != entry_digest(src)}
    report: dict[str, object] = {
        home_key: str(runtime_home),
        "skill_root": str(skill_root),
        "updated": [str(p) for p in changed],
        "migrated": [str(p) for p in legacy],
        "backup": None,
    }
    if not changed and not legacy:
        return report

    backup_parent = runtime_home / "backups" / "zhuzi"
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
        records[path] = {
            "path": str(path),
            "backup": str(saved.relative_to(backup)) if before else None,
            "before_sha256": before,
        }

    journal = {**report, "status": "backed_up", "entries": list(records.values())}
    journal_path = backup / "migration.json"

    def save() -> None:
        journal_path.write_text(json.dumps(journal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    save()
    touched: list[Path] = []
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
        journal.update(
            status="rollback_failed" if rollback_errors else "rolled_back",
            rollback_errors=rollback_errors,
        )
        save()
        if rollback_errors:
            raise RuntimeError(f"rollback incomplete; preserved backup: {backup}; {rollback_errors}")
        raise
    return report


def install_codex_assets(
    codex_home: Path,
    *,
    dry_run: bool = False,
    pin: list[str] | None = None,
    unpin: list[str] | None = None,
    uninstall: bool = False,
) -> dict[str, object]:
    codex_home = codex_home.expanduser().resolve()
    skill_root = resolve_skill_root(codex_home).resolve()
    families = load_manifest_families()

    if uninstall:
        legacy = uninstall_candidates(codex_home, skill_root, runtime="codex")
        if dry_run:
            return {
                "codex_home": str(codex_home),
                "skill_root": str(skill_root),
                "dry_run": True,
                "updated": [],
                "migrated": [str(p) for p in legacy],
                "backup": None,
            }
        import fcntl
        codex_home.mkdir(parents=True, exist_ok=True)
        with (codex_home / ".zhuzi-install.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return apply_install({}, legacy, codex_home, skill_root, home_key="codex_home")

    desired_pins = compute_desired_pins(codex_home, families, pin=pin, unpin=unpin)
    with tempfile.TemporaryDirectory(prefix="zhuzi-install-stage-") as raw:
        targets, wrappers = stage_codex_assets(codex_home, skill_root, Path(raw), desired_pins=desired_pins)
        if dry_run:
            legacy = migration_candidates(
                codex_home, skill_root, targets, wrappers, desired_pins=desired_pins
            )
            return {
                "codex_home": str(codex_home),
                "skill_root": str(skill_root),
                "dry_run": True,
                "updated": [str(p) for p, src in targets.items() if entry_digest(p) != entry_digest(src)],
                "migrated": [str(p) for p in legacy],
                "backup": None,
            }
        import fcntl
        codex_home.mkdir(parents=True, exist_ok=True)
        with (codex_home / ".zhuzi-install.lock").open("a") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise RuntimeError("another zhuzi installation is running") from exc
            legacy = migration_candidates(
                codex_home, skill_root, targets, wrappers, desired_pins=desired_pins
            )
            return apply_install(targets, legacy, codex_home, skill_root, home_key="codex_home")


def install_claude_assets(
    claude_dir: Path | None = None,
    *,
    dry_run: bool = False,
    pin: list[str] | None = None,
    unpin: list[str] | None = None,
    uninstall: bool = False,
) -> dict[str, object]:
    resolved_claude = resolve_claude_dir(claude_dir)
    skill_root = resolved_claude / "skills"
    families = load_manifest_families()

    if uninstall:
        legacy = uninstall_candidates(resolved_claude, skill_root, runtime="claude")
        if dry_run:
            return {
                "claude_dir": str(resolved_claude),
                "skill_root": str(skill_root),
                "dry_run": True,
                "updated": [],
                "migrated": [str(p) for p in legacy],
                "backup": None,
            }
        import fcntl
        resolved_claude.mkdir(parents=True, exist_ok=True)
        with (resolved_claude / ".zhuzi-install.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return apply_install({}, legacy, resolved_claude, skill_root, home_key="claude_dir")

    desired_pins = compute_desired_pins(resolved_claude, families, pin=pin, unpin=unpin)
    with tempfile.TemporaryDirectory(prefix="zhuzi-claude-stage-") as raw:
        targets, legacy_dirs = stage_claude_assets(resolved_claude, Path(raw), desired_pins=desired_pins)
        if dry_run:
            legacy = migration_candidates(
                resolved_claude, skill_root, targets, legacy_dirs, desired_pins=desired_pins
            )
            return {
                "claude_dir": str(resolved_claude),
                "skill_root": str(skill_root),
                "dry_run": True,
                "updated": [str(p) for p, src in targets.items() if entry_digest(p) != entry_digest(src)],
                "migrated": [str(p) for p in legacy],
                "backup": None,
            }
        import fcntl
        resolved_claude.mkdir(parents=True, exist_ok=True)
        with (resolved_claude / ".zhuzi-install.lock").open("a") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise RuntimeError("another zhuzi Claude installation is running") from exc
            legacy = migration_candidates(
                resolved_claude, skill_root, targets, legacy_dirs, desired_pins=desired_pins
            )
            return apply_install(targets, legacy, resolved_claude, skill_root, home_key="claude_dir")


def install_source_only_adapters(codex_home: Path, *, render_concrete: bool | None = None) -> list[Path]:
    result = install_codex_assets(codex_home)
    return [Path(path) for path in result["updated"]]  # type: ignore[index]


def print_human_report(label: str, result: dict[str, object], *, dry_run: bool) -> None:
    print(f"[{label}]")
    for path in result.get("updated", []):  # type: ignore[union-attr]
        print(f"  + {path}")
    for path in result.get("migrated", []):  # type: ignore[union-attr]
        print(f"  - migrated legacy entry: {path}")
    if result.get("backup"):
        print(f"  backup: {result['backup']}")
    print(f"{label} preview only." if dry_run else f"{label} complete.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-skill-root", action="store_true")
    parser.add_argument("--codex-only", action="store_true", help="operate on Codex runtime only")
    parser.add_argument("--claude-only", action="store_true", help="operate on Claude runtime only")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true", help="machine-readable migration report")
    parser.add_argument("--pin", action="append", default=[], help="pin a persona skill as top-level shortcut")
    parser.add_argument("--unpin", action="append", default=[], help="unpin a previously pinned persona skill")
    parser.add_argument("--uninstall", action="store_true", help="backup and remove installed zhuzi assets")
    args = parser.parse_args()

    if args.codex_only and args.claude_only:
        parser.error("cannot combine --codex-only and --claude-only")
    if args.uninstall and (args.pin or args.unpin):
        parser.error("cannot combine --uninstall with --pin or --unpin")

    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    if args.print_skill_root:
        print(resolve_skill_root(codex_home))
        return 0

    try:
        if args.codex_only:
            result = install_codex_assets(
                codex_home, dry_run=args.dry_run, pin=args.pin, unpin=args.unpin, uninstall=args.uninstall
            )
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print_human_report("Codex installation", result, dry_run=args.dry_run)
            return 0

        if args.claude_only:
            result = install_claude_assets(
                None, dry_run=args.dry_run, pin=args.pin, unpin=args.unpin, uninstall=args.uninstall
            )
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print_human_report("Claude installation", result, dry_run=args.dry_run)
            return 0

        claude_res = install_claude_assets(
            None, dry_run=args.dry_run, pin=args.pin, unpin=args.unpin, uninstall=args.uninstall
        )
        codex_res = install_codex_assets(
            codex_home, dry_run=args.dry_run, pin=args.pin, unpin=args.unpin, uninstall=args.uninstall
        )
        combined = {"claude": claude_res, "codex": codex_res, "dry_run": args.dry_run}
        if args.json:
            print(json.dumps(combined, ensure_ascii=False, indent=2))
        else:
            print_human_report("Claude installation", claude_res, dry_run=args.dry_run)
            print()
            print_human_report("Codex installation", codex_res, dry_run=args.dry_run)
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Installation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
