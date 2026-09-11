from src.extract_load import create_raw_table, extract_raw, load_raw
from src.transform_sql import run_transform
from src.validation import validate_data
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
    # COMPLETE
    # --------------------------------

    logger.info("Pipeline completed successfully")
    print("\n========== ELT PIPELINE COMPLETED ==========")


if __name__ == "__main__":
    run_pipeline()
