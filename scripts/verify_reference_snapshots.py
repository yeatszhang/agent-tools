#!/usr/bin/env python3
"""校验固定来源快照的文件完整性，不联网或执行上游脚本。"""

import hashlib
import json
from pathlib import Path
import sys


def verify(manifest_path):
    base = manifest_path.resolve().parent
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors = []
    expected = set()
    total_bytes = 0
    for source in manifest["sources"]:
        commit = source["commit"]
        if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
            errors.append(f"提交号无效：{source['id']}")
        for record in source["files"]:
            relative = record["path"]
            path = (base / relative).resolve()
            if not path.is_relative_to(base / "upstream"):
                errors.append(f"快照路径越界：{relative}")
                continue
            if relative in expected:
                errors.append(f"重复文件记录：{relative}")
            expected.add(relative)
            if not path.is_file():
                errors.append(f"文件缺失：{relative}")
                continue
            data = path.read_bytes()
            total_bytes += len(data)
            if len(data) != record["bytes"]:
                errors.append(f"文件大小不符：{relative}")
            if hashlib.sha256(data).hexdigest() != record["sha256"]:
                errors.append(f"SHA-256 不符：{relative}")
    actual = {
        str(path.relative_to(base))
        for path in (base / "upstream").rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    for relative in sorted(actual - expected):
        errors.append(f"文件未登记：{relative}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"通过：{len(manifest['sources'])} 个来源，{len(expected)} 个文件，{total_bytes} 字节。")
    return 0


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    default = root / "tools/references/design-engineering/sources.lock.json"
    manifest_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default
    sys.exit(verify(manifest_path))
