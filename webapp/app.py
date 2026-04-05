"""Main entry point for the Curriculum–Industry Skill Alignment Dashboard."""
from __future__ import annotations

import streamlit as st

from utils.styles import inject_global_css

# Configure Streamlit page
st.set_page_config(
    page_title="Curriculum–Job Market Alignment Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()


def render_info_card(title: str, body: str) -> None:
    """Render a compact informational card for the welcome page."""
    st.markdown(
        f"""
        <div class="welcome-card">
            <div class="welcome-card__title">{title}</div>
            <div class="welcome-card__body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
        .block-container {
            max-width: 1120px;
            padding-top: 0.8rem;
            padding-bottom: 0.4rem;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at top left, rgba(255,255,255,0.88), rgba(255,255,255,0) 42%),
                linear-gradient(180deg, #eef5ff 0%, #dfeaff 100%);
        }

        [data-testid="stMainBlockContainer"] {
            padding-left: 1.25rem;
            padding-right: 1.25rem;
        }

        .welcome-shell {
            min-height: auto;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            gap: 0.65rem;
        }

        .welcome-hero {
            text-align: center;
            max-width: 900px;
            margin: 0 auto 0.15rem auto;
        }

        .welcome-kicker {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.28rem 0.8rem;
            border-radius: 999px;
            background: rgba(65, 105, 225, 0.12);
            color: #28448b;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.45rem;
        }

        .welcome-title {
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: clamp(2rem, 2.8vw, 3.05rem);
            line-height: 1.03;
            color: #17357d;
            font-weight: 700;
            margin: 0 0 0.35rem 0;
            letter-spacing: -0.02em;
        }

        .welcome-subtitle {
            color: #4b5d7a;
            font-size: 0.96rem;
            line-height: 1.35;
            max-width: 780px;
            margin: 0 auto;
        }

        .welcome-grid {
            max-width: 1040px;
            margin: 0 auto;
        }

        .welcome-card {
            background: rgba(255, 255, 255, 0.94);
            border: 1px solid rgba(120, 148, 206, 0.18);
            border-radius: 22px;
            box-shadow: 0 12px 30px rgba(34, 66, 130, 0.10);
            min-height: 135px;
            padding: 0.9rem 1rem;
            margin-bottom: 0;
        }

        .welcome-card__title {
            color: #193a86;
            font-size: 0.96rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
            letter-spacing: 0.01em;
        }

        .welcome-card__body {
            color: #42556f;
            font-size: 0.88rem;
            line-height: 1.28;
        }

        .welcome-card__body ul {
            margin: 0;
            padding-left: 1.1rem;
        }

        .welcome-card__body li {
            margin: 0.08rem 0;
        }

        .welcome-note {
            text-align: center;
            color: #2a427b;
            font-size: 0.88rem;
            font-weight: 600;
            margin-top: 0.1rem;
        }

        @media (max-width: 768px) {
            .welcome-shell {
                min-height: auto;
                gap: 0.55rem;
            }

            .welcome-title {
                font-size: 1.85rem;
            }

            .welcome-subtitle {
                font-size: 0.9rem;
            }

            .welcome-card {
                min-height: 128px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="welcome-shell">
        <div class="welcome-hero">
            <div class="welcome-kicker">Final Year Research Project</div>
            <div class="welcome-title">Curriculum–Industry Skill Alignment Dashboard</div>
            <div class="welcome-subtitle">
                An interactive summary of NLP-based results showing how closely DCIT course content aligns with job market skill requirements.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

grid_left, grid_right = st.columns(2, gap="large")

with grid_left:
    render_info_card(
        "About the Project",
        "This project evaluates the relationship between university curriculum content and employer skill demands using natural language processing on course outlines and job descriptions.",
    )
    render_info_card(
        "Methods Used",
        "<ul><li>Text preprocessing</li><li>Skill extraction</li><li>Topic modelling</li><li>Closeness metric calculation</li><li>Alignment scoring</li></ul>",
    )

with grid_right:
    render_info_card(
        "What the Dashboard Shows",
        "<ul><li>Course outline counts</li><li>Job description counts</li><li>Closeness metrics</li><li>Alignment scores</li><li>CS and IT breakdowns</li></ul>",
    )
    render_info_card(
        "Pages in this Dashboard",
        "<ul><li>Overview</li><li>Computer Science</li><li>Information Technology</li></ul>",
    )

st.markdown(
    '<div class="welcome-note">Use the sidebar to explore each section of the dashboard.</div>',
    unsafe_allow_html=True,
)
