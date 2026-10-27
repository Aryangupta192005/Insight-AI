
from pathlib import Path
from datetime import date

import pandas as pd
import streamlit as st

from data_manager import (
    REQUIRED_SALES_COLUMNS,
    clean_data,
    data_quality_report,
    generate_sample_data,
    load_csv,
    prepare_sales_data,
    validate_sales_columns,
)

from analytics import (
    business_observations,
    calculate_kpis,
    monthly_sales,
    sales_by_category,
    sales_by_region,
)

from charts import (
    monthly_sales_chart,
    category_sales_chart,
    region_sales_chart,
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_PATH = BASE_DIR / "data" / "sample_sales.csv"

st.set_page_config(
    page_title="Insight AI | Sales Analytics",
    page_icon="📊",
    layout="wide",
)


# --------------------------------------------------
# THEME-AWARE CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    :root {
        --insight-navy: #17324D;
        --insight-teal: #159A9C;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.2rem;
        max-width: 1500px;
    }

    /* Sidebar follows the active Streamlit theme */
    [data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
        border-right: 1px solid rgba(128, 128, 128, 0.25);
    }

    [data-testid="stSidebar"] * {
        color: var(--text-color);
    }

    /* Hero banner intentionally retains a dark background */
    .hero {
        background: linear-gradient(115deg, #17324D, #23536A);
        padding: 1.35rem 1.6rem;
        border-radius: 15px;
        color: #FFFFFF !important;
        margin-bottom: 1rem;
    }

    .hero h1 {
        color: #FFFFFF !important;
        margin: 0 0 0.35rem 0;
        font-size: 2rem;
    }

    .hero p {
        color: #E2F4F4 !important;
        margin: 0;
    }

    /* KPI cards adapt to light and dark backgrounds */
    .kpi {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid rgba(128, 128, 128, 0.30);
        border-radius: 13px;
        padding: 1rem 1.05rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        min-height: 112px;
    }

    .kpi-label {
        color: var(--text-color) !important;
        opacity: 0.78;
        font-size: 0.88rem;
        margin-bottom: 0.4rem;
    }

    .kpi-value {
        color: var(--text-color) !important;
        font-size: 1.55rem;
        font-weight: 750;
        letter-spacing: -0.4px;
        overflow-wrap: anywhere;
    }

    .kpi-sub {
        color: var(--text-color) !important;
        opacity: 0.78;
        font-size: 0.78rem;
        margin-top: 0.25rem;
    }

    /* Section headings follow the active theme */
    .section-title {
        color: var(--text-color) !important;
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0.8rem 0 0.2rem;
    }

    /* Native Streamlit metric cards */
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid rgba(128, 128, 128, 0.30);
        padding: 1rem;
        border-radius: 12px;
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: var(--text-color) !important;
    }

    /* Keep normal application text theme-aware */
    .stMarkdown,
    .stMarkdown p,
    .stMarkdown li,
    .stCaption,
    label {
        color: var(--text-color);
    }

    /* Make data tables readable in either theme */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

if "source_df" not in st.session_state:
    if SAMPLE_PATH.exists():
        st.session_state.source_df = pd.read_csv(SAMPLE_PATH)
    else:
        st.session_state.source_df = generate_sample_data()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("## 📊 Insight AI")
    st.caption("Sales Data Analysis & Visualization")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Data Explorer",
            "Data Cleaning",
            "About Project",
        ],
        index=0,
    )

    st.divider()

    st.markdown("### Data source")

    upload = st.file_uploader(
        "Upload a CSV file",
        type=["csv"],
        help="Uploading a file replaces the current dataset for this session.",
    )

    if upload is not None:
        try:
            uploaded_df = load_csv(upload)
            st.session_state.source_df = uploaded_df
            st.success(f"Loaded {len(uploaded_df):,} rows.")
        except (ValueError, pd.errors.ParserError, UnicodeDecodeError) as exc:
            st.error(f"Unable to load the CSV file: {exc}")

    if st.button("Restore sample dataset", use_container_width=True):
        if SAMPLE_PATH.exists():
            st.session_state.source_df = pd.read_csv(SAMPLE_PATH)
        else:
            st.session_state.source_df = generate_sample_data()

        st.rerun()

    st.caption("Sample data is synthetic.")


# --------------------------------------------------
# PREPARE CURRENT DATASET
# --------------------------------------------------

raw_df = st.session_state.source_df.copy()

valid_sales, missing_columns = validate_sales_columns(raw_df)


def show_empty(message):
    st.info(message)


def fmt_currency(value):
    return f"₹{value:,.2f}"


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.markdown(
        """
        <div class="hero">
            <h1>Insight AI</h1>
            <p>
                Explore revenue, profit, orders and sales trends
                with an interactive data analytics dashboard.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not valid_sales:
        st.warning(
            "This file can still be explored, but sales analytics need "
            "these columns: " + ", ".join(missing_columns)
        )

        st.caption(
            "Upload a CSV with the required column names, "
            "or restore the sample dataset."
        )

    else:
        try:
            data = prepare_sales_data(raw_df)

            valid_dates = data["Order Date"].dropna()

            # -------------------------------
            # FILTERS
            # -------------------------------

            with st.container(border=True):
                st.markdown("**Filter the dashboard**")

                f1, f2, f3 = st.columns([1.25, 1, 1])

                min_date = (
                    valid_dates.min().date()
                    if not valid_dates.empty
                    else date(2024, 1, 1)
                )

                max_date = (
                    valid_dates.max().date()
                    if not valid_dates.empty
                    else date(2025, 12, 31)
                )

                with f1:
                    date_range = st.date_input(
                        "Order date range",
                        value=(min_date, max_date),
                        min_value=min_date,
                        max_value=max_date,
                    )

                with f2:
                    categories = sorted(
                        data["Category"]
                        .dropna()
                        .astype(str)
                        .unique()
                        .tolist()
                    )

                    selected_categories = st.multiselect(
                        "Category",
                        categories,
                        default=categories,
                    )

                with f3:
                    regions = sorted(
                        data["Region"]
                        .dropna()
                        .astype(str)
                        .unique()
                        .tolist()
                    )

                    selected_regions = st.multiselect(
                        "Region",
                        regions,
                        default=regions,
                    )

            # -------------------------------
            # APPLY FILTERS
            # -------------------------------

            filtered = data.copy()

            if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
                start_date, end_date = date_range

                filtered = filtered[
                    filtered["Order Date"].dt.date.between(
                        start_date,
                        end_date,
                    )
                ]

            filtered = filtered[
                filtered["Category"].astype(str).isin(selected_categories)
            ]

            filtered = filtered[
                filtered["Region"].astype(str).isin(selected_regions)
            ]

            if filtered.empty:
                st.info(
                    "No rows match these filters. Adjust the date range, "
                    "category or region."
                )

            else:
                # -------------------------------
                # KPI CALCULATIONS
                # -------------------------------

                kpis = calculate_kpis(filtered)

                cols = st.columns(4)

                metrics = [
                    (
                        "TOTAL SALES",
                        fmt_currency(kpis["total_sales"]),
                        "Revenue in filtered data",
                    ),
                    (
                        "TOTAL PROFIT",
                        fmt_currency(kpis["total_profit"]),
                        "Profit in filtered data",
                    ),
                    (
                        "ORDERS",
                        f'{kpis["number_of_orders"]:,}',
                        "Unique order IDs",
                    ),
                    (
                        "AVG. ORDER VALUE",
                        fmt_currency(kpis["average_order_value"]),
                        "Sales per order",
                    ),
                ]

                for col, (label, value, sub) in zip(cols, metrics):
                    with col:
                        st.markdown(
                            f"""
                            <div class="kpi">
                                <div class="kpi-label">{label}</div>
                                <div class="kpi-value">{value}</div>
                                <div class="kpi-sub">{sub}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                st.markdown("")

                # -------------------------------
                # CHART DATA
                # -------------------------------

                left, right = st.columns(2)

                month_data = monthly_sales(filtered)
                cat_data = sales_by_category(filtered)
                reg_data = sales_by_region(filtered)

                with left:
                    st.markdown("#### Monthly Sales")

                    if month_data.empty:
                        show_empty(
                            "No valid dates available for the monthly trend."
                        )
                    else:
                        st.plotly_chart(
                            monthly_sales_chart(month_data),
                            use_container_width=True,
                        )

                with right:
                    st.markdown("#### Sales by Category")

                    if cat_data.empty:
                        show_empty("No category data available.")
                    else:
                        st.plotly_chart(
                            category_sales_chart(cat_data),
                            use_container_width=True,
                        )

                left2, right2 = st.columns(2)

                with left2:
                    st.markdown("#### Sales by Region")

                    if reg_data.empty:
                        show_empty("No region data available.")
                    else:
                        st.plotly_chart(
                            region_sales_chart(reg_data),
                            use_container_width=True,
                        )

                with right2:
                    st.markdown("#### Business Observations")

                    observations = business_observations(filtered)

                    if observations:
                        for observation in observations:
                            st.markdown(f"- {observation}")
                    else:
                        st.info(
                            "No business observations are available "
                            "for the selected data."
                        )

                    st.caption(
                        "Observations are generated from the current "
                        "filtered data."
                    )

                # -------------------------------
                # EXPORT FILTERED DATA
                # -------------------------------

                st.download_button(
                    "⬇ Download filtered data (CSV)",
                    data=filtered.to_csv(index=False).encode("utf-8"),
                    file_name="insight_ai_filtered.csv",
                    mime="text/csv",
                )

        except (ValueError, KeyError, TypeError) as exc:
            st.error(f"Unable to calculate sales analytics: {exc}")


# --------------------------------------------------
# DATA EXPLORER
# --------------------------------------------------

elif page == "Data Explorer":

    st.markdown("## Data Explorer")

    st.write(
        "Inspect the dataset structure and quality before analysis."
    )

    report = data_quality_report(raw_df)

    a, b, c = st.columns(3)

    a.metric("Rows", f'{report["rows"]:,}')
    b.metric("Columns", report["columns"])
    c.metric("Duplicate rows", report["duplicate_rows"])

    st.markdown("### Preview")

    st.dataframe(
        raw_df.head(100),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Column Summary")

    summary = pd.DataFrame(
        {
            "Column": raw_df.columns.astype(str),
            "Data type": [
                str(raw_df[col].dtype) for col in raw_df.columns
            ],
            "Missing values": [
                int(raw_df[col].isna().sum())
                for col in raw_df.columns
            ],
            "Missing %": [
                round(float(raw_df[col].isna().mean() * 100), 2)
                for col in raw_df.columns
            ],
        }
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "⬇ Download current data (CSV)",
        data=raw_df.to_csv(index=False).encode("utf-8"),
        file_name="insight_ai_data.csv",
        mime="text/csv",
    )


# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

elif page == "Data Cleaning":

    st.markdown("## Data Cleaning")

    st.write(
        "Review missing values and exact duplicate rows, "
        "then export a cleaned copy."
    )

    report = data_quality_report(raw_df)

    a, b = st.columns(2)

    a.metric(
        "Duplicate rows detected",
        report["duplicate_rows"],
    )

    b.metric(
        "Cells with missing values",
        int(raw_df.isna().sum().sum()),
    )

    missing_summary = pd.DataFrame(
        {
            "Column": raw_df.columns.astype(str),
            "Missing values": [
                int(raw_df[col].isna().sum())
                for col in raw_df.columns
            ],
        }
    )

    st.markdown("### Missing-Value Report")

    st.dataframe(
        missing_summary,
        use_container_width=True,
        hide_index=True,
    )

    drop_dupes = st.checkbox(
        "Remove exact duplicate rows",
        value=True,
    )

    drop_empty = st.checkbox(
        "Remove fully empty rows",
        value=True,
    )

    cleaned = clean_data(
        raw_df,
        drop_duplicates=drop_dupes,
        drop_fully_empty=drop_empty,
    )

    st.success(
        f"Cleaning preview: {len(raw_df):,} original rows "
        f"→ {len(cleaned):,} rows."
    )

    st.caption(
        "Partial missing values are reported, not automatically filled "
        "or removed, because the correct treatment depends on the dataset."
    )

    st.dataframe(
        cleaned.head(100),
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "⬇ Download cleaned data (CSV)",
        data=cleaned.to_csv(index=False).encode("utf-8"),
        file_name="insight_ai_cleaned.csv",
        mime="text/csv",
    )


# --------------------------------------------------
# ABOUT PROJECT
# --------------------------------------------------

else:

    st.markdown("## About Insight AI")

    st.write(
        "Insight AI is a beginner-friendly sales analytics project "
        "built to demonstrate data loading, data cleaning, "
        "business calculations and interactive visualization."
    )

    st.markdown("### Project Objectives")

    st.markdown(
        """
        - Summarize sales performance with clear KPIs.
        - Compare sales across months, product categories and regions.
        - Let users inspect data quality before analysis.
        - Provide downloadable filtered and cleaned datasets.
        - Demonstrate a modular Python application suitable for a college project.
        """
    )

    st.markdown("### Technologies")

    st.markdown(
        """
        - **Python** — application logic
        - **Streamlit** — interactive web interface
        - **Pandas** — CSV processing and data aggregation
        - **Plotly** — interactive charts
        - **CSV** — portable dataset format
        """
    )

    st.markdown("### Methodology")

    st.markdown(
        """
        1. Load the sample dataset or a user-uploaded CSV.
        2. Inspect column names and data quality.
        3. Validate sales columns and prepare dates and numbers.
        4. Apply user-selected filters.
        5. Calculate KPIs and grouped summaries.
        6. Display charts and data-driven observations.
        7. Allow users to download filtered or cleaned data.
        """
    )

    st.markdown("### Limitations")

    st.markdown(
        """
        - The included dataset is synthetic and does not represent a real company.
        - Sales analytics require the documented column names.
        - Missing values are reported rather than automatically guessed.
        - The current project does not include machine learning,
          forecasting, authentication or cloud storage.
        """
    )

    st.markdown("### Future Scope")

    st.markdown(
        """
        - Add column mapping for differently named CSV fields.
        - Support configurable currency and date formats.
        - Add product-level drill-down and PDF reports.
        - Integrate forecasting or machine learning in a future version.
        - Connect to a verified business database when needed.
        """
    )

    st.info(
        "Data processing runs locally on the machine where "
        "the Streamlit application is started."
    )
