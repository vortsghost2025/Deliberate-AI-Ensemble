# DEPLOYMENT NOTES

## 1. Purpose
Provide guidelines for safely deploying the system in different environments.

## 2. Environment Requirements
- Python environment with required dependencies.
- Valid API keys (paper mode only by default).
- Stable network connection.
- Logging directory with write permissions.

## 3. Deployment Steps
1. Pull latest version from repository.
2. Validate configuration schema.
3. Run full test suite.
4. Start system in paper mode.
5. Monitor logs for anomalies.
6. Confirm stable behavior before continuing.

## 4. Live Mode Activation (Manual Only)
- Must be explicitly enabled by a human.
- Requires valid API keys.
- Requires confirmation of risk parameters.
- Requires review of safety invariants.

## 5. Post‑Deployment Monitoring
- Monitor logs for errors.
- Confirm circuit breaker readiness.
- Validate agent outputs.
- Review workflow summaries.

## 6. Rollback Procedure
- Stop system immediately.
- Revert to previous stable version.
- Investigate logs.
- Re‑run tests before redeploying.