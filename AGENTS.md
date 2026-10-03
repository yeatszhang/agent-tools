# Repository Instructions

This repository is the source of truth for personal agent tooling.

## Principles

- Prefer portable, model-agnostic Skills.
- Keep `SKILL.md` concise; move long rules/examples into `references/`.
- Keep always-on repository policy in `AGENTS.md`; keep conditional procedures in Skills.
- Link between `AGENTS.md` and Skills instead of duplicating shared rules.
- Keep `AGENTS.md` authoritative; `CLAUDE.md` links to it instead of maintaining a second copy.
- Never commit secrets, tokens, cookies, private keys, or raw credentials.
- For learned behavior, do not promote a one-off edit directly into stable rules.
- Preserve source facts and intent when rewriting user content.
- Add or update eval cases when changing stable behavior.

## Structure

- `skills/`: reusable Agent Skills.
- `agents/`: role definitions and multi-step workflows.
- `mcp/`: MCP catalog and sanitized config examples.
- `tools/`: useful external tools / CLIs.
- `templates/`: starter templates, including repository agent policy.
- `scripts/`: repository maintenance and validation.

## Skill Routing

Read a Skill only when its trigger applies. The root file routes; the Skill contains the detailed procedure.

| When | Skill |
| --- | --- |
| Create, audit, or update repository-level agent instructions | [repo-spec-maintainer](skills/repo-spec-maintainer/SKILL.md) |
| Rewrite or humanize Chinese text, or maintain personal voice rules | [writing-editor](skills/writing-editor/SKILL.md) |

When authoring a new Skill, start from [templates/skill/README.md](templates/skill/README.md). Skills that depend on repository-wide rules should link back to this file rather than restating those rules.

## Repository Spec Templates

Use [templates/repo-spec/README.md](templates/repo-spec/README.md) as the default starting point for a new AI-assisted coding repository. It initializes OpenSpec for change/spec management and keeps broad coding rules in `AGENTS.md`. Its engineering constitution is a template, not automatically a rule for this tooling repository.

Use [templates/agent-harness/README.md](templates/agent-harness/README.md) only for repositories that build an agent runtime or multi-agent orchestration system.
