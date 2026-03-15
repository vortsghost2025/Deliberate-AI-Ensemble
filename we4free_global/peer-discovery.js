/**
 * WE4Free Peer Discovery (QR Code System)
 * 
 * Handles peer discovery and connection bootstrapping via QR codes.
 * No signaling servers. No STUN/TURN. Pure offline.
 * 
 * Flow:
 * 1. Peer A creates offer → generates QR code
 * 2. Peer B scans QR code → extracts offer
 * 3. Peer B creates answer → generates QR code
 * 4. Peer A scans QR code → extracts answer
 * 5. Connection established
 * 
 * Optional: Manual code entry (copy/paste for testing)
 * 
 * Usage:
 *   const discovery = new PeerDiscovery(webrtcManager);
 *   const qrCode = await discovery.generateOfferQR();
 *   // Display QR code...
 *   const answer = await discovery.scanOfferQR(qrData);
 *   // Display answer QR code...
 *   await discovery.scanAnswerQR(answerData, peerId);
 */

// ============================================================================
// QR CODE GENERATOR (Simple SVG-based)
// ============================================================================

class QRGenerator {
  /**
   * Generate QR code as data URL
   * Uses qrcode.js library (include in PWA: https://cdn.jsdelivr.net/npm/qrcode@1.5.1/build/qrcode.min.js)
   */
  static async generate(data) {
    if (typeof QRCode === 'undefined') {
      throw new Error('QRCode library not loaded. Include qrcode.js in your HTML.');
    }

    try {
      // Compress data for smaller QR codes
      const compressed = QRGenerator.compress(data);
      const dataUrl = await QRCode.toDataURL(compressed, {
        errorCorrectionLevel: 'M',
        type: 'image/png',
        width: 400,
        margin: 2
      });
      return dataUrl;
    } catch (err) {
      console.error('QR generation failed:', err);
      throw err;
    }
  }

  static compress(data) {
    // Convert to JSON and base64 encode
    const json = JSON.stringify(data);
    return btoa(json);
  }

  static decompress(compressed) {
    // Decode base64 and parse JSON
    const json = atob(compressed);
    return JSON.parse(json);
  }
}

// ============================================================================
// QR CODE SCANNER
// ============================================================================

class QRScanner {
  constructor() {
    this.scanning = false;
    this.stream = null;
    this.video = null;
  }

  /**
   * Start camera and scan for QR codes
   * Uses html5-qrcode library (include in PWA: https://cdn.jsdelivr.net/npm/html5-qrcode@2.3.8/html5-qrcode.min.js)
   */
  async startScan(videoElement, onScan) {
    if (typeof Html5Qrcode === 'undefined') {
      throw new Error('Html5Qrcode library not loaded. Include html5-qrcode.js in your HTML.');
    }

    this.video = videoElement;
    this.scanning = true;

    const scanner = new Html5Qrcode(videoElement.id);
    
    const config = {
      fps: 10,
      qrbox: { width: 250, height: 250 }
    };

    await scanner.start(
      { facingMode: "environment" },
      config,
      (decodedText) => {
        if (this.scanning) {
          try {
            const data = QRGenerator.decompress(decodedText);
            onScan(data);
            this.stopScan(scanner);
          } catch (err) {
            console.error('Failed to decode QR data:', err);
          }
        }
      },
      (errorMessage) => {
        // Scan errors (ignore)
      }
    );

    return scanner;
  }

  async stopScan(scanner) {
    this.scanning = false;
    if (scanner) {
      await scanner.stop();
      await scanner.clear();
    }
  }
}

// ============================================================================
// PEER DISCOVERY
// ============================================================================

class PeerDiscovery {
  constructor(webrtcManager) {
    this.manager = webrtcManager;
    this.scanner = new QRScanner();
    this.pendingConnections = new Map(); // peerId -> { offer, answer, state }
  }

  // ==========================================================================
  // INITIATOR FLOW (Peer A)
  // ==========================================================================

  /**
   * Step 1 (Initiator): Create offer and generate QR code
   */
  async generateOfferQR() {
    const { peerId, offer } = await this.manager.createOffer();
    
    this.pendingConnections.set(peerId, {
      offer,
      answer: null,
      state: 'waiting-for-answer',
      role: 'initiator'
    });

    const qrDataUrl = await QRGenerator.generate(offer);
    
    return {
      peerId,
      offer,
      qrDataUrl,
      offerCode: QRGenerator.compress(offer) // For manual entry
    };
  }

  /**
   * Step 3 (Initiator): Scan answer QR code and complete connection
   */
  async scanAnswerQR(answerData, peerId) {
    const pending = this.pendingConnections.get(peerId);
    if (!pending) {
      throw new Error('No pending connection for this peerId');
    }

    if (pending.role !== 'initiator') {
      throw new Error('Not an initiator for this connection');
    }

    await this.manager.acceptAnswer(peerId, answerData);

    pending.answer = answerData;
    pending.state = 'connected';

    return { peerId, connected: true };
  }

  /**
   * Step 3 (Initiator): Manual answer entry (alternative to QR scan)
   */
  async acceptAnswerCode(answerCode, peerId) {
    const answerData = QRGenerator.decompress(answerCode);
    return this.scanAnswerQR(answerData, peerId);
  }

  // ==========================================================================
  // RESPONDER FLOW (Peer B)
  // ==========================================================================

  /**
   * Step 2 (Responder): Scan offer QR code and generate answer
   */
  async scanOfferQR(offerData) {
    const { peerId, answer } = await this.manager.acceptOffer(offerData);
    
    this.pendingConnections.set(peerId, {
      offer: offerData,
      answer,
      state: 'waiting-for-initiator',
      role: 'responder'
    });

    const qrDataUrl = await QRGenerator.generate(answer);
    
    return {
      peerId,
      answer,
      qrDataUrl,
      answerCode: QRGenerator.compress(answer) // For manual entry
    };
  }

  /**
   * Step 2 (Responder): Manual offer entry (alternative to QR scan)
   */
  async acceptOfferCode(offerCode) {
    const offerData = QRGenerator.decompress(offerCode);
    return this.scanOfferQR(offerData);
  }

  // ==========================================================================
  // CAMERA SCANNING
  // ==========================================================================

  /**
   * Start camera for QR scanning
   */
  async startCameraScan(videoElement, onScan) {
    return this.scanner.startScan(videoElement, onScan);
  }

  /**
   * Stop camera scanning
   */
  async stopCameraScan(scanner) {
    return this.scanner.stopScan(scanner);
  }

  // ==========================================================================
  // STATE MANAGEMENT
  // ==========================================================================

  getPendingConnections() {
    return Array.from(this.pendingConnections.entries()).map(([peerId, data]) => ({
      peerId,
      ...data
    }));
  }

  clearPendingConnection(peerId) {
    this.pendingConnections.delete(peerId);
  }

  clearAllPending() {
    this.pendingConnections.clear();
  }
}

// ============================================================================
// EXPORTS
// ============================================================================

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { PeerDiscovery, QRGenerator, QRScanner };
}

if (typeof window !== 'undefined') {
  window.PeerDiscovery = PeerDiscovery;
  window.QRGenerator = QRGenerator;
  window.QRScanner = QRScanner;
}
