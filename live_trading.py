"""
Live Trading Mode Launcher
Loads configuration from .env and executes a single trading cycle.
"""

import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Import agents
from agents.orchestrator import OrchestratorAgent
from agents.data_fetcher import DataFetchingAgent
from agents.market_analyzer import MarketAnalysisAgent
from agents.backtester import BacktestingAgent
from agents.risk_manager import RiskManagementAgent
from agents.executor import ExecutionAgent
from agents.monitor import MonitoringAgent


def print_banner():
    """Print startup banner."""
    mode = "🔴 LIVE TRADING" if os.getenv('LIVE_MODE', 'false').lower() == 'true' else "📄 PAPER TRADING"
    print("\n" + "="*70)
    print(f"  MULTI-AGENT TRADING BOT - {mode}")
    print("="*70)
    print(f"  Time: {datetime.utcnow().isoformat()}")
    print(f"  Account: ${os.getenv('ACCOUNT_BALANCE', '10000')}")
    print(f"  Risk Per Trade: {float(os.getenv('RISK_PER_TRADE', '0.01'))*100}%")
    print(f"  Trading Pairs: {os.getenv('TRADING_PAIRS', 'SOL/USDT')}")
    print("="*70 + "\n")


def get_config():
    """Build configuration from environment variables."""
    live_mode = os.getenv('LIVE_MODE', 'false').lower() == 'true'
    paper_trading = os.getenv('PAPER_TRADING', 'true').lower() == 'true'
    
    # Constitutional safety check
    if live_mode and not paper_trading:
        print("⚠️  " + "="*66)
        print("⚠️  LIVE TRADING MODE ACTIVATED")
        print("⚠️  " + "="*66)
        print("⚠️  ")
        print("⚠️  Real orders will be placed on KuCoin exchange")
        print("⚠️  Real money will be used")
        print("⚠️  Losses are permanent")
        print("⚠️  ")
        print("⚠️  Safety features active:")
        print("⚠️    - 1% risk per trade (constitutional limit)")
        print("⚠️    - 5% daily loss limit")
        print("⚠️    - Circuit breaker armed")
        print("⚠️    - Downtrend protection enabled")
        print("⚠️  ")
        print("⚠️  " + "="*66)
        
        response = input("\n⚠️  Type 'I UNDERSTAND THE RISKS' to proceed: ")
        if response != "I UNDERSTAND THE RISKS":
            print("\n❌ Live trading cancelled - safety first")
            sys.exit(0)
        print("\n✅ Proceeding with live trading...\n")
    
    config = {
        # Logging
        'logs_dir': './logs/production',
        
        # Mode
        'live_mode': live_mode,
        'paper_trading': paper_trading,
        
        # Account
        'account_balance': float(os.getenv('ACCOUNT_BALANCE', '10000')),
        
        # Exchange
        'exchange': 'kucoin',
        'api_key': os.getenv('KUCOIN_API_KEY'),
        'api_secret': os.getenv('KUCOIN_API_SECRET'),
        'api_passphrase': os.getenv('KUCOIN_API_PASSPHRASE'),
        
        # Risk (Constitutional - DO NOT CHANGE)
        'risk_per_trade': float(os.getenv('RISK_PER_TRADE', '0.01')),
        'max_daily_loss': float(os.getenv('MAX_DAILY_LOSS', '0.05')),
        
        # Position limits
        'max_position_size_usd': float(os.getenv('MAX_POSITION_SIZE_USD', '1000')),
        'max_trade_loss_usd': float(os.getenv('MAX_TRADE_LOSS_USD', '50')),
        'max_daily_loss_usd': float(os.getenv('MAX_DAILY_LOSS_USD', '200')),
        'min_balance_usd': float(os.getenv('MIN_BALANCE_USD', '500')),
        
        # Position sizing (minimum order strategy)
        'min_position_size_units': float(os.getenv('MIN_POSITION_SIZE_UNITS', '0.001')),
        'enforce_min_position_size_only': os.getenv('ENFORCE_MIN_POSITION_SIZE_ONLY', 'false').lower() == 'true',
        
        # Session limits
        'max_open_positions': int(os.getenv('MAX_OPEN_POSITIONS', '1')),
        'max_trades_per_session': int(os.getenv('MAX_TRADES_PER_SESSION', '2')),
        
        # Order execution
        'order_type': os.getenv('ORDER_TYPE', 'limit'),
        'slippage_tolerance_percent': float(os.getenv('SLIPPAGE_TOLERANCE_PERCENT', '0.5')),
    }
    
    return config


def main():
    """Execute one trading cycle."""
    print_banner()
    
    # Get configuration
    config = get_config()
    
    # Initialize agents
    print("Initializing agents...")
    data_fetcher = DataFetchingAgent(config)
    market_analyzer = MarketAnalysisAgent(config)
    backtester = BacktestingAgent(config)
    risk_manager = RiskManagementAgent(config)
    executor = ExecutionAgent(config)
    monitor = MonitoringAgent(config)
    
    # Initialize orchestrator
    orchestrator = OrchestratorAgent(config)
    orchestrator.register_agent(data_fetcher)
    orchestrator.register_agent(market_analyzer)
    orchestrator.register_agent(backtester)
    orchestrator.register_agent(risk_manager)
    orchestrator.register_agent(executor)
    orchestrator.register_agent(monitor)
    
    print("✅ All agents initialized\n")
    
    # Get trading pairs
    trading_pairs = os.getenv('TRADING_PAIRS', 'SOL/USDT').split(',')
    trading_pairs = [p.strip() for p in trading_pairs]
    
    print(f"Trading Pairs: {', '.join(trading_pairs)}")
    print(f"Starting trading cycle...\n")
    
    # Execute cycle
    try:
        result = orchestrator.execute(trading_pairs)
        
        print("\n" + "="*70)
        print("CYCLE COMPLETE")
        print("="*70)
        
        if result['success']:
            data = result.get('data', {})
            print(f"\n✅ Success: {data.get('trade_executed', False)}")
            
            if data.get('trade_executed'):
                exec_data = data.get('execution', {})
                print(f"\n📊 Trade Details:")
                print(f"   Trade ID: {exec_data.get('trade_id', 'N/A')}")
                print(f"   Entry Price: ${exec_data.get('entry_price', 0):.4f}")
                print(f"   Position Size: {exec_data.get('position_size', 0):.4f}")
                print(f"   Stop Loss: ${exec_data.get('stop_loss', 0):.4f}")
                print(f"   Take Profit: ${exec_data.get('take_profit', 0):.4f}")
                
                if not config['paper_trading']:
                    print(f"\n🔴 LIVE ORDER PLACED ON KUCOIN")
                    print(f"   Order ID: {exec_data.get('order_id', 'N/A')}")
                    print(f"   Stop Order ID: {exec_data.get('stop_order_id', 'N/A')}")
                    print(f"   TP Order ID: {exec_data.get('tp_order_id', 'N/A')}")
            else:
                reason = data.get('execution', {}).get('reason', 'Unknown')
                print(f"\n⚠️  Trade not executed: {reason}")
        else:
            error = result.get('error', 'Unknown error')
            print(f"\n❌ Error: {error}")
        
        # System status
        status = orchestrator.get_system_status()
        print(f"\n📊 System Status:")
        print(f"   Trading Paused: {status['trading_paused']}")
        print(f"   Circuit Breaker: {status['circuit_breaker_active']}")
        
        # Performance summary
        perf = executor.get_performance_summary()
        print(f"\n📈 Performance:")
        print(f"   Total Trades: {perf['total_trades']}")
        print(f"   Win Rate: {perf['win_rate']*100:.1f}%")
        print(f"   Total P&L: ${perf['total_pnl']:.2f}")
        print(f"   Open Positions: {perf['open_positions']}")
        
        print("\n" + "="*70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        print("Checking for open positions...\n")
        
        open_positions = executor.get_open_positions()
        if open_positions:
            print(f"⚠️  WARNING: {len(open_positions)} open position(s)")
            print("   Please manage these manually on KuCoin\n")
        else:
            print("✅ No open positions\n")
    
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("\nCheck logs/trading_bot.log for details")
        print("If live trading, check KuCoin for open orders\n")
        raise


if __name__ == '__main__':
    main()
