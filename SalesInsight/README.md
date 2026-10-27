# SalesInsight: Sales Data Analysis and Visualization Dashboard

A beginner-friendly B.Tech IT mini-project that turns a CSV sales dataset into an interactive dashboard. It uses Python, Streamlit, Pandas and Plotly and runs locally without an API key, cloud database, authentication or machine learning.

> **Dataset note:** `data/sample_sales.csv` contains synthetic demonstration data generated with a fixed random seed. It is not real company data.

## Project abstract

Businesses often store sales records in spreadsheets, but raw rows can make it difficult to see overall performance or compare periods, categories and regions. SalesInsight loads sales data from CSV, validates the required columns, calculates key performance indicators (KPIs), creates interactive charts and provides basic data-quality reports. Users can filter records, inspect the data and download filtered or cleaned CSV files.

## Problem statement

How can a user quickly summarize sales performance and identify basic patterns from a CSV file without needing a complex analytics platform?

## Objectives

- Summarize sales, profit, order count and average order value.
- Visualize monthly sales, sales by category and sales by region.
- Support a supplied sample dataset and user-uploaded CSV files.
- Report missing values and duplicate rows.
- Provide downloadable filtered and cleaned datasets.
- Demonstrate modular Python development and basic testing.

## Features

- Dashboard with four data-driven KPI cards.
- Date, category and region filters.
- Interactive Plotly charts.
- CSV upload and one-click return to sample data.
- Data Explorer with preview, data types and missing-value counts.
- Data Cleaning page with duplicate detection and conservative cleaning options.
- Business observations computed from the selected data.
- CSV exports for filtered, current and cleaned data.
- Friendly validation messages when sales columns are missing.
- Automated tests for core calculations and data handling.

## Technologies used

| Technology | Purpose |
|---|---|
| Python 3.10+ | Application language |
| Streamlit | Local interactive web interface |
| Pandas | CSV loading, cleaning and aggregations |
| Plotly Express | Interactive charts |
| NumPy | Reproducible synthetic dataset generation |
| pytest | Automated tests |

## Architecture

1. **Data input:** load the bundled CSV or a user-uploaded CSV.
2. **Data management (`data_manager.py`):** validate columns, parse dates/numbers and report data quality.
3. **Analytics (`analytics.py`):** calculate KPIs and grouped summaries from current data.
4. **Visualization (`charts.py`):** render monthly, category and region charts.
5. **Interface (`app.py`):** connect modules, show filters and present results.
6. **Export:** download filtered or cleaned rows as CSV.

See [`PROJECT_DIVISION.md`](PROJECT_DIVISION.md) for the proposed three-member work split and module dependencies.

## Folder structure

```text
SalesInsight/
├── app.py
├── data_manager.py
├── analytics.py
├── charts.py
├── requirements.txt
├── run_windows.bat
├── README.md
├── PROJECT_DIVISION.md
├── .gitignore
├── data/
│   └── sample_sales.csv
└── tests/
    └── test_analytics.py
```

## Installation and execution on Windows

### Option A — easiest

1. Install **Python 3.10 or newer** from [python.org/downloads](https://www.python.org/downloads/).
2. During installation, enable **“Add python.exe to PATH”**.
3. Extract `SalesInsight_Project.zip`.
4. Open the extracted `SalesInsight` folder.
5. Double-click `run_windows.bat`. The first run needs an internet connection to install packages.
6. Keep the terminal window open. Streamlit normally opens the dashboard in your browser at `http://localhost:8501`. If it does not, copy that address into your browser.

### Option B — manual commands

Open Command Prompt or the VS Code terminal in the `SalesInsight` project folder and run:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Then visit `http://localhost:8501` if the browser does not open automatically.

### Stop the application

Press `Ctrl+C` in the terminal running Streamlit.

## How to use the dashboard

1. Start on **Dashboard**; the synthetic sample data loads automatically.
2. Change the date range, categories or regions to update the KPIs, charts and observations.
3. Use **Data Explorer** to preview rows and inspect data types and missing values.
4. Use **Data Cleaning** to see duplicates and missing values, choose whether to remove exact duplicate or fully empty rows, then download the cleaned copy.
5. Upload your own CSV from the sidebar. Sales analytics require these exact column names:

```text
Order ID, Order Date, Region, Category, Product, Quantity, Unit Price, Sales, Profit
```

Dates should be parseable and numeric fields should contain numeric values. Invalid values are coerced to missing values and excluded from applicable grouped summaries. Generic exploration still works if required sales columns are absent.

## Testing

From the project folder, activate the virtual environment and run:

```bat
python -m pytest -q
```

The tests cover KPI calculations, monthly/category aggregation, missing-column reporting, date/numeric parsing, duplicate handling, deterministic sample data and empty datasets.

## Expected outputs

- Four KPIs at the top of the dashboard.
- A monthly sales line chart.
- Sales comparison charts for category and region.
- Calculated business observations based on filtered records.
- Table previews and data-quality summaries.
- Downloadable CSV files.

Exact values depend on the selected data and filters; the dashboard does not hardcode KPI results.

## 3–5 minute presentation guide

### Suggested speaking sequence

**0:00–0:30 — Problem and purpose**  
“SalesInsight is a simple sales analytics dashboard. Raw CSV rows are difficult to summarize manually, so this project helps users understand sales, profit, order count and sales patterns through charts and filters.”

**0:30–1:10 — Technologies and architecture**  
“It is built with Python, Streamlit, Pandas and Plotly. Data is loaded from a CSV, checked by `data_manager.py`, summarized by `analytics.py`, visualized by `charts.py`, and presented through `app.py`.”

**1:10–2:20 — Live dashboard demo**  
Show the four KPI cards, change a category or region filter, and point out that the values and charts update from the filtered rows. Explain that average order value is calculated as total sales per unique order.

**2:20–3:00 — Data quality**  
Open Data Explorer and show column types and missing values. Open Data Cleaning and show duplicate detection and CSV export. Explain that missing values are reported rather than automatically guessed or filled.

**3:00–3:40 — Team division**  
“Member 1 would handle CSV preparation and validation, Member 2 would implement calculations and charts, and Member 3 would integrate the dashboard, exports, documentation and tests. This is our suggested work division.”

**3:40–4:15 — Limitations and conclusion**  
“The sample dataset is synthetic, and the sales analysis expects specific column names. Future work could add column mapping, more filters and PDF reports.”

### Five likely viva questions

**1. Why did you use Streamlit?**  
It lets us build an interactive Python dashboard quickly without writing a separate front end.

**2. What is Pandas used for?**  
Pandas loads CSV files into DataFrames and helps clean, filter, group and summarize the data.

**3. How is average order value calculated?**  
Sales are summed for each unique Order ID, and then the mean of those order totals is calculated.

**4. Why is the sample dataset synthetic?**  
It provides safe, repeatable demonstration data without exposing any real company's sales information.

**5. How does the project handle missing values?**  
It reports missing values, converts invalid dates/numbers to missing values where needed, and avoids guessing replacement values. Users can export the data after the available cleaning options.

## Limitations and future scope

- Synthetic data is for demonstration only.
- Required sales column names must match exactly.
- Basic cleaning removes only exact duplicate rows and fully empty rows; partial missing values are reported but not automatically imputed.
- No forecasting, machine learning, cloud database, authentication or multi-user storage.
- Future improvements could include flexible column mapping, currency settings, more detailed product analysis and PDF reporting.

## License / academic use

This is a learning project template. Review the code, run the tests and understand the calculations before presenting it. Adapt it to your institution's requirements and clearly describe the work you personally complete.
