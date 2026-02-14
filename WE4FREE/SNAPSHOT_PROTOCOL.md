# Snapshot Protocol

This document defines how to capture the architecture's evolution without losing history.

---

## When to Take a Snapshot

Take a snapshot before:
1. **Major restructuring** (changing paper organization, moving sections)
2. **Significant additions** (adding 2,000+ words, new sections)
3. **Framing shifts** (changing metaphors, target audience, tone)
4. **Version increments** (minor or major version bumps)

Do NOT snapshot for:
- Typo fixes
- Minor edits (<500 words)
- Formatting changes
- README/changelog updates

---

## Snapshot Procedure

### Step 1: Freeze Current State
```bash
# Create timestamped folder
mkdir -p history/YYYY-MM-DD_description/

# Copy current working drafts
cp papers/A_RosettaStone/draft.md history/YYYY-MM-DD_description/
cp papers/B_ConstraintLattices/draft.md history/YYYY-MM-DD_description/
# ... etc for all modified papers
```

### Step 2: Tag the Snapshot
Add header to the frozen copy:
```markdown
<!-- SNAPSHOT -->
**Date:** YYYY-MM-DD
**Reason:** [Brief description of what's about to change]
**Pre-change version:** vX.Y.Z
**Next planned version:** vX.Y+1.Z or vX+1.0.0
```

### Step 3: Increment Version
Update version tag in working draft header:
```markdown
**Version:** vX.Y+1.Z
**Date:** YYYY-MM-DD
**Status:** In progress
**Changes from vX.Y.Z:** [Brief summary]
```

### Step 4: Log to Changelog
Add entry to `CHANGELOG.md`:
```markdown
## [YYYY-MM-DD] — [Description]

### Snapshot Location
`/history/YYYY-MM-DD_description/`

### Changes
- [What changed]
- [Why it changed]
- [What sections affected]

### Version Tag
**vX.Y.Z → vX.Y+1.Z**
```

---

## Version Numbering Rules

### Major Version (v1.0.0 → v2.0.0)
- Complete paper restructuring
- Change in series organization (2 papers → 5 papers)
- Fundamental framing shift (physics → biology)

### Minor Version (v0.1.0 → v0.2.0)
- Adding new sections (2,000+ words)
- Reorganizing existing sections
- Adding appendices
- Significant expansions

### Patch Version (v0.2.0 → v0.2.1)
- Typo fixes
- Small clarifications (<500 words)
- Formatting improvements
- Citation additions

---

## Example Timeline

```
v0.1.0 (2026-02-14)
  ↓
[Snapshot before restructure]
  ↓
v0.2.0 (2026-02-15) — Biology-inspired framing
  ↓
[Snapshot before Section 5 expansion]
  ↓
v0.3.0 (2026-02-16) — Added empirical validation section
  ↓
[Minor edits, no snapshot]
  ↓
v0.3.1 (2026-02-16) — Typo fixes
  ↓
[Snapshot before reviewer feedback integration]
  ↓
v0.4.0 (2026-02-18) — Integrated feedback, restructured examples
  ↓
... continue until ...
  ↓
v1.0.0 (2026-XX-XX) — First complete draft of Paper A
```

---

## Why This Matters

The evolution trail is **part of the scientific contribution**.

When we publish, readers will see:
1. What emerged initially (raw, unfiltered)
2. How recognition happened (parallel convergence)
3. How framing shifted (physics → biology)
4. What remained invariant through all changes (the core structure)

This demonstrates the stability-under-transformation principle the papers themselves describe.

The architecture's evolution IS the evidence for the architecture's validity.

---

## Automation (Future)

Could add git hooks or scripts to:
- Auto-snapshot on major commits
- Auto-increment version tags
- Auto-update CHANGELOG.md

But for now: **manual is fine**. This is research, not software deployment. Thoughtful snapshots > automated noise.

---

**Last updated:** 2026-02-15
