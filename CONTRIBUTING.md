# Contributing to Decision Plane

Thank you for your interest in contributing to **Decision Plane**.

Decision Plane is a **decision infrastructure framework** focused on **determinism, auditability, and inspection** of machine-learning–driven decision systems.

Contributions are welcome **only** when they preserve the architectural intent and explicit scope of the project.

This document defines:

* how to contribute
* what is in scope
* what is explicitly out of scope
* how contributions are evaluated

---

## Guiding Philosophy

Decision Plane is built around a small set of **non-negotiable principles**:

* Determinism over cleverness
* Auditability over automation
* Explicit state over implicit behavior
* Read models over side effects
* Inspection over execution

A contribution that weakens any of these properties will be rejected, **even if it is technically correct or well implemented**.

This is a design-constrained project by intent.

---

## What You Can Contribute

### 1. Architecture-Aligned Capabilities

Contributions are welcome in the following areas:

* Ingestion boundaries and validation
* Deterministic processing pipelines
* Processing lineage and audit trails
* Read-only replay mechanisms
* Inspection-oriented APIs
* Dashboard and aggregation read models
* Contract definitions and API versioning
* Test coverage for system guarantees
* Documentation and architectural clarification

All contributions must be:

* deterministic
* inspectable
* auditable
* side-effect controlled

---

### 2. Read Models and Inspection Views

You may contribute:

* New read models (e.g. timelines, summaries, aggregations)
* Derived inspection views over existing state
* Additional inspection endpoints

Read models **must**:

* Never mutate authoritative state
* Be reconstructible from persisted data
* Remain optional and replaceable
* Preserve historical truth

Read models exist to **explain what happened**, not to influence execution.

---

### 3. Tests and System Guarantees

Tests are **first-class contributions**.

High-quality contributions include:

* Contract tests
* Read-model tests
* Determinism guarantees
* Replay invariants
* Regression tests

If behavior exists, it must be testable.
If behavior is intentionally unimplemented, that absence must be tested explicitly.

---

### 4. Documentation

Documentation contributions are strongly encouraged, including:

* Architectural clarification
* System guarantees
* Design rationale
* Non-goals and scope boundaries
* Contribution rules

Documentation should prioritize **why** the system behaves the way it does, not just **what** it does.

---

## What You Must NOT Contribute

The following are **explicitly out of scope** and will not be accepted:

* Policy enforcement or action execution
* Automated decision-making logic
* Agent systems or autonomous workflows
* Online or real-time inference guarantees
* Model training or retraining pipelines
* Self-modifying or adaptive systems
* Business-specific rules or thresholds
* Cost optimization tied to business outcomes
* Organizational workflow logic
* Proprietary datasets or trained models

If your contribution answers:

> “What should the system do?”

instead of:

> “What happened and why?”

it does **not** belong in Decision Plane.

---

## Contribution Standards

### Code Style and Structure

* Prefer clarity over abstraction
* Avoid hidden side effects
* Favor explicit data flows
* Keep functions small and inspectable
* Avoid global mutable state
* Prefer boring, readable code

This is an inspection system, not a performance contest.

---

### API Contracts

* All APIs must be versioned
* Breaking changes require a version bump
* Contracts must be tested
* Stub endpoints returning `404` are acceptable when behavior is intentionally unavailable in v1

APIs are **product contracts**, not internal plumbing.

---

### Determinism Requirements

Any contribution that introduces:

* randomness
* time-dependent behavior
* external side effects

must do so **explicitly**, **deterministically**, and **with test coverage**.

Implicit nondeterminism is not allowed.

---

## Commit and Pull Request Guidelines

### Commit Messages

Use explicit, conventional commit prefixes:

* `feat:` new architecture-aligned capability
* `fix:` bug fix or correctness issue
* `chore:` refactors, cleanup, tooling
* `docs:` documentation changes
* `test:` test additions or fixes

Example:

```
feat: add read-only processing lineage timeline
```

---

### Pull Requests

Each pull request must:

* Address a single, coherent concern
* Include tests when behavior changes
* Avoid mixing unrelated changes
* Explain **why** the change is needed
* Reference relevant architectural principles

PRs are typically merged using **squash merge** to preserve a clean history.

---

## Review Criteria

All contributions are evaluated against:

1. Architectural alignment
2. Determinism guarantees
3. Auditability and lineage preservation
4. Clarity and inspectability
5. Test coverage
6. Long-term maintainability

Performance, novelty, or cleverness are **not** primary acceptance criteria.

---

## When in Doubt

If you are unsure whether a contribution fits the project:

* Open an issue first
* Describe the problem, not just the solution
* Explain how the change aligns with the architecture

Discussion before implementation is encouraged and preferred.

---

## Final Note

Decision Plane is intentionally constrained.

Those constraints are what make it useful as a reference architecture.

If a contribution preserves those constraints, it is welcome.
If it violates them, it belongs in a different project.
