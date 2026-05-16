# Deliberate-AI-Ensemble — Agent Instructions

## Project Identity

This is the **Deliberate-AI-Ensemble** — a governance-only remnant of the original multi-agent trading system. All trading logic has been extracted to `kucoin-lane` (Lane 4).

## Current State

- **Trading agents**: DELETED (extracted to `vortsghost2025/kucoin-lane`)
- **Governance layer**: PRESERVED — `agents/ROLES.md`, `agents/COORDINATION.md`, `agents/SAFETY.md`
- **Architecture docs**: PRESERVED — `agents/architecture/` (52 docs + `NAVIGATION_INDEX.md`)
- **Base governance class**: `agents/base_agent.py` (`BaseAgent`, `AgentStatus`)
- **Config**: `config.py` (env-var-only, hardcoded creds scrubbed)

## Mutation Boundary

- **Allowed mutation root:** `S:\Deliberate-AI-Ensemble`
- **Neighboring repos are read-only references** unless the user explicitly authorizes cross-repo work

## What Belongs Here

- Governance documents (roles, coordination, safety)
- Architecture documentation and design records
- Base agent abstractions used by governance layer
- Non-trading Python modules (federation game, narrator, diplomacy, etc.)

## What Does NOT Belong Here

- Trading execution logic → `kucoin-lane`
- KuCoin API integration → `kucoin-lane`
- Risk management for trading → `kucoin-lane`
- Market analysis / backtesting → `kucoin-lane`
- Hardcoded API credentials → NOWHERE (use env vars)

## Stale References

~20 markdown docs still contain file-path links to deleted agent modules (executor.py, orchestrator.py, risk_manager.py, etc.). These are non-runtime references and were intentionally left as historical records.

## Key Files

| Path | Purpose |
|------|---------|
| `agents/ROLES.md` | Ensemble role definitions (Strategist/Engineer/Validator/Archivist) |
| `agents/COORDINATION.md` | 10 coordination states for ensemble workflow |
| `agents/SAFETY.md` | Constitutional enforcement, integrity verification |
| `agents/base_agent.py` | BaseAgent + AgentStatus (governance layer only) |
| `agents/__init__.py` | Exports BaseAgent, AgentStatus |
| `agents/architecture/NAVIGATION_INDEX.md` | Index of 52 architecture documents |
| `config.py` | Env-var-only configuration |

## OUTPUT_PROVENANCE

Any agent-generated markdown in this repo should include provenance headers per `GLOBAL_GOVERNANCE.md`.
