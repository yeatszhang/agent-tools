---
name: desktop-app-engineering
description: 为单平台或跨平台桌面应用比较原生 SwiftUI/WinUI、Electron 与 Tauri，并执行 Electron 宿主/IPC、权限、性能、打包及桌面自动化验证。用于桌面技术选型或 Electron 工程任务；纯 Web UI 和移动端任务不触发。
metadata:
  status: draft
---

# 桌面应用技术选型与 Electron 工程

仓库通用规范见 [AGENTS.md](../../AGENTS.md)。本 Skill 为草案，未经真实 macOS/Windows 桌面产品验证；不得将推荐技术栈误写成基准测试胜者。

## 决策流程

1. 先核查已有项目框架、目标 OS、依赖资产、交互复杂度、原生集成程度、性能预算和发布方式。维护现有项目时不为统一技术栈而迁移。
2. **当前开发者的默认选择**：新建 **macOS + Windows** 跨平台桌面应用优先 Electron，充分利用熟悉的 Node.js/TypeScript、React 生态和 Codex 的 JS/TS 工程与测试工具链。**单平台、UI 简单且原生系统集成为主**时优先评估 macOS SwiftUI 或 Windows WinUI 3；若依赖大量 Node SDK，则仍可选 Electron。**跨平台、UI 简单且安装包/常驻内存等有硬性能约束**时再重点评估 Tauri 2。复杂、数据密集但高性能敏感的应用仍需通过 PoC 判断，不机械选 Electron。
3. 新项目、框架横向对比或技术选型依据需求，读取 [逐层选型依据](references/stack-decisions.md)。React 的默认优先级来自生态、熟悉度与 AI 工作流的工程判断；不存在“Codex 天然更理解 React”的已验证结论。
4. Electron Main / Preload / IPC、权限、Native Module、进程管理、性能、打包及更新相关任务按需读取 [宿主与真实验证](references/runtime-and-verification.md)。Tauri/SwiftUI/WinUI 具体实现必须读取各自版本官方资料，不将 Electron 安全 API 套用到其他宿主。
5. UI 任务先沿用项目 Design Tokens 与组件库；桌面端重点验证原生窗口习惯、菜单、键盘/焦点、分栏缩放、长文本、空/失败/加载状态。纯视觉设计和 DOM 代码审查不触发宿主级安全重构。仓库规范与 Skill 路由维护交给 [repo-spec-maintainer](../repo-spec-maintainer/SKILL.md)。
6. 根据影响选择验证：UI 需要目标窗口运行与截图、IPC 需要边界测试、性能需要相同环境数据、发布需要安装态检查。只要求选型不创建项目；仅改小功能不强制跑所有测试。

## Electron 工程约束

- React Renderer 只暴露业务语义 API，不允许任意 Node.js/文件操作；通过隔离的 Preload 与 Main 进行受限 IPC，Main 验证 sender、权限和运行时参数。
- 启动路径避免同步加载非关键资源，Main 不执行长时间同步任务；经实测需要时再引入 Utility Process、Worker、虚拟化或缓存。
- 面向 Codex 的推荐起点（不是必装清单）：electron-vite、React、TypeScript strict、shadcn/ui + Base UI、Tailwind v4、Vitest 与按需的 Playwright Electron。Zustand、Zod、SQLite、Motion 等按实际需求决定。
- dev server 启动成功不等于安装包正常；macOS/Windows 签名、原生模块、权限和更新须分别验证。

## 交付与证据

记录已知约束、推荐方案、反例、官方能力和工程判断的边界，以及真实测试环境、命令、结果和未验证项目。不要虚构启动时间、包大小、内存或 AI 生成正确率。触发与验收案例见 [evals](evals/README.md)。
