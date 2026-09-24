"""
Data Vortex Round 2: Rebuilding the Semantic Understanding Layer
Production NLP Pipeline for Multi-Task Sentiment & Topic Classification

Target Tasks:
  1. Sentiment Classification  : Negative, Neutral, Positive (3 classes)
  2. Topic Category Modeling    : Account_Security, Community_Discussion,
                                  Feature_Feedback, Technical_Issues (4 classes)

Artifacts Generated:
  - tfidf_vectorizer.pkl
  - sentiment_classifier_model.pkl
  - topic_classifier_model.pkl
  - evaluation_metrics_report.txt
  - Round2_Technical_Report.pdf
"""

import os
import re
import html
import hashlib
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import VotingClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    accuracy_score,
)

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION & HYPERPARAMETERS
# ─────────────────────────────────────────────────────────────────────────────
RANDOM_STATE = 42
TEST_SIZE = 0.20
DATA_PATH = Path("Labeled_Social_NLP_Training_Data.csv")
OUTPUT_DIR = Path(".")

SENTIMENT_CLASSES = ["Negative", "Neutral", "Positive"]
TOPIC_CLASSES = [
    "Account_Security",
    "Community_Discussion",
    "Feature_Feedback",
    "Technical_Issues",
]

# ─────────────────────────────────────────────────────────────────────────────
# 1. PREPROCESSING PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
def clean_social_text(text: str) -> str:
    """
    Cleans raw social media text:
      - Strips HTML tags and unescapes HTML entities (&amp;, &lt;, etc.)
      - Replaces @username handles with <USER> tokens to retain structural context
      - Normalizes web URLs to <URL> tokens
      - Unescapes unicode sequences and handles CSV quotation artifacts
      - Normalizes whitespaces and converts to lowercase
    """
    if not isinstance(text, str) or not text.strip():
        return ""

    # Unescape HTML entities
    text = html.unescape(text)

    # Decode unicode escape artifacts (e.g., \u2019 -> ')
    text = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), text)

    # Normalize URLs
    text = re.sub(r"https?://\S+|www\.\S+", " <URL> ", text)

    # Anonymize user handles while preserving mention signal
    text = re.sub(r"@[\w_]+", " <USER> ", text)

    # Clean HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # Clean CSV quote artifacts ("""word""" -> "word")
    text = re.sub(r'"{2,}', '"', text)

    # Lowercase & normalize spaces
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)

    return text


def load_and_preprocess(filepath: Path) -> pd.DataFrame:
    """Loads CSV dataset and applies full text cleaning pipeline."""
    print(f"[INFO] Loading dataset from: {filepath}")
    df = pd.read_csv(filepath)
    df.dropna(subset=["post_text", "sentiment_label", "topic_category"], inplace=True)
    df["clean_text"] = df["post_text"].apply(clean_social_text)
    print(f"[INFO] Cleaned {len(df)} samples successfully.")
    return df


# ─────────────────────────────────────────────────────────────────────────────
# 2. FEATURE EXTRACTION (TF-IDF)
# ─────────────────────────────────────────────────────────────────────────────
def build_tfidf_vectorizer() -> TfidfVectorizer:
    """
    Sublinear TF-IDF Vectorizer:
      - ngram_range=(1, 2) captures negations ('not happy') & key bigrams
      - sublinear_tf=True dampens extreme word frequencies
      - min_df=2 filters singleton typos; max_df=0.95 removes ubiquitous terms
    """
    return TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        max_features=50000,
        min_df=2,
        max_df=0.95,
        token_pattern=r"(?u)\b\w+\b|<\w+>",
    )


# ─────────────────────────────────────────────────────────────────────────────
# 3. STRATIFIED SPLITTING
# ─────────────────────────────────────────────────────────────────────────────
def stratified_split(df: pd.DataFrame, X_matrix, test_size=0.20, seed=42):
    """
    Performs stratified 80/20 train/test split. Stratifies on combined
    sentiment x topic labels where feasible to preserve class distributions.
    """
    joint_labels = df["sentiment_label"] + "___" + df["topic_category"]
    val_counts = joint_labels.value_counts()
    rare_strata = val_counts[val_counts < 2].index

    # Fallback to sentiment stratification for single-instance strata
    stratify_target = joint_labels.copy()
    if len(rare_strata) > 0:
        stratify_target[stratify_target.isin(rare_strata)] = df.loc[
            stratify_target.isin(rare_strata), "sentiment_label"
        ]

    from sklearn.model_selection import train_test_split
    idx_train, idx_test = train_test_split(
        df.index,
        test_size=test_size,
        random_state=seed,
        stratify=stratify_target,
    )
    return X_matrix[idx_train], X_matrix[idx_test], idx_train, idx_test


# ─────────────────────────────────────────────────────────────────────────────
# 4. MODEL ARCHITECTURES (SOFT-VOTING ENSEMBLES)
# ─────────────────────────────────────────────────────────────────────────────
def build_sentiment_model() -> VotingClassifier:
    """Soft-voting ensemble for Sentiment: Logistic Regression + Calibrated LinearSVC + MNB"""
    lr = LogisticRegression(C=1.0, max_iter=1000, class_weight="balanced", random_state=RANDOM_STATE)
    svc = CalibratedClassifierCV(LinearSVC(C=0.8, max_iter=2000, class_weight="balanced", random_state=RANDOM_STATE), cv=3)
    mnb = MultinomialNB(alpha=0.1)
    return VotingClassifier(
        estimators=[("lr", lr), ("svc", svc), ("mnb", mnb)],
        voting="soft",
        weights=[2, 2, 1],
    )


def build_topic_model() -> VotingClassifier:
    """Soft-voting ensemble for Topic: Logistic Regression + Calibrated LinearSVC + GradientBoosting"""
    lr = LogisticRegression(C=1.0, max_iter=1000, class_weight="balanced", random_state=RANDOM_STATE)
    svc = CalibratedClassifierCV(LinearSVC(C=1.0, max_iter=2000, class_weight="balanced", random_state=RANDOM_STATE), cv=3)
    gb = GradientBoostingClassifier(n_estimators=200, max_depth=5, learning_rate=0.1, random_state=RANDOM_STATE)
    return VotingClassifier(
        estimators=[("lr", lr), ("svc", svc), ("gb", gb)],
        voting="soft",
        weights=[2, 2, 1],
    )


# ─────────────────────────────────────────────────────────────────────────────
# 5. MODEL SERIALIZATION & BINARY VERIFICATION
# ─────────────────────────────────────────────────────────────────────────────
def serialize_artifact(obj, filepath: Path, name: str):
    """Dumps model using joblib with zlib-level compression and verifies reload integrity."""
    print(f"\n[SERIALIZE] Compiling and saving: {name} -> {filepath}")
    joblib.dump(obj, filepath, compress=3)

    file_bytes = filepath.read_bytes()
    md5 = hashlib.md5(file_bytes).hexdigest()
    file_size = filepath.stat().st_size

    # Automated reload verification
    reloaded = joblib.load(filepath)
    assert reloaded is not None, f"CORRUPTION ERROR: {name} failed deserialization!"
    if hasattr(obj, "predict"):
        assert hasattr(reloaded, "predict"), f"ASSERTION FAILED: {name} missing .predict()"
    if hasattr(obj, "transform"):
        assert hasattr(reloaded, "transform"), f"ASSERTION FAILED: {name} missing .transform()"

    print(f"  ✓ Integrity confirmed: {file_size:,} bytes | MD5: {md5}")
    return md5, file_size
