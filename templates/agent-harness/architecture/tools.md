# Tool and Observation Contract

## Action Design

For each tool, document typed inputs, validation, permissions, side effects, timeout, and whether retry is safe. Keep tool names and error variants stable enough for callers to distinguish invalid input, permission denial, execution failure, and timeout.

## Observation Design

Every call returns a definite status, including success with no output. Bound large output and show that truncation occurred; provide an artifact reference or pagination path to the full result. Prefer concise search results and bounded file views so the relevant evidence remains visible.

If the runtime performs post-edit checks such as linting, report them as separate observations with their own status. Do not turn a failed check into a successful edit observation.

## Evidence Surfaces

List which browser, DOM, screenshot, log, metric, and trace tools exist. State how each selects the correct run/workspace and how users can reproduce the observation. Remove unused surfaces from this page.
