# FAILURE MODE ANALYSIS

## 1. Purpose
Identify all known failure modes, their causes, detection methods, and safe responses.

## 2. Failure Mode: Missing Data
- **Cause:** API outage, symbol not found.
- **Detection:** Empty or incomplete dataset.
- **Response:** ERROR → HALTED.

## 3. Failure Mode: Stale Data
- **Cause:** Delayed API response, caching issues.
- **Detection:** Timestamp older than threshold.
- **Response:** ERROR → HALTED.

## 4. Failure Mode: Undefined Regime
- **Cause:** MarketAnalysisAgent cannot classify.
- **Detection:** Regime field missing or invalid.
- **Response:** HALTED.

## 5. Failure Mode: Conflicting Signals
- **Cause:** Agent logic error or corrupted data.
- **Detection:** Signals contradict each other.
- **Response:** ERROR → HALTED.

## 6. Failure Mode: Invalid Backtest Metrics
- **Cause:** Insufficient data or calculation error.
- **Detection:** Missing fields or NaN values.
- **Response:** ERROR → HALTED.

## 7. Failure Mode: Risk Veto
- **Cause:** Unsafe conditions detected.
- **Detection:** Risk agent returns VETO.
- **Response:** HALTED.

## 8. Failure Mode: Execution Error
- **Cause:** API failure, invalid order parameters.
- **Detection:** ExecutionAgent returns error.
- **Response:** ERROR → HALTED.

## 9. Failure Mode: Logging Failure
- **Cause:** File system issues, permission errors.
- **Detection:** LoggingAgent returns error.
- **Response:** ERROR → HALTED.

## 10. Failure Mode: Unexpected Agent Output
- **Cause:** Agent malfunction or bug.
- **Detection:** Missing fields, wrong types.
- **Response:** ERROR → HALTED.

## 11. Failure Mode: Configuration Error
- **Cause:** Invalid or missing config values.
- **Detection:** INIT validation fails.
- **Response:** ERROR → HALTED.