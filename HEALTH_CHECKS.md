# HEALTH CHECKS

## 1. Purpose
Provide automated checks that verify the system is functioning correctly at every layer.

## 2. Health Check Types
### System Health
- CPU within threshold
- Memory within threshold
- Disk space available

### Agent Health
- Agent responds within timeout
- Output matches contract
- No invalid states

### Data Health
- API reachable
- Data fresh
- Data integrity valid

### Workflow Health
- State machine transitions valid
- No stuck states
- No repeated failures

## 3. Health Check Rules
- Run every cycle
- Fail fast
- Log all failures
- Trigger degradation if needed

## 4. Philosophy
Health checks prevent small issues from becoming big failures.