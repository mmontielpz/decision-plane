# Architecture Overview — Phase 2 (Processed Storage & Feature Extraction)

## Purpose of Phase 2

Phase 2 introduces the **processing layer** that transforms immutable raw inputs into **reproducible processed artifacts** and **feature-ready representations**.

The primary goal is to make downstream ML development feasible without compromising the guarantees established in Phase 1:

* raw data remains immutable and auditable
* every processed artifact is traceable to raw inputs
* processing can be rerun deterministically
* failures are observable and recoverable

Phase 2 explicitly prioritizes **correctness and lineage** over performance.

---

## Scope and Responsibilities

Phase 2 is responsible for:

* defining a processed data contract (schemas, naming, versioning)
* creating processed artifacts from raw documents
* extracting minimal baseline representations (e.g., normalized text + metadata)
* generating feature records suitable for model training/inference pipelines
* persisting processing status and lineage metadata
* enabling safe reprocessing (backfills) from raw storage

Phase 2 explicitly avoids:

* model training
* serving inference endpoints
* advanced NLP/CV pipelines (beyond a baseline)
* human labeling workflows (Phase 3)
* distributed compute (later optimization)

---

## High-Level Architecture (Logical)

```text
[Raw Storage]  (Phase 1)
     |
     v
[Processor / Feature Builder]
     |
     |-- Parse / Normalize / Validate
     |-- Extract baseline representation (text, layout hints, metadata)
     |
     v
[Processed Storage]
     |
     v
[Feature Store (MVP)]
     |
     v
[Metadata + Lineage Updates]
     |
     v
[Structured Logs + Metrics (later)]
```

Phase 2 introduces a **batch-first pipeline** that can later be extended to near-real-time.

---

## Data Contracts

### 1. Input Contract (from Phase 1)

Inputs come exclusively from **Raw Storage** and **Metadata Store**:

* raw file path
* document_id
* ingestion_timestamp
* source_system
* optional document_type

Raw inputs are immutable; Phase 2 never alters Phase 1 artifacts.

---

### 2. Processed Artifact Contract

Processed artifacts must be:

* reproducible from raw
* schema-defined
* versioned
* traceable by document_id and processing_run_id

Minimum processed record fields:

* document_id
* ingestion_timestamp
* source_system
* processing_timestamp
* processor_version
* extraction_method (e.g., "plain_text", "pdf_text", "fallback")
* normalized_text (if available)
* parsing_warnings (optional)
* raw_path (lineage pointer)

---

### 3. Feature Record Contract (MVP)

Features are derived from processed artifacts and should be **stable** and **cheap** to compute.

MVP feature record fields:

* document_id
* feature_timestamp
* feature_version
* features (key-value map)

  * token_count
  * char_count
  * line_count
  * has_numbers_ratio
  * has_currency_symbols
  * top_k_keywords (optional, baseline)
* processed_path (lineage pointer)

Features should be deterministic and reproducible across runs.

---

## Storage Strategy

### 1. Processed Storage Layout

Processed artifacts are stored as JSON (MVP) with a deterministic directory structure:

```text
data/processed/
  └── <ingestion_date>/
      └── <source_system>/
          └── <document_id>/
              ├── processed.json
              └── processor_manifest.json
```

Notes:

* `processed.json` contains the processed record (schema-defined).
* `processor_manifest.json` includes run metadata and versioning details.

---

### 2. Feature Storage Layout (MVP)

For MVP, store features as JSON (later can move to Parquet/DuckDB):

```text
data/features/
  └── <feature_version>/
      └── <ingestion_date>/
          └── <source_system>/
              └── <document_id>.json
```

This makes feature backfills explicit and versioned.

---

### 3. Metadata Store Extension (SQLite)

Extend SQLite with processing state tracking.

Minimum new tables:

**processing_runs**

* run_id (uuid)
* started_at
* completed_at
* processor_version
* status (success / failed / partial)
* notes (optional)

**document_processing_status**

* document_id (unique)
* last_run_id
* status (processed / failed / skipped)
* processed_path
* feature_path
* error_code (optional)
* error_message (optional)
* updated_at

Key goals:

* allow reprocessing without ambiguity
* ensure observability over which docs are processed
* detect stuck or failing documents

---

## Core Components

### 1. Processor (Batch Job)

A Python module or CLI job that:

1. scans raw storage for unprocessed documents
2. loads raw files
3. extracts baseline content (text)
4. writes processed artifacts
5. computes minimal features
6. updates SQLite processing state
7. logs structured events

This is intentionally batch-first for determinism.

---

### 2. Extraction Methods (Baseline)

MVP extraction methods:

* `.txt` → read as UTF-8 text
* `.pdf` → defer advanced parsing; baseline extraction can be:

  * placeholder for later (Phase 3)
  * or naive text extraction library (optional, but can be deferred)

For Phase 2 MVP, prefer restricting initial scope to `.txt` or “text-extractable” inputs.

---

### 3. Versioning

Versioning is mandatory to ensure reproducibility:

* `processor_version`: static string in code (e.g., "0.2.0")
* `feature_version`: separate version identifier (e.g., "v1")

Changing feature definitions requires incrementing `feature_version`.

---

## Data Flow (Step-by-Step)

1. Identify candidate documents:

   * raw exists
   * not processed (via SQLite status table)
2. Read raw file.
3. Produce processed representation (normalized text + metadata).
4. Persist processed artifacts to `data/processed/...`.
5. Extract features and persist to `data/features/...`.
6. Update SQLite processing status:

   * processed_path and feature_path
   * status=processed
7. Emit structured logs per document and per run.

---

## Failure Modes and Guarantees

### Raw Read Failures

* status=failed in SQLite
* error_message recorded
* raw remains intact
* document can be retried

### Processing Failures (Parsing)

* failures recorded per document
* processed artifacts not written (or written as partial with warnings, if explicitly supported)
* pipeline continues with other documents

### Feature Extraction Failures

* processing can succeed even if features fail (optional)
* failures must be explicit and queryable

### Reprocessing Guarantees

* processed artifacts and features are reproducible from raw + versioned code
* feature_version isolates changes
* processing_runs table provides lineage per batch execution

---

## Observability (Phase 2)

Minimum events to log (structured):

* processing_run_started
* document_processing_started
* document_processed
* document_failed
* processing_run_completed

Each event includes:

* run_id
* document_id (when applicable)
* paths written
* processor_version / feature_version
* latency (optional)

Metrics are introduced in a later step after correctness is stable.

---

## Phase 2 Deliverables

At the completion of Phase 2, the system provides:

* processed artifacts with explicit schemas and deterministic layout
* a baseline feature store (versioned)
* SQLite processing state tracking
* a batch processor capable of backfills and retries
* integration tests for:

  * processed artifact creation
  * feature generation
  * status tracking and idempotent reprocessing

This establishes a stable foundation for Phase 3 (labeling + modeling).

---

## Phase 2 Non-Goals

Phase 2 does not include:

* production deployment of processor jobs
* distributed compute frameworks
* advanced OCR / PDF layout intelligence
* model training, selection, or inference
* monitoring dashboards (beyond logs)
