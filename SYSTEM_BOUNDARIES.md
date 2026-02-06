# SYSTEM BOUNDARIES

## 1. Purpose
Define what the system does NOT do, preventing scope creep and unsafe behavior.

## 2. Out of Scope
- Live trading by default.
- Automatic configuration changes.
- Strategy optimization or ML training.
- Portfolio rebalancing.
- Multi-asset arbitrage.

## 3. Explicit Non‑Responsibilities
- Managing exchange balances.
- Handling fiat deposits/withdrawals.
- Predicting long-term market trends.
- Running without safety invariants.

## 4. Forbidden Features
- Auto-enabling live mode.
- Bypassing risk manager.
- Executing trades without validation.
- Modifying safety invariants at runtime.

## 5. Human‑Only Actions
- Enabling live mode.
- Adjusting risk parameters.
- Overriding circuit breaker.
- Deploying new agents.

## 6. External Dependencies
- Exchange API availability.
- Market data feed reliability.