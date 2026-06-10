$ErrorActionPreference = "Stop"

$sendTo = [Environment]::GetFolderPath("SendTo")
$shortcutPath = Join-Path $sendTo "Batch Print Kit.lnk"
if (Test-Path $shortcutPath) {
    Remove-Item -LiteralPath $shortcutPath -Force
    Write-Host "Removed $shortcutPath"
} else {
    Write-Host "Shortcut was not installed: $shortcutPath"
}
