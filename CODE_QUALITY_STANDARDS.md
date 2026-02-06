# CODE QUALITY STANDARDS

## 1. Purpose
Define expectations for readability, structure, and maintainability so the system remains understandable and safe to evolve.

## 2. General Principles
- Prefer clarity over cleverness.
- Keep functions small and single‑purpose.
- Make control flow explicit.
- Avoid hidden side effects.

## 3. Naming Conventions
- Use descriptive, intention‑revealing names.
- Use `snake_case` for variables and functions.
- Use `PascalCase` for classes.
- Avoid abbreviations unless widely understood.

## 4. File and Module Structure
- One main responsibility per module.
- Group related logic together.
- Keep orchestration, agents, and utilities separated.
- Avoid circular dependencies.

## 5. Commenting and Documentation
- Comment *why*, not *what*.
- Document public functions and classes.
- Keep README and specs in sync with behavior.
- Update docs when behavior changes.

## 6. Error Handling and Safety
- Never swallow exceptions silently.
- Use structured error handling.
- Respect safety invariants in all code paths.
- Prefer explicit checks over assumptions.

## 7. Style Consistency
- Follow a consistent formatting style.
- Use a linter/formatter where possible.
- Keep imports organized and minimal.