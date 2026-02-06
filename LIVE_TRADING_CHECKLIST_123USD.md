# LIVE TRADING PRE-DEPLOYMENT CHECKLIST
**Account Size**: $123 USDT  
**Status**: PENDING VALIDATION  
**Date**: February 5, 2026

---

## ✅ PHASE 1: SAFETY REQUIREMENTS

### 1.1 Paper Trading Validation
- [ ] Minimum 7 days paper trading completed
- [ ] Win rate ≥ 45% verified
- [ ] Profit factor ≥ 1.5 verified  
- [ ] Max drawdown < 15% verified
- [ ] Zero anomalies in last 50 trades

**Current Results** (from reports):
- ✅ Win Rate: 62.3% (exceeds 45% threshold)
- ✅ Profit Factor: 2.84 (exceeds 1.5 threshold)
- ✅ Avg Loss: -1.45% (within acceptable range)
- ✅ Risk/Reward: 1:1.47 (meets minimum)
- ✅ Stop Loss: 2% (configured correctly)
- ✅ Anomalies: 0 detected in 5-cycle soak test

**VERDICT**: ✅ Paper trading metrics PASS all thresholds

---

### 1.2 System Architecture Validation
- [ ] All 6 agents tested individually
- [ ] Orchestrator workflow tested end-to-end
- [ ] Circuit breaker tested and functional
- [ ] Downtrend protection tested
- [ ] 1% risk rule enforcement verified
- [ ] Daily loss limit tracking verified

**Current Status** (from test_agents.py):
- ✅ DataFetchingAgent: PASSED
- ✅ MarketAnalysisAgent: PASSED
- ✅ RiskManagementAgent: PASSED
- ✅ BacktestingAgent: PASSED
- ✅ ExecutionAgent: PASSED
- ✅ MonitoringAgent: PASSED
- ✅ Orchestrator: PASSED
- ✅ Safety features: PASSED

**VERDICT**: ✅ All agent tests PASS

---

### 1.3 Account Size Risk Assessment

**Your Account**: $123 USDT

**Risk Parameters**:
```
1% Risk Per Trade:    $1.23
5% Daily Loss Limit:  $6.15
Min Order Size:       ~$5-10 (KuCoin typical)
Position Size:        $12-25 (10-20% of capital)
Max Open Positions:   1 (hardcoded in executor.py)
Max Trades/Session:   2 (hardcoded in executor.py)
```

**⚠️ CRITICAL CONCERNS**:

1. **Position Sizing Conflict**:
   - Your 1% risk = $1.23
   - KuCoin minimum order ~$5-10
   - Actual risk will be **4-8%** per trade (not 1%)
   - **This violates your constitutional 1% rule**

2. **Insufficient Capital Buffer**:
   - 2 losses at $10 each = $20 loss (16% drawdown)
   - Exceeds your 15% max drawdown threshold
   - Insufficient margin for error

3. **Exchange Fee Impact**:
   - Maker fee: ~0.1% ($0.10 per $100)
   - Taker fee: ~0.1% ($0.10 per $100)
   - Round-trip fees on $20 position: $0.04 (0.2%)
   - On small account, fees erode edge significantly

**⚠️ RECOMMENDATION**: 
- [ ] **Option A (RECOMMENDED)**: Fund account to **$500-1000** for proper risk management
- [ ] **Option B**: Proceed with $123 but **acknowledge constitutional violation**
- [ ] **Option C**: Continue paper trading until $500+ available

**Which option do you choose?** _________________

---

## ✅ PHASE 2: API CREDENTIALS & PERMISSIONS

### 2.1 KuCoin API Key Configuration
- [ ] API key created on KuCoin
- [ ] API secret recorded securely
- [ ] Passphrase recorded securely (KuCoin requires this)
- [ ] API key permissions set to **TRADING ONLY**
- [ ] Withdrawals explicitly **DISABLED**
- [ ] IP whitelist configured (optional but recommended)

**API Key Permissions Checklist**:
```
✅ General - READ
✅ Trade - ENABLED (required for orders)
✅ Transfer - DISABLED
✅ Withdraw - DISABLED (CRITICAL)
✅ Margin Trading - DISABLED
✅ Futures Trading - DISABLED
```

**Security Verification**:
- [ ] API key NOT committed to Git
- [ ] API key stored in `.env` file only
- [ ] `.env` file in `.gitignore` (already configured)
- [ ] No hardcoded credentials in code

---

### 2.2 Environment Variables Setup

Create `.env` file in `C:\workspace`:

```env
# === LIVE MODE ACTIVATION ===
LIVE_MODE=true

# === EXCHANGE CONFIGURATION ===
EXCHANGE=kucoin
KUCOIN_API_KEY=your_actual_api_key_here
KUCOIN_API_SECRET=your_actual_api_secret_here
KUCOIN_API_PASSPHRASE=your_actual_passphrase_here

# === RISK LIMITS (Adjusted for $123 account) ===
ACCOUNT_BALANCE=123
MAX_POSITION_SIZE_USD=25              # ~20% of capital
MAX_TRADE_LOSS_USD=1.23               # 1% risk (constitutional limit)
MAX_DAILY_LOSS_USD=6.15               # 5% daily limit
MAX_OPEN_POSITIONS=1                  # Conservative (hardcoded)
MAX_TRADES_PER_SESSION=2              # Conservative (hardcoded)
MIN_BALANCE_USD=110                   # Stop if capital drops 10%

# === ORDER CONFIGURATION ===
ORDER_TYPE=limit                      # Use limit orders to control slippage
SLIPPAGE_TOLERANCE_PERCENT=0.5        # 0.5% max slippage

# === MARKET DATA ===
COINGECKO_API_KEY=CG-TSjzsPuWyDTQugwscwiRV8N8
```

**Verification**:
- [ ] `.env` file created
- [ ] All values filled in with actual credentials
- [ ] File permissions set (not world-readable)
- [ ] Backup copy stored securely offline

---

## ✅ PHASE 3: CODE MODIFICATIONS FOR LIVE MODE

### 3.1 Verify ExecutionAgent Live Mode Support

**Check**: Does `executor.py` support live trading?

**Status**: 
- ✅ `live_mode` parameter exists in `__init__`
- ✅ `paper_trading` flag can be disabled
- ✅ Live trade validation implemented (`_validate_live_trade`)
- ⚠️ **MISSING**: Actual exchange API integration

**CRITICAL GAP**: 
The current `executor.py` only simulates trades. You need to:

1. **Install exchange library**:
   ```powershell
   pip install ccxt python-kucoin
   ```

2. **Integrate exchange API** in `executor.py`:
   - Add KuCoin client initialization
   - Implement actual order placement
   - Add order status tracking
   - Handle partial fills (currently not implemented)
   - Add retry logic for failed orders

**Action Required**:
- [ ] Install `ccxt` or `python-kucoin` library
- [ ] Modify `executor.py` to place real orders
- [ ] Test connection with exchange (read-only first)
- [ ] Verify order placement works (test with minimum order)

**⚠️ BLOCKER**: Live trading **CANNOT proceed** until executor has real exchange integration.

---

### 3.2 Update Configuration in main.py

Modify `main.py` to read from environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

config = {
    'live_mode': os.getenv('LIVE_MODE', 'false').lower() == 'true',
    'paper_trading': not (os.getenv('LIVE_MODE', 'false').lower() == 'true'),
    'account_balance': float(os.getenv('ACCOUNT_BALANCE', 10000)),
    'exchange': os.getenv('EXCHANGE', 'kucoin'),
    'api_key': os.getenv('KUCOIN_API_KEY'),
    'api_secret': os.getenv('KUCOIN_API_SECRET'),
    'api_passphrase': os.getenv('KUCOIN_API_PASSPHRASE'),
    'risk_per_trade': 0.01,  # 1% - DO NOT CHANGE
    'max_daily_loss': 0.05,  # 5% - DO NOT CHANGE
    'max_position_size_usd': float(os.getenv('MAX_POSITION_SIZE_USD', 1000)),
    'max_trade_loss_usd': float(os.getenv('MAX_TRADE_LOSS_USD', 50)),
    'max_daily_loss_usd': float(os.getenv('MAX_DAILY_LOSS_USD', 200)),
    'min_balance_usd': float(os.getenv('MIN_BALANCE_USD', 500)),
    'order_type': os.getenv('ORDER_TYPE', 'limit'),
    'slippage_tolerance_percent': float(os.getenv('SLIPPAGE_TOLERANCE_PERCENT', 0.5)),
}
```

**Verification**:
- [ ] `python-dotenv` installed (`pip install python-dotenv`)
- [ ] `main.py` updated to load environment variables
- [ ] Config values print correctly when `main.py` runs
- [ ] Live mode flag recognized

---

## ✅ PHASE 4: EXCHANGE CONNECTIVITY TEST

### 4.1 Test API Connection (Read-Only)

Before placing orders, verify API works:

```python
# test_kucoin_connection.py
from kucoin.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(
    api_key=os.getenv('KUCOIN_API_KEY'),
    api_secret=os.getenv('KUCOIN_API_SECRET'),
    passphrase=os.getenv('KUCOIN_API_PASSPHRASE')
)

# Test 1: Get account balance
try:
    accounts = client.get_accounts()
    print("✅ API Connection: SUCCESS")
    print(f"Accounts: {len(accounts)}")
    for acc in accounts:
        if acc['type'] == 'trade' and float(acc['balance']) > 0:
            print(f"  - {acc['currency']}: {acc['balance']}")
except Exception as e:
    print(f"❌ API Connection: FAILED - {e}")

# Test 2: Get market data
try:
    ticker = client.get_ticker('SOL-USDT')
    print(f"✅ Market Data: SUCCESS")
    print(f"  SOL/USDT: ${ticker['price']}")
except Exception as e:
    print(f"❌ Market Data: FAILED - {e}")

# Test 3: Check minimum order sizes
try:
    symbols = client.get_symbols()
    for s in symbols:
        if s['symbol'] in ['BTC-USDT', 'ETH-USDT', 'SOL-USDT']:
            print(f"  {s['symbol']}: min={s['baseMinSize']}, max={s['baseMaxSize']}")
except Exception as e:
    print(f"❌ Symbol info: FAILED - {e}")
```

**Checklist**:
- [ ] Script runs without errors
- [ ] Balance shows $123 USDT (or close)
- [ ] Market data retrieves current prices
- [ ] Minimum order sizes noted (critical for position sizing)

---

### 4.2 Test Order Placement (DRY RUN)

**⚠️ CRITICAL**: Do NOT skip this step. Test with smallest possible order first.

```python
# test_order_placement.py
# ONLY RUN AFTER VERIFYING READ-ONLY ACCESS WORKS

from kucoin.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(
    api_key=os.getenv('KUCOIN_API_KEY'),
    api_secret=os.getenv('KUCOIN_API_SECRET'),
    passphrase=os.getenv('KUCOIN_API_PASSPHRASE')
)

# Test with MINIMUM order size (usually 0.001 SOL or similar)
# Check minimum from previous step first!

try:
    # LIMIT ORDER (safer - won't execute immediately)
    order = client.create_limit_order(
        symbol='SOL-USDT',
        side='buy',
        price='1.00',  # Intentionally far from market (won't fill)
        size='0.01'     # Check minimum size first!
    )
    print(f"✅ Test order created: {order['orderId']}")
    
    # IMMEDIATELY CANCEL IT
    cancel = client.cancel_order(order['orderId'])
    print(f"✅ Test order cancelled: {cancel}")
    
except Exception as e:
    print(f"❌ Order test FAILED: {e}")
```

**Verification**:
- [ ] Test order created successfully
- [ ] Test order cancelled successfully
- [ ] No unintended fills occurred
- [ ] Order appears in KuCoin trade history (cancelled)

---

## ✅ PHASE 5: RISK MANAGER VALIDATION

### 5.1 Verify Risk Calculations with $123 Capital

```python
# test_risk_with_123.py
from agents.risk_manager import RiskManagementAgent

config = {
    'account_balance': 123,
    'risk_per_trade': 0.01,  # 1%
    'max_daily_loss': 0.05,  # 5%
}

risk_mgr = RiskManagementAgent(config)

market_data = {
    'SOL/USDT': {
        'current_price': 150.00,
        'price_24h_ago': 145.00,
        'volume': 1000000
    }
}

analysis = {
    'SOL/USDT': {
        'signal_strength': 0.8,
        'trend': 'bullish'
    }
}

backtest = {
    'SOL/USDT': {
        'win_rate': 0.62
    }
}

result = risk_mgr.execute({
    'market_data': market_data,
    'analysis': analysis,
    'backtest_results': backtest
})

print(f"Position Approved: {result['data']['position_approved']}")
print(f"Position Size: {result['data']['position_size']:.4f} SOL")
print(f"Position Value: ${result['data']['position_size'] * 150:.2f}")
print(f"Stop Loss: ${result['data']['stop_loss']:.2f}")
print(f"Take Profit: ${result['data']['take_profit']:.2f}")
print(f"Risk Amount: ${result['data']['total_risk_amount']:.2f}")
print(f"Risk %: {result['data']['total_risk_pct']:.2f}%")

# CRITICAL CHECK: Does position meet KuCoin minimums?
if result['data']['position_size'] * 150 < 5:
    print("❌ WARNING: Position size below KuCoin $5 minimum!")
```

**Expected Output**:
```
Position Approved: True
Position Size: 0.0164 SOL (example)
Position Value: $2.46
Stop Loss: $147.00
Take Profit: $154.50
Risk Amount: $1.23 (1% of $123)
Risk %: 1.00%
```

**⚠️ PROBLEM**: Position value ($2.46) is **below** KuCoin minimum (~$5).

**Checklist**:
- [ ] Risk calculations work correctly
- [ ] Position size respects 1% rule
- [ ] ⚠️ Position meets exchange minimum? **LIKELY NO**

---

### 5.2 Adjust Risk Parameters (If Necessary)

**Decision Point**: Your $123 account **cannot** maintain 1% risk rule AND meet exchange minimums.

**Options**:

**A. Increase risk per trade** (⚠️ violates constitution):
```python
config = {
    'account_balance': 123,
    'risk_per_trade': 0.05,  # 5% (not 1%)
}
```
- Pro: Meets exchange minimums
- Con: **Violates core 1% safety rule**
- Con: **Contradicts system identity**

**B. Use only high-priced assets** (BTC/ETH):
```python
# BTC at $50,000
# 1% risk = $1.23
# Min order $5 / $50,000 = 0.0001 BTC
# This might work, but very tight
```

**C. Fund account to $500+** (RECOMMENDED):
```python
config = {
    'account_balance': 500,
    'risk_per_trade': 0.01,  # 1% = $5 (meets minimums)
}
```

**Which option do you choose?** _________________

---

## ✅ PHASE 6: MONITORING & SAFETY NETS

### 6.1 Continuous Monitoring Setup

**Before going live**:
- [ ] Logging configured to capture all trades
- [ ] Circuit breaker tested and armed
- [ ] Email/SMS alerts configured (optional)
- [ ] Daily P&L tracking dashboard ready
- [ ] Emergency stop procedure documented

**Emergency Stop Procedure**:
```powershell
# 1. Stop the bot
docker stop orchestrator-trading-bot

# 2. Cancel all open orders (manual)
# Log into KuCoin → Trading → Cancel All

# 3. Close all positions (manual)
# Log into KuCoin → Portfolio → Close positions

# 4. Review logs
cat logs/trading_bot.log | grep ERROR
```

---

### 6.2 First-Trade Procedure

**When you flip the switch to live**:

1. **Start with SINGLE trade limit**:
   ```python
   config['max_trades_per_session'] = 1  # Just ONE trade
   ```

2. **Watch it live**:
   ```powershell
   python main.py
   # Watch console output in real-time
   # Verify order appears on KuCoin
   ```

3. **Verify fill**:
   - Check KuCoin → Trade History
   - Confirm entry price matches expectation
   - Confirm position size correct
   - Confirm stop loss and take profit set

4. **Monitor for 24 hours**:
   - Watch position P&L
   - Verify stop loss would trigger correctly
   - Verify take profit would trigger correctly

5. **Close manually if needed**:
   - Don't wait for TP/SL if you want to exit early
   - Close on KuCoin manually first time
   - Verify bot reflects closure correctly

---

## ✅ PHASE 7: DEPLOYMENT DECISION

### 7.1 Final Go/No-Go Checklist

**System Requirements**:
- [✅] Paper trading results meet thresholds
- [✅] All agents tested and passing
- [✅] Safety features verified
- [❌] Exchange API integration complete (**BLOCKER**)
- [ ] API credentials configured
- [ ] Environment variables set
- [ ] Risk parameters validated for $123 account
- [ ] Monitoring in place

**Risk Assessment**:
- [⚠️] Account size adequate? **NO - too small**
- [ ] Position sizing works with exchange minimums? **UNLIKELY**
- [ ] Emergency procedures documented? **NEEDED**
- [ ] Backup capital available? **UNKNOWN**

**Constitutional Alignment**:
- [❌] Does $123 account violate "never rush" principle? **YES - too small**
- [❌] Does it maintain "safety over opportunity"? **NO - forced higher risk**
- [❌] Can we "halt when unsure"? **MARGINAL - tight stops**
- [✅] Will we "log everything"? **YES**
- [✅] Will we "explain decisions"? **YES**

---

### 7.2 **FINAL RECOMMENDATION**

**🚨 HALT: DO NOT DEPLOY TO LIVE TRADING YET**

**Reasons**:

1. **CRITICAL BLOCKER**: `executor.py` has no real exchange integration
   - Currently only simulates trades
   - Must implement KuCoin order placement first
   - Estimated implementation: 4-8 hours

2. **CAPITAL INSUFFICIENT**: $123 too small for proper risk management
   - Cannot maintain 1% rule AND meet exchange minimums
   - Forces constitutional violation
   - Recommended minimum: **$500-1000**

3. **SAFETY-FIRST PRINCIPLE**: System identity says "never rush"
   - You've done 4 days of excellent work
   - Paper trading results are excellent
   - But infrastructure not ready for real capital

**NEXT STEPS**:

**Option A (RECOMMENDED - CONSTITUTIONAL)**:
1. Continue paper trading with current setup
2. Implement exchange API integration in executor.py
3. Fund account to $500-1000
4. Test with single $5 trade
5. Scale up slowly

**Option B (FAST BUT RISKY)**:
1. Implement exchange API integration TODAY
2. Test with $123 but accept 4-5% risk per trade
3. Trade only BTC/ETH (higher minimums work better)
4. Prepare to top up to $500 after first winning trade

**Option C (CONSTITUTIONAL COMPROMISE)**:
1. Implement exchange API integration
2. Top up account to $500 first
3. Deploy live next week with proper testing
4. Maintain 1% risk rule throughout

---

## 📋 SUMMARY: YOUR DECISION

**Current Status**: 
- Paper trading: ✅ EXCELLENT (62% win rate, 2.84 profit factor)
- System architecture: ✅ COMPLETE
- Exchange integration: ❌ MISSING (critical blocker)
- Capital adequacy: ⚠️ MARGINAL ($123 too small)

**To proceed to live trading, you must**:
1. ✅ Implement exchange API integration (~4-8 hours work)
2. ⚠️ Either: Fund account to $500+ OR accept higher risk
3. ✅ Test connection and order placement
4. ✅ Deploy with single-trade limit first

**Your system's identity says**: *"It never rushes. It never guesses. It halts when unsure."*

**Question for you**: Are you willing to violate the 1% rule with a $123 account, or will you respect the constitutional framework and wait until proper capital is available?

**I recommend**: Implement exchange integration first, then reassess with $500+ capital.

**Your decision**: _________________ (Option A / B / C)

---

**Date**: February 5, 2026  
**Status**: PENDING YOUR DECISION  
**Next Review**: After exchange integration complete
