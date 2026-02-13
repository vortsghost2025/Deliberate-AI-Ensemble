# Tier 2 Validation Checklist
**Date:** 2026-02-13
**Service Worker Version:** v10
**Purpose:** Validate all Tier 2 features in production

---

## ✅ Pre-Flight Checks

### Environment
- [ ] Production URL accessible: https://deliberateensemble.works
- [ ] Service Worker v10 registered
- [ ] Browser: Chrome/Edge (primary), Firefox/Safari (secondary)
- [ ] DevTools open and ready

---

## 🎯 Feature Validation

### 1. LCP Optimization

**Expected Result:** LCP < 2800ms (target: ~2500ms, was 3351ms)

**Test Steps:**
1. Open DevTools → Lighthouse
2. Run audit (Desktop, Clear storage first)
3. Check "Largest Contentful Paint" metric
4. Verify gradient fades in smoothly after load
5. Check console for: "Gradient applied (post-LCP)"

**Pass Criteria:**
- [ ] LCP < 2800ms
- [ ] Gradient visible and smooth
- [ ] Console log present
- [ ] No layout shifts during gradient application

**Result:**
```
LCP: _____ms
Gradient: YES / NO
Console: YES / NO
Status: PASS / FAIL
```

---

### 2. Integrity Status Indicator

**Expected Result:** Footer badge shows "System Integrity: Verified (12 files)"

**Test Steps:**
1. Scroll to footer on resources.html
2. Check integrity badge color (should be green)
3. Read badge text
4. Open console: `WE4FreeIntegrity.getStatus()`
5. Verify `verified_count: 12`
6. Wait 60 seconds, verify auto-refresh

**Pass Criteria:**
- [ ] Badge visible in footer
- [ ] Badge color: green
- [ ] Text: "System Integrity: Verified (12 files)"
- [ ] Status dot animating
- [ ] Console API returns correct data
- [ ] Auto-updates after 60s

**Result:**
```
Badge: VISIBLE / MISSING
Color: GREEN / YELLOW / RED / BLACK
Text: _______________________
Verified count: ___
Status: PASS / FAIL
```

---

### 3. Emergency Escalation UI

**Expected Result:** Guided fallback through 5 channels with visual progress

**Test Steps:**
1. Navigate to: https://deliberateensemble.works/escalate.html
2. Verify page loads offline (turn on airplane mode)
3. Check "Try Next Option" button present
4. Click button → verify redirect to sms:988 after 1.5s
5. Check channel list shows progress (tried/current/available)
6. Verify "You are safe" reassurance message
7. Check 911 emergency button always visible

**Pass Criteria:**
- [ ] Page loads online
- [ ] Page loads offline
- [ ] All 5 channels listed
- [ ] "Try Next Option" button works
- [ ] Redirect delay is ~1.5s
- [ ] Visual progress tracking works
- [ ] Emergency button always visible
- [ ] Device detection works (skip SMS on desktop)

**Result:**
```
Online load: YES / NO
Offline load: YES / NO
Button works: YES / NO
Progress tracking: YES / NO
Device detection: YES / NO
Status: PASS / FAIL
```

---

### 4. Smart Channel Router

**Expected Result:** Device capabilities detected, channel usage tracked

**Test Steps:**
1. Open resources.html
2. Open console: `WE4FreeChannelRouter.getStatus()`
3. Verify capabilities detected correctly:
   - `is_mobile` (check based on device)
   - `can_call` (should match mobile status)
   - `can_sms` (should match mobile status)
   - `is_online` (should be true)
4. Click a tel: link (e.g., 988)
5. Check console for tracking log
6. Verify IndexedDB entry: `WE4FreeDB.db.sync_status.where('province_code').startsWith('channel_usage').toArray()`

**Pass Criteria:**
- [ ] Status API returns data
- [ ] Capabilities match device
- [ ] Online status correct
- [ ] Tel link clicks tracked
- [ ] IndexedDB stores usage

**Result:**
```
API works: YES / NO
Capabilities: CORRECT / WRONG
Tracking: YES / NO
IndexedDB: WORKING / BROKEN
Status: PASS / FAIL
```

---

### 5. Webchat Fallback

**Expected Result:** Offline-capable form with province auto-fill

**Test Steps:**
1. Navigate to: https://deliberateensemble.works/webchat.html
2. Verify province auto-fills (if previously detected)
3. Fill out form (urgency: urgent, message: "test")
4. Turn on airplane mode
5. Submit form
6. Verify "Message Queued" success message
7. Check IndexedDB: `WE4FreeDB.db.sync_status.where('province_code').startsWith('webchat').toArray()`
8. Verify network status indicator shows offline

**Pass Criteria:**
- [ ] Page loads
- [ ] Province auto-fills
- [ ] Offline indicator works
- [ ] Form submits offline
- [ ] Success message shows
- [ ] IndexedDB stores submission
- [ ] Network status updates

**Result:**
```
Auto-fill: YES / NO
Offline submit: YES / NO
Queue works: YES / NO
IndexedDB: WORKING / BROKEN
Status: PASS / FAIL
```

---

### 6. Conflict Resolver

**Expected Result:** Strategy persists, stats accessible

**Test Steps:**
1. Open console: `WE4FreeConflictResolver.getStats()`
2. Verify returns stats object
3. Change strategy: `WE4FreeConflictResolver.setStrategy('merge')`
4. Reload page
5. Check strategy persisted: `WE4FreeConflictResolver.currentStrategy`
6. Verify should be 'merge'

**Pass Criteria:**
- [ ] Stats API works
- [ ] Strategy change works
- [ ] Strategy persists across reload
- [ ] No console errors

**Result:**
```
Stats API: WORKING / BROKEN
Strategy change: YES / NO
Persistence: YES / NO
Status: PASS / FAIL
```

---

### 7. Service Worker v10

**Expected Result:** v10 active, all files cached, offline works

**Test Steps:**
1. DevTools → Application → Service Workers
2. Verify status: "activated and is running"
3. Check scope: "/" (root)
4. Cache Storage → check "we4free-v10" exists
5. Verify 18+ entries cached (HTML + JS + icons)
6. Turn on airplane mode
7. Navigate to: https://deliberateensemble.works/resources.html
8. Verify page loads completely offline
9. Check console: No fetch errors

**Pass Criteria:**
- [ ] v10 registered
- [ ] v10 activated
- [ ] Cache populated
- [ ] Offline load works
- [ ] No console errors offline

**Result:**
```
Version: v___
Status: ACTIVE / WAITING / ERROR
Cache entries: ___
Offline load: YES / NO
Status: PASS / FAIL
```

---

### 8. Deferred Geolocation

**Expected Result:** Geolocation runs after idle, not blocking render

**Test Steps:**
1. Clear all site data
2. Reload resources.html
3. Check console for timing:
   - "Initialization complete (geolocation deferred)" should come FIRST
   - Geolocation logs should come AFTER
4. Verify no blocking on initial load

**Pass Criteria:**
- [ ] Init message before geolocation
- [ ] Geolocation deferred to idle
- [ ] No blocking observable
- [ ] Console logs in correct order

**Result:**
```
Deferred: YES / NO
Order correct: YES / NO
Status: PASS / FAIL
```

---

### 9. Self-Healing System

**Expected Result:** Checkpoints saved, recovery available

**Test Steps:**
1. Open console: `WE4FreeSelfHealing.saveCheckpoint()`
2. Verify checkpoint saved (no errors)
3. Check IndexedDB: `WE4FreeDB.db.sync_status.get('checkpoint')`
4. Verify checkpoint data exists
5. Check recovery attempts: `WE4FreeSelfHealing.recoveryAttempts`
6. Should be 0 (no failures yet)

**Pass Criteria:**
- [ ] Checkpoint saves successfully
- [ ] IndexedDB stores checkpoint
- [ ] Recovery count accurate
- [ ] No errors in console

**Result:**
```
Checkpoint: SAVED / FAILED
IndexedDB: WORKING / BROKEN
Recovery count: ___
Status: PASS / FAIL
```

---

### 10. IndexedDB Province Cache

**Expected Result:** 13 provinces seeded, emergency numbers present

**Test Steps:**
1. Open console: `WE4FreeDB.db.provinces.count()`
2. Verify returns 13
3. Check: `WE4FreeDB.db.emergency_numbers.count()`
4. Verify returns 8+ (including TTY 711)
5. Get province: `WE4FreeDB.db.provinces.get('BC')`
6. Verify returns British Columbia data

**Pass Criteria:**
- [ ] 13 provinces present
- [ ] 8+ emergency numbers
- [ ] Data structure correct
- [ ] Queries work

**Result:**
```
Province count: ___
Emergency numbers: ___
Queries: WORKING / BROKEN
Status: PASS / FAIL
```

---

## 📊 Overall Results

### Summary
- Total Tests: 10
- Passed: ___
- Failed: ___
- Blocked: ___

### Critical Issues
```
(List any failures that block deployment)
```

### Non-Critical Issues
```
(List any failures that are nice-to-fix)
```

### Performance Metrics
- LCP: _____ms
- Service Worker: v___
- Cache hit rate: ___%
- Offline functionality: ____%

---

## ✅ Go/No-Go Decision

**Criteria for GO:**
- All critical features pass (1-7)
- LCP improved from baseline (3351ms)
- No console errors in normal operation
- Offline mode 100% functional

**Decision:**
- [ ] **GO** - All systems operational, ready for promotion
- [ ] **NO-GO** - Critical issues found, fix before promotion
- [ ] **CONDITIONAL** - Minor issues, document and monitor

**Signatures:**
- Tester: ___________________
- Date: ___________________
- Next Actions: ___________________

---

## 🔧 Bug Template

**For any failures, use this template:**

```
BUG #___: [Short description]

Feature: [Which test section]
Severity: CRITICAL / HIGH / MEDIUM / LOW
Steps to reproduce:
1.
2.
3.

Expected:
Actual:
Console errors:
Screenshots:

Fix required: YES / NO
Workaround available: YES / NO
```

---

**End of Validation**
