import pandas as pd
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def create_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def extract_raw():
    """
    ELT extract step: read the CSV with ZERO cleaning.
    Everything is kept as text - transformation happens later, inside Postgres.
    """
    try:
        file_path = "data/customers.csv"
        df = pd.read_csv(file_path, dtype=str)  # keep everything as raw text

        print(f"Extracted {len(df)} raw rows from CSV.")
        return df

    except FileNotFoundError:
        print("ERROR: customers.csv file was not found.")
        return None

    except Exception as e:
        print(f"ERROR during extraction: {e}")
        return None


def create_raw_table():
    """Creates the staging table that holds untouched, raw data."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_customers (
            customer_id TEXT,
            name TEXT,
            age TEXT,
            city TEXT,
            purchase_amount TEXT,
            _loaded_at TIMESTAMP DEFAULT NOW()
        );
    """)

    connection.commit()
    cursor.close()
    connection.close()

    print("raw_customers table ready.")


def load_raw(df):
    """
    Loads the raw dataframe straight into Postgres. No cleaning, no validation.
    Table is truncated first so each pipeline run reflects the latest CSV
    (dedup/cleanup logic lives in sql/transform.sql instead).
    """
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("TRUNCATE TABLE raw_customers;")

    insert_query = """
        INSERT INTO raw_customers (customer_id, name, age, city, purchase_amount, _loaded_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    now = datetime.now()

    for _, row in df.iterrows():
        cursor.execute(insert_query, (
            row.get("customer_id"),
            row.get("name"),
            row.get("age"),
            row.get("city"),
            row.get("purchase_amount"),
            now
        ))

    connection.commit()
    cursor.close()
    connection.close()

    print(f"{len(df)} raw records loaded into raw_customers.")


if __name__ == "__main__":
    create_raw_table()
    raw_df = extract_raw()
    if raw_df is not None:
        load_raw(raw_df)
