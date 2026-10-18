"""验证样例记录的输出边界与原文保真，不使用真实用户文本。"""

from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/capture_edit.py"


class CaptureEditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.original = self.root / "original.md"
        self.final = self.root / "final.md"
        self.original.write_bytes("初步结果可能改善。\r\n待验证。".encode())
        self.final.write_bytes("初步结果可能改善，仍待验证。".encode())
        self.output = self.root / "output"

    def run_capture(self, with_output=True):
        args = [sys.executable, str(SCRIPT),
                "--original", str(self.original), "--final", str(self.final),
                "--context", "technical"]
        if with_output:
            args += ["--output-dir", str(self.output)]
        return subprocess.run(args, cwd=self.root, capture_output=True, text=True)

    def test_requires_explicit_destination(self):
        before = sorted(path.name for path in self.root.iterdir())
        result = self.run_capture(with_output=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--output-dir", result.stderr)
        self.assertEqual(before, sorted(path.name for path in self.root.iterdir()))

    def test_preserves_source_bytes_and_timezone(self):
        result = self.run_capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        out = Path(result.stdout.strip())
        self.assertEqual(out.parent, self.output.resolve())
        self.assertEqual((out / "original.md").read_bytes(), self.original.read_bytes())
        self.assertEqual((out / "final.md").read_bytes(), self.final.read_bytes())
        meta = json.loads((out / "meta.json").read_text())
        self.assertEqual(meta["status"], "candidate-source")
        self.assertEqual(meta["context"], "technical")
        self.assertIsNotNone(datetime.fromisoformat(meta["created_at"]).tzinfo)

    def test_repeated_capture_keeps_both_observations(self):
        first = self.run_capture()
        second = self.run_capture()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertNotEqual(first.stdout, second.stdout)
        self.assertTrue(Path(first.stdout.strip()).is_dir())
        self.assertTrue(Path(second.stdout.strip()).is_dir())

    def test_diff_keeps_lines_without_final_newline_separate(self):
        self.original.write_text("旧内容", encoding="utf-8")
        self.final.write_text("新内容", encoding="utf-8")
        result = self.run_capture()
        self.assertEqual(result.returncode, 0, result.stderr)
        diff = (Path(result.stdout.strip()) / "diff.patch").read_text()
        self.assertIn("\n-旧内容\n", diff)
        self.assertIn("\n+新内容\n", diff)
        self.assertEqual(diff.count("\\ No newline at end of file"), 2)


if __name__ == "__main__":
    unittest.main()
