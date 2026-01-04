# V1 Feature Matrix — Decision Plane

## Purpose

This document defines the **Decision Plane v1.0 feature set**.

It answers three questions unambiguously:

1. What capabilities exist in v1
2. Why each capability exists
3. How each capability is proven (tests / artifacts)

This is a **delivery contract**, not a roadmap.

---

## V1 Definition

**Decision Plane v1.0** is a:

* Deterministic decision inspection framework
* With full processing lineage
* Replayable execution
* Product-facing read models
* Stable API contracts

It is **not** a production automation engine.

---

## Feature Categories

Features are grouped by **system responsibility**, not by implementation layers.

---

## 1. Ingestion & Raw Artifact Handling

| Feature                    | Description                                  | Proof                     |
| -------------------------- | -------------------------------------------- | ------------------------- |
| Deterministic document IDs | Stable IDs assigned at ingestion             | `test_ingest_endpoint.py` |
| Immutable raw storage      | Raw artifacts never mutate                   | Storage path semantics    |
| Idempotent ingestion       | Duplicate ingestion does not duplicate state | DB constraints            |

**Seniority Signal**
Demonstrates understanding of idempotency, immutability, and data contracts.

---

## 2. Processing Execution

| Feature                  | Description                            | Proof                  |
| ------------------------ | -------------------------------------- | ---------------------- |
| Batch processing         | Controlled batch execution             | `test_batch_runner.py` |
| Versioned processing     | Processor version persisted            | `processing_runs`      |
| Partial failure handling | One doc can fail without halting batch | Status semantics       |

**Seniority Signal**
Shows awareness of real-world batch failure modes.

---

## 3. Processing Lineage (Write Model)

| Feature            | Description                   | Proof                                    |
| ------------------ | ----------------------------- | ---------------------------------------- |
| Processing runs    | Every execution has a run ID  | `processing_runs`                        |
| Step-level lineage | Each step recorded explicitly | `processing_steps`                       |
| Error attribution  | Errors tied to steps          | `test_processing_lineage_write_model.py` |

**High-Value Signal**
This is rarely implemented correctly in ML systems.

---

## 4. Replayability

| Feature            | Description                         | Proof              |
| ------------------ | ----------------------------------- | ------------------ |
| Replay from raw    | Re-run processing deterministically | `replay/runner.py` |
| Isolated runs      | Replay does not overwrite history   | Append-only tables |
| Comparable outputs | Old vs new runs observable          | Read models        |

**Product Impact**
Enables experimentation, debugging, and audits without risk.

---

## 5. Decision Signals (Not Decisions)

| Feature              | Description                       | Proof              |
| -------------------- | --------------------------------- | ------------------ |
| Signal emission      | Confidence and quality signals    | `triage_runner.py` |
| No policy execution  | Signals only, no actions          | Architecture       |
| Explicit uncertainty | Missing / low confidence surfaced | Tests              |

**ML Maturity Signal**
Separates inference from decision authority.

---

## 6. Review Queue (Inspection Layer)

| Feature                | Description                 | Proof                      |
| ---------------------- | --------------------------- | -------------------------- |
| Review queue           | Documents needing attention | `test_review_queue_api.py` |
| Explicit reasons       | Why review is required      | Signal mapping             |
| Deterministic ordering | Stable ordering semantics   | SQL ordering               |

**Product Relevance**
Maps directly to human-in-the-loop workflows.

---

## 7. Document Detail Inspection

| Feature                 | Description                      | Proof                                   |
| ----------------------- | -------------------------------- | --------------------------------------- |
| Unified document view   | All derived state in one payload | `DocumentDetailV1`                      |
| Latest prediction       | Latest model output only         | Repository logic                        |
| Processing lineage view | Step history included            | `test_processing_lineage_read_model.py` |

**Senior MLE Signal**
Shows system-level thinking beyond model outputs.

---

## 8. Read Model Isolation

| Feature                  | Description            | Proof                           |
| ------------------------ | ---------------------- | ------------------------------- |
| Dashboard summary        | Aggregated read model  | `test_dashboard_summary_api.py` |
| Non-authoritative views  | Views rebuildable      | Architecture                    |
| API contract enforcement | Extra fields forbidden | Pydantic contracts              |

**Engineering Discipline Signal**
Prevents accidental coupling.

---

## 9. API Contracts

| Feature             | Description                | Proof            |
| ------------------- | -------------------------- | ---------------- |
| Versioned contracts | Explicit V1 schemas        | `contracts/`     |
| Strict validation   | Extra fields rejected      | `extra="forbid"` |
| Backward safety     | No silent breaking changes | Tests            |

**Open-Source Credibility**
Consumers can trust upgrades.

---

## 10. Audit & Governance Foundations

| Feature              | Description              | Proof          |
| -------------------- | ------------------------ | -------------- |
| Full execution trace | From raw to signal       | Lineage tables |
| Timestamped events   | Every action timestamped | Schema         |
| Queryable history    | SQL-accessible           | DB design      |

**Governance Value**
Supports regulated environments without special tooling.

---

## Explicitly Out of Scope for v1

| Excluded Capability      | Reason                       |
| ------------------------ | ---------------------------- |
| Online inference         | Violates determinism focus   |
| Model training pipelines | Not inspection-layer concern |
| Automated actions        | Governance risk              |
| Real-time SLAs           | Infrastructure concern       |

---

## V1 Completion Criteria

Decision Plane v1.0 is complete when:

* All tests pass
* All contracts are frozen
* Lineage is end-to-end
* Replay is deterministic
* No hidden state exists

This milestone is **already architecture-complete**.

---

## Final Positioning

Decision Plane v1.0 delivers:

* Senior-level ML system design
* Clear separation of concerns
* Audit-ready infrastructure
* Forkable, domain-neutral core

It is intentionally **boring, explicit, and strict**.

That is the value.
