# CHANGELOG STRUCTURE

## 1. Purpose
Provide a consistent format for recording system changes, ensuring traceability and historical clarity.

## 2. Version Format
Use semantic versioning:
- MAJOR.MINOR.PATCH

## 3. Entry Structure
Each entry must include:
- Version number
- Date
- Type of change
- Description
- Impact assessment
- Related documentation updates

## 4. Change Types
- Added: new features or components
- Changed: modifications to existing behavior
- Fixed: bug or issue resolution
- Removed: deprecated or retired components
- Security: safety or risk‑related updates

## 5. Example Entry
### v1.3.0 — 2026‑02‑04
**Added**
- New risk veto logic in RiskManagementAgent.

**Changed**
- Updated orchestrator state transitions for clarity.

**Fixed**
- Corrected timestamp formatting in logs.

**Impact**
- No breaking changes.  
- Safety improved.

## 6. Maintenance Rules
- Every change must be logged.
- No retroactive edits except corrections.
- Major changes require rationale.
- Changelog must remain chronological.

## 7. Philosophy
The changelog is the system’s memory.  
It preserves continuity across updates and refactors.