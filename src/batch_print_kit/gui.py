from __future__ import annotations

import queue
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from batch_print_kit.jobs import build_plan_many, run_print_job
from batch_print_kit.models import PrintItem, PrintResult
from batch_print_kit.printers import find_sumatra_pdf, list_printers, open_printer_settings, print_test_page


DEFAULT_EXTENSIONS = ".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.rtf,.png,.jpg,.jpeg,.bmp"
LANGUAGE_NAMES = {"zh": "简体中文", "en": "English"}
LANGUAGE_BY_NAME = {name: key for key, name in LANGUAGE_NAMES.items()}
TEXT = {
    "zh": {
        "app_title": "批量打印工具",
        "ready": "请选择文件夹或文件开始。",
        "paths": "路径",
        "browse": "浏览",
        "language": "语言",
        "extensions": "扩展名",
        "recursive": "包含子文件夹",
        "printer": "打印机",
        "refresh": "刷新",
        "settings": "打印机设置",
        "test_page": "测试页",
        "scan": "扫描",
        "import_files": "导入文件",
        "remove_selected": "移除选中",
        "clear_queue": "清空",
        "print": "打印",
        "file": "文件",
        "type": "类型",
        "size": "大小",
        "full_path": "完整路径",
        "method": "打印方式",
        "choose_folder": "选择要扫描的文件夹",
        "scanning": "正在扫描...",
        "found": "找到 {count} 个项目。",
        "choose_files": "选择要导入的文件",
        "all_files": "所有文件",
        "import_failed": "导入失败",
        "imported_files": "已导入 {count} 个文件。",
        "nothing_print_title": "没有可打印的项目",
        "nothing_print": "请先扫描或导入文件，再运行打印任务。",
        "submit_title": "提交打印任务",
        "submit_message": "确认把 {count} 个文件提交到 {printer}？",
        "submitting": "正在提交打印任务...",
        "choose_path_title": "请选择路径",
        "choose_path": "请先选择文件夹或文件。",
        "print_submitted": "打印任务已提交",
        "ready_short": "就绪。",
        "failed_count": "{count} 个项目失败。",
        "result_summary": "{title}：{count} 个项目，状态：{statuses}。",
        "selected_from_explorer": "来自资源管理器的 {count} 个选中项目",
        "printer_loaded": "已加载 {count} 个打印机。",
        "printer_none": "系统没有返回可用打印机。",
        "default_printer": "默认打印机",
        "removed_items": "已移除 {count} 个文件。",
        "cleared_queue": "已清空队列。",
        "test_page_sent": "测试页已提交到 {printer}。",
        "settings_failed": "打不开打印机设置",
        "pdf_engine": "PDF 引擎：{engine}",
    },
    "en": {
        "app_title": "Batch Print Kit",
        "ready": "Choose a folder or file to begin.",
        "paths": "Paths",
        "browse": "Browse",
        "language": "Language",
        "extensions": "Extensions",
        "recursive": "Recursive",
        "printer": "Printer",
        "refresh": "Refresh",
        "settings": "Printer Settings",
        "test_page": "Test Page",
        "scan": "Scan",
        "import_files": "Import Files",
        "remove_selected": "Remove Selected",
        "clear_queue": "Clear",
        "print": "Print",
        "file": "File",
        "type": "Type",
        "size": "Size",
        "full_path": "Full path",
        "method": "Method",
        "choose_folder": "Choose folder to scan",
        "scanning": "Scanning...",
        "found": "Found {count} item(s).",
        "choose_files": "Choose files to import",
        "all_files": "All files",
        "import_failed": "Import failed",
        "imported_files": "Imported {count} file(s).",
        "nothing_print_title": "Nothing to print",
        "nothing_print": "Scan or import files before running a print job.",
        "submit_title": "Submit print job",
        "submit_message": "Submit {count} file(s) to {printer}?",
        "submitting": "Submitting print job...",
        "choose_path_title": "Choose a path",
        "choose_path": "Choose a folder or file first.",
        "print_submitted": "Print job submitted",
        "ready_short": "Ready.",
        "failed_count": "{count} item(s) failed.",
        "result_summary": "{title}: {count} item(s), status: {statuses}.",
        "selected_from_explorer": "{count} selected item(s) from Explorer",
        "printer_loaded": "Loaded {count} printer(s).",
        "printer_none": "No printers were returned by the system.",
        "default_printer": "Default printer",
        "removed_items": "Removed {count} file(s).",
        "cleared_queue": "Cleared the queue.",
        "test_page_sent": "Test page sent to {printer}.",
        "settings_failed": "Could not open printer settings",
        "pdf_engine": "PDF engine: {engine}",
    },
}


class BatchPrintApp(tk.Tk):
    def __init__(self, initial_paths: list[Path] | None = None) -> None:
        super().__init__()
        self.title("Batch Print Kit")
        self.geometry("1040x680")
        self.minsize(900, 560)

        self.items: list[PrintItem] = []
        self.events: queue.Queue[tuple[str, object]] = queue.Queue()
        self.text_widgets: list[tuple[tk.Widget, str]] = []
        self.heading_keys = {
            "name": "file",
            "extension": "type",
            "size": "size",
            "method": "method",
            "path": "full_path",
        }

        self.initial_paths = initial_paths or []
        self.language_var = tk.StringVar(value=LANGUAGE_NAMES["zh"])
        self.path_var = tk.StringVar(value=_format_paths(self.initial_paths, "zh"))
        self.extensions_var = tk.StringVar(value=DEFAULT_EXTENSIONS)
        self.printer_var = tk.StringVar()
        self.recursive_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value=self.t("ready"))

        self._build_ui()
        self._apply_language()
        self.refresh_printers(show_status=False)
        self.after(100, self._poll_events)
        if self.initial_paths:
            self.after(150, self.scan)

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        top = ttk.Frame(self, padding=(12, 12, 12, 6))
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(1, weight=1)

        self._label(top, "paths").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Entry(top, textvariable=self.path_var).grid(row=0, column=1, sticky="ew")
        self._button(top, "browse", self._browse_path).grid(row=0, column=2, padx=(8, 0))
        self._label(top, "language").grid(row=0, column=3, sticky="w", padx=(12, 8))
        language_box = ttk.Combobox(top, textvariable=self.language_var, values=list(LANGUAGE_NAMES.values()), state="readonly", width=12)
        language_box.grid(row=0, column=4, sticky="ew")
        language_box.bind("<<ComboboxSelected>>", lambda _event: self._apply_language())

        self._label(top, "extensions").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(8, 0))
        ttk.Entry(top, textvariable=self.extensions_var).grid(row=1, column=1, sticky="ew", pady=(8, 0))
        self._checkbutton(top, "recursive", self.recursive_var).grid(row=1, column=2, sticky="w", padx=(8, 0), pady=(8, 0))

        self._label(top, "printer").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=(8, 0))
        self.printer_box = ttk.Combobox(top, textvariable=self.printer_var, state="readonly")
        self.printer_box.grid(row=2, column=1, sticky="ew", pady=(8, 0))
        self._button(top, "refresh", self.refresh_printers).grid(row=2, column=2, padx=(8, 0), pady=(8, 0))
        self._button(top, "settings", self.open_settings).grid(row=2, column=3, padx=(12, 0), pady=(8, 0))
        self._button(top, "test_page", self.print_test_page).grid(row=2, column=4, padx=(8, 0), pady=(8, 0))

        actions = ttk.Frame(top)
        actions.grid(row=3, column=1, columnspan=4, sticky="e", pady=(10, 0))
        self._button(actions, "scan", self.scan).grid(row=0, column=0, padx=(0, 8))
        self._button(actions, "import_files", self.import_files).grid(row=0, column=1, padx=(0, 8))
        self._button(actions, "remove_selected", self.remove_selected).grid(row=0, column=2, padx=(0, 8))
        self._button(actions, "clear_queue", self.clear_queue).grid(row=0, column=3, padx=(0, 8))
        self._button(actions, "print", self.print_items).grid(row=0, column=4)

        table_frame = ttk.Frame(self, padding=(12, 6, 12, 6))
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = ("index", "name", "extension", "size", "method", "path")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")
        self.table.heading("index", text="#")
        self.table.column("index", width=50, anchor="e", stretch=False)
        self.table.column("name", width=220, stretch=False)
        self.table.column("extension", width=80, stretch=False)
        self.table.column("size", width=100, anchor="e", stretch=False)
        self.table.column("method", width=170, stretch=False)
        self.table.column("path", width=500)
        self.table.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.table.configure(yscrollcommand=scrollbar.set)

        bottom = ttk.Frame(self, padding=(12, 6, 12, 12))
        bottom.grid(row=2, column=0, sticky="ew")
        bottom.columnconfigure(0, weight=1)
        ttk.Label(bottom, textvariable=self.status_var).grid(row=0, column=0, sticky="w")

    def _browse_path(self) -> None:
        folder = filedialog.askdirectory(title=self.t("choose_folder"))
        if folder:
            self.path_var.set(folder)
            self.initial_paths = [Path(folder)]

    def scan(self) -> None:
        paths = self._selected_paths()
        if not paths:
            return
        self._set_busy(self.t("scanning"))
        self._run_worker("scan", lambda: build_plan_many(paths, extensions=self.extensions_var.get(), recursive=self.recursive_var.get()))

    def import_files(self) -> None:
        selected = filedialog.askopenfilenames(title=self.t("choose_files"), filetypes=[(self.t("all_files"), "*.*")])
        if not selected:
            return
        try:
            items = build_plan_many([Path(path) for path in selected], extensions=None, recursive=False)
        except Exception as exc:
            messagebox.showerror(self.t("import_failed"), str(exc))
            return
        self.items = items
        self.initial_paths = [item.path for item in items]
        self.path_var.set(_format_paths(self.initial_paths, self.language_key))
        self._refresh_table()
        self.status_var.set(self.t("imported_files", count=len(items)))

    def refresh_printers(self, show_status: bool = True) -> None:
        printers = list_printers()
        self.printer_box.configure(values=printers)
        if printers and (not self.printer_var.get() or self.printer_var.get() not in printers):
            self.printer_var.set(printers[0])
        if show_status:
            self.status_var.set(self.t("printer_loaded", count=len(printers)) if printers else self.t("printer_none"))

    def open_settings(self) -> None:
        printer_name = self.printer_var.get().strip()
        try:
            open_printer_settings(printer_name or None)
        except Exception as exc:
            messagebox.showerror(self.t("settings_failed"), str(exc))

    def print_test_page(self) -> None:
        printer_name = self.printer_var.get().strip() or None
        result = print_test_page(printer_name)
        if result.status == "failed":
            messagebox.showerror(self.t("failed_count", count=1), result.detail)
            return
        self.status_var.set(self.t("test_page_sent", printer=printer_name or self.t("default_printer")))

    def remove_selected(self) -> None:
        selected_rows = set(self.table.selection())
        if not selected_rows:
            return
        selected_paths = {self.table.item(row, "values")[5] for row in selected_rows}
        before = len(self.items)
        self.items = [item for item in self.items if str(item.path) not in selected_paths]
        self.initial_paths = [item.path for item in self.items]
        self.path_var.set(_format_paths(self.initial_paths, self.language_key))
        self._refresh_table()
        self.status_var.set(self.t("removed_items", count=before - len(self.items)))

    def clear_queue(self) -> None:
        self.items = []
        self.initial_paths = []
        self.path_var.set("")
        self._refresh_table()
        self.status_var.set(self.t("cleared_queue"))

    def print_items(self) -> None:
        if not self.items:
            messagebox.showinfo(self.t("nothing_print_title"), self.t("nothing_print"))
            return
        printer_name = self.printer_var.get().strip() or self.t("default_printer")
        if not messagebox.askyesno(
            self.t("submit_title"),
            self.t("submit_message", count=len(self.items), printer=printer_name),
        ):
            return
        self._set_busy(self.t("submitting"))
        self._run_worker(
            "print",
            lambda: run_print_job(self.items, confirmed=True, printer_name=self.printer_var.get().strip() or None),
        )

    def _selected_paths(self) -> list[Path]:
        if self.initial_paths and self.path_var.get() in _all_formatted_paths(self.initial_paths):
            return self.initial_paths
        raw = self.path_var.get().strip()
        if not raw:
            messagebox.showinfo(self.t("choose_path_title"), self.t("choose_path"))
            return []
        return [Path(raw)]

    def _run_worker(self, event_name: str, work) -> None:
        def target() -> None:
            try:
                self.events.put((event_name, work()))
            except Exception as exc:
                self.events.put(("error", exc))

        threading.Thread(target=target, daemon=True).start()

    def _poll_events(self) -> None:
        try:
            while True:
                name, payload = self.events.get_nowait()
                if name == "scan":
                    self.items = list(payload)  # type: ignore[arg-type]
                    self._refresh_table()
                    self.status_var.set(self.t("found", count=len(self.items)))
                elif name == "print":
                    self._show_results(self.t("print_submitted"), list(payload))  # type: ignore[arg-type]
                elif name == "error":
                    messagebox.showerror("Batch Print Kit", str(payload))
                    self.status_var.set(self.t("ready_short"))
        except queue.Empty:
            pass
        self.after(100, self._poll_events)

    def _refresh_table(self) -> None:
        for row in self.table.get_children():
            self.table.delete(row)
        for index, item in enumerate(self.items, start=1):
            self.table.insert(
                "",
                "end",
                values=(index, item.path.name, item.extension, _format_size(item.size_bytes), _resolve_print_method(item), str(item.path)),
            )

    def _show_results(self, title: str, results: list[PrintResult]) -> None:
        failed = [result for result in results if result.status == "failed"]
        if failed:
            message = "\n".join(f"{result.item.path.name}: {result.detail}" for result in failed[:8])
            messagebox.showerror(title, message)
            self.status_var.set(self.t("failed_count", count=len(failed)))
            return
        statuses = ", ".join(sorted({result.status for result in results}))
        self.status_var.set(self.t("result_summary", title=title, count=len(results), statuses=statuses))
        messagebox.showinfo(title, self.status_var.get())

    def _set_busy(self, message: str) -> None:
        self.status_var.set(message)
        self.update_idletasks()

    def _label(self, parent: tk.Widget, text_key: str) -> ttk.Label:
        widget = ttk.Label(parent)
        self.text_widgets.append((widget, text_key))
        return widget

    def _button(self, parent: tk.Widget, text_key: str, command) -> ttk.Button:
        widget = ttk.Button(parent, command=command)
        self.text_widgets.append((widget, text_key))
        return widget

    def _checkbutton(self, parent: tk.Widget, text_key: str, variable: tk.BooleanVar) -> ttk.Checkbutton:
        widget = ttk.Checkbutton(parent, variable=variable)
        self.text_widgets.append((widget, text_key))
        return widget

    def _apply_language(self) -> None:
        previous_path = self.path_var.get()
        self.title(self.t("app_title"))
        for widget, text_key in self.text_widgets:
            widget.configure(text=self.t(text_key))
        for column, text_key in self.heading_keys.items():
            self.table.heading(column, text=self.t(text_key))
        if self.initial_paths and previous_path in _all_formatted_paths(self.initial_paths):
            self.path_var.set(_format_paths(self.initial_paths, self.language_key))

    @property
    def language_key(self) -> str:
        return LANGUAGE_BY_NAME.get(self.language_var.get(), "zh")

    def t(self, key: str, **values: object) -> str:
        return translate(key, self.language_key, **values)


def _format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.1f} MB"


def translate(key: str, language: str = "zh", **values: object) -> str:
    template = TEXT.get(language, TEXT["zh"]).get(key, TEXT["en"].get(key, key))
    return template.format(**values)


def _format_paths(paths: list[Path], language: str = "zh") -> str:
    if not paths:
        return ""
    if len(paths) == 1:
        return str(paths[0])
    return translate("selected_from_explorer", language, count=len(paths))


def _resolve_print_method(item: PrintItem) -> str:
    if item.extension == ".pdf":
        return "PDF / SumatraPDF" if find_sumatra_pdf() else "PDF / Associated App"
    return item.print_method


def _all_formatted_paths(paths: list[Path]) -> set[str]:
    return {_format_paths(paths, language) for language in LANGUAGE_NAMES}


def main(argv: list[str] | None = None) -> None:
    raw_args = sys.argv[1:] if argv is None else argv
    app = BatchPrintApp([Path(arg) for arg in raw_args])
    app.mainloop()


if __name__ == "__main__":
    main()
