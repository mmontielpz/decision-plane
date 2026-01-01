# Dashboard Metrics v1

## Context

The system processes and manages large volumes of documents coming from one or more sources.
Operators and analysts need immediate situational awareness to understand the current state
of their workload without inspecting individual documents.

This dashboard provides a **read-only operational summary** of the system.

---

## Target User

Primary user:
- Document operator / analyst
- Responsible for monitoring, reviewing, and validating documents
- Not a technical user
- Not interested in pipeline internals

---

## Goal

Provide **instant situational awareness** so the user can answer, in seconds:

- How many documents are currently active?
- How many are already resolved?
- How many require attention?
- Has there been recent activity?

The dashboard does **not** support actions in v1.

---

## Non-Goals

The following are explicitly out of scope for v1:

- Editing documents
- Viewing document content (PDF viewer)
- Feedback or corrections
- Alerts or notifications
- SLA tracking
- ML confidence scores
- Internal pipeline states

---

## Definitions

### Visible Document

A document is considered *visible* if:

```

processing_status ∈ ('processed', 'indexed')

```

This definition is canonical and shared with the Documents list and detail views.

---

## Metrics (v1)

### 1. Total Visible Documents

**Question answered:**
> How many documents are ready and relevant?

Definition:
- Count of visible documents

---

### 2. Processed Documents

**Question answered:**
> How many documents are already resolved?

Definition:
- Count of visible documents with final automated processing
- In v1, this may equal total visible documents

---

### 3. Documents Needing Review

**Question answered:**
> Where does human attention need to be applied?

Definition:
- Documents requiring manual review
- In v1, this metric may be zero

---

### 4. Latest Activity Timestamp

**Question answered:**
> Is the system actively processing documents?

Definition:
- Most recent `updated_at` among visible documents

---

## API Contract (Proposed)

Endpoint:
```

GET /api/dashboard/summary

````

Response shape:
```json
{
  "total_visible_documents": 10,
  "processed_documents": 10,
  "documents_needing_review": 0,
  "latest_activity_at": "2026-01-01T03:09:08Z"
}
````

Notes:

* Read-only
* No pagination
* No filters
* Stable contract

---

## Frontend Expectations

* Dashboard is informational only
* No clickable actions in v1
* Metrics must match Documents list semantics
* No inference or client-side counting

---

## Success Criteria

The dashboard is considered successful if:

* Metrics are consistent with document list and detail views
* Users can understand system state without navigating documents
* No technical knowledge is required to interpret metrics

---

## Future Extensions (Not v1)

Potential future enhancements:

* Urgency / priority signals
* Review queues
* Time-based trends
* Alerts and notifications
* SLA metrics
