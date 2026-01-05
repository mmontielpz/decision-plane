# Processing Model — Decision Plane

## Purpose

This document defines the **processing execution model** of **Decision Plane**.

It specifies:

* How processing is initiated
* How execution is structured
* What processing is allowed to do
* What processing is explicitly forbidden to do
* How determinism, lineage, and replayability are preserved

The processing model describes **pure transformation**, not decision-making.

---

## Processing Model Philosophy

Processing in Decision Plane obeys the following invariants:

* Processing is **deterministic**
* Processing is **side-effect free**
* Processing is **versioned**
* Processing is **observable**
* Processing is **replayable**
* Processing never executes policy or action

Processing **transforms inputs into artifacts and signals**.
It never decides outcomes.

---

## Definition of Processing

In Decision Plane, **processing** is defined as:

> A deterministic transformation of persisted inputs into derived artifacts, accompanied by explicit lineage records.

Processing **does not**:

* branch on business intent
* optimize for outcomes
* mutate historical state
* trigger workflows
* decide what should happen next

---

## Processing Inputs

A processing run may consume:

* Immutable raw document artifacts
* Persisted metadata
* Explicit configuration objects
* Explicit processor version identifiers

Processing may **not** consume:

* External mutable state
* Current time as implicit input
* Non-versioned environment variables
* Policy definitions
* Thresholds tied to business outcomes

All inputs must be **persisted, versioned, and inspectable**.

---

## Processing Outputs

A processing run may produce:

* Derived document artifacts
* Structured intermediate representations
* Feature materializations
* Inspection signals
* Lineage records

Processing may **not** produce:

* Decisions
* Actions
* Notifications
* Workflow triggers
* Side effects outside persisted storage

All outputs must be **persisted explicitly**.

---

## Processing Runs

### Definition

A **processing run** represents a single execution of a processing pipeline over one or more documents.

Each run is recorded as a row in `processing_runs`.

---

### Required Properties

Each processing run must record:

* Unique run identifier
* Processor name and version
* Execution configuration reference
* Start timestamp
* Completion timestamp
* Final run status

Runs are:

* Append-only
* Immutable after completion
* Never overwritten

---

## Processing Steps

### Definition

A **processing step** represents a single, named transformation within a processing run.

Steps are recorded in `processing_steps`.

---

### Step Properties

Each step must record:

* Processing run identifier
* Document identifier
* Step name
* Step version (if applicable)
* Execution status (success, failure, skipped)
* Structured metadata
* Start and end timestamps

Steps must be recorded **even if they fail**.

---

### Step Semantics

Processing steps:

* Execute in a defined order
* Must be individually inspectable
* Must not hide failures
* Must not short-circuit lineage

Partial execution is valid and must be observable.

---

## Determinism Rules

Processing determinism is enforced as follows:

* All logic is versioned
* All inputs are persisted
* All randomness is disallowed unless explicitly seeded and recorded
* No implicit time dependence
* No dependency on external mutable services

Given identical inputs, configuration, and processor version, the system **must** produce identical outputs.

---

## Error Handling Model

Errors during processing:

* Are captured as structured step metadata
* Do not delete or overwrite prior artifacts
* Do not retroactively modify state
* Are visible through lineage inspection

Failures are **data**, not control flow.

---

## Lifecycle State Interaction

Processing is the **only mechanism** allowed to advance document lifecycle state.

Rules:

* State transitions must be explicit
* Each transition must reference a processing run
* Failed processing may update state to `failed`
* No implicit or inferred transitions are allowed

State transitions must never imply action or priority.

---

## Replay Model

Replay is defined as:

> Re-executing a processing pipeline from immutable raw inputs using a specified processor version and configuration.

Replay:

* Always creates a new processing run
* Always produces new lineage records
* Never mutates historical runs or artifacts
* May coexist with prior executions

Replay is **additive**, never corrective.

---

## Separation from Prediction

Processing and prediction are **distinct concerns**.

Processing may:

* Extract features
* Normalize data
* Validate structure
* Generate quality signals

Processing may **not**:

* Invoke models directly unless explicitly defined as a prediction phase
* Interpret model outputs
* Apply thresholds
* Produce decisions

Prediction is handled by a separate execution model.

---

## Prohibited Processing Behaviors

The following are explicitly forbidden:

* Conditional logic based on business meaning
* Priority assignment
* Review queue manipulation
* Policy evaluation
* Workflow orchestration
* External write-backs
* Self-triggering behavior

Any processing logic exhibiting these behaviors violates system boundaries.

---

## Evolution Rules

Allowed:

* Adding new processing steps
* Adding new processor versions
* Extending step metadata
* Introducing new derived artifacts

Disallowed:

* Changing semantics of existing steps
* Introducing implicit branching
* Coupling processing to downstream actions
* Making processing stateful across runs

---

## Final Statement

Processing in Decision Plane exists to make **transformation observable and replayable**.

If processing logic begins to:

* optimize outcomes
* infer intent
* hide failure
* or decide what should happen next

then the system has crossed from **decision inspection** into **decision execution**, and the change must be rejected.
