from src.extract import extract_data
from src.transform import transform_data
from src.validate import validate_data
from src.load import create_table, load_data
from src.logger import logger


def run_pipeline():

    logger.info("========================================")
    logger.info("API DATA PIPELINE STARTED")
    logger.info("========================================")


    try:

        # ======================================
        # STEP 1: EXTRACT
        # ======================================

        logger.info("STEP 1: EXTRACT")

        data = extract_data()

        logger.info(
            "Extract step completed successfully!"
        )


        # ======================================
        # STEP 2: TRANSFORM
        # ======================================

        logger.info("STEP 2: TRANSFORM")

        df = transform_data(data)

        logger.info(
            "Transform step completed successfully!"
        )

        logger.info("Transformed Data:")
        logger.info("\n%s", df)

        logger.info("Data Types:")
        logger.info("\n%s", df.dtypes)


        # ======================================
        # STEP 3: DATA QUALITY
        # ======================================

        logger.info("STEP 3: DATA QUALITY VALIDATION")

        validate_data(df)

        logger.info(
            "Data quality validation completed successfully!"
        )


        # ======================================
        # STEP 4: LOAD
        # ======================================

        logger.info("STEP 4: LOAD")

        create_table()

        load_data(df)

        logger.info(
            "Load step completed successfully!"
        )


        # ======================================
        # PIPELINE COMPLETED
        # ======================================

        logger.info("========================================")
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("========================================")


    except Exception as e:

        logger.exception(
            f"PIPELINE FAILED: {e}"
        )

        raise


if __name__ == "__main__":
    run_pipeline()