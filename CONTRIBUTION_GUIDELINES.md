# CONTRIBUTION GUIDELINES

## 1. Purpose
Provide guidance for future contributors so changes align with the system’s philosophy, safety rules, and engineering standards.

## 2. Before Making a Change
- Read the design philosophy.
- Review safety invariants.
- Understand the orchestrator’s behavior.
- Check related specs and contracts.

## 3. Making a Change
- Work in a dedicated branch.
- Keep changes small and focused.
- Update documentation alongside code.
- Add or update tests for all new behavior.

## 4. Safety Requirements
- No change may weaken safety invariants.
- No change may introduce nondeterminism.
- No change may bypass validation.
- No change may reduce logging or transparency.

## 5. Code Expectations
- Follow code quality standards.
- Maintain modularity.
- Avoid side effects.
- Keep logic explicit.

## 6. Review Expectations
- Every change must be reviewed (self‑review if solo).
- Reviewer checks safety, clarity, and consistency.
- Reviewer ensures documentation is updated.

## 7. After Merging
- Monitor system behavior in paper mode.
- Review logs for anomalies.
- Update changelog.

## 8. Contribution Philosophy
Contributors are custodians of the system’s identity.  
Every change must preserve clarity, safety, and predictability.