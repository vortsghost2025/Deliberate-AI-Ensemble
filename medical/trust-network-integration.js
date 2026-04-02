/**
 * Trust Network Integration
 *
 * Connects WHO data ingestion and federated learning to the medical pipeline.
 * Registers 2 additional agents with the gateway (who-data-agent, federated-learning-agent)
 * bringing the total to 11 medical agents (5 core + 4 clinical + 2 federated).
 *
 * Provides:
 *   - queryWHO(term)           — search WHO data, normalize, return results
 *   - submitLearningUpdate(up) — contribute to federated learning rounds
 *   - processFederatedRequest  — handle gateway messages for federated pipeline
 */

import WHODataFetcher from './who/who-data-fetcher.js';
import {
  normalizeWHOCase,
  normalizeSymptom,
  normalizeLabTest,
  normalizeValue,
  assessDataQuality
} from './who/who-normalizer.js';
import { mapWHOToInternal } from './who/who-mapper.js';
import {
  FederatedLearningCoordinationEngine
} from './intelligence/federated-learning-coordination.js';
import {
  FederatedKnowledgeExchangeEngine
} from './intelligence/federated-knowledge-exchange.js';

// ---------------------------------------------------------------------------
// Agent role constants
// ---------------------------------------------------------------------------

export const FEDERATED_AGENT_ROLES = {
  WHO_DATA: 'WHO_DATA',
  FEDERATED_LEARNING: 'FEDERATED_LEARNING'
};

export const FEDERATED_AGENT_DEFINITIONS = [
  {
    role: FEDERATED_AGENT_ROLES.WHO_DATA,
    name: 'who-data-agent',
    description: 'Fetches, normalizes, and maps WHO surveillance data into the pipeline',
    capabilities: [
      'who-data-fetch',
      'who-data-normalize',
      'who-data-map',
      'who-data-quality-assess'
    ]
  },
  {
    role: FEDERATED_AGENT_ROLES.FEDERATED_LEARNING,
    name: 'federated-learning-agent',
    description: 'Coordinates privacy-preserving federated learning across Trust Network nodes',
    capabilities: [
      'federated-model-management',
      'privacy-preserving-aggregation',
      'knowledge-exchange',
      'training-round-coordination'
    ]
  }
];

// ---------------------------------------------------------------------------
// Module instances (lazily initialized)
// ---------------------------------------------------------------------------

let whoFetcher = null;
let flEngine = null;
let knowledgeExchange = null;
let initialized = false;

// ---------------------------------------------------------------------------
// Initialization
// ---------------------------------------------------------------------------

/**
 * Initialize WHO data fetcher and federated learning coordinator.
 *
 * @param {Object} options
 * @param {Object} [options.who]          — WHODataFetcher options
 * @param {Object} [options.federated]    — FederatedLearningCoordinationEngine options
 * @param {Object} [options.knowledge]    — FederatedKnowledgeExchangeEngine options
 * @returns {Object} status of each module
 */
export function initializeFederatedModules(options = {}) {
  whoFetcher = new WHODataFetcher(options.who || { mockMode: true });

  flEngine = new FederatedLearningCoordinationEngine(options.federated || {
    clusterId: 'trust-network-primary',
    maxVersions: 100
  });

  knowledgeExchange = new FederatedKnowledgeExchangeEngine(options.knowledge || {
    debug: false
  });

  // Seed a default model so the engine is ready for training rounds
  flEngine.createFederatedModel('medical-knowledge-v1', {
    type: 'clinical-decision-support',
    description: 'Federated clinical knowledge model across Trust Network nodes',
    layers: ['symptom-correlation', 'lab-signature', 'protocol-matching'],
    createdAt: Date.now()
  });

  initialized = true;

  return {
    whoFetcher: true,
    federatedLearning: true,
    knowledgeExchange: true,
    defaultModel: 'medical-knowledge-v1'
  };
}

function ensureInitialized() {
  if (!initialized) {
    initializeFederatedModules();
  }
}

// ---------------------------------------------------------------------------
// WHO Data Query
// ---------------------------------------------------------------------------

/**
 * Search WHO data by term and return normalised results.
 *
 * Fetches mock WHO cases, normalises each through the WHO pipeline
 * (normalize → map to internal format), and filters by the search term.
 *
 * @param {string} term — keyword to match against symptoms / diagnoses
 * @param {Object} [options]
 * @param {number} [options.limit=10]      — max cases to fetch
 * @param {string} [options.language='en']  — language for normalisation
 * @returns {Promise<Object>} { results: [...], total, qualitySummary }
 */
export async function queryWHO(term, options = {}) {
  ensureInitialized();

  const limit = options.limit || 10;
  const language = options.language || 'en';

  // 1. Fetch raw WHO cases
  const rawCases = await whoFetcher.fetchCases({ limit });

  // 2. Normalize and map each case
  const processed = rawCases.map(rawCase => {
    const normalized = normalizeWHOCase(rawCase, { language, convertUnits: true });
    const quality = assessDataQuality(normalized);
    const internal = mapWHOToInternal(normalized);
    return { normalized, quality, internal, rawCase };
  });

  // 3. Filter by search term (case-insensitive against symptoms and mapped items)
  const termLower = term.toLowerCase();
  const matched = processed.filter(entry => {
    const searchFields = [
      entry.rawCase.caseId,
      ...(entry.rawCase.symptoms?.list?.map(s => s.term) || []),
      ...(entry.internal.reportedItems || []),
      entry.rawCase.demographics?.chiefComplaint || ''
    ].filter(Boolean);

    return searchFields.some(f => f.toLowerCase().includes(termLower));
  });

  // 4. Quality summary
  const qualities = processed.map(p => p.quality.completeness);
  const avgQuality = qualities.length > 0
    ? qualities.reduce((a, b) => a + b, 0) / qualities.length
    : 0;

  return {
    query: term,
    results: matched.map(m => ({
      caseId: m.rawCase.caseId,
      source: m.rawCase.source,
      demographics: m.rawCase.demographics,
      symptoms: m.rawCase.symptoms,
      laboratoryResults: m.rawCase.laboratoryResults,
      vitals: m.rawCase.vitals,
      quality: m.quality,
      internalFormat: m.internal
    })),
    total: matched.length,
    fetched: rawCases.length,
    qualitySummary: {
      averageCompleteness: avgQuality.toFixed(2),
      totalProcessed: processed.length
    }
  };
}

// ---------------------------------------------------------------------------
// Federated Learning Updates
// ---------------------------------------------------------------------------

/**
 * Submit a learning update to the federated coordinator.
 *
 * Registers a learning node (if new) and contributes its parameters
 * for the next aggregation round.
 *
 * @param {Object} update
 * @param {string} update.nodeId       — unique node identifier
 * @param {Object} update.parameters   — model parameters contributed by the node
 * @param {number} [update.accuracy]   — local model accuracy
 * @returns {Promise<Object>} aggregation result
 */
export async function submitLearningUpdate(update) {
  ensureInitialized();

  const { nodeId, parameters, accuracy = 0 } = update;

  if (!nodeId) {
    return { success: false, error: 'MISSING_NODE_ID' };
  }
  if (!parameters || typeof parameters !== 'object') {
    return { success: false, error: 'MISSING_PARAMETERS' };
  }

  // Register node (idempotent — aggregator handles duplicates)
  flEngine.registerLearningNode(nodeId, {
    ...parameters,
    accuracy,
    submittedAt: Date.now()
  });

  // Conduct a training round with this node
  const roundId = `round-${Date.now()}`;
  const roundResult = flEngine.conductTrainingRound(roundId, [nodeId]);

  return {
    success: roundResult.success,
    nodeId,
    round: roundResult.round || null,
    accuracy: roundResult.accuracy || null,
    error: roundResult.error || null,
    federatedStatus: flEngine.getFederatedStatus()
  };
}

// ---------------------------------------------------------------------------
// Knowledge Exchange helpers
// ---------------------------------------------------------------------------

/**
 * Share a clinical pattern across Trust Network clusters.
 */
export function exchangePattern(patternId, pattern, targetClusters) {
  ensureInitialized();
  return knowledgeExchange.exchangePatternKnowledge(
    patternId,
    pattern,
    targetClusters || ['cluster-primary']
  );
}

/**
 * Get combined status of all federated modules.
 */
export function getFederatedStatus() {
  ensureInitialized();
  return {
    federatedLearning: flEngine.getFederatedStatus(),
    knowledgeExchange: knowledgeExchange.getExchangeStatus(),
    timestamp: Date.now()
  };
}

// ---------------------------------------------------------------------------
// Gateway integration
// ---------------------------------------------------------------------------

/**
 * Get federated agent definitions for gateway registration.
 */
export function getFederatedAgentDefinitions() {
  return FEDERATED_AGENT_DEFINITIONS;
}

/**
 * Handle a federated-request message from the gateway.
 *
 * Supports message subtypes:
 *   - who_query          → queryWHO(term)
 *   - learning_update    → submitLearningUpdate(update)
 *   - pattern_exchange   → exchangePattern(...)
 *   - federated_status   → getFederatedStatus()
 *
 * @param {Object} msg — gateway message
 * @returns {Promise<Object>} response payload
 */
export async function processFederatedRequest(msg) {
  ensureInitialized();

  const requestId = msg.id || msg.requestId || `fed-${Date.now()}`;
  const subtype = msg.subtype || msg.action || 'who_query';
  const payload = msg.data || msg.input || msg.payload || msg;

  try {
    let result;

    switch (subtype) {
      case 'who_query':
        result = await queryWHO(payload.term || payload.query || '', {
          limit: payload.limit || 10,
          language: payload.language || 'en'
        });
        break;

      case 'learning_update':
        result = await submitLearningUpdate({
          nodeId: payload.nodeId,
          parameters: payload.parameters,
          accuracy: payload.accuracy
        });
        break;

      case 'pattern_exchange':
        result = exchangePattern(
          payload.patternId,
          payload.pattern,
          payload.targetClusters
        );
        break;

      case 'federated_status':
        result = getFederatedStatus();
        break;

      default:
        return {
          requestId,
          success: false,
          error: `Unknown federated subtype: ${subtype}`,
          supportedSubtypes: ['who_query', 'learning_update', 'pattern_exchange', 'federated_status']
        };
    }

    return {
      requestId,
      success: true,
      subtype,
      result,
      processedBy: ['who-data-agent', 'federated-learning-agent']
    };
  } catch (error) {
    return {
      requestId,
      success: false,
      error: error.message,
      stack: error.stack
    };
  }
}

export default {
  FEDERATED_AGENT_ROLES,
  FEDERATED_AGENT_DEFINITIONS,
  initializeFederatedModules,
  queryWHO,
  submitLearningUpdate,
  exchangePattern,
  getFederatedStatus,
  getFederatedAgentDefinitions,
  processFederatedRequest
};
