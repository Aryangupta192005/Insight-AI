# SalesInsight — Suggested Three-Member Project Division

This is a proposed division of responsibilities for a three-person college team. It describes how the work could be divided; it is not a claim that three people actually contributed.

## Member 1 — Data Management
**Files:** `data_manager.py`, `data/sample_sales.csv`

- Prepare reproducible synthetic sample sales data.
- Load CSV files and validate required columns.
- Normalize date and numeric fields.
- Report missing values and exact duplicate rows.
- Provide conservative cleaning functions.

## Member 2 — Sales Analytics
**Files:** `analytics.py`, `charts.py`

- Calculate total sales, total profit, unique orders and average order value.
- Aggregate monthly sales, category sales and region sales.
- Generate business observations from calculated values.
- Build reusable Plotly chart functions.

## Member 3 — Dashboard and Integration
**Files:** `app.py`, `README.md`, `tests/test_analytics.py`, `run_windows.bat`

- Build Streamlit navigation, sidebar and filters.
- Connect the data-management and analytics modules.
- Display KPIs, charts, observations and data-quality reports.
- Add CSV downloads, documentation and automated tests.

## Module dependencies

```text
data/sample_sales.csv
        |
        v
 data_manager.py  -----> app.py <----- analytics.py
                           |                |
                           |                v
                           |             charts.py
                           v
                  Streamlit dashboard

tests/test_analytics.py tests data_manager.py and analytics.py
```

`app.py` is the integration point. `analytics.py` uses the preparation function from `data_manager.py`. `charts.py` accepts already-aggregated data and renders Plotly figures. The tests focus on deterministic data and analytics behavior.
