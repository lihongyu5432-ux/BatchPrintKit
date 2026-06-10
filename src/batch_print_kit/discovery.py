from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .models import PrintItem


def parse_extensions(raw: str | Iterable[str] | None) -> set[str]:
    if raw is None:
        return set()
    if isinstance(raw, str):
        parts = raw.split(",")
    else:
        parts = list(raw)

    normalized: set[str] = set()
    for part in parts:
        value = part.strip().lower()
        if not value:
            continue
        if not value.startswith("."):
            value = f".{value}"
        normalized.add(value)
    return normalized


def discover_files(root: Path, *, extensions: set[str] | None = None, recursive: bool = False) -> list[PrintItem]:
    root = root.expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Path does not exist: {root}")

    allowed = extensions or set()
    candidates = [root] if root.is_file() else _iter_files(root, recursive)

    items: list[PrintItem] = []
    for path in candidates:
        if not path.is_file():
            continue
        if allowed and path.suffix.lower() not in allowed:
            continue
        items.append(PrintItem(path=path.resolve(), size_bytes=path.stat().st_size))

    return sorted(items, key=lambda item: natural_sort_key(item.path))


def discover_many(roots: Iterable[Path], *, extensions: set[str] | None = None, recursive: bool = False) -> list[PrintItem]:
    seen: set[Path] = set()
    items: list[PrintItem] = []
    for root in roots:
        for item in discover_files(root, extensions=extensions, recursive=recursive):
            if item.path in seen:
                continue
            seen.add(item.path)
            items.append(item)
    return sorted(items, key=lambda item: natural_sort_key(item.path))


def _iter_files(root: Path, recursive: bool) -> Iterable[Path]:
    pattern = "**/*" if recursive else "*"
    return root.glob(pattern)


def natural_sort_key(path: Path) -> tuple[str, ...]:
    return tuple(part.casefold() for part in path.parts)
