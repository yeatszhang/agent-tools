#!/usr/bin/env python3
"""将当前仓库的 Skills 关联到用户全局目录；默认只预览。"""
import argparse
import os
from pathlib import Path


def link_target(path):
    """读取链接的绝对目标，保留失效目标以判断归属。"""
    if not path.is_symlink():
        return None
    target = Path(os.path.abspath(path.parent / os.readlink(path)))
    return target.parent.resolve() / target.name


def plan_sync(root, home):
    source = root.resolve() / "skills"
    skills = {p.name: p for p in source.iterdir()
              if p.is_dir() and (p / "SKILL.md").is_file()}
    if not skills:
        raise ValueError("未发现有效 Skill，停止同步")
    actions, conflicts = [], []
    for relative in (".agents/skills", ".claude/skills"):
        destination = home / relative
        if destination.exists() and not destination.is_dir():
            conflicts.append(destination)
            continue
        for name, target in sorted(skills.items()):
            path = destination / name
            if path.is_symlink() and path.resolve() == target.resolve():
                continue
            if path.exists() or path.is_symlink():
                conflicts.append(path)
            else:
                actions.append(("创建", path, target))
        if destination.is_dir():
            for path in sorted(destination.iterdir()):
                target = link_target(path)
                # 只清理本仓库按目录名安装、现已移除的 Skill 链接。
                if (target == source / path.name
                        and path.name not in skills):
                    actions.append(("移除失效链接", path, target))
    return actions, conflicts


def sync(root, home, apply=False):
    actions, conflicts = plan_sync(root, home)
    for action, path, target in actions:
        print(f"{action}：{path} -> {target}")
    for path in conflicts:
        print(f"冲突，保留现有内容：{path}")
    if conflicts:
        return 1
    if apply:
        for action, path, target in actions:
            if action == "创建":
                path.parent.mkdir(parents=True, exist_ok=True)
                path.symlink_to(target, target_is_directory=True)
            else:
                # 执行时再次确认，避免误删检查后已变动的链接。
                if link_target(path) != target:
                    raise RuntimeError(f"链接已改变，停止：{path}")
                path.unlink()
    print(f"{'已同步' if apply else '预览'}：{len(actions)} 项变更")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="执行同步，默认仅预览")
    parser.add_argument("--home", type=Path, default=Path.home(), help="目标用户目录，可用于隔离验证")
    args = parser.parse_args()
    return sync(Path(__file__).resolve().parent.parent, args.home.expanduser().resolve(), args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
