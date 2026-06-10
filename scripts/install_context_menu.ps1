$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$exePath = Join-Path $repoRoot "dist\BatchPrintKit\BatchPrintKit.exe"
if (-not (Test-Path $exePath)) {
    throw "Cannot find $exePath. Run scripts\build_windows_exe.ps1 first."
}
$menuText = -join ([char[]](0x7528, 0x6279, 0x91cf, 0x6253, 0x5370, 0x5de5, 0x5177, 0x6253, 0x5f00))
$showMoreText = -join ([char[]](0x663e, 0x793a, 0x66f4, 0x591a, 0x9009, 0x9879))

function Install-BatchPrintVerb {
    param(
        [Parameter(Mandatory = $true)][string]$SubKey,
        [Parameter(Mandatory = $true)][string]$Command
    )

    $key = [Microsoft.Win32.Registry]::CurrentUser.CreateSubKey($SubKey)
    $key.SetValue("MUIVerb", $menuText, [Microsoft.Win32.RegistryValueKind]::String)
    $key.SetValue("Icon", $exePath, [Microsoft.Win32.RegistryValueKind]::String)
    $key.SetValue("Position", "Top", [Microsoft.Win32.RegistryValueKind]::String)
    $key.SetValue("MultiSelectModel", "Player", [Microsoft.Win32.RegistryValueKind]::String)
    $commandKey = $key.CreateSubKey("command")
    $commandKey.SetValue("", $Command, [Microsoft.Win32.RegistryValueKind]::String)
    $commandKey.Close()
    $key.Close()
}

$quotedExe = '"' + $exePath + '"'
Install-BatchPrintVerb -SubKey "Software\Classes\*\shell\BatchPrintKit" -Command "$quotedExe `"%1`""
Install-BatchPrintVerb -SubKey "Software\Classes\Directory\shell\BatchPrintKit" -Command "$quotedExe `"%1`""
Install-BatchPrintVerb -SubKey "Software\Classes\Directory\Background\shell\BatchPrintKit" -Command "$quotedExe `"%V`""

Write-Host "Installed context menu item: $menuText"
Write-Host "If it does not appear in the first Windows 11 menu, click $showMoreText once."
