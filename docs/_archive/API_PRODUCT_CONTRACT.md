# API Product Contract — Risk-Aware ML System

## Purpose

This document defines the **product-facing API contract** for the Risk-Aware ML System.

The goal of this API is to expose **human-centered decision workflows** while
shielding internal ML and system complexity. The contract is designed to remain
stable even as internal models, pipelines, and infrastructure evolve.

This is a **conceptual contract**, not an implementation specification.

---

## Design Principles

* Product semantics over system internals
* Stable contracts over internal flexibility
* Explicit decisions over raw predictions
* Human-in-the-loop by design
* No hidden automation

The UI and external consumers **must not depend** on internal artifacts such as
prediction runs, feature versions, or labeling mechanics.

---

## Core Resources

The product exposes four primary resources:

```

/documents
/decisions
/feedback
/monitoring

```

Each resource maps directly to a user-visible concept.

---

## 1. Documents

### List Documents

```

GET /api/documents

````

**Description**  
Returns a list of documents visible to the user, along with their current
decision state.

**Response**
```json
[
  {
    "document_id": "doc-123",
    "status": "processed",
    "decision": "REVIEW",
    "score": 0.78,
    "last_updated": "2025-01-10T14:22:00Z"
  }
]
````

**Notes**

* `score` is provided for context, not optimization.
* Ordering and pagination are product concerns, not system guarantees.

---

### Upload Document

```
POST /api/documents
```

**Request**

```json
{
  "filename": "contract.pdf",
  "source": "upload"
}
```

**Response**

```json
{
  "document_id": "doc-124",
  "status": "ingested"
}
```

**Notes**

* Ingestion does not imply immediate decision availability.
* Processing and scoring occur asynchronously (batch-first).

---

## 2. Decisions

### Get Decision for Document

```
GET /api/documents/{document_id}/decision
```

**Description**
Returns the latest decision assigned to a document.

**Response**

```json
{
  "decision": "REVIEW",
  "score": 0.78,
  "threshold": 0.60,
  "decision_rule": "score >= threshold",
  "evaluated_at": "2025-01-10T14:22:00Z",
  "model_version": "v1"
}
```

**Notes**

* The decision rule is explicit and auditable.
* Model identifiers are exposed only at a high level.
* Decisions are immutable historical events.

---

## 3. Feedback

### Submit Feedback for Document

```
POST /api/documents/{document_id}/feedback
```

**Description**
Captures human feedback regarding a decision.

**Request**

```json
{
  "feedback_value": "ACCEPT",
  "confidence": 0.9,
  "notes": "Low risk after manual review"
}
```

**Response**

```json
{
  "status": "recorded",
  "feedback_id": 42
}
```

**Notes**

* Feedback does not override decisions automatically.
* Feedback does not trigger retraining.
* All feedback is versioned and auditable.

---

## 4. Monitoring

### Decision Quality Summary

```
GET /api/monitoring/summary
```

**Description**
Provides a high-level view of system decision health.

**Response**

```json
{
  "window": "last_30_days",
  "decision_distribution": {
    "ACCEPT": 72,
    "REVIEW": 28
  },
  "total_cost": 12500,
  "drift_status": {
    "prediction": "OK",
    "decision": "WARNING"
  }
}
```

**Notes**

* Metrics are aggregated and product-oriented.
* No raw drift metrics or training diagnostics are exposed.
* This endpoint is designed for understanding, not tuning.

---

## Explicit Exclusions

The following are intentionally **not exposed** via this API:

* Feature vectors
* Training datasets
* Labeling mechanics
* Raw drift statistics (e.g. PSI values)
* Model training metrics
* Automated policy controls

These exclusions preserve system safety and auditability.

---

## Stability Guarantees

This API contract guarantees:

* Backward compatibility for product consumers
* No breaking changes without explicit versioning
* Clear separation between product and system layers
* Deterministic behavior for identical requests

---

## Relationship to Internal Architecture

Internally, this API maps to:

* ingestion and processing pipelines
* prediction events
* feedback repositories
* monitoring and replay utilities

These mappings are **implementation details** and may evolve independently.

---

## Future Extensions (Non-Binding)

Potential future additions may include:

* pagination and filtering
* role-based access control
* multi-tenant document separation
* exportable audit reports

All such extensions must preserve the principles defined here.

---

## Summary

This API contract defines **how users interact with decisions**, not how models
are trained or deployed.

It reflects a product philosophy centered on:

* trust
* transparency
* accountability
* controlled automation
