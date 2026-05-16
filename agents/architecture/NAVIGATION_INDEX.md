# Architecture Documents — Navigation Index

> OUTPUT_PROVENANCE:
> agent: kilo
> lane: archivist
> target: architecture-doc-index
> generated_at: 2026-05-16T06:15:00Z
> session_id: ws3c

## OBSERVABILITY_DOMAIN
documentation-organization

## NEXT_SAFE_ACTION
Use this index to locate relevant architecture docs by category or tag

---

## Category Index

### System Design & Identity
| # | File | Focus |
|---|------|-------|
| 00 | `00_SKELETON.md` | Document skeleton/template |
| 01 | `01_SYSTEM_OVERVIEW.md` | High-level system architecture |
| 02 | `02_SYSTEM_IDENTITY.md` | System identity and purpose |
| 03 | `03_CORE_PHILOSOPHY.md` | Design philosophy and principles |

### Safety, Risk & Security
| # | File | Focus |
|---|------|-------|
| 04 | `04_SAFETY_ARCHITECTURE.md` | Safety systems and fail-safes |
| 05 | `05_RISK_ARCHITECTURE.md` | Risk management framework |
| 06 | `06_SECURITY_ARCHITECTURE.md` | Security model and controls |
| 27 | `27_SECURITY_ARCHITECTURE.md` | Security architecture (extended) |
| 28 | `28_ACCESS_ARCHITECTURE.md` | Access control and authorization |

### Boundaries & Integration
| # | File | Focus |
|---|------|-------|
| 07 | `07_SYSTEM_BOUNDARIES.md` | System scope and boundaries |
| 08 | `08_INTEGRATION_ARCHITECTURE.md` | External integration patterns |
| 13 | `13_BOUNDARY_ARCHITECTURE.md` | Boundary enforcement |
| 48 | `48_SYSTEM_BOUNDARIES_ARCHITECTURE.md` | System boundary architecture |

### Reliability & Resilience
| # | File | Focus |
|---|------|-------|
| 09 | `09_RELIABILITY_AND_RESILIENCE.md` | Reliability and resilience overview |
| 15 | `15_RESILIENCE_ARCHITECTURE.md` | Resilience patterns |
| 41 | `41_RELIABILITY_ARCHITECTURE.md` | Reliability architecture (extended) |
| 42 | `42_FAULT_TOLERANCE_ARCHITECTURE.md` | Fault tolerance design |
| 43 | `43_FAILSAFE_ARCHITECTURE.md` | Fail-safe mechanisms |
| 19 | `19_RECOVERY_ARCHITECTURE.md` | Recovery procedures |

### Governance & Audit
| # | File | Focus |
|---|------|-------|
| 10 | `10_OPERATIONAL_GOVERNANCE.md` | Operational governance model |
| 14 | `14_INTEGRITY_ARCHITECTURE.md` | Data integrity guarantees |
| 16 | `16_AUDIT_ARCHITECTURE.md` | Audit trail and verification |
| 20 | `20_VALIDATION_ARCHITECTURE.md` | Validation framework |
| 22 | `22_CONSISTENCY_ARCHITECTURE.md` | Consistency guarantees |
| 50 | `50_SYSTEM_GUARANTEES_ARCHITECTURE.md` | System-level guarantees |

### Observability & Monitoring
| # | File | Focus |
|---|------|-------|
| 12 | `12_MONITORING_ARCHITECTURE.md` | Monitoring infrastructure |
| 21 | `21_OBSERVABILITY_ARCHITECTURE.md` | Observability model |
| 44 | `44_OBSERVATION_LIMITS_ARCHITECTURE.md` | Observation boundary limits |

### Dependencies & Updates
| # | File | Focus |
|---|------|-------|
| 17 | `17_DEPENDENCY_ARCHITECTURE.md` | Dependency management |
| 18 | `18_UPDATE_ARCHITECTURE.md` | Update and upgrade patterns |
| 25 | `25_VERSIONING_ARCHITECTURE.md` | Version management |
| 26 | `26_ROLLBACK_ARCHITECTURE.md` | Rollback procedures |
| 31 | `31_COMPATIBILITY_ARCHITECTURE.md` | Compatibility guarantees |

### Deployment & Environment
| # | File | Focus |
|---|------|-------|
| 24 | `24_DEPLOYMENT_ARCHITECTURE.md` | Deployment model |
| 35 | `35_ENVIRONMENT_ARCHITECTURE.md` | Environment management |
| 36 | `36_ISOLATION_ARCHITECTURE.md` | Isolation boundaries |

### Interfaces & Extensions
| # | File | Focus |
|---|------|-------|
| 29 | `29_INTERFACE_ARCHITECTURE.md` | Interface contracts |
| 30 | `30_EXTENSION_ARCHITECTURE.md` | Extension points |

### Performance & Scaling
| # | File | Focus |
|---|------|-------|
| 32 | `32_SCALING_ARCHITECTURE.md` | Scaling model |
| 38 | `38_LATENCY_ARCHITECTURE.md` | Latency requirements |
| 39 | `39_THROUGHPUT_ARCHITECTURE.md` | Throughput design |
| 40 | `40_PERFORMANCE_ARCHITECTURE.md` | Performance architecture |

### State & Resources
| # | File | Focus |
|---|------|-------|
| 33 | `33_STATE_ARCHITECTURE.md` | State management |
| 34 | `34_RESOURCE_ARCHITECTURE.md` | Resource management |

### Constraints & Limits
| # | File | Focus |
|---|------|-------|
| 37 | `37_SEPARATION_OF_CONCERNS_ARCHITECTURE.md` | Separation of concerns |
| 45 | `45_EXECUTION_LIMITS_ARCHITECTURE.md` | Execution boundary limits |
| 46 | `46_BEHAVIORAL_CONSTRAINTS_ARCHITECTURE.md` | Behavioral constraints |
| 47 | `47_ALIGNMENT_LIMITS_ARCHITECTURE.md` | Alignment constraints |
| 49 | `49_SYSTEM_LIMITS_ARCHITECTURE.md` | System-wide limits |

### Supplementary
| # | File | Focus |
|---|------|-------|
| 11 | `11_APPENDICES.md` | Appendices and reference data |
| 23 | `23_INTERACTION_ARCHITECTURE.md` | Interaction patterns |
| — | `RECOVERY_SESSION_NOTES.md` | Recovery session documentation |

---

## Tag Cloud

| Tag | Documents |
|-----|----------|
| `safety` | 04, 05, 43 |
| `security` | 06, 27, 28 |
| `boundary` | 07, 13, 48 |
| `reliability` | 09, 15, 41, 42, 43 |
| `governance` | 10, 14, 16, 50 |
| `observability` | 12, 21, 44 |
| `performance` | 38, 39, 40 |
| `constraints` | 45, 46, 47, 49 |
| `deployment` | 24, 35, 36 |
| `state` | 19, 33 |
| `versioning` | 25, 26, 31 |
| `integration` | 08, 29, 30 |
| `scaling` | 32, 34, 40 |

---

## Quick Lookup

- **"How does the system fail safely?"** → 04, 43
- **"How is risk managed?"** → 05
- **"What are the system boundaries?"** → 07, 13, 48
- **"How is governance enforced?"** → 10, 14, 16, 50
- **"How does recovery work?"** → 19, 42
- **"What can I observe?"** → 12, 21, 44
- **"How are dependencies managed?"** → 17, 18
- **"How does deployment work?"** → 24, 35
- **"What are the system limits?"** → 49, 50
- **"How is performance optimized?"** → 38, 39, 40

---

_Total: 51 numbered documents + 1 supplementary = 52 files_
