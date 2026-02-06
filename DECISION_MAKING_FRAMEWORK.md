# DECISION MAKING FRAMEWORK

## 1. Purpose
Define how the system makes decisions, resolves conflicts, and prioritizes safety across all workflows.

## 2. Decision Hierarchy
1. Safety invariants
2. Risk policies
3. Data validity
4. Agent outputs
5. Optimization or opportunity

Safety always wins.

## 3. Decision Inputs
- Market data
- Agent outputs
- Configuration parameters
- Safety flags
- Historical context (audit trail)

## 4. Conflict Resolution
- If two agents disagree → orchestrator defers to safety.
- If data conflicts with signals → halt workflow.
- If configuration conflicts with safety → safety wins.
- If uncertainty exists → choose the safest path.

## 5. Required Decision Checks
- Is the data valid?
- Is the regime safe?
- Are all agents consistent?
- Are safety invariants satisfied?
- Is execution allowed?

## 6. Decision Outputs
- Approve workflow continuation.
- Halt workflow.
- Trigger circuit breaker.
- Log decision rationale.

## 7. Guiding Philosophy
Decisions must be:
- Explainable
- Deterministic
- Safe
- Auditable
- Consistent