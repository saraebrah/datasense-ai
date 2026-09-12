import pandas as pd
import pytest

from app.ingestion import validate_events_dataframe


def test_valid_events_dataframe_passes_validation():
    df = pd.DataFrame(
        {
            "event_id": ["evt_001"],
            "user_id": ["user_001"],
            "event_name": ["login"],
            "event_timestamp": [
                "2026-08-01T09:00:00"
            ],
            "value": [None],
        }
    )

    validate_events_dataframe(df)


def test_missing_required_column_raises_error():
    df = pd.DataFrame(
        {
            "event_id": ["evt_001"],
            "user_id": ["user_001"],
            "event_name": ["login"],
        }
    )

    with pytest.raises(
        ValueError,
        match="missing required columns",
    ):
        validate_events_dataframe(df)


def test_empty_dataframe_raises_error():
    df = pd.DataFrame(
        columns=[
            "event_id",
            "user_id",
            "event_name",
            "event_timestamp",
            "value",
        ]
    )

    with pytest.raises(
        ValueError,
        match="contains no data rows",
    ):
        validate_events_dataframe(df)


def test_missing_event_id_raises_error():
    df = pd.DataFrame(
        {
            "event_id": [None],
            "user_id": ["user_001"],
            "event_name": ["login"],
            "event_timestamp": [
                "2026-08-01T09:00:00"
            ],
            "value": [None],
        }
    )

    with pytest.raises(
        ValueError,
        match="missing values",
    ):
        validate_events_dataframe(df)


def test_duplicate_event_ids_raise_error():
    df = pd.DataFrame(
        {
            "event_id": [
                "evt_001",
                "evt_001",
            ],
            "user_id": [
                "user_001",
                "user_002",
            ],
            "event_name": [
                "login",
                "signup",
            ],
            "event_timestamp": [
                "2026-08-01T09:00:00",
                "2026-08-01T10:00:00",
            ],
            "value": [
                None,
                None,
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="duplicate event_id",
    ):
        validate_events_dataframe(df)