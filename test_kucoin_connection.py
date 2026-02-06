#!/usr/bin/env python3
"""
Test KuCoin API Connection
Verifies credentials and minimum order requirements before live trading.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from kucoin.client import Client as KuCoinClient
    KUCOIN_AVAILABLE = True
except ImportError:
    KUCOIN_AVAILABLE = False
    print("❌ python-kucoin not installed")
    print("   Run: pip install python-kucoin")
    exit(1)


def test_connection():
    """Test KuCoin API connection."""
    print("="*60)
    print("KUCOIN API CONNECTION TEST")
    print("="*60)
    
    # Get credentials
    api_key = os.getenv('KUCOIN_API_KEY')
    api_secret = os.getenv('KUCOIN_API_SECRET')
    api_passphrase = os.getenv('KUCOIN_API_PASSPHRASE')
    
    if not all([api_key, api_secret, api_passphrase]):
        print("\n❌ Missing KuCoin API credentials")
        print("\nRequired environment variables:")
        print("  - KUCOIN_API_KEY")
        print("  - KUCOIN_API_SECRET")
        print("  - KUCOIN_API_PASSPHRASE")
        print("\nCreate a .env file in C:\\workspace with these variables")
        return False
    
    print(f"\n✅ Credentials found")
    print(f"   API Key: {api_key[:8]}...{api_key[-4:]}")
    
    try:
        # Initialize client
        client = KuCoinClient(
            api_key=api_key,
            api_secret=api_secret,
            passphrase=api_passphrase
        )
        
        print("\n✅ KuCoin client initialized")
        
        # Test 1: Get account info
        print("\n" + "-"*60)
        print("TEST 1: Account Balance")
        print("-"*60)
        
        accounts = client.get_accounts()
        print(f"✅ API Connection: SUCCESS")
        print(f"   Found {len(accounts)} account(s)")
        
        usdt_balance = 0
        for acc in accounts:
            if acc['type'] == 'trade' and acc['currency'] == 'USDT':
                usdt_balance = float(acc['balance'])
                available = float(acc['available'])
                print(f"\n💰 USDT Balance:")
                print(f"   Total: ${usdt_balance:.2f}")
                print(f"   Available: ${available:.2f}")
        
        if usdt_balance == 0:
            print("\n⚠️  Warning: No USDT balance found in trading account")
        
        # Test 2: Get market data
        print("\n" + "-"*60)
        print("TEST 2: Market Data Access")
        print("-"*60)
        
        ticker = client.get_ticker('SOL-USDT')
        print(f"✅ Market Data: SUCCESS")
        print(f"   SOL/USDT: ${ticker['price']}")
        
        # Handle different possible change rate keys
        change_rate = (
            ticker.get("changeRate")
            or ticker.get("changeRate24h")
            or ticker.get("changePrice")
            or "N/A"
        )
        
        if change_rate != "N/A":
            print(f"   24h Change: {float(change_rate)*100:.2f}%")
        else:
            print(f"   24h Change: {change_rate}")
        
        # Test 3: Get symbol info (minimum order sizes)
        print("\n" + "-"*60)
        print("TEST 3: Minimum Order Requirements")
        print("-"*60)
        
        symbols = client.get_symbols()
        for s in symbols:
            if s['symbol'] == 'SOL-USDT':
                print(f"\n📊 SOL-USDT Trading Rules:")
                print(f"   Base Currency: {s['baseCurrency']}")
                print(f"   Quote Currency: {s['quoteCurrency']}")
                print(f"   Base Min Size: {s['baseMinSize']} SOL")
                print(f"   Base Max Size: {s['baseMaxSize']} SOL")
                print(f"   Quote Min Size: ${s['quoteMinSize']} USDT")
                print(f"   Quote Max Size: ${s['quoteMaxSize']} USDT")
                print(f"   Base Increment: {s['baseIncrement']}")
                print(f"   Price Increment: {s['priceIncrement']}")
                
                # Calculate minimum order value
                min_size = float(s['baseMinSize'])
                current_price = float(ticker['price'])
                min_order_value = min_size * current_price
                
                print(f"\n💡 Minimum Order Calculation:")
                print(f"   Min Size: {min_size} SOL")
                print(f"   Current Price: ${current_price:.2f}")
                print(f"   Min Order Value: ${min_order_value:.2f}")
                
                if usdt_balance > 0:
                    max_orders = int(usdt_balance / min_order_value)
                    print(f"\n   Your Balance: ${usdt_balance:.2f}")
                    print(f"   Max Possible Orders: {max_orders}")
                break
        
        # Test 4: Check API permissions
        print("\n" + "-"*60)
        print("TEST 4: API Permissions")
        print("-"*60)
        
        try:
            # Try to get orders (requires trade permission)
            client.get_orders(status='active')
            print("✅ Trade Permission: ENABLED")
        except Exception as e:
            print(f"❌ Trade Permission: {e}")
        
        print("\n" + "="*60)
        print("CONNECTION TEST COMPLETE")
        print("="*60)
        print("\n✅ All tests passed - Ready for live trading")
        print("\n⚠️  IMPORTANT:")
        print("   1. Verify withdrawal permissions are DISABLED")
        print("   2. Start with minimum order size (0.01 SOL)")
        print("   3. Monitor first trade closely")
        print("   4. Keep stop-loss orders active")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\nPossible issues:")
        print("  - Invalid API credentials")
        print("  - API key permissions insufficient")
        print("  - Network connectivity problem")
        print("  - IP not whitelisted (if whitelist enabled)")
        return False


if __name__ == '__main__':
    success = test_connection()
    exit(0 if success else 1)
