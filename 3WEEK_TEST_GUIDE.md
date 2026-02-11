# 3-Week Micro Test - Quick Start Guide

**Status:** Ready to launch  
**Date:** February 10, 2026  
**Fixes Applied:** Unconditional monitoring/auditing, MonitoringAgent resilience

---

## What This Test Validates

✅ **Real bot execution** (not test harness - lesson learned from Feb 7-9)  
✅ **Unconditional logging** (ALL decisions logged - rejections + executions)  
✅ **AuditorAgent validation** (post-cycle safety checks on all outcomes)  
✅ **Entry timing system** (baseline establishment → signal detection)  
✅ **Constitutional restraint** (risk management, downtrend protection)  
✅ **Crash recovery** (graceful handling of interruptions)  
✅ **Multi-day persistence** (prove 3-week runtime capability)

---

## Quick Start (Recommended: Background Mode)

### 1. Verify Configuration

```powershell
# Check paper trading is enabled
Get-Content config.py | Select-String "paper_trading"
# Should show: paper_trading=True
```

### 2. Start Bot

```powershell
# Background mode (survives terminal close, perfect for 3-week test)
.\start_continuous_background.ps1

# Or foreground mode (manual monitoring required)
.\start_continuous.ps1
```

### 3. Monitor Logs

```powershell
# Real-time log monitoring
Get-Content logs/trading_bot.log -Wait -Tail 20

# Event log (structured JSON)
Get-Content logs/events.jsonl -Wait -Tail 5

# Console output (background mode only)
Get-Content logs/console.log -Wait -Tail 20
```

### 4. Stop Bot (When Needed)

```powershell
# Graceful shutdown
.\stop_continuous.ps1
```

---

## Expected Behavior

### Cycle 1 (First Run)
```
[EntryTimingValidator] Baseline established at $XX.XX
[MarketAnalysisAgent] Entry timing DEFERRED: First cycle check
[RiskManagementAgent] Position rejected: First cycle check
[MonitoringAgent] Trade rejected by risk manager
[AuditorAgent] Audit passed (0 violations)
```
**Result:** Rejection logged and audited ✅

### Cycle 2-N (Subsequent Runs)
```
[DataFetchingAgent] Fetched SOL/USDT: $XX.XX
[EntryTimingValidator] Price change: +X.XX%
[MarketAnalysisAgent] Comparing to baseline $XX.XX
[RiskManagementAgent] Evaluating position approval...
```

**If price moved >0.1% from baseline:**
- Risk manager approves position
- ExecutionAgent executes trade (paper mode)
- MonitoringAgent logs execution
- AuditorAgent validates safety checks passed

**If no significant movement:**
- Risk manager rejects (waiting for better signal)
- MonitoringAgent logs rejection
- AuditorAgent validates partial workflow

---

## What Makes This Different from Feb 7-9 Failure

| Feb 7-9 Failure | This Test |
|-----------------|-----------|
| test_agents.py ran (test harness) | main.py runs (actual bot) |
| TEST/USDT@$100 (fake data) | SOL/USDT (real CoinGecko API) |
| Mock trades logged | Real decisions + real rejections |
| OrchestratorAgent never ran | Full 7-agent workflow |
| No MonitoringAgent on rejections | MonitoringAgent ALWAYS runs (finally block) |
| No AuditorAgent | AuditorAgent validates ALL outcomes |
| 9,474 fake entries | Real workflow traces with complete audit trail |

**Key difference:** We now log and audit **what we decided NOT to do**, not just what we did.

---

## Monitoring Checklist (Daily)

**Day 1-7 (Baseline Week):**
- [ ] Bot running (check `Get-Process python`)
- [ ] Logs growing (`Get-ChildItem logs/*.log`)
- [ ] No crashes (`Get-Content logs/trading_bot.log | Select-String "ERROR"`)
- [ ] Rejections logged (`Get-Content logs/events.jsonl | Select-String "rejected"`)
- [ ] Auditor running (`Get-Content logs/trading_bot.log | Select-String "AuditorAgent"`)

**Day 8-14 (Movement Week):**
- [ ] Entry timing decisions logged
- [ ] Trade approvals/rejections with reasoning
- [ ] If trade executed: Auditor validated safety layers
- [ ] No circuit breaker triggers

**Day 15-21 (Validation Week):**
- [ ] Performance metrics accurate
- [ ] Log files manageable size
- [ ] No memory leaks (check `Get-Process python | Select Memory`)
- [ ] Clean audit trail for all decisions

---

## Success Criteria

After 3 weeks, we prove:

✅ **Persistence:** Bot ran continuously without crashes  
✅ **Observability:** Every decision logged and audited  
✅ **Safety:** No silent failures (rejections visible)  
✅ **Restraint:** Risk management working as designed  
✅ **Audit:** AuditorAgent validated all cycles  
✅ **Recovery:** Graceful shutdown/restart capability  

**Deliverable:** Complete log archive proving constitutional framework operates correctly under extended runtime.

---

## Troubleshooting

**Bot won't start:**
```powershell
python main.py  # Test single cycle first
```

**Logs not updating:**
```powershell
Get-Process python  # Verify bot is running
```

**High memory usage:**
```powershell
Get-Process python | Format-List *  # Check memory stats
# Restart if >500MB: .\stop_continuous.ps1 then restart
```

**Need to check audit results:**
```powershell
Get-Content logs/events.jsonl | Select-String "AuditorAgent" | ConvertFrom-Json
```

---

## After 3 Weeks

**Archive logs:**
```powershell
Compress-Archive -Path logs/ -DestinationPath "3week_test_$(Get-Date -Format 'yyyy-MM-dd').zip"
```

**Analysis commands:**
```powershell
# Total cycles
(Get-Content logs/events.jsonl).Count

# Rejections vs executions
Get-Content logs/events.jsonl | Select-String "rejected" | Measure-Object
Get-Content logs/events.jsonl | Select-String "trade_executed.*true" | Measure-Object

# Audit violations (should be 0)
Get-Content logs/events.jsonl | Select-String "audit_passed.*false" | Measure-Object
```

**Share results:** logs/, performance summary, audit report → validation that framework works.

---

**Ready to start 3-week test.**  
**Command:** `.\start_continuous_background.ps1`
