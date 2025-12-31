# Phase 1 — Implementation Stack

Risk-Aware ML System

## 1. Purpose

This document defines the **minimal implementation stack** selected for Phase 1 (Data Ingestion and Storage).

The goal is to enable a **correct, traceable, and reproducible implementation** of the designed ingestion pipeline without introducing premature complexity.

All choices are driven by the system contract defined in Phase 0 and Phase 1 design documents.

---

## 2. Selected Stack (Phase 1)

```text
Language:        Python
API Layer:       FastAPI
Validation:      Pydantic
Raw Storage:     Filesystem (S3-compatible layout)
Processed Data:  Filesystem (JSON / Parquet)
Metadata Store:  SQLite
Logging:         Python structured logging
Metrics:         Basic counters
```

This stack is intentionally minimal and locally reproducible.

---

## 3. Rationale by Component

### 3.1 Language — Python

Python is selected due to:

* ecosystem maturity
* readability and maintainability
* strong support for ML-adjacent workflows
* alignment with production ML systems in practice

No language-level optimizations are required at this stage.

---

### 3.2 API Layer — FastAPI

FastAPI is used to:

* define a clear ingestion contract
* enforce request validation
* expose ingestion endpoints realistically
* support both interactive and batch ingestion

It enables production-like interfaces without operational overhead.

---

### 3.3 Validation — Pydantic

Pydantic is used for:

* schema validation
* type enforcement
* explicit error reporting

More advanced validation frameworks are deferred until ingestion contracts stabilize.

---

### 3.4 Raw Storage — Filesystem (S3-Compatible Layout)

Raw data is stored in a structured filesystem layout that mirrors object storage semantics.

Reasons:

* transparency and inspectability
* immutable raw data guarantees
* easy migration to cloud object storage
* no dependency on external services

The filesystem is treated as the **source of truth**.

---

### 3.5 Processed Data Storage — Filesystem (JSON / Parquet)

Processed data is stored separately from raw data using simple, versionable formats.

Reasons:

* clear separation of concerns
* reproducibility from raw data
* compatibility with downstream pipelines
* minimal tooling requirements

---

### 3.6 Metadata Store — SQLite

SQLite is selected as the sole metadata store for Phase 1.

It is used to track:

* ingestion events
* document identifiers
* timestamps
* ingestion status
* error codes
* basic latency metrics

Reasons for SQLite:

* ACID guarantees
* zero infrastructure overhead
* portability
* ease of inspection
* sufficient for operational metadata

Analytical workloads are explicitly out of scope for Phase 1.

---

### 3.7 Logging — Python Structured Logging

Structured logging is used to:

* record ingestion events
* capture validation and processing errors
* support debugging and observability

Logs are treated as operational signals, not analytics data.

---

### 3.8 Metrics — Basic Counters

Basic counters are implemented to track:

* ingestion throughput
* error rates
* latency distributions

The goal is to define **what should be measured**, not to deploy full monitoring infrastructure.

---

## 4. Explicitly Deferred Technologies

The following technologies are intentionally excluded from Phase 1:

* message brokers (Kafka, etc.)
* workflow orchestrators (Airflow, etc.)
* distributed processing frameworks
* feature stores
* managed cloud services
* container orchestration platforms

These tools are unnecessary for validating the ingestion contract and would introduce avoidable complexity.

---

## 5. Evolution Path

This stack is designed to evolve without requiring system redesign.

Potential future changes include:

* replacing filesystem storage with object storage
* migrating SQLite to a service-backed database
* introducing distributed ingestion
* expanding monitoring infrastructure

Such changes are deferred until system constraints justify them.

---

## 6. Phase 1 Outcome

At the end of Phase 1, this stack enables:

* a working ingestion pipeline
* reproducible storage
* observable system behavior
* a stable foundation for feature engineering and modeling

Implementation begins only after this document is accepted.

---

## Status

Phase 1 — **Implementation stack defined and approved**.
