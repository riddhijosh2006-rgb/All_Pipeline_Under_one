# 🌦️ API Data Pipeline — Weather Data Engineering Project

An end-to-end **Data Engineering pipeline** that extracts hourly weather data from the **Open-Meteo API** for multiple Indian cities, transforms the raw API response using **Pandas**, performs automated data-quality validation, loads the validated data into **PostgreSQL**, executes analytical SQL queries, and presents the results through an interactive **Streamlit dashboard**.

The project follows a complete ETL workflow:

```text
Open-Meteo API
      ↓
   Extract
      ↓
  Transform
      ↓
 Data Validation
      ↓
  PostgreSQL
      ↓
 SQL Analytics
      ↓
Streamlit Dashboard
```

---

## 📌 Project Overview

This project demonstrates how an external API can be converted into a complete data engineering pipeline.

The pipeline collects weather information for **8 Indian cities**:

* Ahmedabad
* Mumbai
* Delhi
* Bangalore
* Pune
* Hyderabad
* Chennai
* Kolkata

For each city, the pipeline retrieves hourly:

* Temperature
* Relative humidity
* Wind speed
* Timestamp

The data is then transformed into a structured Pandas DataFrame, validated using multiple data-quality rules, and stored in PostgreSQL.

The stored data can then be analyzed using SQL and visualized through the Streamlit dashboard.

---

# 🏗️ Architecture

```text
                         ┌──────────────────────────┐
                         │      Open-Meteo API      │
                         │    Weather Forecast API  │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │         EXTRACT          │
                         │       src/extract.py     │
                         │                          │
                         │  8 Indian Cities         │
                         │  Hourly Weather Data     │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │        TRANSFORM         │
                         │      src/transform.py    │
                         │                          │
                         │        Pandas            │
                         │  Data Cleaning/Formatting│
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │    DATA VALIDATION       │
                         │      src/validate.py     │
                         │                          │
                         │  • Empty Data Check      │
                         │  • Schema Check          │
                         │  • NULL Check             │
                         │  • Duplicate Check       │
                         │  • Humidity Range        │
                         │  • Wind Speed Range      │
                         │  • Temperature Range     │
                         │  • Timestamp Check       │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │       PostgreSQL         │
                         │                          │
                         │       weather_data       │
                         └────────────┬─────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                         ▼                         ▼
              ┌──────────────────────┐   ┌──────────────────────┐
              │     SQL ANALYTICS    │   │  STREAMLIT DASHBOARD │
              │   sql/queries.sql    │   │    dashboard/app.py  │
              │                      │   │                      │
              │ 24+ Analytical       │   │ KPIs                 │
              │ Queries              │   │ Temperature Charts   │
              │                      │   │ Humidity Charts      │
              │ Daily Summary View   │   │ Wind Charts          │
              └──────────────────────┘   │ Data Table           │
                                         └──────────────────────┘
```

---

# ✨ Key Features

## 1. Multi-City Weather Extraction

The extraction module connects to the Open-Meteo forecast API and retrieves hourly weather data for eight Indian cities.

The API request collects:

```text
temperature_2m
relative_humidity_2m
wind_speed_10m
```

The pipeline requests **one forecast day** and uses the **Asia/Kolkata** timezone.

---

## 2. Data Transformation

The raw API response is converted into a structured Pandas DataFrame.

The transformed dataset contains:

| Column           | Description                  |
| ---------------- | ---------------------------- |
| `timestamp`      | Weather observation time     |
| `temperature_c`  | Temperature in Celsius       |
| `humidity_pct`   | Relative humidity percentage |
| `wind_speed_kmh` | Wind speed in km/h           |
| `city`           | City name                    |

The transformation layer also converts timestamps into Pandas datetime format and combines data from all cities into a single DataFrame.

---

# 3. Automated Data Quality Validation

Before loading the data into PostgreSQL, the pipeline performs **8 validation checks**.

### Check 1 — DataFrame Not Empty

Ensures that the transformation stage produced data.

### Check 2 — Required Columns

Checks that all required columns exist:

```text
timestamp
temperature_c
humidity_pct
wind_speed_kmh
city
```

### Check 3 — NULL Values

Checks for missing values in required columns.

### Check 4 — Duplicate Records

Checks duplicates using:

```text
timestamp + city
```

### Check 5 — Humidity Range

Humidity must remain between:

```text
0% and 100%
```

### Check 6 — Wind Speed

Wind speed cannot be negative.

### Check 7 — Temperature Range

Temperature must remain within:

```text
-90°C to 60°C
```

### Check 8 — Timestamp

Ensures the timestamp column contains valid datetime values.

If any validation fails, the pipeline raises an exception and stops.

---

# 🗄️ PostgreSQL Data Storage

The project uses PostgreSQL as the primary data warehouse/storage layer.

The pipeline automatically creates the following table if it does not already exist:

```text
weather_data
```

### Table structure

```text
weather_data
│
├── id
├── timestamp
├── temperature_c
├── humidity_pct
├── wind_speed_kmh
└── city
```

The loader uses PostgreSQL through:

```text
psycopg2
```

The database connection is configured using environment variables.

---

# 🔁 Duplicate Prevention

The loader is designed to avoid inserting duplicate weather records.

Records are identified using:

```text
timestamp + city
```

Duplicate records are skipped instead of being inserted again.

This allows the pipeline to be executed repeatedly without unnecessarily duplicating the same city/time records.

---

# 📝 Logging

The project contains a dedicated logging module:

```text
src/logger.py
```

Logs are written to:

```text
logs/pipeline.log
```

The logger records important pipeline events such as:

* API extraction
* Transformation
* Validation
* PostgreSQL connection
* Table creation
* Data loading
* Duplicate records
* Pipeline failures
* Pipeline completion

This makes the pipeline easier to monitor and debug.

---

# 📊 SQL Analytics

The project contains an extensive SQL analytics file:

```text
sql/queries.sql
```

The SQL layer contains **24+ analytical queries and a daily summary view**.

### Analytics included

* View all weather data
* Total record count
* Weather summary
* Temperature classification
* Temperature ranking
* Top 5 hottest hours
* Top 5 coldest hours
* Hottest period
* Coldest period
* Highest humidity
* Lowest humidity
* Strongest wind
* Weakest wind
* 3-hour moving average
* Hourly weather analysis
* Daily weather summary
* Temperature trend
* Highest temperature change
* Weather condition classification
* City-level summary
* Data-quality summary
* Dashboard KPI query
* Dashboard chart data
* Recent weather data

---

# 📅 Daily Weather Summary View

The SQL layer also creates:

```text
weather_daily_summary
```

This view provides city-level daily statistics including:

* Total records
* Average temperature
* Maximum temperature
* Minimum temperature
* Average humidity
* Maximum humidity
* Average wind speed
* Maximum wind speed

---

# 📈 Streamlit Dashboard

The project includes an interactive weather analytics dashboard:

```text
dashboard/app.py
```

The dashboard connects directly to PostgreSQL and displays the stored weather data.

## Dashboard Features

### 🌡️ Current Temperature

Displays the latest available temperature.

### 💧 Current Humidity

Displays the latest humidity percentage.

### 💨 Current Wind

Displays the latest wind speed.

### 📊 Total Records

Displays the number of records for the selected city.

### 📍 City Filter

Users can select a city from the sidebar.

Available cities:

```text
Ahmedabad
Mumbai
Delhi
Bangalore
Pune
Hyderabad
Chennai
Kolkata
```

### 📊 Weather Summary

The dashboard calculates:

* Average temperature
* Maximum temperature
* Minimum temperature
* Average humidity

### 📈 Temperature Trend

Interactive Plotly line chart showing temperature over time.

### 💧 Humidity Trend

Interactive chart showing humidity over time.

### 💨 Wind Speed

Interactive chart showing wind-speed changes over time.

### 📊 Combined Weather Analysis

Displays temperature, humidity, and wind speed together.

### 📋 Weather Data Table

Displays the processed PostgreSQL weather records directly in the dashboard.

### 🔄 Refresh Data

The dashboard includes a refresh option that clears the cached data and reloads the latest PostgreSQL records.

---

# 📂 Project Structure

```text
api_data_pipeline/
│
├── config/
│   └── config.py
│
├── dashboard/
│   └── app.py
│
├── logs/
│   └── pipeline.log
│
├── sql/
│   └── queries.sql
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── load.py
│   ├── pipeline.py
│   └── logger.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

| Technology     | Purpose                   |
| -------------- | ------------------------- |
| Python         | Pipeline development      |
| Requests       | API requests              |
| Open-Meteo API | Weather data source       |
| Pandas         | Data transformation       |
| PostgreSQL     | Data storage              |
| psycopg2       | PostgreSQL connectivity   |
| SQL            | Data analysis             |
| Streamlit      | Interactive dashboard     |
| Plotly         | Data visualization        |
| python-dotenv  | Environment configuration |
| Logging        | Pipeline monitoring       |
| Git            | Version control           |
| GitHub         | Repository hosting        |

---

# ⚙️ Requirements

Before running the project, install:

* Python 3.10+
* PostgreSQL
* Git
* Internet connection

Python dependencies are provided in:

```text
requirements.txt
```

---

# 🚀 Installation

## Step 1 — Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Go inside the project:

```bash
cd api_data_pipeline
```

---

## Step 2 — Create Virtual Environment

On Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

After activation, your terminal should show:

```text
(venv)
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ PostgreSQL Configuration

Create a PostgreSQL database:

```text
weather_pipeline_db
```

Then create a `.env` file in the project root.

Use:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=weather_pipeline_db
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
```

The application reads these values through `config/config.py`.

### ⚠️ Security

Never commit your real `.env` file to GitHub.

Your `.gitignore` should contain:

```gitignore
.env
__pycache__/
*.pyc
```

---

# ▶️ Running the Complete Pipeline

From the project root:

```bash
python -m src.pipeline
```

This executes the complete workflow automatically:

```text
STEP 1 → EXTRACT
       ↓
STEP 2 → TRANSFORM
       ↓
STEP 3 → DATA QUALITY VALIDATION
       ↓
STEP 4 → LOAD
       ↓
PIPELINE COMPLETED
```

You do **not** need to manually execute every Python file when using `pipeline.py`.

---

# 📊 Running the Dashboard

After the pipeline has successfully loaded data into PostgreSQL, run:

```bash
python -m streamlit run dashboard/app.py
```

Alternatively:

```bash
streamlit run dashboard/app.py
```

The Streamlit application will open in your browser.

---

# 🧪 Running Individual Pipeline Components

If you want to test individual stages:

### Extract

```bash
python -m src.extract
```

### Transform

```bash
python -m src.transform
```

### Validation

```bash
python -m src.validate
```

### Database Table Creation

```bash
python -m src.load
```

### Complete Pipeline

```bash
python -m src.pipeline
```

---

# 🔍 Checking Pipeline Logs

After running the pipeline, check:

```text
logs/pipeline.log
```

You can use the log file to identify:

* Successful API requests
* Transformation status
* Validation results
* Database connection problems
* Data loading results
* Duplicate records
* Pipeline errors

---

# 📌 Data Flow

The actual data flow of this project is:

```text
                 Open-Meteo API
                       │
                       │
                       ▼
                src/extract.py
                       │
                       │ Raw API Data
                       ▼
               src/transform.py
                       │
                       │ Pandas DataFrame
                       ▼
                src/validate.py
                       │
                       │ Validated Data
                       ▼
                  src/load.py
                       │
                       ▼
                 PostgreSQL
                weather_data
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
        sql/queries.sql    dashboard/app.py
              │                 │
              ▼                 ▼
       SQL Analytics      Streamlit Dashboard
```

---

# 🎯 Project Objectives

The main objectives of this project are:

1. Build a complete ETL pipeline.
2. Work with a real external API.
3. Extract data for multiple cities.
4. Transform JSON API responses into structured data.
5. Implement automated data-quality checks.
6. Store structured data in PostgreSQL.
7. Prevent duplicate records.
8. Perform advanced SQL analysis.
9. Create reusable analytical views.
10. Build an interactive data visualization dashboard.
11. Implement logging and error handling.
12. Follow environment-based configuration practices.

---

# 💡 What This Project Demonstrates

This project demonstrates practical understanding of:

```text
API Integration
      ↓
ETL Development
      ↓
Data Transformation
      ↓
Data Quality
      ↓
Relational Database
      ↓
SQL Analytics
      ↓
Data Visualization
      ↓
Pipeline Monitoring
```

It is therefore a practical example of an **end-to-end Data Engineering workflow** rather than only a data-analysis project.

---

# 🔮 Future Improvements

The current pipeline can be extended with:

* Apache Airflow for scheduling
* Docker containerization
* AWS S3 data lake
* AWS RDS PostgreSQL
* CI/CD using GitHub Actions
* Automated unit tests
* Pipeline monitoring
* Retry mechanisms for failed API requests
* Historical weather data
* More weather parameters
* More cities and countries
* Cloud deployment
* Data warehouse integration
* Automated daily pipeline execution

---

# 👩‍💻 Author

**Riddhi Joshi**

B.Tech — Computer Science Engineering (Data Science)

---

# ⭐ Final Pipeline

```text
🌐 Open-Meteo API
        ↓
📥 Extract
        ↓
🔄 Transform
        ↓
✅ Validate
        ↓
🗄️ PostgreSQL
        ↓
📊 SQL Analytics
        ↓
📈 Streamlit Dashboard
```

**An end-to-end weather data engineering pipeline built with Python, PostgreSQL, SQL, and Streamlit.**
