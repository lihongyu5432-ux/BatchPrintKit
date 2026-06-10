from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from batch_print_kit import printers
from batch_print_kit.models import PrintItem, PrintOptions


class PrinterTests(unittest.TestCase):
    def test_list_windows_printers_prefers_real_printer_over_pdf_targets(self) -> None:
        payload = [
            {"Name": "导出为WPS PDF", "Default": False},
            {"Name": "Microsoft Print to PDF", "Default": False},
            {"Name": "EPSON L1250 Series", "Default": False},
        ]
        completed = mock.Mock(stdout=json.dumps(payload))

        with mock.patch("batch_print_kit.printers.subprocess.run", return_value=completed):
            self.assertEqual(printers._list_windows_printers()[0], "EPSON L1250 Series")

    def test_list_windows_printers_handles_empty_stdout(self) -> None:
        completed = mock.Mock(stdout=None)

        with mock.patch("batch_print_kit.printers.subprocess.run", return_value=completed):
            self.assertEqual(printers._list_windows_printers(), [])

    def test_pdf_uses_sumatra_when_available(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root / "a.pdf"
            sumatra = root / "SumatraPDF.exe"
            pdf.write_bytes(b"%PDF")
            sumatra.write_text("", encoding="utf-8")

            printer = printers.SystemPrinter(printer_name="EPSON")
            with mock.patch("batch_print_kit.printers.platform.system", return_value="Windows"), mock.patch(
                "batch_print_kit.printers.find_sumatra_pdf", return_value=sumatra
            ), mock.patch("batch_print_kit.printers.subprocess.run") as run:
                result = printer.print_item(PrintItem(path=pdf, size_bytes=4))

            self.assertEqual(result.status, "submitted")
            args = run.call_args.args[0]
            self.assertEqual(args[:3], [str(sumatra), "-silent", "-exit-on-print"])
            self.assertNotIn("-print-settings", args)
            self.assertIn("-print-to", args)

    def test_windows_printer_settings_opens_driver_preferences(self) -> None:
        with mock.patch("batch_print_kit.printers.platform.system", return_value="Windows"), mock.patch(
            "batch_print_kit.printers.subprocess.Popen"
        ) as popen:
            printers.open_printer_settings("EPSON L1250 Series")

        args = popen.call_args.args[0]
        self.assertEqual(args[:3], ["rundll32", "printui.dll,PrintUIEntry", "/e"])
        self.assertEqual(args[-2:], ["/n", "EPSON L1250 Series"])

    def test_pdf_passes_print_options_to_sumatra(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root / "a.pdf"
            sumatra = root / "SumatraPDF.exe"
            pdf.write_bytes(b"%PDF")
            sumatra.write_text("", encoding="utf-8")

            printer = printers.SystemPrinter(
                printer_name="EPSON",
                options=PrintOptions(paper_size="A5", color_mode="grayscale", copies=2),
            )
            with mock.patch("batch_print_kit.printers.platform.system", return_value="Windows"), mock.patch(
                "batch_print_kit.printers.find_sumatra_pdf", return_value=sumatra
            ), mock.patch("batch_print_kit.printers.subprocess.run") as run:
                result = printer.print_item(PrintItem(path=pdf, size_bytes=4))

            args = run.call_args.args[0]
            self.assertEqual(result.status, "submitted")
            self.assertIn("-print-settings", args)
            self.assertIn("2x,paper=A5,monochrome", args)


if __name__ == "__main__":
    unittest.main()
