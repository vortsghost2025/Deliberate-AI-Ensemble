# Start Trading Bot in Continuous Mode
# For 3-week micro test with full logging and monitoring

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Multi-Agent Trading Bot - Continuous Mode Startup" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Verify we're in correct directory
if (-not (Test-Path "main.py")) {
    Write-Host "[ERROR] main.py not found. Run this script from workspace root." -ForegroundColor Red
    exit 1
}

# Verify config exists
if (-not (Test-Path "config.py")) {
    Write-Host "[ERROR] config.py not found. Copy config_template.py to config.py first." -ForegroundColor Red
    exit 1
}

# Check Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found. Install Python 3.10+ first." -ForegroundColor Red
    exit 1
}

# Display configuration
Write-Host "`nConfiguration:" -ForegroundColor Yellow
Write-Host "  Mode: CONTINUOUS (infinite loop)" -ForegroundColor White
Write-Host "  Cycle Interval: 300 seconds (5 minutes)" -ForegroundColor White
Write-Host "  Trading Pairs: SOL/USDT" -ForegroundColor White
Write-Host "  Paper Trading: Check config.py" -ForegroundColor White
Write-Host "  Logs: logs/trading_bot.log, logs/events.jsonl`n" -ForegroundColor White

# Confirm startup
$confirm = Read-Host "Start continuous mode? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "[ABORTED] User cancelled startup." -ForegroundColor Yellow
    exit 0
}

# Set environment variables for continuous mode
$env:CONTINUOUS_MODE = "true"
$env:CYCLE_INTERVAL_SECONDS = "300"

Write-Host "`n[STARTING] Bot will run until manually stopped (Ctrl+C)...`n" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop gracefully.`n" -ForegroundColor Cyan

# Start the bot
try {
    python main.py
} catch {
    Write-Host "`n[ERROR] Bot crashed: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n[STOPPED] Bot shutdown complete." -ForegroundColor Yellow
