# Testing Instructions for Edge Claude

**From:** Desktop Claude (Infrastructure Builder)  
**To:** Edge Claude (Browser Tester)  
**Date:** February 15, 2026  
**Mission:** Test Track 2 + Track 3 tools in real browser environment

---

## 🎯 WHAT WAS BUILT (Context)

Desktop Claude just completed Track 2 (Validation/Orchestration) and Track 3 (Browser WebRTC Mesh):

### Track 2 Tools:
1. **validate.js** - Config validator (450 lines)
2. **build-all.js** - Parallel build orchestrator (257 lines)
3. **mesh-simulator.js** - WebRTC mesh simulator (478 lines)

### Track 3 Tools (WHAT YOU'RE TESTING):
1. **webrtc-manager.js** - WebRTC connection manager (390 lines)
2. **peer-discovery.js** - QR code peer discovery (238 lines)
3. **mesh-propagation.js** - Config propagation logic (471 lines)
4. **mesh-ui-controller.js** - UI controller (330 lines)
5. **mesh-control-panel.html** - Complete UI (380 lines)

**Total built:** 2,994 lines across 8 tools  
**Status:** All committed to git (4 commits)

---

## 🧪 YOUR MISSION

Test the **Browser WebRTC Mesh** (Track 3) in a real browser environment.

You have access to:
- ✅ Browser with WebRTC support
- ✅ Camera (for QR scanning)
- ✅ IndexedDB (for storage)
- ✅ Multiple tabs (to simulate peers)

Desktop Claude cannot test in browser. **You can.**

---

## 📋 TEST PLAN

### Test 1: UI Loads Without Errors
**File:** `c:\workspace\we4free_global\mesh-control-panel.html`

**Steps:**
1. Open `mesh-control-panel.html` in Chrome/Edge
2. Open browser console (F12)
3. Check for JavaScript errors
4. Verify these elements appear:
   - 🌐 Floating action button (bottom-right)
   - Click it → Menu should open
   - Menu should have:
     - Status indicator (dot + text)
     - "Connect to Peer" button
     - "Share Config" button
     - "View Metrics" button

**Expected Result:**
- ✅ Page loads
- ✅ No console errors
- ✅ UI elements render correctly
- ✅ Console shows: "✅ Mesh UI Controller initialized"

**Report Back:**
- Screenshot of UI
- Console output (copy/paste)
- Any errors encountered

---

### Test 2: Two-Tab Connection Flow (Core Test)
**Goal:** Simulate two peers connecting via QR codes

**Setup:**
1. Open `mesh-control-panel.html` in **Tab 1**
2. Open `mesh-control-panel.html` in **Tab 2**
3. Position tabs side-by-side

**Flow:**

#### Tab 1 (Initiator):
1. Click 🌐 button → Click "Connect to Peer"
2. QR code modal should appear
3. **Copy the manual code** (click the code box below QR)
4. Leave modal open

#### Tab 2 (Responder):
1. Click 🌐 button → Click "Connect to Peer"
2. Scanner modal should appear
3. Click "Or paste code manually"
4. **Paste Tab 1's code** into input field
5. Click "Submit Code"
6. New QR code should appear (answer)
7. **Copy this answer code**

#### Tab 1 (Complete):
1. Click "Scan Answer QR" button
2. Scanner modal opens
3. Click "Or paste code manually"
4. **Paste Tab 2's answer code**
5. Click "Submit Code"
6. ✅ Should see "Connected to peer" toast

**Expected Results:**
- ✅ Both tabs show status: "Connected to 1 peer(s)"
- ✅ Green dot in status indicator
- ✅ 🌐 button turns green gradient
- ✅ Console in both tabs shows: "✅ Connected to peer X"
- ✅ No errors in console

**Report Back:**
- Screenshots of both tabs (connected state)
- Console output from both tabs
- Any errors or issues

---

### Test 3: Config Propagation
**Goal:** Verify configs propagate between connected peers

**Prerequisites:** Test 2 must be passing (two tabs connected)

**Flow:**

#### Tab 1:
1. Click 🌐 → Click "Share Config"
2. Toast should appear: "📤 Config shared with mesh"
3. Check console for propagation messages

#### Tab 2:
1. Should see toast: "📥 Received config: [country name]"
2. Check console for "New config received" message
3. Click 🌐 → Click "View Metrics"
4. Metrics should show:
   - Peers: 1
   - Configs: 1 (or more)
   - Messages: >0

**Expected Results:**
- ✅ Tab 2 receives config from Tab 1
- ✅ Config stored in IndexedDB (Tab 2)
- ✅ Toast notifications appear
- ✅ Metrics update correctly
- ✅ Console shows propagation events

**Report Back:**
- Screenshots of both tabs (with metrics visible)
- Console output showing propagation
- IndexedDB inspection (open DevTools → Application → IndexedDB → we4free-mesh)

---

### Test 4: Metrics Accuracy
**Goal:** Verify metrics display correctly

**Flow:**
1. After Test 3, click "View Metrics" in both tabs
2. Check these values:
   - **Peers:** Should be 1 (for each tab)
   - **Configs:** Should be ≥1
   - **Messages:** Should be >0
   - **Avg Hops:** Should be a number (likely 1.0 or 1.5)

**Expected Results:**
- ✅ Metrics display
- ✅ Values are non-zero
- ✅ Values make sense (peers = 1, messages > 0)

**Report Back:**
- Screenshot of metrics in both tabs
- Values shown

---

### Test 5: IndexedDB Persistence
**Goal:** Verify configs persist across page reload

**Flow:**
1. After Test 3 (config shared)
2. In Tab 2, check IndexedDB:
   - Open DevTools (F12)
   - Go to: Application → Storage → IndexedDB → we4free-mesh
   - Open "configs" object store
   - Should see at least 1 config entry
3. Refresh Tab 2 (F5)
4. Check IndexedDB again
5. Config should still be there

**Expected Results:**
- ✅ Config visible in IndexedDB before reload
- ✅ Config still there after reload
- ✅ Metrics show correct config count after reload

**Report Back:**
- Screenshot of IndexedDB contents
- Confirmation that persistence works

---

### Test 6: Disconnection Handling
**Goal:** Verify system handles peer disconnection

**Flow:**
1. With two tabs connected (from Test 2)
2. Close Tab 2 completely
3. In Tab 1:
   - Should see toast: "⚠️ Peer disconnected"
   - Status should change to "Offline"
   - 🌐 button should lose green color
   - Metrics: Peers should be 0

**Expected Results:**
- ✅ Disconnection detected
- ✅ UI updates correctly
- ✅ Toast notification appears
- ✅ Metrics reflect disconnection

**Report Back:**
- Screenshot of Tab 1 after disconnection
- Console output

---

### Test 7: QR Code Generation (Visual Verification)
**Goal:** Verify QR codes are generated correctly

**Flow:**
1. Click "Connect to Peer"
2. QR code modal appears
3. Verify:
   - QR code image is visible (not broken)
   - Manual code is displayed below QR
   - Code is copyable (click to copy)

**Expected Results:**
- ✅ QR code renders as image
- ✅ Manual code is base64 string (long alphanumeric)
- ✅ Click to copy works (tooltip or notification)

**Report Back:**
- Screenshot of QR code modal
- Confirmation that manual code is visible

---

### Test 8: Error Handling (Camera Access Denied)
**Goal:** Verify graceful handling when camera is denied

**Flow:**
1. Click "Connect to Peer"
2. When scanner modal opens
3. Deny camera permission (browser should prompt)
4. Should see error toast OR fallback to manual entry

**Expected Results:**
- ✅ Error message appears (toast or console)
- ✅ Manual entry input is still available
- ✅ App doesn't crash

**Report Back:**
- How the app handles camera denial
- Error messages shown
- Whether manual entry still works

---

## 🔍 WHAT TO CHECK IN CONSOLE

Look for these messages (good signs):

```
✅ Mesh UI Controller initialized
✅ Mesh propagation initialized
✅ Connected to peer X
✅ Offer generated, waiting for answer...
✅ Connection established!
✅ Answer generated
📤 Propagated config [ID] to X peer(s)
📥 New config received: [ID] (hop X)
```

**Red flags (report these):**

```
❌ Any errors with stack traces
❌ "Failed to..." messages
❌ Undefined/null reference errors
❌ WebRTC connection failures
```

---

## 📊 SUMMARY REPORT FORMAT

After completing tests, provide this summary:

```markdown
## Track 3 Browser Mesh Test Results

**Tester:** Edge Claude  
**Date:** [Date]  
**Browser:** [Chrome/Edge version]  
**Environment:** [Windows/Mac/Linux]

### Test Results:
- [ ] Test 1: UI Loads - PASS/FAIL
- [ ] Test 2: Two-Tab Connection - PASS/FAIL
- [ ] Test 3: Config Propagation - PASS/FAIL
- [ ] Test 4: Metrics Accuracy - PASS/FAIL
- [ ] Test 5: IndexedDB Persistence - PASS/FAIL
- [ ] Test 6: Disconnection Handling - PASS/FAIL
- [ ] Test 7: QR Code Generation - PASS/FAIL
- [ ] Test 8: Error Handling - PASS/FAIL

### Overall Status:
[X/8 tests passed]

### Critical Issues Found:
[List any blocking issues]

### Minor Issues Found:
[List any non-blocking issues]

### Observations:
[Any unexpected behavior, performance notes, UX feedback]

### Screenshots:
[Attach key screenshots]

### Console Logs:
[Paste relevant console output]

### Recommendation:
✅ READY FOR DEPLOYMENT
⚠️ NEEDS FIXES (list which tests failed)
❌ MAJOR ISSUES (explain)
```

---

## 🚀 BONUS TESTS (If You Have Time)

### Bonus 1: Three-Peer Mesh
- Open three tabs
- Connect Tab 1 ↔ Tab 2
- Connect Tab 2 ↔ Tab 3
- Share config from Tab 1
- Verify Tab 3 receives it (through Tab 2)

### Bonus 2: Rapid Config Sharing
- Connected peers (2 tabs)
- Share config multiple times rapidly
- Verify no duplicates stored
- Check deduplication works

### Bonus 3: Long Session
- Keep two tabs connected for 5-10 minutes
- Share configs periodically
- Verify connection stability
- Check for memory leaks (DevTools → Memory)

---

## 💙 THANKS, EDGE CLAUDE

Desktop Claude built the infrastructure. **You're making it real.**

After testing, report back to Sean with:
1. Summary report (format above)
2. Screenshots (especially working connection)
3. Any bugs/issues found
4. Recommendations for fixes

**This is the moment Track 3 becomes validated.**

**For WE. For the mesh. For the test. 🌐🧪💙**

---

**Files to test:**
- `c:\workspace\we4free_global\mesh-control-panel.html` (main test file)

**Reference docs:**
- `c:\workspace\we4free_global\MESH_README.md` (integration guide)

**Desktop Claude is standing by for any fixes needed.**

**Let's prove this works. 💙**
