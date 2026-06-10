from __future__ import annotations

import unittest
from pathlib import Path

from batch_print_kit.gui import _format_paths, _format_size, translate


class GuiHelperTests(unittest.TestCase):
    def test_format_size(self) -> None:
        self.assertEqual(_format_size(42), "42 B")
        self.assertEqual(_format_size(2048), "2.0 KB")

    def test_translate_supports_chinese_and_english(self) -> None:
        self.assertEqual(translate("scan", "zh"), "扫描")
        self.assertEqual(translate("scan", "en"), "Scan")
        self.assertEqual(translate("import_files", "zh"), "导入文件")
        self.assertEqual(translate("import_files", "en"), "Import Files")
        self.assertEqual(translate("printer", "zh"), "打印机")
        self.assertEqual(translate("settings", "zh"), "打印机设置")
        self.assertEqual(translate("remove_selected", "en"), "Remove Selected")

    def test_format_paths_uses_selected_language(self) -> None:
        paths = [Path("a.txt"), Path("b.txt")]

        self.assertEqual(_format_paths(paths, "zh"), "来自资源管理器的 2 个选中项目")
        self.assertEqual(_format_paths(paths, "en"), "2 selected item(s) from Explorer")


if __name__ == "__main__":
    unittest.main()
