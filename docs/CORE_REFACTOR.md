# Core Framework Refactor — Scope & Guardrails

## Purpose

This refactor exists to make the backend read as a **generic Document Intake & Triage Framework**.

The goal is not to add features, improve UX, or optimize performance.
The goal is to make **intent, boundaries, and responsibilities unambiguous**.

This is a structural refactor.

---

## Scope (Frozen)

### In scope

* Core framework domain models
* Deterministic triage logic
* Clear separation between:
  * core logic
  * persistence
  * read models
  * API boundary
* Folder and module restructuring when justified by architecture
* Naming cleanup to remove domain leakage

### Explicitly out of scope

* New features
* OCR
* Feedback loops
* Model retraining
* Async pipelines
* Auth / permissions
* UI write actions
* External integrations
* Performance optimizations
* Schema migrations not required by core alignment

---

## Refactor Principles

* Core logic must be framework-level, not product-level
* Domain intent must not leak into core modules
* APIs are thin adapters, not decision makers
* Repositories map data, they do not decide meaning
* Triage logic is deterministic and centralized
* Read models consume triage outputs, never recompute them

---

## Success Criteria

The refactor is successful if:

* The `core/` directory can be read independently to understand the system
* Another senior engineer can explain the system by reading core modules only
* Domain-specific extensions are obvious and isolated
* The framework could be open-sourced without redaction

---

## Non-Goals

This refactor does not aim to:

* Make the system production-ready
* Generalize for all industries
* Optimize ML performance
* Improve UI/UX
* Add configurability or policy engines

---

## Change Discipline

* No behavior changes unless required by clarified contracts
* Commits must be semantic and reviewable
* Squash merge only
* Refactor proceeds in declared phases, in order
