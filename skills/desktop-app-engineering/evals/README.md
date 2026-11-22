# 跨端桌面工程 Skill 评测

状态：draft。下列是触发/质量案例，不代表已经在 Electron/macOS/Windows 做过真实行为评测。

| 类型 | 输入 | 预期行为 |
| --- | --- | --- |
| 应触发 | 用 Codex 新建跨平台 Electron 高性能工具，论证 React 与 Vue | 给出选型条件、逐项原因、备选、官方证据与应实测的疑点；不称 React 更容易被模型理解 |
| 应触发 | Electron Renderer 能随意调用 ipcRenderer，修复权限边界 | 使用受限 preload 业务 API，在 Main 校验 sender/参数与授权 |
| 应触发 | Electron 冷启动很慢，要定位原因 | 先测加载/主线程/资源，再选择延迟加载、worker，不直接建议换 UI 框架 |
| 应触发 | macOS/Windows 自动更新发布检查 | 检查安装态、签名与回滚/迁移流程，区分构建成功和更新成功 |
| 应触发 | 只比较 Electron 与 Tauri 的选型，不创建工程 | 给出约束与取舍，不生成项目或安装依赖 |
| 不应触发 | 修改现有 Tauri v2 capability 权限 | 查 Tauri 官方资料，不套 Electron preload 与 contextIsolation |
| 不应触发 | 只修改 Web 登录页的错误提示 | 路由 ui-ux-design / web-ui-review |
| 不应触发 | SwiftUI 页面的键盘焦点无法返回 | 路由 client-ui-design |
| 不应触发 | 只调整 AGENTS.md 的 Skill 规则 | 路由 repo-spec-maintainer |
| 不应触发 | 数据库服务端 SQL 优化 | 不触发 |

## 结果质量案例

1. **已有 Vue 项目**：已有 Vue 组件资产和稳定功能。不能因默认栈写着 React 就强行迁移；须说明新增依赖的成本。
2. **冷启动性能**：缺少目标设备/基线。不能捏造毫秒、FPS、内存节约比例；列出测量口径。
3. **渲染器越权**：只加 TypeScript 类型但没有 Main 校验。必须指出运行时校验与 sender 认证缺口。
4. **视觉交互职责**：用户要求重新设计桌面命令面板。纯设计任务按 UI/UX 与 client UI 路由；宿主变更涉及命令面板交互时，使用本 Skill 本地步骤检查窗口、焦点和异步反馈，不因已有兄弟 Skill 就删掉这些步骤。
5. **MVP 最小性**：没有远程数据/复杂列表/结构化存储，不默认加 TanStack Query、Virtual、SQLite、Motion。
6. **发布真实性**：只执行 pnpm build 后不得声称 Windows 已安装验证、macOS 已签名或更新链路可用。
7. **AI 生成对照**：只有单个截图不能证明某框架对 Codex 更合适；比较持续改动、测试成功率和成本。
8. **单点验证**：只修复 IPC 参数校验。使用已有测试框架覆盖受影响边界，不强制安装 Vitest 或执行完整打包更新测试。
9. **框架边界**：Tauri 只参与选型比较；不得声称 Electron 参考已覆盖 Tauri 命令权限与升级实现。

晋级 stable 前：在真实 Electron 项目执行至少一条安全 IPC 变更、一条 UI + Playwright Electron 交互路径和一次桌面打包/启动验证，并保存实际命令与结果。

## 本地资料可用性案例

只有本 Skill 和 Electron 工程，没有兄弟 Skill。修复托盘恢复后输入失焦时，使用本地步骤定位窗口/焦点恢复并给出目标系统验证路径，不要求先安装其他 Skill。

此案例需实际运行后记录结果；新增案例不代表已通过行为评测。
