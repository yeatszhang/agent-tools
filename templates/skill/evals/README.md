# Skill Evaluation Cases

Replace these placeholders with realistic user requests before calling the Skill stable. Test routing separately from output quality.

| Kind | Input | Expected |
| --- | --- | --- |
| Should trigger | A request that directly needs this workflow | Skill loads and completes its stated goal. |
| Should trigger | A paraphrase without the Skill name | Skill loads for the same underlying task. |
| Should not trigger | A request that shares keywords but belongs to another workflow | Skill stays unloaded. |
| Should not trigger | A simple question that does not require this workflow | Skill stays unloaded. |
| Result quality | A representative task with edge cases | Output meets the goal, preserves inputs, and reports verification. |

资料可用性案例：为实际任务设置外部来源不可用的条件，检查当前 Skill 的本地流程仍能给出具体步骤与验证边界；若共享参考，确认内容与适用范围完全相同，不误删场景化版本。
