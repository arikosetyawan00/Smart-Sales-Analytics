"""
Data loading utilities for the Smart Sales Analytics dashboard.

The dashboard is built to answer specific business questions (sales trend,
profitability, customer value, product performance, and regional
performance). To let users filter interactively (by Year, Region, Segment,
Category, etc.) and have EVERY chart/KPI respond to those filters, the app
loads the transaction-level cleaned dataset (`Superstore_Clean.csv`) and
aggregates it on the fly with pandas, instead of only reading pre-aggregated
CSVs that can't be filtered.

The pre-aggregated CSVs in `processed/` (produced by
`notebooks/02_Dashboard_Data.ipynb`) are still used for the default,
unfiltered KPI/reference values shown in the sidebar footer.
"""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "processed"
RAW_DATA_PATH = BASE_DIR / "data" / "final" / "Superstore_Clean.csv"
FILTERS_PATH = DATA_DIR / "dashboard_filters.json"


@st.cache_data(show_spinner="Loading Superstore dataset...")
def load_raw_data() -> pd.DataFrame:
    """Load the cleaned, transaction-level Superstore dataset.

    This is the single source of truth for the dashboard. All KPIs and
    charts are derived from this dataframe after filters are applied, which
    keeps the numbers consistent across every tab.
    """

    df = pd.read_csv(RAW_DATA_PATH)

    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    # Guard rails in case the file is reused without the pre-computed
    # date-part columns from the EDA notebook.
    if "Year" not in df.columns:
        df["Year"] = df["Order Date"].dt.year
    if "Month" not in df.columns:
        df["Month"] = df["Order Date"].dt.month
    if "Month Name" not in df.columns:
        df["Month Name"] = df["Order Date"].dt.month_name()
    if "Quarter" not in df.columns:
        df["Quarter"] = df["Order Date"].dt.quarter

    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

    return df


@st.cache_data
def load_filters() -> dict:
    """Load the dropdown/multiselect options used by the sidebar filters."""

    with open(FILTERS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_dashboard():
    """Load the static, pre-aggregated reference tables from `processed/`.

    Kept for backward compatibility / quick reference values (e.g. the
    all-time KPI numbers computed in the notebooks), separate from the
    live, filterable numbers computed from `load_raw_data()`.
    """

    dashboard_kpi = pd.read_csv(DATA_DIR / "dashboard_kpi.csv")
    sales_trend = pd.read_csv(DATA_DIR / "sales_trend.csv")
    category = pd.read_csv(DATA_DIR / "category_performance.csv")
    customer = pd.read_csv(DATA_DIR / "customer_performance.csv")
    product = pd.read_csv(DATA_DIR / "product_performance.csv")
    region = pd.read_csv(DATA_DIR / "region_performance.csv")

    return (
        dashboard_kpi,
        sales_trend,
        category,
        customer,
        product,
        region,
    )


def apply_filters(
    df: pd.DataFrame,
    years=None,
    regions=None,
    segments=None,
    categories=None,
) -> pd.DataFrame:
    """Return a filtered copy of `df` based on the selected sidebar values.

    Any filter left empty (or covering every available option) is treated
    as "no filter" so the dashboard shows the full dataset by default.
    """

    filtered = df.copy()

    if years:
        filtered = filtered[filtered["Year"].isin(years)]
    if regions:
        filtered = filtered[filtered["Region"].isin(regions)]
    if segments:
        filtered = filtered[filtered["Segment"].isin(segments)]
    if categories:
        filtered = filtered[filtered["Category"].isin(categories)]

    return filtered


def compute_kpis(df: pd.DataFrame) -> dict:
    """Compute the headline KPIs for whatever slice of data is passed in."""

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order ID"].nunique()
    total_customers = df["Customer ID"].nunique()

    avg_order_value = total_sales / total_orders if total_orders else 0
    profit_margin = (total_profit / total_sales * 100) if total_sales else 0

    return {
        "Total Sales": total_sales,
        "Total Profit": total_profit,
        "Total Orders": total_orders,
        "Total Customers": total_customers,
        "Average Order Value": avg_order_value,
        "Profit Margin (%)": profit_margin,
    }
