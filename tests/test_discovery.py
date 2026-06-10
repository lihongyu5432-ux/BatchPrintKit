from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from batch_print_kit.discovery import discover_files, discover_many, parse_extensions


class DiscoveryTests(unittest.TestCase):
    def test_parse_extensions_normalizes_values(self) -> None:
        self.assertEqual(parse_extensions("pdf, .DOCX,txt"), {".pdf", ".docx", ".txt"})

    def test_discover_filters_and_sorts_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "b.pdf").write_text("b", encoding="utf-8")
            (root / "a.txt").write_text("a", encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "c.pdf").write_text("c", encoding="utf-8")

            items = discover_files(root, extensions={".pdf"}, recursive=True)

            self.assertEqual([item.path.name for item in items], ["b.pdf", "c.pdf"])

    def test_non_recursive_skips_subfolders(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "top.txt").write_text("top", encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "child.txt").write_text("child", encoding="utf-8")

            items = discover_files(root, extensions={".txt"}, recursive=False)

            self.assertEqual([item.path.name for item in items], ["top.txt"])

    def test_discover_many_deduplicates_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            file_path = root / "top.txt"
            file_path.write_text("top", encoding="utf-8")

            items = discover_many([root, file_path], extensions={".txt"}, recursive=False)

            self.assertEqual([item.path.name for item in items], ["top.txt"])


if __name__ == "__main__":
    unittest.main()
