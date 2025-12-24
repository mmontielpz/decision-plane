# Risk-Aware ML System

## Overview

This repository implements an **end-to-end machine learning system** for **risk-aware decision making** under real-world constraints.

The focus of this project is the **design, implementation, and operation of an ML system**, not a single model.
It covers the lifecycle required to move from raw, unstructured data to deployable and observable ML-driven decisions in production-like environments.

The system is designed to be reusable across domains, with an initial concrete application in enterprise document workflows.

---

## Problem Statement

Organizations process large volumes of operational documents such as contracts, invoices, purchase orders, and compliance artifacts.

Operational issues rarely originate from obvious errors.
They typically arise from **latent and evolving risks**, including:

* subtle inconsistencies
* missing or ambiguous information
* anomalous patterns
* delayed detection
* gradual degradation of system behavior

Many ML approaches frame this as a static classification problem.

In practice, the challenge is **decision prioritization under uncertainty**, where:

* errors have asymmetric cost
* labels are noisy, incomplete, or delayed
* data distributions change over time
* latency and reliability matter
* business constraints shape acceptable outcomes

---

## Project Motivation

This project exists to reflect how ML systems are **built, deployed, and maintained** beyond experimentation.

It intentionally avoids:

* toy datasets
* notebook-only workflows
* accuracy-only evaluation
* model-centric design

Instead, it emphasizes:

* explicit system boundaries
* operational constraints
* failure handling
* reproducibility
* incremental iteration over time

---

## System Scope

The project covers the ML lifecycle as an integrated system:

1. **Continuous Data Collection**
   Handling evolving and heterogeneous inputs.

2. **Data Storage and Versioning**
   Separation of raw and processed data with traceability and reproducibility.

3. **Feature Engineering**
   Feature design guided by stability, cost, and downstream impact.

4. **Labeling Strategy**
   Managing noisy labels, delayed feedback, and human-in-the-loop processes.

5. **Model Training and Evaluation**
   Strong baselines with evaluation aligned to risk and cost, not accuracy alone.

6. **Deployment**
   Batch and online inference with explicit interfaces and failure handling.

7. **Containerization**
   Reproducible environments using Docker.

8. **CI/CD**
   Automated testing and controlled deployment workflows.

9. **Monitoring**
   Observability across data drift, prediction drift, latency, and system health.

10. **Iteration**
    Continuous improvement informed by monitoring and feedback.

---

## Initial Use Case: Document Risk Scoring

The first application of the system focuses on **risk scoring for enterprise documents**.

Rather than producing categorical labels, the system outputs **risk scores** that support downstream actions such as:

* prioritization
* escalation
* routing
* partial or automated handling

This use case was selected because it naturally involves:

* ambiguous or incomplete ground truth
* asymmetric cost of errors
* evolving data distributions
* operational constraints

The underlying architecture remains applicable beyond this domain.

---

## Evaluation Criteria

The system is evaluated using multiple signals rather than a single metric:

* decision quality under cost constraints
* robustness to data and concept drift
* operational stability
* reproducibility
* ease of iteration and change

Known limitations and failure modes are documented explicitly.

---

## Non-Goals

This project is not intended to be:

* a Kaggle-style experiment
* a tutorial or step-by-step guide
* a benchmark leaderboard
* a research paper or novel algorithm proposal

It is a practical, system-oriented implementation.

---

Perfecto.
No hay que reescribir todo el README. **Solo actualizar la sección `Status`** para reflejar el cierre formal de Phase 2, manteniendo coherencia con el resto del documento.

A continuación tienes **la versión final de la sección `Status`**, lista para **reemplazar únicamente esa sección**.

---

## Status

**Phase 1 completed**
Ingestion and raw storage foundation is implemented, including:

* FastAPI ingestion service
* explicit ingestion contracts
* idempotent metadata persistence using SQLite
* deterministic raw data storage
* structured logging
* explicit HTTP error handling
* integration tests validating ingestion behavior

**Phase 2 completed**
Processed storage and feature extraction foundation is implemented, including:

* explicit processed and feature data contracts
* batch processor for reproducible document processing
* versioned processed and feature artifacts
* persistent processing state tracking in SQLite
* idempotent reprocessing and backfill support
* integration tests validating batch processing behavior

The system now provides a **complete pre-model ML system foundation**, and is ready to evolve into **Phase 3: labeling strategy and model development**, driven by operational and business constraints rather than experimentation alone.
