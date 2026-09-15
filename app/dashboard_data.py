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


def build_event_summary_context(df):
    if df.empty:
        return None

    event_counts = (
        df["event_name"]
        .value_counts()
        .to_dict()
    )

    user_counts = (
        df["user_id"]
        .value_counts()
        .to_dict()
    )

    return {
        "total_events": len(df),
        "unique_users": df["user_id"].nunique(),
        "event_types": df["event_name"].nunique(),
        "event_counts": event_counts,
        "events_per_user": user_counts,
        "first_event_time": str(
            df["event_timestamp"].min()
        ),
        "last_event_time": str(
            df["event_timestamp"].max()
        ),
    }


def build_event_qa_context(df):
    if df.empty:
        return None

    working_df = df.copy()

    working_df["event_date"] = (
        working_df["event_timestamp"]
        .dt.date
    )

    event_counts = (
        working_df["event_name"]
        .value_counts()
        .to_dict()
    )

    events_per_user = (
        working_df["user_id"]
        .value_counts()
        .to_dict()
    )

    daily_activity = (
        working_df.groupby("event_date")
        .size()
        .to_dict()
    )

    non_null_values = (
        working_df["value"]
        .dropna()
    )

    value_summary = {
        "count": int(non_null_values.count()),
        "sum": float(non_null_values.sum()),
        "average": (
            float(non_null_values.mean())
            if not non_null_values.empty
            else None
        ),
    }

    return {
        "total_events": len(working_df),
        "unique_users": (
            working_df["user_id"].nunique()
        ),
        "event_types": (
            working_df["event_name"]
            .dropna()
            .unique()
            .tolist()
        ),
        "event_counts": event_counts,
        "events_per_user": events_per_user,
        "daily_activity": {
            str(date): count
            for date, count
            in daily_activity.items()
        },
        "first_event_time": str(
            working_df["event_timestamp"].min()
        ),
        "last_event_time": str(
            working_df["event_timestamp"].max()
        ),
        "value_summary": value_summary,
    }