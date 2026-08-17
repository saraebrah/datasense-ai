import pandas as pd

from repository import (
    get_all_events,
    get_all_weather_forecasts,
)


EVENT_COLUMNS = [
    "event_id",
    "user_id",
    "event_name",
    "event_timestamp",
    "value",
]


WEATHER_COLUMNS = [
    "location_name",
    "country",
    "forecast_time",
    "temperature_c",
    "precipitation_mm",
    "retrieved_at",
]


def load_events_dataframe():
    rows = get_all_events()

    return pd.DataFrame(
        rows,
        columns=EVENT_COLUMNS,
    )


def load_weather_dataframe():
    rows = get_all_weather_forecasts()

    return pd.DataFrame(
        rows,
        columns=WEATHER_COLUMNS,
    )


def get_event_counts_by_type(df):
    return (
        df.groupby("event_name")
        .size()
        .reset_index(name="event_count")
        .sort_values(
            "event_count",
            ascending=False,
        )
    )


def get_daily_event_activity(df):
    daily_df = df.copy()

    daily_df["event_date"] = (
        daily_df["event_timestamp"]
        .dt.date
    )

    return (
        daily_df.groupby("event_date")
        .size()
        .reset_index(name="event_count")
        .sort_values("event_date")
    )