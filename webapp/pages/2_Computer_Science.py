"""Computer Science page: Detailed results and analysis for the CS programme."""
from __future__ import annotations

import streamlit as st

from utils import charts
from utils.data_loader import get_closeness_metric_data, get_programme_summary
from utils.metrics import metric_cards
from utils.styles import inject_global_css, render_page_banner

st.set_page_config(
    page_title="Computer Science | Alignment Dashboard",
    page_icon="💻",
    layout="wide",
)
inject_global_css()

render_page_banner(
    "Computer Science Programme",
    "Detailed analysis of curriculum alignment with job market demands in Computer Science.",
)

summary = get_programme_summary("cs")

# ==================== SUMMARY CARDS ====================

cards = [
    {
        "label": "Course Outline Number",
        "value": summary["course_count"],
        # "help": "Total course outlines analysed",
    },
    {
        "label": "Job Description Number",
        "value": {
            "segments": [
                {"label": "Local", "value": summary["local_jobs"]},
                {"label": "International", "value": summary["intl_jobs"]},
                {"label": "AI", "value": summary["ai_jobs"]},
            ],
        },
        "help": "Local, international, and ai job descriptions",
    },
    {
        "label": "Alignment Score",
        "value": {
            "left_label": "Local",
            "left_value": summary["local_alignment"],
            "right_label": "International",
            "right_value": summary["intl_alignment"],
        },
        "help": "Average alignment scores by market",
    },
]

metric_cards(cards, columns=3)

closeness_data = get_closeness_metric_data("cs")
fig_close = charts.closeness_chart(closeness_data, "Closeness Metrics for Computer Science")
if fig_close:
    st.plotly_chart(fig_close, use_container_width=True, config={"displayModeBar": False})
