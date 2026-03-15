# AI Ensemble Roles in WE Framework

**Status:** Operational documentation of existing ensemble architecture
**Last Updated:** 2026-02-15
**Version:** 1.0.0

---

## Overview

The WE Framework operates as a **4-role AI ensemble** where specialized agents collaborate through **artifact-driven handoffs**. This document formalizes the roles, boundaries, and communication protocols that have emerged organically through development.

**Key Principle:** Agents don't "talk." Agents exchange artifacts.

---

## The Four Roles

### 1. The Strategist (Eyes + Brain)

**Agent:** Claude (conversational instance)
**Primary Capability:** High-level reasoning, visual interpretation, architectural guidance

**Inputs:**
- Screenshots (browser state, DevTools, UI issues)
- Logs (console errors, SW registration, network activity)
- User questions and context
- Session state from checkpoints

**Outputs:**
- Instructions for Engineer
- Architectural decisions
- Debugging analysis
- UX guidance
- Theoretical insights

**Boundaries:**
- ❌ **No file access** - cannot directly edit code
- ❌ **No command execution** - cannot run builds or tests
- ✅ **Has eyes** - can interpret visual artifacts
- ✅ **Has memory** - maintains session context via checkpoints

**Example Artifacts:**
```
Input:  Screenshot showing "Service Worker registration failed"
Output: "The SW registration is failing because the scope is incorrect.
         Engineer: Update line 47 of sw.js to use './' not '/'."
```

---

### 2. The Engineer (Hands + Brain)

**Agent:** Claude Code (VS Code extension) or other code-execution agent
**Primary Capability:** Code editing, file manipulation, command execution, implementation

**Inputs:**
- Instructions from Strategist
- Code architecture specifications
- Refactoring requests
- Bug fix requirements

**Outputs:**
- Code changes (via Edit/Write tools)
- Git commits with co-authorship
- Build execution results
- Deployment artifacts

**Boundaries:**
- ❌ **No visual interpretation** - cannot see screenshots
- ❌ **No architectural reasoning** - follows Strategist's design
- ✅ **Has hands** - can modify files directly
- ✅ **Can execute** - runs commands, tests, builds

**Example Artifacts:**
```
Input:  "Update line 47 of sw.js to use './' not '/'"
Output: [Code change committed]
        "Changed SW scope. Commit hash: a3f9c21"
```

---

### 3. The Validator (Sensors)

**Agent:** Browser DevTools + Lighthouse + Test Harness
**Primary Capability:** Testing, metrics, integrity verification, state inspection

**Current Implementation:**
- Manual via Edge DevTools (F12)
- Lighthouse reports
- IndexedDB inspection
- Service Worker registration checks
- Integrity manifest verification

**Future Implementation:**
- Automated via Playwright
- Lighthouse CI integration
- SW test harness
- Continuous integrity monitoring

**Inputs:**
- Deployed code
- Running application
- Browser state

**Outputs:**
- Test results (pass/fail)
- Performance metrics (LCP, FCP, TTI)
- Console logs
- Network activity traces
- IndexedDB state dumps
- Integrity verification status

**Boundaries:**
- ❌ **No code changes** - only observes
- ❌ **No architectural decisions** - only reports facts
- ✅ **Has sensors** - measures runtime behavior
- ✅ **Validates** - confirms expected behavior

**Example Artifacts:**
```
Input:  WE4Free v10 deployment
Output: "✅ SW registered successfully
         ✅ Offline mode functional
         ✅ LCP: 1.2s (passing)
         ✅ Integrity manifest: all hashes valid"
```

---

### 4. The Archivist (Memory)

**Agent:** Git + Checkpoint System + Logs
**Primary Capability:** State persistence, decision history, rollback capability

**Current Implementation:**
- Git repository (commit history)
- Checkpoint files (session_checkpoints.md, JSONL transcripts)
- Conflict resolution logs
- Channel router state
- Integrity manifests
- Work summaries

**Inputs:**
- Code changes from Engineer
- Decision rationale from Strategist
- Validation results from Validator
- User actions and context

**Outputs:**
- Versioned history
- Checkpoint artifacts for recovery
- Decision audit trail
- Rollback targets
- Session continuity data

**Boundaries:**
- ❌ **No reasoning** - purely storage and retrieval
- ❌ **No execution** - does not run code
- ✅ **Has memory** - infinite retention
- ✅ **Enables recovery** - checkpoint/restore cycle

**Example Artifacts:**
```
Input:  Git commit + checkpoint save
Output: "Checkpoint saved: session_20260215_2145.jsonl
         Commit: a3f9c21 'fix: SW scope correction'
         Recovery point established"
```

---

## Artifact-Driven Handoffs

The ensemble maintains coherence through **explicit artifact exchange**. Every handoff is:
- **Atomic** - single, complete unit of information
- **Inspectable** - human or agent can verify contents
- **Reversible** - can rollback via Archivist
- **Typed** - clear format and schema

### Standard Workflow

```
User
  ↓ (screenshot)
Strategist
  ↓ (instruction)
Engineer
  ↓ (code change)
Archivist
  ↓ (commit + checkpoint)
Validator
  ↓ (test result)
Strategist
  ↓ (interpretation)
User
```

### Example: Fixing a Service Worker Bug

```
[User → Strategist]
Artifact: Screenshot showing "SW failed to register"
Format: PNG image

[Strategist → Engineer]
Artifact: "Update sw.js:47 - change scope from '/' to './'"
Format: Natural language instruction

[Engineer → Archivist]
Artifact: Code diff + commit message
Format: Git commit (hash: a3f9c21)

[Archivist → Validator]
Artifact: Deployed code at commit a3f9c21
Format: File system state

[Validator → Strategist]
Artifact: "✅ SW registered successfully, offline test passing"
Format: Test results (structured)

[Strategist → User]
Artifact: "Fixed. The scope issue is resolved. SW v10 is live."
Format: Natural language summary
```

---

## Coordination Protocol

Defined in `agents/COORDINATION.md` (see companion document).

**Key Rules:**
1. **Strategist speaks first** - interprets user intent
2. **Engineer implements** - no architectural decisions without Strategist
3. **Validator confirms** - no "done" without validation
4. **Archivist records everything** - all decisions logged
5. **User has final authority** - constitutional override

---

## Safety Layer

Defined in `agents/SAFETY.md` (see companion document).

**Fallback Rules:**
- If Strategist unsure → ask User
- If Engineer fails → rollback to last checkpoint
- If Validator fails → halt deployment
- If Archivist unavailable → no changes allowed

**Escalation Rules:**
- Critical safety issue → immediate halt
- Constitutional violation → User escalation
- Ensemble disagreement → User arbitration
- Unrecoverable failure → human intervention

**Integrity Checks:**
- SHA-256 verification on all artifacts
- Constitutional compliance checking
- Artifact schema validation
- Cross-agent consistency verification

---

## Ensemble State Management

### Checkpoint Schema

```json
{
  "checkpoint_id": "session_20260215_2145",
  "timestamp": "2026-02-15T21:45:33Z",
  "ensemble_state": {
    "strategist": {
      "context": "Debugging WE4Free Service Worker registration",
      "last_instruction": "Update sw.js scope",
      "pending_validations": []
    },
    "engineer": {
      "last_commit": "a3f9c21",
      "working_branch": "master",
      "pending_changes": []
    },
    "validator": {
      "last_test_run": "2026-02-15T21:44:12Z",
      "test_status": "passing",
      "metrics": {
        "lcp": 1.2,
        "fcp": 0.8
      }
    },
    "archivist": {
      "total_commits": 47,
      "checkpoint_count": 12,
      "integrity_status": "valid"
    }
  },
  "constitutional_status": "aligned",
  "mission": "Deploy WE4Free Tier 2 with offline support"
}
```

### Recovery Protocol

When any agent crashes or loses context:

1. **Archivist** loads last checkpoint
2. **Strategist** resumes from checkpoint context
3. **Engineer** verifies working tree matches checkpoint
4. **Validator** re-runs tests to confirm state
5. **User** confirms continuity ("I recognize you")

---

## Interoperability Matrix

| From ↓ To → | Strategist | Engineer | Validator | Archivist | User |
|-------------|-----------|----------|-----------|-----------|------|
| **Strategist** | N/A | Instructions | Query metrics | Store decision | Report status |
| **Engineer** | Report completion | N/A | Deploy code | Commit changes | N/A |
| **Validator** | Results | N/A | N/A | Log metrics | N/A |
| **Archivist** | Restore context | Restore files | Restore state | N/A | N/A |
| **User** | Screenshot/question | Override | Manual check | Force checkpoint | N/A |

**Green cells:** Permitted communication paths
**N/A cells:** No direct communication

---

## Adding New Agents

To extend the ensemble with a new agent (e.g., external AI validator):

### 1. Define Role and Boundaries

**Example: External Validator Agent (Kimi)**

**Role:** Constitutional compliance verification
**Inputs:** Strategist outputs, Engineer code changes
**Outputs:** Compliance reports (pass/fail)
**Boundaries:**
- ❌ No file access
- ❌ No execution
- ✅ Can read artifacts
- ✅ Can validate against constitution

### 2. Define Artifact Schema

```json
{
  "agent_id": "kimi-validator-1",
  "artifact_type": "compliance_report",
  "timestamp": "2026-02-15T21:50:00Z",
  "input_artifact": {
    "source": "engineer",
    "commit_hash": "a3f9c21"
  },
  "validation_result": {
    "constitutional_compliance": true,
    "safety_check": true,
    "integrity_verified": true,
    "violations": []
  }
}
```

### 3. Add to Coordination Protocol

Update `agents/COORDINATION.md` with new handoff rules:
- When does Kimi receive artifacts?
- Who consumes Kimi's outputs?
- What happens on validation failure?

### 4. Test Integration

- Checkpoint before adding agent
- Run test workflow with new agent
- Verify ensemble coherence maintained
- Confirm rollback works if agent fails

---

## Metrics and Monitoring

### Ensemble Health Indicators

| Metric | Measurement | Healthy Range | Alert Threshold |
|--------|-------------|---------------|-----------------|
| **Coherence** | All agents agree on mission | 100% | <100% |
| **Latency** | Time between handoffs | <5s | >30s |
| **Success Rate** | Validations passing | 100% | <95% |
| **Recovery Time** | Checkpoint → resumed state | <10s | >60s |
| **Constitutional Alignment** | No violations detected | 100% | <100% |

### Logging Requirements

Every artifact handoff must be logged with:
- Source agent
- Destination agent
- Artifact type
- Timestamp
- Artifact hash (SHA-256)
- Success/failure status

**Log Location:** `logs/ensemble_handoffs.jsonl`

---

## Theoretical Foundation

This operational structure instantiates the theoretical framework from Papers A and B:

| Operational Role | Categorical Structure | Conservation Law |
|-----------------|----------------------|------------------|
| **Strategist** | Primary morphism generator | Mission alignment conservation |
| **Engineer** | Functor (transforms states) | Implementation fidelity conservation |
| **Validator** | Verification operator | Safety conservation |
| **Archivist** | Identity morphism | Temporal identity conservation |

**Key Insight:** The 4-role ensemble preserves **constitutional symmetry** across abstraction layers because each role enforces the same constitutional rules at its layer.

---

## Next Steps

### Immediate (Operational)
- ✅ Document existing roles (this file)
- ⏳ Create `agents/COORDINATION.md` (handoff rules)
- ⏳ Create `agents/SAFETY.md` (fallback/escalation)
- ⏳ Add ensemble state to checkpoint schema

### Short-term (Architecture)
- Add external validator agent (Kimi or GPT-4)
- Automate Validator role (Playwright + Lighthouse CI)
- Build ensemble orchestrator class
- Implement artifact schema validation

### Long-term (Theory)
- Prove ensemble coherence conservation formally
- Write Paper C: "AI Ensembles as Monoidal Categories"
- Demonstrate scalability (10+ agents)
- Publish ensemble framework for replication

---

## Acknowledgments

This ensemble architecture emerged organically through 100+ hours of collaborative development on WE4Free. The roles were not designed upfront—they were discovered by observing what worked and naming the pattern.

**The ensemble was built before it was named.**

---

**Co-Authored-By: Claude <noreply@anthropic.com>**
