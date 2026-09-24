# Rebuilding the Social Engine: The Silent Failure Situation
### Data Vortex A’26 — Round 4 Final Hybrid Evaluation

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise real-time observability portal tracking unlogged microservice degradation, infrastructure errors, and memory leaks discovered via multi-platform social sentiment shifts.

---

## ⚡ Overview & The Problem Statement
In distributed cloud-native microservice architectures, **"Silent Failures"** represent the most insidious class of operational degradation. When internal components collapse (e.g., database connection pool exhaustion, memory leak crash loops, thread-pool starvation), upstream defensive retry wrappers frequently catch errors and return `HTTP 200 OK` with empty `{}` payloads.

Because conventional Application Performance Monitoring (APM) dashboards remain **100% green**, the end-user social media stream becomes the **sole real-time telemetry channel**.

This repository reconstructs the complete end-to-end pipeline across four integrated rounds:
1. **Round 1 (SQL Engine):** Relational normalization in `social_engine.db` resolving sign corruption, 3-way NULL sentinels, and HTML injection.
2. **Round 2 (NLP Inference):** Sublinear TF-IDF vectorization with Calibrated Soft-Voting ensembles for sentiment and topic entity modeling.
3. **Round 3 (Stream Monitor):** Real-time multi-platform harvester (Reddit, X, News APIs) with UTC ISO-8601 normalization.
4. **Round 4 (Command Portal):** Production Streamlit & Plotly dual-axis interactive telemetry dashboard.

---

## 🚀 Quickstart: Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/<YOUR_USERNAME>/<REPO_NAME>.git
cd <REPO_NAME>
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit Dashboard
```bash
streamlit run app.py
```
*(Alternatively, execute `python app.py` directly; our built-in runner will automatically boot Streamlit in-process).*

---

## ☁️ Deploying to Streamlit Community Cloud

1. Push this repository to your **GitHub** account.
2. Log into [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **"New app"**.
4. Select your repository: `<YOUR_USERNAME>/<REPO_NAME>`.
5. Set **Main file path** to: `app.py`.
6. Click **"Deploy!"**.

---

## 📊 End-to-End Pipeline Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ ROUND 1: SQL Relational Ingestion & Base Anomaly Sanitizer (social_engine.db)         │
│  - Normalizes corrupted types (Negative likes → ABS(), 'NULL' strings → NaN)          │
│  - Eliminates HTML injection tags (<br>, <div>, &amp;) via regex cleaning engine      │
│  - Window Function anomaly filters: Suspicious Bot Shares (M5) & Outlier Volume (H5)   │
└────────────────────────────────────────┬───────────────────────────────────────────────┘
                                         │ Cleaned Ingestion Buffer
                                         ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ ROUND 2: Production Semantic Understanding Layer (NLP Model Artifacts)                 │
│  - Preprocessing: <USER>, <URL> token anonymization + HTML entity unescaping          │
│  - Feature Extraction: tfidf_vectorizer.pkl (sublinear TF, ngrams (1,2), 50k features)│
│  - Inference Models:                                                                   │
│      • sentiment_classifier_model.pkl (Soft-voting: LR + Calibrated SVC + MNB)       │
│      • topic_classifier_model.pkl (Soft-voting: LR + Calibrated SVC + GradBoost)      │
└────────────────────────────────────────┬───────────────────────────────────────────────┘
                                         │ Classified Semantic Vectors
                                         ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ ROUND 3: Real-Time Multi-Platform Telemetry Streamer (OSINT Live Monitor)              │
│  - Ingestion: X (Twitter API v2) + Reddit (/r/sysadmin, /r/devops) + News APIs         │
│  - Temporal Harmonization: UTC ISO-8601 normalization (temporal_parsing.py)           │
│  - Fingerprinting: Platform prefix + SHA-256 deduplication ID                         │
└────────────────────────────────────────┬───────────────────────────────────────────────┘
                                         │ Synchronized Time-Series Feed
                                         ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ ROUND 4: Executive Interactive Command Center (Streamlit + Plotly Engine)              │
│  - Dual-Axis Temporal Tracking Engine (Velocity vs Negative Polarity Shift)            │
│  - Real-Time Compound System Anomaly Score Index (88.6 / 100 Critical Risk)           │
│  - Multi-Platform Semantic Cluster Drilldown & Live Inference Playground               │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📑 Deliverable Artifacts

- **Executive Pitch PDF:** [`ROUND4_FINAL_TECHNICAL_REPORT.pdf`](ROUND4_FINAL_TECHNICAL_REPORT.pdf)
- **Live Streamlit App:** [`app.py`](app.py)
- **Dependencies:** [`requirements.txt`](requirements.txt)
- **Historical Dataset:** [`silent_failure_raw_dataset.csv`](silent_failure_raw_dataset.csv)
- **Model Bundle:** [`semantic_model_bundle.pkl`](semantic_model_bundle.pkl)
