# Repository Instructions

This repository is the source of truth for personal agent tooling.

## Principles

- Prefer portable, model-agnostic Skills.
- Keep `SKILL.md` concise; move long rules/examples into `references/`.
- Keep always-on repository policy in `AGENTS.md`; keep conditional procedures in Skills.
- 优先在仓库保存完整可用的本地内容，允许按 Skill 场景冗余；reference 和来源链接可以保留。只有内容与适用范围完全相同的资料才优先共享引用，不能因相似就合并或删减。
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
| 设计产品任务流、界面状态或视觉方案 | [ui-ux-design](skills/ui-ux-design/SKILL.md)（草案） |
| 审查 Web UI 的交互、无障碍或界面性能 | [web-ui-review](skills/web-ui-review/SKILL.md)（草案） |
| 设计、实现或审查原生与桌面客户端 UI | [client-ui-design](skills/client-ui-design/SKILL.md)（草案） |
| Electron/Tauri/原生桌面选型，或 Electron 宿主、IPC、性能与发布验证 | [desktop-app-engineering](skills/desktop-app-engineering/SKILL.md)（草案） |

When authoring a new Skill, start from [templates/skill/README.md](templates/skill/README.md). 完全相同的仓库级规则链接回本文件；场景化操作步骤优先写入对应 Skill。具体维护方式见 [本地资料约定](docs/conventions.md)。

## Repository Spec Templates

Use [templates/repo-spec/README.md](templates/repo-spec/README.md) as the default starting point for a new AI-assisted coding repository. It initializes OpenSpec for change/spec management and keeps broad coding rules in `AGENTS.md`. Its engineering constitution is a template, not automatically a rule for this tooling repository.

Use [templates/agent-harness/README.md](templates/agent-harness/README.md) only for repositories that build an agent runtime or multi-agent orchestration system.
