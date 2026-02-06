# ORCHESTRATOR BEHAVIOR SPECIFICATION

## 1. Purpose
Define the orchestrator’s exact behavior in every state, transition, and failure mode to ensure deterministic, safe, and auditable workflows.

## 2. Core Responsibilities
- Manage workflow state.
- Validate all agent inputs and outputs.
- Enforce safety invariants.
- Route tasks to agents.
- Handle errors and activate circuit breaker.
- Produce complete audit trails.

## 3. Workflow States
- INIT
- FETCH_DATA
- ANALYZE_MARKET
- BACKTEST
- RISK_ASSESSMENT
- EXECUTION
- LOGGING
- COMPLETE
- ERROR
- HALTED

## 4. State Behaviors
### INIT
- Validate configuration.
- Initialize logging.
- Transition → FETCH_DATA.

### FETCH_DATA
- Request fresh market data.
- Validate completeness and freshness.
- If invalid → ERROR.
- If valid → ANALYZE_MARKET.

### ANALYZE_MARKET
- Request regime classification and signals.
- Validate structure and safety flags.
- If bearish → HALTED.
- If valid → BACKTEST.

### BACKTEST
- Request optional backtest.
- Validate metrics.
- Transition → RISK_ASSESSMENT.

### RISK_ASSESSMENT
- Request risk evaluation.
- If veto → HALTED.
- If approved → EXECUTION.

### EXECUTION
- Execute trade (paper mode).
- Validate execution result.
- Transition → LOGGING.

### LOGGING
- Write full audit record.
- Transition → COMPLETE.

### COMPLETE
- End workflow safely.

### ERROR
- Log error context.
- Activate circuit breaker.
- Transition → HALTED.

### HALTED
- System remains stopped until manual restart.

## 5. Message Validation Rules
- All agent messages must include required fields.
- Missing or malformed fields → ERROR.
- Safety flags → HALTED.
- Unexpected agent output → ERROR.

## 6. Circuit Breaker Behavior
- Triggered by any safety violation.
- Stops workflow immediately.
- Requires manual reset.

## 7. Determinism Requirements
- Same inputs → same outputs.
- No hidden state.
- No nondeterministic behavior.

## 8. Philosophy
The orchestrator is the system’s brain and guardian.  
It must always choose the safest possible path.