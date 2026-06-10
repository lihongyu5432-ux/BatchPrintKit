$ErrorActionPreference = "Stop"

$keys = @(
    "Software\Classes\*\shell\BatchPrintKit",
    "Software\Classes\Directory\shell\BatchPrintKit",
    "Software\Classes\Directory\Background\shell\BatchPrintKit"
)

foreach ($key in $keys) {
    try {
        [Microsoft.Win32.Registry]::CurrentUser.DeleteSubKeyTree($key)
        Write-Host "Removed HKCU:\$key"
    } catch [System.ArgumentException] {
        Write-Host "Not installed: HKCU:\$key"
    }
}
