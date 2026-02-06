# TESTING STANDARDS

## 1. Purpose
Define the testing expectations for all components, ensuring reliability, safety, and predictable behavior across the system.

## 2. Testing Categories
### Unit Tests
- Validate individual agent logic.
- Validate message formatting.
- Validate error handling.

### Integration Tests
- Validate orchestrator + agent interactions.
- Validate state transitions.
- Validate safety gates.

### Workflow Tests
- Simulate full trading cycles.
- Validate end‑to‑end behavior.
- Validate circuit breaker activation.

### Safety Tests
- Test bearish regime detection.
- Test missing data scenarios.
- Test risk veto enforcement.
- Test execution failures.

## 3. Required Test Coverage
- All agents must have unit tests.
- All orchestrator transitions must be tested.
- All safety guardrails must be tested.
- All message formats must be validated.

## 4. Test Data Requirements
- Use deterministic mock data.
- Include edge cases.
- Include failure scenarios.
- Include malformed messages.

## 5. Pass/Fail Criteria
- Any safety failure = automatic fail.
- Any malformed message = fail.
- Any unhandled exception = fail.

## 6. Continuous Testing Expectations
- Tests must run before deployment.
- Tests must run after configuration changes.
- Tests must run after agent updates.