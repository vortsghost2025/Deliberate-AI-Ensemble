# WORKFLOW EXAMPLES

## 1. Purpose
Provide fully worked examples of complete workflows to illustrate system behavior.

## 2. Example: Normal Workflow
### Inputs
- Fresh market data
- Clear regime
- Valid signals
- Valid backtest metrics
- Risk APPROVE

### Transitions
INIT → FETCH_DATA → ANALYZE_MARKET → BACKTEST → RISK_ASSESSMENT → EXECUTION → LOGGING → COMPLETE

### Outcome
- Paper trade executed
- Full audit record written

---

## 3. Example: Bearish Regime
### Inputs
- Fresh data
- Regime = bearish

### Transitions
INIT → FETCH_DATA → ANALYZE_MARKET → HALTED

### Outcome
- No trade
- Rationale logged

---

## 4. Example: Risk Veto
### Inputs
- Valid signals
- Backtest metrics
- Risk = VETO

### Transitions
INIT → FETCH_DATA → ANALYZE_MARKET → BACKTEST → RISK_ASSESSMENT → HALTED

### Outcome
- No execution
- Veto rationale logged

---

## 5. Example: Execution Failure
### Inputs
- Approved signal
- ExecutionAgent returns error

### Transitions
INIT → FETCH_DATA → ANALYZE_MARKET → BACKTEST → RISK_ASSESSMENT → EXECUTION → ERROR → HALTED

### Outcome
- Circuit breaker activated
- Error logged

---

## 6. Example: Missing Data
### Inputs
- DataFetcher returns incomplete dataset

### Transitions
INIT → FETCH_DATA → ERROR → HALTED

### Outcome
- Workflow stops immediately
- Error logged