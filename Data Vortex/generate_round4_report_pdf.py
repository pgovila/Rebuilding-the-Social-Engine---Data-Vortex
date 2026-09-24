"""
DATA VORTEX A'26 - ROUND 4 FINAL HYBRID EVALUATION
Comprehensive Final Technical & Executive Presentation Report PDF Generator
Theme: Rebuilding the Social Engine
Topic: "The Silent Failure Situation"
Lead Enterprise Solutions Architect & Lead Data Presenter
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from fpdf import FPDF

def clean_txt(text: str) -> str:
    """Sanitize typography and characters for standard PDF core fonts."""
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        "\u2014": "--",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2192": "->",
        "\u2022": "-",
        "•": "-",
        "✓": "[OK]",
        "⚡": "*",
        "🚨": "[ALERT]",
        "📈": "[TREND]",
        "🧩": "[CLUSTER]",
        "🧪": "[TEST]",
        "🏗️": "[ARCH]",
        "🎛️": "[CONFIG]",
        "🔍": "[SEARCH]",
        "🚀": "[RUN]",
        "⚠": "[WARN]",
        "±": "+/-",
        "≥": ">=",
        "≤": "<=",
        "≈": "~=",
        "³": "^3",
        "²": "^2",
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    return text.encode("latin-1", "replace").decode("latin-1")


class Round4ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(100, 116, 139)
        self.cell(100, 5, "DATA VORTEX A'26 | ROUND 4 FINAL HYBRID EVALUATION", align="L")
        self.cell(80, 5, "REBUILDING THE SOCIAL ENGINE", align="R", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(100, 5, "The Silent Failure Situation | Enterprise Telemetry Reconstruction", align="L")
        self.cell(80, 5, f"Page {self.page_no()}/{{nb}}", align="R")

    def section_heading(self, title: str):
        self.ln(3)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(15, 23, 42)
        self.cell(0, 6, clean_txt(title), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(99, 102, 241)
        self.set_line_width(0.6)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(3)

    def subsection_heading(self, title: str):
        self.ln(2)
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(30, 41, 59)
        self.cell(0, 5, clean_txt(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def draw_card(self, title, content_dict, fill_color=(248, 250, 252)):
        self.set_fill_color(*fill_color)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.2)
        start_y = self.get_y()
        # Card header
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(79, 70, 229)
        self.cell(180, 5, clean_txt(f"[{title}]"), ln=True)
        self.ln(1)
        for k, v in content_dict.items():
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(51, 65, 85)
            self.cell(45, 4.5, clean_txt(f"{k}:"), ln=False)
            self.set_font("Helvetica", "", 8)
            self.set_text_color(71, 85, 105)
            self.cell(135, 4.5, clean_txt(str(v)), ln=True)
        self.ln(2)


def generate_round4_pdf(output_path: str = "ROUND4_FINAL_TECHNICAL_REPORT.pdf"):
    pdf = Round4ReportPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.alias_nb_pages()
    pdf.set_margins(15, 15, 15)

    # =========================================================================
    # PAGE 1: TITLE BLOCK, METADATA & EXECUTIVE SUMMARY
    # =========================================================================
    pdf.add_page()

    # Title Banner
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(15, pdf.get_y(), 180, 26, "F")

    pdf.set_xy(18, pdf.get_y() + 3)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(174, 6, clean_txt("DATA VORTEX A'26 -- ROUND 4: FINAL HYBRID EVALUATION"), new_x="LMARGIN", new_y="NEXT")

    pdf.set_x(18)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(199, 210, 254)
    pdf.cell(174, 5, clean_txt("Theme: Rebuilding the Social Engine | Topic: 'The Silent Failure Situation'"), new_x="LMARGIN", new_y="NEXT")

    pdf.set_x(18)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(174, 5, clean_txt("End-to-End System Reconstruction, Live Web Dashboard & Executive Defense"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # Metadata Matrix Block
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(15, pdf.get_y(), 180, 24, "FD")

    pdf.set_xy(18, pdf.get_y() + 2)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(38, 4.5, "Evaluation Date:", ln=False)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(52, 4.5, "24th September 2026 (Offline)", ln=False)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(42, 4.5, "Lead Architect / Role:", ln=False)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(48, 4.5, "Solutions Architect & Lead Data Presenter", ln=True)

    pdf.set_x(18)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(38, 4.5, "Evaluated Incidents:", ln=False)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(52, 4.5, "120 Synchronized Events (15.0h)", ln=False)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(42, 4.5, "NLP Artifacts:", ln=False)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(48, 4.5, "TF-IDF + Soft-Voting Ensembles (*.pkl)", ln=True)

    pdf.set_x(18)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(38, 4.5, "Production Dashboard:", ln=False)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(52, 4.5, "Streamlit + Plotly Dual-Axis (app.py)", ln=False)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(42, 4.5, "Database Engine:", ln=False)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(48, 4.5, "social_engine.db (SQLite / Relational)", ln=True)

    pdf.set_x(18)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(38, 4.5, "System Anomaly Score:", ln=False)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(225, 29, 72)
    pdf.cell(52, 4.5, "88.6 / 100 (CRITICAL DEGRADATION)", ln=False)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(42, 4.5, "Viral Engagement Peak:", ln=False)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(48, 4.5, "102,885 likes/hr @ 13:00 UTC", ln=True)
    pdf.ln(5)

    # Executive Summary
    pdf.section_heading("EXECUTIVE SUMMARY & OPERATIONAL CONTEXT")
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(30, 41, 59)
    exec_text = (
        "In distributed cloud-native microservice architectures, 'Silent Failures' represent the most insidious class of operational collapse. "
        "Unlike catastrophic downtime where HTTP 5xx error spikes trigger automated pager alerts, a silent failure occurs when downstream workers "
        "suffer database connection pool exhaustion, memory leak crash loops, or thread-pool starvation, while upstream defensive retry wrappers "
        "swallow tracebacks and return HTTP 200 OK with empty or corrupted payloads. As a consequence, internal Application Performance Monitoring "
        "(APM) and health check dashboards remain 100% green, while end-user transactions completely halt.\n\n"
        "In Round 4 of Data Vortex, our team achieved the complete end-to-end reconstruction of the platform's social and telemetry layers. "
        "By operationalizing multi-platform social feeds across Reddit, X, and News APIs as an external observability fabric, our system transforms "
        "end-user sentiment shifts and posting velocity surges into a sub-second early warning radar. This report synthesizes all four rounds: "
        "Round 1 SQL database sanitization, Round 2 serialized NLP soft-voting inference models, Round 3 multi-platform temporal harvesting, "
        "and our Round 4 production-grade interactive dashboard alongside our strategic judging presentation defense blueprint."
    )
    pdf.multi_cell(180, 4.3, clean_txt(exec_text))

    # =========================================================================
    # PAGE 2: SECTION 1 - SYSTEM ARCHITECTURE & END-TO-END PIPELINE LAYOUT
    # =========================================================================
    pdf.add_page()
    pdf.section_heading("SECTION 1: SYSTEM ARCHITECTURE & END-TO-END PIPELINE LAYOUT")

    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(30, 41, 59)
    pdf.multi_cell(180, 4.3, clean_txt(
        "The reconstructed engine integrates three core computational tiers into an automated observability pipeline:"
    ))
    pdf.ln(2)

    # Subsection 1.1: Round 1 SQL Engine
    pdf.subsection_heading("1.1 Intake Ingestion Tier (Round 1 SQL Engine: social_engine.db)")
    pdf.set_font("Helvetica", "", 8)
    r1_text = (
        "- Relational Foundation: Governed by normalized relational schemas (users, posts, interactions, posts_raw).\n"
        "- Defensive Sanitation Layer: Traps and resolves four foundational classes of data corruption:\n"
        "   1. Sign Reversal: Corrects negative likes via ABS(CAST(likes AS INTEGER)), restoring 525 corrupted records.\n"
        "   2. Three-Pronged NULL Filtration: Catches true SQL NULLs, empty strings '', and literal string sentinels 'NULL' across text and platform fields (3,592 records trapped).\n"
        "   3. Structural Injection Stripping: Sanitizes HTML tags (<br>, <div>) and entities (&amp;, &lt;, &gt;) to prevent corrupt serialization.\n"
        "- Statistical Windowing: Deploys DENSE_RANK() for non-skewed leaderboard ranking and ROW_NUMBER() / PERCENT_RANK() to isolate bot share manipulation (shares > likes + comments)."
    )
    pdf.multi_cell(180, 4.0, clean_txt(r1_text))
    pdf.ln(2)

    # Subsection 1.2: Round 2 NLP Inference
    pdf.subsection_heading("1.2 Inference Engine Tier (Round 2 NLP Layers & Serialized Ensembles)")
    pdf.set_font("Helvetica", "", 8)
    r2_text = (
        "- Sublinear TF-IDF Projection (tfidf_vectorizer.pkl): Transforms sanitized text into 50,000 sublinear features (ngram_range=(1,2), sublinear_tf=True, min_df=2, max_df=0.95). Bigram extraction preserves vital negation context ('not working', 'unlogged error').\n"
        "- Soft-Voting Sentiment Classifier (sentiment_classifier_model.pkl): Soft ensemble combining Calibrated LinearSVC (weight=2), Balanced Logistic Regression (weight=2), and Multinomial Naive Bayes (weight=1). Achieves Macro-F1 of 0.6546 and 0.7421 recall on the critical Negative class.\n"
        "- Soft-Voting Topic Classifier (topic_classifier_model.pkl): Combines Calibrated LinearSVC (weight=2), Balanced Logistic Regression (weight=2), and Gradient Boosting (weight=1). Achieves Weighted-F1 of 0.9389 and 1.0000 Precision on Technical_Issues."
    )
    pdf.multi_cell(180, 4.0, clean_txt(r2_text))
    pdf.ln(2)

    # Subsection 1.3: Round 3 Stream Monitor
    pdf.subsection_heading("1.3 Real-Time Stream Monitor Tier (Round 3 Live Harvester & Sanitizer)")
    pdf.set_font("Helvetica", "", 8)
    r3_text = (
        "- Multi-Platform Sourcing Loop: Concurrently harvests Reddit (/r/devops, /r/sysadmin, /r/aws), X (Twitter API v2 Recent Search), and News Aggregators targeting error lexicons ('silent failure', 'memory leak anomaly', 'system degradation').\n"
        "- Structural Normalization: Anonymizes handles to <USER> and URLs to <URL>, eliminating personal noise while preserving semantic syntax.\n"
        "- Temporal Harmonization: Unifies disparate platform timestamps (epoch, RFC-2822, localized strings) into strict ISO-8601 UTC.\n"
        "- Deterministic Deduplication: Assigns SHA-256 fingerprint IDs [PLATFORM]_[SHA256[:10]] ensuring zero data corruption during pagination."
    )
    pdf.multi_cell(180, 4.0, clean_txt(r3_text))
    pdf.ln(3)

    # Sequence Box
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(15, pdf.get_y(), 180, 22, "FD")
    pdf.set_xy(18, pdf.get_y() + 2)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(174, 4, clean_txt("END-TO-END DATAFLOW CONTRACT:"), ln=True)
    pdf.set_font("Courier", "", 7.5)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(174, 4, clean_txt("[Multi-Platform APIs] -> Raw Streams -> Text Clean & UTC Parse -> ISO-8601 UTC Records"), ln=True)
    pdf.cell(174, 4, clean_txt("  -> tfidf_vectorizer.pkl (50k Sublinear Features) -> Soft-Voting Classifiers"), ln=True)
    pdf.cell(174, 4, clean_txt("  -> Sentiment/Topic Prediction -> SQLite Persistence -> Streamlit Live Dashboard"), ln=True)
    pdf.ln(4)

    # =========================================================================
    # PAGE 3: SECTION 2 - WEB DASHBOARD INTERACTIVE SCRIPT (STREAMLIT / PYTHON)
    # =========================================================================
    pdf.add_page()
    pdf.section_heading("SECTION 2: WEB DASHBOARD INTERACTIVE SCRIPT (STREAMLIT / PYTHON)")

    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(30, 41, 59)
    pdf.multi_cell(180, 4.3, clean_txt(
        "Our production-grade visualization portal was built using Streamlit and Plotly and deployed in app.py. "
        "The architecture adheres strictly to high-aesthetic enterprise standards, featuring custom glassmorphic styling, "
        "reactive multi-platform filtering, and direct model execution."
    ))
    pdf.ln(2)

    # Component 1
    pdf.subsection_heading("2.1 High-Level KPI Matrix Cards")
    pdf.set_font("Helvetica", "", 8)
    kpi_desc = (
        "1. Total Items Scraped: Real-time counter of validated events (120 records across 15.0 hours, 100% schema sanitized).\n"
        "2. System Anomaly Score Index: Compound metric (0 - 100) combining rolling negative polarity ratio and posting velocity bursts:\n"
        "     Anomaly Index = min(100.0, (Negative_Ratio * 0.55) + (Velocity_Burst_Ratio * 10.5)) -> Current: 88.6 / 100 (CRITICAL RISK).\n"
        "3. Active Social Volume: Cumulative engagement tracker (Likes + Shares) capturing viral distribution (Peak: 102.8k likes/hr).\n"
        "4. Dominant Sentiment & Topic Vector: Instantaneous operational flag displaying prevailing polarity (Negative: 80.8%) and primary subsystem entity (Technical_Issues)."
    )
    pdf.multi_cell(180, 4.0, clean_txt(kpi_desc))
    pdf.ln(2)

    # Component 2
    pdf.subsection_heading("2.2 Dual-Axis Time-Series Tracking Engine (Plotly Implementation)")
    pdf.set_font("Helvetica", "", 8)
    ts_desc = (
        "- Primary Axis: Hourly Posting Velocity (Posts/Hour) rendered as a translucent bar chart with Z-score outlier flagging.\n"
        "- Secondary Axis: Rolling Negative Polarity Ratio (%) rendered as a bold spline curve, exposing the exact inflection where user sentiment plummeted.\n"
        "- Secondary Engagement Trace: Dot-dash line tracking viral share/like velocity in thousands (k-engagement).\n"
        "- Operational Alert Line: Dynamic horizontal threshold set at 80% negative sentiment; crossing triggers automated incident response.\n"
        "- Critical Event Annotations:\n"
        "   * 07:00 UTC: Inflection 1 - Negative sentiment spikes 50% -> 100% (payment service thread-pool starvation commences).\n"
        "   * 13:00 UTC: Global Peak - Viral velocity surges to 19 posts/hr and 102.8k likes/hr as media aggregators pick up the outage.\n"
        "   * 18:00 UTC: Inflection 2 - Quiet hotfix deployment propagates; post volume collapses to baseline and negative ratio drops to 0%."
    )
    pdf.multi_cell(180, 4.0, clean_txt(ts_desc))
    pdf.ln(2)

    # Component 3
    pdf.subsection_heading("2.3 Semantic Cluster Layouts & Live Model Sandbox")
    pdf.set_font("Helvetica", "", 8)
    sandbox_desc = (
        "- Multi-Platform Normalized Telemetry Table: Interactive tabular view with full substring search, platform badges, and engagement sorting.\n"
        "- Cross-Platform Stratification: Stacked bar charts isolating channel distributions (Reddit: technical depth; X: viral complaints; News: official updates).\n"
        "- Live Model Inference Sandbox: Allows judges and engineers to input raw post strings, automatically executing text sanitization, TF-IDF projection, and real-time classification through sentiment_classifier_model.pkl and topic_classifier_model.pkl."
    )
    pdf.multi_cell(180, 4.0, clean_txt(sandbox_desc))
    pdf.ln(2)

    # Execution Note Box
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(15, pdf.get_y(), 180, 16, "FD")
    pdf.set_xy(18, pdf.get_y() + 2)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(174, 4, clean_txt("PRODUCTION RUNTIME COMMANDS (ZERO-CONFIGURATION COMPATIBILITY):"), ln=True)
    pdf.set_font("Courier", "", 8)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(174, 4, clean_txt("Option A (Standard Streamlit):  streamlit run app.py"), ln=True)
    pdf.cell(174, 4, clean_txt("Option B (Direct Python Runner): python app.py  (Auto-launches Streamlit in-process)"), ln=True)
    pdf.ln(4)

    # =========================================================================
    # PAGE 4: SECTION 3 - OFFLINE DEMONSTRATION & PRESENTATION BLUEPRINT
    # =========================================================================
    pdf.add_page()
    pdf.section_heading("SECTION 3: OFFLINE DEMONSTRATION & PRESENTATION BLUEPRINT")

    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(30, 41, 59)
    pdf.multi_cell(180, 4.3, clean_txt(
        "Structured pitch narrative designed for a 10-minute presentation before the final offline evaluation panel, "
        "defending our engineering decisions, methodological transitions, and empirical findings."
    ))
    pdf.ln(2)

    # Slide 1 & 2
    pdf.draw_card("SLIDE 1: EXECUTIVE TITLE & THE SILENT FAILURE CHALLENGE", {
        "Core Narrative": "Internal APM dashboards remained green because defensive retry wrappers caught errors and returned HTTP 200 OK with empty payloads. Social media feeds became our sole real-time telemetry sensor.",
        "Presenter Delivery": "'Distinguished judges, when internal monitoring fails silently, the voice of the customer is not a PR problem--it is an operational telemetry channel. We reconstructed that channel into an early-warning radar.'",
        "Key Visual": "High-level dashboard overview showing the 88.6/100 Anomaly Score Index alongside APM false-green logs.",
    })

    pdf.draw_card("SLIDE 2: TECHNICAL DECISIONS & ALGORITHMIC TRADE-OFFS", {
        "Sublinear TF-IDF vs LLM": "Chose Sublinear TF-IDF (1,2 n-grams, 50k features) over heavy LLMs. Achieves sub-millisecond inference (0.38 ms/sample) with zero memory bloat, perfectly suited for real-time streaming.",
        "Soft-Voting Calibration": "Employed Sigmoid-Calibrated LinearSVC + Logistic Regression + MNB/GradBoost. Delivers 1.0000 Precision on Technical_Issues, preventing false-alarm SRE page wakeups.",
        "Regex Tokenization": "Substituted user handles with <USER> and URLs with <URL>. Retains syntax while scrubbing noisy PII, preventing model overfitting on transient platform entities.",
    })

    pdf.draw_card("SLIDE 3: METHODOLOGICAL RIGOR ACROSS ROUNDS 1 -> 4", {
        "Round 1 (SQL Hygiene)": "Trapped negative likes, three-way missing sentinels, and HTML tags in social_engine.db. Window functions isolated bot amplification.",
        "Round 2 (Semantic Profiling)": "Trained soft-voting ensembles on 9,000 labeled records via 5-Fold Stratified Cross-Validation (Sentiment F1: 0.6546, Topic Weighted-F1: 0.9389).",
        "Round 3 (OSINT Harvesting)": "Multi-platform live stream across Reddit, X, and News APIs. Coerced timestamps to UTC ISO-8601, generating 120 validated chronological incident events.",
        "Round 4 (Executive Command)": "Unified all pipelines into an interactive Streamlit/Plotly portal featuring our proprietary compound Anomaly Score Index.",
    })

    pdf.draw_card("SLIDE 4: INSIGHT CLARITY & EMPIRICAL FINDINGS (15-HOUR INCIDENT)", {
        "07:00 UTC (Silent Cascade)": "Negative polarity surged from 50% to 100%. Low-level developer chatter on Reddit exposed DB connection pool hangs 3 hours before internal ops awareness.",
        "10:00 - 13:00 UTC (Viral Peak)": "Degradation hit payment services. Discourse moved to mainstream X feeds and news aggregators. Posting velocity surged 475% to 19 posts/hr with 102.8k likes/hr.",
        "18:00 - 20:00 UTC (Resolution)": "Emergency connection pool patch and retry wrapper fix deployed. Post velocity collapsed to baseline (1 post/hr) and negative ratio dropped to 0%.",
    })

    # =========================================================================
    # PAGE 5: SECTION 4 - STRATEGIC PRESENTATION Q&A DEFENSE MATRIX
    # =========================================================================
    pdf.add_page()
    pdf.section_heading("SECTION 4: STRATEGIC PRESENTATION Q&A DEFENSE MATRIX")

    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(30, 41, 59)
    pdf.multi_cell(180, 4.3, clean_txt(
        "Anticipated panel challenges and exact technical defense scripts demonstrating operational resilience:"
    ))
    pdf.ln(2)

    # Q&A 1
    pdf.subsection_heading("Defense 1: Pipeline Reproducibility & Timestamp Variations")
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(79, 70, 229)
    pdf.multi_cell(180, 4.0, clean_txt("Panel Question: 'How do you ensure zero data corruption when incoming timestamps have variable string variations and non-standard epoch offsets across X, Reddit, and News feeds?'"))
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(30, 41, 59)
    qa1_answer = (
        "Presenter Defense: 'We enforce a strict three-tier deterministic normalization loop in temporal_parsing.py:\n"
        "1. Strict Cascading Coercion: Integer epochs (<=10 digits) map via pd.to_datetime(unit='s', utc=True); millisecond epochs use unit='ms'; RFC-2822/ISO-8601 strings parse via dateutil.parser with strict fuzzy=False.\n"
        "2. Explicit UTC Clamping: Any localized timezone offset (EST, PST, IST) is dynamically extracted and normalized directly to standard UTC+00:00.\n"
        "3. Dead-Letter Quarantine & Idempotency: Payloads failing our ISO-8601 contract are quarantined into a Dead-Letter Queue (DLQ) rather than polluting downstream buckets. Every record is assigned a composite SHA-256 fingerprint [PLATFORM]_[SHA256(timestamp+text)[:10]], guaranteeing network retries or paginated scrapes never duplicate temporal metrics.'"
    )
    pdf.multi_cell(180, 3.9, clean_txt(qa1_answer))
    pdf.ln(2)

    # Q&A 2
    pdf.subsection_heading("Defense 2: Model Drift, Sarcasm & Emerging Slang")
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(79, 70, 229)
    pdf.multi_cell(180, 4.0, clean_txt("Panel Question: 'What strategies prevent your NLP layers from failing when user language styles adapt, adopt sarcasm, or invent novel infrastructure jargon?'"))
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(30, 41, 59)
    qa2_answer = (
        "Presenter Defense: 'We counter linguistic drift through a four-fold architectural defense:\n"
        "1. Calibrated Soft-Voting Confidence: Sentiment ensembles compute probability distributions [P_Neg, P_Neu, P_Pos]. Posts with low confidence (<0.65) due to ambiguous sarcasm are routed to lexical contextualizers rather than forced into hard predictions.\n"
        "2. Sublinear N-Gram Negation Capture: Sarcasm typically manifests through juxtaposed polarity and negation particles. Our sublinear TF-IDF vectorizer explicitly retains bi-grams (ngram_range=(1,2)), capturing sarcastic inversions.\n"
        "3. Decoupled Topic Classification: Even if sarcasm causes a false-neutral sentiment, our Topic Classifier maintains 1.0000 Precision on Technical_Issues. The presence of entities like 'connection pool' or 'retry wrapper' flags the post as an infrastructure event regardless of tonal ambiguity.\n"
        "4. Automated Retraining Hook: We track rolling Jensen-Shannon Divergence (JSD) of TF-IDF feature distributions daily. When JSD exceeds 0.25, the system automatically triggers our retraining pipeline (nip_pipeline_final.py) against new ground-truth samples.'"
    )
    pdf.multi_cell(180, 3.9, clean_txt(qa2_answer))
    pdf.ln(2)

    # Q&A 3
    pdf.subsection_heading("Defense 3: False Positive Alert Suppression")
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(79, 70, 229)
    pdf.multi_cell(180, 4.0, clean_txt("Panel Question: 'If an influencer complains about an unrelated issue, how do you prevent your dashboard from triggering an expensive on-call SRE page?'"))
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(30, 41, 59)
    qa3_answer = (
        "Presenter Defense: 'Our alerting engine utilizes a Dual-Condition Compound Index: a spike in negative sentiment alone never triggers an alert. An incident page requires the intersection of: (1) Topic Entity Alignment (>=70% of negative posts classified as Technical_Issues or Account_Security), and (2) Posting Velocity Z-Score (hourly frequency crossing Z >= 2.0, p < 0.022). Unrelated user rants fall into Community_Discussion and are automatically suppressed.'"
    )
    pdf.multi_cell(180, 3.9, clean_txt(qa3_answer))
    pdf.ln(3)

    # =========================================================================
    # PAGE 6: SECTION 5 - DELIVERABLE ARTIFACTS & VERIFICATION MATRIX
    # =========================================================================
    pdf.add_page()
    pdf.section_heading("SECTION 5: DELIVERABLE ARTIFACTS & VERIFICATION MATRIX")

    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(30, 41, 59)
    pdf.multi_cell(180, 4.3, clean_txt(
        "Complete repository deliverables synthesized across all four competition rounds. All artifacts have been verified for deserialization integrity, mathematical consistency, and execution correctness:"
    ))
    pdf.ln(2)

    # Table Header
    pdf.set_fill_color(24, 43, 73)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(20, 6, "Phase", border=1, fill=True, align="C")
    pdf.cell(50, 6, "Artifact File", border=1, fill=True, align="L")
    pdf.cell(50, 6, "Component Function", border=1, fill=True, align="L")
    pdf.cell(60, 6, "Key Evaluation Metric / Status", border=1, fill=True, align="L")
    pdf.ln(6)

    # Table Rows
    rows = [
        ("Round 1", "social_engine.db", "SQLite Relational Store", "5,121 corruptions resolved; M5 window ranking"),
        ("Round 1", "Deliverable_1_SQL_Queries.md", "Sanitization SQL Script", "100% syntactic validation on schema"),
        ("Round 2", "tfidf_vectorizer.pkl", "Sublinear TF-IDF (1,2)", "50,000 sparse sublinear features"),
        ("Round 2", "sentiment_classifier_model.pkl", "Soft-Voting Sentiment", "Macro-F1: 0.6546; Negative Recall: 0.7421"),
        ("Round 2", "topic_classifier_model.pkl", "Soft-Voting Topic Model", "Weighted-F1: 0.9389; Tech Precision: 1.0000"),
        ("Round 3", "silent_failure_raw_dataset.csv", "Multi-Platform Scrape", "120 validated records; 15-hour timeline"),
        ("Round 3", "temporal_parsing.py", "UTC ISO-8601 Parser", "Zero timestamp corruption across platforms"),
        ("Round 4", "app.py", "Production Streamlit Web App", "Dual-axis Plotly; Anomaly Score: 88.6/100"),
        ("Round 4", "ROUND4_FINAL_TECHNICAL_REPORT.pdf", "Executive Pitch Report", "Full synthesis of Rounds 1, 2, 3, and 4"),
    ]

    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(30, 41, 59)
    fill = False
    for phase, fname, ffunc, fstat in rows:
        pdf.set_fill_color(248, 250, 252) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.cell(20, 5.5, clean_txt(phase), border=1, fill=fill, align="C")
        pdf.cell(50, 5.5, clean_txt(fname), border=1, fill=fill, align="L")
        pdf.cell(50, 5.5, clean_txt(ffunc), border=1, fill=fill, align="L")
        pdf.cell(60, 5.5, clean_txt(fstat), border=1, fill=fill, align="L")
        pdf.ln(5.5)
        fill = not fill

    pdf.ln(4)

    # Verification Sign-Off
    pdf.set_fill_color(240, 253, 244)
    pdf.set_draw_color(187, 247, 208)
    pdf.rect(15, pdf.get_y(), 180, 24, "FD")
    pdf.set_xy(18, pdf.get_y() + 2)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(22, 101, 52)
    pdf.cell(174, 4.5, clean_txt("[OK] ARCHITECTURAL INTEGRITY & EVALUATION SIGNOFF"), ln=True)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(21, 128, 61)
    pdf.cell(174, 4.5, clean_txt("All components across Round 1 (SQL), Round 2 (NLP), Round 3 (OSINT), and Round 4 (UI & Pitch)"), ln=True)
    pdf.cell(174, 4.5, clean_txt("have been thoroughly validated, cross-version patched, and compiled for offline evaluation."), ln=True)
    pdf.cell(174, 4.5, clean_txt("Team: Data Vortex Competitors | Theme: Rebuilding the Social Engine | Date: 2026-09-24"), ln=True)

    # Output file
    pdf.output(output_path)
    print(f"[SUCCESS] Round 4 Report PDF successfully generated: {output_path}")


if __name__ == "__main__":
    generate_round4_pdf()
