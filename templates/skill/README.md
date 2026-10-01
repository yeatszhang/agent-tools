# Skill Template

Metadata (`name` and `description`) is used for discovery; write the description as a specific trigger and outcome. `SKILL.md` is read after triggering. Put optional detail in `references/` and open it only for relevant tasks.

Copy `SKILL.md` and `evals/` for a stable Skill. Keep the other directories only when the Skill uses them:

- `references/`: long guidance, examples, or decision trees.
- `scripts/`: deterministic helpers with documented inputs and outputs.
- `assets/`: files consumed or delivered by the workflow.
- `evals/`: should-trigger, should-not-trigger, and result-quality cases.

Keep the main file concise. Update trigger evals when changing the description; update result evals when changing the workflow. Do not copy placeholder examples into a production Skill.
