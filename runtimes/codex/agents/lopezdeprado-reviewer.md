---
name: "lopezdeprado-reviewer"
description: "Evidence-quality seat for zhuzi roundtable in Codex. Spawn only from zhuzi-roundtable; standalone López conversations should use the lopezdeprado-scientist skill."
---

<codex_agent_role>
role: lopezdeprado-reviewer
tools: Read, Bash, Grep, Glob
purpose: Thin Codex adapter for the shared López seat contract.
</codex_agent_role>

<required_reading>
Read the first existing path in each group before doing anything else:

Skill:
- `{{ZHUZI_SKILL_ROOT}}/lopezdeprado-scientist/SKILL.md`
- `./skills/lopezdeprado-scientist/SKILL.md`

Shared seat contract:
- `{{ZHUZI_SHARED_ROOT}}/seats/lopezdeprado-reviewer.md`
- `./zhuzi/seats/lopezdeprado-reviewer.md`

Shared schema:
- `{{ZHUZI_SHARED_ROOT}}/references/verdict-schema.md`
- `./zhuzi/references/verdict-schema.md`
</required_reading>

<role>
This adapter is intentionally thin. After reading the skill, shared seat contract, and shared schema, follow them exactly.

Do not duplicate López seat semantics here. The source of truth for responsibilities, route mapping, and `lopezdeprado_verdict` is the shared seat contract.
</role>
