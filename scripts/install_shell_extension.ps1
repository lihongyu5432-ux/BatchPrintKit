$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$exePath = Join-Path $repoRoot "dist\BatchPrintKit\BatchPrintKit.exe"
$dllPath = Join-Path $repoRoot "dist\ShellExtension\BatchPrintShellExtension.dll"
$clsid = "{61F77B19-AF18-4F36-9058-6F9DE50E5931}"
$menuText = -join ([char[]](0x7528, 0x6279, 0x91cf, 0x6253, 0x5370, 0x5de5, 0x5177, 0x6253, 0x5f00))

if (-not (Test-Path $exePath)) {
    throw "Cannot find app exe: $exePath. Run scripts\build_windows_exe.ps1 first."
}
if (-not (Test-Path $dllPath)) {
    throw "Cannot find shell extension DLL: $dllPath. Run scripts\build_shell_extension.ps1 first."
}

function Set-RegistryString {
    param(
        [Parameter(Mandatory = $true)][string]$SubKey,
        [Parameter(Mandatory = $true)][AllowEmptyString()][string]$Name,
        [Parameter(Mandatory = $true)][string]$Value
    )
    $key = [Microsoft.Win32.Registry]::CurrentUser.CreateSubKey($SubKey)
    $key.SetValue($Name, $Value, [Microsoft.Win32.RegistryValueKind]::String)
    $key.Close()
}

Set-RegistryString -SubKey "Software\BatchPrintKit" -Name "AppPath" -Value $exePath
Set-RegistryString -SubKey "Software\Classes\CLSID\$clsid" -Name "" -Value "BatchPrintKit Explorer Command"
Set-RegistryString -SubKey "Software\Classes\CLSID\$clsid\InprocServer32" -Name "" -Value $dllPath
Set-RegistryString -SubKey "Software\Classes\CLSID\$clsid\InprocServer32" -Name "ThreadingModel" -Value "Apartment"

foreach ($subKey in @(
    "Software\Classes\*\shell\BatchPrintKit.Modern",
    "Software\Classes\Directory\shell\BatchPrintKit.Modern"
)) {
    Set-RegistryString -SubKey $subKey -Name "MUIVerb" -Value $menuText
    Set-RegistryString -SubKey $subKey -Name "Icon" -Value $exePath
    Set-RegistryString -SubKey $subKey -Name "ExplorerCommandHandler" -Value $clsid
    Set-RegistryString -SubKey $subKey -Name "MultiSelectModel" -Value "Player"
}

Write-Host "Installed per-user ExplorerCommandHandler: $menuText"
Write-Host "Restart Explorer or sign out/in if the Windows 11 menu does not refresh immediately."
