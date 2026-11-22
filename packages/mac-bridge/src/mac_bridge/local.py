import asyncio
import importlib.util
import json
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

NATIVE = Path(__file__).with_name("native")
HELPER = Path(sys.prefix) / "libexec" / "mac-bridge-eventkit"


def build_helper(target: Path = HELPER) -> None:
    """编译到当前 Python 环境，编译失败时保留可用的旧版本。"""
    if platform.system() != "Darwin":
        raise ValueError("需要在 macOS 14 或更高版本上运行")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent) as build:
        binary = Path(build) / target.name
        subprocess.run([
            "/usr/bin/xcrun", "swiftc", "-parse-as-library", str(NATIVE / "EventKitHelper.swift"),
            "-Xlinker", "-sectcreate", "-Xlinker", "__TEXT", "-Xlinker", "__info_plist",
            "-Xlinker", str(NATIVE / "Info.plist"), "-o", str(binary),
        ], env={**os.environ, "MACOSX_DEPLOYMENT_TARGET": "14.0"}, check=True)
        os.replace(binary, target)


def notebook_store(root: Path):
    """加载 Mac 所有者在启动时指定的、可信 notebook 仓库自带的检索实现。"""
    path = root / "scripts/notebook_mcp_core.py"
    if not path.is_file():
        raise ValueError("--notebook 需要指向含 scripts/notebook_mcp_core.py 的可信 notebook 仓库")
    spec = importlib.util.spec_from_file_location("notebook_mcp_core", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.NotebookStore(root)


async def native_call(operation: str, **arguments) -> dict:
    if operation.startswith("notes_"):
        command = ["/usr/bin/osascript", "-l", "JavaScript", str(NATIVE / "Notes.js")]
    else:
        if not HELPER.is_file():
            raise ValueError("日历与提醒事项需要先在 Mac 上运行 mac-bridge setup")
        command = [str(HELPER)]
    request = json.dumps({"operation": operation, **arguments}, ensure_ascii=False).encode()
    process = await asyncio.create_subprocess_exec(
        *command, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        env={k: v for k, v in os.environ.items() if k != "MAC_BRIDGE_TOKEN"},
    )
    try:
        output, error = await asyncio.wait_for(process.communicate(request), timeout=60)
    except (TimeoutError, asyncio.CancelledError) as exc:
        if process.returncode is None:
            process.kill()
        await process.wait()
        if isinstance(exc, asyncio.CancelledError):
            raise
        raise ValueError("本机应用超时。请查看 Mac 权限弹窗，写入操作请先查询结果再重试。") from exc
    if process.returncode:
        detail = error.decode(errors="replace").strip()[:600]
        raise ValueError(f"本机应用调用失败，请检查 macOS 应用权限。{detail}")
    return json.loads(output)
