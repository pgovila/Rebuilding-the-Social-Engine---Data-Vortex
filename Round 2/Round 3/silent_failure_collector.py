#!/usr/bin/env python3
"""
Data Vortex Round 3 — Deliverable 1
Multi-Platform Data Extraction Code
Topic: "The Silent Failure Situation"

Simulates scraping Reddit, X, and News APIs for silent-failure phrases,
normalizes cross-platform payloads, and appends model-driven sentiment/topic
predictions using the Round 2 saved pipeline artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import logging
import sys
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd
import joblib

# Local helpers from the Round 3 workspace
sys.path.insert(0, str(Path(__file__).resolve().parent))
from text_standardizer import normalize_platform_text  # noqa: E402
from temporal_parsing import enforce_iso_timeline       # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("silent_failure_collector")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
QUERY_PHRASES = [
    "silent failure",
    "unlogged error",
    "system degradation",
    "memory leak anomaly",
]

PLATFORMS = ["Reddit", "X", "News_API"]

BASE_TIME = datetime(2026, 9, 20, 6, 0, 0, tzinfo=timezone.utc)

# Default synthetic volume — large enough for a time-series slice
DEFAULT_ROWS = 120


# ---------------------------------------------------------------------------
# Platform-specific scraper stubs (production-ready structure; simulated data)
# ---------------------------------------------------------------------------
def _make_text_id(platform: str, ts: datetime, suffix: str) -> str:
    digest = hashlib.sha256(f"{platform}:{ts.isoformat()}:{suffix}".encode()).hexdigest()[:10]
    return f"{platform[:3].upper()}_{digest}"


def _engagement_distribution(platform: str) -> tuple[int, int]:
    """Return realistic (likes, shares) ranges per platform."""
    ranges = {
        "Reddit": (50, 2_500),
        "X": (20, 5_000),
        "News_API": (100, 8_000),
    }
    low, high = ranges[platform]
    likes = int(np.random.randint(low, high + 1))
    shares = int(np.random.randint(0, max(1, likes // 2)))
    return likes, shares


def _timestamp_window(base: datetime, spread_hours: float = 24.0) -> datetime:
    offset = np.random.exponential(scale=spread_hours / 4, size=())[()] if False else np.random.uniform(0, spread_hours)
    return base + timedelta(hours=float(offset))


# Templates per phrase to keep semantics coherent
TEMPLATES: Dict[str, List[Dict[str, Any]]] = {
    "silent failure": [
        {"platforms": ["Reddit", "X"], "role": "user_complaint",
         "text": "Our production cluster hit a silent failure last night — no alerts, just 500s from 02:00 to 05:00 UTC. Customers noticed before ops did."},
        {"platforms": ["News_API", "Reddit"], "role": "technical_feedback",
         "text": "Post-mortem: silent failure in the connection-pool manager masked node dropouts for 4 hours. Memory metrics looked green the whole time."},
        {"platforms": ["X"], "role": "corporate_statement",
         "text": "Update: we identified the silent failure root cause and deployed a quiet hotfix at 09:30 UTC. Monitoring is back to normal."},
        {"platforms": ["Reddit", "X"], "role": "user_complaint",
         "text": "Still seeing silent failure on the /api/v2/stream endpoint. No logs, no exceptions, just empty responses."},
        {"platforms": ["X", "News_API", "Reddit"], "role": "resolution",
         "text": "All-clear: hotfix deployed, services nominal, memory stable. Silent failure fully resolved. Monitoring stays green."},
    ],
    "unlogged error": [
        {"platforms": ["Reddit"], "role": "technical_feedback",
         "text": "Found an unlogged error path in the new retry wrapper — requests fail but the logger swallows the traceback. Has anyone else seen this?"},
        {"platforms": ["X", "News_API"], "role": "user_complaint",
         "text": "Unlogged error spikes every 15 min on the payment service. Finance team flagged it because receipts never arrived."},
        {"platforms": ["Reddit"], "role": "technical_feedback",
         "text": "Unlogged error in the ML inference worker: OOM killed after 20 min, no stderr, no crash dump. Memory leak anomaly suspected."},
        {"platforms": ["X"], "role": "resolution",
         "text": "Hotfix deployed: unlogged error path patched. No recurrence in the last hour. All clear."},
    ],
    "system degradation": [
        {"platforms": ["News_API"], "role": "corporate_statement",
         "text": "We are investigating reports of system degradation affecting API latency in the EU region. All services remain writable."},
        {"platforms": ["Reddit", "X"], "role": "user_complaint",
         "text": "System degradation since the last deploy — p99 latency jumped 6x and dashboards still show green. This is invisible ops."},
        {"platforms": ["X"], "role": "technical_feedback",
         "text": "System degradation trace: DB connection pool exhaustion -> queue backup -> silent failure cascade. Full timeline attached."},
        {"platforms": ["News_API", "X"], "role": "resolution",
         "text": "Incident closed: system degradation resolved after DB pool tuning. Latency back to baseline."},
    ],
    "memory leak anomaly": [
        {"platforms": ["Reddit"], "role": "technical_feedback",
         "text": "Memory leak anomaly confirmed in the Go worker: RSS grows 8 MB/hr even with idle queues. Restarting is the only workaround."},
        {"platforms": ["X", "News_API"], "role": "user_complaint",
         "text": "Memory leak anomaly caused two consecutive silent failures in the ingestion pipeline. Data loss estimate: 12 k events."},
        {"platforms": ["Reddit"], "role": "technical_feedback",
         "text": "Heap profile shows the memory leak anomaly lives in the protobuf decoder. PR incoming."},
        {"platforms": ["X", "News_API"], "role": "resolution",
         "text": "Memory leak anomaly patched in v2.4. Heap stable, no further OOM kills. All services recovered."},
    ],
}

ROLES = {
    "user_complaint": "user_complaint",
    "technical_feedback": "technical_feedback",
    "corporate_statement": "corporate_statement",
}


def scrape_reddit(phrases: List[str], n: int, seed: int = 42) -> List[Dict[str, Any]]:
    """Simulate Reddit API pagination and return normalized records."""
    rng = np.random.default_rng(seed)
    records: List[Dict[str, Any]] = []
    page = 0
    per_page = 25
    generated = 0
    while generated < n:
        page += 1
        for phrase in phrases:
            for tmpl in TEMPLATES[phrase]:
                if "Reddit" not in tmpl["platforms"]:
                    continue
                if generated >= n:
                    break
                ts = BASE_TIME + timedelta(hours=float(rng.uniform(0, 24)))
                likes, shares = _engagement_distribution("Reddit")
                records.append({
                    "text_id": _make_text_id("Reddit", ts, tmpl["role"]),
                    "platform_source": "Reddit",
                    "ISO_timestamp": ts.isoformat(),
                    "raw_post_text": f"{tmpl['text']} [phrase='{phrase}']",
                    "engagement_likes": int(likes),
                    "engagement_shares": int(shares),
                    "role": tmpl["role"],
                })
                generated += 1
        if page * per_page >= n * 2:
            break
    return records


def scrape_x(phrases: List[str], n: int, seed: int = 43) -> List[Dict[str, Any]]:
    """Simulate X (Twitter) API with heavier engagement variance."""
    rng = np.random.default_rng(seed)
    records: List[Dict[str, Any]] = []
    page = 0
    per_page = 20
    generated = 0
    while generated < n:
        page += 1
        for phrase in phrases:
            for tmpl in TEMPLATES[phrase]:
                if "X" not in tmpl["platforms"]:
                    continue
                if generated >= n:
                    break
                ts = BASE_TIME + timedelta(hours=float(rng.uniform(0, 24)))
                likes, shares = _engagement_distribution("X")
                records.append({
                    "text_id": _make_text_id("X", ts, tmpl["role"]),
                    "platform_source": "X",
                    "ISO_timestamp": ts.isoformat(),
                    "raw_post_text": f"{tmpl['text']} #silentfailure [phrase='{phrase}']",
                    "engagement_likes": int(likes),
                    "engagement_shares": int(shares),
                    "role": tmpl["role"],
                })
                generated += 1
        if page * per_page >= n * 2:
            break
    return records


def scrape_news_api(phrases: List[str], n: int, seed: int = 44) -> List[Dict[str, Any]]:
    """Simulate News/aggregator API payloads."""
    rng = np.random.default_rng(seed)
    records: List[Dict[str, Any]] = []
    page = 0
    per_page = 10
    generated = 0
    while generated < n:
        page += 1
        for phrase in phrases:
            for tmpl in TEMPLATES[phrase]:
                if "News_API" not in tmpl["platforms"]:
                    continue
                if generated >= n:
                    break
                ts = BASE_TIME + timedelta(hours=float(rng.uniform(0, 24)))
                likes, shares = _engagement_distribution("News_API")
                records.append({
                    "text_id": _make_text_id("News", ts, tmpl["role"]),
                    "platform_source": "News_API",
                    "ISO_timestamp": ts.isoformat(),
                    "raw_post_text": f"[News] {tmpl['text']} source=engineering-blog phrase={phrase}",
                    "engagement_likes": int(likes),
                    "engagement_shares": int(shares),
                    "role": tmpl["role"],
                })
                generated += 1
        if page * per_page >= n * 2:
            break
    return records


# ---------------------------------------------------------------------------
# Model inference
# ---------------------------------------------------------------------------
def _resolve_model_path(name: str, search_dirs: List[Path]) -> Path:
    for d in search_dirs:
        candidate = d / name
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"Could not find {name} in: {[str(d) for d in search_dirs]}"
    )


def load_pipeline_models(workspace: Path) -> tuple[Any, Any, Any]:
    """Load sentiment/topic models + vectorizer with cross-directory fallback."""
    # workspace = Round 3/ ; its parent is Round 2/ where artifacts live.
    root = workspace.resolve().parent  # Round 2/
    search = [
        root,
        workspace,
        workspace / "models",
    ]
    search = [d.resolve() for d in search]
    vec_path = _resolve_model_path("tfidf_vectorizer.pkl", search)
    sent_path = _resolve_model_path("sentiment_classifier_model.pkl", search)
    topic_path = _resolve_model_path("topic_classifier_model.pkl", search)

    log.info("Loading vectorizer from %s", vec_path)
    vectorizer = joblib.load(vec_path)
    log.info("Loading sentiment model from %s", sent_path)
    sentiment_model = joblib.load(sent_path)
    log.info("Loading topic model from %s", topic_path)
    topic_model = joblib.load(topic_path)
    return vectorizer, sentiment_model, topic_model


def run_inference(
    df: pd.DataFrame,
    vectorizer: Any,
    sentiment_model: Any,
    topic_model: Any,
) -> pd.DataFrame:
    """Apply normalized text to saved models and append prediction flags."""
    if df.empty:
        df["predicted_sentiment"] = pd.Series(dtype=str)
        df["predicted_topic"] = pd.Series(dtype=str)
        return df

    # Prefer the Round 2 training cleaning function so inference stays
    # compatible with the saved pipeline vocabulary.
    try:
        from nlp_pipeline import clean_text as _clean  # type: ignore[import-untyped]
    except Exception:  # noqa: BLE001
        _clean = normalize_platform_text

    texts = df["raw_post_text"].fillna("").astype(str).tolist()
    normalized = [_clean(t) for t in texts]
    normalized = [t if t.strip() else "<empty>" for t in normalized]

    X = vectorizer.transform(normalized)
    df = df.copy()
    df["predicted_sentiment"] = sentiment_model.predict(X)
    df["predicted_topic"] = topic_model.predict(X)
    return df


def _sample_role(phrase: str, phase: str, platform: str, rng: Any) -> str:
    """Pick a role weighted by narrative phase."""
    options = TEMPLATES[phrase]
    filtered = [o for o in options if platform in o["platforms"]]
    if not filtered:
        filtered = options
    if phase == "baseline":
        weights = [3 if o["role"] == "technical_feedback" else 1 for o in filtered]
    elif phase == "crisis":
        weights = [3 if o["role"] == "user_complaint" else 1 for o in filtered]
    else:  # recovery
        weights = [4 if o["role"] == "resolution" else (2 if o["role"] == "corporate_statement" else 1) for o in filtered]
    total = sum(weights)
    r = rng.uniform(0, total)
    cum = 0.0
    for o, w in zip(filtered, weights):
        cum += w
        if r <= cum:
            return o["role"]
    return filtered[0]["role"]


def _narrative_timestamps(n: int, rng: Any) -> np.ndarray:
    """Generate timestamps following the silent-failure narrative arc."""
    phases = [
        # (start_hour, end_hour, hourly_rate)
        (0.0, 4.0, 1.8),    # baseline: low, steady
        (4.0, 9.0, 12.0),   # anomaly onset: sharp spike
        (9.0, 11.5, 6.0),   # sustained crisis chatter
        (11.5, 14.5, 2.5),  # hotfix + recovery
    ]
    samples = []
    for start_h, end_h, rate in phases:
        duration = end_h - start_h
        count = max(1, int(rng.poisson(rate * duration)))
        offsets = rng.uniform(start_h, end_h, size=count)
        samples.extend(offsets.tolist())
    # Trim/extend to exactly n
    samples = np.array(samples)
    if len(samples) > n:
        samples = np.sort(samples)[:n]
    elif len(samples) < n:
        extra = rng.uniform(0.0, 14.5, size=n - len(samples))
        samples = np.concatenate([samples, extra])
    return np.sort(samples)


def build_narrative_dataset(n_rows: int = DEFAULT_ROWS, seed: int = 42) -> pd.DataFrame:
    """Build a story-driven dataset: baseline -> crisis spike -> recovery."""
    rng = np.random.default_rng(seed)
    offsets = _narrative_timestamps(n_rows, rng=rng)
    records: List[Dict[str, Any]] = []

    # Phase label derived from hour
    def phase_of(hour: float) -> str:
        if hour < 4.0:
            return "baseline"
        if hour < 9.0:
            return "crisis"
        return "recovery"

    for offset in offsets:
        ts = BASE_TIME + timedelta(hours=float(offset))
        hour = offset
        phase = phase_of(hour)
        phrase = QUERY_PHRASES[int(rng.integers(0, len(QUERY_PHRASES)))]
        platform = PLATFORMS[int(rng.integers(0, len(PLATFORMS)))]
        role = _sample_role(phrase, phase, platform, rng)
        tmpl_text = next(
            (t["text"] for t in TEMPLATES[phrase] if t["role"] == role and platform in t["platforms"]),
            TEMPLATES[phrase][0]["text"],
        )
        likes, shares = _engagement_distribution(platform)
        # Boost engagement during crisis phase
        if phase == "crisis":
            likes = int(likes * rng.uniform(1.5, 3.0))
            shares = int(shares * rng.uniform(1.5, 3.0))
        records.append({
            "text_id": _make_text_id(platform, ts, role),
            "platform_source": platform,
            "ISO_timestamp": ts.isoformat(),
            "raw_post_text": f"{tmpl_text} [phrase='{phrase}']",
            "engagement_likes": likes,
            "engagement_shares": shares,
            "role": role,
        })

    log.info("Narrative records generated: %d", len(records))
    df = pd.DataFrame(records)
    df = enforce_iso_timeline(df, date_column="ISO_timestamp")

    workspace = Path(__file__).resolve().parent
    vectorizer, sentiment_model, topic_model = load_pipeline_models(workspace)
    df = run_inference(df, vectorizer, sentiment_model, topic_model)

    columns = [
        "text_id", "platform_source", "ISO_timestamp", "raw_post_text",
        "engagement_likes", "engagement_shares", "predicted_sentiment",
        "predicted_topic",
    ]
    df = df[columns]
    return df


# ---------------------------------------------------------------------------
# Pipeline orchestration
# ---------------------------------------------------------------------------
def build_pipeline(n_rows: int = DEFAULT_ROWS, seed: int = 42, narrative: bool = True) -> pd.DataFrame:
    if narrative:
        return build_narrative_dataset(n_rows=n_rows, seed=seed)
    rng = np.random.default_rng(seed)
    per_platform = max(1, n_rows // len(PLATFORMS))
    remainder = n_rows - per_platform * (len(PLATFORMS) - 1)

    log.info("Scraping Reddit (%d rows)...", per_platform)
    records = scrape_reddit(QUERY_PHRASES, per_platform, seed=rng.integers(0, 2**31))
    log.info("Scraping X (%d rows)...", per_platform)
    records += scrape_x(QUERY_PHRASES, per_platform, seed=rng.integers(0, 2**31))
    log.info("Scraping News_API (%d rows)...", remainder)
    records += scrape_news_api(QUERY_PHRASES, remainder, seed=rng.integers(0, 2**31))

    log.info("Raw records collected: %d", len(records))
    df = pd.DataFrame(records)
    df = enforce_iso_timeline(df, date_column="ISO_timestamp")

    workspace = Path(__file__).resolve().parent
    vectorizer, sentiment_model, topic_model = load_pipeline_models(workspace)
    df = run_inference(df, vectorizer, sentiment_model, topic_model)

    columns = [
        "text_id", "platform_source", "ISO_timestamp", "raw_post_text",
        "engagement_likes", "engagement_shares", "predicted_sentiment",
        "predicted_topic",
    ]
    df = df[columns]
    return df


def save_dataset(df: pd.DataFrame, out_path: Path) -> None:
    df.to_csv(out_path, index=False)
    log.info("Saved dataset with %d rows -> %s", len(df), out_path)


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Data Vortex Round 3 — Silent Failure multi-platform collector"
    )
    parser.add_argument(
        "--rows", type=int, default=DEFAULT_ROWS,
        help="Number of synthetic records to generate (default: %(default)s)",
    )
    parser.add_argument(
        "--output", type=str, default="silent_failure_raw_dataset.csv",
        help="Output CSV path",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    df = build_pipeline(n_rows=args.rows, seed=args.seed)
    save_dataset(df, Path(args.output))
    print(df.head(3).to_string())
    print(f"\nRows: {len(df)} | Platforms: {sorted(df['platform_source'].unique())}")
    print(f"Sentiment distribution:\n{df['predicted_sentiment'].value_counts().to_string()}")
    print(f"Topic distribution:\n{df['predicted_topic'].value_counts().to_string()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
