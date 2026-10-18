# Electron + Codex 技术栈选型：依据、边界与反例

基准日期：2026-10-17。适用：新建 macOS/Windows 桌面效率工具，独立开发，Codex 为主要开发者，优先默认体验与实测性能。**不是**所有桌面项目强制栈；现有稳定项目保留现状优先。官方文档说明的是能力，综合选择仍属于工程判断。2026-10-18 复核了 shadcn Base UI 默认值、Forge Vite 和 Playwright Electron 的实验状态；没有重新验证所有依赖。

## 逐层决策

| 层次 | 建议与具体原因 | 什么时候改选 / 代价 | 依据类型与入口 |
| --- | --- | --- | --- |
| 桌面运行时 | **Electron**：捆绑 Chromium，跨平台 Web 渲染环境相对一致；Node.js、窗口、托盘、文件/菜单、进程管理生态成熟；适合 React/Codex 复用 UI 资产。 | 目标以安装包大小、空闲 RAM 为硬约束，且可接受各系统 WebView 差异，可评估 **Tauri**；macOS-only 且原生交互优先可评估 SwiftUI/AppKit。Electron 运行时基线更大，不能宣称性能更优。 | 官方能力：[Electron 进程模型](https://www.electronjs.org/docs/latest/tutorial/process-model)、[Tauri 概述](https://v2.tauri.app/start/)；推荐为工程判断。 |
| 构建 | **electron-vite**：一份入口配置覆盖 Main、Preload、Renderer；Renderer HMR、Main/Preload 热重载、React TS 模板；贴合 Vite 项目。 | 已基于 Forge 的项目无需迁移；若优先使用 Forge 插件/发布体系可用 Forge，但其 Vite 插件当前被标记为 experimental，升级要读变更。electron-vite 加快迭代，不直接证明产品运行时更快。 | 官方：[electron-vite Guide](https://electron-vite.org/guide/)、[Forge Vite Plugin](https://www.electronforge.io/config/plugins/vite)。 |
| UI 框架 | **React + TypeScript strict**：现成组件、AI 生成 UI 的工作流和复杂工作区集成资源广；便于复用 shadcn/ui、状态库与测试范式。TS 提供明确接口，降低跨组件改动的不确定性。 | **Vue 3** 的 Composition API 更简洁、响应式直接，成熟 Vue 代码库优先沿用；Svelte 适合追求极简 Renderer 体积的项目。没有直接的 2026 Codex 长任务对照数据证明 React 的 AI 正确率高于 Vue。 | 工程生态判断；官方：[React](https://react.dev/)、[Vue](https://vuejs.org/)、[React Compiler](https://react.dev/blog/2025/10/07/react-compiler-1)；需项目 A/B。 |
| UI 原语与组件 | **shadcn/ui + Base UI**：项目持有组件源码，容易让 Codex 定点修改；Base UI 提供 headless、无障碍行为原语；组件库与产品视觉设计可分离。2026-07 新建项目默认 Base UI，Radix 仍支持。 | 已用 Radix 无需迁移；大量复杂业务表格可考虑成熟企业组件方案；组件源码自持意味着要维护升级与回归。shadcn 默认样式 ≠ 独特产品设计。 | 官方：[shadcn 2026-07](https://ui.shadcn.com/docs/changelog/2026-07-base-ui-default)、[Base UI](https://base-ui.com/react/overview/quick-start)。 |
| 样式与 Token | **Tailwind CSS v4 + 语义 CSS Token**：CSS-first 的 theme variables 与 shadcn 兼容；统一 Token 能约束 AI 随意造颜色/间距，也方便主题切换。 | 既有 CSS Modules/vanilla-extract 项目不必重构；Tailwind 可能制造长 className 和动态 class 拼装问题，复杂样式可留在独立 CSS。 | 官方：[Tailwind v4](https://tailwindcss.com/blog/tailwindcss-v4)、[shadcn Tailwind v4](https://ui.shadcn.com/docs/tailwind-v4)。 |
| 图标 | **Lucide React**：同一 SVG 语言、React 组件化、易约束尺寸和描边。 | 品牌图标/专有符号单独设计；不要为了少数自定义图标引入第二套通用图标包。 | [Lucide](https://lucide.dev/)。 |
| 状态 | **先本地 state，再 Zustand**：Store API 小，组件可按 selector 订阅，减少不必要的全局状态样板；UI 状态与服务端缓存分离。 | 少量组件仅用 React state；需要极严格的事件记录/复杂状态流时考虑 Redux Toolkit 或状态机；不把每个输入框都放进全局 Store。 | 官方：[Zustand Intro](https://zustand.docs.pmnd.rs/learn/getting-started/introduction)。 |
| 跨进程输入 | **typed IPC + Zod**：TS 定义契约、Zod 在高权限 Main 边界实际解析输入；Preload 仅暴露业务能力。静态类型在进程边界不等于运行时安全。 | 现有验证库可复用，不必为 Zod 换库；不允许 Renderer 调用任意 channel 或执行文件路径。 | 官方：[Electron IPC](https://www.electronjs.org/docs/latest/tutorial/ipc)、[安全检查清单](https://www.electronjs.org/docs/latest/tutorial/security)、[Zod](https://zod.dev/)。 |
| 异步远程数据 | **TanStack Query 按需**：有网络请求、缓存/去重/重试和服务器状态同步时再引入，不代替 UI 本地状态。 | 仅本地设置或直接同步读取时不装；实时 IPC 事件流应单独设计有界缓冲，不把无限日志塞 Query。 | 官方：[TanStack Query](https://tanstack.com/query/latest/docs/framework/react/overview)。 |
| 数据存储 | **少量设置 → JSON / electron-store；关系数据 → SQLite**：把简单 KV 与查询型历史数据区分，先最小化依赖。 | 包含搜索/筛选/聚合、迁移或大量记录时上 SQLite；原生模块需考虑 Electron ABI、签名和 ASAR unpack。 | 工程判断；打包证据：[electron-vite Distribution](https://electron-vite.org/guide/distribution.html)。 |
| 长列表 | **TanStack Virtual 按需**：文件列表、日志、长会话等需要控制 DOM 数量时用虚拟化。 | 几十条静态内容无需引入；高变高/键盘焦点/滚动定位需专项测试。 | 官方：[TanStack Virtual](https://tanstack.com/virtual/latest/docs/introduction)。 |
| 动效 | **CSS 优先；Motion 按需**：简单 hover、fade 使用 CSS；共享布局/可中断复杂交互 Motion 更合适。 | 不要把每个交互都渲染成 JS 动画；遵循系统 reduced motion。 | 官方：[Motion for React](https://motion.dev/docs/react)。 |
| 单测 | **Vitest**：复用 Vite 转换流程、适合 TS/React 逻辑和组件测试；无需维护第二套打包转译配置。 | 已有 Jest 且运行稳定时无须迁移；单测不能证明真实窗口行为。 | 官方：[Why Vitest](https://vitest.dev/guide/why.html)。 |
| 桌面 E2E | **Playwright Electron**：启动 Electron，访问窗口、读页面状态、执行 DOM 操作和截图，允许 Codex 形成实现→运行→检查闭环。 | 官方仍标 experimental；原生文件对话框、托盘、权限弹窗需补主进程或 OS 层测试；纯浏览器截图不足以验收。 | 官方：[Playwright Electron](https://playwright.dev/docs/api/class-electron)。 |
| 打包与更新 | **electron-builder + electron-updater**（当采用其发布流水线时）：macOS/Windows 包及更新 metadata、发布渠道、阶段性升级支持。 | 项目已使用 Forge 就继续用 Forge；自动更新涉及签名、公证、证书/托管服务、安装态验证。不要把 builder 与 Forge 都设为默认发布。 | 官方：[electron-builder Auto Update](https://www.electron.build/docs/features/auto-update/)、[Electron autoUpdater](https://www.electronjs.org/docs/latest/api/auto-updater/)。 |
| AI 开发约束 | **Codex + 简短 AGENTS.md + 按需 Skills**：仓库约束定义架构红线，Skills 按 UI 设计、宿主架构、验证分别加载，防止工具和规则互相覆盖。 | 没有真实改动任务不应先安装一批 UI Skill；不把外部 Skill 经验直接当项目政策。 | 官方：[Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md/)、[项目 Skill 规范](../../../templates/skill/README.md)。 |

## React 而不是 Vue：判定法

- **选择 React**：新项目，团队/Agent 主要围绕 React + shadcn 生态工作；工作区较复杂；计划复用大量 React 组件和设计生成器输出。
- **选择 Vue**：既有 Vue 熟练度、组件/代码资产或更好的项目实测；没有明确依赖 React 生态。
- **不得宣称**：模型在语义上天然更容易理解 React、React 一定更快、任何模型代码生成基准能直接证明 Electron 长期质量。
- **验证方式**：同样需求、约束、Codex 模型档位、时间与目标设备；比较一次通过率、改动轮次/修复次数、E2E 成功率、可维护性、Token 开销、启动和交互 P75/P95；至少对一个完整流程及后续变更任务测试。

## AI Native 产品设计，不属于运行时选型

桌面宿主任务涉及的产品任务、窗口、焦点、异步状态与视觉验收，按本 Skill 的 [原生体验与设计](runtime-and-verification.md#原生体验与设计) 执行。该流程已保留 Electron 场景的完整本地版本及来源，组件 Gallery 按实际需要建立。

## 推荐分层交付

- **参考起点**：选定 Electron 后，可从 electron-vite、React、TypeScript 及既定组件/样式方案开始；保留符合项目约束的替代方案。需要跨进程能力时建立受限接口；按本次改动选择验证，交付安装包时再配置分发链路。这个列表不是 MVP 必装清单。
- **满足条件再加**：SQLite、Query、Virtual、Motion、Monaco、全文搜索、遥测、自动更新、utilityProcess。
- **不默认采用**：Next.js、重量级 ORM、全局 Redux、多套 UI 组件库、多个相似设计 Skill、未经验证的复杂多 Agent harness。

## 证据使用约束

1. 官方资料只证明具体支持能力与 API；“综合最佳”“更适合 Codex”属于结合场景的工程判断。
2. 版本和发布时间会变化：新增依赖、发布链路、平台 API 变动需检查当时官方文档，不把此页写成永久升级清单。
3. 性能指标先建立相同条件基线；没有测试数据时不填入虚构的启动时间、内存占用、FPS 或 AI 正确率。
