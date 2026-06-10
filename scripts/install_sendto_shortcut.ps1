$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$exePath = Join-Path $repoRoot "dist\BatchPrintKit\BatchPrintKit.exe"
if (-not (Test-Path $exePath)) {
    throw "Cannot find $exePath. Run scripts\build_windows_exe.ps1 first."
}

$sendTo = [Environment]::GetFolderPath("SendTo")
$shortcutPath = Join-Path $sendTo "Batch Print Kit.lnk"
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $exePath
$shortcut.WorkingDirectory = Split-Path -Parent $exePath
$shortcut.Description = "Open selected files and folders in Batch Print Kit"
$shortcut.Save()

Write-Host "Installed Send To shortcut:"
Write-Host $shortcutPath
Write-Host ""
Write-Host "Usage: select files/folders in Explorer, right-click, choose Send to > Batch Print Kit."
