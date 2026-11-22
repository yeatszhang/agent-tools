import asyncio
import os
import secrets
import socket
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

from mac_bridge.server import create_server

CLI = str(Path(sys.executable).with_name("mac-bridge"))


class ToolsTests(unittest.IsolatedAsyncioTestCase):
    async def test_read_only_stdio_rejects_writes(self):
        params = StdioServerParameters(command=CLI, args=["serve"])
        async with stdio_client(params) as (reader, writer), ClientSession(reader, writer) as session:
            await session.initialize()
            names = {tool.name for tool in (await session.list_tools()).tools}
            self.assertEqual(names, {"notes_search", "notes_read", "containers_list", "events_list", "reminders_list"})
            result = await session.call_tool("notes_create", {"title": "测试"})
            self.assertTrue(result.isError)

    async def test_write_dispatch_and_date_validation(self):
        server = create_server(None, True)
        with patch("mac_bridge.server.native_call", new_callable=AsyncMock, return_value={"id": "abc"}) as call:
            await server.call_tool("events_create", {
                "title": "评审", "start": "2026-11-20T10:00:00+08:00", "end": "2026-11-20T11:00:00+08:00",
            })
            call.assert_awaited_once_with("events_create", title="评审", start="2026-11-20T02:00:00Z",
                                          end="2026-11-20T03:00:00Z", calendar_id=None)
            from mcp.server.fastmcp.exceptions import ToolError
            for end in ["2026-11-20T01:00:00Z", "2026-11-21T10:00:00", "2027-02-01T10:00:00Z"]:
                with self.assertRaises(ToolError):
                    await server.call_tool("events_list", {"start": "2026-11-20T02:00:00Z", "end": end})
            self.assertEqual(call.await_count, 1)
            await server.call_tool("reminders_complete", {"id": "abc"})
            call.assert_awaited_with("reminders_complete", id="abc")

    async def test_http_credentials_and_read(self):
        # 使用独立夹具验证适配器和两端的协议，不依赖开发者的私人知识库。
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "notebook_mcp_core.py").write_text(
                "class NotebookStore:\n"
                "    def __init__(self, root): self.root = root\n"
                "    def search(self, query, limit): return {'results': [{'id': '测试.md'}]}\n"
                "    def fetch(self, id): return {'text': (self.root / '测试.md').read_text()}\n"
            )
            (root / "测试.md").write_text("协议测试")
            with socket.socket() as sock:
                sock.bind(("127.0.0.1", 0))
                port = sock.getsockname()[1]

            token = secrets.token_urlsafe(32)
            proc = await asyncio.create_subprocess_exec(
                CLI, "serve", "--transport", "http", "--port", str(port), "--notebook", str(root),
                env={**os.environ, "MAC_BRIDGE_TOKEN": token}, stderr=asyncio.subprocess.DEVNULL,
            )
            self.addAsyncCleanup(self.stop, proc)
            url = f"http://127.0.0.1:{port}/mcp"
            async with httpx.AsyncClient(trust_env=False) as client:
                for _ in range(100):
                    try:
                        response = await client.post(url)
                        break
                    except httpx.ConnectError:
                        if proc.returncode is not None:
                            self.fail("HTTP 服务提前退出")
                        await asyncio.sleep(.05)
                else:
                    self.fail("HTTP 服务未就绪")
                self.assertEqual(response.status_code, 401)
                self.assertEqual((await client.post(url, headers={"Authorization": "Bearer wrong"})).status_code, 401)
                client.headers["Authorization"] = f"Bearer {token}"
                async with streamable_http_client(url, http_client=client) as (reader, writer, _):
                    async with ClientSession(reader, writer) as session:
                        await session.initialize()
                        result = await session.call_tool("knowledge_search", {"query": "测试"})
                        self.assertFalse(result.isError)
                        page = result.structuredContent["results"][0]["id"]
                        result = await session.call_tool("knowledge_read", {"id": page})
                        self.assertEqual(result.structuredContent["text"], "协议测试")

    async def stop(self, proc):
        if proc.returncode is None:
            proc.terminate()
        await asyncio.wait_for(proc.wait(), 5)


if __name__ == "__main__":
    unittest.main()
