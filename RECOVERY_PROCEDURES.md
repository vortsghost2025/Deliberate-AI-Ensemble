# RECOVERY PROCEDURES

## 1. Purpose
See FAILURE_MODES.md for the list of failure scenarios and CIRCUIT_BREAKER.md for automated halt conditions.
Define step‑by‑step instructions for safely recovering from errors, halts, or unexpected states.

## 2. Recovery After ERROR State
### Steps
1. Review error logs.
2. Identify root cause.
3. Confirm circuit breaker activation.
4. Fix underlying issue.
5. Restart system manually.

### Expected Outcome
- System returns to INIT.
- No residual state remains.

---

## 3. Recovery After HALTED State
### Steps
1. Review rationale for halt.
2. Confirm safety invariant triggered.
3. Validate configuration.
4. Restart workflow manually.

### Expected Outcome
- System resumes safely.

---

## 4. Recovery After Agent Failure
### Steps
1. Identify failing agent.
2. Review agent logs.
3. Validate agent contract compliance.
4. Patch or replace agent.
5. Run test workflows.

### Expected Outcome
- Agent returns to stable behavior.

---

## 5. Recovery After API Outage
### Steps
1. Confirm external API status.
2. Validate data freshness.
3. Restart workflow.
4. Monitor first few cycles.

### Expected Outcome
- Normal data flow restored.

---

## 6. Recovery Philosophy
Recovery is not about rushing back online — it’s about returning to a known‑safe state with full clarity.