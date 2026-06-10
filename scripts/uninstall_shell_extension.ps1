$ErrorActionPreference = "Stop"

$clsid = "{61F77B19-AF18-4F36-9058-6F9DE50E5931}"
$keys = @(
    "Software\Classes\*\shell\BatchPrintKit.Modern",
    "Software\Classes\Directory\shell\BatchPrintKit.Modern",
    "Software\Classes\CLSID\$clsid",
    "Software\BatchPrintKit"
)

foreach ($key in $keys) {
    try {
        [Microsoft.Win32.Registry]::CurrentUser.DeleteSubKeyTree($key)
        Write-Host "Removed HKCU:\$key"
    } catch [System.ArgumentException] {
        Write-Host "Not installed: HKCU:\$key"
    }
}

Write-Host "Restart Explorer or sign out/in if the menu does not refresh immediately."
