# mac-bridge

让远端 Agent 通过 MCP 查询 Mac 上的 notebook、读写 Apple 备忘录、管理提醒事项和日历。Mac 执行工具并返回结果。服务支持 stdio 和 Streamable HTTP，默认只注册读工具。设计参考了 [Desktop Commander 的本地执行方式](https://desktopcommander.app/)。

## 在 Mac 上准备

需要 macOS 14 或更新版本、Xcode Command Line Tools、Python 3.11+ 和 uv。在本机登录用户的终端里，从本包目录运行以下命令。

```sh
uv sync --locked
uv run --locked mac-bridge setup
uv run --locked mac-bridge status
```

`setup` 用系统 Swift 编译器构建 EventKit 助手，安装到当前虚拟环境的 `libexec/`。更新本包或重建虚拟环境后重新运行。分享给其他 Mac 时可用 `uv build` 生成 wheel，安装 wheel 后在对应 Python 环境运行同一条 `mac-bridge setup` 命令。

`status` 显示日历和提醒事项的系统授权状态。首次查询相应应用时，在 Mac 上处理系统弹窗。备忘录使用 Apple Events，可在「系统设置 → 隐私与安全性 → 自动化」查看启动服务的应用是否有权控制备忘录。日历和提醒事项使用 EventKit，读取数据需要对应的完全访问权限。

## 接入远端 Agent

适用于能在自有主机上运行 MCP 客户端的 Agent。Mac 主动建立 SSH 连接，两端的 MCP 地址都绑定在回环接口。将同一个随机 Bearer 凭据通过各自的凭据存储注入 Mac 和 Agent 的 `MAC_BRIDGE_TOKEN` 环境变量，可用 `openssl rand -hex 32` 生成。

在 Mac 的第一个终端启动服务。此例接入当前用户的 notebook。

```sh
uv run --locked mac-bridge serve --transport http \
  --notebook "$HOME/Documents/notebook"
```

在 Mac 的另一个终端建立反向隧道，将下例的 SSH 目标替换为 Agent 所在主机。远端 SSH 服务需允许远程端口转发，并保持 `GatewayPorts no` 或 `clientspecified`。

```sh
ssh -NT -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 \
  -R 127.0.0.1:18765:127.0.0.1:8765 user@agent-host
```

Agent 在该主机上连接 `http://127.0.0.1:18765/mcp`，传入 `Authorization: Bearer <凭据>`。若 Agent 运行在容器内，转发端口与客户端需要位于同一网络命名空间。关闭 SSH 连接即可断开远端访问。支持 Python MCP SDK 的客户端可用下面的代码检查工具列表。

```python
import asyncio
import os

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main():
    headers = {"Authorization": "Bearer " + os.environ["MAC_BRIDGE_TOKEN"]}
    async with httpx.AsyncClient(headers=headers, trust_env=False) as client:
        url = "http://127.0.0.1:18765/mcp"
        async with streamable_http_client(url, http_client=client) as (reader, writer, _):
            async with ClientSession(reader, writer) as session:
                await session.initialize()
                print([tool.name for tool in (await session.list_tools()).tools])


asyncio.run(main())
```

本机 MCP 客户端或支持启动本地 stdio 子进程的隧道，可以直接执行 `.venv/bin/mac-bridge serve --notebook /绝对路径/notebook`。配置时使用可执行文件绝对路径。托管 Agent 若只能填写公网 HTTPS URL，需要由其支持的网关提供远端接入。

## 工具与写入开关

| 操作对象 | 默认可用 | 启动服务时加入 `--allow-write` |
| --- | --- | --- |
| notebook | `knowledge_search` 按关键词检索，`knowledge_read` 按结果 ID 读取页面 | — |
| Apple 备忘录 | `notes_search` 按标题搜索，`notes_read` 分页读取纯文本 | `notes_create` 在默认文件夹建笔记 |
| 提醒事项 | `reminders_list` 查询未完成事项，支持标题过滤和分页 | `reminders_create`、`reminders_complete` |
| 日历 | `events_list` 按时段查询，包含重复事件实例 | `events_create` 创建单次日程 |

`containers_list` 按 `events` 或 `reminders` 返回账户、日历或清单 ID 和可写状态。创建日程或提醒时可传入目标 `calendar_id`，省略时使用系统默认目标。日期时间携带时区，例如 `2026-11-23T09:00:00+08:00`。创建类调用如果超时，先查询目标应用，避免重复创建。

`--notebook` 指向由 Mac 所有者管理的可信仓库。服务加载其中的 `scripts/notebook_mcp_core.py`，沿用该仓库的检索范围、路径检查与脱敏规则。省略该选项时仅注册 Apple 应用工具。

## 验证

```sh
uv run --locked python -m unittest discover -s __tests__ -v
```

自动测试覆盖 stdio 和 HTTP 客户端、Bearer 鉴权、只读模式、时间参数检查与知识库适配。要验收这台 Mac 上的应用授权，可先调用 `notes_search`、`reminders_list` 和 `events_list`。需要验证写入时，以明确的测试标题创建一条备忘录、一个提醒和一个日程，通过读工具核对，再用返回的提醒 ID 测试完成操作。
