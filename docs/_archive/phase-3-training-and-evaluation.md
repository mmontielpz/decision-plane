# Phase 3 — Training and Evaluation Design

## 1. Objective

The objective of Phase 3 training is to produce **baseline predictive models** that support risk-aware decision making under uncertainty.

The goal is not model optimality, but **reliable and interpretable decision signals** aligned with business cost and operational constraints.

---

## 2. Prediction Target

The system predicts **risk**, not absolute correctness.

Primary prediction targets include:

* probability of downstream escalation
* likelihood of human intervention
* expected cost-weighted error

Predictions are used for **ranking and threshold-based decisions**, not categorical classification.

---

## 3. Training Data Composition

Training datasets are constructed by joining:

* feature records (Phase 2)
* label signals (Phase 3.3)

Constraints:

* labels may be missing or delayed
* features may be incomplete
* not all ingested documents are eligible for training

Training datasets are versioned and immutable once materialized.

---

## 4. Temporal Splitting Strategy

Training and evaluation are separated **by time**, not randomly.

Minimum split strategy:

* training window: historical period
* evaluation window: subsequent period

This prevents:

* label leakage
* optimistic performance estimates
* temporal overfitting

---

## 5. Baseline Models

Phase 3 focuses on simple, interpretable baselines:

* logistic regression
* linear models
* shallow tree-based models

Rationale:

* faster iteration
* easier failure analysis
* robustness to noisy labels
* alignment with decision-making needs

Complex models are deferred to later phases.

---

## 6. Evaluation Metrics

### 6.1 Decision-Oriented Metrics

Primary metrics include:

* recall at top-K
* precision at operational thresholds
* cost-weighted error

These metrics reflect **real decision impact**.

---

### 6.2 Stability Metrics

Models are evaluated for:

* performance consistency across time slices
* sensitivity to label noise
* degradation under partial feature availability

Unstable models are rejected regardless of average performance.

---

## 7. Offline Evaluation Procedure

Each training run produces:

* model artifact
* training dataset reference
* evaluation dataset reference
* metric report
* known limitations

Evaluation results are stored and auditable.

---

## 8. Acceptance Criteria

A model is accepted if:

* it outperforms a trivial baseline
* it improves decision prioritization
* it exhibits stable behavior across time
* its failure modes are understood

Performance gains without stability are insufficient.

---

## 9. Failure Modes

Known failure modes include:

* overfitting to sparse labels
* temporal leakage
* instability across document sources
* excessive sensitivity to noise

Failure modes are documented explicitly.

---

## 10. Non-Goals

Phase 3 explicitly excludes:

* hyperparameter optimization
* ensemble models
* real-time serving
* automated retraining
* production SLAs

These are deferred to later phases.

---

## Summary

This document defines **how models are trained and evaluated**, not which model is “best”.

By enforcing temporal splits, cost-aware metrics, and stability criteria, the system ensures that modeling efforts translate into **useful and trustworthy decisions**.
