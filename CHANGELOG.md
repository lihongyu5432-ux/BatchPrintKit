# Changelog

## 0.2.0

- Add a Tkinter desktop app for Windows users.
- Add a `batch-print-gui` entry point.
- Add PowerShell scripts to launch the GUI and build a Windows executable with PyInstaller.
- Add multiple path support for Explorer handoff workflows.
- Add Send To shortcut install/uninstall scripts for multi-select files and folders.
- Replace desktop import/export actions with direct multi-file import.
- Add a direct Windows Explorer context-menu installer for `批量打印`.
- Rename the Explorer verb to `用批量打印工具打开` and add classic context menu toggle scripts for Windows 11.
- Add a minimal native `IExplorerCommand` shell extension source and per-user build/install scripts.
- Add sparse MSIX package build, sign, install, and uninstall scripts for Windows 11 context-menu identity.
- Add desktop printer selection, printer settings, remove selected, and clear queue controls.
- Add optional SumatraPDF portable installer and PDF-first print backend.
- Remove the desktop dry-run action.
- Make the desktop printer settings button open the selected printer driver's preferences page instead of Windows Settings.

## 0.1.0

- Add directory scanning, extension filtering, stable sorting, and safe print confirmation.
- Add Windows/macOS/Linux printer dispatch adapters.
- Add unit tests and GitHub Actions workflow.
