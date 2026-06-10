$ErrorActionPreference = "Stop"

$subKey = "Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2c}\InprocServer32"
$key = [Microsoft.Win32.Registry]::CurrentUser.CreateSubKey($subKey)
$key.SetValue("", "", [Microsoft.Win32.RegistryValueKind]::String)
$key.Close()

Write-Host "Enabled classic Windows context menu for current user."
Write-Host "Restarting Explorer..."

Get-Process explorer -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Process explorer.exe
