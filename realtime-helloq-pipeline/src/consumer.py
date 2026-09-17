import json
import os

import psycopg2
from dotenv import load_dotenv
from kafka import KafkaConsumer


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
    "KAFKA_TOPIC",
    "helloq-events"
)

CONSUMER_GROUP = "helloq-processing-group"


def create_consumer():
    """Create Kafka consumer."""

    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        group_id=CONSUMER_GROUP,
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        ),
    )


def save_event(event):
    """Validate and save event into processed_events."""

    required_fields = [
        "event_id",
        "user_id",
        "event_type",
        "event_time",
    ]

    for field in required_fields:
        if field not in event or event[field] is None:
            raise ValueError(
                f"Missing required field: {field}"
            )

    query = """
        INSERT INTO processed_events (
            event_id,
            user_id,
            event_type,
            event_time,
            session_id,
            target_user_id,
            city,
            device
        )
        VALUES (
            %s, %s, %s, %s,
            %s, %s, %s, %s
        )
        ON CONFLICT (event_id)
        DO NOTHING;
    """

    connection = None

    try:
        connection = psycopg2.connect(**DB_CONFIG)

        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    event["event_id"],
                    event["user_id"],
                    event["event_type"],
                    event["event_time"],
                    event.get("session_id"),
                    event.get("target_user_id"),
                    event.get("city"),
                    event.get("device"),
                ),
            )

            inserted = cursor.rowcount

        connection.commit()

        return inserted

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if connection:
            connection.close()


def update_realtime_status(event):
    """Update user real-time metrics for one event."""

    event_type = event["event_type"]

    profile_views = (
        1 if event_type == "profile_view" else 0
    )

    interests_sent = (
        1 if event_type == "interest_sent" else 0
    )

    matches_created = (
        1 if event_type == "match_created" else 0
    )

    chats_started = (
        1 if event_type == "chat_started" else 0
    )

    messages_sent = (
        1 if event_type == "message_sent" else 0
    )

    engagement_points = {
        "profile_view": 0.5,
        "interest_sent": 2.0,
        "match_created": 3.0,
        "chat_started": 4.0,
        "message_sent": 1.2,
        "interest_accepted": 2.0,
        "login": 1.0,
        "logout": 0.0,
        "registration_started": 1.0,
        "registration_completed": 1.0,
    }

    score = engagement_points.get(event_type, 1.0)

    current_status = (
        "offline"
        if event_type == "logout"
        else "active"
    )

    last_login = (
        event["event_time"]
        if event_type == "login"
        else None
    )

    query = """
        INSERT INTO user_realtime_status (
            user_id,
            last_event_time,
            last_login,
            last_activity,
            current_status,
            total_events,
            profile_views,
            interests_sent,
            matches_created,
            chats_started,
            messages_sent,
            engagement_score,
            updated_at
        )
        VALUES (
            %s, %s, %s, %s, %s,
            1, %s, %s, %s, %s, %s, %s,
            CURRENT_TIMESTAMP
        )

        ON CONFLICT (user_id)
        DO UPDATE SET

            last_event_time = GREATEST(
                user_realtime_status.last_event_time,
                EXCLUDED.last_event_time
            ),

            last_login = CASE
                WHEN EXCLUDED.last_login IS NOT NULL
                THEN GREATEST(
                    COALESCE(
                        user_realtime_status.last_login,
                        EXCLUDED.last_login
                    ),
                    EXCLUDED.last_login
                )
                ELSE user_realtime_status.last_login
            END,

            last_activity = GREATEST(
                user_realtime_status.last_activity,
                EXCLUDED.last_activity
            ),

            current_status = EXCLUDED.current_status,

            total_events =
                user_realtime_status.total_events + 1,

            profile_views =
                user_realtime_status.profile_views
                + EXCLUDED.profile_views,

            interests_sent =
                user_realtime_status.interests_sent
                + EXCLUDED.interests_sent,

            matches_created =
                user_realtime_status.matches_created
                + EXCLUDED.matches_created,

            chats_started =
                user_realtime_status.chats_started
                + EXCLUDED.chats_started,

            messages_sent =
                user_realtime_status.messages_sent
                + EXCLUDED.messages_sent,

            engagement_score =
                user_realtime_status.engagement_score
                + EXCLUDED.engagement_score,

            updated_at = CURRENT_TIMESTAMP;
    """

    connection = None

    try:
        connection = psycopg2.connect(**DB_CONFIG)

        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    event["user_id"],
                    event["event_time"],
                    last_login,
                    event["event_time"],
                    current_status,
                    profile_views,
                    interests_sent,
                    matches_created,
                    chats_started,
                    messages_sent,
                    score,
                ),
            )

        connection.commit()

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if connection:
            connection.close()


def main():

    print("=" * 60)
    print("HELLOQ REAL-TIME KAFKA CONSUMER")
    print("=" * 60)
    print(f"Kafka server : {KAFKA_SERVER}")
    print(f"Topic        : {KAFKA_TOPIC}")
    print(f"Consumer     : {CONSUMER_GROUP}")
    print("=" * 60)

    consumer = create_consumer()

    processed = 0
    duplicates = 0

    try:

        for message in consumer:

            event = message.value

            try:

                inserted = save_event(event)

                if inserted == 1:

                    update_realtime_status(event)

                    processed += 1

                    print(
                        f"[CONSUMER] "
                        f"event_id={event['event_id']} | "
                        f"user_id={event['user_id']} | "
                        f"type={event['event_type']}"
                    )

                else:

                    duplicates += 1

                    print(
                        f"[DUPLICATE] "
                        f"event_id={event['event_id']} skipped"
                    )

                consumer.commit()

            except Exception as error:

                print(
                    f"[ERROR] "
                    f"event_id={event.get('event_id')} | "
                    f"{error}"
                )

    except KeyboardInterrupt:

        print()
        print("[STOPPED] Consumer stopped by user.")

    finally:

        consumer.close()

        print()
        print(f"Processed events : {processed}")
        print(f"Duplicates       : {duplicates}")


if __name__ == "__main__":
    main()