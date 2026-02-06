# ALERTING RULES

## 1. Purpose
Define when and how the system should raise alerts to signal abnormal, unsafe, or degraded conditions. Alerts ensure the operator is informed, not overwhelmed, and always able to take meaningful action.

---

## 2. Alert Categories

### Safety Alerts
- Invariant violations
- Circuit breaker activations
- Unexpected agent outputs
- Unsafe state transitions

### Performance Alerts
- Slow workflows
- Slow agent responses
- Repeated timeouts
- Latency above threshold

### Stability Alerts
- Repeated errors
- Repeated halts
- High failure rates
- State machine stuck

---

## 3. Alert Severity Levels

### Critical
- Safety invariant violation
- Circuit breaker triggered
- Execution failure
- Data corruption
- State machine in invalid state

### High
- Repeated agent errors
- Workflow slowdown beyond threshold
- Data freshness failure

### Medium
- Elevated error rate
- Minor validation failures
- Intermittent API issues

### Low
- Non‑critical anomalies
- Minor performance drift

---

## 4. Alert Requirements
- Alerts must be actionable.
- Alerts must include context (metric, threshold, timestamp, agent).
- Alerts must be rate‑limited to avoid noise.
- Alerts must be logged in the audit system.
- All alert thresholds must be documented in MONITORING_POLICY.md.
- Alerts must never fire silently or without traceability.

---

## 5. Philosophy
Alerts are not alarms — they are structured signals that guide attention to where it matters most. The goal is clarity and action, not panic.