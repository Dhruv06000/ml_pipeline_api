# Project State

## Project

Production ML Pipeline, API, & Streamlit UI (Python + SQL + FastAPI + Streamlit + Docker)

## Current Milestone

### Milestone 1 — Setup & Project Scaffolding

Status: **In Progress**

---

## Planned Architecture & Pipeline Flow

```text
Database Layer (SQLite / PostgreSQL via SQLAlchemy)
        │
        ├── (SQL Extraction & Feature Filtering Query)
        │
Python Data Pipeline (Pandas / NumPy)
        │
        ├── (Fit/Transform)
        │
Scikit-Learn ML Pipeline (Scaler + Imputer + Model)
        │
        ├── (Serialized Artifact: model_pipeline.joblib)
        │
FastAPI Backend Application
   ├── Pydantic Schemas (Input Validation / Output Formatting)
   ├── REST Endpoints (POST /predict, GET /health, POST /feedback)
   └── Automated Unit & Integration Tests (pytest + httpx)
        │
Streamlit Frontend UI
   ├── Interactive Input Form & "Load Sample Data" Button
   ├── Prediction & Feature Importance Visualization
   └── User Feedback System (👍 / 👎 & Text Comment) ──► Saved back to DB
        │
Docker Containerization & Cloud Deployment (Render / Hugging Face Spaces)
```

## Feature Roadmap (FIXED 10-STEP BOUNDARY)
- [x] Feature 1: Project Structure & Environment Setup

Setup directory layout, requirements.txt with locked dependencies, virtual environment, and .gitignore.

- [ ] Feature 2: SQL Database Setup & Ingestion Layer

Design SQLite/SQLAlchemy database schemas, seed initial data, and write SQL extraction queries for feature filtering.

- [ ] Feature 3: Scikit-Learn Pipeline & Feature Engineering

Construct custom transformers and encapsulate scaling, encoding, and model fitting inside a Scikit-Learn Pipeline.

- [ ] Feature 4: Model Training, Evaluation, & Serialization

Train classification/regression model, evaluate metrics, and serialize artifact using joblib.

- [ ] Feature 5: FastAPI Service & Pydantic Schema Validation

Develop REST endpoints (/health, /predict), Pydantic validation schemas, and database connection logic.

- [ ] Feature 6: User Feedback & Feedback Storage Layer

Create a /feedback endpoint and SQL schema to store user feedback (rating, comment, input snapshot).

- [ ] Feature 7: Streamlit Interactive UI & Feedback Visualizer

Build a clean Streamlit interface with sample input pre-loading, prediction visualizer, and feedback buttons.

- [ ] Feature 8: Automated Testing Suite (pytest)

Write unit tests for SQL queries, pipeline transformers, API endpoints, and feedback collection.

- [ ] Feature 9: Docker Containerization

Create Dockerfile, build multi-stage image, test local container execution, and verify health checks.

- [ ] Feature 10: Cloud Deployment & LinkedIn Showcase

Deploy Docker container to Hugging Face Spaces/Render, publish live URL, and write an executive GitHub README.md.

## Completed Work

Milestone 1 — Setup & Architecture Design

- Defined core architectural principles, SQL pipeline design, and user feedback mechanisms.

- Created LEARNING_CONTEXT.md for long-term project mentoring rules.

- Created PROJECT_STATE.md to track progress and feature delivery.

- Completed Feature 1: Folder structure, requirements.txt, .gitignore, and Python virtual environment setup.

## Current Project Structure
```
ml_pipeline_api/
├── data/                  # Local SQLite database files & raw datasets (gitignored)
├── models/                # Serialized model artifacts (.joblib)
├── src/
│   ├── database.py        # SQL queries & database connection management
│   ├── pipeline.py        # Feature engineering & ML pipeline construction
│   └── train.py           # Training script & artifact serialization
├── app/
│   ├── main.py            # FastAPI entrypoint & routes
│   ├── schemas.py         # Pydantic request/response validation schemas
│   └── config.py         # Environment configurations
├── ui/
│   └── app.py             # Streamlit user interface & feedback component
├── tests/                 # Automated pytest suite
│   ├── test_database.py
│   ├── test_pipeline.py
│   └── test_api.py
├── Dockerfile             # Container configuration
├── requirements.txt       # Project dependencies
├── LEARNING_CONTEXT.md    # Long-term mentoring rules
├── PROJECT_STATE.md       # Progress tracking
└── .gitignore
```
## Status

- Environment Setup & Context Creation: Completed

- Feature 1 (Project Structure & Setup): Completed

- Feature 2 (SQL Database & Ingestion): In Progress

- ML Pipeline Construction: Pending

- FastAPI Serving Layer: Pending

- Streamlit Frontend UI: Pending

- Containerization & Deployment: Pending

## Next Milestone

Feature 2 — SQL Database Setup & Ingestion Layer

Goal: Create an SQLite database using SQLAlchemy, write SQL schemas to hold raw feature data, seed sample records, and write Python functions executing SQL queries to load data into Pandas DataFrames.