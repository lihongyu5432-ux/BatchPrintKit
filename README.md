# Batch Print Kit

[![Tests](https://github.com/lihongyu5432-ux/BatchPrintKit/actions/workflows/test.yml/badge.svg)](https://github.com/lihongyu5432-ux/BatchPrintKit/actions/workflows/test.yml)
[![Release](https://img.shields.io/github/v/release/lihongyu5432-ux/BatchPrintKit)](https://github.com/lihongyu5432-ux/BatchPrintKit/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

English | [简体中文](README.zh-CN.md)

Batch Print Kit is a small open-source Windows desktop and command line tool for building and running batch print jobs.

[Product page](https://lihongyu5432-ux.github.io/BatchPrintKit/) · [Download](https://github.com/lihongyu5432-ux/BatchPrintKit/releases/latest) · [Feedback](https://github.com/lihongyu5432-ux/BatchPrintKit/issues)

![Batch Print Kit desktop screenshot](docs/images/screenshot-main.png)

![Batch Print Kit demo](docs/images/demo.gif)

## Why

Windows can print one file easily, but printing a mixed pile of PDFs, Office documents, images, and folders is still awkward. Batch Print Kit gives that workflow a small queue-based desktop app:

- select many files/folders from Explorer
- review the exact queue before printing
- choose the real printer instead of WPS PDF / Microsoft Print to PDF by accident
- open the selected printer driver's own settings page for paper, grayscale, quality, duplex, and trays
- print PDFs through bundled SumatraPDF when installed

It helps you:

- collect printable files from folders
- filter by extension
- sort files in a predictable order
- review and clean the exact print queue before printing
- import many files directly from a file picker
- choose a printer from the desktop app
- open the selected printer's real driver preferences page for paper, quality, color, grayscale, and other printer-specific options
- print PDFs through optional bundled SumatraPDF instead of the default WPS/PDF association
- send files to the system printer when you explicitly confirm the job
- use a simple Windows desktop interface when a terminal is inconvenient

The project is intentionally dependency-light and works with the Python standard library.

## Download

For normal Windows users, download the latest Windows zip from GitHub Releases:

[Download BatchPrintKit-v0.2.0-win64.zip](https://github.com/lihongyu5432-ux/BatchPrintKit/releases/download/v0.2.0/BatchPrintKit-v0.2.0-win64.zip)

Unzip it and run:

```text
BatchPrintKit.exe
```

Scoop users can install from the Batch Print Kit bucket:

```powershell
scoop bucket add lihongyu https://github.com/lihongyu5432-ux/scoop-bucket
scoop install batch-print-kit
```

## Install from source

```powershell
git clone https://github.com/lihongyu5432-ux/BatchPrintKit.git
cd BatchPrintKit
python -m pip install -e .
```

For local development without installing:

```powershell
$env:PYTHONPATH="src"
python -m batch_print_kit.cli plan examples/sample-docs --extensions .txt,.pdf --recursive
```

## Quick start

Desktop app:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_gui.ps1
```

Or, after installing:

```powershell
batch-print-gui
```

Install Explorer integration:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install_sendto_shortcut.ps1
powershell -ExecutionPolicy Bypass -File scripts\install_context_menu.ps1
powershell -ExecutionPolicy Bypass -File scripts\enable_classic_context_menu.ps1
```

Windows 11 native context-menu integration is available under `native/shell_extension` when Visual Studio C++ Build Tools are installed. See [docs/usage.md](docs/usage.md) for the full install and uninstall commands.

Install the optional PDF engine:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install_sumatra_pdf.ps1
```

Then select files/folders in Windows Explorer, right-click, and choose `用批量打印工具打开`.
The desktop app can also import many files directly.

## Good fit

Batch Print Kit is useful for small offices, warehouses, schools, stores, and anyone who repeatedly prints folders of PDFs, spreadsheets, labels, images, or order documents on Windows.

## Feedback Wanted

Real printer setups vary a lot. If Batch Print Kit works for your printer, or if a specific file type fails, please open an issue with:

- Windows version
- printer model
- file type
- whether PDF printing used SumatraPDF

Stars are appreciated if the tool saves you a little time.

CLI plan:


```powershell
batch-print plan C:\Docs C:\MoreDocs --extensions .pdf,.docx --recursive
```

Print after reviewing the queue:

```powershell
batch-print print C:\Docs --extensions .pdf --recursive --yes
```

By default, `print` only performs a dry run. Add `--yes` to submit jobs.

## Build a Windows executable

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install_sumatra_pdf.ps1
powershell -ExecutionPolicy Bypass -File scripts\build_windows_exe.ps1
```

The built app is written to:

```text
dist\BatchPrintKit\BatchPrintKit.exe
```

## Platform notes

Batch Print Kit delegates rendering to your operating system:

- Windows PDFs: uses portable SumatraPDF when installed through `scripts\install_sumatra_pdf.ps1`
- Other Windows files: uses the registered application's print action via Windows Shell
- macOS/Linux: uses `lp` or `lpr` when available

The `打印机设置` / `Printer Settings` button opens the selected printer driver's preferences window. Use that driver page to set paper size, grayscale/color, quality, duplex, and other options supported by the printer.

## Project status

This is an early but usable project scaffold. The current goal is a reliable, boring batch-print workflow across both the desktop UI and CLI.

See [docs/maintainer-plan.md](docs/maintainer-plan.md) for the maintenance roadmap.

## License

MIT. See [LICENSE](LICENSE).
