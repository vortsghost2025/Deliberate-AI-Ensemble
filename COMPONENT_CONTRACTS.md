# COMPONENT CONTRACTS

## 1. Purpose
Define the input/output guarantees, side effects, and safety constraints for each system component.

---

## 2. Agent Contracts
### Inputs
- Structured data from orchestrator.

### Outputs
- Standardized message dict.

### Side Effects
- Logging only.

### Safety Guarantees
- Must not execute trades.
- Must not bypass orchestrator.

---

## 3. Orchestrator Contract
### Inputs
- Agent outputs.
- Market data.
- Configuration.

### Outputs
- Workflow state messages.
- Execution instructions (validated only).

### Side Effects
- Logging.
- Circuit breaker activation.

### Safety Guarantees
- Enforces all safety gates.
- Halts on malformed or unsafe instructions.

---

## 4. Risk Manager Contract
### Inputs
- Proposed trade details.

### Outputs
- `position_approved: True/False`
- Rejection reason.

### Safety Guarantees
- Final veto authority before execution.

---

## 5. Executor Contract
### Inputs
- Validated trade instructions.

### Outputs
- Execution result message.

### Safety Guarantees
- Defaults to paper mode.
- Enforces session and position limits.

---

## 6. Data Feeds Contract
### Inputs
- External market data.

### Outputs
- Validated, structured data.

### Safety Guarantees
- Must fail safe.