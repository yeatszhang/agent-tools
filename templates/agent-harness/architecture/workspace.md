# Workspace and Isolation

## Ownership

Map each worker to its checkout/worktree, writable directories, process group, browser profile, service instance, ports, and artifact directory. State which resources can be shared read-only and who cleans them up.

## Isolation Rules

- Assign separate mutable workspaces to workers that may run concurrently. If isolation is unavailable, serialize their writes and service use.
- Allocate ports and service names per workspace rather than relying on fixed global values.
- Scope credentials and filesystem permissions to the task. Keep secrets out of logs, events, and copied worktrees.
- Record the base revision and any uncommitted state before a worker starts. Define how results are reviewed and integrated without overwriting another worker's changes.

## Cleanup and Failure

Define what survives a failed run for debugging, retention limits, and how orphaned processes/worktrees are detected. Cleanup must not erase artifacts still needed for review or recovery.
