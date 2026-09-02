import requests


API_URL = "https://api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": 23.0225,
    "longitude": 72.5714,
    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    "forecast_days": 1,
    "timezone": "Asia/Kolkata"
}


def extract_data():
    print("Connecting to Weather API...")

    response = requests.get(
        API_URL,
        params=PARAMS,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    print("API connection successful!")
    return data


if __name__ == "__main__":
    data = extract_data()

    print("\nAvailable data:")
    print(data.keys())

    print("\nHourly data:")
    print(data["hourly"].keys())