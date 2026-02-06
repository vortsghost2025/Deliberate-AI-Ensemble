"""Targeted paper-mode tests for gating behavior.
Injects data-fetch failure and risk rejection; verifies execution is blocked.
"""

from typing import Dict, Any

from agents.orchestrator import OrchestratorAgent


class InjectedOrchestrator(OrchestratorAgent):
    def __init__(self, *args, injected: Dict[str, Dict[str, Any]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.injected = injected or {}
        self.called_agents = []

    def _execute_agent_phase(self, agent_name: str, action: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.called_agents.append(agent_name)
        key = f"{agent_name}.{action}"
        if key in self.injected:
            return self.injected[key]
        return super()._execute_agent_phase(agent_name, action, input_data)


def print_result(label: str, passed: bool, detail: str = "") -> None:
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {label}{(' - ' + detail) if detail else ''}")


def test_data_fetch_failure() -> bool:
    injected = {
        "DataFetchingAgent.fetch_data": {
            "success": False,
            "error": "Injected data fetch failure",
            "data": {}
        }
    }

    orch = InjectedOrchestrator({"paper_trading": True}, injected=injected)
    result = orch.execute(["BTC/USDT"])

    execution_called = "ExecutionAgent" in orch.called_agents
    blocked = not execution_called and not result.get("success", True)

    print_result("Data fetch failure blocks execution", blocked)
    print_result("Execution not called", not execution_called)
    return blocked and not execution_called


def test_risk_rejection_blocks_execution() -> bool:
    injected = {
        "DataFetchingAgent.fetch_data": {
            "success": True,
            "data": {
                "market_data": {"BTC/USDT": {"current_price": 100.0}}
            }
        },
        "MarketAnalysisAgent.analyze_market": {
            "success": True,
            "data": {
                "analysis": {"BTC/USDT": {"signal_strength": 0.1}},
                "regime": "sideways"
            }
        },
        "BacktestingAgent.backtest_signals": {
            "success": True,
            "data": {
                "backtest_results": {"BTC/USDT": {"win_rate": 0.4}}
            }
        },
        "RiskManagementAgent.assess_and_size_position": {
            "success": True,
            "data": {
                "position_approved": False,
                "rejection_reason": "Signal strength too low",
                "assessments": {
                    "BTC/USDT": {
                        "position_approved": False,
                        "rejection_reason": "Signal strength too low",
                        "position_size": 0,
                        "current_price": 100.0,
                        "risk_amount": 0,
                        "stop_loss": 0,
                        "take_profit": 0
                    }
                }
            }
        }
    }

    orch = InjectedOrchestrator({"paper_trading": True}, injected=injected)
    result = orch.execute(["BTC/USDT"])

    execution_called = "ExecutionAgent" in orch.called_agents
    blocked = not execution_called and result.get("success", True) and result.get("data", {}).get("trade_executed") is False

    print_result("Risk rejection blocks execution", blocked)
    print_result("Execution not called", not execution_called)
    return blocked and not execution_called


def main() -> int:
    print("Targeted paper-mode gating tests")
    print("=================================")

    pass_a = test_data_fetch_failure()
    pass_b = test_risk_rejection_blocks_execution()

    all_passed = pass_a and pass_b
    print("=================================")
    print_result("Overall", all_passed)
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
