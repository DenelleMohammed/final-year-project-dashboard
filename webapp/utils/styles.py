"""Custom styling and theming for the Streamlit app."""
from __future__ import annotations

import streamlit as st

# Professional blue color palette
PRIMARY_BLUE = "#1e3a8a"  # Deep blue for headers and key elements
ACCENT_BLUE = "#2563eb"  # Bright blue for interactive elements
LIGHT_BLUE = "#dbeafe"  # Light blue for backgrounds and cards
PALE_BLUE = "#f0f9ff"  # Very light blue for subtle sections
DARK_TEXT = "#0f172a"  # Near-black for readability
MUTED_TEXT = "#475569"  # Gray for secondary text
BORDER_COLOR = "#cbd5e1"  # Border color for cards
SHADOW = "0 4px 12px rgba(15, 23, 42, 0.1)"


def palette() -> list[str]:
    """Return a blue-themed color palette for charts."""
    return [
        "#1e3a8a",  # Deep blue (primary)
        "#2563eb",  # Bright blue
        "#3b82f6",  # Sky blue
        "#60a5fa",  # Light blue
        "#93c5fd",  # Pale blue
        "#2563eb",  # Additional blue shades
        "#1e40af",
    ]


def inject_global_css() -> None:
    """Inject custom CSS for a clean, academic, professional look."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@400;500;600;700&display=swap');
        
        /* Root variables */
        :root {{
            --primary-blue: {PRIMARY_BLUE};
            --accent-blue: {ACCENT_BLUE};
            --light-blue: {LIGHT_BLUE};
            --pale-blue: {PALE_BLUE};
            --text-dark: {DARK_TEXT};
            --text-muted: {MUTED_TEXT};
            --border: {BORDER_COLOR};
            --shadow: {SHADOW};
            --radius: 8px;
        }}
        
        /* General page styling */
        html, body, .stApp, [data-testid="stAppViewContainer"] {{
            background: linear-gradient(180deg, #eff6ff 0%, #dbeafe 55%, #bfdbfe 100%);
            color: var(--text-dark);
            font-family: 'Source Sans 3', sans-serif;
        }}
        
        /* Main container */
        .main {{
            background: transparent;
            padding-top: 0;
        }}
        
        /* Streamlit toolbar - keep only controls visible */
        [data-testid="stHeader"] {{
            background: transparent;
            border-bottom: none;
            box-shadow: none;
        }}

        [data-testid="stToolbar"] {{
            background: transparent;
            border-bottom: none;
            box-shadow: none;
            backdrop-filter: none;
            -webkit-backdrop-filter: none;
        }}
        
        [data-testid="stToolbar"] button {{
            color: var(--primary-blue) !important;
        }}
        
        [data-testid="stToolbar"] svg {{
            stroke: var(--primary-blue) !important;
            fill: var(--primary-blue) !important;
        }}
        
        [data-testid="stToolbar"] * {{
            color: var(--primary-blue) !important;
        }}

        [data-testid="stToolbar"] button:first-of-type {{
            margin-left: 3rem;
        }}
        
        .block-container {{
            padding-top: 1.5rem;
            padding-left: 3rem;
            padding-right: 3rem;
            max-width: 1400px;
            margin-top: 0 !important;
            background: rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(18px) saturate(135%);
            -webkit-backdrop-filter: blur(18px) saturate(135%);
            border: 1px solid rgba(255, 255, 255, 0.24);
            border-radius: 28px;
            box-shadow: 0 20px 48px rgba(6, 16, 48, 0.24);
            margin-top: 1rem !important;
            margin-bottom: 1rem;
            padding-bottom: 2rem;
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--text-dark);
            font-family: 'Playfair Display', serif !important;
            font-weight: 700;
        }}

        /* Streamlit title styling */
        [data-testid="stHeadingMain"] h1 {{
            font-family: 'Playfair Display', serif !important;
        }}

        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}

        /* Page header */
        .page-header {{
            margin: 0 0 1rem 0;
            padding: 0 0 0.25rem 0;
        }}

        .page-header__title {{
            color: var(--primary-blue);
            font-family: 'Playfair Display', serif;
            font-size: 1.95rem;
            font-weight: 700;
            line-height: 1;
            margin: 0;
        }}

        .page-header__subtitle {{
            color: var(--text-muted);
            font-size: 0.8rem;
            line-height: 1.2;
            margin: 0.15rem 0 0 0;
            opacity: 0.95;
            font-family: 'Source Sans 3', sans-serif;
        }}

        h2 {{
            font-size: 1.875rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 3px solid var(--accent-blue);
            padding-bottom: 0.5rem;
            color: var(--primary-blue);
        }}

        h3 {{
            font-size: 1.25rem;
            margin-top: 1.5rem;
            color: var(--primary-blue);
        }}
        
        /* Streamlit markdown headings */
        .stMarkdown h1, 
        .stMarkdown h2, 
        .stMarkdown h3, 
        .stMarkdown h4, 
        .stMarkdown h5, 
        .stMarkdown h6 {{
            font-family: 'Playfair Display', serif;
        }}
        
        .stMarkdownContainer p {{
            color: var(--text-muted);
            line-height: 1.6;
            font-size: 1rem;
            font-family: 'Source Sans 3', sans-serif;
        }}
        
        /* Metric cards (using Streamlit metric) */
        [data-testid="metric-container"] {{
            background-color: var(--pale-blue);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 0.5rem;
            box-shadow: var(--shadow);
        }}
        
        [data-testid="metric-container"] > div:first-child {{
            color: var(--text-muted);
            font-size: 0.875rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        [data-testid="metric-container"] > div:last-child {{
            color: var(--primary-blue);
            font-size: 2rem;
            font-weight: 700;
        }}
        
        /* Sidebar */
        .sidebar .sidebar-content {{
            background-color: var(--pale-blue);
        }}
        
        /* Info/Warning/Error boxes */
        .stInfo {{
            background-color: var(--pale-blue);
            border-left: 4px solid var(--accent-blue);
            border-radius: var(--radius);
        }}
        
        .stWarning {{
            background-color: #fef3c7;
            border-left: 4px solid #f59e0b;
        }}
        
        .stError {{
            background-color: #fee2e2;
            border-left: 4px solid #ef4444;
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: var(--accent-blue);
            color: white;
            border: none;
            border-radius: var(--radius);
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            background-color: var(--primary-blue);
            box-shadow: var(--shadow);
            transform: translateY(-2px);
        }}
        
        /* Dividers */
        hr {{
            border: none;
            height: 2px;
            background: linear-gradient(
                90deg,
                transparent,
                var(--accent-blue),
                transparent
            );
            margin: 2rem 0;
        }}
        
        /* DataFrames */
        .stDataFrame {{
            border: 1px solid var(--border);
            border-radius: var(--radius);
            overflow: hidden;
        }}
        
        /* Expandable sections */
        .streamlit-expanderHeader {{
            background-color: var(--pale-blue);
            color: var(--primary-blue);
            font-weight: 600;
            border-radius: var(--radius);
        }}
        
        /* Plotly charts - ensure good spacing */
        [data-testid="stPlotlyChart"] {{
            border: none;
            border-radius: var(--radius);
                background: white;
            padding: 0;
            overflow: hidden;
            box-sizing: border-box;
        }}

        [data-testid="stPlotlyChart"] .plotly-graph-div {{
            border: none !important;
            padding: 0 !important;
            background: transparent !important;
        }}
        
        /* Section spacing */
        .stMarkdown {{
            margin-bottom: 1rem;
        }}
        
        /* Column styling for better visual hierarchy */
        [data-testid="column"] {{
            background-color: transparent;
        }}
        
        /* Tab-style metric cards */
        .metric-tab-card {{
            background-color: white;
            border: none;
            border-radius: 22px;
            padding: 1rem 1rem 0.8rem 1rem;
            text-align: center;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            min-height: 148px;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        
        .metric-tab-card:hover {{
            box-shadow: 0 8px 16px rgba(37, 99, 235, 0.2);
            transform: translateY(-2px);
        }}
        
        .metric-tab-card,
        .metric-tab-header,
        .metric-tab-value {{
            font-family: 'Source Sans 3', sans-serif;
        }}

        .metric-tab-header {{
            position: absolute;
            top: 0.65rem;
            left: 0;
            display: inline-flex;
            align-items: center;
            font-size: 0.86rem;
            color: white;
            font-weight: 600;
            letter-spacing: 0.03em;
            line-height: 1.2;
            font-family: 'Source Sans 3', sans-serif;
            background: linear-gradient(90deg, #5780c0 0%, #6d8fc7 100%);
            padding: 0.45rem 1rem;
            border-radius: 0 999px 999px 0;
            box-shadow: 0 6px 14px rgba(87, 128, 192, 0.22);
        }}
        
        .metric-tab-value {{
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--primary-blue);
            line-height: 1.1;
        }}

        .metric-tab-split {{
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin-top: 0.55rem;
            width: 100%;
        }}

        .metric-tab-split--multi {{
            justify-content: space-between;
            gap: 0.75rem;
        }}

        .metric-tab-split__item {{
            flex: 0 1 auto;
            min-width: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            white-space: nowrap;
        }}

        .metric-tab-split--multi .metric-tab-split__item {{
            flex: 1 1 0;
        }}

        .metric-tab-split__label {{
            font-size: 0.84rem;
            color: var(--text-muted);
            font-weight: 600;
            line-height: 1.1;
            margin-top: 0.15rem;
        }}

        .metric-tab-split__value {{
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--primary-blue);
            line-height: 1;
        }}

        .metric-tab-subtext {{
            margin-top: 0.2rem;
            color: var(--text-muted);
            font-size: 0.72rem;
            line-height: 1.25;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_banner(title: str, subtitle: str) -> None:
    """Render the page title and subtitle in the main content container."""
    st.markdown(
        f"""
        <div class="page-header">
            <div class="page-header__title">{title}</div>
            <div class="page-header__subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
