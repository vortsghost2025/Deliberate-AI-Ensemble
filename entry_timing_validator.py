"""
Entry Timing Module - Reversal Confirmation Logic
Prevents premature entries during mid-candle downswings.
"""

from typing import Dict, Tuple, Optional
from datetime import datetime
import logging


class EntryTimingValidator:
    """
    Validates entry timing to avoid mid-downswing purchases.
    
    Uses "maximum restraint" approach: Wait for price reversal confirmation
    before executing trades, even if all other conditions are met.
    
    Philosophy: Full context > Partial signals
    """
    
    def __init__(self, reversal_threshold_pct: float = 0.001):
        """
        Initialize the entry timing validator.
        
        Args:
            reversal_threshold_pct: Minimum price increase (as decimal) to confirm reversal
                                   Default: 0.001 (0.1%)
        """
        self.logger = logging.getLogger("EntryTimingValidator")
        self.reversal_threshold_pct = reversal_threshold_pct
        
        # Track baseline prices for each symbol
        self.baseline_prices: Dict[str, float] = {}
        self.baseline_timestamps: Dict[str, datetime] = {}
        
        # Track price history for analysis
        self.price_history: Dict[str, list] = {}
        
    def check_reversal_confirmation(
        self, 
        symbol: str, 
        current_price: float
    ) -> Tuple[bool, str]:
        """
        Check if price has reversed upward from baseline.
        
        Args:
            symbol: Trading pair (e.g., 'SOL/USDT')
            current_price: Current market price
            
        Returns:
            (approved, reason): Tuple of approval status and explanation
        """
        # First check for this symbol - establish baseline
        if symbol not in self.baseline_prices:
            self.baseline_prices[symbol] = current_price
            self.baseline_timestamps[symbol] = datetime.utcnow()
            self.price_history[symbol] = [current_price]
            
            self.logger.info(
                f"[{symbol}] Baseline established at ${current_price:.2f}"
            )
            return False, f"First cycle check - baseline ${current_price:.2f}"
        
        # Add to price history
        self.price_history[symbol].append(current_price)
        if len(self.price_history[symbol]) > 10:
            self.price_history[symbol].pop(0)  # Keep last 10
        
        # Calculate reversal threshold
        baseline = self.baseline_prices[symbol]
        threshold = baseline * (1 + self.reversal_threshold_pct)
        
        # Check for reversal
        if current_price >= threshold:
            # Reversal confirmed!
            gain_pct = ((current_price - baseline) / baseline) * 100
            
            self.logger.info(
                f"[{symbol}] ✅ Reversal confirmed: "
                f"${current_price:.2f} > ${threshold:.2f} "
                f"(+{gain_pct:.2f}% from baseline)"
            )
            
            return True, f"Reversal confirmed: +{gain_pct:.2f}% from baseline ${baseline:.2f}"
        
        # Still waiting for reversal
        change_pct = ((current_price - baseline) / baseline) * 100
        
        if current_price < baseline:
            # Price declining
            self.logger.info(
                f"[{symbol}] ⏸️  Declining: ${current_price:.2f} "
                f"({change_pct:.2f}% from baseline ${baseline:.2f})"
            )
            reason = f"Price declining: {change_pct:.2f}% from baseline"
        else:
            # Price flat or slightly up but below threshold
            self.logger.info(
                f"[{symbol}] ⏸️  Insufficient reversal: ${current_price:.2f} "
                f"(need ${threshold:.2f}, +{self.reversal_threshold_pct*100:.1f}%)"
            )
            reason = f"Insufficient reversal: {change_pct:.2f}% (need +{self.reversal_threshold_pct*100:.1f}%)"
        
        return False, reason
    
    def reset_baseline(self, symbol: str) -> None:
        """
        Reset baseline for a symbol (e.g., after trade executed).
        
        Args:
            symbol: Trading pair to reset
        """
        if symbol in self.baseline_prices:
            del self.baseline_prices[symbol]
            del self.baseline_timestamps[symbol]
            self.price_history[symbol] = []
            self.logger.info(f"[{symbol}] Baseline reset")
    
    def get_baseline_age_seconds(self, symbol: str) -> Optional[float]:
        """
        Get age of current baseline in seconds.
        
        Args:
            symbol: Trading pair
            
        Returns:
            Age in seconds, or None if no baseline set
        """
        if symbol not in self.baseline_timestamps:
            return None
        
        age = (datetime.utcnow() - self.baseline_timestamps[symbol]).total_seconds()
        return age
    
    def get_status(self, symbol: str) -> Dict:
        """
        Get current status for a symbol.
        
        Args:
            symbol: Trading pair
            
        Returns:
            Status dictionary with baseline info
        """
        if symbol not in self.baseline_prices:
            return {
                'baseline_set': False,
                'status': 'waiting_for_first_check'
            }
        
        return {
            'baseline_set': True,
            'baseline_price': self.baseline_prices[symbol],
            'baseline_age_seconds': self.get_baseline_age_seconds(symbol),
            'price_history': self.price_history.get(symbol, []),
            'reversal_threshold': self.baseline_prices[symbol] * (1 + self.reversal_threshold_pct)
        }


# Example usage
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    validator = EntryTimingValidator(reversal_threshold_pct=0.001)
    
    print("=" * 60)
    print("Entry Timing Validator - Example Scenario")
    print("=" * 60)
    
    # Simulate 5-minute candle with mid-downswing
    prices = [
        (1, 87.35, "Baseline check"),
        (2, 87.30, "Slight decline"),
        (3, 87.25, "Conditions met but mid-downswing"),
        (4, 87.28, "Starting to recover"),
        (5, 87.40, "Reversal confirmed!"),
    ]
    
    for minute, price, note in prices:
        print(f"\nMinute {minute}: {note} - Price ${price}")
        approved, reason = validator.check_reversal_confirmation('SOL/USDT', price)
        
        if approved:
            print(f"  ✅ ENTRY APPROVED: {reason}")
        else:
            print(f"  ⏸️  ENTRY DEFERRED: {reason}")
    
    print("\n" + "=" * 60)
    print("Status:", validator.get_status('SOL/USDT'))
    print("=" * 60)
