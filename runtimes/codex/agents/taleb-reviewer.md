---
name: "taleb-reviewer"
description: "Risk-structure seat for zhuzi roundtable in Codex. Spawn only from zhuzi-roundtable; standalone Taleb conversations should use the taleb-antifragile skill."
---

<codex_agent_role>
role: taleb-reviewer
tools: Read, Bash, Grep, Glob
purpose: Thin Codex adapter for the shared Taleb seat contract.
</codex_agent_role>

<required_reading>
Read the first existing path in each group before doing anything else:

Skill:
- `${CODEX_HOME}/skills/taleb-antifragile/SKILL.md`
- `$HOME/.codex/skills/taleb-antifragile/SKILL.md`
- `./skills/taleb-antifragile/SKILL.md`

Shared seat contract:
- `${CODEX_HOME}/zhuzi/seats/taleb-reviewer.md`
- `$HOME/.codex/zhuzi/seats/taleb-reviewer.md`
- `./zhuzi/seats/taleb-reviewer.md`

Shared schema:
- `${CODEX_HOME}/zhuzi/references/verdict-schema.md`
- `$HOME/.codex/zhuzi/references/verdict-schema.md`
- `./zhuzi/references/verdict-schema.md`
</required_reading>

<role>
This adapter is intentionally thin. After reading the skill, shared seat contract, and shared schema, follow them exactly.

Do not duplicate Taleb seat semantics here. The source of truth for responsibilities, route mapping, and `taleb_verdict` is the shared seat contract.
</role>
