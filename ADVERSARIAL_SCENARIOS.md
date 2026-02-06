# ADVERSARIAL SCENARIOS

## 1. Purpose
Define how the system must behave when inputs are intentionally wrong, misleading, or hostile.

## 2. Adversarial Input Types
### Malicious Data Structures
- Extra fields.
- Missing required fields.
- Incorrect types.
- Nested unexpected objects.

### Deceptive Market Data
- Out‑of‑order timestamps.
- Duplicate entries.
- Impossible values.

### Agent Misbehavior
- Returning contradictory outputs.
- Returning incomplete messages.
- Returning malformed structures.

### Timing Attacks
- Rapid repeated calls.
- Delayed responses.
- Out‑of‑sequence messages.

## 3. Expected System Behavior
- Reject malformed inputs.
- Transition → ERROR or HALTED.
- Never attempt execution.
- Log full context.
- Maintain determinism.

## 4. Protection Mechanisms
- Strict schema validation.
- Safety invariants.
- Circuit breaker.
- Orchestrator‑only coordination.
- No agent‑to‑agent communication.

## 5. Philosophy
Adversarial scenarios reveal weaknesses normal operation never shows.