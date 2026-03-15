# Swarm Architecture Refactor Plan

**Status:** Architecture Debt - Known Issue  
**Date:** February 15, 2026  
**Priority:** High (blocks Track 6C distributed compute)

---

## 🔴 Current Problem

**Symptom:** Agents spawn successfully but cannot maintain stable connections.

**Observable behavior:**
- ✅ 7 agents spawn (4 workers, 1 router, 1 observer, 1 coordinator)
- ❌ All 7 agents immediately disconnect
- 🔄 Self-healing attempts infinite reconnection (5 attempts per agent)
- ❌ No jobs can execute (no available agents for task assignment)

**Root cause:** Missing swarm invariants for connection stability.

---

## 🎯 Architectural Invariants Missing

### 1. Stable Agent Identity
- **Current:** Agent identity tied to connection instance (ephemeral)
- **Needed:** Durable agent ID independent of connection state
- **Impact:** Reconnections create "new" agents instead of repairing existing edges

### 2. Single Source of Truth for Membership
- **Current:** Ad-hoc maps scattered across modules
- **Needed:** Canonical SwarmRegistry tracking all agents and connections
- **Impact:** Multiple modules have conflicting views of swarm state

### 3. Explicit Connection State Machine
- **Current:** Binary connected/disconnected
- **Needed:** States: `connecting`, `connected`, `disconnected`, `failed`, `reconnecting`
- **Impact:** Self-healing doesn't know when to retry vs. give up

### 4. Bounded Reconnection
- **Current:** Unbounded retry loops
- **Needed:** Exponential backoff + max attempts + quarantine
- **Impact:** Infinite reconnection attempts consume resources

### 5. Decoupled UI
- **Current:** UI calls connection methods directly
- **Needed:** UI subscribes to registry events only
- **Impact:** UI can trigger connection state inconsistencies

---

## 🏗️ Proposed Architecture

### Module Structure

```
SwarmRegistry (NEW)
  ├─ tracks agents (id, role, state, lastSeen)
  ├─ tracks connections (from, to, state, attempts)
  ├─ emits events: agentAdded, agentRemoved, connectionChanged
  └─ single source of truth

WebRTCManager (REFACTOR)
  ├─ pure edge manager (no swarm logic)
  ├─ takes stable IDs as input
  ├─ maintains state machine per connection
  └─ emits: connectionStateChanged

SwarmSelfHealer (REFACTOR)
  ├─ subscribes to registry events
  ├─ scans for failed/disconnected agents
  ├─ applies bounded reconnection policy
  └─ exponential backoff + max attempts

GossipState (INTEGRATE)
  ├─ propagates membership views between peers
  ├─ reconciles connection intents
  └─ eventual convergence

SwarmCoordinator (REFACTOR)
  ├─ uses registry for all membership queries
  ├─ delegates connection management to WebRTCManager
  └─ focuses on task assignment logic

UI (REFACTOR)
  ├─ subscribes to registry events only
  ├─ never calls connect/disconnect directly
  └─ renders swarm state passively
```

---

## 📋 Refactor Steps

### Step 1: Create SwarmRegistry (NEW FILE)

**File:** `swarm-registry.js`

```javascript
class SwarmRegistry extends EventEmitter {
  constructor() {
    super();
    this.agents = new Map(); // id -> { id, role, state, lastSeen }
    this.connections = new Map(); // `${from}-${to}` -> { from, to, state, attempts, lastAttempt }
  }

  registerAgent(id, role) {
    this.agents.set(id, { id, role, state: 'active', lastSeen: Date.now() });
    this.emit('agent:added', id, role);
  }

  unregisterAgent(id) {
    this.agents.delete(id);
    this.emit('agent:removed', id);
  }

  setConnectionState(fromId, toId, state) {
    const key = `${fromId}-${toId}`;
    const conn = this.connections.get(key) || { from: fromId, to: toId, attempts: 0 };
    conn.state = state;
    conn.lastAttempt = Date.now();
    if (state === 'failed') conn.attempts++;
    this.connections.set(key, conn);
    this.emit('connection:changed', fromId, toId, state);
  }

  getConnectedPeers(agentId) {
    return Array.from(this.connections.entries())
      .filter(([key, conn]) => 
        (conn.from === agentId || conn.to === agentId) && 
        conn.state === 'connected'
      )
      .map(([key, conn]) => conn.from === agentId ? conn.to : conn.from);
  }

  getFailedConnections() {
    return Array.from(this.connections.entries())
      .filter(([key, conn]) => conn.state === 'failed' && conn.attempts < 5)
      .map(([key, conn]) => conn);
  }
}
```

**Priority:** High  
**Estimated time:** 30 minutes

---

### Step 2: Refactor WebRTCManager (MODIFY EXISTING)

**File:** `webrtc-manager.js`

**Changes:**
1. Remove swarm membership logic (no agent spawning)
2. Add connection state machine:
   - `connecting` → `connected` → `disconnected` → `reconnecting` → `failed`
3. Report state changes to registry:
   ```javascript
   onConnectionStateChange(fromId, toId, state) {
     this.registry.setConnectionState(fromId, toId, state);
   }
   ```
4. Accept stable IDs in `connect(fromId, toId)` method

**Functions to modify:**
- `connect()` - add fromId/toId parameters
- `handlePeerConnection()` - report state changes
- `disconnect()` - report to registry

**Priority:** High  
**Estimated time:** 45 minutes

---

### Step 3: Refactor SelfHealingMonitor (MODIFY EXISTING)

**File:** `self-healing.js`

**Changes:**
1. Subscribe to registry events:
   ```javascript
   registry.on('connection:changed', (from, to, state) => {
     if (state === 'disconnected') this.scheduleReconnect(from, to);
   });
   ```
2. Implement bounded reconnection:
   ```javascript
   reconnectLoop() {
     const failed = this.registry.getFailedConnections();
     for (const conn of failed) {
       if (conn.attempts >= 5) continue; // max attempts
       const backoff = Math.min(1000 * Math.pow(2, conn.attempts), 30000);
       if (Date.now() - conn.lastAttempt >= backoff) {
         this.webrtcManager.reconnect(conn.from, conn.to);
       }
     }
   }
   ```
3. Remove agent health pings (registry tracks lastSeen)

**Functions to modify:**
- `checkPeerHealth()` - use registry instead of direct pings
- `reconnectDisconnectedPeers()` - use bounded retry logic
- `rebalanceWorkload()` - query registry for connected peers

**Priority:** High  
**Estimated time:** 30 minutes

---

### Step 4: Integrate SwarmRegistry into SwarmCoordinator

**File:** `swarm-coordinator.js`

**Changes:**
1. Instantiate registry:
   ```javascript
   this.registry = new SwarmRegistry();
   ```
2. Register agents on spawn:
   ```javascript
   spawnAgent(role) {
     const agent = AgentFactory.createAgent(role);
     this.registry.registerAgent(agent.id, role);
     return agent;
   }
   ```
3. Query registry for task assignment:
   ```javascript
   assignTask(task) {
     const workers = Array.from(this.registry.agents.values())
       .filter(a => a.role === 'worker' && a.state === 'active');
     if (workers.length === 0) {
       console.error('❌ No available agents for task assignment');
       return;
     }
     // assign to worker...
   }
   ```

**Functions to modify:**
- `initializeSwarm()` - create registry
- `addAgent()` - register with registry
- `removeAgent()` - unregister from registry
- `getAvailableWorkers()` - query registry

**Priority:** High  
**Estimated time:** 20 minutes

---

### Step 5: Decouple UI from Swarm Logic

**File:** `swarm-ui.html` (inline script)

**Changes:**
1. Subscribe to registry events:
   ```javascript
   window.swarmCoordinator.registry.on('agent:added', (id, role) => {
     this.renderAgentList();
   });
   window.swarmCoordinator.registry.on('connection:changed', (from, to, state) => {
     this.updateHealthStatus();
   });
   ```
2. Remove direct connection calls (no `webrtcManager.connect()` from UI)
3. Render based on registry state only

**Priority:** Medium  
**Estimated time:** 15 minutes

---

### Step 6: Integrate GossipState for Convergence

**File:** `gossip-state.js` (already exists)

**Changes:**
1. Gossip membership data:
   ```javascript
   advertiseAgents() {
     const agents = Array.from(this.registry.agents.values())
       .map(a => ({ id: a.id, role: a.role, lastSeen: a.lastSeen }));
     this.gossip.set('swarm:agents', agents);
   }
   ```
2. Reconcile on gossip receive:
   ```javascript
   onGossipReceived(data) {
     const remoteAgents = data['swarm:agents'] || [];
     for (const agent of remoteAgents) {
       if (!this.registry.agents.has(agent.id)) {
         this.registry.registerAgent(agent.id, agent.role);
         this.webrtcManager.connect(this.localAgentId, agent.id);
       }
     }
   }
   ```

**Priority:** Low (nice-to-have for multi-peer)  
**Estimated time:** 30 minutes

---

## 🧪 Testing Plan

### Test 1: Agent Spawning
- Initialize swarm with 4W, 1R, 1O
- Verify registry contains 7 agents
- Check `registry.agents.size === 7`

### Test 2: Connection Stability
- Wait 30 seconds after spawn
- Verify all agents in `connected` state
- Check `registry.getFailedConnections().length === 0`

### Test 3: Reconnection with Backoff
- Manually disconnect 1 agent
- Verify self-healing attempts reconnection
- Check exponential backoff (1s, 2s, 4s, 8s, 16s)
- Verify max 5 attempts before marking `failed`

### Test 4: Task Assignment
- Submit map/reduce job
- Verify tasks assigned to connected workers
- Check job completes with correct result

### Test 5: UI Consistency
- Check UI reflects registry state
- Verify no console errors about missing agents
- Confirm health status matches registry

---

## 📊 Success Criteria

- ✅ All agents maintain stable connections for >5 minutes
- ✅ Self-healing reconnects within 30 seconds of disconnect
- ✅ No infinite reconnection loops
- ✅ Tasks execute successfully on first attempt
- ✅ UI shows accurate swarm state
- ✅ Zero "no available agents" errors

---

## 🚧 Current Workaround

**For immediate testing:** Use Track 3 (Mesh) instead of Track 6C (Swarm).

The mesh uses simpler peer-to-peer WebRTC without swarm coordination, avoiding the connection stability issues.

**Test mesh at:** `http://localhost:8080/mesh-control-panel.html`

---

## 📝 Notes

This refactor addresses systemic architecture debt, not a surface bug. The swarm was built without explicit connection state management, leading to flapping connections and unreliable task execution.

**Estimated total refactor time:** 2.5-3 hours  
**Recommended approach:** Implement steps 1-4 first (core invariants), test, then add steps 5-6 (polish).

**For WE. For stable swarms. For eventually consistent mesh. 🌐💙**
