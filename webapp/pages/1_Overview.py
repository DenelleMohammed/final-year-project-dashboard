"""Overview page: High-level summary of alignment results across all programmes."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from utils import charts
from utils.data_loader import (
    count_jsonl_records,
    get_overview_alignment_data,
    load_weighted_alignment,
)
from utils.metrics import metric_cards
from utils.styles import inject_global_css, render_page_banner

st.set_page_config(
    page_title="Overview | Alignment Dashboard",
    page_icon="📊",
    layout="wide",
)
inject_global_css()

render_page_banner(
    "Key Statistics",
    "High-level snapshot of curriculum–job market alignment across Computer Science and Information Technology.",
)

counts = count_jsonl_records()

# ==================== SUMMARY STATISTICS ====================

# st.markdown("### Key Statistics")

# Calculate totals for metric cards
course_outline_total = counts.get("CS course outlines", 0) + counts.get("IT course outlines", 0)
job_desc_total = sum(
    counts.get(label, 0)
    for label in [
        "Local CS job posts",
        "Local IT job posts",
        "Intl CS job posts",
        "Intl IT job posts",
        "AI job posts",
    ]
)

# Load weighted alignment scores from CSV and calculate combined CS/IT scores
weighted_alignment_df = load_weighted_alignment()
cs_score = None
it_score = None
overall_score = None

if not weighted_alignment_df.empty:
    cs_row = weighted_alignment_df[weighted_alignment_df["Programme"] == "Computer Science"]
    it_row = weighted_alignment_df[weighted_alignment_df["Programme"] == "Information Technology"]
    overall_row = weighted_alignment_df[weighted_alignment_df["Programme"] == "Weighted rho_w"]
    
    # Calculate weighted alignment using formula: ρ_w = Σ(ρ_thematic × N_thematic) / N_total
    if not cs_row.empty:
        rho_local = cs_row["rho Caribbean"].values[0]
        rho_intl = cs_row["rho International"].values[0]
        n_local = cs_row["JD Count (Local)"].values[0]
        n_intl = cs_row["JD Count (Intl)"].values[0]
        cs_score = (rho_local * n_local + rho_intl * n_intl) / (n_local + n_intl)
    
    if not it_row.empty:
        rho_local = it_row["rho Caribbean"].values[0]
        rho_intl = it_row["rho International"].values[0]
        n_local = it_row["JD Count (Local)"].values[0]
        n_intl = it_row["JD Count (Intl)"].values[0]
        it_score = (rho_local * n_local + rho_intl * n_intl) / (n_local + n_intl)
    
    if not overall_row.empty:
        rho_local = overall_row["rho Caribbean"].values[0]
        rho_intl = overall_row["rho International"].values[0]
        n_local = overall_row["JD Count (Local)"].values[0]
        n_intl = overall_row["JD Count (Intl)"].values[0]
        overall_score = (rho_local * n_local + rho_intl * n_intl) / (n_local + n_intl)

cs_percent = f"{cs_score * 100:.2f}%" if cs_score is not None else "—"
it_percent = f"{it_score * 100:.2f}%" if it_score is not None else "—"
overall_percent = f"{overall_score * 100:.2f}%" if overall_score is not None else "—"

cards = [
    {
        "label": "Course Outlines Count",
        "value": course_outline_total,
        "help": f"CS: {counts.get('CS course outlines', 0)} · IT: {counts.get('IT course outlines', 0)}",
    },
    {
        "label": "Job Descriptions Count",
        "value": job_desc_total,
        "help": "Local + international + AI job posts",
    },
    {
        "label": "Total Alignment Score",
        "value": overall_percent,
        "help": "Combined alignment across both programmes",
    },
]

metric_cards(cards, columns=3)

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# ==================== COMPARISON CHARTS ====================

comparison_data = pd.DataFrame(
    [
        {
            "programme": "Computer Science",
            "course_outlines": counts.get("CS course outlines", 0),
            "local_jobs": counts.get("Local CS job posts", 0),
            "international_jobs": counts.get("Intl CS job posts", 0),
        },
        {
            "programme": "Information Technology",
            "course_outlines": counts.get("IT course outlines", 0),
            "local_jobs": counts.get("Local IT job posts", 0),
            "international_jobs": counts.get("Intl IT job posts", 0),
        },
    ]
)

left_col, right_col = st.columns(2, gap="large")

with left_col:
    fig_counts = charts.overview_counts_chart(comparison_data, "Course Outlines vs Job Descriptions")
    if fig_counts:
        st.plotly_chart(fig_counts, use_container_width=True, config={"displayModeBar": False})

with right_col:
    alignment_data = get_overview_alignment_data()
    fig_alignment = charts.programme_alignment_chart(alignment_data, "Alignment Scores by Field")
    if fig_alignment:
        st.plotly_chart(fig_alignment, use_container_width=True, config={"displayModeBar": False})
