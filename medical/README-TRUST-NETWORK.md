# Trust Network Integration

**Medical Pipeline + WHO Data + Federated Learning**

## Overview

The Trust Network integration connects three major subsystems into a unified medical intelligence platform:

1. **Medical Pipeline** — 5-agent structural processing (ingestion, triage, summarization, risk, output)
2. **Clinical Intelligence** — 4-agent safety-gated clinical analysis (red flags, diagnosis, pattern matching, protocols)
3. **Federated Layer** — 2-agent WHO data ingestion and distributed learning coordination

Total: **11 agents** registered with the Trust Network gateway.

## Architecture

```
                    ┌─────────────────────────┐
                    │   Trust Network Gateway  │
                    │  ws://host:3002          │
                    └────────┬────────────────┘
                             │
                    ┌────────▼────────────────┐
                    │    Gateway Bridge        │
                    │  gateway-bridge.js       │
                    └────────┬────────────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
  ┌────────▼──────┐  ┌──────▼───────┐  ┌──────▼──────────┐
  │ Medical       │  │ Clinical     │  │ Federated /      │
  │ Pipeline      │  │ Intelligence │  │ Trust Network    │
  │ (5 agents)    │  │ (4 agents)   │  │ (2 agents)       │
  └───────────────┘  └──────────────┘  └──────────────────┘
```

## All 11 Agents

### Core Pipeline (5 agents)

| Agent | Role | Responsibilities |
|-------|------|-----------------|
| ingestion-agent | `INGESTION` | Load and normalize raw input data |
| triage-agent | `TRIAGE` | Classify input type and route to processing path |
| summarization-agent | `SUMMARIZATION` | Generate structured summaries and extract fields |
| risk-agent | `RISK` | Apply structural risk scoring |
| output-agent | `OUTPUT` | Format final output and validate invariants |

### Clinical Intelligence (4 agents)

| Agent | Role | Responsibilities |
|-------|------|-----------------|
| red-flag-detector-agent | `RED_FLAG_DETECTOR` | Detects critical red flags requiring immediate intervention (safety gate) |
| diagnosis-engine-agent | `DIAGNOSIS_ENGINE` | Generates ranked differential diagnoses with confidence scores |
| pattern-matcher-agent | `PATTERN_MATCHER` | Matches patient data against known disease patterns |
| protocol-activator-agent | `PROTOCOL_ACTIVATOR` | Activates emergency clinical protocols (DKA, anaphylaxis, trauma, etc.) |

### Federated / Trust Network (2 agents)

| Agent | Role | Responsibilities |
|-------|------|-----------------|
| who-data-agent | `WHO_DATA` | Fetches, normalizes, and maps WHO surveillance data into the pipeline |
| federated-learning-agent | `FEDERATED_LEARNING` | Coordinates privacy-preserving federated learning across Trust Network nodes |

## Gateway Message Formats

### Medical Pipeline Request

Runs the full 5-agent structural pipeline.

```json
{
  "type": "medical_request",
  "id": "req-001",
  "data": {
    "raw": {
      "reportedItems": ["chest pain", "shortness of breath"],
      "severity": "severe"
    },
    "source": "patient-portal"
  }
}
```

### Clinical Request

Runs the 4-agent clinical pipeline (safety-gated).

```json
{
  "type": "clinical_request",
  "id": "clinical-001",
  "data": {
    "demographics": { "age": 58, "sex": "male" },
    "symptoms": {
      "list": [
        { "term": "chest pain", "severity": "severe", "duration": "2 hours" },
        { "term": "shortness of breath", "severity": "moderate" }
      ]
    },
    "vitals": {
      "measurements": [
        { "type": "heart_rate", "value": 110, "unit": "bpm" },
        { "type": "blood_pressure", "value": "90/60", "unit": "mmHg" }
      ]
    }
  }
}
```

### Federated Request (WHO Query)

Fetches WHO data, normalizes it, and returns structured results.

```json
{
  "type": "federated_request",
  "id": "fed-001",
  "subtype": "who_query",
  "data": {
    "term": "chest pain",
    "limit": 10,
    "language": "en"
  }
}
```

### Federated Request (Learning Update)

Contributes a node's model parameters to the federated learning round.

```json
{
  "type": "federated_request",
  "id": "fed-002",
  "subtype": "learning_update",
  "data": {
    "nodeId": "node-clinic-alpha",
    "parameters": {
      "weights": [0.12, 0.87, 0.43],
      "featureImportances": { "chest_pain": 0.92, "troponin": 0.88 }
    },
    "accuracy": 0.89
  }
}
```

### Federated Request (Status)

Returns combined status of federated learning and knowledge exchange.

```json
{
  "type": "federated_request",
  "id": "fed-003",
  "subtype": "federated_status"
}
```

## Example: End-to-End Medical Query

**Input:** Send to gateway:

```json
{
  "type": "federated_request",
  "id": "example-001",
  "subtype": "who_query",
  "data": {
    "term": "Can I take ibuprofen with X medication?",
    "limit": 5
  }
}
```

**Response:**

```json
{
  "type": "agent_response",
  "requestId": "example-001",
  "success": true,
  "pipeline": "federated",
  "subtype": "who_query",
  "result": {
    "query": "Can I take ibuprofen with X medication?",
    "results": [
      {
        "caseId": "WHO-MOCK-1709500000000-0",
        "source": "who-surveillance",
        "demographics": { "age": 55, "sex": "female", "chiefComplaint": "chest pain" },
        "symptoms": {
          "list": [
            { "term": "chest pain", "severity": "severe" },
            { "term": "shortness of breath", "severity": "moderate" }
          ]
        },
        "laboratoryResults": {
          "tests": [
            { "testName": "troponin", "value": 0.85, "unit": "ng/mL", "referenceRange": "< 0.04" }
          ]
        },
        "quality": { "completeness": 0.8, "issues": [], "warnings": [] },
        "internalFormat": {
          "source": "who-surveillance",
          "reportedItems": ["chest pain", "shortness of breath"],
          "severity": "severe"
        }
      }
    ],
    "total": 1,
    "fetched": 5,
    "qualitySummary": { "averageCompleteness": "0.75", "totalProcessed": 5 }
  },
  "agentsExecuted": ["who-data-agent", "federated-learning-agent"]
}
```

## Configuration

### WHO Data Fetcher

By default runs in mock mode with 10 clinical scenario generators. For production:

```javascript
import { initializeFederatedModules } from './trust-network-integration.js';

initializeFederatedModules({
  who: {
    apiEndpoint: 'https://api.who.int/surveillance',
    apiKey: process.env.WHO_API_KEY,
    mockMode: false
  }
});
```

### Federated Learning

The default model `medical-knowledge-v1` is created on initialization. Customize:

```javascript
initializeFederatedModules({
  federated: {
    clusterId: 'clinic-east-cluster',
    maxVersions: 200
  },
  knowledge: {
    debug: true
  }
});
```

## Module Dependencies

```
trust-network-integration.js
├── who/who-data-fetcher.js          (WHODataFetcher)
├── who/who-normalizer.js            (normalizeWHOCase, normalizeSymptom, ...)
├── who/who-mapper.js                (mapWHOToInternal)
├── intelligence/federated-learning-coordination.js  (FederatedLearningCoordinationEngine)
└── intelligence/federated-knowledge-exchange.js     (FederatedKnowledgeExchangeEngine)
```

## Privacy & Compliance

- **Differential Privacy**: All federated learning aggregation applies calibrated noise (epsilon/delta budget)
- **Secure Multi-Party Computation**: Parameter aggregation uses secure-sum with outlier detection
- **No PHI Export**: WHO data is fetched and normalized locally; only aggregated model updates leave the node
- **Privacy Audits**: Every training round generates a compliance audit entry
