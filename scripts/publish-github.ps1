# Create public GitHub repo and push (requires: gh auth login)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI not found. Install: winget install GitHub.cli"
}

$status = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Not logged in to GitHub. Run: gh auth login" -ForegroundColor Yellow
    exit 1
}

$repo = "cloudflare-security-lab"
$exists = gh repo view $repo 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Repo $repo already exists — pushing to origin"
    git push -u origin main
} else {
    gh repo create $repo --public --source=. --remote=origin --push `
        --description "Cloudflare WAF security lab - advanced rules, Python automation, and edge security patterns"
}

Write-Host ""
Write-Host "Done. View repo:" -ForegroundColor Green
gh repo view --web
