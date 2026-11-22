# Electron 运行时、性能、发布与 Codex 验证

适用：有 Electron 桌面宿主任务。本文件覆盖宿主边界、相关桌面交互与真实运行验证；其中交互部分按 Electron 场景保留本地完整步骤。

## 边界与安全

推荐职责：

```text
Renderer (React UI)
  ↕ 受限 window.desktopApi（业务动作，不暴露任意 channel）
Preload (contextBridge)
  ↕ typed IPC / 明确 channel / 参数验证
Main (窗口、菜单、许可、生命周期、任务路由)
  ↕ 按需创建 utilityProcess / 本地服务 / 文件与 DB
Utility Process (重 CPU / 大规模 I/O / 索引等)
```

- 默认 contextIsolation=true、sandbox=true、nodeIntegration=false。只暴露具体、最小的业务 API；不可直接暴露 ipcRenderer、fs、child_process、任意路径执行或通用 shell 命令。
- 在 Main 验证 IPC sender、授权上下文、路径/域名白名单、输入结构和数据大小/频率；Zod 是 schema 选择，不代替权限判断和来源校验。
- 远程内容/第三方资源隔离，限制导航、新窗口、权限、外部 URL，落实 CSP；不得为了开发方便关闭 webSecurity。
- 先读取实际项目的 Electron 版本和架构再使用 API；preload 的 sandbox 能力限制、asar、native addon、Node/Electron ABI 不可忽略。
- 参考：[Electron Security](https://www.electronjs.org/docs/latest/tutorial/security)、[IPC](https://www.electronjs.org/docs/latest/tutorial/ipc)、[Sandbox](https://www.electronjs.org/docs/latest/tutorial/sandbox)、[Context Isolation](https://www.electronjs.org/docs/latest/tutorial/context-isolation)。

## 启动与交互性能

按照官方指南的优先级调查：不必要依赖 → 启动过早加载 → Main 阻塞 → Renderer 阻塞 → 网络等待 → bundle。不要以 React/Svelte/Vue 的口碑代替真实分析。
- **启动**：Main 不做大块同步 I/O；按用户路径延迟初始化数据库、索引、模型服务、Monaco、报表等；记录从进程启动到主窗口可交互。
- **Renderer**：列表项规模大时测量布局/commit 耗时并考虑虚拟化；订阅局部状态；长文本分批，日志/流式消息有界缓冲。React Compiler 可按目标版本实验，不预设绝对收益。
- **宿主**：CPU/内存密集工作放到 Worker/utilityProcess，并设计取消、超时、退出清理；与 UI 通过受限 IPC 传递必要数据，避免高频巨量对象克隆。
- **资源**：只预加载关键字体与资源；避免多个不必要的隐藏 BrowserWindow；排查打包后本地资源路径和 native modules。
- **测量**：同一构建、同一数据规模、同一设备、至少多次冷/热启动，记录 P75/P95、UI 可交互时间、交互延迟、空闲 CPU、工作集内存、泄漏趋势。阈值从用户目标设备与现有版本定义，不使用通用虚构数字。
- 参考：[Electron Performance](https://www.electronjs.org/docs/latest/tutorial/performance)、[utilityProcess](https://www.electronjs.org/docs/latest/api/utility-process)。

## 原生体验与设计

本节参考 [client-ui-design 的平台适配](../../client-ui-design/references/platforms.md)及 [ui-ux-design 的原型流程](../../ui-ux-design/references/ai-prototyping.md)，本地调整为 Electron 宿主变更的交互验收；执行不依赖加载这两个 Skill。

1. 明确本次宿主动作对应的用户任务、入口和完成状态，复用现有组件与 Token。新增界面时先确定信息层级和内容密度；仅需单点修复时不重建设计系统。
2. 修改窗口或标题栏时，检查最小尺寸、分栏约束、拖动区域与可点击控件是否冲突；确认关闭、隐藏到托盘、重新打开和退出符合当前产品约定，未保存数据按约定处理。
3. 修改快捷键、菜单或弹层时，验证键盘能进入、执行和退出；关闭弹层后焦点回到合理位置，窗口恢复后输入目标仍可用。检查快捷键与文本编辑、系统快捷键的冲突。
4. 文件选择、拖放或权限操作覆盖成功、用户取消、无权限和无效输入。UI 应保留必要上下文并提供下一步，主进程仍独立校验权限与数据，不能把 UI 禁用状态当成授权。
5. IPC 长任务提供可观察的开始、进度或等待、完成、失败与适用的取消反馈。连续触发、窗口关闭再打开时避免重复任务或过期结果覆盖；窗口/组件卸载时清理订阅，恢复时重新建立必要状态。
6. 以真实文案、长文本、受影响的主题和窗口尺寸验证主路径与失败恢复。需要探索视觉候选时先比较任务效率和平台适配；只有要验证共享组件/主题时才补 Component Gallery。

原生菜单、托盘、文件对话框和 OS 快捷键在目标系统运行检查；Renderer DOM 断言与截图分别证明交互状态和布局，不能单独证明这些系统行为。

设计探索（Stitch、pen.dev、v0 等）为按需原型工具，不是必需依赖或真实性来源；将确定后的设计意图写到现有设计文档/Token 而不是产生多个并行设计系统。先复用组件，再开发产品专属块。不能把设计截图当作运行证明。

## 端到端验证

只执行当前变更需要的检查。先用项目已有测试工具；没有工具时，以下 Vitest / Playwright 是可选实现方式，不要求替换已有测试框架。

1. 从项目已存在的 `package.json`、构建产物和测试脚本确认可执行命令；必要时建立可重复的启动命令，不硬编码文档示例路径。
2. 用已有测试框架验证受影响的业务逻辑和输入校验；新建 Vite 项目可考虑 Vitest。修改 IPC 时覆盖契约及非法来源/参数拒绝行为。
3. 使用 Playwright Electron 启动 **真实应用**，进入一个完整核心流程，做 DOM 断言和截图。覆盖可观察的首次/空、加载、成功、失败/重试，UI 改动时按需求检查 Light/Dark、尺寸、长文案。
4. 用 DOM 定位作为主要自动化方式；系统托盘、文件选择器、原生授权等如需要，以 Electron Main 断言和 OS 级实测补齐。Playwright 官方 Electron 功能在 2026-10-18 复核时仍标为 experimental，采用时按项目版本确认。
5. 针对截图做视觉检查，但与状态断言区分；修复后重复同一流程。界面可用性不由 E2E 通过或截图单独证明。
6. 明确标注只跑了 Dev、打包后的 App 还是已签名安装包；不能在无 Windows 测试的情况下宣称 Windows 兼容或已完成自动更新。

参考：[Playwright Electron](https://playwright.dev/docs/api/class-electron)、[Vitest](https://vitest.dev/guide/why.html)。

## 打包、签名、更新

- 选择一个主发布链路：electron-builder 与 electron-updater 适合需要跨 macOS/Windows 多目标、发布 metadata、更新的项目；Forge 适合已采用 Forge 生态的项目。electron-vite 可以配合不同分发工具；禁止在没有需求时迁移。
- 检查产物真实路径、ASAR 排除/解包的二进制、原生模块 ABI、用户数据迁移、签名和 macOS notarization，以及 macOS/Windows 安装与卸载路径。
- 自动更新必须在真实安装态验证：更新检测/下载、失败恢复、签名、旧版本迁移及 Windows 安装器行为。发布通道和证书应遵循现有 CI，不写入密钥。
- 参考：[electron-vite Distribution](https://electron-vite.org/guide/distribution.html)、[electron-builder Auto Update](https://www.electron.build/docs/features/auto-update/)、[Electron autoUpdater](https://www.electronjs.org/docs/latest/api/auto-updater/)。

## 报告模板

```text
范围：目标平台 / Electron 版本 / 构建方式
结论：推荐方案 + 为什么 + 不采用什么
代码证据：入口、IPC 处理、窗口选项、当前依赖
测试证据：命令、环境、案例、通过/失败；截图或 trace 路径
性能证据：设备、样本次数、数据规模、冷/热 P75/P95、比较基线
发布证据：构建包、签名、公证、安装后更新测试
限制：没有跑过的平台、实验 API、尚未确认的假设
```
