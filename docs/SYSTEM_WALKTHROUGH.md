# SYSTEM WALKTHROUGH — Decision Plane v1

## Purpose of This Document

This document provides a **concrete, end-to-end walkthrough** of how **Decision Plane v1** behaves for a single document.

It answers, explicitly:

* What happens to a document at each step
* What data is persisted
* What is deterministic vs derived
* Where human interaction occurs
* Where responsibility intentionally stops

This is not an API reference.
This is a **mental model of the system**.

---

## System Role (One Sentence)

**Decision Plane is a deterministic, auditable inspection layer that explains ML-assisted decisions without executing them.**

---

## High-Level Lifecycle

A document in Decision Plane moves through the following **explicit phases**:

```
Ingested
   ↓
Processed
   ↓
Signals Emitted
   ↓
Inspection (Dashboard / Queue / Detail)
   ↓
Human Decision (external)
```

No phase is implicit.
No phase is skipped.
No phase performs actions outside the system boundary.

---

## Step 1 — Ingestion

### Trigger

A client uploads a document and structured metadata.

### API

```
POST /api/ingest
```

### Inputs

* Document file (PDF, etc.)
* Structured metadata (validated schema)

  * document_id
  * ingestion_timestamp
  * source_system

### Persistence (Authoritative)

* `ingestion_events`
* Raw file stored immutably under deterministic path

### Guarantees

* Idempotent ingestion
* Raw artifacts are write-once
* Duplicate uploads do not duplicate state

### What does NOT happen

* No processing
* No prediction
* No inference
* No validation of business meaning

**Outcome:**
The system now knows *a document exists*.

---

## Step 2 — Processing Execution

### Trigger

Batch processing (seeded or real), executed explicitly.

### Internal Behavior

For each document:

* Processing run is created
* Steps are executed sequentially
* Each step records:

  * status
  * timestamp
  * metadata
  * error (if any)

### Persistence (Authoritative)

* `processing_runs`
* `processing_steps`
* `document_processing_status`

### Guarantees

* Deterministic execution
* Step-level lineage
* Partial failure is observable
* Historical runs are never overwritten

### What does NOT happen

* No auto-retry logic
* No hidden fallbacks
* No state mutation outside persisted records

**Outcome:**
The system knows *what happened and why* during processing.

---

## Step 3 — Prediction & Signal Emission

### Trigger

Prediction runs are executed as part of processing.

### Behavior

* Predictions are generated (or not)
* Confidence is evaluated
* Quality signals are emitted

### Signals (Examples)

* low_confidence
* missing_prediction
* unknown_document_type

Signals are **informational only**.

### Persistence (Authoritative)

* `prediction_runs`
* `prediction_events`
* `document_signals`

### Guarantees

* Signals are immutable
* Signals are explainable
* Signals never execute actions

### What does NOT happen

* No threshold tuning
* No policy enforcement
* No automated decisions

**Outcome:**
The system surfaces **uncertainty**, not conclusions.

---

## Step 4 — Visibility Rules

A document becomes **visible** to the product layer only if:

```
processing_status ∈ ('processed', 'indexed')
```

This rule is:

* Canonical
* Shared across all read models
* Tested explicitly

Hidden documents are not deleted.
They are simply not inspectable yet.

---

## Step 5 — Dashboard (Read Model)

### API

```
GET /api/dashboard/summary
```

### Data Shown

* total_visible_documents
* processed_documents
* documents_needing_review
* latest_activity_at

### Guarantees

* Read-only
* Derived from persisted state
* Rebuildable

### What does NOT happen

* No drill-downs
* No actions
* No alerts
* No metrics tuning

**Purpose:**
Situational awareness, not analysis.

---

## Step 6 — Review Queue (Human-in-the-Loop)

### API

```
GET /api/review-queue
```

### Inclusion Logic (Deterministic)

A document appears if **any** condition is true:

* Missing prediction
* Confidence below threshold
* Unknown document type

### Returned Fields

* document_id
* reason (single, explicit)

### Guarantees

* Stable ordering
* Deterministic reasons
* No inference in the UI

### What does NOT happen

* No ranking heuristics
* No prioritization ML
* No auto-assignment

**Purpose:**
Focus human attention where uncertainty exists.

---

## Step 7 — Document Detail Inspection

### API

```
GET /api/documents/{document_id}
```

### Data Shown

* Document metadata
* Current lifecycle state
* Latest prediction (if any)
* Emitted signals
* Processing lineage summary

### Stubbed Endpoints (Intentional)

```
/replay        → 404
/explanation   → 404
/timeline      → 404
```

These stubs:

* Lock API contracts
* Signal future extension points
* Avoid misleading partial implementations

### Guarantees

* No hidden computation
* No implicit aggregation
* No state mutation

**Purpose:**
Enable explanation, not persuasion.

---

## Step 8 — Replay (Read-Only)

### API

```
GET /api/replay/run/{run_id}?threshold=X
```

### Behavior

* Re-evaluates historical predictions
* Uses new threshold
* Produces derived outputs only

### Guarantees

* No writes
* No mutation of history
* Deterministic outputs

### What does NOT happen

* No model retraining
* No persistence
* No side effects

**Purpose:**
Safe experimentation and audit support.

---

## Step 9 — Human Decision (Outside the System)

Decision Plane **stops here**.

It does not:

* Approve
* Reject
* Escalate
* Notify
* Trigger workflows

This boundary is **intentional and permanent**.

---

## Why This Design Matters (MLE Signal)

This system demonstrates:

* Determinism over convenience
* Auditability over automation
* Explicit state over implicit behavior
* Human accountability over ML authority

Most ML systems answer:

> “What is the prediction?”

Decision Plane answers:

> “What happened, why, and where uncertainty exists.”

---

## Extension Model (For Forks & Products)

Allowed extensions:

* Domain-specific ingestion
* Custom processing steps
* New signal types
* New read models

Forbidden extensions:

* Hidden automation
* Implicit decisions
* State mutation via UI
* Non-deterministic behavior

---

## Final Positioning

Decision Plane v1 is **intentionally conservative**.

Its value is not speed.
Its value is **trust**.

If a feature compromises auditability or replayability, it does not belong.
