"""
===============================================================================
PHASE 1 — DATA INTAKE PIPELINE & CLEANING
===============================================================================
Competition : Data Vortex – Rebuilding the Social Engine (Round 1)
Author      : Data Engineering Pipeline
Description : Loads the two raw/corrupted CSVs, profiles data-quality issues,
              applies deterministic cleaning transformations with full
              justification, and exports the finalized cleaned dataset.
===============================================================================
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime

# ─────────────────────────── 1. DATA LOADING ────────────────────────────────

print("=" * 80)
print("PHASE 1: DATA INTAKE PIPELINE & CLEANING")
print("=" * 80)

# Posts CSV has multiline text_content (embedded newlines inside quoted fields).
# We read with python engine to handle that correctly.
posts_raw = pd.read_csv(
    "Social_Engine_Posts_Corrupted.csv",
    engine="python",
    on_bad_lines="warn",
    dtype=str  # Load everything as string first for profiling
)

users_raw = pd.read_csv(
    "Social_Engine_Users.csv",
    dtype=str
)

print(f"\n[LOAD] Posts raw shape : {posts_raw.shape}")
print(f"[LOAD] Users raw shape: {users_raw.shape}")

# ─────────────────────────── 2. RAW DATA PROFILING ──────────────────────────

def profile_dataframe(df, name):
    """Generate a profiling summary for a raw DataFrame."""
    print(f"\n{'-'*60}")
    print(f"  PROFILING: {name}")
    print(f"{'-'*60}")
    print(f"  Rows: {len(df)}  |  Columns: {df.shape[1]}")
    print(f"\n  Column-level summary:")
    for col in df.columns:
        null_count = df[col].isna().sum()
        null_str_count = df[col].astype(str).str.strip().eq("NULL").sum()
        empty_count = df[col].astype(str).str.strip().eq("").sum()
        unique_count = df[col].nunique()
        print(f"    {col:25s} | nulls={null_count:5d} | 'NULL'-strings={null_str_count:5d} "
              f"| empty={empty_count:5d} | unique={unique_count:5d}")
    dup_count = df.duplicated().sum()
    print(f"\n  Full-row duplicates: {dup_count}")
    return dup_count

dup_posts = profile_dataframe(posts_raw, "Posts (Corrupted)")
dup_users = profile_dataframe(users_raw, "Users")

# ─────────────────────────── 3. CLEANING — USERS TABLE ──────────────────────

print("\n" + "=" * 80)
print("CLEANING: Users Table")
print("=" * 80)

users = users_raw.copy()

# 3a. Drop exact duplicates
users.drop_duplicates(inplace=True)
print(f"[CLEAN] Dropped {dup_users} duplicate user rows.")

# 3b. Validate user_id format
invalid_uid = users[~users["user_id"].str.match(r"^user_[a-z0-9]+$", na=False)]
print(f"[CHECK] Invalid user_id format rows: {len(invalid_uid)}")

# 3c. Standardize location
users["location"] = users["location"].str.strip()
print(f"[CLEAN] Standardized location whitespace.")

# 3d. Standardize language codes to lowercase
users["language"] = users["language"].str.strip().str.lower()
print(f"[CLEAN] Lowercased language codes.")

# 3e. Parse account_created as date
users["account_created"] = pd.to_datetime(users["account_created"], errors="coerce")
bad_dates_users = users["account_created"].isna().sum()
print(f"[CHECK] Unparseable account_created dates: {bad_dates_users}")

# 3f. Convert follower_count to integer
users["follower_count"] = pd.to_numeric(users["follower_count"], errors="coerce").astype("Int64")
print(f"[CLEAN] Converted follower_count to integer.")

# 3g. Drop trailing empty row
users = users[users["user_id"].notna() & (users["user_id"].str.strip() != "")]
print(f"[CLEAN] Users final shape: {users.shape}")

# ─────────────────────────── 4. CLEANING — POSTS TABLE ──────────────────────

print("\n" + "=" * 80)
print("CLEANING: Posts Table")
print("=" * 80)

posts = posts_raw.copy()

# 4a. Replace literal "NULL" strings with NaN
for col in posts.columns:
    mask = posts[col].astype(str).str.strip() == "NULL"
    posts.loc[mask, col] = np.nan
    cnt = mask.sum()
    if cnt > 0:
        print(f"[CLEAN] Column '{col}': replaced {cnt} 'NULL' strings with NaN.")

# 4b. Remove HTML/corruption tokens from text_content
def clean_text(text):
    if pd.isna(text):
        return text
    text = str(text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&[a-zA-Z]+;", "", text)
    text = text.replace("\u00c3\u00a9", "")
    text = text.replace("Ã©", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text if text else np.nan

posts["text_content"] = posts["text_content"].apply(clean_text)
print(f"[CLEAN] Removed HTML tags, entities, and encoding artifacts from text_content.")

# 4c. Standardize platform names
posts["platform"] = posts["platform"].str.strip().str.title()
posts["platform"] = posts["platform"].replace("", np.nan)
posts["platform"] = posts["platform"].replace("Youtube", "YouTube")
platform_counts = posts["platform"].value_counts(dropna=False)
print(f"[CLEAN] Platform distribution after standardization:")
for p, c in platform_counts.items():
    label = str(p) if pd.notna(p) else "MISSING"
    print(f"         {label:15s} : {c}")

# 4d. Unify timestamp formats
def parse_timestamp(ts):
    if pd.isna(ts):
        return pd.NaT
    ts = str(ts).strip()
    if not ts:
        return pd.NaT
    try:
        return pd.to_datetime(ts, format="ISO8601")
    except (ValueError, TypeError):
        pass
    try:
        return pd.to_datetime(ts, format="%d-%m-%Y")
    except (ValueError, TypeError):
        pass
    try:
        epoch = float(ts)
        if 1_000_000_000 < epoch < 2_000_000_000:
            return pd.to_datetime(epoch, unit="s")
    except (ValueError, TypeError):
        pass
    return pd.NaT

posts["timestamp"] = posts["timestamp"].apply(parse_timestamp)
unparseable_ts = posts["timestamp"].isna().sum()
print(f"[CLEAN] Parsed timestamps. Unparseable: {unparseable_ts}")
print(f"         Date range: {posts['timestamp'].min()} to {posts['timestamp'].max()}")

# 4e. Convert numeric columns, fix negative values
for col in ["likes", "shares", "comments"]:
    posts[col] = pd.to_numeric(posts[col], errors="coerce")
    neg_count = (posts[col] < 0).sum()
    if neg_count > 0:
        print(f"[CLEAN] Column '{col}': found {neg_count} negative values -> taking absolute value.")
        posts[col] = posts[col].abs()
    posts[col] = posts[col].astype("Int64")

# 4f. Validate post_id uniqueness
dup_pid = posts["post_id"].duplicated().sum()
print(f"[CHECK] Duplicate post_ids: {dup_pid}")
if dup_pid > 0:
    posts.drop_duplicates(subset=["post_id"], keep="first", inplace=True)
    print(f"[CLEAN] Dropped {dup_pid} duplicate post_id rows (kept first).")

# 4g. Validate user_id foreign-key integrity
valid_user_ids = set(users["user_id"].unique())
orphan_posts = posts[~posts["user_id"].isin(valid_user_ids)]
print(f"[CHECK] Posts with user_id not found in Users table: {len(orphan_posts)}")

# 4h. Check fully empty rows
content_cols = ["text_content", "likes", "shares", "comments"]
fully_empty = posts[posts[content_cols].isna().all(axis=1)]
print(f"[CHECK] Rows with all content columns empty: {len(fully_empty)}")

# 4i. Feature Engineering
def extract_hashtags(text):
    if pd.isna(text):
        return ""
    return ", ".join(re.findall(r"#(\w+)", str(text)))

posts["hashtags"] = posts["text_content"].apply(extract_hashtags)

def extract_brand(text):
    if pd.isna(text):
        return np.nan
    brands = ["Nike", "Adidas", "Apple", "Samsung", "Google", "Microsoft",
              "Amazon", "Toyota", "Pepsi", "Coca-Cola"]
    text_str = str(text)
    found = [b for b in brands if b.lower() in text_str.lower()]
    return found[0] if found else np.nan

posts["brand_mentioned"] = posts["text_content"].apply(extract_brand)

# Sentiment proxy from keywords
def extract_sentiment(text):
    if pd.isna(text):
        return "neutral"
    text_lower = str(text).lower()
    positive_words = ["loving it", "best purchase", "absolutely loving", "exceeded my expectations",
                      "highly recommend", "worth every penny", "thrilled", "delighted",
                      "super excited", "impressive", "amazing", "outstanding", "can't contain"]
    negative_words = ["disappointed", "returning it", "wouldn't recommend", "not worth",
                      "had issues", "frustrated", "fed up", "bummed out", "sad to report",
                      "overpriced", "subpar", "frustrating", "disappointing"]
    pos_score = sum(1 for w in positive_words if w in text_lower)
    neg_score = sum(1 for w in negative_words if w in text_lower)
    if pos_score > neg_score:
        return "positive"
    elif neg_score > pos_score:
        return "negative"
    else:
        return "neutral"

posts["sentiment"] = posts["text_content"].apply(extract_sentiment)

posts["total_engagement"] = (
    posts["likes"].fillna(0) + posts["shares"].fillna(0) + posts["comments"].fillna(0)
)
posts["engagement_rate"] = (posts["total_engagement"] / 3).round(2)

posts["post_date"] = posts["timestamp"].dt.date
posts["post_hour"] = posts["timestamp"].dt.hour.astype("Int64")
posts["post_day_of_week"] = posts["timestamp"].dt.day_name()
posts["post_month"] = posts["timestamp"].dt.month.astype("Int64")

print(f"[FEAT] Extracted hashtags, brand mentions, sentiment, engagement metrics, date components.")

# ─────────────────────────── 5. FINAL SUMMARY ──────────────────────────────

print("\n" + "=" * 80)
print("FINAL CLEANED DATASET SUMMARY")
print("=" * 80)
print(f"  Posts: {posts.shape[0]} rows x {posts.shape[1]} columns")
print(f"  Users: {users.shape[0]} rows x {users.shape[1]} columns")
print(f"\n  Posts columns: {list(posts.columns)}")
print(f"  Users columns: {list(users.columns)}")
print(f"\n  Posts missing values:")
for col in posts.columns:
    na_count = posts[col].isna().sum()
    pct = na_count / len(posts) * 100
    if na_count > 0:
        print(f"    {col:25s} : {na_count:5d} ({pct:.1f}%)")

print(f"\n  Users missing values:")
for col in users.columns:
    na_count = users[col].isna().sum()
    if na_count > 0:
        print(f"    {col:25s} : {na_count:5d}")

# ─────────────────────────── 6. EXPORT CLEANED DATA ────────────────────────

posts.to_csv("Social_Engine_Posts_Cleaned.csv", index=False)
users.to_csv("Social_Engine_Users_Cleaned.csv", index=False)
print(f"\n[EXPORT] Saved: Social_Engine_Posts_Cleaned.csv")
print(f"[EXPORT] Saved: Social_Engine_Users_Cleaned.csv")

merged = posts.merge(users, on="user_id", how="left", suffixes=("_post", "_user"))
merged.to_csv("Social_Engine_Merged_Cleaned.csv", index=False)
print(f"[EXPORT] Saved: Social_Engine_Merged_Cleaned.csv")

print("\nPhase 1 Data Cleaning Pipeline Complete.")
