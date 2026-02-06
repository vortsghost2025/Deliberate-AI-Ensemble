# DEPRECATION POLICY

## 1. Purpose
Define how components are safely retired, replaced, or removed without breaking the system.

## 2. Deprecation Principles
- Deprecation must be intentional.
- Safety must not be reduced.
- Documentation must remain accurate.
- Backward compatibility must be considered.

## 3. Deprecation Workflow
1. Identify component to deprecate.
2. Provide rationale for removal.
3. Mark component as deprecated in documentation.
4. Introduce replacement component (if applicable).
5. Update orchestrator and contracts.
6. Remove deprecated component in a later version.
7. Update changelog.

## 4. Required Documentation
- Deprecation rationale
- Replacement details
- Migration notes
- Updated diagrams
- Updated specs

## 5. Deprecation Criteria
- Component no longer aligns with philosophy.
- Component duplicates functionality.
- Component increases risk or ambiguity.
- Component is replaced by a safer or clearer design.

## 6. Philosophy
Deprecation is not destruction — it is refinement.  
The system becomes stronger by removing what no longer serves it.