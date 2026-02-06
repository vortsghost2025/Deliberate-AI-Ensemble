# EVOLUTION GUIDELINES

## 1. Purpose
Define how the system should evolve over time while preserving its identity, safety, and architectural integrity.

## 2. Evolution Principles
- Safety must never be compromised.
- Clarity must increase, not decrease.
- New features must align with system philosophy.
- Complexity must be justified, not accidental.

## 3. Acceptable Evolution Paths
- Adding new agents with clear responsibilities.
- Improving validation, safety, or logging.
- Enhancing observability or auditability.
- Refining state transitions for clarity.
- Expanding documentation or diagrams.

## 4. Discouraged Evolution Paths
- Adding features that increase ambiguity.
- Introducing nondeterministic behavior.
- Creating hidden state or implicit logic.
- Expanding scope beyond core mission.

## 5. Changes Requiring Strong Justification
- Modifying safety invariants.
- Altering orchestrator behavior.
- Changing state machine structure.
- Introducing new workflow paths.

## 6. Evolution Workflow
1. Propose change with rationale.
2. Evaluate using feature framework.
3. Update specs and diagrams.
4. Implement in a branch.
5. Test thoroughly.
6. Review and approve.
7. Update changelog.

## 7. Evolution Philosophy
The system should grow intentionally, not reactively.  
Every change must strengthen clarity, safety, and predictability.