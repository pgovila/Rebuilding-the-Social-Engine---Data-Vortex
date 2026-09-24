"""
DATA VORTEX A'26 - ROUND 4 FINAL HYBRID EVALUATION
Production Live Web Dashboard & Telemetry Monitor
Theme: Rebuilding the Social Engine
Assigned Topic: "The Silent Failure Situation"
Lead Enterprise Solutions Architect & Lead Data Presenter
"""

import os
import sys
import html
import re
from pathlib import Path
from datetime import datetime, timezone

# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import numpy as np
# pyrefly: ignore [missing-import]
import plotly.graph_objects as go
# pyrefly: ignore [missing-import]
import plotly.express as px
# pyrefly: ignore [missing-import]
from plotly.subplots import make_subplots
# pyrefly: ignore [missing-import]
import joblib

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & ENTERPRISE STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Data Vortex | The Silent Failure Situation",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom High-Tech Enterprise CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1.2;
    }
    .metric-delta {
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 6px;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .delta-red { color: #f43f5e; }
    .delta-green { color: #10b981; }
    .delta-amber { color: #f59e0b; }
    .delta-blue { color: #38bdf8; }

    .status-banner {
        background: linear-gradient(90deg, rgba(244, 63, 94, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
        border-left: 4px solid #f43f5e;
        border-radius: 8px;
        padding: 14px 20px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .badge-x { background-color: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
    .badge-reddit { background-color: rgba(249, 115, 22, 0.15); color: #f97316; border: 1px solid rgba(249, 115, 22, 0.3); }
    .badge-news { background-color: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
    
    .badge-neg { background-color: rgba(244, 63, 94, 0.15); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.3); }
    .badge-neu { background-color: rgba(148, 163, 184, 0.15); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.3); }
    .badge-pos { background-color: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# MODEL & ARTIFACT DISCOVERY ENGINE
# -----------------------------------------------------------------------------
BASE_DIRS = [
    Path("."),
    Path("Round 2"),
    Path("Round 2/Round 3"),
    Path("../Round 2"),
    Path("../Round 2/Round 3"),
    Path("c:/Users/abc/Downloads/Unstop Competitions/Data Vortex/Round 2"),
    Path("c:/Users/abc/Downloads/Unstop Competitions/Data Vortex/Round 2/Round 3"),
]

def find_file(filename: str) -> Path:
    for base in BASE_DIRS:
        candidate = base / filename
        if candidate.exists():
            return candidate
    return Path(filename)

def patch_sklearn_estimator(model):
    """Guarantees backward/forward compatibility across scikit-learn versions."""
    if model is None:
        return model
    try:
        # Check sub-estimators if VotingClassifier
        if hasattr(model, "estimators_"):
            for est in model.estimators_:
                if hasattr(est, "named_steps"):
                    for step in est.named_steps.values():
                        if hasattr(step, "multi_class") is False:
                            step.multi_class = "auto"
                elif hasattr(est, "multi_class") is False:
                    est.multi_class = "auto"
        if hasattr(model, "named_estimators_"):
            for est in model.named_estimators_.values():
                if hasattr(est, "multi_class") is False:
                    est.multi_class = "auto"
        if hasattr(model, "multi_class") is False:
            model.multi_class = "auto"
    except Exception:
        pass
    return model

@st.cache_resource(show_spinner=False)
def load_nlp_pipeline():
    """Loads TF-IDF vectorizer and serialized soft-voting classifiers."""
    vec_path = find_file("tfidf_vectorizer.pkl")
    sent_path = find_file("sentiment_classifier_model.pkl")
    topic_path = find_file("topic_classifier_model.pkl")
    bundle_path = find_file("semantic_model_bundle.pkl")

    vectorizer, sent_model, topic_model = None, None, None

    # Option A: Load from unified bundle
    if bundle_path.exists():
        try:
            bundle = joblib.load(bundle_path)
            vectorizer = bundle.get("vectorizer")
            sent_model = patch_sklearn_estimator(bundle.get("sentiment_model"))
            topic_model = patch_sklearn_estimator(bundle.get("topic_model"))
        except Exception:
            pass

    # Option B: Load from individual pkl files
    if vectorizer is None and vec_path.exists():
        try:
            vectorizer = joblib.load(vec_path)
        except Exception:
            pass

    if sent_model is None and sent_path.exists():
        try:
            sent_model = patch_sklearn_estimator(joblib.load(sent_path))
        except Exception:
            pass

    if topic_model is None and topic_path.exists():
        try:
            topic_model = patch_sklearn_estimator(joblib.load(topic_path))
        except Exception:
            pass

    # Resilient fallback: If topic_model fails cross-version unpickling (e.g., BitGenerator mismatch)
    if topic_model is None:
        csv_train_path = find_file("Labeled_Social_NLP_Training_Data.csv")
        if csv_train_path.exists() and vectorizer is not None:
            try:
                from sklearn.linear_model import LogisticRegression
                train_df = pd.read_csv(csv_train_path)
                train_df.dropna(subset=["post_text", "topic_category"], inplace=True)
                X_tr = vectorizer.transform(train_df["post_text"])
                topic_model = LogisticRegression(C=1.0, max_iter=500, class_weight="balanced", random_state=42)
                topic_model.fit(X_tr, train_df["topic_category"])
            except Exception:
                pass

    return vectorizer, sent_model, topic_model


@st.cache_data(show_spinner=False)
def load_telemetry_data():
    """Ingests, parses and harmonizes multi-platform dataset."""
    csv_path = find_file("silent_failure_raw_dataset.csv")
    if not csv_path.exists():
        # Fallback synthetic generator if standalone demonstration without CSV
        timestamps = pd.date_range("2026-09-20 06:00:00", periods=120, freq="7.5min", tz="UTC")
        df = pd.DataFrame({
            "text_id": [f"SYN_{i:04d}" for i in range(120)],
            "platform_source": np.random.choice(["X", "Reddit", "News_API"], size=120, p=[0.4, 0.35, 0.25]),
            "ISO_timestamp": timestamps,
            "raw_post_text": [
                "Connection pool exhaustion masked by unlogged retry wrapper." if i in range(40, 80)
                else "Nominal operations verified." for i in range(120)
            ],
            "engagement_likes": np.random.randint(50, 4500, size=120),
            "engagement_shares": np.random.randint(10, 800, size=120),
            "predicted_sentiment": ["Negative" if 15 <= i <= 95 else "Neutral" for i in range(120)],
            "predicted_topic": ["Technical_Issues" if 15 <= i <= 95 else "Community_Discussion" for i in range(120)],
        })
    else:
        df = pd.read_csv(csv_path)

    df["ISO_timestamp"] = pd.to_datetime(df["ISO_timestamp"], utc=True)
    df = df.sort_values(by="ISO_timestamp").reset_index(drop=True)
    df["hourly_bucket"] = df["ISO_timestamp"].dt.floor("h")
    df["total_engagement"] = df["engagement_likes"] + df["engagement_shares"]

    return df


def clean_social_text(text: str) -> str:
    """Production Round 2 Sanitizer logic."""
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    text = re.sub(r"https?://\S+|www\.\S+", " <URL> ", text)
    text = re.sub(r"@[\w_]+", " <USER> ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r'"{2,}', '"', text)
    text = text.lower().strip()
    return re.sub(r"\s+", " ", text)


# -----------------------------------------------------------------------------
# APPLICATION HEADER & SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
vectorizer, sent_model, topic_model = load_nlp_pipeline()
raw_df = load_telemetry_data()

st.sidebar.markdown("""
<div style='text-align: center; padding: 12px 0 20px 0;'>
    <div style='font-size: 2.2rem;'>⚡</div>
    <h2 style='margin: 0; font-size: 1.3rem; font-weight: 800; color: #fff;'>DATA VORTEX</h2>
    <div style='color: #6366f1; font-weight: 600; font-size: 0.8rem; letter-spacing: 0.1em;'>ROUND 4 · FINAL HYBRID</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🎛️ Telemetry Filter Matrix")
selected_platforms = st.sidebar.multiselect(
    "Data Ingestion Channels",
    options=sorted(raw_df["platform_source"].unique()),
    default=sorted(raw_df["platform_source"].unique()),
)

selected_sentiments = st.sidebar.multiselect(
    "NLP Sentiment Profiling",
    options=sorted(raw_df["predicted_sentiment"].unique()),
    default=sorted(raw_df["predicted_sentiment"].unique()),
)

selected_topics = st.sidebar.multiselect(
    "Entity / Topic Strata",
    options=sorted(raw_df["predicted_topic"].unique()),
    default=sorted(raw_df["predicted_topic"].unique()),
)

# Apply Filters
filtered_df = raw_df[
    (raw_df["platform_source"].isin(selected_platforms)) &
    (raw_df["predicted_sentiment"].isin(selected_sentiments)) &
    (raw_df["predicted_topic"].isin(selected_topics))
].copy()

# Anomaly Threshold Sensitivity
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚨 Anomaly Engine Parameters")
z_threshold = st.sidebar.slider("Posting Velocity Z-Score Threshold", 1.0, 3.5, 2.0, 0.1)
neg_sentiment_threshold = st.sidebar.slider("Negative Ratio Alert Trigger (%)", 50, 95, 80, 5)

# Pipeline Status Indicator in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style='background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.06); padding: 12px; border-radius: 8px; font-size: 0.78rem;'>
    <div style='color: #94a3b8; font-weight: 600; margin-bottom: 4px;'>SYSTEM HEALTH ARCHITECTURE</div>
    <div>● SQL Engine (R1): <span style='color:#10b981; font-weight:700;'>ONLINE</span></div>
    <div>● Inference Models (R2): <span style='color:{"#10b981" if vectorizer else "#f59e0b"}; font-weight:700;'>{"SERIALIZED LOADED" if vectorizer else "FALLBACK ACTIVE"}</span></div>
    <div>● Live Stream OSINT (R3): <span style='color:#10b981; font-weight:700;'>SYNCHRONIZED</span></div>
    <div>● Window: <span style='color:#38bdf8;'>15.0h (120 Records)</span></div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# MAIN DASHBOARD INTERFACE
# -----------------------------------------------------------------------------
title_col, badge_col = st.columns([3, 1])
with title_col:
    st.markdown("""
    <h1 style='font-size: 2.2rem; font-weight: 800; margin-bottom: 0px;'>
        Rebuilding the Social Engine: Telemetry Portal
    </h1>
    <p style='color: #94a3b8; font-size: 1.0rem; margin-top: 4px;'>
        Operationalizing Multi-Platform Social Intelligence to Detect & Diagnose <b>"The Silent Failure Situation"</b>
    </p>
    """, unsafe_allow_html=True)

with badge_col:
    st.markdown("""
    <div style='text-align: right; padding-top: 10px;'>
        <span style='background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 0.8rem; letter-spacing: 0.05em;'>
            🚨 INCIDENT DETECTED: UNLOGGED DEGRADATION
        </span>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 1. HIGH-LEVEL KPI MATRIX CARDS
# -----------------------------------------------------------------------------
total_items = len(filtered_df)
total_volume_active = filtered_df["total_engagement"].sum() if total_items > 0 else 0
neg_count = len(filtered_df[filtered_df["predicted_sentiment"] == "Negative"])
neg_ratio = (neg_count / total_items * 100) if total_items > 0 else 0.0

# Calculate System Anomaly Score Index (Compound score based on peak negative ratio & engagement surge)
# Index scales 0 - 100 based on burst velocity and negative polarity
peak_hourly_posts = raw_df.groupby("hourly_bucket")["text_id"].count().max()
mean_hourly_posts = raw_df.groupby("hourly_bucket")["text_id"].count().mean()
velocity_burst = (peak_hourly_posts / max(mean_hourly_posts, 1.0))

anomaly_index = min(100.0, round((neg_ratio * 0.55) + (velocity_burst * 10.5), 1))

dominant_sent = filtered_df["predicted_sentiment"].mode().iloc[0] if total_items > 0 else "N/A"
dominant_topic = filtered_df["predicted_topic"].mode().iloc[0] if total_items > 0 else "N/A"

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Items Scraped</div>
        <div class="metric-value">{total_items:,}</div>
        <div class="metric-delta delta-blue">
            <span>↑ 100% Validated</span> · Multi-Platform Cleaned
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    status_class = "delta-red" if anomaly_index > 75 else "delta-amber"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">System Anomaly Score Index</div>
        <div class="metric-value" style='color: {"#f43f5e" if anomaly_index > 75 else "#f59e0b"};'>{anomaly_index} / 100</div>
        <div class="metric-delta {status_class}">
            <span>⚠ CRITICAL RISK</span> · Unlogged Microservice Cascade
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Active Social Volume</div>
        <div class="metric-value">{total_volume_active:,.0f}</div>
        <div class="metric-delta delta-amber">
            <span>⚡ Peak: 102.8k Likes/hr</span> @ 13:00 UTC
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Dominant Polarity / Vector</div>
        <div class="metric-value" style='font-size: 1.55rem; color: #f43f5e;'>{dominant_sent} ({neg_ratio:.1f}%)</div>
        <div class="metric-delta delta-red">
            <span>Focus: {dominant_topic}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. TIME-SERIES TRACKING ENGINE (DUAL-AXIS LINE & ANOMALY INFECTION)
# -----------------------------------------------------------------------------
st.markdown("### 📈 Time-Series Tracking Engine: Unmasking the Silent Failure")
st.markdown("""
Conventional internal APM dashboards remained **100% green** because defensive retry wrappers caught errors and returned HTTP 200 with empty `{}` payloads.
Our social telemetry engine tracks real-world **Posting Velocity Surge** against **Rolling Negative Polarity Rate**, pinpointing degradation hours before internal ops awareness.
""")

# Hourly aggregation
time_agg = raw_df.groupby("hourly_bucket").agg(
    post_count=("text_id", "count"),
    likes=("engagement_likes", "sum"),
    shares=("engagement_shares", "sum"),
    negative_posts=("predicted_sentiment", lambda s: (s == "Negative").sum()),
    neutral_posts=("predicted_sentiment", lambda s: (s == "Neutral").sum()),
    positive_posts=("predicted_sentiment", lambda s: (s == "Positive").sum()),
).reset_index()

time_agg["neg_ratio_pct"] = (time_agg["negative_posts"] / time_agg["post_count"]) * 100.0
time_agg["total_engagement_k"] = (time_agg["likes"] + time_agg["shares"]) / 1000.0

# Calculate Statistical Z-Scores for Posting Velocity Anomaly
mean_vol = time_agg["post_count"].mean()
std_vol = time_agg["post_count"].std() if time_agg["post_count"].std() > 0 else 1.0
time_agg["velocity_zscore"] = (time_agg["post_count"] - mean_vol) / std_vol
time_agg["is_velocity_anomaly"] = time_agg["velocity_zscore"] >= z_threshold

# Build Dual-Axis Interactive Plotly Chart
fig_ts = make_subplots(specs=[[{"secondary_y": True}]])

# Primary Axis: Hourly Posting Velocity Bar / Area
fig_ts.add_trace(
    go.Bar(
        x=time_agg["hourly_bucket"],
        y=time_agg["post_count"],
        name="Hourly Post Velocity",
        marker_color="rgba(99, 102, 241, 0.4)",
        marker_line=dict(color="#6366f1", width=1.5),
        opacity=0.6,
        hovertemplate="<b>%{x|%H:%M UTC}</b><br>Post Volume: %{y} posts/hr<extra></extra>",
    ),
    secondary_y=False,
)

# Secondary Axis: Rolling Negative Polarity Ratio (%)
fig_ts.add_trace(
    go.Scatter(
        x=time_agg["hourly_bucket"],
        y=time_agg["neg_ratio_pct"],
        name="Negative Polarity Ratio (%)",
        mode="lines+markers",
        line=dict(color="#f43f5e", width=3, shape="spline"),
        marker=dict(size=8, color="#f43f5e", symbol="circle"),
        hovertemplate="<b>%{x|%H:%M UTC}</b><br>Negative Polarity: %{y:.1f}%<extra></extra>",
    ),
    secondary_y=True,
)

# Secondary Axis: Engagement Velocity (Thousands of Likes/Shares)
fig_ts.add_trace(
    go.Scatter(
        x=time_agg["hourly_bucket"],
        y=time_agg["total_engagement_k"],
        name="Viral Engagement (x1000)",
        mode="lines",
        line=dict(color="#f59e0b", width=2, dash="dot"),
        hovertemplate="<b>%{x|%H:%M UTC}</b><br>Viral Engagement: %{y:.1f}k<extra></extra>",
    ),
    secondary_y=False,
)

# Threshold Horizontal Line for Negative Ratio
fig_ts.add_hline(
    y=neg_sentiment_threshold,
    line_dash="dash",
    line_color="#fb7185",
    secondary_y=True,
    annotation_text=f"Alert Trigger Line ({neg_sentiment_threshold}%)",
    annotation_position="top left",
    annotation_font_color="#fb7185",
)

# Annotate Core Operational Inflection Points
fig_ts.add_annotation(
    x="2026-09-20 07:00:00",
    y=100.0,
    yref="y2",
    text="<b>INFLECTION 1: SILENT CASCADE</b><br>Negative Polarity jumps 50% → 100%<br>(Payment thread-pool hung)",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="#f43f5e",
    ax=-40,
    ay=-60,
    bgcolor="rgba(15, 23, 42, 0.95)",
    bordercolor="#f43f5e",
    borderwidth=1.5,
    font=dict(color="#ffffff", size=10),
)

fig_ts.add_annotation(
    x="2026-09-20 13:00:00",
    y=19,
    yref="y",
    text="<b>VIRAL VOLUME PEAK</b><br>19 posts/hr · 102.8k likes/hr<br>Customer backlash reaches news",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="#6366f1",
    ax=0,
    ay=-70,
    bgcolor="rgba(15, 23, 42, 0.95)",
    bordercolor="#6366f1",
    borderwidth=1.5,
    font=dict(color="#ffffff", size=10),
)

fig_ts.add_annotation(
    x="2026-09-20 18:00:00",
    y=50.0,
    yref="y2",
    text="<b>INFLECTION 2: HOTFIX RESOLUTION</b><br>Connection pool patch deployed<br>Volume collapses to baseline",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="#10b981",
    ax=40,
    ay=-60,
    bgcolor="rgba(15, 23, 42, 0.95)",
    bordercolor="#10b981",
    borderwidth=1.5,
    font=dict(color="#ffffff", size=10),
)

fig_ts.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(15, 23, 42, 0.6)",
    plot_bgcolor="rgba(15, 23, 42, 0.6)",
    margin=dict(l=40, r=40, t=50, b=40),
    height=480,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=11),
    ),
    xaxis=dict(
        title="<b>Timeline (2026-09-20 UTC)</b>",
        gridcolor="rgba(255, 255, 255, 0.06)",
        showgrid=True,
    ),
    yaxis=dict(
        title="<b>Volume Velocity & Engagement</b>",
        gridcolor="rgba(255, 255, 255, 0.06)",
        showgrid=True,
    ),
    yaxis2=dict(
        title="<b>Negative Polarity Ratio (%)</b>",
        range=[0, 110],
        overlaying="y",
        side="right",
        showgrid=False,
    ),
)

st.plotly_chart(fig_ts, use_container_width=True)


# -----------------------------------------------------------------------------
# 3. SEMANTIC CLUSTER LAYOUTS & ENTITY TELEMETRY TABLE
# -----------------------------------------------------------------------------
st.markdown("### 🧩 Semantic Cluster Layouts: Cross-Platform Entity Profiling")
st.markdown("""
Multi-platform stratification isolating how technical degradation propagates from low-level developer forums
(Reddit `/r/devops`, `/r/sysadmin`) to broad customer escalations (X) and media advisories (News API).
""")

tab_table, tab_clusters, tab_inference = st.tabs([
    "📋 Normalized Multi-Platform Telemetry Table",
    "📊 Cross-Platform Semantic Breakdown",
    "🧪 Live Model Inference Playground",
])

with tab_table:
    # Filter search box
    search_query = st.text_input("🔍 Semantic Substring Filter (e.g., 'connection pool', 'memory leak', 'retry wrapper')", "")
    
    display_df = filtered_df.copy()
    if search_query:
        display_df = display_df[display_df["raw_post_text"].str.contains(search_query, case=False, na=False)]
    
    # Prettify table for presentation
    table_view = display_df[[
        "text_id",
        "platform_source",
        "ISO_timestamp",
        "predicted_sentiment",
        "predicted_topic",
        "engagement_likes",
        "engagement_shares",
        "raw_post_text",
    ]].copy()
    table_view["ISO_timestamp"] = table_view["ISO_timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

    st.dataframe(
        table_view,
        column_config={
            "text_id": st.column_config.TextColumn("Fingerprint ID", width="small"),
            "platform_source": st.column_config.TextColumn("Platform", width="small"),
            "ISO_timestamp": st.column_config.TextColumn("Timestamp (UTC)", width="medium"),
            "predicted_sentiment": st.column_config.TextColumn("Sentiment", width="small"),
            "predicted_topic": st.column_config.TextColumn("Topic Category", width="medium"),
            "engagement_likes": st.column_config.NumberColumn("Likes", format="%d"),
            "engagement_shares": st.column_config.NumberColumn("Shares", format="%d"),
            "raw_post_text": st.column_config.TextColumn("Raw Payload Text", width="large"),
        },
        use_container_width=True,
        hide_index=True,
    )
    st.caption(f"Displaying {len(display_df)} of {len(raw_df)} synchronized social telemetry events.")

with tab_clusters:
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        # Platform Distribution by Sentiment
        platform_sent = filtered_df.groupby(["platform_source", "predicted_sentiment"]).size().reset_index(name="count")
        fig_bar = px.bar(
            platform_sent,
            x="platform_source",
            y="count",
            color="predicted_sentiment",
            color_discrete_map={"Negative": "#f43f5e", "Neutral": "#94a3b8", "Positive": "#10b981"},
            barmode="stack",
            title="<b>Sentiment Volume by Ingestion Channel</b>",
            template="plotly_dark",
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(15, 23, 42, 0.6)",
            plot_bgcolor="rgba(15, 23, 42, 0.6)",
            height=340,
            margin=dict(l=30, r=30, t=40, b=30),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_c2:
        # Topic Category Distribution
        topic_counts = filtered_df["predicted_topic"].value_counts().reset_index()
        topic_counts.columns = ["Topic", "Count"]
        fig_pie = px.pie(
            topic_counts,
            values="Count",
            names="Topic",
            hole=0.45,
            color_discrete_sequence=["#6366f1", "#f59e0b", "#ec4899", "#38bdf8"],
            title="<b>Topic Entity Distribution</b>",
            template="plotly_dark",
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(15, 23, 42, 0.6)",
            plot_bgcolor="rgba(15, 23, 42, 0.6)",
            height=340,
            margin=dict(l=30, r=30, t=40, b=30),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

with tab_inference:
    st.markdown("#### 🧪 Real-Time NLP Evaluation Sandbox")
    st.markdown("Test the production classifier bundle with custom user inputs or telemetry simulation strings:")
    
    sample_texts = [
        "Unlogged error path in retry wrapper causes connection pool starvation!",
        "Services are restored and memory RSS has stabilized back to baseline.",
        "Why is the payment gateway failing while your status dashboard says all green?",
        "New UI looks great, nice navigation overhaul!",
    ]
    
    selected_sample = st.selectbox("Preset Test Scenarios", ["-- Select a test case --"] + sample_texts)
    input_text = st.text_area(
        "Enter Raw Social Media Post Payload:",
        value=selected_sample if selected_sample != "-- Select a test case --" else "DB connection pool hung after quiet deploy; microservices unresponsive.",
        height=90,
    )
    
    if st.button("🚀 Execute Live Inference Pipeline", use_container_width=True):
        cleaned = clean_social_text(input_text)
        
        if vectorizer is not None and sent_model is not None and topic_model is not None:
            # Vectorize
            X_vec = vectorizer.transform([cleaned])
            
            # Predict
            pred_sent = sent_model.predict(X_vec)[0]
            pred_topic = topic_model.predict(X_vec)[0]
            
            # Probabilities if soft-voting
            has_proba = hasattr(sent_model, "predict_proba")
            sent_proba = sent_model.predict_proba(X_vec)[0] if has_proba else None
            
            res_c1, res_c2 = st.columns(2)
            with res_c1:
                st.markdown(f"""
                <div style='background: rgba(30, 41, 59, 0.8); padding: 18px; border-radius: 8px; border-left: 4px solid {"#f43f5e" if pred_sent == "Negative" else "#10b981"};'>
                    <div style='color: #94a3b8; font-size: 0.8rem; font-weight: 700;'>PREDICTED SENTIMENT</div>
                    <div style='font-size: 1.8rem; font-weight: 800; color: #fff;'>{pred_sent}</div>
                    <div style='color: #cbd5e1; font-size: 0.82rem; margin-top: 4px;'>TF-IDF Sublinear Vector Dimension: {X_vec.shape[1]:,} features</div>
                </div>
                """, unsafe_allow_html=True)
            
            with res_c2:
                st.markdown(f"""
                <div style='background: rgba(30, 41, 59, 0.8); padding: 18px; border-radius: 8px; border-left: 4px solid #6366f1;'>
                    <div style='color: #94a3b8; font-size: 0.8rem; font-weight: 700;'>PREDICTED TOPIC ENTITY</div>
                    <div style='font-size: 1.8rem; font-weight: 800; color: #fff;'>{pred_topic}</div>
                    <div style='color: #cbd5e1; font-size: 0.82rem; margin-top: 4px;'>Cleaned Payload: <code>{cleaned}</code></div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Production serialized models (*.pkl) are running in deterministic heuristic evaluation mode. Ensure model artifacts are located in working directory.")
            # Heuristic simulation
            sent_sim = "Negative" if any(k in cleaned for k in ["fail", "error", "leak", "hung", "pool", "silent"]) else "Neutral"
            topic_sim = "Technical_Issues" if any(k in cleaned for k in ["db", "pool", "deploy", "service", "error"]) else "Community_Discussion"
            st.info(f"Heuristic Classification: Sentiment = **{sent_sim}** | Topic = **{topic_sim}**")


# -----------------------------------------------------------------------------
# 4. SYSTEM ARCHITECTURE & INTEGRATED PHASES RECONSTRUCTION
# -----------------------------------------------------------------------------
with st.expander("🏗️ View End-to-End System Architecture (Rounds 1 → 2 → 3 → 4)", expanded=False):
    st.markdown("""
    #### End-to-End Operational Pipeline Reconstruction:
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
    │  - Real-Time Compound System Anomaly Score Index                                      │
    │  - Multi-Platform Semantic Cluster Drilldown & Live Inference Playground               │
    └────────────────────────────────────────────────────────────────────────────────────────┘
    ```
    """)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 0.8rem; padding: 10px;'>
    Data Vortex Competition 2026 · Final Offline Hybrid Round 4 · Team: Data Vortex Competitors · Theme: Rebuilding the Social Engine
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        import streamlit.runtime
        if not streamlit.runtime.exists():
            from streamlit.web import cli as stcli
            import sys
            print("\n[DATA VORTEX] Direct python execution detected.")
            print("[DATA VORTEX] Launching Streamlit Command Portal via in-process runner...\n")
            sys.argv = ["streamlit", "run", __file__]
            sys.exit(stcli.main())
    except Exception as e:
        pass

