# Repository Instructions

This repository is the source of truth for personal agent tooling.

## Principles

- Prefer portable, model-agnostic Skills.
- Keep SKILL.md concise; move long rules/examples into references/.
- Never commit secrets, tokens, cookies, private keys, or raw credentials.
- For learned behavior, do not promote a one-off edit directly into stable rules.
- Preserve source facts and intent when rewriting user content.
- Add or update eval cases when changing stable behavior.

## Structure

- `skills/`: reusable Agent Skills.
- `agents/`: role definitions and multi-step workflows.
- `mcp/`: MCP catalog and sanitized config examples.
- `tools/`: useful external tools / CLIs.
- `templates/`: starter templates.
- `scripts/`: repository maintenance and validation.
