# 🚀 All Pipeline Under One

A practical **Data Engineering portfolio** containing end-to-end data pipelines built with Python, SQL, PostgreSQL, APIs, cloud technologies, data validation, logging, processing, and dashboards.

This repository demonstrates different data engineering architectures — from traditional **ETL and ELT pipelines** to API-based pipelines, reverse pipelines, cloud workflows, and real-time data systems.

---

## 📌 Repository Overview

| Project | Pipeline | Main Technologies | Status |
|---|---|---|---|
| **Project 1 — ELT Pipeline** | CSV → PostgreSQL → SQL Transform → Dashboard | Python, Pandas, PostgreSQL, SQL, Streamlit | ✅ Completed |
| **Project 2 — API Data Pipeline** | API → Python → PostgreSQL → Dashboard | Python, REST API, PostgreSQL, Streamlit | ✅ Completed |
| **Project 3 — ETL Pipeline** | Source → Extract → Transform → Load → Database | Python, Pandas, PostgreSQL, SQL | 🔜 Uploading |
| **Project 4 — Reverse Data Pipeline** | Database → Transform → Export / API / Destination | Python, SQL, PostgreSQL | 🔜 Planned |
| **Project 5 — AWS Data Pipeline** | Data → S3 → Processing → Warehouse → BI | AWS, S3, Python, SQL, Power BI | 🔜 Planned |
| **Project 6 — Real-Time Data Pipeline** | Application → API → Kafka → Processing → Database → Dashboard | AWS, Kafka, Python, PostgreSQL | 🔜 Planned |

---

# 📂 Repository Structure

```text
All_Pipeline_Under_one/
│
├── 📁 data-engineering-project-ELT/
├── 📁 api_data_pipeline/
├── 📁 data-engineering-project-ETL/
├── 📁 reverse-data-pipeline/
├── 📁 aws-data-pipeline/
├── 📁 real-time-data-pipeline/
└── README.md
```

> Projects marked as planned will be added as development progresses.

---

# 🏗️ Project 1 — ELT Data Pipeline

## Architecture

```text
CSV Dataset
     ↓
Extract
     ↓
Load Raw Data
     ↓
PostgreSQL
     ↓
SQL Transformation
     ↓
Customers Table
     ↓
Data Validation
     ↓
Streamlit Dashboard
```

### 🔧 Technologies

- Python
- Pandas
- PostgreSQL
- SQL
- psycopg2
- Streamlit
- Plotly
- python-dotenv

### ✨ Features

- CSV data extraction
- Raw data loading into PostgreSQL
- SQL-based transformations
- Data validation
- Duplicate detection
- Data quality checks
- Pipeline logging
- SQL analytics
- Interactive dashboard
- Environment-variable-based database configuration

### 🔄 ELT Approach

```text
Extract → Load → Transform → Validate → Analyze
```

Raw data is first loaded into PostgreSQL, and transformation is performed inside PostgreSQL using SQL.

👉 **Project:** `data-engineering-project-ELT`

---

# 🌐 Project 2 — API Data Pipeline

## Architecture

```text
External API
     ↓
Python Extraction
     ↓
Data Transformation
     ↓
Data Validation
     ↓
PostgreSQL
     ↓
SQL Analytics
     ↓
Streamlit Dashboard
```

### 🔧 Technologies

- Python
- REST API
- Pandas
- PostgreSQL
- SQL
- Streamlit
- Plotly
- Logging
- Data Validation

### ✨ Features

- API data extraction
- Multiple-city support
- Data transformation
- PostgreSQL storage
- Duplicate prevention
- Error handling
- Pipeline logging
- Data-quality validation
- SQL analytics
- Interactive dashboard
- Environment-based configuration

### 📊 Status

The API pipeline is **completed** and demonstrates an end-to-end API-to-database data engineering workflow with an interactive dashboard.

👉 **Project:** `api_data_pipeline`

---

# 🔄 Project 3 — ETL Data Pipeline

This project demonstrates the traditional **ETL (Extract, Transform, Load)** architecture.

## Architecture

```text
Source Dataset
      ↓
Extract
      ↓
Python / Pandas Transformation
      ↓
Data Validation
      ↓
PostgreSQL
      ↓
Analytics / Dashboard
```

### 🔧 Technologies

- Python
- Pandas
- PostgreSQL
- SQL
- Data Validation
- Logging
- Dashboard / Visualization

### 🎯 Purpose

The ETL project is included to compare traditional ETL with the ELT architecture used in Project 1.

### ETL

```text
Extract → Transform → Load
```

### ELT

```text
Extract → Load → Transform
```

The project will demonstrate where transformation takes place and how ETL and ELT differ in an end-to-end data workflow.

👉 **Project:** `data-engineering-project-ETL`

---

# 🔁 Project 4 — Reverse Data Pipeline

A reverse data pipeline moves processed or stored data **from a database or analytical system toward a downstream destination**.

## Planned Architecture

```text
PostgreSQL / Data Warehouse
          ↓
        Extract
          ↓
       Transform
          ↓
   Export / API / Connector
          ↓
   External Destination
```

Possible destinations include:

- CSV / files
- REST API
- External application
- Another database
- Cloud storage

### 🎯 Purpose

This project will demonstrate the reverse direction of conventional data ingestion and show how processed data can be prepared and delivered to downstream systems.

👉 **Project:** `reverse-data-pipeline`

---

# ☁️ Project 5 — AWS Data Pipeline

## Planned Architecture

```text
Data Source
     ↓
Amazon S3
     ↓
Python / AWS Processing
     ↓
Database / Data Warehouse
     ↓
SQL Analytics
     ↓
Power BI
```

### Planned Technologies

- AWS S3
- AWS Glue
- Python
- PostgreSQL / Amazon Redshift
- SQL
- Power BI

The objective is to demonstrate a cloud-based data pipeline using AWS services.

---

# ⚡ Project 6 — Real-Time Data Engineering Pipeline

This project will simulate a pipeline for data generated continuously by a real application.

## Planned Architecture

```text
Real Application
      ↓
API / Event Producer
      ↓
Apache Kafka
      ↓
Stream Processing
      ↓
Database / Data Warehouse
      ↓
Analytics
      ↓
Dashboard
```

### Planned Technologies

- Python
- REST APIs
- AWS
- Amazon S3
- Apache Kafka
- Stream Processing
- PostgreSQL
- SQL
- Streamlit / Power BI

The goal is to demonstrate how application-generated data can be collected, transported, processed, stored, and visualized in a scalable real-time architecture.

---

# 🧰 Technologies & Tools

### Programming
- Python
- SQL

### Data Processing
- Pandas
- NumPy

### Databases
- PostgreSQL
- SQL

### Data Engineering
- ETL
- ELT
- Reverse Pipelines
- Data Validation
- Data Quality
- Logging
- API Pipelines
- Batch Processing
- Streaming

### Cloud
- AWS S3
- AWS Glue
- Amazon Redshift

### Streaming
- Apache Kafka

### Visualization
- Streamlit
- Plotly
- Power BI

### Development
- Git
- GitHub
- VS Code
- Docker

---

# 📈 Learning Progression

```text
Python
   ↓
SQL
   ↓
PostgreSQL
   ↓
ETL
   ↓
ELT
   ↓
API Pipelines
   ↓
Data Validation
   ↓
Logging
   ↓
Dashboards
   ↓
Reverse Pipelines
   ↓
AWS
   ↓
Kafka
   ↓
Real-Time Data Engineering
```

---

# 🎯 Portfolio Goals

This repository focuses on **learning by building practical projects** rather than only studying theory.

The main goals are to demonstrate practical understanding of:

- Data ingestion
- ETL architecture
- ELT architecture
- Reverse data movement
- API integration
- SQL transformations
- Relational databases
- Data quality and validation
- Logging and error handling
- Batch pipelines
- Cloud data pipelines
- Streaming data
- Data visualization
- End-to-end data engineering architecture

---

# 🔐 Security

Sensitive credentials are **not committed** to this repository.

Database credentials and API keys are stored using environment variables.

Example:

```text
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

The actual `.env` file is excluded using `.gitignore`.

Only `.env.example` files are included so developers can understand the required configuration.

---

# 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/riddhijosh2006-rgb/All_Pipeline_Under_one.git
cd All_Pipeline_Under_one
```

Open an individual project directory and follow its project-specific README.

Example:

```bash
cd data-engineering-project-ELT
python -m pip install -r requirements.txt
```

Create your local `.env` file from `.env.example`, configure the required database/API settings, and follow the project's instructions.

---

# 📊 Project Status

```text
Project 1 — ELT Pipeline
████████████████████ 100% ✅

Project 2 — API Data Pipeline
████████████████████ 100% ✅

Project 3 — ETL Pipeline
██████████████░░░░░░  70% 🔜 Uploading

Project 4 — Reverse Data Pipeline
████░░░░░░░░░░░░░░░░  20% 🔜 Planned

Project 5 — AWS Pipeline
██░░░░░░░░░░░░░░░░░░  10% 🔜 Planned

Project 6 — Real-Time Pipeline
██░░░░░░░░░░░░░░░░░░  10% 🔜 Planned
```

---

# 👩‍💻 Author

## Riddhi Joshi

Final-year Computer Science student building practical projects in:

- Data Engineering
- Data Science
- Python
- SQL
- AI/ML
- Cloud Technologies

---

## ⭐ Repository Vision

The long-term goal is to build a complete collection of **end-to-end data engineering projects**, covering multiple directions of data movement.

```text
                         DATA ENGINEERING
                                │
              ┌─────────────────┼─────────────────┐
              ↓                 ↓                 ↓
             ETL               ELT            Reverse
              │                 │              Pipeline
              └─────────────────┼─────────────────┘
                                ↓
                              APIs
                                ↓
                               AWS
                                ↓
                              Kafka
                                ↓
                         Real-Time Systems
```

The repository will continue to grow from basic batch processing toward cloud-based, reverse, and real-time data engineering systems.

⭐ Explore the individual projects to see the complete implementation of each pipeline.
