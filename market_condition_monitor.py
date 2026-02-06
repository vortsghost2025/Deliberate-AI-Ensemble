"""
Market Condition Monitor
Continuously monitors SOL/USDT and alerts when conditions are favorable for live trading.
"""
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from agents.data_fetcher import DataFetchingAgent
from agents.market_analyzer import MarketAnalysisAgent

# Load environment
load_dotenv()

# Configuration
CHECK_INTERVAL_SECONDS = 300  # Check every 5 minutes
ALERT_SOUND = True

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print monitor header."""
    print("=" * 80)
    print(" " * 20 + "🔍 MARKET CONDITION MONITOR")
    print("=" * 80)
    print(f"Monitoring: SOL/USDT")
    print(f"Check Interval: {CHECK_INTERVAL_SECONDS} seconds ({CHECK_INTERVAL_SECONDS/60:.0f} minutes)")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()

def alert_favorable():
    """Alert user that conditions are favorable."""
    print("\n" + "🟢" * 40)
    print("🟢" + " " * 36 + "🟢")
    print("🟢" + " " * 10 + "TRADING CONDITIONS FAVORABLE" + " " * 0 + "🟢")
    print("🟢" + " " * 36 + "🟢")
    print("🟢" * 40)
    print("\n✅ Market regime is no longer bearish!")
    print("✅ You can now run: python live_trading.py")
    print()
    
    # Beep alert
    if ALERT_SOUND:
        for _ in range(3):
            print('\a', end='', flush=True)
            time.sleep(0.5)

def check_conditions():
    """Check current market conditions."""
    config = {
        'coingecko_api_key': os.getenv('COINGECKO_API_KEY'),
        'downtrend_threshold': -5
    }
    
    data_fetcher = DataFetchingAgent(config)
    market_analyzer = MarketAnalysisAgent(config)
    
    # Fetch data
    data_result = data_fetcher.execute({'symbols': ['SOL/USDT']})
    
    if not data_result['success']:
        return None, f"Data fetch failed: {data_result.get('error')}"
    
    market_data = data_result['data']['market_data']
    
    # Analyze
    analysis_result = market_analyzer.execute({'market_data': market_data})
    
    if not analysis_result['success']:
        return None, f"Analysis failed: {analysis_result.get('error')}"
    
    return analysis_result['data'], None

def display_status(analysis_data, check_count):
    """Display current market status."""
    analysis = analysis_data['analysis']['SOL/USDT']
    
    print(f"\n📊 CHECK #{check_count} - {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 80)
    
    # Current conditions
    print(f"\n💰 Price: ${analysis['current_price']:.2f}")
    
    change_color = "🔴" if analysis['price_change_24h'] < 0 else "🟢"
    print(f"{change_color} 24h Change: {analysis['price_change_24h']:+.2f}%")
    
    print(f"📈 RSI: {analysis['rsi']:.1f}")
    print(f"📉 Trend: {analysis['trend']}")
    print(f"🌊 Volatility: {analysis['volatility']}")
    
    # Regime status
    regime = analysis['regime']
    if regime == 'bearish':
        regime_icon = "🔴 BEARISH"
    elif regime == 'bullish':
        regime_icon = "🟢 BULLISH"
    elif regime == 'sideways':
        regime_icon = "🟡 SIDEWAYS"
    else:
        regime_icon = f"⚪ {regime.upper()}"
    
    print(f"\n🎯 Market Regime: {regime_icon}")
    print(f"📊 Signal Strength: {analysis['signal_strength']:.1%}")
    print(f"💡 Recommendation: {analysis['recommendation']}")
    
    # Trading decision
    downtrend = analysis_data['downtrend_detected']
    print("\n" + "=" * 80)
    if downtrend:
        print("⛔ TRADING BLOCKED - Downtrend protection active")
        print(f"   Reason: 24h change ({analysis['price_change_24h']:.2f}%) below -5% threshold")
        print(f"   Need: Price change > -5% to clear bearish status")
        
        # Progress bar showing distance to threshold
        distance_to_clear = -5 - analysis['price_change_24h']
        if distance_to_clear > 0:
            progress = max(0, min(100, (1 - distance_to_clear / 20) * 100))
            bars = int(progress / 5)
            print(f"   Recovery: [{'█' * bars}{'░' * (20 - bars)}] {progress:.0f}%")
            print(f"   ({distance_to_clear:.2f}% to go)")
    else:
        print("✅ TRADING ALLOWED - Conditions favorable")
        print("   Run: python live_trading.py")
    
    print("=" * 80)

def main():
    """Main monitoring loop."""
    clear_screen()
    print_header()
    
    check_count = 0
    last_was_bearish = None
    
    try:
        while True:
            check_count += 1
            
            # Check conditions
            analysis_data, error = check_conditions()
            
            if error:
                print(f"\n❌ Error: {error}")
                print(f"   Retrying in {CHECK_INTERVAL_SECONDS} seconds...")
            else:
                display_status(analysis_data, check_count)
                
                # Check for state change
                is_bearish = analysis_data['downtrend_detected']
                
                if last_was_bearish is True and is_bearish is False:
                    # Changed from bearish to favorable!
                    alert_favorable()
                
                last_was_bearish = is_bearish
            
            # Wait for next check
            print(f"\n⏳ Next check in {CHECK_INTERVAL_SECONDS} seconds... (Ctrl+C to stop)")
            time.sleep(CHECK_INTERVAL_SECONDS)
            
            # Clear for next check (optional, comment out to keep history)
            clear_screen()
            print_header()
    
    except KeyboardInterrupt:
        print("\n\n🛑 Monitor stopped by user")
        print(f"Total checks: {check_count}")
        print(f"Ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nThank you for using the Market Condition Monitor!")

if __name__ == '__main__':
    main()
