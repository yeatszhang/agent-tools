---
name: replace-me
description: 说明用户会提出什么任务、何时应触发，以及这个 Skill 交付什么结果；避免只写宽泛关键词。
---

# Skill Name

只保留触发后每次都需要的规则。任务样例、长决策树和背景放进 `references/`；确定性的可执行步骤才放进 `scripts/`；交付素材放进 `assets/`。不用的目录删除。

## Shared Policy

如果这个 Skill 依赖仓库级约束，在这里链接权威 `AGENTS.md`，不要复制规则。

Example:

```md
Repository-wide policy remains authoritative in [../../AGENTS.md](../../AGENTS.md).
```

## Goal

一句话定义可检查的结果和适用边界。

## Workflow

1. 确认输入、约束和所需参考资料；只读取当前任务相关的 `references/` 文件。
2. 执行最小必要步骤，保留输入事实与用户意图。
3. 验证结果并报告证据、未验证部分和需要用户处理的事项。

## Must

- 写出本 Skill 特有、可以执行的约束；共享规则链接到权威 `AGENTS.md`。

## Avoid

- 不复制仓库级规则，不为假设的场景增加通用流程。

## Validation

- 对照 `evals/` 中的正反触发样例和任务结果样例检查改动。
