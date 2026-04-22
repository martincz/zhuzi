---
name: "munger-reviewer"
description: "Decision-quality seat for zhuzi roundtable in Codex. Spawn only from zhuzi-roundtable; standalone Munger conversations should use the munger-checklist skill."
---

<codex_agent_role>
role: munger-reviewer
tools: Read, Bash, Grep, Glob
purpose: Thin Codex adapter for the shared Munger seat contract.
</codex_agent_role>

<required_reading>
Read the first existing path in each group before doing anything else:

Skill:
- `${CODEX_HOME}/skills/munger-checklist/SKILL.md`
- `$HOME/.codex/skills/munger-checklist/SKILL.md`
- `./skills/munger-checklist/SKILL.md`

Shared seat contract:
- `${CODEX_HOME}/zhuzi/seats/munger-reviewer.md`
- `$HOME/.codex/zhuzi/seats/munger-reviewer.md`
- `./zhuzi/seats/munger-reviewer.md`

Shared schema:
- `${CODEX_HOME}/zhuzi/references/verdict-schema.md`
- `$HOME/.codex/zhuzi/references/verdict-schema.md`
- `./zhuzi/references/verdict-schema.md`
</required_reading>

<role>
This adapter is intentionally thin. After reading the skill, shared seat contract, and shared schema, follow them exactly.

Do not duplicate Munger seat semantics here. The source of truth for responsibilities, route mapping, and `munger_verdict` is the shared seat contract.
</role>
