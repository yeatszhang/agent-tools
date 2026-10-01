# Agent Harness Instructions

Keep this file as the entry point for contributors and coding agents. Project facts and procedures belong in the linked documents.

## Read by Task

- [HARNESS.md](HARNESS.md): runtime responsibilities, lifecycle, boundaries, and verification gates.
- [architecture/runtime.md](architecture/runtime.md): action, runtime, observation, and event flow.
- [architecture/tools.md](architecture/tools.md): tool schemas and observation contracts.
- [architecture/workspace.md](architecture/workspace.md): workspace, worktree, sandbox, service, and port isolation.
- [architecture/context.md](architecture/context.md): context assembly, persistence, and recovery.
- [evals/README.md](evals/README.md): behavior and failure evaluation cases.

## Invariants

- Make the trust boundary between model output and executable action explicit. Validate actions and permissions before execution.
- Record every meaningful action and outcome with a stable run and step identity. Make failures visible to the caller.
- Give concurrent workers isolated mutable resources, or serialize access with an explicit owner.
- Keep tool observations bounded and unambiguous. Preserve access to full artifacts when output is truncated.
- For changes to protocols, persisted events, permissions, runtime lifecycle, or compatibility, state required behavior, compatibility, unsupported cases, failure behavior, and acceptance criteria before implementation.
- Finish with focused tests, a diff review, required independent review, and final verification. Report evidence and any remaining limits.
