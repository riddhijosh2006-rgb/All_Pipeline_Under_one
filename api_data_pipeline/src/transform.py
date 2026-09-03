import pandas as pd

from src.logger import logger


def transform_data(data):

    logger.info("Starting transformation...")

    try:

        all_dataframes = []

        for city, city_data in data.items():

            logger.info(f"Transforming data for {city}...")

            if "hourly" not in city_data:
                raise KeyError(
                    f"Hourly weather data is missing for {city}."
                )

            hourly_data = city_data["hourly"]

            required_columns = [
                "time",
                "temperature_2m",
                "relative_humidity_2m",
                "wind_speed_10m"
            ]

            for column in required_columns:

                if column not in hourly_data:
                    raise KeyError(
                        f"Required column missing for {city}: {column}"
                    )

            city_df = pd.DataFrame({
                "timestamp": hourly_data["time"],
                "temperature_c": hourly_data["temperature_2m"],
                "humidity_pct": hourly_data["relative_humidity_2m"],
                "wind_speed_kmh": hourly_data["wind_speed_10m"]
            })

            city_df["timestamp"] = pd.to_datetime(
                city_df["timestamp"]
            )

            city_df["city"] = city

            all_dataframes.append(city_df)

        df = pd.concat(
            all_dataframes,
            ignore_index=True
        )

        if df.empty:
            raise ValueError(
                "Transformation produced an empty DataFrame."
            )

        logger.info("Transformation completed!")
        logger.info(
            f"Transformed {len(df)} records from "
            f"{df['city'].nunique()} cities."
        )

        return df

    except Exception as e:

        logger.exception(
            f"Transformation failed: {e}"
        )

        raise


if __name__ == "__main__":
    logger.info("Transform module ready.")