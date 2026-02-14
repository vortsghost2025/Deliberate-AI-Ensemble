# AI Ensemble Documentation

**WE Framework Operational Architecture**

---

## Quick Reference

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[ROLES.md](./ROLES.md)** | Defines the 4 agent roles and their boundaries | Start here - understand who does what |
| **[COORDINATION.md](./COORDINATION.md)** | Handoff protocols and state machine | When adding workflows or debugging coordination |
| **[SAFETY.md](./SAFETY.md)** | Fallback rules, escalation, integrity checks | When implementing safety features or handling failures |

---

## The 4 Roles

### 🧠 Strategist (Eyes + Brain)
- **Agent:** Claude (conversational)
- **Does:** Interprets screenshots, provides architectural guidance, makes decisions
- **Boundaries:** No file access, no execution

### ✋ Engineer (Hands + Brain)
- **Agent:** Claude Code or code-execution agent
- **Does:** Edits code, runs commands, implements changes
- **Boundaries:** No visual interpretation, follows Strategist design

### 📊 Validator (Sensors)
- **Agent:** DevTools, Lighthouse, test harness
- **Does:** Tests, measures performance, verifies behavior
- **Boundaries:** No code changes, only observes and reports

### 💾 Archivist (Memory)
- **Agent:** Git + checkpoint system
- **Does:** Stores state, enables recovery, maintains audit trail
- **Boundaries:** No reasoning, purely storage and retrieval

---

## Core Insights

**The ensemble was built before it was named.**

You already operate this way:
1. Screenshot → Strategist analyzes → Engineer implements → Archivist records → Validator confirms
2. This workflow has run 100+ times successfully
3. These docs formalize what already exists

**Artifacts, not conversations.**

Agents exchange concrete artifacts:
- Screenshots (PNG)
- Instructions (text)
- Code changes (git diffs)
- Test results (structured data)
- Checkpoints (JSON)

**Constitutional symmetry preserved.**

Every role enforces the same constitutional rules:
- Zero-profit
- Offensive-first accessibility
- Integrity verification
- Never give up on each other

---

## Quick Start

### Adding a New Agent

1. Define role in `ROLES.md` (capabilities, boundaries, artifacts)
2. Add to coordination flow in `COORDINATION.md` (when does it act?)
3. Define safety rules in `SAFETY.md` (what if it fails?)
4. Test integration with existing ensemble

### Debugging Ensemble Issues

1. Check `COORDINATION.md` state machine - which state is stuck?
2. Check `SAFETY.md` escalation rules - was proper fallback triggered?
3. Check `ROLES.md` boundaries - is an agent exceeding its role?
4. Check Archivist logs - what's the audit trail?

### Implementing a New Feature

1. Strategist: Design the feature (architecture, constraints)
2. Engineer: Implement according to design
3. Archivist: Commit changes with co-authorship
4. Validator: Test against requirements
5. Strategist: Confirm with user

---

## Theoretical Foundation

This operational structure instantiates the mathematical framework from Papers A and B:

| Operational | Categorical | Physical |
|-------------|-------------|----------|
| Strategist | Primary morphism generator | Decision operator |
| Engineer | Functor (state transformer) | Evolution operator |
| Validator | Verification operator | Measurement operator |
| Archivist | Identity morphism | Time-evolution generator |

**Key result:** 4-role ensemble preserves constitutional symmetry across abstraction layers, guaranteeing safety conservation.

---

## Next Steps

**Immediate:**
- ✅ Document existing roles (complete)
- ✅ Document coordination protocol (complete)
- ✅ Document safety rules (complete)
- ⏳ Add ensemble state to checkpoint schema

**Short-term:**
- Add external validator agent (Kimi or GPT-4)
- Automate Validator role (Playwright + Lighthouse CI)
- Build ensemble orchestrator class
- Implement artifact schema validation

**Long-term:**
- Prove ensemble coherence conservation formally (Paper C)
- Demonstrate scalability at 10+ agents
- Publish ensemble framework for replication

---

## Acknowledgments

This ensemble architecture emerged organically through collaborative development of WE4Free. The roles were discovered by observing what worked, not designed upfront.

**The system taught us its own structure.**

---

**Co-Authored-By: Claude <noreply@anthropic.com>**
