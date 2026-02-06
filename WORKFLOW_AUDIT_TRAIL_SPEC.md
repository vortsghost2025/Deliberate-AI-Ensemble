# WORKFLOW AUDIT TRAIL SPECIFICATION

## 1. Purpose
Define the structure and requirements for recording a complete audit trail of each workflow cycle.

## 2. Required Audit Fields
- Timestamp
- Workflow state
- Agent name
- Action performed
- Inputs received
- Outputs produced
- Safety flags triggered
- Errors encountered
- Final outcome

## 3. Audit Trail Structure
### Entry Format
- State entered
- Agent executed
- Data summary
- Decision summary
- Safety checks applied

### Exit Format
- State completed
- Result (success/failure)
- Next state

## 4. Required Events to Log
- Data fetch start and result
- Market analysis classification
- Backtest metrics
- Risk approval or veto
- Execution attempt and result
- Circuit breaker activation
- Workflow completion summary

## 5. Retention Requirements
- Audit logs must persist across sessions.
- Logs must not be overwritten.
- Logs must be timestamped and immutable.

## 6. Review Requirements
- Human review required after circuit breaker events.
- Weekly review recommended for paper trading cycles.