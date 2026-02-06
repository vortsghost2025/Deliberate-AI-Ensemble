# SCENARIO PLAYBOOKS

## 1. Purpose
Provide concrete, real‑world scenarios and define exactly how the system must respond to each one.

## 2. Scenario: Missing Market Data
### Trigger
- DataFetcher returns incomplete or empty data.

### Expected Behavior
- Orchestrator transitions → ERROR.
- Circuit breaker activates.
- Workflow halts.
- Error logged with full context.

### Rationale
Trading without valid data is unsafe.

---

## 3. Scenario: Stale Market Data
### Trigger
- Data timestamp older than allowed threshold.

### Expected Behavior
- Orchestrator rejects data.
- Transition → ERROR.
- Circuit breaker activates.

### Rationale
Stale data leads to invalid decisions.

---

## 4. Scenario: Bearish Market Regime
### Trigger
- MarketAnalysisAgent classifies regime as bearish.

### Expected Behavior
- Orchestrator transitions → HALTED.
- No backtest, no risk assessment, no execution.
- Log rationale.

### Rationale
Avoid trading in unsafe conditions.

---

## 5. Scenario: Conflicting Signals
### Trigger
- MarketAnalysisAgent outputs inconsistent or contradictory signals.

### Expected Behavior
- Orchestrator transitions → ERROR.
- Circuit breaker activates.

### Rationale
Conflicting signals indicate agent malfunction or bad data.

---

## 6. Scenario: Risk Veto
### Trigger
- RiskManagementAgent returns VETO.

### Expected Behavior
- Orchestrator transitions → HALTED.
- No execution allowed.
- Log veto rationale.

### Rationale
Risk agent is the final gatekeeper.

---

## 7. Scenario: Execution Failure
### Trigger
- ExecutionAgent returns error.

### Expected Behavior
- Orchestrator transitions → ERROR.
- Circuit breaker activates.
- Log full execution context.

### Rationale
Execution errors must be treated as critical.

---

## 8. Scenario: Logging Failure
### Trigger
- LoggingAgent cannot write audit record.

### Expected Behavior
- Orchestrator transitions → ERROR.
- Circuit breaker activates.

### Rationale
If it’s not logged, it didn’t happen.

---

## 9. Scenario: Unexpected Agent Output
### Trigger
- Missing fields, wrong types, malformed structure.

### Expected Behavior
- Orchestrator transitions → ERROR.
- Circuit breaker activates.

### Rationale
Unexpected output breaks determinism.

---

## 10. Scenario: API Outage
### Trigger
- DataFetcher or ExecutionAgent cannot reach API.

### Expected Behavior
- Orchestrator transitions → ERROR.
- Circuit breaker activates.

### Rationale
External instability must not propagate into the system.