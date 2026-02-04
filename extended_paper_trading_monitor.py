"""
Extended Continuous Paper Trading Monitor
Runs for 30-60 minutes with 10,000 USDT virtual balance
Strict paper mode with robust anomaly detection
Auto-stops on any error, anomaly, or risk violation
"""

import sys
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple


class ExtendedPaperTradingMonitor:
    """Extended monitoring for continuous paper trading."""
    
    def __init__(self, duration_minutes: int = 30):
        self.target_duration = duration_minutes  # 30-60 minutes
        self.cycles_completed = 0
        self.total_positions_opened = 0
        self.start_time = datetime.utcnow()
        self.end_time = self.start_time + timedelta(minutes=duration_minutes)
        self.stop_flag = False
        self.stop_reason = None
        
        # Account configuration
        self.account_balance = 10000.00  # 10,000 USDT
        self.starting_balance = 10000.00
        self.daily_risk_limit = 500.00  # 5% max daily
        self.daily_risk_used = 0.00
        self.realized_pnl = 0.00
        self.unrealized_pnl = 0.00
        
        # Risk tracking
        self.positions = []
        self.closed_trades = []
        self.cycle_history = []
        self.anomalies = []
        self.errors = []
        
        # Market data rotation
        self.market_data_sets = [
            {'symbol': 'BTC/USDT', 'price': 45230.50, 'volume_24h': 28500000000, 'change': 2.15},
            {'symbol': 'ETH/USDT', 'price': 2485.30, 'volume_24h': 15200000000, 'change': 1.85},
            {'symbol': 'SOL/USDT', 'price': 152.45, 'volume_24h': 2450000000, 'change': 3.25},
            {'symbol': 'XRP/USDT', 'price': 0.52, 'volume_24h': 1200000000, 'change': 1.45},
            {'symbol': 'ADA/USDT', 'price': 0.88, 'volume_24h': 950000000, 'change': 2.35},
        ]
        
        self.current_symbol_index = 0
        self.stats = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_win_rate': 0.0,
            'total_realized_pnl': 0.0,
            'max_loss': 0.0,
            'max_gain': 0.0,
        }
    
    def elapsed_time(self) -> float:
        """Get elapsed time in seconds."""
        return (datetime.utcnow() - self.start_time).total_seconds()
    
    def remaining_time(self) -> float:
        """Get remaining time in seconds."""
        remaining = (self.end_time - datetime.utcnow()).total_seconds()
        return max(0, remaining)
    
    def time_remaining_formatted(self) -> str:
        """Format remaining time."""
        remaining = self.remaining_time()
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        return f"{minutes}m {seconds}s"
    
    def elapsed_time_formatted(self) -> str:
        """Format elapsed time."""
        elapsed = self.elapsed_time()
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        return f"{minutes}m {seconds}s"
    
    def should_continue(self) -> bool:
        """Check if monitoring should continue."""
        if self.stop_flag:
            return False
        if self.remaining_time() <= 0:
            return False
        return True
    
    def check_anomalies(self) -> Tuple[bool, Optional[str]]:
        """Check for anomalies that should halt trading."""
        
        # Check account balance
        if self.account_balance < 100:
            return True, "ANOMALY: Account balance critically low (<$100)"
        
        # Check max drawdown
        drawdown = (self.starting_balance - self.account_balance) / self.starting_balance
        if drawdown > 0.20:  # 20% max drawdown
            return True, f"ANOMALY: Max drawdown exceeded ({drawdown:.1%})"
        
        # Check daily risk
        if self.daily_risk_used > self.daily_risk_limit * 1.1:  # 10% buffer
            return True, f"ANOMALY: Daily risk exceeded ({self.daily_risk_used:.0f} > {self.daily_risk_limit:.0f})"
        
        # Check position count
        if len(self.positions) > 10:
            return True, "ANOMALY: Too many open positions (>10)"
        
        # Check for stuck positions
        now = datetime.utcnow()
        for pos in self.positions:
            age = (now - datetime.fromisoformat(pos['opened_at'])).total_seconds()
            if age > 900:  # 15 minutes max per position
                # Auto-close stuck positions
                pos['status'] = 'CLOSED'
                pos['closed_at'] = now.isoformat()
                pos['close_reason'] = 'Auto-closed (15m timeout)'
        
        return False, None
    
    def get_next_market_data(self) -> Dict[str, Any]:
        """Get next market data (rotating)."""
        data = self.market_data_sets[self.current_symbol_index % len(self.market_data_sets)]
        self.current_symbol_index += 1
        return data
    
    def simulate_trade_outcome(self, symbol: str) -> Optional[Tuple[float, str]]:
        """Simulate if a position hits TP or SL."""
        # Simulate 65% win rate, 35% loss rate
        import random
        if random.random() < 0.65:
            return (1.015, 'TAKE_PROFIT')  # 1.5% gain
        else:
            return (-0.020, 'STOP_LOSS')  # 2% loss
    
    def execute_cycle(self, cycle_num: int) -> Dict[str, Any]:
        """Execute a single trading cycle."""
        
        cycle_start = time.time()
        cycle_data = {
            'cycle_num': cycle_num,
            'timestamp': datetime.utcnow().isoformat(),
            'success': False,
            'trade_opened': False,
            'trade_closed': False,
            'phases': {},
            'error': None,
        }
        
        try:
            # Phase 1: Data Fetch
            market_data = self.get_next_market_data()
            cycle_data['phases']['data_fetch'] = 'COMPLETE'
            
            # Phase 2: Analysis
            signal = 'BUY' if market_data['change'] > 1.5 else 'HOLD'
            cycle_data['phases']['analysis'] = 'COMPLETE'
            
            # Phase 3: Validation
            if signal != 'HOLD':
                cycle_data['phases']['validation'] = 'VALIDATED'
            else:
                cycle_data['phases']['validation'] = 'REJECTED'
                cycle_data['phases']['execution'] = 'SKIPPED'
                cycle_data['phases']['logging'] = 'COMPLETE'
                cycle_data['success'] = True
                return cycle_data
            
            # Phase 4: Risk Management
            risk_amount = 100.00
            if self.daily_risk_used + risk_amount > self.daily_risk_limit:
                cycle_data['phases']['risk_mgmt'] = 'LIMIT_HIT'
                cycle_data['phases']['execution'] = 'SKIPPED'
                cycle_data['phases']['logging'] = 'COMPLETE'
                cycle_data['success'] = True
                return cycle_data
            
            # Phase 5: Execution
            price = market_data['price']
            stop_loss = price * 0.98
            position_size = risk_amount / (price - stop_loss)
            take_profit = price * 1.03
            position_value = position_size * price
            
            trade_id = f"PAPER-{cycle_num}-{int(time.time())}"
            
            position = {
                'trade_id': trade_id,
                'symbol': market_data['symbol'],
                'entry_price': price,
                'position_size': position_size,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'entry_value': position_value,
                'risk_amount': risk_amount,
                'opened_at': datetime.utcnow().isoformat(),
                'status': 'OPEN',
                'closed_at': None,
                'close_reason': None,
                'pnl': 0.0,
            }
            
            self.positions.append(position)
            self.daily_risk_used += risk_amount
            self.total_positions_opened += 1
            cycle_data['trade_opened'] = True
            cycle_data['phases']['execution'] = 'COMPLETE'
            
            # Phase 6: Logging
            cycle_data['phases']['logging'] = 'COMPLETE'
            cycle_data['success'] = True
            
            # Simulate trade outcome
            outcome = self.simulate_trade_outcome(market_data['symbol'])
            if outcome:
                multiplier, reason = outcome
                pnl = risk_amount * multiplier
                position['status'] = 'CLOSED'
                position['closed_at'] = datetime.utcnow().isoformat()
                position['close_reason'] = reason
                position['pnl'] = pnl
                
                self.closed_trades.append(position)
                self.realized_pnl += pnl
                self.account_balance += pnl
                cycle_data['trade_closed'] = True
                
                if pnl > 0:
                    self.stats['winning_trades'] += 1
                    self.stats['max_gain'] = max(self.stats['max_gain'], pnl)
                else:
                    self.stats['losing_trades'] += 1
                    self.stats['max_loss'] = min(self.stats['max_loss'], pnl)
                
                self.positions.remove(position)
            
            self.stats['total_trades'] = len(self.closed_trades)
            if self.stats['total_trades'] > 0:
                self.stats['total_win_rate'] = self.stats['winning_trades'] / self.stats['total_trades']
            self.stats['total_realized_pnl'] = self.realized_pnl
            
            cycle_data['duration'] = time.time() - cycle_start
            return cycle_data
            
        except Exception as e:
            error = f"Cycle {cycle_num} error: {str(e)}"
            self.errors.append(error)
            cycle_data['error'] = error
            self.stop_flag = True
            self.stop_reason = f"ERROR: {error}"
            return cycle_data
    
    def print_header(self, title: str):
        """Print formatted header."""
        print(f"\n{'='*100}")
        print(f"  {title}")
        print(f"{'='*100}\n")
    
    def print_status_line(self):
        """Print current status line."""
        elapsed = self.elapsed_time_formatted()
        remaining = self.time_remaining_formatted()
        balance = self.account_balance
        pnl_pct = (balance - self.starting_balance) / self.starting_balance * 100
        
        print(f"\r[{elapsed} elapsed | {remaining} remaining] "
              f"Cycles: {self.cycles_completed} | "
              f"Balance: ${balance:,.2f} ({pnl_pct:+.2f}%) | "
              f"Positions: {len(self.positions)}", end='', flush=True)
    
    def print_cycle_result(self, cycle_data: Dict[str, Any]):
        """Print cycle result."""
        if not cycle_data.get('success'):
            if cycle_data.get('error'):
                print(f"\n[ERROR] Cycle {cycle_data['cycle_num']}: {cycle_data['error']}")
            return
        
        if cycle_data.get('trade_opened'):
            status = "OPENED"
            if cycle_data.get('trade_closed'):
                status = "OPENED & CLOSED"
            print(f"\n[OK] Cycle {cycle_data['cycle_num']}: Trade {status}")
        else:
            print(f"\n[SKIP] Cycle {cycle_data['cycle_num']}: Skipped")
    
    def print_periodic_summary(self):
        """Print periodic summary every 10 cycles."""
        print(f"\n{'─'*100}")
        print(f"PERIODIC SUMMARY - {self.elapsed_time_formatted()} elapsed")
        print(f"{'─'*100}")
        print(f"  Cycles: {self.cycles_completed} | "
              f"Trades: {self.stats['total_trades']} | "
              f"Win Rate: {self.stats['total_win_rate']:.1%} | "
              f"Realized P&L: ${self.stats['total_realized_pnl']:+,.2f}")
        print(f"  Balance: ${self.account_balance:,.2f} "
              f"({(self.account_balance-self.starting_balance)/self.starting_balance*100:+.2f}%) | "
              f"Daily Risk: ${self.daily_risk_used:.0f}/${self.daily_risk_limit:.0f} "
              f"({self.daily_risk_used/self.daily_risk_limit*100:.0f}%)")
        print(f"  Open Positions: {len(self.positions)} | "
              f"Max Gain: ${self.stats['max_gain']:+,.2f} | "
              f"Max Loss: ${self.stats['max_loss']:+,.2f}")
        print()
    
    def run_extended_session(self, min_cycles: int = 10):
        """Run extended trading session."""
        self.print_header("EXTENDED CONTINUOUS PAPER TRADING SESSION")
        print(f"Start Time: {self.start_time.isoformat()}Z")
        print(f"Target Duration: {self.target_duration} minutes")
        print(f"Starting Balance: ${self.starting_balance:,.2f}")
        print(f"Daily Risk Limit: ${self.daily_risk_limit:.2f} (5%)")
        print(f"Strict Paper Mode: ENABLED")
        print(f"Anomaly Detection: ENABLED")
        print()
        
        try:
            while self.should_continue():
                # Check for anomalies
                has_anomaly, anomaly_msg = self.check_anomalies()
                if has_anomaly:
                    self.anomalies.append(anomaly_msg)
                    self.stop_flag = True
                    self.stop_reason = anomaly_msg
                    break
                
                # Execute cycle
                self.cycles_completed += 1
                cycle_data = self.execute_cycle(self.cycles_completed)
                self.cycle_history.append(cycle_data)
                
                # Print status
                self.print_status_line()
                
                # Print detailed result
                if self.cycles_completed % 1 == 0:
                    self.print_cycle_result(cycle_data)
                
                # Print periodic summary
                if self.cycles_completed % 10 == 0:
                    self.print_periodic_summary()
                
                # Check if we hit daily risk limit
                if self.daily_risk_used >= self.daily_risk_limit:
                    print(f"\n[INFO] Daily risk limit reached. Pausing new trades.")
                    # Continue cycles but skip trade execution
                
                # Small delay
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print(f"\n\n[WARN] USER INTERRUPTED")
            self.stop_flag = True
            self.stop_reason = "User interrupted"
        except Exception as e:
            print(f"\n\n[ERROR] FATAL ERROR: {str(e)}")
            self.stop_flag = True
            self.stop_reason = f"Fatal error: {str(e)}"
        
        # Print final summary
        self.print_final_summary()
    
    def print_final_summary(self):
        """Print comprehensive final summary."""
        self.print_header("EXTENDED SESSION - FINAL REPORT")
        
        elapsed = self.elapsed_time()
        elapsed_minutes = elapsed / 60
        
        print(f"Session Duration: {self.elapsed_time_formatted()} ({elapsed_minutes:.1f} minutes)")
        print(f"Cycles Completed: {self.cycles_completed}")
        print(f"Avg Cycle Time: {elapsed / self.cycles_completed if self.cycles_completed > 0 else 0:.2f} seconds\n")
        
        print("TRADING RESULTS:")
        print(f"  Starting Balance: ${self.starting_balance:,.2f}")
        print(f"  Ending Balance: ${self.account_balance:,.2f}")
        print(f"  Realized P&L: ${self.realized_pnl:+,.2f}")
        print(f"  Return: {(self.account_balance-self.starting_balance)/self.starting_balance*100:+.2f}%\n")
        
        print("POSITION STATISTICS:")
        print(f"  Total Trades Closed: {self.stats['total_trades']}")
        print(f"  Winning Trades: {self.stats['winning_trades']}")
        print(f"  Losing Trades: {self.stats['losing_trades']}")
        print(f"  Win Rate: {self.stats['total_win_rate']:.1%}")
        print(f"  Max Gain: ${self.stats['max_gain']:+,.2f}")
        print(f"  Max Loss: ${self.stats['max_loss']:+,.2f}")
        print(f"  Open Positions: {len(self.positions)}\n")
        
        print("RISK MANAGEMENT:")
        print(f"  Daily Risk Limit: ${self.daily_risk_limit:.2f}")
        print(f"  Daily Risk Used: ${self.daily_risk_used:.2f}")
        print(f"  Risk Utilization: {self.daily_risk_used/self.daily_risk_limit*100:.1f}%")
        print(f"  Max Drawdown: {(self.starting_balance-self.account_balance)/self.starting_balance*100:.2f}%\n")
        
        print("SAFETY STATUS:")
        print(f"  Risk Violations: {len([e for e in self.errors if 'risk' in e.lower()])}")
        print(f"  Anomalies Detected: {len(self.anomalies)}")
        print(f"  Total Errors: {len(self.errors)}")
        print(f"  Circuit Breaker: {'ACTIVATED' if self.stop_flag else 'OFF'}\n")
        
        if self.anomalies:
            print("ANOMALIES:")
            for anomaly in self.anomalies:
                print(f"  [WARN] {anomaly}")
            print()
        
        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(f"  [ERROR] {error}")
            print()
        
        print("="*100)
        
        if self.stop_flag and self.stop_reason:
            if "anomaly" in self.stop_reason.lower():
                print(f"[WARN] SESSION HALTED - {self.stop_reason}")
                self.write_anomaly_report()
            elif "error" in self.stop_reason.lower():
                print(f"[ERROR] SESSION HALTED - {self.stop_reason}")
            else:
                print(f"[INFO] SESSION COMPLETED - {self.stop_reason}")
        else:
            print("[OK] SESSION COMPLETED SUCCESSFULLY - NO VIOLATIONS OR ANOMALIES")
        
        print("="*100 + "\n")
    
    def write_anomaly_report(self):
        """Write anomaly report if session halted."""
        if not self.anomalies:
            return
        
        report_file = "ANOMALY_REPORT.txt"
        timestamp = datetime.utcnow().isoformat()
        
        with open(report_file, 'w') as f:
            f.write("ANOMALY REPORT\n")
            f.write("="*100 + "\n")
            f.write(f"Timestamp: {timestamp}Z\n")
            f.write(f"Session Duration: {self.elapsed_time_formatted()}\n")
            f.write(f"Cycles Completed: {self.cycles_completed}\n\n")
            
            f.write("ANOMALIES DETECTED:\n")
            f.write("-"*100 + "\n")
            for i, anomaly in enumerate(self.anomalies, 1):
                f.write(f"{i}. {anomaly}\n")
            
            f.write("\n\nFINAL STATE:\n")
            f.write("-"*100 + "\n")
            f.write(f"Account Balance: ${self.account_balance:,.2f}\n")
            f.write(f"Starting Balance: ${self.starting_balance:,.2f}\n")
            f.write(f"Realized P&L: ${self.realized_pnl:+,.2f}\n")
            f.write(f"Open Positions: {len(self.positions)}\n")
            f.write(f"Daily Risk Used: ${self.daily_risk_used:.2f}\n")
            
            if self.positions:
                f.write(f"\nOPEN POSITIONS:\n")
                f.write("-"*100 + "\n")
                for pos in self.positions:
                    f.write(f"  {pos['trade_id']}: {pos['symbol']} ({pos['position_size']:.4f} units)\n")
        
        print(f"\n[INFO] Anomaly report written to: {report_file}")


def main():
    """Main entry point."""
    # Run for 30 minutes by default, can be adjusted
    duration = 30  # minutes (change to 60 for 1 hour)
    
    monitor = ExtendedPaperTradingMonitor(duration_minutes=duration)
    monitor.run_extended_session()
    
    # Return exit code
    if monitor.stop_flag and (monitor.anomalies or monitor.errors):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
