# SAFETY CASES

## 1. Purpose
Demonstrate how safety invariants prevent catastrophic outcomes through concrete examples.

## 2. Safety Case: Missing Data
### Hazard
Trading on incomplete data.

### Invariant
Data must be complete and fresh.

### Protection
Orchestrator halts workflow at FETCH_DATA.

---

## 3. Safety Case: Bearish Regime
### Hazard
Entering trades in unsafe market conditions.

### Invariant
Bearish regimes halt execution.

### Protection
Orchestrator transitions → HALTED immediately.

---

## 4. Safety Case: Risk Veto
### Hazard
Executing trades with unacceptable risk.

### Invariant
Risk veto overrides all signals.

### Protection
Execution is blocked.

---

## 5. Safety Case: Execution Failure
### Hazard
Partial or incorrect order placement.

### Invariant
Execution errors trigger circuit breaker.

### Protection
Workflow stops before further damage.

---

## 6. Safety Case: Unexpected Agent Output
### Hazard
Corrupted or unpredictable behavior.

### Invariant
All agent messages must match schema.

### Protection
Orchestrator transitions → ERROR → HALTED.

---

## 7. Safety Case: Logging Failure
### Hazard
Loss of audit trail.

### Invariant
Logging must succeed before completion.

### Protection
Workflow transitions → ERROR.