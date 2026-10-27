import sys
from pathlib import Path
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analytics import calculate_kpis, monthly_sales, sales_by_category, business_observations
from data_manager import (
    REQUIRED_SALES_COLUMNS, clean_data, data_quality_report, generate_sample_data,
    prepare_sales_data, validate_sales_columns,
)

def tiny_data():
    return pd.DataFrame([
        {"Order ID":"A", "Order Date":"2024-01-10", "Region":"North", "Category":"Tech", "Product":"Mouse", "Quantity":2, "Unit Price":10, "Sales":20, "Profit":5},
        {"Order ID":"A", "Order Date":"2024-01-10", "Region":"North", "Category":"Tech", "Product":"Mouse", "Quantity":1, "Unit Price":10, "Sales":10, "Profit":2},
        {"Order ID":"B", "Order Date":"2024-02-10", "Region":"South", "Category":"Office", "Product":"Pen", "Quantity":5, "Unit Price":2, "Sales":10, "Profit":3},
    ])

def test_kpis_use_actual_values_and_unique_orders():
    result = calculate_kpis(tiny_data())
    assert result["total_sales"] == 40
    assert result["total_profit"] == 10
    assert result["number_of_orders"] == 2
    assert result["average_order_value"] == 20

def test_monthly_sales_aggregation():
    result = monthly_sales(tiny_data())
    assert len(result) == 2
    assert result.iloc[0]["Sales"] == 30
    assert result.iloc[1]["Sales"] == 10

def test_category_sales_sorted_descending():
    result = sales_by_category(tiny_data())
    assert result.iloc[0]["Category"] == "Tech"
    assert result.iloc[0]["Sales"] == 30

def test_missing_columns_are_reported():
    valid, missing = validate_sales_columns(pd.DataFrame({"Sales": [1]}))
    assert valid is False
    assert "Order ID" in missing

def test_prepare_sales_data_coerces_bad_dates_and_numbers():
    df = tiny_data()
    df.loc[0, "Order Date"] = "not-a-date"
    df.loc[0, "Sales"] = "unknown"
    result = prepare_sales_data(df)
    assert pd.isna(result.loc[0, "Order Date"])
    assert pd.isna(result.loc[0, "Sales"])

def test_quality_report_and_cleaning():
    df = pd.concat([tiny_data(), tiny_data().iloc[[0]]], ignore_index=True)
    report = data_quality_report(df)
    assert report["duplicate_rows"] == 1
    cleaned = clean_data(df)
    assert len(cleaned) == 3

def test_sample_data_is_reproducible_and_consistent():
    first = generate_sample_data(rows=220, seed=7)
    second = generate_sample_data(rows=220, seed=7)
    pd.testing.assert_frame_equal(first, second)
    assert len(first) == 220
    assert (first["Sales"].round(2) == (first["Quantity"] * first["Unit Price"]).round(2)).all()
    assert (first["Profit"] >= 0).all()

def test_observations_return_calculated_notes():
    notes = business_observations(tiny_data())
    assert len(notes) >= 3
    assert any("Tech" in note for note in notes)

def test_empty_dataframe_with_required_columns_is_safe():
    empty = pd.DataFrame(columns=REQUIRED_SALES_COLUMNS)
    result = calculate_kpis(empty)
    assert result["total_sales"] == 0
    assert result["number_of_orders"] == 0
