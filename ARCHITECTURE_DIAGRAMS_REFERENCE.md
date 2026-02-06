# ARCHITECTURE DIAGRAMS REFERENCE

## 1. Purpose
Provide a central place to describe and reference all conceptual diagrams used to understand the system.

## 2. Diagram Types
### Workflow Diagram
Shows the full end‑to‑end workflow from INIT to COMPLETE.

### State Machine Diagram
Illustrates all valid states and transitions of the orchestrator.

### Agent Interaction Diagram
Shows how agents communicate with the orchestrator and never with each other.

### Data Flow Diagram
Shows how data moves from external APIs through agents and into logs.

### Safety Gate Diagram
Highlights all points where safety checks occur.

## 3. Diagram Descriptions
### Workflow Diagram Description
- Linear flow  
- Safety checks at each step  
- Clear halting conditions  

### State Machine Diagram Description
- Explicit states  
- Deterministic transitions  
- Error and halted states clearly separated  

### Agent Interaction Diagram Description
- Hub‑and‑spoke model  
- Orchestrator at center  
- No lateral communication  

### Data Flow Diagram Description
- DataFetcher → Analysis → Backtest → Risk → Execution → Logging  
- Validation at each step  

### Safety Gate Diagram Description
- Data validity  
- Regime safety  
- Risk veto  
- Execution safety  
- Logging integrity  

## 4. Diagram Philosophy
Diagrams make the system intuitive, teachable, and reviewable.