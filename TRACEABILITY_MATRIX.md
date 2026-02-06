# TRACEABILITY MATRIX

## 1. Purpose
Map requirements, invariants, components, and tests to ensure full end‑to‑end visibility.

## 2. Traceability Links
- Requirement → Component
- Component → Invariant
- Invariant → Test
- Test → Logs
- Logs → Metrics

## 3. Matrix Structure

| Requirement | Component | Invariant | Test | Log Event | Metric |
|------------|-----------|-----------|------|-----------|--------|
| R1         | DataFetcher | I1      | T1   | E1        | M1     |
| R2         | RiskAgent   | I3      | T7   | E4        | M9     |
| R3         | Execution   | I5      | T12  | E9        | M14    |

## 4. Maintenance Rules
- Update matrix with every change
- No orphaned requirements
- No untested invariants
- No unlogged critical events

## 5. Philosophy
A system you cannot trace is a system you cannot trust.