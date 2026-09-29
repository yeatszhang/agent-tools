# Conventions

## Skill 设计

一个 Skill 应回答四件事：

1. 什么时候触发。
2. 核心工作流是什么。
3. 哪些规则必须遵守。
4. 如何验证输出是否变好。

`SKILL.md` 保持短小。大段规则、样例、场景说明放到 `references/` 和 `examples/`。

## 学习型 Skill

长期偏好分为三层：

- `candidate`：一次观察。
- `emerging`：多次出现但证据仍不足。
- `stable`：经过重复观察和 eval，进入默认行为。

不要让 Agent 因单次改动直接重写稳定规则。

## MCP

仓库只维护：

- server 名称
- 官方/上游地址
- transport
- command/url 模板
- 所需环境变量名
- 使用场景
- 本地启用状态说明

永远不提交真实 token / key。

## Evals

每次升级 Stable Rule，至少补一个 case。

优先观察：

- 事实是否保持
- 原始判断是否保持
- AI-pattern 是否减少
- Voice 是否一致
- 人工二次修改量是否下降
