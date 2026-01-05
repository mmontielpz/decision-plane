# Data Model Overview — Decision Plane

## Purpose

This document defines the **core data model** of **Decision Plane** and the **relationships between persisted entities**.

It describes:

* What data exists
* Why it exists
* How it is allowed to change
* What is authoritative vs derived

This is a **system-level data model**, not a domain schema.

---

## Data Model Philosophy

Decision Plane follows these principles:

* **Raw inputs are immutable**
* **Derived artifacts are append-only**
* **State transitions are explicit**
* **Read models are non-authoritative**
* **Nothing is inferred implicitly**

If data is not persisted, it is considered **non-existent**.

---

## High-Level Entity Map

```
Ingestion
│
├── ingestion_events
│
├── documents
│   ├── document_processing_status
│   ├── document_artifacts
│   ├── document_signals
│   └── labels (optional, delayed)
│
├── processing_runs
│   └── processing_steps
│
├── prediction_runs
│   └── prediction_events
│
├── drift_events
│
├── evaluation_windows
│
└── feedback_events
    └── prediction_feedback_links
```

Entities are grouped by **responsibility**, not by execution order.

---

## Core Entities

### 1. `documents`

**Role**

Represents the logical identity of an ingested artifact.

**Key Properties**

* Stable document identifier
* Source reference
* Creation timestamp
* High-level ingestion status

**Guarantees**

* One row per logical document
* Never deleted
* Never rewritten

---

### 2. `ingestion_events`

**Role**

Records the fact that a document entered the system.

**Key Properties**

* Document identifier
* Ingestion timestamp
* Source system
* Ingestion status

**Guarantees**

* One ingestion event per document
* Defines the start of determinism

---

### 3. `document_processing_status`

**Role**

Represents the **current lifecycle state** of a document.

**Key Properties**

* Current status (ingested, processed, failed, indexed, triaged)
* Last processing run reference
* Paths to derived artifacts
* Error metadata (if applicable)

**Guarantees**

* Single authoritative row per document
* Updated explicitly
* No implicit transitions

`triaged` represents a **descriptive lifecycle marker only**.
It does not imply prioritization, enforcement, or action.

---

## Processing Execution Entities

### 4. `processing_runs`

**Role**

Represents a single execution of the processing pipeline.

**Key Properties**

* Run identifier
* Processor version
* Start and completion timestamps
* Final run status

**Guarantees**

* Append-only
* Immutable after completion

---

### 5. `processing_steps`

**Role**

Records **step-level lineage** within a processing run.

**Key Properties**

* Run identifier
* Document identifier
* Step name
* Step status
* Structured metadata
* Timestamps

**Guarantees**

* Append-only
* Ordered by creation time
* Complete execution trace

This table exists to answer **“what happened and why”**.

---

## Prediction and Signal Entities

### 6. `prediction_runs`

**Role**

Represents a batch inference execution.

**Key Properties**

* Model name and version
* Feature version
* Dataset reference
* Execution status
* Execution timestamp

**Guarantees**

* Append-only
* Versioned
* No overwrite of prior runs

---

### 7. `prediction_events`

**Role**

Stores **raw model inference outputs** per document.

**Key Properties**

* Document identifier
* Raw score(s)
* Model output vector (optional)
* Feature hash
* Model version
* Inference metadata
* Prediction run reference

**Guarantees**

* Deterministic per run
* Immutable once written
* **No policy or decision semantics**

This table contains **model facts only**, not interpretations.

---

### 8. `document_signals`

**Role**

Stores **decision-relevant inspection signals** derived from processing or prediction outputs.

Examples:

* low confidence
* missing prediction
* data quality flags
* schema mismatch indicators

**Key Properties**

* Signal type
* Signal value
* Optional confidence
* Timestamp
* Source reference

**Guarantees**

* Informational only
* No enforcement semantics
* No policy thresholds

---

## Monitoring and Evaluation Entities

### 9. `drift_events`

**Role**

Records detected distributional or behavioral shifts.

**Key Properties**

* Metric type
* Metric value
* Window boundaries
* Detection timestamp
* Informational alert flag

**Guarantees**

* Analytical only
* No automatic action
* No enforcement hooks

---

### 10. `evaluation_windows`

**Role**

Stores **aggregated analytical evaluations** over historical windows.

**Key Properties**

* Window boundaries
* Metric counts (tp, fp, tn, fn)
* Evaluation configuration version
* Derived cost or utility values (analytical only)

**Guarantees**

* Fully derived from historical data
* Recomputable at any time
* Non-authoritative
* No decision semantics

This entity supports **post-hoc analysis**, not execution.

---

## Feedback and Labeling Entities

### 11. `labels`

**Role**

Represents human or external labels associated with documents.

**Key Properties**

* Label value
* Source
* Version
* Confidence
* Timestamp

**Guarantees**

* Versioned
* Non-destructive
* Late-arriving labels allowed

---

### 12. `feedback_events` and `prediction_feedback_links`

**Role**

Records external feedback and explicitly links it to historical predictions.

**Guarantees**

* Explicit linkage
* No implicit correction of past predictions
* No retroactive mutation of state

---

## Read Models vs Core State

### Core State (Authoritative)

* documents
* ingestion_events
* document_processing_status
* processing_runs
* processing_steps
* prediction_runs
* prediction_events

### Derived / Read Models (Non-Authoritative)

* inspection queues
* dashboards
* summaries
* timelines
* analytical aggregations

Read models:

* can be rebuilt
* can be replaced
* must never mutate core state

---

## Versioning Strategy

* Schema changes are additive
* Breaking changes require version bumps
* Contracts protect product consumers
* Historical data is never rewritten

---

## Evolution Rules

Allowed:

* New tables
* New columns
* New read models
* New derived analytics

Disallowed:

* Deleting core tables
* Mutating historical records
* Reinterpreting stored data
* Implicit state derivation
* Persisting policy or action semantics

---

## Final Statement

The Decision Plane data model is designed to make **history explicit**.

If data is not persisted, it is not trusted.
If history is mutable, auditability is broken.
If policy enters core state, the system has failed.

All future extensions must preserve these invariants.
