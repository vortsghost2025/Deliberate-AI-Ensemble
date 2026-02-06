# SECURITY MODEL

## 1. Purpose
Define the system’s security philosophy, trust boundaries, and protection mechanisms.

## 2. Security Principles
- Least privilege
- Explicit trust boundaries
- No implicit permissions
- Deterministic behavior
- No shared mutable state
- Fail‑safe defaults

## 3. Trust Boundaries
- Orchestrator: fully trusted
- Agents: partially trusted
- External APIs: untrusted
- User input: untrusted

## 4. Allowed Interactions
- Agents → Orchestrator (allowed)
- Orchestrator → Agents (allowed)
- Agent → Agent (forbidden)
- Agent → External API (allowed only for DataFetcher)
- Orchestrator → External API (forbidden)

## 5. Security Controls
- Schema validation
- Invariant enforcement
- Circuit breaker
- Strict permissions matrix
- Secrets isolation

## 6. Philosophy
Security is not a feature — it is the boundary that defines what the system is allowed to become.