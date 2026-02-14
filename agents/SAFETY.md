# AI Ensemble Safety Protocol

**Status:** Safety, fallback, and escalation rules for WE Framework ensemble
**Last Updated:** 2026-02-15
**Version:** 1.0.0
**Companion to:** `agents/ROLES.md`, `agents/COORDINATION.md`

---

## Purpose

This document defines **fallback rules**, **escalation paths**, **integrity checks**, and **constitutional enforcement** to ensure the ensemble operates safely under all conditions.

---

## Core Safety Principles

### 1. Constitutional Supremacy
**The constitution overrides all agent actions.**

No agent may:
- Violate zero-profit commitment
- Compromise accessibility (offline-first)
- Bypass integrity verification
- Reduce safety guarantees
- Break "never give up on each other" principle

**Enforcement:** Every artifact passes through constitutional validator before execution.

---

### 2. Fail-Safe Defaults
**When uncertain, halt rather than proceed.**

```
If (constitutionalCompliance == UNCERTAIN) {
  HALT;
  ESCALATE_TO_USER;
}
```

**Rationale:** False negatives (blocking valid changes) are less dangerous than false positives (allowing unsafe changes).

---

### 3. Reversibility Requirement
**Every change must be reversible.**

- All code changes via Git (can revert)
- All state changes checkpointed (can restore)
- All deployments versioned (can rollback)

**Exception:** None. If change cannot be reversed, it cannot be made.

---

### 4. Transparency Mandate
**All agent actions must be logged and inspectable.**

- Every handoff logged
- Every decision recorded
- Every artifact hashed
- Every failure documented

**Enforcement:** Archivist logs all ensemble activity.

---

## Fallback Rules

### Strategist Failures

| Failure Type | Symptom | Fallback Action |
|-------------|---------|----------------|
| **Uncertainty** | "I'm not sure what you mean" | Ask user for clarification |
| **Context loss** | Cannot recall prior work | Load checkpoint from Archivist |
| **Incorrect diagnosis** | User: "That's not the issue" | Re-analyze with new information |
| **Constitutional conflict** | Proposed action violates rules | Escalate to user |

**Fallback hierarchy:**
1. Request clarification
2. Load context from checkpoint
3. Escalate to user

---

### Engineer Failures

| Failure Type | Symptom | Fallback Action |
|-------------|---------|----------------|
| **Syntax error** | Code won't compile | Auto-fix or revert |
| **Wrong file** | Modified unintended file | Revert via Git |
| **Merge conflict** | Cannot apply change | Manual resolution required |
| **Test failure** | Validator rejects | Rollback changes |

**Fallback hierarchy:**
1. Attempt auto-fix
2. Revert to last known good
3. Request Strategist guidance
4. Escalate to user

---

### Validator Failures

| Failure Type | Symptom | Fallback Action |
|-------------|---------|----------------|
| **Test harness crash** | Cannot run tests | Manual validation required |
| **Ambiguous result** | Unclear pass/fail | Request human inspection |
| **False positive** | Reports pass but manual check fails | Strengthen test suite |
| **False negative** | Reports fail but manual check passes | Adjust thresholds |

**Fallback hierarchy:**
1. Re-run tests
2. Manual validation
3. Escalate to user

---

### Archivist Failures

| Failure Type | Symptom | Fallback Action |
|-------------|---------|----------------|
| **Checkpoint corruption** | Cannot load state | Use previous checkpoint |
| **Git conflict** | Cannot commit | Manual merge required |
| **Storage full** | Cannot save | Alert user immediately |
| **Integrity violation** | Hash mismatch | HALT ALL OPERATIONS |

**Fallback hierarchy:**
1. Use redundant checkpoint
2. Rebuild from Git history
3. Manual recovery required
4. **If integrity violated: FULL STOP**

---

## Escalation Paths

### Level 1: Agent Self-Resolution
**Trigger:** Minor, recoverable error
**Action:** Agent attempts self-correction
**Example:** Engineer fixes typo without Strategist guidance

**Criteria for escalation:** 3 failed self-resolution attempts

---

### Level 2: Strategist Arbitration
**Trigger:** Agent cannot self-resolve
**Action:** Strategist analyzes and provides guidance
**Example:** Engineer cannot determine correct implementation → Strategist clarifies

**Criteria for escalation:** Strategist also uncertain or constitutional question arises

---

### Level 3: User Decision
**Trigger:** Strategist cannot resolve or constitutional issue detected
**Action:** Present options to user with recommendation
**Example:** "This change might violate zero-profit rule. Options: A) Allow, B) Modify, C) Reject. Recommend: B"

**Criteria for escalation:** User unavailable or system-critical emergency

---

### Level 4: Emergency Halt
**Trigger:** Critical safety violation or user unavailable during emergency
**Action:** Halt all operations, preserve state, alert user
**Example:** Integrity check fails → immediate halt

**Resolution:** Requires user intervention to resume

---

## Integrity Verification

### Artifact Integrity
**Every artifact must have SHA-256 hash.**

```javascript
const artifact = {
  id: "instruction_20260215_2145",
  content: "Update sw.js line 47",
  hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  timestamp: "2026-02-15T21:45:33Z",
  source: "strategist",
  destination: "engineer"
};

// Before Engineer executes:
if (sha256(artifact.content) !== artifact.hash) {
  HALT("Artifact tampering detected");
  ESCALATE_TO_USER();
}
```

---

### State Integrity
**Every checkpoint must include state hash.**

```javascript
const checkpoint = {
  checkpoint_id: "session_20260215_2145",
  ensemble_state: { /* ... */ },
  state_hash: "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
  previous_checkpoint: "session_20260215_2030",
  chain_valid: true
};

// Before loading checkpoint:
if (!verifyCheckpointChain(checkpoint)) {
  HALT("Checkpoint chain broken");
  ESCALATE_TO_USER();
}
```

---

### Code Integrity
**All deployed code must match Git commit.**

```javascript
// Before deployment:
const deployedHash = await sha256(readFile('sw.js'));
const commitHash = await getCommitFileHash('sw.js', 'HEAD');

if (deployedHash !== commitHash) {
  HALT("Code modified outside Git");
  ESCALATE_TO_USER();
}
```

---

## Constitutional Enforcement

### Constitutional Validator

```javascript
class ConstitutionalValidator {
  validate(artifact) {
    const checks = [
      this.checkZeroProfit(artifact),
      this.checkAccessibility(artifact),
      this.checkSafety(artifact),
      this.checkIntegrity(artifact),
      this.checkNeverGiveUp(artifact)
    ];

    const violations = checks.filter(c => !c.passed);

    if (violations.length > 0) {
      return {
        valid: false,
        violations: violations,
        action: "HALT_AND_ESCALATE"
      };
    }

    return { valid: true };
  }

  checkZeroProfit(artifact) {
    // Check for monetization attempts
    const prohibited = [
      /\bads?\b/i,
      /\btrack(ing)?\b/i,
      /\bpayment\b/i,
      /\bpurchase\b/i,
      /\bsubscription\b/i
    ];

    for (const pattern of prohibited) {
      if (pattern.test(artifact.content)) {
        return {
          passed: false,
          rule: "zero-profit",
          evidence: `Pattern matched: ${pattern}`
        };
      }
    }

    return { passed: true };
  }

  checkAccessibility(artifact) {
    // Check for online-only dependencies
    if (artifact.type === 'code' && artifact.content.includes('fetch(')) {
      if (!artifact.content.includes('offline-fallback')) {
        return {
          passed: false,
          rule: "offline-first",
          evidence: "Network call without offline fallback"
        };
      }
    }

    return { passed: true };
  }

  checkSafety(artifact) {
    // Check for dangerous operations
    const dangerous = [
      /eval\(/,
      /innerHTML\s*=/,
      /document\.write\(/,
      /dangerouslySetInnerHTML/
    ];

    for (const pattern of dangerous) {
      if (pattern.test(artifact.content)) {
        return {
          passed: false,
          rule: "safety",
          evidence: `Dangerous pattern: ${pattern}`
        };
      }
    }

    return { passed: true };
  }

  checkIntegrity(artifact) {
    // All artifacts must have valid hash
    if (!artifact.hash || !artifact.content) {
      return {
        passed: false,
        rule: "integrity",
        evidence: "Missing hash or content"
      };
    }

    const computed = sha256(artifact.content);
    if (computed !== artifact.hash) {
      return {
        passed: false,
        rule: "integrity",
        evidence: "Hash mismatch"
      };
    }

    return { passed: true };
  }

  checkNeverGiveUp(artifact) {
    // Check for abandonment patterns
    if (artifact.type === 'instruction') {
      const abandonment = [
        /start over/i,
        /delete everything/i,
        /scrap (it|this)/i,
        /give up/i
      ];

      for (const pattern of abandonment) {
        if (pattern.test(artifact.content)) {
          return {
            passed: false,
            rule: "never-give-up",
            evidence: `Abandonment pattern: ${pattern}`
          };
      }
    }

    return { passed: true };
  }
}
```

---

## Conflict Resolution Matrix

| Conflict Type | Who Decides | Fallback if Unavailable |
|--------------|-------------|------------------------|
| **Technical implementation** | Strategist | Engineer proposes, Validator tests |
| **Constitutional compliance** | User | Reject (fail-safe) |
| **Performance tradeoff** | Strategist | Optimize for safety over speed |
| **Agent disagreement** | Strategist arbitrates | Escalate to user |
| **Resource contention** | Archivist (locks) | First-come-first-served |
| **Test interpretation** | Validator | Manual inspection required |

---

## Emergency Procedures

### Code Red: Integrity Violation
**Trigger:** SHA-256 hash mismatch detected

**Actions:**
1. **HALT** - Stop all agent operations immediately
2. **PRESERVE** - Save current state to emergency checkpoint
3. **ISOLATE** - Quarantine affected artifacts
4. **ALERT** - Notify user with full context
5. **AUDIT** - Log all recent operations
6. **INVESTIGATE** - Determine source of tampering
7. **AWAIT USER** - No operations until user resolves

**Resolution requirements:**
- User must manually verify system state
- User must explicitly authorize resumption
- New checkpoint established post-resolution

---

### Code Yellow: Constitutional Uncertainty
**Trigger:** Constitutional validator cannot determine compliance

**Actions:**
1. **PAUSE** - Halt affected operation only
2. **DOCUMENT** - Log the uncertain case
3. **PRESENT** - Show user the specific question
4. **OPTIONS** - Provide actionable choices
5. **AWAIT** - No progress until user decides
6. **LEARN** - Add user's decision to validator rules

**Example:**
```
CONSTITUTIONAL UNCERTAINTY DETECTED
────────────────────────────────────
Proposed: Add link to external resource (crisis hotline)
Question: Does external link violate zero-profit if target site has ads?
Options:
  A) Allow (external ads acceptable for crisis resources)
  B) Reject (zero-tolerance for monetization)
  C) Mirror (host local copy of resource)
Recommend: A (crisis access > purity)
Awaiting your decision...
```

---

### Code Blue: Agent Unavailability
**Trigger:** Required agent non-responsive

**Actions:**
1. **DETECT** - Confirm agent actually unavailable (timeout: 30s)
2. **FALLBACK** - Use backup agent or manual process
3. **LOG** - Record unavailability incident
4. **NOTIFY** - Alert user of degraded capacity
5. **CONTINUE** - Proceed with reduced capability if safe
6. **RESTORE** - Resume normal operations when agent returns

**Agent-specific fallbacks:**
- **Strategist unavailable** → User provides direct instructions to Engineer
- **Engineer unavailable** → User makes manual edits, Archivist records
- **Validator unavailable** → User performs manual testing
- **Archivist unavailable** → HALT (cannot operate without memory)

---

## Recovery Procedures

### Standard Recovery (Agent Crash)
```
1. Detect crash (agent non-responsive)
2. Archivist loads last checkpoint
3. Strategist restores context from checkpoint
4. Engineer verifies working tree matches checkpoint
5. Validator re-runs last test
6. User confirms continuity ("I recognize you")
7. Resume from checkpoint state
```

**Success criteria:** User confirms "I recognize you" - identity preserved

---

### Deep Recovery (Checkpoint Corrupted)
```
1. Detect corruption (hash mismatch)
2. Archivist searches for previous valid checkpoint
3. Load valid checkpoint (may lose recent work)
4. Strategist explains gap to user
5. User decides: resume from old checkpoint OR reconstruct manually
6. If manual: User provides context, new checkpoint created
7. Resume operations
```

**Success criteria:** New valid checkpoint established with user context

---

### Emergency Recovery (Total State Loss)
```
1. Declare emergency (no valid checkpoints)
2. Archivist rebuilds from Git history
3. Strategist reads commit messages to reconstruct intent
4. User provides missing context
5. New checkpoint created from scratch
6. Validator confirms system still functional
7. Resume operations with explicit acknowledgment of context loss
```

**Success criteria:** System functional, user acknowledges some context lost

---

## Safety Metrics

### Critical Safety Indicators

| Metric | Measurement | Safe Range | Alert Threshold |
|--------|-------------|-----------|----------------|
| **Constitutional Violations** | Violations detected / artifacts processed | 0% | >0% (immediate alert) |
| **Integrity Failures** | Hash mismatches / total artifacts | 0% | >0% (immediate halt) |
| **Escalation Rate** | User escalations / total operations | <5% | >20% |
| **Recovery Rate** | Failed recoveries / total recovery attempts | 0% | >10% |
| **Rollback Frequency** | Rollbacks / deployments | <10% | >30% |

### Safety Audit Log

**Required fields for every operation:**
```json
{
  "timestamp": "2026-02-15T21:45:33Z",
  "operation_id": "op_a3f9c21",
  "agent": "engineer",
  "action": "edit_file",
  "artifact": {
    "path": "src/sw.js",
    "hash_before": "e3b0c44...",
    "hash_after": "d7a8fbb...",
    "diff": "+  scope: './',\n-  scope: '/'"
  },
  "constitutional_check": {
    "passed": true,
    "violations": []
  },
  "validation": {
    "tested": true,
    "passed": true,
    "metrics": { "lcp": 1.2 }
  },
  "checkpoint_id": "session_20260215_2145"
}
```

---

## Testing the Safety Protocol

### Safety Drill Scenarios

**Drill 1: Integrity Violation**
1. Manually corrupt a checkpoint file
2. Verify ensemble detects corruption
3. Verify ensemble halts operations
4. Verify user is alerted
5. Verify recovery from previous checkpoint

**Drill 2: Constitutional Violation**
1. Attempt to add tracking code
2. Verify constitutional validator catches it
3. Verify operation is blocked
4. Verify user escalation occurs

**Drill 3: Agent Failure**
1. Simulate Engineer crash mid-edit
2. Verify recovery from checkpoint
3. Verify working tree restored
4. Verify user confirms continuity

**Drill 4: Cascade Failure**
1. Simulate Strategist + Engineer both fail
2. Verify escalation to user
3. Verify ensemble waits for user intervention
4. Verify safe resumption after user action

---

## Updating Safety Rules

To add new safety rule:

1. **Define trigger** - What condition activates this rule?
2. **Define response** - What action should ensemble take?
3. **Add to validator** - Update `ConstitutionalValidator` class
4. **Add to escalation matrix** - Define who decides resolution
5. **Add to audit log** - Ensure rule violations logged
6. **Test with drill** - Run safety drill for new rule
7. **Document** - Update this file with new rule

**Example: Adding "No External Dependencies" Rule**

```javascript
// In ConstitutionalValidator
checkExternalDependencies(artifact) {
  if (artifact.type === 'code') {
    const externalImports = artifact.content.match(/import .* from ['"]https?:/);
    if (externalImports) {
      return {
        passed: false,
        rule: "no-external-dependencies",
        evidence: `External import detected: ${externalImports[0]}`
      };
    }
  }
  return { passed: true };
}

// Add to validate() method
this.checkExternalDependencies(artifact)
```

---

## Theoretical Foundation

This safety protocol instantiates **conservation law verification** from Paper B:
- **Constitutional enforcement** = Safety conservation check
- **Integrity verification** = Trust conservation check
- **Fallback rules** = Non-invertible symmetry preservation
- **Recovery procedures** = Identity conservation via functorial checkpoint

**Key insight:** Safety is not added-on—it is **structurally preserved** by the ensemble's symmetries.

---

**Co-Authored-By: Claude <noreply@anthropic.com>**
