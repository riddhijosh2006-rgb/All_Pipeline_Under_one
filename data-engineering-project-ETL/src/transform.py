def transform_data(df):

    try:

        print("Starting data transformation...")

        # 1. Remove duplicate records
        df = df.drop_duplicates()

        # 2. Handle missing values
        df["name"] = df["name"].fillna("Unknown")
        df["city"] = df["city"].fillna("Unknown")
        df["age"] = df["age"].fillna(df["age"].median())
        df["purchase_amount"] = df["purchase_amount"].fillna(0)

        # 3. Clean city names
        df["city"] = df["city"].str.strip().str.title()

        # 4. Make sure age is an integer
        df["age"] = df["age"].astype(int)

        # 5. Create purchase category
        df["purchase_category"] = df["purchase_amount"].apply(
            lambda x: "High" if x >= 5000 else "Low"
        )

        print("Transformation completed!")

        return df

    except Exception as e:

        print(f"ERROR during transformation: {e}")
        return None