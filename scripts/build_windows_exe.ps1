$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

python -m pip install pyinstaller
pyinstaller --noconfirm --windowed --name BatchPrintKit --paths src src\batch_print_kit\__main_gui__.py

$sumatra = Join-Path $repoRoot "tools\SumatraPDF\SumatraPDF.exe"
if (Test-Path $sumatra) {
    $dest = Join-Path $repoRoot "dist\BatchPrintKit\tools"
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Copy-Item -LiteralPath $sumatra -Destination (Join-Path $dest "SumatraPDF.exe") -Force
}

Write-Host "Built dist\BatchPrintKit\BatchPrintKit.exe"
