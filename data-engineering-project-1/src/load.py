import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def create_connection():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    return connection


def create_table():

    connection = create_connection()
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name VARCHAR(100),
        age INTEGER,
        city VARCHAR(100),
        purchase_amount NUMERIC(10, 2),
        purchase_category VARCHAR(20)
    );
    """

    cursor.execute(create_table_query)

    connection.commit()

    cursor.close()
    connection.close()

    print("Customers table created successfully!")


def load_data(df):

    connection = create_connection()
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO customers
    (
        customer_id,
        name,
        age,
        city,
        purchase_amount,
        purchase_category
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (customer_id)
    DO UPDATE SET
        name = EXCLUDED.name,
        age = EXCLUDED.age,
        city = EXCLUDED.city,
        purchase_amount = EXCLUDED.purchase_amount,
        purchase_category = EXCLUDED.purchase_category;
    """

    for _, row in df.iterrows():

        cursor.execute(
            insert_query,
            (
                int(row["customer_id"]),
                row["name"],
                int(row["age"]),
                row["city"],
                float(row["purchase_amount"]),
                row["purchase_category"]
            )
        )

    connection.commit()

    cursor.close()
    connection.close()

    print(f"{len(df)} records loaded successfully!")


if __name__ == "__main__":
    create_table()