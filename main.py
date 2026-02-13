"""
Multi-Agent Trading Bot - Main Entry Point
Orchestrates all agents in the trading system for autonomous crypto trading.
"""

import logging
import os
import sys
import time
from datetime import datetime
from typing import Optional

from agents import (
    OrchestratorAgent,
    DataFetchingAgent,
    MarketAnalysisAgent,
    RiskManagementAgent,
    BacktestingAgent,
    ExecutionAgent,
    MonitoringAgent,
    AuditorAgent
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
    """
    Initialize and register all trading agents.
    
    Args:
        config: Configuration dictionary for all agents
        
    Returns:
        Dictionary of initialized agents
    """
    print("\n" + "="*60)
    print("  Multi-Agent Autonomous Trading Bot")
    print("="*60 + "\n")
    
    # Create orchestrator (main conductor)
    orchestrator = OrchestratorAgent(config.get('orchestrator', {}))
    
    # Create and register all sub-agents
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
    
    auditor_agent = AuditorAgent(config.get('auditor', {}))
    orchestrator.register_agent(auditor_agent)
    
    print("[OK] All 7 agents initialized and registered\n")
    
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


def print_status_snapshot(agents: dict):
    """Print a compact one-line system status snapshot."""
    orchestrator = agents['orchestrator']
    status = orchestrator.get_system_status()
    agent_states = ", ".join(
        f"{a['name']}={a['status']}" for a in status['agents']
    )
    print(
        f"STATUS | stage={status['current_stage']} | paused={status['trading_paused']} "
        f"| breaker={status['circuit_breaker_active']} | agents=[{agent_states}]"
    )


def run_trading_cycle(agents: dict, symbols: list):
    """
    Execute one complete trading cycle.
    
    Args:
        agents: Dictionary of initialized agents
        symbols: List of trading pairs to analyze
    """
    orchestrator = agents['orchestrator']
    executor = agents['executor']
    monitor = agents['monitor']
    
    print("\n" + "="*60)
    print("  Starting Trading Cycle")
    print(f"  Symbols: {', '.join(symbols)}")
    print(f"  Time: {datetime.utcnow().isoformat()}")
    print("="*60 + "\n")
    
    # Execute orchestration workflow
    result = orchestrator.execute(symbols)
    
    if not result['success']:
        print(f"\n❌ Orchestration failed: {result['error']}\n")
        return result
    
    data = result.get('data', {})
    
    # Print results
    print("\n" + "-"*60)
    print("Trade Cycle Results:")
    print("-"*60)
    print(f"Trade Executed: {data.get('trade_executed', False)}")
    
    if data.get('trade_executed'):
        exec_data = data.get('execution', {})
        def _fmt_num(value: object, decimals: int = 4) -> str:
            if isinstance(value, (int, float)):
                return f"{value:.{decimals}f}"
            return "n/a"

        print(f"  Trade ID: {exec_data.get('trade_id')}")
        print(f"  Entry Price: ${_fmt_num(exec_data.get('entry_price'))}")
        print(f"  Position Size: {_fmt_num(exec_data.get('position_size'))}")
        print(f"  Stop Loss: ${_fmt_num(exec_data.get('stop_loss'))}")
        print(f"  Take Profit: ${_fmt_num(exec_data.get('take_profit'))}")
    else:
        reason = data.get('reason', 'Unknown')
        print(f"  Reason: {reason}")
    
    # Print performance summary
    perf = executor.get_performance_summary()
    print(f"\nPerformance Summary:")
    print(f"  Total Trades: {perf['total_trades']}")
    print(f"  Win Rate: {perf['win_rate']:.1%}")
    print(f"  Total P&L: ${perf['total_pnl']:.2f}")
    print(f"  Open Positions: {perf['open_positions']}")
    print("-"*60 + "\n")
    
    return result


def main():
    """Main entry point for the trading bot."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger("MainBot")

    def _env_bool(name: str, default: bool = False) -> bool:
        value = os.getenv(name)
        if value is None:
            return default
        return value.lower() == "true"

    def _env_float(name: str, default: Optional[float] = None) -> Optional[float]:
        value = os.getenv(name)
        if value is None:
            return default
        try:
            return float(value)
        except ValueError:
            return None

    def _env_int(name: str, default: Optional[int] = None) -> Optional[int]:
        value = os.getenv(name)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return None

    live_mode_requested = _env_bool("LIVE_MODE", False)
    exchange = os.getenv("EXCHANGE")
    live_api_key = os.getenv("LIVE_API_KEY")
    live_api_secret = os.getenv("LIVE_API_SECRET")
    order_type = os.getenv("ORDER_TYPE", "market")
    slippage_tolerance_percent = _env_float("SLIPPAGE_TOLERANCE_PERCENT")
    min_balance_usd = _env_float("MIN_BALANCE_USD")
    min_position_size_units = _env_float("MIN_POSITION_SIZE_UNITS")

    max_position_size_usd = _env_float("MAX_POSITION_SIZE_USD")
    max_trade_loss_usd = _env_float("MAX_TRADE_LOSS_USD")
    max_daily_loss_usd = _env_float("MAX_DAILY_LOSS_USD")
    max_open_positions = _env_int("MAX_OPEN_POSITIONS")
    max_trades_per_session = _env_int("MAX_TRADES_PER_SESSION")
    account_balance_usd = _env_float("ACCOUNT_BALANCE", None) or _env_float("ACCOUNT_BALANCE_USD", None)

    # Override with config.py if available (takes precedence over environment variables)
    if CONFIG_LOADED and TRADING_CONFIG:
        paper_trading_from_config = TRADING_CONFIG.get('paper_trading', True)
        live_mode_requested = not paper_trading_from_config  # Invert: False paper = True live
        account_balance_from_config = TRADING_CONFIG.get('account_balance')
        if account_balance_from_config is not None:
            account_balance_usd = float(account_balance_from_config)
        
        logger.info(f"[CONFIG.PY] Loaded: paper_trading={paper_trading_from_config}, account_balance=${account_balance_usd}, live_mode={live_mode_requested}")

    missing_live = []
    if live_mode_requested:
        if not exchange:
            missing_live.append("EXCHANGE")
        if not live_api_key:
            missing_live.append("LIVE_API_KEY")
        if not live_api_secret:
            missing_live.append("LIVE_API_SECRET")
        if max_position_size_usd is None:
            missing_live.append("MAX_POSITION_SIZE_USD")
        if max_trade_loss_usd is None:
            missing_live.append("MAX_TRADE_LOSS_USD")
        if max_daily_loss_usd is None:
            missing_live.append("MAX_DAILY_LOSS_USD")
        if max_open_positions is None:
            missing_live.append("MAX_OPEN_POSITIONS")
        if slippage_tolerance_percent is None:
            missing_live.append("SLIPPAGE_TOLERANCE_PERCENT")
        if min_balance_usd is None:
            missing_live.append("MIN_BALANCE_USD")

    live_mode = live_mode_requested and not missing_live
    if live_mode_requested and missing_live:
        logger.warning(
            "LIVE_MODE requested but missing/invalid env vars: %s. Falling back to paper trading.",
            ", ".join(missing_live),
        )
    
    # CRITICAL: Warn if live mode without balance configured
    if live_mode and not account_balance_usd:
        logger.error("CRITICAL: Live mode enabled but no ACCOUNT_BALANCE set - this is dangerous!")
        logger.error("Position sizing will be incorrect. Set ACCOUNT_BALANCE or ACCOUNT_BALANCE_USD in .env")

    logger.info(
        "Startup config: live_mode=%s, exchange=%s, order_type=%s, slippage_tolerance_percent=%s, "
        "max_position_size_usd=%s, max_trade_loss_usd=%s, max_daily_loss_usd=%s, max_open_positions=%s, min_balance_usd=%s",
        live_mode,
        exchange,
        order_type,
        slippage_tolerance_percent,
        max_position_size_usd,
        max_trade_loss_usd,
        max_daily_loss_usd,
        max_open_positions,
        min_balance_usd,
    )
    
    # Configuration for all agents
    config = {
        'orchestrator': {
            'paper_trading': not live_mode
        },
        'data_fetcher': {
            'cache_timeout': 300
        },
        'market_analyzer': {
            'rsi_period': 14,
            'downtrend_threshold': -5,  # Flag bearish if -5% or worse
            'entry_timing_config': ENTRY_TIMING_CONFIG if CONFIG_LOADED and ENTRY_TIMING_CONFIG else {'enabled': False}
        },
        'risk_manager': {
            'account_balance': account_balance_usd if account_balance_usd is not None else 10000,
            'risk_per_trade': 0.01,  # 1% risk per trade (constitutional limit)
            'min_risk_reward_ratio': 1.5,
            'max_daily_loss': 0.05,  # 5% max daily loss
            'min_signal_strength': 0.10,  # 10% minimum signal strength
            'min_win_rate': 0.45,  # 45% minimum win rate
            'min_notional_usd': 1.0,  # Minimum trade notional value (from config.py)
            'min_position_size_units': 0.01,  # Minimum 0.01 SOL
            'min_position_size_by_pair': {
                'SOL/USDT': 0.01,  # 0.01 SOL minimum
                'BTC/USDT': 0.0001  # 0.0001 BTC minimum
            },
            'enforce_min_position_size_only': False  # Use dynamic position sizing based on risk
        },
        'backtester': {
            'min_win_rate': 0.45,
            'max_drawdown': 0.15
        },
        'executor': {
            'paper_trading': not live_mode,
            'live_mode': live_mode,
            'exchange': exchange,
            'order_type': order_type,
            'slippage_tolerance_percent': slippage_tolerance_percent,
            'min_balance_usd': min_balance_usd,
            'max_position_size_usd': max_position_size_usd,
            'max_trade_loss_usd': max_trade_loss_usd,
            'max_daily_loss_usd': max_daily_loss_usd,
            'max_open_positions': max_open_positions,
            'max_trades_per_session': max_trades_per_session,
            'live_api_key': live_api_key,
            'live_api_secret': live_api_secret,
            # KuCoin API credentials from config.py
            'api_key': API_CONFIG.get('api_key') if CONFIG_LOADED and API_CONFIG else None,
            'api_secret': API_CONFIG.get('api_secret') if CONFIG_LOADED and API_CONFIG else None,
            'api_passphrase': API_CONFIG.get('api_passphrase') if CONFIG_LOADED and API_CONFIG else None,
        },
        'monitor': {
            'logs_dir': './logs'
        }
    }
    
    try:
        # Initialize all agents
        agents = initialize_agents(config)

        # Compact status snapshot command
        if len(sys.argv) > 1 and sys.argv[1].lower() == 'status':
            print_status_snapshot(agents)
            return 0
        
        # Print system status
        print_system_status(agents)
        
        # Run trading cycle(s)
        # Example: Trade Solana and Bitcoin
        trading_pairs = ['SOL/USDT']  # Focus on SOL for lifecycle validation
        
        # Read continuous mode configuration from environment
        continuous_mode = os.getenv('CONTINUOUS_MODE', 'false').lower() == 'true'
        cycle_interval = int(os.getenv('CYCLE_INTERVAL_SECONDS', '300'))
        
        if continuous_mode:
            logger.info(f"Starting in CONTINUOUS MODE with {cycle_interval}s interval")
            cycle_count = 0
            while True:
                cycle_count += 1
                logger.info(f"===== Starting Trading Cycle #{cycle_count} =====")
                
                result = run_trading_cycle(agents, trading_pairs)
                
                # Display system status after cycle
                print_system_status(agents)
                
                # Print executor performance
                executor = agents['executor']
                perf = executor.get_performance_summary()
                print(f"Performance Summary (Cycle #{cycle_count}):")
                print(f"  Total Trades: {perf['total_trades']}")
                print(f"  Winning: {perf['winning_trades']} | Losing: {perf['losing_trades']}")
                print(f"  Win Rate: {perf['win_rate']:.1%}")
                print(f"  Total P&L: ${perf['total_pnl']:.2f}")
                print(f"  Average P&L: ${perf['avg_pnl']:.2f}")
                print(f"  Max Win: ${perf['max_win']:.2f} | Max Loss: ${perf['max_loss']:.2f}")
                print(f"  Open Positions: {perf['open_positions']}\n")
                
                logger.info(f"Cycle #{cycle_count} completed. Sleeping for {cycle_interval}s...")
                time.sleep(cycle_interval)
        else:
            # Single-cycle mode (original behavior)
            result = run_trading_cycle(agents, trading_pairs)
            
            # Display system status after cycle
            print_system_status(agents)
            
            # Print executor performance
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
            
            logger.info("Trading cycle completed successfully")
        return 0
    
    except KeyboardInterrupt:
        logger.info("Trading bot interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
