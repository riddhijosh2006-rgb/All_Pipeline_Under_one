from src.extract_load import create_raw_table, extract_raw, load_raw
from src.transform_sql import run_transform
from src.validation import validate_data
from src.reverse_pipeline import run_reverse_pipeline
from src.logger import logger


def run_pipeline():

    print("\n========== ELT PIPELINE STARTED ==========")
    logger.info("Pipeline started")

    # --------------------------------
    # EXTRACT + LOAD (raw, untouched)
    # --------------------------------

    print("\nSTEP 1: EXTRACT + LOAD (raw)")
    logger.info("Starting raw extract + load")

    create_raw_table()
    df = extract_raw()

    if df is None:
        logger.error("Pipeline failed during extraction")
        print("\nPIPELINE FAILED during EXTRACT.")
        return

    load_raw(df)
    logger.info(f"Raw load successful - {len(df)} records loaded into raw_customers")

    # --------------------------------
    # TRANSFORM (inside Postgres)
    # --------------------------------

    print("\nSTEP 2: TRANSFORM (inside PostgreSQL)")
    logger.info("Starting SQL transform")

    try:
        run_transform()
        logger.info("Transformation successful")
    except Exception as e:
        logger.error(f"Pipeline failed during transform: {e}")
        print(f"\nPIPELINE FAILED during TRANSFORM: {e}")
        return

    # --------------------------------
    # VALIDATE
    # --------------------------------

    print("\nSTEP 3: VALIDATE")

    if not validate_data():
        logger.error("Pipeline stopped because validation failed")
        print("\nPIPELINE STOPPED: DATA VALIDATION FAILED.")
        return

    # --------------------------------
    # REVERSE (customers -> action queue, back out to Postgres + CSV)
    # --------------------------------

    print("\nSTEP 4: REVERSE PIPELINE (push insights back out)")
    logger.info("Starting reverse pipeline")

    try:
        run_reverse_pipeline()
        logger.info("Reverse pipeline successful")
    except Exception as e:
        logger.error(f"Reverse pipeline failed: {e}")
        print(f"\nPIPELINE WARNING: reverse pipeline failed: {e}")
        # Not a hard stop - forward ELT already succeeded and customers
        # table is valid, reverse pipeline is an add-on, not load-bearing.

    # --------------------------------
    # COMPLETE
    # --------------------------------

    logger.info("Pipeline completed successfully")
    print("\n========== ELT PIPELINE COMPLETED ==========")


if __name__ == "__main__":
    run_pipeline()
