# REVIEW AND APPROVAL PROCESS

## 1. Purpose
Define how changes are proposed, reviewed, and approved to protect system integrity and safety.

## 2. Change Types
- Minor: small refactors, non‑breaking tweaks.
- Moderate: new features, behavior changes.
- Major: architecture changes, safety logic changes.

## 3. Change Workflow
1. Create a branch for the change.
2. Implement changes with tests.
3. Update relevant documentation.
4. Open a review (self‑review if solo).
5. Run full test suite.
6. Merge only after review and passing tests.

## 4. Review Checklist
- Code is readable and consistent.
- Safety invariants are respected.
- Error handling is explicit.
- Logging is appropriate and not excessive.
- Documentation is updated.
- Tests are present and meaningful.

## 5. Approval Rules
- No change bypasses tests.
- No change weakens safety without explicit justification.
- Major changes require a written rationale in the repo.

## 6. Post‑Merge Expectations
- Monitor behavior in paper mode.
- Review logs for anomalies.
- Roll back if unexpected behavior appears.