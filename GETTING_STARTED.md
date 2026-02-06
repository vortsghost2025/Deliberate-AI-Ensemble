# Getting Started - Multi-Agent Trading Bot

## What You Have

A production-ready Python trading bot with:
- ✅ 6 specialized autonomous agents
- ✅ Orchestrator coordination layer
- ✅ **Critical safety features** (downtrend protection, 1% risk cap)
- ✅ Paper trading by default
- ✅ Real market data (CoinGecko API)
- ✅ Comprehensive logging

## Quick Start (5 minutes)

### 1. **Verify Installation**
```bash
python main.py
```
You should see output showing all agents initializing and one trading cycle completing.

### 2. **Run Tests**
```bash
python test_agents.py
```
This runs unit tests for each agent and verifies the safety features work.

### 3. **Check Logs**
```bash
type logs\trading_bot.log        # Windows
cat logs/trading_bot.log         # macOS/Linux
```

## How It Works

### The Agent Orchestra

When you run the bot, here's what happens:

```
1. ORCHESTRATOR starts the workflow
   ↓
2. DATA FETCHER retrieves current prices (CoinGecko API)
   ↓
3. MARKET ANALYZER calculates indicators
   ├─ [SAFETY CHECK] Detects bearish market → STOPS if yes
   ↓
4. BACKTESTER validates signals with history
   ↓
5. RISK MANAGER calculates position sizes
   ├─ [SAFETY CHECK] Enforces 1% risk max → REJECTS if violated
   ↓
6. EXECUTOR opens paper trades
   ↓
7. MONITOR logs everything
```

### The Three Safety Layers

1. **Downtrend Protection** (Market Analyzer)
   - Automatically pauses trading in bearish markets
   - Protects you from trading in downtrends

2. **1% Risk Rule** (Risk Manager)
   - NEVER risks more than 1% of account per trade
   - Enforced by code, not just guidelines

3. **Circuit Breaker** (Orchestrator)
   - Emergency stop on critical failures
   - Prevents cascade errors

## Customization

### Change Trading Pairs

Edit `main.py`, find this line:
```python
trading_pairs = ['SOL/USDT', 'BTC/USDT']
```

Change to any supported pairs:
- SOL/USDT (Solana)
- BTC/USDT (Bitcoin)
- ETH/USDT (Ethereum)
- RAY/USDT (Raydium)

### Change Account Balance

Edit `main.py`:
```python
config = {
    'risk_manager': {
        'account_balance': 50000,  # Change this
    }
}
```

### Change Risk Settings

Edit `main.py`:
```python
config = {
    'risk_manager': {
        'risk_per_trade': 0.01,    # 1% per trade (default - don't change)
        'max_daily_loss': 0.10,    # 10% daily max (default is 5%)
    }
}
```

## Understanding the Output

### After running `python main.py`, you'll see:

```
============================================================
  Multi-Agent Autonomous Trading Bot
============================================================

Initializing agents...
[OK] All 6 agents initialized and registered

System Status Report
Orchestrator: idle
Trading Paused: False
Circuit Breaker: False

Agent Status:
  • DataFetchingAgent: idle
  • MarketAnalysisAgent: idle
  • RiskManagementAgent: idle
  • BacktestingAgent: idle
  • ExecutionAgent: idle
  • MonitoringAgent: idle

============================================================
  Starting Trading Cycle
  Symbols: SOL/USDT, BTC/USDT
  Time: 2026-02-03T01:48:08.253490
============================================================

Trade Cycle Results:
Trade Executed: True/False
  Trade ID: 1
  Entry Price: $140.25
  Position Size: 0.0714
  Stop Loss: $137.45
  Take Profit: $150.52

Performance Summary:
  Total Trades: 1
  Win Rate: 100.0%
  Total P&L: $25.00
  Open Positions: 1
```

### Log Files Created

```
logs/
├── trading_bot.log       # Full text logs
└── events.jsonl          # Structured event data
```

View logs:
```bash
# Windows
type logs\trading_bot.log

# macOS/Linux
tail -f logs/trading_bot.log
```

## Example Scenarios

### Scenario 1: Market in Downtrend
- Market Analysis detects -6% decline
- Orchestrator **PAUSES** trading
- No trades executed (safety feature active)

### Scenario 2: Great Signal, Small Account
- Signal detected with 80% confidence
- Account balance: $500
- Max risk: $5
- Position size: ~0.02 units
- Trade accepted (risk within limits)

### Scenario 3: Great Signal, Poor History
- Signal detected but backtesting shows 40% win rate
- Risk Manager: "Historical performance too poor"
- Trade **REJECTED** (performance threshold not met)

### Scenario 4: Max Daily Loss Reached
- Lost 3% on first two trades
- New signal appears
- Risk Manager: "Daily loss limit would be exceeded"
- Trade **REJECTED** (circuit breaker protection)

## Extending the System

### Add a New Agent

Create `agents/my_agent.py`:
```python
from agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self, config=None):
        super().__init__("MyAgent", config)
    
    def execute(self, input_data):
        # Your logic here
        self.logger.info("My agent is running")
        return self.create_message(
            action='my_action',
            success=True,
            data={'result': 'success'}
        )
```

Register in `main.py`:
```python
my_agent = MyAgent(config.get('my_agent', {}))
orchestrator.register_agent(my_agent)
```

### Add Live Trading

1. Install exchange library: `pip install ccxt`
2. Get API key from exchange
3. Modify `ExecutionAgent` to detect live mode
4. Replace paper trading with real orders

## Monitoring Your Bot

### Check Agent Health
```python
# In main.py after execution
status = orchestrator.get_system_status()
print(json.dumps(status, indent=2))
```

### View Trade History
```python
# Get all closed trades
trades = executor.get_trade_history()
print(f"Total trades: {len(trades)}")

# Get open positions
positions = executor.get_open_positions()
print(f"Open positions: {len(positions)}")
```

### Export Event Logs
```python
# Get structured events
events = monitor.export_event_log(limit=100)
```

## Troubleshooting

### Bot runs but no trades execute
1. Check logs: `cat logs/trading_bot.log`
2. Verify trading pairs are valid
3. API might be rate-limited (wait 1 minute)

### Got "Bearish regime detected" message
- Market is in downtrend
- Downtrend protection is working! ✓
- Bot will resume when market recovers

### Got "Daily loss limit exceeded"
- You've lost more than 5% today
- System protects you from over-trading
- Limit resets tomorrow

### Prices showing $0
- CoinGecko API rate limited
- Try again in 1 minute
- Consider running less frequently

## Performance Targets

After paper trading for 1-2 weeks:

✓ **Good**: 50-55% win rate, 1.5:1 risk-reward  
✓ **Excellent**: 55%+ win rate, 2:1 risk-reward  
✗ **Poor**: <45% win rate, <1.5:1 risk-reward

If below targets, adjust:
- Trading pair (try less volatile)
- Market regime filter
- Technical indicator parameters

## Before Going Live

1. **Paper trade for 2-4 weeks minimum**
2. **Verify all safety features work**
3. **Test on small account ($100) first**
4. **Use exchange testnet if available**
5. **Document your strategy**
6. **Have an exit plan ready**

## Safety Checklist

Before enabling live trading:

- [ ] Paper trading runs without errors
- [ ] Win rate > 45%
- [ ] Drawdown stays < 15%
- [ ] Daily loss limit working
- [ ] Downtrend detection working
- [ ] Risk calculations verified
- [ ] Read all code comments
- [ ] Understand each agent's role
- [ ] Backup current configuration
- [ ] Start with 5% of capital

## Next Steps

1. Read [README.md](README.md) for detailed architecture
2. Study each agent in `agents/` directory
3. Run `test_agents.py` to verify system
4. Run `main.py` multiple times to see performance
5. Customize configuration in `config_template.py`
6. Read [SECTION_12_FIRST_LIVE_VALIDATION.md](SECTION_12_FIRST_LIVE_VALIDATION.md) to understand live framework validation (Feb 6, 2026)
7. Scale to live trading (when ready)

## Key Files

- **main.py** - Entry point, configuration
- **agents/orchestrator.py** - Main coordinator
- **agents/base_agent.py** - Agent template
- **requirements.txt** - Dependencies
- **README.md** - Architecture overview
- **SECTION_12_FIRST_LIVE_VALIDATION.md** - Live validation proof
- **test_agents.py** - Test suite
- **logs/trading_bot.log** - Activity log

## Support Resources

- See **README.md** for architecture details
- See **agents/** for individual agent code
- Check **logs/** for debugging info
- Review **test_agents.py** for examples

---

**Happy Trading! Remember: Safety First. 🛡️**
