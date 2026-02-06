# SAFETY INVARIANTS — DETAILED SPECIFICATION

## 1. Purpose
Define the system’s non‑negotiable safety guarantees, including rationale, examples, and enforcement logic.

## 2. Invariant Categories
- Data safety
- Regime safety
- Risk safety
- Execution safety
- Structural safety

## 3. Data Safety Invariants
- No workflow continues with missing or stale data.
- DataFetcher must return complete, timestamped data.
- Rationale: Bad data → bad decisions.

## 4. Regime Safety Invariants
- Bearish or undefined regimes halt execution.
- MarketAnalysisAgent must classify regime explicitly.
- Rationale: Avoid trading in unsafe conditions.

## 5. Risk Safety Invariants
- Risk veto always overrides signals.
- Risk agent must justify decisions.
- Rationale: Risk is the final gatekeeper.

## 6. Execution Safety Invariants
- Paper mode is default.
- Live mode requires manual activation.
- ExecutionAgent must validate all parameters.
- Rationale: Prevent unintended trades.

## 7. Structural Safety Invariants
- Agents cannot modify global state.
- Orchestrator validates all messages.
- Circuit breaker halts on violations.
- Rationale: Maintain system integrity.

## 8. Enforcement Logic
- Orchestrator checks invariants at every state.
- Violations → ERROR or HALTED.
- All violations logged with context.

## 9. Examples
- Missing OHLCV → HALTED.
- Bearish regime → HALTED.
- Risk veto → HALTED.
- Execution error → ERROR → HALTED.

## 10. Philosophy
Safety is not a feature — it is the foundation.