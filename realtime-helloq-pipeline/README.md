HelloQ Real-Time Data Pipeline ⚡

A real-time data engineering project that simulates a HelloQ-style application and processes user activity events using Python, Apache Kafka, PostgreSQL, and Streamlit.

Architecture

HelloQ App Simulator
        ↓
Python Event Generator
        ↓
Apache Kafka
        ↓
Kafka Consumer
        ↓
Validation & Processing
        ↓
PostgreSQL
        ↓
Streamlit Dashboard

Tech Stack

Python

Apache Kafka

PostgreSQL

Streamlit

Plotly

psycopg2

kafka-python

Features

Real-time user activity events

Kafka producer and consumer

Live event generation

PostgreSQL event storage

Duplicate event prevention

Real-time user metrics

Live analytics dashboard

Synthetic dataset of ~300 users and ~2,000 historical events

Event Types

registration_started
registration_completed
login
profile_view
interest_sent
interest_accepted
match_created
chat_started
message_sent
logout

Project Structure

realtime-helloq-pipeline/
│
├── src/
│   ├── producer.py
│   ├── consumer.py
│   ├── live_generator.py
│   └── live_consumer.py
│
├── dashboard.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

Run

Start Kafka first, then run:

python -m src.producer

python -m src.consumer

For live events:

python -m src.live_consumer

python -m src.live_generator

Start the dashboard:

python -m streamlit run dashboard.py

Database

PostgreSQL database:

helloq_realtime

Main tables:

users
user_events
matches
chats
processed_events
user_realtime_status

Version

Version 1 – Real-Time Kafka Pipeline ✅

Future Version 2 will explore Spark Structured Streaming and advanced real-time processing.
