# DEGRADATION STRATEGIES

## 1. Purpose
Ensure the system continues operating safely at reduced capability when full functionality is unavailable.

## 2. Degradation Levels
### Level 0 — Full Operation
All components healthy.

### Level 1 — Partial Data Loss
Fallback to cached data.
Disable high‑frequency strategies.

### Level 2 — Analysis Degraded
Disable advanced agents.
Fallback to baseline logic.

### Level 3 — Execution Degraded
Disable live trading.
Enable paper‑only mode.

### Level 4 — Safe State
No trading.
Diagnostics only.

## 3. Transition Rules
- Always degrade downward
- Never auto‑upgrade
- Manual approval required to restore full capability

## 4. Philosophy
A safe partial system is better than a dangerous full system.