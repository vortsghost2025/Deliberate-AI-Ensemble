# INCIDENT RESPONSE GUIDE

## 1. Purpose
Define what to do when something goes wrong: errors, circuit breaker events, or unexpected behavior.

## 2. Incident Types
- Data incidents (missing, stale, invalid).
- Logic incidents (unexpected decisions, wrong state).
- Safety incidents (guardrail not triggered when expected).
- Execution incidents (failed or incorrect execution).

## 3. Immediate Response Steps
1. Stop the system if behavior is unsafe.
2. Confirm circuit breaker status.
3. Preserve logs and audit trails.
4. Capture configuration used at the time.

## 4. Triage Checklist
- What state was the workflow in?
- Which agent or component was active?
- What inputs were being processed?
- Were any safety flags raised?

## 5. Investigation Process
- Review logs and audit trail for the incident window.
- Reproduce the issue in a controlled environment if possible.
- Identify root cause (data, logic, config, external).

## 6. Resolution Steps
- Implement fix in a branch.
- Add or update tests to cover the incident.
- Update documentation if needed.
- Run full test suite.
- Redeploy in paper mode first.

## 7. Post‑Incident Review
- Summarize what happened and why.
- Record what was changed.
- Confirm that safeguards now cover this scenario.