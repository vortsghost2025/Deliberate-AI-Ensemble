# DATA FLOW OVERVIEW

## 1. Purpose
Describe how data moves through the system from input to execution.

## 2. High-Level Flow
Market Data → DataFetcher → MarketAnalysisAgent → Orchestrator → RiskManager → Executor → Exchange (paper mode)

## 3. Stage-by-Stage Breakdown

### Stage 1: Data Fetching
- Input: Exchange API
- Output: Structured market data
- Validation: Missing/invalid data triggers circuit breaker

### Stage 2: Market Analysis
- Input: Market data
- Output: Regime, signals, safety flags
- Validation: Bearish regime triggers pause

### Stage 3: Backtesting (Optional)
- Input: Signals
- Output: Performance metrics
- Validation: Warnings only

### Stage 4: Risk Assessment
- Input: Proposed trade
- Output: Approval or veto
- Validation: Hard veto stops execution

### Stage 5: Execution
- Input: Validated trade
- Output: Execution result
- Validation: Paper mode enforced

### Stage 6: Logging
- Input: All stages
- Output: Full audit trail

## 4. Data Validation Points
- DataFetcher: API success
- MarketAnalysis: Regime classification
- RiskManager: Position sizing
- Executor: Session limits

## 5. Failure Points and Fallbacks
- Any failure → circuit breaker
- Missing data → halt
- Invalid agent output → halt

## 6. Logging Points
- Every stage logs inputs, outputs, and decisions.