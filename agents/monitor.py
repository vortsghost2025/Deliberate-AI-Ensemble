"""
Monitoring & Logging Agent
Logs all activity and generates performance visualizations.
Provides console alerts for important events.
"""

import json
import logging
from typing import Any, Dict, Optional, List
from datetime import datetime
import os

from .base_agent import BaseAgent, AgentStatus


class MonitoringAgent(BaseAgent):
    """
    Monitoring Agent: Central logging and performance tracking.
    
    Responsibilities:
    - Log all agent decisions and data points
    - Track performance metrics
    - Generate alerts for important events
    - Create performance visualizations
    - Maintain audit trail
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the monitoring agent."""
        super().__init__("MonitoringAgent", config)
        self.logs_dir = config.get('logs_dir', './logs') if config else './logs'
        self.log_file = os.path.join(self.logs_dir, 'trading_bot.log')
        self.events_log = os.path.join(self.logs_dir, 'events.jsonl')
        self.alerts: List[Dict[str, Any]] = []
        self.events_count = 0
        
        # Create logs directory if it doesn't exist
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Setup file logging
        self._setup_file_logging()
    
    def _setup_file_logging(self) -> None:
        """Setup file-based logging."""
        file_handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and log trading activity.
        
        Args:
            input_data: Contains workflow results from all agents
            
        Returns:
            Message with logging confirmation
        """
        self.log_execution_start("log_and_monitor")
        
        try:
            # Extract data from all phases (handle None for partial cycles)
            data_result = input_data.get('data_result') or {}
            analysis_result = input_data.get('analysis_result') or {}
            risk_result = input_data.get('risk_result') or {}
            exec_result = input_data.get('exec_result') or {}
            
            # Create comprehensive event log
            event = {
                'timestamp': datetime.utcnow().isoformat(),
                'workflow_stage': input_data.get('workflow_stage', 'unknown'),
                'data_fetch': data_result,
                'market_analysis': analysis_result,
                'risk_assessment': risk_result,
                'execution': exec_result
            }
            
            # Log the event to JSON file
            self._log_event(event)
            
            # Generate alerts for important events
            alerts = self._generate_alerts(event)
            self.alerts.extend(alerts)
            
            for alert in alerts:
                self._log_alert(alert)
            
            self.log_execution_end("log_and_monitor", success=True)
            
            return self.create_message(
                action='log_and_monitor',
                success=True,
                data={
                    'events_logged': self.events_count,
                    'alerts_generated': len(alerts),
                    'alerts': alerts,
                    'log_file': self.log_file,
                    'events_file': self.events_log
                }
            )
        
        except Exception as e:
            error_msg = f"Monitoring error: {str(e)}"
            self.set_status(AgentStatus.ERROR, error_msg)
            self.log_execution_end("log_and_monitor", success=False)
            return self.create_message(
                action='log_and_monitor',
                success=False,
                error=error_msg
            )
    
    def _log_event(self, event: Dict[str, Any]) -> None:
        """Log an event to the events file."""
        try:
            with open(self.events_log, 'a') as f:
                f.write(json.dumps(event) + '\n')
            self.events_count += 1
        except IOError as e:
            self.logger.error(f"Failed to write event log: {e}")
    
    def _log_alert(self, alert: Dict[str, Any]) -> None:
        """Log an alert."""
        level = alert.get('level', 'INFO')
        message = alert.get('message', '')
        
        if level == 'CRITICAL':
            self.logger.critical(f"[CRITICAL] {message}")
        elif level == 'WARNING':
            self.logger.warning(f"[WARN] {message}")
        elif level == 'INFO':
            self.logger.info(f"[INFO] {message}")
        else:
            self.logger.debug(message)
    
    def _generate_alerts(self, event: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate alerts based on workflow events.
        
        Args:
            event: Event dictionary
            
        Returns:
            List of alerts
        """
        alerts = []
        
        # Check execution result
        exec_result = event.get('execution', {})
        if exec_result.get('success'):
            if exec_result.get('data', {}).get('trade_executed'):
                trade_id = exec_result['data'].get('trade_id')
                entry_price = exec_result['data'].get('entry_price')
                size = exec_result['data'].get('position_size')
                entry_price_str = (
                    f"{entry_price:.4f}" if isinstance(entry_price, (int, float)) else "n/a"
                )
                size_str = (
                    f"{size:.4f}" if isinstance(size, (int, float)) else "n/a"
                )
                alerts.append({
                    'level': 'INFO',
                    'message': f'Trade #{trade_id} executed at ${entry_price_str}, size {size_str}',
                    'timestamp': datetime.utcnow().isoformat()
                })
        
        # Check risk assessment
        risk_result = event.get('risk_assessment', {})
        if not risk_result.get('data', {}).get('position_approved', True):
            reason = risk_result['data'].get('rejection_reason', 'Unknown')
            alerts.append({
                'level': 'WARNING',
                'message': f'Trade rejected by risk manager: {reason}',
                'timestamp': datetime.utcnow().isoformat()
            })
        
        # Check market analysis
        analysis_result = event.get('market_analysis', {})
        if analysis_result.get('data', {}).get('downtrend_detected', False):
            alerts.append({
                'level': 'WARNING',
                'message': 'Downtrend detected - trading paused for safety',
                'timestamp': datetime.utcnow().isoformat()
            })
        
        return alerts
    
    def get_performance_report(self, executor_agent) -> Dict[str, Any]:
        """
        Generate performance report from executor agent.
        
        Args:
            executor_agent: ExecutionAgent instance
            
        Returns:
            Performance summary
        """
        summary = executor_agent.get_performance_summary()
        
        report = {
            'timestamp': datetime.utcnow().isoformat(),
            'trading_statistics': summary,
            'alerts_generated': len(self.alerts),
            'events_logged': self.events_count,
            'recent_alerts': self.alerts[-10:] if self.alerts else []
        }
        
        return report
    
    def export_event_log(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Export events from log file.
        
        Args:
            limit: Maximum number of recent events to return
            
        Returns:
            List of events
        """
        events = []
        
        try:
            with open(self.events_log, 'r') as f:
                for line in f:
                    try:
                        event = json.loads(line)
                        events.append(event)
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            pass
        
        # Return most recent events up to limit
        if limit:
            return events[-limit:]
        return events
    
    def get_alerts(self, level: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get alerts, optionally filtered by level.
        
        Args:
            level: Optional level filter (CRITICAL, WARNING, INFO)
            
        Returns:
            List of alerts
        """
        if level:
            return [a for a in self.alerts if a.get('level') == level]
        return self.alerts.copy()
    
    def clear_alerts(self) -> None:
        """Clear all alerts."""
        self.alerts.clear()
        self.logger.info("Alerts cleared")
