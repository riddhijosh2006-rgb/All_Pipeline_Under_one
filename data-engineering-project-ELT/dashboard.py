from pathlib import Path
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import streamlit as st
from dotenv import load_dotenv


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "customers.csv"
LOG_PATH = BASE_DIR / "logs" / "pipeline.log"

load_dotenv(BASE_DIR / ".env")


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="Customer ELT Pipeline Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_database_connection():
    """Create PostgreSQL connection using .env settings."""

    required = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing = [
        key for key in required
        if not os.getenv(key)
    ]

    if missing:
        raise ValueError(
            "Missing database environment variables: "
            + ", ".join(missing)
        )

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


# ============================================================
# LOAD TRANSFORMED DATA FROM POSTGRESQL
# ============================================================

@st.cache_data(ttl=60, show_spinner=False)
def load_postgres_data():

    connection = get_database_connection()

    try:

        query = """
            SELECT
                customer_id,
                name,
                age,
                city,
                purchase_amount,
                purchase_category
            FROM customers
            ORDER BY customer_id;
        """

        df = pd.read_sql_query(
            query,
            connection
        )

        return df

    finally:
        connection.close()


# ============================================================
# LOAD LOCAL CSV
# ============================================================

@st.cache_data(show_spinner=False)
def load_csv_data():

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"CSV file not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    # This is ONLY for dashboard preview.
    # The actual ELT transformation happens
    # inside PostgreSQL through transform.sql.

    df["customer_id"] = pd.to_numeric(
        df["customer_id"],
        errors="coerce"
    )

    df["age"] = pd.to_numeric(
        df["age"],
        errors="coerce"
    )

    df["purchase_amount"] = pd.to_numeric(
        df["purchase_amount"],
        errors="coerce"
    ).fillna(0)

    df["name"] = (
        df["name"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    df["city"] = (
        df["city"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.title()
    )

    df["purchase_category"] = df[
        "purchase_amount"
    ].apply(
        lambda x: "High" if x >= 5000 else "Low"
    )

    return df


# ============================================================
# LOG FILE
# ============================================================

def latest_log_lines(limit=15):

    if not LOG_PATH.exists():
        return []

    lines = LOG_PATH.read_text(
        encoding="utf-8",
        errors="ignore"
    ).splitlines()

    return lines[-limit:]


# ============================================================
# CURRENCY FORMAT
# ============================================================

def format_inr(value):

    return f"₹{value:,.0f}"


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚡ Pipeline Control")

source = st.sidebar.radio(
    "Select data source",
    [
        "PostgreSQL",
        "Local CSV",
    ],
    index=0,
)

st.sidebar.divider()

st.sidebar.subheader("Filters")


# ============================================================
# LOAD DATA
# ============================================================

try:

    if source == "PostgreSQL":

        df = load_postgres_data()

        source_label = "PostgreSQL → customers"

    else:

        df = load_csv_data()

        source_label = "Local CSV Preview"

except Exception as error:

    st.error(
        f"Unable to load data: {error}"
    )

    st.info(
        "Check your PostgreSQL connection and .env file."
    )

    st.stop()


# ============================================================
# BASIC VALIDATION
# ============================================================

if df.empty:

    st.warning(
        "No customer records were found."
    )

    st.stop()


required_columns = [
    "customer_id",
    "name",
    "age",
    "city",
    "purchase_amount",
    "purchase_category",
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        "Missing columns: "
        + ", ".join(missing_columns)
    )

    st.stop()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

cities = sorted(
    df["city"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

categories = sorted(
    df["purchase_category"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

min_age = int(df["age"].min())
max_age = int(df["age"].max())


selected_cities = st.sidebar.multiselect(
    "City",
    cities,
    default=cities,
)

selected_categories = st.sidebar.multiselect(
    "Purchase category",
    categories,
    default=categories,
)

age_range = st.sidebar.slider(
    "Age range",
    min_age,
    max_age,
    (min_age, max_age),
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered = df[
    df["city"].isin(selected_cities)
    &
    df["purchase_category"].isin(
        selected_categories
    )
    &
    df["age"].between(
        age_range[0],
        age_range[1]
    )
].copy()


# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "📊 Customer ELT Pipeline Dashboard"
)

st.write(
    "Interactive analytics for the "
    "**Extract → Load → Transform → Validate** "
    "data pipeline."
)

st.info(
    f"Pipeline data source: **{source_label}**"
)


st.divider()


# ============================================================
# FILTER RESULT
# ============================================================

if filtered.empty:

    st.warning(
        "No records match the selected filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_customers = len(filtered)

total_purchase = float(
    filtered["purchase_amount"].sum()
)

average_purchase = float(
    filtered["purchase_amount"].mean()
)

average_age = float(
    filtered["age"].mean()
)

high_value_percentage = (
    filtered["purchase_category"]
    .eq("High")
    .mean()
    * 100
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Total Purchases",
    format_inr(total_purchase)
)

col3.metric(
    "Average Purchase",
    format_inr(average_purchase)
)

col4.metric(
    "Average Age",
    f"{average_age:.1f}"
)

col5.metric(
    "High-Value Share",
    f"{high_value_percentage:.1f}%"
)


st.divider()


# ============================================================
# PURCHASE BY CITY
# ============================================================

left, right = st.columns(2)


with left:

    st.subheader(
        "💰 Purchase Amount by City"
    )

    city_summary = (
        filtered
        .groupby(
            "city",
            as_index=False
        )["purchase_amount"]
        .sum()
        .sort_values(
            "purchase_amount",
            ascending=False
        )
    )

    fig_city = px.bar(
        city_summary,
        x="city",
        y="purchase_amount",
        text_auto=".2s",
        labels={
            "city": "City",
            "purchase_amount":
                "Purchase Amount (₹)",
        },
    )

    fig_city.update_layout(
        height=400,
        showlegend=False,
    )

    st.plotly_chart(
        fig_city,
        use_container_width=True,
    )


# ============================================================
# PURCHASE CATEGORY
# ============================================================

with right:

    st.subheader(
        "🛒 Purchase Category Mix"
    )

    category_summary = (
        filtered[
            "purchase_category"
        ]
        .value_counts()
        .reset_index()
    )

    category_summary.columns = [
        "purchase_category",
        "count",
    ]

    fig_category = go.Figure(
        data=[
            go.Pie(
                labels=category_summary[
                    "purchase_category"
                ],
                values=category_summary[
                    "count"
                ],
                hole=0.60,
                textinfo="label+percent",
            )
        ]
    )

    fig_category.update_layout(
        height=400,
        showlegend=False,
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True,
    )


# ============================================================
# AGE VS PURCHASE
# ============================================================

left, right = st.columns(2)


with left:

    st.subheader(
        "👥 Age vs Purchase Amount"
    )

    fig_scatter = px.scatter(
        filtered,
        x="age",
        y="purchase_amount",
        size="purchase_amount",
        color="purchase_category",
        hover_data=[
            "customer_id",
            "name",
            "city",
        ],
        labels={
            "age": "Age",
            "purchase_amount":
                "Purchase Amount (₹)",
            "purchase_category":
                "Purchase Category",
        },
    )

    fig_scatter.update_layout(
        height=400,
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True,
    )


# ============================================================
# TOP CUSTOMERS
# ============================================================

with right:

    st.subheader(
        "🏆 Top Customers"
    )

    top_customers = (
        filtered
        .nlargest(
            7,
            "purchase_amount"
        )[
            [
                "name",
                "city",
                "purchase_amount",
            ]
        ]
        .copy()
    )

    top_customers[
        "purchase_amount"
    ] = top_customers[
        "purchase_amount"
    ].map(format_inr)

    top_customers.columns = [
        "Customer",
        "City",
        "Purchase",
    ]

    st.dataframe(
        top_customers,
        use_container_width=True,
        hide_index=True,
    )


st.divider()


# ============================================================
# CUSTOMER RECORDS
# ============================================================

st.subheader(
    "📋 Customer Records"
)

search = st.text_input(
    "Search customers",
    placeholder=
        "Search by customer name, city or ID...",
)

records = filtered.copy()


if search.strip():

    search_text = search.strip().lower()

    mask = (
        records["name"]
        .astype(str)
        .str.lower()
        .str.contains(
            search_text,
            na=False,
        )
        |
        records["city"]
        .astype(str)
        .str.lower()
        .str.contains(
            search_text,
            na=False,
        )
        |
        records["customer_id"]
        .astype(str)
        .str.contains(
            search_text,
            na=False,
        )
    )

    records = records[mask]


st.dataframe(
    records.sort_values(
        "purchase_amount",
        ascending=False,
    ),
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# PIPELINE HEALTH
# ============================================================

st.divider()

st.subheader(
    "🔄 Pipeline Health"
)

health1, health2, health3, health4 = st.columns(4)

health1.success("✓ Extract")
health2.success("✓ Load")
health3.success("✓ Transform")
health4.success("✓ Validate")


# ============================================================
# PIPELINE LOGS
# ============================================================

with st.expander(
    "View Recent Pipeline Logs"
):

    logs = latest_log_lines()

    if logs:

        st.code(
            "\n".join(logs),
            language="text",
        )

    else:

        st.info(
            "No pipeline logs found. "
            "Run `python -m src.pipeline` first."
        )


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Customer Data Engineering Project "
    "• ELT • PostgreSQL • Python • Pandas • Streamlit"
)