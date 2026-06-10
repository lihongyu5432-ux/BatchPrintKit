from __future__ import annotations

import os
import platform
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .models import PrintItem, PrintOptions, PrintResult


CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


class PrinterError(RuntimeError):
    pass


def list_printers() -> list[str]:
    system = platform.system().lower()
    if system == "windows":
        return _list_windows_printers()
    return _list_unix_printers()


def open_printer_settings(printer_name: str | None = None) -> None:
    system = platform.system().lower()
    if system == "windows":
        if not printer_name:
            raise PrinterError("Choose a printer first.")
        subprocess.Popen(
            ["rundll32", "printui.dll,PrintUIEntry", "/e", "/n", printer_name],
            creationflags=CREATE_NO_WINDOW,
        )
        return
    command = shutil.which("system-config-printer")
    if command:
        subprocess.Popen([command])


def print_test_page(printer_name: str | None = None) -> PrintResult:
    item = PrintItem(path=Path("BatchPrintKit Test Page"), size_bytes=0)
    system = platform.system().lower()
    try:
        if system == "windows":
            lines = [
                "Batch Print Kit test page",
                f"Printer: {printer_name or 'Default printer'}",
                "If this page prints, the Windows printer pipeline is working.",
            ]
            command = "$input | Out-Printer"
            if printer_name:
                escaped = printer_name.replace("'", "''")
                command = f"$input | Out-Printer -Name '{escaped}'"
            _run_hidden(
                ["powershell", "-NoProfile", "-Command", command],
                input="\n".join(lines),
                text=True,
                check=True,
            )
            return PrintResult(item=item, status="submitted")
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as handle:
            handle.write("Batch Print Kit test page\n")
            path = Path(handle.name)
        return SystemPrinter(printer_name=printer_name).print_item(PrintItem(path=path, size_bytes=path.stat().st_size))
    except Exception as exc:
        return PrintResult(item=item, status="failed", detail=str(exc))


def _list_windows_printers() -> list[str]:
    try:
        completed = _run_hidden(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "[Console]::OutputEncoding = [Text.Encoding]::UTF8; "
                "Get-Printer | Sort-Object Name | Select-Object Name,Default | ConvertTo-Json -Compress",
            ],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except Exception:
        return []

    raw = (completed.stdout or "").strip()
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    rows = data if isinstance(data, list) else [data]
    names = [_printer_name(row) for row in rows]
    names = [name for name in names if name]
    default_names = [_printer_name(row) for row in rows if isinstance(row, dict) and bool(row.get("Default"))]
    default_names = [name for name in default_names if name]
    preferred = [name for name in names if "WPS" not in name.upper() and "PDF" not in name.upper()]
    ordered = default_names + preferred + names
    return list(dict.fromkeys(ordered))


def _printer_name(row: object) -> str:
    if not isinstance(row, dict):
        return ""
    return str(row.get("Name") or "").strip()


def _list_unix_printers() -> list[str]:
    command = shutil.which("lpstat")
    if not command:
        return []
    try:
        completed = _run_hidden([command, "-a"], check=True, capture_output=True, text=True)
    except Exception:
        return []
    return [line.split()[0] for line in completed.stdout.splitlines() if line.strip()]


class SystemPrinter:
    def __init__(self, printer_name: str | None = None, options: PrintOptions | None = None) -> None:
        self.printer_name = printer_name
        self.options = options

    def print_item(self, item: PrintItem) -> PrintResult:
        system = platform.system().lower()
        try:
            if system == "windows":
                self._print_windows(item.path)
            elif system == "darwin":
                self._print_lp(item.path)
            else:
                self._print_unix(item.path)
        except Exception as exc:  # pragma: no cover - platform integration boundary
            return PrintResult(item=item, status="failed", detail=str(exc))
        return PrintResult(item=item, status="submitted")

    def _print_windows(self, path: Path) -> None:
        if path.suffix.lower() == ".pdf":
            sumatra = find_sumatra_pdf()
            if sumatra:
                args = [str(sumatra), "-silent", "-exit-on-print"]
                settings = _sumatra_print_settings(self.options) if self.options else ""
                if settings:
                    args.extend(["-print-settings", settings])
                if self.printer_name:
                    args.extend(["-print-to", self.printer_name])
                else:
                    args.append("-print-to-default")
                args.append(str(path))
                _run_hidden(args, check=True)
                return
        if self.printer_name:
            os.startfile(str(path), "printto", f'"{self.printer_name}"')  # type: ignore[attr-defined]
            return
        os.startfile(str(path), "print")  # type: ignore[attr-defined]

    def _print_lp(self, path: Path) -> None:
        self._run_print_command(path, preferred=("lp", "lpr"))

    def _print_unix(self, path: Path) -> None:
        self._run_print_command(path, preferred=("lp", "lpr"))

    def _run_print_command(self, path: Path, *, preferred: tuple[str, ...]) -> None:
        command = next((name for name in preferred if shutil.which(name)), None)
        if command is None:
            raise PrinterError("No supported print command found. Install lp or lpr.")

        args = [command]
        if self.printer_name and command == "lp":
            args.extend(["-d", self.printer_name])
        elif self.printer_name and command == "lpr":
            args.extend(["-P", self.printer_name])
        args.append(str(path))

        _run_hidden(args, check=True)


def find_sumatra_pdf() -> Path | None:
    candidates: list[Path] = []
    env_path = os.environ.get("BATCH_PRINT_KIT_SUMATRA")
    if env_path:
        candidates.append(Path(env_path))

    exe_parent = Path(getattr(sys, "executable", "")).resolve().parent if getattr(sys, "executable", "") else None
    if exe_parent:
        candidates.extend(
            [
                exe_parent / "tools" / "SumatraPDF.exe",
                exe_parent / "SumatraPDF.exe",
                exe_parent.parent / "tools" / "SumatraPDF" / "SumatraPDF.exe",
            ]
        )

    module_root = Path(__file__).resolve().parents[2]
    candidates.extend(
        [
            module_root / "tools" / "SumatraPDF" / "SumatraPDF.exe",
            module_root / "tools" / "SumatraPDF.exe",
        ]
    )

    path_hit = shutil.which("SumatraPDF.exe") or shutil.which("SumatraPDF")
    if path_hit:
        candidates.append(Path(path_hit))

    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate
    return None


def _sumatra_print_settings(options: PrintOptions) -> str:
    parts: list[str] = []
    copies = options.normalized_copies()
    if copies > 1:
        parts.append(f"{copies}x")

    paper_size = options.paper_size.strip().upper()
    if paper_size in {"A4", "A5"}:
        parts.append(f"paper={paper_size}")

    color_mode = options.color_mode.strip().lower()
    if color_mode in {"gray", "grayscale", "mono", "monochrome"}:
        parts.append("monochrome")
    elif color_mode == "color":
        parts.append("color")

    return ",".join(parts)


def _run_hidden(*args, **kwargs):
    if CREATE_NO_WINDOW:
        kwargs.setdefault("creationflags", CREATE_NO_WINDOW)
    return subprocess.run(*args, **kwargs)
