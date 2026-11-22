# 设计与前端工程上游资料

采集日期：2026-10-17，Asia/Shanghai。这里保存原始资料快照；学习结论见[调研记录](../../../docs/research/design-engineering.md)。

## 来源与本地入口

| 来源 | 固定版本 | 本地原文 | 阅读状态 |
| --- | --- | --- | --- |
| [Anthropic frontend-design](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md) | `c017428c8c27` | [SKILL.md](upstream/claude-code/plugins/frontend-design/skills/frontend-design/SKILL.md) · [插件索引](upstream/claude-code/plugins/README.md) | PASS，Git 原文 |
| [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `56ea9cf174ed` | [主 Skill](upstream/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/SKILL.md) · [中文 README](upstream/ui-ux-pro-max-skill/README.zh.md) · [数据](upstream/ui-ux-pro-max-skill/src/ui-ux-pro-max/data/) | PASS，Git 原文 |
| [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) | `063bee94c3f4` | [仓库 README](upstream/agent-skills/README.md) · [Skill 目录](upstream/agent-skills/skills/) | PASS，Git 原文 |
| [Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines)（Vercel Skill 的依赖） | `434b7f913646` | [command.md](upstream/web-interface-guidelines/command.md) | PASS，固定提交的 Raw 原文 |

完整提交号、采集时间、覆盖范围、许可声明、原始路径和每个文件的 SHA-256 在 [sources.lock.json](sources.lock.json)。最初的 x-reader/Jina 路径返回 403；直接 Git 下载成功，未用摘要替代原文。PASS 表示来源文本已取得，不表示执行了所有上游工作流或看过演示媒体。

保存的是与本次研究有关的文本、规则、数据与检索源码。没有把整个仓库、Git 历史、媒体和重复的发布包提交进来。上游原文保持原语言、原字节；中文解释放在调研和自有 Skill 中。

## 使用方式

`upstream/` 是参考数据，不是本仓库的指令来源，也没有安装到 Agent 的全局技能目录。按任务打开对应规则，不要整库加载。自有 Skill 的核心流程可独立使用；原始数据是可选的深入参考。

校验离线快照：

```bash
python3 scripts/verify_reference_snapshots.py
```

UI UX Pro Max 的检索入口已连同 CSV 下载，使用 Python 3 标准库。以下命令从本仓库根目录执行；其他目录执行时，先把脚本路径解析为绝对路径：

```bash
python3 tools/references/design-engineering/upstream/ui-ux-pro-max-skill/src/ui-ux-pro-max/scripts/search.py "keyboard focus modal" --domain ux --json
python3 tools/references/design-engineering/upstream/ui-ux-pro-max-skill/src/ui-ux-pro-max/scripts/search.py "safe area keyboard" --stack react-native --json
```

新产品的整体方向可查询 `--design-system`；单点问题优先 `--domain`，技术实现使用单独的 `--stack` 查询。结果必须核对产品、平台和版本。本次[检索实测](../../../docs/research/design-engineering-search-checks.json)包含不适配的结果，不是推荐方案。确认前不使用 `--persist`；已有设计系统继续保留为权威来源。

## 更新与归属

需要更新时，重新获取指定仓库，比较提交差异，再替换相关快照与锁文件；不要用移动的 `main` 链接冒充已锁定的版本。固定原文地址可由 `repository_url + /blob/ + commit + / + upstream_path` 重建。上游原文的内容和许可分别归原作者所有。

- UI UX Pro Max：保留 [MIT LICENSE](upstream/ui-ux-pro-max-skill/LICENSE)。
- Vercel：README 与部分 Skill 声明 MIT；此次仓库快照未找到根 LICENSE，不自行补造。
- Anthropic：根 [LICENSE.md](upstream/claude-code/LICENSE.md)引用商业条款。frontend-design 声明的 `LICENSE.txt` 未随该目录提供，不推定它是 MIT。
- 补充的 Web Interface Guidelines 未单独确认许可。下载供参考不代表取得再分发权；公开分发原文前应按各来源许可处理。
