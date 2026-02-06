# INTEGRATION TEST PLAN

## 1. Purpose
Define how to test interactions between the orchestrator and agents to ensure correct workflow behavior.

## 2. Integration Scenarios
### Normal Workflow
- Valid data → valid signals → valid metrics → APPROVE → EXECUTION → LOGGING.

### Bearish Regime
- Regime = bearish → HALTED.

### Risk Veto
- Risk returns VETO → HALTED.

### Execution Failure
- Execution error → ERROR → HALTED.

### Missing Data
- Incomplete dataset → ERROR → HALTED.

## 3. State Transition Tests
- Validate every transition in the state machine.
- Confirm blocking conditions.
- Confirm error routing.

## 4. Safety Enforcement Tests
- Invariant violations.
- Schema violations.
- Unexpected agent outputs.

## 5. Logging Tests
- Ensure full audit record is produced.
- Ensure logs contain all required fields.

## 6. Success Criteria
- All transitions deterministic.
- All safety checks enforced.
- No unexpected states.

## 7. Philosophy
Integration tests ensure the system behaves as a unified whole.