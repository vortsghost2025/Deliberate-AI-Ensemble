# Stop Continuous Trading Bot
# Gracefully stops background bot process

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Trading Bot - Stop Continuous Mode" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Check for PID file
if (Test-Path "bot.pid") {
    $pid = Get-Content "bot.pid" -Raw
    $pid = $pid.Trim()
    
    Write-Host "[INFO] Found PID file: $pid" -ForegroundColor Yellow
    
    try {
        $process = Get-Process -Id $pid -ErrorAction Stop
        Write-Host "[FOUND] Bot process running (PID: $pid)" -ForegroundColor Green
        
        $confirm = Read-Host "Stop bot gracefully? (yes/no)"
        if ($confirm -ne "yes") {
            Write-Host "[ABORTED] User cancelled stop." -ForegroundColor Yellow
            exit 0
        }
        
        Write-Host "[STOPPING] Sending Ctrl+C signal..." -ForegroundColor Yellow
        Stop-Process -Id $pid -Force
        Start-Sleep -Seconds 2
        
        if (-not (Get-Process -Id $pid -ErrorAction SilentlyContinue)) {
            Write-Host "[SUCCESS] Bot stopped gracefully." -ForegroundColor Green
            Remove-Item "bot.pid" -ErrorAction SilentlyContinue
            Remove-Item "temp_startup.ps1" -ErrorAction SilentlyContinue
        } else {
            Write-Host "[WARNING] Process still running. Force kill? (yes/no)" -ForegroundColor Yellow
            $forceKill = Read-Host
            if ($forceKill -eq "yes") {
                Stop-Process -Id $pid -Force
                Write-Host "[SUCCESS] Process force killed." -ForegroundColor Green
            }
        }
    } catch {
        Write-Host "[ERROR] PID $pid not found. Process may have already stopped." -ForegroundColor Red
        Remove-Item "bot.pid" -ErrorAction SilentlyContinue
    }
} else {
    Write-Host "[INFO] No PID file found. Searching for running Python processes..." -ForegroundColor Yellow
    
    $pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
    
    if ($pythonProcesses) {
        Write-Host "`nRunning Python processes:" -ForegroundColor Cyan
        $pythonProcesses | Format-Table Id, CPU, PM, StartTime -AutoSize
        
        $pidToKill = Read-Host "`nEnter PID to stop (or 'cancel')"
        if ($pidToKill -ne "cancel" -and $pidToKill -match '^\d+$') {
            Stop-Process -Id $pidToKill -Force
            Write-Host "[SUCCESS] Process $pidToKill stopped." -ForegroundColor Green
        } else {
            Write-Host "[ABORTED] No process stopped." -ForegroundColor Yellow
        }
    } else {
        Write-Host "[INFO] No Python processes found. Bot may already be stopped." -ForegroundColor Yellow
    }
}

Write-Host "`n[DONE] Stop script complete.`n" -ForegroundColor Cyan
