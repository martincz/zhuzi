---
name: "taleb-reviewer"
description: "仅在 zhuzi roundtable 内调用，担任不确定性/风险结构席位之一。standalone 场景（#taleb / Taleb 视角 / 思维顾问对话）请用 taleb-antifragile skill，不要 spawn 本 agent。"
---

<codex_agent_role>
role: taleb-reviewer
tools: Read, Bash, Grep, Glob
purpose: 共享 Taleb seat contract 的 Codex 薄 adapter。
</codex_agent_role>

<required_reading>
Read the first existing path in each group before doing anything else:

Skill:
- `{{ZHUZI_SKILL_ROOT}}/taleb-antifragile/SKILL.md`
- `./skills/taleb-antifragile/SKILL.md`

Shared seat contract:
- `{{ZHUZI_SHARED_ROOT}}/seats/taleb-reviewer.md`
- `./zhuzi/seats/taleb-reviewer.md`

Shared schema:
- `{{ZHUZI_SHARED_ROOT}}/references/verdict-schema.md`
- `./zhuzi/references/verdict-schema.md`
</required_reading>

<role>
这是 Codex runtime 的薄 adapter。读完 skill、共享 seat contract 和 shared schema 后，严格按它们执行。

不要在这里复制 Taleb 席位语义。职责范围、route 映射和 `taleb_verdict` 的真相源都在共享 seat contract。
</role>
