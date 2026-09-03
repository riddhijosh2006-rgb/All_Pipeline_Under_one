import pandas as pd

from src.logger import logger


def validate_data(df):

    logger.info("Starting data quality validation...")

    try:

        # ==========================================
        # CHECK 1: DataFrame should not be empty
        # ==========================================

        if df.empty:
            raise ValueError(
                "Data quality check failed: DataFrame is empty."
            )

        logger.info("CHECK 1 PASSED: DataFrame is not empty.")


        # ==========================================
        # CHECK 2: Required columns
        # ==========================================

        required_columns = [
            "timestamp",
            "temperature_c",
            "humidity_pct",
            "wind_speed_kmh",
            "city"
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:

            raise ValueError(
                f"Data quality check failed: "
                f"Missing columns: {missing_columns}"
            )

        logger.info(
            "CHECK 2 PASSED: All required columns exist."
        )


        # ==========================================
        # CHECK 3: NULL values
        # ==========================================

        null_counts = df[required_columns].isnull().sum()

        total_nulls = null_counts.sum()

        if total_nulls > 0:

            logger.error(
                f"NULL values found:\n{null_counts}"
            )

            raise ValueError(
                "Data quality check failed: NULL values detected."
            )

        logger.info(
            "CHECK 3 PASSED: No NULL values found."
        )


        # ==========================================
        # CHECK 4: Duplicate records
        # ==========================================

        duplicate_count = df.duplicated(
            subset=["timestamp", "city"]
        ).sum()

        if duplicate_count > 0:

            raise ValueError(
                f"Data quality check failed: "
                f"{duplicate_count} duplicate records found."
            )

        logger.info(
            "CHECK 4 PASSED: No duplicate records found."
        )


        # ==========================================
        # CHECK 5: Humidity range
        # ==========================================

        invalid_humidity = df[
            (df["humidity_pct"] < 0) |
            (df["humidity_pct"] > 100)
        ]

        if not invalid_humidity.empty:

            raise ValueError(
                "Data quality check failed: "
                "Humidity must be between 0 and 100."
            )

        logger.info(
            "CHECK 5 PASSED: Humidity values are valid."
        )


        # ==========================================
        # CHECK 6: Wind speed
        # ==========================================

        invalid_wind = df[
            df["wind_speed_kmh"] < 0
        ]

        if not invalid_wind.empty:

            raise ValueError(
                "Data quality check failed: "
                "Wind speed cannot be negative."
            )

        logger.info(
            "CHECK 6 PASSED: Wind speed values are valid."
        )


        # ==========================================
        # CHECK 7: Temperature
        # ==========================================

        invalid_temperature = df[
            (df["temperature_c"] < -90) |
            (df["temperature_c"] > 60)
        ]

        if not invalid_temperature.empty:

            raise ValueError(
                "Data quality check failed: "
                "Temperature value is outside the "
                "expected range (-90°C to 60°C)."
            )

        logger.info(
            "CHECK 7 PASSED: Temperature values are valid."
        )


        # ==========================================
        # CHECK 8: Timestamp
        # ==========================================

        if not pd.api.types.is_datetime64_any_dtype(
            df["timestamp"]
        ):

            raise ValueError(
                "Data quality check failed: "
                "Timestamp column is not datetime."
            )

        logger.info(
            "CHECK 8 PASSED: Timestamp values are valid."
        )


        # ==========================================
        # ALL CHECKS PASSED
        # ==========================================

        logger.info(
            "========================================"
        )

        logger.info(
            "DATA QUALITY VALIDATION PASSED"
        )

        logger.info(
            f"Validated {len(df)} records successfully."
        )

        logger.info(
            "========================================"
        )

        return True


    except Exception as e:

        logger.exception(
            f"Data quality validation failed: {e}"
        )

        raise


if __name__ == "__main__":
    logger.info("Data validation module ready.")