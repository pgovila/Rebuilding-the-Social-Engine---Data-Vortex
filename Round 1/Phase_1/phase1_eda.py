"""
===============================================================================
PHASE 1 â€” AUTOMATED EXPLORATORY DATA ANALYSIS (EDA)
===============================================================================
Competition : Data Vortex â€“ Rebuilding the Social Engine (Round 1)
Description : Performs deep EDA on the cleaned dataset to discover social-media
              analytical insights including user behavior, engagement patterns,
              platform dynamics, and temporal trends.
===============================================================================
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ 1. LOAD CLEANED DATA â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

posts = pd.read_csv("Social_Engine_Posts_Cleaned.csv", parse_dates=["timestamp"])
users = pd.read_csv("Social_Engine_Users_Cleaned.csv", parse_dates=["account_created"])
merged = pd.read_csv("Social_Engine_Merged_Cleaned.csv", parse_dates=["timestamp", "account_created"])

print("=" * 80)
print("PHASE 1: EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 80)

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ 2. OVERVIEW STATISTICS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

print("\n" + "â”€" * 60)
print("  2.1 DATASET OVERVIEW")
print("â”€" * 60)
print(f"  Total posts: {len(posts):,}")
print(f"  Total users: {len(users):,}")
print(f"  Unique posting users: {posts['user_id'].nunique():,}")
print(f"  Posts per user (mean): {len(posts) / posts['user_id'].nunique():.1f}")
print(f"  Date range: {posts['timestamp'].min()} to {posts['timestamp'].max()}")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ 2.2 ENGAGEMENT METRICS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

print("\n" + "â”€" * 60)
print("  2.2 ENGAGEMENT STATISTICS")
print("â”€" * 60)
for col in ["likes", "shares", "comments", "total_engagement"]:
    series = posts[col].dropna()
    print(f"\n  {col}:")
    print(f"    Mean   : {series.mean():>10.1f}")
    print(f"    Median : {series.median():>10.1f}")
    print(f"    Std    : {series.std():>10.1f}")
    print(f"    Min    : {series.min():>10.0f}")
    print(f"    Max    : {series.max():>10.0f}")
    print(f"    Q25    : {series.quantile(0.25):>10.1f}")
    print(f"    Q75    : {series.quantile(0.75):>10.1f}")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ 2.3 PLATFORM ANALYSIS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

print("\n" + "â”€" * 60)
print("  2.3 PLATFORM ANALYSIS")
print("â”€" * 60)
platform_stats = posts.groupby("platform", dropna=False).agg(
    post_count=("post_id", "count"),
    avg_likes=("likes", "mean"),
    avg_shares=("shares", "mean"),
    avg_comments=("comments", "mean"),
    avg_engagement=("total_engagement", "mean"),
    unique_users=("user_id", "nunique")
).round(1)
platform_stats = platform_stats.sort_values("post_count", ascending=False)
print(f"\n{platform_stats.to_string()}")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ 2.4 TEMPORAL ANALYSIS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

print("\n" + "â”€" * 60)
print("  2.4 TEMPORAL PATTERNS")
print("â”€" * 60)

# Monthly posting volume
posts_with_date = posts.dropna(subset=["timestamp"])
monthly = posts_with_date.groupby(posts_with_date["timestamp"].dt.to_period("M")).agg(
    post_count=("post_id", "count"),
    avg_engagement=("total_engagement", "mean")
).round(1)
print("\n  Monthly Volume & Engagement:")
print(f"{monthly.to_string()}")

# Day of week analysis
dow = posts.groupby("post_day_of_week", dropna=False).agg(
    post_count=("post_id", "count"),
    avg_engagement=("total_engagement", "mean")
).round(1)
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dow = dow.reindex(day_order)
print("\n  Day-of-Week Activity:")
print(f"{dow.to_string()}")

# Hourly analysis
hourly = posts.groupby("post_hour", dropna=False).agg(
    post_count=("post_id", "count"),
    avg_engagement=("total_engagement", "mean")
).round(1)
print("\n  Hourly Activity Distribution (top 10 by engagement):")
print(f"{hourly.sort_values('avg_engagement', ascending=False).head(10).to_string()}")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ 2.5 BRAND ANALYSIS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

print("\n" + "â”€" * 60)
print("  2.5 BRAND MENTION ANALYSIS")
print("â”€" * 60)
brand_stats = posts.dropna(subset=["brand_mentioned"]).groupby("brand_mentioned").agg(
    mention_count=("post_id", "count"),
    avg_likes=("likes", "mean"),
    avg_shares=("shares", "mean"),
    avg_comments=("comments", "mean"),
    avg_engagement=("total_engagement", "mean"),
    unique_users=("user_id", "nunique")
).round(1).sort_values("mention_count", ascending=False)
print(f"\n{brand_stats.to_string()}")

# Brand-Platform cross-analysis
brand_platform = posts.dropna(subset=["brand_mentioned", "platform"]).groupby(
    ["brand_mentioned", "platform"]
).agg(count=("post_id", "count"), avg_eng=("total_engagement", "mean")).round(1)
print("\n  Brand x Platform (top 20 by count):")
print(f"{brand_platform.sort_values('count', ascending=False).head(20).to_string()}")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ 2.6 SENTIMENT ANALYSIS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

print("\n" + "â”€" * 60)
print("  2.6 SENTIMENT ANALYSIS")
print("â”€" * 60)
sentiment_stats = posts.groupby("sentiment").agg(
    post_count=("post_id", "count"),
    avg_likes=("likes", "mean"),
    avg_shares=("shares", "mean"),
    avg_comments=("comments", "mean"),
    avg_engagement=("total_engagement", "mean")
).round(1)
print(f"\n{sentiment_stats.to_string()}")

# Sentiment by brand
brand_sentiment = posts.dropna(subset=["brand_mentioned"]).groupby(
    ["brand_mentioned", "sentiment"]
).agg(count=("post_id", "count")).reset_index()
brand_sentiment_pivot = brand_sentiment.pivot(
    index="brand_mentioned", columns="sentiment", values="count"
).fillna(0).astype(int)
print("\n  Sentiment Distribution by Brand:")
print(f"{brand_sentiment_pivot.to_string()}")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ 2.7 USER BEHAVIORAL ANALYSIS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

print("\n" + "â”€" * 60)
print("  2.7 USER BEHAVIORAL FLAGS & SEGMENTATION")
print("â”€" * 60)

# Posts per user distribution
user_post_counts = posts.groupby("user_id").agg(
    post_count=("post_id", "count"),
    avg_engagement=("total_engagement", "mean"),
    platforms_used=("platform", "nunique"),
    first_post=("timestamp", "min"),
    last_post=("timestamp", "max")
)
user_post_counts["posting_span_days"] = (
    user_post_counts["last_post"] - user_post_counts["first_post"]
).dt.days

print(f"\n  Posts per user distribution:")
print(f"    Mean   : {user_post_counts['post_count'].mean():.1f}")
print(f"    Median : {user_post_counts['post_count'].median():.1f}")
print(f"    Max    : {user_post_counts['post_count'].max()}")
print(f"    Min    : {user_post_counts['post_count'].min()}")
print(f"    Std    : {user_post_counts['post_count'].std():.1f}")

# Power users (top 1%)
threshold_99 = user_post_counts["post_count"].quantile(0.99)
power_users = user_post_counts[user_post_counts["post_count"] >= threshold_99]
print(f"\n  Power Users (top 1%, >= {threshold_99:.0f} posts): {len(power_users)}")
print(f"    Their avg engagement: {power_users['avg_engagement'].mean():.1f}")

# Bot-like behavior detection: high posting frequency + low engagement
# Flag users posting > 15 times with avg engagement < 1500
bot_candidates = user_post_counts[
    (user_post_counts["post_count"] > 15) &
    (user_post_counts["avg_engagement"] < 1500)
]
print(f"\n  Potential Bot Flags (>15 posts, avg engagement <1500): {len(bot_candidates)}")

# Engagement velocity = total_engagement / posting_span_days
user_post_counts["engagement_velocity"] = (
    user_post_counts["avg_engagement"] / (user_post_counts["posting_span_days"].replace(0, 1))
)

# Segment users
def segment_user(row):
    if row["post_count"] >= threshold_99:
        return "Power User"
    elif row["avg_engagement"] > 4000:
        return "High Engager"
    elif row["avg_engagement"] < 1500 and row["post_count"] > 10:
        return "Low-Engagement Active"
    elif row["post_count"] <= 3:
        return "Casual User"
    else:
        return "Regular User"

user_post_counts["segment"] = user_post_counts.apply(segment_user, axis=1)
segment_counts = user_post_counts["segment"].value_counts()
print(f"\n  User Segments:")
for seg, cnt in segment_counts.items():
    print(f"    {seg:25s} : {cnt}")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ 2.8 GEOGRAPHIC ANALYSIS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

print("\n" + "â”€" * 60)
print("  2.8 GEOGRAPHIC & LANGUAGE ANALYSIS")
print("â”€" * 60)

geo_stats = merged.groupby("location", dropna=False).agg(
    post_count=("post_id", "count"),
    avg_engagement=("total_engagement", "mean"),
    unique_users=("user_id", "nunique")
).round(1).sort_values("post_count", ascending=False)
print("\n  Top 15 Locations by Post Volume:")
print(f"{geo_stats.head(15).to_string()}")

lang_stats = merged.groupby("language", dropna=False).agg(
    post_count=("post_id", "count"),
    avg_engagement=("total_engagement", "mean"),
    unique_users=("user_id", "nunique")
).round(1).sort_values("avg_engagement", ascending=False)
print("\n  Language Engagement Ranking:")
print(f"{lang_stats.to_string()}")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ 2.9 HASHTAG ANALYSIS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

print("\n" + "â”€" * 60)
print("  2.9 HASHTAG ANALYSIS")
print("â”€" * 60)

all_hashtags = posts["hashtags"].str.split(", ").explode()
all_hashtags = all_hashtags[all_hashtags != ""]
hashtag_counts = all_hashtags.value_counts()
print(f"\n  Total unique hashtags: {hashtag_counts.shape[0]}")
print(f"\n  Top 20 Hashtags:")
for tag, cnt in hashtag_counts.head(20).items():
    print(f"    #{tag:25s} : {cnt}")

# Hashtag engagement correlation
posts["hashtag_count"] = posts["hashtags"].apply(
    lambda x: len(str(x).split(", ")) if pd.notna(x) and str(x).strip() else 0
)
ht_eng = posts.groupby("hashtag_count").agg(
    post_count=("post_id", "count"),
    avg_engagement=("total_engagement", "mean")
).round(1)
print(f"\n  Hashtag Count vs Engagement:")
print(f"{ht_eng.to_string()}")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ 2.10 ANOMALY DETECTION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

print("\n" + "â”€" * 60)
print("  2.10 ANOMALY DETECTION")
print("â”€" * 60)

# Engagement outliers using IQR
for col in ["likes", "shares", "comments"]:
    series = posts[col].dropna()
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    upper = Q3 + 1.5 * IQR
    lower = Q1 - 1.5 * IQR
    outliers = series[(series > upper) | (series < lower)]
    print(f"  {col}: IQR outliers = {len(outliers)} ({len(outliers)/len(series)*100:.1f}%)")

# Posting velocity spikes (daily)
daily_posts = posts_with_date.groupby(
    posts_with_date["timestamp"].dt.date
).size()
mean_daily = daily_posts.mean()
std_daily = daily_posts.std()
spike_days = daily_posts[daily_posts > mean_daily + 2 * std_daily]
print(f"\n  Daily posting: mean={mean_daily:.1f}, std={std_daily:.1f}")
print(f"  Spike days (>2 std): {len(spike_days)}")
if len(spike_days) > 0:
    print(f"  Top spike days:")
    for day, cnt in spike_days.sort_values(ascending=False).head(5).items():
        print(f"    {day}: {cnt} posts")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ 2.11 CORRELATION ANALYSIS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

print("\n" + "â”€" * 60)
print("  2.11 CORRELATION MATRIX (Engagement Metrics)")
print("â”€" * 60)
corr_cols = ["likes", "shares", "comments", "total_engagement"]
corr_matrix = posts[corr_cols].corr().round(3)
print(f"\n{corr_matrix.to_string()}")

# Follower count vs engagement
if "follower_count" in merged.columns:
    follower_eng_corr = merged[["follower_count", "total_engagement"]].dropna().corr().iloc[0, 1]
    print(f"\n  Follower Count vs Total Engagement correlation: {follower_eng_corr:.3f}")

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ 2.12 CONTENT COMPLETENESS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

print("\n" + "â”€" * 60)
print("  2.12 CONTENT COMPLETENESS AUDIT")
print("â”€" * 60)
posts["has_text"] = posts["text_content"].notna()
posts["has_platform"] = posts["platform"].notna()
posts["has_likes"] = posts["likes"].notna()

completeness = posts[["has_text", "has_platform", "has_likes"]].mean() * 100
print(f"\n  Field completeness rates:")
print(f"    text_content : {completeness['has_text']:.1f}%")
print(f"    platform     : {completeness['has_platform']:.1f}%")
print(f"    likes        : {completeness['has_likes']:.1f}%")

# Cross-completeness
both_missing = ((~posts["has_text"]) & (~posts["has_platform"])).sum()
print(f"\n  Posts missing BOTH text & platform: {both_missing}")

print("\n" + "=" * 80)
print("EDA COMPLETE")
print("=" * 80)
