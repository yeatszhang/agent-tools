# Context Lifecycle

## Assembly

Document which instructions, repository facts, user inputs, tool observations, and retrieved files enter a run. Define priority and provenance. Load task-specific references when needed instead of copying the whole repository into every prompt.

## Budget and Compaction

Set limits for observations and context. State what is summarized or dropped, how the summary preserves goals, constraints, decisions, unresolved failures, and artifact references, and how a worker can reopen the underlying evidence.

## Handoff and Replay

Describe the minimal handoff record for another worker: current objective, accepted scope contract, workspace revision, completed steps, pending checks, and links to relevant events. Test that recovery does not invent completed work or lose a user constraint.
