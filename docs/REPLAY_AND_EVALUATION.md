# Replay and Evaluation — Decision Plane

## Purpose

This document defines how **replay** and **evaluation** operate within **Decision Plane**.

It specifies:

* what replay means (and what it does not)
* how historical re-execution is performed safely
* how evaluation is derived without mutating history
* how comparison across versions is enabled
* how auditability is preserved under experimentation

Replay and evaluation exist to **understand behavior**, not to correct it.

---

## Core Principles

Replay and evaluation in Decision Plane obey the following principles:

* **History is immutable**
* **Re-execution is additive**
* **Evaluation is derived**
* **No retroactive correction**
* **No policy enforcement**
* **No hidden optimization**

If replay changes the past, it is invalid.

---

## Definition of Replay

In Decision Plane, **replay** is defined as:

> The deterministic re-execution of processing or prediction pipelines from immutable historical inputs, producing new runs and artifacts without modifying existing state.

Replay answers:

* “What would the system produce under different versions or parameters?”

Replay does **not** answer:

* “What should have happened?”

---

## What Can Be Replayed

Replay is allowed for:

### Processing Replay

* re-running processing pipelines
* using different processor versions
* using alternative configurations
* producing new derived artifacts and signals

---

### Prediction Replay

* re-running model inference
* using different model or feature versions
* generating new prediction runs
* emitting new signals

---

## What Cannot Be Replayed

Replay explicitly does **not** include:

* overwriting historical artifacts
* modifying prior signals
* retroactively changing lifecycle state
* “fixing” incorrect past outputs
* enforcing updated policies on historical data

Replay is **parallel**, not corrective.

---

## Replay Inputs

Every replay execution must reference:

* immutable raw document artifacts
* explicit processor or model version
* explicit configuration snapshot
* explicit replay intent metadata

Replay must not rely on:

* current system time
* mutable external services
* environment-dependent defaults

All replay inputs must be inspectable.

---

## Replay Outputs

Each replay produces:

* a new processing or prediction run
* new lineage records
* new derived artifacts
* new signals (if applicable)

All outputs are:

* append-only
* versioned
* historically traceable

No replay output replaces an existing artifact.

---

## Replay Lineage

Replay executions must be explicitly linked to:

* the original document
* the original execution (if applicable)
* the replay trigger metadata

This enables:

* side-by-side comparison
* audit traceability
* controlled experimentation

Replay lineage is part of the audit surface.

---

## Replay Isolation

Replay executions are isolated by construction:

* no shared mutable state
* no shared write paths
* no cascading effects

A replay failure must not affect:

* original executions
* other replays
* read models

---

## Definition of Evaluation

In Decision Plane, **evaluation** is defined as:

> A post-hoc analytical process that derives metrics from historical executions without mutating core state.

Evaluation answers:

* “How did the system behave over time?”
* “How do different versions compare?”

Evaluation does **not** answer:

* “What should be enforced?”
* “Which decision is correct?”

---

## Evaluation Scope

Evaluation may include:

* performance metrics (e.g. confusion matrices)
* stability metrics
* drift indicators
* cost or utility estimates (analytical only)
* comparison across versions or configurations

All evaluation outputs are:

* derived
* recomputable
* non-authoritative

---

## Evaluation Windows

Evaluations are persisted as **evaluation windows**.

Each window defines:

* time or document boundaries
* execution versions considered
* metric definitions
* evaluation configuration version

Evaluation windows are:

* additive
* immutable
* replaceable via recomputation

They never mutate core execution data.

---

## Relationship Between Replay and Evaluation

Replay and evaluation are **orthogonal but complementary**:

* replay produces new executions
* evaluation compares executions
* evaluation never triggers replay
* replay never enforces evaluation outcomes

No feedback loop is implicit.

---

## Prohibited Behaviors

The following are explicitly forbidden:

* replay-triggered state correction
* evaluation-driven enforcement
* automatic rollback based on metrics
* prioritization of documents via replay
* suppression of signals based on outcomes

Any such behavior violates system guarantees.

---

## Auditability Guarantees

Replay and evaluation must ensure:

* every replay is traceable
* every comparison is reproducible
* historical executions remain intact
* differences are explicit, not inferred

Auditability must not require reconstruction or log correlation.

---

## Evolution Rules

Allowed:

* new replay views
* new comparison dimensions
* additional evaluation metrics
* richer lineage visualization

Disallowed:

* mutating historical runs
* collapsing replay into correction
* embedding policy logic
* optimizing execution paths based on evaluation

---

## Final Statement

Replay and evaluation exist to **surface counterfactuals**, not to rewrite history.

If replay becomes correction, the system loses trust.
If evaluation becomes enforcement, the system loses neutrality.

Decision Plane remains valuable only as long as **the past is preserved and the present is inspectable**.
