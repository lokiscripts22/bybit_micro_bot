# scan_secrets.ps1
# Scans all files in the repo for potential secrets (keys, tokens, passwords)

$patterns = @(
    "API_KEY",
    "API_SECRET",
    "SECRET",
    "TOKEN",
    "PASSWORD",
    "PRIVATE_KEY",
    "ACCESS_KEY",
    "SECRET_KEY"
)

Write-Host "Scanning repository for sensitive patterns..." -ForegroundColor Cyan

# Get all files recursively
$files = Get-ChildItem -Path . -Recurse -File

foreach ($pattern in $patterns) {
    Write-Host "`nSearching for pattern: $pattern" -ForegroundColor Yellow
    $found = $false

    foreach ($file in $files) {
        $matches = Select-String -Path $file.FullName -Pattern $pattern -ErrorAction SilentlyContinue
        if ($matches) {
            $found = $true
            foreach ($match in $matches) {
                Write-Host "Found in $($match.Path) on line $($match.LineNumber): $($match.Line.Trim())" -ForegroundColor Red
            }
        }
    }

    if (-not $found) {
        Write-Host "No matches found for $pattern." -ForegroundColor Green
    }
}

Write-Host "`nScan complete." -ForegroundColor Cyan
