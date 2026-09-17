import json
import os
import random
import time
from datetime import datetime

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
    "127.0.0.1:9092"
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_LIVE_TOPIC",
    "helloq-live-events"
)

LIVE_EVENTS = int(
    os.getenv("LIVE_EVENTS", "100")
)

EVENT_DELAY = float(
    os.getenv("LIVE_EVENT_DELAY", "1")
)


EVENT_TYPES = [
    "login",
    "profile_view",
    "profile_view",
    "profile_view",
    "interest_sent",
    "interest_accepted",
    "match_created",
    "chat_started",
    "message_sent",
    "message_sent",
    "logout",
]


def get_users():
    """Load users from PostgreSQL."""

    query = """
        SELECT
            user_id,
            city
        FROM users
        ORDER BY user_id;
    """

    connection = None

    try:
        connection = psycopg2.connect(**DB_CONFIG)

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        return rows

    finally:
        if connection:
            connection.close()


def get_starting_event_id():
    """Get next available event ID across historical and processed events."""

    connection = None

    try:
        connection = psycopg2.connect(**DB_CONFIG)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT GREATEST(
                    COALESCE(
                        (SELECT MAX(event_id) FROM user_events),
                        0
                    ),
                    COALESCE(
                        (SELECT MAX(event_id) FROM processed_events),
                        0
                    )
                );
                """
            )

            last_id = cursor.fetchone()[0]

        return last_id + 1

    finally:
        if connection:
            connection.close()
    """Get next available event ID."""

    connection = None

    try:
        connection = psycopg2.connect(**DB_CONFIG)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COALESCE(MAX(event_id), 0)
                FROM processed_events;
                """
            )

            last_id = cursor.fetchone()[0]

        return last_id + 1

    finally:
        if connection:
            connection.close()


def create_producer():
    """Create Kafka producer."""

    return KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,

        key_serializer=lambda key: str(key).encode("utf-8"),

        value_serializer=lambda value: json.dumps(
            value,
            default=str
        ).encode("utf-8"),
    )
def generate_event(
    event_id,
    users
):
    """Generate one realistic application event."""

    user_id, city = random.choice(users)

    event_type = random.choice(EVENT_TYPES)

    target_user_id = None

    if event_type in {
        "profile_view",
        "interest_sent",
        "interest_accepted",
        "match_created",
        "chat_started",
        "message_sent",
    }:

        possible_targets = [
            user[0]
            for user in users
            if user[0] != user_id
        ]

        target_user_id = random.choice(
            possible_targets
        )

    event = {
        "event_id": event_id,
        "user_id": user_id,
        "event_type": event_type,
        "event_time": datetime.now(),
        "session_id": (
            f"live_session_{user_id}_"
            f"{datetime.now().strftime('%Y%m%d%H')}"
        ),
        "target_user_id": target_user_id,
        "city": city,
        "device": random.choice(
            ["Android", "iOS", "Web"]
        ),
    }

    return event


def main():

    print("=" * 60)
    print("HELLOQ LIVE APPLICATION EVENT GENERATOR")
    print("=" * 60)
    print(f"Kafka server : {KAFKA_SERVER}")
    print(f"Live topic   : {KAFKA_TOPIC}")
    print(f"Events       : {LIVE_EVENTS}")
    print(f"Delay        : {EVENT_DELAY} sec")
    print("=" * 60)

    users = get_users()

    if not users:
        print("[ERROR] No users found.")
        return

    print(f"[POSTGRES] Loaded {len(users)} users.")

    starting_id = get_starting_event_id()

    producer = create_producer()

    print(
        f"[LIVE] Starting from event_id={starting_id}"
    )

    produced = 0

    try:

        for i in range(LIVE_EVENTS):

            event_id = starting_id + i

            event = generate_event(
                event_id,
                users
            )

            producer.send(
                KAFKA_TOPIC,
                key=str(event["user_id"]),
                value=event,
            )

            produced += 1

            print(
                f"[LIVE EVENT] "
                f"event_id={event['event_id']} | "
                f"user_id={event['user_id']} | "
                f"type={event['event_type']} | "
                f"city={event['city']}"
            )

            time.sleep(EVENT_DELAY)

        producer.flush()

        print()
        print(
            f"[SUCCESS] {produced} live events sent."
        )

    except KeyboardInterrupt:

        print()
        print("[STOPPED] Live generator stopped.")

    finally:
        producer.close()


if __name__ == "__main__":
    main()