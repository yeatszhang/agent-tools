# agent-tools

个人 Agent 工具仓库：统一管理可复用的 Skills、Agents、MCP 配置说明、模板和评测资产。

## 目标

1. 一份源仓库，多 Agent 复用。
2. Skill 优先采用开放的 Agent Skills 结构，避免绑定单一运行时。
3. MCP 只记录可公开的配置结构与环境变量名，不提交密钥。
4. 所有“会学习”的 Skill 都把观察、候选规则、稳定规则分层，避免一次修改污染长期风格。
5. 重要 Skill 应有最小 eval，用修改前后样例验证，而不是只凭感觉迭代。

## 目录

```text
agent-tools/
├── skills/                 # 可复用 Skills
│   └── writing-editor/     # 中文去 AI 味 + Personal Voice
├── agents/                 # Agent 角色/工作流定义
├── mcp/                    # MCP catalog 与接入说明
├── tools/                  # 常用 CLI / 工具索引
├── templates/              # Skill / Agent 模板
├── scripts/                # 仓库级脚本
├── docs/                   # 约定与设计文档
└── registry.yaml           # 总索引
```

## 首个 Skill：writing-editor

目标不是“绕过 AI 检测”，而是：

```text
AI Draft
  ↓
Chinese Humanize
  ↓
Personal Voice
  ↓
人工修改
  ↓
Capture Diff
  ↓
Candidate Voice Rules
  ↓
Review / Eval
  ↓
Stable Voice
```

### 两层职责

- **Humanizer**：删除中文 AI 常见模式：空话、宏大开场、模板化总结、过度排比、讲义腔、互联网黑话、欧化句式等。
- **Personal Voice**：学习个人稳定偏好，例如结论优先、信息密度高、具体、有判断、少官话。

### 规则生命周期

```text
candidate → emerging → stable
                 ↘ rejected
```

一次编辑只能产生 candidate；重复观察后再进入 stable。

## 安全约定

- `.env`、token、cookie、个人隐私原文不进 Git。
- MCP 示例只提交环境变量名称，例如 `${GITHUB_TOKEN}`。
- `writing-editor` 的真实个人样例建议放私有仓库；若未来公开仓库，先做脱敏。
