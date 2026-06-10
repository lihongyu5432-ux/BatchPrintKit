$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$msixPath = Join-Path $repoRoot "dist\SparsePackage\BatchPrintKit.ShellExtension.msix"
$subject = "CN=BatchPrintKit"

if (-not (Test-Path $msixPath)) {
    throw "Missing sparse package: $msixPath. Run scripts\build_sparse_package.ps1 first."
}

$signtool = Get-ChildItem "C:\Program Files (x86)\Windows Kits\10\bin" -Recurse -Filter signtool.exe |
    Where-Object { $_.FullName -like "*\x64\signtool.exe" } |
    Sort-Object FullName -Descending |
    Select-Object -First 1
if (-not $signtool) {
    throw "signtool.exe was not found. Install the Windows SDK."
}

$cert = Get-ChildItem Cert:\CurrentUser\My |
    Where-Object { $_.Subject -eq $subject -and $_.HasPrivateKey } |
    Sort-Object NotAfter -Descending |
    Select-Object -First 1

if (-not $cert) {
    $cert = New-SelfSignedCertificate `
        -Type CodeSigningCert `
        -Subject $subject `
        -CertStoreLocation Cert:\CurrentUser\My `
        -KeyAlgorithm RSA `
        -KeyLength 2048 `
        -HashAlgorithm SHA256 `
        -NotAfter (Get-Date).AddYears(3)
}

foreach ($storeSpec in @(
    @{ Name = "TrustedPeople"; Location = "CurrentUser" },
    @{ Name = "Root"; Location = "CurrentUser" },
    @{ Name = "Root"; Location = "LocalMachine" }
)) {
    $store = New-Object System.Security.Cryptography.X509Certificates.X509Store $storeSpec.Name, $storeSpec.Location
    $store.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::ReadWrite)
    $store.Add($cert)
    $store.Close()
}

& $signtool.FullName sign /fd SHA256 /sha1 $cert.Thumbprint $msixPath
if ($LASTEXITCODE -ne 0) {
    throw "signtool failed for $msixPath"
}

Write-Host "Signed sparse package with certificate thumbprint: $($cert.Thumbprint)"
