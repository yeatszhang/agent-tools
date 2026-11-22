---
name: desktop-app-engineering
description: 比较 Electron、Tauri 与平台原生的桌面选型，并实现或排查 Electron 宿主、preload/IPC、权限、性能、打包更新与桌面验证。用于桌面选型及 Electron 工程任务；纯视觉设计、Web 页面、移动端和 Tauri 专属实现不触发。
metadata:
  status: draft
---

# 跨端桌面应用工程

仓库通用约束见 [AGENTS.md](../../AGENTS.md)。本 Skill 仍是 draft：有官方文档依据和案例草案，但未经过实际 Electron/macOS/Windows 项目验证。不要将推荐栈表述为基准测试胜出。

## 决策入口

1. 识别项目现状、目标平台、性能预算、分发方式及 Agent 能力。优先保留项目已在使用、可维护且通过验证的框架；新项目才进行完整选型。用户未限定桌面运行时时比较 Electron、Tauri 和平台原生，而非默认 Electron。
2. 新建 Electron 工程或要求逐层技术选型时，读取 [选型依据与替代方案](references/stack-decisions.md)。其中 Codex 主导场景的 React 优先是限定情境的工程假设，不是模型能力或运行性能事实；其余任务不预加载整套技术栈。
3. 任务涉及主进程、预加载脚本、权限、IPC、重任务、资源、原生模块、打包/升级、性能时，按相关部分读取 [运行时、性能、发布与验证](references/runtime-and-verification.md)。此处负责 Electron 宿主边界，不由 UI Skill 代替安全审核。
4. 纯产品任务流、界面状态、视觉方向或 Design Tokens → [ui-ux-design](../ui-ux-design/SKILL.md)；平台窗口、焦点、键盘、文件拖放和可访问性 → [client-ui-design](../client-ui-design/SKILL.md)；React Renderer 组件/DOM/Web UI 审查 → [web-ui-review](../web-ui-review/SKILL.md)；项目 AGENTS.md 策略路由 → [repo-spec-maintainer](../repo-spec-maintainer/SKILL.md)。单独处理上述领域时按对应 Skill 路由；宿主任务附带的窗口、输入与状态验收已在本 Skill 的运行参考中完整保存，不要求先加载兄弟 Skill。
5. 用户只要求选型或审查时交付相应结果；要求实现时再完成核心路径并选择相关验证。UI 行为用真实窗口操作与截图，IPC 用边界测试，性能用测量，发布用安装态验证；不为单点修复强制执行所有类别。

## 适用范围

- 下列宿主规则及运行参考仅适用于 Electron。Tauri 在本 Skill 中只参与选型比较；其权限、命令和发布实现应使用 Tauri 对应版本资料，不映射成 Main/Preload/IPC。
- [参考选型](references/stack-decisions.md)保留新建重交互工具的候选组合。先遵循当前项目与任务约束，不把参考组合视为必装依赖。
- 原型、浏览器预览、开发态应用和安装包验证是不同证据；报告实际运行的平台与模式。只具备一个平台的环境时，不声称已验证其余平台。

## 安全与性能门槛

- 创建或修改 Electron 权限边界时，使用隔离、sandbox 和受限 Preload API；Main 验证消息来源、业务权限与输入。具体配置与检查项见运行参考，不因无关 UI 修改扩展为整应用安全改造。
- Main 不承担阻塞型计算/大量同步 I/O；必要时使用 Utility Process/worker。启动过程延迟加载非关键模块；IPC 避免高频无界大对象传输。先剖析瓶颈再决定引入虚拟化、缓存、多进程或 React Compiler。
- 打包区分开发态与分发态；原生二进制、ASAR、签名与更新在安装后的程序上验证，不能只跑 dev server。

## 交付格式

- **技术选型**：项目约束 → 推荐 → 逐层原因 → 备选何时更优 → 证据类型（官方能力 / 工程经验 / 尚未验证）→ 需 A/B 验证的指标。
- **实现/排障**：改动范围 → 可复现问题与瓶颈 → 最小实现 → 实际运行证据 → 未验证部分和平台风险。
- 不为单个 UI 调整重构整个桌面架构；不以安装更多 Skills 或组件包作为默认优化措施。

## 验证

触发与结果案例见 [evals](evals/README.md)。设计决策、跨进程安全、实际性能和分发验证属于不同证据类型，应分别报告。
