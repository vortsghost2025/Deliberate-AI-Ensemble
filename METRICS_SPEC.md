# METRICS SPEC

## 1. Purpose
Define the metrics the system collects to monitor performance, stability, and safety.

## 2. Core Metrics
### Workflow Metrics
- Total workflow duration
- Time spent in each state
- Number of halts
- Number of errors

### Agent Metrics
- Response time per agent
- Error rate per agent
- Validation failure rate

### Safety Metrics
- Invariant violation count
- Circuit breaker activations
- Regime safety triggers

## 3. Metric Properties
- Deterministic collection
- Stable definitions
- Human‑interpretable values

## 4. Metric Use Cases
- Detect performance regressions
- Identify unstable agents
- Monitor system health
- Support long‑term analysis

## 5. Philosophy
Metrics are the heartbeat of the system — steady, reliable, and always telling the truth.