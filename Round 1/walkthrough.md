# Walkthrough: Data Vortex Competition — Round 1

> **Competition**: Data Vortex, Aaruush '26
> **Theme**: Rebuilding the Social Engine
> **Phases Completed**: Phase 1 (Data Intake & EDA) + Phase 2 (SQL Rebuild & Analytical Reasoning)

---

## Phase 1: Data Intake Pipeline & Exploratory Data Analysis

### 1.1 Data Cleaning ([`phase1_data_cleaning.py`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Phase_1/phase1_data_cleaning.py))

**Input**: Raw corrupted CSVs (`Social_Engine_Posts_Corrupted.csv`, `Social_Engine_Users.csv`)
**Output**: Cleaned CSVs + merged dataset + SQLite database

| Transformation | Records Affected | Action Taken |
|---------------|-----------------|--------------|
| Duplicate removal | 360 rows | Dropped by `post_id` (kept first) |
| Negative engagement values | 525 instances | Converted to absolute values |
| Timestamp unification | All 12,000 rows | Parsed mixed formats into ISO 8601 |
| HTML tag stripping | ~1,004 posts | Regex removal of `<br>`, `<div>`, `</div>` |
| HTML entity decoding | ~500 posts | Decoded `&amp;`, `&lt;`, `&gt;` to plain chars |
| Text 'NULL' sentinels | ~24 posts | Converted literal 'NULL' strings to NaN |

**Final cleaned dataset**: 12,000 posts, 1,500 users

### 1.2 Exploratory Data Analysis ([`phase1_eda.py`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Phase_1/phase1_eda.py))

Performed 12-section behavioral analysis (Sections 2.1–2.12):

| Section | Key Finding |
|---------|-------------|
| 2.1 Dataset Overview | 12,000 posts / 1,500 users / 8.0 posts per user mean |
| 2.2 Engagement Stats | Likes mean 2,491.9 / Shares mean 1,007.2 / Comments mean 504.3 |
| 2.3 Platform Analysis | Instagram leads avg engagement (3,669.4); 1,784 posts missing platform |
| 2.4 Temporal Patterns | Stable monthly volume (~920–1,038); Wednesday highest engagement day |
| 2.5 Brand Mentions | Adidas most mentioned (1,070); Amazon highest engagement (3,713.1) |
| 2.6 Sentiment | Negative posts outperform positive by ~2% in engagement |
| 2.7 User Segments | 1,010 Regular / 419 High Engager / 46 Casual / 25 Power User / 0 Bots |
| 2.8 Geography | Los Angeles top by volume (459); Arabic leads engagement (3,696.4) |
| 2.9 Hashtags | 29 unique; #Fitness (753) and #Reviews (752) most used |
| 2.10 Anomalies | 0 IQR outliers; 9 spike days (max 54 posts on 2024-06-16) |
| 2.11 Correlations | Likes/Shares/Comments uncorrelated; Follower-Engagement r = -0.011 |
| 2.12 Completeness | ~85% completeness for text/platform/likes; 239 posts missing both |

### Phase 1 Deliverables

| File | Location |
|------|----------|
| Cleaning script | [`phase1_data_cleaning.py`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Phase_1/phase1_data_cleaning.py) |
| EDA script | [`phase1_eda.py`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Phase_1/phase1_eda.py) |
| EDA report | [`phase1_eda_report.md`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Phase_1/phase1_eda_report.md) |
| EDA report (PDF) | [`phase1_eda_report.pdf`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Phase_1/phase1_eda_report.pdf) |
| EDA script output | [`phase1_eda_report_pyfile_result`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Phase_1/phase1_eda_report_pyfile_result) |
| Cleaned posts CSV | [`Social_Engine_Posts_Cleaned.csv`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Phase_1/Social_Engine_Posts_Cleaned.csv) |
| Cleaned users CSV | [`Social_Engine_Users_Cleaned.csv`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Phase_1/Social_Engine_Users_Cleaned.csv) |
| Merged dataset | [`Social_Engine_Merged_Cleaned.csv`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Phase_1/Social_Engine_Merged_Cleaned.csv) |

---

## Phase 2: SQL Rebuild & Analytical Reasoning

### 2.1 Question Selection

| Tier | ID | Question | Approach |
|------|----|----------|----------|
| **Easy** | E2 | Most Engaged Posts | Top 10 by likes+shares+comments; NULL-likes excluded |
| **Medium** | M5 | Detect Suspicious Engagement | Posts where shares > likes+comments; top 20 by shares |
| **Hard** | H5 | Identify Data Anomalies | Negative likes, missing platforms, missing text, HTML artifacts |

### 2.2 Execution Pipeline

The execution script ([`phase2_execute.py`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/phase2_execute.py)) performs the following:

```
1. Load cleaned CSVs into SQLite (posts, users tables)
2. Load raw corrupted CSV into SQLite (posts_raw table — for H5)
3. Execute E2 query → Top 10 most engaged posts
4. Execute M5 query → Top 20 suspicious share-dominant posts
5. Execute H5 query → Anomaly scan across 4 corruption categories
6. Execute H5 summary → Aggregate anomaly counts
7. Output all results to console
```

**Validation**: All 3 queries executed successfully with exit code 0. Full output captured in [`phase2_output.txt`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/phase2_output.txt).

### 2.3 Key Results Summary

| Query | Critical Finding |
|-------|-----------------|
| **E2** | Top post: 7,893 engagement (Instagram, Coca-Cola, Dubai). Instagram holds 3 of top 10. Mid-tier followers (13K–50K) dominate — follower count is irrelevant to engagement. |
| **M5** | **1,209 suspicious posts** (10.1%) where shares > likes+comments. Most extreme: 81.0% share-dominated. Geographic clustering in Mexico City (3x) and Shanghai (3x). 25% of top-20 have NULL platforms — potential API bot vector. |
| **H5** | **5,121 anomalous records** (41.4% corruption rate): 1,846 missing platforms, 1,746 missing text, 1,004 HTML contamination, 525 negative likes. All remediable. The consistent ~15% missing rate across 3 fields points to a single batch-processing failure. |

### 2.4 SQL Techniques Used

| Technique | Where Used | Purpose |
|-----------|-----------|---------|
| Common Table Expressions (CTEs) | All 3 queries | Pipeline clarity, pre-filtering before ranking |
| `DENSE_RANK()` | E2 | Fair tie-handling for engagement leaderboard |
| `ROW_NUMBER()` | M5, H5 | Sequential ranking and per-category sampling |
| `PERCENT_RANK()` | M5 | Anomaly extremity percentile |
| `COUNT(*) OVER (PARTITION BY ...)` | H5 | Per-category totals alongside sample rows |
| `UNION ALL` | H5 | Multi-category anomaly consolidation (preserves overlaps) |
| `NULLIF()` | M5 | Division-by-zero guard in ratio computation |
| `CAST()` / `SUBSTR()` | All | Type safety and text preview truncation |

### Phase 2 Deliverables (4 Separate Files)

| Deliverable | File | Contents |
|-------------|------|----------|
| **D1: SQL Queries** | [`Deliverable_1_SQL_Queries.md`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Deliverable_1_SQL_Queries.md) | Production SQL for E2, M5, H5 with full inline documentation |
| **D2: Results Matrix** | [`Deliverable_2_Results_Matrix.md`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Deliverable_2_Results_Matrix.md) | Tabular output layouts with column definitions |
| **D3: Approach & Logic** | [`Deliverable_3_Approach_Logic.md`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Deliverable_3_Approach_Logic.md) | Architecture diagrams, performance strategies, NULL handling |
| **D4: Insight Report** | [`Deliverable_4_Insight_Report.md`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Deliverable_4_Insight_Report.md) | User core analysis, bot patterns, data integrity audit |

### Supporting Files

| File | Purpose |
|------|---------|
| [`phase2_sql_queries.sql`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/phase2_sql_queries.sql) | Standalone SQL file (all 3 queries + summary aggregation) |
| [`phase2_execute.py`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/phase2_execute.py) | Python execution script (loads data, runs queries, outputs results) |
| [`phase2_output.txt`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/phase2_output.txt) | Raw query execution output log |
| [`social_engine.db`](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/social_engine.db) | SQLite database with posts, users, posts_raw tables |

---

## Verification

| Check | Status | Detail |
|-------|--------|--------|
| Phase 1 cleaning script runs | **PASS** | Produces 12,000-row cleaned CSV |
| Phase 1 EDA script runs | **PASS** | 12 sections, all values match report |
| Phase 2 E2 query | **PASS** | Returns 10 rows, correct sort order |
| Phase 2 M5 query | **PASS** | Returns 20 rows, 1,209 total flagged |
| Phase 2 H5 query | **PASS** | Returns 20 rows (5 per category), 5,121 total anomalies |
| Phase 2 execution script | **PASS** | Exit code 0, full output in phase2_output.txt |
| EDA report synced with script | **PASS** | All values match phase1_eda.py output |
| 4 deliverables in separate files | **PASS** | D1–D4 in Data Vortex folder |
