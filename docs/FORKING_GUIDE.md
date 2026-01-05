# FORKING GUIDE — Decision Plane

## Purpose of This Document

This guide explains **how Decision Plane is intended to be forked and extended** without violating its architectural guarantees.

Decision Plane is designed to be:

* forkable
* extensible
* domain-agnostic

—but only if its **core invariants remain intact**.

This document defines:

* what you may change
* what you must not change
* where domain logic belongs
* how to safely build products on top

---

## Mental Model: Core vs Product

Decision Plane is **infrastructure**, not a product.

Think of it as:

```
┌──────────────────────────┐
│      Product Layer       │  ← Fork here
├──────────────────────────┤
│   Adapters / Read Models │  ← Fork here
├──────────────────────────┤
│      Decision Plane      │  ← Do NOT modify
│        (Core)            │
└──────────────────────────┘
```

The core exists to **explain decisions**, not to execute them.

---

## What You Are Allowed to Change

### 1. Ingestion (Upstream)

You may:

* change how documents enter the system
* add new metadata fields
* integrate message queues or batch loaders
* validate additional schemas

Constraints:

* ingestion must remain deterministic
* raw inputs must remain immutable
* duplicate ingestion must be idempotent

---

### 2. Processing Steps

You may:

* add new processing steps (OCR, NLP, parsers, feature extractors)
* add new processor versions
* emit additional artifacts

Constraints:

* every step must be versioned
* every step must emit lineage
* no step may mutate raw input

---

### 3. Signals

You may:

* add new signal types
* emit richer uncertainty indicators
* surface domain-specific quality flags

Constraints:

* signals are informational only
* signals must not execute actions
* signals must be persisted explicitly

---

### 4. Read Models (Product Views)

You may:

* add dashboards
* add queues
* add summaries
* add timelines
* add comparisons

Constraints:

* read models are non-authoritative
* read models must be rebuildable
* read models must never mutate core state

---

### 5. Domain-Specific Products

You may build:

* Finance inspection systems
* Compliance review platforms
* Healthcare document triage
* Insurance claim inspection tools

These belong in:

* separate repositories
* or clearly isolated modules

Decision Plane remains unchanged.

---

## What You Must NOT Change

These are **hard architectural boundaries**.

### ❌ Do NOT add decision execution

Forbidden:

* auto-approval
* auto-rejection
* escalation triggers
* workflow execution

Reason:

* breaks auditability
* creates irreversible outcomes
* introduces governance risk

---

### ❌ Do NOT add hidden automation

Forbidden:

* agent loops
* background retries
* implicit behavior
* time-based side effects

Reason:

* destroys determinism
* obscures causality

---

### ❌ Do NOT embed domain logic in core

Forbidden:

* finance rules
* legal policies
* healthcare heuristics
* business KPIs

Reason:

* destroys reusability
* couples system to one domain

---

### ❌ Do NOT mutate historical data

Forbidden:

* overwriting runs
* updating past signals
* correcting history silently

Reason:

* breaks replayability
* invalidates audits

---

## Where Domain Logic Belongs

| Concern        | Location             |
| -------------- | -------------------- |
| Business rules | External systems     |
| Policies       | Policy engines       |
| Approvals      | Workflow tools       |
| Notifications  | Downstream consumers |
| Revenue logic  | Product layer        |

Decision Plane emits **facts**, not decisions.

---

## Extension Patterns (Recommended)

### Pattern 1 — Domain Adapter

Create adapters that:

* interpret signals
* translate outputs
* feed downstream systems

No write-back allowed.

---

### Pattern 2 — Vertical Fork

Fork the repo and:

* keep core untouched
* add domain-specific layers
* brand separately

Recommended for commercial products.

---

### Pattern 3 — Signal-Driven Integration

Use Decision Plane as:

* a truth source
* an audit log
* a replay engine

Let another system decide what to do.

---

## Contract Discipline

When extending:

* Public APIs must remain versioned
* Breaking changes require new versions
* Stub endpoints returning 404 are valid contracts

Never remove or repurpose existing contracts.

---

## Governance Principle (Non-Negotiable)

If a feature:

* cannot be replayed
* cannot be audited
* cannot be explained

…it does **not belong** in Decision Plane.

---

## Why This Matters (Design Intent)

Decision Plane is intentionally incomplete.

Its value comes from:

* what it records
* what it refuses to do
* what it makes explicit

This makes it:

* safe to fork
* safe to audit
* safe to sell products on top of

---

## Final Rule

> **Extend by addition, never by mutation.**

If you need to change core behavior, you are building a different system.
