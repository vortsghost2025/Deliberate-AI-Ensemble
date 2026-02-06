# SYSTEM OVERVIEW NARRATIVE

## 1. Purpose
Provide a human‑readable, high‑level explanation of how the entire system works, written as a cohesive story rather than a technical spec.

## 2. The System at a Glance
The system is a disciplined, safety‑first trading architecture built around a central orchestrator and a set of specialized agents.  
Each agent performs one job.  
The orchestrator ensures they work together safely, predictably, and transparently.

## 3. The Workflow Story
A single workflow begins with the orchestrator waking up and checking its environment.  
If everything looks safe, it fetches fresh market data.  
That data is analyzed to determine the current market regime and generate signals.  
If the regime is safe, the system optionally backtests the signals to understand their historical behavior.  
Risk management then evaluates whether the signals are acceptable.  
Only if everything is safe does the system execute a paper trade.  
Finally, the entire workflow is logged in detail.

## 4. The Safety Philosophy
Safety is the foundation.  
Every decision is filtered through invariants, risk rules, and validation steps.  
If anything looks wrong, the system halts immediately and transparently.

## 5. The Agents as Characters
- **DataFetcher**: The scout bringing fresh information.  
- **MarketAnalysisAgent**: The strategist interpreting the environment.  
- **BacktestingAgent**: The historian checking past performance.  
- **RiskManagementAgent**: The guardian ensuring safety.  
- **ExecutionAgent**: The operator placing paper trades.  
- **LoggingAgent**: The archivist recording everything.

## 6. The Orchestrator as Conductor
The orchestrator coordinates all agents, enforces rules, and ensures the system always chooses the safest path.

## 7. The System’s Identity
The architecture is modular, predictable, and transparent — designed to evolve without losing its core philosophy.