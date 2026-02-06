"""
Orchestrator Agent - Main Conductor
The central brain of the multi-agent trading system.
Manages workflow, coordinates handoffs between agents, and ensures all safety checks.
"""

import logging
from typing import Any, Dict, Optional, List
from datetime import datetime
from enum import Enum

from .base_agent import BaseAgent, AgentStatus


class WorkflowStage(Enum):
    """Stages of the trading decision workflow."""
    IDLE = "idle"
    FETCHING_DATA = "fetching_data"
    ANALYZING_MARKET = "analyzing_market"
    BACKTESTING = "backtesting"
    RISK_ASSESSMENT = "risk_assessment"
    EXECUTING = "executing"
    MONITORING = "monitoring"
    ERROR = "error"
    PAUSED = "paused"


class OrchestratorAgent(BaseAgent):
    """
    Orchestrator Agent: Main coordinator of the trading bot system.
    
    Responsibilities:
    - Manage workflow state transitions
    - Coordinate handoffs between agents
    - Enforce safety checks and circuit breakers
    - Handle errors and recovery
    - Log all decision points
    - Block trades during unfavorable market conditions (downtrends, etc.)
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the orchestrator."""
        super().__init__("OrchestratorAgent", config)
        config = config or {}
        self.current_stage = WorkflowStage.IDLE
        self.workflow_history: List[Dict[str, Any]] = []
        self.trading_paused = False
        self.pause_reason: Optional[str] = None
        self.circuit_breaker_active = False
        self.agent_registry: Dict[str, BaseAgent] = {}
        self.logger.setLevel(logging.DEBUG)
        self.is_paper_trading = config.get('paper_trading', True)
        self._last_daily_reset: Optional[str] = None
    
    def register_agent(self, agent: BaseAgent) -> None:
        """
        Register a sub-agent with the orchestrator.
        
        Args:
            agent: Agent instance to register
        """
        self.agent_registry[agent.agent_name] = agent
        self.logger.info(f"Registered agent: {agent.agent_name}")
    
    def pause_trading(self, reason: str) -> None:
        """
        Pause all trading activity with a reason.
        
        Args:
            reason: Reason for pausing (e.g., 'downtrend_detected', 'max_loss_reached')
        """
        self.trading_paused = True
        self.pause_reason = reason
        self.set_status(AgentStatus.PAUSED, f"Trading paused: {reason}")
        self.logger.warning(f"[WARN] TRADING PAUSED: {reason}")
    
    def resume_trading(self) -> None:
        """Resume trading after pause."""
        self.trading_paused = False
        self.pause_reason = None
        self.set_status(AgentStatus.IDLE)
        self.logger.info("Trading resumed")
    
    def activate_circuit_breaker(self, reason: str) -> None:
        """
        Activate circuit breaker (emergency stop).
        
        Args:
            reason: Reason for activation (e.g., 'excessive_losses', 'connectivity_error')
        """
        self.circuit_breaker_active = True
        self.trading_paused = True
        self.pause_reason = f"Circuit breaker: {reason}"
        self.set_status(AgentStatus.ERROR, f"Circuit breaker activated: {reason}")
        self.logger.critical(f"[CRITICAL] CIRCUIT BREAKER ACTIVATED: {reason}")
    
    def is_trading_allowed(self) -> tuple[bool, Optional[str]]:
        """
        Check if trading is currently allowed.
        
        Returns:
            Tuple of (is_allowed, reason_if_not_allowed)
        """
        if self.circuit_breaker_active:
            return False, "Circuit breaker is active"
        if self.trading_paused:
            return False, self.pause_reason
        return True, None
    
    def transition_stage(self, new_stage: WorkflowStage, metadata: Optional[Dict] = None) -> None:
        """
        Transition to a new workflow stage and log it.
        
        Args:
            new_stage: New workflow stage
            metadata: Optional metadata about the transition
        """
        old_stage = self.current_stage
        self.current_stage = new_stage
        
        history_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'from_stage': old_stage.value,
            'to_stage': new_stage.value,
            'metadata': metadata or {}
        }
        self.workflow_history.append(history_entry)
        
        self.logger.info(f"Workflow: {old_stage.value} → {new_stage.value}")

    def _reset_daily_risk_if_needed(self) -> None:
        """Reset daily risk once per UTC day if RiskManagementAgent is registered."""
        today = datetime.utcnow().date().isoformat()
        if self._last_daily_reset == today:
            return

        risk_agent = self.agent_registry.get('RiskManagementAgent')
        if risk_agent and hasattr(risk_agent, 'reset_daily_risk'):
            risk_agent.reset_daily_risk()
            self.logger.info("Daily risk reset executed")
        self._last_daily_reset = today

    def _update_account_balance_if_provided(self, exec_result: Dict[str, Any]) -> None:
        """Update account balance if execution result contains a balance value."""
        exec_data = exec_result.get('data', {}) if isinstance(exec_result, dict) else {}
        new_balance = exec_data.get('account_balance') or exec_data.get('balance')
        if new_balance is None:
            return

        risk_agent = self.agent_registry.get('RiskManagementAgent')
        if risk_agent and hasattr(risk_agent, 'update_account_balance'):
            risk_agent.update_account_balance(float(new_balance))
            self.logger.info(f"Account balance updated from execution: {new_balance}")

    def _validate_agent_output(
        self,
        result: Dict[str, Any],
        agent_name: str,
        required_data_keys: Optional[List[str]] = None
    ) -> bool:
        """Validate agent output structure and trigger circuit breaker on unexpected shapes."""
        if not isinstance(result, dict):
            self.activate_circuit_breaker(f"{agent_name} returned non-dict response")
            return False
        if result.get('success') is False:
            return True
        data = result.get('data')
        if not isinstance(data, dict):
            self.activate_circuit_breaker(f"{agent_name} returned malformed data payload")
            return False
        if required_data_keys:
            missing = [k for k in required_data_keys if k not in data]
            if missing:
                self.activate_circuit_breaker(
                    f"{agent_name} missing required fields: {', '.join(missing)}"
                )
                return False
        return True

    def _validate_market_data(self, market_data: Dict[str, Any]) -> bool:
        if not isinstance(market_data, dict) or not market_data:
            return False
        for pair, data in market_data.items():
            if not isinstance(data, dict):
                return False
            price = data.get('current_price')
            if not isinstance(price, (int, float)) or price <= 0:
                self.logger.error("Unexpected market data for %s: %s", pair, data)
                return False
        return True
    
    def execute(self, market_symbols: List[str], *args, **kwargs) -> Dict[str, Any]:
        """
        Execute the main orchestration workflow.
        
        Args:
            market_symbols: List of trading pairs to analyze (e.g., ['SOL/USDT', 'BTC/USDT'])
            
        Returns:
            Orchestration result message
        """
        self.log_execution_start("orchestrate_trading_workflow")
        
        try:
            # Daily risk reset (UTC)
            self._reset_daily_risk_if_needed()

            # Check if trading is allowed
            allowed, reason = self.is_trading_allowed()
            if not allowed:
                return self.create_message(
                    action='orchestrate_workflow',
                    success=False,
                    error=f"Trading not allowed: {reason}",
                    data={'trading_allowed': False, 'reason': reason}
                )
            
            self.logger.info(f"Starting workflow for symbols: {market_symbols}")
            
            # Step 1: Data Fetching
            self.transition_stage(WorkflowStage.FETCHING_DATA)
            data_result = self._execute_agent_phase(
                'DataFetchingAgent',
                'fetch_data',
                {'symbols': market_symbols}
            )
            if not data_result['success']:
                self.activate_circuit_breaker("Data fetching failed")
                return data_result

            if not self._validate_agent_output(data_result, 'DataFetchingAgent', ['market_data']):
                return self.create_message(
                    action='orchestrate_workflow',
                    success=False,
                    error='Unexpected DataFetchingAgent response'
                )
            
            market_data = data_result.get('data', {}).get('market_data', {})
            if not self._validate_market_data(market_data):
                self.logger.error("No market data returned from DataFetchingAgent")
                self.activate_circuit_breaker("Data fetching returned empty market data")
                return self.create_message(
                    action='orchestrate_workflow',
                    success=False,
                    error='Empty market data from DataFetchingAgent'
                )
            
            # Step 2: Market Analysis
            self.transition_stage(WorkflowStage.ANALYZING_MARKET)
            analysis_result = self._execute_agent_phase(
                'MarketAnalysisAgent',
                'analyze_market',
                {'market_data': market_data}
            )
            if not analysis_result['success']:
                self.logger.error("Market analysis failed - BLOCKING TRADES")
                return analysis_result
            elif not self._validate_agent_output(analysis_result, 'MarketAnalysisAgent', ['analysis', 'regime']):
                return self.create_message(
                    action='orchestrate_workflow',
                    success=False,
                    error='Unexpected MarketAnalysisAgent response'
                )
            
            analysis_data = analysis_result.get('data', {})
            
            # Check market regime - CRITICAL SAFETY FEATURE
            market_regime = analysis_data.get('regime', 'unknown')
            if market_regime == 'bearish':
                self.pause_trading("Bearish market regime detected - downtrend protection active")
                return self.create_message(
                    action='orchestrate_workflow',
                    success=True,
                    data={'trading_paused': True, 'reason': 'bearish_regime'},
                )
            
            # Step 3: Backtesting
            self.transition_stage(WorkflowStage.BACKTESTING)
            backtest_result = self._execute_agent_phase(
                'BacktestingAgent',
                'backtest_signals',
                {
                    'market_data': market_data,
                    'analysis': analysis_data.get('analysis', {})
                }
            )
            if not backtest_result['success']:
                self.logger.error("Backtesting failed - BLOCKING TRADES")
                return backtest_result
            elif not self._validate_agent_output(backtest_result, 'BacktestingAgent', ['backtest_results']):
                return self.create_message(
                    action='orchestrate_workflow',
                    success=False,
                    error='Unexpected BacktestingAgent response'
                )
            
            backtest_data = backtest_result.get('data', {})
            
            # Step 4: Risk Management
            self.transition_stage(WorkflowStage.RISK_ASSESSMENT)
            risk_result = self._execute_agent_phase(
                'RiskManagementAgent',
                'assess_and_size_position',
                {
                    'market_data': market_data,
                    'analysis': analysis_data.get('analysis', {}),
                    'backtest_results': backtest_data.get('backtest_results', {})
                }
            )
            if not risk_result['success']:
                self.logger.error("Risk assessment failed - BLOCKING TRADES")
                return risk_result
            if not self._validate_agent_output(risk_result, 'RiskManagementAgent', ['position_approved']):
                return self.create_message(
                    action='orchestrate_workflow',
                    success=False,
                    error='Unexpected RiskManagementAgent response'
                )
            
            risk_data = risk_result['data']
            
            # Check risk thresholds
            if not risk_data.get('position_approved', False):
                rejection_reason = risk_data.get('rejection_reason')
                self.logger.warning(f"Position rejected by risk manager: {rejection_reason}")
                reason_lower = (rejection_reason or '').lower()
                if 'daily loss limit' in reason_lower or 'risk limit' in reason_lower:
                    self.activate_circuit_breaker("Risk limit hit - trading halted")
                    return self.create_message(
                        action='orchestrate_workflow',
                        success=False,
                        error='Risk limit hit - trading halted'
                    )
                return self.create_message(
                    action='orchestrate_workflow',
                    success=True,
                    data={'trade_executed': False, 'reason': 'risk_rejection'}
                )
            
            # Step 5: Execution (Paper Trading by Default)
            self.transition_stage(WorkflowStage.EXECUTING)
            exec_result = self._execute_agent_phase(
                'ExecutionAgent',
                'execute_trade',
                {
                    'market_data': market_data,
                    'position_size': risk_data.get('position_size'),
                    'stop_loss': risk_data.get('stop_loss'),
                    'take_profit': risk_data.get('take_profit'),
                    'paper_trading': self.is_paper_trading,
                    'account_balance': risk_data.get('account_balance'),
                    'position_approved': risk_data.get('position_approved', False),
                    'risk_approved': risk_data.get('position_approved', False)
                }
            )
            if not self._validate_agent_output(exec_result, 'ExecutionAgent', ['trade_executed']):
                return self.create_message(
                    action='orchestrate_workflow',
                    success=False,
                    error='Unexpected ExecutionAgent response'
                )

            # Optional balance update after execution
            self._update_account_balance_if_provided(exec_result)
            
            # Step 6: Monitoring & Logging
            self.transition_stage(WorkflowStage.MONITORING)
            monitoring_result = self._execute_agent_phase(
                'MonitoringAgent',
                'log_and_monitor',
                {
                    'workflow_stage': WorkflowStage.MONITORING.value,
                    'data_result': data_result,
                    'analysis_result': analysis_result,
                    'risk_result': risk_result,
                    'exec_result': exec_result
                }
            )
            
            # Return final orchestration result
            self.transition_stage(WorkflowStage.IDLE)
            self.log_execution_end("orchestrate_trading_workflow", success=True)
            
            return self.create_message(
                action='orchestrate_workflow',
                success=True,
                data={
                    'trade_executed': exec_result.get('success', False),
                    'analysis': analysis_data,
                    'risk_assessment': risk_data,
                    'execution': exec_result.get('data', {}),
                    'workflow_history_length': len(self.workflow_history)
                }
            )
        
        except Exception as e:
            error_msg = f"Orchestration error: {str(e)}"
            self.activate_circuit_breaker(error_msg)
            self.log_execution_end("orchestrate_trading_workflow", success=False)
            return self.create_message(
                action='orchestrate_workflow',
                success=False,
                error=error_msg
            )
    
    def _execute_agent_phase(
        self,
        agent_name: str,
        action: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a specific agent phase with error handling.
        
        Args:
            agent_name: Name of the agent to execute
            action: Action to perform
            input_data: Input data for the agent
            
        Returns:
            Result message from the agent
        """
        if agent_name not in self.agent_registry:
            error_msg = f"Agent {agent_name} not registered"
            self.logger.error(error_msg)
            return self.create_message(
                action=action,
                success=False,
                error=error_msg,
                data={'agent': agent_name}
            )
        
        try:
            agent = self.agent_registry[agent_name]
            self.logger.debug(f"Executing {agent_name}.{action}")
            result = agent.execute(input_data)
            return result
        except Exception as e:
            error_msg = f"{agent_name} execution failed: {str(e)}"
            self.logger.error(error_msg)
            return self.create_message(
                action=action,
                success=False,
                error=error_msg,
                data={'agent': agent_name}
            )
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status report."""
        agent_statuses = [
            agent.get_status_report()
            for agent in self.agent_registry.values()
        ]
        
        return {
            'orchestrator': self.get_status_report(),
            'current_stage': self.current_stage.value,
            'trading_paused': self.trading_paused,
            'pause_reason': self.pause_reason,
            'circuit_breaker_active': self.circuit_breaker_active,
            'agents': agent_statuses,
            'workflow_history_length': len(self.workflow_history),
            'timestamp': datetime.utcnow().isoformat()
        }
