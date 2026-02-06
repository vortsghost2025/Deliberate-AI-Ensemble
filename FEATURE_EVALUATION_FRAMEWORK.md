# FEATURE EVALUATION FRAMEWORK

## 1. Purpose
Provide a structured method for evaluating new features before they are added to the system.

## 2. Evaluation Criteria
### Safety Impact
- Does the feature affect safety invariants?
- Does it introduce new failure modes?
- Does it increase or reduce risk?

### Clarity Impact
- Does it make the system easier to understand?
- Does it introduce ambiguity?

### Architectural Fit
- Does it align with design philosophy?
- Does it respect modular boundaries?
- Does it require orchestrator changes?

### Scope Alignment
- Does it fit within system boundaries?
- Does it drift toward out‑of‑scope areas?

### Maintenance Cost
- Does it increase complexity?
- Does it require new documentation?
- Does it require new tests?

## 3. Decision Outcomes
- **Approve**: Feature aligns with all criteria.
- **Revise**: Feature needs adjustments.
- **Reject**: Feature conflicts with philosophy or safety.

## 4. Required Artifacts
- Feature rationale
- Updated specs
- Updated diagrams
- Test plan

## 5. Philosophy
Features must earn their place.  
If a feature does not strengthen the system, it does not belong.