# WORKFLOW STATE TRANSITION TABLE

## 1. Purpose
Provide a formal table of all valid workflow transitions, triggers, and blocking conditions.

## 2. Transition Table

| Current State      | Trigger                         | Next State         | Blocking Conditions                     |
|--------------------|----------------------------------|--------------------|------------------------------------------|
| INIT               | Config validated                 | FETCH_DATA         | Invalid config                           |
| FETCH_DATA         | Data valid                       | ANALYZE_MARKET     | Missing/stale data → ERROR               |
| ANALYZE_MARKET     | Regime safe                      | BACKTEST           | Bearish/undefined regime → HALTED        |
| BACKTEST           | Metrics valid                    | RISK_ASSESSMENT    | Invalid metrics → ERROR                  |
| RISK_ASSESSMENT    | Risk APPROVE                     | EXECUTION          | Risk VETO → HALTED                       |
| EXECUTION          | Execution success                | LOGGING            | Execution error → ERROR                  |
| LOGGING            | Log written                      | COMPLETE           | Write failure → ERROR                    |
| ERROR              | Circuit breaker engaged          | HALTED             | —                                        |
| HALTED             | Manual restart                   | INIT               | —                                        |

## 3. Invalid Transitions
- Any state → EXECUTION without approval.
- Any state → COMPLETE without logging.
- Any state → ANALYZE_MARKET without data.

## 4. Transition Philosophy
State transitions must be:
- Deterministic
- Safe
- Auditable
- Explicit