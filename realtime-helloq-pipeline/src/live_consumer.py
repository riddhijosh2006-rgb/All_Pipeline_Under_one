import json
import os

from dotenv import load_dotenv
from kafka import KafkaConsumer

from .consumer import save_event, update_realtime_status


load_dotenv()


KAFKA_SERVER = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "127.0.0.1:9092"
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_LIVE_TOPIC",
    "helloq-live-events"
)

CONSUMER_GROUP = "helloq-live-processing-group"


def create_live_consumer():

    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        group_id=CONSUMER_GROUP,
        auto_offset_reset="latest",
        enable_auto_commit=False,
        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        ),
    )


def main():

    print("=" * 60)
    print("HELLOQ LIVE KAFKA CONSUMER")
    print("=" * 60)
    print(f"Kafka server : {KAFKA_SERVER}")
    print(f"Topic        : {KAFKA_TOPIC}")
    print(f"Consumer     : {CONSUMER_GROUP}")
    print("=" * 60)

    consumer = create_live_consumer()

    processed = 0

    try:

        for message in consumer:

            event = message.value

            try:

                inserted = save_event(event)

                if inserted == 1:

                    update_realtime_status(event)

                    processed += 1

                    print(
                        f"[LIVE CONSUMER] "
                        f"event_id={event['event_id']} | "
                        f"user_id={event['user_id']} | "
                        f"type={event['event_type']}"
                    )

                else:

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
        print("[STOPPED] Live consumer stopped.")

    finally:

        consumer.close()

        print()
        print(
            f"Processed live events: {processed}"
        )


if __name__ == "__main__":
    main()