# CIRCUIT BREAKER

## 1. Purpose
Prevent cascading failures by halting risky operations when thresholds are exceeded.

## 2. Trigger Conditions
- Too many API errors
- Too many invalid agent outputs
- Too many invariant violations
- Excessive latency
- Abnormal market conditions

## 3. Actions on Trigger
- Halt trading
- Halt signal generation
- Log event
- Enter safe state
- Require manual reset

## 4. Reset Rules
- Only after cooldown period
- Only after diagnostics pass
- Only after operator approval

## 5. Philosophy
When in doubt, stop — safety first, always.