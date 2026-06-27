# Bootstrap GH_TOKEN from Windows Git Credential Manager for headless gh/API use.
# Usage: . .\scripts\Use-GitHubTokenFromGcm.ps1
#        gh api user
#        gh repo view vamdevz/cloudflare-security-lab

$ErrorActionPreference = 'Stop'

$input = "protocol=https`nhost=github.com`n`n"
$cred = $input | git credential fill 2>$null
if (-not $cred) {
    Write-Error "No GitHub credentials in Windows Credential Manager. Run: gh auth login --web"
}

$token = ($cred | Where-Object { $_ -match '^password=' }) -replace '^password=',''
if (-not $token) {
    Write-Error "Credential fill returned no token."
}

$env:GH_TOKEN = $token
Write-Host "GH_TOKEN set from Git Credential Manager (session only)." -ForegroundColor Green
