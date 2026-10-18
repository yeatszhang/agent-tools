# Skills

这里存放长期维护、跨 Agent 可复用的 Skills。Skill 是按需加载的 procedural knowledge，不用于承载所有任务都应遵守的仓库级 policy。

## 当前

- [writing-editor](writing-editor/SKILL.md)：中文 Humanizer + Personal Voice + diff learning。
- [repo-spec-maintainer](repo-spec-maintainer/SKILL.md)：创建、裁剪、审查项目级 `AGENTS.md`，并维护 AGENTS ↔ Skill 的 progressive-disclosure 关系。

## 设计与前端工程草案

- [ui-ux-design](ui-ux-design/SKILL.md)：产品任务、交互状态、视觉方向与设计 Token。
- [web-ui-review](web-ui-review/SKILL.md)：基于代码与运行证据审查 Web UI、无障碍和前端性能。
- [client-ui-design](client-ui-design/SKILL.md)：按实际平台处理原生/桌面客户端布局、导航、输入与反馈。
- [desktop-app-engineering](desktop-app-engineering/SKILL.md)：Electron/Tauri/原生桌面选型，以及 Electron 进程/IPC、安全、性能、分发与验证；[逐项选型依据](desktop-app-engineering/references/stack-decisions.md)单独按需加载。Tauri 的具体实现尚未纳入。

以上均为 `draft`，附触发与结果评测案例，尚未经过真实项目行为验证。[调研结论](../docs/research/design-engineering.md)与[上游原文快照](../tools/references/design-engineering/README.md)分开保存。

设计类任务按交付目标选择主 Skill：产品流程与视觉方案用 `ui-ux-design`；已有 Web UI 审查用 `web-ui-review`；平台导航、焦点、窗口与输入行为用 `client-ui-design`；Electron 宿主与发布用 `desktop-app-engineering`。跨层任务只加载涉及的部分，不默认叠加四套完整流程。

## AGENTS.md ↔ Skill

- `AGENTS.md`：always-on 规则、仓库事实、Skill 路由。
- `SKILL.md`：某类任务触发后才需要的 workflow、决策、命令与验证。
- 按 [仓库原则](../AGENTS.md) 优先保留本地可执行内容；只有完全相同的规则共享引用，场景化步骤可放在各 Skill 的 `references/`。

## 引入外部 Skill 的原则

优先 fork / 提炼真正需要的规则，而不是无脑堆多个相似 Skill。

外部项目可以作为 upstream inspiration，但最终稳定工作流尽量收敛到自己的 Skill。
