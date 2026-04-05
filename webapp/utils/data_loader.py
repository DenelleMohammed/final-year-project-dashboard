"""Data loading and summarisation helpers for the alignment dashboard."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

# ==================== CONFIGURATION ====================
# Change these paths to point to your actual data files
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "out"

# CSV result files - these contain the main analysis results
CS_RESULTS_PATH = OUT_DIR / "cs_results.csv"
IT_RESULTS_PATH = OUT_DIR / "it_results.csv"
CS_ALIGNMENT_PATH = OUT_DIR / "cs_alignment_score.csv"
IT_ALIGNMENT_PATH = OUT_DIR / "it_alignment_score.csv"
WEIGHTED_ALIGNMENT_PATH = OUT_DIR / "weighted_alignment_scores.csv"
COURSE_COUNTS_PATH = OUT_DIR / "course_counts.csv"

# Fallback alternatives - tried if primary file not found
FALLBACKS = {
    CS_ALIGNMENT_PATH: [OUT_DIR / "cs_alignment_scores.csv"],
    IT_ALIGNMENT_PATH: [OUT_DIR / "it_alignment.csv"],
}

# JSONL sources for record counting
CS_COURSE_PATH = OUT_DIR / "cs_course_skills.jsonl"
IT_COURSE_PATH = OUT_DIR / "it_course_skills.jsonl"
CS_LOCAL_JOBS_PATH = OUT_DIR / "local_cs_skills.jsonl"
IT_LOCAL_JOBS_PATH = OUT_DIR / "local_it_skills.jsonl"
CS_INTL_JOBS_PATH = OUT_DIR / "international_cs_skills.jsonl"
IT_INTL_JOBS_PATH = OUT_DIR / "international_it_skills.jsonl"
UNRELATED_JOBS_PATH = OUT_DIR / "unrelated_skills.jsonl"
AI_JOBS_PATH = OUT_DIR / "ai_skills.jsonl"


# ==================== PLACEHOLDER DATA ====================


@st.cache_data(show_spinner=False)
def _placeholder_results(label: str) -> pd.DataFrame:
    """Generate example placeholder data when CSV files are missing."""
    if label.lower() == "cs":
        areas = ["Data Science", "Software Engineering", "Networks", "AI Systems"]
    else:
        areas = ["Cyber Security", "Data Analytics", "Cloud Computing", "IT Support"]
    
    return pd.DataFrame(
        {
            "thematic_area": areas,
            "thematic_count": [15, 12, 9, 7],
            "closeness": [0.82, 0.76, 0.71, 0.68],
            "alignment_score": [0.85, 0.78, 0.73, 0.70],
        }
    )


@st.cache_data(show_spinner=False)
def _placeholder_jsonl_counts() -> dict[str, int]:
    """Generate example record counts when JSONL files are missing."""
    return {
        "CS course outlines": 42,
        "IT course outlines": 38,
        "Local CS job posts": 156,
        "Local IT job posts": 142,
        "Intl CS job posts": 203,
        "Intl IT job posts": 187,
        "AI job posts": 95,
        "Unrelated job posts": 23,
    }


# ==================== DATA LOADING ====================


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names and create expected column aliases.
    
    Converts various naming conventions to standard names:
    - dataset/area → thematic_area
    - count → thematic_count
    - alignment → alignment_score
    
    Creates default columns if missing:
    - thematic_count: defaults to 1 per row if absent
    - closeness: defaults to NaN if absent
    """
    data = df.copy()
    data.columns = [c.strip().lower().replace(" ", "_") for c in data.columns]
    
    # Create standard aliases
    if "dataset" in data.columns and "thematic_area" not in data.columns:
        data["thematic_area"] = data["dataset"]
    if "area" in data.columns and "thematic_area" not in data.columns:
        data["thematic_area"] = data["area"]
    if "count" in data.columns and "thematic_count" not in data.columns:
        data["thematic_count"] = data["count"]
    if "alignment" in data.columns and "alignment_score" not in data.columns:
        data["alignment_score"] = data["alignment"]
    
    # Create defaults for missing critical columns
    if "thematic_count" not in data.columns:
        # If no count column exists, default to 1 per row
        data["thematic_count"] = 1
    
    if "closeness" not in data.columns:
        # If no closeness metric, set to NaN (will be handled gracefully)
        data["closeness"] = float('nan')
    
    if "alignment_score" not in data.columns:
        # If no alignment score, set to NaN (will be handled gracefully)
        data["alignment_score"] = float('nan')
    
    return data


def _existing_candidates(primary: Path) -> list[Path]:
    """Return list of candidate paths: primary first, then fallbacks."""
    candidates = [primary]
    if primary in FALLBACKS:
        candidates.extend(FALLBACKS[primary])
    return candidates


@st.cache_data(show_spinner=False)
def load_course_counts() -> pd.DataFrame:
    """Load the course/job summary counts file if it is available."""
    if not COURSE_COUNTS_PATH.exists():
        return pd.DataFrame()

    try:
        raw = pd.read_csv(COURSE_COUNTS_PATH)
    except Exception as exc:
        st.error(f"Error reading {COURSE_COUNTS_PATH.name}: {exc}")
        return pd.DataFrame()

    data = raw.copy()
    data.columns = [c.strip().lower().replace(" ", "_") for c in data.columns]

    aliases = {
        "course_counts": "course_count",
        "local_job_counts": "local_job_count",
        "international_job_counts": "international_job_count",
    }
    for source, target in aliases.items():
        if source in data.columns and target not in data.columns:
            data[target] = data[source]

    for column in ["thematic_area", "course_count", "local_job_count", "international_job_count"]:
        if column not in data.columns:
            data[column] = "" if column == "thematic_area" else 0

    for column in ["course_count", "local_job_count", "international_job_count"]:
        data[column] = pd.to_numeric(data[column], errors="coerce").fillna(0)

    return data[["thematic_area", "course_count", "local_job_count", "international_job_count"]]


def _find_course_counts_row(dataset: str) -> pd.Series | None:
    """Return the exact course_counts.csv row for a programme if available."""
    course_counts = load_course_counts()
    if course_counts.empty:
        return None

    dataset = dataset.lower()
    lookup = {
        "cs": "computer science",
        "it": "information technology",
    }
    target = lookup.get(dataset)
    if target is None:
        raise ValueError("dataset must be 'cs' or 'it'")

    matches = course_counts[course_counts["thematic_area"].astype(str).str.strip().str.lower() == target]
    if matches.empty:
        return None

    return matches.iloc[0]


def _get_ai_job_count() -> int:
    """Return the AI job count from course_counts.csv when available."""
    course_counts = load_course_counts()
    if not course_counts.empty:
        matches = course_counts[course_counts["thematic_area"].astype(str).str.strip().str.lower() == "artificial intelligence"]
        if not matches.empty:
            return int(matches.iloc[0]["international_job_count"])

    return int(count_jsonl_records().get("AI job posts", 0))


@st.cache_data(show_spinner=False)
def load_csv_with_fallback(primary: Path, placeholder_label: str) -> pd.DataFrame:
    """
    Load CSV from primary path, checking fallback filenames if needed.
    
    Returns placeholder data if all candidates fail, with a warning message.
    """
    for candidate in _existing_candidates(primary):
        if candidate.exists():
            try:
                raw = pd.read_csv(candidate)
                return _standardize_columns(raw)
            except Exception as exc:
                st.error(f"Error reading {candidate.name}: {exc}")
                break
    
    # No files found, use placeholder
    st.warning(
        f"📁 Data file not found. Using example data for {placeholder_label.upper()}. "
        f"Place your data at: `{primary}`"
    )
    return _placeholder_results(placeholder_label)


# ==================== PUBLIC DATA API ====================


def load_results(dataset: str) -> pd.DataFrame:
    """Load results for Computer Science or Information Technology."""
    dataset = dataset.lower()
    if dataset == "cs":
        return load_csv_with_fallback(CS_RESULTS_PATH, "cs")
    elif dataset == "it":
        return load_csv_with_fallback(IT_RESULTS_PATH, "it")
    else:
        raise ValueError("dataset must be 'cs' or 'it'")


def load_alignment(dataset: str) -> pd.DataFrame:
    """Load alignment scores for a specific dataset."""
    dataset = dataset.lower()
    if dataset == "cs":
        return load_csv_with_fallback(CS_ALIGNMENT_PATH, "cs")
    elif dataset == "it":
        return load_csv_with_fallback(IT_ALIGNMENT_PATH, "it")
    else:
        raise ValueError("dataset must be 'cs' or 'it'")


@st.cache_data(show_spinner=False)
def load_weighted_alignment() -> pd.DataFrame:
    """Load pre-computed weighted alignment scores if available."""
    if WEIGHTED_ALIGNMENT_PATH.exists():
        try:
            return pd.read_csv(WEIGHTED_ALIGNMENT_PATH)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()


def _find_weighted_row(weighted: pd.DataFrame, dataset: str) -> pd.Series | None:
    """Locate a weighted alignment row for a programme if possible."""
    if weighted.empty:
        return None

    dataset = dataset.lower()
    name_map = {
        "cs": ["computer science", "cs"],
        "it": ["information technology", "it"],
    }
    matches = name_map.get(dataset, [dataset])

    column_lookup = {column.lower(): column for column in weighted.columns}
    for col in ["programme", "dataset", "category", "program"]:
        actual_col = column_lookup.get(col)
        if actual_col is not None:
            values = weighted[actual_col].astype(str).str.lower()
            for match in matches:
                filtered = weighted[values.str.contains(match, na=False)]
                if not filtered.empty:
                    return filtered.iloc[0]

    return None


@st.cache_data(show_spinner=False)
def get_programme_summary(dataset: str) -> dict[str, float | int]:
    """Return static summary values for a programme header card row."""
    dataset = dataset.lower()
    counts = count_jsonl_records()
    weighted = load_weighted_alignment()
    row = _find_weighted_row(weighted, dataset)
    course_row = _find_course_counts_row(dataset)

    if course_row is not None:
        course_count = int(course_row["course_count"])
        local_jobs = int(course_row["local_job_count"])
        intl_jobs = int(course_row["international_job_count"])
    elif dataset == "cs":
        course_count = counts.get("CS course outlines", 0)
        local_jobs = counts.get("Local CS job posts", 0)
        intl_jobs = counts.get("Intl CS job posts", 0)
    elif dataset == "it":
        course_count = counts.get("IT course outlines", 0)
        local_jobs = counts.get("Local IT job posts", 0)
        intl_jobs = counts.get("Intl IT job posts", 0)
    else:
        raise ValueError("dataset must be 'cs' or 'it'")

    local_alignment = None
    intl_alignment = None
    weighted_local_jobs = None
    weighted_intl_jobs = None
    ai_jobs = _get_ai_job_count()
    if row is not None:
        for local_col in ["rho Caribbean", "rho_caribbean", "local_alignment", "local score"]:
            if local_col in row.index:
                local_alignment = float(row[local_col])
                break
        for intl_col in ["rho International", "rho_international", "international_alignment", "intl score"]:
            if intl_col in row.index:
                intl_alignment = float(row[intl_col])
                break
        for local_jobs_col in ["JD Count (Local)", "jd count (local)", "local_jobs"]:
            if local_jobs_col in row.index:
                weighted_local_jobs = int(row[local_jobs_col])
                break
        for intl_jobs_col in ["JD Count (Intl)", "jd count (intl)", "intl_jobs"]:
            if intl_jobs_col in row.index:
                weighted_intl_jobs = int(row[intl_jobs_col])
                break

    if weighted_local_jobs is not None:
        local_jobs = weighted_local_jobs
    if weighted_intl_jobs is not None:
        intl_jobs = weighted_intl_jobs

    if local_alignment is None:
        local_alignment = 0.0 if course_count == 0 else 0.72
    if intl_alignment is None:
        intl_alignment = 0.0 if course_count == 0 else 0.68

    return {
        "course_count": int(course_count),
        "local_jobs": int(local_jobs),
        "intl_jobs": int(intl_jobs),
        "ai_jobs": int(ai_jobs),
        "local_alignment": float(local_alignment),
        "intl_alignment": float(intl_alignment),
    }


@st.cache_data(show_spinner=False)
def get_overview_alignment_data() -> pd.DataFrame:
    """Return the weighted Caribbean and International alignment scores for CS and IT only."""
    weighted = load_weighted_alignment()
    if weighted.empty:
        return pd.DataFrame(
            [
                {"programme": "Computer Science", "rho_caribbean": 0.0, "rho_international": 0.0},
                {"programme": "Information Technology", "rho_caribbean": 0.0, "rho_international": 0.0},
            ]
        )

    rows: list[dict[str, float | str]] = []
    for label, dataset in [("Computer Science", "cs"), ("Information Technology", "it")]:
        row = _find_weighted_row(weighted, dataset)
        if row is None:
            rows.append({"programme": label, "rho_caribbean": 0.0, "rho_international": 0.0})
            continue

        caribbean = 0.0
        international = 0.0
        for local_col in ["rho Caribbean", "rho_caribbean", "local_alignment"]:
            if local_col in row.index:
                caribbean = float(row[local_col])
                break
        for intl_col in ["rho International", "rho_international", "international_alignment"]:
            if intl_col in row.index:
                international = float(row[intl_col])
                break

        rows.append(
            {
                "programme": label,
                "rho_caribbean": caribbean,
                "rho_international": international,
            }
        )

    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def get_closeness_metric_data(dataset: str) -> pd.DataFrame:
    """Return closeness data for the requested programme from the results CSV."""
    dataset = dataset.lower()
    results = load_results(dataset)

    if results.empty or not {"thematic_area", "closeness"}.issubset(results.columns):
        return pd.DataFrame(columns=["thematic_area", "closeness"])

    return results[["thematic_area", "closeness"]].copy()


@st.cache_data(show_spinner=False)
def count_jsonl_records() -> dict[str, int]:
    """Count summary records from the CSV summary file, with JSONL fallback."""
    course_counts = load_course_counts()
    if not course_counts.empty:
        counts = {
            "CS course outlines": 0,
            "IT course outlines": 0,
            "Local CS job posts": 0,
            "Local IT job posts": 0,
            "Intl CS job posts": 0,
            "Intl IT job posts": 0,
            "AI job posts": 0,
            "Unrelated job posts": 0,
        }

        area_map = {
            "computer science": {
                "course": "CS course outlines",
                "local": "Local CS job posts",
                "intl": "Intl CS job posts",
            },
            "information technology": {
                "course": "IT course outlines",
                "local": "Local IT job posts",
                "intl": "Intl IT job posts",
            },
            "artificial intelligence": {
                "intl": "AI job posts",
            },
        }

        for _, row in course_counts.iterrows():
            area = str(row["thematic_area"]).strip().lower()
            mapping = area_map.get(area)
            if mapping is None:
                continue

            if "course" in mapping:
                counts[mapping["course"]] = int(row["course_count"])
            if "local" in mapping:
                counts[mapping["local"]] = int(row["local_job_count"])
            if "intl" in mapping:
                counts[mapping["intl"]] = int(row["international_job_count"])

        return counts

    paths = {
        "CS course outlines": CS_COURSE_PATH,
        "IT course outlines": IT_COURSE_PATH,
        "Local CS job posts": CS_LOCAL_JOBS_PATH,
        "Local IT job posts": IT_LOCAL_JOBS_PATH,
        "Intl CS job posts": CS_INTL_JOBS_PATH,
        "Intl IT job posts": IT_INTL_JOBS_PATH,
        "AI job posts": AI_JOBS_PATH,
    }
    
    counts: dict[str, int] = {}
    for label, path in paths.items():
        if path.exists():
            try:
                with path.open("r", encoding="utf-8") as f:
                    counts[label] = sum(1 for _ in f)
            except Exception:
                counts[label] = 0
        else:
            counts[label] = 0
    
    # If all counts are 0, use placeholders to maintain demo readiness
    if all(v == 0 for v in counts.values()):
        return _placeholder_jsonl_counts()
    
    return counts


def get_course_vs_jobs_data() -> dict[str, int]:
    """
    Aggregate course outlines and job postings by thematic area.
    
    Returns dict with keys: cs_courses, it_courses, cs_jobs, it_jobs
    """
    counts = count_jsonl_records()
    
    cs_courses = counts.get("CS course outlines", 0)
    it_courses = counts.get("IT course outlines", 0)
    
    # Sum all CS jobs (local + international + AI portion)
    cs_jobs = (
        counts.get("Local CS job posts", 0) +
        counts.get("Intl CS job posts", 0) +
        (counts.get("AI job posts", 0) // 2)  # Split AI jobs proportionally
    )
    
    # Sum all IT jobs (local + international + AI portion)
    it_jobs = (
        counts.get("Local IT job posts", 0) +
        counts.get("Intl IT job posts", 0) +
        (counts.get("AI job posts", 0) - counts.get("AI job posts", 0) // 2)  # Remaining AI jobs
    )
    
    return {
        "cs_courses": cs_courses,
        "it_courses": it_courses,
        "cs_jobs": cs_jobs,
        "it_jobs": it_jobs,
    }


def get_local_jobs_data() -> dict[str, int]:
    """Get local job postings by thematic area."""
    counts = count_jsonl_records()
    return {
        "cs_courses": counts.get("CS course outlines", 0),
        "it_courses": counts.get("IT course outlines", 0),
        "cs_jobs": counts.get("Local CS job posts", 0),
        "it_jobs": counts.get("Local IT job posts", 0),
    }


def get_international_jobs_data() -> dict[str, int]:
    """Get international job postings by thematic area."""
    counts = count_jsonl_records()
    return {
        "cs_courses": counts.get("CS course outlines", 0),
        "it_courses": counts.get("IT course outlines", 0),
        "cs_jobs": counts.get("Intl CS job posts", 0),
        "it_jobs": counts.get("Intl IT job posts", 0),
    }


def summarise_results(df: pd.DataFrame) -> dict:
    """Calculate summary statistics for a results dataframe."""
    if df.empty:
        return {
            "thematic_areas": 0,
            "total_count": 0,
            "avg_closeness": 0.0,
            "avg_alignment": 0.0,
        }
    
    return {
        "thematic_areas": (
            df["thematic_area"].nunique() if "thematic_area" in df.columns else len(df)
        ),
        "total_count": (
            float(df["thematic_count"].sum()) if "thematic_count" in df.columns else float(len(df))
        ),
        "avg_closeness": float(
            df["closeness"].mean() if "closeness" in df.columns else 0.0
        ),
        "avg_alignment": float(
            df["alignment_score"].mean() if "alignment_score" in df.columns else 0.0
        ),
    }


def final_weighted_score(dataset: str) -> Optional[float]:
    """
    Calculate final weighted alignment score for a programme.
    
    Tries to load from weighted_alignment_scores.csv first,
    then falls back to averaging the alignment file.
    """
    dataset = dataset.lower()
    
    # Try weighted file first
    weighted = load_weighted_alignment()
    if not weighted.empty:
        candidates = ["dataset_type", "category", "dataset", "programme", "program"]
        for col in candidates:
            if col in weighted.columns:
                filtered = weighted[weighted[col].astype(str).str.lower() == dataset]
                if not filtered.empty:
                    score_col = (
                        "alignment_score"
                        if "alignment_score" in filtered.columns
                        else filtered.columns[-1]
                    )
                    try:
                        return float(filtered[score_col].mean())
                    except (ValueError, TypeError):
                        pass
    
    # Fall back to averaging the alignment file
    alignment_df = load_alignment(dataset)
    if alignment_df.empty:
        return None
    
    if "alignment_score" in alignment_df.columns:
        return float(alignment_df["alignment_score"].mean())
    
    return None
