# Deploy WE4Free Website to Hostinger via SSH/SCP
# Deploys both homepage and resources page

Write-Host "`n🚀 Deploying WE4Free to deliberateensemble.works..." -ForegroundColor Cyan

# SSH Details
$HOST = "88.223.85.164"
$PORT = "65002"
$USER = "u526066719"

# Deploy all HTML files from we4free_website folder
Write-Host "📤 Uploading website files..." -ForegroundColor Yellow
scp -P $PORT we4free_website/*.html ${USER}@${HOST}:~/public_html/

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Deployment successful!" -ForegroundColor Green
    Write-Host "🌐 Homepage: https://deliberateensemble.works" -ForegroundColor Cyan
    Write-Host "💜 Resources: https://deliberateensemble.works/resources.html" -ForegroundColor Cyan
} else {
    Write-Host "❌ Deployment failed. Check SSH credentials." -ForegroundColor Red
}

Write-Host ""
