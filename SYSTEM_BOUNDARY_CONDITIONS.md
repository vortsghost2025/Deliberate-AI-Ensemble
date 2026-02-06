# SYSTEM BOUNDARY CONDITIONS

## 1. Purpose
Define what the system can do, must not do, and will never attempt.  
These boundaries protect safety, clarity, and long‑term maintainability.

## 2. Explicit Capabilities
- Fetch and validate market data.
- Analyze market regimes.
- Generate signals.
- Perform backtests.
- Assess risk.
- Execute paper trades.
- Log and audit all actions.

## 3. Explicit Non‑Capabilities
- No live trading without manual activation.
- No self‑modifying configuration.
- No autonomous parameter tuning.
- No external communication beyond APIs.
- No direct agent‑to‑agent communication.

## 4. Hard Prohibitions
- No execution in unsafe regimes.
- No execution with missing data.
- No bypassing safety invariants.
- No silent failures.
- No unlogged decisions.

## 5. Out‑of‑Scope Areas
- Portfolio optimization.
- Multi‑asset allocation.
- High‑frequency execution.
- Automated strategy generation.
- Machine‑learning‑driven decision making.

## 6. Boundary Enforcement
- Orchestrator validates all actions.
- Circuit breaker halts violations.
- Logs capture all boundary checks.
- Violations require manual review.

## 7. Boundary Philosophy
Boundaries create safety, clarity, and predictability.  
They ensure the system remains stable as it evolves.