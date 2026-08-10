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


def load_csv(file_path):
    df = pd.read_csv(file_path)

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"CSV is missing required columns: {sorted(missing_columns)}"
        )

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


def ingest_csv(file_path):
    df = load_csv(file_path)

    print("CSV loaded successfully.")
    print(f"{len(df)} rows found.\n")

    records = dataframe_to_records(df)

    create_events_table()
    insert_events(records)

    print("Data ingestion complete.")
    print(f"Total events in database: {count_events()}\n")

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