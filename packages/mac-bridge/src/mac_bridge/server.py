import argparse
import asyncio
import hmac
import os
import json
import re
from datetime import timedelta, timezone
from pathlib import Path
from typing import Annotated, Any, Literal

import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import AwareDatetime, Field, StringConstraints
from starlette.responses import PlainTextResponse

from .local import build_helper, native_call, notebook_store

Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=300)]
Identifier = Annotated[str, Field(min_length=1, max_length=2048)]
Offset = Annotated[int, Field(ge=0, le=1000000)]
Limit = Annotated[int, Field(ge=1, le=100)]
READ = ToolAnnotations(readOnlyHint=True)
CREATE = ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False)
COMPLETE = ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True)


def timestamp(value: AwareDatetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def interval(start: AwareDatetime, end: AwareDatetime) -> dict[str, Any]:
    first, last = timestamp(start), timestamp(end)
    if last <= first:
        raise ValueError("结束时间必须晚于开始时间至少一秒")
    return {"start": first, "end": last}


def create_server(notebook: Path | None, allow_write: bool, port: int = 8765) -> FastMCP:
    mcp = FastMCP("mac-bridge", host="127.0.0.1", port=port, stateless_http=True, json_response=True)

    if notebook is not None:
        store = notebook_store(notebook.expanduser().resolve())

        @mcp.tool(annotations=READ)
        async def knowledge_search(query: Title, limit: Annotated[int, Field(ge=1, le=50)] = 10) -> dict[str, Any]:
            """按关键词搜索 notebook 当前正式知识，返回带出处的摘要和页面 ID。"""
            return await asyncio.to_thread(store.search, query, limit=limit)

        @mcp.tool(annotations=READ)
        async def knowledge_read(id: Identifier) -> dict[str, Any]:
            """根据检索结果的 ID 读取正式 Markdown 页面。"""
            return await asyncio.to_thread(store.fetch, id)

    @mcp.tool(annotations=READ)
    async def notes_search(query: Annotated[str, Field(max_length=300)] = "", limit: Limit = 20, offset: Offset = 0) -> dict[str, Any]:
        """按标题搜索 Apple 备忘录，空查询列出备忘录。"""
        return await native_call("notes_search", query=query, limit=limit, offset=offset)

    @mcp.tool(annotations=READ)
    async def notes_read(id: Identifier, offset: Annotated[int, Field(ge=0)] = 0,
                         limit: Annotated[int, Field(ge=1, le=30000)] = 16000) -> dict[str, Any]:
        """按 ID 读取备忘录纯文本，长文使用返回的 next_offset 继续读取。"""
        return await native_call("notes_read", id=id, offset=offset, limit=limit)

    @mcp.tool(annotations=READ)
    async def containers_list(kind: Literal["events", "reminders"]) -> dict[str, Any]:
        """列出日历或提醒清单的名称、账户、可写状态和 ID。"""
        return await native_call("containers", kind=kind)

    @mcp.tool(annotations=READ)
    async def reminders_list(limit: Limit = 50, offset: Offset = 0,
                            query: Annotated[str, Field(max_length=300)] = "") -> dict[str, Any]:
        """列出未完成提醒事项及其清单、截止时间和 ID，可按标题过滤或翻页。"""
        return await native_call("reminders_list", limit=limit, offset=offset, query=query)

    @mcp.tool(annotations=READ)
    async def events_list(start: AwareDatetime, end: AwareDatetime, limit: Limit = 50, offset: Offset = 0) -> dict[str, Any]:
        """列出给定时段内的日程，含重复日程实例。时间须带时区，范围最多 31 天。"""
        if end - start > timedelta(days=31):
            raise ValueError("查询范围最多 31 天")
        return await native_call("events_list", **interval(start, end), limit=limit, offset=offset)

    if allow_write:
        @mcp.tool(annotations=CREATE)
        async def notes_create(title: Title, body: Annotated[str, Field(max_length=30000)] = "") -> dict[str, Any]:
            """在默认账户的默认文件夹创建纯文本备忘录。"""
            return await native_call("notes_create", title=title, body=body)

        @mcp.tool(annotations=CREATE)
        async def reminders_create(title: Title, due: AwareDatetime | None = None,
                                   calendar_id: Identifier | None = None) -> dict[str, Any]:
            """创建提醒事项，可指定带时区的截止时间与目标清单 ID。"""
            return await native_call("reminders_create", title=title, due=timestamp(due) if due else None,
                                     calendar_id=calendar_id)

        @mcp.tool(annotations=COMPLETE)
        async def reminders_complete(id: Identifier) -> dict[str, Any]:
            """将指定 ID 的提醒事项标记为已完成。"""
            return await native_call("reminders_complete", id=id)

        @mcp.tool(annotations=CREATE)
        async def events_create(title: Title, start: AwareDatetime, end: AwareDatetime,
                                calendar_id: Identifier | None = None) -> dict[str, Any]:
            """创建有起止时间的单次日程，可指定目标日历 ID。"""
            return await native_call("events_create", title=title, **interval(start, end), calendar_id=calendar_id)

    return mcp


class BearerAuth:
    def __init__(self, app, token: str):
        self.app = app
        if not re.fullmatch(r"[a-zA-Z0-9._~+/-]{32,}={0,2}", token):
            raise ValueError("HTTP 模式需要在 MAC_BRIDGE_TOKEN 设置至少 32 位的随机 Bearer 凭据")
        self.token = token.encode("ascii")

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = [v for k, v in scope["headers"] if k == b"authorization"]
            scheme, _, value = headers[0].partition(b" ") if len(headers) == 1 else (b"", b"", b"")
            if scheme.lower() != b"bearer" or not hmac.compare_digest(value, self.token):
                response = PlainTextResponse("Unauthorized", 401, headers={"WWW-Authenticate": "Bearer"})
                return await response(scope, receive, send)
        return await self.app(scope, receive, send)


def main():
    parser = argparse.ArgumentParser(description="本地 macOS MCP 服务")
    parser.add_argument("command", choices=["setup", "status", "serve"])
    parser.add_argument("--notebook", type=Path, help="含检索实现的可信 notebook 仓库根目录")
    parser.add_argument("--allow-write", action="store_true", help="注册备忘录、日历和提醒事项的写工具")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    try:
        if args.command == "setup":
            build_helper()
            return
        if args.command == "status":
            print(json.dumps(asyncio.run(native_call("status")), ensure_ascii=False))
            return
        if not 1 <= args.port <= 65535:
            raise ValueError("端口必须在 1 到 65535 之间")
        server = create_server(args.notebook, args.allow_write, args.port)
        if args.transport == "stdio":
            server.run()
            return
        app = BearerAuth(server.streamable_http_app(), os.environ.get("MAC_BRIDGE_TOKEN", ""))
        uvicorn.run(app, host="127.0.0.1", port=args.port, access_log=False, proxy_headers=False)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"{exc}\n")
