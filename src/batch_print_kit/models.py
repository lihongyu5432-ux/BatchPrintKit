from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PrintOptions:
    paper_size: str = "A4"
    color_mode: str = "color"
    copies: int = 1

    def normalized_copies(self) -> int:
        return max(1, min(int(self.copies), 99))


@dataclass(frozen=True)
class PrintItem:
    path: Path
    size_bytes: int

    @property
    def extension(self) -> str:
        return self.path.suffix.lower()

    @property
    def print_method(self) -> str:
        extension = self.extension
        if extension == ".pdf":
            return "PDF / SumatraPDF"
        if extension in {".png", ".jpg", ".jpeg", ".bmp"}:
            return "Image / Windows"
        if extension in {".txt", ".rtf"}:
            return "Text / Windows"
        if extension in {".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"}:
            return "Office / Associated App"
        return "Associated App"


@dataclass(frozen=True)
class PrintResult:
    item: PrintItem
    status: str
    detail: str = ""
