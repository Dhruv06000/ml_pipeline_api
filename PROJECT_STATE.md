# Project State

> Current truth of the project. Long-term working rules live in `LEARNING_CONTEXT.md`.
> Last updated: 2026-09-30

---

## Project

Customer Churn Prediction: Production ML Pipeline, API, & Streamlit UI
(Python + SQL + FastAPI + Streamlit + Docker)

## Current Milestone

### Milestone 2: Re-scoping to a Real Churn Problem

Status: **In Progress**

Reason: The original plan used a mock `customers` table and a generic pipeline. It lacked a problem definition, EDA, baselines, and a proper evaluation plan. The roadmap has been revised (see Change Log).

---

## Problem Definition

Fields marked **TODO** are decisions I make myself, with mentor guidance, in F3. No modeling code until every TODO is filled.

- **Task:** Binary classification. Will a customer churn?
- **Dataset:** Telco Customer Churn. TODO: confirm source and version.
- **Target column:** TODO (expected: `Churn`, Yes/No encoded as 1/0)
- **Prediction moment:** TODO. What is known about the customer at prediction time?
- **Business action a prediction triggers:** TODO (for example, a retention offer)
- **Cost of false negative vs false positive:** TODO
- **Primary metric:** TODO (candidate: PR-AUC)
- **Success criterion:** TODO (for example, beats the logistic regression baseline by X on the primary metric)
- **Excluded columns:** `customerID` (identifier). TODO: others after leakage review.
- **Known data issues:** `TotalCharges` contains blank strings for customers with tenure 0.

---

## Planned Architecture & Pipeline Flow

```text
Database Layer (persistent SQLite file, via sqlite3)
   ├── raw_customers      (untouched load of the dataset)
   ├── clean view/query   (stateless cleaning only; filters documented)
   ├── predictions_log    (inputs, probability, label, threshold, model version)
   └── feedback           (rating, comment, link to prediction)
        │
        ├── (SQL extraction via load_data_to_df)
        │
Pandas DataFrame
        │
        ├── Train/test split (stratified, fixed seed, BEFORE any fitting)
        │
Scikit-Learn Pipeline
   ├── ColumnTransformer
   │     ├── numeric:      impute → scale (only if the model needs it)
   │     └── categorical:  impute → one-hot encode
   └── Classifier (baseline → final model)
        │
        ├── Serialized artifact: model_pipeline.joblib
        └── Metadata file (.json): metrics, feature list, threshold, model version, data version
        │
FastAPI Backend Application
   ├── Pydantic Schemas (Literal/enum categoricals; must match training columns)
   ├── REST Endpoints (POST /predict, GET /health, POST /feedback)
   │     └── /predict returns probability + label + threshold used
   ├── Model loaded once at startup
   └── Automated Unit & Integration Tests (pytest + httpx)
        │
Streamlit Frontend UI
   ├── Interactive Input Form & "Load Sample Data" Button
   ├── Prediction & Feature Importance Visualization
   └── User Feedback System (thumbs up/down & text comment) ──► saved to DB
        │
Docker Containerization & Cloud Deployment (Render / Hugging Face Spaces)
```

### SQL vs Python Division of Labor

- **SQL:** stateless work (filtering, joins, aggregations, type cleaning).
- **Python Pipeline:** anything learned from training data (imputation values, scaling statistics, category lists, model weights).

---

## Feature Roadmap (revisable, see Plan Change Rule)

Tests are written inside each feature, not in a separate phase.

- [x] **F1: Project Structure & Environment Setup**
  Directory layout, `requirements.txt` with locked dependencies, virtual environment, `.gitignore`.

- [x] **F2: SQL Layer v1 (mock data), SUPERSEDED by F4**
  `src/database.py` with `sqlite3`, `customers` table, seed data, `load_data_to_df`, and `tests/test_database.py`. Approach and tests are reusable; schema and seed data will be replaced.

- [ ] **F3: Problem Definition & Data Dictionary**
  Fill every TODO in Problem Definition. Write `docs/data_dictionary.md` (each column: meaning, type, allowed values, available at prediction time?, keep/exclude and why).

- [ ] **F4: Real Data Ingestion (rework of `database.py`)**
  Persistent DB file, raw table, cleaning query/view, documented filters, ingestion script, plus tests.

- [ ] **F5: EDA & Baselines**
  Class balance, missing values, distributions, majority-class baseline, plain logistic regression baseline. Notebook in `notebooks/eda.ipynb`.

- [ ] **F6: Preprocessing Pipeline**
  `ColumnTransformer` (numeric and categorical branches), custom transformers only where needed, plus tests.

- [ ] **F7: Training, Evaluation & Iteration**
  Stratified split, cross-validation, imbalance handling, model comparison, threshold selection, error analysis, artifact + metadata serialization with `joblib`, plus tests.

- [ ] **F8: FastAPI Service & Pydantic Schemas**
  `/health`, `/predict`, schemas matching training columns, model loaded at startup, error handling, plus tests (including schema-to-training-column consistency test).

- [ ] **F9: Prediction Logging & Feedback Storage**
  `predictions_log` and `feedback` tables, `/feedback` endpoint, plus tests.

- [ ] **F10: Streamlit Interactive UI**
  Input form, sample loading, prediction display, feature importance, feedback buttons.

- [ ] **F11: Docker Containerization & Persistence Decision**
  Dockerfile, layer caching, health check. Decide how the model artifact gets into the image (train at build vs download at startup) and where the DB lives when the deployed disk is ephemeral.

- [ ] **F12: Cloud Deployment, README & Model Card**
  Deploy to Hugging Face Spaces/Render, publish live URL, write `README.md` and `docs/model_card.md`.

- [ ] **Final: Coverage Hardening & Rebuild Exercise**
  Raise test coverage, write a personal ML project checklist, then rebuild a smaller version on a different dataset using only official documentation.

---

## Completed Work

### Milestone 1: Setup & Architecture Design

- Defined core architectural principles, SQL pipeline design, and user feedback mechanisms.
- Created `LEARNING_CONTEXT.md` for long-term project mentoring rules (revised 2026-09-30 with ML Engineering Rules).
- Created `PROJECT_STATE.md` to track progress and feature delivery.
- Completed F1: folder structure, `requirements.txt`, `.gitignore`, Python virtual environment.
- Completed F2: `src/database.py` with `sqlite3` schema initialization (`customers` table), seeded mock data, `load_data_to_df`, and passing unit tests (`tests/test_database.py`).
- Note: F2 used a mock `customers` table. Schema and seed data will be replaced in F4 once the real dataset is understood. `load_data_to_df` and the test approach are reusable.

---

## Open Decisions

- `/predict` input: raw feature values (chosen for v1) vs `customer_id` lookup (possible later).
- Feature importance shown in the UI: global importance vs per-prediction (SHAP).
- Primary model family: decided after baselines (F5) and comparison (F7).
- Feedback semantics: a thumbs up/down is opinion, not ground truth. Store it linked to the prediction record so real outcomes can be joined later.
- Persistence for deployed predictions/feedback: decided in F11.
- Whether to add a time-based dataset later to practice point-in-time leakage (Telco has no dates).

---

## Current Project Structure

```text
ml_pipeline_api/
├── data/                  # Local SQLite database files & raw datasets (gitignored)
├── models/                # Serialized artifacts (.joblib gitignored) + metadata (.json)
├── notebooks/
│   └── eda.ipynb          # Exploration & baselines (planned, F5)
├── docs/
│   ├── data_dictionary.md # Columns, leakage answers, documented filters (planned, F3)
│   ├── why_notebook.md    # Decision log (planned)
│   └── model_card.md      # Data, target, metrics vs baseline, limitations (planned, F12)
├── src/
│   ├── __init__.py
│   ├── database.py        # SQL queries & database connection management
│   ├── pipeline.py        # Feature engineering & ML pipeline construction
│   └── train.py           # Training script & artifact serialization
├── app/
│   ├── main.py            # FastAPI entrypoint & routes
│   ├── schemas.py         # Pydantic request/response validation schemas
│   └── config.py          # Environment configuration
├── ui/
│   └── app.py             # Streamlit interface & feedback component
├── tests/                 # Automated pytest suite (written with each feature)
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_pipeline.py
│   └── test_api.py
├── Dockerfile             # Container configuration
├── requirements.txt       # Project dependencies
├── LEARNING_CONTEXT.md    # Long-term mentoring rules
├── PROJECT_STATE.md       # Progress tracking (this file)
└── .gitignore
```

An ingestion script (for example `scripts/ingest_data.py`, or a function in `src/database.py`) will be added in F4.

---

## Status

- Environment Setup & Context Creation: Completed
- F1 (Project Structure & Setup): Completed
- F2 (SQL Layer v1, mock data): Completed, superseded by F4
- F3 (Problem Definition & Data Dictionary): **Next**
- F4 (Real Data Ingestion): Pending
- F5 (EDA & Baselines): Pending
- F6 (Preprocessing Pipeline): Pending
- F7 (Training, Evaluation & Iteration): Pending
- F8 (FastAPI Service): Pending
- F9 (Prediction Logging & Feedback): Pending
- F10 (Streamlit UI): Pending
- F11 (Docker & Persistence): Pending
- F12 (Deployment, README, Model Card): Pending

---

## Next Milestone

**F3: Problem Definition & Data Dictionary**

Goal: Fill every TODO in the Problem Definition section and write `docs/data_dictionary.md`. No modeling code until this is done.

---

## Change Log

- 2026-09-30: Re-scoped from a generic pipeline to churn classification. Reason: the original plan lacked a problem definition, EDA, baseline, and evaluation steps, and used mock data with no real signal. Roadmap expanded from 10 to 12 features plus a final hardening step; testing moved into each feature; F2 marked superseded by F4.
- 2026-09-30: `LEARNING_CONTEXT.md` updated with ML Engineering Rules, Workflow Rules, Why Notebook definition, and Plan Change Rule.