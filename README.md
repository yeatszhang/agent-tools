# agent-tools

个人 Agent 工具仓库：统一管理可复用的 Skills、Agents、MCP 配置说明、模板和评测资产。

## 目标

1. 一份源仓库，多 Agent 复用。
2. Skill 优先采用开放的 Agent Skills 结构，避免绑定单一运行时。
3. `AGENTS.md` 承载 always-on policy，Skill 承载按需 workflow；两者用链接协作，不复制规则。
4. MCP 只记录可公开的配置结构与环境变量名，不提交密钥。
5. 所有“会学习”的 Skill 都把观察、候选规则、稳定规则分层，避免一次修改污染长期风格。
6. 重要 Skill 应有最小 eval，用修改前后样例验证，而不是只凭感觉迭代。

## 目录

```text
agent-tools/
├── skills/
│   ├── writing-editor/          # 中文去 AI 味 + Personal Voice
│   └── repo-spec-maintainer/    # 创建/审查 AGENTS.md 的按需工作流
├── agents/                      # Agent 角色/工作流定义
├── mcp/                         # MCP catalog 与接入说明
├── tools/                       # 常用 CLI / 工具索引
├── templates/
│   ├── skill/                   # Skill 模板
│   └── repo-spec/               # 新项目 AGENTS.md / 工程约束模板
├── scripts/                     # 仓库级脚本
├── docs/                        # 约定与设计文档
└── registry.yaml                # 总索引
```

## AGENTS.md 与 Skill 的边界

推荐使用 progressive disclosure：

```text
AGENTS.md
  ├─ always-on invariants
  ├─ repository facts
  └─ route: "when X, read skills/x/SKILL.md"
                         ↑
SKILL.md                 │
  ├─ conditional workflow
  ├─ commands / decisions│
  └─ shared policy: -----┘ link back to AGENTS.md
```

- 一个事实只有一个 authoritative home。
- Root `AGENTS.md` 尽量短；只保留几乎每个任务都需要知道的规则。
- 包/目录特有规则优先放最近的 nested `AGENTS.md`。
- 长流程、决策树、验证步骤进入 Skill。
- 长背景、示例和 rationale 进入 `references/` 或 docs。

## Repo Spec Template

[templates/repo-spec/AGENTS.md](templates/repo-spec/AGENTS.md) 是启动 AI-assisted coding 项目时的默认工程规范模板，吸收了 Paseo 等 AI-native codebase 中高质量约束，重点防止：

- speculative abstraction / 过度设计
- defensive coding / silent fallback
- unrelated cleanup / diff 扩散
- refactor layering / 新旧路径长期并存
- type-system bypass
- mock-driven false green
- 静态阅读替代 runtime evidence
- 全仓库无差别验证

[repo-spec-maintainer](skills/repo-spec-maintainer/SKILL.md) 负责把模板裁剪成具体项目的 `AGENTS.md`，而不是把模板本身当作 Skill。

## writing-editor

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

一次编辑只能产生 candidate；重复观察后再进入 stable。

## 安全约定

- `.env`、token、cookie、个人隐私原文不进 Git。
- MCP 示例只提交环境变量名称，例如 `${GITHUB_TOKEN}`。
- `writing-editor` 的真实个人样例建议放私有仓库；若未来公开仓库，先做脱敏。
