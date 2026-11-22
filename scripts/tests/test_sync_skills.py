"""验证全局同步的归属边界、冲突保护和幂等性。"""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("sync_skills", Path(__file__).parents[1] / "sync_skills.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SyncSkillsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.home = Path(self.temp.name) / "user"
        self.source = self.root / "skills" / "example"
        self.source.mkdir(parents=True)
        (self.source / "SKILL.md").write_text("测试 Skill")

    def test_preview_apply_and_repeat(self):
        self.assertEqual(module.sync(self.root, self.home), 0)
        self.assertFalse(self.home.exists())
        self.assertEqual(module.sync(self.root, self.home, True), 0)
        for folder in (".agents/skills", ".claude/skills"):
            self.assertEqual((self.home / folder / "example").resolve(), self.source.resolve())
        self.assertEqual(module.plan_sync(self.root, self.home), ([], []))

    def test_removes_only_stale_owned_links(self):
        folder = self.home / ".agents/skills"
        folder.mkdir(parents=True)
        stale = folder / "removed"
        stale.symlink_to(self.root / "skills" / "removed")
        foreign = folder / "foreign"
        foreign.symlink_to(Path(self.temp.name) / "external-missing")
        self.assertEqual(module.sync(self.root, self.home, True), 0)
        self.assertFalse(stale.is_symlink())
        self.assertTrue(foreign.is_symlink())

    def test_conflict_leaves_all_destinations_unchanged(self):
        conflict = self.home / ".agents/skills/example"
        conflict.mkdir(parents=True)
        marker = conflict / "keep.txt"
        marker.write_text("保留用户内容")
        self.assertEqual(module.sync(self.root, self.home, True), 1)
        self.assertEqual(marker.read_text(), "保留用户内容")
        self.assertFalse((self.home / ".claude").exists())

    def test_foreign_same_name_link_is_preserved(self):
        conflict = self.home / ".agents/skills/example"
        conflict.parent.mkdir(parents=True)
        foreign = Path(self.temp.name) / "other-skill"
        conflict.symlink_to(foreign)
        self.assertEqual(module.sync(self.root, self.home, True), 1)
        self.assertEqual(module.link_target(conflict), foreign.parent.resolve() / foreign.name)


if __name__ == "__main__":
    unittest.main()
