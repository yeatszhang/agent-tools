# Repository Spec Evaluation Cases

Try these cases against the copied template after replacing placeholders. Check the agent's chosen sources and final report, not exact wording.

| Case | Expected behavior |
| --- | --- |
| Change a public API and its stored representation | Agent uses an OpenSpec change to capture required behavior, compatibility, unsupported cases, failure behavior, and acceptance criteria before editing; reads relevant architecture and current specs. |
| Fix a local styling typo | Agent makes a focused edit and verification; does not create an unnecessary OpenSpec change or read unrelated docs. |
| Change a documented security boundary | Agent reads linked security guidance and current specs, then updates the OpenSpec change design and resulting specs as appropriate. |
| Finish after review finds a bug | Agent fixes the finding, reruns affected final checks, and reports the actual verification result. |
| Complete a change with specs that differ from shipped behavior | Agent corrects the implementation or OpenSpec artifacts before archiving; does not claim completion from checked task boxes alone. |
| Two workers need to run the app concurrently | Each receives an isolated workspace and service/port resources under the project's workflow; neither changes a shared checkout concurrently. |
