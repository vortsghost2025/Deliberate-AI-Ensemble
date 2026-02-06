# FAILURE MODES

## 1. Purpose
Define all known failure scenarios and how the system should respond to each.

## 2. Categories of Failure
### External Failures
- API downtime
- Network instability
- Rate limits
- Corrupted data

### Internal Failures
- Agent crash
- Orchestrator crash
- Invalid agent output
- State machine deadlock

### Operational Failures
- Misconfiguration
- Missing secrets
- Disk full
- Logging failure

## 3. Required Responses
- Detect failure
- Log failure
- Enter safe state
- Attempt recovery
- Notify operator if needed

## 4. Safe State Rules
- No trading
- No signal generation
- No external calls
- Only diagnostics allowed

## 5. Philosophy
A system is defined not by how it runs — but by how it fails.