import os

import pandas as pd
import plotly.express as px
import psycopg2
import streamlit as st
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh


load_dotenv()


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "helloq_realtime"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}


# ---------------------------------------------------------
# STREAMLIT PAGE
# ---------------------------------------------------------

st.set_page_config(
    page_title="HelloQ Real-Time Analytics",
    page_icon="⚡",
    layout="wide",
)


# Auto refresh every 2 seconds
st_autorefresh(
    interval=2000,
    key="realtime_refresh",
)


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

@st.cache_resource
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def query_database(query, params=None):
    connection = None

    try:
        connection = psycopg2.connect(**DB_CONFIG)

        dataframe = pd.read_sql_query(
            query,
            connection,
            params=params,
        )

        return dataframe

    except Exception as error:
        st.error(f"Database error: {error}")
        return pd.DataFrame()

    finally:
        if connection:
            connection.close()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("⚡ HelloQ Real-Time Analytics")

st.caption(
    "Live application activity → Kafka → Consumer → PostgreSQL → Streamlit"
)

st.divider()


# ---------------------------------------------------------
# KPI DATA
# ---------------------------------------------------------

total_users_query = """
SELECT COUNT(*) AS value
FROM users;
"""

active_users_query = """
SELECT COUNT(*) AS value
FROM user_realtime_status
WHERE current_status = 'active';
"""

live_events_query = """
SELECT COUNT(*) AS value
FROM processed_events
WHERE event_id >= 2001;
"""

matches_query = """
SELECT COUNT(*) AS value
FROM processed_events
WHERE event_type = 'match_created'
AND event_id >= 2001;
"""

chats_query = """
SELECT COUNT(*) AS value
FROM processed_events
WHERE event_type = 'chat_started'
AND event_id >= 2001;
"""

messages_query = """
SELECT COUNT(*) AS value
FROM processed_events
WHERE event_type = 'message_sent'
AND event_id >= 2001;
"""


total_users = query_database(total_users_query)
active_users = query_database(active_users_query)
live_events = query_database(live_events_query)
matches = query_database(matches_query)
chats = query_database(chats_query)
messages = query_database(messages_query)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Total Users",
    int(total_users.iloc[0]["value"])
    if not total_users.empty else 0,
)

c2.metric(
    "Active Users",
    int(active_users.iloc[0]["value"])
    if not active_users.empty else 0,
)

c3.metric(
    "Live Events",
    int(live_events.iloc[0]["value"])
    if not live_events.empty else 0,
)

c4.metric(
    "Live Matches",
    int(matches.iloc[0]["value"])
    if not matches.empty else 0,
)

c5.metric(
    "Live Chats",
    int(chats.iloc[0]["value"])
    if not chats.empty else 0,
)

c6.metric(
    "Live Messages",
    int(messages.iloc[0]["value"])
    if not messages.empty else 0,
)


st.divider()


# ---------------------------------------------------------
# CHART 1 — EVENT DISTRIBUTION
# ---------------------------------------------------------

event_distribution_query = """
SELECT
    event_type,
    COUNT(*) AS event_count
FROM processed_events
WHERE event_id >= 2001
GROUP BY event_type
ORDER BY event_count DESC;
"""

event_data = query_database(event_distribution_query)


left, right = st.columns(2)


with left:

    st.subheader("Live Event Distribution")

    if not event_data.empty:

        fig = px.bar(
            event_data,
            x="event_type",
            y="event_count",
            title="Live Events by Type",
        )

        fig.update_layout(
            xaxis_title="Event Type",
            yaxis_title="Events",
            height=400,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:
        st.info("No live events available yet.")


# ---------------------------------------------------------
# CHART 2 — CITY ACTIVITY
# ---------------------------------------------------------

city_activity_query = """
SELECT
    city,
    COUNT(*) AS event_count
FROM processed_events
WHERE event_id >= 2001
GROUP BY city
ORDER BY event_count DESC;
"""

city_data = query_database(city_activity_query)


with right:

    st.subheader("Activity by City")

    if not city_data.empty:

        fig_city = px.pie(
            city_data,
            names="city",
            values="event_count",
            title="Live Activity Distribution",
        )

        fig_city.update_layout(
            height=400,
        )

        st.plotly_chart(
            fig_city,
            use_container_width=True,
        )

    else:
        st.info("No city activity available yet.")


st.divider()


# ---------------------------------------------------------
# CHART 3 — EVENTS OVER TIME
# ---------------------------------------------------------

event_time_query = """
SELECT
    date_trunc(
        'minute',
        processed_at
    ) AS event_minute,
    COUNT(*) AS event_count
FROM processed_events
WHERE event_id >= 2001
GROUP BY event_minute
ORDER BY event_minute;
"""

time_data = query_database(event_time_query)


st.subheader("Live Event Rate")

if not time_data.empty:

    fig_time = px.line(
        time_data,
        x="event_minute",
        y="event_count",
        markers=True,
        title="Events Processed Over Time",
    )

    fig_time.update_layout(
        xaxis_title="Time",
        yaxis_title="Events",
        height=400,
    )

    st.plotly_chart(
        fig_time,
        use_container_width=True,
    )

else:

    st.info(
        "Waiting for live events..."
    )


# ---------------------------------------------------------
# LATEST EVENTS
# ---------------------------------------------------------

st.divider()

st.subheader("🔴 Latest Live Events")


latest_events_query = """
SELECT
    event_id,
    user_id,
    event_type,
    city,
    device,
    event_time,
    processed_at
FROM processed_events
WHERE event_id >= 2001
ORDER BY processed_at DESC
LIMIT 25;
"""

latest_events = query_database(
    latest_events_query
)


if not latest_events.empty:

    st.dataframe(
        latest_events,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No live events have reached PostgreSQL yet."
    )


# ---------------------------------------------------------
# REAL-TIME USER STATUS
# ---------------------------------------------------------

st.divider()

st.subheader("👤 User Real-Time Status")


status_query = """
SELECT
    user_id,
    current_status,
    total_events,
    profile_views,
    interests_sent,
    matches_created,
    chats_started,
    messages_sent,
    engagement_score,
    updated_at
FROM user_realtime_status
ORDER BY updated_at DESC
LIMIT 20;
"""

status_data = query_database(status_query)


if not status_data.empty:

    st.dataframe(
        status_data,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No real-time user status available."
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "HelloQ Real-Time Data Engineering Project | "
    "Python • Kafka • PostgreSQL • Streamlit"
)

st.caption(
    "Dashboard refresh interval: 2 seconds"
)
