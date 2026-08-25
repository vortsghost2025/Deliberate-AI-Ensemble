# Deliberate AI Ensemble

**Governance, architecture, and historical record for a long-running multi-agent AI experimentation project.**

This repository is the surviving governance-and-historical remnant of the original **Deliberate AI Ensemble**. It preserves the project's coordination rules, safety constraints, agent-role definitions, architecture notes, experimental records, and selected non-trading legacy modules.

It is also a **recovered/consolidated repository**. Several older projects and experiments were preserved here during earlier repository consolidation, so the tree is intentionally broader than a clean single-purpose package. The root README previously described one of those retained subprojects rather than the repository itself; this README corrects that mismatch.

## What this repository is

The Deliberate AI Ensemble explored how multiple AI agents can collaborate under explicit roles, coordination states, evidence requirements, vetoes, and safety boundaries rather than acting as an undifferentiated swarm.

The current repository is primarily a **governance and research archive**, not the active trading runtime it once contained.

### Preserved core

- `agents/ROLES.md` — ensemble role definitions
- `agents/COORDINATION.md` — coordination states and workflow rules
- `agents/SAFETY.md` — constitutional and integrity constraints
- `agents/base_agent.py` — base governance abstraction
- `agents/architecture/` — architecture and design records
- `agents/architecture/NAVIGATION_INDEX.md` — navigation index for the architecture archive
- `AGENTS.md` — current repository identity and mutation boundary

## Historical extraction

The repository previously contained live/paper trading agents and KuCoin integration. That trading logic was extracted into a separate repository, `vortsghost2025/kucoin-lane`.

Historical documentation that still references the old trading modules is retained as evidence of the project's evolution. Those references should not be interpreted as current runtime entry points.

## Other material retained here

Because this repository survived a broader consolidation/recovery period, it also contains selected non-trading and research material, including experimental agent systems, WE4FREE-related artifacts, simulation/game components, research notes, and other historical project remnants.

That mixture is part of the archive's history. When in doubt about current project identity, treat `AGENTS.md` as the authoritative repository-level guide.

## Research themes

Work preserved here touches several recurring themes:

- multi-agent coordination and role separation
- agent vetoes and distributed decision authority
- evidence-first reasoning and provenance
- persistent context and cross-session continuity
- failure detection and recovery
- runtime safety and constitutional constraints
- human/AI collaboration
- experimental work on persistent ensembles and emergent behavior

## Start here

For the current repository boundary and authoritative project identity, read:

1. [`AGENTS.md`](AGENTS.md)
2. [`agents/ROLES.md`](agents/ROLES.md)
3. [`agents/COORDINATION.md`](agents/COORDINATION.md)
4. [`agents/SAFETY.md`](agents/SAFETY.md)
5. [`agents/architecture/NAVIGATION_INDEX.md`](agents/architecture/NAVIGATION_INDEX.md)

Older files such as `00_START_HERE.md`, `.project-identity.txt`, and some historical project summaries may describe earlier phases of the repository and can be stale relative to the current boundary.

## Status

**Current role:** governance-and-historical archive with selected retained experimental modules.

**Active trading runtime:** moved out of this repository.

**Repository history:** intentionally preserved rather than rewritten into a falsely clean lineage.

---

This project is maintained as part of Sean David Ramsingh's public AI systems research and build-in-public work.