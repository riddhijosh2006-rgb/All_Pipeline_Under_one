import psycopg2


def create_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="weather_pipeline_db",
        user="postgres",
        password="YOUR_POSTGRES_PASSWORD",
        port="5432"
    )

    return connection


def create_table():

    connection = create_connection()
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS weather_data (
        timestamp TIMESTAMP,
        temperature_c DECIMAL(10, 2),
        humidity_pct INTEGER,
        wind_speed_kmh DECIMAL(10, 2),
        city VARCHAR(100)
    );
    """

    cursor.execute(create_table_query)

    connection.commit()

    cursor.close()
    connection.close()

    print("Weather table created successfully!")


def load_data(df):

    print("Loading data into PostgreSQL...")

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
    """

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

    connection.commit()

    cursor.close()
    connection.close()

    print(f"{len(df)} rows loaded successfully!")