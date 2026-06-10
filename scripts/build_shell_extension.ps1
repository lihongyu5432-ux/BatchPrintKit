$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $repoRoot "native\shell_extension\BatchPrintShellExtension.cpp"
$outDir = Join-Path $repoRoot "dist\ShellExtension"
$objDir = Join-Path $repoRoot "build\ShellExtension"
$dllPath = Join-Path $outDir "BatchPrintShellExtension.dll"

if (-not (Test-Path $source)) {
    throw "Missing source: $source"
}

$vswhere = Join-Path ${env:ProgramFiles(x86)} "Microsoft Visual Studio\Installer\vswhere.exe"
if (-not (Test-Path $vswhere)) {
    throw "Visual Studio Build Tools were not found. Install the C++ build tools, then rerun this script."
}

$installPath = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
if (-not $installPath) {
    throw "Visual Studio C++ tools were not found. Install the Desktop development with C++ workload."
}

$vcVars = Join-Path $installPath "VC\Auxiliary\Build\vcvars64.bat"
if (-not (Test-Path $vcVars)) {
    throw "Cannot find vcvars64.bat: $vcVars"
}

New-Item -ItemType Directory -Force -Path $outDir | Out-Null
New-Item -ItemType Directory -Force -Path $objDir | Out-Null
$objPath = Join-Path $objDir "BatchPrintShellExtension.obj"
$cmd = "`"$vcVars`" && cl /nologo /utf-8 /EHsc /LD /std:c++17 /W4 /DUNICODE /D_UNICODE `"$source`" /Fo:`"$objPath`" /Fe:`"$dllPath`" ole32.lib shell32.lib advapi32.lib"
cmd.exe /c $cmd

if (-not (Test-Path $dllPath)) {
    throw "Build did not produce $dllPath"
}

Write-Host "Built $dllPath"
