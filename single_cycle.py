"""
Single-Cycle Trading Bot - Test/Validation Mode
Runs ONE complete trading cycle and exits.

Use this for:
- Quick market checks
- Testing changes safely
- Validating configuration
- Getting current price data
- Confirming constitutional restraint

For continuous monitoring, use continuous_trading.py instead.
"""

import logging
import sys
from datetime import datetime

from agents import (
    OrchestratorAgent,
    DataFetchingAgent,
    MarketAnalysisAgent,
    RiskManagementAgent,
    BacktestingAgent,
    ExecutionAgent,
    MonitoringAgent
)

# Import configuration
try:
    from config import TRADING_CONFIG, RISK_CONFIG, API_CONFIG, ENTRY_TIMING_CONFIG
    CONFIG_LOADED = True
except ImportError:
    CONFIG_LOADED = False
    TRADING_CONFIG = None
    RISK_CONFIG = None
    API_CONFIG = None
    ENTRY_TIMING_CONFIG = None


def setup_logging():
    """Setup root logger configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(name)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def initialize_agents(config: dict) -> dict:
    """Initialize and register all trading agents."""
    print("\n" + "="*60)
    print("  Single-Cycle Test Mode")
    print("  (For continuous monitoring, use continuous_trading.py)")
    print("="*60 + "\n")
    
    orchestrator = OrchestratorAgent(config.get('orchestrator', {}))
    
    print("Initializing agents...")
    
    data_agent = DataFetchingAgent(config.get('data_fetcher', {}))
    orchestrator.register_agent(data_agent)
    
    market_agent = MarketAnalysisAgent(config.get('market_analyzer', {}))
    orchestrator.register_agent(market_agent)
    
    risk_agent = RiskManagementAgent(config.get('risk_manager', {}))
    orchestrator.register_agent(risk_agent)
    
    backtest_agent = BacktestingAgent(config.get('backtester', {}))
    orchestrator.register_agent(backtest_agent)
    
    exec_agent = ExecutionAgent(config.get('executor', {}))
    orchestrator.register_agent(exec_agent)
    
    monitor_agent = MonitoringAgent(config.get('monitor', {}))
    orchestrator.register_agent(monitor_agent)
    
    print("[OK] All 6 agents initialized and registered\n")
    
    return {
        'orchestrator': orchestrator,
        'data_fetcher': data_agent,
        'market_analyzer': market_agent,
        'risk_manager': risk_agent,
        'backtester': backtest_agent,
        'executor': exec_agent,
        'monitor': monitor_agent
    }


def print_system_status(agents: dict):
    """Print current system status."""
    orchestrator = agents['orchestrator']
    status = orchestrator.get_system_status()
    
    print("\n" + "="*60)
    print("  System Status Report")
    print("="*60)
    print(f"Orchestrator: {status['orchestrator']['status']}")
    print(f"Trading Paused: {status['trading_paused']}")
    print(f"Circuit Breaker: {status['circuit_breaker_active']}")
    print(f"Current Stage: {status['current_stage']}")
    print(f"\nAgent Status:")
    for agent_status in status['agents']:
        print(f"  • {agent_status['name']}: {agent_status['status']}")
    print("="*60 + "\n")


def run_single_cycle(agents: dict, symbols: list):
    """Execute one complete trading cycle."""
    orchestrator = agents['orchestrator']
    executor = agents['executor']
    
    print("\n" + "="*60)
    print("  Starting Trading Cycle (SINGLE-SHOT)")
    print(f"  Symbols: {', '.join(symbols)}")
    print(f"  Time: {datetime.utcnow().isoformat()}")
    print("="*60 + "\n")
    
    result = orchestrator.execute(symbols)
    
    if not result['success']:
        print(f"\n❌ Orchestration failed: {result['error']}\n")
        return result
    
    data = result.get('data', {})
    
    print("\n" + "-"*60)
    print("Trade Cycle Results:")
    print("-"*60)
    print(f"Trade Executed: {data.get('trade_executed', False)}")
    
    if data.get('trade_executed'):
        exec_data = data.get('execution', {})
        print(f"  Trade ID: {exec_data.get('trade_id')}")
        print(f"  Entry Price: ${exec_data.get('entry_price', 0):.4f}")
        print(f"  Position Size: {exec_data.get('position_size', 0):.4f}")
        print(f"  Stop Loss: ${exec_data.get('stop_loss', 0):.4f}")
        print(f"  Take Profit: ${exec_data.get('take_profit', 0):.4f}")
    else:
        reason = data.get('reason', 'Unknown')
        print(f"  Reason: {reason}")
    
    perf = executor.get_performance_summary()
    print(f"\nPerformance Summary:")
    print(f"  Total Trades: {perf['total_trades']}")
    print(f"  Win Rate: {perf['win_rate']:.1%}")
    print(f"  Total P&L: ${perf['total_pnl']:.2f}")
    print(f"  Open Positions: {perf['open_positions']}")
    print("-"*60 + "\n")
    
    return result


def main():
    """Main entry point for single-cycle mode."""
    setup_logging()
    logger = logging.getLogger("SingleCycleBot")
    
    # Load configuration (from config.py, always paper mode for safety)
    account_balance = 100.0
    if CONFIG_LOADED and TRADING_CONFIG:
        account_balance = TRADING_CONFIG.get('account_balance', 100.0)
        logger.info(f"[CONFIG.PY] Loaded: paper_trading=True (forced), account_balance=${account_balance}")
    
    config = {
        'orchestrator': {
            'paper_trading': True
        },
        'data_fetcher': {
            'cache_timeout': 300
        },
        'market_analyzer': {
            'rsi_period': 14,
            'downtrend_threshold': -5,
            'entry_timing_config': ENTRY_TIMING_CONFIG if CONFIG_LOADED and ENTRY_TIMING_CONFIG else {'enabled': False}
        },
        'risk_manager': {
            'account_balance': account_balance,
            'risk_per_trade': 0.01,
            'min_risk_reward_ratio': 1.5,
            'max_daily_loss': 0.05,
            'min_signal_strength': 0.10,
            'min_win_rate': 0.45,
            'min_position_size_units': 0.01,
            'min_position_size_by_pair': {
                'SOL/USDT': 0.01,
                'BTC/USDT': 0.0001
            },
            'enforce_min_position_size_only': False
        },
        'backtester': {
            'min_win_rate': 0.45,
            'max_drawdown': 0.15
        },
        'executor': {
            'paper_trading': True,  # ALWAYS paper mode in single-cycle
            'live_mode': False,
            'exchange': None,
            'order_type': 'market',
        },
        'monitor': {
            'logs_dir': './logs'
        }
    }
    
    try:
        agents = initialize_agents(config)
        print_system_status(agents)
        
        trading_pairs = ['SOL/USDT']
        result = run_single_cycle(agents, trading_pairs)
        
        print_system_status(agents)
        
        executor = agents['executor']
        perf = executor.get_performance_summary()
        print("Final Performance Summary:")
        print(f"  Total Trades: {perf['total_trades']}")
        print(f"  Winning: {perf['winning_trades']} | Losing: {perf['losing_trades']}")
        print(f"  Win Rate: {perf['win_rate']:.1%}")
        print(f"  Total P&L: ${perf['total_pnl']:.2f}")
        print(f"  Average P&L: ${perf['avg_pnl']:.2f}")
        print(f"  Max Win: ${perf['max_win']:.2f} | Max Loss: ${perf['max_loss']:.2f}")
        print(f"  Open Positions: {perf['open_positions']}\n")
        
        logger.info("Single-cycle test completed successfully")
        return 0
    
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
