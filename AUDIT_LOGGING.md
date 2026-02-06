# AUDIT LOGGING

## 1. Purpose
Provide a complete, immutable record of system actions for traceability, debugging, and compliance.

## 2. Logged Events
- Orchestrator decisions
- Agent outputs
- State transitions
- Trade signals
- Executed trades
- Errors and exceptions
- Invariant violations
- Configuration loads

## 3. Log Requirements
- Timestamped (UTC)
- Structured (JSON)
- Immutable
- Append‑only
- No secrets included
- No PII

## 4. Retention Policy
- 90 days hot storage
- 1 year cold storage
- Delete after 1 year unless flagged

## 5. Access Rules
- Read‑only for all agents
- Write‑only for LoggingAgent
- Full access for Orchestrator

## 6. Philosophy
If it wasn’t logged, it didn’t happen.