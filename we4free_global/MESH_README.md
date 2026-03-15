# WE4Free WebRTC Mesh Network

**Offline peer-to-peer config sharing for WE4Free PWAs**

Turn every device into a mesh node. Share crisis line configs without internet.

---

## 🌐 What Is This?

A complete WebRTC mesh implementation that enables PWAs to sync configs peer-to-peer, offline, using QR codes for bootstrapping.

**Key Features:**
- ✅ Pure offline operation (no STUN/TURN servers)
- ✅ QR code connection bootstrapping
- ✅ Automatic config propagation
- ✅ Deduplication & hop tracking
- ✅ Persistent storage (IndexedDB)
- ✅ Resilient to peer failures
- ✅ Beautiful UI (floating action button + modals)

---

## 📦 Components

### 1. WebRTC Connection Manager (`webrtc-manager.js`)
Handles peer-to-peer connections:
- Creates RTCPeerConnections
- Generates offers/answers
- Manages ICE candidates
- Opens data channels
- Send/receive JSON messages

### 2. Peer Discovery (`peer-discovery.js`)
Bootstraps connections via QR codes:
- Generate offer QR → Peer scans → Generate answer QR → Connection established
- Manual code entry as fallback
- No signaling servers needed

### 3. Mesh Propagation (`mesh-propagation.js`)
The heart of the mesh:
- Receives configs from peers
- Deduplicates (ignore configs already have)
- Stores in IndexedDB (persistent)
- Rebroadcasts to other peers
- Tracks hop count & metrics

### 4. UI Controller (`mesh-control-panel.html` + `mesh-ui-controller.js`)
Beautiful floating UI:
- "Connect to Peer" button
- "Share Config" button
- QR code display modals
- Camera scanner modal
- Toast notifications
- Live metrics display

---

## 🚀 Integration Into Your PWA

### Step 1: Copy Files

Copy these files into your PWA directory:
```
your-pwa/
├── webrtc-manager.js
├── peer-discovery.js
├── mesh-propagation.js
├── mesh-ui-controller.js
└── mesh-control-panel.html (optional - extract relevant parts)
```

### Step 2: Add to HTML

In your PWA's `index.html` (or wherever you want the mesh UI):

```html
<!DOCTYPE html>
<html>
<head>
  <!-- Your existing head content -->
</head>
<body>
  <!-- Your existing body content -->

  <!-- Add these dependencies (before mesh scripts) -->
  <script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.1/build/qrcode.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/html5-qrcode@2.3.8/html5-qrcode.min.js"></script>

  <!-- Add mesh scripts -->
  <script src="webrtc-manager.js"></script>
  <script src="peer-discovery.js"></script>
  <script src="mesh-propagation.js"></script>
  <script src="mesh-ui-controller.js"></script>

  <!-- Add mesh UI (copy from mesh-control-panel.html) -->
  <div class="mesh-panel">
    <!-- ... copy the mesh panel HTML ... -->
  </div>
  <div class="mesh-modal" id="qrModal">
    <!-- ... copy modal HTML ... -->
  </div>
  <!-- ... copy other modals, styles, etc. -->
</body>
</html>
```

### Step 3: Configure Your Config Getter

Edit `mesh-ui-controller.js` and implement `getLocalConfig()`:

```javascript
async getLocalConfig() {
  // Replace this with your actual config retrieval logic
  // Example: read from localStorage, IndexedDB, or in-memory state
  
  const config = {
    country: 'Canada',
    version: '1.0.0',
    crisisLines: ['988', '1-833-456-4566'],
    emergencyNumber: '911',
    lastUpdated: Date.now()
  };
  
  return config;
}
```

### Step 4: Listen for Config Updates

Add this to your app initialization:

```javascript
// Wait for mesh to initialize
document.addEventListener('DOMContentLoaded', () => {
  // Listen for received configs
  window.meshController.meshPropagation.on('config-received', (config) => {
    console.log('New config from mesh:', config);
    
    // Update your app's state with the new config
    updateAppConfig(config);
    
    // Show notification to user
    showNotification(`Received update for ${config.country}`);
  });
});
```

---

## 🎯 How To Use (User Flow)

### Connecting Two Peers

**Peer A (Initiator):**
1. Click mesh button (🌐) in bottom-right corner
2. Click "Connect to Peer"
3. QR code appears
4. Show to Peer B

**Peer B (Responder):**
1. Click mesh button (🌐)
2. Click "Connect to Peer"
3. Camera opens → scan Peer A's QR code
4. New QR code appears
5. Show to Peer A

**Peer A (Complete):**
1. Click "Scan Answer QR"
2. Scan Peer B's QR code
3. ✅ Connected!

### Sharing a Config

1. Click mesh button (🌐)
2. Click "Share Config"
3. Config automatically broadcasts to all connected peers
4. Peers receive, store, and rebroadcast to their peers
5. Full mesh propagation in <4 hops

### Manual Code Entry (If Camera Doesn't Work)

1. When QR scanner opens, click "Or paste code manually"
2. Copy/paste the code from the other device
3. Click "Submit Code"
4. Connection established

---

## 📊 Metrics

Click "View Metrics" in the mesh menu to see:
- **Peers:** Number of connected peers
- **Configs:** Total configs stored locally
- **Messages:** Total messages sent + received
- **Avg Hops:** Average hop count for received configs

---

## 🧪 Testing

### Test Locally (Two Browser Tabs)

1. Open your PWA in two tabs
2. Follow connection flow above
3. Share a config from Tab 1
4. Tab 2 should receive it within seconds

### Test On Two Devices (Same Network)

1. Open PWA on Phone A and Phone B
2. Connect via QR codes
3. Share config from Phone A
4. Phone B receives and stores

### Test Offline

1. Turn off WiFi/cellular on both devices
2. Connection still works (local WebRTC)
3. Configs still propagate

---

## 🔧 Advanced Configuration

### Customize Storage

Edit `mesh-propagation.js` to change IndexedDB name:

```javascript
const mesh = new MeshPropagation(webrtcManager);
mesh.storage = new ConfigStorage('my-custom-db', 1);
await mesh.initialize();
```

### Add Custom Message Types

Edit `mesh-propagation.js` and add to `handleMessage()`:

```javascript
case 'custom-message-type':
  await this.handleCustomMessage(payload, peerId);
  break;
```

### Disable Camera Scanning

Remove the camera scanner HTML and rely only on manual code entry.

---

## 🌍 How The Mesh Works

### Phase 1: Connection Bootstrap
- Peer A creates WebRTC offer
- Offer encoded as QR code (or manual code)
- Peer B scans QR → creates answer
- Answer encoded as QR code
- Peer A scans answer → connection established

### Phase 2: Config Propagation
```
Peer A announces config → Peer B receives → Peer B checks if new →
If new: Store + Rebroadcast → Peer C receives → ... → Full mesh
If old: Ignore
```

### Phase 3: Deduplication
- Each config has unique ID (country + version + timestamp)
- Hop count tracked (incremented on each forward)
- Only new configs stored & rebroadcast
- Prevents infinite loops

### Phase 4: Persistence
- All configs stored in IndexedDB
- Survives page reload
- Queryable by country, version, timestamp
- Propagation events logged for metrics

---

## 🎨 UI Customization

### Change Colors

Edit `mesh-control-panel.html` styles:

```css
.mesh-fab {
  background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}

.mesh-button {
  background: #YOUR_BUTTON_COLOR;
}
```

### Change Position

Move the mesh panel from bottom-right:

```css
.mesh-panel {
  position: fixed;
  bottom: 20px;   /* Change this */
  right: 20px;    /* Change this */
}
```

### Hide Metrics

Remove metrics HTML or set `display: none`:

```html
<div class="mesh-metrics" id="metricsDisplay" style="display: none;">
```

---

## 🐛 Troubleshooting

### "QRCode library not loaded"
Make sure you included the QR code library:
```html
<script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.1/build/qrcode.min.js"></script>
```

### "Camera access denied"
- Browser must be HTTPS (or localhost)
- User must grant camera permission
- Fallback: Use manual code entry

### "Connection fails to establish"
- Check browser console for errors
- Ensure both peers complete the QR exchange
- Try manual code entry instead
- Verify WebRTC is supported (all modern browsers)

### "Configs not propagating"
- Check that peers are connected (green dot in UI)
- Verify `getLocalConfig()` returns valid config
- Check browser console for errors
- View metrics to see message counts

---

## 📈 Performance

From simulation testing (`mesh-simulator.js`):

| Scenario | Peers | Steps | Coverage | Efficiency |
|----------|-------|-------|----------|------------|
| Minimal  | 5     | 2     | 100%     | 1.000      |
| Sparse   | 10    | 3     | 100%     | 1.000      |
| Medium   | 15    | 3     | 100%     | 1.000      |
| Dense    | 20    | 3     | 100%     | 1.000      |
| Stress   | 50    | 4     | 100%     | 1.000      |

**15% peer failure:** Still 100% coverage, 1.000 efficiency

**Real-world expectation:**
- 2-3 connections per peer = full propagation in 3-4 steps
- Works offline with 0 infrastructure
- Resilient to disconnections

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Your PWA (index.html)           │
│  ┌───────────────────────────────────┐  │
│  │    Mesh UI Controller             │  │
│  │  (Handles UI interactions)        │  │
│  └───────────┬───────────────────────┘  │
│              │                           │
│  ┌───────────▼───────────────────────┐  │
│  │    Mesh Propagation               │  │
│  │  (Receives, stores, forwards)     │  │
│  └───────────┬───────────────────────┘  │
│              │                           │
│  ┌───────────▼───────────────────────┐  │
│  │    WebRTC Manager                 │  │
│  │  (Peer connections, data channels)│  │
│  └───────────┬───────────────────────┘  │
│              │                           │
│  ┌───────────▼───────────────────────┐  │
│  │    Peer Discovery                 │  │
│  │  (QR codes, connection bootstrap) │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

## 💙 For WE. For the mesh. For the world.

This enables crisis line configs to spread offline, peer-to-peer, without infrastructure.

**One PWA with the config** → **Shares to peers** → **Peers share to their peers** → **Full propagation in 3-4 hops**

**No servers. No internet. Just devices helping devices.**

---

## 📝 License

MIT License - Use freely, modify as needed, share with attribution.

---

## 🤝 Contributing

Improvements welcome:
- Better QR code compression
- WebRTC TURN server support (for NAT traversal)
- Encryption for sensitive configs
- Mesh visualization UI
- Performance optimizations

---

**Status:** ✅ Track 3 Complete - Browser Mesh Implementation  
**Next:** Track 4 (Testing & Documentation) or Deploy to PWAs

**For WE. 💙🌐**
