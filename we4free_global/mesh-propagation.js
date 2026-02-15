/**
 * WE4Free Mesh Config Propagation
 * 
 * Ports the simulator logic to real WebRTC connections.
 * Handles config distribution, deduplication, and rebroadcasting.
 * 
 * Message Types:
 * - config-announce: "I have config X"
 * - config-request: "Send me config X"
 * - config-update: "Here is config X"
 * - config-list: "I have configs: [A, B, C]"
 * 
 * Propagation Rules (from simulator):
 * - If config is new → store → rebroadcast to all peers
 * - If config is old → ignore
 * - Track hop count to measure propagation distance
 * - Log all messages for metrics
 * 
 * Storage:
 * - IndexedDB for config persistence
 * - Survives page reload
 * - Queryable by country, version, timestamp
 * 
 * Usage:
 *   const mesh = new MeshPropagation(webrtcManager);
 *   await mesh.initialize();
 *   mesh.on('config-received', (config) => console.log('New config:', config));
 *   mesh.announceConfig(myConfig);
 */

// ============================================================================
// INDEXEDDB STORAGE
// ============================================================================

class ConfigStorage {
  constructor(dbName = 'we4free-mesh', version = 1) {
    this.dbName = dbName;
    this.version = version;
    this.db = null;
  }

  async initialize() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };

      request.onupgradeneeded = (event) => {
        const db = event.target.result;

        // Configs store
        if (!db.objectStoreNames.contains('configs')) {
          const configStore = db.createObjectStore('configs', { keyPath: 'id' });
          configStore.createIndex('country', 'country', { unique: false });
          configStore.createIndex('version', 'version', { unique: false });
          configStore.createIndex('receivedAt', 'receivedAt', { unique: false });
        }

        // Propagation log store
        if (!db.objectStoreNames.contains('propagation-log')) {
          const logStore = db.createObjectStore('propagation-log', { autoIncrement: true });
          logStore.createIndex('configId', 'configId', { unique: false });
          logStore.createIndex('timestamp', 'timestamp', { unique: false });
        }
      };
    });
  }

  async saveConfig(config) {
    const transaction = this.db.transaction(['configs'], 'readwrite');
    const store = transaction.objectStore('configs');
    
    const configData = {
      id: config.id || this.generateConfigId(config),
      ...config,
      receivedAt: config.receivedAt || Date.now()
    };

    return new Promise((resolve, reject) => {
      const request = store.put(configData);
      request.onsuccess = () => resolve(configData);
      request.onerror = () => reject(request.error);
    });
  }

  async getConfig(configId) {
    const transaction = this.db.transaction(['configs'], 'readonly');
    const store = transaction.objectStore('configs');

    return new Promise((resolve, reject) => {
      const request = store.get(configId);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async hasConfig(configId) {
    const config = await this.getConfig(configId);
    return config !== undefined;
  }

  async getAllConfigs() {
    const transaction = this.db.transaction(['configs'], 'readonly');
    const store = transaction.objectStore('configs');

    return new Promise((resolve, reject) => {
      const request = store.getAll();
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async deleteConfig(configId) {
    const transaction = this.db.transaction(['configs'], 'readwrite');
    const store = transaction.objectStore('configs');

    return new Promise((resolve, reject) => {
      const request = store.delete(configId);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async logPropagation(event) {
    const transaction = this.db.transaction(['propagation-log'], 'readwrite');
    const store = transaction.objectStore('propagation-log');
    
    const logEntry = {
      ...event,
      timestamp: Date.now()
    };

    return new Promise((resolve, reject) => {
      const request = store.add(logEntry);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async getPropagationLogs(configId = null, limit = 100) {
    const transaction = this.db.transaction(['propagation-log'], 'readonly');
    const store = transaction.objectStore('propagation-log');

    if (configId) {
      const index = store.index('configId');
      const request = index.getAll(configId, limit);
      return new Promise((resolve, reject) => {
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });
    } else {
      const request = store.getAll();
      return new Promise((resolve, reject) => {
        request.onsuccess = () => {
          const results = request.result;
          resolve(results.slice(-limit)); // Last N entries
        };
        request.onerror = () => reject(request.error);
      });
    }
  }

  generateConfigId(config) {
    // Generate unique ID from country + version
    const str = `${config.country}-${config.version || '1.0.0'}-${Date.now()}`;
    return btoa(str).replace(/[^a-zA-Z0-9]/g, '').substring(0, 16);
  }
}

// ============================================================================
// MESH PROPAGATION
// ============================================================================

class MeshPropagation {
  constructor(webrtcManager) {
    this.manager = webrtcManager;
    this.storage = new ConfigStorage();
    this.listeners = {};
    this.messagesSent = 0;
    this.messagesReceived = 0;
    this.configsReceived = 0;
    this.configsPropagated = 0;
    this.initialized = false;

    this.setupWebRTCListeners();
  }

  async initialize() {
    await this.storage.initialize();
    this.initialized = true;
    console.log('✅ Mesh propagation initialized');
  }

  setupWebRTCListeners() {
    // Handle incoming messages
    this.manager.on('message', async (data, peerId) => {
      this.messagesReceived++;
      await this.handleMessage(data, peerId);
    });

    // Handle peer connections
    this.manager.on('peer-connected', async (peerId) => {
      console.log(`📡 Peer ${peerId} connected - syncing configs`);
      await this.syncWithPeer(peerId);
    });

    this.manager.on('peer-disconnected', (peerId) => {
      console.log(`📡 Peer ${peerId} disconnected`);
    });
  }

  // ==========================================================================
  // MESSAGE HANDLING
  // ==========================================================================

  async handleMessage(data, peerId) {
    const { type, payload } = data;

    switch (type) {
      case 'config-announce':
        await this.handleConfigAnnounce(payload, peerId);
        break;
      
      case 'config-request':
        await this.handleConfigRequest(payload, peerId);
        break;
      
      case 'config-update':
        await this.handleConfigUpdate(payload, peerId);
        break;
      
      case 'config-list':
        await this.handleConfigList(payload, peerId);
        break;
      
      default:
        console.warn(`Unknown message type: ${type}`);
    }
  }

  async handleConfigAnnounce(payload, peerId) {
    const { configId } = payload;
    const hasConfig = await this.storage.hasConfig(configId);

    if (!hasConfig) {
      // Request the full config
      this.send(peerId, {
        type: 'config-request',
        payload: { configId }
      });
    }
  }

  async handleConfigRequest(payload, peerId) {
    const { configId } = payload;
    const config = await this.storage.getConfig(configId);

    if (config) {
      this.send(peerId, {
        type: 'config-update',
        payload: { config }
      });
    }
  }

  async handleConfigUpdate(payload, peerId) {
    const { config } = payload;
    const configId = config.id || this.storage.generateConfigId(config);
    config.id = configId;

    const hasConfig = await this.storage.hasConfig(configId);

    if (!hasConfig) {
      // NEW CONFIG! Store and propagate
      const hopCount = (config._hopCount || 0) + 1;
      config._hopCount = hopCount;
      config._receivedFrom = peerId;
      config._receivedAt = Date.now();

      await this.storage.saveConfig(config);
      this.configsReceived++;

      console.log(`✅ New config received: ${configId} (hop ${hopCount})`);

      // Log propagation event
      await this.storage.logPropagation({
        event: 'received',
        configId,
        peerId,
        hopCount
      });

      // Emit event
      this.emit('config-received', config);

      // Rebroadcast to other peers (excluding sender)
      await this.propagateConfig(config, peerId);
    }
  }

  async handleConfigList(payload, peerId) {
    const { configIds } = payload;
    const myConfigs = await this.storage.getAllConfigs();
    const myConfigIds = new Set(myConfigs.map(c => c.id));

    // Find configs we don't have
    const missingConfigIds = configIds.filter(id => !myConfigIds.has(id));

    // Request missing configs
    for (const configId of missingConfigIds) {
      this.send(peerId, {
        type: 'config-request',
        payload: { configId }
      });
    }

    // Announce configs they don't have
    const theirConfigIds = new Set(configIds);
    const newConfigIds = myConfigs
      .filter(c => !theirConfigIds.has(c.id))
      .map(c => c.id);

    for (const configId of newConfigIds) {
      this.send(peerId, {
        type: 'config-announce',
        payload: { configId }
      });
    }
  }

  // ==========================================================================
  // CONFIG PROPAGATION
  // ==========================================================================

  async propagateConfig(config, excludePeerId = null) {
    const connectedPeers = this.manager.getConnectedPeers();
    let sent = 0;

    for (const { peerId } of connectedPeers) {
      if (peerId !== excludePeerId) {
        try {
          this.send(peerId, {
            type: 'config-update',
            payload: { config }
          });
          sent++;
        } catch (err) {
          console.error(`Failed to propagate to peer ${peerId}:`, err);
        }
      }
    }

    if (sent > 0) {
      this.configsPropagated++;
      await this.storage.logPropagation({
        event: 'propagated',
        configId: config.id,
        peers: sent
      });
      console.log(`📤 Propagated config ${config.id} to ${sent} peer(s)`);
    }

    return sent;
  }

  async announceConfig(config) {
    const configId = config.id || this.storage.generateConfigId(config);
    config.id = configId;
    config._hopCount = config._hopCount || 0;
    config._createdAt = Date.now();

    // Save locally
    await this.storage.saveConfig(config);

    // Announce to all peers
    this.broadcast({
      type: 'config-announce',
      payload: { configId }
    });

    console.log(`📢 Announced config: ${configId}`);
    return configId;
  }

  // ==========================================================================
  // PEER SYNCHRONIZATION
  // ==========================================================================

  async syncWithPeer(peerId) {
    const configs = await this.storage.getAllConfigs();
    const configIds = configs.map(c => c.id);

    this.send(peerId, {
      type: 'config-list',
      payload: { configIds }
    });
  }

  // ==========================================================================
  // MESSAGING
  // ==========================================================================

  send(peerId, message) {
    this.manager.sendTo(peerId, message);
    this.messagesSent++;
  }

  broadcast(message) {
    const sent = this.manager.broadcast(message);
    this.messagesSent += sent;
    return sent;
  }

  // ==========================================================================
  // EVENTS
  // ==========================================================================

  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  }

  emit(event, ...args) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => callback(...args));
    }
  }

  // ==========================================================================
  // METRICS
  // ==========================================================================

  getMetrics() {
    return {
      messagesSent: this.messagesSent,
      messagesReceived: this.messagesReceived,
      configsReceived: this.configsReceived,
      configsPropagated: this.configsPropagated,
      connectedPeers: this.manager.getConnectedPeers().length
    };
  }

  async getPropagationStats() {
    const logs = await this.storage.getPropagationLogs();
    const configs = await this.storage.getAllConfigs();

    return {
      totalConfigs: configs.length,
      totalPropagationEvents: logs.length,
      averageHopCount: configs.length > 0
        ? configs.reduce((sum, c) => sum + (c._hopCount || 0), 0) / configs.length
        : 0,
      logs: logs.slice(-20) // Last 20 events
    };
  }
}

// ============================================================================
// EXPORTS
// ============================================================================

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { MeshPropagation, ConfigStorage };
}

if (typeof window !== 'undefined') {
  window.MeshPropagation = MeshPropagation;
  window.ConfigStorage = ConfigStorage;
}
