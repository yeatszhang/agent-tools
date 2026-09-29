#!/usr/bin/env python3
import argparse
import difflib
import json
from datetime import datetime
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--original", required=True)
    p.add_argument("--final", required=True)
    p.add_argument("--context", default="unknown",
                   choices=["technical", "management", "casual", "longform", "unknown"])
    args = p.parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    original = Path(args.original).read_text(encoding="utf-8")
    final = Path(args.final).read_text(encoding="utf-8")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = skill_root / "observations" / stamp
    out.mkdir(parents=True, exist_ok=False)

    (out / "original.md").write_text(original, encoding="utf-8")
    (out / "final.md").write_text(final, encoding="utf-8")

    diff = "".join(difflib.unified_diff(
        original.splitlines(keepends=True),
        final.splitlines(keepends=True),
        fromfile="original.md",
        tofile="final.md",
    ))
    (out / "diff.patch").write_text(diff, encoding="utf-8")

    meta = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
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
