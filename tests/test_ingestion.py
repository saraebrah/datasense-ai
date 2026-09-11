import pandas as pd

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