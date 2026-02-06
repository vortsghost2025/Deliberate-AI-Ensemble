# CONFIGURATION SCHEMA

## 1. Purpose
Define the structure, required fields, defaults, and safety constraints for system configuration.

## 2. Required Fields
### trading_mode
- Type: string
- Allowed: "paper", "live"
- Default: "paper"

### max_daily_loss
- Type: float
- Range: 0.0–0.10
- Default: 0.05

### position_size_limit
- Type: float
- Range: 0.0–0.02
- Default: 0.01

### api_keys
- Type: object
- Required fields: exchange_key, exchange_secret

## 3. Optional Fields
### log_level
- Type: string
- Allowed: "DEBUG", "INFO", "WARNING", "ERROR"
- Default: "INFO"

### backtest_enabled
- Type: boolean
- Default: true

## 4. Default Values
- Paper mode enabled
- Backtesting enabled
- Risk limits conservative

## 5. Validation Rules
- Live mode requires explicit human confirmation
- Risk parameters must not exceed safe ranges
- API keys must be present for live mode

## 6. Forbidden Values
- max_daily_loss > 0.10
- position_size_limit > 0.02
- trading_mode = "live" without keys

## 7. Safety Constraints
- Config must be validated before workflow starts
- Invalid config triggers circuit breaker