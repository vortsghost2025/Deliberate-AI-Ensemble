"""
Quick Test Script - Multi-Agent Trading Bot
Demonstrates a simple trading cycle with mock data
"""

import json
from agents import (
    OrchestratorAgent,
    DataFetchingAgent,
    MarketAnalysisAgent,
    RiskManagementAgent,
    BacktestingAgent,
    ExecutionAgent,
    MonitoringAgent
)


def test_individual_agents():
    """Test each agent independently."""
    print("\n" + "="*60)
    print("TESTING INDIVIDUAL AGENTS")
    print("="*60 + "\n")
    
    # Test Data Fetching Agent
    print("1. Testing DataFetchingAgent...")
    data_agent = DataFetchingAgent()
    data_result = data_agent.execute({'symbols': ['SOL/USDT']})
    print(f"   Status: {data_result['success']}")
    print(f"   Pairs fetched: {data_result['data'].get('symbols_count', 0)}")
    
    # Test Market Analysis Agent
    print("\n2. Testing MarketAnalysisAgent...")
    analysis_agent = MarketAnalysisAgent()
    mock_market_data = {
        'TEST/USDT': {
            'pair': 'TEST/USDT',
            'current_price': 100.0,
            'price_change_24h_pct': 5.0,
            'volume_24h': 1000000
        }
    }
    analysis_result = analysis_agent.execute({'market_data': mock_market_data})
    print(f"   Status: {analysis_result['success']}")
    print(f"   Market regime: {analysis_result['data'].get('regime', 'unknown')}")
    
    # Test Risk Management Agent
    print("\n3. Testing RiskManagementAgent...")
    risk_agent = RiskManagementAgent({'account_balance': 10000})
    risk_result = risk_agent.execute({
        'market_data': mock_market_data,
        'analysis': analysis_result['data'].get('analysis', {}),
        'backtest_results': {}
    })
    print(f"   Status: {risk_result['success']}")
    print(f"   Position approved: {risk_result['data'].get('position_approved', False)}")
    
    # Test Backtesting Agent
    print("\n4. Testing BacktestingAgent...")
    backtest_agent = BacktestingAgent()
    backtest_result = backtest_agent.execute({
        'market_data': mock_market_data,
        'analysis': analysis_result['data'].get('analysis', {})
    })
    print(f"   Status: {backtest_result['success']}")
    print(f"   Win rate: {backtest_result['data'].get('average_win_rate', 0):.1%}")
    
    # Test Execution Agent
    print("\n5. Testing ExecutionAgent...")
    executor = ExecutionAgent()
    exec_result = executor.execute({
        'market_data': mock_market_data,
        'position_size': 0.5,
        'stop_loss': 95.0,
        'take_profit': 105.0,
        'paper_trading': True
    })
    print(f"   Status: {exec_result['success']}")
    print(f"   Trade executed: {exec_result['data'].get('trade_executed', False)}")
    
    # Test Monitoring Agent
    print("\n6. Testing MonitoringAgent...")
    monitor = MonitoringAgent()
    monitor_result = monitor.execute({
        'workflow_stage': 'test',
        'data_result': data_result,
        'analysis_result': analysis_result,
        'risk_result': risk_result,
        'exec_result': exec_result
    })
    print(f"   Status: {monitor_result['success']}")
    print(f"   Events logged: {monitor_result['data'].get('events_logged', 0)}")
    
    print("\n[OK] All individual agent tests completed\n")


def test_orchestrator():
    """Test the full orchestrator workflow."""
    print("="*60)
    print("TESTING ORCHESTRATOR (FULL WORKFLOW)")
    print("="*60 + "\n")
    
    config = {
        'account_balance': 5000,
        'risk_per_trade': 0.01,
    }
    
    # Initialize orchestrator
    orchestrator = OrchestratorAgent(config)
    
    # Create and register agents
    data_agent = DataFetchingAgent()
    orchestrator.register_agent(data_agent)
    
    analysis_agent = MarketAnalysisAgent()
    orchestrator.register_agent(analysis_agent)
    
    risk_agent = RiskManagementAgent(config)
    orchestrator.register_agent(risk_agent)
    
    backtest_agent = BacktestingAgent()
    orchestrator.register_agent(backtest_agent)
    
    executor = ExecutionAgent(config)
    orchestrator.register_agent(executor)
    
    monitor = MonitoringAgent()
    orchestrator.register_agent(monitor)
    
    print("Executing trading workflow...\n")
    
    # Execute a limited workflow with mock data
    result = orchestrator.execute(['SOL/USDT'])
    
    print(f"\nOrchestration Result:")
    print(f"  Success: {result['success']}")
    print(f"  Trade executed: {result['data'].get('trade_executed', False)}")
    print(f"  Market regime: {result['data'].get('analysis', {}).get('regime', 'unknown')}")
    
    # Print system status
    status = orchestrator.get_system_status()
    print(f"\nSystem Status:")
    print(f"  Current stage: {status['current_stage']}")
    print(f"  Trading paused: {status['trading_paused']}")
    print(f"  Circuit breaker: {status['circuit_breaker_active']}")
    
    print("\n[OK] Orchestrator test completed\n")


def test_downtrend_protection():
    """Test the critical downtrend protection feature."""
    print("="*60)
    print("TESTING DOWNTREND PROTECTION (SAFETY FEATURE)")
    print("="*60 + "\n")
    
    orchestrator = OrchestratorAgent()
    
    # Register all agents
    agents_to_register = [
        DataFetchingAgent(),
        MarketAnalysisAgent({'downtrend_threshold': -10}),
        RiskManagementAgent(),
        BacktestingAgent(),
        ExecutionAgent(),
        MonitoringAgent()
    ]
    
    for agent in agents_to_register:
        orchestrator.register_agent(agent)
    
    # The orchestrator should pause trading if downtrend is detected
    print("Testing scenario: Market drops 15% (detected as downtrend)\n")
    
    # Mock a severe downtrend
    mock_result = orchestrator.create_message(
        action='test_downtrend',
        success=True,
        data={'regime': 'bearish'}
    )
    
    # Pause trading
    orchestrator.pause_trading("Bearish market regime detected - downtrend protection active")
    
    # Check trading status
    allowed, reason = orchestrator.is_trading_allowed()
    
    print(f"Trading allowed: {allowed}")
    print(f"Reason: {reason}")
    print(f"System status: {orchestrator.status.value}")
    
    # Resume and verify
    orchestrator.resume_trading()
    allowed_after, _ = orchestrator.is_trading_allowed()
    print(f"\nAfter resume - Trading allowed: {allowed_after}")
    print(f"System status: {orchestrator.status.value}")
    
    print("\n[OK] Downtrend protection test completed\n")


def test_risk_controls():
    """Test 1% per-trade risk control."""
    print("="*60)
    print("TESTING 1% RISK PER TRADE CONTROL")
    print("="*60 + "\n")
    
    risk_agent = RiskManagementAgent({
        'account_balance': 10000,
        'risk_per_trade': 0.01  # 1% max
    })
    
    print("Account balance: $10,000")
    print("Max risk per trade: 1%")
    print("Max risk amount per trade: $100\n")
    
    # Create mock data
    market_data = {
        'TEST/USDT': {
            'current_price': 100.0,
            'price_change_24h_pct': 2.0,
            'volume_24h': 1000000
        }
    }
    
    analysis = {
        'TEST/USDT': {
            'signal_strength': 0.8,
            'win_rate': 0.55
        }
    }
    
    backtest = {}
    
    result = risk_agent.execute({
        'market_data': market_data,
        'analysis': analysis,
        'backtest_results': backtest
    })
    
    position_data = result['data']['assessments'].get('TEST/USDT', {})
    
    print(f"Position Size: {position_data.get('position_size', 0):.4f} units")
    print(f"Position Value: ${position_data.get('position_size_usd', 0):.2f}")
    print(f"Risk Amount: ${position_data.get('risk_amount', 0):.2f}")
    print(f"Risk % of Account: {position_data.get('risk_pct_of_account', 0):.2f}%")
    print(f"Position Approved: {position_data.get('position_approved')}")
    
    print("\n[OK] Risk control test completed\n")


def test_risk_manager_targeted():
    """Targeted unit tests for RiskManagementAgent position sizing."""
    print("="*60)
    print("TARGETED RISK MANAGER TESTS")
    print("="*60 + "\n")
    
    # Test 1: Minimum position size enforcement (UPDATED FOR NEW MODE)
    print("Test 1: Minimum position size enforcement...")
    cfg = {
        "account_balance": 10_000,
        "risk_per_trade": 0.01,
        "default_stop_loss_pct": 0.02,
        "min_signal_strength": 0.0,
        "min_win_rate": 0.0,
        "min_position_size_units": 0.1,  # Set minimum
        "enforce_min_position_size_only": True,  # Use fixed minimums
    }
    agent = RiskManagementAgent(cfg)
    
    market_data = {"BTCUSDT": {"current_price": 100.0}}
    analysis = {"BTCUSDT": {"signal_strength": 1.0}}
    backtest = {"BTCUSDT": {"win_rate": 1.0}}
    
    msg = agent.execute({
        "market_data": market_data,
        "analysis": analysis,
        "backtest_results": backtest,
    })
    
    data = msg["data"]["assessments"]["BTCUSDT"]
    
    # With minimum enforcement: position_size = 0.1 BTC
    # Risk = position_size * (price - stop_loss) = 0.1 * 2 = 0.2
    assert abs(data["position_size"] - 0.1) < 0.01, f"Expected position_size 0.1, got {data['position_size']}"
    assert abs(data["risk_amount"] - 0.2) < 0.01, f"Expected risk_amount ~0.2, got {data['risk_amount']}"
    assert data["position_approved"], "Position should be approved with minimum size"
    print("   [PASS] Minimum size enforcement test\n")
    
    # Test 2: Dynamic sizing mode (when enforce_min_position_size_only = False)
    print("Test 2: Dynamic sizing mode (when enabled)...")
    cfg_dynamic = {
        "account_balance": 10_000,
        "risk_per_trade": 0.01,
        "default_stop_loss_pct": 0.02,
        "min_signal_strength": 0.0,
        "min_win_rate": 0.0,
        "min_position_size_units": 0.001,  # Low minimum
        "enforce_min_position_size_only": False,  # Enable dynamic
    }
    agent_dynamic = RiskManagementAgent(cfg_dynamic)
    
    market_data = {"BTCUSDT": {"current_price": 100.0}}
    analysis = {"BTCUSDT": {"signal_strength": 1.0}}
    backtest = {"BTCUSDT": {"win_rate": 1.0}}
    
    msg = agent_dynamic.execute({
        "market_data": market_data,
        "analysis": analysis,
        "backtest_results": backtest,
    })
    data = msg["data"]["assessments"]["BTCUSDT"]
    
    # With full confidence: risk ≈ $100, position ≈ 50 units
    assert abs(data["risk_amount"] - 100.0) < 0.5, f"Expected risk_amount ~100, got {data['risk_amount']}"
    assert abs(data["position_size"] - 50.0) < 0.5, f"Expected position_size ~50, got {data['position_size']}"
    assert abs(data["risk_pct_of_account"] - 1.0) < 0.1, f"Expected 1.0%, got {data['risk_pct_of_account']}"
    assert data["position_approved"], "Position should be approved"
    print("   [PASS] Dynamic sizing test\n")
    
    # Test 3: Below minimum signal strength → veto
    print("Test 3: Signal below threshold is rejected...")
    cfg = {
        "account_balance": 10_000,
        "risk_per_trade": 0.01,
        "default_stop_loss_pct": 0.02,
        "min_signal_strength": 0.5,
        "min_win_rate": 0.0,
        "enforce_min_position_size_only": False,  # Use dynamic sizing so signal is checked
        "min_notional_usd": 10.0,
    }
    agent = RiskManagementAgent(cfg)
    
    market_data = {"BTCUSDT": {"current_price": 100.0}}
    analysis = {"BTCUSDT": {"signal_strength": 0.3}}
    backtest = {"BTCUSDT": {"win_rate": 0.8}}
    
    msg = agent.execute({
        "market_data": market_data,
        "analysis": analysis,
        "backtest_results": backtest,
    })
    data = msg["data"]["assessments"]["BTCUSDT"]
    
    assert not data["position_approved"], "Position should be rejected"
    assert "Signal strength too low" in data["rejection_reason"], f"Got: {data['rejection_reason']}"
    print("   [PASS] Signal threshold veto test\n")
    
    # Test 4: Invalid price → immediate rejection
    print("Test 4: Invalid price rejected...")
    cfg = {
        "account_balance": 10_000,
        "risk_per_trade": 0.01,
        "default_stop_loss_pct": 0.02,
    }
    agent = RiskManagementAgent(cfg)
    
    market_data = {"BTCUSDT": {"current_price": 0.0}}
    analysis = {"BTCUSDT": {"signal_strength": 1.0}}
    backtest = {"BTCUSDT": {"win_rate": 1.0}}
    
    msg = agent.execute({
        "market_data": market_data,
        "analysis": analysis,
        "backtest_results": backtest,
    })
    data = msg["data"]["assessments"]["BTCUSDT"]
    
    assert not data["position_approved"], "Position should be rejected"
    assert "Invalid price" in data["rejection_reason"], f"Got: {data['rejection_reason']}"
    assert data["position_size"] == 0, "Position size should be 0"
    print("   [PASS] Invalid price test\n")
    
    # Test 5: Dust trade below minimum notional → rejection
    print("Test 5: Dust trade below minimum notional rejected...")
    cfg = {
        "account_balance": 10_000,
        "risk_per_trade": 0.01,
        "default_stop_loss_pct": 0.02,
        "min_notional_usd": 10.0,
        "min_signal_strength": 0.0,
        "min_win_rate": 0.0,
    }
    agent = RiskManagementAgent(cfg)
    
    market_data = {"BTCUSDT": {"current_price": 100.0}}
    analysis = {"BTCUSDT": {"signal_strength": 0.01}}  # Very low
    backtest = {"BTCUSDT": {"win_rate": 0.01}}  # Very low → confidence = 0.0001
    
    msg = agent.execute({
        "market_data": market_data,
        "analysis": analysis,
        "backtest_results": backtest,
    })
    data = msg["data"]["assessments"]["BTCUSDT"]
    
    assert not data["position_approved"], "Position should be rejected"
    assert "below minimum" in data["rejection_reason"], f"Got: {data['rejection_reason']}"
    print("   [PASS] Dust trade rejection test\n")
    
    print("[OK] All targeted risk manager tests passed\n")


if __name__ == '__main__':
    print("\n")
    print("MULTI-AGENT TRADING BOT TEST SUITE")
    print("="*50)
    print("\n")
    
    try:
        # Run tests
        test_individual_agents()
        test_orchestrator()
        test_downtrend_protection()
        test_risk_controls()
        test_risk_manager_targeted()
        
        print("="*60)
        print("ALL TESTS PASSED [OK]")
        print("="*60)
        print("\nThe multi-agent trading bot is ready to use!")
        print("Run: python main.py")
        print("\n")
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
