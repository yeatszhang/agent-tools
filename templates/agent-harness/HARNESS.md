# Harness Contract

Fill this page with the implemented system's current behavior. Remove features that do not exist.

## Components and Ownership

| Component | Responsibility | Interface / code entry point |
| --- | --- | --- |
| Orchestrator | Schedules runs and owns worker assignment | Replace with real path |
| Runtime | Validates and executes actions | Replace with real path |
| Workspace manager | Creates and releases isolated resources | Replace with real path |
| Event store | Persists run and step outcomes | Replace with real path |

## Run Lifecycle

Document the actual states and allowed transitions, including start, action execution, cancellation, timeout, failure, recovery, and cleanup. State who owns each transition. An action should produce either a typed observation or a typed failure; a missing observation must not look like success.

## Permission Boundary

Specify which actor can authorize filesystem, network, process, and external side effects. Record how denials and escalations appear in the event stream. Never treat model text as authorization.

## Evidence and Completion

Name the test commands and the surfaces an agent can inspect: app or browser state, logs, metrics, traces, screenshots, and stored events where relevant. Define how to attribute each artifact to a run and worktree. A completion report should point to observed results and state what could not be verified.

## Maintenance

Keep a small set of golden trajectories and failure cases in `evals/`. When runtime behavior changes, compare action/observation sequences and user-visible outcomes. Remove obsolete compatibility paths and stale docs after migrations.
