# SECRETS MANAGEMENT

## 1. Purpose
Define how API keys, credentials, and sensitive configuration values are stored, loaded, and rotated.

## 2. Storage Requirements
- Never stored in code
- Never logged
- Never printed
- Stored in environment variables or secure vault
- Accessed only at runtime

## 3. Loading Requirements
- Loaded once at startup
- Validated immediately
- Never cached in agents
- Never passed between agents

## 4. Rotation Policy
- Rotate API keys every 90 days
- Rotate immediately after suspected compromise
- Update documentation after rotation

## 5. Access Rules
- Only DataFetcher and ExecutionAgent may access secrets
- Orchestrator may validate presence, not read values
- All other agents: no access

## 6. Philosophy
Secrets are liabilities — minimize exposure, minimize risk.