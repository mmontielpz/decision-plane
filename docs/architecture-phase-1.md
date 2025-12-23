# Architecture Overview — Phase 1 (Ingestion & Raw Storage)

## Purpose of Phase 1

Phase 1 establishes a **reliable, observable, and reproducible ingestion foundation** for the ML system.

The goal of this phase is **not modeling**.
Its purpose is to ensure that all downstream ML components operate on data that is:

* traceable
* versioned
* auditable
* resilient to partial failures
* reproducible over time

All subsequent phases depend on the guarantees introduced here.

---

## Scope and Responsibilities

Phase 1 is responsible for:

* accepting raw inputs through a well-defined ingestion interface
* validating and persisting ingestion metadata
* enforcing idempotent ingestion behavior
* storing raw data deterministically
* exposing clear failure signals
* providing integration-level test coverage

Phase 1 explicitly avoids feature engineering, labeling, and modeling concerns.

---

## High-Level Architecture (Logical)

```text
[Client / Source]
        |
        v
[FastAPI Ingestion Service]
        |
        |-- Validation (schema, required fields)
        |
        v
[Metadata Persistence Layer]
        |
        |-- SQLite (idempotent writes)
        |
        v
[Raw Storage]
        |
        |-- Deterministic filesystem layout
        |
        v
[Structured Logs + HTTP Responses]
```

This architecture prioritizes **clarity and correctness** over throughput.

---

## Core Components

### 1. Ingestion API

**Technology:** FastAPI
**Responsibility:** Entry point for all ingestion events.

The ingestion endpoint enforces:

* explicit request contracts
* schema-based metadata validation
* clear HTTP semantics
* isolation between ingestion and downstream processing

Each request represents a **single ingestion event**.

---

### 2. Validation Layer

**Technology:** Pydantic

Validation occurs before any persistence:

* metadata must be valid JSON
* required fields must be present
* invalid requests are rejected explicitly

Invalid data never reaches storage layers.

---

### 3. Metadata Store

**Technology:** SQLite

The metadata store provides:

* a persistent record of ingestion events
* idempotency guarantees via unique constraints
* traceability across ingestion attempts

Key properties:

* append-only semantics
* deterministic behavior
* local reproducibility for development and testing

This store is the **source of truth** for ingestion state.

---

### 4. Raw Storage

**Technology:** Filesystem (S3-compatible layout)

Raw data is stored using a deterministic directory structure:

```text
data/raw/
  └── <ingestion_date>/
      └── <source_system>/
          └── <document_id>/
              └── <original_filename>
```

Design principles:

* raw data is immutable
* raw data is never overwritten
* raw data can always be reprocessed
* storage layout encodes lineage implicitly

---

### 5. Logging and Observability

**Technology:** Structured Python logging

The ingestion service emits structured logs for:

* successful ingestions
* duplicate detection
* validation failures
* database errors
* filesystem errors

All failures are:

* observable
* explicit
* mapped to HTTP responses

No failure mode is silent.

---

### 6. Integration Tests

**Technology:** pytest + FastAPI TestClient

Phase 1 includes integration-level tests that validate:

* successful ingestion behavior
* idempotent duplicate handling
* validation error handling
* raw storage failure propagation

Tests operate against:

* real SQLite persistence
* real filesystem interactions
* explicit setup and teardown

This ensures behavior matches production semantics.

---

## Data Flow (Step-by-Step)

1. Client submits a multipart ingestion request.
2. Metadata is parsed and validated.
3. Metadata persistence is attempted.
4. Duplicate ingestion is detected via database constraints.
5. Raw data is written only on first ingestion.
6. Logs and HTTP responses reflect the final outcome.

Each step is independently observable.

---

## Failure Modes and Guarantees

### Validation Failures

* Occur before persistence
* Return HTTP 422
* Do not write to storage

### Duplicate Ingestion

* Detected via unique constraints
* Return HTTP 409
* Do not rewrite raw data

### Database Failures

* Return HTTP 500
* Logged explicitly
* Prevent partial writes

### Raw Storage Failures

* Return HTTP 500
* Metadata persistence is not silently rolled back
* Failures are observable and debuggable

---

## Explicit Non-Goals of Phase 1

Phase 1 does **not** address:

* feature extraction
* data cleaning beyond basic validation
* labeling or annotation workflows
* model training or inference
* performance optimization
* distributed scaling

These concerns are deferred intentionally.

---

## Phase 1 Outcome

At the completion of Phase 1, the system provides:

* a stable ingestion contract
* deterministic raw data storage
* idempotent ingestion semantics
* explicit failure handling
* test-validated behavior

This forms a **solid, auditable foundation** for all subsequent ML system phases.
