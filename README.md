# Curriculum–Job Market Alignment Dashboard

A production-ready **Streamlit web application** that visualizes curriculum-job market alignment analysis results. The dashboard presents an NLP-based analysis comparing university course content against job market skill requirements across multiple thematic areas.

## Overview

The app provides three main pages:

1. **Overview** (Home): High-level summary comparing Computer Science and Information Technology programmes
2. **Computer Science**: Detailed CS program results with thematic breakdowns
3. **Information Technology**: Detailed IT program results with thematic breakdowns

Each page displays:
- **Metric cards** with key statistics (courses, jobs, average scores)
- **Interactive Plotly charts** showing thematic counts, closeness metrics, and alignment scores
- **Data tables** for detailed exploration
- **Professional insights** and recommendations

## Design Features

- ✅ **Modern, clean interface** with professional blue color palette
- ✅ **Responsive layout** using Streamlit's responsive grid system
- ✅ **No pie charts** – only bar charts and horizontal bar charts for clarity
- ✅ **Large, readable charts** with clear titles and hover information
- ✅ **Graceful error handling** with placeholder data when files are missing
- ✅ **Full documentation** in captions and interpretation sections
- ✅ **Award-ready presentation** suitable for university demonstrations

## Getting Started

### Prerequisites

- Python 3.9+
- Dependencies: `streamlit`, `plotly`, `pandas` (see [Installation](#installation))

### Installation

Install required packages:

```bash
# From project root
pip install -r requirements.txt

# Or install just the webapp dependencies
pip install streamlit==1.28.1 plotly==5.17.0 pandas==2.2.1
```

### Running the App

From the project root directory:

```bash
streamlit run webapp/app.py
```

The app will open in your default browser at `http://localhost:8501`.

## Data Requirements

The dashboard expects CSV and JSONL files in the `./out/` directory. File paths can be configured in [`utils/data_loader.py`](utils/data_loader.py).

### Required CSV Files

Place these files in `./out/`:

| File | Purpose |
|------|---------|
| `course_counts.csv` | Source of truth for course outline and job description counts |
| `cs_results.csv` | Computer Science analysis results |
| `it_results.csv` | Information Technology analysis results |
| `cs_alignment_score.csv` | CS alignment scores (optional) |
| `it_alignment_score.csv` | IT alignment scores (optional) |
| `weighted_alignment_scores.csv` | Pre-computed weighted scores (optional) |

### CSV Column Requirements

Each CSV should contain these columns (case-insensitive, with automatic aliasing):

```
thematic_area       (or: dataset, area)
thematic_count      (or: count)
closeness
alignment_score     (or: alignment)
```

**Example:**

```csv
thematic_area,thematic_count,closeness,alignment_score
Data Science,15,0.82,0.85
Software Engineering,12,0.76,0.78
Networks,9,0.71,0.73
```

### JSONL Files (fallback for record counts)

Place these JSONL files in `./out/` to populate summary statistics:

| File | Records counted as |
|------|-------------------|
| `cs_course_skills.jsonl` | CS course outlines |
| `it_course_skills.jsonl` | IT course outlines |
| `local_cs_skills.jsonl` | Local CS job posts |
| `local_it_skills.jsonl` | Local IT job posts |
| `international_cs_skills.jsonl` | Intl CS job posts |
| `international_it_skills.jsonl` | Intl IT job posts |
| `ai_skills.jsonl` | AI job posts |

When `course_counts.csv` is present, the dashboard reads course and job counts directly from that file first.

### Placeholder Data

If data files are missing, the app will:
- Display a ⚠️ warning message
- Show realistic placeholder data so demo is still functional
- Continue working without errors

## Project Structure

```
webapp/
├── app.py                    # Main entry point
├── pages/
│   ├── 1_Overview.py         # Overview page
│   ├── 2_Computer_Science.py # CS details page
│   └── 3_Information_Technology.py  # IT details page
├── utils/
│   ├── __init__.py
│   ├── data_loader.py        # Data loading and caching
│   ├── charts.py             # Plotly chart builders
│   ├── metrics.py            # Metric card helpers
│   └── styles.py             # Custom CSS styling
└── README.md                 # This file
```

## Key Components

### 1. Data Loader (`utils/data_loader.py`)

Handles data loading with:
- **Caching** using `@st.cache_data` for performance
- **Fallback logic** for alternative file names
- **Graceful degradation** with placeholder data
- **Column normalization** for flexible CSV formats

**Key functions:**
- `load_results(dataset)` – Load CS or IT results
- `load_alignment(dataset)` – Load alignment scores
- `count_jsonl_records()` – Count records from JSONL files
- `summarise_results(df)` – Calculate summary statistics

### 2. Charts (`utils/charts.py`)

Plotly-based chart builders with professional styling:

- `thematic_count_chart()` – Bar chart of area counts
- `closeness_chart()` – Horizontal bar chart of closeness metrics
- `alignment_score_chart()` – Bar chart of alignment scores

All charts:
- Use consistent blue color palette
- Include informative hover tooltips
- Sort data for visual hierarchy
- Have proper margins and sizing

### 3. Metrics (`utils/metrics.py`)

Reusable metric card rendering:

- `metric_cards(cards, columns)` – Display metric cards in responsive grid
- `_format_value(value)` – Format numbers with appropriate precision

### 4. Styling (`utils/styles.py`)

Custom CSS injection for professional appearance:

- **Color palette**: Blue-themed (deep blue, accent blue, light blue)
- **Typography**: Clear hierarchy with large fonts for headers
- **Components**: Styled boxes, buttons, dividers, info messages
- **Layout**: Generous spacing, readable line heights

## Customization

### Change Data File Paths

Edit `utils/data_loader.py`:

```python
# Lines 8-18
CS_RESULTS_PATH = Path("/your/custom/path/cs_results.csv")
IT_RESULTS_PATH = Path("/your/custom/path/it_results.csv")
# etc...
```

### Modify Color Palette

Edit `utils/styles.py`:

```python
PRIMARY_BLUE = "#1e3a8a"  # Change these hex values
ACCENT_BLUE = "#2563eb"
# etc...
```

### Change Chart Styling

Edit `utils/charts.py`:

```python
def _update_layout_common(fig):
    fig.update_layout(
        height=450,  # Adjust chart height
        # ... other customizations
    )
```

## Performance Optimization

The app uses Streamlit caching to optimize performance:

- **CSV loading** is cached (reloaded only if file changes)
- **JSONL record counting** is cached (recomputed daily by default)
- **Placeholder data** is generated once and cached

For production, you may want to:
- Increase cache TTL in `@st.cache_data` decorators
- Pre-compute aggregations in your data pipeline
- Use a database instead of CSV for large datasets

## Deployment

### Local Development

```bash
streamlit run webapp/app.py
```

### Production Deployment

Popular options:

**Streamlit Cloud** (simplest):
```bash
# Push to GitHub, connect repo to Streamlit Cloud
# Auto-deploys on push
```

**Docker**:
```dockerfile
FROM python:3.9
RUN pip install -r requirements.txt
WORKDIR /app
COPY . /app
EXPOSE 8501
CMD ["streamlit", "run", "webapp/app.py"]
```

**AWS/Azure/GCP**: Deploy the Docker container to your cloud provider

## Troubleshooting

### App won't start

```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run with verbose output
streamlit run webapp/app.py --logger.level=debug
```

### Charts not showing

- Check CSV file paths in `utils/data_loader.py`
- Verify column names match: `thematic_area`, `thematic_count`, `closeness`, `alignment_score`
- Check browser console for JavaScript errors

### Placeholder data showing instead of real data

This is expected if CSV files are not found. To use real data:

1. Ensure CSV files are in `./out/` directory
2. Check file names match paths in `data_loader.py`
3. Verify CSV has required columns (see [CSV Column Requirements](#csv-column-requirements))

### Slow performance

- Check browser's Network tab for slow network requests
- Use `streamlit run --logger.level=warning` to reduce log output
- Consider caching to a database instead of recomputing on each run

## Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

Mobile viewing is supported but charts may be small on phone screens.

## License

This project is part of a final year research project.

## Contact & Support

For questions about:
- **Data preparation**: See [Data Requirements](#data-requirements) section
- **Customization**: Edit relevant utility files in `utils/`
- **Deployment**: Refer to [Deployment](#deployment) section
- **Features**: Review code in individual page files

---

**Last Updated**: 2024  
**Streamlit Version**: 1.28.1+  
**Python**: 3.9+
