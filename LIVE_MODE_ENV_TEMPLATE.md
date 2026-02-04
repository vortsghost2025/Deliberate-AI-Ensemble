# Live Mode Environment Variables

## ⚠️ CRITICAL - Required for Live Trading

Before switching to live mode, you MUST configure these environment variables with your actual exchange credentials:

```bash
# === LIVE MODE ACTIVATION ===
LIVE_MODE=true                          # Switch from paper to live trading

# === EXCHANGE CONFIGURATION ===
EXCHANGE=binance                        # Your exchange (binance/kraken/coinbase/etc)
LIVE_API_KEY=your_actual_api_key_here  # Your exchange API key
LIVE_API_SECRET=your_actual_secret_here # Your exchange API secret

# === RISK LIMITS (Adjust to your capital) ===
MAX_POSITION_SIZE_USD=1000              # Max USD per single position
MAX_TRADE_LOSS_USD=50                   # Max loss allowed per trade
MAX_DAILY_LOSS_USD=200                  # Max total loss per day (circuit breaker)
MAX_OPEN_POSITIONS=3                    # Max concurrent open positions
MIN_BALANCE_USD=500                     # Min account balance to continue trading

# === ORDER CONFIGURATION ===
ORDER_TYPE=limit                        # Order type: limit or market
SLIPPAGE_TOLERANCE_PERCENT=0.5          # Acceptable slippage for orders

# === SYSTEM CONFIGURATION ===
CONTINUOUS_MODE=true                    # Keep running continuously
CYCLE_INTERVAL_SECONDS=300              # Time between trading cycles (5 min)
COINGECKO_API_KEY=CG-TSjzsPuWyDTQugwscwiRV8N8  # Your CoinGecko API key
```

## Docker Run Command (Live Mode)

```bash
docker rm -f orchestrator-live

docker run -d \
  --name orchestrator-live \
  --restart=unless-stopped \
  -e LIVE_MODE=true \
  -e EXCHANGE=binance \
  -e LIVE_API_KEY=YOUR_ACTUAL_API_KEY \
  -e LIVE_API_SECRET=YOUR_ACTUAL_API_SECRET \
  -e MAX_POSITION_SIZE_USD=1000 \
  -e MAX_TRADE_LOSS_USD=50 \
  -e MAX_DAILY_LOSS_USD=200 \
  -e MAX_OPEN_POSITIONS=3 \
  -e MIN_BALANCE_USD=500 \
  -e ORDER_TYPE=limit \
  -e SLIPPAGE_TOLERANCE_PERCENT=0.5 \
  -e CONTINUOUS_MODE=true \
  -e CYCLE_INTERVAL_SECONDS=300 \
  -e COINGECKO_API_KEY=CG-TSjzsPuWyDTQugwscwiRV8N8 \
  orchestrator-bot:latest
```

## Environment File (.env) Method

Create a file named `.env` in C:\workspace:

```env
LIVE_MODE=true
EXCHANGE=binance
LIVE_API_KEY=YOUR_ACTUAL_API_KEY
LIVE_API_SECRET=YOUR_ACTUAL_API_SECRET
MAX_POSITION_SIZE_USD=1000
MAX_TRADE_LOSS_USD=50
MAX_DAILY_LOSS_USD=200
MAX_OPEN_POSITIONS=3
MIN_BALANCE_USD=500
ORDER_TYPE=limit
SLIPPAGE_TOLERANCE_PERCENT=0.5
CONTINUOUS_MODE=true
CYCLE_INTERVAL_SECONDS=300
COINGECKO_API_KEY=CG-TSjzsPuWyDTQugwscwiRV8N8
```

Then run with:
```bash
docker run -d --name orchestrator-live --env-file .env orchestrator-bot:latest
```

## 🔐 Security Best Practices

1. **Never commit API keys to Git** - Add `.env` to your `.gitignore` (already done)
2. **Use read-only API keys if possible** - Check your exchange settings
3. **Restrict API key permissions** - Only enable trading, disable withdrawals
4. **Use IP whitelist** - Restrict API key to your server's IP address
5. **Start with small limits** - Test with minimal MAX_POSITION_SIZE_USD first

## 📊 Recommended Starting Values for Live Trading

For initial live testing with **$1,000-$2,000 capital**:
```bash
MAX_POSITION_SIZE_USD=100        # 10% of capital per position
MAX_TRADE_LOSS_USD=20            # 2% risk per trade
MAX_DAILY_LOSS_USD=50            # 5% max daily drawdown
MAX_OPEN_POSITIONS=2             # Conservative simultaneous trades
MIN_BALANCE_USD=900              # Stop if capital drops 10%
```

For **$5,000+ capital**:
```bash
MAX_POSITION_SIZE_USD=500
MAX_TRADE_LOSS_USD=50
MAX_DAILY_LOSS_USD=150
MAX_OPEN_POSITIONS=3
MIN_BALANCE_USD=4500
```

## ⚠️ Pre-Launch Checklist

Before switching LIVE_MODE=true:

- [ ] Exchange API keys created and tested
- [ ] API key permissions restricted (trading only, no withdrawals)
- [ ] Risk limits match your capital and risk tolerance
- [ ] IP whitelist configured on exchange (optional but recommended)
- [ ] Soak test passed successfully (✅ DONE)
- [ ] You understand that LIVE_MODE=true will use REAL money
- [ ] Stop-loss and circuit breaker limits are appropriate
- [ ] You're monitoring the first few trades closely

## 📋 Monitoring Commands

After starting live mode:

```bash
# Check container status
docker ps --filter "name=orchestrator-live"

# View live logs
docker logs orchestrator-live -f

# Check recent trades
docker logs orchestrator-live --tail 100 | grep "Trade Executed"

# Monitor errors
docker logs orchestrator-live | grep "ERROR"

# Check circuit breaker status
docker logs orchestrator-live | grep "Circuit Breaker"
```

## 🛑 Emergency Stop

To immediately stop live trading:

```bash
docker stop orchestrator-live
docker rm orchestrator-live
```

---

**REMINDER:** Paper trading (LIVE_MODE=false) completed successfully. You must update LIVE_API_KEY and LIVE_API_SECRET with your actual exchange credentials before switching to LIVE_MODE=true.
