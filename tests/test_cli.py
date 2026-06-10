from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from batch_print_kit.cli import main


class CliTests(unittest.TestCase):
    def test_plan_returns_success_when_items_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "invoice.txt").write_text("hello", encoding="utf-8")

            exit_code = main(["plan", str(root), "--extensions", ".txt"])

            self.assertEqual(exit_code, 0)

    def test_plan_returns_two_when_no_items_match(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "invoice.txt").write_text("hello", encoding="utf-8")

            exit_code = main(["plan", str(root), "--extensions", ".pdf"])

            self.assertEqual(exit_code, 2)

    def test_print_without_yes_is_dry_run_success(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "invoice.txt").write_text("hello", encoding="utf-8")

            exit_code = main(["print", str(root), "--extensions", ".txt"])

            self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
