# Agent Instructions

This file defines always-on repository policy for coding agents. Keep it short enough to load on every task. Put task-specific procedures in Skills and link them from the routing section instead of copying them here.

## Repository Map

- Start with [ARCHITECTURE.md](ARCHITECTURE.md) for system boundaries and the main code paths.
- Read `openspec/specs/` for current product behavior and `openspec/changes/` for active or archived change records. Initialize OpenSpec before using this template.
- Add links here for project-specific product, security, reliability, and operational docs. Read them when the task touches that area; do not load every document for every task.

## Engineering Constitution

1. **Validate at boundaries; trust types internally.**
   Validate network, IPC, filesystem, user, and external API inputs once. After validation, do not spread defensive null checks or fallback values through internal code.

2. **Use a zero complexity budget.**
   Every abstraction must solve a current requirement. Avoid speculative extension points, one-implementation interfaces, pass-through wrappers, and generic infrastructure for hypothetical use.

3. **Keep the diff focused.**
   Do not perform unrelated cleanup, renaming, formatting, dependency upgrades, or refactors while completing a scoped task.

4. **Refactor by replacement, not layering.**
   Prefer reshaping the existing path. When a new path replaces an old one, migrate callers and remove the old path in the same change unless compatibility is an explicit requirement.

5. **Make impossible states impossible.**
   Prefer precise domain types, literal unions, and discriminated unions over loose booleans and optional fields that allow invalid combinations.

6. **Do not silence the type system.**
   Avoid `any`, ignore directives, or casts whose only purpose is to suppress an error. Narrow unknown values through validation or control flow.

7. **Fail explicitly.**
   Do not silently substitute requested behavior with fallback behavior. Catch only errors that have a concrete recovery strategy; rethrow unknown failures.

8. **Tests prove behavior, not implementation.**
   Test externally observable outcomes. Avoid tests coupled to private call counts, incidental structure, or implementation details.

9. **Debug from evidence.**
   Prefer focused reproduction, runtime values, logs, and failing tests over conclusions inferred only from static code reading.

10. **Run the smallest verification that proves the change.**
    Start with affected tests, typecheck, and lint. Leave broad integration suites to CI unless the task requires them.

## Before Behavior-Changing Work

Use the project's OpenSpec workflow for features and non-trivial behavior changes. For changes to public APIs, persisted state, protocols, runtime lifecycle, or compatibility boundaries, capture required behavior, compatibility requirements, intentionally unsupported cases, failure behavior, and acceptance criteria in the relevant OpenSpec proposal, specs, and design. Do not maintain a second plan or scope contract for the same change. A small local correction can proceed directly when it needs no change spec.

## Completion Contract

- Implement the agreed scope and run focused verification.
- Review the diff for correctness, scope creep, missing failure paths, and test quality. Seek independent review for high-impact changes when the project workflow supports it; resolve findings before final verification.
- Run any required final checks after the last fix. Report what ran and what remains unverified. Do not claim completion while required checks or review are pending.
- Update and archive the OpenSpec change only after its implemented behavior and verification agree with the artifacts.
- Preserve the current checkout. Create branches or worktrees only when the task or repository workflow calls for them; isolate concurrent workers when they can change the same files, services, or ports.

## Coding Rules

- Comments explain non-obvious **why**, not obvious **what**.
- Prefer domain names over mechanical names such as `data`, `result`, `info`, `manager`, and `temp`.
- Avoid nested ternaries and dense expression pipelines when named intermediate values would make intent clearer.
- Do not keep commented-out code or speculative TODOs without a concrete owner or requirement.
- Documentation should capture decisions, constraints, gotchas, and cross-module invariants rather than narrating code.

## Testing Rules

- Prefer vertical slices: test → implementation → next test.
- Keep tests deterministic; remove reliance on timing, randomness, network jitter, and shared mutable state.
- A flaky test is a bug. Fix the source of nondeterminism instead of deleting, skipping, or retrying it.
- Prefer real lightweight dependencies when practical; otherwise isolate them behind explicit ports and typed fakes.
- Use strong assertions that verify the expected value, not weak truthiness checks.

## Skill Routing

Keep procedural workflows out of this file. Add routes only for Skills that actually exist in the target repository.

Example:

| When | Skill |
| --- | --- |
| Perform a task-specific workflow | `skills/skill-name/SKILL.md` (replace with a link to a real Skill) |

The root file routes; the Skill contains the detailed procedure. Remove example rows after project setup.

## Project-Specific Additions

Add only rules that are true for nearly every task in this repository:

- Package manager / build system:
- Focused test command:
- Typecheck command:
- Lint command:
- Generated files:
- Architecture constraints:
- Security constraints:

For narrower package or directory rules, prefer a nested `AGENTS.md` near the relevant files instead of expanding this root file.
