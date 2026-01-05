# CI/CD and Release Model — Decision Plane

## Purpose

This document defines the **CI/CD and release discipline** of **Decision Plane**.

It specifies:

* how changes are validated
* how guarantees are protected over time
* how releases are versioned and promoted
* how regressions are detected and blocked
* how reproducibility is preserved across environments

CI/CD exists to **enforce architecture**, not to accelerate delivery at its expense.

---

## CI/CD Philosophy

Decision Plane CI/CD follows these principles:

* **Guarantees > velocity**
* **Determinism > convenience**
* **Contracts > implementations**
* **Regression prevention > feature throughput**
* **Reproducibility > optimization**

A change that passes CI is not “working”; it is **architecturally valid**.

---

## Change Classification

Every change must be classified explicitly:

### 1. Non-Breaking (v1.x)

* additive schema changes
* new inspection endpoints
* new derived read models
* new processing or signal types
* documentation updates

### 2. Breaking (v2.0+ required)

* violation of system guarantees
* mutation of historical data
* semantic changes to persisted fields
* write paths in inspection APIs
* policy or action semantics introduced
* change in determinism or replay behavior

Breaking changes **must not** be merged into v1.x.

---

## Branching Model

### Canonical Branches

* `main`
  Always reflects the latest **released, stable** version.

* `develop`
  Integration branch for the next v1.x release.

* `feature/*`
  Isolated, short-lived branches for specific changes.

No direct commits to `main`.

---

## Commit Discipline

Commits must be:

* atomic
* scoped
* reversible
* descriptive

Each commit must clearly state:

* what changed
* why it changed
* which guarantees it touches (if any)

Large, mixed-purpose commits are not acceptable.

---

## Continuous Integration Pipeline

Every pull request must pass the following stages.

---

### 1. Static Validation

Includes:

* formatting and linting
* schema validation
* contract schema checks
* forbidden keyword scanning (e.g. “approve”, “reject”, “trigger” in core code)

This stage prevents **semantic leakage**.

---

### 2. Unit and Property Tests

Tests must verify:

* deterministic behavior
* idempotent ingestion
* append-only semantics
* explicit state transitions
* immutability of historical records

Property-based tests are preferred where applicable.

---

### 3. Contract Tests

Contract tests assert:

* API schemas match documented contracts
* read-only guarantees are enforced
* versioned endpoints remain stable
* intentional 404 stubs behave as documented

If a contract breaks, CI fails.

---

### 4. Replay and Determinism Tests

Replay tests must verify:

* identical outputs for identical inputs
* new runs do not mutate old runs
* lineage completeness
* version isolation between runs

This stage protects **trust in replayability**.

---

### 5. Migration Safety Checks

If schema changes exist:

* migrations must be additive
* historical data must remain readable
* rollback paths must exist

Destructive migrations are forbidden in v1.x.

---

## Continuous Delivery

### Build Artifacts

All releases produce:

* versioned container images
* immutable build artifacts
* cryptographic hashes or digests

Artifacts must be reproducible from source.

---

### Environment Promotion

Typical environments:

* local
* staging
* production

Promotion rules:

* same artifact promoted across environments
* no environment-specific rebuilds
* configuration injected explicitly

Environment drift is not allowed.

---

## Release Versioning

### Semantic Versioning

Decision Plane uses semantic versioning:

```
MAJOR.MINOR.PATCH
```

* MAJOR — breaking architectural changes
* MINOR — additive, backward-compatible features
* PATCH — fixes with no semantic change

v1.x explicitly forbids breaking changes.

---

## Release Gates

A release may only be cut if:

* all CI stages pass
* documentation is updated
* guarantees remain satisfied
* no forbidden behaviors are introduced

Convenience, urgency, or performance gains do not override gates.

---

## Observability in CI/CD

CI/CD must surface:

* test coverage on guarantees
* replay determinism checks
* contract drift
* schema evolution history

Observability exists to detect **architectural decay early**.

---

## Prohibited CI/CD Behaviors

The following are explicitly forbidden:

* skipping tests to unblock merges
* environment-specific logic in core code
* conditional behavior based on deployment target
* hotfixes that bypass guarantees
* undocumented production changes

Any such behavior invalidates system trust.

---

## Evolution Rules

Allowed:

* new tests
* stricter validation
* additional gates
* richer contract enforcement

Disallowed:

* weakening guarantees
* relaxing determinism checks
* hiding failures
* bypassing CI for releases

CI/CD must become **stricter over time**, not looser.

---

## Final Statement

Decision Plane’s CI/CD pipeline is a **governance mechanism**, not a convenience layer.

If CI allows a change that violates determinism, auditability, replayability, or neutrality, then CI has failed—even if the system “works.”

The architecture is protected not by intention, but by enforcement.
