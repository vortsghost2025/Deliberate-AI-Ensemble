# ENGINEERING TENETS

## 1. Purpose
Define the non‑negotiable engineering beliefs that shape how the system is built, maintained, and evolved.

## 2. Tenet: Fail Safe, Not Fast
Speed is irrelevant if safety is compromised.  
The system must always choose the safest behavior.

## 3. Tenet: Explicit Is Better Than Implicit
All assumptions must be visible in code or documentation.  
Hidden behavior is a liability.

## 4. Tenet: Validate Everything
No agent output is trusted without validation.  
No external data is accepted without checks.

## 5. Tenet: No Silent Failures
Every error must be surfaced, logged, and acted upon.  
Silence is danger.

## 6. Tenet: Predictability Over Optimization
A predictable system is more valuable than a fast one.  
Optimization comes only after clarity and safety.

## 7. Tenet: Documentation Is Architecture
Specs, invariants, and diagrams are not optional.  
They are part of the system’s structure.

## 8. Tenet: Replaceability Is Strength
Any agent should be replaceable without rewriting the system.  
Boundaries protect stability.

## 9. Tenet: Safety Is a Feature, Not an Add‑On
Safety is built into every layer, not bolted on afterward.