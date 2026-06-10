# BatchPrintKit Explorer Command

This folder contains a minimal native `IExplorerCommand` shell extension for Windows Explorer context-menu integration.

The DLL is intentionally thin. It only collects selected Explorer paths and launches `BatchPrintKit.exe`; all UI, scanning, and printing stay in the Python desktop app.

## Build

Requires Visual Studio Build Tools with the C++ workload. Windows 11 first-level menu placement can also require app identity through MSIX/Sparse Package registration; the per-user COM installer here is the cautious first step and does not write machine-wide keys.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_shell_extension.ps1
```

## Install

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install_shell_extension.ps1
```

## Uninstall

```powershell
powershell -ExecutionPolicy Bypass -File scripts\uninstall_shell_extension.ps1
```

The installer writes only per-user `HKCU` registry keys.
