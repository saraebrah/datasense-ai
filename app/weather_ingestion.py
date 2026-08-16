from datetime import datetime

from api_client import (
    fetch_weather_forecast,
    geocode_city,
)
from repository import (
    count_weather_forecasts,
    create_weather_forecasts_table,
    get_latest_weather_forecasts,
    upsert_weather_forecasts,
)


def weather_response_to_records(location, weather_data):
    hourly = weather_data["hourly"]

    records = []

    for (
        forecast_time,
        temperature,
        precipitation,
    ) in zip(
        hourly["time"],
        hourly["temperature_2m"],
        hourly["precipitation"],
    ):
        records.append(
            (
                location["id"],
                location["name"],
                location.get("country"),
                location["latitude"],
                location["longitude"],
                datetime.fromisoformat(forecast_time),
                temperature,
                precipitation,
            )
        )

    return records


def ingest_weather(city):
    location = geocode_city(city)

    print(
        f"Location found: "
        f"{location['name']}, "
        f"{location.get('country', 'Unknown')}\n"
    )

    weather_data = fetch_weather_forecast(
        location["latitude"],
        location["longitude"],
        forecast_days=3,
    )

    records = weather_response_to_records(
        location,
        weather_data,
    )

    print("Weather API request successful.")
    print(f"{len(records)} hourly forecasts received.\n")

    create_weather_forecasts_table()
    upsert_weather_forecasts(records)

    print("Weather ingestion complete.")
    print(
        "Total weather forecasts in database: "
        f"{count_weather_forecasts()}\n"
    )

    print("Latest forecasts:")

    for forecast in get_latest_weather_forecasts():
        print(forecast)


if __name__ == "__main__":
    ingest_weather("Toronto, Canada")