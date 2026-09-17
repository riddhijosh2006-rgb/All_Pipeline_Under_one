import json
import os
import time

import psycopg2
from dotenv import load_dotenv
from kafka import KafkaProducer


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "helloq_realtime"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}

KAFKA_SERVER = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092"
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "helloq-events"
)

EVENT_DELAY = float(
    os.getenv("EVENT_DELAY", "0.1")
)


def fetch_events(limit=2000):
    """Read application events from PostgreSQL."""

    query = """
        SELECT
            event_id,
            user_id,
            event_type,
            event_time,
            session_id,
            target_user_id,
            city,
            device
        FROM user_events
        ORDER BY event_time, event_id
        LIMIT %s;
    """

    connection = None

    try:
        connection = psycopg2.connect(**DB_CONFIG)

        with connection.cursor() as cursor:
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()

        print(f"[POSTGRES] Loaded {len(rows)} events.")

        events = []

        for row in rows:
            event = {
                "event_id": row[0],
                "user_id": row[1],
                "event_type": row[2],
                "event_time": row[3],
                "session_id": row[4],
                "target_user_id": row[5],
                "city": row[6],
                "device": row[7],
            }

            events.append(event)

        return events

    except Exception as error:
        print(f"[ERROR] PostgreSQL read failed: {error}")
        raise

    finally:
        if connection:
            connection.close()


def create_kafka_producer():
    """Create Kafka producer."""

    return KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        key_serializer=lambda key: str(key).encode("utf-8"),
        value_serializer=lambda value: json.dumps(
            value,
            default=str
        ).encode("utf-8"),
    )


def stream_events(events):
    """Send events to Kafka one by one."""

    producer = create_kafka_producer()

    print()
    print("=" * 60)
    print("HELLOQ REAL-TIME KAFKA PRODUCER")
    print("=" * 60)
    print(f"Kafka server : {KAFKA_SERVER}")
    print(f"Topic        : {KAFKA_TOPIC}")
    print(f"Events       : {len(events)}")
    print(f"Delay        : {EVENT_DELAY} sec")
    print("=" * 60)

    produced = 0

    try:
        for event in events:

            producer.send(
                KAFKA_TOPIC,
                key=event["user_id"],
                value=event,
            )

            produced += 1

            print(
                f"[PRODUCER] "
                f"event_id={event['event_id']} | "
                f"user_id={event['user_id']} | "
                f"type={event['event_type']}"
            )

            time.sleep(EVENT_DELAY)

        producer.flush()

        print()
        print(f"[SUCCESS] {produced} events sent to Kafka.")

    except KeyboardInterrupt:
        print("\n[STOPPED] Producer stopped by user.")

    except Exception as error:
        print(f"[ERROR] Kafka producer failed: {error}")
        raise

    finally:
        producer.close()


def main():
    print("[START] HelloQ real-time producer")

    events = fetch_events(limit=2000)

    if not events:
        print("[INFO] No events found in PostgreSQL.")
        return

    stream_events(events)


if __name__ == "__main__":
    main()
    