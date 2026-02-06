# System Architecture

This document defines the complete architecture, behavior, safety model, and lifecycle of the system.  
It serves as the single source of truth for how the system is designed to operate.

---

## 1. Overview
The system is designed as a safety‑first, state‑driven architecture for running agent‑based decision and execution cycles. Its purpose is to ensure that every action taken by the system is predictable, observable, recoverable, and governed by strict safety rules.

The system operates in two modes—paper and live—and uses a controlled state machine to prevent unsafe transitions. Every component is designed to be modular, explainable, and replaceable without breaking the whole.

The core philosophy is simple: the system must protect the user, protect itself, and behave consistently under all conditions. Nothing important should live only in the operator’s head; everything must be explicit, logged, and governed.

---

## 2. Core Principles
The system is built on the following foundational principles:

- Safety first: no action is allowed if it cannot be validated.
- Predictability: behavior must be consistent across all environments.
- Observability: every meaningful event must be logged and explainable.
- Recoverability: the system must be able to halt and restart safely.
- Transparency: decisions and state transitions must be visible and traceable.
- Modularity: components must be replaceable without breaking the system.
- Governance: rules, invariants, and lifecycle stages must be enforced.
- Resilience: the system must withstand instability without becoming unstable.

---

## 3. Layered Architecture

### 3.1 Execution & Orchestration Layers

The execution layer defines how the system performs a full decision cycle, while the orchestration layer governs the order, safety checks, and validation steps that wrap each cycle.

The orchestrator is responsible for:
- validating configuration
- validating environment readiness
- validating data freshness
- coordinating agent execution in the correct order
- enforcing safety invariants at each step
- managing state transitions
- halting safely on any violation or uncertainty

The execution cycle consists of:
1. Load and validate configuration  
2. Load and validate system state  
3. Fetch and validate market data  
4. Run decision agent(s)  
5. Validate outputs  
6. If in live mode: run execution agent  
7. Log all actions, decisions, and transitions  
8. Return to idle or next scheduled cycle

TODO: Add deeper detail from architecture sections 1–15.
The execution and orchestration layers draw directly from the foundational principles defined in Sections 1–15.  
These deeper details ensure that every cycle is predictable, explainable, and aligned with the system’s core philosophy.

### Architectural Foundations Integrated Here

- **Determinism (Section 1–2)**  
  Every step in the cycle must produce the same result given the same inputs.  
  No randomness, no hidden state, no implicit behavior.

- **Separation of Concerns (Sections 3–5)**  
  Orchestration controls *order and safety*.  
  Execution controls *actions and computation*.  
  Neither layer may leak responsibilities into the other.

- **Safety-First Design (Sections 6–10)**  
  Every stage of the cycle is wrapped in validation.  
  Any uncertainty triggers a safe halt.  
  No step proceeds without explicit confirmation of readiness.

- **Explainability (Sections 11–13)**  
  Each decision must be reconstructable from logs.  
  The orchestrator ensures that every action is paired with context and reasoning.

- **State Integrity (Sections 14–15)**  
  The orchestrator is responsible for ensuring that the system’s state is always valid, consistent, and aligned with the state machine.

### Deepened Execution Cycle Logic

1. **Load and validate configuration**  
   - Must match schema  
   - Must pass integrity checks  
   - Must be version‑compatible with the running system  

2. **Load and validate system state**  
   - Must match expected state machine position  
   - Must not contain unresolved errors  
   - Must be internally consistent  

3. **Fetch and validate market data**  
   - Must be fresh  
   - Must pass integrity checks  
   - Must match expected format and completeness  

4. **Run decision agent(s)**  
   - Must receive validated inputs only  
   - Must produce deterministic, explainable outputs  
   - Must not violate safety invariants  

5. **Validate outputs**  
   - Check for completeness  
   - Check for safety compliance  
   - Check for internal contradictions  

6. **If in live mode: run execution agent**  
   - Must confirm live authorization  
   - Must validate order parameters  
   - Must enforce risk limits  

7. **Log all actions, decisions, and transitions**  
   - Must include timestamps  
   - Must include reasoning summaries  
   - Must include validation metadata  

8. **Return to idle or next scheduled cycle**  
   - Must confirm system state is stable  
   - Must confirm no pending errors  
   - Must prepare for next cycle cleanly  

This expanded detail ensures that the execution and orchestration layers are fully aligned with the architectural principles defined earlier in the document.

---

### 3.2 Safety & Risk Layers

The safety and risk layer defines the non‑negotiable rules that govern system behavior.  
Its purpose is to ensure that no action, transition, or decision can occur without passing explicit validation.

This layer enforces:

- **Safety invariants**: rules that must always hold true, regardless of mode or state.
- **Risk management boundaries**: constraints that prevent unsafe exposure or behavior.
- **Validation rules**: checks applied before every state transition, decision, or execution step.
- **Forbidden behaviors**: actions the system must never take under any circumstances.
- **Safety governance**: the mechanisms that ensure safety rules cannot be bypassed or ignored.

The safety layer acts as the system’s immune system — it halts execution immediately when uncertainty, invalid data, or inconsistent state is detected.

> TODO: Insert detailed content from sections 16–22 and 29.
The safety and risk layers enforce the system’s non‑negotiable boundaries.  
They ensure that every action, decision, and state transition is compliant with the system’s safety invariants and risk constraints.

### Architectural Foundations Integrated Here

- **Safety Invariants (Sections 6–10)**  
  These define the hard boundaries the system must never cross.  
  Any violation triggers an immediate safe halt.

- **Risk Constraints (Sections 11–13)**  
  These govern exposure, position sizing, and acceptable operational limits.  
  They ensure that even valid decisions remain within controlled risk parameters.

- **Validation Discipline (Sections 14–15)**  
  Every input, output, and intermediate step must be validated.  
  No component may operate on unverified data.

### Core Responsibilities of the Safety & Risk Layers

- Validate configuration before execution  
- Validate environment readiness  
- Validate market data integrity  
- Validate decision agent outputs  
- Validate execution agent parameters  
- Enforce risk limits at every stage  
- Enforce safety invariants continuously  
- Trigger safe halts on any uncertainty or violation  

### Safety Enforcement Logic

1. **Pre‑Cycle Validation**  
   - Configuration schema checks  
   - Environment readiness checks  
   - Data freshness and integrity checks  

2. **Decision Validation**  
   - Ensure outputs are complete  
   - Ensure outputs comply with invariants  
   - Ensure outputs comply with risk limits  

3. **Execution Validation (Live Mode Only)**  
   - Validate order parameters  
   - Validate position sizing  
   - Validate exposure limits  

4. **Continuous Monitoring**  
   - Detect anomalies  
   - Detect stale data  
   - Detect inconsistent state  
   - Detect invariant violations  

5. **Safe Halt Protocol**  
   - Immediately stop execution  
   - Log full context  
   - Transition to ERROR state  
   - Require operator intervention  

This expanded detail ensures that the safety and risk layers are fully aligned with the system’s invariants, risk philosophy, and validation discipline.

---

### 3.3 Observability & Logging Layers

The observability layer ensures that every meaningful action, decision, and state transition is visible, traceable, and auditable.  
Its purpose is to make the system explainable and diagnosable at all times, especially during failures or unexpected behavior.

This layer defines:

- **Logging requirements**: what must be logged, at what granularity, and in which format.
- **Auditability**: the ability to reconstruct decisions, state transitions, and execution paths from logs alone.
- **Metrics**: quantitative signals that reflect system health, performance, and stability.
- **State transition visibility**: clear records of when and why the system enters or exits each state.
- **Error transparency**: all errors must be logged with enough context to diagnose root causes without guesswork.

Observability is what allows the operator to trust the system.  
If something cannot be observed, it cannot be validated — and therefore cannot be considered safe.

> TODO: Insert content from logging, audit, and observability sections.
The observability and logging layers ensure that every action, decision, and state transition is transparent, traceable, and reconstructable.  
They provide the visibility required for debugging, auditing, safety verification, and long‑term system evolution.

### Architectural Foundations Integrated Here

- **Explainability (Sections 11–13)**  
  Every decision must be understandable after the fact.  
  Logs must contain enough context to reconstruct the full reasoning chain.

- **State Integrity (Sections 14–15)**  
  Observability ensures that the system’s internal state always matches expectations.  
  Any deviation becomes immediately visible.

- **Safety & Risk Enforcement (Sections 16–22)**  
  Observability is how the system proves that safety invariants and risk limits were respected at every step.

### Core Responsibilities of the Observability & Logging Layers

- Capture all inputs, outputs, and intermediate steps  
- Record validation results at each stage  
- Log state transitions with timestamps  
- Log decision agent reasoning summaries  
- Log execution agent actions (live mode only)  
- Record safety checks and invariant evaluations  
- Provide structured logs for audit and debugging  
- Ensure logs are immutable and tamper‑evident  

### Observability Logic

1. **Input Logging**  
   - Configuration snapshot  
   - System state snapshot  
   - Market data snapshot  
   - Validation metadata  

2. **Decision Logging**  
   - Decision agent inputs  
   - Decision agent outputs  
   - Confidence scores  
   - Reasoning summaries  
   - Risk assessments  

3. **Execution Logging (Live Mode Only)**  
   - Order parameters  
   - Exchange responses  
   - Execution confirmations  
   - Error or rejection details  

4. **State Transition Logging**  
   - Previous state  
   - Triggering event  
   - New state  
   - Timestamp  
   - Any warnings or anomalies  

5. **Safety & Invariant Logging**  
   - Invariant evaluation results  
   - Risk limit evaluations  
   - Any violations detected  
   - Safe halt triggers  

### Observability Guarantees

- Every cycle is fully reconstructable  
- Every decision is explainable  
- Every invariant evaluation is recorded  
- Every state transition is traceable  
- Every anomaly is visible  
- Nothing happens silently  

This expanded detail ensures that the observability and logging layers provide the transparency, auditability, and explainability required for safe long‑term operation.

---

### 3.4 Lifecycle & Governance Layers

The lifecycle and governance layer defines how the system evolves, how it is deployed, and how it is safely maintained over time.  
Its purpose is to ensure that the system remains stable, auditable, and aligned with its safety principles throughout its entire lifespan.

This layer includes:

- **System lifecycle stages**: initialization, configuration, validation, execution, maintenance, and shutdown.
- **Deployment rules**: requirements for promoting changes from development to paper mode to live mode.
- **Rollback requirements**: the ability to revert to a known‑good state if instability or unexpected behavior occurs.
- **Incident handling**: structured procedures for detecting, responding to, and recovering from failures or anomalies.
- **Decommissioning**: rules for safely retiring components, configurations, or entire system versions.

Governance ensures that changes cannot be made impulsively or unsafely.  
Every modification must be intentional, validated, and reversible.

> TODO: Insert content from sections 23–28 and 32–33.
The lifecycle and governance layers define how the system evolves, how changes are introduced safely, and how operational discipline is maintained over time.  
They ensure that the system remains stable, auditable, and aligned with its architectural principles throughout its entire lifespan.

### Architectural Foundations Integrated Here

- **Versioning Discipline (Sections 23–24)**  
  Every configuration, component, and artifact must be versioned.  
  No unversioned or ad‑hoc changes are allowed.

- **Change Management (Sections 25–26)**  
  All modifications must follow a structured review and validation process.  
  No change enters the system without explicit approval and testing.

- **Governance Principles (Sections 27–28)**  
  The system must remain aligned with its core philosophy.  
  Governance ensures that shortcuts, drift, and silent regressions never accumulate.

- **Long‑Term Evolution (Sections 32–33)**  
  The architecture must support safe iteration, modular upgrades, and future expansion without breaking invariants.

### Core Responsibilities of the Lifecycle & Governance Layers

- Manage configuration lifecycle  
- Manage component lifecycle  
- Enforce versioning rules  
- Enforce change‑review processes  
- Validate upgrades before activation  
- Maintain audit trails for all changes  
- Ensure backward compatibility where required  
- Prevent architectural drift  

### Lifecycle Logic

1. **Configuration Lifecycle**  
   - Version every configuration file  
   - Validate schema compatibility  
   - Validate safety and risk alignment  
   - Log activation and deactivation events  

2. **Component Lifecycle**  
   - Version every module and agent  
   - Validate compatibility before deployment  
   - Run integration tests before activation  
   - Log component transitions  

3. **Change Governance**  
   - Require explicit approval for changes  
   - Require validation and testing  
   - Require audit logging  
   - Reject changes that violate invariants  

4. **Upgrade Path Management**  
   - Support rolling upgrades  
   - Support safe rollback  
   - Validate state compatibility  
   - Prevent partial or inconsistent upgrades  

5. **Drift Prevention**  
   - Detect configuration drift  
   - Detect behavioral drift  
   - Detect architectural violations  
   - Trigger alerts or safe halts when drift is detected  

### Governance Guarantees

- No silent changes  
- No unreviewed modifications  
- No unversioned artifacts  
- No regressions that bypass safety  
- No architectural drift over time  

This expanded detail ensures that the lifecycle and governance layers maintain long‑term stability, auditability, and architectural integrity.

---

### 3.5 Future‑Proofing & Capstone

The future‑proofing layer ensures that the system can evolve safely over time without breaking existing behavior or compromising safety.  
Its purpose is to maintain long‑term stability while allowing controlled, intentional growth.

This layer includes:

- **Modularity**: components must be isolated, replaceable, and independently testable.
- **Versioning**: changes must be tracked, documented, and tied to explicit version increments.
- **Extensibility**: new capabilities must integrate without altering core safety or orchestration logic.
- **Evolution rules**: the system may only evolve through validated, reversible, and governed processes.
- **System identity and philosophy**: the principles that define how the system should behave, even as it grows.

Future‑proofing ensures that the system does not degrade, drift, or become unsafe as it expands.  
It preserves the integrity of the architecture across all future iterations.

> TODO: Insert content from sections 30–31 and 34.
The future‑proofing and capstone layer ensures that the system remains stable, adaptable, and philosophically consistent as it evolves.  
It protects the architecture from drift, degradation, and unintentional complexity over time.

### Architectural Foundations Integrated Here

- **System Identity & Philosophy (Sections 30–31)**  
  The system must always behave according to its core principles.  
  Future changes must reinforce, not dilute, the system’s identity.

- **Long‑Term Evolution & Expansion (Section 34)**  
  The architecture must support new modules, new agents, and new capabilities  
  without breaking invariants or introducing instability.

### Core Responsibilities of the Future‑Proofing Layer

- Preserve architectural clarity as the system grows  
- Maintain strict boundaries between layers  
- Ensure new features integrate cleanly  
- Prevent accidental complexity  
- Prevent philosophical drift  
- Maintain long‑term maintainability  
- Support modular upgrades and extensions  
- Ensure backward compatibility where required  

### Future‑Proofing Logic

1. **Architectural Integrity Checks**  
   - Validate that new components respect existing boundaries  
   - Ensure no layer leaks responsibilities  
   - Detect and reject anti‑patterns  

2. **Compatibility & Evolution**  
   - Validate compatibility with existing modules  
   - Support versioned upgrades  
   - Support safe rollback paths  
   - Maintain stable public interfaces  

3. **Philosophical Consistency**  
   - Ensure new behavior aligns with system identity  
   - Reject changes that violate core principles  
   - Maintain determinism, safety, and explainability  

4. **Modular Expansion**  
   - Allow new agents to be added without rewriting core logic  
   - Allow new data sources to be integrated safely  
   - Allow new execution modes to be introduced cleanly  

5. **Long‑Term Stability**  
   - Detect architectural drift  
   - Detect behavioral drift  
   - Detect configuration drift  
   - Trigger alerts or safe halts when drift is detected  

### Capstone Guarantees

- The system remains stable as it grows  
- The architecture remains clean and understandable  
- The philosophy remains intact  
- The system can evolve without breaking itself  
- Future changes reinforce the design instead of eroding it  

This expanded detail ensures that the future‑proofing and capstone layer protects the system’s identity, stability, and long‑term evolution.

---

## 4. State Machine

The system operates using a strict, explicitly defined state machine.  
Each state represents a controlled phase of operation, and transitions are only allowed when all safety checks pass.

### States

- **Uninitialized**  
  The system has not yet loaded configuration or environment details.

- **Initialized**  
  Configuration is loaded and validated, but the system is not yet ready to run.

- **Ready**  
  All prerequisites are satisfied; the system can begin a decision cycle.

- **Running**  
  The system is actively performing a decision cycle (paper or live).

- **Paused**  
  Execution is temporarily halted but can resume without reinitialization.

- **Error**  
  A violation, inconsistency, or unexpected condition has occurred; the system must halt safely.

- **Shutdown**  
  The system is intentionally stopped and cannot resume without full reinitialization.

### Allowed Transitions

- Uninitialized → Initialized  
- Initialized → Ready  
- Ready → Running  
- Running → Ready  
- Running → Paused  
- Paused → Ready  
- Any state → Error  
- Any state → Shutdown

### Forbidden Transitions

- Running → Initialized  
- Running → Uninitialized  
- Error → Running  
- Shutdown → Any state  
- Any transition that bypasses validation or safety checks

### Entry/Exit Conditions

Each state has explicit requirements:

- **Entering Ready** requires validated configuration, validated environment, and validated data sources.  
- **Entering Running** requires passing all safety invariants and confirming mode (paper or live).  
- **Entering Error** requires immediate halt, logging, and preservation of diagnostic context.  
- **Entering Shutdown** requires safe termination of all active processes.

### Safety Checks at Each Boundary

Before any transition, the system must verify:

- configuration integrity  
- environment readiness  
- data freshness  
- agent output validity  
- invariant compliance  
- absence of unresolved errors  

If any check fails, the system transitions to **Error** immediately.

> TODO: Expand with diagrams and deeper transition logic after consolidation.
The future‑proofing and capstone layer ensures that the system remains stable, adaptable, and philosophically consistent as it evolves.  
It protects the architecture from drift, degradation, and unintentional complexity over time.

### Architectural Foundations Integrated Here

- **System Identity & Philosophy (Sections 30–31)**  
  The system must always behave according to its core principles.  
  Future changes must reinforce, not dilute, the system’s identity.

- **Long‑Term Evolution & Expansion (Section 34)**  
  The architecture must support new modules, new agents, and new capabilities  
  without breaking invariants or introducing instability.

### Core Responsibilities of the Future‑Proofing Layer

- Preserve architectural clarity as the system grows  
- Maintain strict boundaries between layers  
- Ensure new features integrate cleanly  
- Prevent accidental complexity  
- Prevent philosophical drift  
- Maintain long‑term maintainability  
- Support modular upgrades and extensions  
- Ensure backward compatibility where required  

### Future‑Proofing Logic

1. **Architectural Integrity Checks**  
   - Validate that new components respect existing boundaries  
   - Ensure no layer leaks responsibilities  
   - Detect and reject anti‑patterns  

2. **Compatibility & Evolution**  
   - Validate compatibility with existing modules  
   - Support versioned upgrades  
   - Support safe rollback paths  
   - Maintain stable public interfaces  

3. **Philosophical Consistency**  
   - Ensure new behavior aligns with system identity  
   - Reject changes that violate core principles  
   - Maintain determinism, safety, and explainability  

4. **Modular Expansion**  
   - Allow new agents to be added without rewriting core logic  
   - Allow new data sources to be integrated safely  
   - Allow new execution modes to be introduced cleanly  

5. **Long‑Term Stability**  
   - Detect architectural drift  
   - Detect behavioral drift  
   - Detect configuration drift  
   - Trigger alerts or safe halts when drift is detected  

### Capstone Guarantees

- The system remains stable as it grows  
- The architecture remains clean and understandable  
- The philosophy remains intact  
- The system can evolve without breaking itself  
- Future changes reinforce the design instead of eroding it  

This expanded detail ensures that the future‑proofing and capstone layer protects the system’s identity, stability, and long‑term evolution.

---

## 5. Safety Invariants

Safety invariants are the non‑negotiable rules the system must enforce at all times.  
They cannot be bypassed, overridden, or ignored — even by configuration, operator input, or agent logic.

These invariants define the boundaries of safe operation:

1. **No action may occur without validated configuration.**  
   If configuration is missing, invalid, or inconsistent, the system must halt.

2. **No decision may be made using stale or unverified data.**  
   Data freshness and integrity must be confirmed before every cycle.

3. **No state transition may occur without passing all safety checks.**  
   Any failed check forces an immediate transition to the Error state.

4. **Live mode execution requires explicit, validated authorization.**  
   The system must never enter live mode implicitly or accidentally.

5. **Agent outputs must be validated before execution.**  
   Invalid, incomplete, or unsafe outputs must be rejected.

6. **The system must halt on uncertainty.**  
   Ambiguous state, inconsistent data, or unexpected behavior triggers an immediate stop.

7. **All actions must be logged.**  
   If an action cannot be logged, it cannot be performed.

8. **The system must remain deterministic.**  
   The same inputs must always produce the same outputs.

These invariants form the foundation of the system’s safety model.  
Every component, agent, and process must comply with them at all times.

> TODO: Expand with formal invariant definitions after consolidation.

---

## 6. Open Questions / TODOs

This section tracks items that require clarification, deeper analysis, or future refinement.  
It serves as a living backlog for architectural decisions, unresolved design questions, and areas that need expansion.

Current items include:

- Clarify final structure of the decision agent interface.
- Determine whether additional intermediate states are needed in the state machine.
- Validate which safety invariants require formal proofs.
- Expand logging schema for multi‑agent scenarios.
- Finalize rules for versioning and long‑term evolution.
- Integrate persistence and restoration logic after architecture consolidation.
- Review all TODO markers across sections and merge them into this list.

This list will grow and shrink as the architecture matures.  
It ensures that no loose ends are forgotten during consolidation.

> TODO: Add new items as they arise during implementation and review.