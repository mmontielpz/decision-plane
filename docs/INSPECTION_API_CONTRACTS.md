# Inspection API Contracts — Decision Plane

## Purpose

This document defines the **public, product-facing inspection APIs** exposed by **Decision Plane**.

These APIs exist to:

* enable human inspection
* surface lineage, artifacts, and signals
* support analysis and replay comparison

They do **not** execute decisions, mutate core state, or trigger actions.

This document is a **contract**, not an implementation guide.

---

## API Philosophy

Inspection APIs in Decision Plane are:

* **Read-only**
* **Deterministic**
* **Versioned**
* **Side-effect free**
* **Derived from authoritative state**

They expose **what exists**, never **what should happen**.

---

## Contract-First Principle

All inspection APIs are defined by:

* explicit request/response schemas
* stable semantics per version
* backward compatibility within v1.x

Implementations must conform to the contract.
Contracts do not conform to implementations.

---

## Global API Invariants

The following invariants apply to **all inspection endpoints**:

* No endpoint may mutate persisted state
* No endpoint may trigger processing or prediction
* No endpoint may encode policy or decision logic
* No endpoint may infer or resolve outcomes
* No endpoint may hide or suppress data

Violating any invariant constitutes a **breaking change**.

---

## API Versioning

### URL Versioning

All public APIs are versioned at the path level:

```
/api/v1/inspection/...
```

### Version Rules

* v1.x guarantees semantic stability
* Breaking changes require a new major version
* Deprecated fields must remain readable
* Parallel versions may coexist

---

## Core Inspection Resources

### 1. Documents

#### GET /api/v1/inspection/documents

Returns a paginated list of documents.

**Properties**

* document identifier
* source metadata
* current lifecycle state
* ingestion timestamp

No filtering implies prioritization.

---

#### GET /api/v1/inspection/documents/{document_id}

Returns a single document and its high-level state.

Includes:

* identity metadata
* processing status
* references to related resources

---

### 2. Processing Lineage

#### GET /api/v1/inspection/documents/{document_id}/processing-runs

Returns all processing runs associated with a document.

Each run includes:

* run identifier
* processor version
* execution status
* timestamps

---

#### GET /api/v1/inspection/processing-runs/{run_id}/steps

Returns step-level lineage for a processing run.

Includes:

* step name
* step status
* structured metadata
* timestamps

This endpoint exists to answer **“what happened and why”**.

---

### 3. Artifacts

#### GET /api/v1/inspection/documents/{document_id}/artifacts

Returns references to derived artifacts.

Artifacts are:

* immutable
* versioned
* read-only

Artifact retrieval does not imply validity or correctness.

---

### 4. Signals

#### GET /api/v1/inspection/documents/{document_id}/signals

Returns all decision signals associated with a document.

Includes:

* signal type
* value
* confidence (if present)
* source reference
* timestamp

Signals are unordered and non-ranked.

---

### 5. Prediction Inspection

#### GET /api/v1/inspection/documents/{document_id}/predictions

Returns raw prediction outputs for the document.

Includes:

* prediction run reference
* raw scores
* model version
* feature hash
* inference metadata

No interpretation or thresholding is applied.

---

### 6. Evaluation and Analysis

#### GET /api/v1/inspection/evaluation/windows

Returns aggregated evaluation windows.

Includes:

* window boundaries
* metrics
* evaluation configuration reference

All values are explicitly labeled as **analytical**.

---

### 7. Replay Views

#### GET /api/v1/inspection/documents/{document_id}/replays

Returns a comparison view of processing or prediction runs.

Includes:

* run identifiers
* version differences
* artifact and signal deltas

Replay views never overwrite historical data.

---

## Filtering and Query Semantics

Allowed:

* filtering by explicit fields (date, status, type)
* pagination
* sorting by persisted timestamps

Disallowed:

* priority ordering
* hidden scoring
* ranking based on policy
* suppression of results

Filtering is **mechanical**, not semantic.

---

## Error Handling

Inspection APIs use explicit HTTP semantics:

* `200` — successful read
* `404` — resource does not exist or is intentionally unimplemented
* `400` — invalid request
* `500` — internal error

Intentional `404` stubs are valid for unimplemented inspection views in v1.

---

## Authentication and Authorization

Inspection APIs may be protected by authentication layers.

However:

* authorization must not alter response semantics
* access control must not modify or filter data content
* unauthorized access results in denial, not mutation

Security is orthogonal to correctness.

---

## Prohibited API Behaviors

The following are explicitly forbidden:

* POST, PUT, PATCH, DELETE on inspection resources
* endpoints that imply action or resolution
* endpoints that return “recommended decisions”
* endpoints that mutate read models as side effects
* endpoints that auto-advance lifecycle state

Any such endpoint violates system boundaries.

---

## Evolution Rules

Allowed:

* new inspection endpoints
* additional fields in responses
* new read models
* richer lineage views

Disallowed:

* changing semantics of existing fields
* embedding decision logic
* introducing write paths
* collapsing inspection into execution

---

## Auditability Requirements

Inspection APIs must ensure:

* every field is traceable to persisted state
* response data is reproducible
* absence of data is explainable
* historical views remain accessible

APIs are part of the audit surface.

---

## Final Statement

Inspection APIs are the **lens**, not the **hand**.

If an API begins to:

* decide
* prioritize
* resolve
* or act

then it is no longer an inspection API and does not belong in Decision Plane.
