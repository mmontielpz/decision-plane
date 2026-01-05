# Architecture — Decision Plane

## Purpose

This document defines the **authoritative architecture** of **Decision Plane**.

It supersedes all exploratory notes, phase-based documents, and intermediate design discussions.
Its purpose is to define **what the system is and is not**, independent of any domain, customer, or business objective.

Decision Plane is a **decision infrastructure framework**.
It is **not** a domain product, not an automation engine, and not a policy executor.

---

## Architectural Positioning

Decision Plane exists to support **inspection, governance, and reasoning** over decisions produced by document-centric machine learning pipelines.

It is intentionally positioned as:

* signal-first
* inspection-oriented
* deterministic
* replayable
* audit-driven

Decision Plane **does not**:

* decide what actions to take
* enforce outcomes
* optimize business objectives
* automate workflows

Those responsibilities belong **outside** the framework.

---

## Architectural Principles

The system is built around the following **non-negotiable principles**:

* **Determinism over implicit behavior**
* **Auditability over automation**
* **Explicit state transitions**
* **Separation of concerns across layers**
* **Product-facing clarity over internal convenience**

Any component or feature that violates these principles is **out of scope**.

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

Key invariants:

* Each stage produces **explicit artifacts**
* Each stage persists **explicit state**
* No stage mutates upstream outputs
* All transitions are timestamped and auditable

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

Processing produces **artifacts**, not decisions.

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

This layer exists to answer **“what happened and why”**, not **“what should happen next.”**

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

Signals are informational and domain-agnostic.

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

This layer exists for **inspection efficiency**, not correctness.

---

### 6. Serving Layer (API)

Decision Plane exposes **strict, versioned APIs** for:

* Document listing
* Document detail inspection
* Review queue access
* Dashboard summaries
* Deterministic replay (read-only)
* Explanation and timeline endpoints

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

The UI exists to **support human reasoning**, not to replace it.

---

## Open-Source Scope Boundary

Decision Plane **includes**:

* Architecture and system guarantees
* Deterministic ingestion and processing pipelines
* Processing lineage and audit trails
* Signal generation and uncertainty indicators
* Read-only replay and evaluation mechanisms
* Inspection-oriented APIs and contracts
* Synthetic or mock data for testing

Decision Plane **excludes**:

* Policy enforcement or action logic
* Business-specific cost optimization
* Automated decision execution
* Trained production models or learned heuristics
* Domain-specific rules or thresholds
* Organizational workflow logic
* Real or proprietary datasets

These exclusions are **intentional architectural constraints**, not deferred work.

---

## Configuration and Extensibility

Domain-specific behavior may be introduced **only** through:

* Configuration
* Feature flags
* Controlled forks
* Private extensions

The public repository intentionally avoids encoding:

* domain intent
* business economics
* operational strategy

---

## Architectural Stability

This architecture is considered **stable for v1.x**.

Future evolution is expected through:

* Additive read models
* Expanded inspection capabilities
* Extended lineage and replay views

Not through:

* automated decision logic
* self-modifying systems
* agent-based orchestration

---

## Final Statement

Decision Plane exists to demonstrate **how decision-centric ML systems should be built** when correctness, auditability, and inspection matter more than speed or automation.

If a proposed change causes the system to **decide what should happen**, rather than **explain what happened**, the change is **out of scope**.

