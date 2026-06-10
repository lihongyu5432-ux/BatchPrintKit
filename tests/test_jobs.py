from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from batch_print_kit.jobs import build_plan, build_plan_many, run_print_job


class JobTests(unittest.TestCase):
    def test_build_plan_accepts_extension_string(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "invoice.pdf").write_text("pdf", encoding="utf-8")
            (root / "draft.md").write_text("md", encoding="utf-8")

            items = build_plan(root, extensions=".pdf")

            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].path.name, "invoice.pdf")

    def test_dry_run_does_not_submit_to_printer(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "invoice.pdf").write_text("pdf", encoding="utf-8")
            items = build_plan(root, extensions=".pdf")

            results = run_print_job(items, confirmed=False)

            self.assertEqual(results[0].status, "dry-run")

    def test_build_plan_many_accepts_files_and_folders(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            direct = root / "direct.txt"
            direct.write_text("direct", encoding="utf-8")
            nested_root = root / "nested"
            nested_root.mkdir()
            (nested_root / "nested.txt").write_text("nested", encoding="utf-8")

            items = build_plan_many([direct, nested_root], extensions=".txt")

            self.assertEqual([item.path.name for item in items], ["direct.txt", "nested.txt"])


if __name__ == "__main__":
    unittest.main()
