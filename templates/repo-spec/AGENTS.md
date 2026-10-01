# Agent Instructions

This file defines always-on repository policy for coding agents. Keep it short enough to load on every task. Put task-specific procedures in Skills and link them from the routing section instead of copying them here.

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

Keep procedural workflows out of this file. Link to a Skill when a task needs a conditional procedure.

| When | Skill |
| --- | --- |
| Create, audit, or materially revise repository agent policy | [repo-spec-maintainer](../../skills/repo-spec-maintainer/SKILL.md) |
| Add a new reusable Skill | Follow the repository's Skill authoring guidance and [Skill template](../skill/SKILL.md) |

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
