# Repository Spec Template

A starter policy for new AI-assisted coding repositories.

## Purpose

Use this template when starting a new project or when an existing repository lacks clear agent-facing engineering constraints.

The boundary is intentional:

- **AGENTS.md** = always-on repository policy and routing index.
- **Skills** = conditional, task-specific procedures loaded only when relevant.
- **References/docs** = long explanations, examples, and rationale that should not consume every-turn instruction budget.

## Recommended setup

1. Copy `AGENTS.md` to the new repository root.
2. Fill only the project-specific additions that are hard or expensive to discover.
3. Delete generic rules that do not fit the project.
4. Add nested `AGENTS.md` files for package-specific constraints.
5. Link procedural work to Skills instead of copying long workflows into `AGENTS.md`.
6. If Claude-compatible discovery is needed, prefer a `CLAUDE.md` symlink to `AGENTS.md` rather than maintaining two divergent copies.

## Linking pattern

```text
AGENTS.md
  ├─ always-on invariants
  ├─ repository facts
  └─ route: "when X, read skills/x/SKILL.md"
                         ↑
SKILL.md                 │
  ├─ conditional workflow
  ├─ commands / decisions│
  └─ shared policy: -----┘ link back to AGENTS.md
```

Do not duplicate shared rules in both directions. The link is the contract; each fact should have one authoritative home.

## Source inspiration

The engineering constraints are adapted from high-quality AI-native repository practices, especially Paseo's coding/testing guidance, while the instruction-routing design follows the broader pattern used by mature Agent Skills repositories: small always-on `AGENTS.md`, progressive disclosure through Skills, and one source of truth for shared policy.
