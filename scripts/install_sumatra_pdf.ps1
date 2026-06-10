$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$toolsDir = Join-Path $repoRoot "tools\SumatraPDF"
$zipPath = Join-Path $env:TEMP "SumatraPDF-3.6.1-64.zip"
$downloadUrl = "https://www.sumatrapdfreader.org/dl/rel/3.6.1/SumatraPDF-3.6.1-64.zip"

New-Item -ItemType Directory -Force -Path $toolsDir | Out-Null
Write-Host "Downloading SumatraPDF portable..."
Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath

Write-Host "Extracting SumatraPDF..."
Expand-Archive -LiteralPath $zipPath -DestinationPath $toolsDir -Force

$exe = Get-ChildItem -Path $toolsDir -Recurse -Include "SumatraPDF.exe", "SumatraPDF-*-64.exe" | Select-Object -First 1
if (-not $exe) {
    throw "SumatraPDF.exe was not found after extraction."
}
Copy-Item -LiteralPath $exe.FullName -Destination (Join-Path $toolsDir "SumatraPDF.exe") -Force

Write-Host "Installed SumatraPDF portable:"
Write-Host (Join-Path $toolsDir "SumatraPDF.exe")
