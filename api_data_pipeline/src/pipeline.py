from src.extract import extract_data
from src.transform import transform_data
from src.load import create_table, load_data


def run_pipeline():

    print("\n========== API DATA PIPELINE ==========")

    # STEP 1
    print("\nSTEP 1: EXTRACT")
    data = extract_data()

    # STEP 2
    print("\nSTEP 2: TRANSFORM")
    df = transform_data(data)

    print("\nTransformed Data:")
    print(df)

    # STEP 3
    print("\nSTEP 3: LOAD")

    create_table()

    load_data(df)

    print("\n========== PIPELINE COMPLETED ==========")


if __name__ == "__main__":
    run_pipeline()