from pathlib import Path

import pandas as pd

from repository import (
    count_events,
    create_events_table,
    get_latest_product_events,
    insert_events,
)


REQUIRED_COLUMNS = {
    "event_id",
    "user_id",
    "event_name",
    "event_timestamp",
    "value",
}



def validate_events_dataframe(df):
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"CSV is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    if df.empty:
        raise ValueError(
            "CSV contains no data rows."
        )

    required_non_null_columns = [
        "event_id",
        "user_id",
        "event_name",
        "event_timestamp",
    ]

    null_columns = [
        column
        for column in required_non_null_columns
        if df[column].isna().any()
    ]

    if null_columns:
        raise ValueError(
            "Required columns contain missing values: "
            f"{null_columns}"
        )


    duplicate_event_ids = (
        df["event_id"]
        .duplicated()
        .any()
    )

    if duplicate_event_ids:
        raise ValueError(
            "CSV contains duplicate event_id values."
        )


def load_csv(file_source):
    df = pd.read_csv(file_source)

    validate_events_dataframe(df)

    df["event_timestamp"] = pd.to_datetime(
        df["event_timestamp"],
        errors="raise",
    )

    return df


def dataframe_to_records(df):
    records = []

    for row in df.itertuples(index=False):
        value = None if pd.isna(row.value) else float(row.value)

        records.append(
            (
                row.event_id,
                row.user_id,
                row.event_name,
                row.event_timestamp.to_pydatetime(),
                value,
            )
        )

    return records

def ingest_events_dataframe(df):
    validate_events_dataframe(df)

    df = df.copy()

    df["event_timestamp"] = pd.to_datetime(
        df["event_timestamp"],
        errors="raise",
    )

    records = dataframe_to_records(df)

    create_events_table()
    insert_events(records)

    return len(records)


def ingest_csv(file_path):
    df = load_csv(file_path)

    print("CSV loaded successfully.")
    print(f"{len(df)} rows found.\n")

    processed_rows = ingest_events_dataframe(df)

    print("Data ingestion complete.")
    print(f"{processed_rows} rows processed.")
    print(
        f"Total events in database: "
        f"{count_events()}\n"
    )

    print("Latest events:")

    for event in get_latest_product_events():
        print(event)


if __name__ == "__main__":
    sample_file = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "samples"
        / "product_events.csv"
    )

    ingest_csv(sample_file)

