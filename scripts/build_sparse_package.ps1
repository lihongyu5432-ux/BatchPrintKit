$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$manifestSource = Join-Path $repoRoot "packaging\sparse\AppxManifest.xml"
$shellDll = Join-Path $repoRoot "dist\ShellExtension\BatchPrintShellExtension.dll"
$packageRoot = Join-Path $repoRoot "build\SparsePackage"
$assetsDir = Join-Path $packageRoot "Assets"
$outputDir = Join-Path $repoRoot "dist\SparsePackage"
$msixPath = Join-Path $outputDir "BatchPrintKit.ShellExtension.msix"

if (-not (Test-Path $manifestSource)) {
    throw "Missing sparse manifest: $manifestSource"
}
if (-not (Test-Path $shellDll)) {
    throw "Missing shell extension DLL: $shellDll. Run scripts\build_shell_extension.ps1 first."
}

$makeAppx = Get-ChildItem "C:\Program Files (x86)\Windows Kits\10\bin" -Recurse -Filter makeappx.exe |
    Where-Object { $_.FullName -like "*\x64\makeappx.exe" } |
    Sort-Object FullName -Descending |
    Select-Object -First 1
if (-not $makeAppx) {
    throw "makeappx.exe was not found. Install the Windows SDK."
}

Remove-Item -LiteralPath $packageRoot -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $assetsDir | Out-Null
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
Copy-Item -LiteralPath $manifestSource -Destination (Join-Path $packageRoot "AppxManifest.xml") -Force
Copy-Item -LiteralPath $shellDll -Destination (Join-Path $packageRoot "BatchPrintShellExtension.dll") -Force

Add-Type -AssemblyName System.Drawing
function New-Logo {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][int]$Size
    )
    $bitmap = New-Object System.Drawing.Bitmap $Size, $Size
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.Clear([System.Drawing.Color]::FromArgb(32, 113, 202))
    $font = New-Object System.Drawing.Font "Segoe UI", ([Math]::Max(12, [int]($Size / 3))), ([System.Drawing.FontStyle]::Bold)
    $brush = [System.Drawing.Brushes]::White
    $format = New-Object System.Drawing.StringFormat
    $format.Alignment = [System.Drawing.StringAlignment]::Center
    $format.LineAlignment = [System.Drawing.StringAlignment]::Center
    $graphics.DrawString("BP", $font, $brush, (New-Object System.Drawing.RectangleF 0, 0, $Size, $Size), $format)
    $bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()
}

New-Logo -Path (Join-Path $assetsDir "Square44x44Logo.png") -Size 44
New-Logo -Path (Join-Path $assetsDir "Square150x150Logo.png") -Size 150

Remove-Item -LiteralPath $msixPath -Force -ErrorAction SilentlyContinue
& $makeAppx.FullName pack /d $packageRoot /p $msixPath /nv
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $msixPath)) {
    throw "makeappx failed to produce $msixPath"
}

Write-Host "Built sparse package: $msixPath"
