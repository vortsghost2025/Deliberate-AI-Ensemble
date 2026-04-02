#!/usr/bin/env node
/**
 * GATEWAY BRIDGE
 * Connects the medical pipeline to the Kilo gateway WebSocket.
 *
 * Registers 11 medical agents with the gateway (5 core + 4 clinical + 2 federated)
 * and routes incoming messages through the pipeline, returning processed results.
 *
 * Usage:
 *   node gateway-bridge.js
 *   GATEWAY_URL=ws://host:port node gateway-bridge.js
 */

import { WebSocket } from 'ws';
import { createMedicalOrchestrator } from './medical-workflows.js';
import { AGENT_ROLES, getAgentCapabilities } from './medical-agent-roles.js';
import {
  initializeClinicalModules,
  processClinicalQuery,
  getClinicalAgentDefinitions,
  CLINICAL_AGENT_ROLES
} from './clinical-bridge.js';
import {
  initializeFederatedModules,
  processFederatedRequest,
  getFederatedAgentDefinitions,
  FEDERATED_AGENT_ROLES
} from './trust-network-integration.js';

const GATEWAY_URL = process.env.GATEWAY_URL || 'ws://187.77.3.56:3002';
const RECONNECT_DELAY_MS = 5000;
const HEARTBEAT_INTERVAL_MS = 30000;

const AGENT_DEFINITIONS = [
  { role: AGENT_ROLES.INGESTION, name: 'ingestion', description: 'Load and normalize raw input data' },
  { role: AGENT_ROLES.TRIAGE, name: 'triage', description: 'Classify input type and route to processing path' },
  { role: AGENT_ROLES.SUMMARIZATION, name: 'summarization', description: 'Generate structured summaries and extract fields' },
  { role: AGENT_ROLES.RISK, name: 'risk', description: 'Apply structural risk scoring' },
  { role: AGENT_ROLES.OUTPUT, name: 'output', description: 'Format final output and validate invariants' },
  // Clinical intelligence agents
  ...getClinicalAgentDefinitions().map(def => ({
    role: def.role,
    name: def.name,
    description: def.description,
    capabilities: def.capabilities
  })),
  // Federated / Trust Network agents
  ...getFederatedAgentDefinitions().map(def => ({
    role: def.role,
    name: def.name,
    description: def.description,
    capabilities: def.capabilities
  }))
];

let orchestrator = null;
let ws = null;
let heartbeatTimer = null;
let reconnectTimer = null;
let shuttingDown = false;
let pendingRequests = new Map();

function log(level, message, data = null) {
  const timestamp = new Date().toISOString();
  const prefix = `[GatewayBridge ${timestamp}]`;
  const line = data ? `${prefix} ${message} ${JSON.stringify(data)}` : `${prefix} ${message}`;
  if (level === 'error') {
    console.error(line);
  } else {
    console.log(line);
  }
}

function buildAgentId(role) {
  return `medical-${role.toLowerCase()}`;
}

function connect() {
  if (shuttingDown) return;
  log('info', `Connecting to gateway at ${GATEWAY_URL}...`);

  ws = new WebSocket(GATEWAY_URL);

  ws.on('open', () => {
    log('info', 'Connected to gateway');
    registerAgents();
    startHeartbeat();
  });

  ws.on('message', (raw) => {
    let msg;
    try {
      msg = JSON.parse(raw.toString());
    } catch (err) {
      log('error', 'Failed to parse gateway message', { error: err.message });
      return;
    }
    handleMessage(msg);
  });

  ws.on('close', (code, reason) => {
    log('info', 'Gateway connection closed', { code, reason: reason.toString() });
    stopHeartbeat();
    scheduleReconnect();
  });

  ws.on('error', (err) => {
    log('error', 'Gateway WebSocket error', { error: err.message });
  });
}

function send(msg) {
  if (!ws || ws.readyState !== WebSocket.OPEN) {
    log('error', 'Cannot send message, socket not open');
    return false;
  }
  ws.send(JSON.stringify(msg));
  return true;
}

function registerAgents() {
  for (const def of AGENT_DEFINITIONS) {
    const coreCaps = getAgentCapabilities(def.role);
    const capabilities = coreCaps ? coreCaps.tasks : (def.capabilities || []);
    const source = Object.values(FEDERATED_AGENT_ROLES).includes(def.role)
      ? 'trust-network'
      : Object.values(CLINICAL_AGENT_ROLES).includes(def.role)
      ? 'clinical-intelligence'
      : 'medical-pipeline';
    const registration = {
      type: 'agent_register',
      agent: {
        id: buildAgentId(def.role),
        name: def.name,
        role: def.role,
        capabilities,
        description: def.description,
        version: '1.0.0',
        source
      }
    };
    log('info', `Registering agent: ${def.name}`, { id: registration.agent.id });
    send(registration);
  }

  send({
    type: 'bridge_ready',
    agents: AGENT_DEFINITIONS.map(d => buildAgentId(d.role)),
    pipeline: 'medical',
    source: 'gateway-bridge'
  });
}

function handleMessage(msg) {
  const msgType = msg.type;

  switch (msgType) {
    case 'agent_request':
    case 'medical_request':
    case 'request':
      handlePipelineRequest(msg);
      break;

    case 'clinical_request':
      handleClinicalRequest(msg);
      break;

    case 'federated_request':
      handleFederatedRequest(msg);
      break;

    case 'agent_query':
      handleAgentQuery(msg);
      break;

    case 'ping':
      send({ type: 'pong', timestamp: new Date().toISOString() });
      break;

    case 'pong':
      break;

    case 'ack':
    case 'registered':
      log('info', 'Gateway acknowledged', { type: msgType, id: msg.id || msg.agentId });
      break;

    case 'error':
      log('error', 'Gateway error', { error: msg.error, details: msg.details });
      break;

    default:
      log('info', `Unhandled message type: ${msgType}`, { id: msg.id });
      break;
  }
}

async function handlePipelineRequest(msg) {
  const requestId = msg.id || msg.requestId || `req-${Date.now()}`;
  const inputData = msg.data || msg.input || msg.payload || msg;

  log('info', `Processing pipeline request`, { requestId });

  try {
    const result = await orchestrator.executePipeline(inputData);

    const response = {
      type: 'agent_response',
      requestId,
      success: true,
      result: result.output,
      processingTime: result.processingTime,
      agentsExecuted: result.state.processedBy.length,
      auditLog: result.auditLog
    };

    log('info', `Pipeline complete for request`, {
      requestId,
      processingTime: result.processingTime,
      agents: result.state.processedBy.join(' -> ')
    });

    send(response);
  } catch (error) {
    log('error', `Pipeline failed for request`, {
      requestId,
      error: error.message
    });

    send({
      type: 'agent_response',
      requestId,
      success: false,
      error: error.message,
      stack: error.stack
    });
  }
}

async function handleClinicalRequest(msg) {
  const requestId = msg.id || msg.requestId || `clinical-${Date.now()}`;
  const patientData = msg.data || msg.input || msg.payload || msg;

  log('info', `Processing clinical request`, { requestId });

  try {
    const analysis = await processClinicalQuery(patientData);

    const response = {
      type: 'agent_response',
      requestId,
      success: true,
      pipeline: 'clinical',
      result: {
        safetyGate: analysis.safetyGate,
        redFlags: analysis.redFlags,
        differential: analysis.differential,
        protocols: analysis.protocols,
        confidence: analysis.confidence,
        processingTime: analysis.processingTime
      },
      agentsExecuted: [
        'red-flag-detector',
        ...(analysis.differential ? ['diagnosis-engine', 'pattern-matcher'] : []),
        'protocol-activator'
      ]
    };

    log('info', `Clinical analysis complete`, {
      requestId,
      safetyGate: analysis.safetyGate.passed ? 'passed' : 'BLOCKED',
      criticalFlags: analysis.redFlags.critical,
      processingTime: analysis.processingTime
    });

    send(response);
  } catch (error) {
    log('error', `Clinical request failed`, {
      requestId,
      error: error.message
    });

    send({
      type: 'agent_response',
      requestId,
      success: false,
      pipeline: 'clinical',
      error: error.message,
      stack: error.stack
    });
  }
}

async function handleFederatedRequest(msg) {
  const requestId = msg.id || msg.requestId || `federated-${Date.now()}`;

  log('info', `Processing federated request`, { requestId });

  try {
    const result = await processFederatedRequest(msg);

    const response = {
      type: 'agent_response',
      requestId,
      success: result.success,
      pipeline: 'federated',
      subtype: result.subtype,
      result: result.result,
      agentsExecuted: result.processedBy || ['who-data-agent', 'federated-learning-agent']
    };

    log('info', `Federated request complete`, {
      requestId,
      subtype: result.subtype,
      success: result.success
    });

    send(response);
  } catch (error) {
    log('error', `Federated request failed`, {
      requestId,
      error: error.message
    });

    send({
      type: 'agent_response',
      requestId,
      success: false,
      pipeline: 'federated',
      error: error.message,
      stack: error.stack
    });
  }
}

function handleAgentQuery(msg) {
  const requestId = msg.id || msg.requestId || `query-${Date.now()}`;
  const targetAgent = msg.agent || msg.agentId;
  const agentDef = AGENT_DEFINITIONS.find(d => buildAgentId(d.role) === targetAgent || d.name === targetAgent);

  if (!agentDef) {
    send({
      type: 'agent_response',
      requestId,
      success: false,
      error: `Unknown agent: ${targetAgent}`,
      availableAgents: AGENT_DEFINITIONS.map(d => buildAgentId(d.role))
    });
    return;
  }

  const coreCaps = getAgentCapabilities(agentDef.role);
  const capabilities = coreCaps ? coreCaps : { tasks: agentDef.capabilities || [] };

  send({
    type: 'agent_response',
    requestId,
    success: true,
    agent: buildAgentId(agentDef.role),
    role: agentDef.role,
    capabilities,
    status: 'active'
  });
}

function startHeartbeat() {
  stopHeartbeat();
  heartbeatTimer = setInterval(() => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      send({ type: 'heartbeat', timestamp: new Date().toISOString(), agents: AGENT_DEFINITIONS.length });
    }
  }, HEARTBEAT_INTERVAL_MS);
}

function stopHeartbeat() {
  if (heartbeatTimer) {
    clearInterval(heartbeatTimer);
    heartbeatTimer = null;
  }
}

function scheduleReconnect() {
  if (shuttingDown) return;
  if (reconnectTimer) return;

  log('info', `Reconnecting in ${RECONNECT_DELAY_MS}ms...`);
  reconnectTimer = setTimeout(() => {
    reconnectTimer = null;
    connect();
  }, RECONNECT_DELAY_MS);
}

function shutdown(signal) {
  log('info', `Received ${signal}, shutting down...`);
  shuttingDown = true;
  stopHeartbeat();
  if (reconnectTimer) {
    clearTimeout(reconnectTimer);
    reconnectTimer = null;
  }
  if (ws) {
    ws.close(1000, 'shutdown');
  }
  process.exit(0);
}

// Bootstrap
orchestrator = createMedicalOrchestrator();
const clinicalStatus = initializeClinicalModules();
const federatedStatus = initializeFederatedModules();
log('info', 'Medical pipeline orchestrator initialized');
log('info', 'Clinical intelligence modules initialized', clinicalStatus);
log('info', 'Federated / Trust Network modules initialized', federatedStatus);
log('info', 'Pipeline order:', { order: orchestrator.pipelineOrder });
log('info', 'Total agents:', { count: AGENT_DEFINITIONS.length });
log('info', 'Gateway URL:', { url: GATEWAY_URL });

process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));

connect();
