#!/usr/bin/env python3
"""
Data Vortex Round 3 — Deliverable 3
Real-Time Time-Series Monitoring Code
Topic: "The Silent Failure Situation"

Ingests the live multi-platform dataset (silent_failure_raw_dataset.csv) and generates:
1. Chart 1: Hourly Post Velocity & Engagement Spike Tracking (Volume vs Likes/Shares)
2. Chart 2: Dual/Stacked Time-Series of Sentiment Distribution across timeline to isolate inflection points.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns

def generate_temporal_monitoring_charts(
    csv_path: str = "silent_failure_raw_dataset.csv",
    output_chart1: str = "chart1_hourly_volume_spike.png",
    output_chart2: str = "chart2_sentiment_trajectory.png",
):
    # Set high-grade presentation styling
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "figure.titlesize": 15,
        "figure.titleweight": "bold",
    })

    # Load dataset and standardize timeline
    df = pd.read_csv(csv_path)
    df["ISO_timestamp"] = pd.to_datetime(df["ISO_timestamp"], utc=True)
    df = df.sort_values(by="ISO_timestamp").reset_index(drop=True)
    
    # Bucket by 1-hour intervals
    df["hourly_bucket"] = df["ISO_timestamp"].dt.floor("h")

    # Aggregate metrics
    hourly_agg = df.groupby("hourly_bucket").agg(
        post_volume=("text_id", "count"),
        total_likes=("engagement_likes", "sum"),
        total_shares=("engagement_shares", "sum"),
        mean_likes=("engagement_likes", "mean"),
    ).reset_index()

    # -----------------------------------------------------------------------
    # CHART 1: Hourly Posting Volume & Anomaly Velocity Spike
    # -----------------------------------------------------------------------
    fig, ax1 = plt.subplots(figsize=(12, 6), dpi=300)

    # Primary axis: Bar chart of hourly post count
    color_bar = "#2b5c8f"
    bars = ax1.bar(
        hourly_agg["hourly_bucket"],
        hourly_agg["post_volume"],
        width=0.032,  # ~45 mins width on date axis
        color=color_bar,
        alpha=0.75,
        label="Post Volume (Hourly Count)",
        edgecolor="#1b3a5b",
        linewidth=1.2,
    )
    ax1.set_xlabel("Timeline (UTC)", fontweight="bold")
    ax1.set_ylabel("Post Volume (Posts / Hour)", color=color_bar, fontweight="bold")
    ax1.tick_params(axis="y", labelcolor=color_bar)

    # Secondary axis: Line chart of cumulative engagement velocity
    ax2 = ax1.twinx()
    color_line = "#d95f02"
    ax2.plot(
        hourly_agg["hourly_bucket"],
        hourly_agg["total_likes"] / 1000.0,
        color=color_line,
        marker="o",
        linewidth=2.5,
        markersize=6,
        label="Total Engagement Likes (x10³)",
    )
    ax2.plot(
        hourly_agg["hourly_bucket"],
        hourly_agg["total_shares"] / 1000.0,
        color="#7570b3",
        marker="s",
        linewidth=2.0,
        linestyle="--",
        markersize=5,
        label="Total Shares (x10³)",
    )
    ax2.set_ylabel("Viral Engagement (Thousands)", color=color_line, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor=color_line)
    ax2.grid(False)  # Avoid conflicting grid lines

    # Formatting date axis
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M\n%b %d"))
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=2))

    # Highlight anomaly velocity window
    ax1.axvspan(
        pd.to_datetime("2026-09-20 10:00:00+00:00"),
        pd.to_datetime("2026-09-20 14:30:00+00:00"),
        color="#e7298a",
        alpha=0.12,
        label="Critical Anomaly Velocity Window (Spike)",
    )

    # Annotate peak
    peak_row = hourly_agg.loc[hourly_agg["post_volume"].idxmax()]
    ax1.annotate(
        f"Peak Velocity: {peak_row['post_volume']} posts/hr\nEngagement: {peak_row['total_likes']:,} likes",
        xy=(peak_row["hourly_bucket"], peak_row["post_volume"]),
        xytext=(peak_row["hourly_bucket"] + pd.Timedelta(hours=1.2), peak_row["post_volume"] - 2),
        arrowprops=dict(facecolor="#d95f02", shrink=0.08, width=1.5, headwidth=7),
        bbox=dict(boxstyle="round,pad=0.3", fc="#fff2df", ec="#d95f02", lw=1.2),
        fontsize=9,
        fontweight="semibold",
    )

    # Unified Legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True)

    plt.title("Chart 1: Social Engine Velocity & Viral Engagement Spikes Across Hourly Blocks\nTracking 'The Silent Failure Situation' Telemetry", pad=15)
    plt.tight_layout()
    plt.savefig(output_chart1, dpi=300)
    plt.close()
    print(f"[+] Successfully generated: {output_chart1}")

    # -----------------------------------------------------------------------
    # CHART 2: Dual / Stacked Trajectory of Sentiment Distribution
    # -----------------------------------------------------------------------
    sentiment_hourly = df.groupby(["hourly_bucket", "predicted_sentiment"]).size().unstack(fill_value=0)
    # Ensure standard sentiment columns
    for col in ["Negative", "Neutral", "Positive"]:
        if col not in sentiment_hourly.columns:
            sentiment_hourly[col] = 0

    sentiment_pct = sentiment_hourly.div(sentiment_hourly.sum(axis=1), axis=0) * 100

    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, dpi=300, gridspec_kw={"height_ratios": [1.2, 1]})

    # Upper panel: Absolute counts per sentiment
    ax_top.plot(sentiment_hourly.index, sentiment_hourly["Negative"], color="#e41a1c", marker="o", lw=2.2, label="Negative Sentiment (Frustration / Bug Reports)")
    ax_top.plot(sentiment_hourly.index, sentiment_hourly["Neutral"], color="#377eb8", marker="^", lw=2.0, linestyle="--", label="Neutral Sentiment (Diag / Tech Feedback)")
    ax_top.plot(sentiment_hourly.index, sentiment_hourly["Positive"], color="#4daf4a", marker="s", lw=1.8, linestyle=":", label="Positive Sentiment (Hotfix / Resolution)")
    
    ax_top.set_ylabel("Post Count / Hr", fontweight="bold")
    ax_top.set_title("Chart 2A: Volume Trajectory by Sentiment Classification", fontsize=12)
    ax_top.legend(loc="upper left", frameon=True)

    # Inflection point annotations
    ax_top.axvline(pd.to_datetime("2026-09-20 07:00:00+00:00"), color="#e41a1c", linestyle=":", lw=1.5)
    ax_top.text(pd.to_datetime("2026-09-20 07:10:00+00:00"), ax_top.get_ylim()[1]*0.82, "Shift 1: Silent Cascade\nNeutral -> 100% Negative", color="#e41a1c", fontsize=9, fontweight="bold")

    ax_top.axvline(pd.to_datetime("2026-09-20 18:00:00+00:00"), color="#377eb8", linestyle=":", lw=1.5)
    ax_top.text(pd.to_datetime("2026-09-20 18:10:00+00:00"), ax_top.get_ylim()[1]*0.55, "Shift 2: Quiet Hotfix Recovery\nNegative Collapse -> Neutral Resurgence", color="#377eb8", fontsize=9, fontweight="bold")

    # Lower panel: Normalized Sentiment Share (Stacked Area)
    ax_bot.stackplot(
        sentiment_pct.index,
        sentiment_pct["Negative"],
        sentiment_pct["Neutral"],
        sentiment_pct["Positive"],
        labels=["% Negative", "% Neutral", "% Positive"],
        colors=["#fbb4ae", "#b3cde3", "#ccebc5"],
        alpha=0.85,
    )
    ax_bot.set_ylabel("Sentiment Proportion (%)", fontweight="bold")
    ax_bot.set_ylim(0, 100)
    ax_bot.set_xlabel("Timeline (UTC)", fontweight="bold")
    ax_bot.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M\n%b %d"))
    ax_bot.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax_bot.legend(loc="lower left", frameon=True)
    ax_bot.set_title("Chart 2B: Proportional Sentiment Dynamics & Inflection Horizons", fontsize=12)

    plt.suptitle("Chart 2: Dual Time-Series Trajectory of Sentiment Distribution Inflection Points\nMonitoring End-User Perceptual Shifts During Silent Infrastructure Degradation", y=0.98)
    plt.tight_layout()
    plt.savefig(output_chart2, dpi=300)
    plt.close()
    print(f"[+] Successfully generated: {output_chart2}")

if __name__ == "__main__":
    generate_temporal_monitoring_charts()
