# Multi-Agent Trading Bot Configuration File
# Copy this to config.py and customize as needed

# Core Trading Configuration
TRADING_CONFIG = {
    'account_balance': 10000,           # Starting capital in USD
    'paper_trading': True,              # True = simulate, False = LIVE TRADING
    'trading_pairs': ['SOL/USDT', 'BTC/USDT'],  # Pairs to trade
}

# Risk Management (CRITICAL - Do not modify lightly)
RISK_CONFIG = {
    'risk_per_trade': 0.01,             # 1% - NEVER CHANGE THIS
    'min_risk_reward_ratio': 1.5,       # Minimum profit:loss ratio
    'max_daily_loss': 0.05,             # 5% max daily loss
    'account_balance': 10000,           # Same as above
    'min_notional_usd': 10.0,           # Minimum trade value in USD (prevents dust trades)
    'min_position_size_units': 0.001,   # Global minimum position size (in base currency)
    'min_position_size_by_pair': {      # Exchange-specific minimums per trading pair
        'SOL/USDT': 0.1,                # KuCoin minimum: 0.1 SOL
        'BTC/USDT': 0.0001,             # KuCoin minimum: 0.0001 BTC
    },
    'enforce_min_position_size_only': True,  # True = use minimum sizes only (safer for live trading)
}

# Market Analysis
MARKET_CONFIG = {
    'rsi_period': 14,                   # RSI calculation period
    'macd_fast': 12,                    # MACD fast period
    'macd_slow': 26,                    # MACD slow period
    'macd_signal': 9,                   # MACD signal period
    'downtrend_threshold': -5,          # % drop to trigger bearish (-5%)
}

# Backtesting
BACKTEST_CONFIG = {
    'min_win_rate': 0.45,               # Minimum acceptable win rate
    'max_drawdown': 0.15,               # Maximum acceptable drawdown (15%)
}

# Data Fetching
DATA_CONFIG = {
    'cache_timeout': 300,               # 5 minutes between API calls
    'api_timeout': 10,                  # 10 second timeout per API call
}

# Execution
EXECUTION_CONFIG = {
    'paper_trading': True,              # True = paper, False = live
    'max_open_positions': 3,            # Max concurrent open trades
}

# Monitoring & Logging
MONITOR_CONFIG = {
    'logs_dir': './logs',               # Directory for log files
    'enable_alerts': True,              # Console alerts for events
    'alert_level': 'WARNING',           # Minimum alert level
}

# Advanced: Exchange API Configuration
# Only needed if going live trading
EXCHANGE_CONFIG = {
    'exchange': 'binance',              # Exchange name (binance, kucoin, etc)
    'api_key': 'YOUR_API_KEY',         # Your exchange API key
    'api_secret': 'YOUR_API_SECRET',   # Your exchange API secret
    'testnet': True,                    # Use testnet if available
}

# Quick Setup - Use these defaults for most users
QUICK_START_CONFIG = {
    'orchestrator': {},
    'data_fetcher': DATA_CONFIG,
    'market_analyzer': MARKET_CONFIG,
    'risk_manager': RISK_CONFIG,
    'backtester': BACKTEST_CONFIG,
    'executor': EXECUTION_CONFIG,
    'monitor': MONITOR_CONFIG,
}
