"""
Check current market conditions and analysis details.
"""
import os
from dotenv import load_dotenv
from agents.data_fetcher import DataFetchingAgent
from agents.market_analyzer import MarketAnalysisAgent

# Load environment
load_dotenv()

# Initialize agents
config = {
    'coingecko_api_key': os.getenv('COINGECKO_API_KEY'),
    'downtrend_threshold': -5  # Default threshold
}

data_fetcher = DataFetchingAgent(config)
market_analyzer = MarketAnalysisAgent(config)

print("=" * 70)
print("MARKET ANALYSIS DIAGNOSTIC")
print("=" * 70)

# Fetch current data
print("\n1. FETCHING DATA...")
data_result = data_fetcher.execute({'symbols': ['SOL/USDT']})

if data_result['success']:
    market_data = data_result['data']['market_data']
    print(f"✅ Data fetched successfully\n")
    
    # Display raw data
    for pair, data in market_data.items():
        print(f"📊 {pair} RAW DATA:")
        print(f"   Current Price: ${data['current_price']:.2f}")
        print(f"   24h Change: {data['price_change_24h_pct']:.2f}%")
        print(f"   24h Volume: ${data['volume_24h']:,.0f}")
        print()
    
    # Analyze market
    print("\n2. ANALYZING MARKET...")
    analysis_result = market_analyzer.execute({'market_data': market_data})
    
    if analysis_result['success']:
        analysis = analysis_result['data']['analysis']
        print(f"✅ Analysis complete\n")
        
        for pair, pair_analysis in analysis.items():
            print(f"📈 {pair} DETAILED ANALYSIS:")
            print(f"   Current Price: ${pair_analysis['current_price']:.2f}")
            print(f"   24h Change: {pair_analysis['price_change_24h']:.2f}%")
            print(f"   RSI (simulated): {pair_analysis['rsi']:.1f}")
            print(f"   MACD Signal: {pair_analysis['macd_signal']:.2f}")
            print(f"   Trend: {pair_analysis['trend']}")
            print(f"   Volatility: {pair_analysis['volatility']}")
            print(f"   Market Regime: {pair_analysis['regime'].upper()}")
            print(f"   Signal Strength: {pair_analysis['signal_strength']:.2%}")
            print(f"   Recommendation: {pair_analysis['recommendation']}")
            print()
        
        # Overall verdict
        print("\n3. TRADING DECISION:")
        print(f"   Overall Regime: {analysis_result['data']['regime'].upper()}")
        print(f"   Downtrend Detected: {analysis_result['data']['downtrend_detected']}")
        print(f"   Signal Confidence: {analysis_result['data']['signal_confidence']:.2%}")
        
        if analysis_result['data']['downtrend_detected']:
            print("\n   ⚠️  BEARISH REGIME - Trading blocked for safety")
            print("\n   Bearish Criteria (threshold: -5%):")
            for pair, pair_analysis in analysis.items():
                change = pair_analysis['price_change_24h']
                rsi = pair_analysis['rsi']
                regime = pair_analysis['regime']
                
                if regime == 'bearish':
                    reasons = []
                    if change < -5:
                        reasons.append(f"24h change {change:.2f}% < -5%")
                    if rsi < 30:
                        reasons.append(f"RSI {rsi:.1f} < 30 (oversold)")
                    
                    print(f"   • {pair}: {', '.join(reasons)}")
        else:
            print("\n   ✅ Conditions favorable for trading")
    else:
        print(f"❌ Analysis failed: {analysis_result.get('error')}")
else:
    print(f"❌ Data fetch failed: {data_result.get('error')}")

print("\n" + "=" * 70)
