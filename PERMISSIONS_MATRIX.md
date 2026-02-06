# PERMISSIONS MATRIX

## 1. Purpose
Define exactly what each component is allowed to do — and not allowed to do.

## 2. Permission Levels
- FULL: unrestricted within role
- LIMITED: restricted to specific actions
- NONE: forbidden

## 3. Component Permissions

| Component              | Read Data | Write Data | Call API | Generate Signals | Execute Trades | Access Secrets |
|------------------------|-----------|------------|----------|------------------|----------------|----------------|
| Orchestrator           | FULL      | FULL       | NONE     | NONE             | NONE           | LIMITED        |
| DataFetcher            | NONE      | NONE       | FULL     | NONE             | NONE           | FULL           |
| MarketAnalysisAgent    | FULL      | NONE       | NONE     | FULL             | NONE           | NONE           |
| BacktestingAgent       | FULL      | NONE       | NONE     | LIMITED          | NONE           | NONE           |
| RiskManagementAgent    | FULL      | NONE       | NONE     | LIMITED          | NONE           | NONE           |
| ExecutionAgent         | LIMITED   | NONE       | LIMITED  | NONE             | FULL           | LIMITED        |
| LoggingAgent           | FULL      | FULL       | NONE     | NONE             | NONE           | NONE           |

## 4. Forbidden Actions
- Agent → Agent communication
- Agents modifying orchestrator state
- Agents accessing secrets they do not own
- Orchestrator calling external APIs

## 5. Philosophy
Permissions define the system’s blast radius — smaller is safer.