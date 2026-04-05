"""Reusable Plotly chart builders."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .styles import palette, PRIMARY_BLUE, ACCENT_BLUE, LIGHT_BLUE


def _base_kwargs(title: str | None = None) -> dict:
    """Return base layout kwargs for all charts."""
    return {
        "color_discrete_sequence": palette(),
        "title": title or "",
        "template": "plotly_white",
    }


def _update_layout_common(fig: go.Figure) -> None:
    """Apply common layout styling to all charts."""
    fig.update_layout(
        font=dict(family="Segoe UI, sans-serif", size=12, color="#0f172a"),
        title=dict(
            font=dict(family="Playfair Display, serif", size=21, color=PRIMARY_BLUE),
            x=0.02,
            xanchor="left",
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="closest",
        margin=dict(t=62, l=52, r=32, b=46),
        height=360,
    )


def overview_counts_chart(df: pd.DataFrame, title: str = "Course Outlines vs Job Descriptions") -> go.Figure | None:
    """Grouped bar chart comparing course outlines, local jobs, and international jobs by programme."""
    if df.empty:
        return None

    data = df.copy()
    required = {"programme", "course_outlines", "local_jobs", "international_jobs"}
    if not required.issubset(data.columns):
        return None

    melted = data.melt(
        id_vars="programme",
        value_vars=["course_outlines", "local_jobs", "international_jobs"],
        var_name="Series",
        value_name="Count",
    )

    labels = {
        "course_outlines": "Course Outlines",
        "local_jobs": "Local Job Descriptions",
        "international_jobs": "International Job Descriptions",
    }
    melted["Series"] = melted["Series"].map(labels)

    fig = px.bar(
        melted,
        x="programme",
        y="Count",
        color="Series",
        barmode="group",
        color_discrete_map={
            "Course Outlines": PRIMARY_BLUE,
            "Local Job Descriptions": ACCENT_BLUE,
            "International Job Descriptions": LIGHT_BLUE,
        },
        **_base_kwargs(title),
    )

    fig.update_traces(hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y:,.0f}<extra></extra>")
    fig.update_xaxes(title_text="Programme")
    fig.update_yaxes(title_text="Number of Records")
    _update_layout_common(fig)
    fig.update_layout(margin=dict(t=68, l=52, r=32, b=48), height=404)
    return fig


def programme_alignment_chart(df: pd.DataFrame, title: str = "Alignment Scores by Field") -> go.Figure | None:
    """Bar chart comparing weighted alignment scores across programmes."""
    if df.empty:
        return None

    data = df.copy()
    if {"programme", "rho_caribbean", "rho_international"}.issubset(data.columns):
        melted = data.melt(
            id_vars="programme",
            value_vars=["rho_caribbean", "rho_international"],
            var_name="Series",
            value_name="Score",
        )
        labels = {
            "rho_caribbean": "rho Caribbean",
            "rho_international": "rho International",
        }
        melted["Series"] = melted["Series"].map(labels)

        fig = px.bar(
            melted,
            x="programme",
            y="Score",
            color="Series",
            barmode="group",
            labels={"programme": "Programme", "Score": "Alignment Score"},
            color_discrete_map={
                "rho Caribbean": PRIMARY_BLUE,
                "rho International": LIGHT_BLUE,
            },
            **_base_kwargs(title),
        )
        fig.update_traces(hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y:.4f}<extra></extra>")
        fig.update_xaxes(title_text="Programme")
        fig.update_yaxes(title_text="Alignment Score", range=[0, 1])
        _update_layout_common(fig)
        fig.update_layout(showlegend=True, margin=dict(t=68, l=52, r=32, b=48), height=400)
        return fig

    if not {"programme", "alignment_score"}.issubset(data.columns):
        return None

    fig = px.bar(
        data,
        x="programme",
        y="alignment_score",
        labels={"programme": "Programme", "alignment_score": "Alignment Score"},
        color="programme",
        color_discrete_map={
            "Computer Science": PRIMARY_BLUE,
            "Information Technology": ACCENT_BLUE,
            "Artificial Intelligence": LIGHT_BLUE,
        },
        **_base_kwargs(title),
    )

    fig.update_traces(hovertemplate="<b>%{x}</b><br>Alignment: %{y:.3f}<extra></extra>")
    fig.update_xaxes(title_text="Programme")
    fig.update_yaxes(title_text="Alignment Score", range=[0, 1])
    _update_layout_common(fig)
    fig.update_layout(showlegend=True, margin=dict(t=68, l=52, r=32, b=48), height=400)
    return fig


def thematic_count_chart(df: pd.DataFrame, title: str = "Thematic Area Counts") -> go.Figure | None:
    """
    Bar chart showing count of thematic areas.
    
    Sorted descending for visual hierarchy.
    """
    if df.empty:
        return None
    
    data = df.copy()
    
    # Remove NaN values before processing
    if "thematic_count" in data.columns:
        data = data.dropna(subset=["thematic_count"])
        data = data.sort_values("thematic_count", ascending=False)
    
    if data.empty:
        return None
    
    fig = px.bar(
        data,
        x="thematic_area",
        y="thematic_count",
        labels={
            "thematic_area": "Thematic Area",
            "thematic_count": "Number of Occurrences",
        },
        **_base_kwargs(title),
    )
    
    fig.update_traces(
        marker=dict(color=ACCENT_BLUE, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
    )
    
    fig.update_xaxes(title_text="Thematic Area", tickangle=-45)
    fig.update_yaxes(title_text="Count")
    
    _update_layout_common(fig)
    return fig


def closeness_chart(df: pd.DataFrame, title: str = "Closeness Metric by Thematic Area") -> go.Figure | None:
    """
    Vertical bar chart for closeness scores.
    
    Higher values = better alignment. Sorted ascending for visual flow.
    """
    if df.empty:
        return None
    
    data = df.copy()
    
    # Remove NaN values before processing
    if "closeness" in data.columns:
        data = data.dropna(subset=["closeness"])
        data = data.sort_values("closeness", ascending=True)
    
    if data.empty:
        return None
    
    fig = px.bar(
        data,
        x="thematic_area",
        y="closeness",
        labels={
            "thematic_area": "Thematic Area",
            "closeness": "Closeness Score",
        },
        **_base_kwargs(title),
    )
    
    fig.update_traces(
        marker=dict(color=LIGHT_BLUE, line=dict(color=PRIMARY_BLUE, width=1.5)),
        hovertemplate="<b>%{x}</b><br>Closeness: %{y:.3f}<extra></extra>",
    )
    
    fig.update_xaxes(title_text="Thematic Area", tickangle=-45)
    fig.update_yaxes(title_text="Closeness Score", range=[0, 0.3])
    
    _update_layout_common(fig)
    fig.update_layout(margin=dict(t=80, l=60, r=40, b=70), height=420)
    return fig


def alignment_score_chart(
    df: pd.DataFrame, title: str = "Alignment Score by Thematic Area"
) -> go.Figure | None:
    """
    Bar chart showing alignment scores per thematic area.
    
    Sorted descending to highlight best-performing areas.
    """
    if df.empty:
        return None
    
    data = df.copy()
    
    # Remove NaN values before processing
    if "alignment_score" in data.columns:
        data = data.dropna(subset=["alignment_score"])
        data = data.sort_values("alignment_score", ascending=False)
    
    if data.empty:
        return None
    
    fig = px.bar(
        data,
        x="thematic_area",
        y="alignment_score",
        labels={
            "thematic_area": "Thematic Area",
            "alignment_score": "Alignment Score",
        },
        **_base_kwargs(title),
    )
    
    fig.update_traces(
        marker=dict(color=PRIMARY_BLUE, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Alignment: %{y:.3f}<extra></extra>",
    )
    
    fig.update_xaxes(title_text="Thematic Area", tickangle=-45)
    fig.update_yaxes(title_text="Alignment Score", range=[0, 1])
    
    _update_layout_common(fig)
    return fig


def course_vs_jobs_chart(
    cs_courses: int, it_courses: int, cs_jobs: int, it_jobs: int,
    title: str = "Course Outlines vs Job Postings"
) -> go.Figure | None:
    """
    Grouped bar chart comparing course outlines and job postings by thematic area.
    
    Shows CS and IT side-by-side with two bars each: courses and jobs.
    """
    data = pd.DataFrame({
        "Thematic Area": ["Computer Science", "Computer Science", "Information Technology", "Information Technology"],
        "Type": ["Course Outlines", "Job Postings", "Course Outlines", "Job Postings"],
        "Count": [cs_courses, cs_jobs, it_courses, it_jobs],
    })
    
    fig = px.bar(
        data,
        x="Thematic Area",
        y="Count",
        color="Type",
        barmode="group",
        labels={"Count": "Number of Records"},
        color_discrete_map={
            "Course Outlines": PRIMARY_BLUE,
            "Job Postings": ACCENT_BLUE,
        },
        **_base_kwargs(title),
    )
    
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y:,.0f}<extra></extra>",
    )
    
    fig.update_xaxes(title_text="Thematic Area")
    fig.update_yaxes(title_text="Number of Records")
    
    _update_layout_common(fig)
    return fig
