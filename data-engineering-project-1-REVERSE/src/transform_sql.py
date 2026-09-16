import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def run_transform():
    """Executes sql/transform.sql against Postgres - this IS the transform step."""
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = connection.cursor()

    with open("sql/transform.sql", "r") as f:
        sql_script = f.read()

    cursor.execute(sql_script)

    connection.commit()
    cursor.close()
    connection.close()

    print("Transformation completed inside PostgreSQL.")


if __name__ == "__main__":
    run_transform()
