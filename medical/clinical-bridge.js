/**
 * Clinical Bridge
 *
 * Connects the clinical intelligence layer to the gateway bridge.
 * Registers 4 clinical agents and routes medical queries through
 * a safety-gated pipeline: red-flag detection -> diagnosis -> protocol activation.
 */

import { ClinicalRedFlagDetector } from './clinical-intelligence/red-flag-detector.js';
import { DifferentialDiagnosisEngine } from './clinical-intelligence/differential-diagnosis-engine.js';
import { DiseasePatternMatcher } from './clinical-intelligence/disease-pattern-matcher.js';
import { ProtocolActivatorV2 } from './clinical-intelligence/protocol-activator-v2.js';

export const CLINICAL_AGENT_ROLES = {
  RED_FLAG_DETECTOR: 'RED_FLAG_DETECTOR',
  DIAGNOSIS_ENGINE: 'DIAGNOSIS_ENGINE',
  PATTERN_MATCHER: 'PATTERN_MATCHER',
  PROTOCOL_ACTIVATOR: 'PROTOCOL_ACTIVATOR'
};

export const CLINICAL_AGENT_DEFINITIONS = [
  {
    role: CLINICAL_AGENT_ROLES.RED_FLAG_DETECTOR,
    name: 'red-flag-detector',
    description: 'Detects critical red flags requiring immediate intervention (safety gate)',
    capabilities: ['red-flag-detection', 'safety-screening', 'critical-finding-identification']
  },
  {
    role: CLINICAL_AGENT_ROLES.DIAGNOSIS_ENGINE,
    name: 'diagnosis-engine',
    description: 'Generates ranked differential diagnoses with confidence scores',
    capabilities: ['differential-diagnosis', 'clinical-reasoning', 'diagnostic-scoring']
  },
  {
    role: CLINICAL_AGENT_ROLES.PATTERN_MATCHER,
    name: 'pattern-matcher',
    description: 'Matches patient data against known disease patterns',
    capabilities: ['disease-pattern-matching', 'symptom-cluster-analysis', 'lab-signature-recognition']
  },
  {
    role: CLINICAL_AGENT_ROLES.PROTOCOL_ACTIVATOR,
    name: 'protocol-activator',
    description: 'Activates emergency clinical protocols (DKA, anaphylaxis, trauma, etc.)',
    capabilities: ['protocol-activation', 'emergency-protocols', 'clinical-guidelines']
  }
];

let redFlagDetector = null;
let diagnosisEngine = null;
let patternMatcher = null;
let protocolActivator = null;
let initialized = false;

/**
 * Initialize clinical intelligence modules.
 * Standards data is optional -- modules that require it will be skipped
 * until standards are provided via setClinicalStandards().
 */
export function initializeClinicalModules(standards = null) {
  redFlagDetector = new ClinicalRedFlagDetector();
  protocolActivator = new ProtocolActivatorV2(standards || {});

  if (standards?.rules?.rules?.diseasePatterns) {
    patternMatcher = new DiseasePatternMatcher(
      standards.rules.rules.diseasePatterns,
      standards.rules.rules.labThresholds || {}
    );
    diagnosisEngine = new DifferentialDiagnosisEngine(standards);
  } else {
    patternMatcher = null;
    diagnosisEngine = null;
  }

  initialized = true;
  return {
    redFlagDetector: !!redFlagDetector,
    protocolActivator: !!protocolActivator,
    patternMatcher: !!patternMatcher,
    diagnosisEngine: !!diagnosisEngine
  };
}

/**
 * Set or update clinical standards after initialization.
 * Enables the diagnosis engine and pattern matcher.
 */
export function setClinicalStandards(standards) {
  if (standards?.rules?.rules?.diseasePatterns) {
    patternMatcher = new DiseasePatternMatcher(
      standards.rules.rules.diseasePatterns,
      standards.rules.rules.labThresholds || {}
    );
    diagnosisEngine = new DifferentialDiagnosisEngine(standards);
    return { diagnosisEngine: true, patternMatcher: true };
  }
  return { diagnosisEngine: false, patternMatcher: false };
}

/**
 * Process a clinical query through the safety-gated pipeline.
 *
 * Pipeline order:
 *   1. Red-flag detection (safety gate -- critical flags halt processing)
 *   2. Differential diagnosis (if no blocking flags and standards loaded)
 *   3. Protocol activation (based on patient data and diagnosis)
 *
 * Returns structured clinical analysis with confidence scores.
 */
export async function processClinicalQuery(patientData) {
  if (!initialized) {
    initializeClinicalModules();
  }

  const startTime = performance.now();
  const result = {
    timestamp: new Date().toISOString(),
    redFlags: null,
    differential: null,
    protocols: null,
    safetyGate: { passed: true, criticalFlags: [] },
    confidence: {},
    processingTime: 0
  };

  // Step 1: Red-flag detection (safety gate)
  const flags = redFlagDetector.detectRedFlags(patientData);
  const criticalFlags = flags.filter(f => f.severity === 'critical');

  result.redFlags = {
    total: flags.length,
    critical: criticalFlags.length,
    urgent: flags.filter(f => f.severity === 'urgent').length,
    flags
  };

  if (criticalFlags.length > 0) {
    result.safetyGate.passed = false;
    result.safetyGate.criticalFlags = criticalFlags.map(f => ({
      flag: f.flag,
      action: f.action,
      category: f.category
    }));
  }

  // Step 2: Differential diagnosis (requires standards data)
  if (diagnosisEngine) {
    try {
      const differential = diagnosisEngine.generateDifferential(patientData);
      result.differential = {
        diagnoses: differential.differentials,
        cantMiss: differential.cantMiss,
        workup: differential.workup,
        pearl: differential.pearl,
        summary: differential.summary
      };
      result.confidence.differential = differential.summary.topScore;
    } catch (err) {
      result.differential = { error: err.message };
    }
  }

  // Step 3: Protocol activation
  try {
    const protocolResult = protocolActivator.evaluateProtocolActivation(patientData);
    result.protocols = {
      activated: protocolResult.activatedProtocols,
      primary: protocolResult.primaryProtocol,
      totalEvaluated: Object.keys(protocolResult.allScores).length
    };

    if (protocolResult.primaryProtocol) {
      result.confidence.protocol = protocolResult.primaryProtocol.score;
    }
  } catch (err) {
    result.protocols = { error: err.message };
  }

  // Compute overall confidence
  const confidenceValues = Object.values(result.confidence).filter(v => typeof v === 'number');
  result.confidence.overall = confidenceValues.length > 0
    ? confidenceValues.reduce((a, b) => a + b, 0) / confidenceValues.length
    : 0;

  result.processingTime = performance.now() - startTime;

  return result;
}

/**
 * Get a concise clinical summary from a processed result.
 */
export function getClinicalSummary(analysisResult) {
  const summary = {
    safe: analysisResult.safetyGate.passed,
    criticalAlerts: analysisResult.safetyGate.criticalFlags.length,
    topDiagnosis: null,
    activatedProtocols: 0,
    confidence: analysisResult.confidence.overall
  };

  if (analysisResult.differential?.summary) {
    summary.topDiagnosis = {
      name: analysisResult.differential.summary.topDiagnosis,
      score: analysisResult.differential.summary.topScore,
      total: analysisResult.differential.summary.total
    };
  }

  if (analysisResult.protocols?.activated) {
    summary.activatedProtocols = analysisResult.protocols.activated.length;
  }

  return summary;
}

/**
 * Get all clinical agent definitions for gateway registration.
 */
export function getClinicalAgentDefinitions() {
  return CLINICAL_AGENT_DEFINITIONS;
}

export default {
  CLINICAL_AGENT_ROLES,
  CLINICAL_AGENT_DEFINITIONS,
  initializeClinicalModules,
  setClinicalStandards,
  processClinicalQuery,
  getClinicalSummary,
  getClinicalAgentDefinitions
};
