# ORCHESTRATOR STATE MACHINE

## 1. Purpose
Define the workflow states, transitions, and safety gates that govern the orchestrator’s behavior.

## 2. State Definitions
### FETCH_DATA
- Entry: Workflow begins
- Exit: Data successfully fetched or circuit breaker triggered

### ANALYZE_MARKET
- Entry: Valid market data available
- Exit: Regime classified (bullish, neutral, bearish)

### BACKTEST_SIGNAL
- Entry: Market analysis complete
- Exit: Backtest metrics generated (non-blocking)

### RISK_ASSESSMENT
- Entry: Proposed trade exists
- Exit: Approved or vetoed

### EXECUTION
- Entry: Risk approved
- Exit: Trade executed (paper mode)

### MONITORING
- Entry: Execution complete or skipped
- Exit: Workflow summary logged

## 3. Allowed Transitions
- FETCH_DATA → ANALYZE_MARKET
- ANALYZE_MARKET → BACKTEST_SIGNAL
- BACKTEST_SIGNAL → RISK_ASSESSMENT
- RISK_ASSESSMENT → EXECUTION
- EXECUTION → MONITORING
- Any state → CIRCUIT_BREAKER (on failure)

## 4. Forbidden Transitions
- EXECUTION → RISK_ASSESSMENT
- ANALYZE_MARKET → EXECUTION (must pass risk)
- Any state → EXECUTION without approval

## 5. Safety Gates Per State
- FETCH_DATA: API success required
- ANALYZE_MARKET: Bearish regime halts workflow
- RISK_ASSESSMENT: Hard veto respected
- EXECUTION: Paper mode enforced

## 6. Failure Transitions
- Any error → CIRCUIT_BREAKER
- Missing data → CIRCUIT_BREAKER
- Malformed agent output → CIRCUIT_BREAKER