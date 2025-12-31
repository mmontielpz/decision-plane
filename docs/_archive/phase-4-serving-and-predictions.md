# Phase 4 — Serving and Prediction Contracts

## 1. Serving Objectives

Phase 4 introduces production-oriented inference with the goal of generating **risk-aware prediction events** that can be consumed by downstream workflows.

Serving objectives:

* produce predictions reproducibly from versioned inputs
* support batch-first inference with deterministic artifacts
* store predictions as immutable events
* ensure failures are observable and recoverable
* preserve auditability through explicit provenance

The system prioritizes **correctness and traceability** over throughput.

---

## 2. Batch Inference Flow

Batch inference is the primary serving mode in the MVP.

High-level flow:

```text
[Feature Records] (Phase 2)
     |
     v
[Load Model Artifact] (Phase 3)
     |
     v
[Batch Scoring Job]
     |
     |-- failure --> [Error Log + Mark Failed + Continue]
     |
     v
[Prediction Events]
     |
     v
[Prediction Storage + Run Metadata]
```

Step-by-step:

1. Load a stable set of feature records for a bounded run.
2. Load a single model artifact identified by `model_version`.
3. Score records deterministically.
4. Write prediction events to storage (append-only).
5. Store run metadata (start time, end time, counts, status).

No serving occurs without explicit version inputs.

---

## 3. Prediction Data Contract

Predictions are stored as immutable events.

Minimum prediction fields:

* `prediction_id` (unique)
* `document_id`
* `prediction_timestamp`
* `model_version`
* `feature_version`
* `prediction_value` (score or probability)
* `decision_threshold` (optional)
* `decision` (optional, derived from threshold)
* `metadata` (optional JSON)

Notes:

* `prediction_value` must be interpretable as a risk score.
* Thresholds may change over time; both score and threshold are recorded.
* The system supports ranking and threshold-based decisions.

---

## 4. Model and Feature Versioning

Each prediction must be traceable to:

* the exact model artifact (`model_version`)
* the feature representation (`feature_version`)
* the run context (batch job metadata)

Versioning rules:

* a model artifact is immutable once created
* feature definitions are versioned explicitly
* predictions are never overwritten

This enables:

* reproducible replay
* backtesting under new thresholds
* post-hoc audits

---

## 5. Failure Modes

Serving failures must be explicit and observable.

Minimum failure modes to handle:

* missing model artifact
* unreadable or malformed feature record
* scoring runtime error
* prediction write failure
* partial run completion

Handling rules:

* failures are logged with context
* batch job continues when safe to do so
* failures create explicit run status records
* no silent drops of records

---

## 6. Non-Goals

Phase 4 (MVP) explicitly excludes:

* real-time inference SLAs
* auto-scaling or distributed scoring
* canary deployments and traffic splitting
* automated retraining triggers
* monitoring dashboards

These are deferred until the batch serving foundation is stable.

---

## Summary

This document defines how the system will generate and store predictions as **versioned, immutable events** via **batch inference**, enabling monitoring, feedback capture, and future online serving without compromising traceability.
