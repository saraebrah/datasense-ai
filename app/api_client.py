import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

REQUEST_TIMEOUT_SECONDS = 10


def geocode_city(city):
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    response = requests.get(
        GEOCODING_URL,
        params=params,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    response.raise_for_status()

    data = response.json()

    results = data.get("results", [])

    if not results:
        raise ValueError(f"No location found for: {city}")

    return results[0]


def fetch_weather_forecast(latitude, longitude, forecast_days=3):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation",
        "forecast_days": forecast_days,
        "timezone": "GMT",
    }

    response = requests.get(
        FORECAST_URL,
        params=params,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    response.raise_for_status()

    return response.json()