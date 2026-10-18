#!/usr/bin/env python3
import argparse
import difflib
import json
from datetime import datetime
from pathlib import Path
import tempfile

def main():
    p = argparse.ArgumentParser(description="保存已脱敏且明确要求记录的编辑样例")
    p.add_argument("--original", required=True)
    p.add_argument("--final", required=True)
    p.add_argument("--context", default="unknown",
                   choices=["technical", "management", "casual", "longform", "unknown"])
    p.add_argument("--output-dir", required=True,
                   help="样例输出目录；真实文本使用仓库外目录")
    args = p.parse_args()

    original_bytes = Path(args.original).read_bytes()
    final_bytes = Path(args.final).read_bytes()
    original = original_bytes.decode("utf-8")
    final = final_bytes.decode("utf-8")

    created_at = datetime.now().astimezone()
    stamp = created_at.strftime("%Y%m%d-%H%M%S")
    output_root = Path(args.output_dir).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix=f"{stamp}-", dir=output_root))

    (out / "original.md").write_bytes(original_bytes)
    (out / "final.md").write_bytes(final_bytes)

    diff_lines = difflib.unified_diff(
        original.splitlines(keepends=True),
        final.splitlines(keepends=True),
        fromfile="original.md",
        tofile="final.md",
    )
    # 为没有末尾换行的内容保留标准 diff 标记，避免删除与新增行粘连。
    diff = "".join(
        line if line.endswith("\n") else line + "\n\\ No newline at end of file\n"
        for line in diff_lines
    )
    (out / "diff.patch").write_text(diff, encoding="utf-8")

    meta = {
        "created_at": created_at.isoformat(timespec="seconds"),
        "context": args.context,
        "status": "candidate-source",
    }
    (out / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(out)

if __name__ == "__main__":
    main()
