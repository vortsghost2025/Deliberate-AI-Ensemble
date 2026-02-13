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
    WAITING_FOR_NEXT_CYCLE = "waiting_for_next_cycle"  # Between cycles, prevents overlap
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
        self.workflow_history: List[Dict[str, Any]] = []  # Stage transitions
        self.workflow_trace: List[Dict[str, Any]] = []  # Complete agent message trace
        self.trading_paused = False
        self.pause_reason: Optional[str] = None
        self.pause_timestamp: Optional[datetime] = None
        self.resume_warning_given = False
        self.circuit_breaker_active = False
        self.agent_registry: Dict[str, BaseAgent] = {}
        self.logger.setLevel(logging.DEBUG)
        self.is_paper_trading = config.get('paper_trading', True)
        self._last_daily_reset: Optional[str] = None
        
        # Minimum Notional Value Awareness
        self.consecutive_notional_rejections = 0
        self.notional_rejection_threshold = 10  # Pause after 10 consecutive rejections
        self.notional_pause_duration_hours = 1.0  # Suggest 1 hour pause
    
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
        self.pause_timestamp = datetime.now()
        self.resume_warning_given = False
        self.set_status(AgentStatus.PAUSED, f"Trading paused: {reason}")
        self.logger.warning(f"[WARN] 🧊 SNOEPILE FREEZE: Trading paused at {self.pause_timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {reason}")
    
    def resume_trading(self, reason: str = "Manual resume") -> None:
        """Resume trading after pause."""
        pause_duration = None
        if self.pause_timestamp:
            pause_duration = (datetime.now() - self.pause_timestamp).total_seconds() / 3600
        
        self.trading_paused = False
        old_reason = self.pause_reason
        self.pause_reason = None
        self.pause_timestamp = None
        self.resume_warning_given = False
        self.set_status(AgentStatus.IDLE)
        
        duration_str = f" (paused for {pause_duration:.1f} hours)" if pause_duration else ""
        self.logger.info(f"[INFO] 🌱 SNOEPILE THAW: Trading resumed{duration_str} - Reason: {reason} | Previous pause: {old_reason}")
    
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
    
    def _handle_notional_rejection(self, rejection_reason: str, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intelligent handler for minimum notional value rejections.
        
        This method demonstrates system self-awareness: the bot understands its own
        limitations in context and makes strategic decisions rather than just failing.
        
        Args:
            rejection_reason: The rejection reason from risk manager
            risk_data: Full risk assessment data
            
        Returns:
            Final result message with intelligent handling
        """
        self.consecutive_notional_rejections += 1
        
        # Extract details from risk data for intelligent logging
        assessments = risk_data.get('assessments', {})
        first_pair = list(assessments.keys())[0] if assessments else 'Unknown'
        pair = assessments.get(first_pair, {}).get('pair', first_pair) if assessments else 'Unknown'
        account_balance = risk_data.get('account_balance', 0)
        
        # Log with intelligence - explain WHY, not just WHAT
        self.logger.info(
            f"[INTELLIGENCE] Trade signal valid but position size rejected due to minimum notional constraints. "
            f"This is expected behavior with current account balance ${account_balance:.2f}. "
            f"Continuing to monitor. (Consecutive: {self.consecutive_notional_rejections})"
        )
        
        # Adaptive behavior: After repeated rejections, take strategic action
        if self.consecutive_notional_rejections >= self.notional_rejection_threshold:
            pause_message = (
                f"Detected {self.consecutive_notional_rejections} consecutive minimum notional rejections. "
                f"Account balance (${account_balance:.2f}) is below effective trading threshold for {pair}. "
                f"RECOMMENDATION: Increase account balance to $500+ or adjust risk parameters. "
                f"Pausing trading for {self.notional_pause_duration_hours} hour(s) to avoid unnecessary cycles."
            )
            self.logger.warning(f"[ADAPTIVE INTELLIGENCE] {pause_message}")
            
            # Pause trading strategically
            self.pause_trading(f"Account too small for minimum notional (${account_balance:.2f})")
            
            # Reset counter after taking action
            self.consecutive_notional_rejections = 0
            
            return self.create_message(
                action='orchestrate_workflow',
                success=True,
                data={
                    'trade_executed': False,
                    'reason': 'notional_rejection_pause',
                    'intelligence': pause_message,
                    'recommendation': 'Increase account balance to $500+ or adjust risk parameters',
                    'pause_duration_hours': self.notional_pause_duration_hours
                }
            )
        
        # Normal operation - just monitoring
        return self.create_message(
            action='orchestrate_workflow',
            success=True,
            data={
                'trade_executed': False,
                'reason': 'notional_rejection',
                'consecutive_count': self.consecutive_notional_rejections,
                'threshold': self.notional_rejection_threshold
            }
        )
    
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
        
        # Track results for monitoring/auditing (always populated, even on rejection)
        cycle_results = {
            'data_result': None,
            'analysis_result': None,
            'backtest_result': None,
            'risk_result': None,
            'exec_result': None,
            'final_result': None
        }
        
        try:
            # Daily risk reset (UTC)
            self._reset_daily_risk_if_needed()

            # Check if trading is allowed
            allowed, reason = self.is_trading_allowed()
            if not allowed:
                cycle_results['final_result'] = self.create_message(
                    action='orchestrate_workflow',
                    success=False,
                    error=f"Trading not allowed: {reason}",
                    data={'trading_allowed': False, 'reason': reason}
                )
                return cycle_results['final_result']
            
            self.logger.info(f"Starting workflow for symbols: {market_symbols}")
            
            # Step 1: Data Fetching
            self.transition_stage(WorkflowStage.FETCHING_DATA)
            data_result = self._execute_agent_phase(
                'DataFetchingAgent',
                'fetch_data',
                {'symbols': market_symbols}
            )
            cycle_results['data_result'] = data_result
            
            if not data_result['success']:
                self.activate_circuit_breaker("Data fetching failed")
                cycle_results['final_result'] = data_result
                return data_result

            if not self._validate_agent_output(data_result, 'DataFetchingAgent', ['market_data']):
                cycle_results['final_result'] = self.create_message(
                    action='orchestrate_workflow',
                    success=False,
                    error='Unexpected DataFetchingAgent response'
                )
                return cycle_results['final_result']
            
            market_data = data_result.get('data', {}).get('market_data', {})
            if not self._validate_market_data(market_data):
                self.logger.error("No market data returned from DataFetchingAgent")
                self.activate_circuit_breaker("Data fetching returned empty market data")
                cycle_results['final_result'] = self.create_message(
                    action='orchestrate_workflow',
                    success=False,
                    error='Empty market data from DataFetchingAgent'
                )
                return cycle_results['final_result']
            
            # Step 2: Market Analysis
            self.transition_stage(WorkflowStage.ANALYZING_MARKET)
            analysis_result = self._execute_agent_phase(
                'MarketAnalysisAgent',
                'analyze_market',
                {'market_data': market_data}
            )
            cycle_results['analysis_result'] = analysis_result
            
            if not analysis_result['success']:
                self.logger.error("Market analysis failed - BLOCKING TRADES")
                cycle_results['final_result'] = analysis_result
                return analysis_result
            elif not self._validate_agent_output(analysis_result, 'MarketAnalysisAgent', ['analysis', 'regime']):
                cycle_results['final_result'] = self.create_message(
                    action='orchestrate_workflow',
                    success=False,
                    error='Unexpected MarketAnalysisAgent response'
                )
                return cycle_results['final_result']
            
            analysis_data = analysis_result.get('data', {})
            
            # Check market regime - CRITICAL SAFETY FEATURE
            market_regime = analysis_data.get('regime', 'unknown')
            
            # 🧊 SNOEPILE AUTO RESUME PROTOCOL
            if self.trading_paused and not self.circuit_breaker_active:
                # Check if conditions are good for auto-resume
                if market_regime in ['neutral', 'bullish']:
                    if not self.resume_warning_given:
                        # First cycle: give warning
                        self.resume_warning_given = True
                        self.logger.info(f"[INFO] ☀️ SNOEPILE WARMING: Market regime is {market_regime}. Will auto-resume next cycle if conditions hold.")
                        cycle_results['final_result'] = self.create_message(
                            action='orchestrate_workflow',
                            success=True,
                            data={'trading_paused': True, 'resume_warning': True, 'regime': market_regime},
                        )
                        return cycle_results['final_result']
                    else:
                        # Second cycle: auto-resume
                        self.resume_trading(f"Auto-resume: Market regime improved to {market_regime}")
                        self.logger.info(f"[INFO] 🌱 Auto-resumed trading - market regime: {market_regime}")
                        # Continue to trading logic below
                else:
                    # Still bearish, reset warning
                    self.resume_warning_given = False
            
            # Pause if entering bearish regime
            if market_regime == 'bearish' and not self.trading_paused:
                self.pause_trading("Bearish market regime detected - downtrend protection active")
                cycle_results['final_result'] = self.create_message(
                    action='orchestrate_workflow',
                    success=True,
                    data={'trading_paused': True, 'reason': 'bearish_regime'},
                )
                return cycle_results['final_result']
            
            # If still paused (and not auto-resuming), skip trading
            if self.trading_paused:
                cycle_results['final_result'] = self.create_message(
                    action='orchestrate_workflow',
                    success=True,
                    data={'trading_paused': True, 'reason': self.pause_reason},
                )
                return cycle_results['final_result']
            
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
            cycle_results['backtest_result'] = backtest_result
            
            if not backtest_result['success']:
                self.logger.error("Backtesting failed - BLOCKING TRADES")
                cycle_results['final_result'] = backtest_result
                return backtest_result
            elif not self._validate_agent_output(backtest_result, 'BacktestingAgent', ['backtest_results']):
                cycle_results['final_result'] = self.create_message(
                    action='orchestrate_workflow',
                    success=False,
                    error='Unexpected BacktestingAgent response'
                )
                return cycle_results['final_result']
            
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
            cycle_results['risk_result'] = risk_result
            
            if not risk_result['success']:
                self.logger.error("Risk assessment failed - BLOCKING TRADES")
                cycle_results['final_result'] = risk_result
                return risk_result
            if not self._validate_agent_output(risk_result, 'RiskManagementAgent', ['position_approved']):
                cycle_results['final_result'] = self.create_message(
                    action='orchestrate_workflow',
                    success=False,
                    error='Unexpected RiskManagementAgent response'
                )
                return cycle_results['final_result']
            
            risk_data = risk_result['data']
            
            # Check risk thresholds
            if not risk_data.get('position_approved', False):
                rejection_reason = risk_data.get('rejection_reason')
                self.logger.warning(f"Position rejected by risk manager: {rejection_reason}")
                reason_lower = (rejection_reason or '').lower()
                
                # Critical risk limits - activate circuit breaker
                if 'daily loss limit' in reason_lower or 'risk limit' in reason_lower:
                    self.activate_circuit_breaker("Risk limit hit - trading halted")
                    cycle_results['final_result'] = self.create_message(
                        action='orchestrate_workflow',
                        success=False,
                        error='Risk limit hit - trading halted'
                    )
                    return cycle_results['final_result']
                
                # Intelligent handling for minimum notional rejections
                if 'notional' in reason_lower and 'below minimum' in reason_lower:
                    cycle_results['final_result'] = self._handle_notional_rejection(rejection_reason, risk_data)
                    return cycle_results['final_result']
                
                # Generic rejection - reset notional counter (different issue)
                self.consecutive_notional_rejections = 0
                cycle_results['final_result'] = self.create_message(
                    action='orchestrate_workflow',
                    success=True,
                    data={'trade_executed': False, 'reason': 'risk_rejection'}
                )
                return cycle_results['final_result']
            
            # Trade approved - reset notional rejection counter
            self.consecutive_notional_rejections = 0
            
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
            cycle_results['exec_result'] = exec_result
            
            if not self._validate_agent_output(exec_result, 'ExecutionAgent', ['trade_executed']):
                cycle_results['final_result'] = self.create_message(
                    action='orchestrate_workflow',
                    success=False,
                    error='Unexpected ExecutionAgent response'
                )
                return cycle_results['final_result']

            # Optional balance update after execution
            self._update_account_balance_if_provided(exec_result)
            
            # Return final orchestration result
            cycle_results['final_result'] = self.create_message(
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
            
            self.transition_stage(WorkflowStage.WAITING_FOR_NEXT_CYCLE)
            self.log_execution_end("orchestrate_trading_workflow", success=True)
            return cycle_results['final_result']
        
        except Exception as e:
            error_msg = f"Orchestration error: {str(e)}"
            self.activate_circuit_breaker(error_msg)
            self.log_execution_end("orchestrate_trading_workflow", success=False)
            cycle_results['final_result'] = self.create_message(
                action='orchestrate_workflow',
                success=False,
                error=error_msg
            )
            return cycle_results['final_result']
        
        finally:
            # CRITICAL: Always run monitoring and auditing, regardless of outcome
            # This ensures we log rejections, not just executions
            
            # Step 6: Monitoring & Logging (UNCONDITIONAL)
            self.transition_stage(WorkflowStage.MONITORING)
            monitoring_result = self._execute_agent_phase(
                'MonitoringAgent',
                'log_and_monitor',
                {
                    'workflow_stage': WorkflowStage.MONITORING.value,
                    'workflow_trace': self.workflow_trace,  # Full or partial audit trail
                    'data_result': cycle_results.get('data_result'),
                    'analysis_result': cycle_results.get('analysis_result'),
                    'backtest_result': cycle_results.get('backtest_result'),
                    'risk_result': cycle_results.get('risk_result'),
                    'exec_result': cycle_results.get('exec_result'),
                    'final_result': cycle_results.get('final_result')
                }
            )
            
            # Step 7: Post-Cycle Safety Audit (Last Line of Defense) (UNCONDITIONAL)
            if 'AuditorAgent' in self.agent_registry:
                audit_result = self._execute_agent_phase(
                    'AuditorAgent',
                    'audit_safety_checks',
                    {'workflow_trace': self.workflow_trace}
                )
                
                # If audit failed, trigger circuit breaker
                audit_data = audit_result.get('data', {})
                if not audit_data.get('audit_passed', True):
                    violations = audit_data.get('violations', [])
                    violation_summary = '; '.join(violations)
                    self.logger.critical(f"POST-CYCLE AUDIT FAILED: {violation_summary}")
                    # Don't activate circuit breaker here - cycle already returned
                    # But log prominently for human intervention
    
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
            
            # Add to workflow trace for complete auditability
            self.workflow_trace.append(result)
            
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
