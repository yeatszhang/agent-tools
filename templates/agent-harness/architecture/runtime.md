# Runtime and Event Flow

## Execution Contract

```text
Agent decision → typed action → validation / permission check → runtime execution
                                                        ↓
                                typed observation or typed failure → agent
                                                        ↓
                                              append-only event record
```

Define concrete action, observation, and failure variants here. Each event needs a run ID, step ID, timestamp, actor, workspace identity, outcome, and artifact references. Specify ordering, replay, and idempotency guarantees according to the actual store.

## State and Recovery

Describe where authoritative run state lives, how cancellation interrupts actions, what happens on process crash, and how the runtime resumes or marks a run failed. Define timeout behavior and cleanup ownership. Do not infer success from a command that merely started.

## Extension Boundary

Before adding an adapter or fallback, name the current requirement and the existing alternative. Prefer one path per supported capability. Document deliberate unsupported cases and their explicit error.
