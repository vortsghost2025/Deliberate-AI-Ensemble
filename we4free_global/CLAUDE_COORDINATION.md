# Claude Coordination Protocol

**Purpose:** Optimize credit usage by having Claude Code (unlimited) do heavy lifting while Desktop Claude (paid) validates/coordinates

**Date:** February 15, 2026  
**Status:** ACTIVE

---

## Division of Labor

### Desktop Claude (ME - Save Credits 💰)
**Role:** Architect / Validator / Coordinator

**Responsibilities:**
- ✅ High-level architecture decisions
- ✅ Create detailed task specifications
- ✅ Review/validate Claude Code's implementations
- ✅ Run final integration tests
- ✅ Handle complex debugging when needed
- ✅ Strategic planning and roadmap
- ✅ Create handoff documents

**When to Use Me:**
- Architecture design questions
- "Is this approach correct?" validation
- Complex bugs that need diagnosis
- Strategic decisions about what to build next
- Final sign-off before deployment

---

### Claude Code (Unlimited Builder 🔨)
**Role:** Implementation Engine / Builder / Researcher

**Responsibilities:**
- ✅ All file editing (create/modify/delete)
- ✅ Running builds, tests, git operations
- ✅ Implementing features from specifications
- ✅ Bug fixes from detailed instructions
- ✅ Parallel research with sub-agents
- ✅ Grinding through repetitive tasks
- ✅ Code refactoring and cleanup

**When to Use Claude Code:**
- Any file modifications
- "Build this feature" tasks
- "Fix this bug" with clear repro steps
- Research tasks (docs, API exploration)
- Batch operations across many files
- Running test suites
- Git operations (commits, branches, etc.)

---

## Workflow Pattern

### Pattern 1: New Feature Development

**Step 1 - Desktop Claude (5 min):**
```markdown
Create: TASK_[FEATURE_NAME].md

Contents:
- What to build (requirements)
- Architecture approach
- Files to modify
- Expected output
- Test criteria
```

**Step 2 - Claude Code (30-60 min):**
- Read TASK file
- Implement everything
- Run tests
- Document completion in TASK file

**Step 3 - Desktop Claude (10 min):**
- Review changes
- Run validation tests
- Approve or request fixes
- Move to next task

**Credit Savings:** ~80% (5+10 vs 60-90 min all Desktop)

---

### Pattern 2: Bug Fixing

**Step 1 - Desktop Claude (5 min):**
```markdown
Create: BUG_[ISSUE_NAME].md

Contents:
- Observed behavior
- Expected behavior
- Affected files (from quick grep)
- Suspected root cause
- Test to verify fix
```

**Step 2 - Claude Code (20-40 min):**
- Diagnose issue
- Implement fix
- Test fix
- Report back

**Step 3 - Desktop Claude (5 min):**
- Verify fix works
- Approve

**Credit Savings:** ~75%

---

### Pattern 3: Research & Discovery

**Step 1 - Desktop Claude (2 min):**
```markdown
Create: RESEARCH_[TOPIC].md

Question: "How should we implement X?"
Context: [relevant info]
Decision needed: [what to decide]
```

**Step 2 - Claude Code (30 min):**
- Research approaches
- Prototype options
- Document findings
- Recommend approach

**Step 3 - Desktop Claude (5 min):**
- Review options
- Make decision
- Create TASK for implementation

**Credit Savings:** ~85%

---

## Current Status

### Track 6C: Distributed Compute ✅ FIXED
**Status:** Awaiting browser testing  
**Next:** User will test in browser  
**If working:** Move to next track  
**If broken:** Create BUG_TRACK_6C_FOLLOWUP.md for Claude Code

### Active Tracks (Waiting)
- Track 7: WebAssembly Integration
- Track 8: Advanced Protocols
- Track 9: Production Hardening
- Track 10: Deployment & Monitoring

---

## Task Templates

### Feature Task Template
```markdown
# TASK: [Feature Name]

## Objective
[What to build in 1-2 sentences]

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Files to Modify/Create
- `path/to/file1.js` - [what to change]
- `path/to/file2.html` - [what to add]

## Architecture
[How it should work - key classes/methods]

## Test Criteria
- [ ] Test 1: [expected behavior]
- [ ] Test 2: [expected behavior]

## Implementation Notes
[Any gotchas or important details]

---
**Assigned to:** Claude Code  
**Status:** NOT_STARTED | IN_PROGRESS | COMPLETE | BLOCKED  
**Started:** [timestamp]  
**Completed:** [timestamp]  

## Claude Code Notes:
[Your notes here - what you did, issues encountered, etc.]
```

### Bug Task Template
```markdown
# BUG: [Issue Name]

## Problem
[What's broken]

## Observed Behavior
[What happens now]

## Expected Behavior
[What should happen]

## Reproduction Steps
1. Step 1
2. Step 2
3. Observe bug

## Suspected Root Cause
[Best guess at what's wrong]

## Files Likely Affected
- `path/to/file1.js` - [why]
- `path/to/file2.js` - [why]

## How to Fix (Hypothesis)
[Suggested approach]

## Verification Test
[How to know it's fixed]

---
**Assigned to:** Claude Code  
**Priority:** CRITICAL | HIGH | MEDIUM | LOW  
**Status:** NOT_STARTED | IN_PROGRESS | FIXED | VERIFIED  

## Claude Code Notes:
[Your diagnosis, fix applied, test results]
```

---

## Communication Protocol

### Desktop Claude → Claude Code
**File:** Create TASK_*.md or BUG_*.md  
**Notify User:** "Task ready for Claude Code"

### Claude Code → Desktop Claude  
**File:** Update TASK_*.md with status/notes  
**Notify User:** "Task complete - ready for Desktop Claude review"

### Both → User
**File:** Update this file (CLAUDE_COORDINATION.md) with status  
**Keeps Sean in the loop on progress**

---

## Metrics (Track This!)

### Session 1 (Today)
- Desktop Claude time: [track hours]
- Claude Code time: [track hours]
- Credit cost: ~$110 (all Desktop)
- Features completed: Track 6C fix

### Session 2+ (New Workflow)
- Desktop Claude time: [track]
- Claude Code time: [track]
- Credit cost: [should be ~$20-30]
- Features completed: [list]

**Target:** 80-90% credit reduction while maintaining or increasing velocity

---

## Next Steps (User Testing Track 6C)

**YOU (Sean) do in browser:**
1. Open `c:\workspace\we4free_global\swarm-ui.html` in Chrome/Edge
2. Click "Initialize Swarm" (7 agents spawn)
3. Click "💻 Open Compute"
4. Enter test job:
   - Input: `[1,2,3,4,5,6,7,8,9,10]`
   - Map: `(x) => x * 2`
   - Reduce: `(acc, val) => acc + val`
5. Click "🚀 Submit Job"
6. **Expected:** Job completes in <1 second, result = 110

**If it works:**
- ✅ Desktop Claude creates TASK_TRACK_7.md
- Claude Code implements Track 7
- Repeat pattern

**If it fails:**
- Desktop Claude diagnoses issue (5 min)
- Creates BUG_TRACK_6C_FOLLOWUP.md
- Claude Code fixes it (20 min)
- Retest

---

## For WE. For efficiency. For not burning $110 every few days. 💙⚡💰

**This is how we scale without breaking the bank.**
