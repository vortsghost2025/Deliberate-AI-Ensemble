#!/usr/bin/env python3
"""Test which KuCoin API endpoints work with our credentials."""

from kucoin.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

c = Client(
    os.getenv('KUCOIN_API_KEY'),
    os.getenv('KUCOIN_API_SECRET'),
    os.getenv('KUCOIN_API_PASSPHRASE')
)

print("Testing authenticated endpoints:\n")

# Test 1: get_accounts() - known to fail
print("1. get_accounts() [account listing]")
try:
    accounts = c.get_accounts()
    print(f"   ✅ SUCCESS: Found {len(accounts)} accounts\n")
except Exception as e:
    print(f"   ❌ FAILED: {e}\n")

# Test 2: get_account_list() - alternative method
print("2. get_account_list() [alternative account listing]")
try:
    accounts = c.get_account_list()
    print(f"   ✅ SUCCESS: Found accounts\n")
except Exception as e:
    print(f"   ❌ FAILED: {e}\n")

# Test 3: Check if we can validate orders (test mode)
print("3. create_test_order() [test order validation]")
try:
    # KuCoin's sandbox/test order endpoint
    response = c.create_test_order(
        symbol='SOL-USDT',
        side='buy',
        type='market',
        size='0.01'
    )
    print(f"   ✅ SUCCESS: Test order validated\n")
except AttributeError:
    print("   ⚠️  Method not available (library limitation)\n")
except Exception as e:
    print(f"   ❌ FAILED: {e}\n")

# Test 4: Get user info
print("4. get_user() [user account info]")
try:
    user = c.get_user()
    print(f"   ✅ SUCCESS: User info retrieved\n")
except Exception as e:
    print(f"   ❌ FAILED: {e}\n")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print("\nIf get_accounts() fails but other authenticated endpoints work,")
print("we can replace the connection test in executor.py with a working call.")
