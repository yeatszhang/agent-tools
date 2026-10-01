---
name: repo-spec-maintainer
description: Create, audit, or update a repository's AGENTS.md and related agent instructions. Use when starting a new coding project, defining AI coding constraints, reducing instruction bloat, introducing nested AGENTS.md files, or linking repository policy to task-specific Skills.
---

# Repo Spec Maintainer

## Shared policy

This Skill is procedural. Repository-wide rules remain authoritative in [../../AGENTS.md](../../AGENTS.md). The reusable starter policy lives in [../../templates/repo-spec/AGENTS.md](../../templates/repo-spec/AGENTS.md).

Do not duplicate shared repository rules into this Skill.

## Goal

Produce the smallest useful repository instruction surface that is always correct, easy to discover, and cheap to load on every agent turn.

## Workflow

1. Inspect the repository structure, existing `AGENTS.md` / `CLAUDE.md`, build metadata, and test commands.
2. Separate information into:
   - **always-on policy** → `AGENTS.md`
   - **package-specific policy** → nearest nested `AGENTS.md`
   - **conditional procedure** → Skill
   - **long explanation/examples** → docs or Skill references
3. Start from [the repo-spec template](../../templates/repo-spec/README.md), including its OpenSpec setup and small knowledge map, then delete anything that is not demonstrably relevant. Use [the harness template](../../templates/agent-harness/README.md) only for projects that build an agent runtime or multi-agent orchestration system.
4. Preserve one source of truth. Link across surfaces; do not copy the same rule into multiple files.
5. Verify every path and command named in the instructions actually exists.
6. Review the final instruction budget: every root line should either apply to nearly every task or save costly rediscovery.

## AGENTS.md ↔ Skill contract

Use this direction:

```text
AGENTS.md
  "When doing X, read skills/x/SKILL.md"
        ↓
SKILL.md
  "Shared repository policy remains in ../../AGENTS.md"
```

The root file routes; the Skill executes.

A Skill may tighten a rule for its workflow, but it should not restate broad engineering policy.

## Must

- Keep root `AGENTS.md` concise and repository-wide.
- Prefer nested `AGENTS.md` for local constraints.
- Prefer links over duplicated rules.
- Use concrete commands and exact paths.
- Keep policy declarative; keep procedures in Skills.
- Preserve user and repository-specific requirements over template defaults.

## Avoid

- Treating `AGENTS.md` as a full engineering handbook.
- Loading every Skill on every task.
- Maintaining divergent copies of `AGENTS.md` and `CLAUDE.md`.
- Adding speculative rules for technologies the repository does not use.
- Embedding large examples in always-on instructions.

## Validation

Before finishing, confirm:

- root instructions are broadly applicable;
- package-specific rules are scoped near their files;
- Skill routes point to real `SKILL.md` files;
- Skills link back to the authoritative shared policy when needed;
- commands and paths exist;
- OpenSpec paths and architecture links point to real project knowledge rather than template placeholders;
- no parallel plan or decision log duplicates the OpenSpec change record;
- duplicated guidance has been removed.
