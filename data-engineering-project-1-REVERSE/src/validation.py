import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from src.logger import logger

load_dotenv()


def validate_data():
    """
    Same data-quality checks as the old ETL version, but run against the
    transformed 'customers' table in Postgres instead of an in-memory DataFrame.
    """
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    df = pd.read_sql("SELECT * FROM customers", connection)
    connection.close()

    logger.info("Starting data validation")

    # 1. Duplicate customer IDs
    duplicate_ids = df[df["customer_id"].duplicated()]
    if not duplicate_ids.empty:
        logger.error(f"Duplicate customer IDs found: {duplicate_ids['customer_id'].tolist()}")
        print("Validation failed: Duplicate customer IDs found.")
        return False

    # 2. Invalid ages
    invalid_age = df[(df["age"] < 0) | (df["age"] > 120)]
    if not invalid_age.empty:
        logger.error(f"Invalid ages found: {invalid_age['age'].tolist()}")
        print("Validation failed: Invalid age found.")
        return False

    # 3. Invalid purchase amounts
    invalid_purchase = df[df["purchase_amount"] < 0]
    if not invalid_purchase.empty:
        logger.error(f"Invalid purchase amounts found: {invalid_purchase['purchase_amount'].tolist()}")
        print("Validation failed: Negative purchase amount found.")
        return False

    # 4. Missing important values
    for column in ["customer_id", "name", "city"]:
        if df[column].isnull().any():
            logger.error(f"Missing values found in {column}")
            print(f"Validation failed: Missing values in {column}")
            return False

    logger.info(f"Data validation successful - {len(df)} records validated")
    print(f"Data validation successful - {len(df)} records validated")
    return True
