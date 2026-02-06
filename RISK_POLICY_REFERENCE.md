# RISK POLICY REFERENCE

## 1. Purpose
Define the system’s risk philosophy, limits, and non‑negotiable safety constraints that govern all decision‑making.

## 2. Core Risk Principles
- Safety overrides opportunity.
- No decision is better than an unsafe decision.
- All risk assessments must be explicit, not implied.
- Uncertainty increases required caution.

## 3. Risk Limits
- No trades executed without valid, fresh data.
- No trades executed in bearish or undefined regimes.
- No trades executed if any safety flag is raised.
- No trades executed if risk agent returns a veto.

## 4. Required Risk Checks
- Market regime classification.
- Data completeness and freshness.
- Volatility and anomaly detection.
- Signal consistency.
- Configuration validity.

## 5. Prohibited Conditions
- Missing or stale data.
- Conflicting signals.
- Unexpected agent outputs.
- Any unhandled exception.
- Any deviation from safety invariants.

## 6. Risk Escalation Rules
- Any violation triggers circuit breaker.
- Workflow halts immediately.
- Error logged with full context.
- System remains halted until manually restarted.

## 7. Philosophy Summary
The system prioritizes capital preservation, stability, and predictability.  
Risk is never assumed — it is always justified.