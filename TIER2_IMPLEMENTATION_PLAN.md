# Tier 2 Implementation Plan - WE4Free Crisis Infrastructure

## Implementation Order (by dependency and complexity)

### Phase 1: Foundation (Days 1-3)
**1. IndexedDB Province Cache Layer** ✋ START HERE
- Least dependencies, enables all other features
- Use Dexie.js for robust schema management
- Implement province data storage structure
- Add sync engine with exponential backoff
- Files: `db.js`, schema in `province_schema.js`

**2. Integrity Verification Layer**
- SHA-256 verification using Web Crypto API
- Create `integrity.manifest.json` with file hashes
- Add runtime verification to Service Worker
- Files: `integrity.js`, `integrity.manifest.json`, update `sw.js`

### Phase 2: Communication Channels (Days 4-7)
**3. Multi-path Emergency Access - TTY**
- Add TTY/TDD links (tty: URI or relay numbers)
- Update crisis box with TTY option
- File: Update `resources.html` crisis box

**4. Multi-path Emergency Access - Webchat**
- Create simple iframe-based webchat fallback
- Use WebRTC if feasible, otherwise fall back to static contact forms
- Files: `webchat.html`, `webchat.js`

**5. Smart Channel Orchestration**
- Implement fallback logic: tel → SMS → TTY → webchat
- Add device detection and smart routing
- File: `channel_router.js`

### Phase 3: Resilience (Days 8-10)
**6. Self-healing UI Reconstruction**
- Add error boundaries to critical components
- Implement state checkpointing to IndexedDB
- Add automated recovery routines
- Files: `error_boundary.js`, `ui_recovery.js`

**7. Conflict Resolution & Sync**
- Implement last-write-wins for simple data
- Add conflict UI for user resolution when needed
- File: Update `db.js` with conflict resolution

### Phase 4: Testing & Polish (Days 11-14)
**8. Chaos Testing Suite**
- Network failure injection
- Storage corruption scenarios
- Provider outage simulation
- File: `chaos_tests.js`

**9. Accessibility Audit**
- WCAG 2.2 AA compliance check
- Screen reader testing
- Keyboard navigation validation
- File: `accessibility_report.md`

**10. Documentation & Monitoring**
- Local health checks
- Client-side telemetry (opt-in)
- Operational playbooks
- Files: `health_check.js`, `OPERATIONAL_PLAYBOOK.md`

---

## Immediate Next Steps (Right Now)

### 1. IndexedDB Province Cache - Schema Design
```javascript
// Goal: Store province-specific crisis resources offline
const schema = {
  provinces: {
    id: 'province_code', // 'BC', 'ON', 'QC', etc.
    name: 'string',
    emergency_numbers: 'array',
    local_resources: 'array',
    last_updated: 'timestamp',
    version: 'integer'
  },
  sync_status: {
    id: 'auto++',
    province_code: 'string',
    last_sync: 'timestamp',
    pending_updates: 'boolean'
  }
};
```

### 2. Files to Create First
1. `we4free_website/db.js` - Dexie.js wrapper
2. `we4free_website/province_data.json` - Seed data
3. Update `resources.html` to use IndexedDB for offline province data

### 3. Success Criteria for Phase 1
- ✅ Province data loads from IndexedDB when offline
- ✅ Background sync updates data when online
- ✅ No user-facing breakage if IndexedDB fails
- ✅ Console shows sync status: `[WE4Free] Province cache: BC loaded (offline)`

---

## Key Decisions Made

**Why IndexedDB first?**
- Enables all other features (offline multi-path, self-healing state storage)
- Most impact with least risk
- Can be tested independently

**Why TTY before full WebRTC?**
- Accessibility compliance is non-negotiable
- TTY is simpler (just phone numbers + relay info)
- WebRTC is complex, can iterate later

**Why integrity verification early?**
- Protects all future features
- Service Worker already exists, just needs hash checks
- Low implementation cost, high trust value

**Deferred to later:**
- AI-driven UI healing (use heuristics first)
- Full CRDT conflict resolution (use LWW for v1)
- Multi-vendor CPaaS integration (one provider for v1)

---

## Risk Mitigation

**Storage quota exhaustion:**
- Monitor quota usage
- Implement cleanup for stale data
- Fallback to read-only mode if quota hit

**Schema migration failures:**
- Use additive-only migrations
- Test with users stuck offline for weeks
- Provide manual clear cache + re-sync button

**Sync conflicts:**
- Server timestamp wins (LWW)
- Log conflicts for future analysis
- Provide manual refresh button

**Browser compatibility:**
- Feature detect IndexedDB, Web Crypto API
- Progressive enhancement for all features
- Test on iOS Safari, Firefox, Chrome

---

## Starting Now: IndexedDB Implementation

Creating `db.js` with Dexie.js wrapper next...
