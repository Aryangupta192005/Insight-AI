"""CSV loading, validation, synthetic sample data, and data-quality helpers."""
from pathlib import Path
import numpy as np
import pandas as pd

REQUIRED_SALES_COLUMNS = [
    "Order ID", "Order Date", "Region", "Category", "Product",
    "Quantity", "Unit Price", "Sales", "Profit"
]
DATE_COLUMN = "Order Date"

def generate_sample_data(rows: int = 320, seed: int = 42) -> pd.DataFrame:
    """Return reproducible synthetic order-line data with internally consistent totals."""
    rng = np.random.default_rng(seed)
    start = pd.Timestamp("2024-01-01")
    end = pd.Timestamp("2025-12-31")
    days = (end - start).days + 1
    categories = {
        "Technology": [("Laptop", 780), ("Monitor", 210), ("Keyboard", 45), ("Headphones", 85)],
        "Furniture": [("Office Chair", 160), ("Desk", 320), ("Bookshelf", 125), ("Lamp", 35)],
        "Office Supplies": [("Notebook", 6), ("Printer Paper", 9), ("Pen Set", 12), ("Stapler", 18)],
    }
    regions = np.array(["North", "South", "East", "West", "Central"])
    rows_out = []
    for i in range(1, rows + 1):
        category = str(rng.choice(list(categories.keys()), p=[0.36, 0.29, 0.35]))
        product, base_price = categories[category][int(rng.integers(0, len(categories[category])))]
        quantity = int(rng.integers(1, 9))
        unit_price = round(max(1, base_price * float(rng.normal(1, 0.07))), 2)
        sales = round(quantity * unit_price, 2)
        margin = float(rng.uniform(0.08, 0.32))
        profit = round(sales * margin, 2)
        order_date = start + pd.Timedelta(days=int(rng.integers(0, days)))
        rows_out.append({
            "Order ID": f"ORD-{i:04d}",
            "Order Date": order_date.strftime("%Y-%m-%d"),
            "Region": str(rng.choice(regions)),
            "Category": category,
            "Product": product,
            "Quantity": quantity,
            "Unit Price": unit_price,
            "Sales": sales,
            "Profit": profit,
        })
    return pd.DataFrame(rows_out, columns=REQUIRED_SALES_COLUMNS)

def load_csv(source) -> pd.DataFrame:
    """Load CSV from a path or file-like object; raise a readable ValueError on failure."""
    try:
        df = pd.read_csv(source)
    except (pd.errors.ParserError, UnicodeDecodeError, OSError, ValueError) as exc:
        raise ValueError(f"Could not read this CSV file: {exc}") from exc
    if df.empty and len(df.columns) == 0:
        raise ValueError("The CSV file is empty or has no readable header.")
    return df

def validate_sales_columns(df: pd.DataFrame) -> tuple[bool, list[str]]:
    missing = [col for col in REQUIRED_SALES_COLUMNS if col not in df.columns]
    return not missing, missing

def prepare_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize dates and numeric columns without hiding invalid values."""
    valid, missing = validate_sales_columns(df)
    if not valid:
        raise ValueError("Missing required sales columns: " + ", ".join(missing))
    result = df.copy()
    result[DATE_COLUMN] = pd.to_datetime(result[DATE_COLUMN], errors="coerce")
    for col in ["Quantity", "Unit Price", "Sales", "Profit"]:
        result[col] = pd.to_numeric(result[col], errors="coerce")
    return result

def data_quality_report(df: pd.DataFrame) -> dict:
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_by_column": df.isna().sum().astype(int).to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
    }

def clean_data(df: pd.DataFrame, drop_duplicates: bool = True, drop_fully_empty: bool = True) -> pd.DataFrame:
    """Basic, transparent cleaning: optionally remove exact duplicates and fully empty rows."""
    result = df.copy()
    if drop_fully_empty:
        result = result.dropna(how="all")
    if drop_duplicates:
        result = result.drop_duplicates()
    return result.reset_index(drop=True)
