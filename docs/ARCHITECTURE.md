# Architecture — Decision Plane

## Purpose

This document defines the **authoritative architecture** of **Decision Plane**.

It supersedes all phase-based notes, exploratory diagrams, and intermediate design discussions.
Its purpose is to describe **what the system is**, not how it evolved.

Decision Plane is a **decision infrastructure framework**.
It is **not** a domain product, not an automation engine, and not an agent system.

---

## Architectural Positioning

Decision Plane exists to support **inspection, governance, and reasoning over decisions** produced from document-centric machine learning pipelines.

It is intentionally positioned as:

* signal-first
* inspection-oriented
* deterministic
* replayable

It does **not** execute policies, enforce actions, or automate outcomes.

---

## Architectural Principles

The system is built around the following **non-negotiable principles**:

* Determinism over implicit behavior
* Auditability over automation
* Explicit state transitions
* Separation of concerns across layers
* Product-facing clarity over internal convenience

All components and features must conform to these principles.

---

## High-Level System Flow

```
Input Artifact
↓
Ingestion Boundary
↓
Raw Storage (immutable)
↓
Processing Pipeline
    - Extraction (pluggable or mocked)
    - Parsing
    - Feature materialization
↓
Processed Artifacts
↓
Decision Signals
↓
Review / Indexing
↓
Serving API
↓
Inspection Interface
```

Key properties:

* Each stage produces **explicit artifacts**
* Each stage persists **explicit state**
* No stage mutates upstream outputs
* All transitions are auditable

---

## Core Architectural Layers

### 1. Ingestion Boundary

**Responsibilities**

* Receive input artifacts
* Validate structural metadata
* Assign stable, deterministic identifiers
* Persist raw artifacts immutably

**Characteristics**

* Idempotent
* Side-effect controlled
* Fully auditable

The ingestion boundary defines the **start of determinism**.

---

### 2. Processing Layer

**Responsibilities**

* Text extraction (mocked or pluggable)
* Structured parsing
* Feature materialization

**Characteristics**

* Batch-oriented
* Deterministic
* Replayable from raw inputs

All processing steps emit **explicit step-level lineage**.

---

### 3. Processing Lineage Layer

**Responsibilities**

* Record step-level execution events
* Persist run identifiers
* Capture success, failure, and metadata

**Characteristics**

* Write-only during execution
* Read-only for inspection
* Fully ordered and timestamped

This layer exists to answer **“what happened and why”**, not to optimize execution.

---

### 4. Decision Signal Layer

**Responsibilities**

* Produce generic classifications
* Emit confidence and uncertainty signals
* Flag documents requiring human review

**Characteristics**

* Read-only with respect to upstream artifacts
* No policy enforcement
* No autonomous actions

This layer **produces signals, not decisions**.

---

### 5. Review and Indexing Layer

**Responsibilities**

* Materialize review queues
* Aggregate system state for dashboards
* Enable filtering and retrieval

**Characteristics**

* Derived views
* Non-authoritative
* Replaceable without affecting core state

---

### 6. Serving Layer (API)

The system exposes **strict, versioned APIs** for:

* Document listing
* Document detail inspection
* Review queue access
* Dashboard summaries

APIs are treated as **product contracts**, not internal plumbing.

Breaking changes require explicit version bumps.

---

### 7. Inspection Interface (UI)

The inspection interface enables:

* Exploration of documents
* Inspection of artifacts and signals
* Understanding of processing lineage

**Characteristics**

* Read-only with respect to decision logic
* No embedded business rules
* No autonomous behavior

---

## Configuration and Extensibility

Domain-specific behavior is introduced only through:

* Configuration
* Feature flags
* Controlled forks

The public repository **intentionally excludes**:

* Domain rules
* Production-trained models
* Proprietary datasets
* Enforcement or action logic

---

## Explicit Non-Goals

Decision Plane explicitly excludes:

* Autonomous policy execution
* Self-modifying systems
* Automated retraining pipelines
* Real-time inference guarantees
* Agent-based orchestration

These are **design constraints**, not deferred work.

---

## Architectural Stability

This architecture is considered **stable for v1.x**.

Future evolution is expected via:

* Additive features
* Extended read models
* Domain-specific forks

Not through breaking architectural shifts.

---

## Final Statement

Decision Plane exists to demonstrate **how decision-centric ML systems should be built** when correctness, auditability, and inspection matter more than speed or automation.

If a proposed change violates the principles in this document, the change is rejected.
