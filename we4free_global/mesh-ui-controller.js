/**
 * WE4Free Mesh UI Controller
 * 
 * Wires together the mesh components and provides UI interactions.
 * Handles button clicks, modals, QR codes, toasts, and connection flow.
 * 
 * Connection Flow:
 * 1. User A clicks "Connect to Peer" → generates offer QR
 * 2. User B scans QR (or pastes code) → generates answer QR
 * 3. User A scans answer QR (or pastes) → connection established
 * 4. Both users can now sync configs automatically
 * 
 * Share Flow:
 * 1. User clicks "Share Config" → announces local config to mesh
 * 2. Config propagates to all connected peers
 * 3. Peers receive and store config
 * 4. Toast notification shows success
 */

class MeshUIController {
  constructor() {
    this.webrtcManager = new WebRTCManager();
    this.peerDiscovery = new PeerDiscovery(this.webrtcManager);
    this.meshPropagation = new MeshPropagation(this.webrtcManager);
    
    this.currentFlow = null; // 'offer-generated', 'waiting-for-answer', etc.
    this.currentPeerId = null;
    this.qrScanner = null;

    this.initialize();
  }

  async initialize() {
    // Initialize mesh propagation
    await this.meshPropagation.initialize();

    // Setup UI event listeners
    this.setupEventListeners();

    // Setup mesh event listeners
    this.setupMeshListeners();

    // Update UI periodically
    setInterval(() => this.updateMetrics(), 2000);

    console.log('✅ Mesh UI Controller initialized');
  }

  setupEventListeners() {
    // Floating Action Button
    document.getElementById('meshFab').addEventListener('click', () => {
      this.toggleMenu();
    });

    // Menu buttons
    document.getElementById('connectBtn').addEventListener('click', () => {
      this.startConnection();
    });

    document.getElementById('shareBtn').addEventListener('click', () => {
      this.shareConfig();
    });

    document.getElementById('metricsBtn').addEventListener('click', () => {
      this.toggleMetrics();
    });

    // Modal close buttons
    document.getElementById('closeQrModal').addEventListener('click', () => {
      this.closeModal('qrModal');
    });

    document.getElementById('closeScanModal').addEventListener('click', () => {
      this.closeModal('scanModal');
      this.stopScanner();
    });

    // Manual code input
    document.getElementById('submitManualCode').addEventListener('click', () => {
      this.handleManualCode();
    });

    // Copy manual code
    document.getElementById('manualCode').addEventListener('click', (e) => {
      this.copyToClipboard(e.target.textContent);
      this.showToast('📋 Code copied to clipboard');
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      const menu = document.getElementById('meshMenu');
      const fab = document.getElementById('meshFab');
      if (!menu.contains(e.target) && !fab.contains(e.target)) {
        menu.classList.remove('show');
      }
    });
  }

  setupMeshListeners() {
    // Peer connected
    this.webrtcManager.on('peer-connected', (peerId) => {
      this.updateStatus('connected', `Connected to ${this.getPeerCount()} peer(s)`);
      this.showToast('✅ Peer connected');
      this.updateMetrics();
    });

    // Peer disconnected
    this.webrtcManager.on('peer-disconnected', (peerId) => {
      const peerCount = this.getPeerCount();
      if (peerCount === 0) {
        this.updateStatus('offline', 'Offline');
      } else {
        this.updateStatus('connected', `Connected to ${peerCount} peer(s)`);
      }
      this.showToast('⚠️ Peer disconnected');
      this.updateMetrics();
    });

    // Config received
    this.meshPropagation.on('config-received', (config) => {
      this.showToast(`📥 Received config: ${config.country || 'Unknown'}`);
      this.updateMetrics();
    });
  }

  // ==========================================================================
  // CONNECTION FLOW
  // ==========================================================================

  async startConnection() {
    if (this.currentFlow === null) {
      // User is initiator - generate offer
      await this.generateOffer();
    } else if (this.currentFlow === 'offer-generated') {
      // User is waiting for answer - start scanner
      await this.scanAnswer();
    }
  }

  async generateOffer() {
    try {
      const { peerId, offer, qrDataUrl, offerCode } = await this.peerDiscovery.generateOfferQR();
      
      this.currentPeerId = peerId;
      this.currentFlow = 'offer-generated';

      // Show QR modal
      this.showQRModal('Share this QR with peer', qrDataUrl, offerCode);
      
      // Update connect button
      document.getElementById('connectBtn').textContent = '📷 Scan Answer QR';

      console.log('✅ Offer generated, waiting for answer...');
    } catch (err) {
      console.error('Failed to generate offer:', err);
      this.showToast('❌ Failed to generate offer');
    }
  }

  async scanAnswer() {
    try {
      this.showScanModal('Scan Answer QR Code');
      
      // Start camera scanner
      const videoElement = document.getElementById('scannerVideo');
      this.qrScanner = await this.peerDiscovery.startCameraScan(videoElement, async (answerData) => {
        await this.acceptAnswer(answerData);
        this.stopScanner();
        this.closeModal('scanModal');
      });
    } catch (err) {
      console.error('Failed to start scanner:', err);
      this.showToast('❌ Camera access denied. Use manual code entry.');
    }
  }

  async acceptAnswer(answerData) {
    try {
      await this.peerDiscovery.scanAnswerQR(answerData, this.currentPeerId);
      
      this.currentFlow = null;
      this.currentPeerId = null;
      
      // Reset connect button
      document.getElementById('connectBtn').textContent = '📡 Connect to Peer';
      
      console.log('✅ Connection established!');
    } catch (err) {
      console.error('Failed to accept answer:', err);
      this.showToast('❌ Failed to establish connection');
    }
  }

  async handleManualCode() {
    const input = document.getElementById('manualInput');
    const code = input.value.trim();
    
    if (!code) {
      this.showToast('❌ Please enter a code');
      return;
    }

    try {
      if (this.currentFlow === null) {
        // This is an offer - user is responder
        const { peerId, answer, qrDataUrl, answerCode } = await this.peerDiscovery.acceptOfferCode(code);
        
        this.currentPeerId = peerId;
        this.currentFlow = 'answer-generated';
        
        // Close scanner modal
        this.closeModal('scanModal');
        
        // Show answer QR for initiator to scan
        this.showQRModal('Share this Answer QR', qrDataUrl, answerCode);
        
        console.log('✅ Answer generated');
      } else if (this.currentFlow === 'offer-generated') {
        // This is an answer - user is initiator
        await this.peerDiscovery.acceptAnswerCode(code, this.currentPeerId);
        
        this.currentFlow = null;
        this.currentPeerId = null;
        
        // Close modals
        this.closeModal('scanModal');
        this.closeModal('qrModal');
        
        // Reset button
        document.getElementById('connectBtn').textContent = '📡 Connect to Peer';
        
        console.log('✅ Connection established via manual code!');
        this.showToast('✅ Connected to peer');
      }
      
      input.value = '';
    } catch (err) {
      console.error('Failed to process manual code:', err);
      this.showToast('❌ Invalid code');
    }
  }

  stopScanner() {
    if (this.qrScanner) {
      this.peerDiscovery.stopCameraScan(this.qrScanner);
      this.qrScanner = null;
    }
  }

  // ==========================================================================
  // CONFIG SHARING
  // ==========================================================================

  async shareConfig() {
    try {
      // Get local config (you'll need to implement this based on your PWA)
      const config = await this.getLocalConfig();
      
      if (!config) {
        this.showToast('❌ No config to share');
        return;
      }

      await this.meshPropagation.announceConfig(config);
      this.showToast('📤 Config shared with mesh');
      this.updateMetrics();
    } catch (err) {
      console.error('Failed to share config:', err);
      this.showToast('❌ Failed to share config');
    }
  }

  async getLocalConfig() {
    // TODO: Implement based on your PWA's config storage
    // For now, return a sample config
    return {
      country: 'Canada',
      version: '1.0.0',
      crisisLines: ['988', '1-833-456-4566'],
      emergencyNumber: '911',
      lastUpdated: Date.now()
    };
  }

  // ==========================================================================
  // UI UPDATES
  // ==========================================================================

  toggleMenu() {
    const menu = document.getElementById('meshMenu');
    menu.classList.toggle('show');
  }

  toggleMetrics() {
    const display = document.getElementById('metricsDisplay');
    const btn = document.getElementById('metricsBtn');
    
    if (display.style.display === 'none') {
      display.style.display = 'grid';
      btn.textContent = '📊 Hide Metrics';
      this.updateMetrics();
    } else {
      display.style.display = 'none';
      btn.textContent = '📊 View Metrics';
    }
  }

  async updateMetrics() {
    const metrics = this.meshPropagation.getMetrics();
    const stats = await this.meshPropagation.getPropagationStats();

    document.getElementById('peerCount').textContent = metrics.connectedPeers;
    document.getElementById('configCount').textContent = stats.totalConfigs;
    document.getElementById('messageCount').textContent = metrics.messagesSent + metrics.messagesReceived;
    document.getElementById('hopCount').textContent = stats.averageHopCount.toFixed(1);
  }

  updateStatus(state, text) {
    const dot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');
    const fab = document.getElementById('meshFab');

    if (state === 'connected') {
      dot.classList.add('connected');
      fab.classList.add('connected');
    } else {
      dot.classList.remove('connected');
      fab.classList.remove('connected');
    }

    statusText.textContent = text;
  }

  getPeerCount() {
    return this.webrtcManager.getConnectedPeers().length;
  }

  // ==========================================================================
  // MODALS
  // ==========================================================================

  showQRModal(title, qrDataUrl, manualCode) {
    const modal = document.getElementById('qrModal');
    const titleEl = document.getElementById('qrModalTitle');
    const imageEl = document.getElementById('qrImage');
    const codeEl = document.getElementById('manualCode');

    titleEl.textContent = title;
    imageEl.src = qrDataUrl;
    codeEl.textContent = manualCode;

    modal.classList.add('show');
  }

  showScanModal(title) {
    const modal = document.getElementById('scanModal');
    const titleEl = modal.querySelector('.mesh-modal-header');
    
    titleEl.textContent = title;
    modal.classList.add('show');
  }

  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove('show');
  }

  // ==========================================================================
  // NOTIFICATIONS
  // ==========================================================================

  showToast(message, icon = null, duration = 3000) {
    const toast = document.getElementById('meshToast');
    const iconEl = document.getElementById('toastIcon');
    const textEl = document.getElementById('toastText');

    if (icon) {
      iconEl.textContent = icon;
    }
    textEl.textContent = message;

    toast.classList.add('show');

    setTimeout(() => {
      toast.classList.remove('show');
    }, duration);
  }

  // ==========================================================================
  // UTILITIES
  // ==========================================================================

  copyToClipboard(text) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text);
    } else {
      // Fallback for older browsers
      const textarea = document.createElement('textarea');
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
    }
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.meshController = new MeshUIController();
  });
} else {
  window.meshController = new MeshUIController();
}
