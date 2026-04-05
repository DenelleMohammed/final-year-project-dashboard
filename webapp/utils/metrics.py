"""Helper functions for rendering metric cards and formatting values."""
from __future__ import annotations

import math
import textwrap
from typing import Iterable

import streamlit as st


def _format_value(value) -> str:
    """Format a value for display in metric cards."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "—"
    if isinstance(value, float):
        if abs(value) >= 1000:
            return f"{value:,.0f}"
        # Display scores with 2-3 decimals for precision
        if 0 <= value <= 1:
            return f"{value:.3f}"
        return f"{value:,.2f}"
    return str(value)


def _render_split_value(value: dict) -> str:
    """Render a segmented value block for cards that need multiple values."""
    segments = value.get("segments")
    if segments:
        items = []
        for segment in segments:
            label = segment.get("label", "")
            rendered_value = _format_value(segment.get("value"))
            items.append(
                textwrap.dedent(
                    f"""
                    <div class="metric-tab-split__item">
                        <span class="metric-tab-split__value">{rendered_value}</span>
                        <span class="metric-tab-split__label">{label}</span>
                    </div>
                    """
                ).strip()
            )

        split_class = "metric-tab-split metric-tab-split--multi" if len(items) > 2 else "metric-tab-split"
        return textwrap.dedent(
            f"""
            <div class="{split_class}">
                {''.join(items)}
            </div>
            """
        ).strip()

    left_label = value.get("left_label", "Left")
    right_label = value.get("right_label", "Right")
    left_value = _format_value(value.get("left_value"))
    right_value = _format_value(value.get("right_value"))

    return textwrap.dedent(
        f"""
        <div class="metric-tab-split">
            <div class="metric-tab-split__item">
                <span class="metric-tab-split__value">{left_value}</span>
                <span class="metric-tab-split__label">{left_label}</span>
            </div>
            <div class="metric-tab-split__item">
                <span class="metric-tab-split__value">{right_value}</span>
                <span class="metric-tab-split__label">{right_label}</span>
            </div>
        </div>
        """
    ).strip()


def metric_cards(cards: Iterable[dict], columns: int = 4) -> None:
    """
    Render professional metric cards in responsive columns.

    Args:
        cards: List of dict with keys: label, value, delta (optional), help (optional)
        columns: Number of columns to display (default 4 for 4-card layouts)
    """
    cards = list(cards)
    num_cards = len(cards)
    
    # Determine columns intelligently
    if num_cards < columns:
        cols = st.columns(num_cards)
    else:
        cols = st.columns(columns)
    
    for idx, card in enumerate(cards):
        col = cols[idx % len(cols)]
        with col:
            subtext = card.get("help", "")
            raw_value = card.get("value")
            if isinstance(raw_value, dict):
                card_class = "metric-tab-card metric-tab-card--split"
                st.markdown(
                    textwrap.dedent(
                        f"""
                        <div class="{card_class}">
                            <div class="metric-tab-header">{card.get('label', '')}</div>
                            {_render_split_value(raw_value)}
                        </div>
                        """
                    ).strip(),
                    unsafe_allow_html=True,
                )
                continue
            else:
                card_class = "metric-tab-card"
                if card.get("match_split_height"):
                    card_class += " metric-tab-card--tall"
                value_markup = f"<div class=\"metric-tab-value\">{_format_value(raw_value)}</div>"
                subtext_markup = f'<div class="metric-tab-subtext">{subtext}</div>' if subtext else ''
            st.markdown(
                f"""
                <div class="{card_class}">
                    <div class="metric-tab-header">{card.get('label', '')}</div>
                    {value_markup}
                    {subtext_markup}
                </div>
                """,
                unsafe_allow_html=True,
            )
