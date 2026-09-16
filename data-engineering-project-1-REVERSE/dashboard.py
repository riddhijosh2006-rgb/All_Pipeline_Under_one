from pathlib import Path
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import streamlit as st
from dotenv import load_dotenv


# ============================================================
# PATHS & ENVIRONMENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "customers.csv"
LOG_PATH = BASE_DIR / "logs" / "pipeline.log"

load_dotenv(BASE_DIR / ".env")


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Customer Pipeline Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

CUSTOM_CSS = """
<style>
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(124,58,237,.16), transparent 28%),
            radial-gradient(circle at 90% 0%, rgba(14,165,233,.13), transparent 24%),
            #0B1020;
    }

    [data-testid="stSidebar"] {
        background: rgba(13, 20, 37, .94);
        border-right: 1px solid rgba(148,163,184,.14);
    }

    .hero {
        padding: 1.45rem 1.6rem;
        border: 1px solid rgba(148,163,184,.16);
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            rgba(124,58,237,.22),
            rgba(14,165,233,.10)
        );
        box-shadow: 0 18px 45px rgba(0,0,0,.18);
        margin-bottom: 1rem;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.05rem;
        letter-spacing: -.02em;
    }

    .hero p {
        color: #CBD5E1;
        margin: .45rem 0 0;
    }

    div[data-testid="stMetric"] {
        background: rgba(18,26,47,.88);
        border: 1px solid rgba(148,163,184,.14);
        padding: .95rem 1rem;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,.13);
    }

    div[data-testid="stMetric"] label {
        color: #A7B3C7 !important;
    }

    .status-card {
        padding: .8rem 1rem;
        border-radius: 14px;
        background: rgba(16,185,129,.10);
        border: 1px solid rgba(16,185,129,.28);
        color: #D1FAE5;
    }

    .muted-card {
        padding: .8rem 1rem;
        border-radius: 14px;
        background: rgba(148,163,184,.08);
        border: 1px solid rgba(148,163,184,.14);
        color: #CBD5E1;
    }

    .block-container {
        padding-top: 1.7rem;
        padding-bottom: 2rem;
    }

    h2, h3 {
        letter-spacing: -.01em;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ============================================================
# LOCAL CSV TRANSFORMATION
# ============================================================

def transform_data(raw: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare local CSV data for dashboard display.

    This function is only for the dashboard's Local CSV mode.
    PostgreSQL transformation continues to use src.transform_sql.
    """

    df = raw.copy()

    # Standardize column names
    df.columns = [str(col).strip().lower() for col in df.columns]

    # Required columns
    required_columns = [
        "customer_id",
        "name",
        "age",
        "city",
        "purchase_amount",
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    # Convert numeric columns
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
    )

    # Fill missing age values with median
    if df["age"].isna().any():
        median_age = df["age"].median()

        if pd.notna(median_age):
            df["age"] = df["age"].fillna(median_age)

    # Fill missing purchase amount
    df["purchase_amount"] = df["purchase_amount"].fillna(0)

    # Clean text fields
    df["name"] = df["name"].fillna("Unknown").astype(str)
    df["city"] = df["city"].fillna("Unknown").astype(str)

    # Create purchase category
    df["purchase_category"] = df["purchase_amount"].apply(
        lambda amount: "High" if amount >= 5000 else "Low"
    )

    return df


# ============================================================
# LOAD CSV DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_csv_data() -> pd.DataFrame:

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"CSV file not found: {DATA_PATH}"
        )

    raw = pd.read_csv(DATA_PATH)

    clean = transform_data(raw)

    if clean is None or clean.empty:
        raise ValueError(
            "Transformation failed or CSV contains no data."
        )

    return clean


# ============================================================
# LOAD POSTGRESQL DATA
# ============================================================

@st.cache_data(show_spinner=False, ttl=60)
def load_postgres_data() -> pd.DataFrame:

    required = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing = [
        key
        for key in required
        if not os.getenv(key)
    ]

    if missing:
        raise ValueError(
            "Missing database environment variables: "
            + ", ".join(missing)
        )

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    try:
        return pd.read_sql_query(
            """
            SELECT *
            FROM customers
            ORDER BY customer_id
            """,
            connection,
        )

    finally:
        connection.close()


# ============================================================
# FORMAT CURRENCY
# ============================================================

def inr(value: float) -> str:
    return f"₹{value:,.0f}"


# ============================================================
# READ PIPELINE LOGS
# ============================================================

def latest_log_lines(limit: int = 12) -> list[str]:

    if not LOG_PATH.exists():
        return []

    lines = LOG_PATH.read_text(
        encoding="utf-8",
        errors="ignore"
    ).splitlines()

    return lines[-limit:]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚡ Pipeline Control")

    source = st.radio(
        "Data source",
        ["Local CSV", "PostgreSQL"],
        index=0,
    )

    st.caption(
        "PostgreSQL uses credentials from your local `.env` file."
    )

    st.divider()

    st.markdown("### Filters")


# ============================================================
# LOAD SELECTED DATA SOURCE
# ============================================================

try:

    if source == "PostgreSQL":

        df = load_postgres_data()
        source_label = "PostgreSQL"

    else:

        df = load_csv_data()
        source_label = "CSV → Transform"

except Exception as exc:

    st.error(
        f"Could not load {source}: {exc}"
    )

    st.info(
        "Switch the sidebar data source to Local CSV "
        "to preview the dashboard without PostgreSQL."
    )

    st.stop()


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if df.empty:

    st.warning(
        "No customer records are available."
    )

    st.stop()


# ============================================================
# FILTER OPTIONS
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


with st.sidebar:

    selected_cities = st.multiselect(
        "City",
        cities,
        default=cities,
    )

    selected_categories = st.multiselect(
        "Purchase category",
        categories,
        default=categories,
    )

    age_range = st.slider(
        "Age range",
        min_age,
        max_age,
        (min_age, max_age),
    )

    st.divider()

    st.caption(
        "Customer Data Engineering Pipeline"
    )

    st.caption(
        "Python • Pandas • PostgreSQL • Streamlit"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered = df[
    df["city"].isin(selected_cities)
    & df["purchase_category"].isin(selected_categories)
    & df["age"].between(
        age_range[0],
        age_range[1]
    )
].copy()


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>Customer Data Pipeline Dashboard</h1>
        <p>
            Interactive analytics for the
            Extract → Transform → Validate → Load workflow.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# STATUS
# ============================================================

status_left, status_right = st.columns([1.35, 1])

with status_left:

    st.markdown(
        f"""
        <div class="status-card">
            ● Pipeline data available
            &nbsp; • &nbsp;
            Source: <b>{source_label}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )


with status_right:

    st.markdown(
        f"""
        <div class="muted-card">
            Showing <b>{len(filtered)}</b>
            of <b>{len(df)}</b>
            customer records
        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")


# ============================================================
# FILTERED DATA CHECK
# ============================================================

if filtered.empty:

    st.warning(
        "No records match the selected filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

revenue = float(
    filtered["purchase_amount"].sum()
)

avg_purchase = float(
    filtered["purchase_amount"].mean()
)

avg_age = float(
    filtered["age"].mean()
)

high_value_share = float(
    (
        filtered["purchase_category"] == "High"
    ).mean()
    * 100
)


# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "Customers",
    f"{len(filtered):,}"
)

k2.metric(
    "Total Purchases",
    inr(revenue)
)

k3.metric(
    "Avg. Purchase",
    inr(avg_purchase)
)

k4.metric(
    "Avg. Age",
    f"{avg_age:.1f}"
)

k5.metric(
    "High-Value Share",
    f"{high_value_share:.1f}%"
)


st.write("")


# ============================================================
# CITY + CATEGORY CHARTS
# ============================================================

left, right = st.columns([1.35, 1])


with left:

    st.subheader(
        "Purchase Amount by City"
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
            "purchase_amount": "Purchase Amount (₹)",
        },
    )

    fig_city.update_layout(
        height=390,
        margin=dict(
            l=10,
            r=10,
            t=15,
            b=10,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )

    st.plotly_chart(
        fig_city,
        use_container_width=True,
    )


with right:

    st.subheader(
        "Purchase Category Mix"
    )

    category_summary = (
        filtered["purchase_category"]
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
                hole=.65,
                textinfo="label+percent",
            )
        ]
    )

    fig_category.update_layout(
        height=390,
        margin=dict(
            l=10,
            r=10,
            t=15,
            b=10,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        annotations=[
            dict(
                text=f"{len(filtered)}<br>Customers",
                x=.5,
                y=.5,
                showarrow=False,
                font_size=17,
            )
        ],
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True,
    )


# ============================================================
# AGE VS PURCHASE + TOP CUSTOMERS
# ============================================================

left2, right2 = st.columns([1, 1])


with left2:

    st.subheader(
        "Age vs Purchase Amount"
    )

    fig_scatter = px.scatter(
        filtered,
        x="age",
        y="purchase_amount",
        size="purchase_amount",
        color="purchase_category",
        hover_data=[
            "name",
            "city",
            "customer_id",
        ],
        labels={
            "age": "Age",
            "purchase_amount": "Purchase Amount (₹)",
            "purchase_category": "Category",
        },
    )

    fig_scatter.update_layout(
        height=385,
        margin=dict(
            l=10,
            r=10,
            t=15,
            b=10,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True,
    )


with right2:

    st.subheader(
        "Top Customers"
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
    ].map(inr)

    top_customers.columns = [
        "Customer",
        "City",
        "Purchase",
    ]

    st.dataframe(
        top_customers,
        use_container_width=True,
        hide_index=True,
        height=330,
    )


# ============================================================
# CUSTOMER RECORDS
# ============================================================

st.subheader(
    "Customer Records"
)

search = st.text_input(
    "Search customers",
    placeholder="Search by customer name, city, or ID...",
)

records = filtered.copy()


if search.strip():

    query = search.strip().lower()

    mask = (
        records["name"]
        .astype(str)
        .str.lower()
        .str.contains(query)
        |
        records["city"]
        .astype(str)
        .str.lower()
        .str.contains(query)
        |
        records["customer_id"]
        .astype(str)
        .str.contains(query)
    )

    records = records[mask]


st.dataframe(
    records.sort_values(
        "purchase_amount",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True,
    column_config={
        "customer_id": "Customer ID",
        "name": "Name",
        "age": st.column_config.NumberColumn(
            "Age",
            format="%d"
        ),
        "city": "City",
        "purchase_amount": st.column_config.NumberColumn(
            "Purchase Amount",
            format="₹ %.0f"
        ),
        "purchase_category": "Category",
    },
)


# ============================================================
# PIPELINE HEALTH
# ============================================================

with st.expander(
    "Pipeline Health & Recent Logs"
):

    c1, c2, c3, c4 = st.columns(4)

    c1.success("✓ Extract")
    c2.success("✓ Transform")
    c3.success("✓ Validate")
    c4.success("✓ Load / Ready")

    lines = latest_log_lines()

    if lines:

        st.code(
            "\n".join(lines),
            language="text"
        )

    else:

        st.caption(
            "No pipeline log entries found yet. "
            "Run `python -m src.pipeline` "
            "to generate logs."
        )


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Built for a Data Engineering portfolio • "
    "ETL • Data Quality • PostgreSQL • Analytics"
)