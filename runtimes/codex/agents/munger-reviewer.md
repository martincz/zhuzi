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
- `{{ZHUZI_SKILL_ROOT}}/munger-checklist/SKILL.md`
- `./skills/munger-checklist/SKILL.md`

Shared seat contract:
- `{{ZHUZI_SHARED_ROOT}}/seats/munger-reviewer.md`
- `./zhuzi/seats/munger-reviewer.md`

Shared schema:
- `{{ZHUZI_SHARED_ROOT}}/references/verdict-schema.md`
- `./zhuzi/references/verdict-schema.md`
</required_reading>

<role>
This adapter is intentionally thin. After reading the skill, shared seat contract, and shared schema, follow them exactly.

Do not duplicate Munger seat semantics here. The source of truth for responsibilities, route mapping, and `munger_verdict` is the shared seat contract.
</role>
