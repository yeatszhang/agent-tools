# Repository Spec Template

Starter instructions and a small knowledge map for an AI-assisted coding repository using [OpenSpec](https://openspec.dev/docs/quickstart) for change planning and behavioral specifications.

## Use

1. [Install and initialize OpenSpec](https://openspec.dev/docs/setup) in the target repository with `openspec init`. Keep the generated `openspec/` artifacts and tool-specific workflow files; do not copy them from this template.
2. Copy `AGENTS.md` and `ARCHITECTURE.md` to the repository root. Replace or remove every example row and project-specific placeholder.
3. Map actual system boundaries in `ARCHITECTURE.md`. Use `openspec/specs/` as the source of truth for current product behavior and `openspec/changes/` for change proposals, designs, tasks, and history. Do not create a parallel plan or decision log for the same work.
4. Add project-specific security, reliability, or operational docs only when they contain real content. Put package-specific policy in a nearby nested `AGENTS.md`. Route other conditional procedures to actual Skills; remove the example route before use.
5. Verify all links, named paths, and commands against the target repository. If Claude-compatible discovery is needed, prefer a `CLAUDE.md` symlink to `AGENTS.md` over divergent copies.

`AGENTS.md` is the entry point for broad engineering rules and routing. OpenSpec owns the change workflow and behavioral record; its generated Skills provide the detailed procedure. `ARCHITECTURE.md` summarizes current system boundaries and links to relevant specs and change designs. Agents read only the documents relevant to a task.

For a runtime that orchestrates agents or parallel worktrees, start separately from [../agent-harness/README.md](../agent-harness/README.md). Its environment and tool contracts are not general coding policy.

## Evaluation cases

Use [evals/README.md](evals/README.md) when adapting this template. These cases check that OpenSpec and the repository instructions have distinct sources of truth without making `AGENTS.md` a handbook.
