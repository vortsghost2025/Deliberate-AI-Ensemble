# SAFETY GUARDRAILS REFERENCE

## 1. Purpose
Document all safety mechanisms that protect the system from unsafe behavior.

## 2. Global Safety Guardrails
- Circuit breaker halts all trading on critical failure.
- Paper mode enforced unless explicitly overridden.
- Config validation required before workflow start.

## 3. Market Safety Guardrails
- Bearish regime triggers immediate pause.
- Missing or stale data triggers circuit breaker.
- Invalid market structure halts workflow.

## 4. Risk Safety Guardrails
- Position size capped at configured limit.
- Daily loss limit enforced.
- Hard veto respected at all times.

## 5. Execution Safety Guardrails
- Execution only allowed after risk approval.
- No live trades without explicit human confirmation.
- Execution failures trigger circuit breaker.

## 6. Agent Safety Guardrails
- Agents must fail safe.
- Agents must return structured messages.
- Agents must not bypass orchestrator authority.

## 7. Logging Safety Guardrails
- All decisions logged.
- All errors logged with context.
- Workflow summary required after each cycle.