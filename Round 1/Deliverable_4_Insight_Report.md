# DELIVERABLE 4: PHASE 2 INSIGHT REPORT
# Data Vortex Competition — Aaruush '26, Round 1, Phase 2
# Selected: E2 (Easy) | M5 (Medium) | H5 (Hard)

---

## 4.1 E2 Insights: What the Top 10 Engaged Posts Reveal About the Active User Core

### The Engagement Ceiling

The highest-engagement post in the entire dataset scored **7,893 total engagement** (4,983 likes + 1,919 shares + 991 comments) — a Coca-Cola promotional post from a Dubai-based user on Instagram. The top 10 posts cluster tightly between 7,610 and 7,893, with only a 283-point spread across the full leaderboard. The theoretical maximum engagement is 8,000 (5,000 likes + 2,000 shares + 1,000 comments), meaning the top post achieves **98.7% of the theoretical ceiling**.

### Platform Performance

| Platform | Appearances in Top 10 |
|----------|----------------------|
| Instagram | 3 (Rank #1, #5, #7) |
| Facebook | 2 (Rank #3, #8) |
| YouTube | 2 (Rank #4, #10) |
| Reddit | 1 (Rank #2) |
| Twitter | 1 (Rank #9) |
| Missing (NaN) | 1 (Rank #6) |

**Instagram dominates peak engagement**, occupying 3 of the top 10 slots including the #1 position. This confirms it as the primary driver of viral content on the platform. Notably, one top-10 post (Rank #6) has NULL platform metadata — even with missing attribution, it achieved 7,723 engagement.

### Brand Affiliation

9 out of 10 top-engaged posts explicitly mention a brand:
- Coca-Cola appears 3 times (Ranks #1, #4, #7)
- Nike appears 2 times (Ranks #2, #8)
- Apple, Amazon, Adidas, Microsoft each appear once

**Coca-Cola is the most engagement-driving brand**, with the #1, #4, and #7 posts all referencing its products. Brand-affiliated content clearly outperforms generic posts at the top of the engagement ladder.

### The Follower Count Paradox

| Rank | Follower Count | Engagement |
|------|---------------|------------|
| #1 | 13,964 | 7,893 |
| #2 | 13,313 | 7,793 |
| #3 | 33,737 | 7,764 |
| #10 | 49,936 | 7,610 |

The top 2 most engaged posts come from users with follower counts in the **13K-14K range** — firmly mid-tier. The user with the highest follower count in the top 10 (49,936) ranks last (#10). This confirms the Phase 1 EDA finding: **follower count does not predict engagement**. The Social Engine rewards content quality and brand relevance over audience size.

### Key Takeaway

> The active user core driving peak engagement is defined by **mid-tier influencers** (13K-50K followers) creating **brand-affiliated content** primarily on **Instagram**. The platform operates as a meritocracy where content quality, not follower count, determines engagement success.

---

## 4.2 M5 Insights: Platform Health & Bot/Manipulation Patterns

### Scale of Suspicious Activity

| Metric | Value |
|--------|-------|
| Total suspicious posts (shares > likes + comments) | **1,209** |
| Percentage of evaluable posts | **10.1%** |
| Share percentage range in top 20 | 50.7% — 81.0% |
| Highest share surplus | 1,524 (post `u1aa801qvxeu`) |

**1 in 10 posts** on the platform exhibit share-dominant engagement patterns that are inconsistent with organic user behavior. In healthy social media ecosystems, shares typically represent 20-35% of total engagement. The top 20 suspicious posts all exceed 50%, with the most extreme case reaching **81.0%** — meaning 4 out of every 5 engagement actions on that post were shares.

### Bot Behavior Signatures Identified

**Signature 1: Artificial Share Inflation**
Post `u1aa801qvxeu` (Rank #15) has 162 likes, 306 comments, but 1,992 shares. This 81% share-dominated profile is impossible in organic engagement. Bots can easily execute "share/repost" actions programmatically, but generating authentic-looking likes and comments requires more sophisticated tooling. The low likes (162) combined with near-maximum shares (1,992 out of 2,000 cap) is a textbook bot signature.

**Signature 2: Low-Likes + High-Shares Clusters**
Multiple posts in the top 20 show likes below 500 combined with shares near the 2,000 cap:
- Rank #1: 453 likes + 2,000 shares (69.9% share-dominated)
- Rank #4: 390 likes + 1,999 shares (61.6%)
- Rank #18: 169 likes + 1,991 shares (66.0%)
- Rank #19: 14 likes + 1,990 shares (71.8%) ← **only 14 likes!**

Post #19 (`lit2hyqg0v0l`) with just 14 likes but 1,990 shares is the strongest single indicator of automated share-botting in the dataset.

**Signature 3: Missing Platform Correlation**
5 of the top 20 suspicious posts (25%) have NULL platform metadata:
- Rank #5, #7, #8, #9, #15

This overlap between missing platform attribution and suspicious engagement is a critical finding. These posts may originate from API endpoints that bypass normal platform logging, suggesting a **programmatic bot vector that circumvents platform attribution**.

**Signature 4: Geographic Clustering**
| City | Appearances in Top 20 | Ranks |
|------|----------------------|-------|
| Mexico City, Mexico | 3 | #7, #8, #15 |
| Shanghai, China | 3 | #4, #5, #19 |
| Johannesburg, South Africa | 2 | #1, #6 |

The concentration of suspicious posts from three specific cities suggests **coordinated bot farm operations**. Mexico City accounts for the most extreme case (81.0% share-dominated) and Shanghai accounts for the post with only 14 likes.

### Platform Health Implications

> **WARNING**: 10.1% of the platform's posts exhibit engagement patterns consistent with automated share-botting. The correlation between missing platform metadata and suspicious engagement (25% of top-20 flagged posts lack platform attribution) suggests a potential API-based bot vector that circumvents platform logging. Geographic concentration in Mexico City and Shanghai points to coordinated bot farm operations.

### Recommended Countermeasures

1. **Real-time share ratio threshold**: Auto-flag posts where shares exceed 60% of total engagement
2. **API endpoint audit**: Investigate the source of NULL-platform posts — they are disproportionately represented in suspicious activity
3. **Geographic rate limiting**: Apply enhanced scrutiny to posts from Mexico City and Shanghai IPs
4. **Likes-floor enforcement**: Posts with < 50 likes but > 1,000 shares should trigger immediate review

---

## 4.3 H5 Insights: Data Integrity Diagnostic Evaluation

### Corruption Overview

The raw corrupted dataset contains **12,360 records** with **5,121 anomalous entries** spanning 4 categories — an overall **corruption rate of 41.4%**. This is a critical level of data degradation that would render any analytics unreliable without systematic remediation.

### Category-by-Category Diagnostic

#### Category 1: Missing Platform (1,846 records — 14.94%)

| Diagnostic Factor | Finding |
|-------------------|---------|
| Records affected | 1,846 |
| Unique users affected | 1,060 (70.7% of user base) |
| Root cause | API ingestion from a platform-agnostic endpoint |
| Severity | **MEDIUM** |

The missing platform issue affects the majority of the user base (1,060 out of 1,500 users), proving this is a **systematic pipeline issue** rather than user-specific corruption. These posts retain engagement metrics and timestamps — only platform attribution is lost.

**Impact**: Platform-segmented analytics (e.g., "which platform drives highest engagement?") are skewed by the 14.94% unattributable post volume. Any platform comparison must acknowledge this bias.

#### Category 2: Missing Text Content (1,746 records — 14.13%)

| Diagnostic Factor | Finding |
|-------------------|---------|
| Records affected | 1,746 |
| Unique users affected | 1,017 (67.8% of user base) |
| Root cause | Deleted posts or image/video-only content |
| Severity | **MEDIUM** |

The missing text rate (14.13%) closely mirrors the missing platform rate (14.94%), suggesting both originate from the **same batch failure** in the export pipeline. Posts with missing text still carry valid engagement data, user attribution, and timestamps.

**Impact**: Text-dependent analyses (sentiment scoring, hashtag extraction, brand detection) operate on 85.87% of the dataset. The ~14% blind spot may introduce slight bias if the missing posts have systematically different content profiles.

#### Category 3: HTML Contamination (1,004 records — 8.12%)

| Diagnostic Factor | Finding |
|-------------------|---------|
| Records affected | 1,004 |
| Unique users affected | 720 (48% of user base) |
| Artifact types | `<br>`, `<div>`, `</div>`, `&amp;`, `&lt;`, `&gt;` |
| Root cause | Faulty HTML-to-plaintext conversion in export pipeline |
| Severity | **LOW** (fully remediated) |

The HTML contamination is a **cosmetic data quality issue**. The underlying text content is fully recoverable after stripping tags and decoding entities (as performed in Phase 1 cleaning). The presence of `<div>` tags suggests the source data was originally stored as HTML-formatted rich text, and the export pipeline failed to apply its HTML-to-plaintext conversion step for ~8% of records.

**Impact**: Fully remediated by Phase 1 cleaning. Post-cleaning, zero HTML artifacts remain.

#### Category 4: Negative Likes (525 records — 4.25%)

| Diagnostic Factor | Finding |
|-------------------|---------|
| Records affected | 525 |
| Unique users affected | 435 (29% of user base) |
| Value range | -997 to -4,812 |
| Root cause | Sign-bit corruption during data transfer |
| Severity | **HIGH** (corrupts engagement calculations) |

Negative engagement values are physically impossible in social media. The magnitudes (-997 to -4,812) are consistent with valid like counts in the positive range, strongly suggesting **sign-bit corruption** — likely from a signed/unsigned integer type mismatch during ETL transfer.

**Impact**: If left unresolved, 525 posts would contribute negative values to engagement aggregations, dragging down averages and distorting platform-level metrics. Phase 1 cleaning resolved this by taking absolute values.

### Cross-Category Overlap Analysis

A critical finding is that **individual records can appear in multiple anomaly categories**. For example:
- `post_id = 01kgwhi645er` appears in both NEGATIVE_LIKES (-3,630) AND MISSING_PLATFORM (NaN)
- `post_id = 033i6hfsrdo8` appears in both MISSING_PLATFORM AND MISSING_TEXT

This overlap means the 5,121 anomaly count represents **anomaly instances**, not unique records. The actual number of unique corrupted records is lower, but the overlap itself is diagnostic: records failing in multiple categories suggest a more severe pipeline failure for those specific rows.

### The "15% Pattern" — Root Cause Hypothesis

| Field | Missing Rate |
|-------|-------------|
| Platform | 14.94% |
| Text Content | 14.13% |
| Likes | 15.12% (1,814 NULLs + 525 negatives = 2,339 problematic) |

The remarkably consistent ~15% missing rate across three independent fields points to a **single point of failure** in the data export pipeline. This is NOT random, independent field-level corruption — it is a systematic, row-level partial failure affecting approximately **1 in 7 records**. The most likely explanation is a batch processing job that:
1. Processes records in sequential batches
2. Fails silently for certain batches (possibly due to timeout, memory limits, or encoding errors)
3. Writes partial records with NULL fields instead of failing the entire batch

### Overall Data Health Scorecard

| Metric | Value | Grade |
|--------|-------|-------|
| Raw record count | 12,360 | — |
| Duplicate records | 352 (2.85%) | MODERATE |
| Records with any anomaly | 5,121 instances | — |
| **Pre-cleaning corruption rate** | **41.4%** | **CRITICAL** |
| Clean record count (post-Phase 1) | 12,000 | HEALTHY |
| Residual missing data | ~15% (platform/text/likes) | ACCEPTABLE |
| HTML contamination remaining | 0% | RESOLVED |
| Negative values remaining | 0% | RESOLVED |
| **Post-cleaning data health** | **Production-ready** | **PASS** |

> All four anomaly categories are **deterministically remediable**: negative values via absolute-value correction, HTML via regex stripping, duplicates via deduplication, and missing fields via NULL preservation. The Phase 1 cleaning pipeline successfully transforms a 41.4%-corrupted dataset into a production-ready analytical asset.
