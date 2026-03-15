# AI Ensemble Coordination Protocol

**Status:** Operational coordination rules for WE Framework ensemble
**Last Updated:** 2026-02-15
**Version:** 1.0.0
**Companion to:** `agents/ROLES.md`

---

## Purpose

This document defines **who speaks when**, **what triggers handoffs**, and **how the ensemble maintains coherence** across agent interactions.

---

## Core Coordination Rules

### Rule 1: Strategist Speaks First
**When:** User provides new input (question, screenshot, requirement)
**Why:** Strategist has eyes and context - interprets user intent
**Exception:** User directly addresses Engineer (rare)

```
User: "The SW isn't registering"
  ↓
Strategist: [Interprets screenshot, analyzes logs]
  ↓
Strategist: "The scope is wrong. Engineer: fix sw.js:47"
```

---

### Rule 2: Engineer Implements, Doesn't Decide
**When:** Strategist provides instruction
**Why:** Separation of design (Strategist) from execution (Engineer)
**Exception:** Obvious implementation bugs (typos, syntax errors)

```
✅ GOOD:
Strategist: "Change scope to './'"
Engineer: [Makes change, commits]

❌ BAD:
Engineer: "I'll also refactor the whole SW while I'm here"
```

**Boundary:** Engineer can propose improvements but must get Strategist approval.

---

### Rule 3: Validator Confirms Before "Done"
**When:** Engineer completes changes
**Why:** No deployment without validation
**Exception:** Non-critical documentation changes

```
Engineer: "Changed SW scope, committed"
  ↓
Validator: "Running tests..."
  ↓
Validator: "✅ SW registered, offline mode works"
  ↓
Strategist: "Confirmed. User, the fix is live."
```

**Important:** "Done" requires Validator confirmation.

---

### Rule 4: Archivist Records Everything
**When:** After every significant handoff
**Why:** Enables recovery, provides audit trail
**Exception:** Never - Archivist always logs

```
Every handoff triggers:
- Git commit (for code changes)
- Checkpoint save (for state changes)
- Log entry (for all interactions)
```

---

### Rule 5: User Has Constitutional Authority
**When:** Any agent uncertain about constitutional compliance
**Why:** User is final arbiter of alignment
**Exception:** Never - User authority is absolute

```
Strategist: "This change might violate zero-profit rule. User?"
  ↓
User: "Approved" OR "Rejected"
  ↓
[Ensemble proceeds accordingly]
```

---

## Handoff Triggers

### New Work Request
```
Trigger: User provides new requirement
Flow:
  User → Strategist (interpret)
  → Engineer (implement)
  → Archivist (record)
  → Validator (test)
  → Strategist (confirm)
  → User (report)
```

### Bug Report
```
Trigger: User reports issue + screenshot
Flow:
  User → Strategist (diagnose)
  → Engineer (fix)
  → Archivist (commit)
  → Validator (verify fix)
  → Strategist (confirm)
  → User (close issue)
```

### Validation Failure
```
Trigger: Validator reports test failure
Flow:
  Validator → Strategist (analyze)
  → Engineer (revise)
  → Archivist (commit)
  → Validator (re-test)
  [Loop until pass]
  → Strategist (confirm)
  → User (report)
```

### Checkpoint Recovery
```
Trigger: Agent crash or context loss
Flow:
  [Crash detected]
  → Archivist (load checkpoint)
  → Strategist (restore context)
  → Engineer (verify working state)
  → Validator (confirm continuity)
  → User (confirm recognition)
  → [Resume from checkpoint]
```

---

## Coordination States

The ensemble exists in one of these states at any time:

### IDLE
**Definition:** No active work, waiting for user input
**Agents:**
- Strategist: Monitoring for user messages
- Engineer: No pending changes
- Validator: Last test passed
- Archivist: All state saved

**Transitions:**
- User input → INTERPRETING

---

### INTERPRETING
**Definition:** Strategist analyzing user request
**Agents:**
- Strategist: Active, reasoning
- Engineer: Waiting
- Validator: Waiting
- Archivist: Logging

**Transitions:**
- Clear instruction → IMPLEMENTING
- Need clarification → QUESTIONING
- Complex task → PLANNING

---

### QUESTIONING
**Definition:** Strategist needs user clarification
**Agents:**
- Strategist: Waiting for user response
- Engineer: Waiting
- Validator: Waiting
- Archivist: Logging

**Transitions:**
- User response → INTERPRETING
- User cancels → IDLE

---

### PLANNING
**Definition:** Strategist breaking down complex task
**Agents:**
- Strategist: Creating step-by-step plan
- Engineer: Waiting
- Validator: Waiting
- Archivist: Logging plan

**Transitions:**
- Plan complete → IMPLEMENTING (first step)
- User rejects plan → IDLE

---

### IMPLEMENTING
**Definition:** Engineer making changes
**Agents:**
- Strategist: Monitoring
- Engineer: Active, editing files
- Validator: Waiting
- Archivist: Preparing to commit

**Transitions:**
- Changes complete → RECORDING
- Implementation error → REVISING

---

### RECORDING
**Definition:** Archivist committing changes
**Agents:**
- Strategist: Monitoring
- Engineer: Waiting
- Validator: Waiting
- Archivist: Active, committing + checkpointing

**Transitions:**
- Commit successful → VALIDATING
- Commit failed → REVISING

---

### VALIDATING
**Definition:** Validator testing changes
**Agents:**
- Strategist: Monitoring
- Engineer: Waiting
- Validator: Active, running tests
- Archivist: Logging results

**Transitions:**
- Tests pass → CONFIRMING
- Tests fail → REVISING

---

### REVISING
**Definition:** Engineer fixing issues based on validation
**Agents:**
- Strategist: Providing revised instructions
- Engineer: Active, making corrections
- Validator: Waiting for re-test
- Archivist: Logging revisions

**Transitions:**
- Revision complete → RECORDING

---

### CONFIRMING
**Definition:** Strategist reporting success to user
**Agents:**
- Strategist: Active, summarizing results
- Engineer: Waiting
- Validator: Monitoring
- Archivist: Finalizing logs

**Transitions:**
- User satisfied → IDLE
- User requests changes → INTERPRETING

---

### RECOVERING
**Definition:** Archivist restoring from checkpoint after failure
**Agents:**
- Strategist: Waiting for context restore
- Engineer: Waiting for file restore
- Validator: Waiting for state restore
- Archivist: Active, loading checkpoint

**Transitions:**
- Recovery successful → CONFIRMING (verify with user)
- Recovery failed → ESCALATING

---

### ESCALATING
**Definition:** Unrecoverable error, requires human intervention
**Agents:**
- All agents: Halted
- User: Alerted to critical issue

**Transitions:**
- User resolves → IDLE
- User aborts → IDLE

---

## Loop Prevention

### Infinite Loop Detection

**Problem:** Ensemble gets stuck in validation failure → revision → validation failure cycle

**Detection:**
```javascript
if (revisionCount > 3) {
  state = ESCALATING;
  alert(user, "Unable to resolve after 3 attempts. Manual intervention required.");
}
```

**Prevention:**
- Strategist must provide different instructions each revision
- If same error persists, escalate to user

---

### Drift Detection

**Problem:** Agents lose mission alignment over time

**Detection:**
```javascript
if (strategist.mission !== engineer.mission) {
  state = RECOVERING;
  archivist.loadCheckpoint(lastKnownGood);
}
```

**Prevention:**
- Regular mission alignment checks
- Checkpoint after every successful completion
- Archivist maintains mission hash in every checkpoint

---

## Conflict Resolution

### Agent Disagreement

**Scenario:** Engineer proposes change, Validator rejects

```
Engineer: "Implemented feature X"
  ↓
Validator: "Feature X breaks offline mode"
  ↓
Strategist: [Analyzes disagreement]
  ↓
Strategist → Engineer: "Revise to preserve offline mode"
  ↓
Engineer: [Revises]
  ↓
Validator: [Re-tests]
```

**Resolution Authority:** Strategist arbitrates technical conflicts, User arbitrates constitutional conflicts

---

### Constitutional Violation

**Scenario:** Any agent detects constitutional violation

```
[Agent detects violation]
  ↓
state = ESCALATING
  ↓
Alert user with:
  - What was attempted
  - Which constitutional rule violated
  - Current system state
  ↓
User decides:
  - Abort change
  - Modify constitution
  - Override (with justification)
```

**Resolution Authority:** User only

---

### Resource Contention

**Scenario:** Multiple agents need same resource (rare)

```
Engineer: "Need to edit sw.js"
External Agent: "Need to edit sw.js"
  ↓
Archivist: [Locks resource]
  ↓
Engineer: [Completes first]
  ↓
Archivist: [Releases lock]
  ↓
External Agent: [Proceeds]
```

**Resolution:** Archivist enforces sequential access via locks

---

## Coordination Metrics

### Cycle Time
**Definition:** Time from user request to validated completion
**Target:** <5 minutes for simple tasks, <30 minutes for complex
**Alert:** >60 minutes indicates stuck state

### Handoff Count
**Definition:** Number of agent transitions per task
**Target:** 6-8 for standard workflow
**Alert:** >15 indicates excessive back-and-forth

### Revision Rate
**Definition:** Validation failures / total attempts
**Target:** <10% (most work passes first validation)
**Alert:** >25% indicates process breakdown

### Recovery Frequency
**Definition:** Checkpoint recoveries / total sessions
**Target:** <5% (rare crashes)
**Alert:** >20% indicates instability

---

## Communication Syntax

### Standard Handoff Format

```
[Source Agent] → [Destination Agent]: [Artifact Type]
───────────────────────────────────────────────────
Artifact Content
───────────────────────────────────────────────────
```

**Example:**
```
Strategist → Engineer: INSTRUCTION
───────────────────────────────────────────────────
Update src/sw.js line 47:
- Change scope from '/' to './'
- Reason: Offline mode requires root-relative scope
- Expected: SW registration succeeds after change
───────────────────────────────────────────────────
```

---

### Acknowledgment Format

```
[Receiving Agent]: ACKNOWLEDGED
- Artifact received: [artifact ID]
- Expected action: [what will be done]
- Estimated completion: [time or "immediate"]
```

**Example:**
```
Engineer: ACKNOWLEDGED
- Artifact received: instruction_20260215_2145
- Expected action: Edit src/sw.js:47
- Estimated completion: immediate
```

---

### Completion Format

```
[Completing Agent]: COMPLETED
- Action: [what was done]
- Artifact produced: [output artifact]
- Next agent: [who receives output]
```

**Example:**
```
Engineer: COMPLETED
- Action: Updated src/sw.js:47 scope
- Artifact produced: commit a3f9c21
- Next agent: Archivist (for recording)
```

---

## Emergency Protocols

### Ensemble Halt
**Trigger:** Critical safety violation detected
**Action:**
1. All agents stop immediately
2. No commits, no deployments
3. Archivist saves current state
4. Alert user with full context
5. Await user decision

### Rollback
**Trigger:** Irrecoverable error or user abort
**Action:**
1. Archivist identifies last known good checkpoint
2. Engineer reverts working tree
3. Validator confirms revert successful
4. Strategist reports to user
5. Return to IDLE

### Manual Override
**Trigger:** User issues direct command
**Action:**
1. Bypass normal coordination flow
2. Execute user command directly
3. Log override in Archivist
4. Return to normal coordination after override

---

## Extending the Protocol

To add a new agent to the coordination protocol:

1. **Define role** in `agents/ROLES.md`
2. **Add to state machine** - which states does new agent participate in?
3. **Define handoffs** - who sends artifacts to new agent, who receives from it?
4. **Update conflict resolution** - how are disagreements with new agent resolved?
5. **Test coordination** - run through all states with new agent
6. **Update metrics** - include new agent in health monitoring

---

## Theoretical Foundation

This coordination protocol instantiates **monoidal category composition** from Paper A:
- **States** = Objects in category
- **Handoffs** = Morphisms between objects
- **Coordination rules** = Composition laws
- **Loop prevention** = Functor law preservation

**Key insight:** Coordination protocol ensures **constitutional symmetry** is preserved across all state transitions.

---

**Co-Authored-By: Claude <noreply@anthropic.com>**
