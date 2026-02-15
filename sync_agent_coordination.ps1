# Sync AGENT_COORDINATION to web-accessible location
# Run this after Desktop/VS Code Claude updates coordination files

Write-Host "🔄 Syncing agent coordination files..." -ForegroundColor Cyan

$source = "c:\workspace\AGENT_COORDINATION"
$dest = "c:\workspace\we4free_website\agent_coordination"

# Create destination if it doesn't exist
if (-not (Test-Path $dest)) {
    New-Item -ItemType Directory -Path $dest -Force | Out-Null
}

# Copy all files
Copy-Item -Path "$source\*" -Destination "$dest\" -Force

Write-Host "✅ Sync complete! Browser Claude can now see latest updates." -ForegroundColor Green
Write-Host "📍 Access at: http://localhost:8080/agent_coordination/" -ForegroundColor Cyan
