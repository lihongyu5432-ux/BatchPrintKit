from __future__ import annotations

from pathlib import Path

from .discovery import discover_files, discover_many, parse_extensions
from .models import PrintItem, PrintOptions, PrintResult
from .printers import SystemPrinter


def build_plan(root: Path, *, extensions: str | None = None, recursive: bool = False) -> list[PrintItem]:
    return discover_files(root, extensions=parse_extensions(extensions), recursive=recursive)


def build_plan_many(roots: list[Path], *, extensions: str | None = None, recursive: bool = False) -> list[PrintItem]:
    return discover_many(roots, extensions=parse_extensions(extensions), recursive=recursive)


def run_print_job(
    items: list[PrintItem],
    *,
    confirmed: bool = False,
    printer_name: str | None = None,
    options: PrintOptions | None = None,
) -> list[PrintResult]:
    if not confirmed:
        return [PrintResult(item=item, status="dry-run", detail="Add --yes to submit this item.") for item in items]

    printer = SystemPrinter(printer_name=printer_name, options=options)
    return [printer.print_item(item) for item in items]
