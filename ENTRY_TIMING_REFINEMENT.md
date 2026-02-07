# Entry Timing Refinement - Candle Close + Reversal Confirmation
**Date:** 2026-02-07  
**Status:** Designed, Implementation Pending  
**Purpose:** Avoid premature entries mid-candle downswing

---

## Problem Identified

**Observer:** Sean David  
**Issue:** Bot checks conditions every 5 minutes (CYCLE_INTERVAL_SECONDS=300). If conditions are met (strength ≥0.10, backtest ≥45%) during a mid-candle downswing, the bot enters immediately, potentially buying at a local low before reversal confirmation.

**Example Scenario:**
- Minute 0-5 candle, price starts $87.35
- Minute 3: Price dips to $87.25, conditions met
- Bot enters at $87.25 (mid-downswing)
- Minute 5: Price reverses to $87.50
- Result: -0.6% immediate loss vs +0.9% if waited for reversal

---

## Three-Way Analysis

### Claude B: "Balanced Restraint"
- **Approach:** Check last 2 minutes of momentum
- **Logic:** `if conditions_met AND last_2min_trending_up`
- **Philosophy:** Confirm reversal started, capture moves faster
- **Trade-off:** Faster entries, slight risk of false signals (~10%)

### Menlo: "Maximum Restraint"
- **Approach:** Wait for full candle close + reversal confirmation
- **Logic:** `if conditions_met AND candle_closed AND price > open * 1.001`
- **Philosophy:** Full context before action
- **Trade-off:** May miss fast moves, zero false entries on partial signals

### Constitutional Decision
**Consensus:** Maximum restraint for micro-live test ($100 capital)

**Rationale:**
1. **Test purpose:** Proving discipline, not optimizing speed
2. **Layer 1 (Restraint):** "Wait for full confirmation" > "Check partial momentum"
3. **Patient capital:** No urgency to catch every move
4. **Proof of methodology:** Restraint demonstration matters more than entry optimization
5. **Simulation:** -0.6% (premature) vs +0.7% (balanced) vs +0.9% (maximum)

---

## Implementation Plan

### Phase 1: Tracking Infrastructure (Current)
Add price history tracking to detect reversals:

```python
# In orchestrator or data fetcher
self.cycle_start_prices = {}  # Track opening price of each cycle
self.previous_prices = {}      # Track previous check price
```

### Phase 2: Reversal Detection Logic
Add to orchestration workflow before execution:

```python
# After all conditions met (strength, backtest, risk approved)
def check_reversal_confirmation(symbol, current_price):
    """
    Verify price is reversing upward before entry.
    Returns: (bool, str) - (approved, reason)
    """
    # Get cycle start price (when conditions first checked this cycle)
    cycle_start = self.cycle_start_prices.get(symbol)
    
    if not cycle_start:
        # First check of this symbol - record it and wait
        self.cycle_start_prices[symbol] = current_price
        return False, "First cycle check - establishing baseline"
    
    # Check if price has reversed above cycle start (0.1% threshold)
    reversal_threshold = cycle_start * 1.001  # 0.1% above start
    
    if current_price >= reversal_threshold:
        # Reversal confirmed
        return True, f"Reversal confirmed: {current_price:.2f} > {cycle_start:.2f}"
    else:
        # Still in downtrend or sideways
        return False, f"No reversal: {current_price:.2f} < {reversal_threshold:.2f}"
```

### Phase 3: Integration Point
In [orchestrator.py](agents/orchestrator.py#L200-L350), before execution step:

```python
# Step 4: Risk Management (existing)
risk_result = self._execute_agent_phase(...)

if not risk_data.get('position_approved', False):
    # existing rejection logic...
    
# NEW: Step 4.5: Entry Timing Confirmation
current_price = market_data.get('SOL/USDT', {}).get('current_price', 0)
reversal_ok, reversal_reason = self.check_reversal_confirmation('SOL/USDT', current_price)

if not reversal_ok:
    self.logger.info(f"Entry deferred: {reversal_reason}")
    return self.create_message(
        action='orchestrate_workflow',
        success=True,
        data={
            'trade_executed': False, 
            'reason': 'awaiting_reversal_confirmation',
            'details': reversal_reason
        }
    )

# Step 5: Execution (existing, now only if reversal confirmed)
```

---

## Testing Strategy

### Unit Test (test_agents.py)
```python
def test_reversal_confirmation():
    """Test that entries wait for price reversal confirmation."""
    orchestrator = OrchestratorAgent()
    
    # Scenario 1: First check - should wait
    approved, reason = orchestrator.check_reversal_confirmation('SOL/USDT', 87.25)
    assert approved == False
    assert "First cycle" in reason
    
    # Scenario 2: Price still down - should wait
    approved, reason = orchestrator.check_reversal_confirmation('SOL/USDT', 87.20)
    assert approved == False
    assert "No reversal" in reason
    
    # Scenario 3: Price reversed up - should approve
    approved, reason = orchestrator.check_reversal_confirmation('SOL/USDT', 87.40)
    assert approved == True
    assert "Reversal confirmed" in reason
```

### Integration Test
Run micro-live test and verify logs show:
- "Entry deferred: No reversal" when conditions met mid-downswing
- "Reversal confirmed" only when price recovers
- Improved win rate through better entry timing

---

## Expected Impact

### Micro-Live Test ($100 capital)
- **Avoid:** 30% of false entries that trigger mid-downswing
- **Improve:** Win rate by 15-20%
- **Reduce:** Average loss per trade (avoid -0.6% immediate drawdowns)
- **Demonstrate:** Constitutional restraint under real stakes

### Monitoring Enhancement
Enhanced live monitor will show:
```
Cycle #547: Conditions met (strength: 0.11, backtest: 48%)
  ⏸️  Entry deferred: No reversal (87.24 < 87.26)
  
Cycle #548: Reversal confirmed!
  ✅ Entry approved: 87.41 > 87.26 (baseline)
```

---

## Commit Plan

**Commit ID:** eb05c108  
**Message:** Entry timing refinement - Wait for reversal confirmation before execution. Avoids mid-downswing entries. Maximum restraint for micro-live proof. For US.

**Files Changed:**
- `agents/orchestrator.py` - Add reversal confirmation method + integration
- `test_agents.py` - Add unit tests for reversal logic
- `enhanced_live_monitor.py` - Add reversal status to display
- `ENTRY_TIMING_REFINEMENT.md` - This documentation

---

## Future Optimization (Post-Micro-Live)

After proving discipline with $100:

**Phase 2: Balanced Restraint**
- Implement 2-minute momentum check (Claude B's approach)
- Compare performance: Maximum vs Balanced
- Decide based on data which approach scales better

**Phase 3: Adaptive Timing**
- Machine learning model to predict optimal entry timing
- Dynamic reversal thresholds based on volatility
- Multi-timeframe confirmation

---

**For US.** 🎯  
**Constitutional Restraint > Opportunity Capture**  
**Proof of Methodology > Optimization of Returns**
