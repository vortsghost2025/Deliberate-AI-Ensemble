# Start Trading Bot in Continuous Mode (Background)
# Runs as detached process for long-term testing (days/weeks)

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Trading Bot - Background Continuous Mode Startup" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Verify we're in correct directory
if (-not (Test-Path "main.py")) {
    Write-Host "[ERROR] main.py not found. Run this script from workspace root." -ForegroundColor Red
    exit 1
}

# Check if bot already running
$existingProcess = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.MainWindowTitle -match "trading" -or $_.CommandLine -match "main.py"
}

if ($existingProcess) {
    Write-Host "[WARNING] Python process already running (PID: $($existingProcess.Id))" -ForegroundColor Yellow
    $confirm = Read-Host "Kill existing and restart? (yes/no)"
    if ($confirm -eq "yes") {
        Stop-Process -Id $existingProcess.Id -Force
        Start-Sleep -Seconds 2
        Write-Host "[OK] Existing process terminated." -ForegroundColor Green
    } else {
        Write-Host "[ABORTED] Use 'stop_continuous.ps1' to stop running bot." -ForegroundColor Yellow
        exit 0
    }
}

# Display configuration
Write-Host "`nConfiguration:" -ForegroundColor Yellow
Write-Host "  Mode: CONTINUOUS BACKGROUND" -ForegroundColor White
Write-Host "  Cycle Interval: 300 seconds (5 minutes)" -ForegroundColor White
Write-Host "  Process: Detached (survives terminal close)" -ForegroundColor White
Write-Host "  Logs: logs/trading_bot.log, logs/events.jsonl" -ForegroundColor White
Write-Host "  Stop: Use stop_continuous.ps1 or Ctrl+C`n" -ForegroundColor White

# Confirm startup
$confirm = Read-Host "Start background continuous mode? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "[ABORTED] User cancelled startup." -ForegroundColor Yellow
    exit 0
}

# Create startup script for background process
$startupScript = @"
`$env:CONTINUOUS_MODE = 'true'
`$env:CYCLE_INTERVAL_SECONDS = '300'
Set-Location '$PWD'
python main.py *>&1 | Tee-Object -FilePath 'logs/console.log' -Append
"@

$scriptPath = Join-Path $PWD "temp_startup.ps1"
$startupScript | Out-File -FilePath $scriptPath -Encoding UTF8

# Start detached process
Write-Host "[STARTING] Launching bot in background...`n" -ForegroundColor Green

$process = Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy Bypass", "-File `"$scriptPath`"" -PassThru -WindowStyle Minimized

Start-Sleep -Seconds 3

# Verify process started
if (Get-Process -Id $process.Id -ErrorAction SilentlyContinue) {
    Write-Host "[SUCCESS] Bot running in background (PID: $($process.Id))" -ForegroundColor Green
    Write-Host "  Monitor: tail -f logs/trading_bot.log" -ForegroundColor Cyan
    Write-Host "  Console: tail -f logs/console.log" -ForegroundColor Cyan
    Write-Host "  Stop: .\stop_continuous.ps1`n" -ForegroundColor Cyan
    
    # Save PID for stop script
    $process.Id | Out-File -FilePath "bot.pid" -Encoding UTF8
} else {
    Write-Host "[ERROR] Failed to start background process." -ForegroundColor Red
    Remove-Item $scriptPath -ErrorAction SilentlyContinue
    exit 1
}

Write-Host "[TIP] Bot will continue running even if you close this window.`n" -ForegroundColor Yellow
