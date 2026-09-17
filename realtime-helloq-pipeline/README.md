# ⚡ HelloQ Real-Time Data Engineering Pipeline

A local **real-time event-driven data pipeline** that simulates a HelloQ-style matrimony application and processes user activity through **Apache Kafka, Python, PostgreSQL, and Streamlit**.

The project demonstrates how application events can be generated continuously, streamed through Kafka, consumed and validated by Python, stored in PostgreSQL, transformed into real-time user metrics, and visualized through a live analytics dashboard.

---

## 🚀 Project Overview

This project simulates application activity such as:

- User login
- Profile views
- Interest sent
- Interest accepted
- Match creation
- Chat started
- Messages sent
- Logout
- Registration activity

The system contains approximately **300 users** and an initial dataset of around **2,000 historical events**.

After the historical data is established, the project generates new events continuously to simulate live application activity.

---

## 🏗️ Architecture

```text
                   HELLOQ-LIKE APPLICATION
                            │
                            ▼
                  Python Event Generator
                            │
                            ▼
                         Apache Kafka
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
          helloq-events       helloq-live-events
                 │                     │
                 └──────────┬──────────┘
                            │
                            ▼
                    Python Kafka Consumer
                            │
                Validation + Idempotency
                            │
                            ▼
                     PostgreSQL
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
        processed_events       user_realtime_status
                │                       │
                └───────────┬───────────┘
                            │
                            ▼
                    Streamlit Dashboard
                            │
                            ▼
                  Real-Time Analytics
