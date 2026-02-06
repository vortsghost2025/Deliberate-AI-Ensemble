# METRICS CATALOG

## 1. Purpose
Define all quantitative signals used to evaluate system health, performance, and stability.

## 2. Metric Categories

### System Metrics
- CPU usage
- Memory usage
- Disk I/O
- Latency (per agent + orchestrator)

### Workflow Metrics
- Cycle duration
- Agent response times
- State transition counts
- Error frequency

### Trading Metrics
- Signal frequency
- Win/loss ratio
- Drawdown
- Exposure
- Slippage

### Data Metrics
- Data freshness
- API response time
- Missing data rate
- Data integrity checks

## 3. Metric Requirements
- All metrics must be timestamped.
- Metrics must be structured (JSON).
- Metrics must be stored in a time‑series format.
- No secrets or PII may appear in metrics.
- Metrics must be retained for 90 days.
- Metric names must remain stable across versions.

## 4. Philosophy
If you cannot measure it, you cannot trust it.