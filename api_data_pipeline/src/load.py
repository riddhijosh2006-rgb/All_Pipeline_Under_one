import psycopg2

from config.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

from src.logger import logger


def create_connection():

    logger.info("Connecting to PostgreSQL...")

    try:

        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        logger.info("PostgreSQL connection successful!")

        return connection

    except psycopg2.Error as e:

        logger.exception(
            f"PostgreSQL connection failed: {e}"
        )

        raise


def create_table():

    logger.info("Checking weather_data table...")

    connection = None
    cursor = None

    try:

        connection = create_connection()
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            temperature_c DECIMAL(10, 2),
            humidity_pct INTEGER,
            wind_speed_kmh DECIMAL(10, 2),
            city VARCHAR(100)
        );
        """

        cursor.execute(create_table_query)

        connection.commit()

        logger.info(
            "Weather table created successfully!"
        )

    except psycopg2.Error as e:

        if connection:
            connection.rollback()

        logger.exception(
            f"Failed to create weather table: {e}"
        )

        raise

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def load_data(df):

    logger.info("Loading data into PostgreSQL...")

    connection = None
    cursor = None

    try:

        connection = create_connection()
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO weather_data
        (
            timestamp,
            temperature_c,
            humidity_pct,
            wind_speed_kmh,
            city
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (timestamp, city)
        DO NOTHING;
        """

        inserted_rows = 0

        for _, row in df.iterrows():

            cursor.execute(
                insert_query,
                (
                    row["timestamp"],
                    row["temperature_c"],
                    row["humidity_pct"],
                    row["wind_speed_kmh"],
                    row["city"]
                )
            )

            inserted_rows += cursor.rowcount

        connection.commit()

        duplicate_rows = len(df) - inserted_rows

        logger.info(
            f"{inserted_rows} new rows loaded successfully!"
        )

        logger.info(
            f"{duplicate_rows} duplicate rows skipped!"
        )

    except psycopg2.Error as e:

        if connection:
            connection.rollback()

        logger.exception(
            f"Failed to load data into PostgreSQL: {e}"
        )

        raise

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    create_table()