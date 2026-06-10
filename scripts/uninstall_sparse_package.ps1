$ErrorActionPreference = "Stop"

$package = Get-AppxPackage -Name "BatchPrintKit.ShellExtension" -ErrorAction SilentlyContinue
if ($package) {
    Remove-AppxPackage -Package $package.PackageFullName
    Write-Host "Removed sparse package: $($package.PackageFullName)"
} else {
    Write-Host "Sparse package is not installed."
}

$thumbprints = @()
foreach ($location in @("Cert:\CurrentUser\My", "Cert:\CurrentUser\TrustedPeople", "Cert:\CurrentUser\Root", "Cert:\LocalMachine\Root")) {
    Get-ChildItem $location -ErrorAction SilentlyContinue |
        Where-Object { $_.Subject -eq "CN=BatchPrintKit" } |
        ForEach-Object {
            $thumbprints += $_.Thumbprint
            Remove-Item -LiteralPath $_.PSPath -Force -ErrorAction SilentlyContinue
        }
}
if ($thumbprints.Count -gt 0) {
    Write-Host "Removed BatchPrintKit signing certificates."
}

Get-Process explorer -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 1
Start-Process explorer.exe
