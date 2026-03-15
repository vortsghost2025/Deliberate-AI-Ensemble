/**
 * WE4Free - WebRTC P2P File Transfer Prototype
 * 
 * Phase 3 Unlock: Mesh network propagation begins here.
 * 
 * This is a minimal proof-of-concept for offline peer-to-peer
 * transfer of crisis resource configurations using WebRTC.
 * 
 * Use case: Device A has WE4Free Kenya config. Device B has nothing.
 *           They meet offline. A shares config to B via local connection.
 *           B now has crisis resources without internet.
 * 
 * This enables:
 * - Disaster zones (no cell towers)
 * - Refugee camps (no internet)
 * - Remote villages (no infrastructure)
 * - Conflict regions (censored networks)
 */

class WE4FreeP2PTransfer {
  constructor() {
    this.connection = null;
    this.dataChannel = null;
    this.onReceive = null; // Callback for received data
  }

  /**
   * Device A: Sender - Share config with nearby device
   * @param {Object} config - WE4Free country configuration object
   * @returns {Promise<string>} - Connection offer (share via QR/NFC/manual)
   */
  async shareConfig(config) {
    // Create peer connection
    this.connection = new RTCPeerConnection({
      iceServers: [] // No STUN/TURN - local only
    });

    // Create data channel for file transfer
    this.dataChannel = this.connection.createDataChannel('we4free-share', {
      ordered: true // Ensure config arrives intact
    });

    // When channel opens, send the config
    this.dataChannel.onopen = () => {
      console.log('✅ Data channel open - sending config');
      
      // Send as JSON string
      const payload = JSON.stringify({
        type: 'we4free-config',
        version: '1.0.0',
        timestamp: new Date().toISOString(),
        data: config
      });
      
      this.dataChannel.send(payload);
      console.log(`📤 Sent ${payload.length} bytes`);
    };

    // Create connection offer
    const offer = await this.connection.createOffer();
    await this.connection.setLocalDescription(offer);

    // Wait for ICE gathering to complete
    await new Promise(resolve => {
      if (this.connection.iceGatheringState === 'complete') {
        resolve();
      } else {
        this.connection.addEventListener('icegatheringstatechange', () => {
          if (this.connection.iceGatheringState === 'complete') {
            resolve();
          }
        });
      }
    });

    // Return offer as base64 (can encode in QR code)
    const offerString = JSON.stringify(this.connection.localDescription);
    return btoa(offerString);
  }

  /**
   * Device B: Receiver - Accept config from nearby device
   * @param {string} offerBase64 - Connection offer from sender (from QR/NFC/manual)
   * @param {Function} callback - Called when config received: callback(config)
   * @returns {Promise<string>} - Connection answer (send back to sender)
   */
  async receiveConfig(offerBase64, callback) {
    this.onReceive = callback;

    // Create peer connection
    this.connection = new RTCPeerConnection({
      iceServers: [] // No STUN/TURN - local only
    });

    // Listen for data channel from sender
    this.connection.ondatachannel = (event) => {
      this.dataChannel = event.channel;
      
      this.dataChannel.onmessage = (event) => {
        console.log(`📥 Received ${event.data.length} bytes`);
        
        try {
          const payload = JSON.parse(event.data);
          
          if (payload.type === 'we4free-config') {
            console.log('✅ Config received:', payload.data.country);
            
            // Save to IndexedDB for offline access
            this.saveToIndexedDB(payload.data);
            
            // Callback with config
            if (this.onReceive) {
              this.onReceive(payload.data);
            }
          }
        } catch (error) {
          console.error('❌ Failed to parse received data:', error);
        }
      };
    };

    // Parse and apply offer
    const offerString = atob(offerBase64);
    const offer = JSON.parse(offerString);
    await this.connection.setRemoteDescription(offer);

    // Create answer
    const answer = await this.connection.createAnswer();
    await this.connection.setLocalDescription(answer);

    // Wait for ICE gathering
    await new Promise(resolve => {
      if (this.connection.iceGatheringState === 'complete') {
        resolve();
      } else {
        this.connection.addEventListener('icegatheringstatechange', () => {
          if (this.connection.iceGatheringState === 'complete') {
            resolve();
          }
        });
      }
    });

    // Return answer as base64
    const answerString = JSON.stringify(this.connection.localDescription);
    return btoa(answerString);
  }

  /**
   * Complete connection (both devices must call this)
   * @param {string} remoteDescriptionBase64 - Answer from receiver or confirmation from sender
   */
  async completeConnection(remoteDescriptionBase64) {
    const descString = atob(remoteDescriptionBase64);
    const description = JSON.parse(descString);
    await this.connection.setRemoteDescription(description);
    console.log('✅ Connection established');
  }

  /**
   * Save received config to IndexedDB for offline access
   */
  async saveToIndexedDB(config) {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open('we4free-shared-configs', 1);
      
      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains('configs')) {
          db.createObjectStore('configs', { keyPath: 'code' });
        }
      };
      
      request.onsuccess = (event) => {
        const db = event.target.result;
        const transaction = db.transaction(['configs'], 'readwrite');
        const store = transaction.objectStore('configs');
        
        const addRequest = store.put(config);
        addRequest.onsuccess = () => {
          console.log('💾 Config saved to IndexedDB:', config.code);
          resolve();
        };
        addRequest.onerror = reject;
      };
      
      request.onerror = reject;
    });
  }

  /**
   * Close connection
   */
  close() {
    if (this.dataChannel) {
      this.dataChannel.close();
    }
    if (this.connection) {
      this.connection.close();
    }
    console.log('🔌 Connection closed');
  }
}

// Example usage:
async function example() {
  // Device A: Sender
  const sender = new WE4FreeP2PTransfer();
  const myConfig = {
    country: 'Kenya',
    code: 'KE',
    crisis_lines: [/* ... */]
  };
  
  const offerCode = await sender.shareConfig(myConfig);
  console.log('📱 Show this QR code to receiver:', offerCode);
  
  // Receiver scans QR code and sends back answer
  // const answer = await getAnswerFromReceiver();
  // await sender.completeConnection(answer);
  
  // ---
  
  // Device B: Receiver
  const receiver = new WE4FreeP2PTransfer();
  
  // Scan QR code from sender
  // const scannedOffer = scanQRCode();
  
  const answerCode = await receiver.receiveConfig(scannedOffer, (config) => {
    console.log('🎉 Now I have crisis resources for:', config.country);
    // Rebuild UI with new config
    loadCountryConfig(config);
  });
  
  console.log('📱 Show this answer to sender:', answerCode);
  
  // Sender scans answer to complete connection
  // await receiver.completeConnection(confirmationFromSender);
}

/**
 * NEXT STEPS:
 * 
 * 1. QR Code Integration
 *    - Add QR code library (qrcode.js)
 *    - Generate QR from offer/answer strings
 *    - Scan QR with device camera
 * 
 * 2. NFC Transfer (Android)
 *    - Use Web NFC API (if available)
 *    - Tap devices to exchange connection codes
 * 
 * 3. Manual Code Entry
 *    - Show short codes for manual entry
 *    - Fallback when QR/NFC unavailable
 * 
 * 4. Multi-Hop Routing
 *    - Device A → B → C propagation
 *    - Store received configs
 *    - Re-share to other devices
 *    - Version tracking to prevent loops
 * 
 * 5. Security Layer
 *    - Sign configs with private key
 *    - Verify signature before accepting
 *    - Web of trust model
 * 
 * 6. Update Propagation
 *    - Version vectors for conflict resolution
 *    - Merge strategies for config updates
 *    - Ensure latest crisis lines propagate
 * 
 * LIMITATIONS:
 * - Requires HTTPS or localhost (WebRTC security)
 * - Both devices must have compatible browsers
 * - Limited range (same WiFi network or Bluetooth)
 * - No internet required once PWA cached
 * 
 * UNLOCKS:
 * - Offline distribution in disaster zones
 * - Censorship-resistant resource sharing
 * - Rural/remote area accessibility
 * - Refugee camp deployment without infrastructure
 */

// Export for use in PWA
if (typeof module !== 'undefined' && module.exports) {
  module.exports = WE4FreeP2PTransfer;
}
