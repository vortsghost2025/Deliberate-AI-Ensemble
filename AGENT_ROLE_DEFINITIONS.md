# AGENT ROLE DEFINITIONS

## 1. Purpose
Define the specific responsibilities, authority limits, and behavioral expectations for each agent in the system.

## 2. DataFetchingAgent
### Responsibilities
- Retrieve market data from configured providers.
- Validate data structure and freshness.

### Authority Limits
- Cannot classify market regime.
- Cannot generate trade signals.

### Required Outputs
- Structured market data.
- `success: True/False` with error details if applicable.

## 3. MarketAnalysisAgent
### Responsibilities
- Analyze market data.
- Classify regime (bullish, neutral, bearish).
- Generate safety flags.

### Authority Limits
- Cannot approve or reject trades.
- Cannot execute trades.

### Required Outputs
- Regime classification.
- Downtrend detection flag.
- Signal recommendations.

## 4. BacktestingAgent
### Responsibilities
- Evaluate signal performance on historical data.
- Provide non-blocking performance metrics.

### Authority Limits
- Cannot veto trades.
- Cannot modify risk parameters.

### Required Outputs
- Backtest metrics.
- Warnings if performance is poor.

## 5. RiskManagementAgent
### Responsibilities
- Assess proposed trade risk.
- Enforce position sizing rules.
- Apply daily loss limits.

### Authority Limits
- Cannot execute trades.
- Cannot override circuit breaker.

### Required Outputs
- `position_approved: True/False`
- Rejection reason.

## 6. ExecutionAgent
### Responsibilities
- Execute validated trades (paper mode).
- Confirm execution results.

### Authority Limits
- Cannot run without risk approval.
- Cannot modify trade instructions.

### Required Outputs
- Execution result message.