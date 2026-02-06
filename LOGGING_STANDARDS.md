# LOGGING STANDARDS

## 1. Purpose
Define consistent, comprehensive logging rules to ensure traceability, auditability, safety enforcement, and reliable debugging across the entire system.

---

## 2. Log Levels
### DEBUG
Internal details, validation steps, and low‑level agent behavior.

### INFO
Normal workflow events, state transitions, and successful operations.

### WARNING
Non‑blocking issues, recoverable anomalies, or unexpected but safe conditions.

### ERROR
Blocking issues that force the orchestrator into ERROR state.

### CRITICAL
Circuit breaker activation, safety invariant violations, or catastrophic failures.

---

## 3. Required Fields (All Logs)
- **Timestamp**
- **Component name** (Orchestrator, DataFetcher, etc.)
- **Workflow ID**
- **Workflow state**
- **Action performed**
- **Result** (success/failure)
- **Data summary** (inputs/outputs)
- **Safety flags** (if any)
- **Error message** (if applicable)

All fields must be present.  
No partial logs.  
No silent omissions.

---

## 4. Required Messages Per Workflow Stage

### **INIT**
- Configuration validation result  
- Environment readiness  
- Safety invariant pre‑check  

### **FETCH_DATA**
- API request start  
- API request result  
- Data completeness check  
- Data freshness check  
- Validation summary  

### **ANALYZE_MARKET**
- Regime classification  
- Trend/downtrend detection  
- Signal generation summary  
- Safety flags (if any)  

### **BACKTEST**
- Backtest start  
- Metrics summary (win rate, drawdown, etc.)  
- Validation of metrics  

### **RISK_ASSESSMENT**
- Proposed position  
- Risk metrics  
- Approval or veto  
- Rationale  

### **EXECUTION**
- Trade instruction  
- Execution mode (paper/live)  
- Execution result  
- Order metadata  

### **LOGGING**
- Audit record write attempt  
- Audit record success/failure  

### **MONITORING / COMPLETE**
- Final workflow summary  
- Safety gates triggered  
- Final outcome  

---

## 5. Error Log Format
All ERROR and CRITICAL logs must follow this structure:

- **Level:** ERROR or CRITICAL  
- **Message:** Human‑readable explanation  
- **Context:** Inputs, outputs, state, agent involved  
- **Action:** What was attempted  
- **Failure Point:** Where it broke  
- **Safety Response:** ERROR or HALTED  

Errors must always include enough context to reconstruct the event.

---

## 6. Workflow Summary Format
At the end of every workflow, a summary log must include:

- **Start time**  
- **End time**  
- **Total duration**  
- **States visited**  
- **Decisions made**  
- **Signals generated**  
- **Risk decision**  
- **Execution result**  
- **Safety gates triggered**  
- **Final outcome** (COMPLETE, ERROR, HALTED)  

This summary is mandatory.  
If it cannot be written, the workflow must be treated as ERROR → HALTED.

---

## 7. Logging Philosophy
- If it wasn’t logged, it didn’t happen.  
- If it didn’t happen, it cannot be trusted.  
- Logging is not optional — it is a safety mechanism.  
- Logs must be complete, structured, and human‑readable.  
- Logging failures are treated as critical system failures.

---

## 8. Determinism Requirements
- Logs must be deterministic for identical inputs.  
- No randomness in log structure or ordering.  
- Logs must allow full reconstruction of the workflow.

---

## 9. Compliance
All agents and orchestrator components must follow this standard.  
Any deviation is considered a safety violation.
