import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

from config.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Weather Analytics Dashboard",
    page_icon="🌤️",
    layout="wide"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_resource
def create_connection():

    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


# ============================================================
# LOAD WEATHER DATA
# ============================================================

@st.cache_data(ttl=60)
def load_weather_data():

    connection = create_connection()

    query = """
        SELECT
            id,
            timestamp,
            temperature_c,
            humidity_pct,
            wind_speed_kmh,
            city
        FROM weather_data
        ORDER BY timestamp;
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    return df


# ============================================================
# DASHBOARD TITLE
# ============================================================

st.title("🌤️ Weather Analytics Dashboard")

st.markdown(
    "### Real-Time Weather Data Pipeline"
)

st.divider()


# ============================================================
# LOAD DATA
# ============================================================

try:

    df = load_weather_data()

except Exception as e:

    st.error(
        f"Unable to connect to PostgreSQL: {e}"
    )

    st.stop()


# ============================================================
# CHECK DATA
# ============================================================

if df.empty:

    st.warning(
        "No weather data available in PostgreSQL."
    )

    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)

latest_record = df.iloc[-1]

latest_temperature = latest_record[
    "temperature_c"
]

latest_humidity = latest_record[
    "humidity_pct"
]

latest_wind = latest_record[
    "wind_speed_kmh"
]

city = latest_record["city"]


average_temperature = df[
    "temperature_c"
].mean()

maximum_temperature = df[
    "temperature_c"
].max()

minimum_temperature = df[
    "temperature_c"
].min()

average_humidity = df[
    "humidity_pct"
].mean()

average_wind = df[
    "wind_speed_kmh"
].mean()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Dashboard Controls")

selected_city = st.sidebar.selectbox(
    "Select City",
    sorted(df["city"].unique())
)

filtered_df = df[
    df["city"] == selected_city
]

if st.sidebar.button("🔄 Refresh Data"):

    st.cache_data.clear()

    st.rerun()


# ============================================================
# HEADER INFORMATION
# ============================================================

st.subheader(
    f"📍 {selected_city}"
)

st.caption(
    f"Latest available data: "
    f"{latest_record['timestamp']}"
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🌡️ Current Temperature",
        f"{latest_temperature:.1f} °C"
    )


with col2:

    st.metric(
        "💧 Current Humidity",
        f"{latest_humidity:.0f} %"
    )


with col3:

    st.metric(
        "💨 Current Wind",
        f"{latest_wind:.1f} km/h"
    )


with col4:

    st.metric(
        "📊 Total Records",
        len(filtered_df)
    )


st.divider()


# ============================================================
# SUMMARY METRICS
# ============================================================

st.subheader("📊 Weather Summary")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Average Temperature",
        f"{filtered_df['temperature_c'].mean():.1f} °C"
    )


with col2:

    st.metric(
        "Maximum Temperature",
        f"{filtered_df['temperature_c'].max():.1f} °C"
    )


with col3:

    st.metric(
        "Minimum Temperature",
        f"{filtered_df['temperature_c'].min():.1f} °C"
    )


with col4:

    st.metric(
        "Average Humidity",
        f"{filtered_df['humidity_pct'].mean():.1f} %"
    )


st.divider()


# ============================================================
# TEMPERATURE TREND
# ============================================================

st.subheader("🌡️ Temperature Trend")

fig_temperature = px.line(
    filtered_df,
    x="timestamp",
    y="temperature_c",
    markers=True,
    title="Temperature Over Time"
)

fig_temperature.update_layout(
    xaxis_title="Time",
    yaxis_title="Temperature (°C)"
)

st.plotly_chart(
    fig_temperature,
    use_container_width=True
)


# ============================================================
# HUMIDITY TREND
# ============================================================

st.subheader("💧 Humidity Trend")

fig_humidity = px.line(
    filtered_df,
    x="timestamp",
    y="humidity_pct",
    markers=True,
    title="Humidity Over Time"
)

fig_humidity.update_layout(
    xaxis_title="Time",
    yaxis_title="Humidity (%)"
)

st.plotly_chart(
    fig_humidity,
    use_container_width=True
)


# ============================================================
# WIND SPEED
# ============================================================

st.subheader("💨 Wind Speed")

fig_wind = px.line(
    filtered_df,
    x="timestamp",
    y="wind_speed_kmh",
    markers=True,
    title="Wind Speed Over Time"
)

fig_wind.update_layout(
    xaxis_title="Time",
    yaxis_title="Wind Speed (km/h)"
)

st.plotly_chart(
    fig_wind,
    use_container_width=True
)


# ============================================================
# COMBINED WEATHER DATA
# ============================================================

st.subheader("📈 Combined Weather Analysis")

fig_combined = px.line(
    filtered_df,
    x="timestamp",
    y=[
        "temperature_c",
        "humidity_pct",
        "wind_speed_kmh"
    ],
    title="Temperature, Humidity and Wind"
)

st.plotly_chart(
    fig_combined,
    use_container_width=True
)


# ============================================================
# WEATHER DATA TABLE
# ============================================================

st.subheader("📋 Weather Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Data Source: Open-Meteo API → "
    "Python ETL Pipeline → PostgreSQL → Streamlit"
)