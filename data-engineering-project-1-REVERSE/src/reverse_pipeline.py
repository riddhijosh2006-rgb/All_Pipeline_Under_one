"""
Reverse Pipeline (Reverse ETL)
-------------------------------
Forward direction (ELT):  CSV -> raw_customers -> customers (clean)
Reverse direction:        customers (clean) -> back OUT to:
                             1. a new Postgres table (customer_action_queue)
                                that a CRM/marketing sync job could read from
                             2. a CSV file a human or another tool can import
                                directly (data/output/customer_action_queue.csv)

This is the standard "Reverse ETL" pattern: instead of only ever reading
FROM the database for reports, you take computed insights and push them
back OUT into the systems/files people actually use day to day.

Run AFTER sql/transform.sql has built the "customers" table:
    python -m src.reverse_pipeline
"""

import os
import csv
import psycopg2
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = "data/output"
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "customer_action_queue.csv")


def create_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


# ---------------------------------------------------------------------------
# Rule engine: query the clean "customers" table, decide who needs action.
# Threshold values kept as plain constants - easy to explain/tune.
# ---------------------------------------------------------------------------

HIGH_VALUE_THRESHOLD = 5000
PRIORITY_THRESHOLD = 10000


def find_action_candidates(cursor):
    """Returns a list of (customer_id, action_type, message) tuples."""
    candidates = []

    # Rule 1: priority follow-up for very high spenders
    cursor.execute(
        "SELECT customer_id, name, purchase_amount FROM customers WHERE purchase_amount >= %s",
        (PRIORITY_THRESHOLD,)
    )
    for customer_id, name, amount in cursor.fetchall():
        candidates.append((
            customer_id,
            "priority_follow_up",
            f"{name} spent {amount} - flag for a personal follow-up call."
        ))

    # Rule 2: general high-value customer, worth a loyalty offer
    cursor.execute(
        "SELECT customer_id, name, purchase_amount FROM customers "
        "WHERE purchase_amount >= %s AND purchase_amount < %s",
        (HIGH_VALUE_THRESHOLD, PRIORITY_THRESHOLD)
    )
    for customer_id, name, amount in cursor.fetchall():
        candidates.append((
            customer_id,
            "loyalty_offer",
            f"{name} spent {amount} - eligible for a loyalty/repeat-purchase offer."
        ))

    # Rule 3: zero purchase amount - re-engagement needed
    cursor.execute(
        "SELECT customer_id, name FROM customers WHERE purchase_amount = 0"
    )
    for customer_id, name in cursor.fetchall():
        candidates.append((
            customer_id,
            "reengagement_needed",
            f"{name} has no recorded purchase - consider a re-engagement email."
        ))

    return candidates


# ---------------------------------------------------------------------------
# Push into Postgres (idempotent) + export CSV snapshot
# ---------------------------------------------------------------------------

def ensure_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_action_queue (
            id SERIAL PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            action_type TEXT NOT NULL,
            message TEXT,
            resolved BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reverse_pipeline_runs (
            id SERIAL PRIMARY KEY,
            started_at TIMESTAMP NOT NULL,
            finished_at TIMESTAMP,
            status TEXT NOT NULL,
            actions_evaluated INTEGER,
            actions_created INTEGER,
            message TEXT
        );
    """)


def already_pending(cursor, customer_id, action_type):
    """Don't spam - skip if this customer already has an unresolved
    action of this exact type queued."""
    cursor.execute(
        "SELECT id FROM customer_action_queue "
        "WHERE customer_id = %s AND action_type = %s AND resolved = FALSE",
        (customer_id, action_type)
    )
    return cursor.fetchone() is not None


def push_actions(cursor, candidates):
    created = 0
    for customer_id, action_type, message in candidates:
        if already_pending(cursor, customer_id, action_type):
            continue
        cursor.execute(
            "INSERT INTO customer_action_queue (customer_id, action_type, message) "
            "VALUES (%s, %s, %s)",
            (customer_id, action_type, message)
        )
        created += 1
    return created


def export_csv(cursor):
    """Dump the full, current action queue (unresolved items) to CSV -
    the literal reverse of extract.py reading a CSV in. Anything that
    consumes flat files (a CRM import, a spreadsheet, an email tool)
    can pick this up without ever touching Postgres."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    cursor.execute("""
        SELECT q.id, q.customer_id, c.name, c.city, q.action_type, q.message, q.created_at
        FROM customer_action_queue q
        JOIN customers c ON c.customer_id = q.customer_id
        WHERE q.resolved = FALSE
        ORDER BY q.created_at DESC
    """)
    rows = cursor.fetchall()

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "customer_id", "name", "city", "action_type", "message", "created_at"])
        writer.writerows(rows)

    print(f"[EXPORT] {len(rows)} open actions written to {OUTPUT_CSV}")
    return len(rows)


# ---------------------------------------------------------------------------
# Run audit log
# ---------------------------------------------------------------------------

def log_run_start(cursor):
    cursor.execute(
        "INSERT INTO reverse_pipeline_runs (started_at, status) VALUES (%s, 'running') RETURNING id",
        (datetime.now(timezone.utc),)
    )
    return cursor.fetchone()[0]


def log_run_end(cursor, run_id, status, evaluated=0, created=0, message=""):
    cursor.execute(
        """UPDATE reverse_pipeline_runs
           SET finished_at = %s, status = %s, actions_evaluated = %s,
               actions_created = %s, message = %s
           WHERE id = %s""",
        (datetime.now(timezone.utc), status, evaluated, created, message, run_id)
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_reverse_pipeline():
    print("\n[REVERSE] Starting reverse pipeline (customers -> action queue)...")
    connection = create_connection()
    cursor = connection.cursor()

    ensure_tables(cursor)
    connection.commit()

    run_id = log_run_start(cursor)
    connection.commit()

    try:
        candidates = find_action_candidates(cursor)
        created = push_actions(cursor, candidates)
        connection.commit()

        open_count = export_csv(cursor)
        connection.commit()

        log_run_end(cursor, run_id, "success", evaluated=len(candidates), created=created)
        connection.commit()

        print(f"[REVERSE] {len(candidates)} candidates evaluated, {created} new actions queued, "
              f"{open_count} total open actions.")

    except Exception as exc:
        connection.rollback()
        log_run_end(cursor, run_id, "failed", message=str(exc))
        connection.commit()
        print(f"[REVERSE] FAILED: {exc}")
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    run_reverse_pipeline()
