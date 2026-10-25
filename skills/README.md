# Skills

这里存放长期维护、跨 Agent 可复用的 Skills。Skill 是按需加载的 procedural knowledge，不用于承载所有任务都应遵守的仓库级 policy。

## 当前

- [writing-editor](writing-editor/SKILL.md)：中文 Humanizer + Personal Voice + diff learning。
- [repo-spec-maintainer](repo-spec-maintainer/SKILL.md)：创建、裁剪、审查项目级 `AGENTS.md`，并维护 AGENTS ↔ Skill 的 progressive-disclosure 关系。

## 桌面工程 Skill（draft）

- [desktop-app-engineering](desktop-app-engineering/SKILL.md)：单平台原生 / Electron / Tauri 选型及 Electron IPC、安全、性能与桌面自动化；含逐项选型依据。独立可用，不依赖未合并的设计 Skills。

## 全局安装与更新

当前 3 个 Skill 通过源目录符号链接共享给全局环境；同步命令、冲突处理与分支切换说明见 [仓库安装说明](../README.md#全局-skill-关联)。新增或删除 Skill 时同步维护本索引、`registry.yaml` 和根路由，然后运行同步脚本。

## AGENTS.md ↔ Skill

- `AGENTS.md`：always-on 规则、仓库事实、Skill 路由。
- `SKILL.md`：某类任务触发后才需要的 workflow、决策、命令与验证。
- 共享规则只保留一份，另一侧通过相对链接引用。

## 引入外部 Skill 的原则

优先 fork / 提炼真正需要的规则，而不是无脑堆多个相似 Skill。

外部项目可以作为 upstream inspiration，但最终稳定工作流尽量收敛到自己的 Skill。
