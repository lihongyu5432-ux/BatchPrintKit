# Usage Guide

## Desktop app

Start the desktop program from the project folder:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_gui.ps1
```

After installing the package, you can also run:

```powershell
batch-print-gui
```

The desktop app supports folder selection, direct multi-file import, extension filters, recursive scanning, printer selection, printer-driver settings, queue cleanup, test-page printing, and confirmed printing.

For PDF files, install the optional bundled SumatraPDF engine:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install_sumatra_pdf.ps1
```

## Windows Explorer integration

Install the Send To shortcut:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install_sendto_shortcut.ps1
powershell -ExecutionPolicy Bypass -File scripts\install_context_menu.ps1
powershell -ExecutionPolicy Bypass -File scripts\enable_classic_context_menu.ps1
```

After that, select one or more files/folders in Explorer, right-click, and choose:

```text
Send to > Batch Print Kit
用批量打印工具打开
```

The desktop app opens with those selected items preloaded and scans them automatically.

## Printer Settings

Click `打印机设置` / `Printer Settings` after selecting a printer. On Windows this opens that printer driver's own preferences page, not the Windows Settings app. Use the driver page for paper size, grayscale/color, quality, duplex, tray, and other printer-specific options.

## Windows 11 Native Menu

For a Windows Explorer native command handler, build and install the native shell extension:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_shell_extension.ps1
powershell -ExecutionPolicy Bypass -File scripts\install_shell_extension.ps1
powershell -ExecutionPolicy Bypass -File scripts\build_sparse_package.ps1
powershell -ExecutionPolicy Bypass -File scripts\sign_sparse_package.ps1
powershell -ExecutionPolicy Bypass -File scripts\install_sparse_package.ps1
```

This requires Visual Studio Build Tools with the C++ workload. The extension writes per-user registry keys only and launches the existing desktop app. Windows 11 first-level menu placement may also require app identity through MSIX/Sparse Package registration.

Remove the shortcut:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\uninstall_sendto_shortcut.ps1
powershell -ExecutionPolicy Bypass -File scripts\uninstall_context_menu.ps1
powershell -ExecutionPolicy Bypass -File scripts\disable_classic_context_menu.ps1
powershell -ExecutionPolicy Bypass -File scripts\uninstall_shell_extension.ps1
powershell -ExecutionPolicy Bypass -File scripts\uninstall_sparse_package.ps1
```

## Safe workflow

1. Run `plan`.
2. Review the terminal queue.
3. Run `print --yes` only when the queue is correct.

```powershell
batch-print plan C:\Invoices C:\Receipts --extensions .pdf --recursive
batch-print print C:\Invoices C:\Receipts --extensions .pdf --recursive --yes
```

## Importing Files

Click `导入文件` / `Import Files` in the desktop app and select one or more files. The imported files are added to the print queue directly.

## Recommended extension sets

Office documents:

```powershell
--extensions .pdf,.docx,.xlsx
```

Text and markdown review packets:

```powershell
--extensions .txt,.md
```

Images:

```powershell
--extensions .png,.jpg,.jpeg
```

## Exit codes

- `0`: command completed and at least one planned item was found, or dry-run/submit completed
- `1`: command failed
- `2`: plan completed but no files matched

## Real printing caveats

Windows printing uses the default app registered for each non-PDF file extension. If a file does not print, test that file manually from Explorer first. Some apps open a print dialog instead of silently printing.

When SumatraPDF is installed through `scripts\install_sumatra_pdf.ps1`, PDF files are printed through SumatraPDF instead of WPS. Other Office formats may still use the registered app unless a future LibreOffice conversion backend is enabled.
