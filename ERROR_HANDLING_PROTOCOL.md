# ERROR HANDLING PROTOCOL

## 1. Purpose
Define consistent rules for detecting, reporting, and responding to errors across all components.

## 2. Error Categories
- Data errors (missing, invalid, stale)
- Agent errors (malformed output, failure to execute)
- Orchestrator errors (unexpected state)
- External errors (API downtime)
- Safety errors (risk violation)

## 3. Agent Error Behavior
- Must return `success: False`
- Must include `error` field with human-readable message
- Must never raise uncaught exceptions
- Must fail safe (no execution instructions)

## 4. Orchestrator Error Behavior
- Immediately activate circuit breaker
- Log full error context
- Return safe failure message
- Halt workflow

## 5. Circuit Breaker Triggers
- DataFetcher returns `success: False`
- MarketAnalysis detects invalid regime
- RiskManager returns malformed approval data
- ExecutionAgent fails to validate instruction
- Any unhandled exception

## 6. Logging Requirements
- Timestamp
- Component name
- Error category
- Error message
- Workflow state at time of failure

## 7. Recovery Rules
- Manual reset required
- Must not auto-resume
- Must preserve error logs for audit