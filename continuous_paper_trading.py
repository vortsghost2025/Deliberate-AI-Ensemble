"""
Continuous Paper Trading Cycles Monitor
Executes multiple trading cycles with full sequence.
Strict paper mode - no real orders.
Auto-stop on any risk violation or anomaly.
"""

import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


class ContinuousPaperTradingMonitor:
    """Monitor and execute continuous paper trading cycles."""
    
    def __init__(self):
        self.cycles_completed = 0
        self.total_positions_opened = 0
        self.total_profit_loss = 0.0
        self.risk_violations = []
        self.anomalies = []
        self.cycle_history = []
        self.start_time = datetime.utcnow()
        self.stop_flag = False
        self.account_balance = 10000.00
        self.daily_risk_used = 0.0
        self.daily_risk_limit = 500.0  # 5%
        self.max_drawdown = 0.0
        
        # Mock market data - rotates each cycle
        self.market_data_sets = [
            {
                'symbol': 'SOL/USDT',
                'price': 152.45,
                'volume_24h': 2450000000,
                'price_change_24h': 3.25,
                'rsi': 58.2,
                'macd_histogram': 0.036,
                'trend': 'UPTREND'
            },
            {
                'symbol': 'BTC/USDT',
                'price': 45230.50,
                'volume_24h': 28500000000,
                'price_change_24h': 2.15,
                'rsi': 55.8,
                'macd_histogram': 0.028,
                'trend': 'UPTREND'
            },
            {
                'symbol': 'ETH/USDT',
                'price': 2485.30,
                'volume_24h': 15200000000,
                'price_change_24h': 1.85,
                'rsi': 51.4,
                'macd_histogram': 0.015,
                'trend': 'NEUTRAL'
            },
        ]
    
    def print_header(self, title: str):
        """Print formatted header."""
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    
    def print_section(self, title: str, cycle_num: int = None):
        """Print section header."""
        if cycle_num:
            print(f"\n[CYCLE {cycle_num}] {title}")
        else:
            print(f"\n[{title}]")
        print("-" * 80)
    
    def check_anomalies(self) -> Optional[str]:
        """Check for any anomalies that should halt trading."""
        # Check daily risk limit
        if self.daily_risk_used > self.daily_risk_limit:
            return f"ANOMALY: Daily risk limit exceeded ({self.daily_risk_used:.2f} > {self.daily_risk_limit:.2f})"
        
        # Check account balance
        if self.account_balance <= 100:
            return "ANOMALY: Account balance critically low"
        
        # Check max drawdown
        max_acceptable_drawdown = 0.15  # 15%
        current_drawdown = (10000.00 - self.account_balance) / 10000.00
        if current_drawdown > max_acceptable_drawdown:
            return f"ANOMALY: Max drawdown exceeded ({current_drawdown:.1%} > {max_acceptable_drawdown:.1%})"
        
        return None
    
    def execute_cycle(self, cycle_num: int) -> Dict[str, Any]:
        """Execute a single complete trading cycle."""
        
        # Check for anomalies before cycle
        anomaly = self.check_anomalies()
        if anomaly:
            self.anomalies.append(anomaly)
            self.stop_flag = True
            return {'success': False, 'error': anomaly}
        
        cycle_start = time.time()
        cycle_data = {
            'cycle_num': cycle_num,
            'timestamp': datetime.utcnow().isoformat(),
            'phases': {},
            'trade': None,
            'risk_violation': None,
            'anomaly': None
        }
        
        try:
            # Phase 1: Data Fetching
            self.print_section("PHASE 1 - DATA FETCHING", cycle_num)
            market_data = self.market_data_sets[cycle_num % len(self.market_data_sets)]
            print(f"  ✅ {market_data['symbol']}")
            print(f"     Price: ${market_data['price']:.2f}")
            print(f"     24h Change: {market_data['price_change_24h']:+.2f}%")
            print(f"     Volume: ${market_data['volume_24h']:,.0f}\n")
            time.sleep(0.2)
            
            cycle_data['phases']['data_fetch'] = 'COMPLETE'
            
            # Phase 2: Market Analysis
            self.print_section("PHASE 2 - MARKET ANALYSIS", cycle_num)
            print(f"  📊 RSI: {market_data['rsi']:.1f} (neutral)")
            print(f"  📊 MACD Histogram: {market_data['macd_histogram']:+.3f} (bullish)")
            print(f"  📊 Trend: {market_data['trend']}\n")
            
            # Generate signal
            if market_data['price_change_24h'] > 1.5 and market_data['macd_histogram'] > 0:
                signal = 'BUY'
                confidence = 'HIGH'
            elif market_data['price_change_24h'] < -1.5 or market_data['macd_histogram'] < -0.02:
                signal = 'SELL'
                confidence = 'MEDIUM'
            else:
                signal = 'HOLD'
                confidence = 'LOW'
            
            print(f"  🎯 Signal: {signal} ({confidence} confidence)\n")
            time.sleep(0.2)
            
            cycle_data['phases']['analysis'] = 'COMPLETE'
            
            # Phase 3: Signal Validation
            self.print_section("PHASE 3 - SIGNAL VALIDATION", cycle_num)
            
            # Mock backtest results
            if signal == 'BUY':
                win_rate = 0.623
                profit_factor = 2.84
            elif signal == 'SELL':
                win_rate = 0.571
                profit_factor = 1.92
            else:
                win_rate = 0.520
                profit_factor = 1.21
            
            print(f"  ✅ Backtest Results:")
            print(f"     Win Rate: {win_rate:.1%}")
            print(f"     Profit Factor: {profit_factor:.2f}\n")
            
            validated = win_rate > 0.50 and profit_factor > 1.0
            if validated:
                print(f"  ✅ Signal VALIDATED\n")
            else:
                print(f"  ❌ Signal REJECTED (poor expectancy)\n")
            
            time.sleep(0.2)
            
            cycle_data['phases']['validation'] = 'VALIDATED' if validated else 'REJECTED'
            
            # If signal not validated, skip to logging and continue
            if not validated:
                print(f"  → Skipping execution (no valid signal)")
                cycle_data['trade'] = None
                self.print_section("PHASE 6 - LOGGING (NO TRADE)", cycle_num)
                print(f"  📝 Logged: Signal rejected, no position opened\n")
                cycle_data['phases']['execution'] = 'SKIPPED'
                cycle_data['phases']['logging'] = 'COMPLETE'
                return cycle_data
            
            # Phase 4: Risk Management & Position Sizing
            self.print_section("PHASE 4 - RISK MANAGEMENT", cycle_num)
            
            # Check if we can open another position
            risk_per_trade = 0.01  # 1%
            max_risk_amount = 100.00
            
            # Check daily risk
            if self.daily_risk_used + max_risk_amount > self.daily_risk_limit:
                violation = f"Daily risk limit would be exceeded: {self.daily_risk_used + max_risk_amount:.2f} > {self.daily_risk_limit:.2f}"
                print(f"  ❌ {violation}\n")
                cycle_data['risk_violation'] = violation
                self.risk_violations.append(violation)
                self.stop_flag = True
                return cycle_data
            
            price = market_data['price']
            stop_loss = price * 0.98
            position_size = max_risk_amount / (price - stop_loss)
            position_value = position_size * price
            take_profit = price * 1.03
            
            print(f"  💰 Position Sizing:")
            print(f"     Entry: ${price:.2f}")
            print(f"     Stop: ${stop_loss:.2f}")
            print(f"     Target: ${take_profit:.2f}")
            print(f"     Size: {position_size:.4f} units")
            print(f"     Value: ${position_value:,.2f}")
            print(f"     Risk: ${max_risk_amount:.2f} (1%)")
            print(f"     Risk/Reward: 1:{(take_profit-price)/(price-stop_loss):.2f}\n")
            
            # All checks pass
            print(f"  ✅ All risk checks PASSED\n")
            time.sleep(0.2)
            
            cycle_data['phases']['risk_mgmt'] = 'COMPLETE'
            
            # Phase 5: Simulated Execution
            self.print_section("PHASE 5 - PAPER EXECUTION", cycle_num)
            
            trade_id = f"PAPER-C{cycle_num}-{int(time.time())}"
            print(f"  ✅ Paper trade opened")
            print(f"     Trade ID: {trade_id}")
            print(f"     Symbol: {market_data['symbol']}")
            print(f"     Entry: ${price:.2f}")
            print(f"     Size: {position_size:.4f}")
            print(f"     ⚠️  NO REAL ORDERS PLACED\n")
            
            time.sleep(0.2)
            
            cycle_data['phases']['execution'] = 'COMPLETE'
            
            trade = {
                'trade_id': trade_id,
                'symbol': market_data['symbol'],
                'entry_price': price,
                'position_size': position_size,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'status': 'PAPER_OPEN'
            }
            cycle_data['trade'] = trade
            self.total_positions_opened += 1
            self.daily_risk_used += max_risk_amount
            
            # Phase 6: Logging & Monitoring
            self.print_section("PHASE 6 - LOGGING & MONITORING", cycle_num)
            
            print(f"  📝 Cycle Log:")
            print(f"     Timestamp: {cycle_data['timestamp']}Z")
            print(f"     Trade ID: {trade_id}")
            print(f"     Account Balance: ${self.account_balance:,.2f}")
            print(f"     Daily Risk Used: ${self.daily_risk_used:.2f} / ${self.daily_risk_limit:.2f}")
            print(f"     Positions Open: {self.total_positions_opened}\n")
            
            print(f"  ✅ Cycle {cycle_num} COMPLETE\n")
            time.sleep(0.1)
            
            cycle_data['phases']['logging'] = 'COMPLETE'
            cycle_data['success'] = True
            cycle_data['duration'] = time.time() - cycle_start
            
            return cycle_data
            
        except Exception as e:
            error = f"Cycle execution error: {str(e)}"
            print(f"\n  ❌ ERROR: {error}\n")
            self.stop_flag = True
            cycle_data['error'] = error
            return cycle_data
    
    def print_cycle_summary(self, cycle_data: Dict[str, Any]):
        """Print summary after each cycle."""
        if not cycle_data.get('success', False):
            if cycle_data.get('error'):
                print(f"⚠️  CYCLE {cycle_data['cycle_num']} FAILED: {cycle_data['error']}")
            if cycle_data.get('risk_violation'):
                print(f"⚠️  CYCLE {cycle_data['cycle_num']} STOPPED: {cycle_data['risk_violation']}")
            return
        
        summary = f"\n📊 CYCLE {cycle_data['cycle_num']} SUMMARY"
        print(f"\n{'─'*80}")
        print(summary)
        print(f"{'─'*80}")
        print(f"  Duration: {cycle_data.get('duration', 0):.2f}s")
        
        phases_str = ', '.join([f"{k}={v}" for k,v in cycle_data['phases'].items()])
        print(f"  Phases: {phases_str}")
        
        if cycle_data['trade']:
            print(f"  Trade: {cycle_data['trade']['trade_id']} ({cycle_data['trade']['symbol']})")
        else:
            print(f"  Trade: SKIPPED (no valid signal)")
        
        print(f"  Account: ${self.account_balance:,.2f}")
        print(f"  Daily Risk: {self.daily_risk_used:.0f}/{self.daily_risk_limit:.0f} ({self.daily_risk_used/self.daily_risk_limit*100:.1f}%)")
        print()
    
    def run_continuous_cycles(self, max_cycles: int = 5):
        """Run continuous trading cycles."""
        self.print_header("CONTINUOUS PAPER TRADING CYCLES")
        print(f"Starting Time: {self.start_time.isoformat()}Z")
        print(f"Environment: Paper Trading (SAFE MODE)")
        print(f"Starting Balance: ${self.account_balance:,.2f}")
        print(f"Daily Risk Limit: ${self.daily_risk_limit:.2f} (5%)")
        print(f"Cycles to Execute: {max_cycles}\n")
        print("=" * 80)
        
        for cycle_num in range(1, max_cycles + 1):
            # Check stop flag
            if self.stop_flag:
                print(f"\n⚠️  STOPPING - Risk violation or anomaly detected")
                break
            
            try:
                cycle_data = self.execute_cycle(cycle_num)
                self.cycle_history.append(cycle_data)
                self.print_cycle_summary(cycle_data)
                
                # Small delay between cycles
                if cycle_num < max_cycles:
                    time.sleep(0.5)
                    
            except KeyboardInterrupt:
                print(f"\n⚠️  STOPPING - User interrupted")
                self.stop_flag = True
                break
            except Exception as e:
                print(f"\n❌ FATAL ERROR in cycle {cycle_num}: {str(e)}")
                self.stop_flag = True
                break
        
        # Print final summary
        self.print_final_summary()
    
    def print_final_summary(self):
        """Print comprehensive final summary."""
        self.print_header("CONTINUOUS TRADING SESSION - FINAL SUMMARY")
        
        elapsed = (datetime.utcnow() - self.start_time).total_seconds()
        
        print(f"Session Duration: {elapsed:.1f} seconds")
        print(f"Cycles Executed: {len([c for c in self.cycle_history if c.get('success')])}")
        print(f"Total Cycles Started: {len(self.cycle_history)}\n")
        
        # Cycle results
        print("Cycle Results:")
        successful = sum(1 for c in self.cycle_history if c.get('success'))
        with_trades = sum(1 for c in self.cycle_history if c.get('trade'))
        print(f"  ✅ Successful: {successful}")
        print(f"  📊 Trades Opened: {with_trades}")
        print(f"  ⏭️  Skipped: {len(self.cycle_history) - successful}\n")
        
        # Risk summary
        print("Risk Management:")
        print(f"  Starting Balance: $10,000.00")
        print(f"  Current Balance: ${self.account_balance:,.2f}")
        print(f"  Daily Risk Used: ${self.daily_risk_used:.2f}/{self.daily_risk_limit:.2f}")
        print(f"  Risk Utilization: {self.daily_risk_used/self.daily_risk_limit*100:.1f}%\n")
        
        # Safety
        print("Safety Status:")
        print(f"  Risk Violations: {len(self.risk_violations)}")
        print(f"  Anomalies: {len(self.anomalies)}")
        print(f"  Circuit Breaker: {'ACTIVATED' if self.stop_flag else 'OFF'}")
        
        if self.risk_violations:
            print(f"\n  Risk Violations Detected:")
            for violation in self.risk_violations:
                print(f"    ❌ {violation}")
        
        if self.anomalies:
            print(f"\n  Anomalies Detected:")
            for anomaly in self.anomalies:
                print(f"    ⚠️  {anomaly}")
        
        # Overall status
        print(f"\n{'='*80}")
        if not self.stop_flag and len(self.risk_violations) == 0 and len(self.anomalies) == 0:
            print("✅ SESSION COMPLETED SUCCESSFULLY - NO VIOLATIONS OR ANOMALIES")
        elif self.stop_flag:
            print("⚠️  SESSION HALTED - Risk violation or anomaly detected")
        else:
            print("⚠️  SESSION COMPLETED WITH WARNINGS")
        print(f"{'='*80}\n")


def main():
    """Main entry point."""
    monitor = ContinuousPaperTradingMonitor()
    monitor.run_continuous_cycles(max_cycles=5)
    
    # Return appropriate exit code
    if monitor.stop_flag or monitor.risk_violations or monitor.anomalies:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
