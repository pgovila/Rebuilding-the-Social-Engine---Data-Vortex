# Data Vortex Competition — Round 1 Walkthrough

## Deliverables Summary

Both Phase 1 and Phase 2 have been fully executed with all outputs validated.

---

## Phase 1: Data Intake Pipeline & EDA

### Deliverables Produced

| Deliverable | File | Status |
|-------------|------|--------|
| Data Cleaning Script | [phase1_data_cleaning.py](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/phase1_data_cleaning.py) | Executed successfully |
| EDA Script | [phase1_eda.py](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/phase1_eda.py) | Executed successfully |
| Cleaned Posts CSV | [Social_Engine_Posts_Cleaned.csv](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Social_Engine_Posts_Cleaned.csv) | 12,000 rows x 17 cols |
| Cleaned Users CSV | [Social_Engine_Users_Cleaned.csv](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Social_Engine_Users_Cleaned.csv) | 1,500 rows x 5 cols |
| Merged Dataset | [Social_Engine_Merged_Cleaned.csv](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/Social_Engine_Merged_Cleaned.csv) | Posts + Users joined |
| EDA Report | [phase1_eda_report.md](file:///C:/Users/abc/.gemini/antigravity-ide/brain/f06d829a-ca85-4894-be47-97d23fbb10f6/phase1_eda_report.md) | Comprehensive analysis |

### Data Cleaning Summary

| Issue Found | Count | Resolution |
|-------------|-------|-----------|
| Duplicate post rows | 360 | Removed (kept first) |
| 'NULL' string literals | 24 | Converted to NaN |
| HTML artifacts (`<br>`, `<div>`, `&amp;`) | ~200+ posts | Stripped via regex |
| Encoding artifacts (`Ã©`) | ~50+ posts | Removed |
| Negative like values | 525 | Absolute value applied |
| Mixed timestamp formats (ISO/DD-MM-YYYY/Unix) | 12,000 | Unified to datetime |
| Missing platform metadata | 1,784 (14.9%) | Preserved as NaN |
| Missing text content | 1,711 (14.3%) | Preserved as NaN |
| Missing likes | 1,814 (15.1%) | Preserved as NaN |

### Key EDA Findings
- **12,000 posts** from **1,500 users** across **5 platforms** (May 2024 - Apr 2025)
- **Zero bot-like accounts** detected
- **Follower count shows no correlation with engagement** (r = -0.011)
- **Likes, shares, and comments are uncorrelated** (r ≈ 0)
- Top brands: Nike (1,345 mentions), Google (1,334), Samsung (1,291)
- 9 daily activity spikes detected (>2 std deviations)

---

## Phase 2: SQL Rebuild & Analytical Reasoning

### Deliverables Produced

| Deliverable | File | Status |
|-------------|------|--------|
| SQL Schema + Queries | [phase2_sql_queries.sql](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/phase2_sql_queries.sql) | 8 queries, all validated |
| SQL Validation Script | [phase2_validate.py](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/phase2_validate.py) | All queries pass |
| SQLite Database | [social_engine.db](file:///c:/Users/abc/Downloads/Unstop%20Competitions/Data%20Vortex/social_engine.db) | Ready for queries |
| Phase 2 Report | [phase2_report.md](file:///C:/Users/abc/.gemini/antigravity-ide/brain/f06d829a-ca85-4894-be47-97d23fbb10f6/phase2_report.md) | Schema docs + insights |

### SQL Queries Implemented

| # | Category | Query Purpose | Technique |
|---|----------|--------------|-----------|
| 1 | Trend Detection | Viral spike identification via 7-day rolling average | CTE + Window (ROWS BETWEEN) |
| 2 | Anomaly Discovery | Bot-like pattern detection with composite scoring | CTE + NTILE + Multi-signal scoring |
| 3 | Behavioral Grouping | User segmentation by engagement velocity quintiles | CTE + NTILE + JULIANDAY |
| 4 | Correlation Analysis | Platform × Brand × Sentiment engagement drivers | CTE + DENSE_RANK + PARTITION BY |
| 5 | Trend Detection | Monthly brand share-of-voice momentum tracking | CTE + LAG window function |
| 6 | Anomaly Discovery | Weekly engagement drop detection per platform | CTE + Rolling window + ISO week |
| 7 | Behavioral Grouping | Follower-engagement efficiency decile analysis | NTILE(10) + Ratio computation |
| 8 | Correlation Analysis | Optimal posting time discovery per platform | RANK + Two-dimensional GROUP BY |

### Key SQL Insights
- **No bots detected** across 4 independent detection signals
- **Low-follower users** (Decile 1) have **16.7x higher engagement efficiency** than top-follower users
- **Instagram + Coca-Cola + neutral** content = highest engagement combination (4,132 avg)
- **September Week 35** saw simultaneous engagement drops across multiple platforms
- All brands show oscillating market share with no sustained momentum

---

## Validation Results
- Phase 1 cleaning script: Exit code 0
- Phase 1 EDA script: Exit code 0
- Phase 2 SQL validation: All 8 queries returned valid results
- All CSV exports verified and loadable
