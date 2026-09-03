import requests

from src.logger import logger


CITIES = {
    "Ahmedabad": {
        "latitude": 23.0225,
        "longitude": 72.5714
    },
    "Mumbai": {
        "latitude": 19.0760,
        "longitude": 72.8777
    },
    "Delhi": {
        "latitude": 28.6139,
        "longitude": 77.2090
    },
    "Bangalore": {
        "latitude": 12.9716,
        "longitude": 77.5946
    },
    "Pune": {
        "latitude": 18.5204,
        "longitude": 73.8567
    },
    "Hyderabad": {
        "latitude": 17.3850,
        "longitude": 78.4867
    },
    "Chennai": {
        "latitude": 13.0827,
        "longitude": 80.2707
    },
    "Kolkata": {
        "latitude": 22.5726,
        "longitude": 88.3639
    }
}


def extract_data():

    logger.info("Starting weather data extraction for all cities...")

    all_city_data = {}

    for city, coordinates in CITIES.items():

        logger.info(f"Extracting weather data for {city}...")

        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": coordinates["latitude"],
            "longitude": coordinates["longitude"],
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "wind_speed_10m"
            ],
            "forecast_days": 1,
            "timezone": "Asia/Kolkata"
        }

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        all_city_data[city] = response.json()

        logger.info(f"Weather data extracted successfully for {city}.")

    logger.info("Weather data extraction completed for all cities.")

    return all_city_data


if __name__ == "__main__":
    extract_data()