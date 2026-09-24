"""
===============================================================================
PHASE 2: SQL REBUILD & ANALYTICAL REASONING
Data Vortex Competition - Round 1, Phase 2
===============================================================================
Selected Questions:
  E2 - Most Engaged Posts (EASY)
  M5 - Detect Suspicious Engagement (MEDIUM)
  H5 - Identify Data Anomalies (HARD)
===============================================================================
This script:
  1. Loads both raw corrupted AND cleaned data into SQLite
  2. Runs all 3 SQL queries against the appropriate tables
  3. Outputs formatted results for all deliverables
===============================================================================
"""

import sqlite3
import pandas as pd
import numpy as np
import re

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 60)

# ===== DATABASE SETUP =====

conn = sqlite3.connect(':memory:')  # Fresh in-memory DB

# Load CLEANED data into main tables
posts_clean = pd.read_csv("Phase_1/Social_Engine_Posts_Cleaned.csv")
users_clean = pd.read_csv("Phase_1/Social_Engine_Users_Cleaned.csv")

# Load RAW CORRUPTED data for H5 anomaly detection
posts_raw = pd.read_csv(
    "Phase_1/Social_Engine_Posts_Corrupted.csv",
    engine="python",
    on_bad_lines="warn",
    dtype=str
)

# Write to SQLite tables
users_clean.to_sql("users", conn, if_exists="replace", index=False)
posts_clean.to_sql("posts", conn, if_exists="replace", index=False)
posts_raw.to_sql("posts_raw", conn, if_exists="replace", index=False)

print("=" * 80)
print("PHASE 2: SQL ANALYTICAL QUERIES - EXECUTION RESULTS")
print("=" * 80)

# ===================================================================
# E2: MOST ENGAGED POSTS (EASY)
# Find top 10 posts based on likes + shares + comments.
# Ignore posts with missing (NULL) likes.
# ===================================================================

E2_SQL = """
-- =====================================================================
-- E2: MOST ENGAGED POSTS
-- =====================================================================
-- GOAL: Identify the top 10 most engaged posts by total engagement
--        score (likes + shares + comments). Posts with NULL likes are
--        excluded since their engagement score is indeterminate.
--
-- TECHNIQUE: Filtered aggregation with ORDER BY DESC + LIMIT
-- ANSI COMPLIANCE: Standard SQL, no vendor-specific extensions
-- =====================================================================

WITH engagement_scored AS (
    -- Step 1: Compute total engagement for each post,
    --         filtering out records where likes data is missing.
    SELECT
        p.post_id,
        p.user_id,
        p.platform,
        SUBSTR(p.text_content, 1, 80)       AS text_preview,
        CAST(p.likes AS INTEGER)             AS likes,
        p.shares,
        p.comments,
        -- Core engagement formula: sum of all three interaction metrics
        (CAST(p.likes AS INTEGER) + p.shares + p.comments)
                                             AS total_engagement,
        u.location,
        u.language,
        u.follower_count
    FROM posts p
    JOIN users u ON p.user_id = u.user_id
    WHERE p.likes IS NOT NULL  -- Exclude posts with missing likes
),
ranked_posts AS (
    -- Step 2: Rank posts by total engagement using a window function.
    --         DENSE_RANK ensures tied engagement scores share the same rank.
    SELECT
        *,
        DENSE_RANK() OVER (
            ORDER BY total_engagement DESC
        ) AS engagement_rank
    FROM engagement_scored
)
-- Step 3: Return only the top 10 most engaged posts.
SELECT
    engagement_rank,
    post_id,
    user_id,
    platform,
    text_preview,
    likes,
    shares,
    comments,
    total_engagement,
    location,
    follower_count
FROM ranked_posts
WHERE engagement_rank <= 10
ORDER BY engagement_rank ASC, total_engagement DESC;
"""

print("\n" + "-" * 80)
print("  E2: MOST ENGAGED POSTS (Top 10)")
print("-" * 80)
e2_result = pd.read_sql(E2_SQL, conn)
print(e2_result.to_string(index=False))
print(f"\nRows returned: {len(e2_result)}")


# ===================================================================
# M5: DETECT SUSPICIOUS ENGAGEMENT (MEDIUM)
# Find posts where shares > likes + comments combined.
# Return top 20 sorted by shares descending.
# ===================================================================

M5_SQL = """
-- =====================================================================
-- M5: DETECT SUSPICIOUS ENGAGEMENT
-- =====================================================================
-- GOAL: Flag posts exhibiting suspicious engagement patterns where
--        shares exceed the combined total of likes and comments.
--        This is a classic bot/manipulation indicator: organic posts
--        rarely have more shares than likes+comments combined.
--
-- TECHNIQUE: CTE with computed inequality filter + ratio analysis
-- WINDOW FUNCTION: PERCENT_RANK to show how extreme each case is
-- =====================================================================

WITH suspicious_posts AS (
    -- Step 1: Identify posts where shares exceed likes + comments.
    --         Only consider posts with non-null likes for fair comparison.
    SELECT
        p.post_id,
        p.user_id,
        p.platform,
        SUBSTR(p.text_content, 1, 60)       AS text_preview,
        CAST(p.likes AS INTEGER)             AS likes,
        p.shares,
        p.comments,
        (CAST(p.likes AS INTEGER) + p.comments)
                                             AS likes_plus_comments,
        -- Share surplus: how much shares exceed likes+comments
        (p.shares - (CAST(p.likes AS INTEGER) + p.comments))
                                             AS share_surplus,
        -- Share-to-engagement ratio: proportion of total coming from shares
        ROUND(
            CAST(p.shares AS REAL) /
            NULLIF(CAST(p.likes AS INTEGER) + p.shares + p.comments, 0) * 100,
            1
        )                                    AS share_pct_of_total,
        u.location,
        u.follower_count
    FROM posts p
    JOIN users u ON p.user_id = u.user_id
    WHERE p.likes IS NOT NULL
      AND p.shares > (CAST(p.likes AS INTEGER) + p.comments)
),
ranked_suspicious AS (
    -- Step 2: Rank suspicious posts by share volume and compute
    --         percentile to measure how extreme the anomaly is.
    SELECT
        *,
        ROW_NUMBER() OVER (
            ORDER BY shares DESC
        )                                    AS suspicion_rank,
        ROUND(
            PERCENT_RANK() OVER (
                ORDER BY share_surplus ASC
            ) * 100, 1
        )                                    AS surplus_percentile
    FROM suspicious_posts
)
-- Step 3: Return the top 20 most suspicious posts.
SELECT
    suspicion_rank,
    post_id,
    user_id,
    platform,
    text_preview,
    likes,
    shares,
    comments,
    likes_plus_comments,
    share_surplus,
    share_pct_of_total,
    location,
    follower_count
FROM ranked_suspicious
WHERE suspicion_rank <= 20
ORDER BY suspicion_rank ASC;
"""

print("\n" + "-" * 80)
print("  M5: DETECT SUSPICIOUS ENGAGEMENT (Top 20)")
print("-" * 80)
m5_result = pd.read_sql(M5_SQL, conn)
print(m5_result.to_string(index=False))
print(f"\nRows returned: {len(m5_result)}")
print(f"Total suspicious posts (shares > likes+comments): "
      f"{pd.read_sql('SELECT COUNT(*) as c FROM posts WHERE likes IS NOT NULL AND shares > (CAST(likes AS INTEGER) + comments)', conn)['c'][0]}")


# ===================================================================
# H5: IDENTIFY DATA ANOMALIES (HARD)
# Identify corrupted records matching:
#   - Negative likes
#   - Missing platforms
#   - Missing text_content
#   - Text containing HTML entities/tags
# Run against RAW corrupted data to find all anomaly types.
# ===================================================================

H5_SQL = """
-- =====================================================================
-- H5: IDENTIFY DATA ANOMALIES
-- =====================================================================
-- GOAL: Perform a comprehensive data integrity audit by identifying
--        all corrupted records across four anomaly categories:
--        1. Negative likes (sign corruption in numeric fields)
--        2. Missing platform metadata (NULL or empty)
--        3. Missing text content (NULL or empty or literal 'NULL')
--        4. HTML contamination (tags like <br>, <div> or entities
--           like &amp; embedded in text fields)
--
-- TECHNIQUE: UNION ALL of four independent anomaly scans from the
--            raw corrupted data, each tagged with its anomaly type.
--            This enables both per-category and aggregate analysis.
-- WINDOW FUNCTION: COUNT OVER() for running anomaly totals per type.
-- =====================================================================

WITH anomaly_scan AS (
    -- Category 1: NEGATIVE LIKES
    -- Engagement metrics should never be negative. Negative values
    -- indicate sign-corruption during data transfer or ETL failure.
    SELECT
        post_id,
        user_id,
        platform,
        SUBSTR(text_content, 1, 50)          AS text_preview,
        likes                                AS flagged_value,
        'NEGATIVE_LIKES'                     AS anomaly_type,
        'Engagement metric has impossible negative value'
                                             AS anomaly_description
    FROM posts_raw
    WHERE CAST(likes AS REAL) < 0

    UNION ALL

    -- Category 2: MISSING PLATFORM
    -- Platform field is NULL, empty, or contains the literal 'NULL'.
    -- These records cannot be attributed to any social platform.
    SELECT
        post_id,
        user_id,
        platform,
        SUBSTR(text_content, 1, 50)          AS text_preview,
        platform                             AS flagged_value,
        'MISSING_PLATFORM'                   AS anomaly_type,
        'Platform metadata is absent or null-string'
                                             AS anomaly_description
    FROM posts_raw
    WHERE platform IS NULL
       OR TRIM(platform) = ''
       OR TRIM(UPPER(platform)) = 'NULL'

    UNION ALL

    -- Category 3: MISSING TEXT CONTENT
    -- Text content is NULL, empty, or the literal string 'NULL'.
    -- These represent deleted or corrupted post bodies.
    SELECT
        post_id,
        user_id,
        platform,
        SUBSTR(text_content, 1, 50)          AS text_preview,
        CASE
            WHEN text_content IS NULL THEN '<NULL>'
            WHEN TRIM(text_content) = '' THEN '<EMPTY>'
            ELSE 'NULL-string'
        END                                  AS flagged_value,
        'MISSING_TEXT'                       AS anomaly_type,
        'Post body is absent, empty, or null-string'
                                             AS anomaly_description
    FROM posts_raw
    WHERE text_content IS NULL
       OR TRIM(text_content) = ''
       OR TRIM(UPPER(text_content)) = 'NULL'

    UNION ALL

    -- Category 4: HTML CONTAMINATION
    -- Text contains raw HTML tags (<br>, <div>, </div>) or
    -- unescaped HTML entities (&amp;, &lt;, &gt;).
    -- These are injection artifacts from a faulty export pipeline.
    SELECT
        post_id,
        user_id,
        platform,
        SUBSTR(text_content, 1, 50)          AS text_preview,
        CASE
            WHEN text_content LIKE '%<br>%' THEN '<br> tag found'
            WHEN text_content LIKE '%<div>%' THEN '<div> tag found'
            WHEN text_content LIKE '%</div>%' THEN '</div> tag found'
            WHEN text_content LIKE '%&amp;%' THEN '&amp; entity found'
            WHEN text_content LIKE '%&lt;%' THEN '&lt; entity found'
            WHEN text_content LIKE '%&gt;%' THEN '&gt; entity found'
            ELSE 'Other HTML artifact'
        END                                  AS flagged_value,
        'HTML_CONTAMINATION'                 AS anomaly_type,
        'Text contains raw HTML tags or unescaped entities'
                                             AS anomaly_description
    FROM posts_raw
    WHERE text_content LIKE '%<br>%'
       OR text_content LIKE '%<div>%'
       OR text_content LIKE '%</div>%'
       OR text_content LIKE '%&amp;%'
       OR text_content LIKE '%&lt;%'
       OR text_content LIKE '%&gt;%'
),
anomaly_summary AS (
    -- Compute per-type counts using a window function
    SELECT
        *,
        COUNT(*) OVER (PARTITION BY anomaly_type)
                                             AS category_total,
        ROW_NUMBER() OVER (
            PARTITION BY anomaly_type
            ORDER BY post_id
        )                                    AS row_within_category
    FROM anomaly_scan
)
-- Return top 5 examples per category + full category counts
SELECT
    anomaly_type,
    category_total,
    row_within_category,
    post_id,
    user_id,
    platform,
    text_preview,
    flagged_value,
    anomaly_description
FROM anomaly_summary
WHERE row_within_category <= 5
ORDER BY anomaly_type, row_within_category;
"""

print("\n" + "-" * 80)
print("  H5: IDENTIFY DATA ANOMALIES (Top 5 per Category)")
print("-" * 80)
h5_result = pd.read_sql(H5_SQL, conn)
print(h5_result.to_string(index=False))

# Also get the full summary counts
H5_SUMMARY_SQL = """
SELECT
    anomaly_type,
    COUNT(*) AS record_count,
    COUNT(DISTINCT user_id) AS affected_users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM posts_raw), 2) AS pct_of_total
FROM (
    SELECT post_id, user_id, 'NEGATIVE_LIKES' AS anomaly_type
    FROM posts_raw WHERE CAST(likes AS REAL) < 0

    UNION ALL

    SELECT post_id, user_id, 'MISSING_PLATFORM'
    FROM posts_raw
    WHERE platform IS NULL OR TRIM(platform) = '' OR TRIM(UPPER(platform)) = 'NULL'

    UNION ALL

    SELECT post_id, user_id, 'MISSING_TEXT'
    FROM posts_raw
    WHERE text_content IS NULL OR TRIM(text_content) = '' OR TRIM(UPPER(text_content)) = 'NULL'

    UNION ALL

    SELECT post_id, user_id, 'HTML_CONTAMINATION'
    FROM posts_raw
    WHERE text_content LIKE '%<br>%'
       OR text_content LIKE '%<div>%'
       OR text_content LIKE '%</div>%'
       OR text_content LIKE '%&amp;%'
       OR text_content LIKE '%&lt;%'
       OR text_content LIKE '%&gt;%'
) anomalies
GROUP BY anomaly_type
ORDER BY record_count DESC;
"""

print("\n" + "-" * 80)
print("  H5: ANOMALY SUMMARY (Full Counts)")
print("-" * 80)
h5_summary = pd.read_sql(H5_SUMMARY_SQL, conn)
print(h5_summary.to_string(index=False))

total_anomalies = h5_summary['record_count'].sum()
total_raw = pd.read_sql('SELECT COUNT(*) as c FROM posts_raw', conn)['c'][0]
print(f"\nTotal anomalous records: {total_anomalies}")
print(f"Total raw records: {total_raw}")
print(f"Overall data corruption rate: {total_anomalies/total_raw*100:.1f}%")

# Also get duplicate count
dup_count = pd.read_sql("SELECT COUNT(*) as c FROM (SELECT post_id, COUNT(*) as cnt FROM posts_raw GROUP BY post_id HAVING cnt > 1)", conn)['c'][0]
print(f"Duplicate post_ids: {dup_count}")

conn.close()

print("\n" + "=" * 80)
print("ALL PHASE 2 QUERIES EXECUTED SUCCESSFULLY")
print("=" * 80)
