# Phase 1: EDA Report - Rebuilding the Social Engine

## 1. Data Profiling Summary

### Raw Data Overview

| Dataset | Rows | Columns | Duplicates |
|---------|------|---------|------------|
| Posts (Corrupted) | 12,360 | 8 | 360 |
| Users | 1,500 | 5 | 0 |

### Column-Level Quality Assessment (Posts)

| Column | True Nulls | 'NULL' Strings | Unique Values | Issue Type |
|--------|-----------|----------------|---------------|------------|
| post_id | 0 | 0 | 12,000 | 360 duplicate rows |
| user_id | 0 | 0 | 1,500 | All valid FK references |
| platform | 1,846 | 0 | 5 | ~15% missing platform |
| text_content | 1,746 | 24 | 10,225 | HTML artifacts, encoding errors |
| timestamp | 0 | 0 | 8,839 | 3 mixed formats |
| likes | 1,858 | 0 | 4,752 | 525 negative values |
| shares | 0 | 0 | 1,994 | Clean |
| comments | 0 | 0 | 1,001 | Clean |

### Users Table
- **1,500 unique users** across **33 locations** and **10 languages**
- Account creation dates span all of 2023
- Follower counts range from ~100 to ~50,000
- **No missing values, no duplicates** - clean reference data

---

## 2. Data Cleaning Transformations & Justifications

### 2.1 Duplicate Row Removal (360 rows)
**Action**: Dropped 360 exact duplicate rows from Posts table (kept first occurrence).
**Justification**: The corrupted dataset contained 360 fully duplicated rows (identical across all 8 columns). These represent data ingestion errors, not legitimate reposts. Keeping them would inflate engagement metrics.

### 2.2 'NULL' String Replacement (24 in text_content)
**Action**: Converted literal `"NULL"` strings to proper `NaN`.
**Justification**: The corrupted export used the string `"NULL"` as a sentinel value instead of proper null markers. 24 occurrences in `text_content` were converted to maintain consistent null semantics across the pipeline.

### 2.3 HTML & Encoding Artifact Removal
**Action**: Stripped `<br>`, `<div>`, `</div>` HTML tags, decoded `&amp;` entities, removed `Ã©` encoding artifacts.
**Justification**: The data contains injected HTML tags and UTF-8 mojibake (`Ã©` = mis-encoded `é`). These are data corruption tokens from a faulty export pipeline, not genuine user content. Removal preserves the actual text semantics.

### 2.4 Timestamp Format Unification
**Action**: Parsed three distinct timestamp formats into unified `datetime`:
- ISO 8601: `2024-05-05T05:52:34`
- DD-MM-YYYY: `25-09-2024`
- Unix epoch: `1722528840`

**Justification**: The system stored timestamps in multiple formats due to schema migration or multi-source ingestion. Unifying to datetime enables temporal analysis. Date range: **2024-05-01 to 2025-04-30** (12 months of data).

### 2.5 Negative Engagement Values (525 in likes)
**Action**: Took absolute value of 525 negative like counts.
**Justification**: Social media engagement metrics (likes, shares, comments) are inherently non-negative. Negative values (e.g., -4812, -3707) represent sign-corruption during data transfer. The absolute value recovers the most likely intended magnitude.

### 2.6 Platform Name Standardization
**Action**: Title-cased all platform names, normalized "Youtube" to "YouTube".
**Justification**: Ensures consistent grouping. Missing platforms (14.9%) are preserved as NaN since we cannot impute platform from content alone.

### 2.7 Feature Engineering
New derived columns created for downstream analysis:
- `hashtags`: Extracted from text_content using regex
- `brand_mentioned`: Identified from 10 known brands in the dataset
- `sentiment`: Rule-based classification (positive/negative/neutral) from keyword patterns
- `total_engagement`: likes + shares + comments
- `engagement_rate`: total_engagement / 3
- `post_date`, `post_hour`, `post_day_of_week`, `post_month`: Temporal decomposition

---

## 3. Core EDA Insights

### 3.1 Engagement Statistics

| Metric | Mean | Median | Std Dev | Min | Max |
|--------|------|--------|---------|-----|-----|
| Likes | 2,499 | 2,530 | 1,433 | 1 | 5,000 |
| Shares | 987 | 990 | 574 | 0 | 2,000 |
| Comments | 491 | 494 | 286 | 0 | 999 |
| Total Engagement | 3,631 | 3,640 | 1,557 | 17 | 7,920 |

> [!NOTE]
> Engagement follows a near-uniform distribution within bounded ranges, suggesting synthetic data generation with controlled parameters. Likes dominate total engagement (~69%).

### 3.2 Platform Dynamics

| Platform | Posts | % Share | Avg Engagement | Unique Users |
|----------|-------|---------|----------------|-------------|
| YouTube | 2,136 | 17.8% | 3,607 | 1,147 |
| Facebook | 2,135 | 17.8% | 3,660 | 1,173 |
| Twitter | 2,119 | 17.7% | 3,563 | 1,132 |
| Reddit | 2,086 | 17.4% | 3,639 | 1,132 |
| Instagram | 2,038 | 17.0% | 3,650 | 1,139 |
| Missing | 1,784 | 14.9% | 3,644 | 1,063 |

**Insight**: Posts are nearly uniformly distributed across all 5 platforms. Facebook and Instagram lead slightly in average engagement, but the difference is marginal (~3%). This suggests a platform-agnostic user base.

### 3.3 Temporal Patterns

**Monthly Volume**: Consistent posting volume (~920-1,010 posts/month) across the 12-month window, with no seasonal decline, indicating healthy platform retention.

**Day-of-Week**: Activity is evenly distributed across all 7 days (~1,700 posts/day), with no significant weekday vs. weekend skew.

**Peak Activity Hours**: Engagement peaks show no strong hourly pattern, with posts distributed across all 24 hours.

**Spike Days Detected** (>2 standard deviations above mean):
| Date | Posts | Significance |
|------|-------|-------------|
| 2024-06-16 | 54 | Highest single-day volume |
| 2024-05-30 | 51 | Early spike |
| 2024-08-14 | 50 | Mid-summer surge |
| 2025-01-25 | 49 | New Year period |
| 2025-02-19 | 48 | February activity |

### 3.4 Brand Mention Analysis

| Brand | Mentions | Avg Likes | Avg Shares | Avg Engagement | Unique Users |
|-------|----------|-----------|------------|----------------|-------------|
| Nike | 1,345 | 2,507 | 969 | 3,645 | 996 |
| Google | 1,334 | 2,498 | 979 | 3,602 | 990 |
| Samsung | 1,291 | 2,483 | 1,003 | 3,635 | 964 |
| Amazon | 1,279 | 2,535 | 971 | 3,612 | 966 |
| Apple | 1,268 | 2,519 | 977 | 3,652 | 960 |
| Pepsi | 1,261 | 2,486 | 1,006 | 3,664 | 956 |
| Microsoft | 1,241 | 2,479 | 991 | 3,596 | 939 |
| Toyota | 1,226 | 2,460 | 999 | 3,609 | 947 |
| Coca-Cola | 1,221 | 2,540 | 996 | 3,660 | 936 |
| Adidas | 1,197 | 2,486 | 1,005 | 3,626 | 931 |

**Insight**: Nike dominates brand mentions (1,345), but Coca-Cola and Pepsi lead in average engagement. All 10 brands have remarkably similar engagement profiles, suggesting uniform audience interest across brand categories.

### 3.5 Sentiment Distribution

| Sentiment | Posts | Avg Engagement |
|-----------|-------|----------------|
| Positive | 3,651 | 3,635 |
| Negative | 3,494 | 3,611 |
| Neutral | 4,855 | 3,643 |

**Insight**: Sentiment is roughly balanced with a slight positive skew. Engagement rates are virtually identical across sentiments, meaning negative content is NOT penalized by the engagement algorithm - a potential concern for content moderation.

### 3.6 User Segmentation

| Segment | Count | Description |
|---------|-------|-------------|
| Regular User | 1,010 | 4-14 posts, moderate engagement |
| High Engager | 419 | Avg engagement > 4,000 |
| Casual User | 46 | 1-3 posts total |
| Power User | 25 | Top 1% by post volume (15+ posts) |

- **Average posts per user**: 8.0 (median: 8.0)
- **Power users** (25 users) have avg engagement of 3,612 - in line with the population mean
- **Zero bot-like accounts** detected (no user has high frequency + low engagement)

### 3.7 Geographic Distribution

**Top cities by post volume**: Los Angeles (459), Munich (452), Shanghai (451), Barcelona (439)
**Highest engagement cities**: London (3,702), Osaka (3,700), Barcelona (3,692), Los Angeles (3,685)

**Language engagement ranking**: Arabic (ar) leads at 3,696 avg engagement, followed by Chinese (zh) at 3,677. Hindi trails at 3,497.

### 3.8 Correlation Analysis

| | Likes | Shares | Comments |
|---|-------|--------|----------|
| Likes | 1.000 | -0.001 | 0.010 |
| Shares | -0.001 | 1.000 | 0.024 |
| Comments | 0.010 | 0.024 | 1.000 |

**Key Finding**: Likes, shares, and comments are **completely uncorrelated** with each other (correlations near zero). This is unusual for real social media where these metrics typically co-vary. Follower count shows **no correlation** with engagement (-0.011), suggesting engagement is organic and not follower-driven.

### 3.9 Content Completeness

| Field | Completeness |
|-------|-------------|
| text_content | 85.3% |
| platform | 85.1% |
| likes | 84.9% |
| shares | 100% |
| comments | 100% |

- **239 posts** are missing BOTH text content and platform metadata simultaneously

---

## 4. Data Quality Assessment Summary

> [!IMPORTANT]
> The cleaned dataset contains **12,000 posts** from **1,500 users** spanning **May 2024 to April 2025**. After removing 360 duplicates, fixing 525 negative values, converting 24 NULL strings, and stripping HTML artifacts, the dataset is production-ready for Phase 2 SQL ingestion.

### Remaining Missing Data (by design - not imputable)
- **Platform** (14.9%): Cannot reliably impute posting platform from content
- **Text content** (14.3%): Posts may have been deleted or corrupted beyond recovery
- **Likes** (15.1%): Engagement data may not have been captured for all posts
- **Brand** (14.8%): Not all posts mention a brand - this is expected
