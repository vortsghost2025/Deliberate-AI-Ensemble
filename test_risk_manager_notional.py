"""
Isolated Unit Test: Risk Manager Notional Value Validation
Tests the RiskManagementAgent's minimum notional check in isolation.
Does NOT modify main bot. Does NOT disable safety layers.
"""

from agents.risk_manager import RiskManagementAgent


def test_notional_rejection_with_micro_balance():
    """
    Test Case: $80 balance with 0.01 SOL minimum position
    Expected: Rejection due to notional value below $1.00 minimum
    """
    print("="*70)
    print("UNIT TEST: Risk Manager Notional Value Check")
    print("="*70)
    
    # Configuration matching main.py production settings
    config = {
        'account_balance': 80.0,           # Micro-live balance
        'risk_per_trade': 0.01,            # 1% risk
        'min_notional_usd': 1.0,           # The fix we deployed
        'min_position_size_units': 0.01,   # 0.01 SOL minimum
        'min_position_size_by_pair': {
            'SOL/USDT': 0.01
        },
        'enforce_min_position_size_only': True,  # FORCE minimum size to trigger constraint
        'min_signal_strength': 0.10,
        'min_win_rate': 0.45,
        'min_risk_reward_ratio': 1.5,
        'max_daily_loss': 0.05,
        'default_stop_loss_pct': 0.02
    }
    
    # Instantiate Risk Manager
    risk_agent = RiskManagementAgent(config)
    
    # Mock data: Entry timing ALREADY APPROVED (respecting architecture)
    market_data = {
        'SOL/USDT': {
            'symbol': 'SOL/USDT',
            'current_price': 84.20,  # Current SOL price (correct key name)
            'timestamp': '2026-02-13T16:59:37'
        }
    }
    
    analysis = {
        'SOL/USDT': {
            'signal_strength': 0.65,           # Strong signal (exceeds 0.10 minimum)
            'entry_timing_approved': True,     # Entry timing validator PASSED
            'entry_timing_reason': 'Test scenario - entry approved'
        }
    }
    
    backtest_results = {
        'SOL/USDT': {
            'win_rate': 0.557,                 # 55.7% win rate (exceeds 0.45 minimum)
            'max_drawdown': 0.074
        }
    }
    
    # Execute risk assessment
    print("\n📊 Test Scenario:")
    print(f"  Account Balance: ${config['account_balance']:.2f}")
    print(f"  SOL Price: ${market_data['SOL/USDT']['current_price']:.2f}")
    print(f"  Min Position: {config['min_position_size_units']} SOL")
    print(f"  Position Value: {config['min_position_size_units']} × ${market_data['SOL/USDT']['current_price']:.2f} = ${config['min_position_size_units'] * market_data['SOL/USDT']['current_price']:.2f}")
    print(f"  Min Notional: ${config['min_notional_usd']:.2f}")
    print(f"  Entry Timing: {analysis['SOL/USDT']['entry_timing_approved']}")
    print(f"  Signal Strength: {analysis['SOL/USDT']['signal_strength']:.2f}")
    print(f"  Win Rate: {backtest_results['SOL/USDT']['win_rate']:.1%}")
    
    # Call the private method to assess risk for this pair
    result = risk_agent._assess_pair_risk(
        'SOL/USDT',
        market_data['SOL/USDT'],
        analysis['SOL/USDT'],
        backtest_results['SOL/USDT']
    )
    
    print("\n🔍 Risk Assessment Result:")
    print(f"  Position Approved: {result['position_approved']}")
    print(f"  Position Size: {result['position_size']:.4f} SOL")
    print(f"  Position Value: ${result['position_size_usd']:.2f}")
    print(f"  Rejection Reason: {result['rejection_reason']}")
    
    # Validation: Check if rejection contains expected pattern
    print("\n✅ Validation:")
    
    if not result['position_approved']:
        rejection_reason = result['rejection_reason'] or ""
        rejection_lower = rejection_reason.lower()
        
        if 'notional' in rejection_lower and 'below minimum' in rejection_lower:
            print("  ✓ PASS: Rejection reason matches 'notional' + 'below minimum' pattern")
            print(f"  ✓ PASS: Notional check is working correctly")
            print(f"  ✓ PASS: Config value (min_notional_usd: {config['min_notional_usd']}) is being enforced")
            
            # Extract values from rejection message for verification
            if '$' in rejection_reason:
                print(f"  ✓ PASS: Rejection message contains USD values")
                
            print("\n🎯 CONCLUSION: The fix is PROVEN functional.")
            print("   The RiskManagementAgent correctly rejects positions below $1.00 notional.")
            print("   When a real signal passes Entry Timing, this logic will trigger.")
            return True
        else:
            print(f"  ✗ FAIL: Rejection reason does not match expected pattern")
            print(f"  ✗ FAIL: Expected 'notional' AND 'below minimum' in message")
            print(f"  ✗ FAIL: Actual: '{rejection_reason}'")
            return False
    else:
        print("  ✗ FAIL: Position was approved (should have been rejected)")
        print("  ✗ FAIL: Notional check did not trigger")
        return False


if __name__ == '__main__':
    success = test_notional_rejection_with_micro_balance()
    
    print("\n" + "="*70)
    if success:
        print("TEST RESULT: SUCCESS ✓")
        print("The intelligent constraint awareness is operational.")
    else:
        print("TEST RESULT: FAILURE ✗")
        print("The fix did not work as expected.")
    print("="*70)
