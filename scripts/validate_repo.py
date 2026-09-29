#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(__file__).resolve().parent.parent
errors = []

for skill_dir in (root / "skills").iterdir():
    if skill_dir.is_dir() and not (skill_dir / "SKILL.md").exists():
        errors.append(f"missing SKILL.md: {skill_dir.relative_to(root)}")

for forbidden in [".env", "secrets", "private"]:
    if (root / forbidden).exists():
        errors.append(f"forbidden path exists: {forbidden}")

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("OK")
