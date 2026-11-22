---
name: repo-spec-maintainer
description: Create, audit, or update a repository's AGENTS.md and related agent instructions. Use when starting a new coding project, defining AI coding constraints, reducing instruction bloat, introducing nested AGENTS.md files, or linking repository policy to task-specific Skills.
---

# Repo Spec Maintainer

## Shared policy

This Skill is procedural. Repository-wide rules remain authoritative in [../../AGENTS.md](../../AGENTS.md). The reusable starter policy lives in [../../templates/repo-spec/AGENTS.md](../../templates/repo-spec/AGENTS.md).

资料保存与引用方式见 [本地资料约定](../../docs/conventions.md)；本 Skill 中的规范维护步骤按自身场景完整保留。

## Goal

Produce the smallest useful repository instruction surface that is always correct, easy to discover, and cheap to load on every agent turn.

## Workflow

1. Inspect the repository structure, existing `AGENTS.md` / `CLAUDE.md`, build metadata, and test commands.
2. Separate information into:
   - **always-on policy** → `AGENTS.md`
   - **package-specific policy** → nearest nested `AGENTS.md`
   - **conditional procedure** → Skill
   - **long explanation/examples** → docs or Skill references
3. 新建仓库规范时参考 [repo-spec 模板](../../templates/repo-spec/README.md)，只保留实际相关的规则。审查或修改已有规范时，以目标仓库当前工具和结构为准；仅当任务包含工具接入时执行 OpenSpec 安装/初始化，不因编辑 AGENTS.md 自动引入工具。构建 Agent Runtime 或编排系统时才参考 [harness 模板](../../templates/agent-harness/README.md)。
4. 优先在仓库保存完整可执行的流程及参考资料，允许场景化冗余。只有内容与适用范围完全相同才共享引用；对相似但条件、步骤或验收不同的内容保留各自版本，并注明来源与本地调整。
5. Verify every path and command named in the instructions actually exists.
6. Review the final instruction budget: every root line should either apply to nearly every task or save costly rediscovery.

## AGENTS.md ↔ Skill contract

Use this direction:

```text
AGENTS.md
  "When doing X, read skills/x/SKILL.md"
        ↓
SKILL.md
  "Shared repository policy remains in ../../AGENTS.md"
```

The root file routes; the Skill executes.

Skill 可为自身场景完整描述具体操作与验收，即使与其他资料部分重叠。完全相同的通用政策仍链接权威文件；场景化版本不能改变上级政策的约束。

## Must

- Keep root `AGENTS.md` concise and repository-wide.
- Prefer nested `AGENTS.md` for local constraints.
- 必需流程优先本地完整保存；仅完全相同的内容优先引用，不把去重作为独立目标。
- Use concrete commands and exact paths.
- Keep policy declarative; keep procedures in Skills.
- Preserve user and repository-specific requirements over template defaults.

## Avoid

- Treating `AGENTS.md` as a full engineering handbook.
- Loading every Skill on every task.
- Maintaining divergent copies of `AGENTS.md` and `CLAUDE.md`.
- Adding speculative rules for technologies the repository does not use.
- Embedding large examples in always-on instructions.

## Validation

Before finishing, confirm:

- root instructions are broadly applicable;
- package-specific rules are scoped near their files;
- Skill routes point to real `SKILL.md` files;
- Skills link back to the authoritative shared policy when needed;
- commands and paths exist;
- OpenSpec paths and architecture links point to real project knowledge rather than template placeholders;
- `CLAUDE.md`, when present, resolves to the authoritative `AGENTS.md` rather than maintaining a divergent copy;
- no parallel plan or decision log duplicates the OpenSpec change record;
- 场景化步骤在仓库内完整可用，来源可追溯；共享引用仅用于完全相同的资料。

触发、范围与结果回归案例见 [evals](evals/README.md)。只审查时报告发现；明确要求修改或修复时再编辑目标文件。
