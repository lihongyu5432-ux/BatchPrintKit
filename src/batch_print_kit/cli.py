from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .jobs import build_plan_many, run_print_job
from .models import PrintItem, PrintResult


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "plan":
            items = build_plan_many([Path(path) for path in args.paths], extensions=args.extensions, recursive=args.recursive)
            _print_plan(items)
            return 0 if items else 2

        if args.command == "print":
            items = build_plan_many([Path(path) for path in args.paths], extensions=args.extensions, recursive=args.recursive)
            _print_plan(items)
            results = run_print_job(items, confirmed=args.yes, printer_name=args.printer)
            _print_results(results)
            return 0 if all(result.status in {"submitted", "dry-run"} for result in results) else 1
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.print_help()
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="batch-print", description="Plan and run safe batch print jobs.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan", help="Preview files that would be printed.")
    _add_common_args(plan)

    print_cmd = subparsers.add_parser("print", help="Preview and optionally submit a print job.")
    _add_common_args(print_cmd)
    print_cmd.add_argument("--yes", action="store_true", help="Submit files to the system printer.")
    print_cmd.add_argument("--printer", help="Printer name for lp/lpr platforms. Windows support is planned.")

    return parser


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("paths", nargs="+", help="File(s) or folder(s) to scan.")
    parser.add_argument("--extensions", help="Comma-separated extensions, for example .pdf,.docx,.txt.")
    parser.add_argument("--recursive", action="store_true", help="Scan subfolders.")


def _print_plan(items: list[PrintItem]) -> None:
    print(f"Found {len(items)} printable item(s).")
    for index, item in enumerate(items, start=1):
        print(f"{index:>3}. {item.path} ({item.size_bytes} bytes)")


def _print_results(results: list[PrintResult]) -> None:
    if not results:
        return
    print("\nResults:")
    for index, result in enumerate(results, start=1):
        detail = f" - {result.detail}" if result.detail else ""
        print(f"{index:>3}. {result.status}: {result.item.path}{detail}")


if __name__ == "__main__":
    raise SystemExit(main())
