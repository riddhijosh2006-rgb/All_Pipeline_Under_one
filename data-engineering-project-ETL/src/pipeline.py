from src.extract import extract_data
from src.transform import transform_data
from src.validation import validate_data
from src.load import create_table, load_data
from src.logger import logger


def run_pipeline():

    print("\n========== DATA PIPELINE STARTED ==========")
    logger.info("Pipeline started")

    # --------------------------------
    # EXTRACT
    # --------------------------------

    print("\nSTEP 1: EXTRACT")
    logger.info("Starting extraction")

    df = extract_data()

    if df is None:
        logger.error("Pipeline failed during extraction")
        print("\nPIPELINE FAILED during EXTRACT.")
        return

    logger.info(
        f"Extraction successful - {len(df)} records extracted"
    )

    # --------------------------------
    # TRANSFORM
    # --------------------------------

    print("\nSTEP 2: TRANSFORM")
    logger.info("Starting transformation")

    clean_df = transform_data(df)

    if clean_df is None:
        logger.error("Pipeline failed during transformation")
        print("\nPIPELINE FAILED during TRANSFORM.")
        return

    logger.info(
        f"Transformation successful - {len(clean_df)} records ready"
    )

    # --------------------------------
    # VALIDATE
    # --------------------------------

    print("\nSTEP 3: VALIDATE")

    validation_result = validate_data(clean_df)

    if not validation_result:

        logger.error("Pipeline stopped because validation failed")

        print("\nPIPELINE STOPPED: DATA VALIDATION FAILED.")

        return

    # --------------------------------
    # LOAD
    # --------------------------------

    print("\nSTEP 4: LOAD")
    logger.info("Starting database load")

    try:

        create_table()
        load_data(clean_df)

        logger.info(
            f"Load successful - "
            f"{len(clean_df)} records loaded into PostgreSQL"
        )

    except Exception as e:

        logger.error(
            f"Pipeline failed during load: {e}"
        )

        print(
            f"\nPIPELINE FAILED during LOAD: {e}"
        )

        return

    # --------------------------------
    # COMPLETE
    # --------------------------------

    logger.info("Pipeline completed successfully")

    print(
        "\n========== DATA PIPELINE COMPLETED =========="
    )


if __name__ == "__main__":
    run_pipeline()