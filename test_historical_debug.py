#!/usr/bin/env python3
"""Debug script to understand agent data structures"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))

from agents.data_fetcher import DataFetchingAgent
from agents.market_analyzer import MarketAnalysisAgent

load_dotenv()

# Initialize agents
data_fetcher = DataFetchingAgent({
    'name': 'DebugDataFetcher',
    'role': 'data_fetcher'
})

# Fetch data
print("Fetching data...")
result = data_fetcher.execute({'symbols': ['SOL/USDT']})

print("\n" + "=" * 80)
print("FETCH RESULT STRUCTURE:")
print("=" * 80)
print(f"Status: {result.get('status')}")
print(f"Message: {result.get('message')}")
print(f"\nData keys: {list(result.get('data', {}).keys())}")
print(f"\nFull result:")
import json
print(json.dumps(result, indent=2, default=str))
