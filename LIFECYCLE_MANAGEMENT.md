# LIFECYCLE MANAGEMENT

## 1. Purpose
Define how the system is updated, versioned, maintained, and safely evolved over time.

## 2. Versioning Rules
- Semantic versioning recommended (MAJOR.MINOR.PATCH).
- MAJOR changes require full regression testing.
- MINOR changes require integration testing.
- PATCH changes require unit testing.

## 3. Update Workflow
1. Create feature branch.
2. Implement changes.
3. Run full test suite.
4. Update documentation.
5. Merge after review.
6. Deploy to paper mode only.

## 4. Deployment Safety Rules
- Live mode must never auto‑enable.
- All updates must be tested in paper mode first.
- Safety invariants must never be modified without explicit review.

## 5. Maintenance Expectations
- Weekly review of logs.
- Monthly review of risk parameters.
- Quarterly review of architecture.
- Annual review of safety invariants.

## 6. Deprecation Policy
- Deprecated components must be documented.
- Removal requires two release cycles.
- Replacement must be tested and validated.