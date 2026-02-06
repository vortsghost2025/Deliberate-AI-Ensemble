# VERSIONING POLICY

## 1. Purpose
Define how versions are assigned, incremented, and communicated to ensure clarity and compatibility.

## 2. Version Format
Semantic versioning:
**MAJOR.MINOR.PATCH**

### MAJOR
Breaking changes:
- State machine modifications
- Contract changes
- Safety invariant changes

### MINOR
New features that do not break compatibility:
- New agents
- New metrics
- New diagrams
- New validation rules

### PATCH
Bug fixes and small improvements:
- Logging fixes
- Documentation updates
- Minor validation adjustments

## 3. Versioning Rules
- Every release must increment a version number.
- No skipping versions.
- No silent breaking changes.
- Documentation must match version.

## 4. Version Tags
- `stable`
- `experimental`
- `deprecated`

## 5. Philosophy
Versions tell the story of the system’s evolution — clearly, honestly, and predictably.