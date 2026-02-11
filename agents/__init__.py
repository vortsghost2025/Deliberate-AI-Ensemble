# Multi-agent trading bot system
# This package contains all specialized agents coordinated by the orchestrator

from .orchestrator import OrchestratorAgent
from .data_fetcher import DataFetchingAgent
from .market_analyzer import MarketAnalysisAgent
from .risk_manager import RiskManagementAgent
from .backtester import BacktestingAgent
from .executor import ExecutionAgent
from .monitor import MonitoringAgent
from .auditor import AuditorAgent

__all__ = [
    'OrchestratorAgent',
    'DataFetchingAgent',
    'MarketAnalysisAgent',
    'RiskManagementAgent',
    'BacktestingAgent',
    'ExecutionAgent',
    'MonitoringAgent',
    'AuditorAgent',
]
