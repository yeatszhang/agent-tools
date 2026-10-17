# UI/UX、产品设计与前端开发 Skill 调研

日期：2026-10-17。原始链接、提交版本、离线资料和校验方法统一维护在[来源索引](../../tools/references/design-engineering/README.md)，不在这里重复维护。

## 结论

建议采用“产品任务与交互 → 视觉与设计系统 → 平台实现 → 运行验证”的协作方式。这是本次综合判断，不是任何一个上游已经提供的完整流程。

三个来源互补：Anthropic 值得学习如何形成有依据的视觉方向；UI UX Pro Max 值得学习结构化知识检索和设计决策持久化；Vercel 值得学习按影响排序、带反例和正确示例的工程规则。全部安装会造成触发重叠，不能代替清晰的任务边界。

已提炼三个仓库内的草案 Skill：

| 草案 | 任务与产出 | 当前证据 |
| --- | --- | --- |
| [ui-ux-design](../../skills/ui-ux-design/SKILL.md) | 把产品目标落实为任务流、状态、视觉方向和可实现的界面方案 | 上游设计流程 + 设计 Token/状态资料；产品任务模型是本地补充 |
| [web-ui-review](../../skills/web-ui-review/SKILL.md) | 基于代码和运行证据审查 Web UI，给出可定位的问题 | Vercel Web 规则、React 性能和组合模式 |
| [client-ui-design](../../skills/client-ui-design/SKILL.md) | 在已识别的平台中设计、实现或审查客户端交互 | RN 分条规则 + UI UX Pro Max 各原生/桌面栈资料 |

均为 `draft`，包含触发与结果评测案例。没有全局安装、没有把上游审美偏好变成根目录常驻规则，也没有声称经过真实产品验证。

## Anthropic：视觉设计判断与开发流程

阅读了仓库 README、插件索引、frontend-design 原文，以及 feature-dev/code-review 的 README。没有分析闭源运行时，也没有逐个运行插件。

frontend-design 的主要价值在于把视觉选择与业务主题、受众和内容连接起来：先形成精简的颜色、字体、布局方向，再检查是否贴合任务；构建中通过截图批评和修正。文案与操作反馈也被视为界面设计的一部分。[固定版本原文](https://github.com/anthropics/claude-code/blob/c017428c8c27e604840435048d5bce6a9a22c040/plugins/frontend-design/skills/frontend-design/SKILL.md)

值得吸收的是设计理由、自我检查和节制。不要照搬其中“客户已经拒绝模板方案”的假设，也不要为了不同而推翻已有品牌、组件库或用户指定风格。列举某些视觉套路是校准提示，不是永久禁用清单。

feature-dev 展示了先理解现有代码再设计实现的流程；code-review 强调减少低证据误报。可吸收探索现有实现、比较方案、验证发现这些思路。其固定多 Agent 数量、审批阶段和 GitHub 自动发评并非本仓库默认行为。

## UI UX Pro Max：检索知识与设计系统

阅读了主 Skill、仓库说明，以及 Token、状态、原生交互参考；检查了其他六个 Skill 的元数据与入口路由、CSV 结构、平台覆盖和检索源码，并运行了代表性查询。没有验证所有 CSV 行、所有技术栈或 AI 图像生成器。

主 Skill 区分整体设计、单点 UX 和技术栈查询。源码使用 BM25 与本地规则，不应把 README 的“AI-powered”措辞理解为每次搜索都调用模型。数据可按产品、视觉风格、配色、字体、图表和技术栈检索。[固定版本](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/56ea9cf174ed86786187daa9de0e6247cb0747e4)

值得提炼的机制：

- 查询围绕一个意图；验证结果属于当前产品、交互和平台。
- 全局设计决策与页面差异分开，但复用项目已有的 Token 和组件资产。
- 设计 Token 可分为原始值与语义映射；组件存在独立定制需求时再增加组件层。
- 用状态矩阵补全加载、错误、禁用、空数据等界面行为。
- 细节参考按需加载，避免把几十种配色和技术栈塞进一个入口。

检索数据是经验推荐，不是用户研究、可用性测试或平台官方标准。不能把某类行业推荐的颜色、字体、深色模式和动效变成默认品牌策略。数据库的 `Verified At` / `Applies To` 是上游记录，不能替代目标项目版本核对。

其他 Skill 中，`design-system` 的 Token 与状态建模最适合复用；`brand` 的品牌一致性可在有品牌需求时参考；`ui-styling` 适合已有 shadcn/Tailwind 技术栈。`design`、`banner-design`、`slides` 更偏营销物料与演示，不宜扩大为日常产品开发的通用入口；其服务依赖和生成脚本没有在本次启用。

## Vercel：工程规则与适用条件

阅读了仓库索引、相关 Skill 入口和代表性分条规则。保存了 React 性能、组合模式、RN 与 View Transitions 的规则/参考原文；没有执行部署、Token 管理和成本分析工作流。

| 上游入口 | 可吸收内容 | 使用边界 |
| --- | --- | --- |
| [react-best-practices](../../tools/references/design-engineering/upstream/agent-skills/skills/react-best-practices/SKILL.md) | 先排查请求瀑布、包体积，再看渲染与局部计算 | 只用于实际的 React/Next.js 路径；收益需测量 |
| [composition-patterns](../../tools/references/design-engineering/upstream/agent-skills/skills/composition-patterns/SKILL.md) | 按职责组合组件，减少布尔模式爆炸 | 小组件不必为了模式增加 Context/Provider；React 版本特有 API 单独核对 |
| [web-design-guidelines](../../tools/references/design-engineering/upstream/agent-skills/skills/web-design-guidelines/SKILL.md) | 语义、键盘、表单、内容溢出、导航与状态 | 入口本身不含完整规则，实际依赖另一个仓库的 command.md |
| [react-native-skills](../../tools/references/design-engineering/upstream/agent-skills/skills/react-native-skills/SKILL.md) | 长列表、原生导航、安全区、手势与动画 | 不能把 Expo 依赖或特定列表库强加给已有原生项目 |
| [react-view-transitions](../../tools/references/design-engineering/upstream/agent-skills/skills/react-view-transitions/SKILL.md) | 用动效表达层级、身份和状态变化 | 查询实际 React/框架与浏览器支持；不自动升级实验版本 |

规则细节比 README 的统计更可靠：此次 React 规则目录有 70 条，RN 有 36 条（不计 `_sections` / `_template`），README 与 metadata 的数量描述并不完全一致。不要把“有多少条规则”当作完整性证明。

`vercel-optimize`、部署与 CLI Token Skill 主要服务特定托管平台，不纳入通用 UI 开发流程；`writing-guidelines` 是 Vercel 文风，没有覆盖本仓库个人中文 Voice 的理由。

## 产品与客户端的缺口

这三个来源都不足以直接形成完整的产品设计方法。视觉风格检索不能回答需求是否真实、任务是否高频、指标是否改善；后续产品研究 Skill 仍需访谈、任务观察、可用性测试等实际证据。

客户端资料包括 RN、SwiftUI、Compose、Flutter，以及 JavaFX、WPF、WinUI、Avalonia、Uno、UWP 的结构化条目。这里的覆盖表示“有资料入口”，不表示每个平台都已验证。Electron/Tauri、AppKit、编辑器宿主和桌面进程边界没有形成完整工作流。

结合 CodeWiz 的工作场景，建议下一轮用真实需求积累以下候选，而不是本次直接发布成稳定 Skill：

| 候选 | 推荐原因 | 晋级前需要的证据 |
| --- | --- | --- |
| `workbench-interaction` | IDE 的焦点、快捷键、命令面板、面板布局比通用落地页更接近实际工作 | 命令冲突、焦点返回、多窗口与长任务的真实案例 |
| `agent-task-experience` | AI 长任务需要可见进度、取消、恢复、变更检查与失败说明 | 一次完整任务从启动到审阅/撤回的交互验证 |
| `product-discovery` | 避免把设计方案当作需求验证 | 访谈或行为证据、任务成功指标、可用性测试 |
| `design-system-maintainer` | 跨页面、跨 Web/客户端时需要语义与状态一致 | 至少两个实际界面与主题/平台映射；再决定是否从 ui-ux-design 拆分 |
| `desktop-runtime-boundaries` | Electron/Tauri 涉及进程、权限与宿主 API，不只是 UI | 官方运行时资料、实际应用结构、边界与集成测试 |

这一节是结合用户背景的本地建议，不能归因于上述仓库已具备这些能力。

## 实测与质量边界

查询命令、结果与适配判断记录在[检索实测](design-engineering-search-checks.json)。实测最有价值的反例：`developer tool dashboard --design-system` 虽识别为开发者工具，却推荐 FAQ/文档落地页；这不适合直接应用于工作台。`safe area keyboard --stack react-native` 的结果也没有完整覆盖安全区，需将问题拆成独立查询。

因此，自有 Skill 强调“可执行的决策流程 + 结果证据”，没有复制整套规则或视搜索排名为设计结论。当前完成了文件结构、来源完整性、检索运行和案例静态走查；没有真实应用、设备和独立行为评测，草案状态保持不变。

本次校验结果：

- 4 个来源、212 个原文文件、3,859,637 字节通过 SHA-256 校验。
- 校验器能识别文件篡改、文件缺失和未登记文件；负向检查在临时副本中完成。
- 3 个 Skill 通过 skill-creator 的结构校验；仓库校验通过。
- 本次自有文档与入口中的 73 条本地链接均可解析。
- 7 个离线检索查询可运行，分别记录匹配、部分覆盖、错配和无结果，不将它们统称为推荐成功。
