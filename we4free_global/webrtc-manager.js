/**
 * WE4Free WebRTC Connection Manager
 * 
 * Manages peer-to-peer WebRTC connections for offline config propagation.
 * This is the "socket layer" of the mesh network.
 * 
 * Features:
 * - Creates RTCPeerConnections
 * - Generates offers/answers for manual exchange (QR codes)
 * - Handles ICE candidate gathering
 * - Opens reliable data channels
 * - Send/receive JSON messages
 * - Connection lifecycle management
 * 
 * Usage:
 *   const manager = new WebRTCManager();
 *   manager.on('message', (data, peerId) => console.log('Received:', data));
 *   const offer = await manager.createOffer();
 *   // Exchange offer/answer via QR code...
 *   await manager.acceptAnswer(answer);
 */

// ============================================================================
// EVENT EMITTER (Simple)
// ============================================================================

class EventEmitter {
  constructor() {
    this.events = {};
  }

  on(event, listener) {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(listener);
  }

  off(event, listener) {
    if (!this.events[event]) return;
    this.events[event] = this.events[event].filter(l => l !== listener);
  }

  emit(event, ...args) {
    if (!this.events[event]) return;
    this.events[event].forEach(listener => listener(...args));
  }
}

// ============================================================================
// PEER CONNECTION WRAPPER
// ============================================================================

class PeerConnection extends EventEmitter {
  constructor(peerId, isInitiator = false, fromId = null, toId = null) {
    super();
    this.peerId = peerId;
    this.fromId = fromId; // Stable agent ID (initiator)
    this.toId = toId; // Stable agent ID (responder)
    this.isInitiator = isInitiator;
    this.pc = null;
    this.dataChannel = null;
    this.connected = false;
    this.iceCandidates = [];
    this.offerData = null;
    this.answerData = null;
    
    this.initialize();
  }

  initialize() {
    // Create RTCPeerConnection with no STUN/TURN (works offline)
    this.pc = new RTCPeerConnection({
      iceServers: [] // No servers needed for local/offline connections
    });

    // ICE candidate gathering
    this.pc.onicecandidate = (event) => {
      if (event.candidate) {
        this.iceCandidates.push(event.candidate);
      }
    };

    // Connection state monitoring
    this.pc.onconnectionstatechange = () => {
      const state = this.pc.connectionState;
      console.log(`[Peer ${this.peerId}] Connection state: ${state}`);
      
      if (state === 'connected') {
        this.connected = true;
        this.emit('connected');
      } else if (state === 'disconnected' || state === 'failed' || state === 'closed') {
        this.connected = false;
        this.emit('disconnected');
      }
    };

    // Data channel setup
    if (this.isInitiator) {
      this.createDataChannel();
    } else {
      this.pc.ondatachannel = (event) => {
        this.dataChannel = event.channel;
        this.setupDataChannel();
      };
    }
  }

  createDataChannel() {
    this.dataChannel = this.pc.createDataChannel('we4free-mesh', {
      ordered: true,
      maxRetransmits: 3
    });
    this.setupDataChannel();
  }

  setupDataChannel() {
    this.dataChannel.onopen = () => {
      console.log(`[Peer ${this.peerId}] Data channel open`);
      this.emit('datachannel-open');
    };

    this.dataChannel.onclose = () => {
      console.log(`[Peer ${this.peerId}] Data channel closed`);
      this.emit('datachannel-close');
    };

    this.dataChannel.onerror = (error) => {
      console.error(`[Peer ${this.peerId}] Data channel error:`, error);
      this.emit('error', error);
    };

    this.dataChannel.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.emit('message', data);
      } catch (err) {
        console.error(`[Peer ${this.peerId}] Failed to parse message:`, err);
      }
    };
  }

  async createOffer() {
    if (!this.isInitiator) {
      throw new Error('Only initiator can create offer');
    }

    const offer = await this.pc.createOffer();
    
    // Fix SDP setup attribute for DTLS (offerer should use actpass)
    const fixedOffer = {
      type: offer.type,
      sdp: this.fixSetupAttribute(offer.sdp, 'actpass')
    };
    
    await this.pc.setLocalDescription(fixedOffer);

    // Wait for ICE gathering to complete
    await this.waitForICE();

    // Package offer with ICE candidates
    this.offerData = {
      type: 'offer',
      sdp: this.pc.localDescription.sdp,
      candidates: this.iceCandidates
    };

    return this.offerData;
  }

  async acceptOffer(offerData) {
    if (this.isInitiator) {
      throw new Error('Initiator cannot accept offer');
    }

    const offer = new RTCSessionDescription({
      type: 'offer',
      sdp: offerData.sdp
    });

    await this.pc.setRemoteDescription(offer);

    // Add ICE candidates from offer
    if (offerData.candidates) {
      for (const candidate of offerData.candidates) {
        await this.pc.addIceCandidate(new RTCIceCandidate(candidate));
      }
    }

    // Create answer
    const answer = await this.pc.createAnswer();
    
    // Fix SDP setup attribute for DTLS (answerer should use active)
    const fixedAnswer = {
      type: answer.type,
      sdp: this.fixSetupAttribute(answer.sdp, 'active')
    };
    
    await this.pc.setLocalDescription(fixedAnswer);

    // Wait for ICE gathering
    await this.waitForICE();

    // Package answer with ICE candidates
    this.answerData = {
      type: 'answer',
      sdp: this.pc.localDescription.sdp,
      candidates: this.iceCandidates
    };

    return this.answerData;
  }

  async acceptAnswer(answerData) {
    if (!this.isInitiator) {
      throw new Error('Only initiator can accept answer');
    }

    const answer = new RTCSessionDescription({
      type: 'answer',
      sdp: answerData.sdp
    });

    await this.pc.setRemoteDescription(answer);

    // Add ICE candidates from answer
    if (answerData.candidates) {
      for (const candidate of answerData.candidates) {
        await this.pc.addIceCandidate(new RTCIceCandidate(candidate));
      }
    }
  }

  send(data) {
    if (!this.dataChannel || this.dataChannel.readyState !== 'open') {
      throw new Error('Data channel not open');
    }

    const json = JSON.stringify(data);
    this.dataChannel.send(json);
  }

  fixSetupAttribute(sdp, setupValue) {
    // Fix DTLS setup attribute in SDP
    // This ensures proper setup:actpass (offerer) and setup:active (answerer)
    const lines = sdp.split('\r\n');
    const fixedLines = lines.map(line => {
      if (line.startsWith('a=setup:')) {
        return `a=setup:${setupValue}`;
      }
      return line;
    });
    
    // If no setup attribute found, add it after the first m= line
    let foundSetup = false;
    for (let i = 0; i < fixedLines.length; i++) {
      if (fixedLines[i].startsWith('a=setup:')) {
        foundSetup = true;
        break;
      }
    }
    
    if (!foundSetup) {
      for (let i = 0; i < fixedLines.length; i++) {
        if (fixedLines[i].startsWith('m=')) {
          // Insert setup attribute after m= line
          fixedLines.splice(i + 1, 0, `a=setup:${setupValue}`);
          break;
        }
      }
    }
    
    return fixedLines.join('\r\n');
  }

  close() {
    if (this.dataChannel) {
      this.dataChannel.close();
    }
    if (this.pc) {
      this.pc.close();
    }
    this.connected = false;
  }

  waitForICE() {
    return new Promise((resolve) => {
      // Wait for ICE gathering to complete (or timeout after 5s)
      const checkICE = () => {
        if (this.pc.iceGatheringState === 'complete') {
          resolve();
        } else {
          setTimeout(checkICE, 100);
        }
      };
      
      setTimeout(() => resolve(), 5000); // Timeout fallback
      checkICE();
    });
  }
}

// ============================================================================
// WEBRTC MANAGER
// ============================================================================

class WebRTCManager extends EventEmitter {
  constructor(registry = null) {
    super();
    this.peers = new Map(); // peerId -> PeerConnection
    this.nextPeerId = 0;
    this.registry = registry; // Optional SwarmRegistry for connection state tracking
  }

  // Create an offer to send to another peer (initiator side)
  async createOffer(fromId = null, toId = null) {
    const peerId = this.nextPeerId++;
    const peer = new PeerConnection(peerId, true, fromId, toId);
    
    this.setupPeerEvents(peer);
    this.peers.set(peerId, peer);
    
    // Report connecting state to registry
    if (this.registry && fromId && toId) {
      this.registry.setConnectionState(fromId, toId, window.ConnectionState?.CONNECTING || 'connecting');
    }

    const offer = await peer.createOffer();
    
    return {
      peerId,
      offer
    };
  }

  // Accept an offer from another peer (responder side)
  async acceptOffer(offerData, fromId = null, toId = null) {
    const peerId = this.nextPeerId++;
    const peer = new PeerConnection(peerId, false, fromId, toId);
    
    this.setupPeerEvents(peer);
    this.peers.set(peerId, peer);
    
    // Report connecting state to registry
    if (this.registry && fromId && toId) {
      this.registry.setConnectionState(fromId, toId, window.ConnectionState?.CONNECTING || 'connecting');
    }

    const answer = await peer.acceptOffer(offerData);
    
    return {
      peerId,
      answer
    };
  }

  // Complete connection by accepting answer (initiator side)
  async acceptAnswer(peerId, answerData) {
    const peer = this.peers.get(peerId);
    if (!peer) {
      throw new Error(`Peer ${peerId} not found`);
    }

    await peer.acceptAnswer(answerData);
  }

  // Send message to specific peer
  sendTo(peerId, data) {
    const peer = this.peers.get(peerId);
    if (!peer) {
      throw new Error(`Peer ${peerId} not found`);
    }
    peer.send(data);
  }

  // Broadcast message to all connected peers
  broadcast(data) {
    let sent = 0;
    for (const [peerId, peer] of this.peers.entries()) {
      if (peer.connected && peer.dataChannel?.readyState === 'open') {
        try {
          peer.send(data);
          sent++;
        } catch (err) {
          console.error(`Failed to send to peer ${peerId}:`, err);
        }
      }
    }
    return sent;
  }

  // Disconnect from specific peer
  disconnect(peerId) {
    const peer = this.peers.get(peerId);
    if (peer) {
      peer.close();
      this.peers.delete(peerId);
    }
  }

  // Disconnect from all peers
  disconnectAll() {
    for (const peer of this.peers.values()) {
      peer.close();
    }
    this.peers.clear();
  }

  // Get list of connected peers
  getConnectedPeers() {
    return Array.from(this.peers.entries())
      .filter(([_, peer]) => peer.connected)
      .map(([peerId, peer]) => ({ peerId, connected: peer.connected }));
  }

  setupPeerEvents(peer) {
    peer.on('connected', () => {
      console.log(`✅ Connected to peer ${peer.peerId}`);
      this.emit('peer-connected', peer.peerId);
      
      // Report to registry if available
      if (this.registry && peer.fromId && peer.toId) {
        this.registry.setConnectionState(peer.fromId, peer.toId, window.ConnectionState?.CONNECTED || 'connected');
      }
    });

    peer.on('disconnected', () => {
      console.log(`❌ Disconnected from peer ${peer.peerId}`);
      this.emit('peer-disconnected', peer.peerId);
      
      // Report to registry if available
      if (this.registry && peer.fromId && peer.toId) {
        this.registry.setConnectionState(peer.fromId, peer.toId, window.ConnectionState?.DISCONNECTED || 'disconnected');
      }
    });

    peer.on('message', (data) => {
      this.emit('message', data, peer.peerId);
    });

    peer.on('error', (error) => {
      this.emit('error', error, peer.peerId);
      
      // Report to registry if available
      if (this.registry && peer.fromId && peer.toId) {
        this.registry.setConnectionState(peer.fromId, peer.toId, window.ConnectionState?.FAILED || 'failed');
      }
    });
  }
}

// ============================================================================
// EXPORTS
// ============================================================================

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { WebRTCManager, PeerConnection };
}

if (typeof window !== 'undefined') {
  window.WebRTCManager = WebRTCManager;
  window.PeerConnection = PeerConnection;
}
