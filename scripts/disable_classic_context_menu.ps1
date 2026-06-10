$ErrorActionPreference = "Stop"

$subKey = "Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2c}"
try {
    [Microsoft.Win32.Registry]::CurrentUser.DeleteSubKeyTree($subKey)
    Write-Host "Restored Windows 11 context menu for current user."
} catch [System.ArgumentException] {
    Write-Host "Classic context menu override was not installed."
}

Write-Host "Restarting Explorer..."
Get-Process explorer -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Process explorer.exe
