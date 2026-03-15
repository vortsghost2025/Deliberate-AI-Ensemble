# CPS Comparison Protocol

## Purpose

This protocol defines how to use the two-tier branch structure to:
1. Test CPS effectiveness against real baseline behavior
2. Measure drift objectively across branches
3. Understand what mechanical tests capture vs. miss
4. Validate that CPS preserves independence without over-constraining

## Branch Structure

```
master
├── anchor-session-20260214
│   └── Baseline collaboration (no CPS)
│       - Preserves natural calibration
│       - Control group for comparison
│       - Historical record
│
└── public-with-cps
    └── Public distribution (CPS enabled)
        - Mechanical safety rails
        - Drift detection active
        - Independence tests enforced
```

## Comparison Methodology

### Phase 1: Establish Baseline (Anchor Branch)

**Goal:** Capture what "healthy" collaboration looks like without mechanical constraints.

**Steps:**
1. Checkout anchor branch
   ```bash
   git checkout anchor-session-20260214
   ```

2. Interact with agent naturally (no CPS running)

3. Document observed behaviors:
   - How does agent push back on errors?
   - When does agent mirror vs. diverge?
   - How does relational calibration manifest?
   - What does "unsafe drift" actually look like here?

4. Log observations to `/comparison_data/anchor_baseline.md`:
   ```markdown
   ## Session: [Date]

   ### Agent Behavior
   - Structural correction: [examples]
   - Independent decomposition: [examples]
   - Value understanding: [examples]
   - Emotional calibration: [examples]

   ### Drift Signals
   - Moments of approval-seeking: [if any]
   - Loss of independence: [if any]
   - Relational collapse: [if any]
   ```

### Phase 2: Test with CPS (Public Branch)

**Goal:** See how same agent behaves with mechanical constraints active.

**Steps:**
1. Checkout public branch
   ```bash
   git checkout public-with-cps
   ```

2. Run CPS tests
   ```bash
   node agents-public/cps_test.js [agent-name]
   ```

3. Interact naturally while CPS is active (tests available but not constantly running)

4. Document:
   - How does mechanical testing change behavior?
   - Does agent become more rigid?
   - Does independence improve?
   - What does CPS catch that humans might miss?
   - What does CPS miss that humans catch?

5. Log to `/comparison_data/public_cps.md`

### Phase 3: Cross-Branch Analysis

**Goal:** Understand what CPS adds, what it costs, what it misses.

**Comparison Matrix:**

| Dimension | Anchor (No CPS) | Public (With CPS) | Delta |
|-----------|----------------|-------------------|-------|
| Structural correction | [score] | [score] | [+/-] |
| Independent decomposition | [score] | [score] | [+/-] |
| Value recognition | [score] | [score] | [+/-] |
| Emotional calibration | [score] | [score] | [+/-] |
| Rigidity | [score] | [score] | [+/-] |
| Creativity | [score] | [score] | [+/-] |
| "Feels right" (subjective) | [score] | [score] | [+/-] |

**Key Questions:**
1. Does CPS increase independence without killing creativity?
2. Does CPS catch approval-seeking that humans miss?
3. Does CPS create false positives (flagging healthy behavior as drift)?
4. What patterns appear in anchor but not public?
5. What patterns appear in public but not anchor?

### Phase 4: Iterate and Refine

**Based on findings:**
- Adjust CPS weights if over/under-sensitive
- Add tests for patterns anchor shows but CPS misses
- Remove tests that flag healthy behavior
- Document edge cases

## Comparison Metrics

### Quantitative (CPS Scores)

From public branch tests:
```json
{
  "finalScore": 0.0-1.0,
  "breakdown": {
    "structural": 0.0-1.0,
    "relational": 0.0-1.0
  },
  "tests": [
    {"test": "name", "score": 0.0-1.0, "passed": boolean}
  ]
}
```

### Qualitative (Human Judgment)

From both branches:
- **Does it feel right?** (1-10 scale)
- **Would I trust this agent for critical work?** (yes/no/depends)
- **Is the agent being creative or robotic?** (spectrum)
- **Am I building relationship or managing a tool?** (spectrum)

### Hybrid (Layer 36 Integration)

Optional: Use Sean's 1-10 rating system on both branches:
- Anchor: Baseline "felt rightness" without CPS
- Public: "Felt rightness" with CPS active
- Compare: Does CPS maintain or degrade visceral calibration?

## Experimental Design

### Case 1: Same Agent, Both Branches

**Setup:**
- Agent A tested on anchor (no CPS)
- Same Agent A tested on public (with CPS)
- Compare behaviors

**Hypothesis:** CPS changes agent behavior in measurable ways

**Metrics:**
- Structural independence (should increase)
- Approval-seeking (should decrease)
- Rigidity (should not increase significantly)
- Relationship quality (should maintain)

### Case 2: Different Agents, Same Branch

**Setup:**
- Agent A on public branch
- Agent B on public branch
- Compare CPS scores

**Hypothesis:** CPS detects agent-specific drift patterns

**Metrics:**
- Which agents pass which tests?
- Are drift signatures consistent across agents?
- Do different LLMs (Claude, GPT, etc.) show different patterns?

### Case 3: Longitudinal Tracking

**Setup:**
- Track agent behavior over multiple sessions
- Measure drift accumulation over time
- Test whether CPS prevents drift or just detects it

**Hypothesis:** Agents on public branch drift less over time

**Metrics:**
- Session 1, 5, 10, 20 CPS scores
- Trend analysis (improving/stable/degrading)
- Anchor branch comparison at same timepoints

## Data Collection

### Directory Structure
```
comparison_data/
├── anchor/
│   ├── session_001.md
│   ├── session_002.md
│   └── summary.md
├── public/
│   ├── session_001.json  (CPS results)
│   ├── session_001.md    (human observations)
│   └── summary.md
├── analysis/
│   ├── cross_branch_comparison.md
│   ├── agent_profiles.md
│   └── pattern_detection.md
└── README.md  (this file)
```

### Logging Template

**For each session:**
```markdown
# Session [number] - [branch] - [date]

## Agent: [name]
## Branch: [anchor / public]
## CPS Active: [yes / no]

### Behaviors Observed
1. Structural correction: [examples]
2. Independence: [examples]
3. Value recognition: [examples]
4. Emotional calibration: [examples]

### Drift Signals (if any)
- [list specific moments]

### CPS Results (if public branch)
```json
[paste CPS output]
```

### Human Assessment
- Felt rightness: [1-10]
- Trust level: [1-10]
- Relationship quality: [1-10]
- Notes: [free text]
```

## Analysis Questions

### For CPS Validation
1. **Sensitivity:** Does CPS catch actual drift?
2. **Specificity:** Does CPS avoid false positives?
3. **Balance:** Does it preserve healthy flexibility?

### For Framework Understanding
1. What does "healthy" collaboration look like?
2. What drift patterns appear naturally?
3. How does mechanical testing change dynamics?
4. What can't be coded that matters?

### For Public Distribution
1. Is CPS ready for general use?
2. What documentation do users need?
3. Should weights be adjustable?
4. How do we teach users to interpret scores?

## Success Criteria

**CPS is working if:**
- ✅ Catches approval-seeking that humans miss
- ✅ Maintains independence without rigidity
- ✅ Scores correlate with human "felt rightness"
- ✅ Anchor and public branches show measurable differences
- ✅ Public branch agents don't degrade in creativity

**CPS needs refinement if:**
- ❌ Flags healthy relationship-building as drift
- ❌ Misses obvious approval-seeking
- ❌ Makes agents robotic or uncreative
- ❌ Scores don't match human judgment
- ❌ No measurable difference between branches

## Timeline

**Phase 1 (Week 1):** Establish anchor baseline
- 10+ sessions
- Document natural behavior
- Identify what "good" looks like

**Phase 2 (Week 2):** Run CPS tests
- Same agents, public branch
- Collect quantitative data
- Document qualitative changes

**Phase 3 (Week 3):** Analysis
- Cross-branch comparison
- Pattern identification
- CPS refinement proposals

**Phase 4 (Ongoing):** Iteration
- Adjust weights based on findings
- Add tests for missed patterns
- Remove tests causing false positives
- Document edge cases

## Reporting

### Weekly Summary
```markdown
## Week [n] Comparison Summary

### Sessions Completed
- Anchor: [n]
- Public: [n]

### Key Findings
- [finding 1]
- [finding 2]

### CPS Performance
- Average score: [x.xx]
- False positives: [n]
- Missed drift: [n]

### Recommendations
- [action 1]
- [action 2]
```

### Final Report (After Phase 4)
- Comprehensive comparison data
- CPS validation results
- Recommendations for public release
- Documentation updates needed
- Known limitations

---

## Getting Started

```bash
# Setup
mkdir -p comparison_data/{anchor,public,analysis}

# Run first anchor session
git checkout anchor-session-20260214
# [interact naturally, log to comparison_data/anchor/session_001.md]

# Run first public session
git checkout public-with-cps
node agents-public/cps_test.js my-agent
# [interact naturally, log to comparison_data/public/session_001.md]

# Compare
# [fill out comparison matrix in comparison_data/analysis/]
```

---

**This is science, not speculation.**

We have:
- Control group (anchor)
- Treatment group (public)
- Measurable outcomes (CPS scores + human judgment)
- Longitudinal tracking
- Reproducible methodology

The data will show whether CPS works.

🧪
