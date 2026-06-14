$ErrorActionPreference = "Stop"
$body = @{
    host = "lihongyu5432-ux.github.io"
    key = "9832b4fe0ad7c615"
    keyLocation = "https://lihongyu5432-ux.github.io/BatchPrintKit/9832b4fe0ad7c615.txt"
    urlList = @(
        "https://lihongyu5432-ux.github.io/BatchPrintKit/",
        "https://lihongyu5432-ux.github.io/BatchPrintKit/llms.txt",
        "https://github.com/lihongyu5432-ux/BatchPrintKit",
        "https://github.com/lihongyu5432-ux/BatchPrintKit/releases/latest"
    )
} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Uri "https://api.indexnow.org/indexnow" -Method Post -Body $body -ContentType "application/json"
