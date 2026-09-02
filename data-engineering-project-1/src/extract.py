import pandas as pd


def extract_data():

    try:
        file_path = "data/customers.csv"

        df = pd.read_csv(file_path)

        print("Data extracted successfully!")

        print("\nFirst 5 rows:")
        print(df.head())

        print("\nDataset shape:")
        print(df.shape)

        print("\nColumns:")
        print(df.columns)

        return df

    except FileNotFoundError:
        print("ERROR: customers.csv file was not found.")
        return None

    except Exception as e:
        print(f"ERROR during extraction: {e}")
        return None