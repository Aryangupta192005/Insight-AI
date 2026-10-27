"""Business metrics and aggregations for the SalesInsight dashboard."""
import pandas as pd
from data_manager import prepare_sales_data

def calculate_kpis(df: pd.DataFrame) -> dict:
    data = prepare_sales_data(df)
    sales = data["Sales"].sum(min_count=1)
    profit = data["Profit"].sum(min_count=1)
    order_count = data["Order ID"].nunique(dropna=True)
    average_order_value = data.groupby("Order ID", dropna=True)["Sales"].sum().mean()
    return {
        "total_sales": float(sales) if pd.notna(sales) else 0.0,
        "total_profit": float(profit) if pd.notna(profit) else 0.0,
        "number_of_orders": int(order_count),
        "average_order_value": float(average_order_value) if pd.notna(average_order_value) else 0.0,
    }

def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    data = prepare_sales_data(df)
    data = data.dropna(subset=["Order Date", "Sales"])
    if data.empty:
        return pd.DataFrame(columns=["Month", "Sales"])
    result = data.assign(Month=data["Order Date"].dt.to_period("M").dt.to_timestamp())
    return result.groupby("Month", as_index=False)["Sales"].sum().sort_values("Month")

def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    data = prepare_sales_data(df)
    data = data.dropna(subset=["Category", "Sales"])
    return data.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)

def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    data = prepare_sales_data(df)
    data = data.dropna(subset=["Region", "Sales"])
    return data.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)

def business_observations(df: pd.DataFrame) -> list[str]:
    data = prepare_sales_data(df)
    data = data.dropna(subset=["Sales", "Profit"])
    if data.empty:
        return ["No valid sales and profit values are available for observations."]
    notes = []
    cat = data.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    reg = data.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    notes.append(f"{cat.index[0]} is the highest-sales category (₹{cat.iloc[0]:,.2f}).")
    notes.append(f"{reg.index[0]} is the highest-sales region (₹{reg.iloc[0]:,.2f}).")
    total_sales = data["Sales"].sum()
    total_profit = data["Profit"].sum()
    margin = (total_profit / total_sales * 100) if total_sales else 0
    notes.append(f"Overall profit margin is {margin:.1f}% based on available sales and profit values.")
    if "Order Date" in data.columns:
        dated = data.dropna(subset=["Order Date"]).copy()
        dated["Order Date"] = pd.to_datetime(dated["Order Date"], errors="coerce")
        dated = dated.dropna(subset=["Order Date"])
        if not dated.empty:
            month_sales = dated.groupby(dated["Order Date"].dt.to_period("M"))["Sales"].sum().sort_values()
            notes.append(f"Lowest-sales month in the filtered data is {month_sales.index[0]} (₹{month_sales.iloc[0]:,.2f}).")
    return notes
