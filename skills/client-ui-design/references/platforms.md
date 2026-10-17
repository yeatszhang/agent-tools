# 平台适配与参考选择

## 识别输入

技术栈应来自实际工程，例如 React Native/Expo 依赖、Flutter 的 `pubspec.yaml`、Swift 工程、Gradle/Compose 或桌面工程。只有能影响本次选择的版本信息才继续深入，不把所有平台都审查一遍。

## 移动端

关注当前任务涉及的安全区与固定操作栏、键盘遮挡、系统返回与手势、方向与尺寸变化、动态文字、读屏、权限和前后台恢复。按平台区分尺寸单位，不把 px/pt/dp 的数值直接互换。

优先使用已有导航和原生语义控件。内容应在真实文字和辅助设置下仍能完成任务；手势动作有适合平台的替代入口。网络失败、取消与返回不应无意清空用户输入。

## 桌面端

检查窗口缩放、分栏约束、焦点进入/返回、Tab 顺序、快捷键冲突、菜单和上下文操作。只在实际涉及多窗口、文件操作或任务恢复时检查对应场景，不把每次 UI 修改扩展成整套桌面架构设计。

不要把移动端底部导航、安全区和触控反馈直接套给键鼠工作台。高密度工具界面的可用性取决于任务、信息层级和输入效率，不能仅凭留白多少判断好坏。

## 深入资料

[来源索引](../../../tools/references/design-engineering/README.md)记录固定版本；以下离线资料仅在相关平台任务中读取：

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
