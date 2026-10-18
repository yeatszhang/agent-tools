# 平台适配与参考选择

## 识别输入

技术栈应来自实际工程，例如 React Native/Expo 依赖、Flutter 的 `pubspec.yaml`、Swift 工程、Gradle/Compose 或桌面工程。只有能影响本次选择的版本信息才继续深入，不把所有平台都审查一遍。

## 移动端

关注当前任务涉及的安全区与固定操作栏、键盘遮挡、系统返回与手势、方向与尺寸变化、动态文字、读屏、权限和前后台恢复。按平台区分尺寸单位，不把 px/pt/dp 的数值直接互换。

优先使用已有导航和原生语义控件。内容应在真实文字和辅助设置下仍能完成任务；手势动作有适合平台的替代入口。网络失败、取消与返回不应无意清空用户输入。

## 桌面端

检查窗口缩放、分栏约束、焦点进入/返回、Tab 顺序、快捷键冲突、菜单和上下文操作。只在实际涉及多窗口、文件操作或任务恢复时检查对应场景，不把每次 UI 修改扩展成整套桌面架构设计。

不要把移动端底部导航、安全区和触控反馈直接套给键鼠工作台。高密度工具界面的可用性取决于任务、信息层级和输入效率，不能仅凭留白多少判断好坏。

## 各栈的本地检查步骤

以下是面向客户端任务的本地适配；来源见后面的固定快照。本地调整强调状态保持、生命周期和可验证结果，不将上游的库偏好或数值门槛直接作为项目要求。按实际栈选一行执行，不必读取其他平台资料才能开始。

| 技术栈 | 检查与处理 | 验证路径 |
| --- | --- | --- |
| React Native / Expo | 追踪列表项身份、订阅、图片与动画更新；确认键盘遮挡处理和现有导航一致。先定位 JS/布局/图片瓶颈，再决定是否调整列表或动画实现 | 搜索输入 → 打开详情 → 返回；保留搜索词和滚动上下文。按目标设备检查键盘、长列表与后台恢复 |
| SwiftUI | 确认输入状态的持有者与视图身份，避免导航或刷新重建时丢失编辑；优先复用现有导航与系统控件，检查动态文字和辅助标签 | 编辑中切换页面/返回、失败重试；放大文字后仍可到达提交与取消，使用目标系统读屏检查顺序 |
| Android Compose | 检查状态提升与事件回传是否一致，区分瞬时 UI 状态与需恢复的数据；键盘、系统栏、返回处理遵循当前工程约定 | 旋转/重建、返回、键盘展开与关闭；确认未提交输入按产品约定保留，不重复提交请求 |
| Flutter | 检查 Widget 身份、控制器与订阅生命周期，避免重建重复发起副作用；布局约束与键盘避让配合现有导航 | 输入、页面退出再进入、文字缩放与不同窗口尺寸；确认没有重复监听、过期结果回写或被遮住的操作 |
| WPF / WinUI / Avalonia | 检查绑定、命令可用状态、UI 线程更新和窗口生命周期；焦点顺序、快捷键及缩放使用平台行为 | 连续开关窗口、缩小窗口、键盘完成任务、显示缩放与主题变化；确认状态和资源正确恢复/释放 |

对异步操作，逐项确认开始反馈、禁止或合并重复提交、失败保留输入、取消后的状态与返回目的地。性能调整必须使用目标设备测量；具体状态管理、导航和动画 API 以工程版本为准，不能从本表推断某版本一定支持。

## 深入资料

[来源索引](../../../tools/references/design-engineering/README.md)记录固定版本；以下离线资料仅在相关平台任务中读取：

先执行本页本地步骤；以下逐字快照共用仓库副本，只用于深入核对与溯源。单独导出本 Skill 时若未携带它们，按需查[UI UX Pro Max 数据上游](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/src/ui-ux-pro-max/data/stacks)或[Vercel RN 规则](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-native-skills)，并核对实际项目版本；不要自动安装整个资料库。

| 技术栈 | 本地入口 | 范围 |
| --- | --- | --- |
| React Native / Expo | [Vercel RN](../../../tools/references/design-engineering/upstream/agent-skills/skills/react-native-skills/SKILL.md) | 列表、原生导航、图片、手势、动画和依赖组织 |
| SwiftUI | [swiftui.csv](../../../tools/references/design-engineering/upstream/ui-ux-pro-max-skill/src/ui-ux-pro-max/data/stacks/swiftui.csv) | 状态、布局、导航、辅助能力的条目 |
| Android Compose | [jetpack-compose.csv](../../../tools/references/design-engineering/upstream/ui-ux-pro-max-skill/src/ui-ux-pro-max/data/stacks/jetpack-compose.csv) | 组合、状态、列表、布局和平台能力 |
| Flutter | [flutter.csv](../../../tools/references/design-engineering/upstream/ui-ux-pro-max-skill/src/ui-ux-pro-max/data/stacks/flutter.csv) | Widget、布局、状态、生命周期和辅助能力 |
| WPF / WinUI | [wpf.csv](../../../tools/references/design-engineering/upstream/ui-ux-pro-max-skill/src/ui-ux-pro-max/data/stacks/wpf.csv) · [winui.csv](../../../tools/references/design-engineering/upstream/ui-ux-pro-max-skill/src/ui-ux-pro-max/data/stacks/winui.csv) | XAML、绑定、命令、线程、窗口与主题条目 |
| Avalonia | [avalonia.csv](../../../tools/references/design-engineering/upstream/ui-ux-pro-max-skill/src/ui-ux-pro-max/data/stacks/avalonia.csv) | 跨平台控件、绑定、输入、窗口与文件选择条目 |

UI UX Pro Max 还提供 JavaFX、Uno、UWP 等栈的数据，但未在本次逐条验证。通过其检索脚本按栈查询时，核对 `Applies To`、`Status` 和官方文档；这些字段是上游记录，不是对当前工程的兼容保证。

Vercel 某些 RN 条目偏好特定库或对所有列表推荐虚拟化。实践中应结合已有依赖、列表复杂度和测量；小型静态设置页不必为此换库。React Compiler / Reanimated 等组合的 API 需单独核对版本。

## 验证证据

原生检查报告应区分代码审查、模拟器运行、真机操作和性能分析。截图适合检查布局，但不能证明系统键盘、返回手势、读屏和线程性能。没有目标环境时提供具体待验证路径，保留草案与未验证标记。
