from src.logger import logger


def validate_data(df):

    logger.info("Starting data validation")

    # --------------------------------
    # 1. Check required columns
    # --------------------------------

    required_columns = [
        "customer_id",
        "name",
        "age",
        "city",
        "purchase_amount",
        "purchase_category"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        logger.error(
            f"Missing required columns: {missing_columns}"
        )

        print(
            f"Validation failed: Missing columns {missing_columns}"
        )

        return False


    # --------------------------------
    # 2. Check duplicate customer IDs
    # --------------------------------

    duplicate_ids = df[
        df["customer_id"].duplicated()
    ]

    if not duplicate_ids.empty:

        logger.error(
            f"Duplicate customer IDs found: "
            f"{duplicate_ids['customer_id'].tolist()}"
        )

        print("Validation failed: Duplicate customer IDs found.")

        return False


    # --------------------------------
    # 3. Check invalid ages
    # --------------------------------

    invalid_age = df[
        (df["age"] < 0) |
        (df["age"] > 120)
    ]

    if not invalid_age.empty:

        logger.error(
            f"Invalid ages found: "
            f"{invalid_age['age'].tolist()}"
        )

        print("Validation failed: Invalid age found.")

        return False


    # --------------------------------
    # 4. Check invalid purchase amounts
    # --------------------------------

    invalid_purchase = df[
        df["purchase_amount"] < 0
    ]

    if not invalid_purchase.empty:

        logger.error(
            f"Invalid purchase amounts found: "
            f"{invalid_purchase['purchase_amount'].tolist()}"
        )

        print(
            "Validation failed: Negative purchase amount found."
        )

        return False


    # --------------------------------
    # 5. Check missing important values
    # --------------------------------

    important_columns = [
        "customer_id",
        "name",
        "city"
    ]

    for column in important_columns:

        if df[column].isnull().any():

            logger.error(
                f"Missing values found in {column}"
            )

            print(
                f"Validation failed: Missing values in {column}"
            )

            return False


    # --------------------------------
    # Validation successful
    # --------------------------------

    logger.info(
        f"Data validation successful - "
        f"{len(df)} records validated"
    )

    print(
        f"Data validation successful - "
        f"{len(df)} records validated"
    )

    return True