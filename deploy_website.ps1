# Deploy WE4Free Website to Hostinger via SSH/SCP
# Deploys both homepage and resources page

Write-Host "`n🚀 Deploying WE4Free to deliberateensemble.works..." -ForegroundColor Cyan

# SSH Details
$SSH_HOST = "88.223.85.164"
$SSH_PORT = "65002"
$SSH_USER = "u526066719"

# Load password from environment or .env file
$SSH_PASSWORD = $env:SSH_PASSWORD
if (-not $SSH_PASSWORD -and (Test-Path ".env")) {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^SSH_PASSWORD=(.+)$") {
            $SSH_PASSWORD = $matches[1]
        }
    }
}

# Deploy all website files (HTML, JS, JSON, icons) for offline PWA
Write-Host "📤 Uploading website files..." -ForegroundColor Yellow

if ($SSH_PASSWORD) {
    # Use password from environment (requires sshpass or plink)
    # For Windows, use plink from PuTTY if available, otherwise prompt
    $plink = Get-Command plink -ErrorAction SilentlyContinue
    if ($plink) {
        echo y | plink -P $SSH_PORT -pw $SSH_PASSWORD ${SSH_USER}@${SSH_HOST} "exit"
        # Upload HTML files
        pscp -P $SSH_PORT -pw $SSH_PASSWORD we4free_website/*.html ${SSH_USER}@${SSH_HOST}:public_html/
        # Upload JavaScript files
        pscp -P $SSH_PORT -pw $SSH_PASSWORD we4free_website/*.js ${SSH_USER}@${SSH_HOST}:public_html/
        # Upload JSON manifests
        pscp -P $SSH_PORT -pw $SSH_PASSWORD we4free_website/*.json ${SSH_USER}@${SSH_HOST}:public_html/
        # Upload .htaccess if exists
        if (Test-Path "we4free_website/.htaccess") {
            pscp -P $SSH_PORT -pw $SSH_PASSWORD we4free_website/.htaccess ${SSH_USER}@${SSH_HOST}:public_html/
        }
        # Upload icons directory
        if (Test-Path "we4free_website/icons") {
            pscp -r -P $SSH_PORT -pw $SSH_PASSWORD we4free_website/icons ${SSH_USER}@${SSH_HOST}:public_html/
        }
    } else {
        # Fall back to standard scp (will prompt for password)
        Write-Host "💡 Tip: Install PuTTY for password-less deployment" -ForegroundColor Yellow
        scp -P $SSH_PORT -r we4free_website/* ${SSH_USER}@${SSH_HOST}:~/public_html/
    }
} else {
    # No password in environment, use standard scp (upload all)
    scp -P $SSH_PORT -r we4free_website/* ${SSH_USER}@${SSH_HOST}:~/public_html/
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Deployment successful!" -ForegroundColor Green
    Write-Host "🌐 Homepage: https://deliberateensemble.works" -ForegroundColor Cyan
    Write-Host "💜 Resources: https://deliberateensemble.works/resources.html" -ForegroundColor Cyan
} else {
    Write-Host "❌ Deployment failed. Check SSH credentials." -ForegroundColor Red
}

Write-Host ""
