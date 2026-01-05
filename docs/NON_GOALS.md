# Non-Goals — Decision Plane

## Purpose

This document defines what **Decision Plane explicitly does NOT attempt to do**.

These exclusions are **architectural constraints**, not missing features.

They exist to preserve determinism, auditability, and inspection-first design.

If a proposed change violates a non-goal defined here, it is rejected by definition.

---

## Core Philosophy

Decision Plane is a **decision inspection framework**, not a decision execution system.

Non-goals are **intentional boundaries** that protect correctness and trust.

---

## Explicit Non-Goals

The following are **out of scope by design** and will not be added.

---

### 1. Autonomous Decision Execution

Not included:

* automatic approvals or rejections
* policy enforcement
* side effects beyond state recording

Decision Plane produces **signals**, not actions.

---

### 2. Real-Time or Online Inference

Not included:

* synchronous inference APIs
* latency SLAs
* streaming pipelines

The system is **batch-first and replayable**.

---

### 3. Model Training or Orchestration

Not included:

* training pipelines
* hyperparameter tuning
* automated model registry workflows

Models are assumed to exist **outside** the system.

---

### 4. Automated Retraining or Self-Modification

Not included:

* auto-retraining
* adaptive thresholds
* feedback loops that modify models

Self-modifying systems break auditability.

---

### 5. Embedded Business or Domain Logic

Not included:

* finance rules
* legal logic
* healthcare policies
* domain ontologies

Decision Plane is **domain-agnostic by design**.

---

### 6. UI-Driven Logic or Actions

Not included:

* UI-triggered actions
* client-side decision logic

The UI is strictly **read-only with respect to logic**.

---

### 7. Agent-Based or Goal-Driven Systems

Not included:

* agent loops
* planning systems
* autonomous goal pursuit

These violate determinism and explainability.

---

### 8. Performance Optimization as a Primary Objective

Not included:

* premature optimization
* execution tuning
* caching strategies as core concerns

Correctness and auditability take precedence.

---

## Permanent Guardrails

The following rules apply indefinitely:

* no feature without a persisted artifact
* no hidden state
* no implicit transitions
* no silent defaults

If a behavior cannot be audited, it does not belong.

---

## Permitted Extensions (Constraint-Bound)

The following types of extensions are acceptable **only if** they preserve all guarantees:

* additional deterministic processing steps
* richer inspection read models
* enhanced replay and comparison views
* external systems consuming emitted signals

Decision Plane **never** executes policy or action logic itself.

---

## Invariants

The following principles are permanent:

* determinism
* explicit lineage
* replayability
* read-model isolation
* signal-first design

Any proposal that violates these is invalid by definition.

---

## Final Positioning

Decision Plane is intentionally:

* conservative
* explicit
* auditable
* unopinionated

Its value is **trust**, not automation.

---

## Final Status

| File                       | Action               |
| -------------------------- | -------------------- |
| V1_NON_GOALS_AND_FUTURE.md | **REWRITE + RENAME** |
| New name                   | `NON_GOALS.md`       |
| Risk after change          | None                 |
