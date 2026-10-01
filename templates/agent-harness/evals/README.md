# Harness Evaluation Cases

Turn these into executable cases with fixtures and expected observations for the chosen runtime. Evaluate both final outcomes and the trajectory that produced them.

| Case | Expected evidence |
| --- | --- |
| Tool succeeds with empty stdout | Explicit success status and empty-output observation; no ambiguity with timeout. |
| Tool emits more than the display limit | Truncation marker and a retrievable full artifact. |
| Action violates a permission boundary | Denial event, no side effect, and a caller-visible failure. |
| Two workers edit and run services concurrently | Separate writable workspaces, processes, browser state, and ports; results remain attributable. |
| Worker crashes after an action starts | Event history identifies the last known state; recovery does not mark the action complete without evidence. |
| A context handoff occurs mid-task | New worker retains goal, constraints, accepted decisions, pending checks, and links to earlier evidence. |
| Review finds a behavior bug | Fix appears in the final trajectory and required verification reruns after it. |
