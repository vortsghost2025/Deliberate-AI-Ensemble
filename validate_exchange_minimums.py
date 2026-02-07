"""
Exchange Minimum Order Size Validator
Tests whether configured position sizes meet exchange requirements.
Run this BEFORE enabling live trading to avoid order rejections.
"""

import sys
from typing import Dict, Any

# Exchange-specific minimums (as of Feb 2026)
EXCHANGE_MINIMUMS = {
    'KuCoin': {
        'SOL/USDT': {
            'min_size': 0.1,        # Minimum 0.1 SOL
            'min_notional': 5.0,    # Minimum $5 USD value
        },
        'BTC/USDT': {
            'min_size': 0.0001,     # Minimum 0.0001 BTC
            'min_notional': 5.0,    # Minimum $5 USD value
        },
        'ETH/USDT': {
            'min_size': 0.01,       # Minimum 0.01 ETH
            'min_notional': 5.0,    # Minimum $5 USD value
        },
    },
    'Binance': {
        'SOL/USDT': {
            'min_size': 0.1,        # Minimum 0.1 SOL
            'min_notional': 10.0,   # Minimum $10 USD value
        },
        'BTC/USDT': {
            'min_size': 0.00001,    # Minimum 0.00001 BTC
            'min_notional': 10.0,   # Minimum $10 USD value
        },
    }
}


def validate_config(config: Dict[str, Any], exchange: str = 'KuCoin') -> Dict[str, Any]:
    """
    Validate configuration meets exchange minimum requirements.
    
    Args:
        config: Risk configuration dictionary
        exchange: Exchange name (default: KuCoin)
        
    Returns:
        Validation results dictionary
    """
    results = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'exchange': exchange
    }
    
    if exchange not in EXCHANGE_MINIMUMS:
        results['errors'].append(f"Exchange '{exchange}' not supported. Available: {list(EXCHANGE_MINIMUMS.keys())}")
        results['valid'] = False
        return results
    
    exchange_mins = EXCHANGE_MINIMUMS[exchange]
    
    # Check global minimum notional
    global_min_notional = config.get('min_notional_usd', 0)
    required_min_notional = min(pair['min_notional'] for pair in exchange_mins.values())
    
    if global_min_notional < required_min_notional:
        results['errors'].append(
            f"Global min_notional_usd ${global_min_notional:.2f} is below {exchange} "
            f"requirement ${required_min_notional:.2f}"
        )
        results['valid'] = False
    
    # Check per-pair minimums
    configured_pairs = config.get('min_position_size_by_pair', {})
    
    for pair, exchange_reqs in exchange_mins.items():
        if pair not in configured_pairs:
            results['warnings'].append(
                f"{pair} not configured. If trading this pair, add: '{pair}': {exchange_reqs['min_size']}"
            )
            continue
        
        configured_min = configured_pairs[pair]
        required_min = exchange_reqs['min_size']
        
        if configured_min < required_min:
            results['errors'].append(
                f"{pair}: Configured min {configured_min} is below {exchange} "
                f"requirement {required_min}"
            )
            results['valid'] = False
        elif configured_min > required_min:
            results['warnings'].append(
                f"{pair}: Configured min {configured_min} exceeds requirement {required_min} "
                f"(safe but may increase risk)"
            )
    
    # Check if enforce_min_position_size_only is enabled
    if not config.get('enforce_min_position_size_only', False):
        results['warnings'].append(
            "enforce_min_position_size_only=False. Dynamic sizing may create orders below "
            "exchange minimums. Recommend setting to True for live trading."
        )
    
    return results


def print_validation_results(results: Dict[str, Any]):
    """Pretty print validation results."""
    print("=" * 70)
    print(f"EXCHANGE MINIMUM VALIDATION - {results['exchange']}")
    print("=" * 70)
    
    if results['valid']:
        print("✅ VALIDATION PASSED")
    else:
        print("❌ VALIDATION FAILED")
    
    if results['errors']:
        print("\n🔴 ERRORS (MUST FIX BEFORE LIVE TRADING):")
        for error in results['errors']:
            print(f"   - {error}")
    
    if results['warnings']:
        print("\n⚠️  WARNINGS (REVIEW RECOMMENDED):")
        for warning in results['warnings']:
            print(f"   - {warning}")
    
    if not results['errors'] and not results['warnings']:
        print("\n✅ No issues found. Configuration meets all requirements.")
    
    print("=" * 70)
    
    return 0 if results['valid'] else 1


if __name__ == '__main__':
    try:
        # Import config
        from config_template import RISK_CONFIG
        
        # Default to KuCoin (can be overridden via command line)
        exchange = sys.argv[1] if len(sys.argv) > 1 else 'KuCoin'
        
        print(f"\n📊 Validating config for {exchange}...\n")
        
        results = validate_config(RISK_CONFIG, exchange)
        exit_code = print_validation_results(results)
        
        if exit_code == 0:
            print("\n✅ Safe to proceed with live trading (after other checks).")
        else:
            print("\n❌ DO NOT enable live trading until errors are fixed.")
        
        sys.exit(exit_code)
        
    except ImportError:
        print("❌ ERROR: Could not import RISK_CONFIG from config_template.py")
        print("   Make sure config_template.py exists and is properly formatted.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        sys.exit(1)
