# AGENT INTERACTION PROTOCOL

## 1. Purpose
Define how agents communicate with the orchestrator and with each other indirectly through standardized, validated message formats.  
Ensure all agent interactions remain safe, predictable, and aligned with system architecture.

## 2. Communication Model
- Agents never communicate directly with one another.
- All communication flows through the orchestrator.
- The orchestrator is the single source of truth for workflow state.
- Agents operate independently and statelessly unless explicitly designed otherwise.
- Messages must follow the standardized format.

## 3. Message Requirements

### Required Fields
- agent
- action
- timestamp
- success
- data
- error

### Optional Fields
- warnings
- metrics
- safety_flags

## 4. Interaction Rules
- Orchestrator requests → Agent executes → Agent returns standardized message.
- Agents must not request data from other agents.
- Agents must not assume workflow order or global state.
- Agents must not modify configuration or shared resources.
- Orchestrator validates every message before continuing workflow.

## 5. Validation Rules
- Orchestrator validates message structure and required fields.
- Missing fields trigger circuit breaker.
- Malformed or inconsistent data halts workflow.
- Unexpected agent output results in safe failure.
- Orchestrator must confirm:
  - message schema
  - data types
  - safety flags
  - success/failure consistency

## 6. Safety Rules
- Agents must not escalate privileges.
- Agents must not bypass risk or execution gates.
- Agents must not generate trade instructions unless explicitly designated.
- Agents must not modify global state or configuration.
- Agents must fail safe on internal errors.

## 7. Failure Behavior
- Agent returns `success: False` with error details.
- Orchestrator activates circuit breaker.
- Workflow terminates safely.
- Error logged with full context for audit trail.