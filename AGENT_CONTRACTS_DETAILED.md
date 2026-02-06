# AGENT CONTRACTS — DETAILED SPECIFICATION

## 1. Purpose
Define explicit input/output contracts, edge cases, and failure semantics for every agent.

## 2. Shared Contract Rules
All agents must:
- Accept structured input from the orchestrator.
- Return standardized messages.
- Never assume workflow order.
- Never modify global state.
- Fail safe with clear error messages.

## 3. DataFetcher Contract
### Inputs
- Symbol list
- Timeframe
- Required fields

### Outputs
- Fresh market data
- Metadata (timestamps, completeness)

### Failure Conditions
- Missing data
- Stale data
- API errors

## 4. MarketAnalysisAgent Contract
### Inputs
- Valid market data

### Outputs
- Regime classification
- Signal set
- Confidence metrics

### Failure Conditions
- Undefined regime
- Conflicting signals
- Missing fields

## 5. BacktestingAgent Contract
### Inputs
- Signals
- Market data

### Outputs
- Performance metrics
- Drawdown
- Win/loss ratio

### Failure Conditions
- Insufficient data
- Invalid metrics

## 6. RiskManagementAgent Contract
### Inputs
- Signals
- Backtest metrics
- Regime

### Outputs
- APPROVE or VETO
- Rationale
- Safety flags

### Failure Conditions
- Missing metrics
- Undefined risk state

## 7. ExecutionAgent Contract
### Inputs
- Approved signal
- Position size
- Paper trading credentials

### Outputs
- Execution result
- Order metadata

### Failure Conditions
- API errors
- Invalid order parameters

## 8. LoggingAgent Contract
### Inputs
- Full workflow context

### Outputs
- Audit record

### Failure Conditions
- Write errors

## 9. Philosophy
Each agent is a modular, replaceable component with strict boundaries and predictable behavior.