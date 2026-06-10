$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$appExternalLocation = Join-Path $repoRoot "dist\BatchPrintKit"
$msixPath = Join-Path $repoRoot "dist\SparsePackage\BatchPrintKit.ShellExtension.msix"

if (-not (Test-Path (Join-Path $appExternalLocation "BatchPrintKit.exe"))) {
    throw "Cannot find BatchPrintKit.exe under $appExternalLocation. Run scripts\build_windows_exe.ps1 first."
}
if (-not (Test-Path $msixPath)) {
    throw "Cannot find sparse package: $msixPath. Run build_sparse_package.ps1 and sign_sparse_package.ps1 first."
}

powershell -ExecutionPolicy Bypass -File (Join-Path $repoRoot "scripts\install_shell_extension.ps1")

$existing = Get-AppxPackage -Name "BatchPrintKit.ShellExtension" -ErrorAction SilentlyContinue
if ($existing) {
    Remove-AppxPackage -Package $existing.PackageFullName -ErrorAction SilentlyContinue
}

Add-AppxPackage -Path $msixPath -ExternalLocation $appExternalLocation

Get-Process explorer -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 1
Start-Process explorer.exe

Write-Host "Installed sparse package and restarted Explorer."
