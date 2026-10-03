# 仓库规范模板

适用于使用 [OpenSpec](https://openspec.dev/docs/quickstart) 管理变更与行为规格的 AI 辅助编码项目。`AGENTS.md` 保留常驻工程约束，避免与 OpenSpec 重复维护计划。

## 使用方法

1. 在目标仓库[安装并初始化 OpenSpec](https://openspec.dev/docs/setup)：运行 `openspec init`，保留生成的 `openspec/` 和工具专用工作流文件。本模板不复制这些生成物。
2. 将 `AGENTS.md`、`CLAUDE.md` 符号链接和 `ARCHITECTURE.md` 复制到目标仓库根目录，保留 `CLAUDE.md → AGENTS.md` 的链接关系，替换或删除示例行与占位内容。
3. 在 `ARCHITECTURE.md` 写入真实的系统边界与主要流程。`openspec/specs/` 记录当前产品行为，`openspec/changes/` 记录提案、设计、任务和变更历史；同一事项不要再建立平行的计划或决策记录。
4. 在已有的 `openspec/config.yaml` 的 `context` 中补充中文要求，不覆盖原有项目上下文：

   ```yaml
   context: |
     OpenSpec 产出物正文使用简体中文。
     保留工具要求的英文结构标题与关键字；代码标识符和路径保持原样。
   ```

5. 只有安全、可靠性或运维文档有实际内容时才添加入口。包级约束放在附近的嵌套 `AGENTS.md`；其他按需流程链接到真实存在的 Skill，并删除示例路由。
6. 核对目标仓库里的所有链接、路径和命令，确认 `CLAUDE.md` 指向同目录的 `AGENTS.md`。如果目标环境不能可靠检出符号链接，用只包含 `@AGENTS.md` 的 Claude 导入文件代替。

该链接只用于共享指令。Claude 与 Codex 的原生运行配置格式不同，应分别配置。

OpenSpec 的结构标记（如 `## Requirements`、`### Requirement:`、`#### Scenario:` 和变更规格中的 `## ADDED/MODIFIED/REMOVED Requirements`）保留英文，标记后的名称及正文可以写中文。已有需求标题是匹配标识；翻译现有标题时应按需求重命名处理，避免盲目批量替换。修改后运行 `openspec validate --all`。[多语言说明](https://github.com/Fission-AI/OpenSpec/blob/main/docs/multi-language.md)

`AGENTS.md` 是常驻规则与知识入口；OpenSpec 的生成 Skill 承担变更流程；`ARCHITECTURE.md` 概述当前系统边界并链接相关规格和变更设计。Agent 只按任务需要读取这些资料。

构建 Agent Runtime 或多 Agent 编排系统时，再参考独立的 [agent-harness 模板](../agent-harness/README.md)，按需引入执行环境与工具契约。

## 评测案例

裁剪模板时使用 [评测案例](evals/README.md)，检查 OpenSpec 与仓库指令的职责边界，以及新增工程约束是否真正影响行为。
