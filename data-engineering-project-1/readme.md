# Customer Data Engineering Pipeline

A Python-based **ETL Data Engineering Pipeline** that extracts customer data from a CSV file, transforms and validates the data, and loads the processed records into a PostgreSQL database.

This project demonstrates the fundamental stages of a real-world data pipeline:

**Extract → Transform → Validate → Load**

---

## 🚀 Project Overview

The pipeline processes customer transaction data and stores the cleaned and validated information in PostgreSQL.

### Pipeline Architecture

```text
customers.csv
     │
     ▼
┌─────────────┐
│   EXTRACT   │
│   Pandas    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  TRANSFORM  │
│ Data Cleaning│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  VALIDATE   │
│ Data Quality│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    LOAD     │
│ PostgreSQL  │
└─────────────┘
```

---

## ✨ Features

* CSV data extraction using Pandas
* Data transformation and cleaning
* Data validation before loading
* PostgreSQL database integration
* Automatic database table creation
* Environment variable configuration using `.env`
* Duplicate handling using PostgreSQL `ON CONFLICT`
* Pipeline logging
* Error handling
* Modular Python project structure

---

## 🛠️ Technologies Used

| Technology    | Purpose                            |
| ------------- | ---------------------------------- |
| Python        | Pipeline development               |
| Pandas        | Data extraction and transformation |
| PostgreSQL    | Data storage                       |
| psycopg2      | PostgreSQL connection              |
| python-dotenv | Environment variable management    |
| SQL           | Database operations                |
| Git & GitHub  | Version control                    |

---

## 📁 Project Structure

```text
data-engineering-project-1/
│
├── config/
│   └── config.py
│
├── data/
│   └── customers.csv
│
├── logs/
│   └── pipeline.log
│
├── sql/
│   └── queries.sql
│
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── validation.py
│   ├── load.py
│   ├── logger.py
│   └── pipeline.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔄 Pipeline Workflow

### 1. Extract

The pipeline reads customer data from:

```text
data/customers.csv
```

Pandas is used to load the dataset into a DataFrame.

### 2. Transform

The extracted data is cleaned and transformed before entering the database.

### 3. Validate

The transformed dataset is checked for data-quality issues.

The pipeline stops if validation fails.

### 4. Load

After successful validation, the data is loaded into PostgreSQL.

The pipeline automatically creates the `customers` table if it does not already exist.

---

## 🗄️ Database

The pipeline uses PostgreSQL.

Database configuration is stored in environment variables:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

The `customers` table contains:

```sql
customer_id
name
age
city
purchase_amount
purchase_category
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/riddhijosh2006-rgb/All_Pipeline_Under_one.git
```

### 2. Navigate to the project

```bash
cd All_Pipeline_Under_one
```

Then navigate into this pipeline's folder:

```bash
cd data-engineering-project-1
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=customer_pipeline
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
```

**Never commit your actual `.env` file or database password to GitHub.**

### 6. Create the PostgreSQL database

Create a PostgreSQL database named:

```text
customer_pipeline
```

Make sure PostgreSQL is running before executing the pipeline.

### 7. Run the pipeline

From the repository/project directory:

```bash
python -m src.pipeline
```

---

## 📊 Expected Pipeline Output

```text
========== DATA PIPELINE STARTED ==========

STEP 1: EXTRACT
Data extracted successfully!

STEP 2: TRANSFORM
Transformation completed!

STEP 3: VALIDATE
Data validation successful!

STEP 4: LOAD
Customers table created successfully!
Records loaded successfully!

========== DATA PIPELINE COMPLETED ==========
```

---

## 🔐 Security

Sensitive configuration is intentionally excluded from GitHub.

The following files/folders should not be committed:

```text
.env
venv/
__pycache__/
*.pyc
logs/
```

Use `.env.example` to show the required environment variables without exposing credentials.

---

## 🎯 Learning Objectives

This project was created to understand practical Data Engineering concepts including:

* ETL pipelines
* Data extraction
* Data transformation
* Data validation
* Data loading
* PostgreSQL integration
* SQL
* Environment variables
* Logging
* Error handling
* Modular Python architecture
* Git and GitHub

---

## 🔮 Future Improvements

Possible future enhancements include:

* Scheduled pipeline execution
* API-based data extraction
* Apache Airflow orchestration
* Docker containerization
* AWS S3 integration
* Apache Kafka streaming
* Data quality monitoring
* Automated testing
* CI/CD integration
* Cloud deployment
* Dashboard and analytics layer

---

## 👩‍💻 Author

**Riddhi Joshi**

B.Tech – Computer Science Engineering (Data Science)

This project is part of a Data Engineering learning portfolio.
