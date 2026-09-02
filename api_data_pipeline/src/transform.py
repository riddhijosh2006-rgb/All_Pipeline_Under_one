import pandas as pd


def transform_data(data):

    print("Starting transformation...")

    hourly_data = data["hourly"]

    df = pd.DataFrame({
        "timestamp": hourly_data["time"],
        "temperature_c": hourly_data["temperature_2m"],
        "humidity_pct": hourly_data["relative_humidity_2m"],
        "wind_speed_kmh": hourly_data["wind_speed_10m"]
    })

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df["city"] = "Ahmedabad"

    print("Transformation completed!")

    return df


if __name__ == "__main__":
    print("Transform module ready!")